# Robustness Check Results

All checks run on 50 S&P 500 constituents, daily data 2015-01-01 to 2026-04-01. This is the original large-cap pilot, not the G=488 panel that carries the headline numbers; `research/rebuild_g488/RESULT.md` holds the broader re-baseline.

## Summary of the eleven checks

Ten stability checks pass. R11 is an exploratory directional descriptive rather than a stability test, and the manuscript reports it as such (`main.tex` §Robustness).

| # | Check | Result | Verdict |
|---|-------|--------|---------|
| R1 | Window sensitivity | r = 0.56 (252d), 0.66 (500d), 0.75 (756d) | **PASS** — coupling strengthens with longer windows, consistent across all three |
| R2 | Alternative estimators | DFA, R/S, MFDFA(q=2) all agree on H ranges | **PASS** — not method-specific |
| R3 | Shuffled surrogate | Real r=0.63, Shuffled r=0.007 | **PASS** — coupling vanishes when temporal structure destroyed |
| R4 | Non-overlapping windows | r=0.62, 100% positive | **PASS** — not an artifact of window overlap |
| R5 | First-differenced Hurst | r=0.53, 100% positive | **PASS** — not driven by common trends |
| R6 | Squared returns | r=0.58, 98% positive | **PASS** — holds for squared returns, not specific to absolute |
| R7 | Subperiod stability | Pre-COVID 0.41, COVID 0.77, Post-COVID 0.29 | **PASS** — coupling strongest during crisis (interesting finding) |
| R8 | Sector decomposition | All sectors r > 0.64, Finance highest (0.76) | **PASS** — universal across sectors |
| R9 | Market factor | Partial r=0.42 after removing SPY | **PASS** — idiosyncratic coupling persists beyond market-wide factor |
| R10 | DFA polynomial order | Mean H(\|returns\|) 0.7947 linear vs 0.7823 quadratic | **PASS** — 0.012 apart, insensitive to detrending order |
| R11 | Granger causality | Volume H leads price H in 26% of tickers, reverse in 8% | **EXPLORATORY** — directional descriptive, not a stability test; overlapping windows preclude a causal claim |

## Detailed Results

### R1: Window Sensitivity

| Window (trading days) | Mean r | Std | % Positive | n |
|----------------------|--------|-----|-----------|---|
| 252 (~1 year) | 0.5617 | 0.153 | 98% | 50 |
| 500 (~2 years) | 0.6649 | 0.211 | 98% | 50 |
| 756 (~3 years) | 0.7480 | 0.223 | 96% | 50 |

Coupling increases monotonically with window size. Longer windows yield more stable Hurst estimates, reducing noise and revealing the underlying relationship more clearly. This is the expected behavior if the coupling is genuine.

### R2: Alternative Estimators

| Method | H(|returns|) | H(volume) |
|--------|-------------|-----------|
| DFA | 0.795 ± 0.051 | 0.881 ± 0.049 |
| R/S | 0.635 ± 0.028 | 0.740 ± 0.027 |
| MFDFA(q=2) | 0.810 ± 0.055 | 0.888 ± 0.049 |

DFA and MFDFA(q=2) agree closely (expected: MFDFA at q=2 reduces to DFA). R/S gives lower estimates, consistent with Lo (1991)'s finding that R/S underestimates when corrected for short-range dependence. The relative ordering H(vol) > H(|ret|) holds across all three methods.

### R3: Shuffled Surrogate Test

| Condition | Mean r | n |
|-----------|--------|---|
| Real data | 0.6291 | 20 |
| Shuffled (temporal structure destroyed) | 0.0071 | 20 |

**The coupling is 100% driven by temporal structure.** When we shuffle each series independently (preserving the marginal distribution but destroying time ordering), the correlation between rolling Hurst exponents drops to zero. This rules out any static or distributional explanation.

### R4: Non-Overlapping Windows

| Configuration | Mean r | Std | % Positive | n |
|--------------|--------|-----|-----------|---|
| Overlapping (step=20) | 0.5617 | 0.153 | 98% | 50 |
| Non-overlapping (step=252) | 0.6198 | 0.151 | 100% | 50 |

Non-overlapping windows give *slightly higher* correlation than overlapping. This eliminates the concern that overlapping windows inflate the correlation through autocorrelation. If anything, the overlapping estimate is conservative.

### R5: First-Differenced Hurst Series

| Condition | Mean r | Std | % Positive | n |
|-----------|--------|-----|-----------|---|
| Levels | 0.6649 | 0.211 | 98% | 50 |
| First differences (ΔH) | 0.5342 | 0.150 | 100% | 50 |

Coupling persists in first differences at r=0.53. This rules out spurious correlation from common trends. When H(|returns|) *increases*, H(volume) simultaneously *increases* — the co-movement is in the dynamics, not just the levels.

### R6: Squared Returns

| Volatility proxy | Mean r | Std | % Positive | n |
|-----------------|--------|-----|-----------|---|
| |returns| (absolute) | 0.6649 | 0.211 | 98% | 50 |
| returns² (squared) | 0.5825 | 0.196 | 98% | 50 |

Coupling holds for both volatility proxies. Slightly weaker for squared returns, which is expected since squared returns are noisier (more sensitive to outliers). Result is not an artifact of the specific volatility proxy chosen.

### R7: Subperiod Analysis

| Period | Mean r | Std | % Positive | n |
|--------|--------|-----|-----------|---|
| Pre-COVID (2015-2019) | 0.4060 | 0.268 | 88% | 50 |
| COVID (2020-2021) | **0.7665** | 0.228 | 96% | 50 |
| Post-COVID (2022-2026) | 0.2945 | 0.338 | 80% | 50 |

Coupling nearly doubles during the COVID crisis (0.41 → 0.77) in this 50-firm pilot. During periods of extreme market stress, price volatility and volume persistence look much more tightly linked, which is what the MDH predicts when information flow intensifies and both series respond more strongly to the common latent driver. The weaker post-COVID coupling (0.29) could reflect the regime shift to higher interest rates and changed market microstructure.

**Superseded at G = 488.** The doubling does not survive the universe expansion. Within-firm coupling conditioned on VIX regime gives means of 0.549 (low), 0.500 (medium) and 0.562 (high), so the average barely moves. What moves is the spread, with cross-firm σ rising from 0.30 in the low regime to 0.44 in the high regime, and the Mann-Whitney high-versus-low test rejecting at p < 0.001. Stress fans the cross-section out rather than lifting it. See `research/rebuild_g488/RESULT.md` and `main.tex` §Discussion.

### R8: Sector Decomposition

| Sector | Mean r | Range | n |
|--------|--------|-------|---|
| Finance | **0.756** | [0.580, 0.901] | 7 |
| Industrial/Energy | 0.720 | [0.518, 0.879] | 8 |
| Tech | 0.677 | [0.507, 0.892] | 9 |
| Consumer | 0.665 | [0.439, 0.856] | 13 |
| Healthcare | 0.645 | [0.235, 0.818] | 9 |

Finance shows strongest coupling (0.756), healthcare weakest (0.645). The coupling is universal across all sectors — no sector shows negative or near-zero coupling on average. Notable outliers: JPM (0.901, highest), JNJ (0.235, lowest). The JNJ result may reflect its defensive, low-volatility profile.

### R9: Market Factor Control

| Condition | Mean r | Std | % Positive | n |
|-----------|--------|-----|-----------|---|
| Raw correlation | 0.665 | 0.211 | 98% | 50 |
| Partial (controlling for SPY H) | 0.421 | 0.260 | 90% | 30 |

After removing the market-wide fractal factor (SPY's rolling Hurst), stock-level coupling persists at r=0.42. About 37% of the coupling is explained by market-wide Hurst dynamics (both series respond to the same macro environment), but 63% is idiosyncratic — stock-specific price-volume fractal coupling that exists beyond the market factor.

## Implications for the Paper

1. **Window sensitivity (R1):** Report all three windows. The monotonic increase strengthens the finding.
2. **Surrogate test (R3):** This is the most powerful robustness check. Include as a main result, not just robustness.
3. **Non-overlapping (R4):** Directly addresses the #1 methodological critique. Report prominently.
4. **First-differenced (R5):** Rules out common trends. Report in robustness section.
5. **Subperiod (R7).** Superseded at G = 488. Report the dispersion shift, not a mean shift.
6. **Market factor (R9):** Partial r=0.42 is still substantial. The coupling has both systematic and idiosyncratic components.

### R10: DFA Polynomial Order

| Detrending Order | Mean H(|returns|) |
|-----------------|-------------------|
| Linear (order=1, primary) | 0.7947 |
| Quadratic (order=2) | 0.7823 |
| Difference | 0.0124 |

Negligible difference (0.012). The Hurst estimates are robust to the choice of detrending polynomial.

### R11: Granger Causality

| Direction | Count | Percentage |
|-----------|-------|-----------|
| Volume H Granger-causes Price H | 13 | 26% |
| Price H Granger-causes Volume H | 4 | 8% |
| Bidirectional | 3 | 6% |
| Neither | 30 | 60% |

The asymmetry is notable: volume persistence Granger-causes volatility persistence 3x more often than the reverse (26% vs 8%). This suggests that while the coupling is predominantly contemporaneous (lag-0 dominant, Section R1), there is a weak but consistent directional signal: changes in volume persistence slightly precede changes in volatility persistence.

This is consistent with a modified MDH interpretation: information arrival first manifests in trading activity (volume), and the persistence structure of volatility adjusts shortly after. The effect is too weak to show up as a lead in the cross-correlation function (which averages over all tickers) but emerges in the Granger framework (which tests each ticker individually).

**For the paper:** Report as a supplementary finding. The main narrative remains "contemporaneous coupling," but the Granger asymmetry adds a nuance worth a paragraph in the Discussion.

## Remaining

- [x] HAC (Newey-West) standard errors — in `src/fractal_pv/inference_robust.py`, alongside Driscoll-Kraay
- [x] Full S&P 500 expansion — Phase 2, G = 488, see `research/rebuild_g488/RESULT.md`
- [ ] Re-run R1 through R6 and R8 through R11 at G = 488 (currently 50-firm pilot only)
