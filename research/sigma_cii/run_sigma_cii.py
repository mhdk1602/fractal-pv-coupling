#!/usr/bin/env python3
"""sigma(CII): cross-sectional dispersion of price-volume coupling as a market-stress signal.

The make-or-break experiment for the flagship reframe. The firm-conditional
predictive content of CII is a null (two-way clustered t = -0.93 on forward
dollar-volume Amihud at G=488). The proposed positive object is instead the
SECOND moment: sigma(CII)_t = cross-firm standard deviation of the within-firm
Coupling Intensity Index at each rolling-Hurst date. The hypothesis is that when
coupling structure fragments across firms (dispersion rises), the market is
under or entering stress.

Decision rule (pre-registered here, before looking at results):
  - sigma(CII) LEADS an established stress measure (peak cross-correlation at a
    positive lag, AND a predictive regression coefficient on a forward stress
    measure that survives Newey-West with the lagged stress level controlled)
        -> Chaos, Solitons & Fractals-eligible positive headline.
  - sigma(CII) COINCIDES (peak at lag 0, contemporaneous correlation only)
        -> Physica A positive descriptive claim.
  - sigma(CII) is NOISE (no stable contemporaneous or lead relationship)
        -> fall back to the structured precise null.

Stress measures: VIX (implied-vol fear gauge), realized S&P 500 vol (SPY),
high-yield credit stress (HYG realized vol), Pastor-Stambaugh liquidity
innovations (the non-traded liquidity factor; the liquidity channel the
firm-level null was about). All but P-S are daily and aligned as-of to the
~monthly rolling-Hurst dates; P-S is monthly.

Outputs (research/sigma_cii/):
  - cii_panel.parquet        per-firm CII series (cached; expensive to recompute)
  - sigma_cii_series.csv     date, mean/median/std/iqr/count + bootstrap band
  - results.json             all correlations, lead-lag, Granger, predictive regs, verdict
  - SUMMARY.md               human-readable verdict
  - fig_sigma_cii.png/.pdf   sigma(CII) with bootstrap band vs VIX, and the CCF panel
"""

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]   # Matlab---fractal-modelling/
sys.path.insert(0, str(ROOT / "src"))

from fractal_pv.stationarity import prepare_series          # noqa: E402
from fractal_pv.rolling import rolling_dual_hurst            # noqa: E402
from fractal_pv.predict import compute_coupling_intensity    # noqa: E402

OUT = ROOT / "research" / "sigma_cii"
DATA = OUT / "data"
RAW = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)

W, STEP, CORR_WIN = 500, 20, 30
NON_FIRMS = {"SPY", "^VIX", "VVIX", "HYG", "IEF", "LQD"}   # market/ETF series, not firms
RNG = np.random.default_rng(42)


# --------------------------------------------------------------------------- #
# 1. Per-firm CII panel (cached)
# --------------------------------------------------------------------------- #
def ticker_from_path(p: Path) -> str:
    return p.name.split("_")[0]


def build_cii_panel() -> pd.DataFrame:
    """Wide [date x ticker] matrix of within-firm CII. Cached to parquet."""
    cache = DATA / "cii_panel.parquet"
    if cache.exists():
        print(f"[cache] loading {cache}")
        return pd.read_parquet(cache)

    files = sorted(RAW.glob("*_1d_*.parquet"))
    series_by_ticker = {}
    for f in files:
        tk = ticker_from_path(f)
        if tk in NON_FIRMS:
            continue
        try:
            df = pd.read_parquet(f)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df[["Close", "Volume"]].dropna()
            if len(df) < W + CORR_WIN * STEP // STEP + 50:
                # need enough length for rolling + trailing CII window
                if len(df) < W + 50:
                    print(f"  skip {tk}: only {len(df)} rows")
                    continue
            ser = prepare_series(df)
            dates = df.index[1:][: len(ser["abs_log_returns"])].values
            dual = rolling_dual_hurst(
                ser["abs_log_returns"], ser["log_volume"], dates, window=W, step=STEP
            )
            if dual.empty:
                continue
            cii = compute_coupling_intensity(dual, correlation_window=CORR_WIN)
            if cii.empty:
                continue
            series_by_ticker[tk] = cii
            print(f"  {tk}: {len(cii)} CII obs  [{cii.index.min().date()}..{cii.index.max().date()}]")
        except Exception as e:
            print(f"  ERR {tk}: {e}")

    panel = pd.DataFrame(series_by_ticker).sort_index()
    panel.index.name = "date"
    panel.to_parquet(cache)
    print(f"[cache] wrote {cache}  shape={panel.shape}")
    return panel


# --------------------------------------------------------------------------- #
# 2. Cross-sectional aggregates + firm-resample bootstrap band on sigma
# --------------------------------------------------------------------------- #
def cross_sectional(panel: pd.DataFrame, min_firms: int = 10, n_boot: int = 1000) -> pd.DataFrame:
    agg = pd.DataFrame(index=panel.index)
    agg["mean"] = panel.mean(axis=1)
    agg["median"] = panel.median(axis=1)
    agg["std"] = panel.std(axis=1, ddof=1)         # sigma(CII)_t  <-- the object
    agg["iqr"] = panel.quantile(0.75, axis=1) - panel.quantile(0.25, axis=1)
    agg["count"] = panel.count(axis=1)
    agg = agg[agg["count"] >= min_firms].copy()

    # firm-resample bootstrap CI on sigma(CII)_t
    sub = panel.loc[agg.index]
    vals = sub.values                               # [T x G], NaNs where firm absent
    T, G = vals.shape
    boot = np.empty((n_boot, T))
    for b in range(n_boot):
        cols = RNG.integers(0, G, size=G)
        sample = vals[:, cols]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            boot[b] = np.nanstd(sample, axis=1, ddof=1)
    agg["std_lo"] = np.nanpercentile(boot, 2.5, axis=0)
    agg["std_hi"] = np.nanpercentile(boot, 97.5, axis=0)
    agg["std_se"] = np.nanstd(boot, axis=0, ddof=1)
    return agg


# --------------------------------------------------------------------------- #
# 3. Stress indicators aligned to CII dates
# --------------------------------------------------------------------------- #
def fetch_yf_close(ticker: str, start="2014-06-01", end="2026-04-15") -> pd.Series:
    import yfinance as yf
    d = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = d.columns.get_level_values(0)
    s = d["Close"].dropna()
    s.index = pd.to_datetime(s.index)
    return s.sort_index()


def realized_vol(close: pd.Series, window: int = 21) -> pd.Series:
    r = np.log(close / close.shift(1))
    return (r.rolling(window).std() * np.sqrt(252)).dropna()


def load_pastor_stambaugh() -> pd.DataFrame | None:
    f = DATA / "pastor_stambaugh_liq.txt"
    if not f.exists():
        return None
    rows = []
    for line in f.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("%"):
            continue
        parts = line.split()
        if len(parts) >= 4 and parts[0].isdigit() and len(parts[0]) == 6:
            ym = parts[0]
            rows.append({
                "date": pd.Timestamp(int(ym[:4]), int(ym[4:6]), 1) + pd.offsets.MonthEnd(0),
                "ps_level": float(parts[1]),
                "ps_innov": float(parts[2]),     # non-traded liquidity factor (the main series)
                "ps_traded": float(parts[3]),
            })
    if not rows:
        return None
    return pd.DataFrame(rows).set_index("date").sort_index()


def asof_align(daily: pd.Series, dates: pd.DatetimeIndex) -> np.ndarray:
    return daily.reindex(daily.index.union(dates)).ffill().reindex(dates).values


def build_stress(dates: pd.DatetimeIndex) -> pd.DataFrame:
    s = pd.DataFrame(index=dates)
    try:
        vix = fetch_yf_close("^VIX")
        s["vix"] = asof_align(vix, dates)
        s["log_vix"] = np.log(s["vix"])
    except Exception as e:
        print(f"  VIX fail: {e}")
    try:
        spy = fetch_yf_close("SPY")
        s["spy_rv"] = asof_align(realized_vol(spy, 21), dates)
    except Exception as e:
        print(f"  SPY fail: {e}")
    try:
        hyg = fetch_yf_close("HYG")
        s["hyg_rv"] = asof_align(realized_vol(hyg, 21), dates)
    except Exception as e:
        print(f"  HYG fail: {e}")
    ps = load_pastor_stambaugh()
    if ps is not None:
        # monthly: align each CII date to its month-end P-S obs (as-of, backward)
        s["ps_innov"] = ps["ps_innov"].reindex(ps.index.union(dates)).ffill().reindex(dates).values
        s["ps_illiq"] = -s["ps_innov"]   # negative liquidity innovation = stress (sign-flip)
    return s


# --------------------------------------------------------------------------- #
# 4. Lead-lag, Granger, predictive regressions
# --------------------------------------------------------------------------- #
def crosscorr(x: pd.Series, y: pd.Series, max_lag: int = 6) -> pd.DataFrame:
    """CCF of x vs y. lag>0 => x LEADS y (x_t corr y_{t+lag})."""
    out = []
    n = len(x)
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            xs, ys = x.iloc[: n - lag], y.iloc[lag:]
        else:
            xs, ys = x.iloc[-lag:], y.iloc[: n + lag]
        m = (~np.isnan(xs.values)) & (~np.isnan(ys.values))
        if m.sum() < 12:
            continue
        r, p = stats.pearsonr(xs.values[m], ys.values[m])
        out.append({"lag": lag, "r": r, "p": p, "n": int(m.sum())})
    return pd.DataFrame(out)


def granger_both(x: pd.Series, y: pd.Series, maxlag: int = 4) -> dict:
    """Granger tests on first differences (stationarity). Returns min-p per direction."""
    from statsmodels.tsa.stattools import grangercausalitytests
    df = pd.concat([x, y], axis=1).dropna()
    df = df.diff().dropna()
    res = {}
    for name, cols in [("x_causes_y", [df.columns[1], df.columns[0]]),
                       ("y_causes_x", [df.columns[0], df.columns[1]])]:
        try:
            g = grangercausalitytests(df[cols], maxlag=maxlag, verbose=False)
            pmin = min(g[l][0]["ssr_ftest"][1] for l in g)
            larg = min(g, key=lambda l: g[l][0]["ssr_ftest"][1])
            res[name] = {"min_p": float(pmin), "best_lag": int(larg)}
        except Exception as e:
            res[name] = {"error": str(e)[:120]}
    return res


def predictive_reg(sigma: pd.Series, stress: pd.Series, h: int) -> dict:
    """stress_{t+h} ~ const + sigma_t + stress_t  (Newey-West HAC, maxlags=h).

    The coefficient on sigma_t tests whether dispersion predicts FUTURE stress
    beyond the persistence already in the current stress level.
    """
    import statsmodels.api as sm
    df = pd.concat([sigma.rename("sigma"), stress.rename("stress")], axis=1).dropna()
    df["stress_fwd"] = df["stress"].shift(-h)
    df = df.dropna()
    if len(df) < 30:
        return {"error": "n<30", "n": len(df)}
    X = sm.add_constant(df[["sigma", "stress"]])
    model = sm.OLS(df["stress_fwd"], X).fit(cov_type="HAC", cov_kwds={"maxlags": h})
    return {
        "h": h, "n": int(model.nobs),
        "beta_sigma": float(model.params["sigma"]),
        "t_sigma": float(model.tvalues["sigma"]),
        "p_sigma": float(model.pvalues["sigma"]),
        "r2": float(model.rsquared),
        "beta_stress_lag": float(model.params["stress"]),
    }


# --------------------------------------------------------------------------- #
# 5. Main
# --------------------------------------------------------------------------- #
def main():
    print("=== building per-firm CII panel ===")
    panel = build_cii_panel()
    print(f"panel: {panel.shape[1]} firms, {panel.shape[0]} dates, "
          f"{panel.index.min().date()}..{panel.index.max().date()}")

    print("\n=== cross-sectional aggregates + bootstrap band ===")
    agg = cross_sectional(panel)
    agg.index = pd.to_datetime(agg.index)
    print(f"sigma(CII): {len(agg)} dates, mean firms/date = {agg['count'].mean():.0f}")
    print(f"  sigma(CII) range [{agg['std'].min():.3f}, {agg['std'].max():.3f}], "
          f"mean {agg['std'].mean():.3f}")

    print("\n=== stress indicators ===")
    stress = build_stress(agg.index)
    for c in stress.columns:
        print(f"  {c}: {stress[c].notna().sum()} obs")

    results = {"config": {"W": W, "step": STEP, "corr_win": CORR_WIN,
                          "n_firms": int(panel.shape[1]), "n_dates": int(len(agg))},
               "sigma_summary": {"mean": float(agg["std"].mean()),
                                 "min": float(agg["std"].min()),
                                 "max": float(agg["std"].max())}}

    measures = [c for c in ["vix", "log_vix", "spy_rv", "hyg_rv", "ps_illiq"] if c in stress]
    sigma = agg["std"]
    meanc = agg["mean"]

    # (a) contemporaneous correlations: sigma vs stress, and mean vs stress (to replicate ~0.057)
    contemp = {}
    for m in measures:
        d = pd.concat([sigma, stress[m]], axis=1).dropna()
        if len(d) < 12:
            continue
        pr, pp = stats.pearsonr(d.iloc[:, 0], d.iloc[:, 1])
        sr, sp = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
        dm = pd.concat([meanc, stress[m]], axis=1).dropna()
        mr, _ = stats.pearsonr(dm.iloc[:, 0], dm.iloc[:, 1])
        contemp[m] = {"sigma_pearson": float(pr), "sigma_pearson_p": float(pp),
                      "sigma_spearman": float(sr), "sigma_spearman_p": float(sp),
                      "mean_pearson": float(mr), "n": int(len(d))}
    results["contemporaneous"] = contemp

    # (b) lead-lag CCF
    leadlag = {}
    for m in measures:
        cc = crosscorr(sigma, stress[m], max_lag=6)
        if cc.empty:
            continue
        peak = cc.loc[cc["r"].abs().idxmax()]
        lag0 = cc.loc[cc["lag"] == 0].iloc[0]
        # strongest POSITIVE-lag (sigma leads) point
        pos = cc[cc["lag"] > 0]
        best_pos = pos.loc[pos["r"].abs().idxmax()] if not pos.empty else None
        leadlag[m] = {
            "peak_lag": int(peak["lag"]), "peak_r": float(peak["r"]), "peak_p": float(peak["p"]),
            "lag0_r": float(lag0["r"]), "lag0_p": float(lag0["p"]),
            "best_pos_lag": (None if best_pos is None else int(best_pos["lag"])),
            "best_pos_r": (None if best_pos is None else float(best_pos["r"])),
            "best_pos_p": (None if best_pos is None else float(best_pos["p"])),
            "ccf": cc.to_dict("records"),
        }
    results["lead_lag"] = leadlag

    # (c) Granger both directions
    granger = {}
    for m in measures:
        granger[m] = granger_both(sigma, stress[m], maxlag=4)
    results["granger"] = granger

    # (d) predictive regressions h in {1,3,6}
    pred = {}
    for m in measures:
        pred[m] = {f"h{h}": predictive_reg(sigma, stress[m], h) for h in (1, 3, 6)}
    results["predictive"] = pred

    # (e) verdict
    verdict = decide(contemp, leadlag, pred, measures)
    results["verdict"] = verdict
    print(f"\n=== VERDICT: {verdict['call'].upper()} ===")
    print(verdict["rationale"])

    # save
    agg.to_csv(OUT / "sigma_cii_series.csv")
    stress.to_csv(OUT / "stress_indicators.csv")
    json.dump(results, open(OUT / "results.json", "w"), indent=2, default=str)
    write_summary(results)
    make_figure(agg, stress, leadlag)
    print(f"\nWrote {OUT}/results.json, SUMMARY.md, sigma_cii_series.csv, fig_sigma_cii.png")


def decide(contemp, leadlag, pred, measures) -> dict:
    leads, coincides = [], []
    for m in measures:
        ll = leadlag.get(m, {})
        pr = pred.get(m, {})
        # LEAD: peak CCF at positive lag AND a predictive reg (h=1 or 3) with |t|>2
        lead_ccf = ll.get("peak_lag", 0) > 0 and ll.get("peak_p", 1) < 0.05
        lead_reg = any(isinstance(pr.get(f"h{h}"), dict) and abs(pr[f"h{h}"].get("t_sigma", 0)) > 2.0
                       and pr[f"h{h}"].get("p_sigma", 1) < 0.05 for h in (1, 3))
        if lead_ccf and lead_reg:
            leads.append(m)
        elif abs(contemp.get(m, {}).get("sigma_pearson", 0)) > 0.3 and contemp.get(m, {}).get("sigma_pearson_p", 1) < 0.05:
            coincides.append(m)
    if leads:
        call = "leads"
        rat = (f"sigma(CII) leads {', '.join(leads)}: peak cross-correlation at a positive lag "
               f"AND a Newey-West predictive coefficient with |t|>2. Chaos, Solitons & Fractals-eligible headline.")
    elif coincides:
        call = "coincides"
        rat = (f"sigma(CII) co-moves contemporaneously with {', '.join(coincides)} (|Pearson|>0.3, p<0.05) "
               f"but does not robustly lead. Physica A positive descriptive claim.")
    else:
        call = "noise"
        rat = ("No stable contemporaneous (|r|>0.3) or leading relationship survives. "
               "Fall back to the structured precise null; do not headline sigma(CII).")
    return {"call": call, "leads": leads, "coincides": coincides, "rationale": rat}


def write_summary(r: dict):
    L = []
    L.append("# sigma(CII) make-or-break: results\n")
    c = r["config"]
    L.append(f"Universe: {c['n_firms']} firms, {c['n_dates']} rolling-Hurst dates "
             f"(W={c['W']}, step={c['step']}, CII window={c['corr_win']}).")
    L.append(f"sigma(CII) range [{r['sigma_summary']['min']:.3f}, {r['sigma_summary']['max']:.3f}], "
             f"mean {r['sigma_summary']['mean']:.3f}.\n")
    L.append(f"## Verdict: **{r['verdict']['call'].upper()}**\n\n{r['verdict']['rationale']}\n")
    L.append("## Contemporaneous correlation (sigma vs stress; mean-CII vs stress for contrast)\n")
    L.append("| stress | sigma Pearson | p | sigma Spearman | p | mean-CII Pearson | n |")
    L.append("|---|---|---|---|---|---|---|")
    for m, d in r["contemporaneous"].items():
        L.append(f"| {m} | {d['sigma_pearson']:+.3f} | {d['sigma_pearson_p']:.3f} | "
                 f"{d['sigma_spearman']:+.3f} | {d['sigma_spearman_p']:.3f} | "
                 f"{d['mean_pearson']:+.3f} | {d['n']} |")
    L.append("\n## Lead-lag (lag>0 => sigma LEADS stress)\n")
    L.append("| stress | peak lag | peak r | peak p | lag0 r | best +lag | +lag r | +lag p |")
    L.append("|---|---|---|---|---|---|---|---|")
    for m, d in r["lead_lag"].items():
        bpr = "" if d["best_pos_r"] is None else f"{d['best_pos_r']:+.3f}"
        bpp = "" if d["best_pos_p"] is None else f"{d['best_pos_p']:.3f}"
        L.append(f"| {m} | {d['peak_lag']} | {d['peak_r']:+.3f} | {d['peak_p']:.3f} | "
                 f"{d['lag0_r']:+.3f} | {d['best_pos_lag']} | {bpr} | {bpp} |")
    L.append("\n## Predictive regressions: stress_{t+h} ~ sigma_t + stress_t (Newey-West)\n")
    L.append("| stress | h | beta_sigma | t_sigma | p_sigma | R2 | n |")
    L.append("|---|---|---|---|---|---|---|")
    for m, hs in r["predictive"].items():
        for hk, d in hs.items():
            if "error" in d:
                continue
            L.append(f"| {m} | {d['h']} | {d['beta_sigma']:+.4f} | {d['t_sigma']:+.2f} | "
                     f"{d['p_sigma']:.3f} | {d['r2']:.3f} | {d['n']} |")
    L.append("\n## Granger (first differences, min p over lags 1-4)\n")
    L.append("| stress | sigma->stress min p (lag) | stress->sigma min p (lag) |")
    L.append("|---|---|---|")
    for m, d in r["granger"].items():
        a = d.get("x_causes_y", {}); b = d.get("y_causes_x", {})
        L.append(f"| {m} | {a.get('min_p','-'):.3} ({a.get('best_lag','-')}) | "
                 f"{b.get('min_p','-'):.3} ({b.get('best_lag','-')}) |"
                 if "min_p" in a and "min_p" in b else f"| {m} | err | err |")
    (OUT / "SUMMARY.md").write_text("\n".join(L))


def make_figure(agg, stress, leadlag):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8),
                                   gridspec_kw={"height_ratios": [2, 1.2]})
    ax1.fill_between(agg.index, agg["std_lo"], agg["std_hi"], color="C0", alpha=0.18,
                     label=r"$\sigma(\mathrm{CII})_t$ 95% firm-resample CI")
    ax1.plot(agg.index, agg["std"], color="C0", lw=1.7, label=r"$\sigma(\mathrm{CII})_t$ (cross-firm SD)")
    ax1b = ax1.twinx()
    if "vix" in stress:
        ax1b.plot(agg.index, stress["vix"], color="C3", lw=1.0, alpha=0.8, label="VIX")
        ax1b.set_ylabel("VIX", color="C3")
    ax1.set_ylabel(r"$\sigma(\mathrm{CII})_t$", color="C0")
    ax1.set_title(r"Cross-sectional dispersion of price-volume coupling vs market stress")
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(alpha=0.3)
    for ds, lab in [("2020-03-16", "COVID"), ("2022-09-26", "rate-hike")]:
        ax1.axvline(pd.Timestamp(ds), color="k", ls="--", lw=0.5, alpha=0.5)

    # CCF panel vs VIX
    if "vix" in leadlag:
        cc = pd.DataFrame(leadlag["vix"]["ccf"])
        ax2.bar(cc["lag"], cc["r"], color=["C2" if l > 0 else "C7" for l in cc["lag"]])
        ax2.axvline(0, color="k", lw=0.6)
        ax2.set_xlabel("lag (rolling-Hurst steps ~1 month; lag>0 = sigma(CII) leads VIX)")
        ax2.set_ylabel("cross-corr")
        ax2.set_title("Lead-lag: sigma(CII) vs VIX")
        ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "fig_sigma_cii.png", dpi=130, bbox_inches="tight")
    fig.savefig(OUT / "fig_sigma_cii.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
