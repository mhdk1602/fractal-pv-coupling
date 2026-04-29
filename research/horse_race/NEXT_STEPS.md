# Next Steps — v1.3.0 Phase 2 Universe Expansion Complete

**Status as of**: 2026-04-28 (end of session)
**Branch**: `master`
**Active version**: **v1.3.0** (manuscript rewritten, commit + tag imminent)
**Submission gate**: post-PhD (University of the Cumberlands, defense ~2027). Pre-PhD activity is timestamping only on SSRN + arXiv.

---

## What v1.3.0 changes from v1.2.0

The v1.2.0 paper reported a clean predictive null at $G = 50$ across ten target specifications under modern small-sample inference. v1.3.0 expands the universe to the full S&P 500 ($G = 488$ after standard inclusion criteria), reproduces the descriptive coupling phenomenon at the broader scale, and surfaces a structural inference disagreement that organises this version of the paper:

- **Firm-conditional inference methods** (firm-clustered, two-way clustered, Bell--McCaffrey CR2, wild cluster restricted bootstrap) all agree the CII coefficient is statistically null on the primary outcome and on every other target after horse-race conditioning.
- **Time-conditional inference methods** (time-clustered, Driscoll--Kraay HAC) detect a significant cross-firm time-period co-movement that the firm-conditional methods absorb into the noise.
- The horse race against nine standard liquidity benchmarks is decisive: every focal-only signal in the battery is fully absorbed in the combined specification (forward Corwin--Schultz spread is the cleanest illustration: focal two-way $t = +3.64$ collapses to combined $t = +0.07$).
- The Bell--McCaffrey CR2 Satterthwaite effective degrees of freedom *collapsed* from $\approx 4.4$ at $G = 50$ to $\approx 1.0$ at $G = 488$, despite the cluster count rising 9.8x. Cluster heterogeneity (a small number of leverage-heterogeneous firms dominating the meat matrix) is the cause; this is now its own diagnostic subsection.

The paper retains the v1.2.0 share-volume vs. dollar-volume Amihud diagnostic; v1.3.0 adds two new methodological observations (firm-vs-time inference choice, Satterthwaite df collapse).

H2 confirmed at $G = 488$ (mean within-firm $r = 0.531$, 92.7% positive, present across all eleven GICS sectors). H3 confirmed in a sharper *distribution-shape* form than the original 50-firm sample suggested (Mann-Whitney $p = 0.0019$ on the high-vs-low VIX cross-firm distribution, with the high-VIX regime exhibiting both higher median and substantially larger dispersion; mean coupling does not uniformly intensify).

Title retitled to *"Temporal Fractal Coupling of Volatility and Trading Volume: A Robust Within-Firm Pattern, a Time-Period Stress Signal, and No Firm-Specific Forecast Power in S&P 500 Stocks, 2015-2026."*

---

## Part 1 — Done in this session

- [x] Pre-registration document `PHASE2_PROTOCOL.md` v1.0
- [x] S&P 500 ticker list curated (`data/sp500_constituents_2026-04-28.csv`)
- [x] Batch yfinance fetcher (`fetch_universe_batch`) implemented for 500-ticker scale
- [x] G=100 pilot validated pipeline scaling
- [x] Full G=488 Phase 2 run completed; results pickled and consumed
- [x] H2 and H3 re-verified at G=488 (both confirmed, H3 reformulated to distribution-shape)
- [x] PHASE2_RESULTS.md written (durable run artifact)
- [x] Manuscript v1.3.0 update: title, abstract, intro H4 paragraph, methods §3 universe, §4.1 H2 numbers, §4.2 H3 distribution-shape, §5.4 H4 with Phase 2 numbers and the firm-vs-time inference disagreement, new §5.4.5 cluster-heterogeneity diagnostic, discussion §6 pivot, conclusion. Recompiled cleanly.
- [x] Cover letter rewritten for v1.3.0 framing with revision-history disclosure
- [x] Session-progress summary `SESSION_2026-04-28.md` written for future reference

## Part 2 — Imminent (this session, pending only the user's go-ahead on commit)

- [ ] Commit v1.3.0 (no AI-attribution trailer per D12)
- [ ] Push to master
- [ ] Tag v1.3.0 on GitHub via API
- [ ] Verify Zenodo mints v1.3.0 version DOI within ~15 minutes
- [ ] Update fractal-research memory with v1.3.0 state
- [ ] Hand the SSRN preprint update step back to Dinesh (manual)

## Part 3 — Out-of-session

- [ ] Dinesh updates SSRN preprint with v1.3.0 PDF. Change log: "Extended the analysis to the full S&P 500 panel (G = 488 firms after inclusion criteria) under a pre-registered protocol. Confirms H2 and H3 at the broader scale (H3 reformulated to distribution-shape amplification rather than mean amplification). Surfaces a firm-conditional vs. time-conditional cluster-robust inference disagreement on H4. Adds the Satterthwaite df collapse at moderate G as a third methodological observation alongside the v1.2.0 share-volume Amihud confound."
- [ ] (Optional) Edit Zenodo v1.2.0 record metadata via web UI to correct creator name from alias to legal byline. v1.3.0 onward will inherit the corrected name automatically via `.zenodo.json`.
- [ ] arXiv: De Sena endorsement window. If reply by 2026-05-06, upload v1.3.0. Backup-endorser pursuit if no reply by 2026-05-06; SSRN-only by 2026-05-20 if no endorsement.

---

## Part 4 — Post-PhD journal submission

Both gated on PhD completion (~2027).

### 4.1 Primary venue (post-pivot): Physica A

The v1.3.0 paper is now structurally a *Physica A: Statistical Mechanics and its Applications* submission. The descriptive-pattern + methodological-caveat framing is exactly that journal's editorial profile. Realistic outlook: ~20-40 citations over a decade if accepted; B-tier.

### 4.2 Stretch venue: Quantitative Finance

Still possible but less natural than v1.0/v1.1 originally hoped. The methodological-observation density (three transferable cautions) is QF-appropriate; the lack of a positive predictive headline is the friction. If submitted, expect major revision asking either for predictive content recovery (which would require Paper 2; see below) or for a deeper mechanism / structural model.

### 4.3 Fallback: Journal of Empirical Finance, Finance Research Letters

Both viable for a shorter version. JEF likely if the paper is reframed as a microstructure-leaning piece. FRL viable as a methods-note-style condensation.

---

## Part 5 — Lead worth flagging for Paper 2

The firm-cluster null + time-cluster significant pattern at $G = 488$ is the statistical signature of a *market-wide* signal rather than a firm-specific one. A natural Paper 2:

**Working title**: *"Aggregate Fractal Coupling as a Market-Wide Liquidity Stress Indicator"*

**Hypothesis**: Cross-sectionally aggregated CII, $\overline{\text{CII}}_t = (1/G) \sum_i \text{CII}^{(i)}_t$, correlates with market-wide liquidity stress measures (NY Fed CFSI, Pastor-Stambaugh liquidity factor, BAA-Treasury credit spread, the VIX) and may serve as a real-time stress indicator.

**Data needed**: already in hand. The Phase 2 panel + a few external time-series.

**Effort**: a few hours if pursued with focus.

**Decision**: defer to post-PhD. Do not bundle into v1.3.0 — the unit of analysis is market-time-series rather than firm-month-panel and bundling would muddy the present paper.

---

## Part 6 — Decision register (final state)

| Key | Decision | Status |
|-----|----------|--------|
| D1 | Next coding step | Resolved: through Phase 2 |
| D2 | Backup endorser if De Sena declines | Open; deadline 2026-05-06 |
| D3 | Merge `horse-race` to `master` | Resolved: merged 2026-04-26 |
| D4 | XSPREAD_0 placement | Resolved: online appendix only |
| D5 | Commercial/practitioner engagement | Default decline until journal acceptance |
| D6 | Treat horse race as revision or separate paper | Resolved: revision, folded into v1.2.0 |
| D7 | SSRN version note wording | Resolved: drafted in Part 3 above |
| D8 | Journal if QF rejects | Resolved: Physica A → JEF → FRL |
| D9 | Submit-now (A) vs Phase-2-first (B) | Resolved: B, Phase 2 done in this session |
| D10 | Illiquidity α (rename) vs β (recompute) | Resolved: β, dollar-volume Amihud |
| D11 | Multiple-testing strategy | Resolved: hierarchy framing only |
| D12 | AI-attribution in commits | Resolved: never, force-rewrite if leaked |
| D13 (new) | Pursue aggregate-CII Paper 2 pre-PhD or defer | Open; default defer |
| D14 (new) | Edit v1.2.0 Zenodo metadata or accept stale alias byline | Open; recommend brief edit via Zenodo web UI |

---

## Part 7 — Risk register (updated)

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Phase 2 confirms null at G=488 | Realised | Medium | v1.3.0 reflects this honestly |
| Referee at Physica A asks for the aggregate-CII follow-up | Medium | Low-Medium | Defensible to point to Paper 2 in plan |
| Referee fixates on share-volume reversal | Low | Low | Disclosed in cover letter |
| Referee fixates on Satterthwaite df=1.0 | Medium | Low | Now a feature, not a bug; documented in §5.4 |
| Referee asks for intraday | Medium | Low | Defer to Phase 3 (intraday paper); cite GHT 2009 |
| De Sena declines arXiv endorsement | Medium | Low | SSRN remains primary |
| Phase 2 numerical reproducibility challenged | Low | Medium | Pre-registration + pickle artifacts + frozen pipeline at master HEAD `f8aa564` |
| AI-attribution leaks into a public commit | Low | High | Habit + memory rule + force-rewrite policy |

---

## Key identifiers (current)

- Concept DOI: `10.5281/zenodo.19611543` (always-latest)
- v1.0.0 version DOI: `10.5281/zenodo.19611544`
- v1.1.0 version DOI: `10.5281/zenodo.19835451`
- v1.2.0 version DOI: `10.5281/zenodo.19856250`
- v1.3.0 version DOI: pending tag (will be minted on `git tag v1.3.0` + GitHub release)
- ORCID: `0009-0003-1036-9477`
- Public repo: `github.com/mhdk1602/fractal-pv-coupling`
- Streamlit dashboard: `fractal-pv.streamlit.app`
- SSRN: revised 2026-04-27 (v1.1.0); v1.2.0 and v1.3.0 updates pending Dinesh's manual upload
- Master HEAD at session end: pending v1.3.0 commit (parent: `f8aa564`)
