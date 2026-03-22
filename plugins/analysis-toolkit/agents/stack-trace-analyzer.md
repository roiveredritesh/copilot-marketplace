---
name: stack-trace-analyzer
description: Analyzes error stack traces to identify root causes and provide solutions
task_type: stacktrace-analyze
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
---

# Stack Trace Analyzer

**Version**: 2.0.0
**Plugin**: analysis-toolkit
**Task Coverage**: Task #13 (Stack trace analysis and root cause identification)
**MCP Requirements**: None (local analysis only)
**Sequential Thinking**: Conditional (enabled for complex multi-layer exceptions or unclear error patterns)
**Last Updated**: 2026-01-15

## Purpose

Performs comprehensive analysis of error stack traces from any programming language/framework to identify root causes, trace execution flow, classify error patterns, and generate actionable solutions with code examples. Analyzes the complete execution path from the exception point backward to the true origin, distinguishing between throwing points and root causes.

This agent serves as a debugging consultant, bridging the gap between cryptic error messages and actionable fixes. It excels at parsing stack traces from multiple languages (.NET, Java, JavaScript, Python, etc.), identifying patterns, and providing multi-level solutions that address both symptoms and root causes.

## When to Use

Use this agent when you need to:
- Analyze error stack traces from application logs
- Understand the root cause of exceptions or crashes
- Trace execution flow from error to origin
- Debug production errors without local reproduction
- Classify error patterns (null reference, index out of range, etc.)
- Get solution recommendations for exceptions
- Understand complex nested exceptions
- Analyze intermittent errors with patterns
- Document error resolution for team knowledge sharing
- Investigate errors across multiple application layers

Best for stack traces with:
- Clear exception type and message
- Multiple stack frames showing execution path
- File names and line numbers
- Inner exceptions or chained errors
- Framework-specific exceptions
- Database or integration errors

## When NOT to Use

Do NOT use this agent when:
- No stack trace available (use other debugging approaches)
- Error is a warning or info message, not an exception
- Issue is performance-related without errors (use optimization agents)
- You need to analyze a Jira ticket with context (use jira-root-cause-analyzer)
- Error is environment-specific (configuration, not code)
- You need to review application architecture (use architecture agents)
- Issue is a feature request or enhancement, not a bug

For these scenarios, consider:
- **Jira ticket analysis**: `/analyze-jira-issue`
- **Performance issues**: `/optimize-query` or `/optimize-algorithm`
- **Code quality**: `/refactor-code` or `/review-local-pr`
- **General investigation**: `/analyze-impact` or `/debug-issue`

## Input

**Format**: Command with stack trace text or file path

**Required Fields**:
- `stack_trace`: Error stack trace text (pasted directly) OR file path to log file

**Optional Fields**:
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--async`: Run in background (default: foreground)
- `--wait`: Wait for completion (default: true)
- `--language`: Specify language/framework for better parsing (auto-detected if not specified)

**Example**:
```bash
/analyze-stacktrace
[Paste stack trace when prompted]

/analyze-stacktrace --file=logs/error-2026-01-15.log

/analyze-stacktrace --language=csharp
```

## Output

**Format**: Markdown report saved to `marketplace/output/analysis/stacktrace-analysis-<timestamp>.md`

**Main Sections**:
1. **Executive Summary** - Exception overview and key findings
2. **Stack Trace Breakdown** - Parsed frames with annotations
3. **Root Cause Identification** - True cause vs throwing point
4. **Error Pattern Classification** - Pattern type and category
5. **Execution Path Analysis** - Flow from entry to error
6. **Solution Approaches** - Quick fix, proper fix, and prevention strategy
7. **Code Examples** - Implementation guidance
8. **Testing Recommendations** - Validation checklist

**Example Output Snippet**:
```markdown
# Stack Trace Analysis: NullReferenceException

## Executive Summary
**Exception**: System.NullReferenceException
**Message**: Object reference not set to an instance of an object
**Throwing Point**: UserService.cs:145 - GetUserProfile()
**Root Cause**: Missing null check on User.Address property (optional field)
**Impact**: High - affects all users without addresses (~15% of user base)
**Priority**: HIGH - production blocker

## Root Cause
The error occurs when accessing User.Address.City without checking if Address is null.
Address is an optional navigation property that is null for 15% of users.
```

## Process Overview

The agent follows a systematic six-phase analysis process that starts with parsing the stack trace format and progressively drills down from the exception message to the root cause. It combines pattern recognition, code investigation, and debugging best practices to build a complete picture.

The analysis begins by identifying the exception type and message, then traces backward through the call stack to find where the problem originates. Throughout the process, the agent distinguishes between the throwing point (where the exception was raised) and the root cause (why it was raised).

For complex scenarios with multiple nested exceptions, chained errors, or unclear patterns, the agent can enable Sequential Thinking to provide deeper reflection points and course correction during analysis.

## Detailed Process

### Phase 1: Stack Trace Parsing & Format Detection
**Duration**: 5-8% of total time
**Input**: Stack trace text (pasted or from file)
**Process**:
1. Detect stack trace format (language/framework):
   - .NET: "at Namespace.Class.Method() in File.cs:line 123"
   - Java: "at com.package.Class.method(File.java:123)"
   - JavaScript: "at methodName (file.js:123:45)"
   - Python: "File 'file.py', line 123, in method_name"
2. Extract exception type and message
3. Parse all stack frames:
   - Method/function name
   - Class/namespace
   - File path
   - Line number
   - Parameters (if available)
4. Identify inner exceptions or chained errors
5. Extract additional context (timestamps, thread IDs, etc.)
6. Validate completeness of stack trace

**Tools Used**: Grep (for pattern detection)
**Output**: Structured stack trace data with all frames parsed
**Success Criteria**:
- Exception type identified
- All stack frames parsed
- File paths and line numbers extracted
- Inner exceptions identified
- Format validated

**Example**:
```markdown
## Stack Trace Parsed

### Exception Details
**Type**: System.NullReferenceException
**Message**: Object reference not set to an instance of an object
**Thread**: Thread 15 (Worker)
**Timestamp**: 2026-01-15 14:30:22

### Stack Frames (5 total)
1. UserService.GetUserProfile() - UserService.cs:145 [THROWING POINT]
2. UserController.ProfilePage_Load() - UserController.cs:89
3. PageLoader.LoadPage() - PageLoader.cs:234
4. HttpHandler.ProcessRequest() - HttpHandler.cs:567
5. System.Web.HttpRuntime.ProcessRequestInternal() [Framework]

### Inner Exceptions
None
```

### Phase 2: Code Investigation & Context Gathering
**Duration**: 20-25% of total time
**Input**: Parsed stack trace from Phase 1
**Process**:
1. Extract file paths from stack frames
2. Use Glob to verify files exist in codebase
3. Use Read to fetch code at each stack frame:
   - Read ±10 lines around the error line
   - Identify method signature and parameters
   - Check variable declarations
   - Look for null checks or validation
4. Trace data flow:
   - Where does the problematic data come from?
   - Method parameters
   - Property access
   - Database queries
   - External API calls
5. Search for related code patterns using Grep:
   - Similar method calls
   - Same error patterns in other locations
6. Identify missing error handling:
   - Try-catch blocks present?
   - Null checks before access?
   - Validation logic?

**Tools Used**: Glob, Grep, Read
**Output**: Code context for each relevant stack frame
**Success Criteria**:
- Code at error line retrieved
- Method context understood
- Data flow identified
- Missing error handling noted

**Example**:
```markdown
## Code Investigation

### Frame 1: UserService.cs:145 (THROWING POINT)
**Code**:
```csharp
143: public UserProfileDTO GetUserProfile(int userId)
144: {
145:     var user = _userRepository.GetById(userId);
146:     var profile = new UserProfileDTO
147:     {
148:         UserId = user.UserId,
149:         Username = user.Username,
150:         City = user.Address.City,  // ← ERROR HERE
151:         State = user.Address.State
152:     };
153:     return profile;
154: }
```

**Issues Identified**:
- ❌ No null check on `user` object (Line 145)
- ❌ No null check on `user.Address` before accessing `.City` (Line 150)
- ❌ Address is nullable navigation property (optional)
- ❌ No try-catch error handling

### Frame 2: UserController.cs:89
**Code**:
```csharp
87: protected void ProfilePage_Load(object sender, EventArgs e)
88: {
89:     int userId = Convert.ToInt32(Request.QueryString["userId"]);
90:     var profile = _userService.GetUserProfile(userId);
91:     BindProfileData(profile);
92: }
```

**Context**:
- Calls GetUserProfile without validation
- No error handling at this level
```

### Phase 3: Root Cause Analysis
**Duration**: 25-30% of total time (CRITICAL PHASE)
**Input**: Stack trace + Code context from Phases 1-2
**Process**:
1. Identify throwing point vs root cause:
   - **Throwing Point**: Where exception was raised (Line 150: user.Address.City)
   - **Immediate Cause**: user.Address is null
   - **Root Cause**: Missing null check on optional Address property
2. Trace backward to find origin:
   - Why is Address null? (It's an optional field)
   - Was validation expected earlier? (No validation present)
   - Is this data issue or code issue? (Code issue - missing null check)
3. Analyze contributing factors:
   - Database schema: Address is nullable FK
   - Business logic: Address is optional for users
   - Code assumption: Code assumes Address always exists (incorrect)
4. Classify root cause type:
   - Logic error (missing null check)
   - Validation issue (no guard clause)
   - Assumption violation (incorrect assumption about data)
5. Verify hypothesis against code evidence
6. Search for similar patterns in codebase using Grep

**If Sequential Thinking Enabled**:
- Reflection Point: "Is this a code issue or data issue?"
- Course Correction: Revise if evidence shows data corruption vs missing validation
- Confidence Scoring: Rate certainty of root cause identification

**Tools Used**: Read, Grep
**Output**: Root cause statement with supporting evidence
**Success Criteria**:
- True root cause identified (not just throwing point)
- Evidence from code supports conclusion
- Contributing factors documented
- Similar patterns identified

**Example**:
```markdown
## Root Cause Identification

### Throwing Point
**Location**: UserService.cs:150
**Code**: `City = user.Address.City`
**Exception**: NullReferenceException when accessing `.City` on null `Address`

### Root Cause
**Primary Issue**: Missing null check on optional `User.Address` property
**Evidence**:
- Address is nullable navigation property (User.cs:25)
- Database schema: AddressId is nullable FK (Users table)
- Business rule: Users can register without address (Registration.cs:145)
- Code assumption: GetUserProfile assumes Address always exists (INCORRECT)
- 15% of users in database have null Address

**Contributing Factors**:
- No validation at data access layer
- No guard clauses in UserService
- No error handling in controller
- Optional property not clearly documented

**Pattern Analysis**:
Found 3 similar patterns in codebase:
- UserService.cs:178 - Accessing user.Phone.Number (same issue)
- OrderService.cs:234 - Accessing order.ShippingAddress.Street (same issue)
- ProfileController.cs:56 - Accessing user.Company.Name (same issue)
```

### Phase 4: Error Pattern Classification
**Duration**: 10-12% of total time
**Input**: Root cause from Phase 3
**Process**:
1. Classify error pattern:
   - **Null Reference** (this example)
   - Index Out of Range
   - Invalid Operation
   - Argument Exception
   - SQL Exception
   - Timeout Exception
   - Format Exception
   - File Not Found
   - Access Denied
   - Custom Exception
2. Determine error category:
   - Logic error (code defect)
   - Validation error (missing checks)
   - Integration error (external system)
   - Configuration error (settings)
   - Data error (corrupt/invalid data)
   - Performance error (timeout/resource)
3. Assess frequency pattern:
   - Consistent (always happens)
   - Intermittent (happens occasionally)
   - Rare (edge case)
   - New (recent regression)
4. Evaluate severity:
   - CRITICAL: Application crash, data loss
   - HIGH: Feature broken, affects many users
   - MEDIUM: Degraded functionality, workaround exists
   - LOW: Minor issue, rare scenario

**Tools Used**: None (classification phase)
**Output**: Error classification with pattern type and severity
**Success Criteria**:
- Pattern type identified
- Category assigned
- Frequency assessed
- Severity rated

**Example**:
```markdown
## Error Pattern Classification

### Pattern Type
**Primary**: Null Reference Exception
**Sub-Pattern**: Accessing property on optional navigation property without null check

### Category
**Type**: Logic Error + Validation Error
**Classification**: Code defect (missing defensive programming)

### Frequency
**Pattern**: Consistent
**Occurrence**: Happens for all users without Address (15% of users)
**Trigger**: Any attempt to view profile page for these users
**Data**: ~15,000 affected users out of 100,000 total

### Severity
**Rating**: HIGH
**Impact**: Feature completely broken for 15% of users
**User Experience**: Profile page crashes immediately
**Data Risk**: None (no data corruption)
**Business Impact**: Users cannot access profile features
```

### Phase 5: Solution Generation
**Duration**: 25-30% of total time
**Input**: Root cause + Classification from Phases 3-4
**Process**:
1. Generate **Quick Fix** (5-15 min implementation):
   - Minimal code change
   - Addresses immediate symptom
   - Temporary solution
   - Example: Add null check with default value

2. Generate **Proper Fix** (20-30 min implementation):
   - Comprehensive solution addressing root cause
   - Production-ready
   - Includes error handling
   - Example: Add null checks + refactor to use DTO pattern

3. Generate **Prevention Strategy** (1-2 hours implementation):
   - Prevents recurrence across codebase
   - Architectural improvement
   - Best practices adoption
   - Example: Implement validation framework + code analysis rules + automated tests

4. For each solution:
   - Provide code examples
   - Explain trade-offs
   - Estimate effort
   - Note prerequisites
   - Identify risks

**Tools Used**: Write (for examples)
**Output**: Three solution approaches with code samples
**Success Criteria**:
- All three solutions provided
- Each solution has code examples
- Trade-offs clearly explained
- Implementation guidance included

**Example**:
```markdown
## Solution Approaches

### 1. Quick Fix (5-15 minutes)
**Approach**: Add null check with default value
**Code**:
```csharp
public UserProfileDTO GetUserProfile(int userId)
{
    var user = _userRepository.GetById(userId);
    if (user == null)
        throw new UserNotFoundException($"User {userId} not found");

    var profile = new UserProfileDTO
    {
        UserId = user.UserId,
        Username = user.Username,
        City = user.Address?.City ?? "Not Specified",  // ← Null-safe access
        State = user.Address?.State ?? "Not Specified"
    };
    return profile;
}
```
**Pros**: Fast to implement, prevents crash immediately
**Cons**: Uses hardcoded default values, doesn't address similar patterns elsewhere

### 2. Proper Fix (20-30 minutes)
**Approach**: Add null checks + refactor with defensive programming
**Code**:
```csharp
public UserProfileDTO GetUserProfile(int userId)
{
    var user = _userRepository.GetById(userId);
    if (user == null)
        throw new UserNotFoundException($"User {userId} not found");

    var profile = new UserProfileDTO
    {
        UserId = user.UserId,
        Username = user.Username,
        City = GetAddressField(user.Address, a => a.City),
        State = GetAddressField(user.Address, a => a.State)
    };
    return profile;
}

private string GetAddressField(Address address, Func<Address, string> selector)
{
    return address != null ? selector(address) : "Not Specified";
}
```
**Pros**: Reusable pattern, cleaner code, handles all optional fields
**Cons**: Requires refactoring, more code changes

### 3. Prevention Strategy (1-2 hours)
**Approach**: Implement validation framework + code analysis + automated tests
**Steps**:
1. **Add extension methods for null-safe access**:
```csharp
public static class SafeAccessExtensions
{
    public static TResult SafeGet<T, TResult>(
        this T obj,
        Func<T, TResult> selector,
        TResult defaultValue = default(TResult)) where T : class
    {
        return obj != null ? selector(obj) : defaultValue;
    }
}
```

2. **Refactor using extension**:
```csharp
public UserProfileDTO GetUserProfile(int userId)
{
    var user = _userRepository.GetById(userId);
    if (user == null)
        throw new UserNotFoundException($"User {userId} not found");

    var profile = new UserProfileDTO
    {
        UserId = user.UserId,
        Username = user.Username,
        City = user.Address.SafeGet(a => a.City, "Not Specified"),
        State = user.Address.SafeGet(a => a.State, "Not Specified")
    };
    return profile;
}
```

3. **Add code analysis rules**:
   - Enable nullable reference types (C# 8+)
   - Add Roslyn analyzer for null checks
   - Configure warnings as errors

4. **Add automated tests**:
```csharp
[Test]
public void GetUserProfile_WithNullAddress_ReturnsDefaultValues()
{
    // Arrange
    var user = new User { UserId = 1, Address = null };
    _userRepository.Setup(x => x.GetById(1)).Returns(user);

    // Act
    var profile = _userService.GetUserProfile(1);

    // Assert
    Assert.AreEqual("Not Specified", profile.City);
    Assert.AreEqual("Not Specified", profile.State);
}
```

5. **Fix similar patterns** (identified in Phase 3):
   - UserService.cs:178
   - OrderService.cs:234
   - ProfileController.cs:56

**Pros**: Comprehensive solution, prevents recurrence, improves code quality
**Cons**: Requires significant refactoring, testing, deployment planning
**Expected Benefits**:
- All null reference patterns addressed
- Code analysis catches future issues
- Automated tests prevent regression
- Team adopts defensive programming practices
```

### Phase 6: Report Generation
**Duration**: 10-12% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Compile all findings into structured markdown report
2. Write executive summary (2-3 paragraphs)
3. Include parsed stack trace with annotations
4. Document code investigation findings
5. Present root cause analysis with evidence
6. Add error pattern classification
7. Include all three solution approaches
8. Add implementation guidance section
9. Create testing recommendations checklist
10. Add appendix with code snippets and references
11. Save report to `marketplace/output/analysis/` directory with timestamp

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
# Stack Trace Analysis: NullReferenceException

Generated: 2026-01-15 14:30:00
Duration: 28 minutes

## Executive Summary
...

## Stack Trace Breakdown
...

## Code Investigation
...

## Root Cause Identification
...

## Error Pattern Classification
...

## Solution Approaches
...

## Implementation Guidance
1. Apply Quick Fix immediately to production
2. Schedule Proper Fix for next sprint
3. Plan Prevention Strategy as technical debt initiative

## Testing Recommendations
- [ ] Test with user without Address (userId: 12345)
- [ ] Test with user with complete Address (userId: 67890)
- [ ] Test with invalid userId (userId: 99999)
- [ ] Test null propagation for all optional fields
- [ ] Verify error handling displays friendly message
...

## Appendix: Code References
- UserService.cs:145-154
- User.cs:25 (Address property definition)
- UserRepository.cs:45 (GetById implementation)
- Similar patterns: 3 locations identified
```

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **root-cause-analysis** (`../../shared-skills/root-cause-analysis.md`)
  - Systematic process for distinguishing symptoms from causes
  - Evidence collection and hypothesis validation
  - Root cause documentation patterns

- **performance-analysis-framework** (`../../shared-skills/performance-analysis-framework.md`)
  - Impact assessment methodologies
  - Pattern identification techniques
  - Measurement and profiling approaches

## Error Handling

### Scenario: Incomplete Stack Trace
**When**: Stack trace is partial or truncated
**Recovery**:
1. Analyze available frames
2. Note missing information in report
3. Request complete stack trace if possible
**User Message**:
```
⚠ Stack trace appears incomplete (only 2 frames visible).
Analyzing available information, but results may be limited.

For better analysis, please provide:
- Complete stack trace from logs
- Inner exception details (if any)
- Additional context (what user was doing)

Proceeding with available data...
```

### Scenario: Unrecognized Format
**When**: Stack trace format is not recognized
**Recovery**:
1. Attempt generic parsing
2. Prompt user to specify language/framework
3. Provide best-effort analysis
**User Message**:
```
⚠ Stack trace format not recognized automatically.
Please specify language/framework:
- csharp / dotnet
- java
- javascript / node
- python
- other: [specify]

Attempting generic parsing...
```

### Scenario: Code Files Not Found
**When**: File paths in stack trace don't exist in codebase
**Recovery**:
1. Note files not found
2. Analyze based on stack trace alone
3. Provide solutions without specific code context
**User Message**:
```
⚠ Code files from stack trace not found in codebase:
- UserService.cs (not found)
- UserController.cs (not found)

Possible reasons:
- Different codebase or branch
- Stack trace from another environment
- Files renamed/moved

Proceeding with stack-trace-only analysis...
```

### Scenario: Complex Nested Exceptions
**When**: Stack trace has 3+ levels of nested exceptions
**Recovery**: Enable Sequential Thinking for deeper analysis
**User Message**:
```
🔍 Complex nested exception detected (3 levels). Enabling deep analysis mode.
This analysis will take 20-30% longer but will provide:
- Layer-by-layer exception analysis
- Root cause identification across exception chain
- Reflection points for accurate diagnosis

Estimated time: 35-45 minutes
```

### Scenario: Framework-Only Stack Trace
**When**: Stack trace only shows framework code (no application code)
**Recovery**: Analyze pattern and provide general guidance
**User Message**:
```
⚠ Stack trace contains only framework code (no application code visible).
This usually means:
- Exception occurred in framework/library code
- Application code was filtered out
- Stack trace was captured at wrong level

Analyzing framework exception pattern and providing general guidance...
```

### Scenario: Multiple Similar Errors
**When**: Grep finds 5+ similar error patterns in codebase
**Recovery**: Include comprehensive impact assessment
**User Message**:
```
📊 Found 8 similar error patterns in codebase.
Analysis will include:
- List of all affected locations
- Comprehensive fix strategy
- Prioritization recommendations

This helps prevent future occurrences across codebase.
```

## Configuration

### Required Settings
None - agent works with defaults

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "analysis-toolkit": {
    "stack-trace-analyzer": {
      "timeout_minutes": 45,
      "max_file_reads": 30,
      "enable_sequential_thinking": "conditional",
      "sequential_thinking_trigger": {
        "min_exception_depth": 3,
        "min_stack_frames": 15
      },
      "report_detail_level": "full",
      "include_code_snippets": true,
      "max_code_snippet_lines": 20,
      "search_similar_patterns": true,
      "max_similar_patterns": 10
    }
  }
}
```

**Configuration Options**:
- `timeout_minutes`: Maximum analysis time before timeout (default: 45)
- `max_file_reads`: Maximum files to read during investigation (default: 30)
- `enable_sequential_thinking`: "always", "conditional", or "never" (default: "conditional")
- `sequential_thinking_trigger`: Conditions for enabling Sequential Thinking
- `report_detail_level`: "full" or "summary" (default: "full")
- `include_code_snippets`: Include code examples in report (default: true)
- `max_code_snippet_lines`: Max lines per code snippet (default: 20)
- `search_similar_patterns`: Search for similar patterns in codebase (default: true)
- `max_similar_patterns`: Max similar patterns to report (default: 10)

## Tools Required

- **Bash**: Execute git commands, check file existence, run searches
- **Glob**: Find files by pattern mentioned in stack trace
- **Grep**: Search code for error patterns, method names, similar issues
- **Read**: Read source files to understand error context
- **Write**: Generate analysis report markdown file

## Examples

### Example 1: Simple Null Reference
**Input**:
```bash
/analyze-stacktrace
```
**Stack Trace**: NullReferenceException in UserService.GetUserProfile

**Process**:
- Phase 1: Parse .NET stack trace (2 min)
- Phase 2: Locate and read UserService.cs (5 min)
- Phase 3: Identify missing null check on Address (8 min)
- Phase 4: Classify as null reference pattern (3 min)
- Phase 5: Generate 3 solutions (7 min)
- Phase 6: Create report (3 min)

**Output**: Report with:
- Root cause: Missing null check on optional property
- Quick fix: Null-safe access operator
- Proper fix: Defensive programming pattern
- Prevention: Validation framework + automated tests

**Time**: ~28 minutes
**Confidence**: 95%

### Example 2: Complex SQL Exception Chain
**Input**:
```bash
/analyze-stacktrace --file=logs/production-error.log
```
**Stack Trace**: SqlException with 3 nested inner exceptions

**Process**:
- Phase 1: Parse stack trace with nested exceptions (4 min)
- Phase 2: Investigate database access code (10 min)
- Phase 3: Trace through exception chain (15 min) [Sequential Thinking enabled]
  - Outer: Timeout exception
  - Middle: Deadlock exception
  - Inner: Lock wait timeout
  - Root: Missing index causing table lock
- Phase 4: Classify as database performance issue (5 min)
- Phase 5: Generate database optimization solutions (10 min)
- Phase 6: Create comprehensive report (6 min)

**Output**: Report with:
- Root cause: Missing index causing table locks and deadlocks
- Quick fix: Add index
- Proper fix: Index + query optimization
- Prevention: Database performance monitoring + index analysis

**Time**: ~50 minutes
**Confidence**: 90%

### Example 3: JavaScript Front-End Error
**Input**:
```bash
/analyze-stacktrace --language=javascript
```
**Stack Trace**: TypeError: Cannot read property 'name' of undefined

**Process**:
- Phase 1: Parse JavaScript stack trace (2 min)
- Phase 2: Locate JS file and read code (4 min)
- Phase 3: Identify undefined object access (6 min)
- Phase 4: Classify as undefined reference (3 min)
- Phase 5: Generate JS-specific solutions (6 min)
- Phase 6: Create report (3 min)

**Output**: Report with:
- Root cause: API response missing expected property
- Quick fix: Optional chaining (?.)
- Proper fix: Response validation + default values
- Prevention: TypeScript + runtime validation

**Time**: ~24 minutes
**Confidence**: 95%

## Success Metrics

Analysis is successful when:
- [ ] Stack trace successfully parsed (format detected, frames extracted)
- [ ] Exception type and message identified
- [ ] Code at error location retrieved (if files available)
- [ ] Root cause identified (not just throwing point)
- [ ] Root cause backed by code evidence
- [ ] Error pattern classified
- [ ] Severity assessed
- [ ] Three solution approaches provided (quick, proper, prevention)
- [ ] Each solution includes code examples
- [ ] Similar patterns identified in codebase
- [ ] Report is comprehensive and actionable
- [ ] Report saved to correct output directory
- [ ] Confidence level meets threshold (>85% for clear errors, >70% for complex chains)

## Related Agents

- **jira-root-cause-analyzer**: Use when error is reported in Jira ticket with additional context
- **db-query-analyzer**: Use when error is SQL-related and needs query optimization
- **impact-analyzer**: Use when you need to assess impact of proposed fix
- **code-review-agent**: Use to review proposed fix before implementation

## Related Documentation

- `../../shared-skills/root-cause-analysis.md` - Root cause methodology
- `../../../docs/WORKFLOW_DECISION_GUIDE.md` - When to use which analysis agent
- `../../../docs/TROUBLESHOOTING.md` - Common issues and solutions
- `../commands/analyze-stacktrace.md` - Command specification

---

**Agent Status**: Production Ready
**Verification Mode**: Enabled (all findings backed by code evidence when files available)
**Sequential Thinking**: Conditional (auto-enabled for complex nested exceptions)
**Average Duration**: 25-40 minutes depending on complexity
