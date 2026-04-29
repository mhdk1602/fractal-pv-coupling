# Phase 2 Pre-Registration Protocol

**Version**: 1.0
**Created**: 2026-04-28
**Status**: pre-registered before any G > 50 data fetch
**Author**: Dineshkumar Malempati Hari

This document fixes the Phase 2 specification *before* the larger-universe
analysis runs. It exists so that ex-post outcomes cannot be reframed: every
decision rule, threshold, and acceptance criterion is committed here and
the analysis script (`research/horse_race/run_phase2.py`, to be created)
will execute exactly this protocol.

---

## 1. Purpose

Phase 2 is a **test, not a rescue**. The v1.2.0 manuscript reports a
robust predictive null for the Coupling Intensity Index (CII) at G = 50
firms across ten target specifications and three small-sample-corrected
inference methods. Phase 2 asks one question only:

> Does the predictive null persist when the universe is expanded to the
> current full S&P 500 constituency, or does a clean signal emerge that
> survives both standard convention (dollar-volume Amihud) and
> dependence-robust inference?

There is no version of Phase 2 that reframes the v1.2.0 null as something
else. Either the null is confirmed at higher power, or a new positive
result emerges that meets the criteria fixed below.

---

## 2. Universe and sample

### 2.1 Tickers

- Universe: current (April 2026) S&P 500 constituents.
- Source for the ticker list: Wikipedia "List of S&P 500 companies" snapshot,
  or equivalent published list, recorded as a frozen CSV in
  `data/sp500_constituents_2026-04-28.csv` before any fetch.
- Approximate count: ~503 unique tickers (S&P 500 includes a few firms
  with dual share classes).

### 2.2 Time period

- Start date: 2015-01-01 (matching v1.2.0).
- End date: 2026-04-01 (matching v1.2.0).
- Daily OHLCV from Yahoo Finance via `yfinance`.

### 2.3 Inclusion criteria

A ticker is included in the Phase 2 panel if:

- It returns at least 600 trading-day observations of OHLCV from Yahoo
  Finance over the window.
- ADF and KPSS stationarity tests on the log-returns series pass at the
  pre-registered thresholds (matching v1.2.0).
- The price series has no zero or missing volumes for >5% of trading days.

Tickers failing any of the above are excluded with a recorded reason
in the run log. The expected effective universe is 400–500 firms. The
analysis is robust to any G in that range.

### 2.4 Survivorship-bias note

Using the current April 2026 constituency excludes firms that were dropped
from the index between 2015 and 2026 (e.g., bankruptcies, acquisitions).
This is the same survivorship-bias pattern as v1.2.0 and is disclosed
identically. Phase 2 does not attempt point-in-time membership because the
authoritative source (CRSP) is paywalled and the fix would require WRDS
access.

---

## 3. Pipeline (frozen)

The Phase 2 pipeline reuses `src/fractal_pv/` exactly as committed at
master HEAD `f8aa564`. No code changes between protocol freeze and Phase 2
run except as needed for batch-scale data fetching. Specifically:

1. `fractal_pv.data.fetch_universe` — extended for batch yfinance pulls
   with retry/throttling; all other arguments unchanged.
2. `fractal_pv.stationarity.prepare_series` — unchanged.
3. `fractal_pv.rolling.rolling_dual_hurst` — unchanged.
   - Window `W = 500` trading days, step `Δ = 20`.
4. `fractal_pv.predict.compute_coupling_intensity` — unchanged.
   - CII window `L = 30` rolling-Hurst observations.
5. `fractal_pv.predict.compute_forward_metrics` — unchanged.
   - Horizon `h = 21` trading days.
   - **Amihud illiquidity uses dollar volume in the denominator**
     (`|r| / (V × P)`, scaled by 1e6), per the v1.2.0 standard.
6. `fractal_pv.benchmarks.compute_all_benchmarks` — unchanged.
   - Roll, Corwin-Schultz MSPREAD_0, dollar-volume Amihud, turnover,
     vol-of-vol.
7. `fractal_pv.inference_robust.robust_panel_regression` — unchanged.
   - Six baseline SE methods plus CR2 + Satterthwaite + WCR for the focal
     coefficient.

Any code change after this protocol date that affects estimated
coefficients or inference will be flagged in the Phase 2 results document
with explicit before/after comparison.

---

## 4. Targets, primary and secondary

### 4.1 Primary outcome

- **Forward dollar-volume Amihud illiquidity** at $h = 21$ trading days.
  This matches the v1.2.0 primary outcome and is the canonical target.

### 4.2 Secondary outcomes (pre-specified)

The same ten target specifications used in the v1.2.0 battery, in the
same order:

1. Standard dollar-volume Amihud (primary)
2. log Amihud
3. ΔAmihud (forward minus contemporaneous)
4. Forward Corwin-Schultz spread
5. Forward Roll spread
6. Forward vol-of-vol
7. Realised volatility
8. Maximum drawdown
9. Abnormal turnover
10. *(reserved for one new outcome if the literature suggests one before the run; if added, recorded here before fetch)*

**Pre-registered prior**: the forward Corwin-Schultz spread is the most
likely candidate to recover signal at higher G, because at G = 50 it
already crosses 5% under firm-only clustering and reaches HC1 t = 4.04.
That observation does not change the criteria below; it is recorded here
to be transparent about which target I would be unsurprised to see
recover.

---

## 5. Decision rule (pre-committed)

For each target, the Phase 2 result is one of three categories:

### 5.1 Category A — "Predictive null confirmed"

The two-way clustered $p$-value > 0.10 *and* the Driscoll-Kraay
$p$-value > 0.10 *and* the wild cluster restricted bootstrap $p$-value
> 0.10, all in the focal-only specification with Hurst controls.

### 5.2 Category B — "Robust signal recovered"

The two-way clustered $p$-value < 0.05 *and* the Driscoll-Kraay
$p$-value < 0.05 *and* the wild cluster restricted bootstrap
$p$-value < 0.05 *and* the Bell-McCaffrey CR2 $p$-value < 0.10, all in
the combined-with-9-benchmarks specification, *and* the sign of the
coefficient matches the focal-only specification, *and* the coefficient
magnitude is at least 25% as large as the focal-only estimate.

The "in the combined specification" requirement is binding. A signal
that appears in focal-only but vanishes in combined is not Category B;
it is Category C.

### 5.3 Category C — "Borderline / mixed"

Anything between A and B. Examples: strong under HC1 but null under
two-way; strong in focal-only but null in combined; strong under WCR
but null under CR2 and Driscoll-Kraay.

### 5.4 Per-target decisions

| Primary outcome (Amihud) | Action |
|---|---|
| A (null confirmed) | Phase 2 Amihud null becomes the headline. Submit to Physica A. |
| B (robust signal) | Reframe paper around the recovered signal. Reconsider QF as primary venue. |
| C (mixed) | Report transparently, do not promote the signal to a headline. Likely Physica A or strong preprint only. |

| Any secondary outcome | Action |
|---|---|
| A | Confirms v1.2.0 null. No reframing. |
| B | Discuss in the manuscript as a *secondary* finding, do not promote to headline (because it would be one of nine and would face multiple-testing scrutiny). |
| C | Mention in robustness; do not feature. |

| H2 (within-firm temporal coupling) at G = 500 | Action |
|---|---|
| Mean within-firm $r > 0.5$ with > 80% of firms positive | H2 confirmed at G=500; descriptive contribution intact. |
| Mean $r$ between 0.3 and 0.5 with 60-80% positive | H2 weakened; reframe as "moderate large-cap-skewed phenomenon." |
| Mean $r < 0.3$ or < 60% positive | H2 was a 50-firm artifact. Stop. Leave SSRN as the artifact. |

These thresholds are fixed in advance and will not be adjusted after
seeing results.

---

## 6. Multiple-testing position

The primary outcome (forward dollar-volume Amihud) is the only outcome
that can carry the headline. The other nine targets are exploratory
robustness checks. If exactly one of the nine secondary outcomes reaches
Category B, it will be reported transparently but described as an
exploratory finding requiring independent replication, not a confirmed
result.

If two or more secondary outcomes reach Category B with consistent signs,
that is *prima facie* evidence of a recovered signal and the manuscript
will be reframed accordingly, with Bonferroni-adjusted $p$-values reported
for the family.

---

## 7. Inference rigor

The full v1.2.0 inference menu carries to Phase 2 unchanged:

- HC1 (reference only).
- Firm-clustered $t(G_{\text{firm}} - 1)$.
- Time-clustered $t(G_{\text{month}} - 1)$.
- Two-way clustered with Cameron-Gelbach-Miller (2011) eigenvalue PSD adjustment.
- Newey-West, Bartlett bandwidth (reference only).
- Driscoll-Kraay (1998), Bartlett bandwidth ≥ 21.
- Bell-McCaffrey CR2 with Satterthwaite df at the firm dimension (Imbens-Kolesár 2016).
- Wild cluster restricted bootstrap with 999 Rademacher resamples (Cameron-Gelbach-Miller 2008; MacKinnon-Webb 2017).

At G ≈ 500 the Satterthwaite df should rise sharply versus the 4.4–6.3
observed at G = 50; this is mechanical and pre-expected. It is the only
inference change anticipated, and it is the reason Phase 2 is a fair test
of the "Was the v1.2.0 null a small-sample artifact?" question.

---

## 8. What is *not* allowed after the protocol freeze

To prevent ex-post moving of goalposts:

- No adding new targets after the run unless the addition is pre-disclosed
  here and the Phase 2 runner is rerun.
- No changing window parameters (`W`, `Δ`, `L`, `h`) after the run.
- No subsetting tickers after the run except for the documented inclusion
  criteria in §2.3.
- No swapping inference methods after the run except to add a method I
  did not previously implement (which would be reported as additive, not
  substitutive).
- No reframing a Category C outcome as Category B by changing the
  thresholds.

---

## 9. Compute and runtime budget

- Data fetch: ~30–60 minutes for 500 tickers at 1-day resolution from
  Yahoo Finance via batched yfinance pulls with throttling and retry.
- Stationarity + rolling Hurst: ~4–6 hours on this workstation
  (~110 rolling windows × 500 firms × 2 series × DFA fit).
- Predictive panel + horse-race: ~30 minutes.
- CR2 + WCR for Phase 2: ~15–30 minutes (WCR scales linearly with sample).
- **Total**: ~6–8 hours of wall-clock; runs overnight comfortably.

Storage:
- `data/raw/` parquet cache will grow to ~2 GB.
- `research/horse_race/cache/phase2_*.pkl` for intermediate results.

---

## 10. Output artifacts

After the Phase 2 run completes, three artifacts are produced:

1. `research/horse_race/PHASE2_RESULTS.md` — primary deliverable. Contains
   the headline numbers, all ten target specifications across all
   inference methods, the decision-rule outcome per target, and the
   recommended action.
2. Updated `research/horse_race/cache/phase2_*.pkl` files for full
   reproducibility.
3. A pre-draft of the v1.3.0 manuscript update (no commit yet, just a
   working document at `research/paper/main_phase2_draft.tex`) that I
   can review before deciding to ship.

The decision on whether to commit a v1.3.0 release happens *after* I read
the Phase 2 results, not before.
