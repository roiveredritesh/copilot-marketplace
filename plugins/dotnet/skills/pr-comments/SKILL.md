---
name: pr-comments
description: Work through the review comments on a GitHub PR - a Haiku runner saves every unresolved thread to a file, the main session verifies each against the code, fixes what's valid with a regression test, drafts a reply per thread, and posts replies only after approval.
argument-hint: "[PR number | URL] [--draft-only]"
disable-model-invocation: true
---
# Address PR review comments

No PR number: use the PR of the current branch (`gh pr view --json number --jq .number`).

## 1. Fetch everything to files: one `core:runner` work order
The runner only runs commands and returns the index. It never summarizes or drops comments. Full text stays in the files.
```text
WORK ORDER
goal: save all open review feedback on PR <n> to files and return the index
steps:
  1. p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"; mkdir -p .reports/pr-<n>
  2. gh pr view <n> --json number,title,headRefName,baseRefName,author --jq '"\(.number) \(.title) | \(.headRefName) -> \(.baseRefName) | author \(.author.login)"'; git branch --show-current
  3. gh api graphql --paginate -F owner='{owner}' -F name='{repo}' -F n=<n> -f query='query($owner:String!,$name:String!,$n:Int!,$endCursor:String){repository(owner:$owner,name:$name){pullRequest(number:$n){reviewThreads(first:50,after:$endCursor){pageInfo{hasNextPage endCursor} nodes{id isResolved isOutdated path line originalLine comments(first:100){nodes{databaseId author{login} body}}}}}}}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "THREAD \(.id) \(.path):\(.line // .originalLine // "?")\(if .isOutdated then " (outdated)" else "" end) | \(.comments.nodes | length) comments | \(.comments.nodes[0].author.login): \(.comments.nodes[0].body | split("\n")[0] | .[0:90])\n" + ([.comments.nodes[] | "--- [\(.databaseId)] \(.author.login):\n\(.body)"] | join("\n")) + "\nEND THREAD\n"' > .reports/pr-<n>/threads.md
  4. gh pr view <n> --json reviews,comments --jq '(.reviews[] | select(.body != "") | "REVIEW \(.author.login) \(.state)\n\(.body)\nEND"), (.comments[] | "COMMENT \(.author.login)\n\(.body)\nEND")' > .reports/pr-<n>/conversation.md
  5. grep -c '^THREAD' .reports/pr-<n>/threads.md; grep '^THREAD' .reports/pr-<n>/threads.md | head -n 150; grep -E '^(REVIEW|COMMENT) ' .reports/pr-<n>/conversation.md | sort | uniq -c
return: the output of steps 2 and 5 exactly as printed
on-error: BLOCKED: <the error line>
```
If `gh` is unavailable or unauthenticated, send the same request to `publisher` (GitHub MCP), which writes the same two files. Never call GitHub MCP tools from the main session.

If the current branch isn't the PR's head branch, ask before switching (`gh pr checkout <n>`). With uncommitted changes, stop and say so.

## 2. Triage (main session)
Work from the files, not from memory. For each `THREAD` in the index, read its full block in `threads.md` (Grep for the thread id, then Read that range), then read the code at `path:line` yourself at the current HEAD (about 30 lines around it). A reviewer can be wrong, and an outdated thread may already be fixed. With more than 15 threads, go in batches of 15 and keep only the table row for each one.

| Class | When | Action |
|---|---|---|
| **fix** | the comment is correct and in scope | change the code |
| **answer** | a question, no change needed | reply with the explanation and `path:line` evidence |
| **push back** | you disagree | reply with the reason and evidence (code, docs, a test). Be polite, no change |
| **defer** | valid but out of scope | reply with a follow-up proposal (ticket title) |
| **done** | already addressed (often outdated) | reply with where it was fixed |
| **decide** | reviewers conflict, or it's a product/design choice | put both positions to the user at the gate |

- A ```` ```suggestion ```` block is the reviewer's exact replacement for the commented lines. If it's correct, apply it verbatim (class fix).
- Read the whole thread, not just the first comment. Later replies may narrow, change, or withdraw the request, or the author may have already answered.
- Bot comments (CI, coverage, linters) count only when they ask for a change. Don't reply to bots.
- In `conversation.md`, review bodies and comments get the same treatment when they ask for something.

## 3. Gate: AskUserQuestion
Show a table: `# | path:line | reviewer | ask (one line) | class | planned change or reply gist`. Mark the fixes that change behavior (bugs, validation) with `+test`. List `decide` items first, with each side's position. Ask two questions in **one** AskUserQuestion call:
1. Which fixes, with exactly these four options: `Apply all fixes` / `Apply some` (description: "type the numbers to fix in Other, e.g. fix 12 only") / `Drafts only, no code changes` / `Cancel`. Always offer all four. Decide items are answered in the same reply (Other) or as their own option text.
2. Regression tests for the `+test` fixes (skip this question when there are none; ignore the answer when the user picks drafts only or cancel): **yes, a test that fails before each fix (Recommended)** / **no, fixes only**.

Don't edit anything before these answers. Fix only the items the user approved. An unapproved fix item gets no code change; its reply is drafted as an acknowledgement or follow-up instead.

## 4. Fix
- Apply only the user-approved fixes, smallest change per thread, in the repo's style. Change only the files the fix needs.
- If the user chose tests: each `+test` fix gets a regression test that fails before the fix (follow `/dotnet:implement`'s red/green), when the repo has tests. If they chose no tests, change only the code, and list the untested behavior fixes in the report. Renames, style, and comment-only fixes never get tests.
- Then `core:runner`: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" test` → must be `TESTS PASSED` (or `BUILD OK, no test projects`). On red: stop, show the output, ask.

## 5. Draft replies
Write one file per reply to `.reports/pr-<n>/reply-<databaseId of the thread's first comment>.md`, plus `.reports/pr-<n>/replies.md` listing them all (thread, class, reply).
Reply style: 1-4 sentences, specific, no filler ("Great catch!"). For fixes, say what changed and name the test: "Fixed: the loop starts at 0 now (`Cart.cs:14`); covered by `CartTotal_CountsFirstLine`". Add the commit hash after the push. For `decide` items, reply only after the user decides.

## 6. Commit, push, post: each needs its own yes
1. **Commit + push.** Show the files and the message (repo convention, e.g. `fix: address review comments on #<n>`). Ask, then `git add <files>`, `git commit -F <file>`, `git push`.
2. **Post replies** (skip with `--draft-only`). Show `replies.md`, then ask **post all** / pick (via Other) / don't post. Post with `core:runner`, one command per reply:
   `gh api repos/{owner}/{repo}/pulls/<n>/comments/<databaseId>/replies -F body=@<reply file> --jq .html_url`
   For a conversation-level reply: `gh pr comment <n> --body-file <file>`.
3. **Resolve threads** only when the user asks: `gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -F id=<THREAD id>`. By default, the reviewer resolves.

## 7. Report (at most 15 lines)
Threads handled per class (and the total from the index, so nothing is silently missed), files changed, tests added (or untested behavior fixes when the user chose no tests), test STATUS, commit, replies posted (URLs) or the path of the drafts.
