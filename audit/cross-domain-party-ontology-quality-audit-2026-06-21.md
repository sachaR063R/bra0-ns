# Party / Role socle — Keet 6-dim ontology-quality audit (2026-06-21)

> **Subject**: `cross-domain/party` transverse Référentiel socle, version **0.2.0** (grounded
> rebuild, ADR-129). **Engine**: rudof 0.2.8. **Auditors**: Noam (6-dim grid owner), Nael
> (OntoClean/UFO), Athena (third-party-referential doctrine). **Controller**: Sacha.
> **Maturity transition**: DRAFT → **AUDITED** (PUBLISHED stays gated by the ontology-quality
> whitelist, Sacha-only). **Aggregate verdict**: **PASS** (strictest dimension = PASS).

## Corpus under audit

```
party-role.tbox.ttl                          core TBox (Category/Kinds/SubKind/Role/Relator)
alignments/party-role.alignments.ttl         CMNS · FIBO · GLEIF · FOAF · ORG
alignments/party-role-bfo-2020.ttl           BFO 2020 systematic grounding
party-role.shex                              ORM surface (ShEx parity)
queries/grounding-gate-bfo.rq                CI gate (BFO ancestor reachability)
party-role-style-guide.md · party-role-cqs.md · this audit
```

## Evidence (rudof 0.2.8, 2026-06-21)

| Check | Command | Result |
|---|---|---|
| Parse-merge (3 TTL) | `rudof query` over all three files | **PROVEN** — clean |
| BFO systematic gate (§3.7) | `grounding-gate-bfo.rq` | **PROVEN** — 0 rows (every class reaches a BFO ancestor) |
| General external grounding | external-ancestor / conformsTo / whyNoStandard gate | **PROVEN** — 0 rows |
| CQ-G3 Party = Category | `party:Party party:ontoCleanType ?v` | **PROVEN** — "Category" |
| CQ-S2 LegalEntity = SubKind | `party:LegalEntity party:ontoCleanType ?v` | **PROVEN** — "SubKind" |
| CQ-G4 LEI on the SubKind | `party:legalEntityIdentifier rdfs:domain ?v` | **PROVEN** — party:LegalEntity |
| CQ-S1 person XOR organisation | `owl:disjointWith` | **PROVEN** — holds |
| CQ-S3 any Party may play | `party:plays rdfs:domain ?v` | **PROVEN** — party:Party (Category) |

Per-class anchors (direct + inherited): Party → cmns:Party, foaf:Agent, bfo:IndependentContinuant;
NaturalPerson → fibo Person, foaf:Person, bfo:MaterialEntity; Organisation → fibo FormalOrganization,
foaf:Organization, org:Organization; LegalEntity → gleif L1 LegalEntity, org:FormalOrganization;
PartyRole → cmns:PartyRole, bfo:Role; Relationship → bfo:SpecificallyDependentContinuant + whyNoStandard.

## Six dimensions

| # | Dimension | Verdict | Notes |
|---|---|---|---|
| 1 | **Accuracy** | PASS | OntoClean faults of 0.1.0 corrected: Party→Category (C-1), NaturalPerson/Organisation→Kinds (C-2), LegalEntity→SubKind (C-3), LEI as extrinsic identifier not identity criterion (C-4). L1/L2 hold. |
| 2 | **Completeness** | PASS | CQ set authored (`party-role-cqs.md`): grounding/structural CQs PROVEN; business CQs answerable on a consumer ABox. |
| 3 | **Conciseness** | PASS | No redundant axioms; anchor-stubs minimal; one `ontoCleanType` per class. |
| 4 | **Adaptability** | PASS | Single shared `party:PartyRole` consumed multi-lens (banking proven; omyn-tiers/wealth-management pending P3). Anchor-stub method keeps the socle embeddable for the standalone projection. |
| 5 | **Clarity** | PASS | Five-layer lexical on every term (rdfs:label bilingual · skos:prefLabel · skos:definition · rdfs:comment · skos:scopeNote). |
| 6 | **Consistency** | PASS | rudof parse-merge clean; disjointness holds; no anti-rigid-subsumes-rigid edge; BFO + external grounding both 0-row. |

## §3.7–§3.9 binding invariants

- **§3.7 BFO grounding systematic** — SATISFIED via `party-role-bfo-2020.ttl`; gate 0 rows.
- **§3.8 ShEx + SHACL parity** — ShEx ORM (`party-role.shex`) present; SHACL validation lives in the
  consuming modules (banking C1..C8), per the socle/consumer split.
- **§3.9 companion files** — `.ttl` (×3) · `.shex` · `-style-guide.md` · `-cqs.md` · this
  `-quality-2026-06-21.md` — complete.

## Open items (carried, non-blocking for AUDITED)

- **O-1b** — `party:Organisation` BFO anchor: currently inherited from Party (independent continuant)
  to avoid the material-entity vs object-aggregate debate for legal persons. Revisit if a stronger
  anchor is required.
- **Q-129-2** — `omyn-tiers` consumption pattern (P-A vs P-C). Athena, P3.
- **Q-129-4** — version + hash16 scheme for the AUDITED tag feeding consumer manifests. P3.

## Verdict

**PASS — promote to AUDITED.** Publication to `schema.bra0.org/cross-domain/party` remains gated by
the ontology-quality whitelist (Sacha-only). P3 (consumer re-pin) may proceed against 0.2.0.
