---
name: analyze
description: Requirement analysis before planning - from a Jira ticket key or provided details, work out the goal, current behavior in code, acceptance criteria, impacted areas, risks, and open questions, and write an analysis file that /dotnet:plan takes as input.
argument-hint: "<ISSUE-KEY | details | file> [more context]"
disable-model-invocation: true
---
# Analyze a requirement

Output: one analysis file that `/dotnet:plan` reads. This skill decides **what** has to change and why. It doesn't decide how (that's plan) and doesn't write code.

## 1. Get the requirement
- **Ticket key** (`ABC-123`): if `~/.claude/agents/publisher.md` exists, dispatch `publisher`:
  ```text
  WORK ORDER
  goal: fetch Jira issue <KEY> for requirement analysis
  steps:
    1. Get issue <KEY> with fields: summary, type, status, priority, components, labels, fixVersions, description, acceptance criteria (custom field if present), comments, linked issues, attachments (names only).
  return:
    KEY | type | status | priority
    Summary: <one line>
    Description (first 30 lines; keep acceptance criteria, steps-to-reproduce, and stack traces intact)
    Last 5 comments: <author>: <first 3 lines each>
    Links: <type> <KEY> <summary> (at most 5)
    Attachments: <names>
  on-error: BLOCKED: <one line>
  ```
  If there's no publisher or the result is BLOCKED, ask the user to paste the ticket text (or run `/core:setup`) and continue with that.
- **Details or a file:** use the text given. Read a file path yourself.
- Use any extra context in the arguments or conversation (design notes, a linked ticket the user pasted).

## 2. Find the current behavior: dispatch in ONE message
- `core:scout`: "scope: <src dirs, or the whole repo if unknown> | terms: <4-8 domain nouns, routes, UI labels, table or type names from the requirement>. Return at most 50 lines: (a) where the behavior lives today (entry points, handlers/pages, services) with path:line, (b) domain/data types and DB tables or migrations involved, (c) validation and business rules already enforced, with path:line, (d) the test projects and tests covering this area, (e) config keys or feature flags involved. `not found` for anything absent."
- `core:runner`: `git log -n 15 --format='%h %ad %an %s' --date=short -- <the 1-3 most likely dirs>` → return as printed, at most 20 lines. (Recent churn and who knows the area.)

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 3. Analyze (main session)
Compare what the requirement asks for with what the code does. Separate facts from assumptions:
- Ticket statements and code facts (`path:line`) are facts.
- Anything you infer is an assumption. Label it `(assumption)`.
- Acceptance criteria missing from the ticket are written as `(proposed)`.

If a **blocking** question remains (it changes scope or behavior, and no reasonable default exists), ask at most 3 in one AskUserQuestion call, then fold the answers in. List non-blocking questions with the default you'll assume.

## 4. Write the analysis file
Write it with the Write tool to `.reports/analysis-<KEY or slug>.md`. Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`. Format:
```
# Analysis: <KEY> <summary>
Source: <ticket KEY / user details> · Date: <yyyy-mm-dd>
## Goal
<the business problem in 2-3 sentences; who benefits>
## Current behavior
<what happens today, with path:line>
## Requirements
Functional: numbered list. Non-functional: performance, security, compatibility (only those that apply).
## Acceptance criteria
Given/When/Then, one per line; mark (proposed) where the ticket didn't state it
## Impacted areas
| Area | Files / types (path) | Change type: new / modify / remove | Notes |
Covers code, DB (tables, migrations), API contracts, UI, config, and tests.
## Out of scope
## Dependencies
<other teams, services, packages, linked tickets>
## Risks and edge cases
## Assumptions
## Open questions
<blocking: answered above | non-blocking: question → assumed default>
## Size and next step
S / M / L with a one-line reason. Next: /dotnet:plan <this file>, or /dotnet:spike <question> first when an unknown needs research.
```

## 5. Report (chat, at most 15 lines)
Print the goal, the impacted areas (as one line each), the open questions, the size, and the file path. 
Last line, always: `Steps: scout=<dispatched> runner=<dispatched> verified=<n refs opened> file=<path>`. Fill every key; write `skipped (<reason>)` rather than leaving one out.
