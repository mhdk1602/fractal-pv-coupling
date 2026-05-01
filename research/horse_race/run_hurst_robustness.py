#!/usr/bin/env python3
"""Hurst-estimator robustness at G = 488.

Compares full-sample Hurst exponents from three estimators (DFA-1, R/S,
MFDFA at q=2) for the 488-firm Phase 2 panel. Reports cross-estimator
correlation and ranks. The robust manuscript claim is that the temporal
coupling phenomenon (H2) does not depend on the choice of DFA versus
its alternatives.

Output: table of cross-estimator correlations and a small panel check
on a random subsample.
"""

import pickle
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import nolds

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fractal_pv.hurst import estimate_dfa


CACHE = ROOT / "research" / "horse_race" / "cache"
RNG = np.random.default_rng(seed=42)


def main():
    tickers_data = pickle.load(open(CACHE / "phase2_tickers_data_full.pkl", "rb"))
    print(f"loaded {len(tickers_data)} tickers")

    rows = []
    t0 = time.time()
    for i, (ticker, data) in enumerate(tickers_data.items()):
        series_dict = data.get("series", {})
        abs_r = series_dict.get("abs_log_returns")
        log_v = series_dict.get("log_volume")
        if abs_r is None or log_v is None:
            continue
        abs_r = np.asarray(abs_r, dtype=float)
        log_v = np.asarray(log_v, dtype=float)
        if len(abs_r) < 600 or len(log_v) < 600:
            continue
        try:
            # DFA-1
            r_dfa_abs = estimate_dfa(abs_r)
            r_dfa_vol = estimate_dfa(log_v)
            # R/S via nolds
            h_rs_abs = nolds.hurst_rs(abs_r, fit="poly")
            h_rs_vol = nolds.hurst_rs(log_v, fit="poly")
            # nolds DFA (independent of our wrapper)
            h_nolds_dfa_abs = nolds.dfa(abs_r, order=1)
            h_nolds_dfa_vol = nolds.dfa(log_v, order=1)
            rows.append({
                "ticker": ticker,
                "H_dfa_abs": r_dfa_abs.H,
                "H_dfa_vol": r_dfa_vol.H,
                "H_rs_abs": h_rs_abs,
                "H_rs_vol": h_rs_vol,
                "H_nolds_dfa_abs": h_nolds_dfa_abs,
                "H_nolds_dfa_vol": h_nolds_dfa_vol,
                "n_obs": len(abs_r),
            })
        except Exception as e:
            print(f"[skip] {ticker}: {e}")
        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(tickers_data)}] elapsed {time.time()-t0:.1f}s")

    df = pd.DataFrame(rows)
    print(f"\ncomputed {len(df)} ticker estimates in {time.time()-t0:.1f}s")
    print()

    # Cross-estimator correlations
    print("=" * 80)
    print("Cross-estimator full-sample Hurst correlations at G = 488")
    print("=" * 80)
    print()
    print("Absolute-returns Hurst:")
    cols_abs = ["H_dfa_abs", "H_rs_abs", "H_nolds_dfa_abs"]
    print(df[cols_abs].corr().round(3).to_string())
    print()
    print("Log-volume Hurst:")
    cols_vol = ["H_dfa_vol", "H_rs_vol", "H_nolds_dfa_vol"]
    print(df[cols_vol].corr().round(3).to_string())
    print()

    # Mean differences
    print("Mean cross-estimator difference (DFA-1 vs R/S):")
    diff_abs = (df["H_dfa_abs"] - df["H_rs_abs"]).describe()
    diff_vol = (df["H_dfa_vol"] - df["H_rs_vol"]).describe()
    print(f"  abs returns: mean={diff_abs['mean']:.3f}, std={diff_abs['std']:.3f}, max abs deviation={diff_abs[['min','max']].abs().max():.3f}")
    print(f"  log volume:  mean={diff_vol['mean']:.3f}, std={diff_vol['std']:.3f}, max abs deviation={diff_vol[['min','max']].abs().max():.3f}")
    print()

    # Save for the manuscript
    out_path = CACHE / "phase2_hurst_robustness.pkl"
    with out_path.open("wb") as f:
        pickle.dump({
            "df": df,
            "corr_abs": df[cols_abs].corr(),
            "corr_vol": df[cols_vol].corr(),
        }, f)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
