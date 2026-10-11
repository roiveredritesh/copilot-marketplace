#!/usr/bin/env bash
# Stop hook launcher. Needs Python 3.8+; without it the check is skipped (never blocks).
d=${BASH_SOURCE[0]//\\//}; d=${d%/*}
for py in python3 python; do
  if "$py" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; then
    exec "$py" "$d/steps_check.py"
  fi
done
exit 0
