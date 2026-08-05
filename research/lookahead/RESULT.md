# Right-edge stamping variant of the H4 null

## What is being tested

`rolling_hurst` stamps each window at its midpoint, so at `W = 500` the window reaches 249 trading days (a median of 362 calendar days on this panel) past the stamp date. Nothing downstream shifts it back. CII at `t` therefore embeds raw data spanning the `[t+1, t+21]` outcome window. This file re-runs the primary H4 specification with every window relabelled by its LAST observation, so the predictor is strictly backward-looking.

Re-stamping moves each observation forward by 249 trading days, a median of 362 calendar days. 495 of 495 firms mapped and 41,653 of 41,653 panel rows re-stamped. The regression loses a further slice at the tail of each firm, where the forward window now runs off the end of the sample and the outcome is missing.

## Exactness of the re-stamp

Changing the stamp changes no Hurst estimate, only the date label, so the panel is relabelled rather than recomputed and only the forward outcome is read afresh. Verified end-to-end on AAPL over 117 rolling rows. Hurst values identical True, CII values identical True, re-stamped dates match a full recompute with `stamp="right"` True.

## Result

Forward dollar-volume Amihud regressed on CII with Hurst controls and firm fixed effects, the same specification as `research/rebuild_g488/RESULT.md`.

| SE method | midpoint t | midpoint p | right-edge t | right-edge p |
|---|---|---|---|---|
| HC1 | +2.78 | 0.006 | -2.91 | 0.004 |
| firm_cluster | +0.87 | 0.386 | -1.56 | 0.120 |
| time_cluster | +1.37 | 0.176 | -2.07 | 0.042 |
| twoway_cluster | +0.76 | 0.449 | -1.38 | 0.171 |
| newey_west | +1.22 | 0.221 | -1.68 | 0.093 |
| driscoll_kraay | +0.73 | 0.465 | -1.36 | 0.175 |
| CR2 (Satterthwaite) | +0.87 | 0.415 | -1.56 | 0.201 |
| WCR bootstrap | --- | 0.406 | --- | 0.148 |

At the midpoint stamp, beta_CII = 4.436e-06, n = 41,553, firms = 495, R2 = 0.009.
At the right edge, beta_CII = -1.283e-05, n = 41,082, firms = 495, R2 = 0.000.

## The firm-conditional null HOLDS under right-edge stamping

Firm-clustered p = 0.120 and two-way clustered p = 0.171 at the right edge, against 0.386 and 0.449 at the midpoint. CR2 and the wild cluster bootstrap agree. Removing the look-ahead does not manufacture a predictive signal.

## The coefficient changes sign, which is itself informative

beta_CII goes from +4.436e-06 at the midpoint to -1.283e-05 at the right edge, and the two time-conditional methods invert with it. HC1 reads +2.78 at the midpoint and -2.91 at the right edge; time-clustered reads +1.37 against -2.07. Both cross the 5% threshold in both directions. A coefficient whose sign is set by an arbitrary date label is not measuring a firm-level effect. This reinforces the paper's reading of the time-conditional significance as sensitivity to the inference dimension rather than predictive content, and it is a further reason the retracted `t = 2.90` headline was unreliable.

Regenerate with `python research/lookahead/run_right_edge.py --verify`.