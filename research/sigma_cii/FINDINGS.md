# σ(CII) make-or-break, findings and decision

> **This is the ORIGINAL G=51 run of 2026-05-28, kept as the record of first
> result.** It is not reproducible as it stands, because the script globbed
> whatever `data/raw/` happened to hold that day. The universe is now pinned by
> an explicit ticker file plus a written manifest, and the "one confirmation
> worth running" flagged in the Caveats below has been run at the full available
> universe. See `CONFIRMATION_FULL.md` for that result and treat it as the
> current statement. Note also that the `r̄ ≈ 0.665` quoted below is the
> superseded 50-firm pilot figure; the `G = 488` value is `0.531`.

**Run date:** 2026-05-28. **Universe:** 51 large-cap S&P 500 names (the validated primary universe, on-disk parquet cache). **Frequency:** rolling-Hurst dates, W=500/step=20, CII trailing window=30 → 87 ~monthly observations, 2018-05 to 2025-03 (the COVID crash is inside the window). **Stress measures:** VIX and log-VIX (yfinance), realized S&P 500 vol (SPY, 21d), high-yield credit stress (HYG, 21d realized vol), Pástor-Stambaugh non-traded liquidity innovations (sign-flipped to an illiquidity/stress reading), monthly through Dec 2024.

## Verdict: NULL. σ(CII) is not a market-stress signal.

The reframe hypothesis was that the cross-sectional dispersion of price-volume coupling, σ(CII)_t, rises before or with market stress and could serve as an early-warning object — the positive headline the firm-level CII null (two-way clustered t = −0.93 on forward dollar-volume Amihud) never delivered. The data do not support it.

**1. No lead.** Granger causality (first differences, lags 1-4) is null in both directions for every stress measure (min p ≥ 0.38 for σ→stress; ≥ 0.12 for stress→σ). The apparent lag-6 cross-correlation peaks (VIX −0.33, HYG −0.38) are negative-signed and are the expected artifact of correlating two highly persistent series at long lags; Granger removes them. No predictive regression of forward stress on σ(CII)_t survives once the lagged stress level is controlled (the lone hyg_rv h=6 coefficient, t=−2.20, is isolated across h, wrong-signed for an early-warning story, and unremarkable among 15 tests).

**2. No contemporaneous relationship for the dispersion.** σ(CII) vs each stress measure in levels: |Pearson| ≤ 0.18, none significant at 5% (VIX −0.14 p=0.20; HYG −0.18 p=0.10). In first differences: |r| ≤ 0.13, all p ≥ 0.23.

**3. The mean does co-move in levels, but it is a spurious trend.** The cross-sectional MEAN of CII tracks stress in levels (vs log-VIX +0.54, vs VIX +0.47, vs SPY-RV +0.31, all p<0.01) — which contradicts the planning note's claim that mean-CII vs VIX was ≈0.057 (a G=488 figure; the level correlation is clearly universe- and trend-sensitive). But mean-CII has AR(1)=0.986, near a random walk. In first differences the co-movement collapses to +0.03 (p=0.79) against log-VIX and is null for every measure. This is a classic spurious-regression result (Granger-Newbold): the levels correlation reflects shared trending, not a relationship between innovations.

## What this means for the flagship

- **Do not headline σ(CII) as a stress signal**, and do not pursue the Chaos, Solitons & Fractals "dispersion leads stress" route on this evidence. The decision rule's outcome is the structured precise null.
- **The honest contribution stands where it already was:** the descriptive within-firm temporal coupling (rolling H(|r|) and H(volume) co-evolve, r̄≈0.665) plus the carefully-established firm-conditional predictive null. That is a Physica A descriptive/statistical-mechanics paper, framed around long-range correlations and a precise null, not a forecasting claim.
- **This is a useful negative result, not wasted effort.** It forecloses a tempting but unsupported headline before review would have, and it is consistent with the portfolio thesis: own the rigorous nulls.

## Caveats and the one confirmation worth running

- **Universe size.** 51 firms gives a noisy σ(CII)_t. The plan called for G=488, where the dispersion estimate is far tighter. The differenced nulls here are flat enough (|r|≈0.01–0.13) that more firms are unlikely to manufacture a lead — the issue is the absence of a relationship between innovations, not estimator noise — but a G=488 run is the definitive test and is the right confirmation before fully closing the σ(CII) door. It requires fetching ~440 additional tickers via yfinance and recomputing the rolling-Hurst panel (~30–40 min).
- **Frequency.** The rolling-Hurst construction is inherently ~monthly. Any stress lead living at weekly/daily frequency is invisible here by design.
- **One episode (COVID) drives the levels picture.** mean-CII rose 0.54→0.76 in 2020 H1; this is the same episode behind the paper's prior H3 "COVID amplification" claim, and it does not generalize to a systematic signal in differences.

## Reproduce

`research/sigma_cii/run_sigma_cii.py` (uses the on-disk `data/raw/*.parquet`, the `fractal_pv` package, yfinance for VIX/SPY/HYG, and the saved Pástor-Stambaugh file). Per-firm CII panel cached at `research/sigma_cii/data/cii_panel.parquet`; tables in `SUMMARY.md`, full numbers in `results.json`, figure in `fig_sigma_cii.pdf`.
