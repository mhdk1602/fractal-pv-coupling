# Journal Readiness Plan — v1.4.0

**Goal**: bring the manuscript to a confident-submission state targeting *Quantitative Finance* as primary, with explicit fallback ladder. Target threshold: 80% of the work that distinguishes "submittable" from "competitive at QF tier."

**Constraints**
- Submission gated on PhD completion (~2027). Pre-PhD activity is timestamping (SSRN + arXiv) and iterative manuscript improvement.
- No AI-attribution in commits or files.
- Writing style: precise, varied paragraph length, no AI-generic filler vocabulary (delve, leverage, foster, robust [non-technical], synergy, holistic, etc.), em-dashes ≤ 1 per page, first-person active voice where appropriate, qualified hedging where honest.
- Cite resources accurately. Every empirical claim, every number, every benchmark estimator gets its primary citation.

**Tier ladder (post-pivot, honest)**

| Rank | Venue | IF | Plausible outcome |
|---|---|---|---|
| 1 | *Quantitative Finance* (T&F) | ~1.7 | major revision → ~50-60% accept after revise |
| 2 | *Chaos, Solitons & Fractals* (Elsevier) | ~7.8 | minor revision plausible if framed methodologically |
| 3 | *Journal of Empirical Finance* (Elsevier) | ~2.0 | major revision; microstructure-leaning fit |
| 4 | *Physica A: Statistical Mechanics and its Applications* (Elsevier) | ~3.3 | minor revision likely; safest landing |
| 5 | *Finance Research Letters* (Elsevier) | short format | letter-style; fastest path |

A-tier finance (JoF, RFS, JFE) is structurally not on the table; this paper does not match those journals' selection criteria regardless of polishing.

---

## Definition of 80% journal-ready

The 80% threshold is met when:

1. The manuscript is internally consistent: every number cross-references correctly across abstract, intro, results, discussion, conclusion, and tables.
2. Every table has real numbers, no placeholder text.
3. Every figure references the panel it actually depicts.
4. The Sample appendix and Replication guide reflect the actual Phase 2 G=488 universe.
5. The pre-registration discipline is visible in the methodology section.
6. The paper carries one additional empirical exhibit beyond the v1.3.0 baseline that grounds the time-conditional finding (aggregate-CII evidence).
7. A Hurst-estimator robustness check defends the construction against the obvious "DFA-only" critique.
8. The mechanism section connects the descriptive coupling to one or more standard theoretical channels (MDH, information arrival, adverse selection) at the right level of restraint.
9. Multiple-testing handling is explicit, not implicit.
10. Bibliography is complete, every benchmark has its primary citation, no missing entries, no stale DOIs.

The remaining 20% (external review, professional copyedit, journal-specific formatting, final pre-submission audit) happens close to actual submission post-PhD.

---

## Execution plan

### Phase A — Critical fixes (mandatory for any submission)

**A1. Fill Table 6 horse-race placeholders with real G=488 per-benchmark numbers.**
- Action: extend `run_phase2.py` (or write a sibling script) to run the nine per-benchmark regressions for Amihud illiquidity and realized volatility at G=488; cache results.
- Output: replace the placeholder table rows in `main.tex` with actual β, t-stats (twoway, DK), and R² per benchmark, matching the v1.2.0 table structure.
- Cite: \citet{roll1984spread}, \citet{corwin2012simple}, \citet{amihud2002illiquidity}, \citet{goyenko2009liquidity}, \citet{hasbrouck2009trading}, \citet{abdi2017simple}.

**A2. Re-run the Robustness section at G=488 or relabel.**
- Action: decide between (a) re-running the original robustness suite (window sensitivity W ∈ {252, 500, 756}, non-overlapping windows, first-differenced Hurst, surrogate test, squared-returns alternative, subperiod analysis, sector decomposition, market-factor partial correlation, DFA polynomial order, R/S vs DFA, Granger causality) at G=488; or (b) keeping the G=50 numbers with explicit "v1.0 50-firm sample" labeling and adding a brief Phase 2 verification block.
- Recommendation: option (b) for surrogate, sector, subperiod (already strong); option (a) for window sensitivity and Hurst-estimator robustness (which will be redone for A3 anyway).

**A3. Hurst-estimator robustness panel.**
- Action: rerun the H4 primary regression with H estimated by R/S analysis \citep{lo1991long}, DFA-1 (already done), and a wavelet-based estimator. Compare CII coefficients and t-stats across the three estimators.
- Output: small panel table in §6 robustness or as an appendix exhibit.
- Defends against the "your result depends on DFA" critique.

**A4. Update Sample Composition appendix.**
- Action: replace the 50-firm hardcoded list with a sector-distribution table for G=488 plus a reference to `data/sp500_constituents_2026-04-28.csv` for the full constituency.
- Recompile Appendix A.

**A5. Update Replication Guide appendix.**
- Action: replace v1.0 pipeline references with `run_phase2.py` + `PHASE2_PROTOCOL.md` + `respec_battery.py` and v1.4.0-specific instructions.
- Recompile Appendix B.

**A6. Surface pre-registration discipline in the methodology section.**
- Action: add a brief subsection in §3 (Methodology) or §4 (Data) explicitly noting that Phase 2 was run under a pre-registered protocol (`PHASE2_PROTOCOL.md`) frozen at master HEAD `f8aa564` before any G > 50 fetch, with per-target decision rules committed in advance.
- Pre-registration is uncommon in econophysics; surfacing it is a credibility signal.

**A7. Numerical cross-check sweep.**
- Action: every numerical claim in abstract / intro / results / discussion / conclusion must cross-reference correctly to a table or to `PHASE2_RESULTS.md`. Sweep for v1.0/v1.2 numerical artifacts that may have leaked into v1.3.0 prose.
- Method: grep for specific numbers (0.665, 0.531, 2.90, 0.33, etc.) and verify each occurrence is consistent with its source.

### Phase B — Strong-to-have (lifts paper from "submittable" to "competitive at QF")

**B1. Aggregate-CII exhibit.**
- Action: compute the cross-sectional mean of CII at each rolling-Hurst date across all 488 firms, $\overline{\text{CII}}_t = (1/G) \sum_i \text{CII}^{(i)}_t$. Plot against VIX over the 2015-2026 window. Compute correlation with VIX, and with one or two additional stress indicators (e.g., NY Fed CFSI if accessible, or a constructed stress proxy from VIX + BAA-Treasury spread).
- Output: one figure + one paragraph in §6 (Discussion) under a new subsection "Cross-Sectional Aggregation: A Time-Period Stress Indicator."
- Cite: \citet{adrian2017fed} or similar for stress indicators if used.
- Critical framing: this is the empirical handle that makes the time-conditional finding tangible. Without it, the firm-vs-time inference disagreement is abstract.

**B2. Mechanism subsection expansion.**
- Action: write half a page to a page connecting the descriptive coupling phenomenon to standard theoretical channels at the appropriate restraint level: MDH \citep{clark1973subordinated, andersen1996return}, sequential information-arrival \citep{copeland1976model}, Kyle-style adverse selection \citep{kyle1985continuous}, and inventory-based microstructure \citep{brunnermeier2009market}. Be explicit that the paper documents the phenomenon and rules in/out specific channels via the inference-disagreement pattern, but does not claim structural identification.
- Output: rewrite §6.4 "Consistency with the MDH on the Descriptive Side Only" into a fuller §6.4 "Theoretical Channels and What the Inference Disagreement Implies."

**B3. Multiple-testing footnote.**
- Action: add an explicit paragraph in §5.4 that addresses the multiple-testing concern. The horse-race absorption pattern *is* the multiple-testing handling for the family of nine targets: every focal-only signal collapses to null in the combined specification, regardless of which individual target is tested. State this directly. Add Bonferroni-adjusted p-values for the four primary outcomes (Amihud, RV, drawdown, abnormal turnover) as a robustness check footnote.
- Output: one paragraph + one short table or in-line note.

### Phase C — Polish

**C1. CITATION.cff at repo root.**
- Action: add a Citation File Format file alongside `.zenodo.json`. Reuses the same author/title metadata. Standard format per the [CFF spec](https://citation-file-format.github.io/).

**C2. arXiv-ready 200-word abstract.**
- Action: separate condensed abstract for arXiv submission (when De Sena endorses), distinct from the paper abstract.
- Output: `research/submission/arxiv_abstract.md`.

**C3. Bibliography sweep.**
- Action: verify every benchmark estimator citation appears, every \citet in the manuscript resolves, every \citep page-number convention is consistent. Add any missing entries (e.g., \citet{copeland1976model} for sequential-information mechanism if added).
- Use bibtex log to find unresolved cites.

**C4. End-to-end re-read.**
- Action: read the manuscript front-to-back as a referee would. Flag any awkward transitions, inconsistent terminology, em-dash count > 1 per page, repeated banned vocabulary.
- Output: notes file with specific line-level comments to address.

---

## Step-by-step execution sequence

This is the concrete order. Each step ends with a self-contained deliverable so that we can pause cleanly between user turns.

| # | Step | Deliverable | User check-in |
|---|---|---|---|
| 1 | Run per-benchmark horse-race regressions at G=488 (A1 prep) | New script + cache file with per-benchmark β/t-stats | After cache produced |
| 2 | Update Table 6 in main.tex with real numbers (A1) | Recompiled PDF, Table 6 verified | After recompile |
| 3 | Sample appendix update (A4) | Updated Appendix A | Bundled with step 4 |
| 4 | Replication guide update (A5) | Updated Appendix B | After step 4 |
| 5 | Pre-registration disclosure (A6) | New subsection in §3 or §4 | After step 5 |
| 6 | Robustness section update / relabel (A2) | Updated §6 | After step 6 |
| 7 | Hurst-estimator robustness panel (A3) | New panel + analysis | After step 7 |
| 8 | Numerical cross-check sweep (A7) | Verified consistency | Inline |
| 9 | Aggregate-CII exhibit (B1) | New figure + new subsection | After step 9 |
| 10 | Mechanism subsection expansion (B2) | Rewritten §6.4 | After step 10 |
| 11 | Multiple-testing footnote (B3) | Added paragraph + small table | After step 11 |
| 12 | CITATION.cff + arXiv abstract (C1, C2) | Two new files | Bundled |
| 13 | Bibliography sweep (C3) | references.bib clean | Inline |
| 14 | End-to-end re-read (C4) | Final pass; commit v1.4.0; tag; mint Zenodo | Final user check-in |

After step 14: 80% threshold met. The remaining 20% (external review, copyedit, journal-specific formatting, pre-submission audit) is post-PhD.

---

## Resources I will cite

Beyond what's already in `references.bib` v1.3.0:

- \citet{adrian2017fed} or alternative for stress-index reference if B1 uses one
- \citet{copeland1976model} for sequential information arrival, B2
- \citet{lo1991long} for R/S Hurst estimator, A3
- A wavelet-Hurst reference (Abry & Veitch 1998 or Veitch & Abry 1999), A3
- Bonferroni \citep{bonferroni1936teoria} for multiple-testing footnote, B3

---

## What is explicitly not in scope for v1.4.0

- Paper 2 (aggregate CII as a market-wide stress indicator) as a full standalone paper. Only the in-paper exhibit (B1) lands here. Paper 2 is a separate post-PhD effort.
- Phase 3 intraday extension. Deferred.
- Cross-asset (ETFs, futures, crypto). Deferred.
- Romano-Wolf step-down. Bonferroni footnote suffices for v1.4.0; Romano-Wolf becomes appendix material if a referee asks.
- WRDS / CRSP point-in-time membership correction. Survivorship bias remains disclosed-in-limitations.

---

## Master HEAD checkpoint

This plan was written against master HEAD `b92f6e2` (v1.3.0). The pipeline freeze under `PHASE2_PROTOCOL.md` continues to apply: any code change that affects estimated coefficients or inference will be flagged in the v1.4.0 commit message with explicit before/after comparison.
