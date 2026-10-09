---
name: review
description: Review the current branch or a GitHub PR for bugs, security issues, and breaking changes, with tests run by a Haiku runner in parallel.
argument-hint: "[base-branch | PR number] [--save]"
disable-model-invocation: true
---
# Review changes

You (the main session) do the judging. Haiku agents only fetch and run things. Keep everything you read proportional to the change.

## 1. Scope
- Argument is a PR number or URL: `gh pr view <n> --json number,title,baseRefName,headRefName,additions,deletions,files --jq '{title,baseRefName,headRefName,additions,deletions,files:[.files[].path]}'`. The diff source is `gh pr diff <n>`. If `gh` is missing or not authenticated, fall back to the GitHub MCP if one is available, else stop and say so.
- Otherwise: base = the first argument, else `main`, else `master`. Let `MB=$(git merge-base <base> HEAD)`. The diff is `git diff $MB` (includes uncommitted work).
- Run `git diff --shortstat $MB` (or use the PR's additions/deletions) to size it.

## 2. Dispatch in ONE message (parallel)
- `core:runner`, work order: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → return the output as printed. Skip it for a remote PR not checked out locally.
- Only if the diff is **over 600 changed lines**: split the changed files into chunks of about 400 lines (keep a file's tests with it) and give each chunk to `core:reviewer` (at most 4) with the base ref. You then review only cross-file concerns.

## 3. Review (diff ≤ 600 lines, or cross-file concerns)
Read the diff file by file (`git diff $MB -- <file>`). Open surrounding code only when the hunk alone isn't enough. Apply [checklist.md](checklist.md).
When a public signature, DTO, DB column, config key, or route changed, send `core:scout` a work order: "find callers/usages of <symbol> outside <changed files>; return path:line, at most 30 lines".

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact in the report, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 4. Report (chat; at most 60 lines)
```
Verdict: approve | approve with nits | changes requested
Build/tests: <runner STATUS line>
| Sev | Location | Problem | Fix |
```
Most severe first, real problems only (no style nits unless asked). End with "Not checked:" if any part was skipped.
With `--save`, also write the report to `~/.claude/reports/<repo-folder-name>/review-<branch-or-pr>-<yyyymmdd>.md` and print the path.
