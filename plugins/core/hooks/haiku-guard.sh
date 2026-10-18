#!/usr/bin/env bash
# PreToolUse + SessionStart(compact) launcher for the Haiku context guard. Needs Python 3.8+; without it the guard is skipped.
d=${BASH_SOURCE[0]//\\//}; d=${d%/*}
for py in python3 python; do
  if "$py" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; then
    exec "$py" "$d/haiku_guard.py"
  fi
done
exit 0
