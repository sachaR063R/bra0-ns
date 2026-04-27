#!/usr/bin/env bash
# probe-iris.sh — ADR-058 §2.12 E2E acceptance probe.
#
# Modes:
#   local  — assert presence of expected files in _site/ (CI default).
#   live   — HTTP-probe https://schema.bra0.org against the same contract.
#
# Acceptance contract (ADR-058 §2.12 + ADR-060 §3):
#   1. Eight directory landings (6 canonical + 2 static) return HTML.
#   2. Every whitelisted TTL is reachable as text/turtle.
#   3. The single foreign-namespace mirror (neuro-upper) carries the mirror
#      banner. edgy migrated to canonical; retroeng kept private (ADR-060).
#   4. Each ontology HTML carries an audit-meta block.
#   5. Canonical HTMLs carry <link rel="alternate" type="text/turtle">.
#   6. Static landings exist:
#        /evidence-os/query/   lists evoQ-kpi-shapes.shapes.ttl
#        /cross-domain/        lists edgy/ as published child
#   7. No public surface artefact references omyn.ai/schema/{edgy,retroeng}.

set -euo pipefail

MODE="${1:-local}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WHITELIST="${ROOT}/docs-published.txt"
SITE="${ROOT}/_site"
BASE_URL="https://schema.bra0.org"

CANONICAL_DIRS=(
  "agent-service-contract"
  "essence-kernel"
  "capability"
  "evidence-os"
  "evidence-os/edcc"
  "cross-domain/edgy"
)
STATIC_DIRS=(
  "evidence-os/query"
  "cross-domain"
)
MIRRORS=(
  "capability/neuro-upper.ttl"
)

fail_count=0

err() {
  echo "::error::$*" >&2
  fail_count=$((fail_count + 1))
}
ok() { echo "  ✓ $*"; }

probe_local() {
  echo "== Local probe (mode=local) =="

  echo "-- Directory landings --"
  for d in "${CANONICAL_DIRS[@]}" "${STATIC_DIRS[@]}"; do
    idx="${SITE}/${d}/index.html"
    if [ -f "${idx}" ]; then
      ok "${d}/index.html present"
    else
      err "Missing landing: ${d}/index.html"
    fi
  done

  echo "-- Raw TTL reachability --"
  while IFS=';' read -r ttl _badge _audit _date; do
    [ -z "${ttl}" ] && continue
    [[ "${ttl}" =~ ^[[:space:]]*# ]] && continue
    ttl="${ttl#"${ttl%%[![:space:]]*}"}"  # ltrim
    if [ -f "${SITE}/${ttl}" ]; then
      ok "${ttl}"
    else
      err "Missing raw TTL in _site: ${ttl}"
    fi
  done < <(grep -v '^[[:space:]]*#' "${WHITELIST}" | grep -v '^[[:space:]]*$')

  echo "-- Mirror banner injection --"
  for m in "${MIRRORS[@]}"; do
    html="${SITE}/${m%.ttl}.html"
    if [ ! -f "${html}" ]; then
      err "Mirror HTML missing: ${html#"${SITE}/"}"
      continue
    fi
    if grep -q 'ns-mirror-banner' "${html}"; then
      ok "${m%.ttl}.html carries mirror banner"
    else
      err "Mirror banner missing in ${m%.ttl}.html"
    fi
  done

  echo "-- Audit-meta block on ontology HTMLs --"
  while IFS= read -r html; do
    rel="${html#"${SITE}/"}"
    [ "$(basename "${rel}")" = "index.html" ] && continue
    if grep -q 'ns-audit-meta' "${html}"; then
      ok "${rel}"
    else
      err "audit-meta block missing in ${rel}"
    fi
  done < <(find "${SITE}" -mindepth 2 -name "*.html" -type f | sort)

  echo "-- Alternate link on canonical landings --"
  for d in "${CANONICAL_DIRS[@]}"; do
    idx="${SITE}/${d}/index.html"
    [ -f "${idx}" ] || continue
    if grep -q 'rel="alternate" type="text/turtle"' "${idx}"; then
      ok "${d}/index.html carries alternate link"
    else
      err "Alternate link missing in ${d}/index.html"
    fi
  done

  echo "-- Static landing self-checks --"
  query_idx="${SITE}/evidence-os/query/index.html"
  if [ -f "${query_idx}" ]; then
    if grep -q 'evoQ-kpi-shapes.shapes.ttl' "${query_idx}"; then
      ok "evidence-os/query/index.html lists shapes TTL"
    else
      err "Static landing does not link evoQ-kpi-shapes.shapes.ttl"
    fi
  fi
  cd_idx="${SITE}/cross-domain/index.html"
  if [ -f "${cd_idx}" ]; then
    if grep -q 'edgy/' "${cd_idx}"; then
      ok "cross-domain/index.html lists edgy/ child"
    else
      err "cross-domain/ static landing does not list edgy/ child"
    fi
  fi

  echo "-- omyn.ai/schema rupture-sèche (ADR-060) --"
  if grep -REn 'omyn\.ai/schema/(edgy|retroeng)' "${SITE}" >/dev/null 2>&1; then
    err "Public surface contains omyn.ai/schema/{edgy,retroeng} references"
    grep -REn 'omyn\.ai/schema/(edgy|retroeng)' "${SITE}" >&2 || true
  else
    ok "No omyn.ai/schema/{edgy,retroeng} references in _site/"
  fi
}

probe_live() {
  echo "== Live probe (mode=live, base=${BASE_URL}) =="

  curl_status() { curl -sS -o /dev/null -w '%{http_code}' -L "$1"; }
  curl_ctype()  { curl -sS -o /dev/null -w '%{content_type}' -L "$1"; }

  echo "-- Directory landings (HTML) --"
  for d in "${CANONICAL_DIRS[@]}" "${STATIC_DIRS[@]}"; do
    code="$(curl_status "${BASE_URL}/${d}/")"
    if [ "${code}" = "200" ]; then
      ok "GET ${d}/ → 200"
    else
      err "GET ${d}/ → ${code}"
    fi
  done

  echo "-- Raw TTL (text/turtle) --"
  while IFS=';' read -r ttl _badge _audit _date; do
    [ -z "${ttl}" ] && continue
    [[ "${ttl}" =~ ^[[:space:]]*# ]] && continue
    ttl="${ttl#"${ttl%%[![:space:]]*}"}"
    code="$(curl_status "${BASE_URL}/${ttl}")"
    ctype="$(curl_ctype "${BASE_URL}/${ttl}")"
    if [ "${code}" = "200" ] && [[ "${ctype}" == text/turtle* ]]; then
      ok "GET ${ttl} → 200 ${ctype}"
    else
      err "GET ${ttl} → ${code} ${ctype}"
    fi
  done < <(grep -v '^[[:space:]]*#' "${WHITELIST}" | grep -v '^[[:space:]]*$')
}

case "${MODE}" in
  local) probe_local ;;
  live)  probe_live ;;
  *)
    echo "Usage: $0 {local|live}" >&2
    exit 2
    ;;
esac

if [ "${fail_count}" -ne 0 ]; then
  echo
  echo "::error::Probe failed with ${fail_count} error(s) (mode=${MODE})"
  exit 1
fi
echo
echo "✓ Probe passed (mode=${MODE})"
