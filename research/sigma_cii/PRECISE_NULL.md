# The H4 null is precise, not underpowered (G=51)

Panel: 4437 firm-months, 51 firms, forward horizon h=21 days. Specification: forward Amihud illiquidity ~ CII + H(|r|) + H(volume), firm fixed effects, two-way (firm x month) clustered SEs (Cameron-Gelbach-Miller 2011).

## 1. The share-volume vs dollar-volume confound, reproduced

| forward target | beta_CII | HC1 t | two-way t | two-way p |
|---|---|---|---|---|
| share-volume Amihud (confounded proxy) | 0.4691 | 10.65 | 3.21 | 0.002 |
| dollar-volume Amihud (Amihud 2002, correct) | 0.0000 | 1.69 | 0.46 | 0.646 |

The share-volume proxy can look significant under naive SEs; the price-impact-correct dollar-volume measure does not survive two-way clustering. This is the diagnostic behind the retraction of the earlier 't = 2.90' headline.

## 2. The dollar-volume null, stated precisely

- beta_CII = 0.0000, two-way clustered t = 0.46 (p = 0.646, df = 50).
- Bell-McCaffrey CR2: t = 0.57, p = 0.579, Satterthwaite df = 10.40.
- Wild-cluster restricted bootstrap (firm clusters, 999 reps): p = 0.579.
- Standardized effect: +0.018 target-SD per CII-SD, 95% CI [-0.062, +0.099].
- **The CI excludes any |effect| larger than 0.10 SD.** This is a precise null: the data rule out an economically meaningful firm-conditional predictive effect, not merely fail to detect one.

## 3. Robust to measurement-error attenuation

CII, H(|r|) and H(volume) are generated regressors estimated with error, which biases the OLS slope toward zero. Disattenuating the standardized effect and its CI by a reliability ratio kappa (regression-calibration, single-regressor approximation beta_true = beta_obs / kappa):

| kappa (reliability) | disattenuated std beta | disattenuated 95% CI |
|---|---|---|
| 0.9 | +0.021 | [-0.068, +0.110] |
| 0.7 | +0.026 | [-0.088, +0.141] |
| 0.5 | +0.037 | [-0.123, +0.197] |

Even under a generous kappa = 0.5 (half the regressor variance is noise), the disattenuated CI still excludes effects larger than ~0.20 SD. The null is not an artifact of attenuation; correcting for it does not surface a meaningful effect.

## Bottom line

The firm-conditional predictive content of CII for forward illiquidity is a precise, attenuation-robust null on the 51-firm universe, consistent with the G=488 Phase-2 result (two-way t = -0.93). The flagship's honest claim is the descriptive temporal coupling plus this bounded null; the paper should report the standardized CI and the attenuation check so a referee reads 'precisely zero,' not 'underpowered.' The G=488 panel reruns this exact specification for the headline figure.