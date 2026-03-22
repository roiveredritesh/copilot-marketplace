# /fix-linq-bug Command

## Description

Identify and fix common LINQ-to-SQL bugs including null reference exceptions, lazy loading issues, DataContext lifetime problems, change tracking errors, and deferred execution issues. Provides corrected code with detailed explanations and testing guidance.

## Usage

```bash
/fix-linq-bug <file-path> [--report=full|summary]
```

## Parameters

### Required

- **`<file-path>`**: Path to the C# file containing LINQ-to-SQL code with bugs
  - Must be a valid C# source file (.cs extension)
  - File should contain LINQ-to-SQL queries or DataContext usage
  - Example: `src/Services/OrderService.cs`

### Optional Flags

- **`--report=full|summary`**: Report detail level (default: `full`)
  - `full` - Comprehensive bug fix report with detailed analysis and testing guidance
  - `summary` - Concise bug fix summary with before/after code

## Examples

### Example 1: Fix Null Reference Exception

```bash
/fix-linq-bug src/Services/OrderService.cs --report=full
```

**Input Code** (with bug):
```csharp
public void ProcessOrder(int orderId)
{
    using (var db = new DataContext())
    {
        var order = db.Orders.FirstOrDefault(o => o.Id == orderId);

        // Bug: order could be null!
        Console.WriteLine(order.Customer.Name);
    }
}
```

**What it generates**:

**Fixed Code**:
```csharp
public void ProcessOrder(int orderId)
{
    using (var db = new DataContext())
    {
        var order = db.Orders.FirstOrDefault(o => o.Id == orderId);

        if (order == null)
        {
            throw new ArgumentException($"Order with ID {orderId} not found");
        }

        if (order.Customer == null)
        {
            throw new InvalidOperationException(
                $"Order {orderId} has no associated customer");
        }

        Console.WriteLine(order.Customer.Name);
    }
}
```

**Report Includes**:
- Bug description and severity (Critical)
- Root cause analysis
- Trigger scenario
- Before/after code comparison
- Alternative fixes (null-conditional operator)
- Testing recommendations

**Output**: `marketplace/output/linq-analysis/linq-bug-fix-OrderService-20260115-143022.md`

---

### Example 2: Fix N+1 Lazy Loading Issue

```bash
/fix-linq-bug src/DataAccess/CustomerRepository.cs --report=full
```

**Input Code** (with bug):
```csharp
public List<string> GetCustomerNamesWithOrders()
{
    using (var db = new DataContext())
    {
        var customers = db.Customers.Where(c => c.IsActive).ToList();

        // Bug: Accessing Orders causes N+1 queries
        return customers
            .Where(c => c.Orders.Any())
            .Select(c => c.Name)
            .ToList();
    }
}
```

**Fixed Code**:
```csharp
public List<string> GetCustomerNamesWithOrders()
{
    using (var db = new DataContext())
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Customer>(c => c.Orders);
        db.LoadOptions = dlo;

        var customers = db.Customers
            .Where(c => c.IsActive)
            .ToList();

        return customers
            .Where(c => c.Orders.Any())
            .Select(c => c.Name)
            .ToList();
    }
}
```

**Output**: `marketplace/output/linq-analysis/linq-bug-fix-CustomerRepository-20260115-143022.md`

---

### Example 3: Fix Disposed Context Issue

```bash
/fix-linq-bug src/BusinessLogic/OrderProcessor.cs --report=full
```

**Input Code** (with bug):
```csharp
public Order GetOrderWithDetails(int orderId)
{
    Order order;
    using (var db = new DataContext())
    {
        order = db.Orders.First(o => o.Id == orderId);
    }

    // Bug: Accessing navigation property after DataContext disposed
    var itemCount = order.OrderDetails.Count();
    return order;
}
```

**Fixed Code**:
```csharp
public Order GetOrderWithDetails(int orderId)
{
    using (var db = new DataContext())
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.OrderDetails);
        db.LoadOptions = dlo;

        var order = db.Orders.First(o => o.Id == orderId);

        // Force materialization before DataContext disposal
        var itemCount = order.OrderDetails.Count();

        return order;
    }
}
```

**Output**: `marketplace/output/linq-analysis/linq-bug-fix-OrderProcessor-20260115-143022.md`

---

### Example 4: Fix Change Tracking Issue

```bash
/fix-linq-bug src/DataAccess/OrderRepository.cs --report=summary
```

**Input Code** (with bug):
```csharp
public void UpdateOrderStatus(int orderId, string newStatus)
{
    Order order;
    using (var db1 = new DataContext())
    {
        order = db1.Orders.First(o => o.Id == orderId);
    }

    using (var db2 = new DataContext())
    {
        order.Status = newStatus;
        db2.SubmitChanges(); // Bug: order not tracked by db2!
    }
}
```

**Fixed Code**:
```csharp
public void UpdateOrderStatus(int orderId, string newStatus)
{
    using (var db = new DataContext())
    {
        var order = db.Orders.First(o => o.Id == orderId);
        order.Status = newStatus;
        db.SubmitChanges(); // Properly tracked and updated
    }
}
```

**Output**: `marketplace/output/linq-analysis/linq-bug-fix-OrderRepository-20260115-143022.md`

---

## Bug Types Detected and Fixed

### Critical Bugs
1. **Null Reference Exceptions**
   - `FirstOrDefault()` without null check
   - Navigation property without null check
   - Collection access without validation

2. **Disposed DataContext Access**
   - Accessing navigation properties after `using` block
   - Deferred queries executing outside DataContext scope

3. **Data Loss Issues**
   - Change tracking not working
   - Updates not persisting

### High Priority Bugs
4. **Lazy Loading N+1 Queries**
   - Navigation properties accessed in loops
   - Missing DataLoadOptions configuration

5. **Change Tracking Problems**
   - Attaching entities incorrectly
   - Modifying entities from different DataContext

### Medium Priority Bugs
6. **Deferred Execution Issues**
   - Returning `IQueryable` that executes outside scope
   - Query not materialized before DataContext disposal

7. **DataContext Lifetime Issues**
   - DataContext in class field (long-lived)
   - Missing `using` statement
   - DataContext created in loop

### Low Priority Issues
8. **Concurrency Issues**
   - No optimistic concurrency handling
   - Missing `ChangeConflictException` handling

9. **Code Smells**
   - Redundant DataContext instantiation
   - Inefficient query patterns

## Report Contents

### Full Report Includes:
1. **Executive Summary**
   - Total bugs found
   - Bugs fixed
   - Severity breakdown
   - Manual review required (if any)

2. **Bugs Fixed Section**
   For each bug:
   - **Title**: Descriptive name
   - **Severity**: Critical/High/Medium/Low
   - **Type**: Null Reference, Lazy Loading, DataContext Lifetime, etc.
   - **Location**: File, method, line numbers
   - **Risk**: What happens when bug triggers
   - **Problem**: Detailed explanation of what's wrong
   - **Trigger Scenario**: Code that causes the bug
   - **Fixed Code**: Complete corrected code
   - **Alternative Fixes**: Other approaches (if applicable)
   - **Explanation**: Why the fix works
   - **Testing Recommendations**: How to verify

3. **Code Changes Summary**
   - List of all modified methods
   - Diff showing changes
   - Key improvements highlighted

4. **Testing Recommendations**
   - Unit tests to create
   - Edge cases to verify
   - Integration test scenarios
   - Performance testing (if applicable)

5. **Verification Checklist**
   - Step-by-step verification steps
   - Expected outcomes
   - Rollback plan

### Summary Report Includes:
1. **Bugs Found and Fixed**
   - Count by severity
   - Quick list with line numbers

2. **Code Changes**
   - Before/after code snippets

3. **Testing Steps**
   - Quick verification checklist

## Output Location

All reports are saved to:
```
marketplace/output/linq-analysis/linq-bug-fix-{filename}-{timestamp}.md
```

Example:
```
marketplace/output/linq-analysis/linq-bug-fix-OrderService-20260115-143022.md
```

## Delegation

This command delegates to the **`linq-bug-fixer`** agent, which performs:
1. Bug pattern detection
2. Root cause analysis
3. Fix generation with error handling
4. Validation of fixes
5. Code application (optional)
6. Report generation

See `agents/linq-bug-fixer.md` for detailed agent specification.

## When to Use This Command

Use `/fix-linq-bug` when you encounter:
- **Production errors** related to LINQ-to-SQL (NullReferenceException, disposed context, etc.)
- **"Object reference not set to an instance of an object"** errors
- **"Cannot access a disposed object"** errors
- **Performance issues** from lazy loading (N+1 queries)
- **Data not persisting** after calling `SubmitChanges()`
- **Unexpected null values** from navigation properties
- **Concurrency conflicts** in multi-user scenarios
- **Code review feedback** about LINQ-to-SQL issues

## When NOT to Use

Don't use this command when:
- Code is working correctly (use `/optimize-linq` for performance instead)
- You need to analyze for potential issues (use `/analyze-linq` instead)
- Issues are not LINQ-to-SQL related
- You want to convert to stored procedures (use `/convert-linq-to-sql` instead)

## Fix Application Options

By default, fixes are **NOT applied** to the source file. The report shows what should be changed.

To apply fixes automatically (use with caution):
```bash
/fix-linq-bug src/Services/OrderService.cs --apply-fixes
```

**Note**: Original file will be backed up with `.backup` extension before changes.

## Common Bug Patterns Fixed

### Pattern 1: FirstOrDefault Without Null Check
```csharp
// Before (Bug)
var user = db.Users.FirstOrDefault(u => u.Id == id);
return user.Email; // NullReferenceException if not found

// After (Fixed)
var user = db.Users.FirstOrDefault(u => u.Id == id);
if (user == null)
    throw new ArgumentException($"User {id} not found");
return user.Email;
```

### Pattern 2: Navigation Property Without Eager Loading
```csharp
// Before (Bug - N+1 queries)
var orders = db.Orders.ToList();
foreach (var order in orders)
{
    Console.WriteLine(order.Customer.Name); // Separate query each time
}

// After (Fixed)
var dlo = new DataLoadOptions();
dlo.LoadWith<Order>(o => o.Customer);
db.LoadOptions = dlo;

var orders = db.Orders.ToList();
foreach (var order in orders)
{
    Console.WriteLine(order.Customer.Name); // Already loaded
}
```

### Pattern 3: Disposed Context Access
```csharp
// Before (Bug)
Order order;
using (var db = new DataContext())
{
    order = db.Orders.First(o => o.Id == id);
}
var name = order.Customer.Name; // Disposed context!

// After (Fixed)
Order order;
using (var db = new DataContext())
{
    var dlo = new DataLoadOptions();
    dlo.LoadWith<Order>(o => o.Customer);
    db.LoadOptions = dlo;

    order = db.Orders.First(o => o.Id == id);
    var _ = order.Customer.Name; // Force load before disposal
}
var name = order.Customer.Name; // Safe now
```

### Pattern 4: Change Tracking Not Working
```csharp
// Before (Bug)
Order order;
using (var db1 = new DataContext())
{
    order = db1.Orders.First(o => o.Id == id);
}
using (var db2 = new DataContext())
{
    order.Status = "Updated";
    db2.SubmitChanges(); // Nothing happens - order not tracked!
}

// After (Fixed)
using (var db = new DataContext())
{
    var order = db.Orders.First(o => o.Id == id);
    order.Status = "Updated";
    db.SubmitChanges(); // Properly tracked and saved
}
```

## Performance Impact

- **Analysis Time**: 5-15 minutes depending on file size
- **No Runtime Impact**: Bug fixing is static code analysis
- **Performance Improvement**: N+1 fixes can improve query performance by 90%+

## Follow-Up Actions

After receiving the bug fix report:

1. **Review Fixes**
   - Understand each bug and its fix
   - Verify fix doesn't break functionality

2. **Apply Changes**
   - Manually apply fixes from report
   - Or use `--apply-fixes` flag with caution

3. **Test Thoroughly**
   - Create unit tests for each bug scenario
   - Test edge cases (null data, empty collections, etc.)
   - Run integration tests

4. **Performance Test**
   ```bash
   # If N+1 queries were fixed, verify performance improvement
   # Measure query count before/after
   ```

5. **Deploy**
   - Deploy to staging first
   - Monitor for any issues
   - Deploy to production after verification

## Common Use Cases

### Use Case 1: Production Error Investigation
```bash
# Production error: "Object reference not set to an instance of an object"
# in OrderService.ProcessOrder method

/fix-linq-bug src/Services/OrderService.cs --report=full
# Review report to find and fix null reference bugs
```

### Use Case 2: Performance Issue from Lazy Loading
```bash
# Dashboard page is slow - suspected N+1 queries

/fix-linq-bug src/DataAccess/DashboardRepository.cs --report=full
# Review report for lazy loading issues and apply DataLoadOptions fixes
```

### Use Case 3: Data Not Persisting
```bash
# Updates to Order status are not being saved

/fix-linq-bug src/DataAccess/OrderRepository.cs --report=full
# Review report for change tracking issues
```

## Tips

1. **Test edge cases**: After applying fixes, test with null data, empty collections, non-existent IDs
2. **Create unit tests**: For each bug fixed, create a unit test to prevent regression
3. **Review before applying**: Always review fixes before applying automatically
4. **Backup first**: If using `--apply-fixes`, ensure code is in version control
5. **Performance test**: If N+1 fixes applied, measure performance improvement

## Troubleshooting

### "No bugs detected"
- File may already be bug-free (good!)
- Or file doesn't contain LINQ-to-SQL code
- Try analyzing other files

### "Manual review required for Bug #3"
- Bug is complex and automatic fix may not be appropriate
- Review the report for recommended actions
- Apply fix manually with careful testing

### "Fix would break functionality"
- Agent detected that automatic fix would change behavior
- Manual refactoring required
- Review alternative solutions in report

## Related Commands

- **`/analyze-linq`** - Analyze for potential issues before they become bugs
- **`/optimize-linq`** - Optimize performance after bugs are fixed
- **`/convert-linq-to-sql`** - Convert to stored procedures for better control

## Support

For issues or questions:
- Review the bug fix report for detailed explanations
- Check `agents/linq-bug-fixer.md` for agent details
- See `docs/TROUBLESHOOTING.md` for common issues

---

**Command Version**: 2.0.0
**Agent**: linq-bug-fixer
**Plugin**: linq-to-sql-expert
