# σ(CII) confirmation at the full universe, G = 495

**Run date** 2026-08-04. **Status** confirmation of the original G=51 run of 2026-05-28 recorded in `FINDINGS.md`, which flagged a G≈488 rerun as "the one confirmation worth running". This file is the current statement; `FINDINGS.md` is kept as the record of first result.

## NULL confirmed. σ(CII) is not a market-stress signal.

The pre-registered decision rule at `run_sigma_cii.py:12-22` has three branches. This run lands squarely in the third, **NOISE**, and the script's own `decide()` returns that call mechanically. No lead, so no Chaos, Solitons & Fractals headline. No contemporaneous relationship at |Pearson| > 0.3, so no Physica A descriptive claim either. Fall back to the structured precise null.

## What changed against the original run

The original result was not reproducible. `run_sigma_cii.py` globbed `data/raw/*_1d_*.parquet`, so the universe was whatever the cache held on the day. It held 51 firms in May; it holds 501 now. Two fixes, both in `run_sigma_cii.py`.

First, the universe is pinned. It is read from an explicit newline-delimited ticker file (`--universe`, default `universe_full.txt`), and every run writes `universe_manifest<tag>.json` recording each ticker, its source file, row count, date span, CII observation count, and a SHA-256 over the sorted ticker list. This run used 501 pinned tickers, all 501 resolved in `data/raw`, 495 surviving the panel build, digest `241ac1f339d01b9c...`. The six dropped are recent index additions with too little history for a 500-day window plus a 30-step trailing correlation, namely CEG, GEHC, GEV, KVUE, SOLV and VLTO.

Second, outputs are tagged. `--tag full` suffixes every artifact, so the unsuffixed G=51 files are untouched.

## The panel

495 firms over the same 87 rolling-Hurst dates as the original, 2018-05-21 to 2025-03-25, W=500, step=20, CII trailing window=30. Firms contributing per date run 462 to 465, against a flat 51 before. σ(CII) ranges [0.322, 0.464] with a mean of 0.413, and the 95% firm-resample bootstrap band has a median width of 0.056 against 0.195 originally, three and a half times tighter, which is what a ninefold larger cross-section buys.

## 1. No lead

Granger causality on first differences, lags 1 through 4, is null in both directions for every stress measure. The smallest p for σ→stress is 0.572 and for stress→σ is 0.625. The cross-correlation function peaks at lag 6 for VIX, SPY-RV and HYG-RV, but every one of those peaks is negative-signed (−0.20, −0.16, −0.16), wrong-signed for an early-warning story, none significant at 5%, and the expected artifact of correlating two persistent series at long lags. Of the twelve predictive regressions of forward stress on σ(CII) with the lagged stress level controlled, the largest |t| is 1.21. Not one crosses the threshold. The original run's lone survivor, hyg_rv at h=6 with t = −2.20, does not reappear; it now reads t = −0.75, p = 0.452, which is what an isolated result among fifteen tests usually turns out to be.

## 2. No contemporaneous relationship

σ(CII) against each stress measure in levels gives |Pearson| ≤ 0.137, none significant (VIX +0.109 p=0.31; log-VIX +0.137 p=0.21; SPY-RV +0.126 p=0.24; HYG-RV +0.120 p=0.27). In first differences |r| ≤ 0.135, all p ≥ 0.21. Two Spearman coefficients drift toward the boundary (SPY-RV +0.206 p=0.055, HYG-RV +0.255 p=0.017), both far below the pre-registered |r| > 0.3 bar and unsupported by the Pearson, the differences or the Granger tests.

One sign did flip against the original. At G=51 the σ-versus-stress correlations were weakly negative (VIX −0.14, HYG −0.18); at G=495 they are weakly positive (+0.109, +0.120). Neither set is distinguishable from zero, and a correlation whose sign turns over with the universe is the signature of noise, not of a small effect finally resolving.

## 3. The mean still co-moves in levels, and it is still spurious

The cross-sectional mean of CII tracks stress in levels, against log-VIX +0.566, VIX +0.490, SPY-RV +0.325, HYG-RV +0.313. That replicates the original run's pattern and again contradicts the planning note's mean-CII-versus-VIX ≈ 0.057. But mean-CII has AR(1) = 0.986, near a random walk, and in first differences the co-movement collapses to +0.027 (p = 0.81) against log-VIX and is null for every measure (|r| ≤ 0.028, all p ≥ 0.80). This is the Granger-Newbold spurious-regression pattern. The levels correlation reflects shared trending, not a relationship between innovations. Nine times the cross-section did not change the conclusion.

## What this settles

The caveat that closed `FINDINGS.md` was that 51 firms give a noisy σ(CII)_t and that G≈488 was the definitive test. It has now been run. The dispersion estimate is three and a half times tighter and the nulls are, if anything, flatter. The σ(CII) door is closed on evidence rather than on assumption, and the honest contribution stands where it already was, the descriptive within-firm temporal coupling (mean r = 0.531 at G = 488) plus the bounded firm-conditional predictive null.

## Two limits worth stating

**Pástor-Stambaugh is missing from this run.** The original included P-S non-traded liquidity innovations as a fifth stress measure, loaded from `research/sigma_cii/data/pastor_stambaugh_liq.txt`. That directory is gitignored and the file is gone, so this run covers four measures rather than five. P-S was null in the original and the liquidity channel is also covered by the firm-level Amihud null, so the omission does not change the verdict, but the confirmation is one measure short of the original and the file should be restored before any write-up leans on it.

**Frequency, unchanged.** The rolling-Hurst construction is inherently monthly. Any stress lead living at weekly or daily frequency is invisible here by design, at either universe size.

## Reproduce

```bash
python research/sigma_cii/run_sigma_cii.py --universe research/sigma_cii/universe_full.txt --tag full
```

The per-firm CII panel caches to `research/sigma_cii/data/cii_panel_full.parquet` (gitignored, about 25 minutes to rebuild from `data/raw`). Tables in `SUMMARY_full.md`, full numbers in `results_full.json`, universe in `universe_manifest_full.json`, series in `sigma_cii_series_full.csv`, figure in `fig_sigma_cii_full.pdf`.
