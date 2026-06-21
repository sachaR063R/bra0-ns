# 6-Dimension Ontology Quality Audit — Capability Operations (`cap:`)

> **Auditor:** Quinn (QA) + Nael (Architect) — concerted
> **Date:** 2026-06-21
> **Protocol:** Keet 6-dim quality framework — see `_bmad/docs/ontology-quality-audit-grid-keet-6dim.md`
> **Context:** ADR-132 §3.1 re-audit sub-phase (C-R2b STALE-AUDIT cohort) under ADR-134 audit-staleness pinning. Re-audit of the 2026-04-20 PASS (Nael), now stale: source bumped to **0.2.6** (modified 2026-06-06).
> **Scope:** `ontologies/capabilities/capability-operations.ttl` (840 triples, 10 classes / 87 capability individuals across GOV/SL/DP/TP/NS families / 9 object + 9 datatype properties) + `capability-operations.shapes.ttl` (198 triples) + BFO sidecar `capability-operations-bfo-2020.ttl` (9 grounding axioms). Lattice-operation classes (Add/Specialize/Lift/DemoteMerge) sealed ADR-065. Layer L1 (capability spine).
> **Imports:** edgy (upper alignment), BFO 2020 (via sidecar), SKOS, SHACL.
> **Tools:** `rapper -i turtle -c` + `rudof shacl-validate` (rudof 0.2.8) + `git hash-object`.
> **Audit pin (ADR-134):** TBox `git hash-object` = `732569ba5ef4149177d1f5150b420d0535a3d037`. Prior audited blob (2026-04-20) = `cf2a117ad2e77213a16b91534935ca9c594765c5` — **distinct**, confirming the STALE-AUDIT premise.
> **Companion audits:** `agent-service-contract-ontology-quality-audit-2026-06-21.md`, `evidence-os-ontology-quality-2026-04-22.md`.

---

## Summary

| Dim | Verdict | Severity | Evidence |
|-----|---------|----------|----------|
| 1. Accuracy        | PASS                  | —          | BFO grounding via sidecar (9 axioms); GOV/SL/DP/TP/NS family partition faithful; descriptive-leaf subsumption doctrine honoured |
| 2. Completeness    | PASS                  | —          | 87 capability individuals; lattice-operation classes (Add/Specialize/Lift/DemoteMerge) sealed ADR-065 |
| 3. Conciseness     | PASS                  | —          | descriptive-leaf subsumption (no rename); reuses edgy/BFO; bridged to asc via `asc:Capability ≡ cap:Capability` (ADR-098) |
| 4. Adaptability    | PASS-WITH-1-WARNING   | sh:Warning | versionInfo + created + modified present; **W2** = no `.shex` companion (§3.8) → AUDITED ceiling |
| 5. Clarity         | PASS                  | —          | strong skos: 72 prefLabel / 41 definition / 74 comment / CC BY-SA license; scopeNote sparse (1) |
| 6. Consistency     | PASS-WITH-1-WARNING   | sh:Warning | rudof 0 Violations after **W1** severity correction; 24 documented Warnings (operations-completeness, lift trigger W13) |

**Overall: PASS-WITH-2-WARNINGS.** cap 0.2.6 is faithfully grounded, strongly documented, and rudof-clean once the aspirational completeness shape carries its intended `sh:Warning` severity. The two warnings — W1 operations-completeness (24, → W13) and W2 `.shex` parity debt (§3.8) — are tracked, non-blocking. Re-pinned to current content-hash `732569ba`, replacing the stale 2026-04-20 pointer.

---

## Dimension 1 — Accuracy
> "The ontology reflects its domain faithfully; no class, property, or alignment misrepresents reality."
### Evidence
- BFO 2020 grounding mediated through the sidecar `capability-operations-bfo-2020.ttl` (9 axioms); capabilities ground as `bfo:Disposition` per the grid §3.7 common-landing table.
- The GOV / SL / DP / TP / NS family partition (`cap:family sh:in (…)`) represents the capability domain faithfully; lattice operations model edit primitives (ADR-065/070).
- `asc:Capability ≡ cap:Capability` bridge (ADR-098) keeps the agent-side and registry-side capability concept identical.
### Gap
- None material; sidecar grounding is documented mediation (same pattern as asc).
### Verdict
**PASS** — domain faithfully represented; BFO grounding present via sidecar.

## Dimension 2 — Completeness
> "Every intended concept and relation is expressed; CQs have a path in the TBox."
### Evidence
- 87 capability individuals span all five families; 10 classes include the four lattice-operation classes sealed under ADR-065.
- Edit-primitive coverage (Add / Specialize / Lift / DemoteMerge) gives the spine its malleable-lifecycle operations (ADR-070).
### Gap
- None blocking.
### Verdict
**PASS** — concept and operation coverage complete for the capability spine.

## Dimension 3 — Conciseness
> "Reuse before invent; no class exists that a W3C/enterprise standard already provides."
### Evidence
- Descriptive-leaf subsumption doctrine: 60 descriptive leaves subsume to 39 α′ canonical capabilities rather than being renamed/duplicated.
- `owl:equivalentClass` bridge to `asc:Capability` over duplication; upper reuse via edgy/BFO.
### Gap
- None.
### Verdict
**PASS** — reuse-before-invent honoured; descriptive leaves subsume, not multiply.

## Dimension 4 — Adaptability
> "Layers evolve at independent cadences without breaking their contracts."
### Evidence
- Versioning complete: `owl:versionInfo "0.2.6"`, `dct:created "2026-04-20"`, `dct:modified "2026-06-06"`.
- Two-tier shape contract: `CapabilityOperationsShape` (structural, `minCount 0`) + `CompleteCapabilityOperationsShape` (aspirational, `minCount 1`) — a deliberate now-vs-roadmap separation (Nael).
### Gap (documented — W2)
- No `.shex` companion (§3.8 ShEx + SHACL parity). This caps cap at the AUDITED ceiling; promotion beyond AUDITED is blocked until the ShEx schema lands and parity passes. Recorded as a named CONDITIONAL-to-PASS lift item, not a publication blocker for the AUDITED badge.
### Verdict
**PASS-WITH-1-WARNING (W2)** — versioning sound; `.shex` parity debt tracked.

## Dimension 5 — Clarity
> "Every term is readable by a stranger — labels, definitions, scope notes, license, provenance."
### Evidence
- `dct:license` CC BY-SA 4.0 present.
- Strong 5-layer lexical: 72 `skos:prefLabel`, 41 `skos:definition`, 74 `rdfs:comment`, 30 `rdfs:label` — materially stronger skos coverage than asc.
### Gap
- `skos:scopeNote` sparse (1 occurrence); usage guidance could be richer. Minor; does not lower the verdict.
### Verdict
**PASS** — readable; skos definitions present on the bulk of signifying entities.

## Dimension 6 — Consistency
> "The ontology does not contradict itself; rudof validation passes."
### Evidence
- `rapper -i turtle -c`: TBox 840 triples, shapes 198 triples — both parse clean.
- `rudof shacl-validate` (with BFO sidecar) → **0 Violations, 24 Warnings** after the W1 severity correction.
### Gap (documented — W1)
- Before this re-audit, `cap:CompleteCapabilityOperationsShape` carried **no `sh:severity`** on its three operation properties (`hasInterface`/`hasSparqlOperation`/`hasCliOperation` `minCount 1`), so they defaulted to `sh:Violation` and produced 24 false-red Violations — contradicting the shape's own header intent ("informational at first… blocker at W13"). Corrected in this re-audit: the three properties now carry `sh:severity sh:Warning` with a §3.5 lift-trigger note (promote to `sh:Violation` at W13 for Evidence-OS-V1-relevant capabilities; descriptive leaves exempt). The 24 operations-completeness gaps persist as visible, tracked Warnings.
### Verdict
**PASS-WITH-1-WARNING (W1)** — rudof-clean (0 Violations); 24 operations-completeness Warnings tracked to W13.

---

## Cross-audit reinforcement
### Matrix A — this audit strengthens `agent-service-contract-ontology-quality-audit-2026-06-21.md`
| Prior item | This audit's contribution | Strengthening effect |
|---|---|---|
| asc W2 silent-Warning severity fix | cap W1 applies the same §3.5 severity discipline at gate-reddening scale | Confirms the severity-declaration discipline as a cross-TBox invariant: undeclared severity is a defect whether it under- (asc) or over- (cap) reports |

### Matrix B — `agent-service-contract-…-2026-06-21.md` strengthens this audit
| Prior ratchet | This audit's inheritance | Strengthening effect |
|---|---|---|
| asc `≡ cap:Capability` bridge (ADR-098) | cap inherits the bridge as a Conciseness asset | The bridge that keeps asc concise also keeps cap concise — bidirectional reuse confirmed |

### Joint invariants confirmed binding
- §3.5 Cardinality + lift trigger (undeclared severity is a defect — now satisfied on cap).
- §3.6 rudof-clean publication gate (0 Violations, Warnings permitted with §3.5 documentation).
- §3.7 BFO grounding systematic (satisfied via sidecar).
- §3.8 ShEx + SHACL parity (NOT met — `.shex` absent → AUDITED ceiling).

---

## Recommendation

cap 0.2.6 is **AUDITED-eligible at PASS-WITH-2-WARNINGS**. The artifact is rudof-clean once the aspirational completeness shape carries its intended `sh:Warning` severity (W1), and the `.shex` parity gap (W2, §3.8) holds it at the AUDITED ceiling. Per ADR-134, re-pin to the current TBox content-hash `732569ba…`, replacing the stale 2026-04-20 pointer to `cf2a117a`.

**Promotion roadmap:**
| To version | Trigger | Effect |
|---|---|---|
| W13 cycle gate | every non-descriptive-leaf Evidence-OS-V1 capability carries the three operation handles | Promotes the 24 Warnings to Violations, clears W1 → Dimension 6 to PASS |
| (parity) | author `capability-operations.shex` + parity check passes | Clears W2 (§3.8) → Dimension 4 to PASS; lifts the AUDITED ceiling |
| both cleared | — | Overall PASS; eligible for higher maturity |

**Whitelist line proposal** (HTML doc gate, `ontologies/docs-published.txt` — Sacha-only edit):
```
ontologies/capabilities/capability-operations.ttl  2026-06-21  PASS-WITH-2-WARNINGS  Quinn+Nael  # re-audit at 0.2.6, pin 732569ba (ADR-134)
```

**Registry line proposal** (IRI gate, `bra0-ns/docs-published.txt` — Sacha-only edit):
```
capability/capability-operations.ttl;Audited;audit/capability-operations-ontology-quality-audit-2026-06-21.md;2026-06-21
```

---

## Annex — commands used
```bash
git hash-object ontologies/capabilities/capability-operations.ttl
#   => 732569ba5ef4149177d1f5150b420d0535a3d037   (current — new pin)
git ls-tree -r <commit@2026-04-20> -- …/capability-operations.ttl
#   => cf2a117ad2e77213a16b91534935ca9c594765c5   (prior audited blob — distinct → STALE-AUDIT confirmed)

rapper -i turtle -c ontologies/capabilities/capability-operations.ttl          # => 840 triples, clean
rapper -i turtle -c ontologies/capabilities/capability-operations.shapes.ttl   # => 198 triples, clean
rudof shacl-validate \
  -s ontologies/capabilities/capability-operations.shapes.ttl \
  ontologies/capabilities/capability-operations.ttl \
  ontologies/capabilities/capability-operations-bfo-2020.ttl
#   before W1 fix => 24 Violations ; after W1 fix => 0 Violations, 24 Warnings
```

Audit closed 2026-06-21 — ADR-132 §3.1 re-audit sub-phase (C-R2b), ADR-134 content-hash pin. Quinn (QA) + Nael (Architect), concerted.
