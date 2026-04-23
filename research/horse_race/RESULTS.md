# Horse Race Results: CII vs Standard Liquidity Benchmarks

Generated: 2026-04-23 16:50

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
| **CII** | 0.481 | HC1 | 10.02 | 0.0000 | 4397 |
|  |  | firm_cluster | 3.51 | 0.0010 | 49 |
|  |  | time_cluster | 4.95 | 0.0000 | 82 |
|  |  | twoway_cluster | 2.99 | 0.0043 | 49 |
|  |  | newey_west | 5.41 | 0.0000 | 4397 |

_n = 4400, firms = 50, months = 83, R² = 0.026_

#### Per-benchmark regressions

| Benchmark | β | t (HC1) | t (firm) | t (twoway) | p (twoway) | R² | n |
|-----------|---|---------|----------|------------|------------|-----|---|
| roll_spread | 13.2 | 3.98 | 4.01 | 3.05 | 0.0037 | 0.026 | 4400 |
| corwin_schultz | 90.5 | 7.35 | 4.66 | 3.40 | 0.0013 | 0.039 | 4400 |
| amihud_rolling | 3.4e+04 | 4.46 | 3.78 | 2.70 | 0.0096 | 0.048 | 4400 |
| turnover | -0.234 | -3.94 | -3.29 | -2.63 | 0.0115 | 0.017 | 4400 |
| vol_of_vol | 1.47 | 3.48 | 3.60 | 1.74 | 0.0876 | 0.014 | 4400 |
| lagged_rv | 5.72 | 5.75 | 3.92 | 3.18 | 0.0026 | 0.038 | 4400 |
| lagged_illiq | 3.24e+04 | 4.29 | 3.68 | 2.58 | 0.0131 | 0.044 | 4400 |
| abn_turnover_t | -0.144 | -2.46 | -3.26 | -1.49 | 0.1425 | 0.013 | 4400 |
| vix | 0.0391 | 7.48 | 4.95 | 4.53 | 0.0000 | 0.070 | 4400 |

#### Combined specification (CII + all benchmarks + controls)


| Variable | β | SE method | t | p | df |
|----------|---|-----------|---|---|-----|
| **CII** | 0.335 | HC1 | 6.49 | 0.0000 | 4388 |
|  |  | firm_cluster | 2.46 | 0.0174 | 49 |
|  |  | time_cluster | 3.87 | 0.0002 | 82 |
|  |  | twoway_cluster | 2.19 | 0.0331 | 49 |
|  |  | newey_west | 3.78 | 0.0002 | 4388 |
| **roll_spread** | -5.05 | HC1 | -1.88 | 0.0597 | 4388 |
|  |  | firm_cluster | -2.27 | 0.0277 | 49 |
|  |  | time_cluster | -1.71 | 0.0909 | 82 |
|  |  | twoway_cluster | -1.99 | 0.0517 | 49 |
|  |  | newey_west | -1.95 | 0.0511 | 4388 |
| **corwin_schultz** | 21.6 | HC1 | 1.24 | 0.2145 | 4388 |
|  |  | firm_cluster | 1.87 | 0.0673 | 49 |
|  |  | time_cluster | 1.31 | 0.1922 | 82 |
|  |  | twoway_cluster | 2.15 | 0.0363 | 49 |
|  |  | newey_west | 1.64 | 0.1004 | 4388 |
| **amihud_rolling** | 9.7e+04 | HC1 | 2.89 | 0.0039 | 4388 |
|  |  | firm_cluster | 4.14 | 0.0001 | 49 |
|  |  | time_cluster | 2.54 | 0.0130 | 82 |
|  |  | twoway_cluster | 3.15 | 0.0028 | 49 |
|  |  | newey_west | 2.65 | 0.0080 | 4388 |
| **turnover** | -0.26 | HC1 | -1.48 | 0.1398 | 4388 |
|  |  | firm_cluster | -0.91 | 0.3647 | 49 |
|  |  | time_cluster | -1.32 | 0.1903 | 82 |
|  |  | twoway_cluster | -0.87 | 0.3869 | 49 |
|  |  | newey_west | -1.14 | 0.2532 | 4388 |
| **vol_of_vol** | -1.49 | HC1 | -4.06 | 0.0001 | 4388 |
|  |  | firm_cluster | -2.81 | 0.0070 | 49 |
|  |  | time_cluster | -2.68 | 0.0089 | 82 |
|  |  | twoway_cluster | -2.21 | 0.0320 | 49 |
|  |  | newey_west | -3.51 | 0.0004 | 4388 |
| **lagged_rv** | 0.383 | HC1 | 0.45 | 0.6494 | 4388 |
|  |  | firm_cluster | 0.35 | 0.7300 | 49 |
|  |  | time_cluster | 0.34 | 0.7319 | 82 |
|  |  | twoway_cluster | 0.29 | 0.7722 | 49 |
|  |  | newey_west | 0.37 | 0.7079 | 4388 |
| **lagged_illiq** | -7.46e+04 | HC1 | -2.29 | 0.0218 | 4388 |
|  |  | firm_cluster | -3.52 | 0.0010 | 49 |
|  |  | time_cluster | -2.12 | 0.0371 | 82 |
|  |  | twoway_cluster | -2.82 | 0.0070 | 49 |
|  |  | newey_west | -2.42 | 0.0155 | 4388 |
| **abn_turnover_t** | -0.0371 | HC1 | -0.22 | 0.8262 | 4388 |
|  |  | firm_cluster | -0.16 | 0.8723 | 49 |
|  |  | time_cluster | -0.22 | 0.8232 | 82 |
|  |  | twoway_cluster | -0.16 | 0.8711 | 49 |
|  |  | newey_west | -0.19 | 0.8474 | 4388 |
| **vix** | 0.0334 | HC1 | 7.10 | 0.0000 | 4388 |
|  |  | firm_cluster | 4.39 | 0.0001 | 49 |
|  |  | time_cluster | 4.44 | 0.0000 | 82 |
|  |  | twoway_cluster | 3.49 | 0.0010 | 49 |
|  |  | newey_west | 7.79 | 0.0000 | 4388 |
| **H_price** | 0.399 | HC1 | 2.00 | 0.0452 | 4388 |
|  |  | firm_cluster | 1.49 | 0.1432 | 49 |
|  |  | time_cluster | 0.85 | 0.3959 | 82 |
|  |  | twoway_cluster | 0.80 | 0.4303 | 49 |
|  |  | newey_west | 1.93 | 0.0536 | 4388 |
| **H_volume** | -1.25 | HC1 | -5.04 | 0.0000 | 4388 |
|  |  | firm_cluster | -2.29 | 0.0266 | 49 |
|  |  | time_cluster | -4.33 | 0.0000 | 82 |
|  |  | twoway_cluster | -2.21 | 0.0321 | 49 |
|  |  | newey_west | -3.16 | 0.0016 | 4388 |

_n = 4400, firms = 50, months = 83, R² = 0.109_

### Target: `realized_vol`

#### Focal alone + controls

| Variable | β | SE method | t | p | df |
|----------|---|-----------|---|---|-----|
| **CII** | 0.00361 | HC1 | 2.24 | 0.0249 | 4397 |
|  |  | firm_cluster | 1.11 | 0.2725 | 49 |
|  |  | time_cluster | 0.99 | 0.3263 | 82 |
|  |  | twoway_cluster | 0.78 | 0.4375 | 49 |
|  |  | newey_west | 1.51 | 0.1316 | 4397 |

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
| **roll_spread** | 0.00889 | HC1 | 0.13 | 0.8937 | 4388 |
|  |  | firm_cluster | 0.16 | 0.8737 | 49 |
|  |  | time_cluster | 0.08 | 0.9356 | 82 |
|  |  | twoway_cluster | 0.09 | 0.9319 | 49 |
|  |  | newey_west | 0.14 | 0.8883 | 4388 |
| **corwin_schultz** | 1.03 | HC1 | 3.01 | 0.0026 | 4388 |
|  |  | firm_cluster | 3.30 | 0.0018 | 49 |
|  |  | time_cluster | 1.31 | 0.1944 | 82 |
|  |  | twoway_cluster | 1.33 | 0.1903 | 49 |
|  |  | newey_west | 2.95 | 0.0032 | 4388 |
| **amihud_rolling** | 3.76e+03 | HC1 | 5.97 | 0.0000 | 4388 |
|  |  | firm_cluster | 5.63 | 0.0000 | 49 |
|  |  | time_cluster | 2.57 | 0.0119 | 82 |
|  |  | twoway_cluster | 2.54 | 0.0142 | 49 |
|  |  | newey_west | 5.89 | 0.0000 | 4388 |
| **turnover** | -0.00369 | HC1 | -1.06 | 0.2904 | 4388 |
|  |  | firm_cluster | -0.85 | 0.4013 | 49 |
|  |  | time_cluster | -0.42 | 0.6777 | 82 |
|  |  | twoway_cluster | -0.40 | 0.6906 | 49 |
|  |  | newey_west | -0.97 | 0.3322 | 4388 |
| **vol_of_vol** | -0.0231 | HC1 | -1.78 | 0.0748 | 4388 |
|  |  | firm_cluster | -1.80 | 0.0779 | 49 |
|  |  | time_cluster | -0.70 | 0.4879 | 82 |
|  |  | twoway_cluster | -0.70 | 0.4885 | 49 |
|  |  | newey_west | -1.85 | 0.0638 | 4388 |
| **lagged_rv** | 0.199 | HC1 | 7.41 | 0.0000 | 4388 |
|  |  | firm_cluster | 5.36 | 0.0000 | 49 |
|  |  | time_cluster | 5.36 | 0.0000 | 82 |
|  |  | twoway_cluster | 4.41 | 0.0001 | 49 |
|  |  | newey_west | 6.90 | 0.0000 | 4388 |
| **lagged_illiq** | -3.87e+03 | HC1 | -6.11 | 0.0000 | 4388 |
|  |  | firm_cluster | -5.56 | 0.0000 | 49 |
|  |  | time_cluster | -2.65 | 0.0097 | 82 |
|  |  | twoway_cluster | -2.60 | 0.0123 | 49 |
|  |  | newey_west | -6.08 | 0.0000 | 4388 |
| **abn_turnover_t** | 0.00274 | HC1 | 0.83 | 0.4073 | 4388 |
|  |  | firm_cluster | 0.64 | 0.5265 | 49 |
|  |  | time_cluster | 0.37 | 0.7146 | 82 |
|  |  | twoway_cluster | 0.34 | 0.7318 | 49 |
|  |  | newey_west | 0.75 | 0.4548 | 4388 |
| **vix** | 0.000933 | HC1 | 9.06 | 0.0000 | 4388 |
|  |  | firm_cluster | 9.03 | 0.0000 | 49 |
|  |  | time_cluster | 2.11 | 0.0382 | 82 |
|  |  | twoway_cluster | 2.11 | 0.0403 | 49 |
|  |  | newey_west | 9.89 | 0.0000 | 4388 |
| **H_price** | 0.0106 | HC1 | 1.96 | 0.0505 | 4388 |
|  |  | firm_cluster | 2.23 | 0.0303 | 49 |
|  |  | time_cluster | 0.39 | 0.6970 | 82 |
|  |  | twoway_cluster | 0.39 | 0.6964 | 49 |
|  |  | newey_west | 2.17 | 0.0302 | 4388 |
| **H_volume** | 0.0127 | HC1 | 1.63 | 0.1022 | 4388 |
|  |  | firm_cluster | 1.30 | 0.2002 | 49 |
|  |  | time_cluster | 0.98 | 0.3291 | 82 |
|  |  | twoway_cluster | 0.89 | 0.3764 | 49 |
|  |  | newey_west | 1.50 | 0.1348 | 4388 |

_n = 4400, firms = 50, months = 83, R² = 0.184_

## Interpretation notes

1. **Primary question**: compare the CII t-statistic (twoway-clustered) between the focal-only specification and the combined specification. Material degradation indicates CII's predictive content is subsumed by one or more benchmarks.

2. **Hardest competitor**: `lagged_illiq` (the target's own past value for the Amihud target). If CII survives alongside lagged_illiq in the combined spec, the orthogonal-information claim stands.

3. **Tier 3 caveats**: Two-way SEs currently zero-floor negative diagonals with a warning; CGM (2011) §2.3 eigen-adjustment pending. At G_firm = 50 the t(G−1) reference distribution is optimistic; Bell-McCaffrey CR2 with Satterthwaite df and WCR bootstrap are planned upgrades before submission.
