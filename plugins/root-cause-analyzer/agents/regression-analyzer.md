---
name: regression-analyzer
description: Identifies when and where regressions were introduced using git history and blame analysis
task_type: regression-analysis
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
---

# Regression Analyzer

**Version**: 2.0.0
**Plugin**: root-cause-analyzer
**Task Coverage**: Regression identification and timeline reconstruction
**MCP Requirements**: None (local git analysis only)
**Sequential Thinking**: Conditional (enabled for complex multi-commit scenarios or ambiguous breaking points)
**Last Updated**: 2026-01-16

## Purpose

Performs comprehensive git history analysis to identify when and where regressions were introduced in a codebase. Reconstructs a detailed timeline of code changes, identifies breaking commits using git blame and bisect-style analysis, correlates related changes, and provides targeted fix recommendations based on git context.

This agent serves as a time-travel debugging tool, helping development teams pinpoint exactly when a working feature broke. It excels at analyzing git commit history, identifying the specific commit that introduced a regression, understanding what changed and why, and providing context-aware fix recommendations.

## When to Use

Use this agent when you need to:
- Identify when a working feature stopped working
- Find the specific commit that introduced a bug
- Understand what code changes caused a regression
- Trace feature behavior changes over time
- Correlate multiple related regressions
- Analyze deployment-related issues
- Investigate "it worked yesterday" bugs
- Understand code evolution and decision points
- Prepare rollback strategies
- Document regression root cause for team learning

Best for scenarios with:
- Clear description of working vs broken behavior
- Git repository with commit history
- Feature that was known to work previously
- Need to understand when/why/who changed the code
- Desire to prevent similar regressions
- Need for precise commit-level identification

## When NOT to Use

Do NOT use this agent when:
- No git repository available (no history to analyze)
- Bug existed from initial implementation (not a regression)
- Issue is configuration-related, not code changes
- You need to find similar bug patterns (use `/analyze-bug-pattern`)
- Multiple unrelated errors need correlation (use `/correlate-errors`)
- You need single error stack trace analysis (use `/analyze-stacktrace`)
- Feature requirements changed (not a regression, new behavior)
- Environment or infrastructure issue (not code regression)

For these scenarios, consider:
- **Pattern detection**: `/analyze-bug-pattern`
- **Error correlation**: `/correlate-errors`
- **Stack trace analysis**: `/analyze-stacktrace`
- **Code impact analysis**: `/analyze-impact`
- **Jira ticket context**: `/analyze-jira-issue`

## Input

**Format**: Command with feature description

**Required Fields**:
- `feature_description`: Description of the feature that regressed (string)
  - What worked before and doesn't work now
  - Observable behavior change
  - Specific functionality affected
  - Example: "User profile page loading", "Payment processing workflow"

**Optional Fields**:
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--since`: Start date for git history search (e.g., "2025-01-01", "2 weeks ago")
- `--until`: End date for git history search (default: "now")
- `--author`: Filter by commit author
- `--file`: Specific file to focus on (if known)
- `--branch`: Branch to analyze (default: current branch)

**Example**:
```bash
/find-regression "User profile page loading"

/find-regression "Payment processing workflow" --since="2 weeks ago"

/find-regression "Email notification delivery" --author="john.doe@example.com"

/find-regression "Shopping cart total calculation" --file="CartService.cs" --report=summary
```

## Output

**Format**: Markdown report saved to `marketplace/output/root-cause-analysis/regression-<feature>-<timestamp>.md`

**Main Sections**:
1. **Executive Summary** - Regression overview and key findings
2. **Feature Definition** - What regressed and expected behavior
3. **Git History Analysis** - Commit timeline and relevant changes
4. **Breaking Commit Identification** - The commit that introduced regression
5. **Code Change Analysis** - What changed and why it broke the feature
6. **Related Changes** - Other commits that may have contributed
7. **Fix Recommendations** - How to fix based on git context
8. **Prevention Strategy** - How to prevent similar regressions

**Example Output Snippet**:
```markdown
# Regression Analysis: User Profile Page Loading

## Executive Summary
**Feature**: User profile page loading and data display
**Status**: BROKEN - Page crashes with NullReferenceException
**Breaking Commit**: abc123f (2026-01-10 14:23:15)
**Author**: John Doe <john.doe@example.com>
**Root Cause**: Removed null check on optional Address property during refactoring
**Impact**: 15% of users cannot load profile page

## Breaking Commit Details
**Commit**: abc123f
**Date**: 2026-01-10 14:23:15
**Author**: John Doe
**Message**: "Refactor UserService to simplify DTO mapping"

**Files Changed**:
- UserService.cs (+15, -20 lines)
- UserProfileDTO.cs (+3, -5 lines)

**Critical Change (UserService.cs:150)**:
```diff
-    City = user.Address?.City ?? "Not Specified",
+    City = user.Address.City,
```

**Analysis**: Removed null-conditional operator, assuming Address always exists.
```

## Process Overview

The agent follows a systematic six-phase analysis process that starts with defining the regressed feature and progressively narrows down git history to find the exact breaking commit. It combines git log analysis, git blame for code authorship, commit diff analysis, and bisect-style reasoning to pinpoint when the regression occurred.

The analysis begins by understanding what worked before and what's broken now. Then it traverses git history to identify all commits affecting the feature area. Each relevant commit is analyzed for potential breaking changes. Through a process of elimination and evidence gathering, the breaking commit is identified and its changes are analyzed in detail.

For complex scenarios with multiple interacting commits or unclear breaking points, the agent can enable Sequential Thinking to provide deeper reflection on causality and course-correct if early hypotheses don't align with evidence.

## Detailed Process

### Phase 1: Feature Definition & Expected Behavior
**Duration**: 8-10% of total time
**Input**: Feature description from user
**Process**:
1. Parse feature description to extract key elements:
   - **Feature name**: What functionality is affected
   - **Current behavior**: What's broken or changed
   - **Expected behavior**: What should happen (previous working state)
   - **Observable symptoms**: Errors, crashes, incorrect results
   - **Affected components**: UI, backend, database, integration
2. Identify code areas likely involved:
   - Use Grep to find relevant files by feature name
   - Search for related classes, methods, controllers
   - Identify entry points (UI pages, API endpoints)
   - Map feature to code components
3. Determine analysis scope:
   - Date range: When did it last work? (from user or estimate)
   - File scope: Which files are likely affected
   - Branch scope: Which branch to analyze
   - Commit scope: Approximate commit count to analyze
4. Define success criteria for identification:
   - What evidence confirms the breaking commit?
   - Code changes that match the regression symptom
   - Timing aligns with when regression was observed
   - Author confirms or code review shows the issue

**Tools Used**: Grep, Glob
**Output**: Structured feature definition with code components mapped
**Success Criteria**:
- Feature clearly defined with expected vs actual behavior
- Code components identified (files, classes, methods)
- Analysis scope determined (date range, files, branch)
- Success criteria established

**Example**:
```markdown
## Feature Definition

### Feature Name
"User Profile Page Loading"

### Current Behavior (BROKEN)
- Profile page crashes with error: "Object reference not set to an instance of an object"
- Affects users without address on file
- Error occurs immediately on page load
- Started happening ~2 weeks ago

### Expected Behavior (PREVIOUS WORKING STATE)
- Profile page loads successfully for all users
- Users without address see "Not Specified" for City/State
- No errors or crashes
- Worked until approximately 2026-01-10

### Observable Symptoms
- Exception: NullReferenceException
- Location: UserService.GetUserProfile
- Frequency: 100% for users without address (15% of user base)
- User impact: Cannot access profile page

### Code Components Identified
**Primary Files** (via Grep):
- UserService.cs (contains GetUserProfile method)
- UserController.cs (calls UserService)
- UserProfileDTO.cs (DTO for profile data)

**Entry Points**:
- /Profile/UserProfile.aspx (UI page)
- UserController.ProfilePage_Load (event handler)
- UserService.GetUserProfile (service method)

### Analysis Scope
- **Date Range**: 2025-12-15 to 2026-01-15 (1 month, covers ~2 weeks before regression)
- **Files**: UserService.cs, UserController.cs, UserProfileDTO.cs, User.cs
- **Branch**: main (production branch)
- **Estimated Commits**: ~50-80 commits to analyze

### Success Criteria
Breaking commit will have:
- Changes to UserService.cs or related files
- Modifications to GetUserProfile or DTO mapping
- Timing: Between 2026-01-05 and 2026-01-12 (when regression observed)
- Code change that explains NullReferenceException on Address property
```

### Phase 2: Git History Traversal & Commit Collection
**Duration**: 20-25% of total time
**Input**: Feature definition and scope from Phase 1
**Process**:
1. Execute git log to get commit history:
   ```bash
   git log --since="<date>" --until="<date>" --oneline --all -- <files>
   ```
   - Filter by date range from scope
   - Filter by files/paths identified
   - Include commit hash, date, author, message
   - Include branch information
2. Collect commit metadata:
   - Commit hash (SHA)
   - Commit date and time
   - Author name and email
   - Commit message
   - Files changed in commit
   - Number of lines added/removed
   - Parent commits (for merge analysis)
3. Categorize commits by relevance:
   - **High relevance**: Changes to identified files (UserService.cs)
   - **Medium relevance**: Changes to related files (User.cs, DTOs)
   - **Low relevance**: Changes to other files in same component
   - **Noise**: Unrelated commits (documentation, tests)
4. Sort commits chronologically (oldest to newest)
5. Build commit timeline with key events:
   - Feature changes
   - Refactoring commits
   - Bug fix commits
   - Merge commits
   - Deployment tags (if present)
6. Identify potential suspects:
   - Commits touching UserService.GetUserProfile
   - Refactoring commits (high risk)
   - Commits with messages like "fix", "refactor", "cleanup"
   - Commits by authors who work on this code

**Tools Used**: Bash (git log, git show)
**Output**: Chronological commit timeline with relevance scoring
**Success Criteria**:
- All commits in date range collected
- Metadata complete for each commit
- Commits categorized by relevance
- Timeline constructed chronologically
- Suspects identified

**Example**:
```markdown
## Git History Analysis

### Commit Timeline (2025-12-15 to 2026-01-15)

**Total Commits**: 67
**Relevant Commits**: 12 (touching UserService.cs or related files)
**High-Risk Commits**: 3 (refactoring or significant changes)

### High-Relevance Commits (12 total)

#### Commit 1: abc123f (HIGH RISK)
**Date**: 2026-01-10 14:23:15
**Author**: John Doe <john.doe@example.com>
**Message**: "Refactor UserService to simplify DTO mapping"
**Files Changed**:
- UserService.cs (+15, -20 lines)
- UserProfileDTO.cs (+3, -5 lines)
**Risk**: HIGH - Refactoring commit, significant line changes, timing matches regression

#### Commit 2: def456a
**Date**: 2026-01-08 09:15:30
**Author**: Jane Smith <jane.smith@example.com>
**Message**: "Add logging to UserService"
**Files Changed**:
- UserService.cs (+8, -2 lines)
**Risk**: LOW - Only added logging, no logic changes

#### Commit 3: ghi789b
**Date**: 2026-01-05 16:45:00
**Author**: John Doe <john.doe@example.com>
**Message**: "Update User entity to include optional Address"
**Files Changed**:
- User.cs (+5, -0 lines)
- UserRepository.cs (+2, -1 lines)
**Risk**: MEDIUM - Changed User entity, might affect Address handling

#### Commit 4: jkl012c
**Date**: 2025-12-28 11:30:00
**Author**: Admin <admin@example.com>
**Message**: "Merge branch 'feature/profile-enhancements' into main"
**Files Changed**: Multiple (merge commit)
**Risk**: MEDIUM - Merge commit, could have conflicts

#### Commits 5-12: Lower risk (bug fixes, minor changes, unrelated refactoring)

### Timeline Visualization
```
2025-12-15 ────────────────────────────────────────────────────── 2026-01-15
              │                    │           │         │
              │                    │           │         │
         Merge commit        User entity   Logging   REFACTOR ← Suspect!
         (jkl012c)          update        (def456a)  (abc123f)
                            (ghi789b)
                                                       ↑
                                               Regression observed
                                               around this date
```

### Suspect Commits (Top 3)
1. **abc123f** (2026-01-10) - Refactoring DTO mapping - **PRIMARY SUSPECT**
2. **ghi789b** (2026-01-05) - Updated User entity with optional Address
3. **jkl012c** (2025-12-28) - Merge commit with potential conflicts
```

### Phase 3: Git Blame Analysis & Code Authorship
**Duration**: 15-18% of total time
**Input**: Commit timeline from Phase 2
**Process**:
1. Use git blame on critical files/lines:
   ```bash
   git blame -L <start>,<end> <file>
   ```
   - Focus on error location (UserService.cs:150)
   - Get blame for ±20 lines around error
   - Identify who last modified each line
   - Get commit hash for each line change
2. For each blamed line, extract:
   - Commit hash that last changed the line
   - Author of that commit
   - Date of change
   - Original code vs current code
3. Cross-reference with commit timeline:
   - Match blame commits to timeline commits
   - Identify if suspect commits modified error location
   - Verify timing (within regression window)
4. Analyze code ownership patterns:
   - Who owns this code (primary author)
   - Recent changes by different authors (handoff issues)
   - Frequent contributors to this code
5. Build evidence chain:
   - Lines that changed when regression occurred
   - Commits that touched those lines
   - Authors responsible for those changes
   - Timing correlation with regression

**Tools Used**: Bash (git blame, git show)
**Output**: Line-by-line authorship with commit mapping
**Success Criteria**:
- Blame analysis complete for error location
- Commits identified for each changed line
- Authorship mapped to timeline
- Evidence chain established

**Example**:
```markdown
## Git Blame Analysis

### Error Location: UserService.cs:150

**Git Blame Output**:
```
abc123f (John Doe 2026-01-10 14:23:15 +0000 148) var profile = new UserProfileDTO
abc123f (John Doe 2026-01-10 14:23:15 +0000 149) {
abc123f (John Doe 2026-01-10 14:23:15 +0000 150)     City = user.Address.City,  ← ERROR LINE
abc123f (John Doe 2026-01-10 14:23:15 +0000 151)     State = user.Address.State
abc123f (John Doe 2026-01-10 14:23:15 +0000 152) };
def456a (Jane Smith 2026-01-08 09:15:30 +0000 153) _logger.LogInfo("Profile created");
```

**Analysis**:
- **Lines 148-152**: Last modified by commit **abc123f** (John Doe, 2026-01-10)
- **Line 150** (error line): Changed in commit **abc123f**
- **Line 153**: Changed in commit **def456a** (different author, logging only)

**Cross-Reference with Timeline**:
- Commit **abc123f** is PRIMARY SUSPECT from Phase 2
- Timing: 2026-01-10 (matches regression observation window)
- Author: John Doe (primary contributor to UserService.cs)

### Code Ownership Analysis

**UserService.cs Historical Ownership**:
- **John Doe**: 68% of lines (primary owner)
- **Jane Smith**: 22% of lines (logging and error handling)
- **Admin**: 10% of lines (initial scaffold)

**Recent Changes (Last 30 days)**:
- **abc123f** (John Doe): Modified lines 140-155 (refactoring)
- **def456a** (Jane Smith): Modified lines 153-155 (logging)
- **ghi789b** (John Doe): Modified lines 70-75 (unrelated method)

### Evidence Chain
1. Error occurs at line 150: `City = user.Address.City`
2. Line 150 last modified by commit **abc123f** on 2026-01-10
3. Commit **abc123f** timing matches regression window (regression observed ~2026-01-10 to 2026-01-12)
4. Commit message: "Refactor UserService to simplify DTO mapping" (indicates code changes)
5. Author John Doe is primary code owner (familiar with codebase)

**Conclusion**: Commit **abc123f** is highly likely to be the breaking commit.
```

### Phase 4: Breaking Commit Identification
**Duration**: 25-30% of total time (CRITICAL PHASE)
**Input**: Commit timeline + Blame analysis from Phases 2-3
**Process**:
1. Focus on primary suspect (abc123f in example):
   - Get full commit diff using `git show <commit-hash>`
   - Analyze all file changes in the commit
   - Identify code changes at error location
2. Analyze commit diff for breaking changes:
   - **Added code**: New lines that could introduce bugs
   - **Removed code**: Deleted lines that were protective (null checks, validation)
   - **Modified code**: Changed logic that could break assumptions
   - **Refactored code**: Structural changes that alter behavior
3. For the error location specifically:
   - Compare before (parent commit) vs after (this commit)
   - Identify what was removed (protective code)
   - Identify what was added (risky code)
   - Explain how change causes the regression
4. Verify breaking change hypothesis:
   - Does the code change explain the regression symptom?
   - Would this change cause NullReferenceException?
   - Is timing consistent?
   - Are there other changes that could contribute?
5. If hypothesis unclear, use bisect-style reasoning:
   - Checkout parent commit (before suspect)
   - Would error occur? (No → commit is breaking point)
   - Checkout suspect commit (after change)
   - Would error occur? (Yes → confirms breaking commit)
6. Build evidence for breaking commit:
   - Specific lines changed
   - Why those changes break the feature
   - Commit message context
   - Author intent (if deducible from message)

**If Sequential Thinking Enabled**:
- Reflection Point: "Is this commit truly the breaking point or just correlated?"
- Course Correction: If evidence is weak, analyze adjacent commits
- Confidence Check: Rate certainty (95%+ for clear breaks, 80%+ for complex cases)

**Tools Used**: Bash (git show, git diff)
**Output**: Breaking commit identified with evidence
**Success Criteria**:
- Breaking commit identified with high confidence
- Specific code changes pinpointed
- Explanation of how change causes regression
- Evidence chain complete

**Example**:
```markdown
## Breaking Commit Identification

### Primary Suspect: abc123f

**Full Commit Diff** (UserService.cs relevant portion):
```diff
 public UserProfileDTO GetUserProfile(int userId)
 {
     var user = _userRepository.GetById(userId);
     if (user == null)
         throw new UserNotFoundException($"User {userId} not found");

-    // Old code (BEFORE - WORKING)
-    var profile = new UserProfileDTO
-    {
-        UserId = user.UserId,
-        Username = user.Username,
-        City = user.Address?.City ?? "Not Specified",
-        State = user.Address?.State ?? "Not Specified"
-    };
+    // New code (AFTER - BROKEN)
+    var profile = new UserProfileDTO
+    {
+        UserId = user.UserId,
+        Username = user.Username,
+        City = user.Address.City,  // ← REMOVED null-conditional operator
+        State = user.Address.State  // ← REMOVED null-conditional operator
+    };

     return profile;
 }
```

### Breaking Change Analysis

**What Was Removed**:
```csharp
City = user.Address?.City ?? "Not Specified"
```
- **Null-conditional operator** (`?.`): Protected against null Address
- **Null-coalescing operator** (`??`): Provided default value
- **Result**: Safe code that handled null Address gracefully

**What Was Added**:
```csharp
City = user.Address.City
```
- **Direct property access**: Assumes Address is never null
- **No null check**: Will throw NullReferenceException if Address is null
- **Result**: Unsafe code that crashes when Address is null

### Why This Breaks the Feature

**Regression Causality**:
1. **Before**: Code used `user.Address?.City ?? "Not Specified"`
   - If Address is null: Expression short-circuits, returns "Not Specified"
   - If Address exists: Returns actual City value
   - **Result**: Works for all users (with or without address)

2. **After**: Code uses `user.Address.City`
   - If Address is null: Attempts to access `.City` on null object
   - **Exception thrown**: NullReferenceException
   - If Address exists: Returns actual City value
   - **Result**: Crashes for users without address (15% of users)

**Commit Message Context**:
"Refactor UserService to simplify DTO mapping"
- **Author intent**: Simplify code (remove operators)
- **Mistake**: Removed protective operators, introduced vulnerability
- **Likely reason**: Assumed Address always exists (incorrect assumption)

### Verification

**Hypothesis**: Removing null-conditional operator causes NullReferenceException

**Evidence Supporting Hypothesis**:
1. ✅ Error type matches: NullReferenceException
2. ✅ Error location matches: Line 150 (user.Address.City)
3. ✅ Code change explains error: Removed null check
4. ✅ Timing matches: Commit date (2026-01-10) aligns with regression observation
5. ✅ Affected users matches: Only users with null Address (15%)

**Confidence**: 98% (very high certainty)

### Conclusion
**Breaking Commit**: abc123f (2026-01-10 14:23:15)
**Author**: John Doe <john.doe@example.com>
**Root Cause**: Removed null-conditional operator during refactoring, introduced null reference crash
```

### Phase 5: Related Change Correlation
**Duration**: 12-15% of total time
**Input**: Breaking commit from Phase 4
**Process**:
1. Identify related commits that may have contributed:
   - Commits by same author around same time
   - Commits touching related files (User.cs, UserProfileDTO.cs)
   - Commits in same branch/PR
   - Commits with related messages (part of same feature/refactor)
2. Analyze if regression is compound (multiple commits):
   - Did earlier commit set up conditions?
   - Did later commit trigger the issue?
   - Are there dependent changes?
3. Review commit messages for context:
   - Was this part of a larger refactoring?
   - Was there a PR or code review?
   - Were there related bug reports or fixes?
4. Check for partial fixes or workarounds:
   - Were there commits attempting to fix this?
   - Incomplete fixes that missed this location?
5. Build complete timeline:
   - Breaking commit + context
   - Related commits before/after
   - Fix attempts (if any)
   - Current state

**Tools Used**: Bash (git log, git show)
**Output**: Related commits with correlation analysis
**Success Criteria**:
- Related commits identified
- Contribution of each commit understood
- Timeline complete with context
- Any fix attempts documented

**Example**:
```markdown
## Related Change Correlation

### Commits Related to abc123f (Breaking Commit)

#### Related Commit 1: ghi789b (5 days before)
**Date**: 2026-01-05 16:45:00
**Author**: John Doe (same author)
**Message**: "Update User entity to include optional Address"
**Files Changed**: User.cs, UserRepository.cs

**Changes**:
```diff
+public class User
+{
+    public int UserId { get; set; }
+    public string Username { get; set; }
+    public Address Address { get; set; }  // ← Made Address optional (nullable FK)
+}
```

**Analysis**:
- Made Address property optional in data model
- This change set up the condition for null Address
- However, code at that time (UserService.cs) had null checks
- Not breaking on its own, but created precondition

**Correlation**: Setup commit - created condition for future regression

#### Related Commit 2: def456a (2 days before)
**Date**: 2026-01-08 09:15:30
**Author**: Jane Smith (different author)
**Message**: "Add logging to UserService"
**Files Changed**: UserService.cs

**Changes**:
```diff
+_logger.LogInfo("Profile created for user {userId}", userId);
```

**Analysis**:
- Only added logging, no logic changes
- No impact on regression
- Coincidental timing

**Correlation**: Unrelated - no contribution to regression

#### Subsequent Commits: None
- No commits after abc123f attempting to fix the issue
- No workarounds or partial fixes
- Regression remains in current code

### Regression Timeline

```
2026-01-05: ghi789b - Make Address optional (SETUP)
              ↓
              (3 days)
              ↓
2026-01-08: def456a - Add logging (UNRELATED)
              ↓
              (2 days)
              ↓
2026-01-10: abc123f - Remove null check (BREAKING) ← Regression introduced
              ↓
              (2 days)
              ↓
2026-01-12: Regression observed in production
              ↓
2026-01-16: Analysis conducted (today)
```

### Compound Regression Analysis

**Is this a compound regression?** Partially

**Contributing Factors**:
1. **Primary**: Commit abc123f removed null check (direct cause)
2. **Setup**: Commit ghi789b made Address optional (created possibility of null)
3. **Context**: Refactoring without full understanding of data model changes

**Root Cause**:
- Commit abc123f is the breaking commit (removed safety net)
- However, regression was made possible by ghi789b (making Address optional)
- If Address was never optional, removing null check wouldn't cause issues
- Problem: Refactoring (abc123f) didn't account for recent data model change (ghi789b)

**Lesson**: When refactoring, consider recent changes to data models and assumptions
```

### Phase 6: Fix Recommendations & Prevention Strategy
**Duration**: 10-12% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Generate fix recommendations based on git context:

   **Immediate Fix (Revert)**:
   - Option 1: Revert the breaking commit
   - Option 2: Cherry-pick the fix
   - Option 3: Forward fix with proper null check

   **Proper Fix**:
   - Restore null checks with proper error handling
   - Consider why change was made (simplification) and address properly
   - Add tests to prevent recurrence

   **Prevention Strategy**:
   - Code review practices
   - Test coverage requirements
   - Refactoring guidelines
   - Communication about data model changes

2. Provide git commands for each fix option:
   - Revert: `git revert <commit-hash>`
   - Cherry-pick: `git cherry-pick <fix-commit>`
   - Manual fix: Code example + commit message template

3. Generate rollback plan:
   - Revert commit in hotfix branch
   - Test revert
   - Deploy to production
   - Create proper fix for next release

4. Create prevention recommendations:
   - **Code Review**: Require reviews for refactoring commits
   - **Testing**: Mandate edge case tests (null scenarios)
   - **Communication**: Link related commits in messages
   - **CI/CD**: Add null reference checks in static analysis
   - **Documentation**: Document assumptions about data models

5. Provide commit message templates:
   - For revert commit
   - For forward fix
   - For proper solution

**Tools Used**: Write
**Output**: Comprehensive fix guide with git commands
**Success Criteria**:
- Multiple fix options provided
- Git commands accurate and ready to use
- Rollback plan complete
- Prevention strategy actionable
- Commit templates helpful

**Example**:
```markdown
## Fix Recommendations

### Option 1: Immediate Revert (FASTEST - 5 minutes)

**Approach**: Revert the breaking commit to restore previous working state

**Git Commands**:
```bash
# Create hotfix branch
git checkout main
git pull origin main
git checkout -b hotfix/revert-userservice-refactor

# Revert the breaking commit
git revert abc123f

# Review the revert (make sure it's correct)
git show HEAD

# Test the revert locally
# ... run tests, verify profile page works ...

# Push and create PR
git push origin hotfix/revert-userservice-refactor
```

**Commit Message** (auto-generated by git revert):
```
Revert "Refactor UserService to simplify DTO mapping"

This reverts commit abc123f.

Reason: The refactoring removed null-conditional operators for
optional Address property, causing NullReferenceException for
15% of users without addresses. Reverting to restore null checks
and default values.

Regression analysis: output/root-cause/regression-userprofile-20260116.md
```

**Pros**:
- Fastest fix (5 minutes)
- Restores working state immediately
- Safe (just undoes the breaking change)

**Cons**:
- Undoes entire commit (including any good changes)
- Doesn't address root cause of why refactoring happened
- Need proper fix later

**Recommendation**: Use for immediate production hotfix

---

### Option 2: Forward Fix (BALANCED - 20 minutes)

**Approach**: Apply proper null check without reverting entire commit

**Code Change** (UserService.cs:150):
```csharp
// Current (BROKEN)
City = user.Address.City,
State = user.Address.State

// Fixed (WORKING)
City = user.Address?.City ?? "Not Specified",
State = user.Address?.State ?? "Not Specified"
```

**Git Commands**:
```bash
# Create fix branch
git checkout main
git pull origin main
git checkout -b fix/userservice-null-check

# Make the code change (edit UserService.cs)
# ... apply fix above ...

# Commit the fix
git add UserService.cs
git commit -m "$(cat <<'EOF'
Fix NullReferenceException in UserService.GetUserProfile

Restore null-conditional operators for optional Address property
that were removed in commit abc123f. This fixes profile page
crashes for users without addresses (15% of users).

Changes:
- Restore ?. operator for safe null checking
- Restore ?? operator for default values
- Add unit test for null Address scenario

Root cause: Refactoring in abc123f removed protective null checks
Regression analysis: output/root-cause/regression-userprofile-20260116.md

Fixes: Regression introduced in abc123f
EOF
)"

# Add unit test
# ... create test for null Address scenario ...
git add UserServiceTests.cs
git commit --amend --no-edit

# Push and create PR
git push origin fix/userservice-null-check
```

**Unit Test to Add**:
```csharp
[TestMethod]
public void GetUserProfile_UserWithoutAddress_ReturnsDefaultValues()
{
    // Arrange
    var user = new User
    {
        UserId = 1,
        Username = "testuser",
        Address = null  // ← Test null scenario
    };
    _mockRepository.Setup(x => x.GetById(1)).Returns(user);

    // Act
    var profile = _userService.GetUserProfile(1);

    // Assert
    Assert.AreEqual("Not Specified", profile.City);
    Assert.AreEqual("Not Specified", profile.State);
}
```

**Pros**:
- Fixes the specific issue (targeted)
- Adds test coverage
- Good commit message with context
- Keeps any other good changes from abc123f

**Cons**:
- Slightly more work than revert (20 min vs 5 min)
- Need to write and test the fix

**Recommendation**: Use for proper fix after hotfix

---

### Option 3: Comprehensive Solution (BEST - 2 hours)

**Approach**: Fix all similar issues and prevent recurrence

**Step 1**: Apply fix to UserService.GetUserProfile (as in Option 2)

**Step 2**: Scan for similar patterns (use /analyze-bug-pattern)
```bash
/analyze-bug-pattern "Missing null check on optional navigation property"
```

**Step 3**: Fix all identified locations (from pattern analysis)

**Step 4**: Add null reference prevention
```csharp
// Enable nullable reference types (C# 8+)
// In .csproj
<PropertyGroup>
  <Nullable>enable</Nullable>
</PropertyGroup>

// Update User.cs to mark Address as nullable
public Address? Address { get; set; }  // ← Explicit nullable
```

**Step 5**: Add code analysis rules
```xml
<!-- Directory.Build.props -->
<PropertyGroup>
  <AnalysisLevel>latest</AnalysisLevel>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>
```

**Step 6**: Add comprehensive tests for all optional properties

**Pros**:
- Fixes all similar issues (not just this one)
- Prevents future occurrences
- Improves code quality
- Build-time checking for null issues

**Cons**:
- Significant time investment (2 hours)
- Requires C# 8+ and framework updates
- May require team training

**Recommendation**: Use as follow-up after immediate fix deployed

---

## Prevention Strategy

### Code Review Improvements

**Add to Code Review Checklist**:
- [ ] Refactoring preserves null checks for optional properties
- [ ] Data model changes communicated to consumers
- [ ] Edge cases tested (null, empty, edge values)
- [ ] Related commits linked in message (e.g., "Related to ghi789b")

**Review Process**:
- Require 2 approvals for refactoring commits
- Flag removals of protective code (null checks, validations)
- Review recent data model changes when reviewing service changes

### Testing Requirements

**Mandatory Tests for Service Methods**:
- Happy path test (normal case)
- Edge case test (null, empty, boundary)
- Error case test (exceptions, validation failures)

**Test Naming Convention**:
```csharp
[TestMethod]
public void MethodName_Scenario_ExpectedBehavior()
{
    // Example: GetUserProfile_UserWithoutAddress_ReturnsDefaultValues
}
```

### CI/CD Integration

**Static Analysis**:
- Enable nullable reference types (C# 8+)
- Add Roslyn analyzers for null checking
- Fail build on null reference warnings

**Automated Tests**:
- Require 80%+ code coverage
- Mandate edge case tests for public methods
- Run regression test suite on all commits

### Communication Practices

**Commit Message Template**:
```
<type>: <short summary>

<detailed description>

Related commits: <hash> <hash>
Affects: <components>
Breaking change: [Yes/No]
```

**Data Model Change Protocol**:
- When making properties optional, notify team
- Search for usages and verify null handling
- Update documentation for optional fields

### Team Training

**Topics to Cover**:
- Defensive programming (null checks, validations)
- Nullable reference types (C# 8+)
- Git bisect for regression debugging
- Impact analysis before refactoring

---

## Rollback Plan

### If Fix Fails or Causes New Issues

**Rollback Steps**:
```bash
# Revert the fix
git revert HEAD

# Or reset to previous state
git reset --hard HEAD~1
git push origin <branch> --force

# Deploy previous version
# ... deployment commands ...
```

**Monitoring**:
- Watch error rates for 24 hours post-deploy
- Monitor user impact metrics
- Check for new exceptions

**Escalation**:
- If revert doesn't fix: Investigate further (may be compound issue)
- If new errors appear: May need different fix approach
```

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **root-cause-analysis** (`../../shared-skills/root-cause-analysis.md`)
  - Systematic evidence gathering
  - Causality analysis
  - Root cause vs symptom differentiation

- **performance-analysis-framework** (`../../shared-skills/performance-analysis-framework.md`)
  - Impact assessment methodologies
  - Timeline reconstruction
  - Change correlation

- **code-review-best-practices** (`../../shared-skills/code-review-best-practices.md`)
  - Code change analysis
  - Review checklist generation
  - Best practice identification

## Error Handling

### Scenario: Not in Git Repository
**When**: Current directory is not a git repository
**Recovery**: Cannot proceed without git history
**User Message**:
```
❌ Git repository not found.

Regression analysis requires git history to identify when code changed.

Please ensure:
- You're in a git repository directory
- The directory has been initialized with `git init`
- There are commits in the repository

Cannot proceed without git history.
```

### Scenario: No Commits in Date Range
**When**: Git log returns no commits for specified date range
**Recovery**: Expand date range or suggest different scope
**User Message**:
```
⚠ No commits found in specified date range.

**Search Parameters**:
- Date range: 2025-12-15 to 2026-01-15
- Files: UserService.cs, UserController.cs
- Branch: main

**Suggestions**:
- Expand date range (try --since="2 months ago")
- Check if feature exists in this branch
- Verify file paths are correct
- Try without file filter to see all commits

Would you like to expand the search range?
```

### Scenario: Multiple Potential Breaking Commits
**When**: Several commits could be the breaking point
**Recovery**: Enable Sequential Thinking for deeper analysis
**User Message**:
```
🔍 Found multiple potential breaking commits (4 candidates).

Enabling deep analysis mode to determine actual breaking commit.

**Candidates**:
1. abc123f - Refactoring (high probability)
2. def456a - Data model change (medium probability)
3. ghi789b - Logic change (medium probability)
4. jkl012c - Merge commit (low probability)

Analyzing each commit's impact on regression...
Estimated time: 15-20 minutes
```

### Scenario: Feature Description Too Vague
**When**: Cannot map feature to code components
**Recovery**: Request more specific information
**User Message**:
```
⚠ Feature description is too vague to analyze accurately.

**Provided**: "something broke"
**Need**:
- What specific feature or functionality broke?
- What's the observable error or symptom?
- When did it last work?
- Which page/component is affected?

**Example good description**:
"User profile page loading - crashes with NullReferenceException - worked until ~2 weeks ago"

Please provide more details.
```

### Scenario: Breaking Commit Has Been Reverted
**When**: Git history shows commit was already reverted
**Recovery**: Identify why revert was needed and if issue persists
**User Message**:
```
ℹ Breaking commit was already reverted.

**Breaking Commit**: abc123f (2026-01-10)
**Revert Commit**: xyz789d (2026-01-11)
**Revert Message**: "Revert refactoring due to crashes"

**Analysis**:
- Issue was identified and reverted
- Current code should be working
- If issue persists, may be different root cause

Is the regression still occurring? If yes, it may be a different commit.
```

### Scenario: Insufficient Git Metadata
**When**: Commit messages are uninformative or missing
**Recovery**: Rely more on code diff analysis, less on context
**User Message**:
```
⚠ Commit messages are sparse (no detailed descriptions).

Relying on code diff analysis rather than commit message context.
Analysis will take longer but will still identify breaking commit.

Recommendation: Encourage team to write descriptive commit messages.
```

## Configuration

### Required Settings
None - agent works with defaults (requires git repository)

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "root-cause-analyzer": {
    "regression-analyzer": {
      "default_date_range_days": 30,
      "max_commits_to_analyze": 100,
      "git_blame_context_lines": 10,
      "include_merge_commits": true,
      "enable_sequential_thinking": "conditional",
      "sequential_thinking_trigger": {
        "min_candidate_commits": 3,
        "unclear_breaking_point": true
      },
      "timeout_minutes": 45,
      "file_type_priority": [".cs", ".java", ".js", ".py"],
      "exclude_patterns": ["*Test.cs", "*Tests.cs", "*.Designer.cs"]
    }
  }
}
```

**Configuration Options**:
- `default_date_range_days`: Days to look back if not specified (default: 30)
- `max_commits_to_analyze`: Maximum commits to process (default: 100)
- `git_blame_context_lines`: Lines of context for git blame (default: 10)
- `include_merge_commits`: Analyze merge commits (default: true)
- `enable_sequential_thinking`: "always", "conditional", or "never" (default: "conditional")
- `timeout_minutes`: Maximum analysis time (default: 45)
- `file_type_priority`: Prioritize certain file types in analysis
- `exclude_patterns`: Exclude files from analysis (tests, generated code)

## Tools Required

- **Bash**: Execute git commands (log, blame, show, diff)
- **Glob**: Find files by pattern for feature mapping
- **Grep**: Search code for feature-related components
- **Read**: Read source files to understand code changes
- **Write**: Generate comprehensive regression report

## Examples

### Example 1: Simple Regression (Single Breaking Commit)
**Input**:
```bash
/find-regression "User profile page loading"
```

**Process**:
- Phase 1: Map feature to UserService.cs, UserController.cs (3 min)
- Phase 2: Collect 67 commits from last 30 days, filter to 12 relevant (7 min)
- Phase 3: Git blame identifies commit abc123f at error location (5 min)
- Phase 4: Analyze abc123f diff, find removed null check (8 min)
- Phase 5: Identify related commit ghi789b (setup condition) (4 min)
- Phase 6: Generate fix recommendations (revert, forward fix, prevention) (5 min)

**Output**: Report with:
- Breaking commit: abc123f
- Root cause: Removed null-conditional operator
- Related: ghi789b made Address optional
- Fix options: Revert (5 min), Forward fix (20 min), Comprehensive (2 hrs)

**Time**: ~32 minutes
**Confidence**: 98%

### Example 2: Complex Regression (Multiple Interacting Commits)
**Input**:
```bash
/find-regression "Payment processing workflow" --since="1 month ago"
```

**Process**:
- Phase 1: Map feature to PaymentService, PaymentGateway, Order entities (4 min)
- Phase 2: Collect 124 commits, filter to 18 relevant (10 min)
- Phase 3: Git blame shows multiple authors, multiple commits (7 min)
- Phase 4: Analyze 4 candidate commits (15 min) [Sequential Thinking enabled]
  - Candidate 1: Data model change (setup)
  - Candidate 2: Validation logic change (indirect)
  - Candidate 3: Integration refactoring (breaking)
  - Candidate 4: Configuration change (trigger)
  - Reflection: "Which commit is the true breaking point?"
  - Course correction: Compound regression (Commit 3 + Commit 4)
- Phase 5: Correlate all 4 commits into timeline (8 min)
- Phase 6: Generate complex fix with multiple components (8 min)

**Output**: Report with:
- Primary breaking commit: Commit 3 (integration refactoring)
- Trigger commit: Commit 4 (configuration change)
- Setup commits: Commit 1, 2 (created conditions)
- Fix strategy: Revert Commit 4, fix Commit 3, adjust for Commits 1-2

**Time**: ~52 minutes
**Confidence**: 85% (Sequential Thinking enabled for complex analysis)

### Example 3: Merge Conflict Regression
**Input**:
```bash
/find-regression "Shopping cart total calculation" --since="2 weeks ago"
```

**Process**:
- Phase 1: Map feature to CartService.CalculateTotal (3 min)
- Phase 2: Collect 45 commits, identify merge commit as suspect (6 min)
- Phase 3: Git blame points to merge commit (4 min)
- Phase 4: Analyze merge commit diff, find conflict resolution issue (12 min)
  - Merge combined changes from two branches
  - Conflict resolution chose wrong version
  - Tax calculation logic lost during merge
- Phase 5: Identify both branch commits that conflicted (6 min)
- Phase 6: Generate fix to restore correct conflict resolution (5 min)

**Output**: Report with:
- Breaking commit: Merge commit (conflict resolution error)
- Root cause: Incorrect conflict resolution, lost tax calculation
- Related: Two feature branches that conflicted
- Fix: Restore correct conflict resolution from branch A

**Time**: ~36 minutes
**Confidence**: 92%

## Success Metrics

Analysis is successful when:
- [ ] Feature clearly defined with expected vs actual behavior
- [ ] Code components mapped to feature
- [ ] Git history collected for relevant date range
- [ ] Commits categorized by relevance
- [ ] Git blame executed for error location
- [ ] Breaking commit identified with high confidence (>85%)
- [ ] Specific code changes pinpointed
- [ ] Explanation of how change causes regression provided
- [ ] Related commits identified and correlated
- [ ] Multiple fix options provided (revert, forward fix, comprehensive)
- [ ] Git commands accurate and ready to use
- [ ] Prevention strategy actionable
- [ ] Report comprehensive and well-structured
- [ ] Report saved to correct output directory

## Related Agents

- **codebase-pattern-analyzer**: Use to find similar bugs after identifying regression cause
- **error-correlation-analyzer**: Use when multiple errors may stem from same regression
- **stack-trace-analyzer**: Use for detailed error analysis before regression analysis
- **impact-analyzer**: Use to assess impact of proposed fixes
- **code-review-agent**: Use to review fixes before deployment

## Related Documentation

- `../../shared-skills/root-cause-analysis.md` - Root cause methodology
- `../../shared-skills/code-review-best-practices.md` - Code review patterns
- `../commands/find-regression.md` - Command specification
- `../../../docs/WORKFLOW_DECISION_GUIDE.md` - When to use which analysis agent

---

**Agent Status**: Production Ready
**Verification Mode**: Enabled (all findings backed by git evidence)
**Sequential Thinking**: Conditional (auto-enabled for multiple candidate commits or unclear breaking points)
**Average Duration**: 30-50 minutes depending on commit history complexity
