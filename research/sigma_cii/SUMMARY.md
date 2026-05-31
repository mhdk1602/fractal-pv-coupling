# sigma(CII) make-or-break: results

Universe: 51 firms, 87 rolling-Hurst dates (W=500, step=20, CII window=30).
sigma(CII) range [0.254, 0.459], mean 0.367.

## Verdict: **NOISE**

No stable contemporaneous (|r|>0.3) or leading relationship survives. Fall back to the structured precise null; do not headline sigma(CII).

## Contemporaneous correlation (sigma vs stress; mean-CII vs stress for contrast)

| stress | sigma Pearson | p | sigma Spearman | p | mean-CII Pearson | n |
|---|---|---|---|---|---|---|
| vix | -0.140 | 0.196 | -0.132 | 0.223 | +0.466 | 87 |
| log_vix | -0.153 | 0.157 | -0.132 | 0.223 | +0.539 | 87 |
| spy_rv | -0.093 | 0.390 | -0.013 | 0.903 | +0.311 | 87 |
| hyg_rv | -0.178 | 0.099 | -0.095 | 0.381 | +0.336 | 87 |
| ps_illiq | -0.007 | 0.951 | +0.109 | 0.316 | +0.052 | 87 |

## Lead-lag (lag>0 => sigma LEADS stress)

| stress | peak lag | peak r | peak p | lag0 r | best +lag | +lag r | +lag p |
|---|---|---|---|---|---|---|---|
| vix | 6 | -0.325 | 0.003 | -0.140 | 6 | -0.325 | 0.003 |
| log_vix | -6 | -0.333 | 0.002 | -0.153 | 6 | -0.319 | 0.004 |
| spy_rv | 6 | -0.275 | 0.013 | -0.093 | 6 | -0.275 | 0.013 |
| hyg_rv | 6 | -0.382 | 0.000 | -0.178 | 6 | -0.382 | 0.000 |
| ps_illiq | -5 | +0.104 | 0.354 | -0.007 | 6 | -0.055 | 0.625 |

## Predictive regressions: stress_{t+h} ~ sigma_t + stress_t (Newey-West)

| stress | h | beta_sigma | t_sigma | p_sigma | R2 | n |
|---|---|---|---|---|---|---|
| vix | 1 | -14.8855 | -1.07 | 0.283 | 0.261 | 86 |
| vix | 3 | -29.7789 | -1.18 | 0.236 | 0.131 | 84 |
| vix | 6 | -48.3678 | -1.68 | 0.093 | 0.125 | 81 |
| log_vix | 1 | -0.4402 | -0.91 | 0.364 | 0.423 | 86 |
| log_vix | 3 | -0.9559 | -0.99 | 0.321 | 0.193 | 84 |
| log_vix | 6 | -1.7634 | -1.55 | 0.120 | 0.147 | 81 |
| spy_rv | 1 | -0.1111 | -0.66 | 0.512 | 0.275 | 86 |
| spy_rv | 3 | -0.3350 | -0.99 | 0.323 | 0.041 | 84 |
| spy_rv | 6 | -0.5470 | -1.66 | 0.096 | 0.076 | 81 |
| hyg_rv | 1 | -0.0980 | -1.31 | 0.192 | 0.470 | 86 |
| hyg_rv | 3 | -0.2926 | -1.51 | 0.130 | 0.119 | 84 |
| hyg_rv | 6 | -0.4322 | -2.20 | 0.028 | 0.147 | 81 |
| ps_illiq | 1 | -0.0280 | -0.24 | 0.811 | 0.001 | 86 |
| ps_illiq | 3 | -0.0181 | -0.18 | 0.857 | 0.001 | 84 |
| ps_illiq | 6 | -0.0628 | -0.71 | 0.476 | 0.003 | 81 |

## Granger (first differences, min p over lags 1-4)

| stress | sigma->stress min p (lag) | stress->sigma min p (lag) |
|---|---|---|
| vix | 0.754 (2) | 0.857 (1) |
| log_vix | 0.489 (2) | 0.742 (1) |
| spy_rv | 0.669 (1) | 0.768 (1) |
| hyg_rv | 0.738 (4) | 0.393 (1) |
| ps_illiq | 0.378 (1) | 0.117 (3) |