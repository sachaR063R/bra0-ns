# bra0-ns

Namespace registry serving `https://schema.bra0.org/*` — the canonical
resolution host for bra0 RDF vocabularies.

## Scope

This repository hosts the HTML + Turtle renderings of every bra0
product-facing RDF vocabulary whose namespace root is `schema.bra0.org`.

Current in-scope namespaces (ratified 2026-04-17):

- `cap:` → `https://schema.bra0.org/capability#` (capability operations)
- `bra0m:` → `https://schema.bra0.org/module#` (module registry)
- `evo:` → `https://schema.bra0.org/evidence-os#` (Evidence OS vocabulary)
- `evoQ:` → `https://schema.bra0.org/evidence-os/query#` (SHACL result shapes)

Out of scope (hosted elsewhere):

- `asc:` → `https://schema.bra0.org/agent-service-contract#`
- `ess:` → `https://schema.bra0.org/essence-kernel#`

## This repo is a publication target, not a source of truth

The authoritative source for every TTL in `ns/` lives in the private
governance repository `bra0_meta`, under `ontologies/governance/`. Files
arrive here only after they pass a 6-dimension ontology quality audit and Sacha
explicitly approves publication (ADR-054 discipline).

Do not edit the TTL files here directly. All modifications flow
`bra0_meta → (ontology quality audit) → Sacha review → publish script → this repo`.

## Publication discipline (ADR-054)

Every published ontology carries one of four badges:

- **DRAFT** — published for peer visibility, no external validation.
- **PROPOSED** — submitted to an external authority (W3C, OMG, peer-reviewed venue), no sign-off yet.
- **ADOPTED** — accepted by an external authority.
- **DEPRECATED** — superseded; IRIs remain resolvable, banner redirects.

Default is DRAFT. Production-grade badges require evidence in `audit/`.

## Namespace resolution pattern

IRI `https://schema.bra0.org/evidence-os#Commit` resolves as follows:

- Browser / LLM crawler → `ns/evidence-os/index.html` (pylode-rendered)
- RDF tooling → `ns/evidence-os/evidence-os.ttl` (raw Turtle)
- Fragment `#Commit` → HTML anchor inside `index.html`

Content negotiation (Accept-header routing) is not supported by GitHub
Pages natively; the HTML and TTL are exposed as distinct URLs. The
fragment IRI resolves to the HTML by default. A future Cloudflare
Workers layer can add content negotiation without breaking any IRI.

## Build

`.github/workflows/pages.yml` regenerates `_site/` from `ns/**/*.ttl`
using [pyLODE](https://github.com/RDFLib/pyLODE) (v3.x, Apache-2.0,
Australian Linked Data Working Group).

`.github/workflows/validate.yml` runs [rudof](https://github.com/rudof-project/rudof)
SHACL validation on every TTL listed in `docs-published.txt`. Ratchet
floor = 50 violations (audit-orthogonal coupled-stack baseline).

Both workflows are no-op pass-through during the bootstrap phase
(no ontologies whitelisted yet) and activate on first publication.

## Governance

- **Single controller**: Sacha Roger (`sachaR063R <sacha@omyn.ai>`).
- **Commits**: Sacha-only. No AI attribution.
- **ontology quality gate**: `docs-published.txt` is the whitelist. No whitelist
  entry = no publication.
- **Legal**: dual-licensed MIT OR Apache-2.0 (see `LICENSE-MIT`,
  `LICENSE-APACHE`). Individual TTL files may carry a distinct license
  header (typically CC-BY-SA-4.0 for the ontology content itself).

## Related

- Project documentation: https://bra0.org/
- Source repository (product): https://github.com/sachaR063R/bra0
- Governance repository (private): bra0_meta (internal)
- ADR-054 publication discipline: maintained in the governance repository
- ADR-056 domain acquisition: maintained in the governance repository
