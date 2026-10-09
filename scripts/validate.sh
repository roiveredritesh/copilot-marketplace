#!/usr/bin/env bash
# Validate the marketplace manifest and every plugin. Warnings fail (--strict), so run it before every push.
set -u
cd "$(dirname "$0")/.."
fail=0
for target in . plugins/*/; do
  if out=$(claude plugin validate --strict "$target" 2>&1); then
    echo "ok    $target"
  else
    echo "FAIL  $target"; echo "$out" | grep -E '❯|✘' | head -n 20
    fail=1
  fi
done
exit $fail
