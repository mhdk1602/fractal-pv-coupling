#!/usr/bin/env python3
"""Phase 2 runner: full S&P 500 (G ≈ 500) under the pre-registered protocol.

Reads `data/sp500_constituents_2026-04-28.csv`, batch-fetches via yfinance,
runs the v1.2.0 pipeline end-to-end, applies the decision rule fixed in
`research/horse_race/PHASE2_PROTOCOL.md`, and writes
`research/horse_race/PHASE2_RESULTS.md`.

Pipeline is identical to v1.2.0 modulo universe size:

  1. fetch_universe_batch (yfinance multi-ticker)
  2. prepare_series (stationarity verification per ticker)
  3. rolling_dual_hurst (parallel via joblib; W=500, step=20)
  4. build_prediction_panel (h=21, dollar-volume Amihud)
  5. compute_all_benchmarks (Roll, Corwin-Schultz, dollar Amihud, turnover, vol-of-vol)
  6. build_enriched_panel (lagged_rv, lagged_illiq, abn_turnover, vix)
  7. ten-target horse race (focal-only and combined)
  8. CR2 + WCR for primary target
  9. apply pre-registered decision rule

Usage:
    .venv/bin/python research/horse_race/run_phase2.py --universe full
    .venv/bin/python research/horse_race/run_phase2.py --universe pilot --pilot-size 100

Long-running (~6-8h on workstation for full universe).
"""

import argparse
import csv
import pickle
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fractal_pv.data import fetch_universe_batch
from fractal_pv.stationarity import prepare_series
from fractal_pv.rolling import rolling_dual_hurst
from fractal_pv.predict import build_prediction_panel
from fractal_pv.benchmarks import compute_all_benchmarks
from fractal_pv.inference_robust import (
    build_enriched_panel,
    horse_race_regression,
    robust_panel_regression,
)


CACHE = ROOT / "research" / "horse_race" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)
DATA_RAW = ROOT / "data" / "raw" / "sp500_phase2"
DATA_RAW.mkdir(parents=True, exist_ok=True)


# Targets in the pre-registered order from PHASE2_PROTOCOL.md §4.2.
TARGETS = [
    ("amihud_illiq", "Amihud illiquidity (primary, dollar-volume)"),
    ("log_amihud", "log Amihud"),
    ("delta_amihud", "ΔAmihud (forward − contemp.)"),
    ("fwd_corwin_schultz", "forward Corwin-Schultz spread"),
    ("fwd_roll_spread", "forward Roll spread"),
    ("fwd_vol_of_vol", "forward vol-of-vol"),
    ("realized_vol", "realised volatility"),
    ("max_drawdown", "max drawdown"),
    ("abnormal_turnover", "abnormal turnover"),
]

BENCH_COLS = [
    "roll_spread", "corwin_schultz", "amihud_rolling", "turnover",
    "vol_of_vol", "lagged_rv", "lagged_illiq", "abn_turnover_t", "vix",
]
HURST_CONTROLS = ["H_price", "H_volume"]


def _load_tickers(csv_path: Path) -> list[str]:
    tickers = []
    with open(csv_path) as f:
        r = csv.DictReader(f)
        for row in r:
            tickers.append(row["Symbol"])
    return sorted(tickers)


def _stage(name: str, fn, force: bool = False):
    """Pickle-cache a stage's output. Same convention as run_horse_race.py."""
    path = CACHE / f"phase2_{name}.pkl"
    if path.exists() and not force:
        print(f"  [cache hit] phase2_{name}")
        with path.open("rb") as f:
            return pickle.load(f)
    print(f"  [computing] phase2_{name}")
    t0 = time.time()
    out = fn()
    elapsed = time.time() - t0
    with path.open("wb") as f:
        pickle.dump(out, f)
    print(f"  [done] phase2_{name} in {elapsed:.1f}s")
    return out


def _wrap_tickers_data(raw: dict) -> dict:
    """Normalize fetch output into the form predict.py expects."""
    wrapped = {}
    for ticker, df in raw.items():
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)
        try:
            series = prepare_series(df)
        except Exception as e:
            print(f"    [warn] prepare_series failed for {ticker}: {e}")
            series = {}
        wrapped[ticker] = {"df": df, "series": series, "dates": df.index.to_numpy()}
    return wrapped


def _compute_rolling(tickers_data: dict) -> dict:
    rolling_results = {}
    total = len(tickers_data)
    for i, (ticker, data) in enumerate(tickers_data.items(), 1):
        series = data.get("series", {})
        abs_returns = series.get("abs_log_returns")
        log_volume = series.get("log_volume")
        dates = data.get("dates")
        if abs_returns is None or log_volume is None:
            print(f"    [skip] {ticker}: missing prepared series")
            continue
        try:
            dual = rolling_dual_hurst(
                abs_returns, log_volume, dates=dates, window=500, step=20,
            )
            if dual is not None and not dual.empty:
                rolling_results[ticker] = {"dual": dual}
                if i % 25 == 0 or i == total:
                    print(f"    [{i:>3}/{total}] {ticker}: {len(dual)} windows")
        except Exception as e:
            print(f"    [warn] {ticker}: {e}")
    return rolling_results


def _compute_benchmarks(tickers_data: dict) -> dict:
    out = {}
    for ticker, data in tickers_data.items():
        df = data["df"]
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)
        try:
            out[ticker] = compute_all_benchmarks(df, window=21)
        except Exception as e:
            print(f"    [warn] {ticker}: {e}")
    return out


def _merge_benchmarks(enriched: pd.DataFrame, benchmarks_by_ticker: dict) -> pd.DataFrame:
    out_rows = []
    bench_cols = ["roll_spread", "corwin_schultz", "amihud", "turnover", "vol_of_vol"]
    for ticker, sub in enriched.groupby("ticker"):
        bench_df = benchmarks_by_ticker.get(ticker)
        if bench_df is None:
            continue
        sub = sub.copy()
        sub["date"] = pd.to_datetime(sub["date"]).astype("datetime64[ns]")
        bench_reset = bench_df.reset_index()
        bench_reset.columns = ["date"] + list(bench_reset.columns[1:])
        bench_reset["date"] = pd.to_datetime(bench_reset["date"]).astype("datetime64[ns]")
        sub = sub.sort_values("date")
        bench_reset = bench_reset.sort_values("date")
        merged = pd.merge_asof(
            sub, bench_reset[["date"] + bench_cols],
            on="date", direction="backward",
            tolerance=pd.Timedelta("7D"),
        )
        merged = merged.rename(columns={"amihud": "amihud_rolling"})
        out_rows.append(merged)
    if not out_rows:
        return enriched.copy()
    return pd.concat(out_rows, ignore_index=True)


def _augment_targets(panel: pd.DataFrame) -> pd.DataFrame:
    """Add the secondary target columns the protocol specifies."""
    panel = panel.sort_values(["ticker", "date"]).copy()
    panel["log_amihud"] = np.log(panel["amihud_illiq"].clip(lower=1e-12))
    panel["delta_amihud"] = panel.groupby("ticker")["amihud_illiq"].diff()
    for col in ["corwin_schultz", "roll_spread", "vol_of_vol", "amihud_rolling"]:
        panel[f"fwd_{col}"] = panel.groupby("ticker")[col].shift(-1)
    return panel


def _extended_p(reg_result: dict, key: str) -> float | None:
    """Extract a p-value from the extended dict.

    Keys per inference_robust.robust_panel_regression: 'cr2', 'wcr_bootstrap'.
    """
    ext = reg_result.get("extended")
    if not ext:
        return None
    if key == "cr2":
        return ext.get("cr2", {}).get("p")
    if key == "wcr":
        return ext.get("wcr_bootstrap", {}).get("p")
    return None


def _classify(target_res: dict, secondary: bool = False) -> str:
    """Apply the pre-registered decision rule. Returns 'A', 'B', or 'C'."""
    focal = target_res.get("focal_only", {})
    if "error" in focal:
        return "C"
    cii = focal.get("coefficients", {}).get("CII", {})

    twoway_p = cii.get("twoway_cluster", {}).get("p", 1.0)
    dk_p = cii.get("driscoll_kraay", {}).get("p", 1.0)
    wcr_p = _extended_p(focal, "wcr")
    if wcr_p is None:
        wcr_p = _extended_p(target_res.get("combined", {}), "wcr")

    # Category A: predictive null confirmed
    if twoway_p > 0.10 and dk_p > 0.10 and (wcr_p is None or wcr_p > 0.10):
        return "A"

    # Category B: combined-spec robust signal
    combined = target_res.get("combined", {})
    if "error" in combined:
        return "C"
    cii_combined = combined.get("coefficients", {}).get("CII", {})
    twoway_p_c = cii_combined.get("twoway_cluster", {}).get("p", 1.0)
    dk_p_c = cii_combined.get("driscoll_kraay", {}).get("p", 1.0)
    cr2_p = _extended_p(combined, "cr2") or 1.0
    wcr_p_c = _extended_p(combined, "wcr") or 1.0

    beta_focal = cii.get("beta", 0.0)
    beta_combined = cii_combined.get("beta", 0.0)
    same_sign = (beta_focal * beta_combined) > 0
    magnitude_ok = abs(beta_focal) > 0 and (abs(beta_combined) / abs(beta_focal)) >= 0.25

    if (twoway_p_c < 0.05 and dk_p_c < 0.05 and wcr_p_c < 0.05 and cr2_p < 0.10
            and same_sign and magnitude_ok):
        return "B"

    return "C"


def main(args):
    print("=" * 100)
    print(f"Phase 2 runner — {datetime.now().isoformat(timespec='seconds')}")
    print(f"  universe: {args.universe} (pilot size: {args.pilot_size})")
    print(f"  cache:    {CACHE}")
    print(f"  raw data: {DATA_RAW}")
    print("=" * 100)

    csv_path = ROOT / "data" / "sp500_constituents_2026-04-28.csv"
    all_tickers = _load_tickers(csv_path)

    if args.universe == "pilot":
        ticker_set = all_tickers[: args.pilot_size]
        suffix = f"pilot{args.pilot_size}"
    else:
        ticker_set = all_tickers
        suffix = "full"

    print(f"\n[1/7] Fetching {len(ticker_set)} tickers")
    raw = fetch_universe_batch(
        ticker_set,
        start="2015-01-01",
        end="2026-04-01",
        cache_dir=DATA_RAW,
        min_observations=600,
        batch_size=50,
    )

    print(f"\n[2/7] Wrapping and preparing series")
    tickers_data = _stage(f"tickers_data_{suffix}", lambda: _wrap_tickers_data(raw),
                          force=args.force_stage in ("tickers_data", "all"))

    print(f"\n[3/7] Rolling dual-Hurst (slow stage)")
    rolling_results = _stage(f"rolling_results_{suffix}",
                             lambda: _compute_rolling(tickers_data),
                             force=args.force_stage in ("rolling", "all"))
    print(f"      {len(rolling_results)} tickers with rolling Hurst")

    print(f"\n[4/7] Base prediction panel (dollar-volume Amihud)")
    base_panel = _stage(f"base_panel_{suffix}",
                        lambda: build_prediction_panel(tickers_data, rolling_results,
                                                       horizon=21, correlation_window=30),
                        force=args.force_stage in ("panel", "all"))
    print(f"      {len(base_panel)} observations, {base_panel['ticker'].nunique()} tickers")

    print(f"\n[5/7] Enriched panel + benchmarks")
    enriched_panel = _stage(f"enriched_panel_{suffix}",
                            lambda: build_enriched_panel(base_panel, tickers_data, horizon=21),
                            force=args.force_stage in ("panel", "all"))
    benchmarks_by_ticker = _stage(f"benchmarks_{suffix}",
                                  lambda: _compute_benchmarks(tickers_data),
                                  force=args.force_stage in ("panel", "all"))
    panel = _stage(f"panel_final_{suffix}",
                   lambda: _augment_targets(_merge_benchmarks(enriched_panel, benchmarks_by_ticker)),
                   force=args.force_stage in ("panel", "all"))
    print(f"      final panel: {panel.shape}")

    print(f"\n[6/7] Running horse race for {len(TARGETS)} targets")
    target_results = {}
    for target_col, target_label in TARGETS:
        if target_col not in panel.columns:
            print(f"    [skip] {target_col}: not in panel")
            continue
        sub = panel.dropna(subset=["CII", target_col] + HURST_CONTROLS)
        if len(sub) < 100:
            print(f"    [skip] {target_col}: only {len(sub)} obs after dropna")
            continue
        focal_only = robust_panel_regression(
            sub, target=target_col, regressors=["CII"] + HURST_CONTROLS,
            extended_focal="CII" if target_col == "amihud_illiq" else None,
            wcr_n_boot=999,
        )
        sub_comb = panel.dropna(
            subset=["CII", target_col] + HURST_CONTROLS + BENCH_COLS
        )
        if len(sub_comb) >= 100:
            combined = robust_panel_regression(
                sub_comb, target=target_col,
                regressors=["CII"] + BENCH_COLS + HURST_CONTROLS,
                extended_focal="CII",
                wcr_n_boot=999,
            )
        else:
            combined = {"error": f"insufficient n={len(sub_comb)} for combined"}
        target_results[target_col] = {
            "label": target_label,
            "focal_only": focal_only,
            "combined": combined,
        }
        cii_focal = focal_only.get("coefficients", {}).get("CII", {})
        cii_comb = combined.get("coefficients", {}).get("CII", {}) if "error" not in combined else {}
        print(f"    {target_col:25s}: focal twoway t={cii_focal.get('twoway_cluster', {}).get('t', float('nan')):+.2f} "
              f"p={cii_focal.get('twoway_cluster', {}).get('p', float('nan')):.3f}  "
              f"combined twoway t={cii_comb.get('twoway_cluster', {}).get('t', float('nan')):+.2f} "
              f"p={cii_comb.get('twoway_cluster', {}).get('p', float('nan')):.3f}")

    print(f"\n[7/7] Applying decision rule")
    classifications = {}
    for target_col, res in target_results.items():
        cat = _classify(res, secondary=(target_col != "amihud_illiq"))
        classifications[target_col] = cat
        print(f"    {target_col:25s}: Category {cat}")

    # Save full results
    out_path = CACHE / f"phase2_full_results_{suffix}.pkl"
    with out_path.open("wb") as f:
        pickle.dump({
            "panel_shape": panel.shape,
            "n_firms": panel["ticker"].nunique(),
            "n_months": panel["date"].nunique(),
            "target_results": target_results,
            "classifications": classifications,
        }, f)
    print(f"\n  Saved {out_path}")
    print()
    print("Run complete.")
    return target_results, classifications


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--universe", choices=["pilot", "full"], default="pilot")
    p.add_argument("--pilot-size", type=int, default=100)
    p.add_argument("--force-stage", default="",
                   help="One of: tickers_data, rolling, panel, all")
    main(p.parse_args())
