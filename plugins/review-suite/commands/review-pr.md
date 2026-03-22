---
description: "Comprehensive code review of a GitHub pull request"
argument-hint: "<owner>/<repo> <pr-number> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write, Task]
---

# Command: /review-pr

## Usage

```
/review-pr <owner>/<repo> <pr-number> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **owner/repo**: GitHub repository identifier
  - Format: `owner/repo` (e.g., "microsoft/dotnet", "anthropics/claude-code")
  - Both parts required, case-sensitive

- **pr-number**: Pull request number
  - Format: Integer (e.g., 1234)
  - Examples: `/review-pr microsoft/dotnet 12345`

### Optional Flags

- **--async**: Execute in background
  - Returns immediately with task ID
  - Review happens asynchronously
  - Example: `/review-pr microsoft/dotnet 1234 --async`

- **--wait**: Execute synchronously, block until complete
  - Waits for review to complete
  - Returns full report
  - Example: `/review-pr microsoft/dotnet 1234 --wait`
  - Default if neither flag specified

- **--report=full|summary**
  - `full`: Comprehensive review report (default)
  - `summary`: Brief summary only
  - Example: `/review-pr microsoft/dotnet 1234 --report=summary`

## Examples

### Example 1: Quick Review (Sync, Full Report)
```
/review-pr microsoft/dotnet 12345 --wait
```
Output:
```
Reviewing PR: microsoft/dotnet#12345
[Analyzing code changes...]
[Checking security...]
[Assessing architecture...]
[Generating report...]

✅ Review Complete!

Report: marketplace/output/reviews/dotnet-pr-12345-review.md

Key Findings:
- Security: ✅ PASS
- Architecture: ⚠️ Minor issues
- Performance: ✅ PASS
- Tests: ✅ PASS
- Recommendation: APPROVE with suggestions
```

### Example 2: Background Review (Async)
```
/review-pr microsoft/dotnet 12345 --async
```
Output:
```
Starting background review...

Task ID: task-20251030-160000-pr-abc123
Status: Queued
Estimated time: 8-15 minutes

Check progress:
  /task-status task-20251030-160000-pr-abc123

When complete:
  marketplace/output/reviews/dotnet-pr-12345-review.md
```

### Example 3: Quick Summary (Async)
```
/review-pr microsoft/dotnet 12345 --async --report=summary
```
Output:
```
Starting background review (summary only)...

Task ID: task-20251030-160015-pr-def456
Estimated time: 3-8 minutes

Summary will be saved to:
  marketplace/output/reviews/dotnet-pr-12345-summary.md
```

### Example 4: Known Repository Shorthand
```
/review-pr my-repo 567

# Assumes context from recent work
# Expands to: /review-pr my-org/my-repo 567
```

## Implementation

### Step 1: Parse and Validate Arguments

```
1. Parse input:
   - Extract owner/repo (validate format)
   - Extract pr-number (validate integer)
   - Extract flags (--async, --wait, --report)

2. Validate parameters:
   - owner/repo contains exactly one slash
   - Both owner and repo non-empty
   - pr-number is valid positive integer
   - Flags are recognized
   - No conflicting flags (--async and --wait together)

3. Set execution mode:
   - If --async: mode = async
   - If --wait: mode = sync
   - If neither: mode = sync (default)

4. Set report level:
   - If --report=summary: report_level = summary
   - If --report=full or not specified: report_level = full
```

### Step 2: Authentication Check

```
1. Verify GitHub MCP is available:
   - Check .mcp.json for github server config
   - Verify credentials are set

2. If unavailable:
   - Return error: "GitHub MCP server not configured"
   - Provide setup instructions

3. If available:
   - Proceed to Step 3
```

### Step 3: Queue or Execute Review Task

**For Async Execution:**
```
1. Create task entry in .claude/task-queue.json:
   {
     "task_id": "task-20251030-160000-pr-abc123",
     "type": "pr-review",
     "status": "queued",
     "owner": "microsoft",
     "repo": "dotnet",
     "pr_number": 12345,
     "report_level": "full",
     "created": "2025-10-30T16:00:00Z",
     "estimated_completion": "2025-10-30T16:10:00Z"
   }

2. Return immediately:
   Task ID: task-20251030-160000-pr-abc123
   Status: Queued
   Estimated time: 8-15 minutes
   Check: /task-status task-20251030-160000-pr-abc123

3. Background task coordinator processes the task
   - Fetches PR details via GitHub MCP
   - Analyzes code changes
   - Generates comprehensive report
   - Updates task status
```

**For Sync Execution:**
```
1. Display progress:
   Reviewing PR: microsoft/dotnet#12345
   [Analyzing code changes...]
   [Checking security...]
   [Assessing architecture...]
   [Generating report...]

2. Delegate to pr-comprehensive-reviewer agent
   - Wait for agent to complete
   - Receive report data

3. Display report or summary
   - Full report: Show all details
   - Summary: Show key findings only

4. Return completion message with report location
```

### Step 4: Return Response

**Async Response:**
```
Status: Queued
Task ID: task-20251030-160000-pr-abc123
Estimated time: 8-15 minutes

Check progress:
  /task-status task-20251030-160000-pr-abc123

Report will be saved to:
  marketplace/output/reviews/microsoft-dotnet-pr-12345-review.md
```

**Sync Response (Full Report):**
```
# PR Review: microsoft/dotnet#12345

[Full report content]

Report saved to: marketplace/output/reviews/microsoft-dotnet-pr-12345-review.md
```

**Sync Response (Summary):**
```
# PR Review Summary: microsoft/dotnet#12345

## Key Findings
- Security: ✅ PASS
- Architecture: ⚠️ Review needed
- Performance: ✅ PASS

## Recommendations
[Brief recommendations]

Full report: marketplace/output/reviews/microsoft-dotnet-pr-12345-review.md
```

---

## Input Validation

### Valid Inputs
```
✅ /review-pr microsoft/dotnet 12345
✅ /review-pr microsoft/dotnet 12345 --wait
✅ /review-pr microsoft/dotnet 12345 --async
✅ /review-pr microsoft/dotnet 12345 --async --report=summary
✅ /review-pr my-org/my-repo 567
```

### Invalid Inputs
```
❌ /review-pr microsoft dotnet 12345          (missing slash)
❌ /review-pr microsoft/dotnet abc            (non-numeric PR number)
❌ /review-pr microsoft/dotnet -100           (negative PR number)
❌ /review-pr microsoft/dotnet/extra 12345    (extra slash)
❌ /review-pr microsoft/dotnet 12345 --wait --async  (conflicting flags)
❌ /review-pr microsoft/dotnet 12345 --report=invalid (invalid report type)
```

### Error Messages

**Invalid Format:**
```
Error: Invalid repository format
Expected: /review-pr owner/repo <number>
Example: /review-pr microsoft/dotnet 12345
You provided: microsoft dotnet 12345
```

**Invalid PR Number:**
```
Error: PR number must be a positive integer
You provided: "abc"
Example: /review-pr microsoft/dotnet 12345
```

**GitHub MCP Unavailable:**
```
Error: GitHub MCP server not configured
To use this command, set up the GitHub MCP server:

1. Add to .mcp.json:
   "github": {
     "command": "npx",
     "args": ["@modelcontextprotocol/server-github"],
     "env": {
       "GITHUB_TOKEN": "your-token"
     }
   }

2. Restart Claude Code

For help: https://docs.claude.com/mcp/github
```

---

## Output Locations

### Report Files
```
Full Review:   marketplace/output/reviews/<owner>-<repo>-pr-<number>-review.md
Summary:       marketplace/output/reviews/<owner>-<repo>-pr-<number>-summary.md
Status:        .claude/task-status/<task-id>.md
```

### Example Paths
```
marketplace/output/reviews/microsoft-dotnet-pr-12345-review.md
marketplace/output/reviews/my-org-my-repo-pr-567-summary.md
.claude/task-status/task-20251030-160000-pr-abc123.md
```

---

## Typical Analysis Time

- **Small PR** (< 100 lines, 2-3 files): 3-8 minutes
- **Medium PR** (100-500 lines, 5-10 files): 8-15 minutes
- **Large PR** (> 500 lines, 10+ files): 15-30 minutes
- **Complex PR** (architecture changes): 20-45 minutes

**Recommendation**: Use `--async` for anything larger than a small PR.

---

## Integration with GitHub

### What Data Is Accessed

Via GitHub MCP, this command accesses:
- PR metadata (title, description, author, reviewers)
- PR diff (changed lines)
- File metadata (names, extensions)
- Commit information
- Related issues/discussions (if referenced)

### What Data Is NOT Accessed

- Sensitive information in code comments
- Hardcoded secrets (reviewed but not exposed)
- Private repository content (if not authorized)

### Authentication

Uses GitHub token from MCP configuration:
```json
{
  "github": {
    "command": "npx",
    "args": ["@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
    }
  }
}
```

---

## Review Standards Applied

This command triggers comprehensive review following standards from CLAUDE.md:

### Critical Priority Review Areas
1. **Security**: SQL injection, XSS, auth bypass, hardcoded secrets
2. **Breaking Changes**: API compatibility, schema changes, dependency impacts
3. **Performance**: N+1 queries, memory leaks, async patterns, LOH usage
4. **Integration Risks**: Service calls, transactions, dependencies
5. **Error Handling**: Exception handling, logging, rollback

### Domain-Specific Review
- **C#/.NET**: SOLID principles, async/await, memory management, IDisposable
- **ASP.NET WebForms**: Lifecycle, ViewState, postback flow, Telerik controls
- **Database**: LINQ queries, transactions, concurrency handling
- **Architecture**: Layering, separation of concerns, extensibility

---

## Related Commands

- `/task-status <task-id>` - Check progress on async reviews
- `/validate-solution <file>` - Validate proposed solutions
- `/review-pr-list <owner>/<repo>` - List open PRs
- `/team-review <pr-number>` - Request team review consensus

---

## FAQ

**Q: What if my repository is private?**
A: Ensure your GitHub token has access to the private repository. The MCP server uses your configured token.

**Q: Can I review multiple PRs at once?**
A: Run the command multiple times with `--async` to queue them. Each will be reviewed independently.

**Q: How detailed is the review?**
A: Very detailed! Full reports include security, architecture, performance, testing, and documentation assessment with specific line-by-line feedback.

**Q: Can I customize review criteria?**
A: The review follows CLAUDE.md standards. Contact your team lead to customize review standards.

**Q: What if the PR hasn't been fetched yet?**
A: The command will fetch all necessary information from GitHub. Just provide the repository and PR number.

**Q: Can I review PRs from other repositories?**
A: Yes! Provide the `owner/repo` and PR number from any GitHub repository you have access to.

**Q: How long does a review take?**
A: Typical times:
- Small PR: 3-8 minutes
- Medium PR: 8-15 minutes
- Large PR: 15-30 minutes

**Q: Where are reports saved?**
A: Reports are saved to:
`marketplace/output/reviews/<owner>-<repo>-pr-<number>-review.md`

**Q: Can I export the review?**
A: Yes! Reports are markdown files. Copy from `marketplace/output/reviews/` to share.

**Q: What if the PR has conflicts?**
A: The review analyzes the code changes. Merge conflicts are noted if present.

**Q: Can I get the review as JSON?**
A: Reports are markdown. For structured data, parse the markdown or request custom format.

---

## Pro Tips

**Tip 1: Use Async for Large PRs**
Large PRs take longer. Use `--async` so you don't wait:
```
/review-pr my-org/my-repo 1234 --async
```

**Tip 2: Quick Assessment with Summary**
Need just key findings? Use summary report:
```
/review-pr my-org/my-repo 1234 --report=summary
```

**Tip 3: Batch Reviews**
Queue multiple reviews:
```
/review-pr my-org/my-repo 1234 --async
/review-pr my-org/my-repo 1235 --async
/review-pr my-org/my-repo 1236 --async
```

**Tip 4: Check Progress**
Monitor async reviews:
```
/task-status task-20251030-160000-pr-abc123
```

**Tip 5: Share Findings**
Reports are shareable markdown:
```
Copy: marketplace/output/reviews/my-repo-pr-1234-review.md
Share: Send to team/customer
```

**Tip 6: Team Discussion**
Use reports as basis for code review discussions:
1. Run `/review-pr`
2. Share report with reviewers
3. Discuss findings together

---

## Troubleshooting

### GitHub MCP Not Available
```
Error: GitHub MCP server not configured

Solution:
1. Check .mcp.json in project root
2. Verify github server is configured
3. Ensure GITHUB_TOKEN is set
4. Restart Claude Code
```

### Invalid Repository
```
Error: Repository not found: invalid/repo

Solution:
1. Verify repository name is correct
2. Check you have access to repository
3. Confirm repository is public or token has access
```

### PR Not Found
```
Error: PR #12345 not found in invalid/repo

Solution:
1. Verify PR number is correct
2. Check repository name matches PR repo
3. Ensure PR is open (not draft)
```

### Timeout
```
Error: Review timed out after 45 minutes

Solution:
1. Very large PRs may timeout
2. Try breaking into smaller PRs
3. Use --async for better timeout handling
```

---

## Command Lifecycle

```
1. User runs: /review-pr microsoft/dotnet 12345

2. Command validates:
   - Argument format correct
   - PR number valid
   - GitHub MCP available

3. Command queues task:
   - Creates task entry in queue
   - Sets status to "queued"
   - Assigns task ID

4. Background coordinator processes:
   - Picks up task from queue
   - Delegates to pr-comprehensive-reviewer agent
   - Agent fetches PR details
   - Agent analyzes code
   - Agent generates report

5. Report saved:
   - marketplace/output/reviews/<repo>-pr-<number>-review.md

6. User checks progress:
   - /task-status <task-id>
   - Views report when ready
```

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Associated Plugin**: Review Suite
**Delegated To**: pr-comprehensive-reviewer agent
**Task Coverage**: Task #3 (Review PRs on GitHub)
