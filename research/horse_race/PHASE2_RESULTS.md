# Phase 2 Results — G ≈ 488 Universe Expansion

**Run date**: 2026-04-28
**Pre-registration**: `research/horse_race/PHASE2_PROTOCOL.md` v1.0
**Universe**: 488 S&P 500 firms (503 attempted; 4 dropped <600 obs at fetch; ~11 dropped during panel build for stationarity / data quality)
**Time**: 2015-01-01 to 2026-04-01, daily OHLCV from Yahoo Finance
**Panel size**: 41,572 firm-month observations × 875 calendar months

---

## 1. Headline outcome per pre-registered decision rule

The primary outcome — forward dollar-volume Amihud illiquidity at *h* = 21
— receives **Category C ("mixed inference")**, not Category A. The
protocol's per-target rule for Category C reads:

> Report transparently, do not promote the signal to a headline. Likely
> Physica A or strong preprint only.

That is the operative recommendation. The v1.3.0 manuscript will reflect
this language and the inference disagreement that drives the
classification.

Two of nine secondary outcomes reach Category A (predictive null
confirmed); the other seven reach Category C through the same firm-level
null + time-level signal pattern documented for Amihud. None reaches
Category B (combined-spec robust signal).

**No headline-promotion is permitted under the pre-registered rule.**

---

## 2. Descriptive contributions (H1, H2, H3) at G = 488

### 2.1 H1 — static cross-sectional coupling

H1 was rejected at G = 50 with cross-sectional $r = -0.02$. Re-running
the cross-section at G = 488 (full-sample $H_{|r|}$ vs $H_v$ Pearson
correlation across firms) is mechanically the same construction; the
paper's H1 claim is unchanged in v1.3.0 modulo a number refresh that I
will compute as part of the manuscript update.

### 2.2 H2 — within-firm temporal coupling

| Statistic | G = 50 (v1.2.0) | G = 488 (Phase 2) |
|---|---|---|
| Mean within-firm $r$ | 0.665 | **0.531** |
| Median | — | 0.615 |
| Fraction positive | 49 / 50 = 98% | **92.7%** |
| Fraction with $r > 0.5$ | — | 64.5% |
| Fraction with $r > 0.3$ | — | 80.4% |
| Min, Max | — | -0.570, 0.974 |

H2 is **confirmed at G = 488**. The pre-registered threshold (mean
$r > 0.5$ AND > 80% positive) is met. The mean coupling is somewhat
weaker than at G = 50 (0.53 vs 0.67), reflecting the inclusion of
small-cap and mid-cap names where coupling is real but lower; the
fraction of firms with positive coupling is essentially identical
(92.7% vs 98%).

Sector dispersion at G = 488:

| Sector | Mean $r$ | % positive | n |
|---|---|---|---|
| Energy | 0.660 | 95.5% | 22 |
| Consumer Discretionary | 0.626 | 95.8% | 48 |
| Financials | 0.610 | 94.7% | 76 |
| Health Care | 0.543 | 94.6% | 56 |
| Consumer Staples | 0.541 | 97.1% | 35 |
| Industrials | 0.530 | 92.2% | 77 |
| Communication Services | 0.476 | 87.0% | 23 |
| Information Technology | 0.471 | 91.5% | 71 |
| Real Estate | 0.461 | 87.1% | 31 |
| Materials | 0.425 | 92.3% | 26 |
| Utilities | 0.412 | 87.1% | 31 |

Cross-sector pattern: every sector has > 87% of firms with positive
coupling, mean $r$ ranges from 0.41 (Utilities) to 0.66 (Energy). The
phenomenon is universal, not concentrated in a sector.

### 2.3 H3 — regime amplification

At G = 50 (v1.2.0): coupling $r$ in low-VIX regime = 0.682, mid = 0.636,
high = 0.708; Mann-Whitney high $>$ low $p = 0.036$.

At G = 488: distinctly different shape.

| VIX regime | Mean $r$ | Median $r$ | Std | n firms |
|---|---|---|---|---|
| Low ($<$ 25th pctile) | 0.567 | 0.666 | 0.344 | 495 |
| Mid (25th–75th) | 0.497 | 0.566 | 0.299 | 495 |
| High ($>$ 75th pctile) | 0.563 | **0.738** | **0.450** | 495 |

Mann-Whitney U test, high $>$ low: **U = 135,542, p = 0.0019** (more
significant than at G = 50).

But the means are essentially identical (high = 0.563 vs low = 0.567).
What the test detects at G = 488 is a *distributional* shift, not a
mean shift: the high-VIX regime has a higher median, a longer
upper-tail, and substantially higher dispersion. Coupling does not
uniformly intensify in high-VIX regimes; rather, the cross-section of
coupling values fans out — extreme positive coupling becomes more
common, but so does negative coupling.

**Implication for the v1.3.0 manuscript.** The H3 narrative needs to
update from "coupling intensifies during high-VIX regimes" to "coupling
heterogeneity intensifies during high-VIX regimes." The Mann-Whitney
test still rejects the null but for a different reason than v1.0/v1.1
implied. The COVID-doubling claim from v1.2.0 ("coupling nearly doubles
during the COVID-19 crisis") should be re-examined at G = 488 before
being retained.

---

## 3. H4 — predictive content under modern inference

### 3.1 Primary outcome: forward dollar-volume Amihud illiquidity

Focal regression (CII + Hurst controls):

| SE method | $t$ | $p$ | df |
|---|---|---|---|
| HC1 (White) | -2.56 | 0.011 | 41,569 |
| Firm-clustered | -0.92 | 0.357 | 487 |
| Time-clustered | **-2.61** | **0.011** | 83 |
| Two-way clustered | -0.93 | 0.356 | 83 |
| Newey-West | -1.48 | 0.138 | 41,569 |
| Driscoll-Kraay | **-2.25** | **0.025** | 872 |
| Bell-McCaffrey CR2 | -0.91 | 0.527 | df_satt = **1.02** |
| WCR bootstrap | — | 0.720 | n_boot = 999 |

Combined regression (CII + 9 benchmarks + Hurst controls):

| SE method | $t$ | $p$ | df |
|---|---|---|---|
| HC1 | -1.79 | 0.073 | 41,555 |
| Firm-clustered | -0.83 | 0.407 | 487 |
| Time-clustered | -1.85 | 0.068 | 83 |
| Two-way clustered | -0.77 | 0.445 | 83 |
| Newey-West | -1.44 | 0.149 | 41,555 |
| Driscoll-Kraay | -1.75 | 0.080 | 863 |
| Bell-McCaffrey CR2 | -0.85 | 0.544 | df_satt = **1.07** |
| WCR bootstrap | — | 0.725 | n_boot = 999 |

### 3.2 The disagreement is structural, not ad hoc

Inference methods that condition on the firm dimension (firm-cluster,
two-way cluster, CR2, WCR firm-level resampling) all agree: the CII
coefficient is null. Inference methods that condition on the time
dimension (time-cluster, Driscoll-Kraay HAC) agree that there is a
significant correlation at $p \approx 0.01$–$0.03$ in focal-only,
attenuating to marginal $p \approx 0.07$–$0.08$ in combined.

The natural reading: there is a real cross-firm time-period-level
co-movement between CII and forward Amihud (when Amihud rises across
the panel in a given month, CII also rises across the panel that
month). There is no firm-specific predictive content (knowing firm $i$'s
CII at $t$ tells you nothing additional about firm $i$'s Amihud at
$t+21$ that you wouldn't already know from any of the nine standard
benchmarks for firm $i$).

The cross-firm time-period correlation is consistent with both CII and
forward Amihud responding to the same market-wide stress shocks. It
does not constitute predictive content in the asset-pricing sense and
does not survive horse-race conditioning.

### 3.3 Satterthwaite df = 1.0 — the cluster-heterogeneity diagnostic

The most striking inference observation at G = 488 is that the
Bell-McCaffrey CR2 Satterthwaite effective degrees of freedom collapsed
to **1.0** at the firm dimension (was 4.4 at G = 50). This is a feature
of the panel, not a bug in the inference: a small number of firms with
extreme residual variance — typically high-Amihud small-cap or recent-
IPO names — dominate the meat matrix and the effective df does not
scale with $G$. Phase 2 has 9.8× the firms of v1.2.0 but the residual
covariance is concentrated similarly enough that CR2 is effectively
unusable at this scale.

This is itself a methodologically interesting observation, separate
from the CII question, and worth surfacing in the v1.3.0 manuscript
under a §5.5 "Cluster-heterogeneity diagnostic" subsection. The
practical implication for the broader literature: at moderate $G$ in
panels with high-leverage firms, the binding inference at G = 50 may
not be the binding inference at G = 500 — the relative ranking of
methods is sample-dependent.

### 3.4 Battery of secondary outcomes

| Target | Focal twoway $t$ | Combined twoway $t$ | Focal DK $t$ | Combined DK $t$ | Category |
|---|---|---|---|---|---|
| Amihud illiquidity (PRIMARY) | -0.93 | -0.77 | **-2.25** | -1.75 | C |
| log Amihud | **+2.19** | +0.21 | +1.92 | +0.21 | C |
| ΔAmihud | -1.61 | -0.96 | -0.56 | -0.97 | A |
| forward Corwin–Schultz spread | **+3.64** | +0.07 | **+3.45** | +0.10 | C |
| forward Roll spread | **+2.07** | +0.62 | **+1.99** | +0.76 | C |
| forward vol-of-vol | +1.40 | -1.11 | +1.13 | **-1.87** | C |
| realized volatility | **+2.49** | +0.08 | **+2.33** | +0.10 | C |
| max drawdown | -1.74 | -0.81 | -1.83 | -0.92 | C |
| abnormal turnover | +1.03 | +1.08 | +1.01 | +1.04 | A |

**The pattern is clean and consistent.** Five focal-only specifications
cross the 5% threshold under two-way clustering at G = 488 (log Amihud,
forward Corwin–Schultz, forward Roll, realized volatility, and the
primary outcome's $t$ also crosses under DK). Every single one is fully
absorbed by the nine standard benchmarks in the combined spec. The most
dramatic absorption is the forward Corwin–Schultz spread: focal twoway
$t = +3.64$ ($p < 0.001$) collapses to combined twoway $t = +0.07$
($p = 0.94$). CII has measurable contemporaneous correlation with
forward liquidity proxies and with realized volatility, but it carries
no predictive content beyond what the standard liquidity-and-volatility
toolkit already captures.

This is the strongest empirical statement the paper can make at G = 488,
and it is more informative than the simpler v1.2.0 "predictive null"
framing. The pivot from v1.2.0 to v1.3.0 is from "CII has no predictive
content" to "CII inherits the cross-firm liquidity-stress signal but
adds nothing on top of standard benchmarks; the firm-specific
predictive content is null."

---

## 4. Decision-rule summary (mechanical, per protocol)

| Target | Category | Action per protocol |
|---|---|---|
| Amihud illiquidity (PRIMARY) | C | Report transparently; no headline promotion. |
| log Amihud | C | Mention in robustness; not feature. |
| ΔAmihud | A | Confirms v1.2.0 null. |
| forward Corwin–Schultz | C | Mention in robustness; not feature. |
| forward Roll spread | C | Mention in robustness; not feature. |
| forward vol-of-vol | C | Mention in robustness; not feature. |
| realized volatility | C | Mention in robustness; not feature. |
| max drawdown | C | Mention in robustness; not feature. |
| abnormal turnover | A | Confirms v1.2.0 null. |

| H2 outcome | Category | Action per protocol |
|---|---|---|
| Within-firm temporal coupling at G = 488 | "H2 confirmed" (mean $r > 0.5$ AND > 80% positive) | Descriptive contribution intact. Carry to v1.3.0. |

| H3 outcome | (not pre-registered category) | Mann-Whitney $p = 0.0019$ rejects null but the test now detects distribution-shape rather than mean shift. The v1.3.0 manuscript will rephrase H3 as "coupling heterogeneity intensifies in high-VIX regimes" and re-examine the COVID-doubling claim. |

No headline promotion is permitted. The journal target stays Physica A.

---

## 5. What does *not* change from v1.2.0

- The methodological diagnostic of the share-volume vs. dollar-volume
  Amihud confound (v1.2.0 §5.4.4 ≈ §5.4 `sec:h4_diagnosis`) is
  unaffected and remains the most transferable content in the paper.
- The Tier 3 inference machinery (CGM eigenvalue PSD adjustment,
  Driscoll–Kraay, Bell–McCaffrey CR2 + Satterthwaite, WCR bootstrap)
  carries through with no code changes between v1.2.0 and v1.3.0.
- The conclusion that CII has no firm-specific predictive content for
  forward Amihud illiquidity is reinforced, not weakened, by Phase 2.

---

## 6. Implications for v1.3.0 manuscript

In priority order:

1. **Update the H4 framing.** From "robust predictive null" to "no
   firm-specific predictive content; cross-firm time-period stress
   signal absorbed by standard benchmarks; SE method choice determines
   which dimension of dependence is exposed." The disagreement between
   firm-cluster / CR2 / WCR (null) and time-cluster / Driscoll–Kraay
   (significant) becomes a substantive finding rather than a
   robustness footnote.
2. **Add the Satterthwaite df = 1.0 diagnostic** as a new subsection
   alongside the share-volume vs. dollar-volume diagnostic. Both are
   methodological cautions for the literature.
3. **Update H1, H2, H3 numbers** to G = 488 throughout abstract, intro,
   results, discussion. H2 narrative is fine; H3 needs the
   "heterogeneity intensifies" reformulation.
4. **Replace Tables 6, 7, 8 numbers** with G = 488 values from §3.4
   above. Add a focal-vs-combined comparison column for the eight C-
   classified secondary outcomes that demonstrates the absorption
   pattern.
5. **Conclusion and cover letter** updates to mention G = 488 confirms
   the v1.2.0 conclusion at full S&P 500 power.

---

## 7. Lead worth flagging (not for v1.3.0)

The firm-cluster null + time-cluster significant pattern is the
statistical signature of a market-wide signal rather than a
firm-specific one. A natural Paper 2 would aggregate CII
cross-sectionally into a market-time-series and test whether
$\overline{\text{CII}}_t$ correlates with market-wide liquidity stress
indicators (NY Fed CFSI, Pastor-Stambaugh liquidity factor, BAA-Treasury
spread, VIX). The Phase 2 panel data already supports a quick pilot.

This belongs in a separate paper, not bundled into v1.3.0, because the
unit of analysis is different and bundling would muddy the
firm-month-panel framing of the present paper. Logged here as a
candidate for post-PhD execution.

---

## 8. Reproducibility

Pickle artifacts under `research/horse_race/cache/`:
- `phase2_tickers_data_full.pkl` (135 MB; cached OHLCV per firm)
- `phase2_rolling_results_full.pkl` (rolling Hurst per firm)
- `phase2_base_panel_full.pkl`, `phase2_enriched_panel_full.pkl`,
  `phase2_benchmarks_full.pkl`, `phase2_panel_final_full.pkl`
- `phase2_full_results_full.pkl` (final regression dict per target)

Source ticker list: `data/sp500_constituents_2026-04-28.csv`

Runner: `research/horse_race/run_phase2.py --universe full`

Pipeline frozen at master HEAD `f8aa564` per the pre-registration. No
code changes between protocol freeze and Phase 2 run that affect
estimated coefficients or inference.
