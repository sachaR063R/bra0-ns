# 6-Dimension Ontology Quality Audit — bra0 Motivation Registry

> **Auditor:** bra0 ontology team
> **Date:** 2026-04-28
> **Protocol:** six-dimension ontology quality framework (Accuracy · Completeness · Conciseness · Adaptability · Clarity · Consistency) — Maria Keet rigor
> **Scope:** instance-level motivation registry — `motivation-registry.ttl` (430 triples) coupled to its `motivation-registry.shapes.ttl` (133 triples).
> **Layer:** L0.5 Cross-domain ABox under TBox parent (`edgy:`) — Q-NS-2 pattern per ADR-060.
> **Imports:** `edgy:` (cross-domain TBox) + `archimate:` (Motivation extensions). **`mapping-edgy-archimate` import REMOVED 2026-04-28** pending S2 §E.2 (canonical IRI).
> **Tool:** `rudof shacl-validate -s motivation-registry.shapes.ttl motivation-registry.ttl` + `rapper -i turtle -c`.
> **Companion audit:** [`evidence-os-ontology-quality-2026-04-22.md`](evidence-os-ontology-quality-2026-04-22.md) — see §"Cross-audit reinforcement" below for mutual reinforcement matrix.
> **Sign-off chain:** Co-STORM Phase 2026-04-28 / S1 (Sacha sole signatory) — Decision A verdict D, β builder patch, RETROACTIF SYSTÉMATIQUE on style-guide §3.3.

---

## Summary

| Dim | Verdict | Severity | Evidence path |
|-----|---------|----------|---------------|
| 1. Accuracy | **PASS** | — | EDGY native vocabulary used canonically (`edgy:Purpose / Outcome / People / Brand`); ArchiMate Motivation extensions (`Driver / Assessment / Principle / Value`) reused without invention. Punning policy (`a edgy:Purpose , archimate:Goal`) makes the EDGY↔ArchiMate close-match queryable both directions. |
| 2. Completeness | **PASS** | — | All 9 sections instantiated: Stakeholders (3), Drivers (3), Assessments (3), Principles (3), Values (3), Purposes (4 native + 17 SDGs), Outcomes (3), Stories (2), Deprecation register (1). 17 UN SDGs aligned via `skos:exactMatch http://metadata.un.org/sdg/N`. |
| 3. Conciseness | **PASS** | — | Zero invented motivation classes — entire registry is **ABox over reused TBox**. P1 Least Power exemplary: external standards (UN SDG metadata, SDGIO, ArchiMate, EDGY, SKOS, PROV) reused before invention. |
| 4. Adaptability | **PASS** | — | `owl:versionInfo "0.3.1"` on TTL + `"0.2.1"` on shapes; deprecation register (§ 0) demonstrates non-destructive evolution via `owl:deprecated` + `owl:sameAs` + `dcterms:isReplacedBy` triple-witness pattern. v0.1 → v0.2 → v0.3 trajectory is reviewer-traceable. |
| 5. Clarity | **PASS** | — | Every signifying instance carries `rdfs:label` + `skos:prefLabel` + `skos:definition` (genus + differentia, Keet rule) + `rdfs:comment` (narrative) + `skos:scopeNote` (usage). License (`CC BY-SA 4.0`) declared on header. Bilingual parity en/fr on user-facing instances. |
| 6. Consistency | **PASS-WITH-1-DESIGN-WARNING** | — | rudof: **0 Violations · 1 Warning**. Sole warning fires on `bra0mot:Purpose-SovereignKnowledgeSpaces` (`skos:definition` MinCount(1)) — **by design**, the deprecated instance is exempt from the v0.3.0 mandate (§ shapes file `SkosDefinitionShape Severity: Warning` per CQ-MR-05 ratchet plan). |

**Overall:** **PASS** — the motivation registry is reviewer-presentable, publication-ready, and serves as the canonical exemplar of the bra0 ABox-over-TBox pattern (Q-NS-2). One warning is intentional (deprecation register exemption); promotes to Violation in v0.4 once all instances comply per shapes file comment.

---

## Dimension 1 — Accuracy

> "The ontology reflects its domain faithfully; no class, property, or alignment misrepresents reality."

### Evidence

- **EDGY native typing**: `edgy:Purpose / edgy:Outcome / edgy:People / edgy:Brand` used as primary class for every Stakeholder/Purpose/Outcome instance. Per project memory `reference_edgy_facet_iri_lowercase.md`, instances use canonical lowercase facet IRIs (`edgy:identityFacet` etc.) — never the uppercase Facet classes. CQ-MR-12 detects regression.
- **ArchiMate Motivation extensions** (`archimate:Driver / Assessment / Principle / Value`) imported via `https://purl.org/archimate` — these are the official ArchiMate classes per the Open Group standard, not bra0 inventions.
- **UN SDG alignment**: 17 SDG instances use `skos:exactMatch http://metadata.un.org/sdg/N` (the **canonical UN metadata IRI** scheme, not a derived form). Enforced as Warning by `bra0mot:SDGAlignmentShape` `sh:pattern "^http://metadata\\.un\\.org/sdg/[0-9]{1,2}$"`.
- **SDGIO secondary grounding**: `skos:closeMatch sdgio:NNNN` provides BFO-aligned ontology grounding without overriding the authoritative UN IRI.
- **Punning policy at ABox**: `bra0mot:Purpose-Sovereignty a edgy:Purpose , archimate:Goal` — dual-typing makes the EDGY↔ArchiMate `closeMatch` operational at instance level. Each Purpose is queryable through both lenses. Documented in TTL header §"Conventions (v0.2.0)".

### Gap
None at instance scope. The registry inherits the one CONDITIONAL on `edgy:People ⊏ BFO_0000040` from the EDGY TBox audit (per `evidence-os-ontology-quality-2026-04-22.md` §1) — propagation to the registry is documentary only; no instance asserts a wrong BFO claim.

### Verdict
**PASS** — registry-side accuracy is unconditional. The EDGY-side Accuracy CONDITIONAL is tracked by the parent audit, not duplicated here.

---

## Dimension 2 — Completeness

> "Every intended concept and relation is expressed; CQs have a path in the TBox."

### Evidence

- **9 sections instantiated** matching the EDGY+ArchiMate Motivation layer:
  - § 0 Deprecation register (1 instance — `Purpose-SovereignKnowledgeSpaces`)
  - § 1 Stakeholders (3 — Sacha, bra0 community, EU organizations)
  - § 2 Drivers (3 — Hirschman optionality, frugality pressure, evidence-discipline)
  - § 3 Assessments (3 — sovereignty diagnosis, frugality diagnosis, evidence diagnosis)
  - § 4 Principles (3 — P1 Least Power, P2 Sovereignty, P12 Audit-Forward Posterity)
  - § 5 Values (3 — sovereignty value, frugality value, evidence value)
  - § 6 Purposes (4 native + 17 UN SDG) — Sovereignty, ContinuousInteroperability, EvidenceFirst, Frugality
  - § 7 Outcomes (3 — AlternativesAvailable, ImmutableTrail, AuditableDecision)
  - § 8 Stories (2 — SymbolicFirstPrimacy, OpenCoreCollaboration)
- **17 UN SDGs** present and individually aligned via skos:exactMatch — coverage gap on global sustainability framing closed.
- **CQs supported**: per `motivation-registry.cqs.md` (companion file in `_bmad/work/`), 12 competency questions land via SPARQL on this ABox. CQ-MR-05 (skos:definition mandatory) is shape-enforced as Warning; CQ-MR-06 (Purpose/Outcome disjointness) as Violation; CQ-MR-12 (Facet IRI lowercase) as bra0mot-side check.
- **Provenance**: every locally-authored instance carries `dcterms:creator bra0mot:Stakeholder-Sacha` + `dcterms:date "2026-04-28"^^xsd:date` (or older for legacy instances).

### Gap
None at registry scope.

The deprecated `Purpose-SovereignKnowledgeSpaces` does not carry `skos:definition` — flagged by `bra0mot:SkosDefinitionShape` as Warning. By design: deprecated instances are exempt from the v0.3 lexical mandate; promotion to Violation tracked for v0.4 once all instances comply.

### Verdict
**PASS** — coverage of the EDGY+ArchiMate Motivation layer + UN SDG corpus is complete for the v0.3.1 scope. Backlog: cap: ↔ edgy:Purpose linkage (Q-NS-1 alignment file) is **out of scope** for v0.3 per TTL header.

---

## Dimension 3 — Conciseness

> "Reuse before invent; no class exists that a W3C/enterprise standard already provides."

### Evidence

- **Zero invented classes.** The entire registry is ABox over reused TBox:
  - Native EDGY: `edgy:Purpose / Outcome / People / Brand` (4 reused)
  - ArchiMate Motivation: `archimate:Driver / Assessment / Principle / Value / Goal / Stakeholder / Course-of-Action` (7 reused)
  - W3C/SKOS: `skos:exactMatch / closeMatch / prefLabel / definition / scopeNote` (5 reused)
  - DCMI/Dublin Core: `dcterms:creator / date / source / isReplacedBy / license / created / modified` (7 reused)
  - PROV-O: `prov:wasGeneratedBy` (1 reused)
  - OWL: `owl:deprecated / sameAs / versionInfo / imports / Ontology` (5 reused)
- **External authoritative IRIs**:
  - 17 × UN SDG metadata IRIs (`http://metadata.un.org/sdg/N`)
  - 17 × SDGIO BFO-aligned IRIs (`http://purl.obolibrary.org/obo/SDGIO_NNNN`)
- **Defence prose for every multi-typed instance**: dual-typing `a edgy:Purpose , archimate:Goal` carries an inline rdfs:comment defending the punning per the v0.2.0 convention block in the TTL header.

### Gap
None.

### Verdict
**PASS** — exemplar of P1 Least Power. Sets a reuse-density precedent that is observably stricter than the evo:/asc: stack. Future bra0 ABox files should be benchmarked against this density.

---

## Dimension 4 — Adaptability

> "Layers evolve at independent cadences without breaking their contracts."

### Evidence

- **`owl:versionInfo`**: TTL `"0.3.1"`, shapes `"0.2.1"`. Independent cadence: shapes ratchet (v0.2.0 → 0.2.1) does not require TTL version bump.
- **Deprecation register (§ 0) is the load-bearing feature**: `Purpose-SovereignKnowledgeSpaces` (v0.1 broad parent) was narrowed to four orthogonal peers in v0.2 via the **triple-witness pattern**:
  - `owl:deprecated true` (OWL signal)
  - `owl:sameAs Purpose-Sovereignty` (formal OWL fusion — preserves entailments)
  - `dcterms:isReplacedBy Purpose-Sovereignty` (SKOS-side replacement)
  - `rdfs:comment` documenting the absorbed verbs ("edit"→ContinuousInteroperability, "audit"→EvidenceFirst, "federate"→ContinuousInteroperability)
  This pattern is reviewer-readable, OWL-reasoner-correct, and downstream-consumer-safe.
- **Path-shape adaptability** (added 2026-04-28): canonical IRI rewritten from v0.1's `schema.bra0.org/motivation-registry/` to v0.3.1's `schema.bra0.org/cross-domain/edgy/motivation-registry/` (D-path) per Co-STORM S1 Decision A. **Rupture-sèche** applied — no `owl:sameAs` legacy carry-over (vacuous in practice; v0.3.0 was never publicly resolvable). The ADR-060 cross-domain rank is honoured at the namespace level.
- **Shape ratchet plan**: `SkosDefinitionShape` is `sh:Severity sh:Warning` for v0.3; promotes to Violation in v0.4 once all instances comply. Documented in shapes file comment block. Adaptability through deferred enforcement.

### Gap
The `mapping-edgy-archimate.ttl` `owl:imports` was REMOVED on 2026-04-28 pending S2 §E.2 (canonical IRI). Tracked as backlog. Re-add once whitelisted in bra0-ns. Documented in TTL line 62-64. Does not block v0.3.1 publication.

### Verdict
**PASS** — registry leads the bra0 stack on versioning + deprecation discipline. Cross-strengthens evo: by demonstrating the triple-witness pattern is operational.

---

## Dimension 5 — Clarity

> "Every term is readable by a stranger — `rdfs:label` + `rdfs:comment` in target languages; licence and provenance visible."

### Evidence

- **License**: `dcterms:license "https://creativecommons.org/licenses/by-sa/4.0/"` on the ontology header (TTL line 55, shapes line 22). **Closes the P0-9 Clarity gap raised by the evidence-os audit** — the registry sets the precedent every bra0-authored ontology now follows.
- **Genus + differentia (Keet rule)**: every signifying instance carries `skos:definition` formed as `<broader-class> + <distinguishing-trait>`. Shape `bra0mot:SkosDefinitionShape` enforces (Warning until v0.4).
- **Five-layer lexical discipline** per signifying instance:
  - `rdfs:label` — minimal en string for graph rendering
  - `skos:prefLabel` — UI-rendering canonical label (prefLabel is for humans, label is for graphs)
  - `skos:definition` — genus + differentia (Keet)
  - `rdfs:comment` — narrative ("why does this exist")
  - `skos:scopeNote` — usage ("when do you use this, when not")
- **Bilingual parity**: en + fr language tags on user-facing instances (Stakeholders, Purposes, Outcomes). Shape requires `@en` minimum.
- **Audit-forward provenance**: `dcterms:creator` + `dcterms:date` on every locally-authored instance. Reviewers can date-bisect any instance.
- **Style-guide companion**: `motivation-registry-style-guide.md` (in `_bmad/docs/`) documents the lexical discipline. Per Co-STORM S1 follow-up #4 (RETROACTIF SYSTÉMATIQUE), every bra0-authored ontology MUST receive a style-guide companion; registry is the reference template.

### Gap
None at registry scope.

### Verdict
**PASS** — registry leads the bra0 stack on Clarity. Closes evo:/edgy: P0-9 license gap by example.

---

## Dimension 6 — Consistency

> "The ontology does not contradict itself; rudof validation passes."

### Evidence

- **rudof shacl-validate**: 0 Violations, 1 Warning (run: 2026-04-28).
- **rapper parse**: 430 triples in TTL, 133 triples in shapes. Both parse clean.
- **Disjointness invariant** (CQ-MR-06): `bra0mot:PurposeOutcomeDisjointShape` — an instance MUST NOT be `a edgy:Purpose , edgy:Outcome` simultaneously. Per BFO grounding: Purposes are infinite-game continuants (RealizableEntity), Outcomes are finite measurables (ProcessBoundary). Validated zero violations on the 22 Purposes + 3 Outcomes.
- **No cyclic imports**: registry imports `edgy:` + `archimate:`; neither imports back. Cross-layer directionality: cross-domain L0.5 → external standards. No cycle.
- **Stakeholder type closure**: `bra0mot:StakeholderShape` requires every `archimate:Stakeholder` to also be `edgy:People` OR `edgy:Brand` per the official EDGY-ArchiMate mapping. Validated zero violations.
- **Path-shape consistency** (added 2026-04-28): every IRI in the ontology resolves under the canonical D-path namespace `https://schema.bra0.org/cross-domain/edgy/motivation-registry/`. Verified by leak-grep (zero matches on legacy `schema.bra0.org/motivation-registry/` or `omyn.ai/schema/`).

### Gap

The 1 Warning on `Purpose-SovereignKnowledgeSpaces` (no `skos:definition`) is **by design** — deprecated instances are exempt from the v0.3 mandate. Promotes to Violation in v0.4 once all instances comply. Documented in shapes file `SkosDefinitionShape` comment block.

### Verdict
**PASS-WITH-1-DESIGN-WARNING** — the warning is structurally intentional and tracked.

---

## Cross-audit reinforcement

> Mutual reinforcement matrix between this audit and [`evidence-os-ontology-quality-2026-04-22.md`](evidence-os-ontology-quality-2026-04-22.md). Each row identifies an item where the two audits **strengthen each other**: the motivation registry serves as the empirical ABox witness for TBox claims in the evidence-os stack, and the evidence-os ratchet discipline carries forward to the registry's CI gating.

### Matrix A — registry strengthens evidence-os audit

| evidence-os item | Registry contribution | Strengthening effect |
|---|---|---|
| **Dim 2 P0-2 (3-Story arbitration)** — `edgy:Story ∪ asc:Story ∪ evo:UserStory` cross-layer coverage gap. | Registry instantiates 2 `edgy:Story` instances (`SymbolicFirstPrimacy`, `OpenCoreCollaboration`), each typed `a edgy:Story , archimate:Course-of-Action`. | Provides the **first concrete ABox witness** of `edgy:Story` semantics — the P0-2 UNION arbitration can now be tested against real instance data, not abstracted alone. The dual-typing demonstrates one viable resolution path (punning at instance level rather than TBox-level UNION class). |
| **Dim 5 P0-9 (license unification)** — `dct:license` missing on `evo:` and `edgy:` headers. | Registry header carries `dcterms:license "https://creativecommons.org/licenses/by-sa/4.0/"` since v0.1.0. Shapes file mirrors. | Sets the **operational precedent**: every bra0-authored ontology's header now has a working template to copy. The P0-9 fix is a 3-line edit on each missing file. |
| **Dim 4 — Adaptability (PASS at evo:)** — `owl:versionIRI` discipline. | Registry uses `owl:versionInfo "0.3.1"` + deprecation register (§ 0) demonstrating the **triple-witness pattern** (`deprecated` + `sameAs` + `isReplacedBy`). | Extends the Adaptability discipline from version-string-only (evo:) to **non-destructive class evolution** (registry §0). Future evo: class deprecations have a battle-tested pattern. |
| **Dim 5 — Clarity bilingual parity (PASS at evo:)** — bilingual `@fr` + `@en`. | Registry adds the **5-layer lexical discipline**: `label` + `prefLabel` + `definition` + `comment` + `scopeNote`. | Tightens the Clarity bar: evo:'s 2-layer (`label` + `comment`) becomes the floor; registry's 5-layer becomes the ceiling. Style-guide retroactive sweep (Co-STORM S1 follow-up #4) backports this pattern. |
| **Dim 3 — Conciseness CONDITIONAL (P0-7/P0-8 multi-parent)** — `asc:AgentService` 3 parents, `evo:ComplianceFramework` 2 parents. | Registry's **punning policy** at ABox (`a edgy:Purpose , archimate:Goal`) demonstrates that multi-typing is defensible **as instance-level pragma**, not class-level confusion. | Reframes P0-7/P0-8: the question is not "is multi-parenting OK", but "where in the stack does multi-typing live". Registry demonstrates ABox is the right layer; pushes evo:/asc: to defend why their multi-parent occurs at TBox. |

### Matrix B — evidence-os audit strengthens this audit

| evidence-os ratchet | Registry inheritance | Strengthening effect |
|---|---|---|
| **rudof coupled floor (50 violations held)** | Registry runs against its own shapes file: 0 Violations + 1 design Warning. | Registry's 0/1 result is **stricter than the evo: stack baseline of 50** — sets the v0.4 ratchet target for the coupled run (registry instances added to coupled validation must not lift the floor). |
| **Cross-reference table convention (§ "Cross-audit cross-reference")** | This audit adopts the same table format ("Item / file-level / coupled") in the matrices above. | Establishes a **reusable audit-pattern**: every new bra0 audit declares its mutual reinforcement with prior audits. Cumulative knowledge instead of audit-island. |
| **Disjointness axiom discipline (P0-6)** | Registry adds `PurposeOutcomeDisjointShape` (CQ-MR-06): an instance MUST NOT be both `edgy:Purpose` and `edgy:Outcome`. | Pushes the disjointness pattern from asc: TBox into ABox-level shape enforcement. Validates that the pattern scales across the L0.5 / L1 / L3 layer boundary. |
| **No-cycle import directionality (evo:→asc:, never reverse)** | Registry imports `edgy: + archimate:` only; neither imports the registry. | Confirms the **cross-domain → external-standards** directionality holds at L0.5 (registry layer) symmetrically to L1/L3 (asc:/evo:). One contiguous invariant across 3 layers. |
| **Multi-arbitration chain (P0-2/7/8/9 lift CONDITIONAL → PASS)** | Registry's design-Warning on deprecation exempt is **the same arbitration shape**: a known gap, scoped, documented, with a defined lift trigger (v0.4 promotion to Violation). | Registry inherits the discipline of "CONDITIONAL with named-lift-trigger" rather than silent gap. Audit-forward posterity (P12) operates the same way at L0.5 as at L1/L3. |

### Joint invariants (now binding on both audits)

These cross-cutting rules are now **load-bearing for any future bra0 ontology audit** — they emerged from the mutual reinforcement of the evidence-os + motivation-registry audits and apply going forward to retroactive sweeps and new ontologies alike:

1. **License visibility is non-optional**: `dcterms:license` on every ontology header (closes P0-9 by precedent).
2. **5-layer lexical discipline**: `rdfs:label` + `skos:prefLabel` + `skos:definition` (Keet genus+differentia) + `rdfs:comment` + `skos:scopeNote` for every signifying instance/class. Shape-enforced as Warning, ratcheting to Violation per ontology's roadmap.
3. **Triple-witness deprecation**: `owl:deprecated` + `owl:sameAs` + `dcterms:isReplacedBy` whenever an IRI is superseded. The deprecation entry survives the migration.
4. **Punning over UNION** for cross-vocabulary equivalence at instance level (registry's pattern), versus UNION class invention at TBox level (rejected by P1 Least Power).
5. **Cardinality contracts** in shapes carry an explicit `Severity` + an explicit lift-trigger comment. No silent shapes; every Warning is on a documented ratchet.
6. **rudof-clean is the publication gate**: 0 Violations is mandatory; design-warnings allowed iff documented in the shapes file with a v-Next promotion trigger.

These six joint invariants are the **shared backbone** of the audit-forward posterity contract. Future audits cite this section instead of re-deriving these rules.

---

## Recommendation

The motivation registry is **publication-ready** at v0.3.1. The whitelist line for `bra0-ns/docs-published.txt` is:

```
cross-domain/edgy/motivation-registry/motivation-registry.ttl;DRAFT;audit/motivation-registry-quality-2026-04-28.md;2026-04-28
```

**Build verification (pre-publication)**:
- ✓ Mirror staged at `bra0-ns/cross-domain/edgy/motivation-registry/motivation-registry.ttl` (byte-identical to `bra0_meta/ontologies/enterprise/motivation-registry.ttl`)
- ✓ rapper parse: 430 triples, clean
- ✓ rudof shacl-validate: 0 Violations, 1 design Warning (deprecation exempt)
- ✓ ADR-058 §2.1 + §2.7 step 11 (β flat-TTL alias) honoured by builder patch (3 pytest cases GREEN, 52/52 suite GREEN)
- ✓ ADR-060 §3 cross-domain rank consistent (registry sits at L0.5 ABox under `edgy:` TBox parent)
- Pending Sacha sign-off: whitelist line lands as soon as leak-grep on `_site/<motivation-registry>` post-build returns clean (per Co-STORM S1 follow-up #3 ordering).

**Promotion roadmap**:

| To version | Trigger | Effect |
|---|---|---|
| v0.4 | All instances carry `skos:definition` (including deprecated) | `SkosDefinitionShape` Warning → Violation; this audit's Dim 6 lifts to **PASS** unconditional (no design-warning) |
| v0.5 | S2 §E.2 lands canonical IRI for `mapping-edgy-archimate.ttl` | Re-add `owl:imports <mapping-edgy-archimate>` to TTL line 60; closes the §0 backlog item |
| v0.6 | Q-NS-1 alignment file (cap: ↔ edgy:Purpose) signed | Adds `dcterms:requires` triples linking each capability family to its motivation-registry Purpose; activates Dim 2 Completeness backlog item |

No new rudof shape, no new fixture required for v0.3.1 publication. The 6-dim audit closes here; v0.4 audit will reference this one as predecessor.

---

## Annex — commands used

```bash
# Parse cleanliness (pre-publication gate)
rapper -i turtle -c ontologies/enterprise/motivation-registry.ttl
# => 430 triples
rapper -i turtle -c ontologies/enterprise/motivation-registry.shapes.ttl
# => 133 triples

# rudof SHACL validation (pre-publication gate)
rudof shacl-validate \
  -s ontologies/enterprise/motivation-registry.shapes.ttl \
  ontologies/enterprise/motivation-registry.ttl
# => 0 Violations, 1 Warning (Purpose-SovereignKnowledgeSpaces — by design)

# Mirror parity (publication-target gate)
diff bra0_meta/ontologies/enterprise/motivation-registry.ttl \
     bra0-ns/cross-domain/edgy/motivation-registry/motivation-registry.ttl
# => identical

# Mirror rudof check (publication-target gate)
rudof shacl-validate \
  -s bra0_meta/ontologies/enterprise/motivation-registry.shapes.ttl \
  bra0-ns/cross-domain/edgy/motivation-registry/motivation-registry.ttl
# => 0 Violations, 1 Warning (same warning — by design)
```

Audit closed 2026-04-28 — Co-STORM Phase 2026-04-28 / S1 sign-off context.
