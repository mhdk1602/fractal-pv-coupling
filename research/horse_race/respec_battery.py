#!/usr/bin/env python3
"""Respecification battery for D10 fallout.

Switching to dollar-volume Amihud killed the original headline. This script
tests whether any clean predictive signal survives under alternative target
specifications, before pivoting the paper to a null-result framing.

Tests:
  A. log(amihud_illiq)              transform skewness
  B. delta_amihud                   forward minus contemporaneous
  C. fwd_corwin_schultz             effective spread as primary outcome
  D. fwd_roll_spread                Roll spread as primary outcome
  E. fwd_vol_of_vol                 vol-of-vol target
  F. fwd_amihud_rolling             rolling-Amihud benchmark as target
  G. max_drawdown                   already in panel
  H. abnormal_turnover              already in panel

Each runs both focal-only (CII + Hurst controls) and combined (CII +
9 benchmarks + Hurst controls). Driscoll-Kraay reported alongside the
five baseline SEs. CR2 + WCR computed for the focal-only spec only,
to economise on bootstrap time.
"""

import sys
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fractal_pv.inference_robust import robust_panel_regression


CACHE = ROOT / "research" / "horse_race" / "cache"
panel = pickle.load(open(CACHE / "panel_final.pkl", "rb"))
panel = panel.sort_values(["ticker", "date"]).copy()

# --- Target construction ---

panel["log_amihud"] = np.log(panel["amihud_illiq"].clip(lower=1e-12))
panel["delta_amihud"] = panel.groupby("ticker")["amihud_illiq"].diff()
# Forward shifts: panel is monthly-stepped (~20 trading days), so shift by -1 row
# approximates a one-month-forward window. The benchmark columns are computed
# on the same calendar grid via pd.merge_asof, so a 1-row forward shift matches
# the existing 21-day forward horizon.
for col in ["corwin_schultz", "roll_spread", "vol_of_vol", "amihud_rolling"]:
    panel[f"fwd_{col}"] = panel.groupby("ticker")[col].shift(-1)

targets = [
    ("amihud_illiq", "amihud_illiq (level dollar Amihud, primary)"),
    ("log_amihud", "log dollar Amihud"),
    ("delta_amihud", "ΔAmihud (forward − contemporaneous)"),
    ("fwd_corwin_schultz", "forward Corwin-Schultz spread"),
    ("fwd_roll_spread", "forward Roll spread"),
    ("fwd_vol_of_vol", "forward vol-of-vol"),
    ("fwd_amihud_rolling", "forward rolling-Amihud"),
    ("realized_vol", "realised vol (already null)"),
    ("max_drawdown", "max drawdown"),
    ("abnormal_turnover", "abnormal turnover"),
]

bench_cols = [
    "roll_spread", "corwin_schultz", "amihud_rolling", "turnover",
    "vol_of_vol", "lagged_rv", "lagged_illiq", "abn_turnover_t", "vix",
]
hurst_controls = ["H_price", "H_volume"]
focal = "CII"


def _summary(res: dict, label: str) -> str:
    """One-line summary of a regression: focal coefficient and t under each SE."""
    if "error" in res:
        return f"{label}: ERROR {res.get('error')}"
    c = res["coefficients"][focal]
    parts = [f"β={c['beta']:+.3g}"]
    for m in ["HC1", "firm_cluster", "twoway_cluster", "driscoll_kraay"]:
        if m in c:
            s = c[m]
            star = ""
            if s["p"] < 0.01:
                star = "***"
            elif s["p"] < 0.05:
                star = "**"
            elif s["p"] < 0.10:
                star = "*"
            parts.append(f"{m[:6]} t={s['t']:+.2f}({star or '·'})")
    parts.append(f"R²={res['r_squared']:.3f}")
    parts.append(f"n={res['n']}")
    return f"{label}: " + "  ".join(parts)


def _run(target: str) -> dict:
    """Run focal-only and combined specifications for a single target."""
    out = {"target": target}
    sub = panel.dropna(subset=[focal, target] + hurst_controls).copy()
    if len(sub) < 100:
        out["error"] = f"insufficient n={len(sub)}"
        return out

    # Focal-only: CII + Hurst controls
    out["focal_only"] = robust_panel_regression(
        sub, target=target, regressors=[focal] + hurst_controls,
    )

    # Combined: CII + 9 benchmarks + Hurst controls
    sub_comb = panel.dropna(
        subset=[focal, target] + hurst_controls + bench_cols
    ).copy()
    if len(sub_comb) >= 100:
        out["combined"] = robust_panel_regression(
            sub_comb,
            target=target,
            regressors=[focal] + bench_cols + hurst_controls,
        )
    return out


print("=" * 100)
print("RESPECIFICATION BATTERY: hunting for any clean CII signal under standard Amihud convention")
print("=" * 100)
print()

results = {}
for target, label in targets:
    print(f"--- {label} (col: {target}) ---")
    r = _run(target)
    if "error" in r:
        print(f"  {r['error']}")
        print()
        continue
    if "focal_only" in r and "error" not in r["focal_only"]:
        print("  " + _summary(r["focal_only"], "FOCAL "))
    if "combined" in r and "error" not in r.get("combined", {}):
        print("  " + _summary(r["combined"], "COMBND"))
    print()
    results[target] = r

# Save results for follow-up
with open(ROOT / "research" / "horse_race" / "cache" / "respec_results.pkl", "wb") as f:
    pickle.dump(results, f)

print()
print("=" * 100)
print("HEADLINE TABLE: focal-only CII coefficient and twoway-clustered significance per target")
print("=" * 100)
print(f"{'target':30s}  {'β':>11s}  {'twoway t':>10s}  {'p':>8s}  {'R²':>6s}")
for target, label in targets:
    r = results.get(target)
    if r is None or "focal_only" not in r or "error" in r["focal_only"]:
        continue
    c = r["focal_only"]["coefficients"][focal]
    if "twoway_cluster" in c:
        s = c["twoway_cluster"]
        marker = " <-- SURVIVOR" if s["p"] < 0.05 else ""
        print(f"{target:30s}  {c['beta']:+11.3g}  {s['t']:+10.2f}  {s['p']:8.4f}  {r['focal_only']['r_squared']:6.3f}{marker}")

print()
print("=" * 100)
print("HEADLINE TABLE (combined w/ 9 benchmarks): same metric")
print("=" * 100)
print(f"{'target':30s}  {'β':>11s}  {'twoway t':>10s}  {'p':>8s}  {'R²':>6s}")
for target, label in targets:
    r = results.get(target)
    if r is None or "combined" not in r or "error" in r.get("combined", {}):
        continue
    c = r["combined"]["coefficients"][focal]
    if "twoway_cluster" in c:
        s = c["twoway_cluster"]
        marker = " <-- SURVIVOR" if s["p"] < 0.05 else ""
        print(f"{target:30s}  {c['beta']:+11.3g}  {s['t']:+10.2f}  {s['p']:8.4f}  {r['combined']['r_squared']:6.3f}{marker}")
