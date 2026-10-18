#!/usr/bin/env bash
# SessionStart hook: plain stdout becomes session context, so Claude delegates to the
# executors without the user naming them. CLAUDE_CORE_DELEGATION=0 turns it off.
[ "${CLAUDE_CORE_DELEGATION:-1}" = "0" ] && exit 0
cat <<'X'
Delegation policy (core plugin). The core:scout and core:runner subagents run on Haiku at a small fraction of the main model's price, and only their condensed result enters this conversation. Dispatching them through the Agent tool (subagent_type "core:scout" / "core:runner") is the default for:
- core:scout: code or web lookups that need several searches or span more than ~3 files (where something lives, callers and usages, a feature's flow, conventions, library facts). Preferred over a run of inline Grep/Read calls and over Explore or general-purpose.
- core:runner: shell commands with long or noisy output (git log/diff/blame, gh PR data and CI logs, dotnet/msbuild build and test, read-only psql/sqlcmd).
- core:reviewer: review of a diff over ~600 changed lines, one chunk per dispatch.
Inline is cheaper for a single Grep, one small Read, or a command with a few lines of output. Independent dispatches go in one message so they run in parallel.
Executors see only their prompt and refuse vague ones: give exact paths or globs plus symbols, or the exact commands, and a return format with a line cap. Open the 1-2 decision-critical path:line results yourself before relying on them. An executor stops at a context budget below Haiku's 100K price tier; a reply ending in `not done: ...` needs a fresh order for just those steps.
X
