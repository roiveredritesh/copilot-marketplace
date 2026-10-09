---
name: spike
description: Time-boxed research spike for a technical question - about existing code (how does X work, can we change Y, what breaks) or new technology (which library/approach, is it viable). Haiku agents gather code, git, web, and NuGet facts; the main session compares and recommends.
argument-hint: "<question> [--poc] [--save] [--confluence <space>]"
disable-model-invocation: true
---
# Spike

A spike answers **one question so a decision can be made**. It does not ship code.

## 1. Frame (main session; ask at most 3 questions in one AskUserQuestion if unclear)
```
Question: <one sentence>
Decision it informs: <what will be decided, by whom>
Type: existing | new | both
Options to compare: <2-4, or "discover">
Must-haves / constraints: <.NET version, license, PostgreSQL, Framework vs Core, perf/SLA, budget>
Done when: <the evidence that would settle it>
```

## 2. Gather evidence: dispatch independent work orders in ONE message
**Existing code** (`core:scout`): "scope: <dirs/globs> | terms: <type names, interfaces, config keys for the area>. Return: entry points, the core types and their responsibilities, data flow (request → service → DB), extension points, and the tests covering it, all with path:line; at most 60 lines."
**Existing history** (`core:runner`): `git log --since=12.months --format='%h %ad %an %s' --date=short -- <paths> | head -n 30` and `git shortlog -sn --since=12.months -- <paths> | head -n 5` (churn and owners).
**New technology** (`core:scout`, web): one work order per option:
```text
goal: facts on <option> for a .NET <version> app<, with PostgreSQL>
steps:
  1. WebSearch: "<option> .NET <version> documentation", "<option> release notes", "<option> vs <other option>"
  2. WebFetch the official docs/README and the latest release notes found
return (one line each, with source URL): latest version + date | license | supported .NET targets | maintenance (last release, open issues trend if shown) | key features for <constraints> | known limitations/breaking changes | PostgreSQL/Npgsql support (if relevant)
```
**NuGet facts** (`core:runner`): `dotnet package search <id> --take 3 --source https://api.nuget.org/v3/index.json` per candidate → latest version, owners, downloads.

## 3. Optional PoC (`--poc`, or when the facts can't settle it)
Build the smallest experiment that tests the riskiest assumption, **outside the working tree**: `git worktree add ../<repo>-spike-<slug>` for existing code, or `dotnet new` in a temp folder for new tech. Run it with `core:runner` (`dotnet.sh build|test`, or a BenchmarkDotNet run with condensed output). Time-box it: at most 3 build/run rounds. Report what it proved and what it didn't. Clean up the worktree when done, unless the user wants to keep it.

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact in the report, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 4. Decide (main session)
Compare the options against the must-haves. Only facts with a source (URL or `path:line`) go into the matrix. Anything else is listed under "Assumptions" and can't decide the recommendation by itself. A `not found` from scout stays `not found`; don't fill it from memory without saying so.

## 5. Report (chat; at most 50 lines)
```
Spike: <question>
Answer / recommendation: <one paragraph>   Confidence: high | medium | low
| Criterion | Option A | Option B | ... |   (each cell backed by a source URL or path:line)
Evidence: key findings with sources
PoC result: <if run>
Risks & unknowns: what is still unproven, and how to prove it
Next steps: concrete, with a rough effort (S/M/L) - hand-off to /dotnet:plan
```
With `--save`, also write the report to `~/.claude/reports/<repo-folder-name>/spike-<slug>-<yyyymmdd>.md`. With `--confluence <space>`, publish it as an ADR-style page through `/docs-kit:confluence adr` (needs docs-kit).
