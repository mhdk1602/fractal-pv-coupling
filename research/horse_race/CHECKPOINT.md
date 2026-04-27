# Checkpoint: Horse Race Extension

**Date**: 2026-04-23
**Branch**: `horse-race`
**Latest commit**: `ad7e75a` — Horse race v1: CII retains orthogonal predictive content for illiquidity

---

## Status summary

One-sentence read: v1 manuscript is submitted to SSRN and awaiting arXiv endorsement; the horse-race extension on the `horse-race` branch has produced headline results that strengthen H4 and are ready to slot into a revision as Table 6.

---

## What is complete

### Main manuscript (v1, on `master`)

- [x] Submission-ready LaTeX with 46 references, 9 figures, 5 tables
- [x] Two appendices: 50-ticker sample with GICS sectors; replication guide
- [x] Independent-researcher affiliation
- [x] Zero banned AI vocabulary; em-dashes reduced to 2 (both in thesis sentence)
- [x] Zenodo DOI `10.5281/zenodo.19611544`, concept + version-specific
- [x] ORCID `0009-0003-1036-9477` registered and attached
- [x] SSRN uploaded 2026-04-16 under CC BY-NC-ND
- [x] GitHub release `v1.0.0` on `fractal-pv-coupling`
- [x] Public dashboard repo `fractal-pv-dashboard` live, Streamlit app deployable
- [x] `replicate.py` master script; README documents data provenance and execution order

### Horse-race extension (on `horse-race` branch)

- [x] `src/fractal_pv/benchmarks.py` — five estimators with full citations:
  - Roll (1984) proportional effective spread, zero-flooring convention
  - Corwin-Schultz (2012) MSPREAD_0 with overnight adjustment; XSPREAD_0 robustness variant
  - Amihud (2002) illiquidity with dollar volume and 10⁶ scaling
  - Normalized turnover (spike indicator)
  - Volatility of volatility
- [x] Two referee audits incorporated; all corrections documented in commit messages
- [x] `inference_robust.py` Tier 1 + Tier 2 fixes:
  - `get_indexer` pad semantics (fixed silent look-ahead)
  - HC1 weighted-X form (O(nk) memory)
  - Correct df for all 5 SE methods per Cameron-Miller (2015)
  - Nested-FE convention (k_effective excludes absorbed FE)
  - `horse_race_regression` accepts arbitrary regressor lists
  - `horse_race_summary_table` convenience output
  - Warnings for non-PSD two-way sandwich and `G ≤ 1` edge cases
- [x] `run_horse_race.py` runner with pickle caching under `cache/`
- [x] Horse race v1 executed over the full 50-ticker panel
- [x] `RESULTS.md` with three-class specifications per target

### Headline horse-race findings

| Target: Amihud illiquidity | CII β | t (two-way) | p |
|---|---|---|---|
| CII alone + Hurst controls | 0.481 | 2.99 | 0.0043 |
| CII combined with 9 benchmarks + controls | 0.335 | 2.19 | 0.033 |

CII retains significance at the 5% level when conditioned on lagged Amihud, VIX, Corwin-Schultz, Roll, turnover, vol-of-vol, lagged RV, abnormal turnover, and Hurst levels. Orthogonal-information claim stands.

For realized volatility, CII runs at t = -0.18 in the combined spec. The paper's existing H4 null is reinforced.

---

## What is pending before journal submission

### Tier 3 inference upgrades (must-have; ~2-3 weeks)

These are publication-grade corrections flagged by the second referee audit. At G_firm = 50 the t(G − 1) reference distribution is optimistic; the audit's "what the referee will actually ask for" section names these as non-negotiable.

- [ ] **Wild Cluster Restricted (WCR) bootstrap** p-values for clustered SEs.
      Cameron-Gelbach-Miller (2008, REStat); MacKinnon-Webb (2017, JAE).
      Python port: `wildboottestpy` or R `fwildclusterboot` via `rpy2`.
      Estimated effort: 1-2 weeks.
- [ ] **Bell-McCaffrey CR2 + Satterthwaite df**.
      Imbens-Kolesár (2016, REStat); `dfadjust` / `clubSandwich` logic.
      At unbalanced G_firm ≈ 50, Satterthwaite df typically falls in [10, 30].
      Estimated effort: 3-5 days.
- [ ] **CGM (2011) §2.3 eigenvalue adjustment** for non-PSD two-way sandwich.
      Currently zero-floors negative diagonals with a warning.
      Estimated effort: 1 day.
- [ ] **Driscoll-Kraay SEs** on the daily panel, Bartlett bandwidth 21-42.
      Driscoll-Kraay (1998, REStat); Hoechle (2007, Stata J).
      Replaces pooled Newey-West per audit.
      Estimated effort: 2-3 days.

### Manuscript integration (v1 revision)

- [ ] Draft new **Table 6** with horse-race results: focal-only vs combined, two-way clustered SEs, ΔR² and Δt across specifications
- [ ] Add ~200 words to Section H4 explaining the horse race and its interpretation
- [ ] Update Discussion Section ("Relation to Existing Methods") to cite horse-race result
- [ ] Add benchmark citations to `references.bib` (Roll 1984, Corwin-Schultz 2012, GHT 2009, FHT 2017, Hasbrouck 2009, Abdi-Ranaldo 2017, Cameron-Miller 2015, Imbens-Kolesár 2016, MacKinnon-Nielsen-Webb 2023, Driscoll-Kraay 1998)
- [ ] Update Appendix B (Replication Guide) to mention the horse-race module

### Publication logistics

- [ ] **Cover letter for Quantitative Finance** (T&F Manuscript Central format)
- [ ] **arXiv submission package** (tar.gz with main.tex, bib, figures, elsarticle.cls)
- [ ] **Backup endorser list** (3 candidates; approach sequentially at 7-day intervals if De Sena declines)

---

## Awaiting external action

- [ ] SSRN indexing (submitted 2026-04-16; typically 5-10 business days; at day 7 and counting)
- [ ] De Sena's response to LinkedIn message (sent 2026-04-22; no reply yet)
- [ ] Link Zenodo DOI to ORCID profile (manual step via orcid.org → Works → Add → Search & Link → Zenodo)

---

## Decisions pending

**D1 — Next coding step.** Three candidates, ordered by referee-impact:
  - (a) Tier 3: WCR bootstrap + CR2 + CGM eigen + DK. The binding publication requirements.
  - (b) Manuscript integration: draft Table 6 and the accompanying Section H4 text using v1 SE methods. Upgrade SEs in a second pass.
  - (c) Horse-race v2: add XSPREAD_0 robustness; sensitivity sweep across rolling window (21-day vs 63-day spreads).

  **My recommendation**: (b) first, then (a). The Table 6 draft is cheap to write now and clarifies exactly which numbers will be upgraded under Tier 3. The upgrades then slot into the table in a single revision pass.

**D2 — If De Sena declines or doesn't respond by 2026-05-06 (two weeks).**
  - Approach backup endorser #1. Candidate pool to be identified from:
    - Recent arXiv q-fin.ST authors with tangential overlap
    - Cited authors still active (Kristoufek, Podobnik, Abdi, Hasbrouck — long shots but worth one attempt)
    - Academics in the fractal-finance community (Barunik, Kwapień, Drożdż)

**D3 — When to merge `horse-race` branch to `master`.**
  - Recommendation: after Tier 3 upgrades are complete and integrated into the manuscript. Keep `master` at submission-ready state until then.

**D4 — XSPREAD_0 robustness table placement.**
  - Recommendation: online appendix, not main text. Table 6 uses MSPREAD_0 only (authors' primary). XSPREAD_0 goes in a supplementary table for referees who ask.

**D5 — Response to potential practitioner interest post-arXiv.**
  - Keep the academic track clean. Decline practitioner collaborations until journal acceptance. Revisit after v1 is accepted.

---

## Risks and contingencies

| Risk | Probability | Mitigation |
|------|-------------|------------|
| De Sena declines endorsement | Medium | Backup endorser list; arXiv is not the only preprint route (SSRN already live) |
| SSRN takes >2 weeks to index | Low-Medium | Escalate to SSRN editor; verify submission status |
| Tier 3 WCR bootstrap reveals CII doesn't survive with small-sample correction | Low | Pivot claim: CII predicts changes in illiquidity; or extend horizon |
| Quantitative Finance desk-rejects | Medium | Fallback: Physica A (econophysics-friendly), Journal of Empirical Finance, Finance Research Letters |
| Horse-race sample is too narrow (50 S&P 500) | Low for v1 | Already acknowledged in Limitations; Phase 2 expansion is planned |
| Referee demands intraday replication | Medium | Defer to second paper; cite data constraints honestly |

---

## Repository map (current state)

```
fractal-pv-coupling/            (private)
├── master                      Submission-ready v1 manuscript
│   └── research/paper/main.{tex,pdf}
│   └── research/lineage/hari_2013_msc_fractal_modelling_kcl.pdf
│   └── research/RESEARCH_PLAN.md
│   └── research/notes/IP_PROTECTION.md
│   └── src/fractal_pv/          (10 modules)
│   └── replicate.py
│
└── horse-race                  This work-in-progress branch
    ├── src/fractal_pv/benchmarks.py       (NEW, ~460 lines)
    ├── src/fractal_pv/inference_robust.py (MAJOR REFACTOR)
    ├── src/fractal_pv/predict.py          (HC1 fix)
    └── research/horse_race/
        ├── run_horse_race.py              (NEW, runner)
        ├── RESULTS.md                     (NEW, v1 output)
        └── CHECKPOINT.md                  (this file)

fractal-pv-dashboard/            (public, MIT)
└── Enhanced Streamlit app with 7 tabs
```

---

## Key identifiers for cross-reference

- Zenodo DOI: `10.5281/zenodo.19611544`
- ORCID: `0009-0003-1036-9477`
- Private repo: `github.com/mhdk1602/fractal-pv-coupling`
- Public repo: `github.com/mhdk1602/fractal-pv-dashboard`
- Streamlit app: `fractal-pv.streamlit.app`
- SSRN submission: 2026-04-16 (awaiting index)
- MSc lineage: `research/lineage/hari_2013_msc_fractal_modelling_kcl.pdf`
