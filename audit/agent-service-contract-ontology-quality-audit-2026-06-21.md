# 6-Dimension Ontology Quality Audit — Agent Service Contract (`asc:`)

> **Auditor:** Quinn (QA) — foundational co-sign Noam (Scientific Director)
> **Date:** 2026-06-21
> **Protocol:** Keet 6-dim quality framework — see `_bmad/docs/ontology-quality-audit-grid-keet-6dim.md`
> **Context:** ADR-132 §3.1 re-audit sub-phase (C-R2b STALE-AUDIT cohort) under ADR-134 audit-staleness pinning. Re-audit of the 2026-04-20 PASS (Nael), now stale: source bumped 0.4.0 → **0.10.0** (modified 2026-05-23).
> **Scope:** `ontologies/governance/agent-service-contract.ttl` (756 triples, 29 classes / 36 object + 61 datatype properties) + `agent-service-contract.shapes.ttl` (538 triples) + `agent-service-contract.shex` + BFO sidecar `agent-service-contract-bfo-2020.ttl` (42 grounding axioms). Layer L1 (governance TBox).
> **Imports:** `https://schema.bra0.org/cross-domain/edgy#` (TBox header); PROV-O, DCAT, ODRL, SKOS, SHACL, BFO 2020 (vocabulary reuse).
> **Tools:** `rapper -i turtle -c` + `rudof shacl-validate` (rudof 0.2.8) + `git hash-object`.
> **Audit pin (ADR-134):** TBox `git hash-object` = `f8d4dd4142196e71eecdce06658b3d3880019975`. Prior audited blob (2026-04-20) = `02b177d4a7974dd46e5a55c07fdf911ce6f2048b` — **distinct**, confirming the STALE-AUDIT premise that triggered this re-audit.
> **Companion audits:** `evidence-os-ontology-quality-2026-04-22.md`, `motivation-registry-quality-2026-04-28.md`.

---

## Summary

| Dim | Verdict | Severity | Evidence |
|-----|---------|----------|----------|
| 1. Accuracy        | PASS                  | —          | BFO grounding mediated (sidecar + transitive PROV-O/DCAT parents), documented; `asc:Capability ≡ cap:Capability` bridge (ADR-098) defensible |
| 2. Completeness    | PASS                  | —          | 29 classes / 36+61 props; 0.4→0.10 additions (`Realization`, `provenLevel`, `PostExternal`, P15 capability-first facet) all carry label+comment; 7 CQs |
| 3. Conciseness     | PASS                  | —          | `equivalentClass` bridge over duplication; reuses PROV-O/DCAT/ODRL/edgy, no reinvention |
| 4. Adaptability    | PASS-WITH-1-WARNING   | sh:Warning | versionInfo + versionIRI + `dct:modified`; 25 `sh:severity` (23 Violation / 2 Warning) — Warnings now carry §3.5 lift-trigger notes (**W2**) |
| 5. Clarity         | PASS-WITH-1-WARNING   | sh:Warning | 2 of 5 lexical layers (`rdfs:label` bilingual + rich `rdfs:comment`); skos layers absent, substance inline in comment (**W1**) |
| 6. Consistency     | PASS                  | —          | rudof 0 violations; rapper clean (756 / 538 triples) |

**Overall: PASS-WITH-2-WARNINGS.** asc 0.10.0 is structurally sound, rudof-clean, and faithfully grounded; the two warnings (W1 skos enrichment, W2 silent-Warning lift triggers) are documented in the shapes file with a named lift trigger at v0.11. Re-pinned to current content-hash `f8d4dd41`. The verdict re-attests the current artifact honestly per ADR-134 rather than carrying the stale 2026-04-20 pointer.

---

## Dimension 1 — Accuracy
> "The ontology reflects its domain faithfully; no class, property, or alignment misrepresents reality."
### Evidence
- BFO 2020 grounding is **mediated, not absent**: the sidecar `agent-service-contract-bfo-2020.ttl` carries 42 grounding axioms, and core classes inherit BFO ancestry transitively through their declared parents (`asc:AgentService rdfs:subClassOf prov:SoftwareAgent, dcat:DataService`; `asc:InputDefence` typed `prov:Plan ⊏ … ⊏ bfo:0000031`, stated in `rdfs:comment`).
- The `asc:Capability ≡ cap:Capability` `owl:equivalentClass` bridge (ADR-098, P1 staged convergence) is documented with its P2 retirement plan; it represents the domain (agent capability = registered capability) faithfully without forcing a premature merge.
### Gap
- Direct `rdfs:subClassOf bfo:*` axioms are absent from the main TBox (grounding is externalised to the sidecar + transitive). Defensible under the grid's mediated-grounding allowance; flagged here for traceability, not as a failure.
### Verdict
**PASS** — domain faithfully represented; BFO grounding present via documented mediation.

## Dimension 2 — Completeness
> "Every intended concept and relation is expressed; CQs have a path in the TBox."
### Evidence
- 29 classes, 36 object + 61 datatype properties cover the governed-agent surface (service, capability, mandate, policy, gating, I/O shapes, external-engagement boundary, realization).
- The 0.4.0 → 0.10.0 growth materialised real governance capability: `asc:Realization` + `asc:provenLevel` (v0.10.0), `asc:PostExternal` + `externalEngagementMode` (v0.9.0 / ADR-110), `asc:hasOutputShape` (v0.7.0 / ADR-093), P15 capability-first enforcement facet — each with label + comment.
- 7 competency questions enumerated in the workbook (`experiments/asc-ontology-quality-audit-workbook.md` §2) with SPARQL answer patterns.
### Gap
- CQ file is the in-repo workbook rather than a dedicated `agent-service-contract-cqs.md` companion (§3.9). Documented; does not block AUDITED.
### Verdict
**PASS** — concept coverage complete for the governance domain; CQ paths exist.

## Dimension 3 — Conciseness
> "Reuse before invent; no class exists that a W3C/enterprise standard already provides."
### Evidence
- Agents reuse `prov:SoftwareAgent`; services reuse `dcat:DataService`; permissions reuse `odrl:`; provenance reuse `prov:qualifiedAssociation`; upper alignment reuses `edgy:`.
- The capability concept is **bridged** (`owl:equivalentClass cap:Capability`) rather than duplicated — the canonical P1-Least-Power move.
### Gap
- None.
### Verdict
**PASS** — reuse-before-invent honoured throughout; no redundant class.

## Dimension 4 — Adaptability
> "Layers evolve at independent cadences without breaking their contracts."
### Evidence
- Versioning complete: `owl:versionInfo "0.10.0"`, `owl:versionIRI`, `dct:created` + `dct:modified "2026-05-23"`.
- 25 `sh:severity` declarations (23 `sh:Violation`, 2 `sh:Warning`); the two Warnings (`CollaborationShape` / `prov:qualifiedAssociation`, `TemporalValidityShape` / `asc:reviewDate`) now carry **§3.5 lift-trigger notes** naming v0.11 and the coverage precondition (**warning W2**, applied in this re-audit).
- Refactor history shows contract-preserving evolution (holonic apparatus removed under ADR-052; `asc:Story` → `edgy:Task` under ADR-052/053).
### Gap (documented — W2)
- Before this re-audit the 2 Warnings were silent (no lift trigger), a §3.5 violation. Fixed in-band; tracked to promotion at v0.11.
### Verdict
**PASS-WITH-1-WARNING (W2)** — versioning and severity discipline sound; silent-Warning gap closed with a named lift trigger.

## Dimension 5 — Clarity
> "Every term is readable by a stranger — labels, definitions, scope notes, license, provenance."
### Evidence
- `dct:license` CC BY-SA 4.0 present; `dct:creator` + `dct:created`/`dct:modified` present.
- 153 `rdfs:label` (bilingual en/fr) + 143 `rdfs:comment` — every signifying class and major property carries a bilingual label and a rich, reference-bearing comment whose text supplies genus + differentia inline.
### Gap (documented — W1)
- The 5-layer lexical discipline (grid §3.2) is met on **2 of 5 layers**: `skos:prefLabel`, `skos:definition`, and `skos:scopeNote` are absent (0 occurrences). The definitional substance exists but lives inside `rdfs:comment` rather than in machine-addressable skos triples. This is a *standard-elevation* gap: §3.2 was ratified 2026-04-28, after asc's 2026-04-20 PASS. Documented as **warning W1** in the shapes-file header with lift trigger v0.11 (land `skos:definition` on 100% of signifying classes + add a live `SkosDefinitionShape`).
### Verdict
**PASS-WITH-1-WARNING (W1)** — readable to a stranger today via bilingual labels + rich comments; skos enrichment warning-tracked to v0.11, not blocking.

## Dimension 6 — Consistency
> "The ontology does not contradict itself; rudof validation passes."
### Evidence
- `rapper -i turtle -c`: TBox 756 triples, shapes 538 triples — both parse clean.
- `rudof shacl-validate -s …shapes.ttl all-agents.ttl …agent-service-contract.ttl` → **No Errors found** (0 violations).
- 23 `sh:Violation` shapes actively enforce the agent contract (agentType, temporal validity, human reviewer, collaboration).
### Gap
- None.
### Verdict
**PASS** — rudof-clean; no internal contradiction.

---

## Cross-audit reinforcement
### Matrix A — this audit strengthens `evidence-os-ontology-quality-2026-04-22.md`
| Prior item | This audit's contribution | Strengthening effect |
|---|---|---|
| evidence-os Severity convention (§3.5 genesis) | asc §3.5 lift-trigger notes applied to its 2 silent Warnings | Confirms the lift-trigger discipline holds on a second governance TBox |

### Matrix B — `motivation-registry-quality-2026-04-28.md` strengthens this audit
| Prior ratchet | This audit's inheritance | Strengthening effect |
|---|---|---|
| 5-layer lexical formalised (§3.2) | asc Clarity measured against the 5-layer bar; gap surfaced as W1 | The motivation-registry bar is what made asc's skos gap visible — cumulative audit knowledge |

### Joint invariants confirmed binding
- §3.1 License visibility (asc carries CC BY-SA 4.0).
- §3.5 Cardinality + lift trigger (now satisfied on all asc Warnings).
- §3.6 rudof-clean publication gate (0 violations).
- §3.7 BFO grounding systematic (satisfied via documented mediation).

---

## Recommendation

asc 0.10.0 is **AUDITED-eligible at PASS-WITH-2-WARNINGS**. The artifact is rudof-clean, faithfully grounded, and the two warnings are documented in the shapes file with a named lift trigger at v0.11. Per ADR-134, re-pin the audit to the current TBox content-hash `f8d4dd41…` so the pointer attests the artifact actually shipped, replacing the stale 2026-04-20 pointer to `02b177d4`.

**Promotion roadmap:**
| To version | Trigger | Effect |
|---|---|---|
| v0.11 | `skos:definition` (genus + differentia) on 100% of signifying classes + live `SkosDefinitionShape` | Clears W1 → Dimension 5 to PASS |
| v0.11 | every governed agent carries `prov:qualifiedAssociation`; every Mandate carries `asc:reviewDate` | Promotes the 2 Warnings to Violations, clears W2 → Dimension 4 to PASS |
| v0.11 (both cleared) | — | Overall PASS; eligible for omat:Published re-confirmation |

**Whitelist line proposal** (HTML doc gate, `ontologies/docs-published.txt` — Sacha-only edit):
```
ontologies/governance/agent-service-contract.ttl  2026-06-21  PASS-WITH-2-WARNINGS  Quinn  # re-audit at 0.10.0, pin f8d4dd41 (ADR-134)
```

**Registry line proposal** (IRI gate, `bra0-ns/docs-published.txt` — Sacha-only edit; asc is foundational governance, IRI-resolved):
```
agent-service-contract.ttl;Audited;audit/agent-service-contract-ontology-quality-audit-2026-06-21.md;2026-06-21
```

---

## Annex — commands used
```bash
git hash-object ontologies/governance/agent-service-contract.ttl
#   => f8d4dd4142196e71eecdce06658b3d3880019975   (current — new pin)
git ls-tree -r <commit@2026-04-20> -- …/agent-service-contract.ttl
#   => 02b177d4a7974dd46e5a55c07fdf911ce6f2048b   (prior audited blob — distinct → STALE-AUDIT confirmed)

rapper -i turtle -c ontologies/governance/agent-service-contract.ttl          # => 756 triples, clean
rapper -i turtle -c ontologies/governance/agent-service-contract.shapes.ttl   # => 538 triples, clean
rudof shacl-validate \
  -s ontologies/governance/agent-service-contract.shapes.ttl \
  ontologies/governance/agents/all-agents.ttl \
  ontologies/governance/agent-service-contract.ttl                            # => No Errors found
```

Audit closed 2026-06-21 — ADR-132 §3.1 re-audit sub-phase (C-R2b), ADR-134 content-hash pin. Quinn (QA) + Noam (foundational co-sign).
