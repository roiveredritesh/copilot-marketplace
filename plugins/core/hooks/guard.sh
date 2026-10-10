#!/usr/bin/env bash
# PreToolUse guard for Bash, enforced by Claude Code (the model can't skip it).
# - Database writes through psql/sqlcmd are denied unless the session is read-only
#   (psql: default_transaction_read_only=on; sqlcmd: the bundled audit.sql or a
#   rolled-back transaction). Set CLAUDE_ALLOW_DB_WRITES=1 to opt out.
# - Outward actions (git push, PR/issue/release writes, gh api writes) always ask the user.
input=$(cat)
# The command string, still JSON-escaped; good enough for keyword checks.
cmd=$(printf '%s' "$input" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\(\([^"\\]\|\\.\)*\)".*/\1/p')
[ -z "$cmd" ] && exit 0

decide() { # decision reason
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
  exit 0
}
has() { printf '%s' "$cmd" | grep -qiE "$1"; }
B='(^|[;&|(`[:space:]]|\\")'   # start of a word (loose: a false "ask" is cheap)
# Command position (strict, for DB tools): after a separator or quote, then optional
# VAR=value prefixes, wrappers, and a directory path. Keeps `echo psql` allowed.
C='(^|[;&|(`]|\\n|\\"|'"'"')[[:space:]]*([A-Za-z_][A-Za-z0-9_]*=(\\"[^"]*\\"|[^[:space:]]*)[[:space:]]+)*((rtk|sudo|env|exec|time|xargs)[[:space:]]+)*(\\"[^"]*[/\\]|[^[:space:]"]*[/\\])?'

# --- database writes --------------------------------------------------------
if [ "${CLAUDE_ALLOW_DB_WRITES:-}" != "1" ]; then
  if has "${C}(dropdb|createdb|pg_restore|bcp)(\.exe)?([[:space:]]|$)"; then
    decide deny "ritesh-marketplace guard: database-changing tool blocked. Hand the command to the user, or set CLAUDE_ALLOW_DB_WRITES=1 to allow."
  fi
  if has "${C}psql(\.exe)?([[:space:]\\\"]|$)" && ! has "psql(\.exe)?\\\\?\"?[[:space:]]+(--version|-V|--help)([[:space:]]|$)"; then
    has 'default_transaction_read_only=on' ||
      decide deny "ritesh-marketplace guard: psql must run read-only (PGOPTIONS=\\\"-c default_transaction_read_only=on\\\"). Write fixes to files for the user to apply, or set CLAUDE_ALLOW_DB_WRITES=1."
  fi
  if has "${C}sqlcmd(\.exe)?([[:space:]\\\"]|$)" && ! has "sqlcmd(\.exe)?\\\\?\"?[[:space:]]+(-\?|--version)([[:space:]]|$)"; then
    if ! has 'skills[/\\]+mssql[/\\]+audit\.sql' && ! { has 'rollback' && ! has 'commit'; }; then
      decide deny "ritesh-marketplace guard: sqlcmd may only run the bundled audit.sql or SELECTs inside BEGIN TRAN ... ROLLBACK. Write fixes to files for the user to apply, or set CLAUDE_ALLOW_DB_WRITES=1."
    fi
  fi
fi

# --- outward actions: always ask ---------------------------------------------
if has "${B}git([[:space:]]+-[^[:space:]]+([[:space:]]+[^-][^[:space:]]*)?)*[[:space:]]+push([[:space:]]|$)"; then
  decide ask "ritesh-marketplace guard: git push publishes commits. Confirm?"
fi
if has "${B}gh[[:space:]]+(pr[[:space:]]+(create|comment|merge|review|close|reopen|edit|ready)|issue[[:space:]]+(create|comment|close|reopen|edit|delete)|release[[:space:]]+(create|delete|edit|upload)|repo[[:space:]]+(create|delete|edit|rename|archive))([[:space:]]|$)"; then
  decide ask "ritesh-marketplace guard: this gh command changes GitHub. Confirm?"
fi
if has "${B}gh[[:space:]]+api([[:space:]]|$)"; then
  if has '[[:space:]](-X|--method)[[:space:]=]*(POST|PUT|PATCH|DELETE)' || has 'mutation' ||
     { has '[[:space:]](-f|-F|--field|--raw-field|--input)[[:space:]=]' && ! has "${B}gh[[:space:]]+api[[:space:]]+graphql"; }; then
    decide ask "ritesh-marketplace guard: this gh api call writes to GitHub. Confirm?"
  fi
fi
exit 0
