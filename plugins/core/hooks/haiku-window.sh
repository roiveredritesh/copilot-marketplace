#!/usr/bin/env bash
# SessionStart launcher for the Haiku compaction check. Needs Python 3.8+; without it the check is skipped.
d=${BASH_SOURCE[0]//\\//}; d=${d%/*}
for py in python3 python; do
  if "$py" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; then
    exec "$py" "$d/haiku_window.py"
  fi
done
exit 0
