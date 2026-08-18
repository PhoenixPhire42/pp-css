#!/usr/bin/env bash
# Build public skins from monkie styles, commit, push, purge jsDelivr @main.
#
# Usage:
#   ./publish.sh                     # publish all, commit if dirty, push, purge
#   ./publish.sh --dry-run           # build only
#   ./publish.sh --no-commit         # build + purge only (you commit yourself)
#   ./publish.sh --message "msg"     # custom commit message
#   ./publish.sh --tag v1.2.2        # also create/move lightweight tag + purge it
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
STYLES="${PP_STYLES:-$ROOT/../styles}"
DRY=0
DO_COMMIT=1
DO_PUSH=1
DO_PURGE=1
MSG=""
TAG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=1; DO_COMMIT=0; DO_PUSH=0; DO_PURGE=0; shift ;;
    --no-commit) DO_COMMIT=0; shift ;;
    --no-push) DO_PUSH=0; shift ;;
    --no-purge) DO_PURGE=0; shift ;;
    --message|-m) MSG="${2:-}"; shift 2 ;;
    --tag) TAG="${2:-}"; shift 2 ;;
    --styles) STYLES="${2:-}"; shift 2 ;;
    -h|--help)
      sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

cd "$ROOT"

echo "==> publish-from-styles  styles=$STYLES"
python3 "$ROOT/publish-from-styles.py" --styles "$STYLES"

# Stamp build id into each CSS header so you can verify CDN freshness
STAMP="$(date -u +%Y-%m-%dT%H%MZ)"
SHA_SHORT="$(git rev-parse --short HEAD 2>/dev/null || echo 'local')"
for f in "$ROOT"/skins/*.css; do
  [[ -f "$f" ]] || continue
  # insert/replace a single build line after the first closing header */
  if grep -q 'pp-css-build:' "$f"; then
    # portable in-place: rewrite first pp-css-build line
    python3 - "$f" "$STAMP" "$SHA_SHORT" <<'PY'
import sys
from pathlib import Path
p, stamp, sha = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = p.read_text(encoding="utf-8")
import re
t2, n = re.subn(
    r" \* pp-css-build:.*",
    f" * pp-css-build: {stamp} src={sha}",
    t,
    count=1,
)
if n == 0:
    t2 = t.replace(
        " */\n",
        f" *\n * pp-css-build: {stamp} src={sha}\n */\n",
        1,
    )
p.write_text(t2, encoding="utf-8")
PY
  else
    python3 - "$f" "$STAMP" "$SHA_SHORT" <<'PY'
import sys
from pathlib import Path
p, stamp, sha = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = p.read_text(encoding="utf-8")
# After first block comment's closing */
idx = t.find("*/")
if idx >= 0:
    t = t[: idx + 2] + f"\n/* pp-css-build: {stamp} src={sha} */" + t[idx + 2 :]
    p.write_text(t, encoding="utf-8")
PY
  fi
done
echo "    stamped pp-css-build: $STAMP src=$SHA_SHORT"

if [[ "$DRY" -eq 1 ]]; then
  echo "dry-run: skip commit/push/purge"
  exit 0
fi

if [[ "$DO_COMMIT" -eq 1 ]]; then
  git add skins/ README.md CATALOG.md publish-from-styles.py purge-jsdelivr.sh publish.sh 2>/dev/null || true
  git add skins/ skins/assets/ 2>/dev/null || true
  git add skins/
  if git diff --cached --quiet; then
    echo "ok: nothing to commit (working tree clean after publish)"
  else
    if [[ -z "$MSG" ]]; then
      MSG="publish skins: ${STAMP}"
    fi
    git commit -m "$MSG"
    echo "    committed: $MSG"
  fi
fi

if [[ "$DO_PUSH" -eq 1 ]]; then
  git push origin HEAD
  echo "    pushed HEAD → origin"
  if [[ -n "$TAG" ]]; then
    git tag -f "$TAG" -m "pp-css ${TAG} ${STAMP}"
    git push -f origin "refs/tags/${TAG}"
    echo "    tag ${TAG} pushed"
  fi
fi

NEW_SHA="$(git rev-parse --short HEAD)"
echo ""
echo "==> recommended install URLs (immutable commit pin)"
for f in "$ROOT"/skins/*.css; do
  base="$(basename "$f")"
  echo "  https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@${NEW_SHA}/skins/${base}"
done

if [[ "$DO_PURGE" -eq 1 ]]; then
  echo ""
  "$ROOT/purge-jsdelivr.sh" main || echo "warn: main purge incomplete" >&2
  if [[ -n "$TAG" ]]; then
    "$ROOT/purge-jsdelivr.sh" "$TAG" || echo "warn: tag purge incomplete" >&2
  fi
fi

echo ""
echo "==> verify ember header on CDN (may take ~30s)"
sleep 2
curl -fsSL "https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/phoenix-ember.css" 2>/dev/null \
  | head -20 || echo "warn: CDN fetch failed (try again shortly)"
echo ""
echo "Done. Prefer @${NEW_SHA} pins in site settings if @main ever lags again."
