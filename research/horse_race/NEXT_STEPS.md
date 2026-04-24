# Next Steps — Post Horse Race Extension

**Status at**: 2026-04-24
**Branch**: `horse-race` (ready for merge)
**Latest commit**: `a865a05` — LaTeX fix + recompiled PDF

---

## Part 1 — Immediate (this week)

### 1.1 Merge `horse-race` into `master`

The branch is feature-complete for the v1 revision. All referee audits incorporated, all Tier 3 inference methods operational, Table 6 and Table 7 integrated into the manuscript, cover letter drafted, PDF compiles cleanly.

```bash
cd /Users/haridines/github/personal/Matlab---fractal-modelling
git pull origin horse-race         # sync local first
git checkout master
git merge horse-race --no-ff        # preserve branch history
git push origin master
```

After merge, `master` becomes the canonical revised manuscript.

### 1.2 Update SSRN preprint

SSRN accepts revised versions. Log in, navigate to the paper's author dashboard, replace the PDF with the updated `main.pdf` from master. The submission retains its abstract ID; version count increments.

Short change log for the revision note:
> Added Section 5.4 (Horse Race Against Standard Liquidity Predictors) with 9 benchmarks including Roll (1984), Corwin-Schultz (2012), rolling Amihud, and four baseline controls. Added small-sample-corrected inference via Bell-McCaffrey CR2 with Satterthwaite df and the wild cluster restricted bootstrap. Updated Tables 6-7; bibliography expanded by 10 entries.

### 1.3 Mint a new Zenodo version DOI

A GitHub release on master triggers Zenodo to create a new version DOI automatically. The concept DOI (`10.5281/zenodo.19611544`) continues to resolve to the latest.

```bash
gh release create v1.1.0 --repo mhdk1602/fractal-pv-coupling \
  --title "v1.1.0: Horse race extension and Tier 3 inference upgrades" \
  --notes "Adds horse race against 9 standard liquidity predictors, Bell-McCaffrey CR2 + Satterthwaite df, and wild cluster restricted bootstrap. Updated manuscript Tables 6-7."
```

---

## Part 2 — Short-term (next 2-4 weeks)

### 2.1 De Sena endorsement follow-up

LinkedIn message sent 2026-04-22. No reply as of 2026-04-24.

Decision tree:

- **If reply by 2026-05-06 (two-week window):** proceed with arXiv upload immediately.
- **If no reply by 2026-05-06:** approach backup endorser #1 with a briefer version of the same message, citing the SSRN preprint and Zenodo DOI.
- **If no endorsement by 2026-05-20:** proceed with SSRN-only preprint distribution. SSRN is the more important venue for finance anyway; arXiv is secondary.

Backup endorser candidates to identify in advance:
- Recent arXiv q-fin.ST corresponding authors whose work cites DFA or Hurst in finance
- Academics cited in the manuscript's bibliography who are still active
- Members of the econophysics-finance community (Kristoufek, Barunik, Drożdż) known to endorse first-time submitters

### 2.2 arXiv submission package

Already drafted in `research/submission/` conceptually. Before actual upload:

- [ ] Build tarball: `main.tex`, `references.bib`, `figures/*.pdf`, `elsarticle.cls`
- [ ] Write the 200-word arXiv abstract (separate from paper abstract)
- [ ] ORCID field, Zenodo DOI in the "report number" or "comments" field
- [ ] Category: `q-fin.ST` primary, consider cross-listing to `stat.ME`
- [ ] License: CC BY-NC-ND to match SSRN

### 2.3 Link Zenodo DOI to ORCID

One-time manual step (5 minutes): orcid.org → Works → Add → Search & Link → DataCite → search `10.5281/zenodo.19611544` → import. This completes the research identity chain.

---

## Part 3 — Journal submission (4-8 weeks out)

### 3.1 Final manuscript QA pass

Before Quantitative Finance submission:

- [ ] Read the compiled PDF end-to-end for typos and layout issues
- [ ] Verify all figure references resolve (no `??` placeholders)
- [ ] Verify all citations appear in the reference list
- [ ] Spell-check all tables
- [ ] Confirm the author-block affiliation is "Independent Researcher" only
- [ ] Verify the Data Availability section has current DOI
- [ ] Word count against journal limit (Quantitative Finance is typically flexible)

### 3.2 Quantitative Finance submission

Target date: 2026-05-15, conditional on SSRN indexing complete and revision stable for ≥1 week.

Submission portal: https://mc.manuscriptcentral.com/tandf/qf

Attachments:
- Manuscript PDF (`main.pdf`)
- Cover letter (`cover_letter_quantfinance.md` converted to DOCX or PDF)
- Supplementary materials (optional: CHECKPOINT.md, replication-script summary)

Uncomment the `\journal{Quantitative Finance}` line in `main.tex` before generating the submission PDF.

### 3.3 Response preparation

Within 24 hours of submission, draft a single-file `research/submission/referee_response_template.md` anticipating likely criticisms:

1. "Why not intraday data?" → defer to Phase 3, cite data-cost constraints, reference existing daily-frequency papers for methodological precedent
2. "Why only S&P 500?" → defer to Phase 2, acknowledge survivorship bias, cite GHT 2009 and Amihud 2002 as having similar scope
3. "Why CII rather than DCCA or coherence?" → already addressed in Discussion §6.5; CII is a second-order property (scaling exponent co-movement) while DCCA is a first-order property (level cross-correlation)
4. "How does this relate to [specific paper we missed]?" → prepare to add 1-3 citations quickly

---

## Part 4 — Medium-term (2026 H2)

### 4.1 Phase 2 — Market breadth extension (second paper)

Working title: *Fractal Price-Volume Coupling Across Asset Classes: Small Caps, International Markets, and Cryptocurrencies*

Scope:
- **Russell 2000 constituents**: 50 representative small caps, point-in-time membership to avoid survivorship bias
- **Sector ETFs**: 11 GICS SPDR ETFs (XLK, XLF, etc.) for aggregated behaviour
- **International**: FTSE 100, Nikkei 225, DAX 40, Hang Seng samples
- **Cryptocurrencies**: BTC, ETH, top-10 by market cap; handle 24/7 trading via calendar-day rolling windows
- **ADRs**: US-listed depositary receipts for price-discovery comparison

Key research questions:
- Does CII survive in less-liquid asset classes?
- Does the illiquidity prediction generalize across market structures?
- Does crypto's 24/7 trading alter the coupling dynamics?
- Does ADR price discovery mechanism produce different coupling patterns?

Timeline: begin data collection 2026-06; first results 2026-09; submission-ready manuscript 2026-12.

Venue options: Journal of Financial Markets (if coupling breaks in some classes, interesting null), Journal of Empirical Finance (if coupling holds uniformly), or Finance Research Letters for a shorter note.

### 4.2 Phase 3 — Intraday frequency (third paper)

Working title: *Intraday Fractal Coupling Around Scheduled Information Events*

Scope:
- 5-minute or 30-minute bars for ~50 S&P 500 stocks
- Event study around FOMC announcements, earnings releases, macroeconomic data releases
- Test whether CII tightens in the minutes before scheduled information events

Data: Polygon.io Starter subscription (~$200/month for sufficient history), or WRDS TAQ if institutional access becomes available.

Timeline: 2027 H1. Deferred until first and second papers are submitted or accepted.

Venue: Journal of Financial Markets, Review of Financial Studies (ambitious), or Journal of Empirical Finance.

### 4.3 Dissertation integration (parallel track)

The fractal work is methodologically orthogonal to the PhD on institutional pressures and data governance. However, a methodology-chapter cross-reference is defensible: cite the fractal-coupling paper as an exemplar of evidence-first empirical methodology.

Action: raise at next PhD committee meeting, post-v1 submission. Do not attempt to force the fractal work into the dissertation proper; keep as orthogonal research programs.

---

## Part 5 — Decisions pending

Keyed to the CHECKPOINT.md decision register, updated:

| Key | Decision | Status |
|-----|----------|--------|
| D1 | Next coding step | **Resolved**: Tier 3 + Table 6 complete |
| D2 | Backup endorser if De Sena declines | Open; decide by 2026-05-06 |
| D3 | When to merge `horse-race` to `master` | **Resolved**: now (Part 1.1 above) |
| D4 | XSPREAD_0 placement | **Resolved**: online appendix only; MSPREAD_0 in main table |
| D5 | Commercial/practitioner engagement post-arXiv | Open; default: decline until journal acceptance |
| D6 (new) | Treat horse race as revision or separate paper | **Resolved**: revision of v1 |
| D7 (new) | SSRN version note wording | Open; draft text in Part 1.2 above |
| D8 (new) | Journal if QF desk-rejects | Physica A → Journal of Empirical Finance → Finance Research Letters (priority order) |

---

## Part 6 — Risk register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| De Sena declines / silence | Medium | Low-Medium | Backup endorsers; SSRN is primary venue anyway |
| SSRN indexing >2 weeks | Low | Low | Status check at day 10; escalate if needed |
| QF desk-rejects | Medium | Medium | Fallback journals ordered; response-letter template prepared |
| Referee demands intraday replication | Medium | Medium | Cite data constraints; promise for Phase 3; defend daily frequency with GHT 2009 precedent |
| CR2 marginal p = 0.066 becomes the referee's focus | Medium-High | Medium | Emphasise WCR p = 0.018 as binding inference per MW 2017; cite Satterthwaite conservatism explicitly |
| Phase 2 coupling fails in crypto or small caps | Low-Medium | Low | Honest null is still publishable; cite boundary conditions |
| Practitioner inquiry compromises academic track | Low | Medium | Decline commercial engagement until journal acceptance |

---

## Key identifiers (unchanged from CHECKPOINT.md)

- Zenodo concept DOI: `10.5281/zenodo.19611544`
- ORCID: `0009-0003-1036-9477`
- Private repo: `github.com/mhdk1602/fractal-pv-coupling`
- Public repo: `github.com/mhdk1602/fractal-pv-dashboard`
- Streamlit app: `fractal-pv.streamlit.app`
- SSRN submission date: 2026-04-16 (day 8 and counting)
- De Sena LinkedIn message: 2026-04-22 (two days ago)
- Horse-race branch: `horse-race` on private repo, ready for merge to master
