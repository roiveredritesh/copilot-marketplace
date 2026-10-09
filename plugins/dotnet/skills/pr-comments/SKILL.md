---
name: pr-comments
description: Work through the review comments on a GitHub PR - fetch unresolved threads with a Haiku runner, verify each against the code, fix what's valid, draft a reply per thread, and post replies only after approval.
argument-hint: "[PR number | URL] [--draft-only]"
disable-model-invocation: true
---
# Address PR review comments

No PR number: use the PR of the current branch (`gh pr view --json number --jq .number`).

## 1. Facts: one `core:runner` work order
```text
WORK ORDER
goal: collect open review feedback on PR <n>
steps:
  1. gh pr view <n> --json number,title,url,headRefName,baseRefName,author --jq '"\(.number) \(.title) | \(.headRefName) -> \(.baseRefName) | author \(.author.login)"'; git branch --show-current
  2. gh api graphql -F owner='{owner}' -F name='{repo}' -F n=<n> -f query='query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviewThreads(first:100){nodes{id isResolved isOutdated path line comments(first:20){nodes{databaseId author{login} body}}}}}}}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "THREAD \(.id) \(.path):\(.line // "?")\(if .isOutdated then " (outdated)" else "" end)\n" + ([.comments.nodes[] | "  [\(.databaseId)] \(.author.login): \(.body | split("\n") | .[0:12] | join("\n    "))"] | join("\n"))'
  3. gh pr view <n> --json reviews,comments --jq '(.reviews[] | select(.body != "") | "REVIEW \(.author.login) \(.state): \(.body | split("\n") | .[0:10] | join(" / "))"), (.comments[-15:][] | "COMMENT \(.author.login): \(.body | split("\n") | .[0:6] | join(" / "))")'
return: the outputs as printed, labelled 1-3, at most 200 lines
on-error: BLOCKED: <the error line>
```
If `gh` is unavailable or unauthenticated, send the same request to `publisher` (GitHub MCP) with the same return format. Never call GitHub MCP tools from the main session.

If the current branch isn't the PR's head branch, ask before switching (`gh pr checkout <n>`). With uncommitted changes, stop and say so.

## 2. Triage (main session)
For every unresolved thread, read the code at `path:line` yourself (about 30 lines around it, at the current HEAD). A reviewer can be wrong, and an outdated thread may already be fixed. Classify each one:

| Class | When | Action |
|---|---|---|
| **fix** | the comment is correct and in scope | change the code |
| **answer** | a question, no change needed | reply with the explanation and `path:line` evidence |
| **push back** | you disagree | reply with the reason and evidence (code, docs, a test). Be polite, no change |
| **defer** | valid but out of scope | reply with a follow-up proposal (ticket title) |
| **done** | already addressed (often outdated) | reply with where it was fixed |

Review summary bodies and conversation comments get the same treatment when they ask for something.

## 3. Gate: AskUserQuestion
Show a table: `# | path:line | reviewer | ask (one line) | class | planned change or reply gist`. Ask: **apply as proposed** / change classes (the user names them via Other) / cancel. Don't edit anything before this answer.

## 4. Fix
Apply the approved fixes, smallest change per thread. Respect the repo's style; follow `/dotnet:implement`'s rule: change only the files the fix needs. Then `core:runner`: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → must be `TESTS PASSED` (or `BUILD OK, no test projects`). On red: stop, show the output, ask.

## 5. Draft replies
Write one file per reply to `.reports/pr-<n>/reply-<databaseId of the thread's first comment>.md`, plus `.reports/pr-<n>/replies.md` listing them all (thread, class, reply). Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`.
Reply style: 1-4 sentences, specific, no filler ("Great catch!"). For fixes, say what changed: "Fixed: now validates `percent` before rounding (`CatalogItem.cs:41`)". Add the commit hash after the push.

## 6. Commit, push, post: each needs its own yes
1. **Commit + push.** Show the files and the message (repo convention, e.g. `fix: address review comments on #<n>`). Ask, then `git add <files>`, `git commit -F <file>`, `git push`.
2. **Post replies** (skip with `--draft-only`). Show `replies.md`, then ask **post all** / pick (via Other) / don't post. Post with `core:runner`, one command per reply:
   `gh api repos/{owner}/{repo}/pulls/<n>/comments/<databaseId>/replies -F body=@<reply file> --jq .html_url`
   For a conversation-level reply: `gh pr comment <n> --body-file <file>`.
3. **Resolve threads** only when the user asks: `gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -F id=<THREAD id>`. By default, the reviewer resolves.

## 7. Report (at most 15 lines)
Threads handled per class, files changed, test STATUS, commit, replies posted (URLs) or the path of the drafts.
