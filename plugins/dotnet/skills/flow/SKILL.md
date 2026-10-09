---
name: flow
description: Spec-driven SDLC in one command - analyze, (spike), plan, implement, (tests), review, pr - with an approval gate after every step and a resumable spec folder per ticket.
argument-hint: "<ISSUE-KEY | details> [--no-tdd] | resume <KEY or slug> | status <KEY or slug>"
disable-model-invocation: true
---
# Spec-driven flow

Runs the SDLC skills of this plugin in order. You stop for the user's approval after every step. Each step follows its own skill: **Read `${CLAUDE_PLUGIN_ROOT}/skills/<step>/SKILL.md` when the step starts** (not earlier) and follow it, with the overrides below. Follow it exactly, including its `core:scout`/`core:runner` dispatches: don't do their searches, git, or build commands in the main session yourself. That's where the cost saving comes from.

## Spec folder
`.reports/<KEY or short-slug>/`. Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`. It holds:
- `analysis.md`: the analyze output. It overrides the path in the analyze skill.
- `plan.md`: the plan output. Always write it here, as if `--save` were given.
- `progress.md`: the source of truth for where the flow is:
  ```
  # Flow <KEY>: <summary>
  mode: tdd | code-first
  - [x] analyze - approved <yyyy-mm-dd>
  - [ ] spike - skipped | pending
  - [ ] plan
  - [ ] implement
  - [ ] tests - code-first only
  - [ ] review
  - [ ] pr
  notes: <revision feedback, decisions at gates>
  ```

`resume <KEY>`: read `progress.md`, `analysis.md`, and `plan.md` from the folder, then continue at the first unchecked step. Don't redo approved steps. `status <KEY>`: print `progress.md` and stop.

## Steps
1. **analyze**: `skills/analyze/SKILL.md`. If the input is already an analysis file, copy it in and go to the gate.
2. **spike** (conditional): only when the analysis lists an unknown that needs research before planning. At the gate, ask whether to run it: `skills/spike/SKILL.md`, with the result appended to `analysis.md` under `## Spike result`. Otherwise mark it skipped.
3. **plan**: `skills/plan/SKILL.md`, with `analysis.md` as the input.
4. **implement**: `skills/implement/SKILL.md`, with `plan.md` as the input. Pass the mode (`--no-tdd` → code-first). Implement's own stop-on-red rules apply inside the step.
5. **tests** (code-first mode only): offer `skills/tests/SKILL.md` for the behaviors implement listed as untested. Skip it in TDD mode.
6. **review**: `skills/review/SKILL.md` against the base branch. Fix high-severity findings only after the user approves them at the gate.
7. **pr**: `skills/pr/SKILL.md`. It asks again before committing and before creating the PR. Put the analysis goal and acceptance criteria in the PR description.

## Gate after every step
1. Update `progress.md` (step result plus any notes).
2. Show at most 15 lines: what the step produced, key decisions, open questions or risks, and the artifact path. The user opens the file for the full text; don't paste it.
3. Ask with one AskUserQuestion:
   - **Approve**: check the step off, then start the next one.
   - **Revise**: the user's feedback (from "Other" or a follow-up) goes into `notes`. Redo only this step and then come back to this gate.
   - **Pause**: stop here. Tell the user: `/clear`, then `/dotnet:flow resume <KEY>` to continue with a small context.

   After analyze and after plan, recommend Pause + resume to the user when the session is already long. A fresh session that reads the spec files costs less than carrying the whole history.

Never start the next step without an explicit Approve. Never skip a gate, even when the step looked trivial.
