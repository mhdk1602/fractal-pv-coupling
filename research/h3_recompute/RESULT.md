# H3 VIX-regime recompute (G=488) — fixing the n=495 bug

Universe loaded: 501 firms (window 2015-01-01 to 2026-04-15).

| regime | published mean/med/std | recomputed mean/med/std | recomputed n | match |
|---|---|---|---|---|
| low | 0.567/0.666/0.344 | 0.549/0.622/0.301 | 477 | NO |
| medium | 0.497/0.566/0.299 | 0.500/0.563/0.315 | 496 | YES |
| high | 0.563/0.738/0.45 | 0.562/0.729/0.440 | 493 | YES |

Mann-Whitney high>low: recomputed U=138624, p=0.0000 (published U=135542, p=0.0019).

**NOT a faithful match** (data snapshot differs from the frozen run). Do NOT overwrite the published mean/median/std. The recomputed n is indicative only; the author should recompute n on the frozen panel. Divergence per regime: low=DIFF, medium=ok, high=ok.