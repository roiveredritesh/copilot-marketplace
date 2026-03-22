---
description: "Identify when and where regression was introduced using git history"
argument-hint: "<feature> [--since=date] [--report=full|summary]"
allowed-tools: [Bash, Glob, Grep, Read, Write]
---

# Command: /find-regression

## Usage

```
/find-regression <feature> [--since=date] [--until=date] [--author=name] [--file=path] [--report=full|summary]
```

## Arguments

### Required Arguments

- **feature**: Description of the feature that regressed
  - What worked before and doesn't work now
  - Observable behavior change
  - Specific functionality affected
  - Examples:
    - "User profile page loading"
    - "Payment processing workflow"
    - "Email notification delivery"
    - "Shopping cart total calculation"

### Optional Flags

- **--since=date**: Start date for git history search
  - Examples: "2025-01-01", "2 weeks ago", "30 days ago"
  - Default: 30 days ago

- **--until=date**: End date for git history search
  - Examples: "2026-01-15", "today", "yesterday"
  - Default: now

- **--author=name**: Filter by commit author
  - Example: "john.doe@example.com" or "John Doe"
  - Useful for focusing on specific developer's changes

- **--file=path**: Specific file to focus on (if known)
  - Example: "UserService.cs" or "src/Services/UserService.cs"
  - Narrows search scope

- **--report=full|summary**: Report level (default: `full`)
  - `full`: Comprehensive analysis with git details and fix options
  - `summary`: Condensed findings with breaking commit info

## Examples

```bash
# Basic regression analysis
/find-regression "User profile page loading"

# Regression in last 2 weeks
/find-regression "Payment processing workflow" --since="2 weeks ago"

# Regression by specific author
/find-regression "Email notification delivery" --author="john.doe@example.com"

# Regression in specific file
/find-regression "Shopping cart total calculation" --file="CartService.cs"

# Regression with summary report
/find-regression "API authentication" --since="1 month ago" --report=summary
```

## Prerequisites

- **Git repository required**: This command requires a git repository with commit history
- If not in a git repo, command will fail with error message
- If git history is insufficient (too few commits), results may be incomplete

## Implementation

### Step 1: Verify Git Repository
Check if current directory is a git repository:
```bash
git rev-parse --git-dir
```

If not, return error:
```
❌ Git repository not found.

Regression analysis requires git history to identify when code changed.

Please ensure:
- You're in a git repository directory
- The directory has been initialized with `git init`
- There are commits in the repository
```

### Step 2: Parse Arguments
- Extract feature description
- Extract optional flags (since, until, author, file, report)
- Set defaults (since: 30 days ago, until: now, report: full)
- Validate date formats

### Step 3: Delegate to Agent
Load and execute **regression-analyzer** agent with parameters:
- feature_description: User-provided feature
- date_range: (since, until)
- author_filter: Author name (if specified)
- file_filter: File path (if specified)
- report_level: full or summary

### Step 4: Execute Agent Process
Agent performs 6-phase analysis:
1. **Feature Definition & Expected Behavior** (8-10% of time)
   - Parse feature description
   - Map to code components (using Grep)
   - Define analysis scope

2. **Git History Traversal & Commit Collection** (20-25% of time)
   - Execute git log for date range
   - Collect commit metadata
   - Categorize by relevance
   - Build timeline

3. **Git Blame Analysis & Code Authorship** (15-18% of time)
   - Use git blame on error locations
   - Identify who modified code
   - Cross-reference with timeline

4. **Breaking Commit Identification** (25-30% of time) [CRITICAL]
   - Analyze suspect commits
   - Review code diffs
   - Identify breaking changes
   - Verify hypothesis

5. **Related Change Correlation** (12-15% of time)
   - Identify related commits
   - Check for compound regressions
   - Build complete timeline

6. **Fix Recommendations & Prevention** (10-12% of time)
   - Generate revert option
   - Generate forward fix
   - Generate comprehensive solution
   - Provide git commands

### Step 5: Generate Report
Write comprehensive markdown report to:
`marketplace/output/root-cause/regression-<feature>-<timestamp>.md`

Report includes:
- Executive summary with breaking commit
- Feature definition (what regressed)
- Git history timeline
- Breaking commit details with diff
- Code change analysis
- Related commits
- 3-level fix recommendations (revert, forward fix, comprehensive)
- Git commands ready to use
- Prevention strategy

### Step 6: Return Results
Display completion status with:
- Breaking commit hash and author
- When regression occurred
- What changed
- Fix options
- Report location

## Output Locations

- **Full Report**: `marketplace/output/root-cause/regression-<feature>-<timestamp>.md`
- **Summary Report**: `marketplace/output/root-cause/regression-<feature>-<timestamp>-summary.md`

## Expected Duration

**Simple Regression** (single breaking commit):
- Feature definition: 3 minutes
- Git history: 7 minutes
- Git blame: 5 minutes
- Breaking commit: 8 minutes
- Related changes: 4 minutes
- Fix recommendations: 5 minutes
- **Total**: ~32 minutes

**Complex Regression** (multiple interacting commits):
- Feature definition: 4 minutes
- Git history: 10 minutes
- Git blame: 7 minutes
- Breaking commit: 15 minutes (Sequential Thinking may enable)
- Related changes: 8 minutes
- Fix recommendations: 8 minutes
- **Total**: ~52 minutes

## Success Criteria

Command is successful when:
- [ ] Git repository verified
- [ ] Feature mapped to code components
- [ ] Git history collected for date range
- [ ] Commits categorized by relevance
- [ ] Git blame executed for error location
- [ ] Breaking commit identified with high confidence (>85%)
- [ ] Code changes pinpointed
- [ ] Related commits identified
- [ ] Multiple fix options provided (revert, forward, comprehensive)
- [ ] Git commands ready to use
- [ ] Report generated and saved

## Output Format

```
# ✓ Regression Analysis Complete

**Feature**: User profile page loading
**Execution Time**: 32 minutes

## Summary
- **Breaking Commit**: abc123f (2026-01-10 14:23:15)
- **Author**: John Doe <john.doe@example.com>
- **Root Cause**: Removed null-conditional operator during refactoring
- **Impact**: 15% of users cannot load profile page
- **Confidence**: 98%

## Breaking Commit Details
**Commit**: abc123f
**Date**: 2026-01-10 14:23:15
**Message**: "Refactor UserService to simplify DTO mapping"
**Files Changed**: UserService.cs (+15, -20), UserProfileDTO.cs (+3, -5)

**Critical Change** (UserService.cs:150):
```diff
- City = user.Address?.City ?? "Not Specified",
+ City = user.Address.City,
```

**Analysis**: Removed null-conditional operator, assuming Address always exists.

## Related Commits
1. ghi789b (5 days before) - Made Address optional in User entity
2. def456a (2 days before) - Added logging (unrelated)

## Fix Options
1. **Immediate Revert** (5 minutes) - Restore previous working state
2. **Forward Fix** (20 minutes) - Add null check without reverting
3. **Comprehensive Solution** (2 hours) - Fix + prevent recurrence

## Output Files
- **Full Analysis**: marketplace/output/root-cause/regression-userprofile-20260116-120145.md
- **Summary**: marketplace/output/root-cause/regression-userprofile-20260116-120145-summary.md

## Recommended Action
1. **Immediate**: Apply revert or forward fix (use git commands in report)
2. **Short-term**: Test fix thoroughly
3. **Long-term**: Implement prevention strategy (nullable reference types, tests)

## Next Steps
- Review full report for detailed git commands
- Choose fix option (revert recommended for quick production fix)
- Apply fix using provided git commands
- Deploy and monitor
- Implement prevention strategy
```

## FAQ

**Q: What if I'm not in a git repository?**
A: Command will fail. Regression analysis requires git history.

**Q: How far back does it search?**
A: Default: 30 days. Use --since to search further back (e.g., --since="3 months ago").

**Q: Can it analyze merge conflicts?**
A: Yes, it can identify regressions introduced during merge conflict resolution.

**Q: What if multiple commits contributed?**
A: Agent identifies all related commits and primary breaking commit. Report includes complete timeline.

**Q: How accurate is breaking commit identification?**
A: 95%+ for clear regressions. 85%+ for complex multi-commit regressions.

**Q: Will it suggest how to fix?**
A: Yes, provides 3 fix levels: immediate revert, forward fix, and comprehensive solution with git commands.

## Error Scenarios

### Not in Git Repository
```
❌ Git repository not found.

Cannot proceed without git history.
```

### No Commits in Date Range
```
⚠ No commits found in specified date range.

Search parameters:
- Date range: 2025-12-15 to 2026-01-15
- Files: UserService.cs

Suggestions:
- Expand date range (try --since="2 months ago")
- Check if feature exists in this branch
- Verify file paths are correct
```

### Feature Description Too Vague
```
⚠ Feature description is too vague to analyze accurately.

Provided: "something broke"

Need:
- What specific feature or functionality broke?
- What's the observable error or symptom?
- When did it last work?

Example: "User profile page loading - crashes with NullReferenceException - worked until ~2 weeks ago"
```

## Integration with Other Commands

### Complete Bug Investigation Workflow
```bash
# Step 1: Find when regression occurred
/find-regression "User profile page loading"

# Step 2: Find similar patterns in codebase
/analyze-bug-pattern "Missing null check on optional properties"

# Step 3: Fix all instances
# ... apply fixes from both reports ...

# Step 4: Review changes
/review-local-pr fix-branch
```

### Post-Deployment Issue Investigation
```bash
# Step 1: Analyze the error
/analyze-stacktrace

# Step 2: Find when it was introduced
/find-regression "Feature from stack trace analysis"

# Step 3: Correlate with other errors
/correlate-errors "Related errors from logs"

# Step 4: Apply comprehensive fix
# ... use findings from all reports ...
```

## Git Commands Provided in Report

The report includes ready-to-use git commands:

**Revert Command**:
```bash
git checkout main
git pull origin main
git checkout -b hotfix/revert-userservice-refactor
git revert abc123f
git push origin hotfix/revert-userservice-refactor
```

**Forward Fix Command**:
```bash
git checkout main
git pull origin main
git checkout -b fix/userservice-null-check
# ... make code changes ...
git add UserService.cs
git commit -m "Fix NullReferenceException in UserService.GetUserProfile"
git push origin fix/userservice-null-check
```

**Comprehensive Solution Command**:
```bash
# Full implementation with tests, static analysis, etc.
# Detailed steps provided in report
```

## Related Commands

- `/analyze-stacktrace` - Analyze error before finding regression
- `/analyze-bug-pattern` - Find similar patterns after identifying regression
- `/correlate-errors` - Correlate multiple errors possibly from same regression
- `/analyze-impact` - Assess impact of fix before applying

---

**Command Version**: 2.0.0
**Last Updated**: 2026-01-16
**Delegated To**: regression-analyzer agent
**Expected Duration**: 30-50 minutes
**MCP Requirements**: None (local git analysis only)
**Git Requirement**: Yes (must be in git repository)
