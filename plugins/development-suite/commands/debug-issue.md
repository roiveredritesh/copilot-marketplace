# Command: /debug-issue

Analyzes code issues and errors, providing debugging strategies, root cause identification, and step-by-step resolution guidance.

**Task Coverage**: Task #12 (Debug and troubleshoot issues in code)

## Usage

```
/debug-issue <error-context> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **error-context**: Error message, stack trace, or problem description
  - Exception message: `/debug-issue "NullReferenceException at UserService.GetUser line 45"`
  - Full stack trace: `/debug-issue "System.ArgumentException: Value cannot be null..."`
  - Problem description: `/debug-issue "Getting intermittent deadlock in data access"`
  - Can reference file: `/debug-issue error.txt` (file containing error details)
  - Interactive mode: `/debug-issue` (prompts for error details)

### Optional Flags

- **--async**: Execute in background (good for complex debugging)
- **--wait**: Execute synchronously (default)
- **--report=full|summary**: Report detail level (full by default)

## Examples

```bash
# Debug with wait (synchronous)
/debug-issue "NullReferenceException: Object reference not set to an instance of an object"

# Background debugging for complex issue
/debug-issue "System.Data.DataException: Timeout expired..." --async

# Quick summary report
/debug-issue "ArgumentException: Email format invalid" --report=summary

# Debug from file (stack trace file)
/debug-issue error-trace.txt --wait

# Interactive debugging (prompts for details)
/debug-issue
```

## Implementation

### Step 1: Parse Error Context

- Extract error information from input
- If file path provided, read error details from file
- If interactive mode, prompt for error details:
  - Error message or exception type
  - Stack trace (if available)
  - Source code context (which method, class)
  - Test case reproducing issue
  - Recent code changes

**Process**:
1. Detect input type:
   - If file path (contains . or /), read file
   - If empty string, enter interactive mode
   - Otherwise, treat as error message/stack trace
2. Parse error information:
   - Extract exception type
   - Extract error message
   - Parse stack trace if present
   - Identify method and line number
3. Request additional context if needed:
   - Ask for source code
   - Ask for reproduction steps
   - Ask for recent changes
4. Validate enough information to analyze

**Outputs**: Error type, error message, stack trace, source context

### Step 2: Analyze & Queue Task

**For Async Mode**:
1. Create task ID: `task-YYYYMMDD-HHMMSS-debug-{random}`
2. Create status file: `.claude/task-status/{task-id}.md`
3. Queue to background coordinator with:
   - Task type: `debugging`
   - Error context: Full error details
   - Report level: Full or summary
4. Return task ID and estimated time
5. Indicate how to monitor progress

**For Sync Mode**:
1. Delegate to debug-helper agent immediately
2. Wait for analysis completion
3. Return final report

**Async Response**:
```
Task ID: task-20251030-150045-debug-xyz789
Status: Analyzing error
Estimated time: 8-15 minutes

Monitor progress: /task-status task-20251030-150045-debug-xyz789
```

### Step 3: Delegate to Agent

**For sync mode**, invoke debug-helper agent with:
- Input: Error message, stack trace, code context
- Process: 7-phase debugging analysis
- Output: Root cause, debugging strategy, proposed solutions
- Report: Full debugging guide with step-by-step instructions

**Agent Tasks**:
1. Parse error context
2. Trace execution flow
3. Identify root cause
4. Create debugging strategy
5. Propose solutions (immediate/proper/comprehensive)
6. Create verification plan
7. Generate complete debugging report

### Step 4: Return Response

**Sync Mode Response**:
```
# Debugging Analysis: NullReferenceException in UserService

## Root Cause Identified
The user parameter in GetUserAsync is not null-checked before accessing properties.

## Proposed Solutions
[Code examples with immediate, proper, and comprehensive fixes]

## Debugging Instructions
[Step-by-step debugging strategy]

Report: marketplace/output/reviews/nullreference-debug-analysis.md
```

**Response includes**:
- Error summary
- Root cause identified
- Execution flow analysis
- Variable state analysis
- Debugging instructions
- Proposed code solutions
- Verification steps
- Related issues if found
- Where full report is saved

## Output Locations

- Full analysis: `marketplace/output/reviews/<issue>-debug-analysis.md`
- Quick guide: `marketplace/output/reviews/<issue>-debug-guide.md`
- Summary: `marketplace/output/reviews/<issue>-summary.md`
- Task status: `.claude/task-status/<task-id>.md`

## Typical Analysis Time

- Simple error (NullReferenceException, ArgumentException): 5-10 minutes
- Complex error (Deadlock, Memory leak, race condition): 10-20 minutes
- Intermittent issue: 15-25 minutes

**Recommendation**: Use `--async` for complex or intermittent issues.

## Error Categories Handled

### Logic Errors
- Off-by-one in loops
- Incorrect conditional logic
- Wrong comparison operators
- Copy-paste errors
- Missing validation

### State Errors
- NullReferenceException
- Objects used after disposal
- Invalid state transitions
- Race conditions
- Shared mutable state

### Resource Errors
- FileNotFoundException
- NetworkException
- TimeoutException
- OutOfMemoryException
- Connection pooling exhausted

### Type Errors
- ArgumentException (wrong type)
- InvalidOperationException (wrong state)
- FormatException (bad data format)
- InvalidCastException
- TypeLoadException

### Concurrency Issues
- Deadlock (circular lock)
- Race condition
- Stale data
- Cache invalidation
- Event ordering

### Integration Errors
- API contract changes
- External service timeout
- Authentication failure
- Database connection failure
- Message queue issues

### Async/Await Issues
- Missing await
- ConfigureAwait(false) missing
- Sync over async deadlock
- Exception not propagated
- Improper task handling

## Debugging Information Provided

For each issue analysis:
- **Root Cause**: What's actually wrong
- **Evidence**: Why you believe this is the cause
- **Execution Path**: How code reaches the error
- **Variable States**: What variables contain at failure
- **Breakpoint Strategy**: Where to put breakpoints
- **Logging Strategy**: What to log for visibility
- **Proposed Fixes**: Immediate, proper, and comprehensive solutions
- **Verification**: How to verify fix works
- **Prevention**: How to avoid this in future

## Interactive Debugging Mode

When using `/debug-issue` without arguments, you'll be prompted for:

1. **Error Message or Exception Type**
   - "NullReferenceException"
   - "System.ArgumentException: Invalid format"
   - Paste full stack trace

2. **Source Code Context**
   - Method where error occurs
   - Lines causing issue
   - Calling code

3. **Reproduction Information**
   - How to reproduce the issue
   - Input that causes failure
   - Expected vs actual behavior

4. **Environment Details**
   - .NET Framework version
   - Database system
   - OS information
   - Recent code changes

5. **Test Case or Data**
   - Sample data that triggers issue
   - Test case that reproduces

## Integration with Other Tools

**Debugging Tools**:
- Visual Studio Debugger
- Breakpoints and watches
- Call stack inspection
- Local variables window
- Immediate window

**Analysis Tools**:
- Stack trace parsing
- Code inspection
- Execution flow tracing
- Variable state analysis
- Performance profilers

**Related Commands**:
- `/analyze-stacktrace`: For complex stack trace parsing
- `/root-cause-analysis`: For Jira issue debugging
- `/validate-solution`: For testing proposed fixes

## FAQ

**Q: What information do I need to provide?**
A: At minimum, the error message. More detail = better analysis.

**Q: Can you fix it automatically?**
A: No, but I'll identify the root cause and propose solutions.

**Q: What if it's intermittent?**
A: I'll help identify race conditions, concurrency issues, or timing problems.

**Q: How do I know if the fix is correct?**
A: Follow the verification steps in the debugging report.

**Q: What if I have a memory leak?**
A: Use memory profiler suggestions in debugging report, follow analysis.

**Q: Can you identify performance issues?**
A: Yes, if related to debugging. Use `/optimize-query` or `/optimize-algorithm` for optimization.

**Q: What about third-party library issues?**
A: Yes, same debugging approach applies.

**Q: Will you review my fix?**
A: Use `/validate-solution` or `/review-pr` from Review Suite plugin.

**Q: How long does analysis take?**
A: Simple: 5-10 min, Complex: 10-20 min, Intermittent: 15-25 min.

**Q: Can you find similar issues in codebase?**
A: Yes, debugging analysis identifies similar patterns if found.

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Delegated To**: debug-helper agent
**Task Coverage**: Task #12
