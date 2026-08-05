# sigma(CII) make-or-break: results

Universe: 495 firms, 87 rolling-Hurst dates (W=500, step=20, CII window=30). Pinned by `research/sigma_cii/universe_full.txt`, exact firms recorded in `universe_manifest_full.json`.
sigma(CII) range [0.322, 0.464], mean 0.413.

## Verdict: **NOISE**

No stable contemporaneous (|r|>0.3) or leading relationship survives. Fall back to the structured precise null; do not headline sigma(CII).

## Contemporaneous correlation (sigma vs stress; mean-CII vs stress for contrast)

| stress | sigma Pearson | p | sigma Spearman | p | mean-CII Pearson | n |
|---|---|---|---|---|---|---|
| vix | +0.109 | 0.314 | +0.038 | 0.730 | +0.490 | 87 |
| log_vix | +0.137 | 0.207 | +0.038 | 0.730 | +0.566 | 87 |
| spy_rv | +0.126 | 0.244 | +0.206 | 0.055 | +0.325 | 87 |
| hyg_rv | +0.120 | 0.268 | +0.255 | 0.017 | +0.313 | 87 |

## Lead-lag (lag>0 => sigma LEADS stress)

| stress | peak lag | peak r | peak p | lag0 r | best +lag | +lag r | +lag p |
|---|---|---|---|---|---|---|---|
| vix | 6 | -0.201 | 0.071 | +0.109 | 6 | -0.201 | 0.071 |
| log_vix | -6 | -0.184 | 0.100 | +0.137 | 1 | +0.123 | 0.259 |
| spy_rv | 6 | -0.155 | 0.168 | +0.126 | 6 | -0.155 | 0.168 |
| hyg_rv | 6 | -0.160 | 0.154 | +0.120 | 6 | -0.160 | 0.154 |

## Predictive regressions: stress_{t+h} ~ sigma_t + stress_t (Newey-West)

| stress | h | beta_sigma | t_sigma | p_sigma | R2 | n |
|---|---|---|---|---|---|---|
| vix | 1 | +4.7571 | +0.31 | 0.754 | 0.252 | 86 |
| vix | 3 | -8.7221 | -0.28 | 0.782 | 0.096 | 84 |
| vix | 6 | -48.8421 | -1.21 | 0.227 | 0.082 | 81 |
| log_vix | 1 | +0.2790 | +0.47 | 0.641 | 0.418 | 86 |
| log_vix | 3 | +0.0629 | +0.05 | 0.958 | 0.168 | 84 |
| log_vix | 6 | -1.3172 | -0.90 | 0.368 | 0.089 | 81 |
| spy_rv | 1 | +0.1365 | +0.64 | 0.521 | 0.275 | 86 |
| spy_rv | 3 | +0.0341 | +0.08 | 0.938 | 0.012 | 84 |
| spy_rv | 6 | -0.4304 | -0.79 | 0.432 | 0.025 | 81 |
| hyg_rv | 1 | +0.0348 | +0.33 | 0.743 | 0.463 | 86 |
| hyg_rv | 3 | -0.0097 | -0.04 | 0.968 | 0.049 | 84 |
| hyg_rv | 6 | -0.2560 | -0.75 | 0.452 | 0.028 | 81 |

## Granger (first differences, min p over lags 1-4)

| stress | sigma->stress min p (lag) | stress->sigma min p (lag) |
|---|---|---|
| vix | 0.689 (2) | 0.926 (2) |
| log_vix | 0.586 (2) | 0.872 (1) |
| spy_rv | 0.572 (1) | 0.791 (3) |
| hyg_rv | 0.631 (2) | 0.625 (1) |