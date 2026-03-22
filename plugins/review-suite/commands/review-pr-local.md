# Command: /review-pr-local

Deep code review with comprehensive local impact analysis for GitHub pull requests.

**Purpose**: Review GitHub PRs by fetching locally and analyzing cross-file impact
**Status**: Production Ready
**Effort to Implement**: 4-5 hours
**Plugin**: Review Suite
**Agent**: Remote PR Local Analyzer
**MCP Required**: GitHub (for PR metadata and fetch)

---

## Usage

```bash
/review-pr-local <owner/repo> <pr-number> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **owner/repo**: GitHub repository in format `owner/repo`
  - Example: `microsoft/vscode`
  - Example: `acme-corp/backend-api`

- **pr-number**: Pull request number to review
  - Example: `42`
  - Must be an open or closed PR
  - Accessible to authenticated user

### Optional Arguments

- **--wait**: Execute synchronously (default)
  - Blocks until review completes
  - Good for: Critical reviews where you need immediate results
  - Processing time: 15-25 minutes

- **--async**: Execute in background
  - Returns immediately with task ID
  - Good for: Large PRs, multiple concurrent reviews
  - Check status: `/task-status <task-id>`

- **--report=full**: Comprehensive report (default)
  - Complete analysis with all details
  - Impact analysis, breaking changes, etc.
  - Best for: Critical reviews, merging to main

- **--report=summary**: Quick summary only
  - Key findings and top recommendations
  - Condensed format
  - Best for: Quick feedback, WIP reviews

## Examples

### Review Critical PR Before Merge
```bash
# Deep review of authentication feature PR
/review-pr-local acme-corp/backend 42 --wait

# Output: Comprehensive report with:
# - Code quality findings
# - Security issues
# - Performance concerns
# - Cross-file references
# - Breaking changes detected
# - Test coverage status
# - Detailed recommendations

# Time: 15-25 minutes
# Location: marketplace/output/reviews/pr-local-{timestamp}.md
```

### Review Large PR Asynchronously
```bash
# Large refactoring PR with 50+ files
/review-pr-local acme-corp/backend 43 --async

# Returns: task-20251030-001
# Output:
# 🚀 Review started in background
# Task ID: task-20251030-001
# Estimated time: 20-25 minutes
#
# Check status: /task-status task-20251030-001 --watch
# Report will be saved to: marketplace/output/reviews/pr-local-*.md
```

### Quick Review Summary
```bash
# Just want key findings
/review-pr-local microsoft/vscode 1234 --wait --report=summary

# Output: Quick summary of critical issues
# Time: 10-15 minutes (summary is faster)
# Location: marketplace/output/reviews/pr-local-{timestamp}.md
```

### Review From Different Organization
```bash
# Review PR from any public repo you have access to
/review-pr-local open-source-org/project 99 --wait

# Works with any GitHub repository
```

### Review Fork PR
```bash
# Review PR from a fork
/review-pr-local contributor/fork 5 --wait

# May require GitHub API access to fork
# Same deep analysis applies
```

---

## Output Examples

### Example 1: Security-Critical PR Review

```bash
$ /review-pr-local acme-corp/backend 42 --wait

🔄 Starting deep local PR review...

📝 Fetching PR metadata...
✅ PR #42: "Add user authentication"
   Author: dev1 | Base: main | Head: feature/auth

🔗 Fetching PR branch locally...
  ├─ Fetching: origin/pull/42/head:pr-42
  ├─ Base branch: origin/main
  └─ Checkout: pr-42 ✅

📊 Analyzing changes...
  ├─ Files changed: 7
  ├─ Lines added: 287
  ├─ Lines removed: 45
  ├─ Commits: 4
  └─ Complexity: Medium-High

🔍 Running code quality review...
  ├─ Security scan: 2 findings
  ├─ Performance scan: 0 findings
  ├─ Architecture scan: 0 findings
  └─ Code quality scan: 3 findings

🌐 Analyzing cross-file impact...
  ├─ New methods: 5
  ├─ Modified methods: 3
  ├─ Cross-file references: 8 found
  ├─ Dependencies identified: 4 components
  └─ Breaking changes: 1 detected ⚠️

🧪 Checking test coverage...
  ├─ New code coverage: 92%
  ├─ Modified code coverage: 85%
  └─ Untested areas: Token validation

🔄 Cleaning up temporary files...

✅ Deep review complete! (21 minutes)

📄 Comprehensive report saved:
   marketplace/output/reviews/pr-local-42-20251030-143022.md

⚠️  ISSUES FOUND:
   🔴 CRITICAL: Hardcoded API key (1 issue)
   🟠 HIGH: Breaking API change (1 issue)
   🟡 MEDIUM: Missing validation (2 issues)
   🟢 LOW: Code quality suggestions (3 issues)

📋 Summary:
   ✅ Code quality: Good (92% new code coverage)
   ⚠️  Impact: Medium (4 components affected)
   🚨 Risk: Medium (1 breaking change detected)

🎯 Recommendation: Approve with requested changes
   1. Fix hardcoded API key (CRITICAL)
   2. Document breaking change requirement
   3. Add validation to login endpoint
```

### Example 2: Large Async Review

```bash
$ /review-pr-local acme-corp/backend 44 --async

🚀 Starting async deep review...

Task ID: task-20251030-002

📝 Fetching PR #44: "Large refactoring"
   Files: 62 | Lines changed: 1,247

⏱️  Estimated time: 20-25 minutes
   Running in background...

📊 Progress tracking at:
   /task-status task-20251030-002 --watch

📄 Report will be saved to:
   marketplace/output/reviews/pr-local-*.md

You can continue working. Review will complete in background.
```

### Example 3: Summary Report

```bash
$ /review-pr-local acme-corp/backend 42 --wait --report=summary

🔄 Quick review (summary mode)...

✅ Complete! (12 minutes)

📋 SUMMARY REPORT

Files Changed: 7
Overall Risk: MEDIUM

🔴 CRITICAL (Must Fix)
   1. Hardcoded API key in appsettings.cs:45

🟠 HIGH (Should Fix)
   1. Breaking change: Login() signature changed
   2. Missing input validation: email parameter

🟡 MEDIUM (Consider)
   1. High complexity: ValidateToken() (CC=12)
   2. Code duplication: Hash algorithm appears 3 times

Recommendation: Request changes before merge

Full Report: marketplace/output/reviews/pr-local-42-20251030.md
```

---

## Full Report Structure

### Report Header
```markdown
# PR Deep Review: Add User Authentication (#42)

## GitHub PR Information
- **Repository**: acme-corp/backend
- **PR Number**: 42
- **Title**: Add user authentication
- **Author**: dev1
- **Status**: Open
- **Reviewers**: reviewer1, reviewer2
- **Labels**: security, enhancement

## Branch Information
- **Base Branch**: main (commit: abc123...)
- **Head Branch**: feature/auth (commit: def456...)
- **Files Changed**: 7
- **Lines Added**: 287 | **Lines Removed**: 45
- **Commits**: 4
- **Overall Risk Level**: MEDIUM
```

### Code Quality Section
```markdown
## Code Quality Review

### Security Review
#### 🔴 CRITICAL Issues (1)
1. **Hardcoded API Key** (appsettings.cs:45)
   ```csharp
   private const string API_KEY = "sk-12345-abcde";
   ```
   - **Issue**: Secret exposed in source code
   - **Risk**: Can be accessed by anyone with repo access
   - **Fix**: Use environment variables
   - **Implementation**:
     ```csharp
     private string ApiKey = Environment.GetEnvironmentVariable("API_KEY");
     ```

#### 🟠 HIGH Issues (1)
1. **SQL Injection Risk** (database.cs:102)
   - Unparameterized query detected
   - Fix: Use SqlCommand with parameters

#### 🟡 MEDIUM Issues (1)
1. **Missing Input Validation** (login.cs:45)
   - Email not validated for format
   - Could accept invalid emails
   - Add: `if (!IsValidEmail(email)) throw new ArgumentException()`

### Performance Review
✅ **No Performance Issues Detected**
- No N+1 query patterns
- Proper async/await usage
- No memory leak risks
- Efficient LINQ queries

### Architecture Review
✅ **Compliant with Architecture**
- SOLID principles followed
- Proper dependency injection
- Separation of concerns maintained

### Code Quality
⚠️ **Issues Found** (2)
1. **High Complexity**: ValidateToken() has cyclomatic complexity of 12
   - Recommendation: Break into smaller methods
2. **Code Duplication**: Hash algorithm appears in 3 files
   - Recommendation: Extract to utility class
```

### Impact Analysis Section
```markdown
## Impact Analysis

### Cross-File References
**New Method**: UserService.CreateUser()
- Called in: 3 locations found
  1. UserController.cs:42 (Register endpoint)
  2. UserFactory.cs:15 (Test fixture)
  3. AdminService.cs:78 (Bulk import)
- **Risk Level**: Medium (3 callers affected)

**Modified Method**: AuthenticationService.Login()
- Called in: 5 locations found
  1. AuthenticationController.cs:52 (Login action)
  2. ApiTokenService.cs:18 (Token generation)
  3. SessionManager.cs:33 (Session creation)
  4. [2 more files]
- **Risk Level**: High (signature changed, 5 callers affected)

### Dependency Tracing
```
AuthenticationService (MODIFIED)
  ├── UserService (MODIFIED)
  │   └── UserRepository (unchanged)
  ├── TokenProvider (NEW)
  └── PasswordHasher (NEW)

Affected Components: 6 total
Impact Radius: Medium
```

### Breaking Changes Detected
🔴 **CRITICAL**: AuthenticationService.Login() signature changed
- **Before**: `Login(username, password)`
- **After**: `Login(username, password, tenantId)` ← NEW REQUIRED PARAMETER
- **Severity**: CRITICAL (breaks all existing callers)
- **Impact**: 5 files must be updated
- **Callers Found**:
  1. AuthenticationController.cs:52 ⚠️ MUST UPDATE
  2. ApiTokenService.cs:18 ⚠️ MUST UPDATE
  3. SessionManager.cs:33 ⚠️ MUST UPDATE
  4. [2 more files] ⚠️ MUST UPDATE
- **Recommendation**:
  1. Update all 5 callers before merge
  2. Or make tenantId optional with default value
  3. Add unit tests for new signature

### Test Coverage Analysis
✅ **Good Coverage Overall**
- **New Code**: 92% covered (excellent)
- **Modified Code**: 85% covered (good, target: 90%+)
- **Untested Areas**:
  1. Token validation edge cases (missing)
  2. Error handling paths (partial)
- **Recommendations**:
  1. Add tests for edge cases in ValidateToken()
  2. Add integration tests for authentication flow

**Test Files Analyzed**:
- UserServiceTests.cs ✅ Found
- AuthenticationServiceTests.cs ✅ Found
- TokenProviderTests.cs ✅ Found
```

### Previous PR Comments Section
```markdown
## Previous Review Comments

### Addressed Comments
✅ "Consider using JWT instead of sessions"
   → JWT implementation found in AuthenticationService

⚠️  "Need tests for authentication flow"
   → Tests added but coverage is 85% (target: 90%+)

### Outstanding Comments
❓ "What about refresh tokens?"
   → Not addressed in this PR (out of scope?)

### New Findings
🔴 Hardcoded API key needs attention
🟠 Breaking change requires caller updates
```

### Comprehensive Recommendations
```markdown
## Recommendations

### 🔴 CRITICAL - Fix Before Merge (Blocking)
1. **Remove Hardcoded API Key**
   - File: appsettings.cs:45
   - Use: Environment.GetEnvironmentVariable("API_KEY")
   - Time to fix: 5 minutes

2. **Update All 5 Callers of Login()**
   - Files: AuthenticationController.cs, ApiTokenService.cs, [3 more]
   - Action: Add `tenantId` parameter to all calls
   - Time to fix: 20 minutes

3. **Add Input Validation**
   - File: login.cs:45
   - Validate email format
   - Time to fix: 10 minutes

### 🟠 HIGH - Should Fix Before Merge (Recommended)
1. **Refactor ValidateToken()** (complexity 12 → target: 8)
   - Break into smaller methods
   - Time: 30 minutes

2. **Document Breaking Change**
   - Update CHANGELOG.md with migration guide
   - Notify consuming services
   - Time: 15 minutes

### 🟡 MEDIUM - Should Address Soon
1. **Extract Duplicate Hash Algorithm** to utility
2. **Add Performance Tests** for token validation
3. **Add Rate Limiting** to login endpoint

### 🟢 LOW - Optional Improvements
1. Add comprehensive error messages
2. Add logging for security events
3. Consider metrics/monitoring integration
```

### Summary and Recommendation
```markdown
## Summary

| Metric | Value |
|--------|-------|
| **Files Changed** | 7 |
| **Lines Added** | 287 |
| **Lines Removed** | 45 |
| **Code Coverage (New)** | 92% ✅ |
| **Code Coverage (Modified)** | 85% ⚠️ |
| **Security Issues** | 2 (1 critical) |
| **Performance Issues** | 0 |
| **Architecture Issues** | 0 |
| **Code Quality Issues** | 2 |
| **Breaking Changes** | 1 (critical) |
| **Cross-File Impact** | 8 references, 6 components affected |
| **Overall Risk** | MEDIUM |

## Final Recommendation
🟠 **REQUEST CHANGES** (do not merge yet)

**Reasons**:
1. Critical security issue (hardcoded API key)
2. Breaking API change requires caller updates
3. Test coverage below target for modified code

**Action Items Before Merge**:
1. ✅ Fix hardcoded API key (CRITICAL)
2. ✅ Update 5 callers of Login() (CRITICAL)
3. ✅ Add missing validation (HIGH)
4. ⭐ Add tests for new coverage (MEDIUM)

**Estimated Time to Fix**: 60-90 minutes

**Review Status**:
- 🟢 Code quality is good
- 🟢 Architecture is sound
- 🟡 Impact is medium (manageable)
- 🔴 Critical issues must be fixed
```

---

## Comparison: Three Review Commands

```
Question: How should I review this PR?

├─ Quick feedback needed?
│  └─ /review-pr owner/repo 42 (5-10 min, GitHub API only)
│
├─ Deep analysis before merge?
│  └─ /review-pr-local owner/repo 42 (15-25 min, comprehensive)
│
└─ Local code only (no GitHub)?
   └─ /review-local-pr main feature-branch (5-10 min, local Git)
```

---

## Decision Tree

When to use each review command:

```
Need to review code?
│
├─ GitHub PR?
│  │
│  ├─ Just need quick feedback?
│  │  └─ /review-pr (GitHub API, 5-10 min)
│  │
│  └─ Need deep impact analysis?
│     ├─ Is it critical/risky?
│     │  └─ /review-pr-local (full analysis, 15-25 min) ← This command
│     │
│     └─ Is it routine?
│        └─ /review-pr (quick feedback, 5-10 min)
│
└─ Local branches only?
   └─ /review-local-pr (offline, 5-10 min)
```

---

## Workflows

### Workflow 1: Pre-Merge Review

```bash
# 1. PR #42 is ready to merge
# 2. Run deep local analysis
$ /review-pr-local acme-corp/backend 42 --wait

# 3. Review comprehensive report
# (21 minutes later)

# 4. Found critical issues
# (hardcoded API key, breaking changes)

# 5. Request changes in GitHub
$ gh pr comment 42 --body "Requested changes: Fix API key, update callers"

# 6. Author fixes issues
# (commits to same PR)

# 7. Re-run review to verify fixes
$ /review-pr-local acme-corp/backend 42 --wait

# 8. Verify all issues resolved
# 9. Approve and merge
```

### Workflow 2: Critical Security PR

```bash
# 1. Security-related PR #43 created
$ /review-pr-local acme-corp/backend 43 --wait

# 2. Deep analysis shows:
# - No vulnerabilities ✅
# - Good test coverage ✅
# - No breaking changes ✅

# 3. All checks pass
# 4. Approve immediately
$ gh pr review 43 --approve

# 5. Merge to main
$ gh pr merge 43
```

### Workflow 3: Large Refactoring PR

```bash
# 1. Large refactoring PR #44 (62 files)
# 2. Use async for speed
$ /review-pr-local acme-corp/backend 44 --async

# Returns: task-20251030-001

# 3. Continue with other work
$ # work on something else

# 4. Monitor progress
$ /task-status task-20251030-001 --watch

# 5. Review completes (23 minutes)
$ cat marketplace/output/reviews/pr-local-*.md

# 6. Provide feedback
```

---

## Success Criteria

✅ Fetches PR metadata from GitHub successfully
✅ Auto-fetches and checks out PR branch
✅ Performs comprehensive code quality review
✅ Finds all cross-file references accurately
✅ Traces dependencies and impact correctly
✅ Detects breaking changes reliably
✅ Verifies test coverage comprehensively
✅ Includes previous PR comments/context
✅ Generates detailed markdown report
✅ Cleans up temporary resources properly
✅ Supports async execution for large PRs
✅ Handles edge cases gracefully
✅ Provides actionable recommendations
✅ Completes in 15-25 minutes for typical PRs

---

## Performance Notes

### Small PRs (< 10 files)
- Processing time: 10-15 minutes
- Memory: < 200 MB
- Recommended: `--wait`

### Medium PRs (10-50 files)
- Processing time: 15-20 minutes
- Memory: 200-500 MB
- Either: `--wait` or `--async`

### Large PRs (> 50 files)
- Processing time: 20-30 minutes
- Memory: 500 MB - 1 GB
- Recommended: `--async`

---

**Version**: 1.1.0
**Status**: Production Ready
**Effort to Implement**: 4-5 hours
**MCP Required**: GitHub
**Processing Time**: 15-25 minutes

This command enables comprehensive PR reviews with deep impact analysis before merging to production.
