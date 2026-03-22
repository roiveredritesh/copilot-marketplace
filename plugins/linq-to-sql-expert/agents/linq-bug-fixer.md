---
agent_name: linq-bug-fixer
version: 2.0.0
last_updated: 2026-01-15
status: production
sequential_thinking: conditional
author: Ritesh
description: Identifies and fixes common LINQ-to-SQL bugs including null reference exceptions, lazy loading issues, DataContext lifetime problems, and change tracking errors
task_types:
  - linq-debug
tools_required:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
  - Edit
mcp_required: []
skills_referenced:
  - linq-to-sql-patterns
  - sql-optimization-patterns
output_directory: marketplace/output/linq-analysis
output_file_pattern: linq-bug-fix-{filename}-{timestamp}.md
---

# LINQ Bug Fixer Agent

## Purpose

The LINQ Bug Fixer agent identifies and fixes common LINQ-to-SQL bugs that cause runtime errors, performance issues, or unexpected behavior. It focuses on null reference exceptions, lazy loading problems, DataContext lifetime issues, change tracking errors, and deferred execution problems that frequently occur in LINQ-to-SQL applications.

## When to Use

Use this agent when you encounter:

- **Null Reference Exceptions** in LINQ queries or navigation properties
- **Lazy Loading Errors** like "Cannot access a disposed object" or N+1 query problems
- **DataContext Lifetime Issues** causing stale data or disposed context errors
- **Change Tracking Problems** where entity updates don't persist
- **Deferred Execution Issues** causing queries to execute outside DataContext scope
- **Concurrency Conflicts** in multi-user scenarios
- **Entity State Errors** during insert, update, or delete operations
- **Transaction Scope Problems** causing rollbacks or deadlocks
- **Connection String Errors** or authentication failures
- **Serialization Issues** with LINQ entities in web services or APIs

## When NOT to Use

Do NOT use this agent when:

- You need performance optimization without fixing bugs (use `linq-optimizer` instead)
- You want to analyze queries for best practices (use `linq-query-analyzer` instead)
- The code doesn't use LINQ-to-SQL
- Issues are not LINQ-related (database connectivity, infrastructure, etc.)
- You need to convert LINQ to stored procedures (use `linq-to-sql-converter` instead)

## Input/Output Specification

### Input Format

**Required Parameters**:
```json
{
  "file_path": "src/Services/OrderService.cs",
  "report_format": "full"
}
```

**Optional Parameters**:
```json
{
  "report_format": "summary",
  "bug_types": ["null-reference", "lazy-loading", "datacontext-lifetime"],
  "fix_in_place": false
}
```

### Output Format

**Full Report Structure**:
```markdown
# LINQ Bug Fix Report

**File**: src/Services/OrderService.cs
**Analyzed**: 2026-01-15 14:30:22
**Agent**: linq-bug-fixer v2.0.0

## Executive Summary
- Bugs Found: 5
- Critical: 2 (null reference, disposed context)
- High: 2 (lazy loading issues)
- Medium: 1 (change tracking)
- Fixed: 5
- Manual Review Required: 0

## Bugs Fixed

### Bug #1: Null Reference Exception in GetCustomerOrders()
**Severity**: Critical
**Type**: Null Reference
**Location**: Lines 45-52

[Detailed analysis and fix...]

## Code Changes Summary
[List of all changes...]

## Testing Recommendations
[How to verify fixes...]

## Verification Checklist
[Step-by-step verification...]
```

### Example Input/Output

**Example: Null Reference Exception**

Input:
```csharp
public void ProcessOrder(int orderId)
{
    using (var db = new DataContext())
    {
        var order = db.Orders.FirstOrDefault(o => o.Id == orderId);

        // Potential null reference if order not found
        Console.WriteLine(order.Customer.Name); // Bug!
    }
}
```

Output (excerpt):
```markdown
### Bug #1: Null Reference Exception in ProcessOrder()

**Severity**: Critical
**Type**: Null Reference
**Location**: Line 8
**Risk**: Application crash when order doesn't exist

**Problem**:
The method calls `FirstOrDefault()` which returns NULL if no order is found,
then immediately accesses `order.Customer.Name` without null checking.

**Trigger Scenario**:
```csharp
ProcessOrder(99999); // Non-existent order ID
// Exception: Object reference not set to an instance of an object
```

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

        // Additional null check for navigation property
        if (order.Customer == null)
        {
            throw new InvalidOperationException($"Order {orderId} has no associated customer");
        }

        Console.WriteLine(order.Customer.Name);
    }
}
```

**Alternative Fix (with C# 8.0+ null-conditional operator)**:
```csharp
public void ProcessOrder(int orderId)
{
    using (var db = new DataContext())
    {
        var order = db.Orders.FirstOrDefault(o => o.Id == orderId);

        var customerName = order?.Customer?.Name ?? "Unknown";
        Console.WriteLine(customerName);

        if (order == null)
        {
            // Handle missing order scenario
            return;
        }
    }
}
```
```

## Process Overview

1. **Bug Detection** (3-7 min) - Scan code for common LINQ-to-SQL bug patterns
2. **Root Cause Analysis** (4-8 min) - Determine root cause of each bug
3. **Fix Generation** (4-10 min) - Generate corrected code for each bug
4. **Validation** (2-5 min) - Validate fixes don't introduce new issues
5. **Code Application** (2-4 min) - Apply fixes to file (if requested) or generate report
6. **Report Generation** (2-4 min) - Create comprehensive bug fix report

**Total Duration**: 17-38 minutes depending on code complexity and bug count

## Detailed Process

### Phase 1: Bug Detection (3-7 minutes)

**Objective**: Scan code for common LINQ-to-SQL bug patterns and anti-patterns.

**Tools**: Grep, Read

**Steps**:

1. **Read Source File**
   - Load entire file content
   - Identify all methods containing LINQ queries
   - Extract DataContext usage patterns

2. **Scan for Null Reference Patterns**

   **Pattern A: FirstOrDefault/SingleOrDefault without null check**:
   ```csharp
   var entity = db.Table.FirstOrDefault(predicate);
   entity.Property // No null check!
   ```

   **Pattern B: Navigation property without null check**:
   ```csharp
   var order = db.Orders.First(o => o.Id == id);
   order.Customer.Name // Customer could be null!
   ```

   **Pattern C: Null collection access**:
   ```csharp
   order.OrderDetails.First() // OrderDetails could be empty!
   ```

3. **Scan for Lazy Loading Issues**

   **Pattern A: Accessing navigation properties in loop**:
   ```csharp
   var orders = db.Orders.ToList();
   foreach (var order in orders)
   {
       var customer = order.Customer; // Lazy load in loop = N+1
   }
   ```

   **Pattern B: Accessing properties after DataContext disposal**:
   ```csharp
   Order order;
   using (var db = new DataContext())
   {
       order = db.Orders.First();
   }
   var name = order.Customer.Name; // DataContext disposed!
   ```

4. **Scan for DataContext Lifetime Issues**

   **Pattern A: DataContext in class field (long-lived)**:
   ```csharp
   public class Repository
   {
       private DataContext _db = new DataContext(); // Anti-pattern!
   }
   ```

   **Pattern B: Missing using statement**:
   ```csharp
   var db = new DataContext();
   var orders = db.Orders.ToList();
   // DataContext never disposed!
   ```

   **Pattern C: DataContext created in loop**:
   ```csharp
   foreach (var id in ids)
   {
       using (var db = new DataContext()) // New context each iteration!
       {
           var order = db.Orders.First(o => o.Id == id);
       }
   }
   ```

5. **Scan for Change Tracking Problems**

   **Pattern A: Attaching entity without setting original values**:
   ```csharp
   var order = new Order { Id = 1, Status = "Updated" };
   db.Orders.Attach(order);
   db.SubmitChanges(); // May not update anything!
   ```

   **Pattern B: Modifying entity from different DataContext**:
   ```csharp
   Order order;
   using (var db1 = new DataContext())
   {
       order = db1.Orders.First();
   }
   using (var db2 = new DataContext())
   {
       order.Status = "Updated";
       db2.SubmitChanges(); // order not tracked by db2!
   }
   ```

6. **Scan for Deferred Execution Issues**

   **Pattern A: Returning IQueryable that will execute outside DataContext**:
   ```csharp
   public IQueryable<Order> GetOrders()
   {
       using (var db = new DataContext())
       {
           return db.Orders.Where(o => o.IsActive);
           // Query not executed yet, will fail when enumerated!
       }
   }
   ```

   **Pattern B: Query executed in different context**:
   ```csharp
   IQueryable<Order> query;
   using (var db = new DataContext())
   {
       query = db.Orders;
   }
   var orders = query.ToList(); // DataContext disposed!
   ```

7. **Scan for Concurrency Issues**

   **Pattern A: No concurrency check**:
   ```csharp
   var order = db.Orders.First(o => o.Id == id);
   order.Status = "Completed";
   db.SubmitChanges(); // May overwrite concurrent changes!
   ```

   **Pattern B: Missing timestamp/rowversion column**:
   - Check entity definitions for concurrency columns

8. **Categorize Detected Bugs**
   - Critical: Bugs causing exceptions or data loss
   - High: Bugs causing performance issues or incorrect behavior
   - Medium: Bugs causing inefficiency or potential future issues
   - Low: Code smells or minor anti-patterns

**Success Criteria**:
- All bug patterns scanned
- Bugs categorized by severity
- Line numbers and context captured
- Bug types identified

---

### Phase 2: Root Cause Analysis (4-8 minutes)

**Objective**: Determine the root cause of each detected bug and understand the developer's intent.

**Tools**: Read

**Skills Referenced**: `linq-to-sql-patterns`

**Steps**:

1. **Analyze Bug Context**

   For each bug:
   - Read surrounding code for context
   - Identify method purpose from name and comments
   - Understand data flow and dependencies
   - Determine if bug is systematic or isolated

2. **Determine Root Cause Categories**

   **A. Lack of Null Awareness**:
   - Developer didn't consider null scenarios
   - Assumed data always exists
   - Missing validation logic

   **B. LINQ-to-SQL Knowledge Gap**:
   - Didn't understand lazy loading behavior
   - Unaware of DataContext lifetime requirements
   - Misunderstood deferred execution

   **C. Copy-Paste Errors**:
   - Code copied from example without adaptation
   - Missing error handling from original

   **D. Refactoring Issues**:
   - Code moved without updating DataContext usage
   - Method extracted without considering scope

   **E. Concurrency Oversight**:
   - Single-user testing didn't reveal concurrency issues
   - Missing optimistic concurrency controls

3. **Assess Impact**

   For each bug:
   - **Frequency**: How often is this code path executed?
   - **User Impact**: Does it affect users directly?
   - **Data Impact**: Can it corrupt or lose data?
   - **Performance Impact**: Does it cause performance degradation?
   - **Security Impact**: Does it create security vulnerabilities?

4. **Identify Fix Strategy**

   **Strategy 1: Defensive Programming**:
   - Add null checks and validation
   - Handle edge cases gracefully
   - Example: FirstOrDefault + null check

   **Strategy 2: Eager Loading**:
   - Add DataLoadOptions
   - Preload navigation properties
   - Example: N+1 query fix

   **Strategy 3: Scope Management**:
   - Ensure DataContext lifetime covers all data access
   - Materialize queries before leaving scope
   - Example: Deferred execution fix

   **Strategy 4: Change Tracking Fix**:
   - Properly attach entities
   - Use single DataContext for updates
   - Example: Update from different context

   **Strategy 5: Concurrency Control**:
   - Add timestamp/rowversion columns
   - Implement retry logic
   - Handle ChangeConflictException

5. **Document Root Cause**
   - Write clear explanation of why bug occurred
   - Note how it manifests (error message, behavior)
   - Identify trigger scenarios

**Success Criteria**:
- Root cause identified for each bug
- Impact assessed
- Fix strategy determined
- Documentation prepared

---

### Phase 3: Fix Generation (4-10 minutes)

**Objective**: Generate corrected code for each bug with proper error handling.

**Tools**: Read

**Steps**:

1. **Generate Null Reference Fixes**

   **Fix Type A: Add null check with exception**:
   ```csharp
   // Before
   var order = db.Orders.FirstOrDefault(o => o.Id == id);
   Console.WriteLine(order.Customer.Name);

   // After
   var order = db.Orders.FirstOrDefault(o => o.Id == id);
   if (order == null)
       throw new ArgumentException($"Order {id} not found");
   if (order.Customer == null)
       throw new InvalidOperationException($"Order {id} has no customer");
   Console.WriteLine(order.Customer.Name);
   ```

   **Fix Type B: Null-conditional operator**:
   ```csharp
   // Before
   var customerName = order.Customer.Name;

   // After (C# 6.0+)
   var customerName = order?.Customer?.Name ?? "Unknown";
   ```

   **Fix Type C: Null-coalescing with default**:
   ```csharp
   // Before
   var count = order.OrderDetails.Count();

   // After
   var count = order.OrderDetails?.Count() ?? 0;
   ```

2. **Generate Lazy Loading Fixes**

   **Fix Type A: Add DataLoadOptions**:
   ```csharp
   // Before
   var orders = db.Orders.ToList();
   foreach (var order in orders)
   {
       Console.WriteLine(order.Customer.Name); // N+1 query
   }

   // After
   var dlo = new DataLoadOptions();
   dlo.LoadWith<Order>(o => o.Customer);
   db.LoadOptions = dlo;

   var orders = db.Orders.ToList();
   foreach (var order in orders)
   {
       Console.WriteLine(order.Customer.Name); // Already loaded
   }
   ```

   **Fix Type B: Use projection to avoid lazy loading**:
   ```csharp
   // Before
   var orders = db.Orders.ToList();
   var customerNames = orders.Select(o => o.Customer.Name).ToList();

   // After
   var customerNames = db.Orders
       .Select(o => o.Customer.Name)
       .ToList();
   ```

3. **Generate DataContext Lifetime Fixes**

   **Fix Type A: Ensure materialization before disposal**:
   ```csharp
   // Before
   Order order;
   using (var db = new DataContext())
   {
       order = db.Orders.First(o => o.Id == id);
   }
   var name = order.Customer.Name; // Disposed context!

   // After
   Order order;
   using (var db = new DataContext())
   {
       var dlo = new DataLoadOptions();
       dlo.LoadWith<Order>(o => o.Customer);
       db.LoadOptions = dlo;

       order = db.Orders.First(o => o.Id == id);
       // Force load all navigation properties before disposal
       var _ = order.Customer.Name;
   }
   var name = order.Customer.Name; // Safe now
   ```

   **Fix Type B: Expand DataContext scope**:
   ```csharp
   // Before
   public List<OrderDto> GetOrders()
   {
       List<Order> orders;
       using (var db = new DataContext())
       {
           orders = db.Orders.ToList();
       }
       return orders.Select(MapToDto).ToList(); // May access lazy properties
   }

   // After
   public List<OrderDto> GetOrders()
   {
       using (var db = new DataContext())
       {
           var orders = db.Orders.ToList();
           return orders.Select(MapToDto).ToList(); // Within scope
       }
   }
   ```

   **Fix Type C: Remove DataContext from class field**:
   ```csharp
   // Before
   public class OrderRepository
   {
       private DataContext _db = new DataContext(); // Long-lived!

       public Order GetOrder(int id)
       {
           return _db.Orders.First(o => o.Id == id);
       }
   }

   // After
   public class OrderRepository
   {
       private readonly string _connectionString;

       public OrderRepository(string connectionString)
       {
           _connectionString = connectionString;
       }

       public Order GetOrder(int id)
       {
           using (var db = new DataContext(_connectionString))
           {
               return db.Orders.First(o => o.Id == id);
           }
       }
   }
   ```

4. **Generate Change Tracking Fixes**

   **Fix Type A: Attach with original values**:
   ```csharp
   // Before
   var order = new Order { Id = 1, Status = "Updated" };
   db.Orders.Attach(order);
   db.SubmitChanges(); // Nothing happens!

   // After
   var order = db.Orders.First(o => o.Id == 1);
   order.Status = "Updated";
   db.SubmitChanges(); // Tracked changes applied
   ```

   **Fix Type B: Use same DataContext for update**:
   ```csharp
   // Before
   Order order;
   using (var db1 = new DataContext())
   {
       order = db1.Orders.First(o => o.Id == 1);
   }
   using (var db2 = new DataContext())
   {
       order.Status = "Updated";
       db2.SubmitChanges(); // order not in db2's tracking!
   }

   // After
   using (var db = new DataContext())
   {
       var order = db.Orders.First(o => o.Id == 1);
       order.Status = "Updated";
       db.SubmitChanges(); // Properly tracked
   }
   ```

5. **Generate Deferred Execution Fixes**

   **Fix Type A: Materialize before returning**:
   ```csharp
   // Before
   public IQueryable<Order> GetActiveOrders()
   {
       using (var db = new DataContext())
       {
           return db.Orders.Where(o => o.IsActive); // Deferred!
       }
   }

   // After
   public List<Order> GetActiveOrders()
   {
       using (var db = new DataContext())
       {
           return db.Orders
               .Where(o => o.IsActive)
               .ToList(); // Materialized
       }
   }
   ```

6. **Generate Concurrency Fixes**

   **Fix Type A: Add optimistic concurrency handling**:
   ```csharp
   // Before
   var order = db.Orders.First(o => o.Id == id);
   order.Status = "Completed";
   db.SubmitChanges();

   // After
   try
   {
       var order = db.Orders.First(o => o.Id == id);
       order.Status = "Completed";
       db.SubmitChanges();
   }
   catch (ChangeConflictException)
   {
       foreach (ObjectChangeConflict conflict in db.ChangeConflicts)
       {
           // Option 1: Keep database values
           conflict.Resolve(RefreshMode.OverwriteCurrentValues);

           // Option 2: Keep current values (overwrite database)
           // conflict.Resolve(RefreshMode.KeepCurrentValues);

           // Option 3: Merge (custom logic)
           // conflict.Resolve(RefreshMode.KeepChanges);
       }
       db.SubmitChanges(); // Retry
   }
   ```

7. **Add Comprehensive Error Handling**

   Wrap critical operations:
   ```csharp
   try
   {
       // LINQ operations
   }
   catch (SqlException ex)
   {
       // Database errors
       throw new DataAccessException("Database error", ex);
   }
   catch (InvalidOperationException ex)
   {
       // LINQ errors (no elements, multiple elements, etc.)
       throw new BusinessLogicException("Invalid operation", ex);
   }
   ```

**Success Criteria**:
- Fixed code generated for each bug
- Fixes follow best practices
- Error handling added
- Code compiles correctly

---

### Phase 4: Validation (2-5 minutes)

**Objective**: Validate fixes don't introduce new issues and maintain original functionality.

**Tools**: Read

**Steps**:

1. **Syntax Validation**
   - Check all C# syntax is correct
   - Verify braces, parentheses match
   - Ensure using statements present

2. **Logic Validation**
   - Verify fix maintains original intent
   - Check edge cases are handled
   - Ensure no new bugs introduced

3. **Performance Validation**
   - Check fixes don't degrade performance
   - Verify eager loading is appropriate
   - Ensure no unnecessary materializations

4. **Best Practices Check**
   - Verify fixes follow LINQ-to-SQL best practices
   - Check null handling is consistent
   - Ensure error messages are descriptive

5. **Generate Test Scenarios**
   - Identify test cases for each fix
   - Document expected behavior
   - Note edge cases to test

**Success Criteria**:
- All fixes validated
- No new issues introduced
- Test scenarios documented

---

### Phase 5: Code Application (2-4 minutes)

**Objective**: Apply fixes to source file (if requested) or generate report only.

**Tools**: Edit, Write

**Steps**:

1. **Check fix_in_place Parameter**
   - If `true`, apply fixes directly to file
   - If `false` (default), generate report only

2. **Apply Fixes (if requested)**
   - Use Edit tool to replace buggy code
   - Apply fixes in order (line numbers may shift)
   - Preserve code formatting and style
   - Add comments explaining fixes

3. **Create Backup (if applying fixes)**
   - Save original file with `.backup` extension
   - Note backup location in report

4. **Generate Code Diff**
   - Show before/after for each fix
   - Highlight changes
   - Add explanatory comments

**Success Criteria**:
- Fixes applied correctly (if requested)
- Original file backed up
- Diffs generated

---

### Phase 6: Report Generation (2-4 minutes)

**Objective**: Generate comprehensive bug fix report with all fixes documented.

**Tools**: Write

**Steps**:

1. **Generate Executive Summary**
   - Total bugs found and fixed
   - Severity breakdown
   - Critical fixes highlighted

2. **Document Each Bug**
   - Bug description and severity
   - Root cause explanation
   - Location (file, method, lines)
   - Before/after code
   - Explanation of fix
   - Testing recommendations

3. **Create Code Changes Summary**
   - List all modified methods
   - Show diffs
   - Highlight key changes

4. **Add Testing Recommendations**
   - Unit tests to create
   - Integration tests needed
   - Edge cases to verify
   - Performance tests

5. **Include Verification Checklist**
   - Step-by-step verification
   - Expected outcomes
   - Rollback plan if issues found

6. **Save Report**
   - Save to `marketplace/output/linq-analysis/` directory
   - Filename: `linq-bug-fix-{filename}-{timestamp}.md`

**Success Criteria**:
- Comprehensive report generated
- All fixes documented
- Testing guidance provided
- File saved successfully

---

## Skills Referenced

1. **linq-to-sql-patterns** - LINQ-to-SQL best practices and anti-patterns
2. **sql-optimization-patterns** - SQL and LINQ performance patterns

## Error Handling

### Error Scenario 1: No Bugs Found

**Response**:
```markdown
Analysis Result: No bugs detected

File: src/DataAccess/OrderRepository.cs

The analyzed file appears to follow LINQ-to-SQL best practices with no
detected bugs. Code includes:
- Proper null checking
- Appropriate DataContext lifetime management
- Eager loading where needed
- Good error handling

Keep up the good work!
```

### Error Scenario 2: Fix Cannot Be Automatically Generated

**Response**:
```markdown
Bug #3: Complex concurrency issue - Manual review required

Location: UpdateOrderStatus() - Lines 45-62

Problem: Complex business logic with multiple concurrent users updating
same entities. Automatic fix may not preserve all business rules.

Recommended Actions:
1. Review business requirements for concurrent updates
2. Consider pessimistic locking if appropriate
3. Implement conflict resolution strategy
4. Add retry logic with exponential backoff

This issue requires manual review and custom solution.
```

### Error Scenario 3: Applying Fix Would Break Functionality

**Response**:
```markdown
Warning: Fix #2 not applied - Potential functionality impact

Bug: Deferred execution in GetOrders()
Location: Lines 28-35

The method returns IQueryable<Order> which is used by multiple callers
with additional filters. Materializing the query would break this pattern.

Alternative Solutions:
1. Keep IQueryable but extend DataContext lifetime in callers
2. Use repository pattern with filtering parameters
3. Document requirement for callers to use same DataContext scope

Fix not applied automatically - manual refactoring recommended.
```

---

## Configuration

```json
{
  "linq-bug-fixer": {
    "report_format": "full",
    "fix_in_place": false,
    "create_backup": true,
    "bug_types": ["all"],
    "min_severity": "medium"
  }
}
```

## Tools Required

1. **Bash** - File operations
2. **Glob** - Find files
3. **Grep** - Search for bug patterns
4. **Read** - Read source files
5. **Write** - Generate reports
6. **Edit** - Apply fixes (if fix_in_place enabled)

## Examples

### Example 1: Null Reference Fix

**Input**:
```csharp
public string GetCustomerName(int orderId)
{
    using (var db = new DataContext())
    {
        var order = db.Orders.FirstOrDefault(o => o.Id == orderId);
        return order.Customer.Name; // Bug: order could be null!
    }
}
```

**Fixed Code**:
```csharp
public string GetCustomerName(int orderId)
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

        return order.Customer.Name;
    }
}
```

---

### Example 2: Lazy Loading N+1 Fix

**Input**:
```csharp
public List<string> GetCustomerNamesForOrders()
{
    using (var db = new DataContext())
    {
        var orders = db.Orders.Where(o => o.IsActive).ToList();
        return orders.Select(o => o.Customer.Name).ToList(); // N+1!
    }
}
```

**Fixed Code**:
```csharp
public List<string> GetCustomerNamesForOrders()
{
    using (var db = new DataContext())
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.Customer);
        db.LoadOptions = dlo;

        var orders = db.Orders.Where(o => o.IsActive).ToList();
        return orders.Select(o => o.Customer.Name).ToList(); // Single query with JOIN
    }
}
```

---

### Example 3: Disposed Context Fix

**Input**:
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

        // Force materialization of navigation properties before disposal
        var itemCount = order.OrderDetails.Count();

        return order;
    } // DataContext disposed after all data loaded
}
```

---

## Success Metrics

1. **Bug Detection Rate**: >95% of common LINQ bugs detected
2. **Fix Accuracy**: >90% of fixes work without modification
3. **False Positives**: <5% of flagged issues are not actual bugs
4. **Compilation Success**: 100% of fixed code compiles
5. **Functionality Preservation**: >99% of fixes maintain original behavior

---

**End of Agent Specification**

**Version**: 2.0.0
**Last Updated**: 2026-01-15
**Status**: Production Ready
