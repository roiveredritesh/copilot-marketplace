---
name: pr
description: Commit the current changes with a message in the repo's convention and open a GitHub PR with a generated description (gh first, GitHub MCP via publisher as fallback). Asks once, showing exactly what will be committed, pushed, and opened.
argument-hint: "[base-branch] [--draft] [--commit-only]"
disable-model-invocation: true
---
# Commit and PR

## 1. Facts: one `core:runner` work order
```text
steps:
  1. git branch --show-current; git rev-parse --abbrev-ref origin/HEAD 2>/dev/null
  2. git status --short | head -n 40
  3. git diff --stat HEAD | tail -n 25
  4. git log -12 --format=%s
  5. gh auth status 2>&1 | head -n 3
  6. git remote get-url origin; gh repo view --json nameWithOwner --jq .nameWithOwner 2>&1 | head -n 1
return: the outputs, labelled, at most 80 lines
```

## 2. Prepare (main session)
- The diff content: read `git diff HEAD -- <file>` for files whose purpose isn't clear from their names, and reuse a `/dotnet:review` result from this session if there is one.
- **Never commit** secrets, `.env` files, `bin/`/`obj/`, or unrelated files. List anything suspicious and leave it unstaged.
- Commit message: follow the convention visible in `git log` (Conventional Commits like `feat(api): ...` if used, else an imperative summary under 72 characters), then a body with *why*, not a file list. Add the `Co-Authored-By` line your session instructions specify, if any.
- On the default branch: propose a branch name (`feat/<slug>`, `fix/<slug>`) and create it before committing.

## 3. Confirm, then act
Show the files to stage, the commit message, and (unless `--commit-only`) the PR title and body. Ask once (AskUserQuestion: **commit + push + PR** / commit only / edit / cancel), naming the remote and branch the push goes to. If step 6 shows `origin` isn't a GitHub repo (and no `publisher` is set up), don't offer the PR option: offer commit only / edit / cancel and say why. Then:
1. `git add <files>` (explicit paths, never `git add -A` blindly) and `git commit -F <message file>`.
2. `git push -u origin <branch>`.
3. `gh pr create --base <base> --title "<title>" --body-file <file> [--draft]`.
   If `gh` is unavailable or unauthenticated, send the same title/body to `publisher` (GitHub MCP) with the return `pr number | url`.
4. Last line, always: `Steps: facts=<runner> confirm=<asked: choice> commit=<hash | no> push=<remote/branch | no> pr=<url | no>`. Fill every key; write `skipped (<reason>)` rather than leaving one out.

PR body template:
```
## Summary
<what and why, 2-4 lines>
## Changes
- <grouped by area, not by file>
## Testing
- <what ran: /dotnet:build test STATUS, new tests, manual checks>
## Risks / rollout
- <migrations, config changes, feature flags, breaking API changes; "none" if none>
```
Print the PR URL. Don't merge or enable auto-merge.
