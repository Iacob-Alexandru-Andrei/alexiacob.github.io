#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

BUNDLE_BIN="${BUNDLE_BIN:-bundle}"

echo "[public-surface] building site"
"$BUNDLE_BIN" exec jekyll clean --quiet
"$BUNDLE_BIN" exec jekyll build --quiet

fail=0
for forbidden in _site/README.md _site/docs _site/templates _site/guardrails _site/scripts; do
  if [[ -e "$forbidden" ]]; then
    echo "[public-surface][FAIL] forbidden output present: $forbidden"
    fail=1
  fi
done

if rg -n "/Users/" _site >/tmp/public-surface-paths.txt; then
  echo "[public-surface][FAIL] absolute local paths found in public output"
  cat /tmp/public-surface-paths.txt
  fail=1
fi
rm -f /tmp/public-surface-paths.txt

if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "[public-surface][OK] no forbidden internal outputs detected"
