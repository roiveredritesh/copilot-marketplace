---
name: implement
description: Execute a plan or task step by step - TDD by default (failing test first, then code, then green), or code-first with --no-tdd - with a Haiku build/test check after every step; stops on red instead of piling on changes.
argument-hint: "<plan file | 'the plan above' | task> [--no-tdd]"
disable-model-invocation: true
---
# Implement

Input: a plan (from `/dotnet:plan`, a file, or the conversation) or a single task. Without a plan, write a 3–7 step plan first (each step small, with its files and how it will be verified) and show it before starting.

**Mode.** TDD is the default. Use **code-first** mode when the user passes `--no-tdd` or asks for it in words ("without TDD", "no tests first", "bina TDD"). State the mode in your first line.

## TDD loop (default), one step at a time
Make the test style known first: if this session hasn't seen the repo's tests yet, use step 1 of `/dotnet:tests` (the scout house-style order).

For each step:

1. **Red.** Write the smallest test that expresses the step's behavior. Run `core:runner`:
   `DOTNET_TEST_FILTER="FullyQualifiedName~<NewTestName>" bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → return as printed.
   It must fail **for the expected reason** (assertion or missing member). A compile error in the test project counts as red only when the member doesn't exist yet. If it passes already, the behavior exists: adjust the step.
2. **Green.** Write the minimal production code to pass. Same runner order. Must report `TESTS PASSED`.
3. **Refactor** only if the step left duplication or an unclear name. Re-run.
4. **Step gate.** `core:runner`: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` (the full suite) → must be `TESTS PASSED`. Then print one line: `step <n>/<total> done - <files changed>`.

A step with no testable behavior (config, DI wiring) skips red/green with a one-line reason but still runs the step gate.

## Code-first loop (`--no-tdd`), one step at a time
1. **Code.** Make the step's change.
2. **Step gate.** `core:runner`: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test`. The existing suite must report `TESTS PASSED`, or `BUILD OK, no test projects` when the repo has no tests. Then print one line: `step <n>/<total> done - <files changed>`.

No new tests are written in this mode. At the end, list the behaviors left untested and suggest `/dotnet:tests <target>` for them.

## Rules (both modes)
- **Stop on red.** If a step or its gate fails twice in a row, stop, show the runner output and your hypothesis, and ask. Don't start the next step on a red build.
- Change only the files the step names. If another file must change, say so first.
- Database migrations: generate them, show the SQL (`dotnet ef migrations script`), and suggest a lock-safety check with `/postgresql:pg <file>` or `/sqlserver:mssql <file>` (whichever the repo uses). Don't apply them to a shared database.
- Guidance: when a step touches EF Core, ASP.NET Core, or hot-path/async code, read only the matching file from `${CLAUDE_PLUGIN_ROOT}/skills/guide/` (`efcore.md`, `aspnetcore.md`, `csharp-perf.md`).
- Don't commit. At the end, suggest `/dotnet:review` and then `/dotnet:pr`.

## Finish (at most 15 lines)
Mode, steps done, tests added (or behaviors left untested in code-first mode), final suite STATUS, open issues or follow-ups.
