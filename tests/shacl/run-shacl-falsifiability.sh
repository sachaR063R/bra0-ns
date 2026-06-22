#!/usr/bin/env bash
# bra0-ns SHACL falsifiability harness — rudof-sparql-revalidation-2026-06-22.
#
# Replaces the parse-only TODO in validate.yml with REAL SHACL validation. Each
# whitelisted .shapes.ttl named in tests/shacl/manifest.tsv is run against a
# negative fixture and asserted to behave:
#   violate       -> must fire on the bad fixture (proves it is not vacuous).
#   conform       -> must stay clean on a good fixture.
#   known-dormant -> provably vacuous under rudof 0.2.8 (sh:SPARQLTarget selects
#                    an empty focus set); conforms-on-breach today. Counted as
#                    XFAIL so CI stays green AND honest. If such a shape ever
#                    FIRES, the harness fails loudly: dormancy is resolved and the
#                    manifest row must be promoted to expected=violate.
#
# Engine note: rudof is the SHACL Core engine. It silently no-ops sh:sparql and
# sh:SPARQLTarget, which is exactly the false-green this harness exists to expose.
set -euo pipefail
cd "$(dirname "$0")/../.."   # repo root

MANIFEST=tests/shacl/manifest.tsv
FIXTURES=tests/shacl/fixtures
fail=0; pass=0; xfail=0

conforms() { # <shapes> <data> -> "true" if no violations, "false" otherwise
  if rudof shacl-validate -s "$1" "$2" 2>&1 | grep -qiE "No Errors found"; then
    echo true
  else
    echo false
  fi
}

echo "== bra0-ns SHACL falsifiability harness =="
while IFS='|' read -r shapes fixture expected note; do
  case "$shapes" in ''|'#'*) continue ;; esac
  if [ ! -f "$shapes" ]; then
    echo "  FAIL  shapes not found: $shapes"; fail=1; continue
  fi
  if [ ! -f "$FIXTURES/$fixture" ]; then
    echo "  FAIL  fixture not found: $FIXTURES/$fixture"; fail=1; continue
  fi
  got=$(conforms "$shapes" "$FIXTURES/$fixture")
  case "$expected" in
    violate)
      if [ "$got" = false ]; then
        echo "  PASS  $shapes fires on $fixture"; pass=$((pass+1))
      else
        echo "  FAIL  $shapes is VACUOUS on $fixture (conforms-on-breach) — $note"; fail=1
      fi ;;
    conform)
      if [ "$got" = true ]; then
        echo "  PASS  $shapes clean on $fixture"; pass=$((pass+1))
      else
        echo "  FAIL  $shapes unexpectedly fires on good $fixture — $note"; fail=1
      fi ;;
    known-dormant)
      if [ "$got" = true ]; then
        echo "  XFAIL $shapes dormant on $fixture (rudof no-ops SPARQLTarget, expected) — $note"; xfail=$((xfail+1))
      else
        echo "  XPASS $shapes now FIRES on $fixture — dormancy resolved; promote manifest row to expected=violate — $note"; fail=1
      fi ;;
    *)
      echo "  FAIL  unknown expected='$expected' for $shapes"; fail=1 ;;
  esac
done < "$MANIFEST"

echo "----"
echo "pass=$pass  xfail(known-dormant)=$xfail"
if [ "$fail" -ne 0 ]; then
  echo "SHACL FALSIFIABILITY: FAIL"
  exit 1
fi
echo "SHACL FALSIFIABILITY: PASS"
