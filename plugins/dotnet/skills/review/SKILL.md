---
name: review
description: Review the current branch or a GitHub PR for bugs, security issues, and breaking changes, with tests run by a Haiku runner in parallel.
argument-hint: "[base-branch | PR number] [--save]"
disable-model-invocation: true
---
# Review changes

You (the main session) do the judging. Haiku agents only fetch and run things. Keep everything you read proportional to the change.

## 1. Scope
- Argument is a PR number or URL: `gh pr view <n> --json number,title,baseRefName,headRefName,additions,deletions,files --jq '{title,baseRefName,headRefName,additions,deletions,files:[.files[].path]}'`. The diff source is `gh pr diff <n>`. If `gh` is missing or not authenticated, fall back to plain git (no MCP needed): `git fetch origin pull/<n>/head:pr-<n>`, then diff `origin/<base>...pr-<n>` (base `main` unless the user names one). For metadata (title, base) only, dispatch `publisher` (GitHub MCP) if it is set up. Never call GitHub MCP tools from the main session.
- Otherwise: base = the first argument, else `main`, else `master`. Let `MB=$(git merge-base <base> HEAD)`. The diff is `git diff $MB` (includes uncommitted work).
- Run `git diff --shortstat $MB` (or use the PR's additions/deletions) to size it.

## 2. Dispatch in ONE message (parallel)
- `core:runner`, work order: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → return the output as printed. Skip it for a remote PR not checked out locally.
- Only if the diff is **over 600 changed lines**: split the changed files into chunks of about 400 lines (keep a file's tests with it) and give each chunk to `core:reviewer` (at most 4) with the base ref. You then review only cross-file concerns.

## 3. Review (diff ≤ 600 lines, or cross-file concerns)
Read the diff file by file (`git diff $MB -- <file>`). Open surrounding code only when the hunk alone isn't enough. Apply [checklist.md](checklist.md). For EF Core, ASP.NET Core, or hot-path/async changes, also read the matching file from `${CLAUDE_PLUGIN_ROOT}/skills/guide/` (`efcore.md`, `aspnetcore.md`, `csharp-perf.md`).
When a public signature, DTO, DB column, config key, or route changed, send `core:scout` a work order: "find callers/usages of <symbol> outside <changed files>; return path:line, at most 30 lines".

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact in the report, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 4. Report (chat; at most 60 lines)
```
Verdict: approve | approve with nits | changes requested
Build/tests: <runner STATUS line>
| Sev | Location | Problem | Fix |
```
Most severe first, real problems only (no style nits unless asked). End with "Not checked:" if any part was skipped.
Last line, always: `Steps: scope=<base..head, n lines> dispatched=<scout, runner, reviewer as used> verified=<n refs opened>`. Fill every key; write `skipped (<reason>)` rather than leaving one out.
With `--save`, also write the report to `.reports/review-<branch-or-pr>-<yyyymmdd>.md` and print the path. Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`.
