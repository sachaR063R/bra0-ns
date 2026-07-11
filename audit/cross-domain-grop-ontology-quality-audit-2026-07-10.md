# GROP kernel — Keet 6-dim ontology-quality audit (2026-07-10)

> **Subject**: `cross-domain/grop` — GROP (Generic Runtime Operating Protocol) interop kernel,
> version **0.1.0 DRAFT**, with its now-complete companion set. **Protocol**:
> `_bmad/docs/ontology-quality-audit-grid-keet-6dim.md` (Keet 6-dim). **Engines**: rudof 0.2.8
> (SHACL Core only, ADR-128) + Oxigraph 0.5.8 (all SPARQL gates, feedback 2026-06-22).
> **Auditor**: sachaR063R (S-B session, GROP publication phase, delegated execution).
> **Controller**: Sacha. **Session constraint**: audit is READ-ONLY over the corpus; this file
> and the S-B session note are the only writes. **Maturity transition sought**: DRAFT → AUDITED.
> **Aggregate verdict**: **CONDITIONAL** (strictest dimensions = Clarity, Consistency; two named
> blockers B1/B2, both Sacha-gated kernel-side edits).
>
> Promotion to `omat:Audited`, whitelist rows (both gates) and IRI publication on
> `schema.bra0.org/cross-domain/grop` are **Sacha-only acts**. This audit recommends; it
> executes nothing.

## Corpus under audit

```
grop.ttl                              core TBox 0.1.0 DRAFT (3 classes, 5 named individuals, 7 properties)
grop.shapes.ttl                       SHACL Core companion 0.1.0 (10 shapes, instance layer)
grop.shex                             ShEx ORM companion 0.1.0 (strict-parity claim)
grop-style-guide.md                   naming + lexical + class-by-class commentary
grop-cqs.ttl                          13 cq:CompetencyQuestion instances (ADR-130 pilot, born governed)
grop-cqs.md                           hand-written interim projection of grop-cqs.ttl
alignments/grop-bfo-2020.ttl          BFO 2020 systematic grounding sidecar 0.2.0
queries/grounding-gate-bfo.rq         BFO ancestor-reachability gate (0 rows = PASS)
protocols/valueflows.ttl              first concrete protocol registration 0.1.1 (UNCOMMITTED diff — F-SB-1)
```

Kernel graph-level gates (artifact tier, consumed not audited-as-subject):
`_bmad/work/ks-holonic-cartography-2026-07-07/P3-standard/gates/` — `G1b-artifact.rq`,
`G2-artifact.rq`, `G3-artifact.rq`, `G4-kernel-cohesion-artifact.rq`, `ST4-artifact.rq`
(+ supplementary `F5-1-no-commerce-leak.rq`, `F5-2-borrow-provenance.rq`).

Companion dependency: `ontologies/cross-domain/cq/` (cq.ttl 0.1.0 DRAFT pilot, cq.shapes.ttl,
queries/binding-coherence-gate.rq) — itself **unaudited** (F-SB-6).

## §5.2 — Mechanical evidence (run LIVE 2026-07-10, this session)

All commands and literal results. `rapper` and `rudof shex` invocations were
**permission-denied by session policy**; parse cleanliness is witnessed by Oxigraph
strict-mode load (no `--lenient`) + rudof turtle parsing, per the binding estate rule
(rudof for SHACL Core, Oxigraph for all SPARQL).

| # | Check | Command | Literal result | Verdict |
|---|---|---|---|---|
| 1 | Parse cleanliness (5 TTL) | `oxigraph load --location /tmp/sb-grop-kernel-1010 --file grop.ttl --file protocols/valueflows.ttl --file alignments/grop-bfo-2020.ttl` (strict mode) + checks 2/6 loading grop-cqs.ttl, cq corpus | loads clean, no error | **PROVEN** |
| 2 | SHACL Core validation | `rudof shacl-validate -s grop.shapes.ttl grop.ttl protocols/valueflows.ttl` | `No Errors found` | **PROVEN** — 0 Violations |
| 3 | Gate G1b (minimality, artifact) | `oxigraph query --location /tmp/sb-grop-kernel-1010 --results-format csv --query-file .../G1b-artifact.rq` | `x,p` (header only, 0 rows) | **PROVEN** |
| 3 | Gate G2 (native interop, artifact) | same store, `G2-artifact.rq` | `ks` (0 rows) | **PROVEN** |
| 3 | Gate G3 (derivation, artifact) | same store, `G3-artifact.rq` | `p` (0 rows) | **PROVEN** |
| 3 | Gate G4 (kernel cohesion, artifact) | same store, `G4-kernel-cohesion-artifact.rq` | `k,o` (0 rows) | **PROVEN** |
| 3 | Gate ST4 (no-fusion, artifact) | same store, `ST4-artifact.rq` | `a,b` (0 rows) | **PROVEN** |
| 3+ | F5-1 (no commerce leak) / F5-2 (borrow provenance) | same store | `x,t` / `x,t` (0 rows each) | **PROVEN** |
| 4 | BFO grounding gate (§3.7) | same store, `queries/grounding-gate-bfo.rq` | `ungroundedClass` (0 rows) | **PROVEN** |
| 4 | BFO gate NEGATIVE CONTROL | fresh store loading grop.ttl WITHOUT the alignment; same query | 3 rows: `grop#ConcreteProtocol`, `grop#Kernel`, `grop#Phase` | **PROVEN** — gate is live, fires on missing landings |
| 5 | CQ well-formedness (SHACL) | `rudof shacl-validate -s cq/cq.shapes.ttl cq/cq.ttl cq/cq-cqs.ttl grop/grop-cqs.ttl` | `No Errors found` | **PROVEN** |
| 5 | Binding-coherence gate | `oxigraph load /tmp/sb-cq-binding-1010` (cq.ttl + cq-cqs.ttl + grop-cqs.ttl) + `binding-coherence-gate.rq` | `cq,declaredOrdinal,maxTermOrdinal` (0 rows) | **PROVEN** |
| 6 | Style-guide coverage | `scripts/lint-style-guide-coverage.sh` **does not exist** in this repo (Glob verified) — manual check performed | 3/3 classes (§5), 5/5 named individuals (§6), 7/7 properties (§7) named in grop-style-guide.md | **PROVEN manually** — 100% coverage; script inapplicability recorded (F-SB-8) |
| 7 | ShEx/SHACL parity (§3.8) | `scripts/check-shex-shacl-parity.sh` **does not exist** (Glob verified); `rudof shex` permission-denied — manual structural comparison performed | see Dimension 6 evidence: 10 shapes ↔ 10+1 ShEx shapes, same required properties, cardinalities, value sets | **PASS manually**; mechanical ShEx syntax validation **UNVERIFIED** (F-SB-8) |

Negative-control method note: the protocol's "mutated /tmp copy" variant was blocked by the
session write policy (`Write` to /tmp denied). The substituted falsification — running the
grounding gate over the kernel with the alignment omitted — is strictly equivalent for the
gate's contract (landing axioms absent → gate must fire; it fired, 3 rows). The G1b/G2/G3/G4/ST4
negative controls were performed with mutated fixtures at P3 (2026-07-07, gate headers) and are
carried, not re-run. The three ephemeral stores `/tmp/sb-grop-kernel-1010`,
`/tmp/sb-grop-negctrl-1010`, `/tmp/sb-cq-binding-1010` could not be deleted (rm denied by
session policy); Sacha may remove them.

## §3 floor invariants — 9 verdicts

| Invariant | Verdict | Evidence |
|---|---|---|
| §3.1 License visibility | **PASS** (1 warning) | `dcterms:license` present on all 5 headers. Form deviation: grop.ttl / grop.shapes.ttl / valueflows.ttl carry the string literal `"CC BY-SA 4.0"`, the grid specifies `<SPDX-or-URL>`; alignment + cqs use the URL form (F-SB-2). Missing-license FAIL trigger not met. |
| §3.2 Five-layer lexical | **FAIL at the AUDITED bar → CONDITIONAL** (blocker B1) | `skos:scopeNote` is present on **0/13** signifying entities (only the ontology header carries one); AUDITED requires full 5 layers on ≥80%. Also missing: `skos:prefLabel` on `grop:kernel`, `grop:phase`, `grop:rolesBorrow`; `rdfs:comment` on `grop:offerRole`, `grop:rolesBorrow`. grop-style-guide.md §4 declares a **4-layer** discipline — a documented deviation, but below the grid bar (F-SB-3). Lift plan: gated kernel-side lexical pass (grop.ttl edits are Sacha-gated per ADR-140), see roadmap. |
| §3.3 Triple-witness deprecation | **PASS** (vacuous) | No deprecated IRI exists in the corpus; nothing was ever published under schema.bra0.org/cross-domain/grop. |
| §3.4 Punning over UNION | **PASS** | No UNION class anywhere. Cross-vocabulary reuse is instance-level: VF map puns `vf:Intent/Proposal/Commitment` as phase carriers (`vf:Intent grop:phase grop:Request`); AS2 roles reused directly, no re-mint. |
| §3.5 Cardinality contracts with explicit severity | **FAIL as written → CONDITIONAL** (blocker B2) | **No `sh:severity` triple appears anywhere in grop.shapes.ttl** (all 10 shapes silent → default sh:Violation, but the invariant demands *explicit* severity; "silent shapes = Consistency FAIL"). No Warning shapes exist, so no lift-trigger comments are owed. Lift plan: shapes 0.1.1 adds explicit `sh:severity sh:Violation` per property/node shape — a companion edit, Sacha-gated (F-SB-4). |
| §3.6 rudof-clean publication gate | **PASS** (kernel side) | rudof shacl-validate = 0 Violations, 0 Warnings (mechanical check 2). Mirror parity is N/A: no `bra0-ns/cross-domain/grop/` staging exists yet (verified — bra0-ns cross-domain contains edgy/party/retroeng only); staging is a Sacha-gated publication act. |
| §3.7 BFO grounding systematic | **PASS** | All 3 local classes reach `bfo:BFO_0000031` (GDC) via the 0.2.0 sidecar; gate 0 rows, negative-tested live this session (3 rows on omission). The Phase ⊑ Process alternative is OntoClean-rejected and recorded in the sidecar header (not re-litigated). Machine-readable OntoClean annotations pending = R4, named and tracked (F-SB-5, non-blocking warning — §3.7 itself does not require them). |
| §3.8 ShEx + SHACL parity | **PASS** (manual; mechanical validation UNVERIFIED) | Manual structural comparison: KernelShape value set `(grop:kernel)` ↔ `[ grop:kernel ]`; Phase triad `sh:in (Request Offer Commit)` ↔ value set; SpeaksSubjectShape `minCount 1 + sh:in` ↔ `grop:speaks [ grop:kernel ] +`; lanes/polarity/attestation `sh:nodeKind sh:BlankNodeOrIRI` ↔ `NONLITERAL *`; ConcreteProtocol `sh:hasValue grop:kernel` ↔ ShEx two-constraint partition (documented as the rudof-EXTRA workaround). One extra ShEx shape (`grop:InteractionShape`) is a declared ORM convenience composition adding nothing beyond the conjunction — parity preserved. Parity script does not exist; `rudof shex` denied this session (F-SB-8). |
| §3.9 Companion files | **PASS** (1 warning) | All companions present: .ttl, .shapes.ttl, .shex, -style-guide.md, CQ corpus (governed grop-cqs.ttl + interim grop-cqs.md projection, 13 ≥ 10 questions with SPARQL paths), this audit. Warning: the CQ indexing vocabulary (cq: 0.1.0 DRAFT) is itself unaudited (F-SB-6). |

**Floor score: 7/9 PASS — §3.2 and §3.5 unsatisfied at the AUDITED bar, both with documented
lift plans → per the eligibility table (6-8/9), the subject is CONDITIONAL.** (The §7.1 triage
checklist scores 9/9 — license, BFO, label+comment, parse, and all five companions exist, with
this file as the audit — which is what made the full §5 review admissible.)

## Six dimensions

| # | Dimension | Verdict | Notes |
|---|---|---|---|
| 1 | **Accuracy** | PASS-WITH-1-WARNING | BFO grounding PROVEN (0 rows, negative-tested); GDC landings semantically defended (specifications, not occurrences; continuant/occurrent cut argued in sidecar header); OntoClean meta-typing analysed prose-level, Kind assignments defensible, L1/L2 hold; borrow characterization honest (`prov:wasDerivedFrom`, NOT `owl:equivalentClass`, AS2-subtyping UNVERIFIED caveats preserved). Warning: R4 machine-readable OntoClean annotations (party:ontoCleanType pattern) not yet in grop.ttl — named, tracked (sidecar header R4 + ADR-140 §5), non-blocking for §3.7. |
| 2 | **Completeness** | PASS-WITH-1-WARNING | 13 CQs (≥10) with SPARQL paths, each traced to an actual grop.ttl declaration or a PROVEN gate; well-formedness SHACL + binding-coherence gate both green live this session; rung discipline (L1 kernel terms, L3 census term) coherent with ADR-130 §4. Warning: the indexation layer rides the unaudited cq: 0.1.0 DRAFT pilot — the CQs' substance stands on its own, the "born governed" claim inherits DRAFT status (F-SB-6, conservative reading). |
| 3 | **Conciseness** | PASS | Closed mint, borrow-first throughout: AS2 verbs/roles and VC 2.0 reused, no re-mint; the only mints (two lanes) resolve the logged D-F5-1 debt (no external vocabulary ships the binding); no role class minted (O-GROP-1, party socle inheritance); minimality mechanically enforced (G1b + F5-1 + F5-3 composite, green live); no UNION, no redundant axiom. |
| 4 | **Adaptability** | PASS-WITH-2-WARNINGS | Versioned companions with owl:versionIRI; sidecar evolves independently (0.1.0→0.2.0 Phase re-landing executed cleanly with rejected alternative recorded); no deprecation debt (§3.3 vacuous); tracked refinement ladder R1-R4 named. Warnings: (a) grop.ttl itself lacks `owl:versionIRI` (companions have it — F-SB-7); (b) §3.5 explicit-severity absence also binds here (shared with Consistency, counted once as blocker B2). |
| 5 | **Clarity** | **CONDITIONAL** | Labels/definitions/comments are strong and gate-traceable; style guide covers 100% of terms; license present on every header. Blocker B1: five-layer lexical below the AUDITED bar — `skos:scopeNote` on 0% of signifying entities, `skos:prefLabel`/`rdfs:comment` gaps on 5 entities (F-SB-3); license literal-form normalization (F-SB-2). Lift: Sacha-gated kernel lexical pass (grop.ttl 0.1.1 or 0.2.0). |
| 6 | **Consistency** | **CONDITIONAL** | rudof SHACL Core = 0 Violations (PROVEN); all five artifact gates + F5-1/F5-2 + BFO gate green live; no contradiction (all landings on one BFO branch, no disjointness conflict, no anti-rigid-subsumes-rigid edge); ShEx/SHACL parity holds by manual comparison. Blocker B2: §3.5 silent shapes — no explicit `sh:severity` in grop.shapes.ttl (F-SB-4). Lift: shapes 0.1.1 severity pass, Sacha-gated. |

**Aggregate: CONDITIONAL** (≥1 CONDITIONAL, no FAIL-without-lift-plan).

## ADR-134 content-hash pinning table

Pinned by `git hash-object` (content hash, NOT semver — ADR-134), working tree = committed
state for all pinned artifacts (git status clean except valueflows.ttl, which is deliberately
NOT pinned — F-SB-1).

| Artifact | Content hash (git hash-object) | Version |
|---|---|---|
| `grop.ttl` | `12c221ad615110437c329fcdc7e80ae3ce11097a` | 0.1.0 |
| `grop.shapes.ttl` | `e14225249e2e25f5dd14368c79e5c9c24bb37e1a` | 0.1.0 |
| `grop.shex` | `6839a2be80752a41045e228419e27ca52b74c41f` | 0.1.0 |
| `grop-style-guide.md` | `cd29808b642c2ab6855da13ee496ff0e113b7e99` | — |
| `grop-cqs.ttl` | `89b6bf8c1de4f771544378efcb7e7cba8b64a949` | 0.1.0 |
| `alignments/grop-bfo-2020.ttl` | `7e76c12c8b626e1cb42edadec0045c9edbabfa29` | 0.2.0 |
| `queries/grounding-gate-bfo.rq` | `221bc21d94b824d0ffa8304d3d4b7a14ce4397c9` | — |

## Findings (F-SB-*)

- **F-SB-1** — `protocols/valueflows.ttl` carries a pre-existing **uncommitted** diff
  (0.1.0 → 0.1.1: reified rdf:Statement maps re-expressed as live `grop:phase` triples so the
  artifact-tier G1b bites; working-tree blob `a13f027`). All gates in this audit ran over the
  **working-tree** state and are green. Out of scope for the kernel verdict (it does not change
  any gate result); the file is not in the pinning table. Sacha decision owed: commit or revert.
- **F-SB-2** — `dcterms:license` value form: string literal `"CC BY-SA 4.0"` in grop.ttl,
  grop.shapes.ttl, valueflows.ttl vs the grid's `<SPDX-or-URL>` (URL form already used by the
  alignment and CQ corpus). Normalize at the next gated kernel edit. Warning, non-blocking.
- **F-SB-3** — **Blocker B1 (§3.2 / Clarity)**: `skos:scopeNote` absent on all 13 signifying
  entities (0% vs ≥80% AUDITED bar); `skos:prefLabel` missing on `grop:kernel`, `grop:phase`,
  `grop:rolesBorrow`; `rdfs:comment` missing on `grop:offerRole` and `grop:rolesBorrow`.
  grop-style-guide.md §4 codifies 4 layers — the guide itself must be re-aligned to the grid's
  5 layers when the kernel lexical pass lands.
- **F-SB-4** — **Blocker B2 (§3.5 / Consistency, Adaptability)**: no explicit `sh:severity` on
  any of the 10 shapes in grop.shapes.ttl (silent-shape rule). Fix is mechanical (explicit
  `sh:severity sh:Violation` per shape), companion-side, Sacha-gated.
- **F-SB-5** — R4: machine-readable OntoClean annotations (party:ontoCleanType pattern) not yet
  in grop.ttl; analysis exists prose-level in the sidecar + style guide. Named and tracked
  (sidecar R4, ADR-140 §5). Touches Accuracy as a warning; does NOT block AUDITED (§3.7 is
  satisfied; OntoClean machine-readability is ADR-129 party-socle discipline, not a grid floor
  invariant).
- **F-SB-6** — Companion cq: module (`ontologies/cross-domain/cq/`, 0.1.0 DRAFT pilot) is itself
  unaudited. Conservative reading adopted: a companion's maturity does not cap the subject's
  verdict when the subject's own §3.9 evidence (13 CQs + SPARQL paths) stands without it, BUT the
  "born governed" indexation claim is carried at DRAFT strength until cq: passes its own audit.
  Recorded as a Completeness warning.
- **F-SB-7** — grop.ttl header lacks `owl:versionIRI` (grop.shapes.ttl, grop-cqs.ttl and the
  sidecar all carry one). Minor; add at next gated kernel edit.
- **F-SB-8** — Tooling inapplicability recorded honestly: `scripts/check-shex-shacl-parity.sh`
  and `scripts/lint-style-guide-coverage.sh` do not exist in this repo (grid §3.8/§3.9 name them
  as CI intent); parity and coverage were established manually (results above). `rapper` and
  `rudof shex` invocations were permission-denied by the session sandbox → mechanical ShEx
  syntax validation is **UNVERIFIED** this session (parse-level only via manual review).

## Cross-audit reinforcement

### Matrix A — this audit strengthens `party-role-quality-2026-06-21.md`
| Prior item | This audit's contribution | Effect |
|---|---|---|
| party:PartyRole ⊑ bfo:Role as THE estate role socle | GROP mints no role class; polarity poles ground through party:PartyRole (O-GROP-1) | Confirms the socle is consumed, single-sourced, beyond banking |
| Anchor-stub method (Oxigraph-WASM, no owl:imports resolution) | Re-applied verbatim in grop-bfo-2020.ttl, gate green + negative-tested | Second independent confirmation of the method |

### Matrix B — prior audits strengthen this one
| Prior ratchet | Inheritance here | Effect |
|---|---|---|
| ADR-128 (rudof no-ops sh:sparql) | grop.shapes.ttl is SHACL-Core-only by construction; all graph invariants in Oxigraph gates | No inert sh:sparql anywhere in the corpus |
| ADR-134 content-hash pinning | 7-artifact pinning table above | Audit staleness detectable mechanically |
| Feedback 2026-06-23 (absolute paths, csv results) | All gate runs used absolute paths + `--results-format csv` | No false-green-on-wrong-file risk |

### Joint invariants confirmed binding
- §3.7 BFO grounding via separate sidecar + 0-row gate + live negative control.
- Oxigraph-only SPARQL gating; rudof confined to SHACL Core.

## Recommendation

**CONDITIONAL — does NOT yet recommend AUDITED (omat:Audited).** The kernel's substance is
strong: all five artifact gates, both minimality composites, the BFO grounding gate (with live
negative control), rudof SHACL Core, CQ well-formedness and binding coherence are ALL green,
run live this session. Two named blockers, both mechanical and Sacha-gated, separate it from
AUDITED:

- **B1 (F-SB-3)**: kernel lexical pass — add `skos:scopeNote` (+ the 5 prefLabel/comment gaps)
  to ≥80% of signifying entities, and re-align grop-style-guide.md §4 from 4 to 5 layers.
- **B2 (F-SB-4)**: shapes severity pass — explicit `sh:severity` on all 10 shapes
  (grop.shapes.ttl 0.1.1).

**Promotion roadmap:**
| To version | Trigger | Effect |
|---|---|---|
| grop.ttl 0.1.1 (gated) | B1 lexical pass + F-SB-2 license URL + F-SB-7 versionIRI | Clarity → PASS; floor §3.2 → PASS |
| grop.shapes.ttl 0.1.1 (gated) | B2 explicit severities (+ re-run rudof + parity) | Consistency → PASS; floor §3.5 → PASS |
| re-audit delta (S-B′) | both above landed; re-pin hashes per ADR-134 | Aggregate → PASS; **recommends AUDITED (omat:Audited)** |
| kernel 0.2.x | R4 machine-readable OntoClean; cq: module audited | Accuracy/Completeness warnings lift |

**Whitelist line proposals** (drafted, NOT actionable until the re-audit closes PASS; both
rows are **Sacha-only** edits, as are omat: promotion, bra0-ns mirror staging and IRI
publication):

bra0_meta `ontologies/docs-published.txt`:
```
ontologies/cross-domain/grop/grop.ttl  <re-audit-date>  PASS  <auditor>  # pin 12c221ad + BFO sidecar 7e76c12c (ADR-134); supersedes CONDITIONAL 2026-07-10
```

bra0-ns `docs-published.txt`:
```
cross-domain/grop/grop.ttl;Audited;audit/cross-domain-grop-ontology-quality-audit-<re-audit-date>.md;<publish-date>
```

## Annex — commands used (literal)

```bash
# store 1 — kernel + first protocol + grounding sidecar (strict mode, parse witness)
oxigraph load --location /tmp/sb-grop-kernel-1010 \
  --file ontologies/cross-domain/grop/grop.ttl \
  --file ontologies/cross-domain/grop/protocols/valueflows.ttl \
  --file ontologies/cross-domain/grop/alignments/grop-bfo-2020.ttl        # => clean

# SHACL Core (rudof 0.2.8)
rudof shacl-validate -s ontologies/cross-domain/grop/grop.shapes.ttl \
  ontologies/cross-domain/grop/grop.ttl \
  ontologies/cross-domain/grop/protocols/valueflows.ttl                   # => No Errors found

# five artifact gates + supplements (all: header row only = 0 rows = PASS)
oxigraph query --location /tmp/sb-grop-kernel-1010 --results-format csv \
  --query-file _bmad/work/ks-holonic-cartography-2026-07-07/P3-standard/gates/G1b-artifact.rq
#   idem G2-artifact.rq, G3-artifact.rq, G4-kernel-cohesion-artifact.rq, ST4-artifact.rq,
#   F5-1-no-commerce-leak.rq, F5-2-borrow-provenance.rq

# BFO grounding gate + negative control
oxigraph query --location /tmp/sb-grop-kernel-1010 --results-format csv \
  --query-file ontologies/cross-domain/grop/queries/grounding-gate-bfo.rq # => 0 rows (PASS)
oxigraph load --location /tmp/sb-grop-negctrl-1010 \
  --file ontologies/cross-domain/grop/grop.ttl                            # alignment omitted
oxigraph query --location /tmp/sb-grop-negctrl-1010 --results-format csv \
  --query-file ontologies/cross-domain/grop/queries/grounding-gate-bfo.rq
# => 3 rows: grop#ConcreteProtocol, grop#Kernel, grop#Phase (gate fires — PROVEN live)

# CQ corpus gates
rudof shacl-validate -s ontologies/cross-domain/cq/cq.shapes.ttl \
  ontologies/cross-domain/cq/cq.ttl ontologies/cross-domain/cq/cq-cqs.ttl \
  ontologies/cross-domain/grop/grop-cqs.ttl                               # => No Errors found
oxigraph load --location /tmp/sb-cq-binding-1010 --file cq.ttl --file cq-cqs.ttl \
  --file ../grop/grop-cqs.ttl
oxigraph query --location /tmp/sb-cq-binding-1010 --results-format csv \
  --query-file ontologies/cross-domain/cq/queries/binding-coherence-gate.rq  # => 0 rows

# ADR-134 pins
git hash-object grop.ttl grop.shapes.ttl grop.shex grop-style-guide.md \
  grop-cqs.ttl alignments/grop-bfo-2020.ttl queries/grounding-gate-bfo.rq
```

Audit closed 2026-07-10 — S-B session, GROP publication phase
(`_bmad/work/ks-holonic-cartography-2026-07-07/PUBLISH-GROP/`). Sign-off chain: ADR-140
posture (S-A arbitrage) → this S-B audit → Sacha countersignature required for any promotion,
whitelist row, mirror staging, or IRI publication.

---

# S-B′ — re-audit delta (2026-07-11)

> **Subject**: the B1+B2 lift landed as commit `c45da42` (`grop.ttl` 0.1.1, `grop.shapes.ttl`
> 0.1.1, `grop.shex` 0.1.1, `grop-style-guide.md` re-aligned). Lift is **annotation-only on the
> kernel**: zero structural triple added or removed; the node contract of the companions is
> unchanged. Scope of this delta: re-verify the two failed floor invariants, re-run the full
> mechanical corpus, re-pin hashes (ADR-134), restate the aggregate. Everything else in the
> 2026-07-10 audit stands unmodified.

## Blocker closure

| Blocker | Lift delivered | Re-verification (live 2026-07-11) | Floor verdict |
|---|---|---|---|
| **B1 (F-SB-3, §3.2)** | `skos:scopeNote` on **15/15** grop: entities (bar: ≥80% of 13 signifying); `skos:prefLabel` added on `grop:kernel`/`grop:phase`/`grop:rolesBorrow`; `rdfs:comment` added on `grop:offerRole`/`grop:rolesBorrow`; style guide §4 codifies **5** lexical layers | SPARQL count over the loaded kernel: 15 distinct grop: subjects carry `skos:scopeNote` | **§3.2 → PASS** |
| **B2 (F-SB-4, §3.5)** | explicit `sh:severity sh:Violation` on all 12 node shapes + all 8 property shapes (20 occurrences); SHACL Core only, no new constraint | rudof `No Errors found` over grop.ttl 0.1.1 + valueflows.ttl; negative control (phase outside triad + self-minted `grop:speaks` object) fires **4 violations** — severities are live, not inert | **§3.5 → PASS** |

Also lifted in the same commit: **F-SB-2** (license now `<https://creativecommons.org/licenses/by-sa/4.0/>`
in grop.ttl and grop.shapes.ttl — valueflows.ttl keeps the literal pending the F-SB-1 decision)
and **F-SB-7** (`owl:versionIRI <…/cross-domain/grop/0.1.1>` on the kernel header).

## Mechanical evidence (full re-run, live)

| Check | Result | Verdict |
|---|---|---|
| rudof SHACL Core (shapes 0.1.1 over grop.ttl 0.1.1 + valueflows.ttl) | `No Errors found` | **PROVEN** |
| Negative control (mutated fixture, /tmp) | 4 violations | **PROVEN** — shapes fire |
| G1b / G2 / G3 / G4 / ST4 (artifact tier, Oxigraph) | header-only ×5 (0 rows) | **PROVEN** |
| BFO grounding gate (sidecar 0.2.0 co-loaded) | 0 rows | **PROVEN** |
| cq: binding-coherence gate (grop-cqs.ttl co-loaded) | 0 rows | **PROVEN** |
| cq: BFO grounding gate + cq: SHACL | 0 rows / `No Errors found` | **PROVEN** |
| scopeNote coverage (SPARQL COUNT) | 15/15 | **PROVEN** |
| Companion line-reference traceability | every grop.ttl anchor cited by shapes/shex/style-guide re-verified against the 0.1.1 file (3 drifts corrected in the lift: inverted lane span, VC-borrow off-by-one, kernel-block span) | **PROVEN manually** |

Carried unchanged from 2026-07-10: mechanical ShEx syntax validation remains **UNVERIFIED**
(F-SB-8 — no parity script, `rudof shex` unavailable); parity holds by manual structural
comparison, unaffected by the lift (annotations and comments only on the ShEx side).

## ADR-134 re-pinning table (supersedes the 2026-07-10 table)

| Artifact | Content hash (git hash-object) | Version |
|---|---|---|
| `grop.ttl` | `7ede6bba08f602135b62b9923fd18764ae3961ef` | 0.1.1 |
| `grop.shapes.ttl` | `6a472e5b0c2fee03c03c7b4d9918568da1fa9ab3` | 0.1.1 |
| `grop.shex` | `c280a6162cc16ea8121a873e510d032fd3cd45c9` | 0.1.1 |
| `grop-style-guide.md` | `c47c2354942a7506e17a74e0ef04fb9a5bffe376` | — |
| `grop-cqs.ttl` | `89b6bf8c1de4f771544378efcb7e7cba8b64a949` | 0.1.0 (unchanged) |
| `grop-cqs.md` | `7e3db405b75d587591e24ade6da26cc79f6d133e` | — (unchanged) |
| `alignments/grop-bfo-2020.ttl` | `7e76c12c8b626e1cb42edadec0045c9edbabfa29` | 0.2.0 (unchanged) |
| `queries/grounding-gate-bfo.rq` | `221bc21d94b824d0ffa8304d3d4b7a14ce4397c9` | — (unchanged) |

`protocols/valueflows.ttl` remains deliberately unpinned (F-SB-1 open, working-tree blob
`a13f027`, Sacha decision owed: commit or revert).

## Findings status after the lift

| Finding | Status |
|---|---|
| F-SB-1 (valueflows.ttl uncommitted diff) | **OPEN** — Sacha decision owed |
| F-SB-2 (license literal form) | **LIFTED** on grop.ttl + grop.shapes.ttl; residual on valueflows.ttl rides F-SB-1 |
| F-SB-3 = B1 | **LIFTED** (§3.2 PASS) |
| F-SB-4 = B2 | **LIFTED** (§3.5 PASS) |
| F-SB-5 (R4 machine-readable OntoClean) | OPEN, non-blocking — kernel 0.2.x roadmap |
| F-SB-6 (cq: 0.1.0 DRAFT unaudited) | OPEN, Completeness warning — cq: audit is its own session |
| F-SB-7 (kernel versionIRI) | **LIFTED** |
| F-SB-8 (parity/coverage scripts absent, ShEx mechanical UNVERIFIED) | OPEN, recorded — CI-intent debt |

## Restated verdict

**Floor: 9/9 PASS. Dimensions: Clarity → PASS, Consistency → PASS; Accuracy and Completeness
keep their named warnings (F-SB-5, F-SB-6). Aggregate: PASS — this re-audit RECOMMENDS
AUDITED (`omat:Audited`) for `cross-domain/grop` 0.1.1.**

Promotion, whitelist rows (both gates), bra0-ns mirror staging and IRI publication remain
**Sacha-only acts**. Actionable whitelist rows (pins updated to 0.1.1):

bra0_meta `ontologies/docs-published.txt`:
```
ontologies/cross-domain/grop/grop.ttl  2026-07-11  PASS  sachaR063R  # pin 7ede6bba + BFO sidecar 7e76c12c (ADR-134); S-B′ lifts CONDITIONAL 2026-07-10
```

bra0-ns `docs-published.txt`:
```
cross-domain/grop/grop.ttl;Audited;audit/cross-domain-grop-ontology-quality-audit-2026-07-10.md;<publish-date>
```

Re-audit delta closed 2026-07-11 — S-B′ (same session chain). Sacha countersignature required
for promotion and every publication act.
