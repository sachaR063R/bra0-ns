"""Unit + integration tests for build_namespace_landings.

Specification source: ADR-058 — Namespace landing contract.

The tests below are the executable contract. The orchestrator script must
satisfy them. Any change in injection order, mirror-banner wording, audit
relative-path computation, or whitelist parsing semantics MUST be reflected
here first (RED), then in the script (GREEN).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

import build_namespace_landings as B


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


MINIMAL_PYLODE_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Test Ontology</title></head>
<body>
<header><h1>Test Ontology</h1></header>
<main><section id="Foo">Foo class</section></main>
</body>
</html>
"""


HTML_WITHOUT_HEADER_OR_BODY = """\
<!DOCTYPE html>
<html>
<head><title>Pathological</title></head>
</html>
"""


def make_entry(
    ttl: str,
    *,
    badge: str = "DRAFT",
    audit: str = "audit/test-audit.md",
    date: str = "2026-04-26",
) -> dict:
    """Build a whitelist entry the way parse_whitelist would."""
    path = Path(ttl)
    return {
        "ttl": ttl,
        "badge": badge,
        "audit": audit,
        "date": date,
        "dir": str(path.parent),
        "filename": path.name,
        "basename": path.stem,
    }


# ---------------------------------------------------------------------------
# parse_whitelist
# ---------------------------------------------------------------------------


def test_parse_whitelist_skips_comments_and_blank_lines(tmp_path, monkeypatch):
    wl = tmp_path / "docs-published.txt"
    wl.write_text(
        "# header comment\n"
        "\n"
        "agent-service-contract/agent-service-contract.ttl;DRAFT;audit/a.md;2026-04-23\n"
        "  \n"
        "# another comment\n"
        "essence-kernel/essence-kernel.ttl;PROPOSED;audit/b.md;2026-04-24\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(B, "WHITELIST", wl)
    entries = B.parse_whitelist()
    assert len(entries) == 2
    assert entries[0]["ttl"] == "agent-service-contract/agent-service-contract.ttl"
    assert entries[0]["badge"] == "DRAFT"
    assert entries[1]["badge"] == "PROPOSED"


def test_parse_whitelist_fails_on_malformed_line(tmp_path, monkeypatch):
    wl = tmp_path / "docs-published.txt"
    wl.write_text("only-two-fields;DRAFT\n", encoding="utf-8")
    monkeypatch.setattr(B, "WHITELIST", wl)
    with pytest.raises(SystemExit):
        B.parse_whitelist()


def test_parse_whitelist_extracts_dir_filename_basename(tmp_path, monkeypatch):
    wl = tmp_path / "docs-published.txt"
    wl.write_text(
        "evidence-os/edcc/edcc-bridge.ttl;DRAFT;audit/x.md;2026-04-23\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(B, "WHITELIST", wl)
    e = B.parse_whitelist()[0]
    assert e["dir"] == "evidence-os/edcc"
    assert e["filename"] == "edcc-bridge.ttl"
    assert e["basename"] == "edcc-bridge"


# ---------------------------------------------------------------------------
# is_canonical / is_mirror
# ---------------------------------------------------------------------------


def test_is_canonical_true_for_mapped_basename():
    assert B.is_canonical(make_entry("essence-kernel/essence-kernel.ttl"))


def test_is_canonical_false_for_non_mapped_basename():
    assert not B.is_canonical(
        make_entry("agent-service-contract/agent-service-contract.shapes.ttl")
    )


def test_is_canonical_false_for_unknown_dir():
    assert not B.is_canonical(make_entry("does-not-exist/whatever.ttl"))


def test_is_mirror_true_for_known_path():
    # ADR-060 §3 — only neuro-upper remains a mirror after edgy migrated to
    # canonical (cross-domain/edgy/) and retroeng was unpublished.
    assert B.is_mirror(make_entry("capability/neuro-upper.ttl"))


def test_is_mirror_false_for_canonical_in_same_dir():
    assert not B.is_mirror(make_entry("capability/capability-operations.ttl"))


def test_is_mirror_false_for_migrated_edgy():
    """ADR-060 §3 — cross-domain/edgy/edgy.ttl is canonical, not a mirror."""
    assert not B.is_mirror(make_entry("cross-domain/edgy/edgy.ttl"))


def test_is_canonical_true_for_cross_domain_edgy():
    """ADR-060 §3 — cross-domain/edgy/ promoted to canonical landing dir."""
    assert B.is_canonical(make_entry("cross-domain/edgy/edgy.ttl"))


def test_canonical_and_mirror_are_disjoint():
    """ADR-058 invariant: a TTL cannot be both canonical and a mirror."""
    for ttl in B.MIRRORS:
        assert not B.is_canonical(make_entry(ttl)), (
            f"{ttl} is registered as both canonical and mirror — invariant broken"
        )


# ---------------------------------------------------------------------------
# inject_audit_meta — depth-aware relative-path computation
# ---------------------------------------------------------------------------


def test_inject_audit_meta_depth_1_path():
    entry = make_entry("agent-service-contract/agent-service-contract.ttl")
    out = B.inject_audit_meta(MINIMAL_PYLODE_HTML, entry)
    assert 'href="../audit/test-audit.md"' in out


def test_inject_audit_meta_depth_2_path():
    entry = make_entry("evidence-os/edcc/edcc-bridge.ttl")
    out = B.inject_audit_meta(MINIMAL_PYLODE_HTML, entry)
    assert 'href="../../audit/test-audit.md"' in out


def test_inject_audit_meta_contains_badge_and_date():
    entry = make_entry(
        "essence-kernel/essence-kernel.ttl",
        badge="PROPOSED",
        date="2026-05-15",
    )
    out = B.inject_audit_meta(MINIMAL_PYLODE_HTML, entry)
    assert "PROPOSED" in out
    assert "2026-05-15" in out


def test_inject_audit_meta_uses_audit_basename_in_link_text():
    entry = make_entry(
        "evidence-os/evidence-os.ttl",
        audit="audit/very-long-name-2026-04-22.md",
    )
    out = B.inject_audit_meta(MINIMAL_PYLODE_HTML, entry)
    # Visible link text = basename, not full path
    assert ">very-long-name-2026-04-22.md</a>" in out


def test_inject_audit_meta_fails_on_html_with_no_anchor():
    entry = make_entry("essence-kernel/essence-kernel.ttl")
    with pytest.raises(SystemExit):
        B.inject_audit_meta(HTML_WITHOUT_HEADER_OR_BODY, entry)


# ---------------------------------------------------------------------------
# inject_mirror_banner
# ---------------------------------------------------------------------------


def test_inject_mirror_banner_contains_canonical_iri():
    entry = make_entry("capability/neuro-upper.ttl")
    out = B.inject_mirror_banner(MINIMAL_PYLODE_HTML, entry)
    assert "ns-mirror-banner" in out
    assert "urn:omyn:neuro:" in out


def test_inject_mirror_banner_contains_disclaimer_text():
    entry = make_entry("capability/neuro-upper.ttl")
    out = B.inject_mirror_banner(MINIMAL_PYLODE_HTML, entry)
    assert "External vocabulary" in out
    assert "documentation mirror" in out
    assert "Fragment resolution does not apply" in out


def test_inject_mirror_banner_fails_on_html_with_no_anchor():
    entry = make_entry("capability/neuro-upper.ttl")
    with pytest.raises(SystemExit):
        B.inject_mirror_banner(HTML_WITHOUT_HEADER_OR_BODY, entry)


# ---------------------------------------------------------------------------
# inject_siblings_nav
# ---------------------------------------------------------------------------


def test_inject_siblings_nav_lists_others_in_same_dir():
    self_entry = make_entry("agent-service-contract/agent-service-contract.shapes.ttl")
    canonical = make_entry("agent-service-contract/agent-service-contract.ttl")
    out = B.inject_siblings_nav(
        MINIMAL_PYLODE_HTML, self_entry, [self_entry, canonical]
    )
    assert "agent-service-contract.ttl" in out
    assert 'href="agent-service-contract.html"' in out


def test_inject_siblings_nav_omits_self():
    self_entry = make_entry("agent-service-contract/agent-service-contract.shapes.ttl")
    other = make_entry("agent-service-contract/agent-service-contract.ttl")
    out = B.inject_siblings_nav(MINIMAL_PYLODE_HTML, self_entry, [self_entry, other])
    # self listed nowhere
    assert "agent-service-contract.shapes.ttl" not in out
    assert 'href="agent-service-contract.shapes.html"' not in out


def test_inject_siblings_nav_marks_canonical_with_label():
    self_entry = make_entry("agent-service-contract/agent-service-contract.shapes.ttl")
    canonical = make_entry("agent-service-contract/agent-service-contract.ttl")
    out = B.inject_siblings_nav(
        MINIMAL_PYLODE_HTML, self_entry, [self_entry, canonical]
    )
    assert "(canonical)" in out


def test_inject_siblings_nav_marks_external_mirror_with_label():
    self_entry = make_entry("capability/capability-operations.ttl")
    mirror = make_entry("capability/neuro-upper.ttl")
    out = B.inject_siblings_nav(MINIMAL_PYLODE_HTML, self_entry, [self_entry, mirror])
    assert "(external mirror)" in out


def test_inject_siblings_nav_no_op_when_alone_in_dir():
    self_entry = make_entry("essence-kernel/essence-kernel.ttl")
    out = B.inject_siblings_nav(MINIMAL_PYLODE_HTML, self_entry, [self_entry])
    assert "ns-siblings" not in out


def test_inject_siblings_nav_excludes_other_directories():
    self_entry = make_entry("capability/capability-operations.ttl")
    other_dir = make_entry("essence-kernel/essence-kernel.ttl")
    out = B.inject_siblings_nav(
        MINIMAL_PYLODE_HTML, self_entry, [self_entry, other_dir]
    )
    assert "essence-kernel.ttl" not in out


# ---------------------------------------------------------------------------
# inject_alternate_link
# ---------------------------------------------------------------------------


def test_inject_alternate_link_present_in_head():
    entry = make_entry("essence-kernel/essence-kernel.ttl")
    out = B.inject_alternate_link(MINIMAL_PYLODE_HTML, entry)
    # Inserted before </head>
    assert re.search(
        r'<link rel="alternate" type="text/turtle" href="essence-kernel\.ttl">\s*</head>',
        out,
    )


def test_inject_alternate_link_fails_when_no_head_close():
    entry = make_entry("essence-kernel/essence-kernel.ttl")
    bad = "<html><body>nope</body></html>"
    with pytest.raises(SystemExit):
        B.inject_alternate_link(bad, entry)


# ---------------------------------------------------------------------------
# post_process — composition contract
# ---------------------------------------------------------------------------


def test_post_process_canonical_writes_alternate_link(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "ROOT", tmp_path)
    html_path = tmp_path / "essence-kernel" / "essence-kernel.html"
    html_path.parent.mkdir(parents=True)
    html_path.write_text(MINIMAL_PYLODE_HTML, encoding="utf-8")
    entry = make_entry("essence-kernel/essence-kernel.ttl")
    B.post_process(html_path, entry, [entry])
    out = html_path.read_text(encoding="utf-8")
    assert 'rel="alternate"' in out
    assert "ns-audit-meta" in out


def test_post_process_mirror_writes_banner(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "ROOT", tmp_path)
    html_path = tmp_path / "capability" / "neuro-upper.html"
    html_path.parent.mkdir(parents=True)
    html_path.write_text(MINIMAL_PYLODE_HTML, encoding="utf-8")
    mirror = make_entry("capability/neuro-upper.ttl")
    canonical = make_entry("capability/capability-operations.ttl")
    B.post_process(html_path, mirror, [mirror, canonical])
    out = html_path.read_text(encoding="utf-8")
    assert "ns-mirror-banner" in out
    # Mirrors do not get the alternate link (they are not canonical)
    assert 'rel="alternate"' not in out


def test_post_process_non_canonical_non_mirror_no_banner_no_alternate(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(B, "ROOT", tmp_path)
    html_path = (
        tmp_path / "agent-service-contract" / "agent-service-contract.shapes.html"
    )
    html_path.parent.mkdir(parents=True)
    html_path.write_text(MINIMAL_PYLODE_HTML, encoding="utf-8")
    shape = make_entry(
        "agent-service-contract/agent-service-contract.shapes.ttl"
    )
    canonical = make_entry(
        "agent-service-contract/agent-service-contract.ttl"
    )
    B.post_process(html_path, shape, [shape, canonical])
    out = html_path.read_text(encoding="utf-8")
    assert "ns-mirror-banner" not in out
    assert 'rel="alternate"' not in out
    # but the audit-meta block IS present (every page gets it)
    assert "ns-audit-meta" in out


# ---------------------------------------------------------------------------
# render — fails loudly on missing TTL
# ---------------------------------------------------------------------------


def test_render_fails_on_missing_ttl(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", tmp_path / "_site")
    entry = make_entry("essence-kernel/essence-kernel.ttl")
    with pytest.raises(SystemExit):
        B.render(entry)


def test_render_fails_on_pylode_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", tmp_path / "_site")
    ttl = tmp_path / "essence-kernel" / "essence-kernel.ttl"
    ttl.parent.mkdir(parents=True)
    ttl.write_text("# minimal", encoding="utf-8")
    entry = make_entry("essence-kernel/essence-kernel.ttl")

    class FakeResult:
        returncode = 1
        stdout = ""
        stderr = "synthetic failure"

    monkeypatch.setattr(B.subprocess, "run", lambda *a, **k: FakeResult())
    with pytest.raises(SystemExit):
        B.render(entry)


# ---------------------------------------------------------------------------
# copy_canonicals_to_index — fails loud on missing canonical render
# ---------------------------------------------------------------------------


def test_copy_canonicals_fails_when_canonical_render_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", tmp_path / "_site")
    (tmp_path / "_site").mkdir()
    with pytest.raises(SystemExit):
        B.copy_canonicals_to_index()


def test_copy_canonicals_creates_index_html_per_canonical_dir(tmp_path, monkeypatch):
    site = tmp_path / "_site"
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    for ns_dir, canonical_filename in B.CANONICAL_TTL.items():
        d = site / ns_dir
        d.mkdir(parents=True)
        html_name = canonical_filename.replace(".ttl", ".html")
        (d / html_name).write_text("CANONICAL_BODY", encoding="utf-8")
    # Static landings also need their layout fixture to exist.
    for ns_dir, layout_rel in B.STATIC_LANDINGS.items():
        layout = tmp_path / layout_rel
        layout.parent.mkdir(parents=True, exist_ok=True)
        layout.write_text("STATIC_BODY", encoding="utf-8")
    B.copy_canonicals_to_index()
    for ns_dir in B.CANONICAL_TTL:
        idx = site / ns_dir / "index.html"
        assert idx.exists()
        assert idx.read_text(encoding="utf-8") == "CANONICAL_BODY"
    for ns_dir in B.STATIC_LANDINGS:
        idx = site / ns_dir / "index.html"
        assert idx.exists()
        assert idx.read_text(encoding="utf-8") == "STATIC_BODY"


# ---------------------------------------------------------------------------
# verify_count — invariant guard
# ---------------------------------------------------------------------------


def test_verify_count_passes_when_matching(tmp_path, monkeypatch):
    site = tmp_path / "_site"
    site.mkdir()
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    (site / "a").mkdir()
    (site / "a" / "x.html").write_text("x")
    (site / "a" / "index.html").write_text("idx")  # ignored by counter
    entries = [make_entry("a/x.ttl")]
    B.verify_count(entries)  # should not raise


def test_verify_count_fails_when_mismatch(tmp_path, monkeypatch):
    site = tmp_path / "_site"
    site.mkdir()
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    (site / "a").mkdir()
    (site / "a" / "x.html").write_text("x")
    entries = [
        make_entry("a/x.ttl"),
        make_entry("a/y.ttl"),  # missing render
    ]
    with pytest.raises(SystemExit):
        B.verify_count(entries)


# ---------------------------------------------------------------------------
# CANONICAL_TTL / MIRRORS — registry shape (regression guards)
# ---------------------------------------------------------------------------


def test_canonical_ttl_covers_seven_pylode_rendered_directories():
    """ADR-060 §3 + Co-STORM 2026-04-28 S1 Decision A — seven canonical landings.

    `cross-domain/edgy/` joins the canonical set: edgy is a bra0-authored
    cross-domain ontology hosted at https://schema.bra0.org/cross-domain/edgy#.
    `cross-domain/edgy/motivation-registry/` joins per Q-NS-2 ABox-under-TBox
    pattern — instance-level motivation registry resolves at
    https://schema.bra0.org/cross-domain/edgy/motivation-registry/.
    `evidence-os/query/` remains a static landing (SHACL-only).
    """
    assert set(B.CANONICAL_TTL) == {
        "agent-service-contract",
        "essence-kernel",
        "capability",
        "evidence-os",
        "evidence-os/edcc",
        "cross-domain/edgy",
        "cross-domain/edgy/motivation-registry",
    }


def test_mirrors_covers_one_known_foreign_namespace():
    """ADR-060 §3 — only neuro-upper remains a mirror.

    edgy migrated to canonical (cross-domain/edgy/). retroeng unpublished
    (Sacha decision 2026-04-26 — kept private until deep review).
    """
    assert set(B.MIRRORS) == {
        "capability/neuro-upper.ttl",
    }


def test_mirrors_carries_no_omyn_ai_iri():
    """ADR-060 §4 (rupture sèche) — no MIRROR may point to omyn.ai/schema/*."""
    for path, iri in B.MIRRORS.items():
        assert "omyn.ai/schema" not in iri, (
            f"{path} → {iri} violates the omyn.ai/schema rupture sèche policy"
        )


# ---------------------------------------------------------------------------
# Voie A — SHAPES_SKIP set (ADR-058 §2.10)
# ---------------------------------------------------------------------------


def test_shapes_skip_set_covers_eight_known_files():
    """ADR-058 §2.10 — eight SHACL-only TTLs skip pyLODE rendering."""
    assert set(B.SHAPES_SKIP) == {
        "agent-service-contract/agent-service-contract.shapes.ttl",
        "evidence-os/evo-story.shapes.ttl",
        "evidence-os/evo-change-pipeline.shapes.ttl",
        "evidence-os/evo-test-evidence.shapes.ttl",
        "evidence-os/evo-ambient-agent-policy.shapes.ttl",
        "evidence-os/query/evoQ-kpi-shapes.shapes.ttl",
        "evidence-os/edcc/edcc-pemd.shapes.ttl",
        "evidence-os/edcc/edcc-csrd.shapes.ttl",
    }


def test_shapes_skip_and_canonical_are_disjoint():
    """A canonical TTL can never be in the skip set (would orphan its dir)."""
    canonical_paths = {
        f"{ns_dir}/{filename}" for ns_dir, filename in B.CANONICAL_TTL.items()
    }
    assert canonical_paths.isdisjoint(set(B.SHAPES_SKIP))


def test_shapes_skip_and_mirrors_are_disjoint():
    """A foreign-namespace mirror is never a SHACL-only file."""
    assert set(B.MIRRORS).isdisjoint(set(B.SHAPES_SKIP))


# ---------------------------------------------------------------------------
# Voie A — STATIC_LANDINGS dict (ADR-058 §2.11)
# ---------------------------------------------------------------------------


def test_static_landings_covers_query_and_cross_domain():
    """ADR-058 §2.11 + ADR-060 §3 — two static landings.

    - evidence-os/query/ — SHACL-only result-structure shapes.
    - cross-domain/ — parent grouping for cross-domain ontologies (currently
      only edgy is published; retroeng kept private pending review).
    """
    assert B.STATIC_LANDINGS == {
        "evidence-os/query": "_layouts/evidence-os-query-landing.html",
        "cross-domain": "_layouts/cross-domain-landing.html",
    }


def test_static_landings_and_canonical_are_disjoint():
    """A directory cannot be both canonical and static-landing."""
    assert set(B.STATIC_LANDINGS).isdisjoint(set(B.CANONICAL_TTL))


# ---------------------------------------------------------------------------
# Voie A — render() skips SHAPES_SKIP (still copies raw TTL)
# ---------------------------------------------------------------------------


def test_render_skips_pylode_for_shapes_but_copies_raw_ttl(tmp_path, monkeypatch):
    """ADR-058 §2.10 — shapes get raw TTL only, no pyLODE invocation, no HTML."""
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", tmp_path / "_site")
    ttl_rel = "agent-service-contract/agent-service-contract.shapes.ttl"
    ttl = tmp_path / ttl_rel
    ttl.parent.mkdir(parents=True)
    ttl.write_text("# shapes", encoding="utf-8")
    entry = make_entry(ttl_rel)

    called = {"n": 0}

    def fake_run(*a, **k):  # pragma: no cover - should not be called
        called["n"] += 1
        raise AssertionError("pyLODE must not be invoked for SHAPES_SKIP entries")

    monkeypatch.setattr(B.subprocess, "run", fake_run)
    result = B.render(entry)
    assert result is None
    assert called["n"] == 0
    # Raw TTL was still copied to _site/
    copied = tmp_path / "_site" / ttl_rel
    assert copied.exists()
    # No HTML produced
    html = tmp_path / "_site" / ttl_rel.replace(".ttl", ".html")
    assert not html.exists()


# ---------------------------------------------------------------------------
# Voie A — copy_canonicals_to_index() handles static landings
# ---------------------------------------------------------------------------


def test_copy_canonicals_writes_static_landing_for_query(tmp_path, monkeypatch):
    """ADR-058 §2.11 — static layout copied verbatim to <static-dir>/index.html."""
    site = tmp_path / "_site"
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    # Provide canonical renders for every pyLODE-canonical dir.
    for ns_dir, canonical_filename in B.CANONICAL_TTL.items():
        d = site / ns_dir
        d.mkdir(parents=True)
        html_name = canonical_filename.replace(".ttl", ".html")
        (d / html_name).write_text("CANONICAL_BODY", encoding="utf-8")
    # Provide every static layout file declared in STATIC_LANDINGS.
    for ns_dir, layout_rel in B.STATIC_LANDINGS.items():
        layout = tmp_path / layout_rel
        layout.parent.mkdir(parents=True, exist_ok=True)
        # Body marker per dir to assert the right one lands at the right path.
        marker = "STATIC_QUERY_BODY" if ns_dir == "evidence-os/query" else f"STATIC_{ns_dir.upper().replace('/', '_')}_BODY"
        layout.write_text(marker, encoding="utf-8")
    # Pre-create static landing dirs (would normally be made when their TTLs
    # render — cross-domain has no TTLs of its own, so create explicitly).
    for ns_dir in B.STATIC_LANDINGS:
        (site / ns_dir).mkdir(parents=True, exist_ok=True)

    B.copy_canonicals_to_index()

    idx = site / "evidence-os" / "query" / "index.html"
    assert idx.exists()
    assert idx.read_text(encoding="utf-8") == "STATIC_QUERY_BODY"


def test_copy_canonicals_fails_when_static_layout_missing(tmp_path, monkeypatch):
    """Missing static layout = build failure."""
    site = tmp_path / "_site"
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    for ns_dir, canonical_filename in B.CANONICAL_TTL.items():
        d = site / ns_dir
        d.mkdir(parents=True)
        html_name = canonical_filename.replace(".ttl", ".html")
        (d / html_name).write_text("CANONICAL_BODY", encoding="utf-8")
    (site / "evidence-os" / "query").mkdir(parents=True)
    # NB: no _layouts/ file written.
    with pytest.raises(SystemExit):
        B.copy_canonicals_to_index()


# ---------------------------------------------------------------------------
# β path-shape — emit_flat_ttl_aliases (ADR-058 §2.1 + §2.7 step 11)
# ---------------------------------------------------------------------------


def test_flat_ttl_alias_emitted_for_every_canonical_dir(tmp_path, monkeypatch):
    """ADR-058 §2.7 step 11 — every canonical directory gets a flat-TTL alias.

    For each `<dir>` in CANONICAL_TTL, the build copies
    `_site/<dir>/<canonical-basename>.ttl` to `_site/<dir>.ttl`. Cardinality:
    one flat alias per canonical directory.
    """
    site = tmp_path / "_site"
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    # Stage canonical TTLs as if `render()` had already copied them.
    for ns_dir, canonical_filename in B.CANONICAL_TTL.items():
        d = site / ns_dir
        d.mkdir(parents=True)
        # Marker per dir to assert byte-identical copy lands at the flat path.
        marker = f"CANONICAL_TURTLE_{ns_dir.replace('/', '_')}"
        (d / canonical_filename).write_text(marker, encoding="utf-8")

    B.emit_flat_ttl_aliases()

    for ns_dir, canonical_filename in B.CANONICAL_TTL.items():
        flat = site / f"{ns_dir}.ttl"
        assert flat.exists(), f"Flat alias missing: {flat.relative_to(tmp_path)}"
        marker = f"CANONICAL_TURTLE_{ns_dir.replace('/', '_')}"
        assert flat.read_text(encoding="utf-8") == marker, (
            f"Flat alias content drift at {flat.relative_to(tmp_path)}"
        )


def test_flat_ttl_alias_fails_when_canonical_ttl_missing(tmp_path, monkeypatch):
    """ADR-058 §2.7 step 11 — missing canonical TTL = hard build failure."""
    site = tmp_path / "_site"
    site.mkdir()
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    # No canonical TTL staged.
    with pytest.raises(SystemExit):
        B.emit_flat_ttl_aliases()


def test_flat_ttl_alias_equals_current_source_ttl_after_rebuild(tmp_path, monkeypatch):
    """Diana R2 #3 lift (2026-04-28) — idempotency guard.

    Scenario: a stale `_site/<dir>.ttl` exists from a prior build referencing
    yesterday's TTL content. The current rebuild must emit a flat alias whose
    content equals the CURRENT source TTL, not whatever was cached in _site.

    Asserts that `emit_flat_ttl_aliases()` invoked after a fresh
    `_site/<dir>/<canonical>.ttl` write produces a flat alias whose bytes
    match the current source — never the stale prior content.
    """
    site = tmp_path / "_site"
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    # Restrict CANONICAL_TTL to one entry for this test's scope.
    monkeypatch.setattr(B, "CANONICAL_TTL", {"a/b": "b.ttl"})

    ns_dir, canonical_filename = "a/b", "b.ttl"

    # Stage a STALE flat alias from "yesterday".
    site.mkdir()
    stale_flat = site / f"{ns_dir}.ttl"
    stale_flat.parent.mkdir(parents=True, exist_ok=True)
    stale_flat.write_text("STALE_YESTERDAY_TTL_CONTENT", encoding="utf-8")

    # Stage CURRENT canonical TTL (as if render() just copied it).
    current_dir = site / ns_dir
    current_dir.mkdir(parents=True, exist_ok=True)
    (current_dir / canonical_filename).write_text(
        "CURRENT_SOURCE_TTL_CONTENT", encoding="utf-8"
    )

    B.emit_flat_ttl_aliases()

    # The flat alias must reflect the CURRENT source, not the stale cache.
    assert stale_flat.read_text(encoding="utf-8") == "CURRENT_SOURCE_TTL_CONTENT", (
        "Flat alias serves stale content — Diana #3 regression"
    )


def test_main_wipes_site_before_rebuild(tmp_path, monkeypatch):
    """Diana R2 #3 lift (2026-04-28) — `_site/` wiped at start of main().

    Asserts that `main()` removes any pre-existing `_site/` tree before
    invoking the build pipeline. This is the structural guard that keeps
    cached state from leaking into the next build.
    """
    site = tmp_path / "_site"
    wl = tmp_path / "docs-published.txt"
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    monkeypatch.setattr(B, "WHITELIST", wl)

    # Pre-populate _site with a stale artefact that should NOT survive.
    site.mkdir()
    (site / "stale.ttl").write_text("STALE_ARTEFACT", encoding="utf-8")

    # Empty whitelist makes main() exit early after the wipe-and-mkdir;
    # but actually the wipe happens AFTER the empty-whitelist check, so
    # use a whitelist with a non-existent TTL to force the wipe path
    # then fail at render. The wipe must happen first.
    wl.write_text(
        "fake/fake.ttl;DRAFT;audit/fake.md;2026-04-28\n", encoding="utf-8"
    )

    with pytest.raises(SystemExit):
        B.main()

    # The stale artefact must be gone (wipe happened before render-fail).
    assert not (site / "stale.ttl").exists(), (
        "Stale _site/ artefact survived rebuild — Diana #3 regression"
    )


def test_flat_ttl_alias_cardinality_matches_canonical_dirs(tmp_path, monkeypatch):
    """ADR-058 §2.12 cardinality #5 — flat-alias count == canonical-dir count."""
    site = tmp_path / "_site"
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    for ns_dir, canonical_filename in B.CANONICAL_TTL.items():
        d = site / ns_dir
        d.mkdir(parents=True)
        (d / canonical_filename).write_text("# turtle", encoding="utf-8")

    B.emit_flat_ttl_aliases()

    flat_aliases = sorted(p for p in site.rglob("*.ttl") if p.parent != site / list(B.CANONICAL_TTL)[0].split("/")[0] or True)
    # Re-derive: count files at exact `_site/<dir>.ttl` paths.
    expected_flats = {site / f"{ns_dir}.ttl" for ns_dir in B.CANONICAL_TTL}
    actual_flats = {p for p in expected_flats if p.exists()}
    assert actual_flats == expected_flats
    assert len(actual_flats) == len(B.CANONICAL_TTL)


# ---------------------------------------------------------------------------
# Voie A — verify_count uses revised cardinality
# ---------------------------------------------------------------------------


def test_verify_count_excludes_shapes_from_html_expectation(tmp_path, monkeypatch):
    """ADR-058 §2.7 — only non-shapes entries must produce HTML files."""
    site = tmp_path / "_site"
    site.mkdir()
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    # One ontology entry → expects one HTML.
    (site / "a").mkdir()
    (site / "a" / "x.html").write_text("x")
    # One shapes entry → expects no HTML.
    (site / "a" / "y.ttl").write_text("# shapes raw only")

    entries = [
        make_entry("a/x.ttl"),
        make_entry("a/y.shapes.ttl"),
    ]
    # Force y.shapes.ttl into SHAPES_SKIP for this test.
    monkeypatch.setattr(B, "SHAPES_SKIP", {"a/y.shapes.ttl"})
    B.verify_count(entries)  # should not raise


def test_verify_count_fails_when_ontology_html_missing_even_if_shapes_present(
    tmp_path, monkeypatch
):
    site = tmp_path / "_site"
    site.mkdir()
    monkeypatch.setattr(B, "ROOT", tmp_path)
    monkeypatch.setattr(B, "SITE", site)
    (site / "a").mkdir()
    # ontology HTML missing
    entries = [
        make_entry("a/x.ttl"),
        make_entry("a/y.shapes.ttl"),
    ]
    monkeypatch.setattr(B, "SHAPES_SKIP", {"a/y.shapes.ttl"})
    with pytest.raises(SystemExit):
        B.verify_count(entries)
