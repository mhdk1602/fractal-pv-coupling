# Cover Letter: Quantitative Finance

---

Dineshkumar Malempati Hari
Independent Researcher
mhdk.dinesh@gmail.com
ORCID: 0009-0003-1036-9477

[Date]

The Editors
*Quantitative Finance*
Taylor & Francis

Dear Editors,

I am pleased to submit the manuscript "Temporal Fractal Coupling of Volatility and Trading Volume: A Robust Within-Firm Pattern, a Time-Period Stress Signal, and No Firm-Specific Forecast Power in S&P 500 Stocks, 2015–2026" for consideration. The paper develops a dynamic measure of fractal memory co-evolution, documents that within-firm temporal coupling is strong and regime-amplified across the full S&P 500 panel ($G = 488$ firms after standard inclusion criteria), reports a structured null for the predictive question — firm-specific predictive content rejected under firm-conditional cluster-robust inference, while time-conditional inference detects cross-firm time-period co-movement that the nine-benchmark horse race fully absorbs — and delivers three transferable methodological observations about share-volume vs. dollar-volume Amihud confounds, firm-vs-time inference choice, and Satterthwaite df collapse at moderate cluster counts.

## Contribution

The paper introduces the Coupling Intensity Index (CII), a time-varying rolling Pearson correlation between two rolling Hurst exponents (absolute returns and log-volume) within a firm. CII captures a second-order fractal property: how memory structures co-evolve rather than what they are in the cross-section.

Across 488 current S&P 500 constituents over 2015–2026 (out of 503 attempted), the empirical results are:

1. **Static null** (H1 rejected): cross-sectional Pearson correlation between full-sample $H_{|r|}$ and $H_{v}$ is null in this sample.
2. **Within-firm temporal coupling** (H2 confirmed at full S&P 500): mean within-firm $r = 0.531$, 92.7% of firms positive, 80.4% above $r = 0.3$. The phenomenon is universal across all eleven GICS sectors, ranging from mean $r = 0.66$ in Energy to $r = 0.41$ in Utilities.
3. **Regime heterogeneity amplification** (H3 confirmed in distribution shape): the high-VIX regime exhibits a higher median (0.738 vs. 0.666) and substantially greater dispersion than the low-VIX regime; Mann-Whitney $p = 0.0019$. Mean coupling does not uniformly intensify with stress; the cross-section fans out.
4. **Firm-specific predictive null** (H4 rejected at the firm-month unit of analysis): under inference robust to two-way clustering, Bell-McCaffrey CR2 with Satterthwaite degrees of freedom, and the wild cluster restricted bootstrap, CII has no incremental predictive content for forward dollar-volume Amihud, the Corwin-Schultz spread, the Roll spread, realised volatility, vol-of-vol, max drawdown, abnormal turnover, log Amihud, or $\Delta$Amihud. Every focal-only signal in the battery is fully absorbed by nine standard liquidity benchmarks in the combined horse-race specification (the cleanest case is the forward Corwin-Schultz spread, where focal two-way $t = +3.64$ collapses to combined $t = +0.07$).
5. **Time-conditional co-movement detected**: time-clustered standard errors and Driscoll-Kraay HAC do detect a significant cross-firm time-period correlation between CII and several forward proxies. The natural reading: CII inherits a market-wide stress co-movement that aggregates across firms in any given month, but adds no firm-specific forecasting content beyond what the standard toolkit captures. The horse-race absorption is uniform across all SE methods.
6. **Three transferable methodological observations**: (a) share-volume vs. dollar-volume Amihud differ in a multiplicative price-level factor that cluster-robust inference does not detect; the diagnosis lives in the dependent-variable definition. (b) Firm-conditional and time-conditional cluster-robust methods can disagree at the same data when residual dependence is strong on both dimensions; the choice of which inference to call "the" inference should match the unit of forecast the paper claims. (c) Increasing the cluster count from $G = 50$ to $G = 488$ did not raise the Bell-McCaffrey CR2 Satterthwaite effective degrees of freedom — it remained at approximately 1.0 — because a small number of leverage-heterogeneous firms dominate the meat matrix; researchers should report Satterthwaite df as a routine diagnostic rather than assume it scales with $G$.

The combination of (1)–(3), (4)–(5), and (6) is the paper's contribution: a robust descriptive pattern of within-firm fractal coupling at full S&P 500 scale, a structurally informative inference disagreement that pinpoints which dimension of dependence carries CII's apparent signal, and three transferable methodological cautions for the econophysics-meets-finance interface.

## Fit with *Quantitative Finance*

The paper combines three strands that the journal has historically supported. First, it applies detrended fluctuation analysis and rolling-Hurst tools drawn from econophysics to a representative U.S. equity sample, extending the line of work on power-law cross-correlations and time-varying memory published in the journal. Second, it operates within the empirical finance tradition of Amihud, Goyenko-Holden-Trzcinka, Corwin-Schultz, and Hasbrouck on liquidity measurement, testing the novel measure against the standard benchmarks that a microstructure referee would demand. Third, it implements small-sample-corrected cluster-robust inference at the level of rigour that the journal's recent methodology-aware submissions have used (CR2 with Satterthwaite df, wild cluster restricted bootstrap, Driscoll-Kraay HAC, Cameron-Gelbach-Miller eigenvalue PSD adjustment for two-way CRVE). The synthesis is presented in the spirit that I believe is most useful to readers: documenting the descriptive pattern, reporting the predictive null honestly across multiple specifications, and converting the share-volume vs. dollar-volume Amihud divergence into a transferable methodological lesson rather than a buried inconvenience.

## Declarations

The manuscript is a single-author submission, is not under consideration elsewhere, and has not been previously published in whole or in part. The author declares no competing interests. The research received no external funding. All data are from Yahoo Finance via the `yfinance` Python package; no proprietary or restricted data are used. The complete analysis code, manuscript source, and replication guide are archived at Zenodo (concept DOI: 10.5281/zenodo.19611543, always resolving to the latest version) and GitHub (github.com/mhdk1602/fractal-pv-coupling).

## Research lineage and revision history

The paper builds on earlier master's-level work I undertook at King's College London in 2013 under the supervision of Dr. Enzo De Sena. That project examined whether Hurst-based fractal characteristics of stock-price series were associated with average trading volume in the cross section, and found a weak but statistically significant static relationship. The present paper is substantially different in question, method, and contribution: it shifts from static cross-sectional association to temporal co-evolution within firms, introduces the dynamic CII, runs a formal horse race against nine standard liquidity benchmarks, and applies publication-grade small-sample inference. I disclose this lineage here for completeness; the 2013 MSc report is archived with the submission materials.

The manuscript has been circulated as an SSRN preprint through three revisions. Versions 1.0–1.1 reported a positive predictive result for CII against a share-volume Amihud variant on a 50-firm large-cap subsample. Version 1.2 corrected that result by switching to the standard dollar-volume Amihud convention and documenting the share-volume vs. dollar-volume divergence as a substantive methodological finding. Version 1.3 (the present submission) extended the analysis to the full $G = 488$ S&P 500 panel under a pre-registered protocol, reproducing the descriptive coupling phenomenon at the broader scale and surfacing the structural disagreement between firm-conditional and time-conditional inference that organises this version of the paper. The pre-registration and the per-target decision rules are archived alongside the manuscript on the public GitHub repository.

## Suggested reviewers

I would be grateful if the editorial team considered reviewers active in the econophysics-finance interface. Without suggesting specific individuals, scholars with prior publications in *Quantitative Finance* on power-law cross-correlations, Hurst exponent estimation in finance, or liquidity-proxy evaluation would be well placed to evaluate the methodological choices.

Thank you for your consideration.

Yours sincerely,

Dineshkumar Malempati Hari
Independent Researcher
ORCID: 0009-0003-1036-9477
