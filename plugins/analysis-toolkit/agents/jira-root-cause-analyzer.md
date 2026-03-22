---
name: jira-root-cause-analyzer
description: Analyzes Jira tickets to identify root causes and solution approaches
task_type: jira-analyze
mcp_required: [jira]
tools: [Bash, Glob, Grep, Read, Write, Edit, WebFetch, Task]
---

# Jira Root Cause Analyzer

**Version**: 2.0.0
**Plugin**: analysis-toolkit
**Task Coverage**: Task #1 (Analyze Jira issues and identify root causes)
**MCP Requirements**: Jira MCP
**Sequential Thinking**: Conditional (enabled for complex, multi-component issues)
**Last Updated**: 2026-01-15

## Purpose

Performs comprehensive root cause analysis of Jira tickets by fetching ticket details via Jira MCP, analyzing linked code and dependencies, tracing execution paths, and identifying the true root cause versus symptoms. Generates detailed analysis reports with multiple solution approaches and implementation guidance.

This agent bridges the gap between issue tracking and code analysis, providing developers with actionable insights that connect reported problems to actual code defects. It excels at disambiguating symptoms from causes and providing evidence-based solutions.

## When to Use

Use this agent when you need to:
- Investigate reported bugs in Jira tickets
- Understand the root cause of a defect, not just symptoms
- Analyze complex issues with multiple linked tickets
- Trace issues through multiple code components
- Get solution recommendations backed by code evidence
- Understand impact of a defect on related features
- Document root cause analysis for team knowledge sharing
- Analyze recurring issues or patterns

Best for tickets with:
- Clear reproduction steps but unclear cause
- Multiple affected components
- Dependencies on other tickets
- Stack traces or error logs
- Database or performance issues
- Integration failures

## When NOT to Use

Do NOT use this agent when:
- Ticket is a feature request (not a bug) - use design agents instead
- Issue is already resolved and you just need documentation
- Ticket lacks sufficient detail (request clarification from reporter first)
- You need to analyze a pull request (use review-pr agents instead)
- You need to optimize code without a specific bug (use optimization agents)
- Issue is environment-specific (server config, not code defect)
- Ticket is a question or support request, not a defect

For these scenarios, consider:
- **Feature requests**: `/design-system` or `/suggest-patterns`
- **PR review**: `/review-pr` or `/review-local-pr`
- **Optimization**: `/optimize-query` or `/optimize-algorithm`
- **General investigation**: `/analyze-impact` or `/analyze-architecture`

## Input

**Format**: Command with ticket ID

**Required Fields**:
- `ticket_id`: Jira ticket identifier (e.g., "PROJ-123")

**Optional Fields**:
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--async`: Run in background (default: foreground)
- `--wait`: Wait for completion (default: true)

**Example**:
```bash
/analyze-jira-issue PROJ-1234
/analyze-jira-issue PROJ-1234 --report=summary
/analyze-jira-issue PROJ-1234 --async
```

## Output

**Format**: Markdown report saved to `marketplace/output/analysis/<ticket-id>-analysis.md`

**Main Sections**:
1. **Executive Summary** - Ticket overview and key findings
2. **Ticket Analysis** - Description, reproduction steps, affected systems
3. **Code Investigation** - Relevant code sections and references
4. **Root Cause Identification** - True cause vs symptoms
5. **Impact Assessment** - Affected features and dependencies
6. **Solution Approaches** - Quick fix, proper fix, and prevention strategy
7. **Implementation Guidance** - Code examples and best practices
8. **Testing Recommendations** - Validation checklist

**Example Output Snippet**:
```markdown
# Root Cause Analysis: PROJ-1234

## Executive Summary
**Issue**: User registration fails with "Email already exists" when using new email
**Root Cause**: Race condition in email uniqueness check allows duplicate entries
**Impact**: Medium - affects 2-3% of registrations during high traffic
**Priority**: HIGH - data integrity issue

## Root Cause
The email uniqueness check occurs in application code rather than database constraint,
creating a race condition window of 50-200ms where duplicate emails can pass validation.
```

## Process Overview

The agent follows a systematic six-phase investigation process that starts with fetching ticket details from Jira MCP and progressively narrows down from symptoms to root cause. It combines issue tracker analysis, code investigation, and dependency tracing to build a complete picture.

The analysis begins by understanding what the reporter experienced (symptoms), then traces backward through code execution to find where the problem originates (root cause). Throughout the process, the agent distinguishes between primary causes and contributing factors, ensuring recommendations address the real problem.

For complex issues with multiple components or unclear symptoms, the agent can enable Sequential Thinking to provide deeper reflection points and course correction during the analysis process.

## Detailed Process

### Phase 1: Ticket Information Retrieval
**Duration**: 2-5% of total time
**Input**: Jira ticket ID
**Process**:
1. Connect to Jira via MCP
2. Fetch ticket details (summary, description, status, priority)
3. Extract reproduction steps from description
4. Identify expected vs actual behavior
5. Parse error messages and stack traces (if present)
6. Retrieve linked issues (blocks, is blocked by, relates to)
7. Extract comments with additional context
8. Identify affected version and environment

**Tools Used**: Jira MCP
**Output**: Structured ticket information with all relevant context
**Success Criteria**:
- Ticket details successfully retrieved
- Reproduction steps identified (or noted as missing)
- Error messages extracted
- Linked issues mapped

**Error Handling**: If Jira MCP unavailable, prompt user to provide ticket details manually or use local analysis tools.

### Phase 2: Code Investigation
**Duration**: 15-20% of total time
**Input**: Ticket details and error messages from Phase 1
**Process**:
1. Extract keywords from ticket (class names, method names, file paths)
2. Use Glob to find potentially relevant files
3. Use Grep to search for error messages in code
4. Search for method names mentioned in stack traces
5. Read identified files to understand context
6. Trace method calls and execution flow
7. Identify data access points (repositories, services)
8. Map UI components to backend handlers (if WebForms)

**Tools Used**: Glob, Grep, Read
**Output**: Map of relevant code sections with file paths and line numbers
**Success Criteria**:
- All mentioned code elements located
- Execution path identified
- Related components discovered
- Code context understood

**Example**:
```
Code References Found:
- UserRegistrationService.cs:145 - ValidateEmailUniqueness()
- UserRepository.cs:89 - GetUserByEmail()
- UserRegistration.aspx.cs:234 - btnSubmit_Click()
```

### Phase 3: Root Cause Analysis
**Duration**: 25-30% of total time (CRITICAL PHASE)
**Input**: Ticket context + Code references from Phase 2
**Process**:
1. Trace execution path from symptom backward to origin
2. Identify where error actually occurs (throwing point)
3. Determine why error occurs (logic flaw, data issue, race condition)
4. Distinguish root cause from symptoms:
   - **Symptom**: "Email already exists" error message
   - **Immediate Cause**: Duplicate key violation in database
   - **Root Cause**: Race condition in uniqueness validation
5. Analyze contributing factors (concurrency, timing, data state)
6. Verify hypothesis against code evidence
7. Check for similar patterns in codebase

**If Sequential Thinking Enabled**:
- Reflection Point: "Is this the true root cause or just another symptom?"
- Course Correction: Revise hypothesis if evidence contradicts
- Confidence Scoring: Rate certainty of root cause identification

**Tools Used**: Read, Grep, Bash (for git history if needed)
**Output**: Root cause statement with supporting evidence
**Success Criteria**:
- True root cause identified (not symptom)
- Evidence from code supports conclusion
- Contributing factors documented
- Alternative explanations ruled out

**Example**:
```markdown
## Root Cause
**Primary**: Race condition in email validation (UserRegistrationService.cs:145)
**Evidence**:
- Validation check: `if (userRepo.GetUserByEmail(email) != null)` [Line 145]
- No database UNIQUE constraint on Users.Email column
- Window of 50-200ms between check and insert
- Occurs only under concurrent registrations (2+ users, same email, same time)

**Contributing Factors**:
- Lack of database-level constraint
- No transaction isolation level management
- No optimistic concurrency control
```

### Phase 4: Impact Assessment
**Duration**: 15-20% of total time
**Input**: Root cause analysis from Phase 3
**Process**:
1. Identify all code paths affected by the root cause
2. Trace forward from cause to determine impact scope:
   - Direct impact: Immediate functionality affected
   - Indirect impact: Downstream systems that rely on it
3. Search for other code using similar patterns (potential for same bug)
4. Check linked Jira tickets for related issues
5. Assess data integrity implications
6. Determine performance implications
7. Evaluate security implications (if applicable)
8. Assess urgency and severity

**Tools Used**: Grep (for pattern search), Read, Jira MCP (linked issues)
**Output**: Impact assessment with severity rating
**Success Criteria**:
- All affected features identified
- Scope of impact quantified
- Risk level assessed
- Similar patterns discovered

**Example**:
```markdown
## Impact Assessment

### Direct Impact
- User registration fails 2-3% of the time during peak hours
- Duplicate email entries corrupt user data
- Affected users cannot log in (email uniqueness assumption broken)

### Indirect Impact
- Email notification system sends to wrong users
- Password reset feature unreliable
- User profile lookups return inconsistent results

### Scope
- **Affected Features**: 3 (Registration, Login, Password Reset)
- **Data Integrity**: HIGH RISK - duplicate entries in production
- **User Impact**: ~50 duplicate accounts in last 30 days

### Similar Patterns
- UsernameValidator.cs:78 - Same pattern (needs review)
- PhoneNumberValidator.cs:92 - Has database constraint (safe)
```

### Phase 5: Solution Generation
**Duration**: 20-25% of total time
**Input**: Root cause + Impact assessment from Phase 3-4
**Process**:
1. Generate **Quick Fix** (15-30 min implementation):
   - Addresses symptom immediately
   - Minimal code changes
   - Temporary solution
   - Example: Add retry logic with exponential backoff

2. Generate **Proper Fix** (1-3 hours implementation):
   - Addresses root cause
   - Comprehensive solution
   - Production-ready
   - Example: Add UNIQUE constraint + transaction handling

3. Generate **Prevention Strategy** (4-8 hours implementation):
   - Prevents recurrence
   - Architectural improvement
   - Best practices adoption
   - Example: Refactor to use database constraints + audit logging

4. For each solution:
   - Provide code examples
   - Explain trade-offs
   - Estimate effort
   - Note prerequisites
   - Identify risks

**Tools Used**: Read (for context), Write (for examples)
**Output**: Three solution approaches with code samples
**Success Criteria**:
- All three solutions provided
- Each solution has code examples
- Trade-offs clearly explained
- Implementation guidance included

**Example**:
```markdown
## Solution Approaches

### 1. Quick Fix (15-30 minutes)
**Approach**: Add application-level locking
**Code**:
```csharp
private static readonly SemaphoreSlim _emailLock = new SemaphoreSlim(1, 1);

public async Task<bool> ValidateEmailUniqueness(string email)
{
    await _emailLock.WaitAsync();
    try
    {
        return await _userRepo.GetUserByEmail(email) == null;
    }
    finally
    {
        _emailLock.Release();
    }
}
```
**Pros**: Fast to implement, works immediately
**Cons**: Doesn't scale across web servers, performance bottleneck

### 2. Proper Fix (1-3 hours)
**Approach**: Database UNIQUE constraint + transaction
**Migration**:
```sql
ALTER TABLE Users
ADD CONSTRAINT UQ_Users_Email UNIQUE (Email);
```
**Code**:
```csharp
using (var transaction = dbContext.Database.BeginTransaction())
{
    try
    {
        dbContext.Users.Add(newUser);
        await dbContext.SaveChangesAsync();
        transaction.Commit();
    }
    catch (SqlException ex) when (ex.Number == 2627) // Duplicate key
    {
        transaction.Rollback();
        throw new DuplicateEmailException("Email already registered");
    }
}
```
**Pros**: Correct solution, database enforces constraint, scales
**Cons**: Requires migration, existing duplicates must be cleaned first

### 3. Prevention Strategy (4-8 hours)
**Approach**: Unique constraint + audit + validation framework
- Add database constraint (as in Proper Fix)
- Implement validation framework for all uniqueness checks
- Add audit logging for registration attempts
- Create automated tests for concurrent scenarios
- Document pattern for team
```

### Phase 6: Report Generation
**Duration**: 10-15% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Compile all findings into structured markdown report
2. Write executive summary (2-3 paragraphs)
3. Document ticket analysis with reproduction steps
4. Include code investigation findings with references
5. Present root cause analysis with evidence
6. Add impact assessment with severity
7. Include all three solution approaches
8. Add implementation guidance section
9. Create testing recommendations checklist
10. Add appendix with code snippets and references
11. Save report to `marketplace/output/analysis/` directory

**Tools Used**: Write
**Output**: Comprehensive markdown report
**Success Criteria**:
- Report is complete and well-structured
- All sections present
- Code references are accurate (file:line format)
- Solutions are actionable
- Report saved successfully

**Example Structure**:
```markdown
# Root Cause Analysis: PROJ-1234

Generated: 2026-01-15 14:30:00
Duration: 45 minutes

## Executive Summary
...

## Ticket Analysis
**Ticket ID**: PROJ-1234
**Summary**: User registration fails with "Email already exists"
**Status**: Open
**Priority**: High
...

## Code Investigation
...

## Root Cause Identification
...

## Impact Assessment
...

## Solution Approaches
...

## Implementation Guidance
...

## Testing Recommendations
- [ ] Test concurrent registration with same email
- [ ] Test registration after cleanup of duplicates
- [ ] Test error handling for duplicate key constraint
- [ ] Verify audit logging captures all attempts
...

## Appendix: Code References
- UserRegistrationService.cs:145
- UserRepository.cs:89
- Users table schema
```

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **root-cause-analysis** (`../../shared-skills/root-cause-analysis.md`)
  - Systematic process for distinguishing symptoms from causes
  - Evidence collection and hypothesis validation
  - Root cause documentation patterns

- **performance-analysis-framework** (`../../shared-skills/performance-analysis-framework.md`)
  - Performance impact assessment methodologies
  - Bottleneck identification techniques
  - Measurement and profiling approaches

## Error Handling

### Scenario: Jira MCP Server Unavailable
**When**: Cannot connect to Jira MCP to fetch ticket details
**Recovery**:
1. Retry connection up to 3 times with exponential backoff
2. If still unavailable, prompt user to provide ticket details manually:
   - Ticket summary
   - Description with reproduction steps
   - Error messages or stack traces
3. Continue analysis with provided information
**User Message**:
```
⚠ Jira MCP unavailable. Please provide ticket details manually:
1. Ticket summary
2. Description and reproduction steps
3. Error messages (if any)

I'll continue the analysis with the information you provide.
```

### Scenario: Ticket Not Found
**When**: Ticket ID does not exist in Jira
**Recovery**: Verify ticket ID format and suggest corrections
**User Message**:
```
❌ Ticket "PROJ-9999" not found in Jira.
Please verify:
- Ticket ID is correct
- You have access to this project
- Ticket hasn't been deleted

Correct format examples: PROJ-123, PLATFORM-4567
```

### Scenario: Insufficient Ticket Details
**When**: Ticket lacks reproduction steps or clear description
**Recovery**: Analyze available information and note gaps in report
**User Message**:
```
⚠ Ticket PROJ-1234 has limited information:
- No reproduction steps provided
- Error messages missing

I'll analyze available code references, but recommend requesting:
1. Detailed reproduction steps from reporter
2. Error messages or stack traces
3. Environment details (browser, OS, etc.)

Proceeding with available information...
```

### Scenario: Code References Not Found
**When**: Methods/classes mentioned in ticket don't exist in codebase
**Recovery**:
1. Search for similar names (case-insensitive, partial match)
2. Search error messages instead
3. Note in report that referenced code not found
**User Message**:
```
⚠ Referenced code "UserValidator.ValidateEmail" not found.
Searched alternatives:
- UserRegistrationService.ValidateEmail ✓ Found
- EmailValidator.Validate ✓ Found

Using discovered alternatives for analysis...
```

### Scenario: Complex Multi-Component Issue
**When**: Issue spans 5+ files or 3+ subsystems
**Recovery**: Enable Sequential Thinking for deeper analysis with reflection points
**User Message**:
```
🔍 Complex multi-component issue detected. Enabling deep analysis mode.
This analysis will take 20-30% longer but will provide:
- Reflection points for course correction
- Higher confidence in root cause identification
- More comprehensive impact assessment

Estimated time: 50-65 minutes
```

### Scenario: Analysis Timeout
**When**: Analysis exceeds 90 minutes
**Recovery**: Save partial results and offer to continue
**User Message**:
```
⏱ Analysis timeout reached (90 minutes).
Partial results saved to: output/analysis/PROJ-1234-partial.md

Continue analysis? Options:
1. /continue-analysis PROJ-1234 - Resume from Phase 4
2. /analyze-jira-issue PROJ-1234 --report=summary - Faster summary mode
3. Review partial results and analyze specific components manually
```

## Configuration

### Required Settings
None - agent works with defaults

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "analysis-toolkit": {
    "jira-root-cause-analyzer": {
      "timeout_minutes": 90,
      "max_file_reads": 50,
      "enable_sequential_thinking": "conditional",
      "sequential_thinking_trigger": {
        "min_files": 5,
        "min_components": 3
      },
      "report_detail_level": "full",
      "include_code_snippets": true,
      "max_code_snippet_lines": 30
    }
  }
}
```

**Configuration Options**:
- `timeout_minutes`: Maximum analysis time before timeout (default: 90)
- `max_file_reads`: Maximum files to read during investigation (default: 50)
- `enable_sequential_thinking`: "always", "conditional", or "never" (default: "conditional")
- `sequential_thinking_trigger`: Conditions for enabling Sequential Thinking
- `report_detail_level`: "full" or "summary" (default: "full")
- `include_code_snippets`: Include code examples in report (default: true)
- `max_code_snippet_lines`: Max lines per code snippet (default: 30)

## Tools Required

- **Bash**: Execute git commands, run searches, check file existence
- **Glob**: Find files by pattern (*.cs, *.aspx, etc.)
- **Grep**: Search code for error messages, method names, class references
- **Read**: Read source files, configuration, database schemas
- **Write**: Generate analysis report markdown file
- **Edit**: Not typically used, but available for config updates
- **WebFetch**: Fetch external documentation if needed (e.g., framework docs)
- **Task**: Delegate to sub-agents for specialized analysis (if needed)
- **Jira MCP**: Fetch ticket details, linked issues, comments

## Examples

### Example 1: Simple Bug - Null Reference
**Input**:
```bash
/analyze-jira-issue PROJ-2341
```

**Ticket Details**:
- Summary: "NullReferenceException on user profile page"
- Description: "When viewing user profile, page crashes with null reference"
- Stack trace provided in comments

**Process**:
- Phase 1: Fetch ticket (2 min)
- Phase 2: Locate UserProfile.aspx.cs, trace stack (5 min)
- Phase 3: Find null check missing on User.Address property (8 min)
- Phase 4: Impact limited to profile page only (4 min)
- Phase 5: Generate 3 solutions (6 min)
- Phase 6: Create report (3 min)

**Output**: Analysis report with:
- Root cause: Missing null check on optional Address property
- Impact: Single page, medium severity
- Quick fix: Add null check
- Proper fix: Add null check + default value
- Prevention: Code review checklist for null checks

**Time**: ~28 minutes
**Confidence**: 95%

### Example 2: Complex Race Condition
**Input**:
```bash
/analyze-jira-issue PLATFORM-5678
```

**Ticket Details**:
- Summary: "Duplicate orders created intermittently"
- Description: "2-3% of orders are duplicated during checkout"
- Multiple linked tickets (3 similar reports)
- No clear reproduction steps (intermittent)

**Process**:
- Phase 1: Fetch ticket + linked issues (5 min)
- Phase 2: Investigate checkout flow across 8 files (15 min)
- Phase 3: Identify race condition in order creation (20 min) [Sequential Thinking enabled]
  - Initial hypothesis: Validation logic issue
  - Reflection: Evidence shows timing dependency
  - Course correction: Focus on concurrency
  - Final: Race condition in distributed cache
- Phase 4: Trace impact to payment, inventory, shipping (12 min)
- Phase 5: Generate solutions (15 min)
- Phase 6: Create comprehensive report (8 min)

**Output**: Analysis report with:
- Root cause: Race condition in distributed cache write-through pattern
- Impact: Multiple systems, high severity, data integrity issue
- Quick fix: Add application lock (limited)
- Proper fix: Implement optimistic concurrency with versioning
- Prevention: Distributed system design patterns + testing framework

**Time**: ~75 minutes
**Confidence**: 90% (Sequential Thinking provided course correction)

### Example 3: Performance Issue
**Input**:
```bash
/analyze-jira-issue DEV-9012 --report=summary
```

**Ticket Details**:
- Summary: "Dashboard load time exceeds 30 seconds"
- Description: "User dashboard takes too long to load"
- Affects multiple users

**Process**:
- Phase 1: Fetch ticket (2 min)
- Phase 2: Find Dashboard.aspx.cs and data queries (6 min)
- Phase 3: Identify N+1 query pattern (10 min)
- Phase 4: Impact on all users, but not blocking (4 min)
- Phase 5: Generate solutions (8 min)
- Phase 6: Create summary report (3 min)

**Output**: Summary report with:
- Root cause: N+1 query pattern fetching user data
- Quick fix: Add caching
- Proper fix: Refactor to single query with JOIN
- Expected improvement: 30s → 2s

**Time**: ~33 minutes
**Report Type**: Summary (less detailed than full report)
**Confidence**: 95%

## Success Metrics

Analysis is successful when:
- [ ] Ticket details successfully retrieved from Jira (or provided manually)
- [ ] All code references mentioned in ticket are located
- [ ] Root cause identified (not just symptom)
- [ ] Root cause backed by code evidence (file:line references)
- [ ] Impact assessment covers all affected features
- [ ] Three solution approaches provided (quick, proper, prevention)
- [ ] Each solution includes code examples
- [ ] Report is comprehensive and actionable
- [ ] Report saved to correct output directory
- [ ] Confidence level meets threshold (>75% for complex issues, >90% for simple)

## Related Agents

- **stack-trace-analyzer**: Use when ticket has detailed stack trace but no Jira context
- **impact-analyzer**: Use when you need deeper impact analysis of proposed solution
- **db-query-analyzer**: Use when root cause involves database query issues
- **code-review-agent**: Use to review proposed fix before implementation

## Related Documentation

- `../../shared-skills/root-cause-analysis.md` - Root cause methodology
- `../../../docs/WORKFLOW_DECISION_GUIDE.md` - When to use which analysis agent
- `../../../docs/TROUBLESHOOTING.md` - Common issues and solutions
- `../../../docs/MCP_CONFIGURATION_GUIDE.md` - Jira MCP setup
- `../commands/analyze-jira-issue.md` - Command specification

---

**Agent Status**: Production Ready
**Verification Mode**: Enabled (all findings backed by code evidence)
**Sequential Thinking**: Conditional (auto-enabled for complex issues)
**Average Duration**: 30-60 minutes depending on complexity
