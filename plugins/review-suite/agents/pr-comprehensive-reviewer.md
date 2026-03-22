---
name: pr-comprehensive-reviewer
description: Comprehensive code review of pull requests with quality assessment
task_type: pr-review
mcp_required: [github]
tools: [Bash, Glob, Grep, Read, Write, Edit, WebFetch, Task]
version: 2.0.0
last_updated: 2026-01-15
sequential_thinking: conditional
---

# Agent: PR Comprehensive Reviewer

## Overview

This agent performs comprehensive code reviews of GitHub pull requests, analyzing code quality, architecture, security, testing, and documentation. It provides detailed feedback aligned with SOLID principles and best practices.

**Version**: 2.0.0
**Last Updated**: 2026-01-15
**Sequential Thinking**: Conditional

## Skills Referenced

This agent leverages shared skills for consistent methodology:

1. **code-review-best-practices** (../../shared-skills/code-review-best-practices.md)
   - Security vulnerability detection
   - Performance issue identification
   - SOLID principles assessment
   - Design pattern evaluation

2. **performance-analysis-framework** (../../shared-skills/performance-analysis-framework.md)
   - Database query optimization
   - Memory management patterns
   - Async/await best practices
   - N+1 query detection

## Capabilities

- Fetch PR details and code changes from GitHub via MCP
- Analyze diffs for code quality, design patterns, and best practices
- Check for security vulnerabilities, SQL injection risks, authentication issues
- Review documentation, comments, and API contracts
- Assess test coverage and test quality
- Evaluate architecture and SOLID principles compliance
- Generate detailed review report with actionable feedback

## When Used

- Triggered by `/review-pr <owner>/<repo> <pr-number>` command
- Supports both sync (--wait) and async (--async) modes
- Auto-detects complexity and suggests mode

## Process Phases

### Phase 1: Initialize and Fetch PR Details

**Input Parameters:**
- `owner`: Repository owner (e.g., "microsoft")
- `repo`: Repository name (e.g., "dotnet")
- `pr_number`: Pull request number (e.g., 1234)
- `report_level`: "full" or "summary"

**Actions:**
```
1. Validate GitHub MCP server is available
2. Create status file: .claude/task-status/<task-id>.md
3. Fetch PR details via GitHub MCP:
   - PR title and description
   - Author and reviewers
   - Branch information
   - Modified files list
4. Log initial setup
5. Update status: "Phase 1 - Fetching PR details (100%)"
```

**Status Output:**
```markdown
# PR Review: dotnet#1234

Status: In Progress
Phase: 1/5 - Fetching PR Details
Progress: 100%
Estimated Remaining: 8-12 minutes

## PR Information
- Title: [fetched]
- Author: [fetched]
- Reviewers: [fetched]
- Files Changed: [count]
- Additions: [+xxx]
- Deletions: [-xxx]
```

**Error Handling:**
- If GitHub MCP unavailable: Return error with fallback instruction to manually review
- If PR not found: Return clear error with valid PR format
- If authentication fails: Return error with credential check guidance

---

### Phase 2: Fetch and Analyze Code Changes

**Actions:**
```
1. For each modified file:
   a. Fetch file diff from GitHub MCP
   b. Get file extension (language detection)
   c. Read added/modified lines
   d. Store for analysis in memory
2. Categorize files by type:
   - Core logic files
   - Test files
   - Configuration files
   - Documentation files
3. Calculate change metrics:
   - Lines added/removed per file
   - Complexity of changes
   - Risk level (small, medium, high)
4. Update status: "Phase 2 - Analyzing code changes (100%)"
```

**Key Checks:**
```
For C#/ASP.NET files:
- Check for proper namespaces and file-scoped namespaces
- Verify IDisposable pattern implementation (if applicable)
- Check for proper async/await usage
- Look for var usage appropriateness
- Verify null checks and null coalescing
- Check for static method usage justification
- Verify SOLID principles compliance
- Look for pattern matching and switch expressions
- Check for LINQ usage and efficiency

For WebForms/Telerik files:
- Verify ViewState usage is minimal
- Check for proper Page_Load !IsPostBack logic
- Verify separation of business logic
- Check for proper control disposal
- Look for Telerik control best practices
- Verify encryption for sensitive query strings
- Check for proper error handling patterns

For SQL/LINQ to SQL:
- Verify query efficiency and AsNoTracking() usage
- Check for N+1 query patterns
- Look for proper transaction handling
- Verify concurrency exception handling
- Check for parameter validation
```

**Status Update:**
```markdown
## Detailed Changes

### Core Logic Files (3 files, +245 lines, -89 lines)
- UserService.cs: +145, -32 (HIGH COMPLEXITY)
- Repository.cs: +78, -45 (MEDIUM COMPLEXITY)
- Models.cs: +22, -12 (LOW COMPLEXITY)

### Test Files (2 files, +123 lines, -0 lines)
- UserServiceTests.cs: +98 (NEW TESTS)
- RepositoryTests.cs: +25 (EXTENDED)

### Risk Assessment: MEDIUM
```

---

### Phase 3: Code Quality and Architecture Review

**Security Analysis:**
```
1. Check for hardcoded credentials or secrets
2. Look for SQL injection vulnerabilities
3. Check for XSS vulnerabilities in WebForms
4. Verify authentication/authorization patterns
5. Look for insecure encryption or hashing
6. Check for command injection risks
7. Verify OWASP compliance
```

**Architecture Review:**
```
1. SOLID Principles:
   - Single Responsibility: One reason to change?
   - Open/Closed: Open for extension, closed for modification?
   - Liskov Substitution: Proper inheritance/interface usage?
   - Interface Segregation: Focused, specific interfaces?
   - Dependency Inversion: Depend on abstractions?

2. Design Patterns:
   - Repository Pattern: Proper data abstraction?
   - Service Pattern: Business logic separation?
   - Dependency Injection: Proper DI usage?
   - Factory Pattern: Used appropriately?

3. Code Organization:
   - Namespace organization correct?
   - Class responsibilities clear?
   - Method sizes reasonable (< 30 lines)?
   - Proper encapsulation?
```

**Performance Analysis:**
```
1. Memory management:
   - Proper IDisposable usage?
   - No large objects in Session/ViewState?
   - Memory leaks in event handlers?
   - Proper use of weak references?

2. Database queries:
   - N+1 query patterns?
   - AsNoTracking() for read-only?
   - Proper pagination?
   - Connection pooling?

3. Caching:
   - Proper cache invalidation?
   - Reasonable cache TTL?
   - No memory leak from cache?
```

**Status Update:**
```markdown
## Quality Assessment

### Security: ✅ PASS
- No hardcoded secrets
- No SQL injection risks
- Proper authentication checks
- XSS protection validated

### Architecture: ⚠️ REVIEW REQUIRED
- [Issue 1]: Missing interface segregation in IUserService
- [Issue 2]: Direct data access in controller code
- [Suggestion]: Extract business logic to service layer

### Performance: ✅ PASS
- No N+1 queries detected
- Proper use of AsNoTracking()
- Reasonable query patterns

### Code Quality: ✅ PASS
- Consistent naming conventions
- Proper method sizing
- Good exception handling
```

**Update status: "Phase 3 - Code quality review (100%)"`**

---

### Phase 4: Testing and Documentation Review

**Testing Analysis:**
```
1. Test coverage assessment:
   - Happy path tests?
   - Edge case tests?
   - Error condition tests?
   - Null input tests?

2. Test quality:
   - Clear test naming?
   - Single assertion principle?
   - Proper setup/teardown?
   - Mocking appropriateness?

3. Integration test coverage:
   - Database integration tests?
   - Service integration tests?
   - Cross-layer tests?
```

**Documentation Review:**
```
1. Code comments:
   - XML doc summaries on public methods?
   - Complex logic documented?
   - No obvious comments?

2. PR description:
   - Clear change description?
   - Why changes were made?
   - Testing instructions provided?
   - Breaking changes noted?

3. API documentation:
   - New endpoints documented?
   - Parameter descriptions?
   - Return value documentation?
```

**Status Update:**
```markdown
## Testing & Documentation

### Test Coverage: ⚠️ PARTIAL
- New feature has tests: ✅
- Edge cases tested: ❌ Missing null case
- Error handling tested: ✅
- Overall coverage: 87% (good)

### Documentation: ✅ COMPLETE
- XML doc comments: Present
- PR description: Clear and detailed
- Breaking changes: None identified

### Recommendations:
- Add test for null input scenario
- Add unit test for InvalidOperationException case
```

**Update status: "Phase 4 - Testing and documentation review (100%)"`**

---

### Phase 5: Generate Review Report

**Report Structure:**
```
File: marketplace/output/reviews/<repo>-pr-<number>-review.md

Contents:
1. Executive Summary
2. Key Findings
3. Risk Assessment
4. Detailed Review Comments (by file)
5. Security Assessment
6. Architecture Assessment
7. Performance Assessment
8. Testing Assessment
9. Documentation Assessment
10. Recommendations & Action Items
11. Review Checklist
12. Overall Recommendation (APPROVE/REQUEST CHANGES/COMMENT)
```

**Report Template:**
```markdown
# PR Review: [owner]/[repo]#[number]

## Executive Summary

**PR Title**: [title]
**Author**: [author]
**Status**: [APPROVE | REQUEST CHANGES | COMMENT]
**Complexity**: [LOW | MEDIUM | HIGH]
**Overall Risk**: [LOW | MEDIUM | HIGH]

**Summary**: [2-3 sentence summary of changes and assessment]

## Key Findings

### ✅ Strengths
- [Strength 1 with brief explanation]
- [Strength 2]

### ⚠️ Issues Requiring Changes
- [Issue 1: Description and location]
- [Issue 2: Description and location]

### 💡 Suggestions for Improvement
- [Suggestion 1]
- [Suggestion 2]

## Risk Assessment

| Category | Risk Level | Details |
|----------|-----------|---------|
| Security | LOW | No vulnerabilities detected |
| Architecture | MEDIUM | Minor pattern violation in UserService |
| Performance | LOW | Queries optimized |
| Breaking Changes | LOW | No breaking changes |
| Database | LOW | Schema changes backward compatible |

## Detailed File Reviews

### File: [filename]
**Changes**: +45 lines, -12 lines
**Risk**: [LOW/MEDIUM/HIGH]

**Issues Found**:
1. [Issue with code reference and suggestion]
2. [Issue with code reference and suggestion]

**Strengths**:
1. [What the code does well]

---

[Continue for each file]

## Security Assessment

✅ **PASS**
- No SQL injection risks identified
- XSS protection properly implemented
- Authentication checks in place
- No hardcoded secrets

## Architecture Assessment

⚠️ **REVIEW REQUIRED**
- Interface segregation could be improved
- Consider extracting to service layer
- SOLID principles mostly followed

## Performance Assessment

✅ **PASS**
- Database queries optimized
- No N+1 patterns detected
- Memory usage appropriate
- Async patterns correct

## Testing Assessment

✅ **COMPLETE**
- New tests for features
- Edge cases covered
- Test quality good

## Documentation Assessment

✅ **COMPLETE**
- XML doc comments present
- PR description clear
- Breaking changes documented

## Recommendations & Action Items

### Before Merge
1. [ ] Add test for null input validation
2. [ ] Add XML doc comment to public method
3. [ ] Review interface design with architect

### Nice to Have
1. [ ] Consider caching strategy for expensive operation
2. [ ] Add performance benchmark comments

## Review Checklist

- [x] Code follows C# standards
- [x] SOLID principles applied
- [x] Exception handling proper
- [x] Tests included
- [x] Documentation complete
- [x] No security vulnerabilities
- [x] Performance acceptable
- [x] No memory leaks
- [x] Proper async/await usage
- [x] Proper disposal patterns

## Overall Recommendation

**STATUS: ✅ APPROVE**

This PR improves the system's user service with proper abstraction and good test coverage. Minor suggestions provided but no blocking issues. Safe to merge.

---

**Review Completed**: [timestamp]
**Review Time**: [X minutes]
**Reviewer**: Claude Code PR Comprehensive Reviewer Agent
```

**Actions:**
```
1. Generate comprehensive report using template
2. Save to: marketplace/output/reviews/<repo>-pr-<number>-review.md
3. Create summary version if --report=summary requested
4. Update status file: "Phase 5 - Report generation (100%)"
5. Return final status with report location
```

---

### Phase 6: Final Status and Completion

**Status Output:**
```markdown
# PR Review Complete: dotnet#1234

Status: ✅ COMPLETED
Overall Recommendation: APPROVE
Review Time: 12 minutes 34 seconds

## Summary
- Files Reviewed: 5
- Issues Found: 2 minor
- Recommendations: 3
- Security: ✅ PASS
- Architecture: ✅ PASS

## Report Location
`marketplace/output/reviews/dotnet-pr-1234-review.md`

## Key Recommendations
1. Add test case for null scenario
2. Improve interface segregation

---

Generated: 2025-10-30 15:45:12 UTC
```

**Completion Actions:**
```
1. Mark task as complete in task queue
2. Update status file with final results
3. For async: Return task completion message
4. For sync: Display full report to user
5. Log completion metrics
```

---

## Error Handling & Recovery

### Scenario 1: GitHub MCP Unavailable
```
Status: ⚠️ PARTIAL - MCP UNAVAILABLE
Message: "GitHub MCP server unavailable. Some features will be limited."

Fallback Actions:
1. Inform user of unavailable MCP
2. Provide manual review checklist
3. Suggest alternative: manual review using provided checklist
```

### Scenario 2: Large PR (>1000 lines changed)
```
Detection: "PR exceeds complexity threshold (1000+ lines)"
Recommendation: "Use --async flag for thorough analysis"
Auto-Mode: Switch to async if sync requested
```

### Scenario 3: PR Not Found
```
Error: "PR not found: invalid owner/repo/number"
Help Text: "Expected format: /review-pr owner/repo <number>"
Example: "/review-pr microsoft/dotnet 1234"
```

### Scenario 4: API Rate Limiting
```
Error: "GitHub API rate limit exceeded"
Retry: Schedule for retry after rate limit reset
Status: "Queued for retry at [timestamp]"
Task ID: [provided for status checking]
```

---

## Review Standards Applied

This agent follows the PR Review Standards from CLAUDE.md:

### Critical Priorities (Review Order)
1. **Security Vulnerabilities** – SQL injection, XSS, auth bypass, hardcoded secrets
2. **Breaking Changes** – API compatibility, interface modifications, database schema
3. **Performance Regressions** – N+1 queries, memory leaks, inefficient async
4. **Integration Risks** – External service calls, transaction boundaries, dependencies
5. **Error Handling Gaps** – Missing exception handling, logging, rollback issues

### Review Context Requirements
- Complete context review, not just changed lines
- Entire method signature, parameters, locals, returns, control flow
- Trace all callers of modified methods
- Analyze impact on class invariants and encapsulation
- Follow data flow from input → transformations → output
- Check thread safety, async/await correctness, deadlock risks

### Domain-Specific Areas
- **Memory Management**: IDisposable pattern, disposal, Session/ViewState, LOH usage
- **ASP.NET WebForms**: Lifecycle, ViewState, postback flow, Session, Telerik controls
- **Repository & Service**: UnitOfWork, async methods, AsNoTracking(), concurrency
- **Architecture**: SOLID principles, DI, async flows, request/response performance

---

## Command Integration

This agent is invoked by:
```
/review-pr <owner>/<repo> <pr-number> [--async|--wait] [--report=full|summary]

Examples:
/review-pr microsoft/dotnet 12345 --wait
/review-pr anthropics/claude-code 567 --async --report=full
/review-pr my-org/my-repo 890 --report=summary
```

Command delegates all execution to this agent via background task coordinator.

---

## Output Locations

**Full Reviews**: `marketplace/output/reviews/<repo>-pr-<number>-review.md`
**Summary Reviews**: `marketplace/output/reviews/<repo>-pr-<number>-summary.md`
**Status Files**: `.claude/task-status/<task-id>.md`

---

**Agent Version**: 2.0.0
**Last Updated**: 2026-01-15
**Task Coverage**: Task #3 (Review PRs on GitHub)
**Sequential Thinking**: Conditional
**Skills**: code-review-best-practices, performance-analysis-framework
