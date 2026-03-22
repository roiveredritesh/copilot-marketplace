# Skill: Root Cause Analysis

## Overview

Root cause analysis (RCA) is a systematic methodology for identifying underlying causes of problems, not just addressing surface symptoms. This skill is fundamental to debugging, troubleshooting, and improving system reliability.

## When to Use This Skill

- **Investigating Bugs**: Find why a defect occurred
- **Production Issues**: Diagnose failures in live environments
- **Test Failures**: Understand why tests are failing
- **Performance Problems**: Identify performance bottlenecks
- **System Outages**: Trace failures to root causes
- **Feature Issues**: Determine why features behave unexpectedly

## Root Cause Analysis Process

### Step 1: Understand the Symptom

**What to do**:
1. Clearly define what went wrong
2. Understand when it happens
3. Note any error messages
4. Identify who/what is affected

**Questions to ask**:
- What is the observed behavior?
- What should the correct behavior be?
- When did this first occur?
- Does it happen consistently or intermittently?
- Who/what is impacted?

### Step 2: Gather Evidence

**Evidence types**:
- Exception messages and stack traces
- Log entries and timestamps
- System metrics (memory, CPU, disk)
- Recent code changes
- Environment information
- User actions and input

### Step 3: Develop Hypothesis

**Formulation**:
- `If [condition], then [error would occur]`
- Based on evidence and logic
- Testable hypothesis

**Rank by likelihood**:
- HIGH: Most probable based on evidence
- MEDIUM: Possible given evidence
- LOW: Unlikely but possible

### Step 4: Investigate Root Cause

**Search Methods**:

1. **Stack Trace Analysis**
   - Trace from exception location upward
   - Find where error originates

2. **Code Review**
   - Examine code that throws exception
   - Look for missing null checks
   - Check parameter validation

3. **Dependency Tracing**
   - What calls the method throwing error?
   - What assumptions does it make?
   - Are those assumptions valid?

4. **Logic Testing**
   - Walk through code mentally
   - Test with different inputs
   - Verify assumptions

### Step 5: Identify Actual vs Immediate Cause

**Immediate Cause**:
- The direct cause of the error
- Example: Null reference at specific line

**Actual Root Cause**:
- The underlying reason for immediate cause
- Example: Lack of input validation

**Contributing Factors**:
- Conditions that enabled the problem
- Missing error handling
- Missing validation
- Insufficient logging
- Weak testing

### Step 6: Assess Contributing Factors

Factors that enabled or worsened the problem:
- No parameter validation
- No null handling
- Poor error logging
- Missing test for edge cases

### Step 7: Prevent Recurrence

**Prevention Strategy**:
1. Immediate Fix: Address the immediate cause
2. Testing: Add unit tests for edge cases
3. Logging: Log unexpected conditions
4. Code Review: Check for similar patterns
5. Standards: Establish coding standards

## Common Root Cause Patterns

### Pattern 1: Missing Null Validation
**Symptom**: NullReferenceException
**Root Cause**: Parameter or property null without check
**Fix**: Add null check or validation

### Pattern 2: Missing Error Handling
**Symptom**: Unhandled exception propagates
**Root Cause**: Expected error not caught
**Fix**: Add try-catch or validation

### Pattern 3: Incorrect Logic
**Symptom**: Wrong result or behavior
**Root Cause**: Algorithm or logic error
**Fix**: Correct the logic

### Pattern 4: Missing Initialization
**Symptom**: Undefined or zero values
**Root Cause**: Object/variable not initialized
**Fix**: Initialize properly

### Pattern 5: Race Condition
**Symptom**: Intermittent failures
**Root Cause**: Concurrent access without synchronization
**Fix**: Add locking or synchronization

## Investigation Tools & Techniques

### Tool 1: Stack Trace Analysis
- Provides call stack
- Shows exact location of exception
- Indicates method chain

### Tool 2: Logging
- Trace execution flow
- Log important state changes
- Useful for intermittent issues

### Tool 3: Breakpoint Debugging
- Pause execution
- Inspect variables and state
- Step through code

### Tool 4: Code Review
- Examine suspicious code
- Look for patterns
- Check error handling

### Tool 5: Testing
- Reproduce the issue
- Test hypotheses
- Verify fixes

## Root Cause Analysis Checklist

- [ ] Clear symptom definition
- [ ] All evidence gathered
- [ ] Multiple hypotheses developed
- [ ] Investigation completed
- [ ] Immediate cause identified
- [ ] Actual root cause found
- [ ] Contributing factors documented
- [ ] Fix solution developed
- [ ] Testing plan created
- [ ] Prevention measures identified
- [ ] Similar issues checked for
- [ ] Documentation updated

## Key Takeaways

1. **Root cause ≠ Immediate cause**: Dig deeper
2. **Ask why**: Multiple times, until you find real cause
3. **Document findings**: For future reference
4. **Test thoroughly**: Prevent recurrence
5. **Fix properly**: Not just patch symptoms
6. **Share knowledge**: Help team learn from issues

---

**Last Updated**: 2025-10-30
