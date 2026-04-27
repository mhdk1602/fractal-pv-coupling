#!/usr/bin/env python3
"""Horse race runner: CII vs standard liquidity benchmarks.

Extends Section H4 of the manuscript with a formal comparison of the
Coupling Intensity Index against established liquidity-state predictors.
Outputs research/horse_race/RESULTS.md with all five SE methods, three
specifications (focal-only, per-benchmark, combined), and diagnostic
tables.

Specifications follow Goyenko, Holden & Trzcinka (2009, JFE 92) §5.2,
adapted to the 50-ticker S&P 500 panel used in the main manuscript.

Usage:
    python research/horse_race/run_horse_race.py

Expected runtime: 10-20 minutes dominated by rolling dual-Hurst
estimation across 50 tickers. Intermediate results are pickled to
research/horse_race/cache/ for reuse across runs.
"""

import sys
import pickle
import warnings
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

# Allow overriding the parquet cache dir for cross-machine runs.
import os
_override_cache = os.environ.get("FRACTAL_PV_CACHE_DIR")
if _override_cache:
    import fractal_pv.data as _data_mod
    _data_mod.DEFAULT_CACHE_DIR = Path(_override_cache)

from fractal_pv.data import fetch_universe, SP500_SAMPLE
from fractal_pv.stationarity import prepare_series
from fractal_pv.rolling import rolling_dual_hurst
from fractal_pv.predict import build_prediction_panel
from fractal_pv.benchmarks import compute_all_benchmarks
from fractal_pv.inference_robust import (
    build_enriched_panel,
    horse_race_regression,
    horse_race_summary_table,
    robust_panel_regression,
)


OUTDIR = ROOT / "research" / "horse_race"
CACHEDIR = OUTDIR / "cache"
CACHEDIR.mkdir(parents=True, exist_ok=True)


def _cached(name: str):
    """Decorator factory to cache a function's output as pickle."""
    def wrap(fn):
        def inner(*args, force: bool = False, **kw):
            path = CACHEDIR / f"{name}.pkl"
            if path.exists() and not force:
                print(f"  [cache hit] {name}")
                with path.open("rb") as f:
                    return pickle.load(f)
            print(f"  [computing] {name}")
            out = fn(*args, **kw)
            with path.open("wb") as f:
                pickle.dump(out, f)
            return out
        return inner
    return wrap


# ---------------------------------------------------------------------------
# Data pipeline
# ---------------------------------------------------------------------------

@_cached("tickers_data")
def _load_tickers() -> dict:
    """Load the 50-ticker universe and wrap each entry as {'df', 'series'}.

    fetch_universe() returns a dict of bare DataFrames, but the downstream
    modules (predict, inference_robust) expect the wrapped form. This builder
    normalizes the interface.
    """
    raw = fetch_universe(SP500_SAMPLE, start="2015-01-01")
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


@_cached("rolling_results")
def _compute_rolling(tickers_data: dict) -> dict:
    """Compute rolling dual Hurst for each ticker.

    rolling_dual_hurst expects abs-log-returns and log-volume arrays, so we
    pull them from the pre-computed series dict built in _load_tickers.
    """
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
                print(f"    [{i:>2}/{total}] {ticker}: {len(dual)} windows")
        except Exception as e:
            print(f"    [warn] {ticker}: {e}")
    return rolling_results


@_cached("base_panel")
def _build_base_panel(tickers_data: dict, rolling_results: dict) -> pd.DataFrame:
    return build_prediction_panel(
        tickers_data, rolling_results, horizon=21, correlation_window=30,
    )


@_cached("benchmarks_by_ticker")
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


@_cached("enriched_panel")
def _enrich(base_panel: pd.DataFrame, tickers_data: dict) -> pd.DataFrame:
    return build_enriched_panel(base_panel, tickers_data, horizon=21)


def _merge_benchmarks(
    enriched: pd.DataFrame,
    benchmarks_by_ticker: dict,
) -> pd.DataFrame:
    """Merge per-ticker benchmark columns into the panel on (ticker, date)."""
    out_rows = []
    bench_cols = ["roll_spread", "corwin_schultz", "amihud", "turnover", "vol_of_vol"]

    for ticker, sub in enriched.groupby("ticker"):
        bench_df = benchmarks_by_ticker.get(ticker)
        if bench_df is None:
            continue
        sub = sub.copy()
        sub["date"] = pd.to_datetime(sub["date"]).astype("datetime64[ns]")
        # Use as-of merge with pad semantics.
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
        # The benchmarks module returns amihud already scaled; rename to
        # differentiate from the panel's lagged_illiq.
        merged = merged.rename(columns={"amihud": "amihud_rolling"})
        out_rows.append(merged)

    if not out_rows:
        return enriched.copy()
    return pd.concat(out_rows, ignore_index=True)


# ---------------------------------------------------------------------------
# Results writer
# ---------------------------------------------------------------------------

def _fmt(x, fmt=".3f"):
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return "—"
    return format(x, fmt)


def _specification_block(hr: dict, target: str, focal: str) -> str:
    """Markdown block for one target's horse-race result."""
    lines = []
    lines.append(f"### Target: `{target}`")
    lines.append("")
    lines.append("#### Focal alone + controls")
    focal_res = hr["focal_only"]
    if "error" not in focal_res:
        lines.append(_coef_table(focal_res, focal))

    lines.append("")
    lines.append("#### Per-benchmark regressions")
    lines.append("")
    lines.append("| Benchmark | β | t (HC1) | t (firm) | t (twoway) | p (twoway) | R² | n |")
    lines.append("|-----------|---|---------|----------|------------|------------|-----|---|")
    for per in hr["per_benchmark"]:
        if "error" in per:
            continue
        bench = per["benchmark_name"]
        c = per["coefficients"].get(bench)
        if c is None:
            continue
        lines.append(
            f"| {bench} | {_fmt(c['beta'], '.3g')} "
            f"| {_fmt(c['HC1']['t'], '.2f')} "
            f"| {_fmt(c['firm_cluster']['t'], '.2f')} "
            f"| {_fmt(c['twoway_cluster']['t'], '.2f')} "
            f"| {_fmt(c['twoway_cluster']['p'], '.4f')} "
            f"| {_fmt(per['r_squared'], '.3f')} "
            f"| {per['n']} |"
        )

    lines.append("")
    lines.append("#### Combined specification (CII + all benchmarks + controls)")
    lines.append("")
    combined = hr["combined"]
    if "error" not in combined:
        lines.append(_coef_table(combined, focal, show_all=True))
    lines.append("")
    return "\n".join(lines)


def _coef_table(res: dict, focal: str, show_all: bool = False) -> str:
    """Markdown coefficient table showing all six SE methods per regressor."""
    lines = []
    lines.append("")
    lines.append("| Variable | β | SE method | t | p | df |")
    lines.append("|----------|---|-----------|---|---|-----|")
    regressors = list(res["coefficients"].keys()) if show_all else [focal]
    methods = [
        "HC1", "firm_cluster", "time_cluster",
        "twoway_cluster", "newey_west", "driscoll_kraay",
    ]
    for reg in regressors:
        c = res["coefficients"][reg]
        for i, m in enumerate(methods):
            if m not in c:
                continue
            var_cell = f"**{reg}**" if i == 0 else ""
            beta_cell = _fmt(c["beta"], ".3g") if i == 0 else ""
            s = c[m]
            lines.append(
                f"| {var_cell} | {beta_cell} | {m} "
                f"| {_fmt(s['t'], '.2f')} "
                f"| {_fmt(s['p'], '.4f')} "
                f"| {s['df']} |"
            )
    lines.append(
        f"\n_n = {res['n']}, firms = {res['n_firms']}, "
        f"months = {res['n_months']}, R² = {_fmt(res['r_squared'], '.3f')}_"
    )
    return "\n".join(lines)


def _extended_block(extended_results: dict) -> str:
    """Markdown block for CR2 + Satterthwaite + WCR results on CII combined."""
    lines = []
    lines.append("## Publication-grade inference for CII (combined specification)")
    lines.append("")
    lines.append(
        "These are the referee-demanded small-sample corrections for the "
        "CII coefficient under the combined specification (CII + 9 "
        "benchmarks + Hurst controls). Reported per Imbens-Kolesár (2016) "
        "for CR2 + Satterthwaite df, and Cameron-Gelbach-Miller (2008) / "
        "MacKinnon-Webb (2017) for the wild cluster restricted bootstrap."
    )
    lines.append("")
    lines.append(
        "| Target | β | CR2 t | CR2 p | Satterthwaite df | WCR p (999 draws) |"
    )
    lines.append("|--------|---|-------|-------|-------------------|-------------------|")
    for target, ext_res in extended_results.items():
        e = ext_res.get("extended")
        if e is None:
            continue
        cr2 = e["cr2"]
        wcr = e["wcr_bootstrap"]
        lines.append(
            f"| `{target}` | {_fmt(e['beta'], '.3g')} "
            f"| {_fmt(cr2['t'], '.2f')} "
            f"| {_fmt(cr2['p'], '.4f')} "
            f"| {_fmt(cr2['df_satterthwaite'], '.1f')} "
            f"| {_fmt(wcr['p'], '.4f')} |"
        )
    lines.append("")
    lines.append(
        "_CR2 uses firm-level clusters with Bell-McCaffrey adjustment. "
        "WCR uses Rademacher weights and restricted-null residuals. The "
        "CR2 Satterthwaite df is typically much smaller than G_firm − 1 "
        "under unbalanced clusters; interpret the CR2 p-value as the "
        "binding small-sample-corrected inference._"
    )
    lines.append("")
    return "\n".join(lines)


def _write_results(results: dict, panel_info: dict):
    path = OUTDIR / "RESULTS.md"
    lines = []
    lines.append("# Horse Race Results: CII vs Standard Liquidity Benchmarks")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("## Panel summary")
    lines.append("")
    for k, v in panel_info.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Specifications")
    lines.append("")
    lines.append(
        "Three classes of regressions per target, following Goyenko-Holden-Trzcinka "
        "(2009, JFE 92) §5.2. All regressions include firm fixed effects via within "
        "demeaning. Degrees of freedom: HC1 and Newey-West at t(n−k); one-way clusters "
        "at t(G−1); two-way at t(min(G₁,G₂)−1). The two-way clustered t-statistic is "
        "the primary basis for inference, per Cameron-Gelbach-Miller (2011, JBES)."
    )
    lines.append("")
    lines.append("Benchmarks included:")
    lines.append("")
    lines.append("- `roll_spread` — Roll (1984) proportional effective spread")
    lines.append("- `corwin_schultz` — Corwin-Schultz (2012) MSPREAD_0 with overnight adjustment")
    lines.append("- `amihud_rolling` — Amihud (2002) illiquidity, rolling 21-day, dollar-volume, 10⁶ scaling")
    lines.append("- `turnover` — Normalized turnover (current / trailing mean)")
    lines.append("- `vol_of_vol` — Realized volatility of realized volatility")
    lines.append("- `lagged_rv` — Lagged realized volatility (past horizon)")
    lines.append("- `lagged_illiq` — Lagged Amihud over past horizon (baseline from enriched panel)")
    lines.append("- `abn_turnover_t` — Abnormal turnover spike")
    lines.append("- `vix` — Cboe VIX level")
    lines.append("")
    lines.append("## Results by target")
    lines.append("")
    for target, hr in results.items():
        if target.startswith("_"):
            continue
        lines.append(_specification_block(hr, target, focal="CII"))

    extended = results.get("_extended")
    if extended:
        lines.append(_extended_block(extended))

    lines.append("## Interpretation notes")
    lines.append("")
    lines.append(
        "1. **Primary question**: compare the CII t-statistic (twoway-clustered) "
        "between the focal-only specification and the combined specification. "
        "Material degradation indicates CII's predictive content is subsumed "
        "by one or more benchmarks."
    )
    lines.append("")
    lines.append(
        "2. **Hardest competitor**: `lagged_illiq` (the target's own past value "
        "for the Amihud target). If CII survives alongside lagged_illiq in the "
        "combined spec, the orthogonal-information claim stands."
    )
    lines.append("")
    lines.append(
        "3. **Inference layers** reported here: HC1 (reference only), firm-clustered, "
        "time-clustered, two-way clustered with CGM eigenvalue PSD adjustment, "
        "Newey-West (flagged for DK replacement), Driscoll-Kraay on daily periods "
        "with Bartlett bandwidth ≥21, CR2 + Satterthwaite df at the firm dimension, "
        "and WCR bootstrap with Rademacher weights under the restricted null. The "
        "CR2 and WCR results are the binding publication-grade inferences; the "
        "five SE methods above them are descriptive."
    )
    lines.append("")

    path.write_text("\n".join(lines))
    print(f"Wrote {path}")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def main(force: bool = False):
    print("[1/6] Loading tickers")
    tickers_data = _load_tickers(force=force)
    print(f"      {len(tickers_data)} tickers loaded")

    print("[2/6] Rolling dual-Hurst estimation (slow step)")
    rolling_results = _compute_rolling(tickers_data, force=force)
    print(f"      {len(rolling_results)} tickers with rolling Hurst")

    print("[3/6] Base prediction panel")
    base = _build_base_panel(tickers_data, rolling_results, force=force)
    print(f"      {len(base)} observations, {base['ticker'].nunique()} tickers")

    print("[4/6] Enriching panel with baseline finance controls")
    enriched = _enrich(base, tickers_data, force=force)
    print(f"      {len(enriched)} rows after enrichment")

    print("[5/6] Computing microstructure benchmarks per ticker")
    benchmarks_by_ticker = _compute_benchmarks(tickers_data, force=force)
    print(f"      {len(benchmarks_by_ticker)} ticker benchmark frames")

    print("      Merging benchmarks into panel")
    panel = _merge_benchmarks(enriched, benchmarks_by_ticker)
    panel.to_pickle(CACHEDIR / "panel_final.pkl")

    print("[6/6] Running horse race regressions")

    BENCHMARKS_ROLLING = [
        "roll_spread", "corwin_schultz", "amihud_rolling",
        "turnover", "vol_of_vol",
    ]
    BENCHMARKS_BASELINE = [
        "lagged_rv", "lagged_illiq", "abn_turnover_t", "vix",
    ]
    CONTROLS = ["H_price", "H_volume"]
    TARGETS = ["amihud_illiq", "realized_vol"]

    results = {}
    for target in TARGETS:
        if target not in panel.columns:
            print(f"      [skip] target {target} not in panel")
            continue
        all_benchmarks = BENCHMARKS_ROLLING + BENCHMARKS_BASELINE
        present = [b for b in all_benchmarks if b in panel.columns]
        missing = [b for b in all_benchmarks if b not in panel.columns]
        if missing:
            print(f"      [note] missing columns for {target}: {missing}")

        subset = panel.dropna(subset=present + CONTROLS + [target, "CII"]).copy()
        print(f"      {target}: n={len(subset)} after dropna")

        hr = horse_race_regression(
            subset,
            target=target,
            focal_regressor="CII",
            benchmark_regressors=present,
            controls=CONTROLS,
        )
        results[target] = hr

    # Extended inference (CR2 + Satterthwaite; WCR bootstrap) for the CII
    # coefficient under the combined specification. These per-regressor
    # computations are the publication-grade SE methods recommended by
    # Imbens-Kolesár (2016) and MacKinnon-Nielsen-Webb (2023) at G_firm = 50.
    print("      Running extended inference (CR2 + WCR) for CII combined spec")
    extended_results = {}
    for target in TARGETS:
        if target not in panel.columns:
            continue
        present = [b for b in BENCHMARKS_ROLLING + BENCHMARKS_BASELINE if b in panel.columns]
        subset = panel.dropna(subset=present + CONTROLS + [target, "CII"]).copy()
        print(f"        {target}: CR2 + WCR on combined spec (n={len(subset)})")
        ext = robust_panel_regression(
            subset,
            target=target,
            regressors=["CII"] + present + CONTROLS,
            extended_focal="CII",
            wcr_n_boot=999,
        )
        extended_results[target] = ext
    results["_extended"] = extended_results

    panel_info = {
        "tickers (after rolling + enrichment)": panel["ticker"].nunique(),
        "total rows": len(panel),
        "date range": (
            f"{pd.to_datetime(panel['date'].min()).date()} to "
            f"{pd.to_datetime(panel['date'].max()).date()}"
        ),
        "benchmarks available": ", ".join([
            b for b in BENCHMARKS_ROLLING + BENCHMARKS_BASELINE
            if b in panel.columns
        ]),
    }

    _write_results(results, panel_info)
    print("Done.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true", help="Bypass all caches")
    args = p.parse_args()
    main(force=args.force)
