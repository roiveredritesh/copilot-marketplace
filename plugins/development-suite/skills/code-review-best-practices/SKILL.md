# Skill: Code Review Best Practices

## Overview

Code review is a critical quality gate that improves code quality, catches bugs early, shares knowledge, and enforces standards. This skill provides a comprehensive framework for conducting effective, thorough code reviews across all programming languages.

## When to Use This Skill

- **Reviewing pull requests** before merge
- **Validating proposed solutions** for bugs
- **Code quality assessments** and audits
- **Mentoring developers** on code quality
- **Establishing review standards** for teams
- **Security reviews** of critical code

## Code Review Philosophy

### Goals of Code Review
1. **Catch bugs and issues** before production
2. **Improve code quality** and maintainability
3. **Share knowledge** across team
4. **Enforce standards** and best practices
5. **Mentor developers** through feedback
6. **Prevent technical debt** accumulation

### What Code Review is NOT
- Opportunity to critique the person
- Place for nitpicking style preferences
- Gatekeeping or power struggle
- Opportunity to rewrite others' code
- Place to demand perfection

### Review Mindset
- **Be kind**: Assume positive intent
- **Be specific**: Provide clear, actionable feedback
- **Be constructive**: Suggest improvements, not just problems
- **Be humble**: Your way isn't always the only way
- **Be timely**: Review promptly to unblock team

## Comprehensive Code Review Checklist

### 1. Functionality & Requirements

- [ ] **Meets requirements**: Does the code do what was requested?
- [ ] **Handles edge cases**: Empty lists, null values, boundaries?
- [ ] **Correct business logic**: Aligns with domain rules?
- [ ] **No regressions**: Doesn't break existing functionality?
- [ ] **Complete implementation**: No TODOs or placeholders?

**Questions to ask**:
- Does this solve the stated problem?
- What happens with invalid input?
- Are all acceptance criteria met?

### 2. Code Quality & Design

- [ ] **Follows SOLID principles**: Single responsibility, open/closed, etc.
- [ ] **DRY (Don't Repeat Yourself)**: No unnecessary duplication?
- [ ] **Separation of concerns**: Proper layering (UI, business, data)?
- [ ] **Appropriate abstractions**: Not over-engineered or under-engineered?
- [ ] **Clear naming**: Variables, methods, classes are descriptive?
- [ ] **Manageable complexity**: Methods and classes are reasonably sized?

**Red flags**:
- Methods > 50 lines
- Classes > 500 lines
- Duplicate code blocks
- God classes/methods
- Unclear variable names (x, temp, data)

### 3. Error Handling & Validation

- [ ] **Input validation**: All inputs validated before use?
- [ ] **Proper exception handling**: Try-catch where appropriate?
- [ ] **Meaningful error messages**: Errors are clear and actionable?
- [ ] **Null handling**: Null checks where needed?
- [ ] **Fail-fast**: Errors detected early?
- [ ] **Logging**: Errors logged with sufficient context?

**Common issues**:
```csharp
// BAD: No validation
public void ProcessOrder(Order order)
{
    var total = order.Items.Sum(i => i.Price); // NullReferenceException if order or Items is null
}

// GOOD: Proper validation
public void ProcessOrder(Order order)
{
    if (order == null)
        throw new ArgumentNullException(nameof(order));

    if (order.Items == null || !order.Items.Any())
        throw new ArgumentException("Order must have at least one item", nameof(order));

    var total = order.Items.Sum(i => i.Price);
}
```

### 4. Security

- [ ] **No SQL injection**: Parameterized queries used?
- [ ] **No XSS vulnerabilities**: User input sanitized?
- [ ] **Authentication/Authorization**: Proper access checks?
- [ ] **No sensitive data exposure**: Passwords, keys, PII protected?
- [ ] **Secure dependencies**: No known vulnerable libraries?
- [ ] **HTTPS for sensitive data**: API calls use secure transport?

**Critical security patterns**:
```csharp
// BAD: SQL Injection vulnerability
var sql = $"SELECT * FROM Users WHERE Username = '{username}'";

// GOOD: Parameterized query
var sql = "SELECT * FROM Users WHERE Username = @Username";
// Use parameter: command.Parameters.AddWithValue("@Username", username);

// BAD: XSS vulnerability
<div>@Model.UserInput</div>

// GOOD: Encoded output
<div>@Html.Encode(Model.UserInput)</div>
```

### 5. Performance

- [ ] **No obvious bottlenecks**: N+1 queries, nested loops on large data?
- [ ] **Efficient algorithms**: Appropriate time complexity?
- [ ] **Database queries optimized**: Proper indexing, no SELECT *?
- [ ] **Caching considered**: Appropriate for frequently accessed data?
- [ ] **Resource cleanup**: Connections, files, streams disposed?
- [ ] **Async/await used properly**: For I/O-bound operations?

**Common performance issues**:
```csharp
// BAD: N+1 query problem
var orders = db.Orders.ToList();
foreach (var order in orders)
{
    var customer = db.Customers.Find(order.CustomerId); // N queries
}

// GOOD: Eager loading
var orders = db.Orders.Include(o => o.Customer).ToList(); // 1 query
```

### 6. Testing

- [ ] **Unit tests included**: Critical logic tested?
- [ ] **Tests actually test something**: Not just placeholder tests?
- [ ] **Edge cases covered**: Null, empty, boundary conditions?
- [ ] **Test names clear**: Describe what's being tested?
- [ ] **Tests are independent**: Don't rely on other tests?
- [ ] **Mocks used appropriately**: External dependencies mocked?

**Test quality indicators**:
```csharp
// GOOD: Clear test name and structure
[Test]
public void ProcessOrder_WithNullOrder_ThrowsArgumentNullException()
{
    // Arrange
    var processor = new OrderProcessor();

    // Act & Assert
    Assert.Throws<ArgumentNullException>(() => processor.ProcessOrder(null));
}
```

### 7. Maintainability

- [ ] **Code is readable**: Easy to understand logic flow?
- [ ] **Comments where needed**: Complex logic explained?
- [ ] **No commented-out code**: Old code removed?
- [ ] **Consistent style**: Matches project conventions?
- [ ] **Logging appropriate**: Key operations logged?
- [ ] **Magic numbers avoided**: Constants used instead?

**Maintainability patterns**:
```csharp
// BAD: Magic numbers and unclear logic
if (order.Status == 3 && order.Total > 1000)

// GOOD: Named constants and clear logic
private const int StatusCompleted = 3;
private const decimal LargeOrderThreshold = 1000m;

if (order.Status == StatusCompleted && order.Total > LargeOrderThreshold)
```

### 8. Documentation

- [ ] **API documented**: Public methods have XML comments?
- [ ] **README updated**: If public interface changed?
- [ ] **Migration guide**: If breaking changes introduced?
- [ ] **Inline comments**: Complex algorithms explained?
- [ ] **Architecture docs updated**: If design changed?

```csharp
/// <summary>
/// Processes an order and calculates the total amount including tax and shipping.
/// </summary>
/// <param name="order">The order to process. Cannot be null.</param>
/// <returns>The total amount including all fees.</returns>
/// <exception cref="ArgumentNullException">Thrown when order is null.</exception>
public decimal ProcessOrder(Order order)
{
    // Implementation
}
```

### 9. Database Changes

- [ ] **Migration scripts included**: Schema changes documented?
- [ ] **Backward compatible**: Won't break existing code?
- [ ] **Rollback plan**: Can changes be reverted?
- [ ] **Indexes added**: For new query patterns?
- [ ] **Data migrated**: Existing data handled properly?

### 10. Configuration & Dependencies

- [ ] **No hardcoded values**: Configuration in config files?
- [ ] **Dependencies justified**: New libraries necessary?
- [ ] **Version pinned**: Dependency versions specified?
- [ ] **License compatible**: New dependencies license-compliant?

## Review Process & Workflow

### Step 1: Understand the Context
**Before reviewing**:
1. Read the ticket/issue description
2. Understand what problem is being solved
3. Review any design docs or discussions
4. Check if there are special considerations

### Step 2: Initial Scan
**Quick pass (5-10 minutes)**:
1. Look at the file changes list
2. Check if changes make sense at high level
3. Verify all necessary files updated
4. Identify files needing deep review

### Step 3: Deep Review
**Detailed pass (20-60 minutes)**:
1. Review each file thoroughly
2. Check against checklist above
3. Note issues and questions
4. Verify tests cover changes

### Step 4: Test Verification
**If possible**:
1. Pull the branch locally
2. Run tests
3. Test the functionality manually
4. Verify edge cases

### Step 5: Provide Feedback
**When commenting**:
1. Use constructive language
2. Explain the "why" behind suggestions
3. Distinguish between blocking issues and suggestions
4. Offer specific alternatives
5. Ask questions when unsure

## Feedback Categories

### 🔴 Critical (Must Fix)
Issues that **must** be addressed before merge:
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Correctness bugs
- Missing error handling for critical paths

**Example**:
> 🔴 **Critical**: This SQL query is vulnerable to SQL injection. Please use parameterized queries instead.

### 🟡 Important (Should Fix)
Issues that **should** be addressed but might be acceptable with justification:
- Performance concerns
- Code quality issues
- Missing tests
- Potential bugs in edge cases

**Example**:
> 🟡 **Important**: This N+1 query could be slow with many orders. Consider using eager loading with `Include()`.

### 🔵 Suggestion (Nice to Have)
Improvements that would be nice but aren't required:
- Code style improvements
- Refactoring opportunities
- Additional tests
- Documentation enhancements

**Example**:
> 🔵 **Suggestion**: Consider extracting this validation logic into a separate method for better readability.

### ❓ Question
Clarifications or understanding gaps:
**Example**:
> ❓ **Question**: Why did we choose to use a Dictionary here instead of a List? Is there a performance consideration I'm missing?

## Review Anti-Patterns to Avoid

### Anti-Pattern 1: Nitpicking Style
```
// BAD feedback
"You should use var instead of explicit type here"
"This line could be one line instead of two"
"I prefer brackets on same line"
```

**Fix**: Use linters and formatters for style. Focus on substance.

### Anti-Pattern 2: Rewriting in Your Style
```
// BAD feedback
"I would rewrite this entire method like this: [20 lines of code]"
```

**Fix**: Suggest improvements, but respect author's approach if it works.

### Anti-Pattern 3: Vague Criticism
```
// BAD feedback
"This doesn't look right"
"Can you improve this?"
"This is confusing"
```

**Fix**: Be specific about what's wrong and why.

### Anti-Pattern 4: Demanding Perfection
```
// BAD feedback
"Before merging, also refactor the entire module, add 50 more tests,
and rewrite the documentation"
```

**Fix**: Focus on the changes at hand. File follow-up tickets for future work.

### Anti-Pattern 5: Blocking Without Reasoning
```
// BAD feedback
"No, do it differently" [no explanation]
```

**Fix**: Explain why and suggest specific alternatives.

## Good Feedback Examples

### Example 1: Security Issue
```
🔴 **Critical - SQL Injection Vulnerability**

This query concatenates user input directly into SQL:
`var sql = $"SELECT * FROM Users WHERE Name = '{userName}'";`

This is vulnerable to SQL injection. An attacker could input: `' OR '1'='1`

**Fix**: Use parameterized queries:
```csharp
var sql = "SELECT * FROM Users WHERE Name = @UserName";
command.Parameters.AddWithValue("@UserName", userName);
```

**Reference**: [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
```

### Example 2: Performance Concern
```
🟡 **Important - Potential N+1 Query**

On line 45, we're loading orders and then fetching the customer for each order in the loop:
```csharp
foreach (var order in orders)
{
    var customer = db.Customers.Find(order.CustomerId); // N database queries
}
```

With 1000 orders, this makes 1001 database queries.

**Suggestion**: Use eager loading:
```csharp
var orders = db.Orders.Include(o => o.Customer).ToList(); // 1 query with JOIN
foreach (var order in orders)
{
    var customer = order.Customer; // Already loaded
}
```

This should significantly improve performance when dealing with many orders.
```

### Example 3: Code Quality
```
🔵 **Suggestion - Extract Method**

The validation logic in `ProcessOrder` (lines 20-45) is 26 lines and handles multiple concerns.

**Suggestion**: Consider extracting into a separate method:
```csharp
private void ValidateOrder(Order order)
{
    // Validation logic here
}

public void ProcessOrder(Order order)
{
    ValidateOrder(order);
    // Processing logic
}
```

This would improve readability and make the validation logic reusable and testable.
```

## Language-Specific Considerations

### C# / .NET
- Check for proper `using` statements or `IDisposable` implementation
- Verify async/await used correctly (no `async void`)
- Check LINQ queries for efficiency
- Verify nullable reference types handled properly (C# 8+)

### JavaScript/TypeScript
- Check for proper error handling in Promises
- Verify `const` used instead of `let` when appropriate
- Check for memory leaks (event listeners cleaned up)
- Verify TypeScript types are meaningful (not just `any`)

### Python
- Check for proper exception handling
- Verify list comprehensions used appropriately
- Check for PEP 8 compliance
- Verify type hints used (Python 3.5+)

### SQL
- Check for proper indexing
- Verify parameterized queries (no SQL injection)
- Check for efficient JOIN usage
- Verify transactions used where needed

## Code Review Checklist Summary

```
[ ] Functionality - Does it work correctly?
[ ] Code Quality - Is it well-designed and maintainable?
[ ] Error Handling - Proper validation and error handling?
[ ] Security - No vulnerabilities?
[ ] Performance - No obvious bottlenecks?
[ ] Testing - Adequate test coverage?
[ ] Maintainability - Easy to understand and modify?
[ ] Documentation - Sufficient inline and API docs?
[ ] Database - Schema changes handled properly?
[ ] Configuration - No hardcoded values?
```

## Key Takeaways

1. **Focus on substance**: Not style preferences
2. **Be constructive**: Suggest, don't just criticize
3. **Prioritize issues**: Critical > Important > Suggestions
4. **Explain why**: Help reviewee learn
5. **Be timely**: Review promptly to unblock
6. **Test when possible**: Don't just read code
7. **Assume positive intent**: Be kind and respectful
8. **It's a conversation**: Discuss, don't dictate

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Core Development
