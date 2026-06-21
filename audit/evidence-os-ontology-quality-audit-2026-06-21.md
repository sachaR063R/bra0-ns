# 6-Dimension Ontology Quality Audit — Evidence OS (`evo:` + `evoQ:`)

> **Auditor:** Quinn (QA) + Nael (Architect) — concerted
> **Date:** 2026-06-21
> **Protocol:** Keet 6-dim quality framework — see `_bmad/docs/ontology-quality-audit-grid-keet-6dim.md`
> **Context:** ADR-132 §3.1 re-audit sub-phase (C-R2b STALE-AUDIT cohort) under ADR-134 audit-staleness pinning. Re-audit of the 2026-04-22 DRAFT, now stale: §3.7 BFO grounding + §3.8 ShEx/SHACL parity were ratified as Sacha invariants on **2026-04-28**, *after* the original audit — so neither invariant was ever tested against Evidence OS.
> **Scope (C-R2b evo + evoQ cohort):**
> - `ontologies/governance/evidence-os/evidence-os.ttl` (213 triples, 12 classes / 24 properties) + new BFO alignment sidecar `evidence-os-bfo-2020.ttl` (23 triples, 12 grounding axioms)
> - shapes: `evo-story.shapes.ttl` (37), `evo-change-pipeline.shapes.ttl` (96), `evo-test-evidence.shapes.ttl` (90), `evo-ambient-agent-policy.shapes.ttl` (47)
> - query result-structure shapes: `evoQ-kpi-shapes.shapes.ttl` (403 triples, 16 result shapes)
> - Excludes the EDCC extension files (`edcc-*`), separately tracked at DRAFT.
> **Imports:** PROV-O, SKOS, DCAT, ODRL, SOSA, SPARQL-SD (native W3C uppers); BFO 2020 + IAO (via sidecar).
> **Tools:** `rapper -i turtle -c` + `rudof shacl-validate` (rudof 0.2.8) + `git hash-object`.
> **Audit pins (ADR-134, content-hash):**
> | Artifact | Audited blob (this audit) | Prior audited blob (2026-04-20/22) | Delta |
> |---|---|---|---|
> | `evidence-os.ttl` | `5d9e33928cd192524bbfb4f5fcc0a47e7aa61a30` | `300eedb88db73310f94b393985d4924d4516b0c8` | STALE |
> | `evoQ-kpi-shapes.shapes.ttl` | `e0d6160dccda5598486be178e9be24b6d0076d79` | `cfa85b8d9e7a5fa977e462b826c9fc7656e08308` | STALE |
> | `evidence-os-bfo-2020.ttl` | `9ec9ab0b308ace3fe4572887dbc3c8009df2f145` | — (new this re-audit) | NEW |
> | `evo-ambient-agent-policy.shapes.ttl` | `991a9eb9e2201b41d2ff38151a171582a25398f5` | (re-encoded this re-audit) | CHANGED |
> | `evo-story.shapes.ttl` | `6a009a42ce1f4bf35baedd926dc15097d586ca3c` | (§3.5 prose note) | CHANGED |
> | `evo-change-pipeline.shapes.ttl` | `98e69c50c81ed88be588532a10384580e6cef5bd` | (§3.5 prose note) | CHANGED |
> | `evo-test-evidence.shapes.ttl` | `8deb1b704cf1daae0c4c087fa441b13c85365867` | (§3.5 prose note) | CHANGED |
> **Companion audits:** `agent-service-contract-ontology-quality-audit-2026-06-21.md`, `capability-operations-ontology-quality-audit-2026-06-21.md`.

---

## Summary

### evo (evidence-os.ttl + 4 shapes + BFO sidecar)

| Dim | Verdict | Severity | Evidence |
|-----|---------|----------|----------|
| 1. Accuracy        | PASS (via new sidecar) | —          | **§3.7 closed**: `evidence-os-bfo-2020.ttl` grounds all 12 classes (5 prov:Activity → BFO_0000015 process; 7 artifact/concept → IAO_0000030 ICE). Original audit predated the 2026-04-28 BFO invariant. |
| 2. Completeness    | PASS                  | —          | 12 classes + 24 properties; CQ surface (traceability/change-pipeline/test-evidence/ambient-policy) covered by 4 shape families + 16 evoQ result shapes |
| 3. Conciseness     | PASS                  | —          | strict W3C reuse (PROV-O/SKOS/DCAT/ODRL); "no re-statement of PROV-O patterns under evo:"; one surviving top class (evo:Control) |
| 4. Adaptability    | PASS-WITH-1-WARNING   | sh:Warning | versionInfo 0.2.0 + created present; **W2** = no `.shex` companion (§3.8) → AUDITED ceiling |
| 5. Clarity         | PASS-WITH-1-WARNING   | sh:Warning | license CC BY-SA; strong rdfs (35 label / 34 comment); **W1** = skos lexical layer near-absent (1 prefLabel / 0 definition / 0 scopeNote) (§3.2) |
| 6. Consistency     | PASS                  | —          | rudof 0 Violations on all happy-paths; all 4 failure fixtures live (3/3/3/2) after the **dormant-shape re-encode** + **drifted-fixture restore** |

**Overall evo: PASS-WITH-2-WARNINGS.**

### evoQ (evoQ-kpi-shapes.shapes.ttl)

| Dim | Verdict | Severity | Evidence |
|-----|---------|----------|----------|
| 1. Accuracy        | PASS                  | — | result-structure shapes over SPARQL rows; no domain TBox classes → §3.7 N/A |
| 2. Completeness    | PASS                  | — | 16 result shapes cover the KPI query surface |
| 3. Conciseness     | PASS                  | — | reuses evo: + sh:; no reinvention |
| 4. Adaptability    | PASS-WITH-1-WARNING   | sh:Warning | versionInfo 0.2.0; **W2** = no `.shex` → AUDITED ceiling |
| 5. Clarity         | PASS                  | — | license CC BY-SA; label+comment per shape |
| 6. Consistency     | PASS                  | — | rudof 0 Violations on happy-path; failure fixture → 38 Violations (live negative test) |

**Overall evoQ: PASS-WITH-1-WARNING.**

---

## Dimension 1 — Accuracy
> "The ontology reflects its domain faithfully; no class, property, or alignment misrepresents reality."
### Evidence
- **§3.7 gap found and closed.** The original 2026-04-22 audit awarded a DRAFT badge before the BFO-grounding invariant existed (ratified 2026-04-28). At re-audit `evidence-os.ttl` carried **0 BFO references** — a latent §3.7 Accuracy defect ("class without BFO grounding = Accuracy FAIL").
- Remediated via the ADR-064 alignment-file pattern (asc/cap precedent): `evidence-os-bfo-2020.ttl` grounds all 12 classes without polluting the W3C-reuse native TBox. Two load-bearing floors: prov:Activity events → `obo:BFO_0000015` (process); prov:Entity artifacts + skos:Concept/ConceptScheme normative entities → `obo:IAO_0000030` (information content entity).
- Coverage = 12/12 classes (100%); sidecar parses (23 triples), fixtures still validate with the sidecar in the loop.
### Gap
- None material post-sidecar. More-specific BFO/IAO subtypes (planned process, plan specification) are defensible refinements tracked in the sidecar's evolution.
### Verdict
**PASS** — domain faithfully represented; §3.7 BFO grounding now systematic via sidecar.

## Dimension 2 — Completeness
> "Every intended concept and relation is expressed; CQs have a path in the TBox."
### Evidence
- 12 classes span the evidence lifecycle (Control / change pipeline / test evidence / workflow / ambient-agent invocation / compliance framework); 24 properties wire the traceability graph.
- Validation surface: 4 evo shape families (story, change-pipeline, test-evidence, ambient-agent-policy) + 16 evoQ result-structure shapes.
### Verdict
**PASS** — concept and relation coverage complete for the Evidence OS spine.

## Dimension 3 — Conciseness
> "Reuse before invent; no class exists that a W3C/enterprise standard already provides."
### Evidence
- Design doctrine (TBox comment): "W3C reuse before extension (PROV-O, DCAT, SKOS, ODRL, SOSA, SPARQL-SD); no speculative classes (every class justified by ≥2 use cases); no re-statement of PROV-O patterns under evo:".
- One surviving top-level class (evo:Control on skos:Concept); operational classes re-parented directly on PROV-O.
### Verdict
**PASS** — reuse-before-invent strongly honoured.

## Dimension 4 — Adaptability
> "Layers evolve at independent cadences without breaking their contracts."
### Evidence
- Versioning present: `owl:versionInfo "0.2.0"`, `dct:created`, versionIRI on every shape file.
- The BFO sidecar's alignment-file separation lets the BFO upper evolve independently of the W3C-grounded native TBox.
### Gap (documented — W2)
- No `.shex` companion (§3.8 ShEx + SHACL parity). Caps both evo and evoQ at the AUDITED ceiling; promotion beyond AUDITED is blocked until the ShEx schema lands and parity passes.
### Verdict
**PASS-WITH-1-WARNING (W2)** — versioning sound; `.shex` parity debt tracked.

## Dimension 5 — Clarity
> "Every term is readable by a stranger — labels, definitions, scope notes, license, provenance."
### Evidence
- `dct:license` CC BY-SA 4.0 present on TBox + every shape file.
- Strong rdfs coverage: 35 `rdfs:label`, 34 `rdfs:comment` on the TBox.
### Gap (documented — W1)
- The skos lexical layer is near-absent: **1** `skos:prefLabel`, **0** `skos:definition`, **0** `skos:scopeNote`. `skos:` is used structurally (`skos:Concept`/`skos:ConceptScheme` superclassing) rather than lexically. Same §3.2 debt class as asc. Lift trigger: add skos:prefLabel/definition/scopeNote on signifying entities at the next minor.
### Verdict
**PASS-WITH-1-WARNING (W1)** — readable via rdfs; skos 5-layer lexical debt tracked. (evoQ: PASS — shapes carry label+comment+license, no signifying TBox entities requiring skos.)

## Dimension 6 — Consistency
> "The ontology does not contradict itself; rudof validation passes."
### Evidence
- `rapper -i turtle -c`: all 7 artifacts parse clean (TBox 213, sidecar 23, shapes 37/96/90/47, evoQ 403).
- `rudof shacl-validate`: every happy-path fixture → **0 Violations** (§3.6 gate clean). Every failure fixture → live Violations: evo-story 3, evo-change-pipeline 3, evo-test-evidence 3, evo-ambient-agent-policy **2**, evoQ **38**.
### Two regressions found and fixed (the staleness-gate payoff)
- **Dormant shape (re-encoded).** `evo:AmbientAgentPolicyShape` used `sh:SPARQLTarget`/`sh:select`, which **rudof 0.2.8 does not evaluate** (verified 2026-06-21: a direct `sh:targetNode` probe fired 2 Violations on the same data; the SPARQLTarget form fired 0). The shape had targeted nothing since authoring — the same dormancy class as cap's `sh:sparql` `DemoteMergePublishedADRShape`. Re-encoded to `sh:targetSubjectsOf evo:agentRoleProfile` (pure SHACL Core, rudof-native, identical intent). Now fires correctly.
- **Drifted negative test (restored).** The `evo-ambient-agent-policy/failure.ttl` fixture used the obsolete predicate `evo:role` instead of `evo:agentRoleProfile`, so even under a working target it carried no targeted triple. Corrected; failure fixture now → 2 Violations.
- **§3.5 severity declared.** All evo + evoQ constraints are hard MUSTs; the SHACL default `sh:Violation` is the intended severity. Intent is now declared in prose in each shape file (rudof 0.2.8 does not propagate NodeShape-level severity to property constraints — verified — so per-property `sh:Violation` tokens would be behavior-free noise; no Warning-class shape exists here, so the cap/asc silent-misreport defect cannot arise).
### Verdict
**PASS** — rudof-clean; all negative tests live after the re-encode + fixture restore.

---

## Cross-audit reinforcement
### Matrix A — this audit strengthens `capability-operations-ontology-quality-audit-2026-06-21.md`
| Prior item | This audit's contribution | Strengthening effect |
|---|---|---|
| cap re-encoded a dormant `sh:sparql` shape to pure SHACL Core | evo re-encodes a dormant `sh:SPARQLTarget` shape to `sh:targetSubjectsOf` | Confirms rudof-native-encoding as a cross-TBox publication invariant: SPARQL-extension constructs (`sh:sparql`, `sh:SPARQLTarget`) are DORMANT under rudof 0.2.8 and MUST be re-expressed in SHACL Core to be load-bearing |

### Matrix B — `capability-operations-…-2026-06-21.md` strengthens this audit
| Prior ratchet | This audit's inheritance | Strengthening effect |
|---|---|---|
| cap BFO sidecar (ADR-064 alignment-file separation) | evo authors `evidence-os-bfo-2020.ttl` on the same pattern | The sidecar pattern that grounded cap without polluting its native TBox grounds evo without disturbing its W3C-reuse doctrine — bidirectional precedent confirmed |

### Joint invariants confirmed binding
- §3.2 5-layer lexical (skos debt tracked as W1 — same as asc).
- §3.5 severity declared (no Warning-class shape; default-Violation intent declared in prose).
- §3.6 rudof-clean publication gate (0 Violations; all negative tests live).
- §3.7 BFO grounding systematic (closed via sidecar — was the latent gap).
- §3.8 ShEx + SHACL parity (NOT met — `.shex` absent → AUDITED ceiling).

---

## Recommendation

Both artifacts are **AUDITED-eligible**: evo at **PASS-WITH-2-WARNINGS** (W1 skos lexical, W2 `.shex` parity), evoQ at **PASS-WITH-1-WARNING** (W2 `.shex` parity). The §3.7 BFO gap — invisible to the 2026-04-22 audit because the invariant postdated it — is closed by the new sidecar. Two dormant/drifted-test regressions are fixed. Per ADR-134, pin each artifact to its current content-hash, replacing the stale 2026-04-20/22 pointers.

**Promotion roadmap:**
| Trigger | Effect |
|---|---|
| add skos:prefLabel/definition/scopeNote on signifying TBox entities | clears W1 → evo Dimension 5 to PASS |
| author `evidence-os.shex` (+ evoQ ShEx) + parity check passes | clears W2 (§3.8) → Dimension 4 to PASS; lifts the AUDITED ceiling |
| both cleared | Overall PASS; eligible for higher maturity |

**Whitelist line proposals** (HTML doc gate, `ontologies/docs-published.txt` — Sacha-only edit):
```
ontologies/governance/evidence-os/evidence-os.ttl                      2026-06-21  PASS-WITH-2-WARNINGS  Quinn+Nael  # re-audit at 0.2.0, pin 5d9e3392 + BFO sidecar 9ec9ab0b (ADR-132 §3.1 / ADR-134)
ontologies/governance/evidence-os/evo-story.shapes.ttl                 2026-06-21  PASS-WITH-2-WARNINGS  Quinn+Nael  # re-audit at 0.2.0, pin 6a009a42
ontologies/governance/evidence-os/evo-change-pipeline.shapes.ttl       2026-06-21  PASS-WITH-2-WARNINGS  Quinn+Nael  # re-audit at 0.2.0, pin 98e69c50
ontologies/governance/evidence-os/evo-test-evidence.shapes.ttl         2026-06-21  PASS-WITH-2-WARNINGS  Quinn+Nael  # re-audit at 0.2.0, pin 8deb1b70
ontologies/governance/evidence-os/evo-ambient-agent-policy.shapes.ttl  2026-06-21  PASS-WITH-2-WARNINGS  Quinn+Nael  # re-encoded SPARQLTarget→targetSubjectsOf, pin 991a9eb9
ontologies/governance/evidence-os/evoQ-kpi-shapes.shapes.ttl           2026-06-21  PASS-WITH-1-WARNING   Quinn+Nael  # re-audit at 0.2.0, pin e0d6160d
```

**Registry line proposals** (IRI gate, `bra0-ns/docs-published.txt` — Sacha-only edit):
```
evidence-os/evidence-os.ttl;Audited;audit/evidence-os-ontology-quality-audit-2026-06-21.md;2026-06-21
evidence-os/evo-story.shapes.ttl;Audited;audit/evidence-os-ontology-quality-audit-2026-06-21.md;2026-06-21
evidence-os/evo-change-pipeline.shapes.ttl;Audited;audit/evidence-os-ontology-quality-audit-2026-06-21.md;2026-06-21
evidence-os/evo-test-evidence.shapes.ttl;Audited;audit/evidence-os-ontology-quality-audit-2026-06-21.md;2026-06-21
evidence-os/evo-ambient-agent-policy.shapes.ttl;Audited;audit/evidence-os-ontology-quality-audit-2026-06-21.md;2026-06-21
evidence-os/query/evoQ-kpi-shapes.shapes.ttl;Audited;audit/evidence-os-ontology-quality-audit-2026-06-21.md;2026-06-21
```

---

## Annex — commands used
```bash
git hash-object ontologies/governance/evidence-os/evidence-os.ttl
#   => 5d9e3392…   (current — new pin; audited 2026-04-20 blob = 300eedb8… → STALE)
git hash-object ontologies/governance/evidence-os/evoQ-kpi-shapes.shapes.ttl
#   => e0d6160d…   (current — new pin; audited blob = cfa85b8d… → STALE)

rapper -i turtle -c <each artifact>          # => 213/23/37/96/90/47/403 triples, all clean

# Dormancy probe (sh:SPARQLTarget not evaluated by rudof 0.2.8):
rudof shacl-validate -s <targetNode probe> failure.ttl   # => 2 Violations
rudof shacl-validate -s evo-ambient-agent-policy.shapes.ttl failure.ttl  # before re-encode => 0 ; after => 2

# Final fixture sweep (happy=0, failure>0):
#   evo-story 0/3 ; evo-change-pipeline 0/3 ; evo-test-evidence 0/3 ;
#   evo-ambient-agent-policy 0/2 ; evoQ-kpi-shapes 0/38
```

Audit closed 2026-06-21 — ADR-132 §3.1 re-audit sub-phase (C-R2b), ADR-134 content-hash pin. Quinn (QA) + Nael (Architect), concerted.
