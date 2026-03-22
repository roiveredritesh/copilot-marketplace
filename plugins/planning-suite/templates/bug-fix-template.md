---
template-name: bug-fix
description: Template for planning bug fixes with root cause analysis and comprehensive validation
applies-to: [bug-fix, issue-resolution, defect-fix]
required-inputs: [bug-description, reproduction-steps, expected-behavior]
---

# Template: Bug Fix Planning

## When to Use
Use this template to plan bug fixes, especially when you have existing analysis from Jira.

**Examples**:
- Fix user login timeout not working
- Correct calculation error in reporting
- Fix race condition in async code

## Required Inputs

1. **Bug Description**: What's the problem
2. **Reproduction Steps**: How to reproduce
3. **Expected Behavior**: What should happen
4. **Current Behavior**: What actually happens

## Planning Structure

### Phase 1: Root Cause Analysis (30-60 min)

**If using existing analysis**:
- Read analysis output from Jira ticket
- Extract root cause findings
- Note affected files already identified

**If no analysis**:
- Reproduce the bug
- Add logging to understand flow
- Trace execution path
- Identify root cause

**Output**: Root cause documented

### Phase 2: Impact Assessment (30 min)

**Assess**:
- Which files need modification
- Dependencies affected
- Other bugs this might cause
- Performance impact
- Data consistency impact

**Output**: Impact analysis

### Phase 3: Fix Design (30-60 min)

**Design**:
- What change fixes the root cause
- Why this approach
- Alternative approaches and why not chosen
- Minimal change principle (fix bug, don't refactor)

**Output**: Solution design document

### Phase 4: Implement Fix (Variable)

**Steps**:
1. Locate problematic code
2. Implement fix
3. Add comments explaining fix
4. Verify fix compiles

**Code Pattern**:
```csharp
// BEFORE - Buggy code
public User GetUser(int id)
{
    return _context.Users.FirstOrDefault(x => x.Id == id); // Race condition
}

// AFTER - Fixed
public User GetUser(int id)
{
    var user = _context.Users
        .AsNoTracking()
        .FirstOrDefaultAsync(x => x.Id == id)
        .GetAwaiter()
        .GetResult();
    return user;
}
```

### Phase 5: Add Test to Catch Bug (1 hour)

**Create**:
- Unit test that reproduces bug
- Verify test fails with old code
- Verify test passes with fix

**Code Template**:
```csharp
[Test]
public void GetUser_ConcurrentAccess_ReturnsSameUser()
{
    // Arrange
    var userId = 1;
    var tasks = new List<Task<User>>();

    // Act - simulate concurrent access
    for (int i = 0; i < 10; i++)
    {
        tasks.Add(Task.Run(() => _userService.GetUserAsync(userId)));
    }

    var results = Task.WhenAll(tasks).Result;

    // Assert - all should get same user
    Assert.True(results.All(u => u.Id == userId));
}
```

### Phase 6: Verify Fix (Variable)

**Test**:
- Reproduce original issue - verify it's fixed
- Run unit tests - all pass
- Run regression tests - no new breaks
- Manual testing - system works normally

### Phase 7: Code Review (15 min)

**Checklist**:
- [ ] Minimal change (no refactoring)
- [ ] Comments explain why
- [ ] Test included
- [ ] No performance regression
- [ ] No new warnings

### Phase 8: Deploy & Monitor (Variable)

**Steps**:
1. Deploy to staging
2. Verify fix on staging
3. Deploy to production
4. Monitor logs for errors
5. Verify metrics normal

## Fix Patterns by Type

### Pattern: Null Check Missing
```csharp
// BEFORE
var value = obj.Property; // Can throw if obj is null

// AFTER
var value = obj?.Property; // Safe null handling
if (value == null) return null; // or handle appropriately
```

### Pattern: Async/Await Deadlock
```csharp
// BEFORE
var result = asyncMethod().Result; // Deadlock risk

// AFTER
var result = await asyncMethod(); // Proper async
```

### Pattern: Off-By-One Error
```csharp
// BEFORE
for (int i = 0; i <= list.Count; i++) // Includes out of bounds
{
    ProcessItem(list[i]);
}

// AFTER
for (int i = 0; i < list.Count; i++) // Correct bounds
{
    ProcessItem(list[i]);
}
```

### Pattern: Missing Lock/Synchronization
```csharp
// BEFORE
private List<User> _cache = new(); // Not thread-safe

// AFTER
private readonly object _lock = new();
private List<User> _cache = new();

public User GetFromCache(int id)
{
    lock (_lock)
    {
        return _cache.FirstOrDefault(u => u.Id == id);
    }
}
```

## File-Level Changes

Typical bug fix:
- 1-3 files modified
- 5-50 lines changed
- 1-2 test files added/modified

## Testing Strategy

### Bug Fix Testing Hierarchy

1. **Unit Test** (mandatory)
   - Test specific bug condition
   - Reproduce original issue
   - Verify fix

2. **Regression Test** (recommended)
   - Verify related functionality
   - Ensure fix doesn't break other features

3. **Integration Test** (if needed)
   - Test end-to-end workflow
   - Verify with real data/services

4. **Manual Testing** (recommended)
   - Reproduce original steps
   - Verify system behavior normal

## Success Criteria

- [ ] Root cause identified and documented
- [ ] Fix implemented and tested
- [ ] Unit test added and passes
- [ ] No regression in other tests
- [ ] Code review approved
- [ ] Deployed to production
- [ ] Monitoring shows no new errors
- [ ] User verifies fix works

## Risk Assessment

**Risks for Bug Fixes**:
- **Low Risk**: Single file change, isolated logic
- **Medium Risk**: Multiple file changes, shared dependencies
- **High Risk**: Core logic change, affects data integrity

**Mitigation**:
- Thorough testing
- Code review
- Staging validation
- Monitoring post-deployment
- Rollback plan ready

## Rollback Plan

**When**: If fix causes new issues
**How**:
1. Revert code change
2. Redeploy previous version
3. Verify system healthy
4. Investigate what went wrong

## Documentation

**Document**:
- Root cause explanation
- Why fix was chosen
- Edge cases handled
- What test covers

---

**Template Version**: 1.0.0
**Complexity**: Low to Medium
**Typical Effort**: 1-4 hours (depends on bug complexity)
**Risk Level**: Medium
