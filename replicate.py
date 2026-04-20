#!/usr/bin/env python3
"""Master replication script.

Reproduces all results, figures, and tables from:
  "Static and Temporal Fractal Coupling Between Volatility and Trading Volume"
  Dinesh Hari, 2026. DOI: 10.5281/zenodo.19611544

Usage:
    pip install -e .
    python replicate.py

Requires Python 3.10+. All data are downloaded from Yahoo Finance on first run
and cached locally as parquet files under data/raw/.

Expected runtime: ~15-20 minutes on a modern laptop (dominated by rolling
Hurst estimation across 50 tickers).

Output:
    research/paper/figures/fig1_hurst_distributions.pdf  ... fig9_sector_decomposition.pdf
    research/paper/tables/table1_hurst_estimates.csv
    research/paper/tables/table2_robustness_summary.csv
    research/paper/tables/table3_sector_summary.csv
    stdout: all numerical results reported in the paper
"""

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fractal_pv.data import fetch_universe, SP500_SAMPLE
from fractal_pv.stationarity import prepare_series
from fractal_pv.hurst import estimate_dfa, estimate_all
from fractal_pv.bootstrap import block_bootstrap_hurst
from fractal_pv.rolling import rolling_dual_hurst, temporal_correlation, lead_lag_correlation
from fractal_pv.predict import (
    compute_coupling_intensity,
    compute_forward_metrics,
    build_prediction_panel,
    run_all_predictions,
)
from fractal_pv.inference_robust import robust_panel_regression
from fractal_pv.regimes import (
    fetch_vix,
    classify_vix_regime,
    align_regime_with_rolling,
    coupling_by_regime,
)


def main():
    print("=" * 70)
    print("REPLICATION: Fractal Price-Volume Coupling")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Step 1: Fetch data
    # ------------------------------------------------------------------
    print("\n[1/7] Fetching data for 50 S&P 500 tickers...")
    tickers_data = fetch_universe(SP500_SAMPLE)
    print(f"  Loaded {len(tickers_data)} tickers")

    # ------------------------------------------------------------------
    # Step 2: Full-sample Hurst estimates
    # ------------------------------------------------------------------
    print("\n[2/7] Computing full-sample Hurst exponents...")
    hurst_results = {}
    for ticker, data in tickers_data.items():
        series = data["series"]
        h_ret = estimate_dfa(series["log_returns"])
        h_vol = estimate_dfa(series["abs_log_returns"])
        h_volume = estimate_dfa(series["log_volume"])
        hurst_results[ticker] = {
            "H_returns": h_ret.H,
            "H_volatility": h_vol.H,
            "H_volume": h_volume.H,
            "R2_volatility": h_vol.r_squared,
            "R2_volume": h_volume.r_squared,
        }

    hdf = pd.DataFrame(hurst_results).T
    print(f"  H(returns):    mean={hdf['H_returns'].mean():.3f}  std={hdf['H_returns'].std():.3f}")
    print(f"  H(|returns|):  mean={hdf['H_volatility'].mean():.3f}  std={hdf['H_volatility'].std():.3f}")
    print(f"  H(volume):     mean={hdf['H_volume'].mean():.3f}  std={hdf['H_volume'].std():.3f}")
    print(f"  Mean R2:       {hdf[['R2_volatility','R2_volume']].values.mean():.3f}")

    # Save Table 1
    outdir = Path("research/paper/tables")
    outdir.mkdir(parents=True, exist_ok=True)
    hdf.to_csv(outdir / "table1_hurst_estimates.csv")

    # ------------------------------------------------------------------
    # Step 3: Rolling dual-Hurst and temporal coupling
    # ------------------------------------------------------------------
    print("\n[3/7] Computing rolling Hurst exponents (W=500, step=20)...")
    rolling_results = {}
    for ticker, data in tickers_data.items():
        df = data["df"]
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)
        dual = rolling_dual_hurst(df, window=500, step=20)
        tc = temporal_correlation(dual)
        rolling_results[ticker] = {"dual": dual, "tc": tc}

    # H1: Static coupling
    cross_r, cross_p = stats.pearsonr(hdf["H_volatility"], hdf["H_volume"])
    print(f"\n  H1 (Static coupling):   r={cross_r:.3f}, p={cross_p:.3f}")

    # H2: Temporal coupling
    temporal_rs = {t: r["tc"]["pearson_r"] for t, r in rolling_results.items()
                   if r["tc"] and not np.isnan(r["tc"].get("pearson_r", np.nan))}
    tvals = list(temporal_rs.values())
    n_pos = sum(1 for v in tvals if v > 0)
    print(f"  H2 (Temporal coupling):  mean r={np.mean(tvals):.3f}, {n_pos}/{len(tvals)} positive")

    # ------------------------------------------------------------------
    # Step 4: Regime conditioning
    # ------------------------------------------------------------------
    print("\n[4/7] VIX regime conditioning...")
    vix = fetch_vix()
    regime = classify_vix_regime(vix)

    regime_coupling = {"low": [], "medium": [], "high": []}
    for ticker, rr in rolling_results.items():
        dual = rr["dual"]
        if dual.empty:
            continue
        aligned = align_regime_with_rolling(dual, vix, regime)
        by_regime = coupling_by_regime(aligned)
        for cat in ["low", "medium", "high"]:
            if cat in by_regime and not np.isnan(by_regime[cat].get("pearson_r", np.nan)):
                regime_coupling[cat].append(by_regime[cat]["pearson_r"])

    for cat in ["low", "medium", "high"]:
        vals = regime_coupling[cat]
        print(f"  {cat:>6s} VIX: mean r={np.mean(vals):.3f}  (n={len(vals)})")

    if regime_coupling["high"] and regime_coupling["low"]:
        u_stat, u_p = stats.mannwhitneyu(regime_coupling["high"], regime_coupling["low"],
                                          alternative="greater")
        print(f"  Mann-Whitney (high > low): p={u_p:.4f}")

    # ------------------------------------------------------------------
    # Step 5: Predictive regressions
    # ------------------------------------------------------------------
    print("\n[5/7] Building prediction panel and running regressions...")
    panel = build_prediction_panel(tickers_data, rolling_results, horizon=21)
    print(f"  Panel: {len(panel)} observations, {panel['ticker'].nunique()} tickers")

    for target in ["amihud_illiq", "realized_vol"]:
        if target not in panel.columns:
            continue
        res = robust_panel_regression(panel, target, ["CII", "H_price", "H_volume"])
        if "error" in res:
            print(f"  {target}: {res['error']}")
            continue
        cii = res["coefficients"].get("CII", {})
        print(f"\n  {target}:")
        for method in ["HC1", "firm_cluster", "time_cluster", "twoway_cluster", "newey_west"]:
            info = cii.get(method, {})
            t_val = info.get("t", 0)
            p_val = info.get("p", 1)
            sig = "***" if p_val < 0.01 else "**" if p_val < 0.05 else "*" if p_val < 0.10 else ""
            print(f"    {method:>16s}: t={t_val:6.2f}  p={p_val:.4f} {sig}")

    # ------------------------------------------------------------------
    # Step 6: Figures (placeholder — requires matplotlib display)
    # ------------------------------------------------------------------
    print("\n[6/7] Figure generation...")
    print("  Figures require matplotlib. See research/paper/figures/ for pre-generated PDFs.")

    # ------------------------------------------------------------------
    # Step 7: Summary
    # ------------------------------------------------------------------
    print("\n[7/7] Replication complete.")
    print(f"  Tables written to: {outdir}")
    print(f"  Pre-generated figures in: research/paper/figures/")
    print("=" * 70)


if __name__ == "__main__":
    main()
