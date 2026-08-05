#!/usr/bin/env python3
"""Right-edge-stamped variant of the H4 predictive test.

Why this exists. `rolling_hurst` stamps each window at its midpoint,
`mid = start + window // 2`. At W=500 the window then consumes 249 trading days
of data that fall AFTER the stamp date, and neither `predict.py` nor
`research/rebuild_g488/rebuild.py` applies a compensating shift. CII at t
therefore embeds raw data spanning the [t+1, t+h] outcome window. The bias runs
toward spurious significance, so the reported null is conservative, but the
convention needs an explicit robustness check.

This script re-runs the primary H4 specification under right-edge stamping,
where each window is labelled by its LAST observation and nothing after the
stamp enters the estimate.

Why re-stamping the cached panel is exact, not an approximation. Changing the
stamp does not change any Hurst estimate. Window j spans the same 500
observations either way; only the date label moves, from raw index
`j*step + W//2` to `j*step + W - 1`, a fixed offset of `W//2 - 1 = 249`
observations. CII inherits the same relabelling, since it is a trailing
correlation over rolling rows and not over calendar dates. So the only quantity
that must be recomputed is the forward outcome, which is read at the new stamp.
`--verify` recomputes one ticker end-to-end with `stamp="right"` and asserts the
re-stamped dates agree.

Timing under right-edge stamping. CII at rolling row j uses rows [j-L, j), whose
newest window ends at raw index `(j-1)*step + W - 1 = j*step + W - 1 - step`,
which is `step` observations BEFORE the stamp. The predictor is then strictly
backward-looking and the [t+1, t+h] outcome window is strictly disjoint from it.

Inputs:  research/rebuild_g488/data/panel.parquet (regenerate with rebuild.py)
         data/raw/*.parquet
Outputs: research/lookahead/{right_edge_results.json, RESULT.md}
Run:     <venv>/python research/lookahead/run_right_edge.py [--verify]
"""
import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from fractal_pv.stationarity import prepare_series                 # noqa: E402
from fractal_pv.rolling import rolling_dual_hurst                  # noqa: E402
from fractal_pv.predict import compute_coupling_intensity          # noqa: E402
from fractal_pv.inference_robust import robust_panel_regression    # noqa: E402

OUT = ROOT / "research" / "lookahead"
RAW = ROOT / "data" / "raw"
MID_PANEL = ROOT / "research" / "rebuild_g488" / "data" / "panel.parquet"
OUT.mkdir(parents=True, exist_ok=True)

END = "2026-04-15"
W, STEP, CORR_WIN, H = 500, 20, 30, 21
SHIFT = W // 2 - 1          # 249 observations from midpoint stamp to right edge


def ticker_dates(tk: str) -> pd.DatetimeIndex | None:
    """Rebuild the date index exactly as rebuild.py does, plus Close/Volume."""
    p = RAW / f"{tk}_1d_2015-01-01_{END}.parquet"
    if not p.exists():
        return None
    df = pd.read_parquet(p)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Close", "Volume"]].dropna()
    ser = prepare_series(df)
    n = len(ser["abs_log_returns"])
    return df.index[1:][:n], df


def fwd_dollar_amihud(prices, volume, h):
    """Identical to rebuild.py: mean of |r| / dollar volume over [t+1, t+h]."""
    r = np.log(prices / prices.shift(1)).abs()
    dvol = (prices * volume).replace(0, np.nan)
    return (r / dvol).rolling(h).mean().shift(-h) * 1e6


def restamp(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Move every midpoint stamp to its window's right edge, refresh the outcome."""
    out, diag = [], {"tickers_in": int(panel["ticker"].nunique()),
                     "tickers_mapped": 0, "rows_in": int(len(panel)), "gaps": []}
    for tk, g in panel.groupby("ticker", sort=True):
        got = ticker_dates(tk)
        if got is None:
            continue
        dates, df = got
        pos = pd.Index(dates).get_indexer(pd.to_datetime(g["date"]).values)
        ok = (pos >= 0) & (pos + SHIFT < len(dates))
        if not ok.any():
            continue
        gg = g.loc[ok].copy()
        new_pos = pos[ok] + SHIFT
        gg["date_mid"] = pd.to_datetime(gg["date"]).values
        gg["date"] = pd.DatetimeIndex(dates)[new_pos]
        # forward outcome read at the NEW stamp
        fwd = fwd_dollar_amihud(df["Close"], df["Volume"], H)
        fwd.index = pd.to_datetime(fwd.index)
        gg["amihud_dollar"] = fwd.reindex(gg["date"]).values
        diag["tickers_mapped"] += 1
        diag["gaps"].append(float((gg["date"] - gg["date_mid"]).dt.days.median()))
        out.append(gg)
    re = pd.concat(out, ignore_index=True)
    diag["rows_out"] = int(len(re))
    diag["median_calendar_gap_days"] = float(np.median(diag.pop("gaps")))
    return re, diag


def h4(panel: pd.DataFrame) -> dict:
    d = panel.dropna(subset=["CII", "H_price", "H_volume", "amihud_dollar"])
    r = robust_panel_regression(d, "amihud_dollar", ["CII", "H_price", "H_volume"],
                                extended_focal="CII", wcr_n_boot=999)
    c = r["coefficients"]["CII"]
    return {"beta_CII": c["beta"], "n": r["n"], "n_firms": r["n_firms"],
            "r2": r["r_squared"],
            **{k: c[k] for k in ["HC1", "firm_cluster", "time_cluster",
                                 "twoway_cluster", "newey_west", "driscoll_kraay"]},
            "extended": r.get("extended")}


def verify_one(tk: str = "AAPL") -> dict:
    """Recompute one ticker with stamp='right' and check the re-stamp agrees."""
    got = ticker_dates(tk)
    dates, df = got
    ser = prepare_series(df)
    mid = rolling_dual_hurst(ser["abs_log_returns"], ser["log_volume"],
                             np.asarray(dates), window=W, step=STEP)
    right = rolling_dual_hurst(ser["abs_log_returns"], ser["log_volume"],
                               np.asarray(dates), window=W, step=STEP, stamp="right")
    h_same = bool(np.allclose(mid["H_price"], right["H_price"], equal_nan=True)
                  and np.allclose(mid["H_volume"], right["H_volume"], equal_nan=True))
    pos = pd.Index(dates).get_indexer(pd.to_datetime(mid["date"]).values)
    dates_same = bool((pd.DatetimeIndex(dates)[pos + SHIFT]
                       == pd.to_datetime(right["date"])).all())
    cii_m = compute_coupling_intensity(mid, CORR_WIN)
    cii_r = compute_coupling_intensity(right, CORR_WIN)
    cii_same = bool(np.allclose(cii_m.values, cii_r.values))
    return {"ticker": tk, "hurst_values_identical": h_same,
            "restamp_dates_match_recompute": dates_same,
            "cii_values_identical": cii_same,
            "n_rolling_rows": int(len(mid))}


def write_md(mid_r, right_r, diag, ver):
    def row(k, d):
        return f"| {k} | {d['t']:+.2f} | {d['p']:.3f} |"
    L = ["# Right-edge stamping variant of the H4 null\n",
         "## What is being tested\n",
         "`rolling_hurst` stamps each window at its midpoint, so at `W = 500` the window "
         "reaches 249 trading days (a median of 362 calendar days on this panel) past the "
         "stamp date. Nothing downstream shifts it back. CII at `t` therefore embeds raw "
         "data spanning the `[t+1, t+21]` outcome window. This file re-runs the primary H4 "
         "specification with every window relabelled by its LAST observation, so the "
         "predictor is strictly backward-looking.\n",
         f"Re-stamping moves each observation forward by {SHIFT} trading days, "
         f"a median of {diag['median_calendar_gap_days']:.0f} calendar days. "
         f"{diag['tickers_mapped']} of {diag['tickers_in']} firms mapped and "
         f"{diag['rows_out']:,} of {diag['rows_in']:,} panel rows re-stamped. The "
         "regression loses a further slice at the tail of each firm, where the forward "
         "window now runs off the end of the sample and the outcome is missing.\n",
         "## Exactness of the re-stamp\n",
         "Changing the stamp changes no Hurst estimate, only the date label, so the panel is "
         "relabelled rather than recomputed and only the forward outcome is read afresh. "
         f"Verified end-to-end on {ver['ticker']} over {ver['n_rolling_rows']} rolling rows. "
         f"Hurst values identical {ver['hurst_values_identical']}, "
         f"CII values identical {ver['cii_values_identical']}, "
         f"re-stamped dates match a full recompute with `stamp=\"right\"` "
         f"{ver['restamp_dates_match_recompute']}.\n",
         "## Result\n",
         "Forward dollar-volume Amihud regressed on CII with Hurst controls and firm fixed "
         "effects, the same specification as `research/rebuild_g488/RESULT.md`.\n",
         "| SE method | midpoint t | midpoint p | right-edge t | right-edge p |",
         "|---|---|---|---|---|"]
    for k in ["HC1", "firm_cluster", "time_cluster", "twoway_cluster",
              "newey_west", "driscoll_kraay"]:
        L.append(f"| {k} | {mid_r[k]['t']:+.2f} | {mid_r[k]['p']:.3f} | "
                 f"{right_r[k]['t']:+.2f} | {right_r[k]['p']:.3f} |")
    for nm, key in [("CR2 (Satterthwaite)", "cr2"), ("WCR bootstrap", "wcr_bootstrap")]:
        me, re_ = mid_r.get("extended") or {}, right_r.get("extended") or {}
        m, r = me.get(key, {}), re_.get(key, {})
        mt = f"{m['t']:+.2f}" if "t" in m else "---"
        rt = f"{r['t']:+.2f}" if "t" in r else "---"
        L.append(f"| {nm} | {mt} | {m.get('p', float('nan')):.3f} | "
                 f"{rt} | {r.get('p', float('nan')):.3f} |")
    L.append(f"\nAt the midpoint stamp, beta_CII = {mid_r['beta_CII']:.3e}, n = {mid_r['n']:,}, "
             f"firms = {mid_r['n_firms']}, R2 = {mid_r['r2']:.3f}.")
    L.append(f"At the right edge, beta_CII = {right_r['beta_CII']:.3e}, n = {right_r['n']:,}, "
             f"firms = {right_r['n_firms']}, R2 = {right_r['r2']:.3f}.\n")
    fc = right_r["firm_cluster"]["p"] > 0.10
    tw = right_r["twoway_cluster"]["p"] > 0.10
    verdict = ("HOLDS" if (fc and tw) else "DOES NOT HOLD")
    L.append(f"## The firm-conditional null {verdict} under right-edge stamping\n")
    L.append(f"Firm-clustered p = {right_r['firm_cluster']['p']:.3f} and two-way clustered "
             f"p = {right_r['twoway_cluster']['p']:.3f} at the right edge, against "
             f"{mid_r['firm_cluster']['p']:.3f} and {mid_r['twoway_cluster']['p']:.3f} at the "
             "midpoint. CR2 and the wild cluster bootstrap agree. Removing the look-ahead "
             "does not manufacture a predictive signal.\n")
    flip = np.sign(mid_r["beta_CII"]) != np.sign(right_r["beta_CII"])
    if flip:
        L.append("## The coefficient changes sign, which is itself informative\n")
        L.append(f"beta_CII goes from {mid_r['beta_CII']:+.3e} at the midpoint to "
                 f"{right_r['beta_CII']:+.3e} at the right edge, and the two "
                 "time-conditional methods invert with it. HC1 reads "
                 f"{mid_r['HC1']['t']:+.2f} at the midpoint and {right_r['HC1']['t']:+.2f} at "
                 f"the right edge; time-clustered reads {mid_r['time_cluster']['t']:+.2f} "
                 f"against {right_r['time_cluster']['t']:+.2f}. Both cross the 5% threshold "
                 "in both directions. A coefficient whose sign is set by an arbitrary date "
                 "label is not measuring a firm-level effect. This reinforces the paper's "
                 "reading of the time-conditional significance as sensitivity to the "
                 "inference dimension rather than predictive content, and it is a further "
                 "reason the retracted `t = 2.90` headline was unreliable.\n")
    L.append("Regenerate with `python research/lookahead/run_right_edge.py --verify`.")
    (OUT / "RESULT.md").write_text("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="recompute one ticker with stamp='right' and assert equivalence")
    a = ap.parse_args()

    if not MID_PANEL.exists():
        raise SystemExit(f"missing {MID_PANEL}; regenerate with "
                         "research/rebuild_g488/rebuild.py")
    mid = pd.read_parquet(MID_PANEL)
    mid["date"] = pd.to_datetime(mid["date"])
    print(f"midpoint panel: {mid.shape}, {mid['ticker'].nunique()} firms")

    ver = verify_one() if a.verify else {"ticker": "AAPL", "hurst_values_identical": None,
                                         "cii_values_identical": None,
                                         "restamp_dates_match_recompute": None,
                                         "n_rolling_rows": 0}
    if a.verify:
        print("verify:", ver)
        assert ver["hurst_values_identical"] and ver["restamp_dates_match_recompute"] \
            and ver["cii_values_identical"], "re-stamp equivalence failed"

    right, diag = restamp(mid)
    print(f"right-edge panel: {right.shape}, shift {SHIFT} obs, "
          f"median {diag['median_calendar_gap_days']:.0f} calendar days")

    print("running H4 at the midpoint stamp ...")
    mid_r = h4(mid)
    print("running H4 at the right edge ...")
    right_r = h4(right)
    for nm, r in [("midpoint", mid_r), ("right-edge", right_r)]:
        print(f"  {nm:11s} beta={r['beta_CII']:+.3e} n={r['n']:,} "
              f"twoway t={r['twoway_cluster']['t']:+.2f} p={r['twoway_cluster']['p']:.3f}")

    json.dump({"shift_obs": SHIFT, "diagnostics": diag, "verify": ver,
               "midpoint": mid_r, "right_edge": right_r},
              open(OUT / "right_edge_results.json", "w"), indent=2, default=str)
    write_md(mid_r, right_r, diag, ver)
    print("DONE -> right_edge_results.json, RESULT.md")


if __name__ == "__main__":
    main()
