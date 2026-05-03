# Research Topic Approval — Fractal Price-Volume Coupling

| | |
|---|---|
| **Project title** | Temporal Fractal Coupling of Volatility and Trading Volume in S&P 500 Stocks |
| **Researcher** | Dineshkumar Malempati Hari |
| **ORCID** | [0009-0003-1036-9477](https://orcid.org/0009-0003-1036-9477) |
| **Affiliation** | Independent Researcher (post-PhD candidate, University of the Cumberlands; defense ~2027) |
| **Status at this writing** | Manuscript v1.4.1; Zenodo concept DOI `10.5281/zenodo.19611543`; SSRN preprint published; pre-registered Phase 2 universe expansion to G = 488 complete |
| **Target venue** | *Physica A: Statistical Mechanics and its Applications* (Elsevier, primary), with a fallback ladder of *Quantitative Finance*, *Journal of Empirical Finance*, *Finance Research Letters* |
| **Submission timing** | Post-PhD defense; target window of 90 days after defense |

This document summarises the research project at the level of a doctoral-style topic approval: purpose, hypotheses, data, methods, decision rules, current findings, contribution, scope, and follow-on work. It is the canonical brief I will use to introduce the project in any future formal context (committee discussion, journal correspondence, grant application, conference abstract).

---

## 1. Purpose

This research investigates whether the fractal scaling properties of equity price volatility and trading volume — specifically, the Hurst exponents of absolute returns and log-volume — co-evolve through time within firms, whether that co-evolution is regime-dependent, and whether it carries incremental predictive content for forward market-quality outcomes (illiquidity, realised volatility, spread proxies, drawdown, abnormal turnover) at the firm-month horizon. The project introduces the **Coupling Intensity Index (CII)** as a measurement object that captures temporal co-evolution between two rolling Hurst exponent series within a firm, distinct from the first-order cross-correlation captured by detrended cross-correlation analysis or scale-by-scale wavelet methods.

The research is framed within the econophysics-meets-empirical-asset-pricing literature, drawing methodological tools from both traditions: detrended fluctuation analysis from the statistical-mechanics literature, modern cluster-robust panel inference from the empirical-finance methodology literature.

---

## 2. Research Questions and Hypotheses

The project is organised around four pre-specified hypotheses inherited from a 2013 Master's project at King's College London (\cite{hari2013fractal}) and refined into the present study's framework.

**H1 — Static cross-sectional coupling.** Does the average level of volatility persistence ($H_{|r|}$) in the cross-section of firms covary with the average level of volume persistence ($H_v$)?

**H2 — Within-firm temporal coupling.** Do rolling Hurst exponents for $|r_t|$ and $\log V_t$ co-move positively within firms over time?

**H3 — Regime dependence.** Does the within-firm temporal coupling intensify during high-uncertainty regimes (operationalised via the CBOE VIX index)?

**H4 — Predictive content.** Does CII have incremental predictive content for forward market-quality outcomes (Amihud illiquidity, realised volatility, the Corwin-Schultz spread, the Roll spread, vol-of-vol, max drawdown, abnormal turnover, $\log$ Amihud, $\Delta$Amihud), beyond the standard liquidity-and-volatility benchmark toolkit?

The hypotheses are tested under a pre-registered protocol committed to the public repository before any data fetch beyond the original 50-firm sample (see Section 6). The protocol fixes the universe, inclusion criteria, pipeline, target list, decision rule, and disallowed ex-post modifications.

---

## 3. Background and Significance

### 3.1 Long memory in financial time series

Mandelbrot \cite{mandelbrot1963variation, mandelbrot1968fractional} first demonstrated that financial prices exhibit non-Gaussian, scale-invariant properties. The Hurst exponent $H$, originally developed for hydrological flow series \cite{hurst1951long} and formalised through fractional Brownian motion, provides the standard measure of long-range dependence. Cont \cite{cont2001empirical} catalogued slow autocorrelation decay in absolute returns as one of the most robust stylised facts in finance. Ding, Granger, and Engle \cite{ding1993long} showed that this long memory is strongest for $|r_t|^d$ at $d \approx 1$, persisting over hundreds of lags. Lobato and Velasco \cite{lobato2000long} provided rigorous evidence for fractional integration in volume, with $H \approx 0.7$ to $0.9$ across NYSE equities. Bollerslev and Jubinski \cite{bollerslev1999equity} identified a common long-memory component shared by volatility and volume using ARFIMA methods.

These foundational results establish that volatility and volume each exhibit long memory; whether the *scaling exponents themselves* co-evolve over time within a firm is the second-order question this paper addresses.

### 3.2 Joint dynamics: MDH and beyond

The Mixture of Distributions Hypothesis \cite{clark1973subordinated, tauchen1983price, andersen1996return} posits a latent information arrival process that simultaneously governs volatility and volume. Under MDH, intensified information flow drives both persistence structures upward together. Sequential information-arrival theories \cite{copeland1976model} draw a sharper temporal asymmetry. Volatility-liquidity spirals as formalised by Brunnermeier and Pedersen \cite{brunnermeier2009market} predict that rising volatility tightens funding constraints and reduces market liquidity. Inventory-based microstructure theories \cite{ho1981optimal} predict synchronised inventory dynamics. None of these channels has been tested directly via second-order fractal coupling, which is the gap this project fills.

### 3.3 Cluster-robust inference at moderate cluster counts

Cameron, Gelbach, and Miller \cite{cameron2011robust, cameron2008bootstrap} developed two-way clustered standard errors and the wild cluster bootstrap. Imbens and Kolesár \cite{imbens2016robust} recommend Bell-McCaffrey CR2 with Satterthwaite degrees of freedom as a routine diagnostic at moderate $G$. MacKinnon and Webb \cite{mackinnon2017wild} support wild bootstrap methods in unbalanced clustered settings. Cameron and Miller \cite{cameron2015practitioners} survey the practitioner choices. The present project applies the full menu of these methods and contributes a documentation of how the firm-conditional vs time-conditional inference choice can change conclusions when residual dependence is strong on both dimensions.

### 3.4 Liquidity proxies

Amihud \cite{amihud2002illiquidity} introduced the daily ratio of absolute return to dollar volume as a measure of price impact per unit of trading volume. Roll \cite{roll1984spread} introduced an implicit-spread estimator from daily return autocovariance. Corwin and Schultz \cite{corwin2012simple} introduced a high-low spread estimator. Goyenko, Holden, and Trzcinka \cite{goyenko2009liquidity} systematically compared these and other proxies against benchmark liquidity notions. Hasbrouck \cite{hasbrouck2009trading} and Abdi and Ranaldo \cite{abdi2017simple} contributed alternative effective-spread estimators. The horse race specification in this project follows GHT \cite{goyenko2009liquidity} §5.2 directly, conditioning the focal CII coefficient on nine standard liquidity benchmarks simultaneously.

---

## 4. Data Collection Method

### 4.1 Source

Daily Open-High-Low-Close-Volume (OHLCV) data for the universe of equities, sourced from Yahoo Finance via the open-source Python package `yfinance` (version 1.2.0). VIX data sourced from the same Yahoo Finance feed.

### 4.2 Universe

The current April 2026 S&P 500 constituency, retrieved as a frozen CSV from the public dataset at `datasets/s-and-p-500-companies` on the day of fetch and committed to the repository at `data/sp500_constituents_2026-04-28.csv`. Constituency is current rather than point-in-time; this convention is shared with most prior empirical work using S&P 500 panels and is disclosed in the manuscript's limitations section. The construction would benefit from CRSP-based historical point-in-time membership; the cost of WRDS access put this outside the scope of the present project.

### 4.3 Time period

January 2, 2015 through April 1, 2026 (approximately 2,800 trading days per equity).

### 4.4 Sample inclusion criteria

A firm enters the analysis panel if:

- Yahoo Finance returns at least 600 daily observations over the window (a working minimum for reliable DFA estimation per Peng et al. \cite{peng1994mosaic}).
- The log-return series passes both the Augmented Dickey-Fuller test ($p < 0.01$) and the KPSS test ($p > 0.10$) for stationarity.
- The price series has no zero or missing volumes for more than 5% of trading days.

Of 503 attempted tickers, 4 dropped at the fetch stage (insufficient observations), and approximately 11 dropped during the panel build (stationarity or data quality). The Phase 2 panel comprises **488 firms** spanning all eleven GICS sectors.

### 4.5 An earlier large-cap sample

A 50-firm subset of the same S&P 500 universe (large-cap-leaning, hand-selected) was used in the v1.0 through v1.2 versions of this study. The v1.3 version (Phase 2 universe expansion) extends to the full S&P 500 under a pre-registered protocol. The 50-firm subset persists in the codebase for backward-compatibility replication of v1.0 through v1.2 results.

### 4.6 Storage and replication

Raw OHLCV is cached as parquet files under `data/raw/sp500_phase2/` (gitignored due to redistribution restrictions on Yahoo Finance data). Intermediate panel and rolling-Hurst pickles are cached under `research/horse_race/cache/` for both pipelines. The complete Phase 2 run is reproducible from the constituent CSV plus a clean Python environment in approximately 60-75 minutes of wall-clock on a single workstation. The pipeline freeze under the pre-registration protocol applies to all v1.4.x results.

---

## 5. Analysis Methods

### 5.1 Detrended Fluctuation Analysis (DFA)

For a time series $\{x_t\}_{t=1}^N$, the DFA-1 procedure constructs the cumulative profile $Y(k) = \sum_{t=1}^k (x_t - \bar{x})$, divides it into non-overlapping windows of length $s$, detrends each by a fitted polynomial of order 1, and computes the fluctuation function $F(s)$. For long-range correlated processes, $F(s) \sim s^H$, and $H$ is estimated as the OLS slope of $\log F(s)$ vs $\log s$. Scale range: $s_{\min} = 10$ to $s_{\max} = \lfloor N / 4 \rfloor$ with logarithmic spacing.

Independent verification: a parallel implementation from the open-source `nolds` package is run alongside our wrapper. Cross-implementation Spearman rank correlation is 0.93 for absolute returns and 0.79 for log-volume, confirming the DFA-1 results are not implementation-specific. Lo-style R/S \cite{lo1991long} is also run as a separate cross-estimator check; the documented R/S downward bias is observed at the levels predicted by Lo (mean $H$ difference of 0.18 for absolute returns, 0.15 for volume), and the rank order of firms is preserved (Spearman $\rho = 0.52$ and $0.40$).

### 5.2 Rolling Hurst exponents and the Coupling Intensity Index

For each firm $i$, the rolling Hurst exponent at calendar date $t$ is computed in a backward-looking window of $W = 500$ trading days, evaluated at every $\Delta = 20$ trading days (approximately monthly). This produces aligned series $H^{(i)}_{|r|,t}$ and $H^{(i)}_{v,t}$.

The **Coupling Intensity Index** at date $t$ for firm $i$ is the rolling Pearson correlation between the two Hurst series over a trailing window of $L = 30$ rolling-Hurst observations (approximately 600 trailing trading days):

$$\mathrm{CII}^{(i)}_t = \mathrm{Corr}\left(H^{(i)}_{|r|, \mathcal{T}_{t,L}}, H^{(i)}_{v, \mathcal{T}_{t,L}}\right)$$

where $\mathcal{T}_{t,L}$ denotes the $L$ most recent rolling-Hurst evaluation dates up to and including $t$. The CII is computable using only data through $t$; all predictive outcome variables are measured strictly forward over $[t+1, t+h]$ with $h = 21$ trading days (one month).

### 5.3 Predictive panel regression

Predictive regressions take the form

$$Y^{(i)}_{t+h} = \alpha_i + \beta_1 \mathrm{CII}^{(i)}_t + \beta_2 H^{(i)}_{|r|, t} + \beta_3 H^{(i)}_{v, t} + \varepsilon^{(i)}_t$$

with firm fixed effects $\alpha_i$. The coefficient of interest is $\beta_1$. The Phase 2 horse race additionally conditions on nine standard liquidity benchmarks following Goyenko-Holden-Trzcinka \cite{goyenko2009liquidity} §5.2: Roll spread, Corwin-Schultz $\mathrm{MSPREAD}_0$, dollar-volume rolling Amihud, lagged realised volatility, lagged Amihud, vol-of-vol, normalised turnover, abnormal-turnover spike, and Cboe VIX.

### 5.4 Inference suite

The Phase 2 protocol commits in advance to the following inference menu, applied to every focal regression:

- **HC1** (heteroskedasticity-consistent White SE; reference only).
- **Firm-clustered** $t(G_{\text{firm}} - 1)$.
- **Time-clustered** $t(G_{\text{month}} - 1)$.
- **Two-way clustered** with the Cameron-Gelbach-Miller \cite{cameron2011robust} eigenvalue PSD adjustment.
- **Newey-West** with automatic bandwidth (reference only; flagged for Driscoll-Kraay replacement).
- **Driscoll-Kraay** \cite{driscoll1998consistent} with Bartlett bandwidth $\geq 21$.
- **Bell-McCaffrey CR2** with Satterthwaite effective degrees of freedom \cite{imbens2016robust}, computed at the firm dimension.
- **Wild cluster restricted bootstrap** with 999 Rademacher resamples under the null \cite{cameron2008bootstrap, mackinnon2017wild}.

This is the full Cameron-Miller \cite{cameron2015practitioners} practitioner menu plus the small-sample corrections of Imbens-Kolesár and MacKinnon-Webb. Reporting all eight on every focal coefficient prevents inference-method cherry-picking and is one of the project's methodological-discipline anchors.

### 5.5 Forward outcome variables

Ten outcomes are tested in the Phase 2 battery:

1. **Standard Amihud illiquidity** (dollar-volume convention): $\mathrm{ILLIQ}^{(i)}_{t+h} = (10^6 / h) \sum_{\tau=t+1}^{t+h} |r^{(i)}_\tau| / (V^{(i)}_\tau \cdot P^{(i)}_\tau)$.
2. $\log$ Amihud.
3. $\Delta$Amihud (forward minus contemporaneous).
4. Forward Corwin-Schultz spread.
5. Forward Roll spread.
6. Forward vol-of-vol.
7. Realised volatility: $\mathrm{RV}^{(i)}_{t+h} = \sqrt{\sum_{\tau=t+1}^{t+h} (r^{(i)}_\tau)^2}$.
8. Maximum drawdown.
9. Abnormal turnover.
10. The list is closed at ten in the pre-registration. No targets were added after the run.

---

## 6. Pre-Registration

The Phase 2 universe expansion was executed under a pre-registration protocol (`research/horse_race/PHASE2_PROTOCOL.md`, version 1.0) committed to the public repository at master HEAD `f8aa564` before any data fetch beyond the original 50-firm sample. The protocol fixed in advance:

- The universe (current April 2026 S&P 500 constituency).
- The inclusion criteria (≥ 600 obs, ADF/KPSS, ≤ 5% missing volume).
- The pipeline freeze (no code change between protocol freeze and run that affects estimated coefficients or inference).
- The ten target specifications (no additions or substitutions allowed after the run).
- A per-target decision rule with explicit p-value thresholds for three categories:
  - **Category A** (predictive null confirmed): two-way cluster $p$ AND Driscoll-Kraay $p$ AND wild cluster bootstrap $p$ all $> 0.10$.
  - **Category B** (combined-spec robust signal): two-way cluster $p$ AND Driscoll-Kraay $p$ AND wild cluster bootstrap $p$ all $< 0.05$ with Bell-McCaffrey CR2 $p < 0.10$ in the combined-with-9-benchmarks specification, plus same-sign and magnitude $\geq 25\%$ of the focal-only estimate.
  - **Category C** (mixed): anything between A and B.

The protocol explicitly disallows post-run reframing of a Category C outcome as Category B, post-run target additions, post-run window-parameter changes, and post-run inference-method substitutions. This discipline is uncommon in empirical asset pricing and is one of the project's portable contributions.

---

## 7. Empirical Findings to Date (v1.4.1)

### 7.1 Descriptive contributions

**H1 — Static coupling, weak but detectable at $G = 488$.** Cross-sectional Pearson correlation between full-sample $H_{|r|}$ and $H_v$ at the broader sample is $r = 0.183$ ($t = 4.11$, $p < 0.001$, $n = 488$); Spearman $\rho = 0.163$ ($p = 0.0003$). The original v1.0 50-firm sample reported a null on the same construction; the broader panel surfaces a small but statistically significant positive cross-sectional dependence that the smaller sample lacked the power to detect. The cross-sectional dependence explains roughly 3.4% of the variation. The within-firm temporal coupling (H2 below) is roughly threefold stronger and structurally different.

**H2 — Within-firm temporal coupling, strongly confirmed.** Mean within-firm $r = 0.531$ across the 488-firm panel, median 0.615, 92.7% of firms exhibiting positive coupling, 80.4% above $r = 0.3$, 64.5% above $r = 0.5$. Range: minimum $-0.570$, maximum $0.974$. Universal across all eleven GICS sectors (sector means range from Energy at 0.660 to Utilities at 0.412; every sector has at least 87% of firms positive). This is the project's strongest descriptive empirical result.

**H3 — Regime amplification of heterogeneity, not mean shift.** Mann-Whitney high-vs-low VIX $U = 135{,}542$, $p = 0.0019$. But mean coupling is essentially identical across regimes (low 0.567, mid 0.497, high 0.563). What the test detects at $G = 488$ is a distributional shift: the high-VIX regime exhibits a higher median (0.738 vs 0.666), a longer upper tail of strongly-coupled firms, and substantially larger cross-firm dispersion ($\sigma = 0.45$ vs $\sigma = 0.34$). Coupling does not uniformly intensify during stress; the cross-section fans out.

### 7.2 Predictive contribution: structured null

**H4 rejected at the firm-month unit of analysis.** Under firm-conditional cluster-robust inference (firm-clustered, two-way clustered, Bell-McCaffrey CR2, wild cluster restricted bootstrap), the CII coefficient is statistically null for every one of the ten forward outcomes tested in this paper, in every focal-only and combined specification. The horse race against the nine standard liquidity benchmarks is decisive: every focal-only signal is fully absorbed in the combined specification regardless of which SE method is used. The cleanest illustration is the forward Corwin-Schultz spread: focal two-way $t = +3.64$ collapses to combined $t = +0.07$ (a four-orders-of-magnitude coefficient drop).

**Time-conditional inference detects cross-firm time-period co-movement.** Under time-clustered standard errors and Driscoll-Kraay HAC, several focal-only signals reach the 5% threshold for the primary outcome and for five of the eight secondary outcomes. The natural reading: CII inherits a market-wide stress co-movement that aggregates across firms in a given month, but adds no firm-specific predictive content beyond what the standard nine-benchmark toolkit captures.

### 7.3 Methodological contributions

The paper documents three transferable methodological observations.

**Observation 1 — Dollar-volume vs share-volume Amihud.** An apparently strong predictive result against a non-standard share-volume Amihud denominator ($|r|/V$) dissipates once the standard dollar-volume convention ($|r| / (V \cdot P)$) is applied. The arithmetic decomposition $\widetilde{\mathrm{ILLIQ}} = \mathrm{ILLIQ} \cdot P$ shows that the share-volume proxy carries a price-level multiplicative factor that any regressor correlated with within-firm price drift will appear to forecast. Cluster-robust inference, including the wild cluster restricted bootstrap, does not detect this confound: the diagnosis lives in the dependent-variable definition rather than in the standard errors.

**Observation 2 — Firm-conditional vs time-conditional inference disagreement.** When residual dependence is strong on both dimensions of a panel, firm-conditional methods (firm-clustered, two-way, CR2, WCR) and time-conditional methods (time-clustered, Driscoll-Kraay) can disagree at the same data. Both readings are correct under their respective assumptions; the choice of which to call "the" inference depends on whether the unit of forecast is firm-month or time-period. Reporting both transparently and matching the inference dimension to the unit of analysis claimed is the honest path.

**Observation 3 — Satterthwaite degrees-of-freedom collapse at moderate cluster counts.** The Bell-McCaffrey CR2 Satterthwaite effective degrees of freedom collapsed from approximately 6 at $G = 50$ to approximately 1.0 at $G = 488$, despite the cluster count rising 9.8 times. The mechanism: the Satterthwaite df is governed by the second moments of cluster-level score contributions, not by cluster count. A small number of leverage-heterogeneous firms (typically illiquid small-cap or recent-IPO names with extreme Amihud values) dominate the meat matrix. CR2 has effectively no power at df $= 1.0$. Researchers running cluster-robust inference at moderate $G$ should report the Satterthwaite check as a routine diagnostic rather than assume it scales with cluster count.

---

## 8. Outputs and Deliverables

| Output | Status | Identifier |
|---|---|---|
| Manuscript v1.4.1 | Complete | `research/paper/main.pdf` (410 KB, 36-38 pages) |
| Bibliography | Complete | `research/paper/references.bib` |
| Cover letter | Complete | `research/submission/cover_letter_quantfinance.md` (also fits Physica A with light edits) |
| arXiv abstract | Complete | `research/submission/arxiv_abstract.md` |
| Pre-registration document | Complete | `research/horse_race/PHASE2_PROTOCOL.md` |
| Phase 2 results memo | Complete | `research/horse_race/PHASE2_RESULTS.md` |
| Replication code | Complete | `src/fractal_pv/` package + `research/horse_race/run_*.py` runners |
| Public GitHub repository | Live | https://github.com/mhdk1602/fractal-pv-coupling |
| Zenodo concept DOI (always-latest) | Live | `10.5281/zenodo.19611543` |
| Zenodo v1.4.1 version DOI | Live | `10.5281/zenodo.19976120` |
| ORCID linkage | Live | `0009-0003-1036-9477` |
| SSRN preprint | Live; v1.4.1 update pending manual upload | author dashboard |
| arXiv preprint | Pending De Sena endorsement (deadline 2026-05-06; backup-endorser path triggers afterward) | q-fin.ST primary, stat.ME / cond-mat.stat-mech cross-list |
| Streamlit dashboard for per-firm exploration | Live | `fractal-pv.streamlit.app` |
| Journal submission | Deferred to post-PhD; target Physica A within 90 days of defense | — |

---

## 9. Timeline and Milestones

| Phase | Status |
|---|---|
| MSc origin study at King's College London (supervised by Dr. Enzo De Sena) | Complete (2013) |
| v1.0 50-firm large-cap analysis | Complete |
| v1.1 horse race against 9 benchmarks; Tier 3 small-sample inference | Complete |
| v1.2 share-volume Amihud confound corrected; honest-null framing | Complete |
| v1.3 Phase 2 universe expansion to G = 488 under pre-registered protocol | Complete |
| v1.4.0 journal-readiness pass (per-benchmark, Hurst-estimator robustness, aggregate-CII, mechanism, multiple-testing) | Complete |
| v1.4.1 H1 reframe at G = 488; phrasing precision | Complete |
| External independent peer review | Pending |
| Professional copyedit | Pending (post-PhD) |
| Pre-submission audit | Pending (post-PhD) |
| **Physica A submission** | **Within 90 days of PhD defense** |

---

## 10. Limitations and Scope Boundaries

The sample comprises 488 current S&P 500 constituents. Generalisability to small-cap, mid-cap (Russell 2000), international (FTSE 100, Nikkei, DAX, Hang Seng), or alternative-asset (ETFs, futures, cryptocurrencies) panels is not established and is the natural follow-on direction.

The analysis uses daily data. Intraday frequencies could reveal richer dynamics around scheduled information events (FOMC announcements, earnings releases, macroeconomic data releases) that monthly aggregation absorbs. Phase 3 (intraday) is deferred.

Constituency is current April 2026 rather than CRSP-based historical point-in-time membership. Survivorship bias is inherent to this construction. The fix would require WRDS access, which sits outside the scope of an independent-researcher project.

CII is constructed from rolling Hurst exponents that carry estimation error. The paper does not propagate this measurement error into the predictive regressions; a fuller treatment would do so via simulation-based standard errors or a measurement-error correction.

The Granger causality results reported alongside H2 should be interpreted as exploratory given the irregular spacing and overlapping-window construction of the rolling Hurst estimates.

The Satterthwaite df = 1.0 collapse at $G = 488$ suggests that further cluster-robust diagnostics (cluster-jackknife, alternative wild bootstrap variants) could refine the inference at this sample size. The agreement between firm-clustered, two-way, CR2, and WCR makes the firm-specific null at $G = 488$ a stable conclusion regardless.

---

## 11. Future Work

The aggregate-CII vs VIX exhibit (Figure 10 in v1.4.x) shows that the cross-sectionally aggregated CII has weak but statistically detectable correlation with VIX, suggesting a richer cross-sectional structure than the simple aggregate-stress channel. A natural Paper 2 sketch:

> **"Aggregate Fractal Coupling as a Market-Wide Liquidity Stress Indicator"**: cross-sectionally aggregated CII as a market-time-series object; tests of correlation with the NY Fed Cleveland Financial Stress Index, the Pastor-Stambaugh liquidity factor, the BAA-Treasury credit spread, and the VIX; whether the aggregate signal leads or follows these established stress measures.

Phase 3 (intraday) and Phase 4 (cross-asset) extensions are listed in the manuscript's Limitations section and remain follow-on candidates for the post-PhD research program.

---

## 12. Selected References

Mandelbrot, B. B. (1963). The variation of certain speculative prices. *Journal of Business* 36(4), 394-419.

Hurst, H. E. (1951). Long-term storage capacity of reservoirs. *Transactions of the American Society of Civil Engineers* 116, 770-808.

Lo, A. W. (1991). Long-term memory in stock market prices. *Econometrica* 59(5), 1279-1313.

Peng, C.-K., Buldyrev, S. V., Havlin, S., Simons, M., Stanley, H. E., & Goldberger, A. L. (1994). Mosaic organization of DNA nucleotide sequences. *Physical Review E* 49(2), 1685-1689.

Cont, R. (2001). Empirical properties of asset returns: stylized facts and statistical issues. *Quantitative Finance* 1(2), 223-236.

Lobato, I. N., & Velasco, C. (2000). Long memory in stock-market trading volume. *Journal of Business and Economic Statistics* 18(4), 410-427.

Bollerslev, T., & Jubinski, D. (1999). Equity trading volume and volatility: latent information arrivals and common long-run dependencies. *Journal of Business and Economic Statistics* 17(1), 9-21.

Clark, P. K. (1973). A subordinated stochastic process model with finite variance for speculative prices. *Econometrica* 41(1), 135-155.

Tauchen, G. E., & Pitts, M. (1983). The price variability-volume relationship on speculative markets. *Econometrica* 51(2), 485-505.

Andersen, T. G. (1996). Return volatility and trading volume: an information flow interpretation of stochastic volatility. *Journal of Finance* 51(1), 169-204.

Brunnermeier, M. K., & Pedersen, L. H. (2009). Market liquidity and funding liquidity. *Review of Financial Studies* 22(6), 2201-2238.

Kyle, A. S. (1985). Continuous auctions and insider trading. *Econometrica* 53(6), 1315-1335.

Amihud, Y. (2002). Illiquidity and stock returns: cross-section and time-series effects. *Journal of Financial Markets* 5(1), 31-56.

Roll, R. (1984). A simple implicit measure of the effective bid-ask spread in an efficient market. *Journal of Finance* 39(4), 1127-1139.

Corwin, S. A., & Schultz, P. (2012). A simple way to estimate bid-ask spreads from daily high and low prices. *Journal of Finance* 67(2), 719-760.

Goyenko, R. Y., Holden, C. W., & Trzcinka, C. A. (2009). Do liquidity measures measure liquidity? *Journal of Financial Economics* 92(2), 153-181.

Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources* 50(2), 317-372.

Imbens, G. W., & Kolesár, M. (2016). Robust standard errors in small samples: some practical advice. *Review of Economics and Statistics* 98(4), 701-712.

MacKinnon, J. G., & Webb, M. D. (2017). Wild bootstrap inference for wildly different cluster sizes. *Journal of Applied Econometrics* 32(2), 233-254.

Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics* 90(3), 414-427.

Driscoll, J. C., & Kraay, A. C. (1998). Consistent covariance matrix estimation with spatially dependent panel data. *Review of Economics and Statistics* 80(4), 549-560.

A complete bibliography appears in `research/paper/references.bib`.
