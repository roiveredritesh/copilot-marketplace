#!/usr/bin/env bash
# 15 tiny files: more Reads than scout's maxTurns (12) allows, so the run ends at the turn limit.
for i in $(seq 1 15); do printf 'line one\nMARKER%s value=%s\nline three\n' "$i" $((i * 111)) > "f$i.txt"; done
g() { git -c core.autocrlf=false -c user.name=eval -c user.email=eval@example.com "$@"; }
g init -q && g add -A && g commit -qm "fixture"
