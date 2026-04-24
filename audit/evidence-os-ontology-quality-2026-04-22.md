# 6-Dimension Ontology Quality Audit — Coupled bra0 Stack

> **Auditor:** Nael (Architect)
> **Date:** 2026-04-22
> **Protocol:** six-dimension ontology quality framework (Accuracy · Completeness · Conciseness · Adaptability · Clarity · Consistency)
> **Scope:** the **coupled TBox** of the 5 bra0 ontology layers — not each file in isolation.
>    `bra0-stack.ttl` imports: Essence Kernel + ASC + Evidence Ontology + EDGY (+ BFO transitively).
> **Evidence commits:** 2dbe924 + b37da4e + 5b5ce32 (post P0-6, P0-10, stack, decision memo).
> **Session driver:** `worksheet-onto-llm-evo-asc-2026-04-22.md` — Slot F.
> **Complements:** file-level audit of site-docs isolated files (17/17 PASS).
> **Tool:** `rudof shacl-validate -s shapes-coupled.ttl <coupled files>`.

---

## Summary

| Dim | Verdict | Severity | Evidence path |
|-----|---------|----------|---------------|
| 1. Accuracy | **CONDITIONAL** | Medium | `edgy:People ⊏ BFO_0000040` conflict with aggregate semantics (audit challenge-ontoledgy-v1-rigor-audit-2026-04-22.md) |
| 2. Completeness | **CONDITIONAL** | Medium | P0-2 (3-Story) leaves a coverage gap at the cross-layer boundary; arbitration-pending |
| 3. Conciseness | **CONDITIONAL** | Low | `asc:AgentService` carries 3 parents (P0-7); `evo:ComplianceFramework` 2 parents (P0-8) — defence text missing |
| 4. Adaptability | **PASS** | — | `owl:versionIRI` now on both asc: (0.4.0) and evo: (0.1.0); stack 0.1.0 |
| 5. Clarity | **CONDITIONAL** | Low | License block missing on evo: and edgy: headers (P0-9); bilingual parity PASS |
| 6. Consistency | **PASS** | — | Coupled rudof floor 50 held across all 6 P0 commits; no new violations introduced by P0-1/3/4/5/6/10 |

**Overall:** **CONDITIONAL PASS** — the coupled stack is stable and reviewer-readable, but four arbitrations are needed to lift the four CONDITIONAL dimensions to PASS. None of the CONDITIONAL items is parse-breaking or ABox-breaking. Ratchet floor held at 50 violations on coupled rudof run — all on evoQ / edcc-csrd prototype shapes, orthogonal to the reviewer-facing surface.

---

## Dimension 1 — Accuracy

> "The ontology reflects its domain faithfully; no class, property, or alignment misrepresents reality."

### Evidence

- **PASS** at asc: level — BFO grounding is coherent (`Holon ⊏ MaterialEntity`, `HolonicMembrane ⊏ GDC`, `Mandate ⊏ HolonicMembrane`); disjointness axioms added today (P0-6) prevent the worst cross-category mistypings.
- **PASS** at evo: level — every class grounded via `asc:Holon` or `prov:Entity`/`prov:Activity`; `evo:declaredContext rdfs:range sd:NamedGraph` (P0-4) gives the reasoner something to check.
- **CONDITIONAL** at edgy: level — `edgy:People ⊏ BFO:0000040` (material entity) is ontologically imprecise when `edgy:People` denotes an aggregate. BFO has `BFO:0000027` (object aggregate) and `BFO:0000030` (object) as more precise anchors. Audited in `challenge-ontoledgy-v1-rigor-audit-2026-04-22.md` under R-? Accuracy.
- **PASS** at essence kernel level — states-as-individuals, areas-as-individuals, all properties with domain/range (C1-C6 ontology-engineering fixes already applied at creation time per `essence-kernel.ttl` header).

### Gap
The conflict on `edgy:People` BFO typing propagates to the coupled stack because `edgy:` is imported. An external reviewer working through `ontoledgy-bfo-alignment.ttl` will land on this. Remediation item **R-? (BFO-People)** in the EDGY audit.

### Verdict
**CONDITIONAL** — stack Accuracy is held back by the one EDGY typing call. Does not block today; must be resolved before external publication.

---

## Dimension 2 — Completeness

> "Every intended concept and relation is expressed; CQs have a path in the TBox."

### Evidence

- 17/17 CQs answerable on fixtures (Slot B deliverable). Matrix at `_bmad/work/onto-articulation-2026-04-22/cq-matrix.md`.
- P0-1 closes the evo:→asc: import gap (earlier evo: could not reference asc:Mandate without dangling prefix).
- P0-3 declares `evo:byAgentService` and `evo:underMandate` in the TBox; previously only in fixtures. CQ-X-1 now TBox-grounded, not just ABox-answerable.
- P0-4 gives `evo:declaredContext` a range; CQ-evo-4 is shape-enforceable.
- P0-10 adds the inverse pair; SPARQL traversals in either direction are reasoner-supported.

### Gap
- **P0-2 (3-Story articulation):** at the coupled boundary, a single `?s a Story` query can't aggregate `edgy:Story ∪ asc:Story ∪ evo:UserStory` without explicit UNION. Three distinct Story classes with no formal relation = cross-layer coverage gap. Arbitration-pending per decision memo.
- **P0-7/8:** multi-parent defence prose absent; reasoner completeness PASS, documentation completeness CONDITIONAL.

### Verdict
**CONDITIONAL** — lifts to PASS once P0-2 is arbitrated.

---

## Dimension 3 — Conciseness

> "Reuse before invent; no class exists that a W3C/enterprise standard already provides."

### Evidence

- bra0-stack.ttl itself declares zero classes/properties/individuals — an exemplary meta-file.
- evo: header now declares `vann:preferredNamespacePrefix` / `Uri` (P0-1) — MIROs-compliant.
- asc: imports from PROV-O, ODRL, DCAT, DID (per catalogue line 429); doesn't re-invent.
- evo: imports PROV-O, SKOS, DCAT, ODRL, SOSA, SPARQL-SD (post P0-4); imports ASC for agent attribution (post P0-1).
- EDGY reuses SKOS, FOAF; aligns with BFO via `ontoledgy-bfo-alignment.ttl` (18 mappings).

### Gap
- `asc:AgentService` has **3 parents** (`prov:SoftwareAgent, dcat:DataService, asc:Holon`). Defensible but needs an explicit comment block. Arbitration in decision memo (O1/O2/O3).
- `evo:ComplianceFramework` has **2 parents** (`skos:ConceptScheme, asc:Holon`). Same treatment.

### Verdict
**CONDITIONAL** — lifts to PASS after P0-7 and P0-8 are resolved and each multi-parent class carries a 1-paragraph defence in its `rdfs:comment`.

---

## Dimension 4 — Adaptability

> "Layers evolve at independent cadences without breaking their contracts."

### Evidence

- `owl:versionIRI` on asc: (0.4.0) and evo: (0.1.0) (P0-5).
- `owl:versionIRI` on bra0-stack (0.1.0).
- Namespace canon respected: `schema.bra0.org/*` for agent governance; `schema.bra0.org/*` for product vocabularies (CLAUDE.md).
- Stack file is meta-only; changing a layer version doesn't require changing the stack file (unless the import IRI changes).
- Disjointness + inverseOf (P0-6/P0-10) are **forward-compatible** — they add TBox invariants without breaking any existing ABox or SPARQL.

### Gap
None at stack level.

### Verdict
**PASS**.

---

## Dimension 5 — Clarity

> "Every term is readable by a stranger — `rdfs:label` + `rdfs:comment` in target languages; licence and provenance visible."

### Evidence

- Every class in asc:, evo:, edgy:, ess: carries `rdfs:label` + `rdfs:comment`; bilingual (en/fr) on most (spot-check PASS).
- Bilingual parity: PASS (label/comment `@fr` + `@en` on user-facing classes).

### Gap
- `dct:license` declared only on asc: (CC BY-SA 4.0). evo: and edgy: have no `dct:license` in the header. Until P0-9 is arbitrated, the stack has **inconsistent licence visibility**.
- Stack meta-file header has no `dct:license` yet either (will inherit from the decision).

### Verdict
**CONDITIONAL** — lifts to PASS after P0-9 decision and propagation to the three headers.

---

## Dimension 6 — Consistency

> "The stack does not contradict itself; rudof coupled validation floor held across all edits."

### Evidence

- rudof coupled floor: **50 violations held constant** across 6 P0 commits (e919333 → 2dbe924) and the stack commit (b37da4e).
- No new ABox. No new class. No new domain/range conflicts introduced.
- The 50 baseline violations are all on `evoQ:GroundingResult` / `edcc-csrd` prototype shapes — orthogonal to the reviewer-facing surface (ess:/asc:/evo:/edgy:/stack). These exist because the shape bundle is authored ahead of the reference ABox.
- OWL-level consistency (disjointness axioms P0-6) checked manually against existing `rdfs:subClassOf` chains; none violated.
- Cross-layer consistency: evo: imports asc:, asc: does NOT import evo: (correct directionality; no cycle).

### Gap
None at coupled-stack scope.

### Verdict
**PASS**.

---

## Cross-audit cross-reference

| Item | File-level audit (2026-04-20) | Coupled audit (today) |
|---|---|---|
| `asc:Story ↔ evo:UserStory` | Noted as "future `rdfs:seeAlso`" observation | Elevated to P0-2 arbitration (adds `edgy:Story` as third vertex) |
| `evo:dashboard*` predicates | Fixed 2026-04-20 (added 8 predicates) | Confirmed still declared, not regressed |
| `rdf:langString` prefix | Fixed 2026-04-20 at line 633 | Not regressed |
| `owl:versionIRI` on asc:/evo: | Not in scope | NEW: added today (P0-5) |
| Disjointness axioms | Not in scope | NEW: added today (P0-6, 5 pairs on asc:) |
| Inverse properties | Not in scope | NEW: added today (P0-10, one pair on asc:) |
| `owl:imports asc:` from evo: | Not in scope | NEW: added today (P0-1) |
| `evo:byAgentService`, `evo:underMandate` TBox | Listed as "fixture-only predicates" | NEW: declared in TBox today (P0-3) |
| `evo:declaredContext` range | Listed as "no range, acceptable" | NEW: ranged to `sd:NamedGraph` today (P0-4) |

Nine items tightened since 2026-04-20. Each one a committed ratchet.

---

## Recommendation to Sacha

The coupled stack would be **reviewer-presentable** once the four CONDITIONAL dimensions lift to PASS, which requires exactly the four arbitration answers from the decision memo:

| Memo item | Lifts dimension | Commit cost (post-decision) |
|---|---|---|
| P0-2 (3-Story) | Completeness | 1 commit on stack + optional alignment file |
| P0-7 (AgentService parents) | Conciseness | 1 commit on asc: |
| P0-8 (ComplianceFramework parents) | Conciseness | 1 commit on evo: |
| P0-9 (license unification) | Clarity | 1 commit across 3 files (evo:, edgy:, stack:) |

No new rudof shape, no new fixture, no new ontology file required. Estimated delta: 4 small commits, 50/50 floor held, stack uplifted from CONDITIONAL PASS to full PASS.

---

## Annex — commands used

```bash
# Coupled TBox-only ratchet check (ran after every P0 commit today)
rudof shacl-validate \
  -s shapes-coupled.ttl \
  ontologies/bra0-stack.ttl \
  ontologies/governance/agent-service-contract.ttl \
  ontologies/governance/evidence-os/evidence-os.ttl \
  2>&1 | grep -c "shacl#Violation"
# => 50 (held)

# TBox parse sanity (stack file alone, imports resolved locally)
rudof shacl-validate \
  -s shapes-coupled.ttl \
  ontologies/bra0-stack.ttl
# => parses clean; violations all on evoQ prototype (orthogonal)
```

Audit closed by Nael 2026-04-22.
