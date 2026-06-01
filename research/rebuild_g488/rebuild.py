#!/usr/bin/env python3
"""Path 2: regenerate the full G~488 results from current data, reproducibly.

Removes the dependence on a lost frozen panel. Builds one cached panel from
live Yahoo Finance data and regenerates every core table from it, so the paper
is anchored to committed code + a live source rather than a vanished cache.

Tables regenerated (all from the SAME fresh snapshot, so internally consistent):
  - Hurst summary:   mean/std of full-sample H(returns), H(|r|), H(volume)
  - H1 (static):     cross-sectional Pearson r between full H(|r|) and H(volume)
  - H2 (temporal):   per-firm corr(rolling H_|r|, rolling H_vol); mean, % positive
  - H3 (regime):     per-firm within-VIX-regime coupling; mean/median/std/n + MWU
  - H4 (predictive): forward dollar-volume Amihud ~ CII + H controls, firm FE,
                     six SE methods + CR2/Satterthwaite + WCR bootstrap

Caches: research/rebuild_g488/data/{panel.parquet, full_hurst.parquet} so
re-runs (and table-only edits) are fast.
Outputs: research/rebuild_g488/{tables.json, RESULT.md}.

Window end = 2026-04-15 (keep the stated sample window; refresh is in the data
snapshot, not the period). Run: <venv>/python research/rebuild_g488/rebuild.py
"""
import json, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from fractal_pv.stationarity import prepare_series                 # noqa: E402
from fractal_pv.hurst import estimate_dfa                          # noqa: E402
from fractal_pv.rolling import rolling_dual_hurst                  # noqa: E402
from fractal_pv.predict import compute_coupling_intensity         # noqa: E402
from fractal_pv.regimes import classify_vix_regime                 # noqa: E402
from fractal_pv.inference_robust import robust_panel_regression    # noqa: E402

OUT = ROOT / "research" / "rebuild_g488"
DATA = OUT / "data"
RAW = ROOT / "data" / "raw"
DATA.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
END = "2026-04-15"
W, STEP, CORR_WIN, H, MIN_OBS = 500, 20, 30, 21, 500
NON = {"SPY", "^VIX", "VVIX", "HYG", "IEF", "LQD"}


def fetch_universe():
    import yfinance as yf
    csv = ROOT / "data" / "sp500_constituents_2026-04-28.csv"
    tickers = pd.read_csv(csv)["Symbol"].str.replace(".", "-", regex=False).tolist()
    CH = 40
    for i in range(0, len(tickers), CH):
        need = [t for t in tickers[i:i+CH] if not (RAW / f"{t}_1d_2015-01-01_{END}.parquet").exists()]
        if need:
            try:
                d = yf.download(need, start="2015-01-01", end=END, progress=False,
                                group_by="ticker", auto_adjust=False, threads=True)
                for t in need:
                    try:
                        s = (d[t] if isinstance(d.columns, pd.MultiIndex) else d).dropna(how="all")
                        if len(s) >= MIN_OBS:
                            s.to_parquet(RAW / f"{t}_1d_2015-01-01_{END}.parquet")
                    except Exception:
                        pass
            except Exception:
                pass
    for t in [t for t in tickers if not (RAW / f"{t}_1d_2015-01-01_{END}.parquet").exists()]:
        try:
            d = yf.download(t, start="2015-01-01", end=END, progress=False, auto_adjust=False)
            if isinstance(d.columns, pd.MultiIndex):
                d.columns = d.columns.get_level_values(0)
            d = d.dropna(how="all")
            if len(d) >= MIN_OBS:
                d.to_parquet(RAW / f"{t}_1d_2015-01-01_{END}.parquet")
        except Exception:
            pass
    data = {}
    for t in tickers:
        if t in NON:
            continue
        p = RAW / f"{t}_1d_2015-01-01_{END}.parquet"
        if p.exists():
            df = pd.read_parquet(p)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df[["Close", "Volume"]].dropna()
            if len(df) >= MIN_OBS:
                data[t] = df
    return data


def fwd_dollar_amihud(prices, volume, h):
    r = np.log(prices / prices.shift(1)).abs()
    dvol = (prices * volume).replace(0, np.nan)
    return (r / dvol).rolling(h).mean().shift(-h) * 1e6


def build_panel():
    pf, hf, dp = DATA / "panel.parquet", DATA / "full_hurst.parquet", DATA / "dual_panel.parquet"
    if pf.exists() and hf.exists() and dp.exists():
        print("[cache] panel + full_hurst + dual")
        return pd.read_parquet(pf), pd.read_parquet(hf), pd.read_parquet(dp)
    import yfinance as yf
    data = fetch_universe()
    print(f"universe: {len(data)} firms")
    vix = yf.download("^VIX", start="2015-01-01", end=END, progress=False, auto_adjust=False)
    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)
    vix = vix["Close"].dropna(); vix.index = pd.to_datetime(vix.index)
    regime = classify_vix_regime(vix)
    rd = regime.reset_index(); rd.columns = ["date", "regime"]
    rd["date"] = pd.to_datetime(rd["date"]).dt.tz_localize(None).astype("datetime64[ns]")
    rd = rd.sort_values("date")

    rows, fhur, dual_rows = [], [], []
    for tk, df in data.items():
        ser = prepare_series(df)
        # full-sample Hurst (H1 + summary)
        try:
            fhur.append({"ticker": tk,
                         "H_ret": estimate_dfa(ser["log_returns"]).H,
                         "H_absr": estimate_dfa(ser["abs_log_returns"]).H,
                         "H_vol": estimate_dfa(ser["log_volume"]).H})
        except Exception:
            pass
        dates = df.index[1:][: len(ser["abs_log_returns"])]
        dual = rolling_dual_hurst(ser["abs_log_returns"], ser["log_volume"], dates.values, window=W, step=STEP)
        if dual.empty:
            continue
        cii = compute_coupling_intensity(dual, correlation_window=CORR_WIN)
        d = dual.dropna(subset=["H_price", "H_volume"]).copy()
        d["date"] = pd.to_datetime(d["date"]).dt.tz_localize(None).astype("datetime64[ns]")
        d = pd.merge_asof(d.sort_values("date"), rd, on="date", direction="nearest")
        # full rolling series (all dates) for H2/H3 — NOT restricted to CII-available dates
        dual_rows.append(d.assign(ticker=tk)[["date", "H_price", "H_volume", "regime", "ticker"]])
        d = d.set_index("date")
        m = pd.DataFrame({"CII": cii}); m.index = pd.to_datetime(m.index)
        m = m.join(d[["H_price", "H_volume", "regime"]], how="inner")
        m["amihud_dollar"] = fwd_dollar_amihud(df["Close"], df["Volume"], H).reindex(m.index)
        m["ticker"] = tk
        rows.append(m.reset_index().rename(columns={"index": "date"}))
    panel = pd.concat(rows, ignore_index=True)
    if "date" not in panel.columns:
        panel = panel.rename(columns={panel.columns[0]: "date"})
    full_h = pd.DataFrame(fhur)
    dual_panel = pd.concat(dual_rows, ignore_index=True)
    panel.to_parquet(pf); full_h.to_parquet(hf); dual_panel.to_parquet(dp)
    print(f"[cache] wrote panel {panel.shape}, full_hurst {full_h.shape}, dual {dual_panel.shape}")
    return panel, full_h, dual_panel


def main():
    panel, fh, dual = build_panel()
    panel["date"] = pd.to_datetime(panel["date"])
    res = {"window_end": END, "n_firms_panel": int(panel["ticker"].nunique()),
           "n_firms_full_hurst": int(len(fh))}

    # Hurst summary
    res["hurst_summary"] = {c: {"mean": float(fh[c].mean()), "std": float(fh[c].std())}
                            for c in ["H_ret", "H_absr", "H_vol"]}

    # H1 static cross-sectional
    r1, p1 = stats.pearsonr(fh["H_absr"], fh["H_vol"])
    sr1, sp1 = stats.spearmanr(fh["H_absr"], fh["H_vol"])
    res["H1_static"] = {"pearson_r": float(r1), "pearson_p": float(p1),
                        "spearman_r": float(sr1), "spearman_p": float(sp1), "n": int(len(fh))}

    # H2 temporal: per-firm corr of rolling H_price, H_volume (FULL rolling series)
    temporal = []
    for tk, g in dual.groupby("ticker"):
        gg = g.dropna(subset=["H_price", "H_volume"])
        if len(gg) >= 10:
            rr, pp = stats.pearsonr(gg["H_price"], gg["H_volume"])
            temporal.append({"ticker": tk, "r": float(rr), "p": float(pp)})
    td = pd.DataFrame(temporal)
    res["H2_temporal"] = {"mean_r": float(td["r"].mean()), "median_r": float(td["r"].median()),
                          "pct_positive": float((td["r"] > 0).mean() * 100),
                          "pct_pos_sig": float(((td["r"] > 0) & (td["p"] < 0.05)).mean() * 100),
                          "n_firms": int(len(td))}

    # H3 regime: per-firm within-regime coupling (FULL rolling series, not CII-restricted)
    per = {"low": [], "medium": [], "high": []}
    for tk, g in dual.groupby("ticker"):
        for rg in ("low", "medium", "high"):
            s = g[g["regime"] == rg].dropna(subset=["H_price", "H_volume"])
            if len(s) >= 10:
                rr, _ = stats.pearsonr(s["H_price"], s["H_volume"])
                if np.isfinite(rr):
                    per[rg].append(float(rr))
    h3 = {}
    for rg in ("low", "medium", "high"):
        a = np.array(per[rg])
        h3[rg] = {"mean": float(a.mean()), "median": float(np.median(a)),
                  "std": float(a.std(ddof=1)), "n_firms": int(len(a))}
    U, pU = stats.mannwhitneyu(per["high"], per["low"], alternative="greater")
    h3["mannwhitney_high_gt_low"] = {"U": float(U), "p": float(pU)}
    res["H3_regime"] = h3

    # H4 predictive: forward dollar-volume Amihud ~ CII + H controls, firm FE
    h4 = robust_panel_regression(panel.dropna(subset=["CII", "H_price", "H_volume", "amihud_dollar"]),
                                 "amihud_dollar", ["CII", "H_price", "H_volume"],
                                 extended_focal="CII", wcr_n_boot=999)
    cii = h4["coefficients"]["CII"]
    res["H4_predictive"] = {
        "beta_CII": cii["beta"],
        "HC1": cii["HC1"], "firm_cluster": cii["firm_cluster"], "time_cluster": cii["time_cluster"],
        "twoway_cluster": cii["twoway_cluster"], "newey_west": cii["newey_west"],
        "driscoll_kraay": cii["driscoll_kraay"], "extended": h4.get("extended"),
        "n": h4["n"], "n_firms": h4["n_firms"], "r2": h4["r_squared"],
    }

    json.dump(res, open(OUT / "tables.json", "w"), indent=2, default=str)
    write_md(res)
    print("DONE -> tables.json, RESULT.md")


def write_md(r):
    L = ["# G=488 re-baseline on refreshed data (Path 2)\n"]
    L.append(f"Window 2015-01-01 to {r['window_end']}. Panel firms: {r['n_firms_panel']}; "
             f"full-Hurst firms: {r['n_firms_full_hurst']}. All tables from one fresh snapshot.\n")
    hs = r["hurst_summary"]
    L.append("## Hurst summary (full sample)")
    L.append(f"- H(returns): {hs['H_ret']['mean']:.3f} ± {hs['H_ret']['std']:.3f}")
    L.append(f"- H(|returns|): {hs['H_absr']['mean']:.3f} ± {hs['H_absr']['std']:.3f}")
    L.append(f"- H(volume): {hs['H_vol']['mean']:.3f} ± {hs['H_vol']['std']:.3f}\n")
    h1 = r["H1_static"]
    L.append(f"## H1 static: cross-sectional Pearson r(H|r|, Hvol) = {h1['pearson_r']:+.3f} "
             f"(p={h1['pearson_p']:.3f}), Spearman {h1['spearman_r']:+.3f} (p={h1['spearman_p']:.3f}), n={h1['n']}\n")
    h2 = r["H2_temporal"]
    L.append(f"## H2 temporal: mean r={h2['mean_r']:.3f}, median={h2['median_r']:.3f}, "
             f"{h2['pct_positive']:.0f}% positive ({h2['pct_pos_sig']:.0f}% positive & significant), n={h2['n_firms']}\n")
    L.append("## H3 regime (the n=495 fix: per-regime firm counts, all <= panel size)\n")
    L.append("| regime | mean | median | std | n firms |")
    L.append("|---|---|---|---|---|")
    for rg in ("low", "medium", "high"):
        d = r["H3_regime"][rg]
        L.append(f"| {rg} | {d['mean']:.3f} | {d['median']:.3f} | {d['std']:.3f} | {d['n_firms']} |")
    mw = r["H3_regime"]["mannwhitney_high_gt_low"]
    L.append(f"\nMann-Whitney high>low: U={mw['U']:.0f}, p={mw['p']:.4f}\n")
    h4 = r["H4_predictive"]
    L.append("## H4 predictive: forward dollar-volume Amihud ~ CII + H controls (firm FE)\n")
    L.append(f"beta_CII = {h4['beta_CII']:.4f}; n={h4['n']}, firms={h4['n_firms']}, R2={h4['r2']:.3f}")
    L.append("| SE method | t | p |")
    L.append("|---|---|---|")
    for k in ["HC1", "firm_cluster", "time_cluster", "twoway_cluster", "newey_west", "driscoll_kraay"]:
        L.append(f"| {k} | {h4[k]['t']:+.2f} | {h4[k]['p']:.3f} |")
    if h4.get("extended"):
        e = h4["extended"]
        L.append(f"| CR2 (Satterthwaite df={e['cr2']['df_satterthwaite']:.2f}) | {e['cr2']['t']:+.2f} | {e['cr2']['p']:.3f} |")
        L.append(f"| WCR bootstrap | --- | {e['wcr_bootstrap']['p']:.3f} |")
    L.append("\nEvery value above regenerates from `research/rebuild_g488/rebuild.py` on current data. "
             "No frozen-panel dependency.")
    (OUT / "RESULT.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
