# cq: applicability-ladder scheme — ontology quality audit (Keet 6-dim), 2026-07-11

> Subject: `ontologies/cross-domain/cq/` — cq.ttl 0.1.0 + companions (shapes, shex,
> style guide, BFO sidecar, self-indexed CQ corpus, 2 Oxigraph gates).
> Method: the same grid as the GROP S-B audit (grop-quality-2026-07-10.md) — Keet
> 6 dimensions + floor invariants §3.x + mechanical evidence run LIVE, negative-tested.
> Closes finding **F-SB-6** of the GROP audit (companion cq: module unaudited).
> **Controller**: Sacha (GO 2026-07-11 "go tous, dans l'ordre").

## §1 — Subject inventory

| Artifact | Version at audit open | Role |
|---|---|---|
| cq.ttl | 0.1.0 | core scheme (2 classes, 4+1 properties, 4 rungs, 1 SKOS scheme + 5 frames — closed §2.5 mint) |
| cq.shapes.ttl | 0.1.0 | ADR-130 §2.6 gate 1 well-formedness (SHACL Core only, ADR-128 discipline) |
| cq.shex | 0.1.0 | ORM surface, strict structural parity (Keet §3.8) |
| cq-cqs.ttl | 0.1.0 | self-indexed CQ corpus (5 CQs at open) |
| cq-style-guide.md | — | Keet §3.9 companion |
| alignments/cq-bfo-2020.ttl | 0.1.0 | BFO 2020 systematic grounding sidecar |
| queries/binding-coherence-gate.rq | — | ADR-130 §2.6 gate 2 (Oxigraph, 0 rows = PASS) |
| queries/grounding-gate-bfo.rq | — | Keet §3.7 gate (Oxigraph, 0 rows = PASS) |

## §2 — Mechanical evidence (run LIVE 2026-07-11)

| # | Check | Command / query | Result | Status |
|---|---|---|---|---|
| 1 | Parse + SHACL well-formedness | `rudof shacl-validate -s cq.shapes.ttl cq.ttl cq-cqs.ttl grop/grop-cqs.ttl` | No Errors found | **PROVEN** |
| 2 | SHACL NEGATIVE CONTROL | synthetic CQ missing cq:appliesAtScale + cq:contextualFrame | 2 Violations | **PROVEN** — shapes live |
| 3 | Binding-coherence gate (§2.6 gate 2) | Oxigraph, queries/binding-coherence-gate.rq over cq.ttl + cq-cqs.ttl + grop-cqs.ttl | 0 rows | **PROVEN** |
| 4 | Coherence NEGATIVE CONTROL | mutated CQ declared cq:upper (ordinal 0) asking about an L1 term | 1 row (CQ-BAD2, 0 < 1) | **PROVEN** — gate live |
| 5 | BFO grounding gate (§3.7) | Oxigraph, queries/grounding-gate-bfo.rq with sidecar co-loaded | 0 rows | **PROVEN** |
| 6 | BFO NEGATIVE CONTROL | same query, sidecar omitted | 2 rows (CompetencyQuestion, ScaleRung) | **PROVEN** — gate live |
| 7 | Five-layer lexical + bilingual labels (§3.2) | SPARQL over the 17 signifying entities (2 classes + 5 properties + 4 rungs + 1 scheme + 5 frames): label / prefLabel / definition / comment / scopeNote / label@fr | 0 gaps — 17/17 × 6 layers | **PROVEN** |
| 8 | Ordinal discipline | collision query (GROUP BY ordinal HAVING >1) | 0 rows — 0..3 distinct | **PROVEN** |
| 9 | Ladder closure (Q-130-1) | rung outside the closed four | 0 rows | **PROVEN** |
| 10 | Frame scale-invariance (Q-130-6) | frame carrying cq:definedAtScale | 0 rows | **PROVEN** |
| 11 | Explicit severity (§3.5) | `grep -c sh:severity cq.shapes.ttl` | **0 at audit open** | **FAIL → blocker B1** |
| 12 | CQ corpus size (§3.9 bar ≥10) | COUNT self-indexed CQs | **5 at audit open** | **FAIL → blocker B2** |
| 13 | ShEx/SHACL parity (§3.8) | manual structural comparison (2 shapes ↔ 2 shex shapes; same paths, cardinalities, node kinds; sh:class type-check documented as merged-graph concern on the ShEx side) | holds | **PASS manually** — mechanical ShEx validation UNVERIFIED (rides F-SB-8) |

## §3 — Floor invariants

| Invariant | Verdict | Note |
|---|---|---|
| §3.1 license + versionInfo + versionIRI | PASS | IRI-form CC BY-SA 4.0 + versionIRI on all four RDF artifacts |
| §3.2 five-layer lexical | PASS | 17/17 mechanically verified (check 7), bilingual labels included |
| §3.3 triple-witness deprecation | PASS (vacuous) | nothing ever published under schema.bra0.org/cross-domain/cq |
| §3.4 punning over UNION | PASS | no UNION class; frames are skos:Concept, no cross-vocabulary re-mint |
| §3.5 explicit severity | **FAIL as written → B1** | 0 sh:severity in cq.shapes.ttl (silent-shapes rule; same class as GROP B2) |
| §3.6 rudof-clean | PASS | check 1 |
| §3.7 BFO grounding systematic | PASS | both classes → BFO_0000031 (GDC), gate negative-tested; FrameScheme is SKOS infrastructure, outside gate scope (conservative reading in the sidecar header) |
| §3.8 ShEx companion + parity | PASS | check 13 |
| §3.9 companions | **FAIL as written → B2** | all five companions exist BUT the CQ corpus is 5 < 10 |

**Floor at audit open: 7/9 → CONDITIONAL, blockers B1 + B2, both with mechanical lift plans.**

## §4 — Six dimensions

| # | Dimension | Verdict | Notes |
|---|---|---|---|
| 1 | Accuracy | PASS-WITH-1-WARNING | GDC landings follow the grop:Phase 0.2.0 precedent (identity-criteria reasoning recorded, rejected Process alternative inherited); ADR-130 §2.5 realized verbatim; warning: no machine-readable OntoClean annotation (party:ontoCleanType) on the two classes — same non-blocking class as GROP F-SB-5 was (**F-CQ-1**) |
| 2 | Completeness | CONDITIONAL → PASS after lift | B2: corpus 5 < 10 at open; every existing CQ traces to a real declaration or gate |
| 3 | Conciseness | PASS | closed §2.5 mint exactly (Q-130-4/5/6 resolutions recorded in-file); no redundant axiom; frames deliberately OPEN with justification |
| 4 | Adaptability | PASS | versionIRI everywhere; ordinal-insertion design (no renumbering); open frame scheme; sidecar evolves independently |
| 5 | Clarity | PASS | 17/17 five-layer + bilingual, mechanically verified; style guide covers 100% of terms |
| 6 | Consistency | CONDITIONAL → PASS after lift | B1: silent shapes; gates + parity otherwise green, both landings on one BFO branch, no disjointness conflict |

## §5 — Lift delta (same session, Sacha GO "go tous")

- **B1 lifted**: cq.shapes.ttl 0.1.1 — explicit `sh:severity sh:Violation` on all 5
  property shapes; cq.shex tracks 0.1.1 (severity is reporting metadata, structurally
  invisible — parity unchanged).
- **B2 lifted**: cq-cqs.ttl 0.1.1 — corpus extended CQ-L6..CQ-L10 (asserted-rung
  coverage, frame resolution, L1 self-binding, BFO grounding, well-formedness floor);
  each traces to an actual declaration, gate, or shapes constraint; nothing invented.
- **Post-lift re-run** (all LIVE 2026-07-11): rudof No Errors; binding-coherence 0 rows;
  BFO gate 0 rows; corpus COUNT = 10; asksAbout-term rung coverage (CQ-L6 sketch) 0 rows.
- cq.ttl itself is **byte-untouched** (0.1.0).

## §6 — ADR-134 pins (post-lift)

| Artifact | Version | Pin (git hash-object) |
|---|---|---|
| cq.ttl | 0.1.0 | `4be42171` |
| cq.shapes.ttl | 0.1.1 | `f221fdab` |
| cq.shex | 0.1.1 | `8c92ecd5` |
| cq-cqs.ttl | 0.1.1 | `3f51fed8` |
| cq-style-guide.md | — | `230d9ba2` |
| alignments/cq-bfo-2020.ttl | 0.1.0 | `6efc883c` |
| queries/binding-coherence-gate.rq | — | `a7a288c6` |
| queries/grounding-gate-bfo.rq | — | `eb39ad41` |

## §7 — Findings

- **F-CQ-1** (warning, non-blocking): no machine-readable OntoClean annotation on
  cq:CompetencyQuestion / cq:ScaleRung. Prose analysis exists in the sidecar (identity
  criteria, GDC reasoning). Lift = the exact party:ontoCleanType pattern just applied
  to grop 0.2.0; scheme-side gated edit, named for cq: 0.2.x.
- **F-CQ-2** — **CLOSED same session**: mechanical ShEx validation now PROVEN via
  `scripts/check-shex-shacl-parity.sh` (rudof shex parse + predicate-set parity,
  negative-tested; see GROP audit S-B‴ delta). Check 13 upgrades from
  "PASS manually" to mechanically patrolled.
- **F-CQ-3** (named follow-up, inherited): term-rung DERIVATION from an ontology→rung
  map (Q-130-5) — the gate sees only asserted rungs; CQ-L6 patrols the author
  obligation meanwhile.

## §8 — Verdict

**Floor after lift: 9/9 PASS. Dimensions: 5 PASS + Accuracy PASS-WITH-1-WARNING
(F-CQ-1). Aggregate: PASS — this audit RECOMMENDS AUDITED (`omat:Audited`) for
`cross-domain/cq` (core 0.1.0, companions 0.1.1), pins §6.**

Consequences upstream: the GROP audit's Completeness warning (F-SB-6 — "born
governed" carried at DRAFT strength) is **LIFTED**: the indexation layer now rides an
audited scheme.

Promotion, whitelist rows (both gates), bra0-ns staging and IRI publication remain
**Sacha-only acts** and are NOT executed under this audit (the 2026-07-11 GO named
the audit, not the publication). Actionable row if/when Sacha publishes:

bra0_meta `ontologies/docs-published.txt`:
```
ontologies/cross-domain/cq/cq.ttl  2026-07-11  PASS  Sacha  # pin 4be42171 + BFO sidecar 6efc883c (ADR-134); audit cq-quality-2026-07-11.md
```
