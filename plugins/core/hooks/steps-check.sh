#!/usr/bin/env bash
# Stop hook launcher. Needs Python 3.8+; without it the check is skipped (never blocks).
src=${BASH_SOURCE[0]//\\//}; case $src in */*) d=${src%/*};; *) d=.;; esac  # Windows passes backslashes
for py in python3 python; do
  if "$py" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; then
    "$py" "$d/steps_check.py"
    exit 0  # never pass a crash on: a hook that exits 2 blocks what it guards
  fi
done
exit 0
