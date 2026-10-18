#!/usr/bin/env bash
# usage: run.sh <dir from setup.sh> <name> <git-ref> <prompt> [extra claude args...]   (MODEL=haiku for a Haiku main session)
# Fresh worktree of eShopOnWeb at <ref>, Sonnet main + the /core:setup settings, core + dotnet plugins, clean env.
H=$(cd "$(dirname "$0")" && pwd); S=$(cd "$1" && pwd); name=$2; ref=$3; prompt=$4; shift 4
M=$(cd "$H/../../plugins" && pwd)
[ -f "$S/settings.json" ] || echo '{"env": {"CLAUDE_CODE_SUBAGENT_MODEL": "haiku"}, "modelSettings": {"haiku": {"autoCompactWindow": 100000}}}' > "$S/settings.json"  # what /core:setup writes
wt="$S/wt/$name"; rm -rf "$wt"; git -C "$S/eShopOnWeb" worktree prune
git -C "$S/eShopOnWeb" worktree add -q --detach "$wt" "$ref" && git -C "$wt" checkout -q -B "run-$name" 2>/dev/null
cd "$wt" && env -i HOME="$HOME" PATH="$PATH" TERM=dumb HTTPS_PROXY="$HTTPS_PROXY" https_proxy="$https_proxy" NO_PROXY="$NO_PROXY" \
  no_proxy="$no_proxy" NODE_EXTRA_CA_CERTS="$NODE_EXTRA_CA_CERTS" SSL_CERT_FILE="$SSL_CERT_FILE" ANTHROPIC_BASE_URL="$ANTHROPIC_BASE_URL" \
  DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1 timeout 1500 claude -p --model "${MODEL:-sonnet}" --output-format json --max-turns 60 \
  --settings "$S/settings.json" --plugin-dir "$M/core" --plugin-dir "$M/dotnet" \
  --allowedTools Read Glob Grep Skill Agent Bash Edit Write TodoWrite "$@" <<< "$prompt" > "$S/out-$name.json" 2> "$S/err-$name.txt"
python3 "$H/report.py" "$S/out-$name.json" "$name"
