# Essence Kernel + EDGY — Keet 6-dim ontology-quality re-audit (2026-06-21)

> **Subjects**: `foundation/essence-kernel.ttl` (Essence Kernel, strategic layer) and
> `enterprise/edgy.ttl` (OntolEDGY cross-domain enterprise-design vocabulary).
> **Engine**: rudof 0.2.8 / rapper. **Auditors**: Quinn (6-dim grid), Nael (grounding).
> **Controller**: Sacha. **Sub-phase**: ADR-132 §3.1 **C-R2a** (assumed "in-sync"
> direct DRAFT→AUDITED promotion). **Pinning**: ADR-134 content-hash.
> **Maturity transition**: DRAFT → **AUDITED** (PUBLISHED stays whitelist-gated, Sacha-only).
> **Aggregate verdicts**: ess **PASS-WITH-2-WARNINGS** · edgy **PASS-WITH-2-WARNINGS**.

## Why a re-audit and not a direct promotion (C-R2a premise correction)

The C-R2a cohort was scoped as "in sync — direct badge." The ADR-134 staleness gate
falsified that premise for both files:

- Both `essence-kernel.ttl` and `edgy.ttl` were last modified in commit `da5553f`
  (**2026-04-28**, a header-cosmetics chore) — **after** their original audits
  (ess/edgy carried 2026-04-20 / 2026-04-13 PASS verdicts). Modified-after-audit = STALE-AUDIT.
- More materially, both files **predate** the binding invariants ratified **2026-04-28**:
  §3.7 (BFO grounding systematic) and §3.8 (ShEx+SHACL parity ceiling). The original PASS
  verdicts never tested either invariant.

So both were re-audited at the current grid, content-hash pinned, and badged fresh. The
staleness gate paid off again: it caught that edgy's BFO grounding existed **only as prose**.

## Content-hash pins (ADR-134)

```
essence-kernel.ttl              dda7c22dffdb2b3bc20141919a5db78723a839e3
edgy.ttl                        a2d53f562ed92ef4faeb303cca997a20f74cd8e2
edgy-bfo-2020.ttl  (new)        4b22fae4372638ddafdd9e7e245d988c0ca727b2
```

## Evidence (rudof 0.2.8 / rapper, 2026-06-21)

| Check | Result |
|---|---|
| Parse `essence-kernel.ttl` | **PROVEN** — 498 triples, clean |
| Parse `edgy.ttl` | **PROVEN** — 522 triples, clean |
| Parse `edgy-bfo-2020.ttl` (new sidecar) | **PROVEN** — 17 triples, clean |
| ess §3.7 BFO grounding | **PROVEN inline** — `rdfs:subClassOf bfo:0000001 / 0000031 / 0000016 / 0000015` chains via `@prefix bfo: <…/obo/BFO_>` |
| edgy §3.7 BFO grounding (before) | **GAP** — prose only (header comment + unused `edgy:groundedInBFO` object property); no `rdfs:subClassOf bfo:*` axioms |
| edgy §3.7 BFO grounding (after) | **PROVEN via sidecar** — tetrad-spine grounding (7 axioms) |

### edgy §3.7 closure — tetrad-spine grounding (not the grid leaf table)

The grid §3.7 per-leaf table is internally inconsistent with edgy's own hierarchy:
`edgy:Task ⊑ edgy:Outcome`, yet the table wants `Task → bfo:Process` (occurrent). Landing
the leaf on an occurrent while its parent lands on a continuant forces occurrent/continuant
disjointness and makes the leaf unsatisfiable. The satisfiable grounding is at the **tetrad
spine**; every leaf inherits transitively. Per ADR-064 §2.6 conservative-parent rule,
more-specific BFO subtypes for individual leaves are deferred refinements.

```
edgy:Element      → obo:BFO_0000001 (entity)
edgy:Intersection → obo:BFO_0000001 (entity)
edgy:People       → obo:BFO_0000004 (independent continuant)
edgy:Object       → obo:BFO_0000004 (independent continuant)
edgy:Activity     → obo:BFO_0000003 (occurrent)
edgy:Outcome      → obo:BFO_0000020 (specifically dependent continuant)
edgy:Facet        → obo:BFO_0000020 (specifically dependent continuant)
```

Multi-inheritance satisfiability: `edgy:Organization ⊑ People+Intersection`,
`edgy:Product/Brand ⊑ Object+Intersection`. People/Object → BFO_0000004, Intersection →
BFO_0000001; BFO_0000004 ⊑ BFO_0000001, so no disjointness conflict.

## Six dimensions

### Essence Kernel (`essence-kernel.ttl`)

| # | Dimension | Verdict | Notes |
|---|---|---|---|
| 1 | Accuracy | PASS | Genuine inline BFO grounding (Alpha/State/Activity/Competency chains land on BFO continuant/GDC/disposition/process). |
| 2 | Completeness | PASS | OMG Essence Kernel alpha/state/activity coverage present. |
| 3 | Conciseness | PASS | No redundant axioms. |
| 4 | Adaptability | PASS | Strategic-layer vocabulary reused by downstream KS. |
| 5 | Clarity | **WARN (W-skos)** | rdfs label/comment present; skos prefLabel/definition/scopeNote = 0/0/0. Five-layer lexical not met. |
| 6 | Consistency | PASS | rapper parse clean; grounding chains consistent. |

### EDGY (`edgy.ttl` + `edgy-bfo-2020.ttl`)

| # | Dimension | Verdict | Notes |
|---|---|---|---|
| 1 | Accuracy | PASS | §3.7 gap closed via sidecar tetrad-spine grounding; was prose-only before. |
| 2 | Completeness | PASS | 22-class EDGY tetrad (People/Object/Activity/Outcome + Facet + Intersection) + leaves complete. |
| 3 | Conciseness | PASS | No redundant axioms; sidecar adds 7 grounding axioms + header only. |
| 4 | Adaptability | PASS | Mid-level cross-domain vocabulary; native TBox stays on its own spine, BFO loaded only by cross-graph consumers (ADR-064). |
| 5 | Clarity | **WARN (W-skos)** | Partial skos (1 prefLabel / 1 definition); five-layer lexical not met across all terms. |
| 6 | Consistency | PASS | rapper parse clean on all three files; multi-inheritance satisfiable (checked above). |

## §3.7–§3.8 binding invariants

- **§3.7 BFO grounding systematic** — ess SATISFIED inline; edgy SATISFIED via
  `edgy-bfo-2020.ttl` sidecar (ADR-064 alignment-file separation).
- **§3.8 ShEx + SHACL parity** — neither file ships a `.shex` ORM surface → **W-shex**.
  This caps both at the AUDITED ceiling (not PUBLISHED) until ShEx parity is authored.

## Whitelist + registry rows

**bra0_meta `ontologies/docs-published.txt`** (HTML doc gate):
```
ontologies/foundation/essence-kernel.ttl  2026-06-21  PASS-WITH-2-WARNINGS  Quinn  # re-audit, pin dda7c22d (ADR-132 §3.1 C-R2a / ADR-134); W-skos + W-shex; supersedes 2026-04-20 Nael PASS
ontologies/enterprise/edgy.ttl            2026-06-21  PASS-WITH-2-WARNINGS  Quinn  # re-audit, pin a2d53f56 + BFO sidecar 4b22fae4 (ADR-132 §3.1 C-R2a / ADR-134); §3.7 closed via sidecar; W-skos + W-shex; supersedes 2026-04-13 Sacha PASS
```

**bra0-ns `docs-published.txt`** (IRI resolution gate): ess + edgy rows DRAFT → Audited,
pointing to this audit file.

## Command annex

```
rapper -i turtle -c ontologies/foundation/essence-kernel.ttl     # 498 triples
rapper -i turtle -c ontologies/enterprise/edgy.ttl               # 522 triples
rapper -i turtle -c ontologies/enterprise/edgy-bfo-2020.ttl      # 17 triples
git hash-object ontologies/foundation/essence-kernel.ttl ontologies/enterprise/edgy.ttl ontologies/enterprise/edgy-bfo-2020.ttl
```
