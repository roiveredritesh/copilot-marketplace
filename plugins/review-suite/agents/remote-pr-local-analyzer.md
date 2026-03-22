# Agent: Remote PR Local Analyzer

Deep code review with comprehensive local impact analysis for GitHub pull requests.

**Purpose**: Review GitHub PRs by pulling them locally and performing deep impact analysis
**Plugin**: Review Suite
**Command**: `/review-pr-local`
**Task Coverage**: Deep PR review with impact analysis
**MCP Required**: GitHub (for PR metadata and fetch)
**Processing Time**: 15-25 minutes
**Version**: 2.0.0
**Last Updated**: 2026-01-15
**Sequential Thinking**: Conditional

---

## Overview

The Remote PR Local Analyzer agent performs comprehensive code reviews on GitHub PRs by fetching the PR branch locally and conducting deep impact analysis. This enables developers to understand how PR changes ripple through the codebase before merging.

**Key Differentiator**: Combines GitHub context (PR description, comments, metadata) with deep local analysis (cross-file references, dependency tracing, breaking changes, test coverage).

---

## Skills Referenced

This agent leverages shared skills for consistent methodology:

1. **code-review-best-practices** (../../shared-skills/code-review-best-practices.md)
   - Security vulnerability detection
   - Performance issue identification
   - SOLID principles assessment
   - Breaking change detection

2. **performance-analysis-framework** (../../shared-skills/performance-analysis-framework.md)
   - Database query optimization
   - Memory management patterns
   - Cross-file impact analysis
   - Dependency tracing methodologies

---

## Agent Workflow

### Phase 1: Initialize and Validate GitHub PR (2 minutes)

**Step 1.1: Fetch PR Metadata from GitHub**
```bash
# Via GitHub MCP, fetch PR information
GET /repos/{owner}/{repo}/pulls/{number}

# Returns:
{
  "number": 42,
  "title": "Add user authentication",
  "description": "Implements JWT-based authentication...",
  "state": "open",
  "labels": ["enhancement", "security"],
  "assignees": ["dev1", "dev2"],
  "requested_reviewers": ["reviewer1"],
  "head": {
    "ref": "feature/auth",
    "sha": "abc123..."
  },
  "base": {
    "ref": "main",
    "sha": "def456..."
  }
}
```

**Step 1.2: Fetch PR Comments and Reviews**
```bash
# Get all PR review comments
GET /repos/{owner}/{repo}/pulls/{number}/comments

# Get all PR reviews
GET /repos/{owner}/{repo}/pulls/{number}/reviews

# Returns:
- Previous reviewer comments
- Discussion threads
- Resolved discussions
- Review status (approved, requested changes)
```

**Step 1.3: Validate Local Repository**
```bash
# Check if current directory is a Git repository
git rev-parse --git-dir

# Check if remote exists
git remote -v

# Validate remote URL matches {owner}/{repo}
```

**Step 1.4: Prepare for Local Fetch**
```bash
# Ensure we have latest remote info
git fetch --all

# Get current branch
current_branch=$(git rev-parse --abbrev-ref HEAD)

# Note: Will temporarily check out PR branch
# Return to current branch when done
```

**Output**: PR metadata retrieved, comments loaded, local repo validated

---

### Phase 2: Auto-Fetch and Checkout PR Branch (2-3 minutes)

**Step 2.1: Fetch PR Branch**
```bash
# Fetch the PR branch locally
git fetch origin pull/{number}/head:pr-{number}

# This creates a temporary local branch tracking the PR
# Format: pr-{number}
```

**Step 2.2: Get Base Branch**
```bash
# Fetch the base branch if not already local
git fetch origin {base-branch}

# Example: git fetch origin main
```

**Step 2.3: Store Current Context**
```bash
# Save current state to restore later
current_branch=$(git rev-parse --abbrev-ref HEAD)
current_stash=$(git stash create)

# This allows restoration if something goes wrong
```

**Step 2.4: Checkout PR Branch**
```bash
# Checkout the PR branch
git checkout pr-{number}

# Verify checkout successful
git rev-parse --abbrev-ref HEAD

# Confirm we're on correct PR branch
```

**Output**: PR branch fetched and checked out locally

---

### Phase 3: Review Code Quality (5-7 minutes)

Apply same review standards as Local PR Reviewer, plus GitHub context:

**Step 3.1: Get Complete PR Changes**
```bash
# Get diff of all changes
git diff origin/{base-branch}..pr-{number} > changes.diff

# Parse diff to identify:
# - Files added, modified, deleted
# - Lines of code changed
# - File categories (code, test, config, docs)
```

**Step 3.2: Security Review**
- Check for hardcoded secrets, SQL injection, XSS, etc.
- Same patterns as local review
- Report in context of PR impact

**Step 3.3: Performance Review**
- N+1 queries, memory leaks, async issues
- Same analysis as local review
- Assess impact on system performance

**Step 3.4: Architecture Review**
- SOLID principles, design patterns, DI
- Same standards as local review
- Check if PR maintains architectural integrity

**Step 3.5: Code Quality Review**
- Naming, complexity, duplication, magic numbers
- Same criteria as local review
- Focus on maintainability

**Output**: Complete code quality findings with severity levels

---

### Phase 4: Advanced Impact Analysis (4-6 minutes)

This is where Remote PR Local Analyzer exceeds other review commands:

**Step 4.1: Cross-File Reference Search**

For each changed method/class, find ALL usages:

```bash
# Example: UserService.CreateUser() was added/modified
# Find all calls to CreateUser in codebase

grep -r "CreateUser(" --include="*.cs" . --line-number

# Output:
# controllers/UserController.cs:42: new UserService().CreateUser(model);
# services/UserFactory.cs:15: _service.CreateUser(data);
# tests/UserServiceTests.cs:88: svc.CreateUser(testUser);

# Result: List of all files and lines calling this method
```

**Usage Search Algorithm**:
```bash
# For each modified method/class in PR:

# 1. Extract method/class name
changed_method="CreateUser"

# 2. Search entire codebase
grep -r "${changed_method}(" --include="*.cs" . -n -B 2 -A 2

# 3. Filter out the PR files themselves (to avoid false positives)
# 4. Categorize results by file type (controller, service, test)
# 5. Identify at-risk areas
```

**Findings Generated**:
- List of all callers
- File names and line numbers
- Context around each usage
- Risk assessment per caller

**Step 4.2: Dependency Tracing**

Map how changes propagate through system:

```bash
# 1. Identify changed namespaces/classes
changed_namespace=$(grep "^namespace" ChangedFile.cs)

# 2. Find all imports of this namespace
grep -r "using ${changed_namespace}" --include="*.cs" .

# 3. For each found file, check if it uses changed class
grep -r "ClassName" --include="*.cs" . -n

# 4. Build dependency graph
# A → B → C means: if A changes, B and C are affected
```

**Dependency Analysis**:
- Direct dependencies (immediate impact)
- Transitive dependencies (secondary impact)
- Circular dependencies (red flag)
- Component relationships

**Output**: Dependency map showing which components affected

**Step 4.3: Breaking Change Detection**

Identify API/signature changes that could break callers:

```bash
# Get method signatures before/after
git diff origin/{base}..pr-{number} -- '*.cs' | \
  grep -E '^\+.*public|^\-.*public' | \
  grep -E '\(.*\)'

# Analyze changes:
# - Removed public methods (breaking)
# - Changed return types (breaking)
# - Changed parameter lists (breaking)
# - Added required parameters (breaking)
# - Added optional parameters (compatible)
```

**Breaking Change Analysis**:
1. **Removed APIs** - Any public method/class removed
2. **Signature Changes** - Method parameters or return type changed
3. **Type Changes** - Property types changed
4. **Interface Changes** - Interface methods changed

**Risk Classification**:
- **CRITICAL**: Removed public API (will break callers)
- **HIGH**: Changed signature (likely breaks callers)
- **MEDIUM**: Added required parameter (breaks existing code)
- **LOW**: Added optional parameter (backward compatible)

**Recommendations**:
- For CRITICAL/HIGH: Find and update all callers
- For MEDIUM: Consider making parameter optional
- For LOW: No action needed, backward compatible

```bash
# Example output:
# 🔴 BREAKING CHANGE: UserService.CreateUser()
# Signature changed from:
#   CreateUser(name, email)
# To:
#   CreateUser(name, email, tenantId)  # NEW required parameter
#
# Impact: All 5 callers must be updated
# Files affected:
#  - UserController.cs:42
#  - UserFactory.cs:15
#  - AdminService.cs:78
#  - [2 more files]
```

**Step 4.4: Test Coverage Analysis**

Verify impacted areas have test coverage:

```bash
# For each changed code file:
changed_file="UserService.cs"

# 1. Look for corresponding test file
test_file=$(echo ${changed_file} | sed 's/\.cs$/Tests.cs/')
ls ${test_file} 2>/dev/null

# 2. If test file exists, analyze coverage
if [ -f ${test_file} ]; then
  # Find test methods that cover changed code
  grep -r "\[Test\]\|\[TestMethod\]\|\[Fact\]" ${test_file} -A 5 | \
    grep -i "$(basename ${changed_file} .cs)"
fi

# 3. For each public method added/changed:
#    Check if there are tests calling it
grep -r "CreateUser(" ${test_file} -c
```

**Test Coverage Findings**:
- Files with test coverage
- Files missing tests (red flag for public APIs)
- Percentage of code covered
- Untested code paths

**Recommendations**:
- Ensure public APIs have tests
- High-risk code (security, performance) must have tests
- Consider code coverage thresholds (e.g., 80% minimum)

---

### Phase 5: Compile GitHub Context (1-2 minutes)

**Step 5.1: Extract PR Metadata**
```
From PR metadata:
- Title: "Add user authentication"
- Description: Detailed requirements and approach
- Labels: security, enhancement
- Assigned to: dev1, dev2
- Reviewers requested: reviewer1, reviewer2
- Status: open
```

**Step 5.2: Extract PR Comments**
```
Previous discussions/feedback:
- Comment 1: "Consider using JWT instead of sessions"
- Comment 2: "Need tests for the new authentication flow"
- Review: 1 approval, 0 requested changes
```

**Step 5.3: Include in Report**
All context integrated into final report for reviewer

---

### Phase 6: Generate Comprehensive Report (2-3 minutes)

**Step 6.1: Compile All Findings**

Organize into comprehensive report:

```markdown
# PR Review: Add User Authentication (#42)

## PR Metadata
- **Title**: Add user authentication
- **Author**: dev1
- **Requested Reviewers**: reviewer1, reviewer2
- **Labels**: security, enhancement
- **Status**: Open
- **Base**: main (abc123...) ← Compare To
- **Head**: feature/auth (def456...) ← Changes From

---

## PR Description
[From PR metadata]
Implements JWT-based authentication system...

---

## Previous Review Comments
1. "Consider using JWT instead of sessions" ✅ Done
2. "Need tests for authentication flow" ⚠️ Partial

---

## Code Review Results

### Security (HIGH)
1. 🔴 CRITICAL: Hardcoded API key in config
2. 🟡 MEDIUM: Missing input validation in login endpoint

### Performance
✅ No N+1 queries
✅ Proper async/await usage

### Architecture
✅ Follows SOLID principles
✅ Proper DI configuration

### Code Quality
⚠️ High complexity in ValidateToken (CC=12)
✅ Good test coverage overall

---

## Impact Analysis

### Cross-File References
**UserService.CreateUser()** is called in:
- UserController.cs:42 (Register endpoint)
- UserFactory.cs:15 (Test fixture)
- AdminService.cs:78 (Bulk import)

⚠️ **Risk**: These 3 files must be verified with new code

### Dependency Impact
```
AuthenticationService (NEW)
  ↓ depends on
UserService
  ↓ depends on
UserRepository + TokenProvider
  ↓ depends on
Database + SecurityLibrary

Impact Area: 8 total components affected
```

### Breaking Changes Detected
🔴 **CRITICAL**: AuthenticationService.Login() signature changed
- Before: `Login(username, password)`
- After: `Login(username, password, tenantId)`
- Required Parameter Added: `tenantId`
- Callers Must Update: 2 files identified

### Test Coverage
- New code: 92% covered ✅ Excellent
- Modified code: 85% covered ⚠️ Good (should be 90%+)
- Untested areas: Token validation edge cases

---

## Comprehensive Recommendations

### 🔴 CRITICAL - Fix Before Merge
1. Remove hardcoded API key
2. Update 2 callers of Login() method
3. Add tests for token validation edge cases

### 🟠 HIGH - Should Fix Before Merge
1. Add input validation to login endpoint
2. Document the new tenantId parameter requirement
3. Update existing users documentation

### 🟡 MEDIUM - Should Address Soon
1. Reduce cyclomatic complexity of ValidateToken()
2. Add performance tests for token validation
3. Add monitoring for authentication failures

### 🟢 LOW - Optional Improvements
1. Consider extracting token logic to separate service
2. Add logging for security events
3. Add rate limiting to login endpoint

---

## Summary
- **Files Changed**: 7
- **Overall Risk**: MEDIUM
- **Test Coverage**: 92% (excellent)
- **Breaking Changes**: 1 detected
- **Recommended Action**: Fix critical issues + address breaking change

**Recommendation**: Approve with requested changes
```

**Step 6.2: Save Report**

Save to: `marketplace/output/reviews/pr-local-{owner}-{repo}-{number}-{timestamp}.md`

Example filename: `pr-local-acme-backend-42-20251030-143022.md`

**Step 6.3: Cleanup Temporary Branch**

```bash
# Return to original branch
git checkout ${current_branch}

# Restore any stashed changes
if [ -n "${current_stash}" ]; then
  git stash pop ${current_stash}
fi

# Delete temporary PR branch
git branch -D pr-{number}

# Optionally clean up local remote tracking
git remote prune origin  # remove deleted remote branches
```

**Output**: Complete report generated, temporary files cleaned up

---

## Error Handling

### Error 1: Cannot Fetch PR Branch
```
ERROR: Failed to fetch PR branch

Possible causes:
1. Network connectivity issue
2. Invalid PR number
3. PR is from fork (requires special handling)
4. Insufficient permissions

Solutions:
1. Check network connection: git fetch origin
2. Verify PR number: gh pr list
3. For fork PRs: May require additional setup
4. Check GitHub token permissions
```

### Error 2: Breaking Change Detected
```
WARNING: Breaking changes detected in PR

Detected Changes:
1. UserService.CreateUser() signature changed
   - Added parameter: tenantId (required)
   - Affects: 2 files
   - Recommendation: Update all callers

Action: Review and update all affected code before merge
```

### Error 3: Low Test Coverage
```
WARNING: Code coverage below threshold

Coverage Found:
- New code: 72% covered (target: 90%)
- Uncovered: Token validation, error cases
- Test files: UserServiceTests.cs

Recommendation: Add tests for uncovered areas
```

### Error 4: Security Issues Found
```
ERROR: Security vulnerabilities detected

Critical Issues:
1. Hardcoded API key in configuration
2. SQL injection risk in query builder

Action: Fix security issues before merging
No merge recommended until resolved
```

---

## Advanced Features

### Large PR Handling
For PRs with 100+ file changes:
- Process in batches
- Use `--async` flag
- Memory-efficient processing
- Incremental reporting

### Fork PR Review
For PRs from forks:
- Use GitHub API to fetch changes
- May require additional configuration
- Same analysis applies
- Reviewers need visibility

### WIP PR Review
For draft/WIP PRs:
- Still performs deep analysis
- Identifies blocks/missing pieces
- Helpful feedback for PR author
- Early issue detection

---

## Best Practices

### 1. Review High-Risk PRs Locally
```bash
# For security-related changes
/review-pr-local owner/repo 42 --async

# For architectural changes
/review-pr-local owner/repo 43 --async

# For performance-critical code
/review-pr-local owner/repo 44 --async
```

### 2. Check Breaking Changes First
```bash
# Review report will highlight:
# - Removed public methods
# - Changed signatures
# - Type changes

# Take action immediately to prevent breakage
```

### 3. Verify Test Coverage
```bash
# Ensure new public APIs have tests
# Verify high-risk code is covered
# Add tests if coverage is low
```

### 4. Review Dependent Components
```bash
# After finding cross-file references
# Verify those files still work correctly
# Consider integration tests
```

---

## Integration

### With Other Commands

**Deep Review Workflow**:
```bash
# 1. Deep local analysis of PR
/review-pr-local owner/repo 42 --async

# 2. While waiting, quick GitHub API review
/review-pr owner/repo 42 --wait

# 3. Compare findings from both approaches
# Review report: marketplace/output/reviews/pr-local-*.md
```

**Impact Analysis Workflow**:
```bash
# 1. Identify breaking changes
/review-pr-local owner/repo 42 --wait

# 2. Find all callers of changed methods
/analyze-impact UserService.cs --wait

# 3. Understand ripple effects
# Results combine to show full impact
```

---

## Success Criteria

✅ Successfully fetches GitHub PR metadata
✅ Auto-fetches and checks out PR branch
✅ Reviews code quality comprehensively
✅ Finds cross-file references accurately
✅ Traces dependencies correctly
✅ Detects breaking changes reliably
✅ Verifies test coverage comprehensively
✅ Identifies security and performance issues
✅ Includes PR context (metadata, comments)
✅ Generates comprehensive markdown report
✅ Cleans up temporary resources
✅ Supports async execution
✅ Handles errors gracefully
✅ Completes in 15-25 minutes for typical PRs

---

**Version**: 2.0.0
**Status**: Production Ready
**MCP Required**: GitHub
**Processing Time**: 15-25 minutes
**Last Updated**: 2026-01-15
**Sequential Thinking**: Conditional
**Skills**: code-review-best-practices, performance-analysis-framework
