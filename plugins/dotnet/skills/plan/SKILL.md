---
name: plan
description: Turn a feature, refactor, or migration request into a file-level execution plan for a .NET codebase, with a Haiku scout mapping the relevant code first.
argument-hint: "<what to build or change> [--save]"
disable-model-invocation: true
---
# Plan a change

## 1. Clarify
If the goal, scope, or acceptance criteria are ambiguous, ask at most 3 questions in one AskUserQuestion call before mapping code.

## 2. Map the code: dispatch `core:scout` (one order; split into at most 3 parallel orders only for very large repos)
"Return at most 50 lines: (a) entry points for <feature area> (controllers/endpoints/handlers/pages), (b) the domain/data types involved (path:line), (c) the closest existing feature to copy patterns from, (d) the test projects and an example test for that area."
Also run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" detect` yourself (it is about 8 lines).

## 3. Write the plan (chat)
```
Goal / Non-goals
Approach: 2-4 sentences, and why this over the obvious alternative
Steps (each small enough to build and test on its own):
  1. <change> - files: path, path - verify: build | test <name> | manual check
Data/migrations: schema changes and lock-safety (PostgreSQL: see postgresql:pg)
Risks & rollback
Test plan
```
Prefer the repo's existing patterns over new abstractions. Every step lists the exact files. No step should leave the build broken.
With `--save`, also write it to `~/.claude/reports/<repo-folder-name>/plan-<slug>-<yyyymmdd>.md` and print the path.
