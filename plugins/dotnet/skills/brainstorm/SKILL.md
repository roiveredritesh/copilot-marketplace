---
name: brainstorm
description: Brainstorm options before there is a spec - feature ideas, architecture or design approaches, alternatives to existing code, or ways to solve a problem - grounded in the codebase, compared on your criteria, ending in a chosen direction that feeds /dotnet:spike, /dotnet:analyze, or /dotnet:plan.
argument-hint: "<idea | problem | 'alternatives for <area>'> [--save]"
disable-model-invocation: true
---
# Brainstorm

This skill explores **what could be done**. `/dotnet:spike` checks facts about a known question, and `/dotnet:analyze` pins down a known requirement. If the user already knows what they want, say so and suggest those instead.

## 1. Frame (main session)
Restate the goal in one sentence. Identify the mode: **feature ideas**, **design approaches**, **alternatives to existing code**, or **problem solving**. Then ask at most 3 questions in one AskUserQuestion call, only about what changes the options: users and goal, hard constraints (deadline, budget, tech it must or mustn't use, compatibility with .NET Framework), and how the options will be judged (speed, cost, risk, simplicity, scalability). Skip questions the input already answers.

## 2. Ground it in the code (only when existing code is involved)
Dispatch `core:scout`: "scope: <dirs/globs for the area> | terms: <type names, routes, tables from the idea>. Return at most 40 lines: where the related behavior lives (path:line), the patterns and libraries already used for similar things, extension points (interfaces, DI registrations, events), and constraints (TFM, packages, DB). `not found` for anything absent."
For a quick external fact (does a library exist, is it maintained), one `core:scout` web order. Deep research belongs to `/dotnet:spike` later.

## 3. Diverge (main session)
Produce **3-5 options that differ in approach**, not variations of one idea. Always include the **simplest thing that could work** (often reuse, configuration, or doing nothing), and one bolder option when it's reasonable. For each option:
```
### <n>. <name>: <one-line idea>
How: 2-4 lines, naming where it fits in this codebase (path:line from the scout) or the new pieces needed
Effort: S | M | L - why
Pros / Cons: 2-3 each
Risks and unknowns: what could make it fail; mark anything needing research as (spike)
```
Facts about the code carry `path:line`. Anything you're assuming about the code, users, or load is marked `(assumption)`.

## 4. Converge
Show a matrix: options × the user's criteria (`++ / + / 0 / - / --`) with one line of reasoning per cell where it isn't obvious. Recommend one option, or a combination, and give the deciding reason in two sentences. Then ask with AskUserQuestion: pick an option (one per option, at most 4; offer the rest via Other) or **explore further** (the user says which direction).

## 5. Record and hand off
Write the result to `.reports/brainstorm-<slug>.md` (always, so later steps can read it). Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`. It contains the goal, the constraints and criteria, all the options (short), the matrix, the chosen direction, and the open questions.

Next step, by what's left open:
- Unknowns marked `(spike)` → `/dotnet:spike <question>`
- A clear direction → `/dotnet:analyze .reports/brainstorm-<slug>.md` (or `/dotnet:flow`), then `/dotnet:plan`

Chat output: at most 40 lines (options in short form, the matrix, the recommendation, the file path). The full detail lives in the file.
