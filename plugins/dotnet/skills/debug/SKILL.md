---
name: debug
description: Find the root cause of a .NET exception, stack trace, failing test, or bug report, using Haiku agents to locate code and dig through git history.
argument-hint: "<stack trace | error | failing test | bug description> [--save]"
disable-model-invocation: true
---
# Root-cause a .NET problem

You (the main session) form and test hypotheses. Haiku agents fetch evidence. Stop when the cause is proven by code or history, not merely plausible.

## 1. Read the symptom
From the input, extract the exception type and message, the frames that point into this repo (not `System.*` or `Microsoft.*`), the failing test name, and any timeframe ("since Tuesday", "after deploy").

## 2. Gather evidence: dispatch in ONE message (parallel)
- `core:scout`: "for each of these frames <file:line or Type.Method>, return the method signature and lines ±10 around the line; at most 60 lines total".
- `core:runner`: "for <files from the frames>, run `git log --since=<timeframe or 30.days> --format='%h %ad %an %s' --date=short -- <files>`; return at most 20 lines".
- If a failing test is named, also a `core:runner` reproduce order: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → return the output as printed.

## 3. Hypothesize and verify
List at most 3 hypotheses ranked by evidence. Verify the top one by reading the exact code path (Read the needed ranges yourself). Typical .NET causes: null from `FirstOrDefault`/config/DI, async deadlock or unobserved task, EF tracking or lazy loading after context disposal, `DateTime` kind/timezone, culture parsing, DI lifetime (scoped in singleton), race on shared state, serialization name/casing changes.

For a regression, have `core:runner` search history: `git log -S'<symbol or literal>' --format='%h %ad %s' --date=short -- <path>` or `git log -L <start>,<end>:<file> --format='%h %s' -n 5 | grep -E '^[0-9a-f]{7} |^[+-][^+-]' | head -40`. Run `git bisect` only with the user's explicit OK, because it checks out commits.

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact in the report, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 4. Report (chat; at most 40 lines)
```
Root cause: <one sentence>
Evidence: path:line - why it fails (and commit <hash> if it is a regression)
Fix: <minimal change, as a short diff sketch>
Test to add: <name + what it asserts>
Confidence: high | medium (what would confirm it)
```
With `--save`, also write it to `.reports/debug-<yyyymmdd-hhmm>.md` and print the path. Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`.
