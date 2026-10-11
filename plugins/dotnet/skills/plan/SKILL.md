---
name: plan
description: Turn a feature, refactor, or migration request into a file-level execution plan for a .NET codebase, with a Haiku scout mapping the relevant code first.
argument-hint: "<analysis file | what to build or change> [--save]"
disable-model-invocation: true
---
# Plan a change

## 1. Clarify
If the input is an analysis file from `/dotnet:analyze` (or one is in the conversation), read it. Its goal, acceptance criteria, impacted areas, and answered questions are settled input: don't re-ask them, use its impacted files and terms as the scout scope, and carry its acceptance criteria into the test plan. For a large or unclear request without one, suggest `/dotnet:analyze` first.

If the goal, scope, or acceptance criteria are still ambiguous, ask at most 3 questions in one AskUserQuestion call before mapping code.

## 2. Map the code: dispatch `core:scout` (one order; split into at most 3 parallel orders only for very large repos)
"scope: <src dirs or globs> | terms: <3-6 type names, routes, or keywords for the feature>. Return at most 50 lines: (a) entry points matching the terms (controllers/endpoints/handlers/pages), (b) the domain/data types involved (path:line), (c) the closest existing feature to copy patterns from, (d) the test projects and an example test for that area."
Also run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" detect` yourself (it is about 8 lines).

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact in the report, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 3. Write the plan (chat)
```
Goal / Non-goals
Approach: 2-4 sentences, and why this over the obvious alternative
Steps (each small enough to build and test on its own):
  1. <change> - files: path, path - verify: build | test <name> | manual check
Data/migrations: schema changes and lock-safety (suggest `/postgresql:pg` or `/sqlserver:mssql` for the migration review)
Risks & rollback
Test plan
```
Prefer the repo's existing patterns over new abstractions. Every step lists the exact files. Last line, always: `Steps: scout=<dispatched> verified=<n refs opened> saved=<path | no>`. Fill every key; write `skipped (<reason>)` rather than leaving one out.
With `--save`, also write it to `.reports/plan-<slug>-<yyyymmdd>.md` and print the path. Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`.
