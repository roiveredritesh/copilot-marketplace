---
name: implement
description: Execute a plan or task step by step with TDD (failing test first, then code, then green) and a Haiku build/test check after every step; stops on red instead of piling on changes.
argument-hint: "<plan file | 'the plan above' | task> [--no-tdd]"
disable-model-invocation: true
---
# Implement with TDD

Input: a plan (from `/dotnet:plan`, a file, or the conversation) or a single task. Without a plan, write a 3–7 step plan first (each step small, with its files and how it will be verified) and show it before starting.

Make the test style known: if this session hasn't seen the repo's tests yet, use step 1 of `/dotnet:tests` (the scout house-style order).

## Loop, one step at a time
For each step:

1. **Red.** Write the smallest test that expresses the step's behavior. Run `core:runner`:
   `DOTNET_TEST_FILTER="FullyQualifiedName~<NewTestName>" bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → return as printed.
   It must fail **for the expected reason** (assertion or missing member). A compile error in the test project counts as red only when the member doesn't exist yet. If it passes already, the behavior exists: adjust the step.
2. **Green.** Write the minimal production code to pass. Same runner order. Must report `TESTS PASSED`.
3. **Refactor** only if the step left duplication or an unclear name. Re-run.
4. **Step gate.** `core:runner`: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` (the full suite) → must be `TESTS PASSED`. Then print one line: `step <n>/<total> done - <files changed>`.

Rules:
- **Stop on red.** If green or the gate fails twice in a row, stop, show the runner output and your hypothesis, and ask. Don't start the next step on a red build.
- Change only the files the step names. If another file must change, say so first.
- Skip tests (`--no-tdd`, or a step with no testable behavior such as config or DI wiring) only with a one-line reason, but still run the build gate (`dotnet.sh build`).
- Database migrations: generate them, show the SQL (`dotnet ef migrations script`), and check them against `postgresql:pg` migration-safety. Don't apply them to a shared database.
- Don't commit. At the end, suggest `/dotnet:review` and then `/dotnet:pr`.

## Finish (at most 15 lines)
Steps done, tests added, final suite STATUS, open issues or follow-ups.
