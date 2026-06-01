#!/usr/bin/env python3
"""Faithful recompute of the H3 VIX-regime table at G=488 to fix the n=495 bug.

The published Table (tab:vix_regime) lists "n firms = 495" for all three VIX
regimes against a 488-firm panel, which is impossible (n is a firm count).
The mean/median/std came from the real frozen run; only n is anomalous.

This reproduces the H3 sub-analysis directly (rolling dual-Hurst per firm ->
per-firm within-regime Pearson coupling -> cross-firm distribution per regime),
matching the methodology in src/fractal_pv/regimes.py + rolling.py. It does NOT
run the full 6-8h inference pipeline; only the H3 table.

Validation gate: if the recomputed mean/median/std per regime match the
published values (0.567/0.666/0.344 low; 0.497/0.566/0.299 medium;
0.563/0.738/0.450 high) within rounding, the pipeline is faithful and the
recomputed n (and Mann-Whitney U) can be trusted to fix the table. If they
diverge materially, we report the divergence and DO NOT overwrite the table.

Window end = 2026-04-15 to match the paper's frozen snapshot.
Outputs: research/h3_recompute/{vix_regime_recompute.json, RESULT.md}
"""
import json, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from fractal_pv.stationarity import prepare_series      # noqa: E402
from fractal_pv.rolling import rolling_dual_hurst        # noqa: E402
from fractal_pv.regimes import classify_vix_regime       # noqa: E402

OUT = ROOT / "research" / "h3_recompute"
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
END = "2026-04-15"
W, STEP, MIN_OBS = 500, 20, 500
PUBLISHED = {  # mean, median, std from tab:vix_regime
    "low":    (0.567, 0.666, 0.344),
    "medium": (0.497, 0.566, 0.299),
    "high":   (0.563, 0.738, 0.450),
}


def load_universe():
    import yfinance as yf
    csv = ROOT / "data" / "sp500_constituents_2026-04-28.csv"
    tickers = pd.read_csv(csv)["Symbol"].str.replace(".", "-", regex=False).tolist()
    print(f"universe: {len(tickers)} candidate tickers")
    data = {}
    # batch download in chunks (faster + fewer rate-limit hits), cache per ticker
    CHUNK = 40
    for i in range(0, len(tickers), CHUNK):
        chunk = tickers[i:i + CHUNK]
        need = [t for t in chunk if not (RAW / f"{t}_1d_2015-01-01_{END}.parquet").exists()]
        if need:
            try:
                df = yf.download(need, start="2015-01-01", end=END, progress=False,
                                 group_by="ticker", auto_adjust=False, threads=True)
                for t in need:
                    try:
                        sub = df[t] if isinstance(df.columns, pd.MultiIndex) else df
                        sub = sub.dropna(how="all")
                        if len(sub) >= MIN_OBS:
                            sub.to_parquet(RAW / f"{t}_1d_2015-01-01_{END}.parquet")
                    except Exception:
                        pass
            except Exception as e:
                print(f"  chunk {i} fetch error: {str(e)[:80]}")
        print(f"  fetched through {i+CHUNK}/{len(tickers)}", flush=True)
    # retry any ticker still uncached, one at a time (batch group_by can drop some)
    missing = [t for t in tickers if not (RAW / f"{t}_1d_2015-01-01_{END}.parquet").exists()]
    for t in missing:
        try:
            df = yf.download(t, start="2015-01-01", end=END, progress=False, auto_adjust=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df.dropna(how="all")
            if len(df) >= MIN_OBS:
                df.to_parquet(RAW / f"{t}_1d_2015-01-01_{END}.parquet")
        except Exception:
            pass
    print(f"  retried {len(missing)} previously-failed tickers", flush=True)
    # load all cached
    for t in tickers:
        p = RAW / f"{t}_1d_2015-01-01_{END}.parquet"
        if p.exists():
            df = pd.read_parquet(p)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df[["Close", "Volume"]].dropna()
            if len(df) >= MIN_OBS:
                data[t] = df
    print(f"loaded {len(data)} firms with >= {MIN_OBS} obs")
    return data


def main():
    import yfinance as yf
    data = load_universe()
    # VIX + regime classification on the full daily VIX series
    vix = yf.download("^VIX", start="2015-01-01", end=END, progress=False, auto_adjust=False)
    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)
    vix = vix["Close"].dropna()
    vix.index = pd.to_datetime(vix.index)
    regime = classify_vix_regime(vix)            # low/medium/high by 25/75 pctile
    regdf = regime.reset_index()
    regdf.columns = ["date", "regime"]
    regdf["date"] = pd.to_datetime(regdf["date"]).dt.tz_localize(None).astype("datetime64[ns]")
    regdf = regdf.sort_values("date")

    # per-firm within-regime coupling
    per_firm = {"low": [], "medium": [], "high": []}
    nfirm = 0
    for tk, df in data.items():
        ser = prepare_series(df)
        dates = df.index[1:][: len(ser["abs_log_returns"])]
        dual = rolling_dual_hurst(ser["abs_log_returns"], ser["log_volume"],
                                  dates.values, window=W, step=STEP)
        if dual.empty:
            continue
        d = dual.dropna(subset=["H_price", "H_volume"]).copy()
        d["date"] = pd.to_datetime(d["date"]).dt.tz_localize(None).astype("datetime64[ns]")
        # assign each rolling date its VIX regime via merge_asof nearest (matches align_regime_with_rolling)
        d = pd.merge_asof(d.sort_values("date"), regdf, on="date", direction="nearest")
        nfirm += 1
        for rg in ("low", "medium", "high"):
            sub = d[d["regime"] == rg]
            if len(sub) >= 10:
                r, _ = stats.pearsonr(sub["H_price"], sub["H_volume"])
                if np.isfinite(r):
                    per_firm[rg].append(float(r))
    print(f"firms with rolling coupling: {nfirm}")

    rows, recomputed = {}, {}
    for rg in ("low", "medium", "high"):
        arr = np.array(per_firm[rg])
        rows[rg] = {"mean": float(arr.mean()), "median": float(np.median(arr)),
                    "std": float(arr.std(ddof=1)), "n_firms": int(len(arr))}
        recomputed[rg] = rows[rg]
        print(f"  {rg:7}: mean={rows[rg]['mean']:.3f} median={rows[rg]['median']:.3f} "
              f"std={rows[rg]['std']:.3f} n={rows[rg]['n_firms']}")

    # Mann-Whitney high > low on the per-firm distributions
    U, p = stats.mannwhitneyu(per_firm["high"], per_firm["low"], alternative="greater")
    print(f"Mann-Whitney high>low: U={U:.0f}, p={p:.4f}  (published U=135542, p=0.0019)")

    # validation gate: do mean/median/std match published within tolerance?
    matches = {}
    for rg, (m, md, sd) in PUBLISHED.items():
        rc = recomputed[rg]
        ok = (abs(rc["mean"] - m) < 0.03 and abs(rc["median"] - md) < 0.03 and abs(rc["std"] - sd) < 0.05)
        matches[rg] = ok
    faithful = all(matches.values())

    result = {"recomputed": recomputed, "published": PUBLISHED,
              "mannwhitney": {"U": float(U), "p": float(p)},
              "n_firms_loaded": len(data), "faithful_match": faithful,
              "matches_per_regime": matches, "window_end": END}
    json.dump(result, open(OUT / "vix_regime_recompute.json", "w"), indent=2)

    L = ["# H3 VIX-regime recompute (G=488) — fixing the n=495 bug\n"]
    L.append(f"Universe loaded: {len(data)} firms (window 2015-01-01 to {END}).\n")
    L.append("| regime | published mean/med/std | recomputed mean/med/std | recomputed n | match |")
    L.append("|---|---|---|---|---|")
    for rg in ("low", "medium", "high"):
        m, md, sd = PUBLISHED[rg]; rc = recomputed[rg]
        L.append(f"| {rg} | {m}/{md}/{sd} | {rc['mean']:.3f}/{rc['median']:.3f}/{rc['std']:.3f} "
                 f"| {rc['n_firms']} | {'YES' if matches[rg] else 'NO'} |")
    L.append(f"\nMann-Whitney high>low: recomputed U={U:.0f}, p={p:.4f} (published U=135542, p=0.0019).")
    if faithful:
        L.append("\n**FAITHFUL: recompute reproduces the published mean/median/std within tolerance.** "
                 "The recomputed n values are trustworthy and replace the impossible 495. "
                 f"Corrected n: low={recomputed['low']['n_firms']}, "
                 f"medium={recomputed['medium']['n_firms']}, high={recomputed['high']['n_firms']}.")
    else:
        L.append("\n**NOT a faithful match** (data snapshot differs from the frozen run). "
                 "Do NOT overwrite the published mean/median/std. The recomputed n is indicative only; "
                 "the author should recompute n on the frozen panel. Divergence per regime: "
                 + ", ".join(f"{k}={'ok' if v else 'DIFF'}" for k, v in matches.items()) + ".")
    (OUT / "RESULT.md").write_text("\n".join(L))
    print("FAITHFUL" if faithful else "NOT-FAITHFUL", "-> wrote", OUT / "RESULT.md")


if __name__ == "__main__":
    main()
