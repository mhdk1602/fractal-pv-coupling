#!/usr/bin/env python3
"""Per-benchmark horse-race regressions at G = 488 for Table 6 of v1.4.0.

The full Phase 2 runner stores focal-only and combined-with-9-benchmarks
specifications. The v1.3.0 manuscript needs the per-benchmark specifications
(CII + one benchmark + Hurst controls) for the table cells that are
currently placeholder text. This script computes those.

Output: cache pickle with per-benchmark β/t-stats for the named benchmark
in each regression, for both Amihud illiquidity and realised volatility.
The CII coefficient in each per-benchmark regression is also stored so the
text can confirm it is null in every per-benchmark spec.

Usage:
    .venv/bin/python research/horse_race/run_per_benchmark.py
"""

import pickle
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fractal_pv.inference_robust import robust_panel_regression


CACHE = ROOT / "research" / "horse_race" / "cache"

BENCH_COLS = [
    "roll_spread", "corwin_schultz", "amihud_rolling", "turnover",
    "vol_of_vol", "lagged_rv", "lagged_illiq", "abn_turnover_t", "vix",
]
HURST_CONTROLS = ["H_price", "H_volume"]


def main():
    panel = pickle.load(open(CACHE / "phase2_panel_final_full.pkl", "rb"))
    print(f"panel: {panel.shape}, {panel['ticker'].nunique()} firms, "
          f"{panel['date'].nunique()} months")

    targets = ["amihud_illiq", "realized_vol"]
    out = {}

    for target in targets:
        out[target] = {}
        print(f"\n=== Per-benchmark horse race for target: {target} ===")
        for bench in BENCH_COLS:
            sub = panel.dropna(
                subset=["CII", target, bench] + HURST_CONTROLS
            ).copy()
            if len(sub) < 100:
                print(f"  [skip] {bench}: only {len(sub)} obs after dropna")
                continue
            t0 = time.time()
            res = robust_panel_regression(
                sub,
                target=target,
                regressors=["CII", bench] + HURST_CONTROLS,
            )
            elapsed = time.time() - t0
            cii = res["coefficients"].get("CII", {})
            bench_coef = res["coefficients"].get(bench, {})
            out[target][bench] = {
                "n": res["n"],
                "n_firms": res["n_firms"],
                "n_months": res["n_months"],
                "r_squared": res["r_squared"],
                "cii": cii,
                "benchmark_coef": bench_coef,
                "elapsed_sec": elapsed,
            }
            cii_2way = cii.get("twoway_cluster", {})
            bench_2way = bench_coef.get("twoway_cluster", {})
            print(
                f"  {bench:20s}: "
                f"benchmark β={bench_coef.get('beta', float('nan')):+.3g} "
                f"t_2way={bench_2way.get('t', float('nan')):+.2f} "
                f"p={bench_2way.get('p', float('nan')):.4f}  "
                f"|  CII β={cii.get('beta', float('nan')):+.3g} "
                f"t_2way={cii_2way.get('t', float('nan')):+.2f} "
                f"p={cii_2way.get('p', float('nan')):.4f}  "
                f"R²={res['r_squared']:.3f}  ({elapsed:.1f}s)"
            )

    out_path = CACHE / "phase2_per_benchmark.pkl"
    with out_path.open("wb") as f:
        pickle.dump(out, f)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
