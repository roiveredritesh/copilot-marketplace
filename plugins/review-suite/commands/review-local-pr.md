# Command: /review-local-pr

Review local Git branch changes without GitHub access.

**Purpose**: Self-review code before creating pull requests or pushing to remote
**Status**: Production Ready
**Effort to Implement**: 3-4 hours
**Plugin**: Review Suite
**Agent**: Local PR Reviewer
**MCP Required**: None (local Git only)

---

## Usage

```bash
/review-local-pr <base-branch> [compare-branch] [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **base-branch**: The branch to compare against (e.g., `main`, `develop`)
  - Used as the starting point for comparison
  - Must exist locally
  - Typically the target branch for a PR

### Optional Arguments

- **compare-branch**: The branch to review (default: current branch)
  - Branch containing changes to review
  - If not specified: uses current branch
  - Must exist locally

- **--wait**: Execute synchronously (default)
  - Blocks until review completes
  - Good for: Quick reviews (< 15 minutes)
  - Shows real-time progress

- **--async**: Execute in background
  - Returns immediately with task ID
  - Good for: Large reviews (> 15 minutes)
  - Check progress with `/task-status <task-id>`

- **--report=full**: Comprehensive report (default)
  - All findings, recommendations, details
  - Detailed analysis of each issue
  - Best for: Critical reviews, deep analysis

- **--report=summary**: Quick summary only
  - Key findings and top recommendations
  - Condensed format
  - Best for: Quick validation, multiple reviews

## Examples

### Review Branch Before Merge
```bash
# Review feature branch against main
/review-local-pr main feature-auth --wait

# Output: Comprehensive review report
# Time: 5-10 minutes
# Location: marketplace/output/reviews/local-pr-{timestamp}.md
```

### Review Uncommitted Changes
```bash
# Review all uncommitted changes
/review-local-pr HEAD --wait

# Pre-commit quality gate
# Catches issues before committing
```

### Review Current Branch (Implicit)
```bash
# Review current branch against main
# (assumes you're currently on feature-branch)
/review-local-pr main --wait

# Uses current branch as compare-branch
```

### Review Specific Commits
```bash
# Review last 5 commits
/review-local-pr HEAD~5 HEAD --wait

# Useful for reviewing commit batch before push
```

### Async Review for Large Changes
```bash
# Review large feature branch
/review-local-pr main big-refactor --async

# Returns: task-20251030-001
# Check status: /task-status task-20251030-001 --watch
```

### Quick Summary
```bash
# Just want key findings
/review-local-pr main feature --wait --report=summary

# Faster output, less detail
```

### Compare Against Develop
```bash
# For projects using develop/main workflow
/review-local-pr develop feature-payment --wait

# Works with any branch naming scheme
```

### Review Against Different Remote
```bash
# Compare against remote branch (fetch first)
git fetch origin
/review-local-pr origin/main feature --wait

# After fetch, remote branches available
```

---

## Output Examples

### Example 1: Simple Feature Review

```bash
$ /review-local-pr main feature-user-auth --wait

🔄 Starting local PR review...
📊 Analyzing changes...
  ├─ Files changed: 5
  ├─ Lines added: 142
  ├─ Lines removed: 28
  ├─ Commits: 3
  └─ Complexity: Medium

✅ Review complete! (8 minutes)

Report saved to:
📄 marketplace/output/reviews/local-pr-20251030-143022.md

Summary:
  ⚠️  Security: 1 finding (High)
  ⚠️  Performance: 0 findings
  ⚠️  Architecture: 0 findings
  ⚠️  Code Quality: 2 findings (Medium)
  ✅ Testing: Good coverage
  ✅ Documentation: Updated

Recommendation: Fix security issue before committing
```

### Example 2: Uncommitted Changes Review

```bash
$ /review-local-pr HEAD --wait

🔄 Reviewing uncommitted changes...
📊 Analyzing working tree...
  ├─ Modified files: 3
  ├─ New files: 1
  ├─ Deleted files: 0
  └─ Complexity: Low

✅ Review complete! (4 minutes)

Report saved to:
📄 marketplace/output/reviews/local-pr-20251030-140251.md

Summary:
  ✅ Security: Clear
  ✅ Performance: No issues
  ✅ Architecture: Compliant
  ⚠️  Code Quality: 1 suggestion
  ✅ Testing: Should add tests
  ✅ Documentation: No changes needed

Recommendation: Ready to commit
```

### Example 3: Large Async Review

```bash
$ /review-local-pr main large-refactor --async

🚀 Starting async review...
Task ID: task-20251030-002

📊 Analysis will take approximately 15-20 minutes
   Run: /task-status task-20251030-002 --watch

Report will be saved to: marketplace/output/reviews/local-pr-{timestamp}.md

You can continue working. Review will complete in background.
```

---

## Report Format

### Full Report Structure

```markdown
# Local PR Review: feature-user-auth

## Executive Summary
- **Base Branch**: main
- **Compare Branch**: feature-user-auth
- **Files Changed**: 5
- **Lines Added**: 142 | **Lines Removed**: 28
- **Commits**: 3
- **Overall Risk**: MEDIUM
- **Review Time**: 8 minutes

## Key Findings
1. Hardcoded API key in authentication service (CRITICAL)
2. Missing null check in UserValidator (HIGH)
3. Inconsistent naming in new methods (LOW)

---

## Security Review

### Critical Issues
1. **Hardcoded API Key** (appsettings.cs:45)
   ```csharp
   private const string API_KEY = "sk-12345...";
   ```
   **Issue**: API key should never be hardcoded
   **Risk**: Secret exposed in source code
   **Recommendation**: Use environment variables or config
   **Fix**: Use: `Environment.GetEnvironmentVariable("API_KEY")`

### High Priority Issues
1. **SQL Injection Risk** (database.cs:102)
   ```csharp
   var query = $"SELECT * FROM Users WHERE Id = {userId}";
   ```
   **Issue**: Unparameterized query
   **Risk**: SQL injection attack vulnerability
   **Recommendation**: Use parameterized queries
   **Fix**: Use: `SqlCommand` with parameters

---

## Performance Review

### No Performance Issues Detected
✅ No N+1 query patterns found
✅ No blocking async calls
✅ No memory leak risks
✅ Async/await properly used
✅ No large object heap concerns

---

## Architecture Review

### Compliant
✅ Single Responsibility Principle followed
✅ Proper dependency injection
✅ Repository pattern correctly implemented
✅ Separation of concerns maintained

---

## Code Quality Review

### Medium Issues
1. **Inconsistent Method Naming** (validation.cs)
   - New methods use camelCase
   - Existing code uses PascalCase
   - Recommendation: Follow PascalCase convention for public methods

### Suggestions
1. Extract magic numbers to constants
2. Add XML documentation to new public methods
3. Reduce method complexity (UserValidator.Validate has complexity of 8)

---

## Impact Analysis

### Modified Public Methods
1. `UserService.CreateUser()` - NEW
2. `UserValidator.Validate()` - CHANGED
3. `AuthenticationService.Login()` - CHANGED

### Potential Impact Areas
- **UserRepository**: Called by UserService (affected by changes)
- **UserController**: Uses UserService (needs verification)
- **AuthenticationController**: Uses AuthenticationService (affected)

### Breaking Changes
⚠️ **WARNING**: `AuthenticationService.Login()` signature changed
- **Before**: `Login(username, password)`
- **After**: `Login(username, password, tenantId)` - NEW PARAMETER
- **Impact**: All callers must pass tenantId
- **Recommendation**: Check and update all callers
- **Files affected**: AuthenticationController.cs, LoginService.cs

---

## Testing Status

### Test Coverage
✅ New code has test files: UserServiceTests.cs exists
⚠️ Test coverage: 85% of new code covered
❌ Missing coverage: Edge cases for invalid tenantId

### Recommendations
1. Add test cases for tenantId validation
2. Add integration tests for authentication flow
3. Add edge case tests for CreateUser method

---

## Documentation Status

### Updates Found
✅ README.md updated with authentication info
✅ XML doc comments added to new public methods
⚠️ CHANGELOG.md not updated (consider adding)

### Recommendations
1. Document the new tenantId parameter
2. Add usage examples for new authentication flow
3. Update API documentation

---

## Recommendations Summary

### 🔴 CRITICAL - Must Fix Before Commit
1. Remove hardcoded API key from appsettings.cs
2. Fix SQL injection vulnerability in database.cs
3. Update all callers of changed Login() method signature

### 🟠 HIGH - Should Fix Before Push
1. Add missing null checks in UserValidator
2. Add test cases for missing coverage
3. Document breaking changes in CHANGELOG

### 🟡 MEDIUM - Consider for Future
1. Refactor UserValidator.Validate() (high complexity)
2. Extract magic numbers to constants
3. Add integration tests

### 🟢 LOW - Optional Improvements
1. Standardize method naming across codebase
2. Add more comprehensive error messages

---

## Related Commands

```bash
# Validate specific file after fixes
/validate-solution UserService.cs --wait

# Deeper impact analysis
/analyze-impact UserService.cs --wait

# Review PR before pushing
/review-pr owner/repo 42 --wait  (if PR exists)
```

---

**Review Completed**: 2025-10-30 14:30:22
**Review Type**: Local Branch Comparison
**Reviewed By**: Claude Code - Review Suite v1.1.0
**Agent**: Local PR Reviewer
```

### Summary Report Structure

For `--report=summary`:

```markdown
# Local PR Review Summary: feature-user-auth

## Overview
- **Files Changed**: 5
- **Overall Risk**: MEDIUM
- **Review Time**: 8 minutes

## Key Findings
1. 🔴 CRITICAL: Hardcoded API key (appsettings.cs:45)
2. 🟠 HIGH: SQL injection risk (database.cs:102)
3. 🟡 MEDIUM: Missing null checks (validation.cs)

## Recommendations
**Before Commit**: Fix critical issues (#1, #2)
**Before Push**: Add tests and documentation
**Optional**: Refactor complex methods

## Affected Areas
- UserService (new, high impact)
- UserValidator (modified)
- AuthenticationService (modified, signature changed)

**Full Report**: marketplace/output/reviews/local-pr-{timestamp}.md

---
```

---

## Workflow Examples

### Workflow 1: Pre-Commit Self-Review

```bash
# 1. You've finished coding, have uncommitted changes
$ git status
# (shows modified files)

# 2. Quick self-review
$ /review-local-pr HEAD --wait --report=summary

# 3. Review output
# (identifies 2 code quality issues)

# 4. Fix the issues
$ # (edit files to fix issues)

# 5. Commit with confidence
$ git add .
$ git commit -m "Add user authentication feature"

# 6. Push
$ git push origin feature-auth
```

### Workflow 2: Pre-Push Deep Review

```bash
# 1. You've finished feature and made commits
$ git log main..HEAD --oneline
# (shows 5 commits)

# 2. Deep review before pushing
$ /review-local-pr main --async

# 3. Continue working while review runs
$ # (check emails, work on other tasks)

# 4. Monitor progress
$ /task-status task-20251030-001 --watch
# (review completes in 12 minutes)

# 5. Review findings
$ cat marketplace/output/reviews/local-pr-*.md

# 6. Fix any issues found
$ # (fix issues if any)

# 7. Push with confidence
$ git push origin feature
```

### Workflow 3: Code Review Before Creating PR

```bash
# 1. Feature branch ready for PR
$ git checkout feature-payment

# 2. Local review
$ /review-local-pr develop feature-payment --wait

# 3. Review results
# (no critical issues, 1 suggestion)

# 4. Fix suggestion
$ # (minor refactoring)

# 5. Create PR
$ gh pr create --title "Add payment processing" --body "..."

# 6. Push to GitHub for team review
$ git push origin feature-payment
```

---

## Decision: When to Use Each Review Command

```
Need to review code?
│
├─ Is it a GitHub PR?
│  │
│  ├─ YES → Need deep impact analysis?
│  │  │
│  │  ├─ YES → /review-pr-local (15-25 min)
│  │  │         • Auto-fetches PR branch
│  │  │         • Deep local analysis
│  │  │         • Breaking change detection
│  │  │         • Test coverage check
│  │  │
│  │  └─ NO → /review-pr (5-10 min)
│  │           • Quick GitHub API review
│  │           • Fast feedback
│  │
│  └─ NO → Is it local branches?
│     │
│     └─ YES → /review-local-pr (5-10 min)
│               • Compare any branches
│               • Review uncommitted changes
│               • Pre-push quality gate
│               • No network needed
```

---

## Success Criteria

✅ Reviews local branches successfully
✅ Reviews uncommitted changes
✅ Reviews commit ranges
✅ Works entirely offline (no network)
✅ Applies all code review standards
✅ Detects security, performance, architecture issues
✅ Assesses code quality
✅ Analyzes impact of changes
✅ Generates comprehensive markdown report
✅ Supports --async for large reviews
✅ Handles edge cases gracefully
✅ Completes in 5-10 minutes for typical changes

---

**Version**: 1.1.0
**Status**: Production Ready
**Effort to Implement**: 3-4 hours
**Dependencies**: Git repository, local branches
**MCP Required**: None

This command enables pre-push code reviews without network access or GitHub integration.
