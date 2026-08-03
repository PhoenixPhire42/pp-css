#!/usr/bin/env bash
# Purge jsDelivr CDN cache for PhoenixPhire42/pp-css so @main tracks GitHub.
#
# Usage:
#   ./purge-jsdelivr.sh              # purge @main (all skins + assets)
#   ./purge-jsdelivr.sh main         # same
#   ./purge-jsdelivr.sh v1.2.1-flame # purge a tag
#   ./purge-jsdelivr.sh 4f74ab0      # purge a commit (usually unnecessary)
#
# https://www.jsdelivr.com/documentation#id-purge
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OWNER="${PP_CSS_OWNER:-PhoenixPhire42}"
REPO="${PP_CSS_REPO:-pp-css}"
REF="${1:-main}"

# Bash 3-safe file list (macOS /bin/bash)
PATHS=()
while IFS= read -r rel; do
  [[ -n "$rel" ]] && PATHS+=("$rel")
done < <(
  find "$ROOT/skins" -type f \( -name '*.css' -o -name '*.png' -o -name '*.jpg' -o -name '*.svg' -o -name '*.webp' \) \
    | sed "s|^$ROOT/||" | sort -u
  echo "skins"
  echo "skins/assets"
)

if [[ ${#PATHS[@]} -eq 0 ]]; then
  echo "error: no skin files under $ROOT/skins" >&2
  exit 1
fi

echo "==> purge jsDelivr  gh/${OWNER}/${REPO}@${REF}"
echo "    ${#PATHS[@]} path(s)"
FAIL=0
OK=0
for rel in "${PATHS[@]}"; do
  url="https://purge.jsdelivr.net/gh/${OWNER}/${REPO}@${REF}/${rel}"
  code=$(curl -sS -o /tmp/jsd-purge-body.json -w "%{http_code}" --max-time 45 "$url" || echo "000")
  if [[ "$code" == "200" ]]; then
    OK=$((OK + 1))
    printf "  ok  %s\n" "$rel"
  else
    FAIL=$((FAIL + 1))
    printf "  FAIL %s  http=%s\n" "$rel" "$code" >&2
    head -c 200 /tmp/jsd-purge-body.json 2>/dev/null || true
    echo >&2
  fi
  sleep 0.15
done

echo "==> done  ok=$OK fail=$FAIL  ref=@${REF}"
if [[ "$FAIL" -gt 0 ]]; then
  echo "note: some purges failed. Prefer commit/tag pins for installs:" >&2
  echo "  https://cdn.jsdelivr.net/gh/${OWNER}/${REPO}@<tag-or-sha>/skins/<file>.css" >&2
  exit 1
fi

echo "CDN @${REF} should refresh within ~1–2 minutes."
