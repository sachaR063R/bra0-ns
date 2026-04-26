#!/usr/bin/env python3
"""build-namespace-landings.py — S2 v1 namespace publication helper.

Implements ADR-058 (Voie A). Reads docs-published.txt as the single trigger.
For each whitelisted TTL:
  - Copies the raw TTL to _site/<dir>/<basename>.ttl
  - If TTL is in SHAPES_SKIP (SHACL-only, ADR-058 §2.10): stop after copy.
  - Otherwise runs pyLODE to render _site/<dir>/<basename>.html, then injects
    (in order) audit-meta block, sibling nav, and (if mirror) banner.
  - For canonical TTLs only: copies the rendered HTML to _site/<dir>/index.html
    and injects <link rel="alternate" type="text/turtle"> in <head>.
  - For STATIC_LANDINGS directories (ADR-058 §2.11): copies a hand-written
    layout file to _site/<dir>/index.html.
  - Hard-fails on any missing TTL, pyLODE error, or failed injection.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # repo root
SITE = ROOT / "_site"
WHITELIST = ROOT / "docs-published.txt"

# ADR-058 §2.2 (Voie A) — canonical TTL per namespace directory rendered via pyLODE.
# `evidence-os/query/` is intentionally absent: it carries SHACL-only shapes
# and is served by a hand-written static landing per §2.11.
CANONICAL_TTL: dict[str, str] = {
    "agent-service-contract": "agent-service-contract.ttl",
    "essence-kernel": "essence-kernel.ttl",
    "capability": "capability-operations.ttl",
    "evidence-os": "evidence-os.ttl",
    "evidence-os/edcc": "edcc-bridge.ttl",
}

# ADR-058 §2.4 — known foreign-namespace mirrors.
# Adding a new mirror requires Sacha-only edit, similar to whitelist discipline.
MIRRORS: dict[str, str] = {
    "capability/edgy.ttl": "http://www.omyn.ai/schema/edgy#",
    "capability/retroeng.ttl": "https://omyn.ai/schema/retroeng#",
    "capability/neuro-upper.ttl": "urn:omyn:neuro:",
}

# ADR-058 §2.10 (Voie A) — SHACL-only TTLs that pyLODE cannot render.
# Raw TTL is still copied to _site/, but no HTML is produced and no
# post-processing runs. v2 will replace this skip-set with a Rust SHACL→HTML
# renderer (Voie B, separate ADR).
SHAPES_SKIP: set[str] = {
    "agent-service-contract/agent-service-contract.shapes.ttl",
    "evidence-os/evo-story.shapes.ttl",
    "evidence-os/evo-change-pipeline.shapes.ttl",
    "evidence-os/evo-test-evidence.shapes.ttl",
    "evidence-os/evo-ambient-agent-policy.shapes.ttl",
    "evidence-os/query/evoQ-kpi-shapes.shapes.ttl",
    "evidence-os/edcc/edcc-pemd.shapes.ttl",
    "evidence-os/edcc/edcc-csrd.shapes.ttl",
}

# ADR-058 §2.11 (Voie A) — directories served by a hand-written static landing
# rather than a pyLODE-rendered canonical TTL.
STATIC_LANDINGS: dict[str, str] = {
    "evidence-os/query": "_layouts/evidence-os-query-landing.html",
}


def fail(msg: str) -> None:
    print(f"::error::{msg}", file=sys.stderr)
    sys.exit(1)


def parse_whitelist() -> list[dict]:
    entries: list[dict] = []
    for raw in WHITELIST.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(";")
        if len(parts) != 4:
            fail(f"Malformed whitelist line: {raw!r}")
        ttl, badge, audit, date = (p.strip() for p in parts)
        path = Path(ttl)
        entries.append(
            {
                "ttl": ttl,
                "badge": badge,
                "audit": audit,
                "date": date,
                "dir": str(path.parent),
                "filename": path.name,
                "basename": path.stem,
            }
        )
    return entries


def is_canonical(entry: dict) -> bool:
    return CANONICAL_TTL.get(entry["dir"]) == entry["filename"]


def is_mirror(entry: dict) -> bool:
    return entry["ttl"] in MIRRORS


def render(entry: dict) -> Path | None:
    """Render a whitelisted TTL.

    Always copies the raw TTL into _site/. Returns the rendered HTML path,
    or None if the entry is in SHAPES_SKIP (raw-TTL-only).
    """
    src = ROOT / entry["ttl"]
    if not src.exists():
        fail(f"Whitelisted TTL missing: {entry['ttl']}")
    out_dir = SITE / entry["dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    # Raw Turtle alongside the rendered HTML.
    shutil.copy2(src, out_dir / entry["filename"])
    if entry["ttl"] in SHAPES_SKIP:
        # ADR-058 §2.10 — SHACL-only file, skip pyLODE.
        return None
    out_html = out_dir / f"{entry['basename']}.html"
    result = subprocess.run(
        ["pylode", str(src), "-o", str(out_html)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail(
            f"pyLODE failed on {entry['ttl']}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    if not out_html.exists():
        fail(f"pyLODE produced no output for {entry['ttl']}")
    return out_html


def inject_block(html: str, block: str, label: str) -> str:
    """Insert block immediately before </header>, or after <body> as fallback."""
    new_html, n = re.subn(r"(</header>)", block + r"\1", html, count=1)
    if n == 0:
        new_html, n = re.subn(r"(<body[^>]*>)", r"\1" + block, html, count=1)
    if n == 0:
        fail(f"Could not inject {label} (no </header> or <body> anchor found)")
    return new_html


def inject_audit_meta(html: str, entry: dict) -> str:
    depth = entry["dir"].count("/") + 1
    audit_rel = "../" * depth + entry["audit"]
    block = (
        '<aside class="ns-audit-meta" '
        'style="background:#e7f3ff;border-left:4px solid #0066cc;'
        'padding:0.7em 1em;margin:1em 0;font-size:0.9em;">'
        f'Badge: <strong>{entry["badge"]}</strong> · '
        f'Audit: <a href="{audit_rel}">{Path(entry["audit"]).name}</a> · '
        f'Published: {entry["date"]}'
        "</aside>"
    )
    return inject_block(html, block, "audit-meta")


def inject_mirror_banner(html: str, entry: dict) -> str:
    canonical_iri = MIRRORS[entry["ttl"]]
    block = (
        '<aside class="ns-mirror-banner" '
        'style="background:#fff3cd;border-left:4px solid #ffc107;'
        'padding:1em;margin:1em 0;font-size:0.95em;">'
        "<strong>External vocabulary — documentation mirror.</strong> "
        f"Canonical IRI: <code>&lt;{canonical_iri}&gt;</code>. "
        "Fragment resolution does not apply on schema.bra0.org for "
        "this vocabulary; this page exists for documentation "
        "traceability only."
        "</aside>"
    )
    new_html = inject_block(html, block, "mirror-banner")
    if "ns-mirror-banner" not in new_html:
        fail(f"Mirror banner not found in output for {entry['ttl']} after injection")
    return new_html


def inject_siblings_nav(html: str, entry: dict, all_entries: list[dict]) -> str:
    siblings = [
        e for e in all_entries if e["dir"] == entry["dir"] and e["ttl"] != entry["ttl"]
    ]
    if not siblings:
        return html
    items: list[str] = []
    for sib in siblings:
        if is_canonical(sib):
            label = " <em>(canonical)</em>"
        elif is_mirror(sib):
            label = " <em>(external mirror)</em>"
        else:
            label = ""
        items.append(
            f'<li><a href="{sib["basename"]}.html">{sib["filename"]}</a>{label}</li>'
        )
    block = (
        '<nav class="ns-siblings" '
        'style="background:#f5f5f5;padding:0.7em 1em;margin:1em 0;font-size:0.9em;">'
        "<strong>Other vocabularies in this directory:</strong>"
        f'<ul style="margin:0.3em 0 0 1.5em;">{"".join(items)}</ul>'
        "</nav>"
    )
    return inject_block(html, block, "siblings-nav")


def inject_alternate_link(html: str, entry: dict) -> str:
    link = f'<link rel="alternate" type="text/turtle" href="{entry["filename"]}">'
    new_html, n = re.subn(r"(</head>)", link + r"\1", html, count=1)
    if n == 0:
        fail(f"<head> not found for canonical {entry['ttl']}")
    return new_html


def post_process(html_path: Path, entry: dict, all_entries: list[dict]) -> None:
    html = html_path.read_text(encoding="utf-8")
    html = inject_audit_meta(html, entry)
    html = inject_siblings_nav(html, entry, all_entries)
    if is_mirror(entry):
        html = inject_mirror_banner(html, entry)
    if is_canonical(entry):
        html = inject_alternate_link(html, entry)
    html_path.write_text(html, encoding="utf-8")


def copy_canonicals_to_index() -> None:
    for ns_dir, canonical_filename in CANONICAL_TTL.items():
        canonical_html = SITE / ns_dir / canonical_filename.replace(".ttl", ".html")
        index_html = SITE / ns_dir / "index.html"
        if not canonical_html.exists():
            fail(f"Canonical render missing: {canonical_html.relative_to(ROOT)}")
        shutil.copy2(canonical_html, index_html)
        print(f"  ✓ {ns_dir}/index.html ← {canonical_filename}")
    # ADR-058 §2.11 — static landings copied verbatim from _layouts/.
    for ns_dir, layout_rel in STATIC_LANDINGS.items():
        layout_path = ROOT / layout_rel
        index_html = SITE / ns_dir / "index.html"
        if not layout_path.exists():
            fail(f"Static layout missing: {layout_rel}")
        index_html.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(layout_path, index_html)
        print(f"  ✓ {ns_dir}/index.html ← {layout_rel} (static)")


def verify_count(entries: list[dict]) -> None:
    rendered = sorted(
        p
        for p in SITE.rglob("*.html")
        if p.name != "index.html" and p.parent != SITE
    )
    expected = [e for e in entries if e["ttl"] not in SHAPES_SKIP]
    if len(rendered) != len(expected):
        fail(
            f"Whitelist/HTML count mismatch: "
            f"{len(expected)} ontology entries vs {len(rendered)} rendered files "
            f"(of {len(entries)} whitelist entries, "
            f"{len(entries) - len(expected)} are SHACL-only)"
        )
    print(
        f"  ✓ Ontology HTML count = {len(rendered)} "
        f"(of {len(entries)} whitelist entries; "
        f"{len(entries) - len(rendered)} SHACL-only skipped)"
    )


def main() -> None:
    if not WHITELIST.exists():
        print("Bootstrap phase: no whitelist file. Skipping.")
        return

    entries = parse_whitelist()
    if not entries:
        print("Bootstrap phase: empty whitelist. Skipping.")
        return

    SITE.mkdir(exist_ok=True)
    print(f"Rendering {len(entries)} whitelisted TTLs ...")
    for e in entries:
        html_path = render(e)
        if html_path is None:
            # SHAPES_SKIP — raw TTL only, no HTML, no post-processing.
            print(f"  ✓ {e['ttl']} → raw TTL only (SHACL-only, ADR-058 §2.10)")
            continue
        post_process(html_path, e, entries)
        print(f"  ✓ {e['ttl']} → {html_path.relative_to(ROOT)}")

    print("Promoting canonicals + static landings to index.html ...")
    copy_canonicals_to_index()

    print("Verifying counts ...")
    verify_count(entries)

    n_landings = len(CANONICAL_TTL) + len(STATIC_LANDINGS)
    print(
        f"\n✓ Build complete: {len(entries)} whitelist entries, "
        f"{n_landings} directory landings "
        f"({len(CANONICAL_TTL)} canonical + {len(STATIC_LANDINGS)} static)."
    )


if __name__ == "__main__":
    main()
