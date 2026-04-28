# Next Steps — v1.2.0 Pivot to Honest-Null Framing

**Status as of**: 2026-04-28
**Branch**: `master`
**Active version**: **v1.2.0** (in progress — manuscript rewritten, awaiting commit + tag)
**Submission gate**: post-PhD (University of the Cumberlands, defense ~2027). Pre-PhD activity is timestamping only on SSRN + arXiv.

---

## What v1.2.0 changes from v1.1.0

The headline empirical claim of v1.0/v1.1 (CII predicts Amihud illiquidity) was driven by a price-level component of a non-standard share-volume Amihud denominator. Once the standard dollar-volume Amihud convention is applied, CII has no incremental predictive content for any of ten standard market-quality outcomes under inference robust to two-way clustering, Bell--McCaffrey CR2, and the wild cluster restricted bootstrap. The v1.2.0 manuscript:

- Retitles to *"Temporal Fractal Coupling of Volatility and Trading Volume: A Robust Pattern Without Forecast Power in S&P 500 Stocks, 2015–2026"*.
- Keeps H1 (rejected), H2 (confirmed), H3 (confirmed) unchanged. These remain the paper's robust descriptive contribution.
- Rewrites H4 as a clean null. New Tables 6–10: focal-only across six SE methods, ten-target battery, horse race, small-sample-corrected inference, side-by-side share-vs-dollar-volume diagnostic.
- Adds a new diagnostic subsection (`sec:h4_diagnosis`) decomposing $\widetilde{\mathrm{ILLIQ}} = \mathrm{ILLIQ} \cdot P$ and explaining the price-level confound.
- Pivots Discussion §6 to "pattern without predictive content" and adds a methodological-lesson subsection.
- Rewrites the Conclusion and the *Quantitative Finance* cover letter to match.

Numerically: CII focal-only on dollar-volume Amihud has $\hat\beta = 4.0\times10^{-7}$, two-way clustered $t = 0.33$, $p = 0.745$. CR2 $p = 0.507$. WCR $p = 0.517$. The full battery is in `cache/respec_results.pkl` and reproduced in Table~\ref{tab:battery} of the manuscript.

---

## Part 1 — Done

- [x] D10 (β): predict.py uses dollar-volume Amihud; pipeline rerun and verified
- [x] Respecification battery (10 targets) — all null under dependence-robust SEs
- [x] Manuscript rewrite end-to-end (abstract, intro, methods §3.6, results §5.4, discussion §6, conclusion)
- [x] Cover letter rewrite for the new framing
- [x] D11: hierarchy framing in §3.6 (Amihud primary, others exploratory). Romano-Wolf appendix omitted because all targets are null and FW corrections would only widen $p$ values.
- [x] Force-pushed master after stripping the Co-Authored-By: Claude trailer from commit 708537a → f3e8365. v1.1.0 tag and Zenodo v1.1.0 DOI unaffected.

---

## Part 2 — Imminent

- [ ] Commit v1.2.0 manuscript + cover letter + plan refresh, **without any AI-attribution trailer or footer** (Dinesh's standing instruction; force-rewrite if accidentally included).
- [ ] Tag v1.2.0 on GitHub. Zenodo will mint a new version DOI within 15 minutes.
- [ ] Update SSRN preprint with v1.2.0 PDF. Brief change log: "Corrects the v1.1.0 H4 result by switching to the standard dollar-volume Amihud convention. Adds a methodological diagnostic of the share-volume vs. dollar-volume divergence. H1, H2, and H3 unchanged."
- [ ] Update the project memory at `~/.claude/projects/-Users-haridines-github-BCG/memory/fractal-research.md` with the new headline.

---

## Part 3 — Phase 2 universe expansion (G ≈ 500)

The most natural follow-up. Phase 2 is now **a confirmation/extension exercise rather than a rescue attempt**: it tests whether the predictive null persists at full S&P 500 scale (likely yes) or whether a clean signal emerges with more data (possibly, e.g. on the forward Corwin-Schultz spread, which got close at $G = 50$).

### 3.1 Scope

- Universe: full S&P 500 over 2015–2026, point-in-time membership to avoid forward selection. Approximately 500 firms × 2,800 daily observations = O(1.4M) firm-day observations.
- Re-run the full pipeline: rolling H, CII, forward metrics (dollar-volume Amihud), panel regressions, horse race, Tier 3 inference.
- Particular attention: forward Corwin-Schultz spread, which had focal HC1 $t = 4.04$ and firm-cluster $t = 2.32$ at $G = 50$ but two-way clustering kills it at $t = 1.39$. At $G = 500$ the cluster-heterogeneity penalty drops sharply; this is the most plausible recovery candidate.

### 3.2 Compute and storage

- Yahoo Finance has rate limits at 500-ticker scale; use parallel fetches with backoff or move to a paid feed (Polygon $200/mo would also cover Phase 3).
- Rolling DFA at $W = 500$, $\Delta = 20$ across 500 names will take ~6h on a typical workstation; budget overnight runs.
- Store intermediate parquet under `data/raw/sp500_full/` and `data/processed/sp500_full/`.

### 3.3 New robustness checks unlocked at G = 500

- Industry-cluster CR2 (cluster on GICS sector with G = 11 — small but enough for a separate column).
- Sub-sample stability: 250-firm splits, pre/post-COVID splits.
- Survivorship-bias test: include defunct/de-indexed names with truncated panels.

### 3.4 Decision rule for Phase 2

- **If predictive null persists at $G = 500$**: paper stays as v1.2.0 in essence; add the G=500 panel as a confirmation study; ship to Quantitative Finance post-PhD. The negative result is now well-powered.
- **If a clean signal recovers** (most likely on Corwin-Schultz spread or vol-of-vol): the paper recovers a positive predictive claim; restructure §5.4 to lead with the recovery; reposition the v1.2.0 ten-target battery as a small-sample limitation.
- **If the temporal coupling itself weakens at G = 500** (least likely, would be surprising): rethink whether the H2/H3 pattern is a large-cap artifact.

---

## Part 4 — Submission strategy

Both gated on PhD completion (~2027). No journal submission before then.

### 4.1 Pre-PhD: timestamping only

- SSRN: continue revising; v1.2.0 to be uploaded.
- arXiv: pending De Sena endorsement (LinkedIn message 2026-04-22). If endorsed by 2026-05-06, upload v1.2.0. Otherwise pursue a backup endorser; if nothing by 2026-05-20, ship SSRN-only.
- Zenodo: each tagged release auto-mints a version DOI; concept DOI 10.5281/zenodo.19611543 always resolves to the latest.

### 4.2 Post-PhD: journal target

- Primary: *Quantitative Finance* (Taylor & Francis). Cover letter already drafted; resubmit/refresh closer to defense.
- Fallback order: *Physica A* → *Journal of Empirical Finance* → *Finance Research Letters*.
- *Physica A* is now the most natural fit given the descriptive-pattern-plus-methodological-caveat framing of v1.2.0; promote to primary if QF reads as too finance-heavy at submission time.

---

## Part 5 — Decision register

| Key | Decision | Status |
|-----|----------|--------|
| D1 | Next coding step | Resolved: Tier 3 + Table 6 + Phase 2 plan |
| D2 | Backup endorser if De Sena declines | Open; decide by 2026-05-06 |
| D3 | Merge `horse-race` to `master` | Resolved: 2026-04-26 (`7ca0392`) |
| D4 | XSPREAD_0 placement | Resolved: online appendix only |
| D5 | Commercial/practitioner engagement | Open; default decline until journal acceptance |
| D6 | Treat horse race as revision or separate paper | Resolved: revision of v1, now folded into v1.2.0 |
| D7 | SSRN version note wording | Open: v1.2.0 change log drafted in Part 2 above |
| D8 | Journal if QF rejects | Resolved: Physica A → JEF → FRL (priority) |
| D9 | Submit now (A) or Phase 2 first (B) | Resolved: B (Phase 2 first) gated by PhD |
| D10 | Illiquidity definition: rename (α) or recompute with dollar volume (β) | Resolved: β (dollar volume), executed |
| D11 | Multiple-testing strategy | Resolved: hierarchy framing only; RW omitted (all-null result makes it redundant) |
| D12 | AI-attribution in commits | Resolved: never. Force-rewrite if accidentally included. |

---

## Part 6 — Risk register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Phase 2 confirms null at $G = 500$ | High | Medium | Paper is publishable as a clean negative result; reframe as a confirmation study |
| Phase 2 recovers a signal we can't replicate cleanly | Low–Medium | Medium | Pre-register the Phase 2 specification before fetching data; document the null at G=50 as the calibration |
| Referee fixates on the share-volume reversal | Medium | Low | The diagnostic is a feature of v1.2.0; the cover letter pre-empts this |
| Referee asks for intraday | Medium | Low | Defer to Phase 3 (intraday); cite GHT 2009 daily-data precedent |
| De Sena declines arXiv endorsement | Medium | Low | SSRN remains primary venue; alternative endorsers identified |
| AI-attribution accidentally lands in a public commit | Low | High | Habit + this checklist + force-rewrite if it slips through |

---

## Key identifiers (current)

- Concept DOI: `10.5281/zenodo.19611543` (resolves to latest)
- v1.0.0 version DOI: `10.5281/zenodo.19611544`
- v1.1.0 version DOI: `10.5281/zenodo.19835451`
- v1.2.0 version DOI: pending (will be minted on tag push)
- ORCID: `0009-0003-1036-9477`
- Public repo: `github.com/mhdk1602/fractal-pv-coupling`
- Streamlit dashboard: `fractal-pv.streamlit.app`
- SSRN submission: 2026-04-16; revised 2026-04-27 (v1.1.0); v1.2.0 update pending
- Master HEAD: `f3e8365` (after Claude-trailer strip and force-push)
