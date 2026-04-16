# Research Plan: Temporal Coupling of Price and Volume Fractality

## Working Title

**"Temporal Coupling of Price and Volume Fractality: Evidence from Rolling Hurst Analysis of S&P 500 Constituents"**

Alternative: *"Co-movement of Memory Structure in Price Volatility and Trading Volume: A Fractal Perspective on the Mixture of Distributions Hypothesis"*

---

## 1. The Finding (What We Have)

| Result | Value | Significance |
|--------|-------|-------------|
| Cross-sectional H(|ret|) vs H(vol) correlation | r = -0.02, p = 0.88 | Null. No static coupling. |
| Temporal (rolling) correlation | mean r = **0.665** | **100% of 50 tickers significant** |
| Direction | 49/50 positive | Near-universal positive coupling |
| Lead-lag | lag=0 strongest | Contemporaneous, no precedence |
| Sole outlier | META (r = -0.42) | Decoupled during 2022-23 crisis |
| H(|returns|) | 0.795 ± 0.051 | Replicates literature (0.7-0.8) |
| H(volume) | 0.881 ± 0.049 | Slightly high (literature: 0.7-0.9) |
| H(returns) | 0.461 ± 0.036 | Replicates EMH (≈ 0.5) |
| DFA R² | 0.994 ± 0.002 | Excellent monofractal fit |

## 2. Why This Is Publishable

**The conceptual distinction nobody has made:**
- DCCA (Podobnik & Stanley 2008) measures whether price and volume *move together* at different time scales.
- Our approach measures whether the *memory structure* of price and volume *evolves in tandem* — a second-order fractal property.
- Static cross-sectional analysis (what most papers do) finds nothing.
- Temporal rolling analysis (what we do) finds strong, universal coupling.
- This is a statement about how the *complexity* of two financial processes co-evolves, not how their levels co-move.

**Supporting the MDH through a new lens:**
- The Mixture of Distributions Hypothesis (Clark 1973, Tauchen & Pitts 1983) posits a common latent factor (information arrival) driving both volatility and volume.
- Bollerslev & Jubinski (1999) found common long-memory components using ARFIMA.
- We find the same coupling in the *fractal scaling properties* of both series — a complementary, independent confirmation using a completely different methodology.
- The contemporaneous lag-0 dominance is exactly what MDH predicts: a shared driver, not a causal chain.

## 3. Target Journals (Ranked)

| Rank | Journal | IF | Review Time | Fit | Strategy |
|------|---------|-----|-------------|-----|----------|
| 1 | **Chaos, Solitons & Fractals** | 7.8 | 2-4 mo | Excellent | Best IF-to-fit ratio. Fractal methods + complex systems. |
| 2 | **Physica A** | 3.3 | 2-4 mo | Perfect | Natural home for DFA + financial markets. Safest bet. |
| 3 | **Quantitative Finance** | 1.5 | 4-8 mo | Good | Finance audience. Needs strong MDH framing. |
| 4 | **Scientific Reports** | 4.6 | 2-4 mo | Good | Nature branding. Broad audience. |
| 5 | **Fractal and Fractional** | 5.4 | 1-2 mo | Good | Fast review. Niche but respected. |

**Recommended submission path:** Submit to Chaos, Solitons & Fractals first. If rejected, pivot to Physica A (near-certain acceptance if methodology is sound). If we add Granger causality and economic framing, consider Quantitative Finance.

## 4. Paper Structure

### Section 1: Introduction (1.5 pages)
- Open with the price-volume relationship as a central question in market microstructure
- Note that fractal properties (Hurst exponents) of both series are well-studied *individually*
- Identify the gap: nobody has studied how these fractal properties *co-evolve over time*
- State the static-temporal paradox (no cross-sectional coupling, strong temporal coupling)
- Frame as a fractal-lens test of the MDH
- Contributions: (1) novel framing via independent rolling Hurst comparison, (2) universal temporal coupling finding, (3) contemporaneous structure supporting MDH, (4) crisis-driven decoupling (META)

### Section 2: Literature Review (2.5 pages)
- 2.1 Fractal properties of financial time series (Mandelbrot 1963, Cont 2001)
- 2.2 Hurst exponent estimation: DFA and its properties (Peng 1994, Kantelhardt 2002, Weron 2002)
- 2.3 Long memory in volatility and volume (Ding et al. 1993, Lobato & Velasco 2000, Bollerslev & Jubinski 1999)
- 2.4 Price-volume cross-correlation (Karpoff 1987, Podobnik et al. 2009)
- 2.5 The Mixture of Distributions Hypothesis (Clark 1973, Tauchen & Pitts 1983, Andersen 1996)
- 2.6 Time-varying Hurst exponents (Cajueiro & Tabak 2004, Alvarez-Ramirez et al. 2008, Grech & Mazur 2004)
- 2.7 Gap: no study examines temporal co-movement of H(|returns|) and H(volume)

### Section 3: Methodology (3 pages)
- 3.1 DFA estimation procedure (Peng 1994), with scale selection and R² quality check
- 3.2 Rolling window Hurst: window=500 days, step=20 days, with sensitivity analysis
- 3.3 Cross-correlation: Pearson and Spearman on rolling H series
- 3.4 Lead-lag analysis: cross-correlation at lags ±1 to ±5
- 3.5 Statistical inference: block bootstrap CIs (Politis & Romano 1994), HAC standard errors for overlapping windows
- 3.6 Validation: synthetic fBm with known H to verify estimator accuracy

### Section 4: Data (1.5 pages)
- 4.1 Sample: 50 S&P 500 constituents, 2015-01-01 to 2026-04-01, daily OHLCV
- 4.2 Selection criteria and sector representation (11 GICS sectors)
- 4.3 Descriptive statistics (returns, volume, stationarity tests)
- 4.4 Preprocessing: log returns, absolute log returns, log volume

### Section 5: Results (4 pages)
- 5.1 Full-sample Hurst estimates: replicate canonical findings
  - Table: H(returns), H(|returns|), H(volume) for all 50 tickers by sector
  - Comparison with literature values
- 5.2 Cross-sectional analysis: null result (r = -0.02)
- 5.3 Temporal (rolling) analysis: the core finding
  - Figure: rolling H(|returns|) and H(volume) for exemplar tickers (AAPL, JPM, META)
  - Table: rolling Pearson r for all 50 tickers
  - Distribution of rolling r values
- 5.4 Lead-lag structure: lag=0 dominant, symmetric decay
- 5.5 The META anomaly: negative coupling during corporate crisis

### Section 6: Robustness (2 pages)
- 6.1 Window length sensitivity (252, 500, 756 days)
- 6.2 Alternative estimators (R/S, MFDFA at q=2)
- 6.3 Shuffled surrogate test (destroy temporal structure → coupling vanishes)
- 6.4 Subperiod analysis (pre-COVID vs COVID vs post-COVID)
- 6.5 Sector controls (within-sector vs between-sector coupling)
- 6.6 Market factor: H(S&P 500) as a common driver
- 6.7 First-differenced Hurst series (rule out common trends)
- 6.8 Squared returns vs absolute returns

### Section 7: Discussion (2 pages)
- MDH interpretation: common information arrival drives both memory structures
- Why cross-sectional fails but temporal succeeds: the distinction between *level* and *dynamics*
- Crisis-driven decoupling: what META tells us about regime breaks
- Comparison with DCCA literature: complementary, not competing
- Implications for risk management: long-memory modeling should jointly model volatility and volume persistence
- Limitations: sample limited to US large-cap, daily frequency, survivorship bias

### Section 8: Conclusion (0.5 pages)

**Total: ~17 pages** (fits Chaos, Solitons & Fractals and Physica A guidelines)

## 5. Essential Citations (38 papers)

### Foundational Fractal Finance (6)
1. Mandelbrot, B.B. (1963). The Variation of Certain Speculative Prices. *J. Business*, 36(4), 394-419.
2. Mandelbrot, B.B. & Van Ness, J.W. (1968). Fractional Brownian Motions. *SIAM Review*, 10(4), 422-437.
3. Mandelbrot, B.B. (1997). *Fractals and Scaling in Finance*. Springer.
4. Peters, E.E. (1994). *Fractal Market Analysis*. Wiley.
5. Cont, R. (2001). Empirical Properties of Asset Returns. *Quantitative Finance*, 1(2), 223-236.
6. Lo, A.W. (1991). Long-term Memory in Stock Market Prices. *Econometrica*, 59(5), 1279-1313.

### DFA/MFDFA Methodology (6)
7. Hurst, H.E. (1951). Long-term Storage Capacity of Reservoirs. *Trans. ASCE*, 116, 770-808.
8. Peng, C.-K. et al. (1994). Mosaic Organization of DNA Nucleotide Sequences. *Phys. Rev. E*, 49(2), 1685.
9. Kantelhardt, J.W. et al. (2002). MFDFA of Nonstationary Time Series. *Physica A*, 316, 87-114.
10. Weron, R. (2002). Estimating Long-range Dependence: Finite Sample Properties. *Physica A*, 312, 285-299.
11. Barunik, J. & Kristoufek, L. (2010). Hurst Exponent Estimation Under Heavy-tailed Distributions. *Physica A*, 389(18), 3844-3855.
12. Shao, Y.-H. et al. (2012). Comparing FA, DFA and DMA Performance. *Scientific Reports*, 2, 835.

### Long Memory in Volatility & Volume (5)
13. Ding, Z., Granger, C.W.J. & Engle, R.F. (1993). A Long Memory Property of Stock Returns. *J. Empirical Finance*, 1(1), 83-106.
14. Lobato, I.N. & Velasco, C. (2000). Long Memory in Stock-market Trading Volume. *JBES*, 18(4), 410-427.
15. Bollerslev, T. & Jubinski, D. (1999). Common Long-run Dependencies in Volatility and Volume. *JBES*, 17(1), 9-21.
16. Ray, B.K. & Tsay, R.S. (2000). Long-range Dependence in Daily Stock Volatilities. *JBES*, 18(2), 254-262.
17. Plerou, V., Gopikrishnan, P. & Stanley, H.E. (2003). Two-phase Behaviour of Financial Markets. *Nature*, 421, 130.

### Price-Volume Relationship (4)
18. Karpoff, J.M. (1987). The Relation Between Price Changes and Trading Volume. *JFQA*, 22(1), 109-126.
19. Gallant, A.R., Rossi, P.E. & Tauchen, G. (1992). Stock Prices and Volume. *RFS*, 5(2), 199-242.
20. Chen, G., Firth, M. & Rui, O.M. (2001). Dynamic Relation Between Stock Returns, Trading Volume, and Volatility. *Financial Review*, 36(3), 153-174.
21. Podobnik, B. et al. (2009). Cross-correlations Between Volume Change and Price Change. *PNAS*, 106(52), 22079-22084.

### Mixture of Distributions Hypothesis (5)
22. Clark, P.K. (1973). A Subordinated Stochastic Process Model. *Econometrica*, 41(1), 135-155.
23. Epps, T.W. & Epps, M.L. (1976). Stochastic Dependence of Price Changes and Volumes. *Econometrica*, 44(2), 305-321.
24. Tauchen, G.E. & Pitts, M. (1983). The Price Variability-Volume Relationship. *Econometrica*, 51(2), 485-505.
25. Andersen, T.G. (1996). Return Volatility and Trading Volume: An Information Flow Interpretation. *J. Finance*, 51(1), 169-204.
26. Liesenfeld, R. (1998). Dynamic Bivariate Mixture Models. *JBES*, 16(1), 101-109.

### DCCA / Cross-Correlation (4)
27. Podobnik, B. & Stanley, H.E. (2008). Detrended Cross-correlation Analysis. *Phys. Rev. Lett.*, 100(8), 084102.
28. Zebende, G.F. (2011). DCCA Cross-correlation Coefficient. *Physica A*, 390(4), 614-618.
29. Kristoufek, L. (2014). Measuring Correlations Between Non-stationary Series with DCCA. *Physica A*, 402, 291-298.
30. Cao, G., Xu, L. & Cao, J. (2012). MF-DCCA Between Chinese Exchange and Stock Market. *Physica A*, 391(20), 4855-4866.

### Time-Varying Hurst / Rolling Analysis (4)
31. Cajueiro, D.O. & Tabak, B.M. (2004). Hurst Exponent Over Time: Emerging Markets Becoming Efficient. *Physica A*, 336, 521-537.
32. Alvarez-Ramirez, J. et al. (2008). Time-varying Hurst Exponent for US Stock Markets. *Physica A*, 387(24), 6159-6169.
33. Grech, D. & Mazur, Z. (2004). Can One Make Crash Prediction Using Local Hurst Exponent? *Physica A*, 336, 133-145.
34. Wang, Y., Liu, L. & Gu, R. (2009). Multifractal DFA of Shenzhen Stock Market. *Int. Rev. Financial Analysis*, 18(5), 271-276.

### Market Efficiency & Structure (4)
35. Di Matteo, T., Aste, T. & Dacorogna, M.M. (2005). Long-term Memories of Developed and Emerging Markets. *EPJ B*, 46(2), 309-317.
36. Fama, E.F. (1970). Efficient Capital Markets: A Review. *J. Finance*, 25(2), 383-417.
37. Politis, D.N. & Romano, J.P. (1994). The Stationary Bootstrap. *JASA*, 89(428), 1303-1313.
38. Newey, W.K. & West, K.D. (1987). A Simple, Positive Semi-definite, HAC Covariance Estimator. *Econometrica*, 55(3), 703-708.

## 6. What Reviewers Will Ask (Anticipated Critiques)

### Critical (must address in paper)
1. **"Why not DCCA?"** — Our approach measures co-movement of *memory structure* (second-order fractal property), not co-movement of *levels*. DCCA and our method answer different questions. We discuss this in Section 7.
2. **"Overlapping windows inflate correlation."** — Address with HAC standard errors (Newey-West) and block bootstrap. Also show non-overlapping results.
3. **"Window length sensitivity."** — Show results for 252, 500, 756 days.
4. **"Finite sample DFA bias."** — Validate with synthetic fBm at our window lengths. Cite Weron (2002).

### Important (address in robustness)
5. **"Shuffled surrogate test."** — Destroy temporal structure, show coupling vanishes. Key null model.
6. **"Common trends / spurious correlation."** — First-difference the Hurst series and re-test.
7. **"Market-wide factor."** — Compute H(S&P 500) and partial out the market component.
8. **"Subperiod stability."** — Pre-COVID / COVID / post-COVID splits.
9. **"50 stocks is not the full S&P 500."** — Justify selection, show sector representativeness.
10. **"Squared returns vs absolute returns."** — Show both, explain why absolute is preferred (Ding et al. 1993).

### Nice to have (strengthens paper)
11. **"Granger causality between H series."** — Does H(volume) predict future H(|returns|)?
12. **"Sector heterogeneity."** — Do some sectors show stronger coupling?
13. **"Conditioning on volatility regime."** — Does coupling strengthen during high-vol periods?

## 7. Robustness Checks Checklist

- [ ] Window sensitivity: 252 / 500 / 756 days
- [ ] Alternative estimators: R/S, MFDFA(q=2)
- [ ] Shuffled surrogate: destroy temporal structure → coupling vanishes
- [ ] Non-overlapping windows: eliminates autocorrelation concern
- [ ] First-differenced Hurst series: rules out common trends
- [ ] Squared returns: verify absolute returns result
- [ ] Subperiod: pre-2020, 2020-2021, 2022-2026
- [ ] Sector decomposition: within vs between coupling
- [ ] Market factor: partial correlation controlling for H(S&P 500)
- [ ] HAC standard errors: Newey-West for overlapping windows
- [ ] DFA polynomial order: linear vs quadratic detrending

## 8. Connection to PhD Thesis

Your PhD (University of Cumberland, defense ~2027) studies **institutional pressures and data governance adoption in professional services firms** using Institutional Theory (DiMaggio & Powell 1983). It's qualitative, focused on consulting firms as dual-role governance practitioners.

**These are separate research streams.** Don't force a connection. But two genuine bridges exist:

### Bridge 1: BCBS 239 and Long Memory in Risk Data
Your dissertation discusses BCBS 239 (risk data aggregation) as a coercive institutional pressure. Our finding that volatility and volume have strong long memory (H >> 0.5) has *direct implications* for BCBS 239 compliance: risk models that assume short-memory processes (standard GARCH) underestimate tail risk. Proper risk data aggregation requires acknowledging long-memory dependencies. This creates a footnote or future-work paragraph in your dissertation Chapter 1 connecting your professional quantitative work to the regulatory pressures you study.

### Bridge 2: Dissertation Defense Narrative
When defending your PhD, having a peer-reviewed quantitative publication (even in a different domain) demonstrates methodological breadth. A committee member asking "can you do quantitative work?" gets answered by a Physica A or Chaos, Solitons & Fractals publication. The two papers together show you can work across qualitative and quantitative paradigms, which is rare and valued.

### What NOT to do
Don't try to merge the two into one paper. The fractal paper is econophysics/quantitative finance. The dissertation is qualitative information systems. Combining them would confuse reviewers in both venues and weaken both arguments.

## 9. Academic & Commercial Implications

### Academic Implications
1. **For MDH literature:** Our finding provides independent fractal-domain evidence for the mixture of distributions hypothesis. The MDH was tested with ARFIMA models (Bollerslev & Jubinski 1999) and with DCCA (Podobnik et al. 2009). Our rolling Hurst correlation is a third, independent methodology reaching the same conclusion.
2. **For market efficiency literature:** The null cross-sectional result confirms that *static* fractal properties don't differentiate stocks. Efficiency holds in the cross-section. But temporal dynamics reveal structure that static analysis misses.
3. **For crisis dynamics:** META's negative coupling during its 2022-23 corporate crisis suggests that regime breaks can decouple normally paired fractal properties. This has implications for crisis detection.
4. **For methodology:** Rolling independent Hurst comparison is a simple, interpretable alternative to DCCA for studying how fractal properties co-evolve. It's accessible to researchers without DCCA expertise.

### Commercial / Practitioner Implications
1. **Risk management:** If volatility and volume persistence co-move, risk models should jointly model both. A spike in H(volume) predicts a concurrent spike in H(|returns|), meaning volatility will become more persistent. This has value-at-risk and portfolio allocation implications.
2. **Trading signals:** The contemporaneous coupling means monitoring H(volume) in real-time could provide early warning of volatility regime shifts (volume data updates faster than volatility estimates based on returns).
3. **Anomaly detection:** Stocks whose temporal coupling breaks down (like META in 2022) may be experiencing unusual market dynamics worth investigating.
4. **Market surveillance:** Regulators could use fractal coupling metrics as a market health indicator — decoupling across many stocks simultaneously could signal systemic stress.

## 10. Timeline

| Phase | What | Duration | Status |
|-------|------|----------|--------|
| **Data & Code** | Expand to 50 tickers, rolling analysis, robustness | Done | ✓ |
| **Robustness** | All 11 checks from Section 7 | 2-3 weeks | Next |
| **Writing** | Sections 1-4 (Intro, Lit Review, Methods, Data) | 2-3 weeks | — |
| **Results** | Sections 5-6 (Results, Robustness) with figures | 2 weeks | — |
| **Discussion** | Sections 7-8 (Discussion, Conclusion) | 1 week | — |
| **Internal review** | Self-review + grammar + formatting | 1 week | — |
| **Advisor feedback** | If applicable — informal review | 2 weeks | — |
| **Submission** | Chaos, Solitons & Fractals | Target | 8-10 weeks from now |
| **Review** | Expect 2-4 months | — | — |

## 11. Publication Costs

| Journal | Open Access Fee | Subscription (free) | Notes |
|---------|----------------|--------------------|----|
| Chaos, Solitons & Fractals | ~$3,390 | Yes, free | Hybrid model |
| Physica A | ~$3,000 | Yes, free | Hybrid model |
| Scientific Reports | ~$2,490 | No (OA only) | Nature portfolio |
| Fractal and Fractional | ~$2,400 | No (OA only) | MDPI |

You can publish for free (subscription access, not open access) in Chaos, Solitons & Fractals and Physica A. Readers access through institutional subscriptions. Open access costs more but increases citations.

## 12. File Structure for This Research

```
research/
├── RESEARCH_PLAN.md          ← this file
├── paper/
│   ├── main.tex              ← LaTeX manuscript
│   ├── references.bib        ← BibTeX
│   ├── figures/               ← Publication-quality plots
│   └── tables/                ← LaTeX tables
├── robustness/
│   ├── window_sensitivity.py
│   ├── surrogate_test.py
│   ├── subperiod_analysis.py
│   └── results/               ← Robustness output
├── data/
│   ├── results_50_tickers.csv
│   ├── rolling_correlations.csv
│   └── lead_lag_results.csv
└── notes/
    ├── reviewer_responses.md  ← Pre-drafted responses to anticipated critiques
    └── submission_log.md      ← Track submissions, rejections, revisions
```
