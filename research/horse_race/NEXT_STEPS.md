# Next Steps — Post Horse Race + Memo Integration

**Status as of**: 2026-04-28
**Branch**: `master` (horse-race merged at `7ca0392`; v1.1.0 released)
**Latest revision driver**: `research_revision_memo.md` (2026-04-28)

This plan supersedes the prior version. It absorbs the manuscript-level
findings from the revision memo and reorders the remaining work into two
explicit lanes: **Tier A** (executable without further decisions) and
**Tier B** (needs your judgement before I touch the manuscript). Each item
is labelled accordingly.

---

## Part 1 — What is now done

- [x] **Merge `horse-race` into `master`.** Merge commit `7ca0392` on master, pushed to `github.com/mhdk1602/fractal-pv-coupling`.
- [x] **SSRN preprint revised.** Author dashboard updated 2026-04-27. SSRN did not request a change-log note this round.
- [x] **GitHub release v1.1.0.** https://github.com/mhdk1602/fractal-pv-coupling/releases/tag/v1.1.0
- [x] **Zenodo v1.1.0 DOI minted.** Initial release failed because the repo was private; deleted and recreated after making the repo public, which re-fired the webhook. New version DOI: **10.5281/zenodo.19835451**. Concept DOI 10.5281/zenodo.19611543 now resolves to v1.1.0.
- [x] **ORCID linked.** Zenodo concept DOI confirmed under ORCID 0009-0003-1036-9477.
- [x] **Local workspace sync.** Master pulled into `/Users/haridines/github/personal/Matlab---fractal-modelling/` from terminal with FDA.

The operational chain (merge → SSRN → GitHub → Zenodo → ORCID) is closed.
Remaining work is on the manuscript itself and on submission strategy.

---

## Part 2 — Manuscript harmonization (memo response)

The memo identifies a set of internal-consistency issues that the v1.1.0
revision did not fully address. They are real and verifiable in the
compiled PDF: I checked each claim against `main.pdf` before listing it
here. Some are cosmetic; a few materially change how a referee reads the
paper.

### 2.1 Tier A — execute without further input

| Item | Verified | Action |
|------|----------|--------|
| Footer reads "Preprint submitted to Elsevier" | ✓ p1 of PDF | Uncomment `\journal{Quantitative Finance}` so the footer reads "Preprint submitted to Quantitative Finance" |
| ORCID renders as "URL: 0009-0003-1036-9477" | ✓ p1 of PDF | Replace `\ead[orcid]{...}` with a proper ORCID footnote linking to `https://orcid.org/...` |
| Body text reads "Appendix Appendix B" | ✓ in body, line 501 | Remove the manual "Appendix" prefix where `\ref{app:replication}` and `\ref{app:tickers}` are used; elsarticle already prepends "Appendix" |
| Abstract/intro/methods/conclusion call two-way clustering "the most conservative inference" | ✓ in PDF text | Rewrite to acknowledge CR2/WCR as the stricter small-sample tests; integrate horse-race headline into abstract |
| Methods §3.5 lists only HC1 / firm / time / two-way / Newey-West | ✓ lines 148–149 | Add brief subsection naming CR2/Satterthwaite and WCR; reference Table 7 |

I will execute this lane immediately. None of these change the
substantive claims; they make the paper internally consistent with what
Table 7 already shows.

### 2.2 Tier B — needs your decision before I touch it

These are substantive and could shift numbers or framing. I want your
explicit go-ahead on each before I edit.

#### 2.2.1 Illiquidity definition (mathematical mismatch)

The dependent variable in §3.6 is defined with **share volume** in the
denominator. The horse-race benchmark in §5.4 uses **dollar volume**
($V \times P$). These are not the same Amihud, and a referee will fairly
ask which dependent variable the paper is actually forecasting.

Two clean fixes:

- **Option α (rename)**: relabel the dependent variable as a
  share-volume-scaled illiquidity proxy and reserve "Amihud" for the
  benchmark. No re-computation. Two-paragraph definitional fix.

- **Option β (re-compute)**: change the dependent variable to standard
  dollar-volume Amihud and rerun the predictive panel. Affects Tables
  1–7 and most numbers in §5.3 and §5.4. Probably 1–2 days of compute
  and rewrite. Higher chance of stronger headline because dollar Amihud
  is less noisy than share-volume Amihud.

My recommendation: **Option β**, because the paper is now anchored on
illiquidity as the primary outcome and using the standard convention
removes a free attack point. But it is your call.

#### 2.2.2 Table 6 split

Current Table 6 is hard to read because the per-benchmark rows show
the **benchmark** $t$-statistic, not the CII $t$-statistic. A reader
cannot see whether CII actually survives in each per-benchmark
specification. The memo's fix:

- **Panel A**: CII coefficient and $t$ across {focal-only,
  per-benchmark (one row per benchmark), combined}. The reader sees
  CII survival on every line.
- **Panel B**: benchmark coefficients in the combined model (what
  Table 6 currently shows).

This requires re-running `horse_race_regression` and capturing the CII
coefficient row from each per-benchmark fit. Maybe a half-day of work.
I'd recommend doing it.

#### 2.2.3 Outcome hierarchy + multiple-testing

The paper scans four outcomes (illiquidity, realised vol, abnormal
turnover, max drawdown) and several specifications. There is currently
no explicit family-wise correction or pre-registered hierarchy. Two
strategies, not mutually exclusive:

- **Hierarchy framing**: state in §3.6 (and abstract) that Amihud
  illiquidity is the **primary** H4 outcome and the other three are
  exploratory. Cheap; pure prose.
- **Romano–Wolf step-down** in an appendix: more defensible than
  Bonferroni, but adds compute and code.

Recommendation: do the hierarchy framing now (Tier A-able if you
greenlight) and add the Romano–Wolf table as appendix material if you
do Phase 2 anyway.

#### 2.2.4 Economic significance section

The paper is statistically defended but currently has no compact
section translating the CII coefficient into practitioner units. The
memo's framing — and I agree — is that the natural application is
**liquidity surveillance / execution-risk forecasting**, not return
prediction. So:

- Standardise: report effect of one-SD change in CII on next-month
  Amihud in basis points or dollar units.
- Decile sort: average forward Amihud in highest vs lowest CII decile;
  show the gap.
- Optional: a brief example of the signal aggregated cross-sectionally
  as a market-wide liquidity stress index.

Adds one short subsection (≈1 page + 1 figure or table) to §5 or §6.

#### 2.2.5 Methods section expansion

§3.5 currently describes only the original five SE methods. The
manuscript now uses:

- CGM (2011) PSD-adjusted two-way clustering (the existing two-way
  estimator was upgraded — needs a sentence)
- Bell–McCaffrey CR2 with Satterthwaite df at the firm dimension
- Wild cluster restricted bootstrap with Rademacher weights
- Driscoll–Kraay (computed in code; not currently surfaced in the
  manuscript)

Add §3.5.1 (baseline CRVE), §3.5.2 (small-sample corrections), §3.5.3
(horse-race design). About a page of methods prose, no new analysis.

#### 2.2.6 Hurst-estimator robustness visibility

The robustness table already includes R/S and MFDFA at $q=2$. The memo
suggests promoting estimator robustness more visibly because the
paper now anchors on CII as a research object. A clean addition would
be a small panel re-running the H4 illiquidity regression with H from
DFA, R/S, and a wavelet-based estimator. Two-day compute.

### 2.3 Tier C — Phase 2 universe expansion

This is the highest-ROI single change, but it is a separate research
sprint, not a revision pass. Detailed in Part 5.

---

## Part 3 — Endorsement, arXiv, and SSRN distribution

### 3.1 De Sena endorsement window

LinkedIn message sent 2026-04-22. Decision rule unchanged from prior
plan:

- **Reply by 2026-05-06**: proceed with arXiv upload immediately.
- **No reply by 2026-05-06**: contact backup endorser candidate #1
  with a tightened pitch citing SSRN preprint and the Zenodo v1.1.0
  DOI.
- **No endorsement by 2026-05-20**: ship SSRN-only. SSRN is the
  primary venue for finance work; arXiv is secondary.

### 3.2 arXiv submission package (when endorsed)

- [ ] Build tarball with `main.tex`, `references.bib`, `figures/*.pdf`,
      `elsarticle.cls`
- [ ] Write 200-word arXiv abstract (separate from paper abstract)
- [ ] Cite Zenodo v1.1.0 DOI in comments field
- [ ] Primary category `q-fin.ST`; cross-list `stat.ME`
- [ ] License `CC BY-NC-ND` to match SSRN

---

## Part 4 — Quantitative Finance submission

### 4.1 Decision: Option A (submit now) vs Option B (Phase 2 first)

The memo and my own assessment both put this fork explicitly. The
honest version:

- **Option A**: clean up Part 2 Tier A items + Tier B items 2.2.3
  (hierarchy) and 2.2.4 (economic significance), then submit. Time to
  submission: 1–2 weeks. Most likely outcome: major revision asking
  for sample expansion and economic significance development.

- **Option B**: do Tier B in full plus Phase 2 universe expansion to
  ~500 firms, then submit. Time to submission: 4–8 weeks. Most likely
  outcome: minor revision or accept with light comments because the
  most attackable parts (G=50, marginal CR2, missing economic
  significance) are pre-empted.

I recommend **Option B** if you can afford 4–8 weeks. Reasons:

1. The CR2 marginal $p$-value is the single biggest threat. Universe
   expansion is the only intervention that mechanically raises the
   Satterthwaite df.
2. Economic significance and mechanism are easier to write once the
   broader-sample numbers are in front of you.
3. The methodology contribution is real either way; the empirical
   evidence is what determines which tier of journal accepts.

If you choose Option A, I'll execute Tier A + the cheap Tier B items
and you submit at the end of next week.

### 4.2 Submission mechanics (when ready)

- Portal: https://mc.manuscriptcentral.com/tandf/qf
- Manuscript PDF (`main.pdf`)
- Cover letter (`research/submission/cover_letter_quantfinance.md`,
  converted to PDF)
- Optional: replication-script summary, CHECKPOINT excerpt
- `\journal{Quantitative Finance}` already set after Part 2.1

### 4.3 Anticipated referee response template

Already drafted at the head of `research/submission/`. Refresh after
Part 2 is done with the actual revision-pass language.

---

## Part 5 — Phase 2: Universe expansion

Working title for the follow-on / revision: *Fractal Price–Volume
Coupling and Forward Illiquidity in the S&P 500*.

### 5.1 Scope

- Universe: full S&P 500 over 2015–2026, point-in-time membership to
  avoid forward selection. Approximately 500 firms × ~2,800 daily
  observations = O(1.4M) firm-day observations.
- Re-run the full pipeline: rolling H, CII, forward metrics, panel
  regressions, horse race, Tier 3 inference.
- Compare CR2 Satterthwaite df at G=500 vs the current G=50. Expected:
  df rises substantially, CR2 $p$-value moves below 5%.

### 5.2 Compute and storage

- Yahoo Finance has rate limits at 500-ticker scale; use parallel
  fetches with backoff or move to a paid feed (Polygon $200/mo would
  cover this and Phase 3).
- Rolling DFA at $W=500$, $\Delta=20$ across 500 names will take ~6h
  on this machine; budget overnight runs.
- Store intermediate parquet under `data/raw/sp500_full/` and
  `data/processed/sp500_full/`.

### 5.3 New robustness checks unlocked at G=500

- Industry-cluster CR2 (cluster on GICS sector with G=11 — small but
  enough for a separate column).
- Sub-sample stability: 250-firm splits, pre/post-COVID splits.
- Survivorship-bias test: include defunct/de-indexed names with
  truncated panels.

### 5.4 Other extensions deferred to a separate paper

- Russell 2000 small caps
- Sector ETFs / international indices / crypto
- Intraday frequencies

These are correctly scoped as Paper 2 and Paper 3, not part of this
revision.

---

## Part 6 — Decision register

| Key | Decision | Status |
|-----|----------|--------|
| D1 | Next coding step | Resolved: Tier 3 + Table 6 complete |
| D2 | Backup endorser if De Sena declines | Open; decide by 2026-05-06 |
| D3 | When to merge `horse-race` to `master` | Resolved: merged 2026-04-26 |
| D4 | XSPREAD_0 placement | Resolved: online appendix only |
| D5 | Commercial/practitioner engagement post-arXiv | Open; default decline until journal acceptance |
| D6 | Treat horse race as revision or separate paper | Resolved: revision of v1 |
| D7 | SSRN version note wording | Resolved: SSRN did not request a note |
| D8 | Journal if QF desk-rejects | Physica A → JEF → FRL (priority order) |
| **D9** | **Submit now (Option A) or Phase 2 first (Option B)** | **OPEN — needs your call** |
| **D10** | **Illiquidity definition: rename (α) or recompute with dollar volume (β)** | **OPEN — needs your call; my recommendation β** |
| **D11** | **Multiple-testing: hierarchy framing only, or hierarchy + Romano–Wolf appendix** | **OPEN — recommend hierarchy now, RW only with Phase 2** |

---

## Part 7 — Risk register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| De Sena declines / silence | Medium | Low | Backup endorsers; SSRN is primary anyway |
| QF desk-rejects | Low–Medium | Medium | Fallback journals ordered; cover letter handles fit explicitly |
| Referee demands intraday replication | Medium | Medium | Defer to Phase 3, cite GHT 2009 daily-data precedent |
| Referee fixates on CR2 marginal $p=0.066$ | High | Medium | Phase 2 (option B) mechanically raises Satterthwaite df; otherwise emphasise WCR per MacKinnon-Webb 2017 |
| Referee fixates on illiquidity definition mismatch | Medium | Low–Medium | Resolve via D10 before submission; both options close this |
| Phase 2 weakens or reverses headline at G=500 | Low | High | Run early on a 100-firm pilot; if headline collapses, the Tier 3 work is still publishable as a methods note |

---

## Part 8 — Concrete next-72-hours plan

If you greenlight everything Tier-A-able:

1. **Today (2026-04-28)**: Tier A manuscript fixes (front matter,
   ORCID, appendix typo, inference language harmonization, methods
   subsection adds). Recompile, push. No new release tag yet.
2. **2026-04-29**: D10 decision (illiquidity definition). If β,
   re-run prediction panel and rebuild Tables 1–7 from new numbers.
3. **2026-04-30**: Outcome-hierarchy framing + economic-significance
   subsection draft.
4. **2026-05-01**: Recompile, push, optional v1.1.1 release if you
   want the cleanup minted on Zenodo.

If you choose Option B, freeze the manuscript here, kick off Phase 2
data fetch in parallel, and reconvene on the new numbers around
2026-05-12.

---

## Key identifiers (current)

- Concept DOI: `10.5281/zenodo.19611543` (resolves to latest)
- v1.0.0 version DOI: `10.5281/zenodo.19611544`
- v1.1.0 version DOI: `10.5281/zenodo.19835451`
- ORCID: `0009-0003-1036-9477`
- Public repo: `github.com/mhdk1602/fractal-pv-coupling`
- Streamlit dashboard: `fractal-pv.streamlit.app`
- SSRN submission: 2026-04-16; revised 2026-04-27
- Master HEAD: `7ca0392` (horse-race merge)
- v1.1.0 release id: 314311304 (recreated after public-repo flip)
