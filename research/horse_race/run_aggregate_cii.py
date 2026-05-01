#!/usr/bin/env python3
"""Aggregate CII exhibit for the v1.4.0 manuscript.

Computes the cross-sectional mean of CII at each rolling-Hurst date
across all 488 Phase 2 firms, plots it against VIX, and reports the
correlation. This is the empirical handle that grounds the
firm-conditional vs. time-conditional inference disagreement reported
in Section 5.4: if there is a market-wide stress co-movement that the
time-clustered standard errors and Driscoll-Kraay HAC pick up, the
aggregate of CII across firms should track standard market-wide stress
indicators.

Output:
  - figure at research/paper/figures/fig10_aggregate_cii_vix.pdf
  - summary table of correlations
"""

import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

CACHE = ROOT / "research" / "horse_race" / "cache"
FIG_DIR = ROOT / "research" / "paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    panel = pickle.load(open(CACHE / "phase2_panel_final_full.pkl", "rb"))
    print(f"panel: {panel.shape}, {panel['ticker'].nunique()} firms")

    # Aggregate CII per date: mean across firms within each evaluation date
    panel = panel.copy()
    panel["date"] = pd.to_datetime(panel["date"])
    agg = (
        panel.groupby("date")["CII"]
        .agg(["mean", "median", "std", "count"])
        .reset_index()
        .rename(columns={"mean": "CII_mean", "median": "CII_median",
                         "std": "CII_std", "count": "n_firms"})
    )
    print(f"aggregate dates: {len(agg)}, range {agg['date'].min()} to {agg['date'].max()}")

    # VIX
    vix = yf.download("^VIX", start="2015-01-01", end="2026-04-15",
                      progress=False, auto_adjust=False)
    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)
    vix_close = vix["Close"].dropna().sort_index()
    vix_close.index = pd.to_datetime(vix_close.index)

    # Merge: VIX as-of for each rolling-Hurst date
    agg = agg.sort_values("date")
    vix_aligned = vix_close.reindex(agg["date"], method="ffill")
    agg["vix"] = vix_aligned.values

    # Correlations
    sub = agg.dropna()
    pearson_r = np.corrcoef(sub["CII_mean"], sub["vix"])[0, 1]
    print(f"Pearson r: aggregate CII vs VIX = {pearson_r:.3f}")
    from scipy import stats
    spearman = stats.spearmanr(sub["CII_mean"], sub["vix"])
    print(f"Spearman rho: aggregate CII vs VIX = {spearman.correlation:.3f} (p = {spearman.pvalue:.4f})")
    print(f"Pearson r: aggregate CII (median) vs VIX = {np.corrcoef(sub['CII_median'], sub['vix'])[0, 1]:.3f}")

    # Add log VIX too for the variant where stress is multiplicative
    sub["log_vix"] = np.log(sub["vix"])
    pearson_log = np.corrcoef(sub["CII_mean"], sub["log_vix"])[0, 1]
    print(f"Pearson r: aggregate CII vs log(VIX) = {pearson_log:.3f}")

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                                     gridspec_kw={"height_ratios": [2, 1]})

    # Top: aggregate CII with shaded ±1 std band
    ax1.fill_between(
        sub["date"],
        sub["CII_mean"] - sub["CII_std"],
        sub["CII_mean"] + sub["CII_std"],
        color="C0", alpha=0.15, label=r"$\pm 1\sigma$ across firms"
    )
    ax1.plot(sub["date"], sub["CII_mean"], color="C0", linewidth=1.6,
             label=r"$\overline{\mathrm{CII}}_t$ (cross-sectional mean)")
    ax1.plot(sub["date"], sub["CII_median"], color="C0", linewidth=0.8,
             linestyle="--", alpha=0.6, label=r"$\mathrm{median}_t \mathrm{CII}$")
    ax1.set_ylabel("Aggregate CII")
    ax1.set_title(r"Cross-sectionally aggregated CII vs.\ VIX, $G = 488$")
    ax1.legend(loc="upper right", fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(0, color="black", linewidth=0.5)

    # Bottom: VIX
    ax2.plot(sub["date"], sub["vix"], color="C3", linewidth=1.0)
    ax2.set_ylabel("VIX")
    ax2.set_xlabel("Date")
    ax2.grid(True, alpha=0.3)
    ax2.axhline(20, color="grey", linewidth=0.5, linestyle=":", alpha=0.6)

    # Annotate key episodes
    for date_str, label in [("2020-03-16", "COVID"), ("2022-09-26", "rate-hike\nstress")]:
        d = pd.Timestamp(date_str)
        ax1.axvline(d, color="black", linestyle="--", linewidth=0.5, alpha=0.5)
        ax2.axvline(d, color="black", linestyle="--", linewidth=0.5, alpha=0.5)
        ax1.annotate(label, xy=(d, ax1.get_ylim()[1]), xytext=(2, -2),
                     textcoords="offset points", fontsize=8, va="top",
                     ha="left")

    fig.tight_layout()
    out = FIG_DIR / "fig10_aggregate_cii_vix.pdf"
    fig.savefig(out, bbox_inches="tight")
    print(f"\nSaved {out}")

    # Save numbers for the manuscript
    pickle.dump({
        "agg_df": agg,
        "pearson_r_vix": pearson_r,
        "spearman_rho_vix": spearman.correlation,
        "spearman_p_vix": spearman.pvalue,
        "pearson_r_logvix": pearson_log,
    }, open(CACHE / "phase2_aggregate_cii.pkl", "wb"))
    print(f"Saved cache pickle")


if __name__ == "__main__":
    main()
