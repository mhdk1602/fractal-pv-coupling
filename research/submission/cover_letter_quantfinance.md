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

I am pleased to submit the manuscript "Temporal Fractal Coupling of Volatility and Trading Volume: A Robust Pattern Without Forecast Power in S&P 500 Stocks, 2015–2026" for consideration in *Quantitative Finance*. The paper develops a dynamic measure of fractal memory co-evolution, documents that within-firm temporal coupling is strong and regime-amplified during stress, reports an honest null for the predictive question against ten standard market-quality outcomes under modern small-sample inference, and dissects a price-level confound in non-standard share-volume illiquidity proxies that is portable to the wider literature.

## Contribution

The paper introduces the Coupling Intensity Index (CII), a time-varying rolling Pearson correlation between two rolling Hurst exponents (absolute returns and log-volume) within a firm. CII captures a second-order fractal property: how memory structures co-evolve rather than what they are in the cross-section.

Across 50 S&P 500 constituents over 2015–2026, the empirical results are:

1. **Static null**: the cross-sectional correlation between full-sample $H_{|r|}$ and $H_{v}$ is $-0.02$.
2. **Temporal coupling**: within-firm rolling-Hurst coupling is strong and positive in 49 of 50 equities (mean $r = 0.665$).
3. **Regime amplification**: coupling is significantly higher in high-VIX regimes (Mann-Whitney $p = 0.036$) and nearly doubles during the COVID-19 crisis.
4. **Predictive null**: under inference robust to two-way clustering (Cameron-Gelbach-Miller 2011), Bell-McCaffrey CR2 with Satterthwaite effective degrees of freedom (Imbens and Kolesár, 2016), and the wild cluster restricted bootstrap (Cameron-Gelbach-Miller 2008; MacKinnon-Webb 2017), CII has no incremental predictive content for forward Amihud illiquidity in the standard dollar-volume convention, nor for realised volatility, the Corwin-Schultz spread, the Roll spread, vol-of-vol, max drawdown, or abnormal turnover.
5. **Methodological diagnostic**: an apparently strong predictive result emerges against a non-standard share-volume Amihud denominator and dissipates under the standard dollar-volume convention. The decomposition $\widetilde{\mathrm{ILLIQ}} = \mathrm{ILLIQ} \cdot P$ shows that the share-volume proxy carries a price-level component that any regressor correlated with within-firm price drift will appear to forecast. Cluster-robust inference, including the wild cluster restricted bootstrap, does not protect against this confound: the diagnosis requires examining the dependent variable rather than the standard errors.

The combination of (1)–(3) and (4)–(5) is the paper's contribution: a robust descriptive pattern of within-firm fractal coupling, a clean null for the predictive question at $G = 50$ firms across ten target specifications and three modern small-sample inference methods, and a methodological caveat that should improve future empirical work in the econophysics-meets-finance interface.

## Fit with *Quantitative Finance*

The paper combines three strands that the journal has historically supported. First, it applies detrended fluctuation analysis and rolling-Hurst tools drawn from econophysics to a representative U.S. equity sample, extending the line of work on power-law cross-correlations and time-varying memory published in the journal. Second, it operates within the empirical finance tradition of Amihud, Goyenko-Holden-Trzcinka, Corwin-Schultz, and Hasbrouck on liquidity measurement, testing the novel measure against the standard benchmarks that a microstructure referee would demand. Third, it implements small-sample-corrected cluster-robust inference at the level of rigour that the journal's recent methodology-aware submissions have used (CR2 with Satterthwaite df, wild cluster restricted bootstrap, Driscoll-Kraay HAC, Cameron-Gelbach-Miller eigenvalue PSD adjustment for two-way CRVE). The synthesis is presented in the spirit that I believe is most useful to readers: documenting the descriptive pattern, reporting the predictive null honestly across multiple specifications, and converting the share-volume vs. dollar-volume Amihud divergence into a transferable methodological lesson rather than a buried inconvenience.

## Declarations

The manuscript is a single-author submission, is not under consideration elsewhere, and has not been previously published in whole or in part. The author declares no competing interests. The research received no external funding. All data are from Yahoo Finance via the `yfinance` Python package; no proprietary or restricted data are used. The complete analysis code, manuscript source, and replication guide are archived at Zenodo (concept DOI: 10.5281/zenodo.19611543, always resolving to the latest version) and GitHub (github.com/mhdk1602/fractal-pv-coupling).

## Research lineage and revision history

The paper builds on earlier master's-level work I undertook at King's College London in 2013 under the supervision of Dr. Enzo De Sena. That project examined whether Hurst-based fractal characteristics of stock-price series were associated with average trading volume in the cross section, and found a weak but statistically significant static relationship. The present paper is substantially different in question, method, and contribution: it shifts from static cross-sectional association to temporal co-evolution within firms, introduces the dynamic CII, runs a formal horse race against nine standard liquidity benchmarks, and applies publication-grade small-sample inference. I disclose this lineage here for completeness; the 2013 MSc report is archived with the submission materials.

The manuscript has previously been circulated as an SSRN preprint. Earlier preprint versions reported a positive predictive result for CII against a share-volume Amihud variant. The present version corrects that result by switching to the standard dollar-volume Amihud convention, documenting the divergence, and treating the share-volume vs. dollar-volume comparison as a substantive finding rather than a hidden specification choice. The revision strengthens the paper's methodological honesty and is the version submitted here.

## Suggested reviewers

I would be grateful if the editorial team considered reviewers active in the econophysics-finance interface. Without suggesting specific individuals, scholars with prior publications in *Quantitative Finance* on power-law cross-correlations, Hurst exponent estimation in finance, or liquidity-proxy evaluation would be well placed to evaluate the methodological choices.

Thank you for your consideration.

Yours sincerely,

Dineshkumar Malempati Hari
Independent Researcher
ORCID: 0009-0003-1036-9477
