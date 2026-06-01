# G=488 re-baseline on refreshed data (Path 2)

Window 2015-01-01 to 2026-04-15. Panel firms: 495; full-Hurst firms: 501. All tables from one fresh snapshot.

## Hurst summary (full sample)
- H(returns): 0.468 ± 0.033
- H(|returns|): 0.793 ± 0.068
- H(volume): 0.878 ± 0.076

## H1 static: cross-sectional Pearson r(H|r|, Hvol) = +0.179 (p=0.000), Spearman +0.164 (p=0.000), n=501

## H2 temporal: mean r=0.530, median=0.615, 93% positive (86% positive & significant), n=498

## H3 regime (the n=495 fix: per-regime firm counts, all <= panel size)

| regime | mean | median | std | n firms |
|---|---|---|---|---|
| low | 0.549 | 0.622 | 0.301 | 477 |
| medium | 0.500 | 0.563 | 0.315 | 496 |
| high | 0.562 | 0.729 | 0.440 | 493 |

Mann-Whitney high>low: U=138624, p=0.0000

## H4 predictive: forward dollar-volume Amihud ~ CII + H controls (firm FE)

beta_CII = 0.0000; n=41553, firms=495, R2=0.009
| SE method | t | p |
|---|---|---|
| HC1 | +2.78 | 0.006 |
| firm_cluster | +0.87 | 0.386 |
| time_cluster | +1.37 | 0.176 |
| twoway_cluster | +0.76 | 0.449 |
| newey_west | +1.22 | 0.221 |
| driscoll_kraay | +0.73 | 0.465 |
| CR2 (Satterthwaite df=6.98) | +0.87 | 0.415 |
| WCR bootstrap | --- | 0.406 |

Every value above regenerates from `research/rebuild_g488/rebuild.py` on current data. No frozen-panel dependency.