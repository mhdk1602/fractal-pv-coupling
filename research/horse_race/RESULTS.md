# Horse Race Results: CII vs Standard Liquidity Benchmarks

Generated: 2026-04-27 20:46

## Panel summary

- tickers (after rolling + enrichment): 50
- total rows: 4400
- date range: 2018-05-18 to 2025-04-22
- benchmarks available: roll_spread, corwin_schultz, amihud_rolling, turnover, vol_of_vol, lagged_rv, lagged_illiq, abn_turnover_t, vix

## Specifications

Three classes of regressions per target, following Goyenko-Holden-Trzcinka (2009, JFE 92) §5.2. All regressions include firm fixed effects via within demeaning. Degrees of freedom: HC1 and Newey-West at t(n−k); one-way clusters at t(G−1); two-way at t(min(G₁,G₂)−1). The two-way clustered t-statistic is the primary basis for inference, per Cameron-Gelbach-Miller (2011, JBES).

Benchmarks included:

- `roll_spread` — Roll (1984) proportional effective spread
- `corwin_schultz` — Corwin-Schultz (2012) MSPREAD_0 with overnight adjustment
- `amihud_rolling` — Amihud (2002) illiquidity, rolling 21-day, dollar-volume, 10⁶ scaling
- `turnover` — Normalized turnover (current / trailing mean)
- `vol_of_vol` — Realized volatility of realized volatility
- `lagged_rv` — Lagged realized volatility (past horizon)
- `lagged_illiq` — Lagged Amihud over past horizon (baseline from enriched panel)
- `abn_turnover_t` — Abnormal turnover spike
- `vix` — Cboe VIX level

## Results by target

### Target: `amihud_illiq`

#### Focal alone + controls

| Variable | β | SE method | t | p | df |
|----------|---|-----------|---|---|-----|
| **CII** | 4.01e-07 | HC1 | 1.16 | 0.2455 | 4397 |
|  |  | firm_cluster | 0.41 | 0.6870 | 49 |
|  |  | time_cluster | 0.50 | 0.6205 | 82 |
|  |  | twoway_cluster | 0.33 | 0.7452 | 49 |
|  |  | newey_west | 0.56 | 0.5788 | 4397 |
|  |  | driscoll_kraay | 0.21 | 0.8328 | 85 |

_n = 4400, firms = 50, months = 83, R² = 0.153_

#### Per-benchmark regressions

| Benchmark | β | t (HC1) | t (firm) | t (twoway) | p (twoway) | R² | n |
|-----------|---|---------|----------|------------|------------|-----|---|
| roll_spread | 0.000131 | 6.63 | 6.59 | 2.42 | 0.0192 | 0.190 | 4400 |
| corwin_schultz | 0.00068 | 8.50 | 7.91 | 2.78 | 0.0078 | 0.191 | 4400 |
| amihud_rolling | 0.669 | 24.35 | 32.92 | 9.83 | 0.0000 | 0.485 | 4400 |
| turnover | -8.26e-07 | -3.56 | -4.87 | -1.36 | 0.1814 | 0.155 | 4400 |
| vol_of_vol | 1.86e-05 | 6.13 | 5.41 | 2.30 | 0.0260 | 0.169 | 4400 |
| lagged_rv | 4.46e-05 | 7.75 | 6.64 | 2.41 | 0.0196 | 0.191 | 4400 |
| lagged_illiq | 0.649 | 22.42 | 30.28 | 8.60 | 0.0000 | 0.463 | 4400 |
| abn_turnover_t | -3.28e-07 | -1.18 | -1.64 | -0.36 | 0.7237 | 0.154 | 4400 |
| vix | 2.58e-07 | 9.28 | 7.70 | 3.48 | 0.0011 | 0.212 | 4400 |

#### Combined specification (CII + all benchmarks + controls)


| Variable | β | SE method | t | p | df |
|----------|---|-----------|---|---|-----|
| **CII** | -2.23e-07 | HC1 | -0.85 | 0.3936 | 4388 |
|  |  | firm_cluster | -0.71 | 0.4783 | 49 |
|  |  | time_cluster | -0.35 | 0.7235 | 82 |
|  |  | twoway_cluster | -0.34 | 0.7335 | 49 |
|  |  | newey_west | -0.81 | 0.4171 | 4388 |
|  |  | driscoll_kraay | -0.52 | 0.6045 | 76 |
| **roll_spread** | 9.63e-06 | HC1 | 0.86 | 0.3881 | 4388 |
|  |  | firm_cluster | 0.82 | 0.4150 | 49 |
|  |  | time_cluster | 0.55 | 0.5829 | 82 |
|  |  | twoway_cluster | 0.54 | 0.5904 | 49 |
|  |  | newey_west | 0.87 | 0.3821 | 4388 |
|  |  | driscoll_kraay | 0.63 | 0.5283 | 76 |
| **corwin_schultz** | -6.84e-05 | HC1 | -1.07 | 0.2836 | 4388 |
|  |  | firm_cluster | -1.23 | 0.2229 | 49 |
|  |  | time_cluster | -0.80 | 0.4288 | 82 |
|  |  | twoway_cluster | -0.86 | 0.3961 | 49 |
|  |  | newey_west | -1.10 | 0.2714 | 4388 |
|  |  | driscoll_kraay | -0.89 | 0.3746 | 76 |
| **amihud_rolling** | 1.6 | HC1 | 10.22 | 0.0000 | 4388 |
|  |  | firm_cluster | 12.45 | 0.0000 | 49 |
|  |  | time_cluster | 5.84 | 0.0000 | 82 |
|  |  | twoway_cluster | 6.15 | 0.0000 | 49 |
|  |  | newey_west | 10.89 | 0.0000 | 4388 |
|  |  | driscoll_kraay | 4.88 | 0.0000 | 76 |
| **turnover** | -5.27e-06 | HC1 | -7.14 | 0.0000 | 4388 |
|  |  | firm_cluster | -5.29 | 0.0000 | 49 |
|  |  | time_cluster | -4.35 | 0.0000 | 82 |
|  |  | twoway_cluster | -3.81 | 0.0004 | 49 |
|  |  | newey_west | -6.23 | 0.0000 | 4388 |
|  |  | driscoll_kraay | -3.47 | 0.0009 | 76 |
| **vol_of_vol** | 7.61e-07 | HC1 | 0.34 | 0.7319 | 4388 |
|  |  | firm_cluster | 0.33 | 0.7391 | 49 |
|  |  | time_cluster | 0.18 | 0.8554 | 82 |
|  |  | twoway_cluster | 0.18 | 0.8567 | 49 |
|  |  | newey_west | 0.31 | 0.7564 | 4388 |
|  |  | driscoll_kraay | 0.23 | 0.8181 | 76 |
| **lagged_rv** | -4.62e-05 | HC1 | -10.10 | 0.0000 | 4388 |
|  |  | firm_cluster | -5.58 | 0.0000 | 49 |
|  |  | time_cluster | -6.59 | 0.0000 | 82 |
|  |  | twoway_cluster | -4.70 | 0.0000 | 49 |
|  |  | newey_west | -8.88 | 0.0000 | 4388 |
|  |  | driscoll_kraay | -5.18 | 0.0000 | 76 |
| **lagged_illiq** | -0.88 | HC1 | -5.59 | 0.0000 | 4388 |
|  |  | firm_cluster | -6.61 | 0.0000 | 49 |
|  |  | time_cluster | -3.38 | 0.0011 | 82 |
|  |  | twoway_cluster | -3.56 | 0.0008 | 49 |
|  |  | newey_west | -5.81 | 0.0000 | 4388 |
|  |  | driscoll_kraay | -2.55 | 0.0127 | 76 |
| **abn_turnover_t** | 3.53e-06 | HC1 | 5.28 | 0.0000 | 4388 |
|  |  | firm_cluster | 4.06 | 0.0002 | 49 |
|  |  | time_cluster | 3.65 | 0.0005 | 82 |
|  |  | twoway_cluster | 3.17 | 0.0026 | 49 |
|  |  | newey_west | 4.67 | 0.0000 | 4388 |
|  |  | driscoll_kraay | 3.16 | 0.0022 | 76 |
| **vix** | 1.17e-07 | HC1 | 6.01 | 0.0000 | 4388 |
|  |  | firm_cluster | 4.88 | 0.0000 | 49 |
|  |  | time_cluster | 1.88 | 0.0636 | 82 |
|  |  | twoway_cluster | 1.84 | 0.0725 | 49 |
|  |  | newey_west | 5.76 | 0.0000 | 4388 |
|  |  | driscoll_kraay | 4.55 | 0.0000 | 76 |
| **H_price** | 6.19e-06 | HC1 | 6.44 | 0.0000 | 4388 |
|  |  | firm_cluster | 6.70 | 0.0000 | 49 |
|  |  | time_cluster | 1.69 | 0.0948 | 82 |
|  |  | twoway_cluster | 1.69 | 0.0966 | 49 |
|  |  | newey_west | 6.79 | 0.0000 | 4388 |
|  |  | driscoll_kraay | 2.88 | 0.0051 | 76 |
| **H_volume** | 2.09e-06 | HC1 | 1.58 | 0.1149 | 4388 |
|  |  | firm_cluster | 1.51 | 0.1365 | 49 |
|  |  | time_cluster | 1.29 | 0.1991 | 82 |
|  |  | twoway_cluster | 1.25 | 0.2161 | 49 |
|  |  | newey_west | 1.57 | 0.1175 | 4388 |
|  |  | driscoll_kraay | 1.09 | 0.2801 | 76 |

_n = 4400, firms = 50, months = 83, R² = 0.521_

### Target: `realized_vol`

#### Focal alone + controls

| Variable | β | SE method | t | p | df |
|----------|---|-----------|---|---|-----|
| **CII** | 0.00361 | HC1 | 2.24 | 0.0249 | 4397 |
|  |  | firm_cluster | 1.11 | 0.2725 | 49 |
|  |  | time_cluster | 0.99 | 0.3263 | 82 |
|  |  | twoway_cluster | 0.78 | 0.4375 | 49 |
|  |  | newey_west | 1.51 | 0.1316 | 4397 |
|  |  | driscoll_kraay | 0.69 | 0.4906 | 85 |

_n = 4400, firms = 50, months = 83, R² = 0.024_

#### Per-benchmark regressions

| Benchmark | β | t (HC1) | t (firm) | t (twoway) | p (twoway) | R² | n |
|-----------|---|---------|----------|------------|------------|-----|---|
| roll_spread | 0.845 | 13.66 | 17.77 | 2.97 | 0.0046 | 0.099 | 4400 |
| corwin_schultz | 4.7 | 14.98 | 22.16 | 3.08 | 0.0034 | 0.112 | 4400 |
| amihud_rolling | 898 | 8.98 | 9.38 | 2.12 | 0.0390 | 0.053 | 4400 |
| turnover | 0.000227 | 0.20 | 0.23 | 0.06 | 0.9521 | 0.023 | 4400 |
| vol_of_vol | 0.113 | 9.64 | 12.78 | 2.17 | 0.0347 | 0.052 | 4400 |
| lagged_rv | 0.351 | 18.02 | 22.49 | 3.82 | 0.0004 | 0.142 | 4400 |
| lagged_illiq | 818 | 8.36 | 8.95 | 2.00 | 0.0508 | 0.047 | 4400 |
| abn_turnover_t | 0.00478 | 2.84 | 2.95 | 0.83 | 0.4079 | 0.027 | 4400 |
| vix | 0.00167 | 18.71 | 21.55 | 3.91 | 0.0003 | 0.146 | 4400 |

#### Combined specification (CII + all benchmarks + controls)


| Variable | β | SE method | t | p | df |
|----------|---|-----------|---|---|-----|
| **CII** | -0.000832 | HC1 | -0.50 | 0.6142 | 4388 |
|  |  | firm_cluster | -0.41 | 0.6854 | 49 |
|  |  | time_cluster | -0.18 | 0.8546 | 82 |
|  |  | twoway_cluster | -0.18 | 0.8596 | 49 |
|  |  | newey_west | -0.46 | 0.6440 | 4388 |
|  |  | driscoll_kraay | -0.20 | 0.8426 | 76 |
| **roll_spread** | 0.00889 | HC1 | 0.13 | 0.8937 | 4388 |
|  |  | firm_cluster | 0.16 | 0.8737 | 49 |
|  |  | time_cluster | 0.08 | 0.9356 | 82 |
|  |  | twoway_cluster | 0.09 | 0.9319 | 49 |
|  |  | newey_west | 0.14 | 0.8883 | 4388 |
|  |  | driscoll_kraay | 0.07 | 0.9415 | 76 |
| **corwin_schultz** | 1.03 | HC1 | 3.01 | 0.0026 | 4388 |
|  |  | firm_cluster | 3.30 | 0.0018 | 49 |
|  |  | time_cluster | 1.31 | 0.1944 | 82 |
|  |  | twoway_cluster | 1.33 | 0.1903 | 49 |
|  |  | newey_west | 2.95 | 0.0032 | 4388 |
|  |  | driscoll_kraay | 0.97 | 0.3343 | 76 |
| **amihud_rolling** | 3.76e+03 | HC1 | 5.97 | 0.0000 | 4388 |
|  |  | firm_cluster | 5.63 | 0.0000 | 49 |
|  |  | time_cluster | 2.57 | 0.0119 | 82 |
|  |  | twoway_cluster | 2.54 | 0.0142 | 49 |
|  |  | newey_west | 5.89 | 0.0000 | 4388 |
|  |  | driscoll_kraay | 2.27 | 0.0261 | 76 |
| **turnover** | -0.00369 | HC1 | -1.06 | 0.2904 | 4388 |
|  |  | firm_cluster | -0.85 | 0.4013 | 49 |
|  |  | time_cluster | -0.42 | 0.6777 | 82 |
|  |  | twoway_cluster | -0.40 | 0.6906 | 49 |
|  |  | newey_west | -0.97 | 0.3322 | 4388 |
|  |  | driscoll_kraay | -0.36 | 0.7193 | 76 |
| **vol_of_vol** | -0.0231 | HC1 | -1.78 | 0.0748 | 4388 |
|  |  | firm_cluster | -1.80 | 0.0779 | 49 |
|  |  | time_cluster | -0.70 | 0.4879 | 82 |
|  |  | twoway_cluster | -0.70 | 0.4885 | 49 |
|  |  | newey_west | -1.85 | 0.0638 | 4388 |
|  |  | driscoll_kraay | -1.24 | 0.2203 | 76 |
| **lagged_rv** | 0.199 | HC1 | 7.41 | 0.0000 | 4388 |
|  |  | firm_cluster | 5.36 | 0.0000 | 49 |
|  |  | time_cluster | 5.36 | 0.0000 | 82 |
|  |  | twoway_cluster | 4.41 | 0.0001 | 49 |
|  |  | newey_west | 6.90 | 0.0000 | 4388 |
|  |  | driscoll_kraay | 6.32 | 0.0000 | 76 |
| **lagged_illiq** | -3.87e+03 | HC1 | -6.11 | 0.0000 | 4388 |
|  |  | firm_cluster | -5.56 | 0.0000 | 49 |
|  |  | time_cluster | -2.65 | 0.0097 | 82 |
|  |  | twoway_cluster | -2.60 | 0.0123 | 49 |
|  |  | newey_west | -6.08 | 0.0000 | 4388 |
|  |  | driscoll_kraay | -2.48 | 0.0155 | 76 |
| **abn_turnover_t** | 0.00274 | HC1 | 0.83 | 0.4073 | 4388 |
|  |  | firm_cluster | 0.64 | 0.5265 | 49 |
|  |  | time_cluster | 0.37 | 0.7146 | 82 |
|  |  | twoway_cluster | 0.34 | 0.7318 | 49 |
|  |  | newey_west | 0.75 | 0.4548 | 4388 |
|  |  | driscoll_kraay | 0.30 | 0.7624 | 76 |
| **vix** | 0.000933 | HC1 | 9.06 | 0.0000 | 4388 |
|  |  | firm_cluster | 9.03 | 0.0000 | 49 |
|  |  | time_cluster | 2.11 | 0.0382 | 82 |
|  |  | twoway_cluster | 2.11 | 0.0403 | 49 |
|  |  | newey_west | 9.89 | 0.0000 | 4388 |
|  |  | driscoll_kraay | 3.50 | 0.0008 | 76 |
| **H_price** | 0.0106 | HC1 | 1.96 | 0.0505 | 4388 |
|  |  | firm_cluster | 2.23 | 0.0303 | 49 |
|  |  | time_cluster | 0.39 | 0.6970 | 82 |
|  |  | twoway_cluster | 0.39 | 0.6964 | 49 |
|  |  | newey_west | 2.17 | 0.0302 | 4388 |
|  |  | driscoll_kraay | 0.73 | 0.4683 | 76 |
| **H_volume** | 0.0127 | HC1 | 1.63 | 0.1022 | 4388 |
|  |  | firm_cluster | 1.30 | 0.2002 | 49 |
|  |  | time_cluster | 0.98 | 0.3291 | 82 |
|  |  | twoway_cluster | 0.89 | 0.3764 | 49 |
|  |  | newey_west | 1.50 | 0.1348 | 4388 |
|  |  | driscoll_kraay | 0.75 | 0.4547 | 76 |

_n = 4400, firms = 50, months = 83, R² = 0.184_

## Publication-grade inference for CII (combined specification)

These are the referee-demanded small-sample corrections for the CII coefficient under the combined specification (CII + 9 benchmarks + Hurst controls). Reported per Imbens-Kolesár (2016) for CR2 + Satterthwaite df, and Cameron-Gelbach-Miller (2008) / MacKinnon-Webb (2017) for the wild cluster restricted bootstrap.

| Target | β | CR2 t | CR2 p | Satterthwaite df | WCR p (999 draws) |
|--------|---|-------|-------|-------------------|-------------------|
| `amihud_illiq` | -2.23e-07 | -0.70 | 0.5067 | 6.3 | 0.5170 |
| `realized_vol` | -0.000832 | -0.40 | 0.7033 | 5.9 | 0.7030 |

_CR2 uses firm-level clusters with Bell-McCaffrey adjustment. WCR uses Rademacher weights and restricted-null residuals. The CR2 Satterthwaite df is typically much smaller than G_firm − 1 under unbalanced clusters; interpret the CR2 p-value as the binding small-sample-corrected inference._

## Interpretation notes

1. **Primary question**: compare the CII t-statistic (twoway-clustered) between the focal-only specification and the combined specification. Material degradation indicates CII's predictive content is subsumed by one or more benchmarks.

2. **Hardest competitor**: `lagged_illiq` (the target's own past value for the Amihud target). If CII survives alongside lagged_illiq in the combined spec, the orthogonal-information claim stands.

3. **Inference layers** reported here: HC1 (reference only), firm-clustered, time-clustered, two-way clustered with CGM eigenvalue PSD adjustment, Newey-West (flagged for DK replacement), Driscoll-Kraay on daily periods with Bartlett bandwidth ≥21, CR2 + Satterthwaite df at the firm dimension, and WCR bootstrap with Rademacher weights under the restricted null. The CR2 and WCR results are the binding publication-grade inferences; the five SE methods above them are descriptive.
