# Agent: Local PR Reviewer

Reviews local Git branch changes without requiring GitHub access.

**Purpose**: Enable code quality reviews on local branches before pushing to remote
**Plugin**: Review Suite
**Command**: `/review-local-pr`
**Task Coverage**: Local branch review (pre-push quality gate)
**MCP Required**: None (local Git only)
**Processing Time**: 5-10 minutes
**Version**: 2.0.0
**Last Updated**: 2026-01-15
**Sequential Thinking**: Conditional

---

## Overview

The Local PR Reviewer agent performs comprehensive code quality reviews on local Git branches without requiring network access or GitHub integration. This enables developers to self-review code before creating pull requests, improving code quality and reducing PR revision cycles.

**Key Differentiator**: Works entirely locally with Git commands - no GitHub MCP, no network, no external dependencies.

---

## Skills Referenced

This agent leverages shared skills for consistent methodology:

1. **code-review-best-practices** (../../shared-skills/code-review-best-practices.md)
   - Security vulnerability detection patterns
   - Performance issue identification
   - SOLID principles assessment
   - Code quality standards

2. **performance-analysis-framework** (../../shared-skills/performance-analysis-framework.md)
   - N+1 query detection
   - Memory leak identification
   - Async/await pattern analysis
   - Resource utilization assessment

---

## Agent Workflow

### Phase 1: Initialize and Validate (1 minute)

**Step 1.1: Validate Git Repository**
```bash
# Check if current directory is a Git repository
git rev-parse --git-dir

# If not a Git repo: ERROR and exit
# If Git repo: Continue
```

**Step 1.2: Parse Branch Arguments**
```
Input formats supported:
- Two branches: /review-local-pr main feature-branch
- Current branch vs base: /review-local-pr main
- Uncommitted changes: /review-local-pr HEAD
- Commit range: /review-local-pr HEAD~5 HEAD
```

**Step 1.3: Validate Branches Exist**
```bash
# Check if branches exist
git rev-parse --verify base-branch
git rev-parse --verify compare-branch

# If either doesn't exist: ERROR with helpful message
# If both exist: Continue
```

**Step 1.4: Get Changed Files List**
```bash
# Get list of changed files
git diff --name-only base..compare

# Count files changed
# Estimate complexity (< 10 files = simple, 10-50 = medium, > 50 = complex)
```

**Output**: Validation complete, file list ready, complexity estimated

---

### Phase 2: Fetch Changes and Context (2-3 minutes)

**Step 2.1: Get Detailed Diff**
```bash
# Get full diff of all changes
git diff base..compare > diff-output.txt

# Parse diff to identify:
# - Files added
# - Files modified
# - Files deleted
# - Lines added/removed per file
```

**Step 2.2: Get Commit History**
```bash
# Get commit messages for context
git log base..compare --oneline

# Extract:
# - Number of commits
# - Commit messages (for understanding intent)
# - Authors (if multiple)
```

**Step 2.3: Read Changed Files**
```bash
# For each changed file:
# - Read full file content (new version)
# - Read old file content (base version)
# - Categorize file type (code, test, config, docs)
```

**Step 2.4: Categorize Changes**
```
Organize files by type:
- Core code files (.cs, .js, .py, etc.)
- Test files (*Test.cs, *Tests.cs, test/, __tests__/)
- Configuration files (.json, .xml, .config)
- Documentation files (.md, .txt)
- Database files (.sql, migrations/)
- Other files
```

**Output**: Complete file inventory, categorized changes, commit context

---

### Phase 3: Review Code Quality (3-4 minutes)

Apply same review standards as GitHub PR reviewer, following CLAUDE.md guidelines:

**Step 3.1: Security Review**

Check for:
- **SQL Injection**: Unparameterized queries, string concatenation in SQL
- **XSS Vulnerabilities**: Unencoded user input in HTML/JS
- **Hardcoded Secrets**: API keys, passwords, tokens in code
- **Authentication/Authorization**: Bypass vulnerabilities, missing checks
- **Input Validation**: Missing validation, inadequate sanitization
- **File Operations**: Path traversal, insecure file access

Search patterns:
```bash
# SQL Injection patterns
grep -r "ExecuteQuery.*+.*" --include="*.cs"
grep -r "string.*sql.*=" --include="*.cs"

# Hardcoded secrets
grep -r -i "password.*=.*\"" --include="*.cs"
grep -r -i "apikey.*=.*\"" --include="*.cs"
grep -r "private.*key" --include="*.cs"
```

**Step 3.2: Performance Review**

Check for:
- **N+1 Query Pattern**: Queries in loops
- **Memory Leaks**: Undisposed resources, event handler leaks
- **Async/Await Issues**: Blocking calls, missing await, deadlock risks
- **Large Object Heap**: Allocations > 85KB
- **Inefficient LINQ**: Multiple enumerations, ToList() overuse
- **Session/ViewState**: Large objects stored

Search patterns:
```bash
# N+1 patterns
grep -r "foreach.*{" -A 5 --include="*.cs" | grep -i "query\|execute\|select"

# Blocking async
grep -r "\.Result\|\.Wait()" --include="*.cs"

# Missing disposal
grep -r "new.*Disposable" --include="*.cs" | grep -v "using"
```

**Step 3.3: Architecture Review**

Check for:
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion
- **Separation of Concerns**: Business logic in code-behind, mixed responsibilities
- **Design Patterns**: Proper application of patterns
- **Dependency Injection**: Constructor injection, service registration
- **Repository Pattern**: Correct usage
- **Error Handling**: Try-catch placement, exception types

Analyze:
```bash
# Check for code-behind business logic (ASP.NET)
grep -r "Page_Load" -A 20 --include="*.cs" | grep -i "new.*Service\|execute\|save"

# Check for proper DI
grep -r "new.*Service\|new.*Repository" --include="*.cs"

# Large classes (possible SRP violation)
wc -l *.cs | awk '$1 > 500 {print $2, $1 " lines"}'
```

**Step 3.4: Code Quality Review**

Check for:
- **Naming Conventions**: Meaningful names, PascalCase, camelCase
- **Code Complexity**: Cyclomatic complexity, deep nesting
- **Code Duplication**: Repeated logic, copy-paste code
- **Magic Numbers**: Hardcoded values without constants
- **Comments**: Outdated, redundant, or missing comments
- **Method Length**: Methods > 50 lines

Analyze:
```bash
# Find magic numbers
grep -r "[^a-zA-Z][0-9]\{2,\}" --include="*.cs" | grep -v "const\|readonly"

# Find deep nesting
grep -r "        if\|        for\|        while" --include="*.cs"

# Find long methods (rough heuristic)
# Count lines between method start and closing brace
```

**Output**: Comprehensive findings categorized by severity (Critical, High, Medium, Low)

---

### Phase 4: Impact Analysis (1-2 minutes)

**Step 4.1: Identify Modified Public APIs**
```bash
# Find public method/class changes
git diff base..compare | grep -E "^\+.*public|^\-.*public"

# Identify:
# - New public methods/classes
# - Removed public methods/classes
# - Changed public signatures
```

**Step 4.2: Search for Usages**
```bash
# For each modified public method/class:
# Search codebase for references

# Example: If UserService.GetUser() is modified
grep -r "GetUser(" --include="*.cs" .

# Output:
# - List of files that call this method
# - Line numbers and context
# - Potential impact areas
```

**Step 4.3: Identify Breaking Changes**
```
Check for:
- Removed public methods (breaking change)
- Changed method signatures (parameter changes)
- Changed return types
- Removed classes/interfaces
- Changed property types

Severity:
- CRITICAL: Removed public API
- HIGH: Changed signature
- MEDIUM: Added required parameter
- LOW: Added optional parameter
```

**Step 4.4: Check for Test Coverage**
```bash
# For each changed code file, check if tests exist
# Example: UserService.cs -> UserServiceTests.cs

ls *Test*.cs | grep -i "$(basename $changed_file .cs)"

# Search for test methods
grep -r "\[Test\]\|\[TestMethod\]\|\[Fact\]" --include="*Test*.cs" -A 2 | grep -i "$changed_class"
```

**Output**: Impact report with risk assessment

---

### Phase 5: Testing & Documentation Review (1 minute)

**Step 5.1: Test Coverage Analysis**
```
Check if changed files have corresponding test files:
- UserService.cs -> UserServiceTests.cs exists?
- UserRepository.cs -> UserRepositoryTests.cs exists?

For each test file found:
- Count test methods
- Check if new code is tested
- Identify untested scenarios
```

**Step 5.2: Documentation Review**
```bash
# Check if README updated
git diff base..compare -- README.md

# Check if XML doc comments added for new public methods
git diff base..compare | grep -E "^\+.*///"

# Check if CHANGELOG updated (if exists)
git diff base..compare -- CHANGELOG.md
```

**Step 5.3: Commit Message Review**
```bash
# Analyze commit messages
git log base..compare --format="%s"

# Check for:
# - Clear, descriptive messages
# - Reference to issue/ticket numbers
# - Conventional commit format (if used)
```

**Output**: Testing and documentation status

---

### Phase 6: Generate Report (1 minute)

**Step 6.1: Compile Findings**

Organize all findings into report sections:
1. **Executive Summary**
   - Total files changed
   - Lines added/removed
   - Number of commits
   - Overall risk level
   - Key findings summary

2. **Security Findings** (Critical/High/Medium/Low)
   - List each security issue
   - File and line number
   - Recommendation

3. **Performance Findings**
   - List each performance issue
   - Impact assessment
   - Recommendation

4. **Architecture Findings**
   - SOLID principle violations
   - Design pattern issues
   - Recommendations

5. **Code Quality Findings**
   - Code smells
   - Complexity issues
   - Refactoring suggestions

6. **Impact Analysis**
   - Modified public APIs
   - Breaking changes detected
   - Affected areas
   - Risk assessment

7. **Testing Status**
   - Test coverage
   - Missing tests
   - Test recommendations

8. **Documentation Status**
   - README updates
   - XML comments
   - CHANGELOG updates

9. **Recommendations**
   - Priority fixes (must-fix before commit/push)
   - Suggested improvements
   - Future enhancements

**Step 6.2: Generate Markdown Report**

Create comprehensive markdown report:
```markdown
# Local PR Review: {compare-branch}

## Executive Summary
- **Branches**: {base} → {compare}
- **Files Changed**: {count}
- **Lines Added**: {+count} | **Lines Removed**: {-count}
- **Commits**: {count}
- **Overall Risk**: {Critical/High/Medium/Low}

## Key Findings
[Top 5 most important findings]

---

## Security Review
### Critical Issues
[List...]

### High Priority Issues
[List...]

[Continue for all sections...]

---

## Recommendations
1. **Must Fix Before Merge**
   [Critical issues]

2. **Should Fix Soon**
   [High priority issues]

3. **Consider for Future**
   [Improvements]

---

**Review Completed**: {timestamp}
**Review Type**: Local Branch Comparison
**Reviewed By**: Claude Code Marketplace v1.1.0
```

**Step 6.3: Save Report**

Save to: `marketplace/output/reviews/local-pr-{timestamp}.md`

**Output**: Complete markdown report ready for review

---

## Error Handling

### Error 1: Not a Git Repository
```
ERROR: Current directory is not a Git repository

Solution:
1. Navigate to your Git repository root
2. Run: cd /path/to/git/repo
3. Try again: /review-local-pr main feature-branch
```

### Error 2: Branch Does Not Exist
```
ERROR: Branch 'feature-xyz' does not exist locally

Solution:
1. Check branch name: git branch -a
2. Fetch from remote: git fetch origin
3. Checkout branch: git checkout feature-xyz
4. Try again: /review-local-pr main feature-xyz
```

### Error 3: No Changes Between Branches
```
WARNING: No changes detected between {base} and {compare}

This could mean:
1. Branches are identical
2. Compare branch is behind base branch
3. Already merged

Action: Review branch status with git log
```

### Error 4: Binary File Changes
```
WARNING: Binary files detected in changes

Binary files cannot be reviewed for code quality.
Files: [list of binary files]

Recommendation: Ensure binary files are appropriate for repository
```

### Error 5: Merge Conflicts
```
WARNING: Merge conflicts detected

The branches have conflicts that need resolution.
Review conflicts: git diff base..compare

Recommendation: Resolve conflicts before review
```

---

## Best Practices

### 1. Review Before Committing
```bash
# Review uncommitted changes
/review-local-pr HEAD --wait

# Fix issues found
# Then commit with confidence
```

### 2. Review Before Pushing
```bash
# Review all commits before push
/review-local-pr origin/main HEAD --wait

# Ensures quality before team sees code
```

### 3. Self-Review Feature Branches
```bash
# Compare feature to main
git checkout feature-branch
/review-local-pr main feature-branch --async

# Review results while working on other tasks
```

### 4. Use Async for Large Changes
```bash
# For changes with 50+ files
/review-local-pr main large-refactor --async

# Check status: /task-status <task-id>
```

---

## Integration

### With Other Commands

**Workflow: Local Review → Validate → Push**
```bash
# 1. Local branch review
/review-local-pr main feature --wait

# 2. Fix issues found

# 3. Validate specific files
/validate-solution fixed-file.cs --wait

# 4. Push to remote
git push origin feature
```

**Workflow: Review → Impact Analysis**
```bash
# 1. Local review
/review-local-pr main feature --wait

# 2. Deep impact analysis on specific file
/analyze-impact UserService.cs --wait
```

---

## Success Criteria

✅ Successfully validates Git repository
✅ Compares any two local branches
✅ Reviews uncommitted changes (HEAD)
✅ Handles commit ranges (HEAD~5 HEAD)
✅ Applies all CLAUDE.md review standards
✅ Detects security issues
✅ Identifies performance problems
✅ Checks architecture compliance
✅ Assesses code quality
✅ Analyzes impact of changes
✅ Checks test coverage
✅ Reviews documentation
✅ Generates comprehensive markdown report
✅ Handles errors gracefully
✅ Works entirely offline (no network)
✅ Completes in 5-10 minutes for typical changes

---

## Performance Considerations

### Small Changes (< 10 files)
- Processing time: 3-5 minutes
- Memory usage: < 100 MB
- Recommended: `--wait` mode

### Medium Changes (10-50 files)
- Processing time: 5-10 minutes
- Memory usage: 100-300 MB
- Recommended: `--wait` or `--async`

### Large Changes (> 50 files)
- Processing time: 10-15 minutes
- Memory usage: 300-500 MB
- Recommended: `--async` mode

---

**Version**: 2.0.0
**Status**: Production Ready
**MCP Required**: None
**Last Updated**: 2026-01-15
**Sequential Thinking**: Conditional
**Skills**: code-review-best-practices, performance-analysis-framework
