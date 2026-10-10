---
name: tests
description: Write or extend tests for .NET code in the repo's existing test style (xUnit/NUnit/MSTest, mocks, assertions), run them through a Haiku runner, and optionally report coverage.
argument-hint: "<class | method | file | feature> [--coverage]"
disable-model-invocation: true
---
# Write tests

## 1. Learn the house style: one `core:scout` work order
"scope: tests/** and **/*Tests*.csproj | target: <exact type or file under test>. Return at most 40 lines: (a) the test project(s) covering the target and their framework (xUnit/NUnit/MSTest), (b) mocking library (Moq/NSubstitute/FakeItEasy/none), assertion library (FluentAssertions/Shouldly/built-in), (c) one existing test file closest to <target> (path), (d) fixtures/builders/test-data helpers (path:line), (e) integration-test setup if present (WebApplicationFactory, Testcontainers, a test DB)."
Read the closest test file yourself, then match its naming, layout (Arrange/Act/Assert), and helpers. Don't add a new test library when one is already used.

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact in the report, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 2. Decide what to test (main session)
Read <target>. List the behaviors: the happy path, each branch, validation failures, boundary values, null and empty inputs, exceptions, and async cancellation. One test per behavior, with names stating the behavior (`Method_Condition_ExpectedResult` or the repo's convention).
- Unit tests: the class under test plus mocks for its I/O dependencies only. Don't mock what you own when the real thing is cheap.
- API endpoints: `WebApplicationFactory<Program>` integration tests (see [patterns.md](patterns.md)).
- PostgreSQL-specific behavior (SQL, constraints, jsonb, migrations): Testcontainers, not the EF in-memory provider.

## 3. Write, then run: `core:runner` work order
`DOTNET_TEST_FILTER="FullyQualifiedName~<TestClassName>" bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → return the output as printed.
- `TESTS FAILED` because of a test bug: fix the test. Because of a real product bug: stop and report it with the failing test as evidence. Don't change product code unless the user asked.
- `NO TESTS MATCHED`: fix the filter or the test discovery (attributes, public class).
At most 3 run/fix rounds, then report what remains.

## 4. Coverage (`--coverage`)
`core:runner`: `DOTNET_COVERAGE_FILE_REGEX="<target file name>" bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" coverage` → return as printed. Add tests for uncovered branches that matter. Don't chase 100%.

## 5. Report (at most 20 lines)
Tests added (file + names), the run's STATUS line, coverage before/after when measured, and any product bugs found.
Last line, always: `Steps: style=<scout dispatched | known> run=<STATUS> rounds=<n> coverage=<measured | not asked>`. Fill every key; write `skipped (<reason>)` rather than leaving one out.
