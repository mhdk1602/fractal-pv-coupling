# Cover Letter: Quantitative Finance

---

Dinesh Hari
Independent Researcher
mhdk.dinesh@gmail.com
ORCID: 0009-0003-1036-9477

[Date]

The Editors
*Quantitative Finance*
Taylor & Francis

Dear Editors,

I am pleased to submit the manuscript "Static and Temporal Fractal Coupling Between Volatility and Trading Volume: Evidence from S&P 500 Stocks, 2015–2026" for consideration in *Quantitative Finance*. The paper develops a dynamic measure of fractal memory co-evolution and demonstrates that it carries statistically significant predictive information for market illiquidity that is orthogonal to the standard liquidity-proxy toolkit.

## Contribution

The paper introduces the Coupling Intensity Index (CII), a time-varying measure of whether the Hurst exponents of absolute returns and log-volume move together within a firm. CII captures a second-order fractal property: how memory structures co-evolve rather than what they are in the cross-section. Across 50 S&P 500 constituents over 2015–2026, I find that the cross-sectional relationship between full-sample Hurst exponents is null ($r = -0.02$), yet within-firm temporal coupling is strong and positive in 49 of 50 equities (mean $r = 0.665$). This static-versus-temporal paradox is the paper's organizing tension.

Panel predictive regressions with firm fixed effects establish that CII predicts future Amihud illiquidity at the one-month horizon. The coefficient survives five standard-error specifications, including two-way clustering by firm and time following Cameron, Gelbach, and Miller (2011), and small-sample corrections including Bell-McCaffrey CR2 with Satterthwaite effective degrees of freedom (Imbens and Kolesár, 2016) and the wild cluster restricted bootstrap (Cameron, Gelbach, and Miller, 2008; MacKinnon and Webb, 2017). In a formal horse race against nine standard liquidity predictors, including lagged Amihud, VIX, Corwin-Schultz, Roll spread, turnover, and volatility of volatility, CII retains significance under the WCR bootstrap at $p = 0.018$. The paper also reports a clean null: CII does not predict realised volatility once inference properly accounts for cross-sectional and temporal dependence. This asymmetry is central to the interpretation: the signal concerns market function and liquidity regimes, not price dynamics directly.

## Fit with *Quantitative Finance*

The paper combines three strands that the journal has historically supported. First, it applies detrended fluctuation analysis and related long-memory tools drawn from econophysics to a representative U.S. equity sample, extending work by Podobnik, Kristoufek, and others published in the journal. Second, it operates within the empirical finance tradition of Amihud, Goyenko-Holden-Trzcinka, and Hasbrouck on liquidity measurement, testing the novel measure against the standard benchmarks that a finance referee would demand. Third, it adheres to the small-sample-corrected cluster-robust inference that the journal's recent methodology-rigorous submissions have used. The synthesis of these three, with honest reporting of both positive and null findings, is what the paper offers.

## Declarations

The manuscript is a single-author submission, is not under consideration elsewhere, and has not been previously published in whole or in part. The author declares no competing interests. The research received no external funding. All data are from Yahoo Finance via the `yfinance` Python package; no proprietary or restricted data are used. The complete analysis code and manuscript source are archived at Zenodo (DOI: 10.5281/zenodo.19611544) and GitHub (github.com/mhdk1602/fractal-pv-coupling). A step-by-step replication guide appears as Appendix B of the manuscript.

## Research lineage

The paper builds on earlier master's-level work I undertook at King's College London in 2013 under the supervision of Dr. Enzo De Sena. That project examined whether Hurst-based fractal characteristics of stock-price series were associated with average trading volume in the cross section, and found a weak but statistically significant static relationship. The present paper is substantially different in question, method, and contribution. It shifts from static cross-sectional association to temporal co-evolution; introduces the dynamic Coupling Intensity Index; conditions the predictive regressions on standard liquidity benchmarks in a formal horse race; and applies publication-grade small-sample inference (Bell-McCaffrey CR2; WCR bootstrap). I disclose this lineage here for completeness; the 2013 MSc report is archived with the submission materials.

## Suggested reviewers

I would be grateful if the editorial team considered reviewers active in the econophysics-finance interface. Without suggesting specific individuals, scholars with prior publications in *Quantitative Finance* on power-law cross-correlations, Hurst exponent estimation in finance, or liquidity-proxy evaluation would be well placed to evaluate the methodological choices.

Thank you for your consideration.

Yours sincerely,

Dinesh Hari
Independent Researcher
ORCID: 0009-0003-1036-9477
