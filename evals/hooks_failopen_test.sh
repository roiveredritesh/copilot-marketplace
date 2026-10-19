#!/usr/bin/env bash
# Every core hook must fail open: exit 0, whatever goes wrong (no Python, bad input, a crash, a relative path).
# A hook that exits 2 blocks the tool call or the stop it guards.  usage: bash evals/hooks_failopen_test.sh
root=$(cd "$(dirname "$0")/.." && pwd); hooks="$root/plugins/core/hooks"
pass=0; fail=0
check() { if [ "$2" = 0 ]; then pass=$((pass+1)); echo "ok    $1"; else fail=$((fail+1)); echo "FAIL  $1 (exit $2)"; fi; }
nopy=$(mktemp -d); trap 'rm -rf "$nopy"' EXIT
for c in bash cat sed grep awk tr head tail cut dirname basename env printf; do ln -s "$(command -v $c)" "$nopy/$c" 2>/dev/null; done
inputs=('not json' '{}' '{"hook_event_name":"PreToolUse","tool_name":"Read","transcript_path":"/nonexistent.jsonl","tool_input":{"file_path":"/nonexistent","offset":"x"}}' '{"hook_event_name":"Stop","transcript_path":"/nonexistent.jsonl","last_assistant_message":"Steps: verified=9"}')
for h in haiku-guard.sh haiku-window.sh steps-check.sh delegation.sh; do
  for i in "${inputs[@]}"; do
    echo "$i" | bash "$hooks/$h" >/dev/null 2>&1; check "$h, input ${i:0:24}" $?
    (cd "$hooks" && echo "$i" | bash "$h" >/dev/null 2>&1); check "$h by relative path, input ${i:0:24}" $?
  done
  echo '{}' | env -i PATH="$nopy" bash "$hooks/$h" >/dev/null 2>&1; check "$h without Python" $?
done
# a crash inside the Python file must not become exit 2: point a copy of each launcher at a script that exits 2
crash=$(mktemp -d)
for pair in haiku-guard.sh:haiku_guard.py haiku-window.sh:haiku_window.py steps-check.sh:steps_check.py; do
  cp "$hooks/${pair%%:*}" "$crash/"; printf 'import sys\nsys.exit(2)\n' > "$crash/${pair#*:}"
  echo '{}' | bash "$crash/${pair%%:*}" >/dev/null 2>&1; check "${pair%%:*} when its Python exits 2" $?
done
rm -rf "$crash"
echo; echo "$pass/$((pass+fail)) passed"
[ "$fail" = 0 ]
