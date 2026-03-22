# Skill: LINQ-to-SQL Patterns

## Overview

LINQ-to-SQL is a powerful ORM for .NET Framework that maps database tables to C# classes. However, it has specific patterns, anti-patterns, and optimization techniques that developers must understand to build performant applications. This skill covers best practices, common pitfalls, and migration strategies.

## When to Use This Skill

- **Analyzing LINQ queries** for performance issues
- **Debugging LINQ-to-SQL bugs** like N+1 queries
- **Optimizing data access** in .NET Framework applications
- **Converting LINQ to SQL** stored procedures
- **Code reviewing** LINQ-to-SQL data access code
- **Migrating** from LINQ-to-SQL to Entity Framework or Dapper

## LINQ-to-SQL Architecture

### DataContext
The `DataContext` represents a connection to the database and tracks entity changes.

**Best Practices**:
- Use short-lived DataContext instances (request scope)
- Dispose DataContext after use (using statement)
- Don't share DataContext across threads
- Use connection string from configuration

### Entity Classes
Generated classes that map to database tables.

**Best Practices**:
- Partial classes for custom logic
- Keep entities simple (anemic model)
- Use relationships (foreign keys) properly
- Validate in business layer, not entities

## Common LINQ-to-SQL Patterns

### Pattern 1: Basic Query with Filtering

```csharp
// Good: Efficient single-pass query
using (var db = new MyDataContext())
{
    var users = db.Users
        .Where(u => u.IsActive && u.Department == "IT")
        .Select(u => new {
            u.UserId,
            u.FullName,
            u.Email
        })
        .ToList();
}
```

**Why it works**:
- Single database query
- Projects only needed columns
- Filters in database (WHERE clause)
- Short-lived DataContext

### Pattern 2: Eager Loading with DataLoadOptions

```csharp
// Good: Eager loading prevents N+1
using (var db = new MyDataContext())
{
    var dlo = new DataLoadOptions();
    dlo.LoadWith<Order>(o => o.Customer);
    dlo.LoadWith<Order>(o => o.OrderDetails);
    db.LoadOptions = dlo;

    var orders = db.Orders
        .Where(o => o.OrderDate > DateTime.Now.AddDays(-30))
        .ToList();

    // Customer and OrderDetails already loaded
    foreach (var order in orders)
    {
        Console.WriteLine(order.Customer.Name);
        foreach (var detail in order.OrderDetails)
        {
            Console.WriteLine(detail.ProductName);
        }
    }
}
```

**Why it works**:
- Loads related entities upfront
- Prevents N+1 query problem
- Uses SQL JOINs efficiently

### Pattern 3: Deferred Execution

```csharp
// Query is not executed yet
var query = db.Users.Where(u => u.IsActive);

// Add more filters
if (!string.IsNullOrEmpty(department))
{
    query = query.Where(u => u.Department == department);
}

// Now execute
var users = query.ToList(); // Single SQL query with all filters
```

**Why it works**:
- Composable queries
- Single database roundtrip
- Filters combined in WHERE clause

### Pattern 4: Repository Pattern

```csharp
public class UserRepository : IUserRepository
{
    private readonly string _connectionString;

    public UserRepository(string connectionString)
    {
        _connectionString = connectionString;
    }

    public User GetById(int userId)
    {
        using (var db = new MyDataContext(_connectionString))
        {
            return db.Users.FirstOrDefault(u => u.UserId == userId);
        }
    }

    public List<User> GetActiveUsers()
    {
        using (var db = new MyDataContext(_connectionString))
        {
            return db.Users.Where(u => u.IsActive).ToList();
        }
    }
}
```

**Why it works**:
- Encapsulates data access
- Testable (interface)
- Short-lived DataContext per method
- Separation of concerns

## Common Anti-Patterns

### Anti-Pattern 1: N+1 Query Problem

```csharp
// BAD: Causes N+1 queries
using (var db = new MyDataContext())
{
    var orders = db.Orders.ToList(); // 1 query

    foreach (var order in orders)
    {
        // N queries (one per order)
        var customer = db.Customers.FirstOrDefault(c => c.CustomerId == order.CustomerId);
        Console.WriteLine(customer.Name);
    }
}
```

**Problem**: (1 + N) database queries for N orders

**Fix**: Use DataLoadOptions or Join
```csharp
// GOOD: Single query with JOIN
using (var db = new MyDataContext())
{
    var dlo = new DataLoadOptions();
    dlo.LoadWith<Order>(o => o.Customer);
    db.LoadOptions = dlo;

    var orders = db.Orders.ToList(); // 1 query with JOIN

    foreach (var order in orders)
    {
        Console.WriteLine(order.Customer.Name); // No additional query
    }
}
```

### Anti-Pattern 2: Loading All Records Then Filtering

```csharp
// BAD: Loads all records into memory
using (var db = new MyDataContext())
{
    var users = db.Users.ToList() // Loads ALL users
        .Where(u => u.IsActive && u.Department == "IT");
}
```

**Problem**: Loads entire table into memory, filters in C#

**Fix**: Filter in database
```csharp
// GOOD: Filters in database
using (var db = new MyDataContext())
{
    var users = db.Users
        .Where(u => u.IsActive && u.Department == "IT")
        .ToList(); // Only loads filtered records
}
```

### Anti-Pattern 3: Long-Lived DataContext

```csharp
// BAD: DataContext lives too long
public class UserService
{
    private MyDataContext _db = new MyDataContext(); // Shared instance

    public User GetUser(int id)
    {
        return _db.Users.FirstOrDefault(u => u.UserId == id);
    }
}
```

**Problems**:
- Change tracking bloat
- Memory leaks
- Stale data
- Thread safety issues

**Fix**: Short-lived DataContext
```csharp
// GOOD: New DataContext per method
public class UserService
{
    private readonly string _connectionString;

    public User GetUser(int id)
    {
        using (var db = new MyDataContext(_connectionString))
        {
            return db.Users.FirstOrDefault(u => u.UserId == id);
        }
    }
}
```

### Anti-Pattern 4: Selecting Entire Entities When Not Needed

```csharp
// BAD: Loads all columns
var userNames = db.Users
    .Where(u => u.IsActive)
    .ToList() // Loads all columns
    .Select(u => u.FullName);
```

**Problem**: Loads unnecessary columns

**Fix**: Project in LINQ
```csharp
// GOOD: Projects only needed column
var userNames = db.Users
    .Where(u => u.IsActive)
    .Select(u => u.FullName)
    .ToList(); // Only loads FullName column
```

### Anti-Pattern 5: Implicit Query Execution in Loops

```csharp
// BAD: Query executes on every iteration
foreach (var department in departments)
{
    var count = db.Users.Count(u => u.Department == department); // N queries
}
```

**Fix**: Execute once
```csharp
// GOOD: Single query
var counts = db.Users
    .GroupBy(u => u.Department)
    .Select(g => new { Department = g.Key, Count = g.Count() })
    .ToDictionary(x => x.Department, x => x.Count);

foreach (var department in departments)
{
    var count = counts.ContainsKey(department) ? counts[department] : 0;
}
```

## Performance Optimization Techniques

### Technique 1: Use Compiled Queries

```csharp
// Define compiled query once
private static readonly Func<MyDataContext, int, User> GetUserByIdQuery =
    CompiledQuery.Compile((MyDataContext db, int userId) =>
        db.Users.FirstOrDefault(u => u.UserId == userId));

// Use multiple times (faster than regular query)
using (var db = new MyDataContext())
{
    var user = GetUserByIdQuery(db, 123);
}
```

**Benefits**:
- Query translation cached
- Faster subsequent executions
- Good for frequently-used queries

### Technique 2: Use Projection to DTOs

```csharp
public class UserDto
{
    public int UserId { get; set; }
    public string FullName { get; set; }
    public string Email { get; set; }
}

var users = db.Users
    .Where(u => u.IsActive)
    .Select(u => new UserDto
    {
        UserId = u.UserId,
        FullName = u.FullName,
        Email = u.Email
    })
    .ToList();
```

**Benefits**:
- Loads only needed columns
- No change tracking overhead
- Explicit contract (DTO)

### Technique 3: Use Direct SQL for Complex Queries

```csharp
var results = db.ExecuteQuery<UserSummary>(
    @"SELECT u.UserId, u.FullName, COUNT(o.OrderId) as OrderCount
      FROM Users u
      LEFT JOIN Orders o ON u.UserId = o.UserId
      WHERE u.IsActive = 1
      GROUP BY u.UserId, u.FullName"
);
```

**When to use**:
- Complex aggregations
- Performance-critical queries
- When LINQ generates inefficient SQL

### Technique 4: Batch Operations

```csharp
// Batch inserts
using (var db = new MyDataContext())
{
    db.Users.InsertAllOnSubmit(newUsers);
    db.SubmitChanges(); // Single batch
}

// Batch updates
using (var db = new MyDataContext())
{
    var users = db.Users.Where(u => u.Department == "IT").ToList();
    foreach (var user in users)
    {
        user.IsActive = false;
    }
    db.SubmitChanges(); // Single batch update
}
```

## Converting LINQ to SQL Stored Procedures

### When to Convert
- Query is performance-critical
- Query is complex and frequently used
- Need database-level optimization (indexes, query hints)
- Reduce network traffic
- Centralize business logic

### Conversion Process

**Step 1: Analyze LINQ Query**
```csharp
var orders = db.Orders
    .Where(o => o.OrderDate >= startDate && o.OrderDate <= endDate)
    .Where(o => o.Status == "Completed")
    .Select(o => new
    {
        o.OrderId,
        o.OrderDate,
        CustomerName = o.Customer.Name,
        TotalAmount = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
    })
    .ToList();
```

**Step 2: Generate SQL**

Use SQL Profiler or logging to see generated SQL:
```sql
SELECT o.OrderId, o.OrderDate, c.Name as CustomerName,
       SUM(od.Quantity * od.UnitPrice) as TotalAmount
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId
LEFT JOIN OrderDetails od ON o.OrderId = od.OrderId
WHERE o.OrderDate >= @p0 AND o.OrderDate <= @p1
  AND o.Status = @p2
GROUP BY o.OrderId, o.OrderDate, c.Name
```

**Step 3: Create Stored Procedure**
```sql
CREATE PROCEDURE usp_GetCompletedOrders
    @StartDate DATETIME,
    @EndDate DATETIME,
    @Status NVARCHAR(50)
AS
BEGIN
    SELECT o.OrderId, o.OrderDate, c.Name as CustomerName,
           SUM(od.Quantity * od.UnitPrice) as TotalAmount
    FROM Orders o
    INNER JOIN Customers c ON o.CustomerId = c.CustomerId
    LEFT JOIN OrderDetails od ON o.OrderId = od.OrderId
    WHERE o.OrderDate >= @StartDate AND o.OrderDate <= @EndDate
      AND o.Status = @Status
    GROUP BY o.OrderId, o.OrderDate, c.Name
END
```

**Step 4: Call from LINQ-to-SQL**
```csharp
public class OrderSummary
{
    public int OrderId { get; set; }
    public DateTime OrderDate { get; set; }
    public string CustomerName { get; set; }
    public decimal TotalAmount { get; set; }
}

using (var db = new MyDataContext())
{
    var results = db.ExecuteQuery<OrderSummary>(
        "EXEC usp_GetCompletedOrders @p0, @p1, @p2",
        startDate, endDate, "Completed"
    ).ToList();
}
```

## Migration Strategies

### From LINQ-to-SQL to Entity Framework Core

**Differences**:
- DataContext → DbContext
- DataLoadOptions → Include() method
- Table<T> → DbSet<T>
- SubmitChanges() → SaveChanges()

**Migration Steps**:
1. Create EF Core DbContext
2. Generate entity classes
3. Replace DataContext with DbContext
4. Update query syntax (Include, ThenInclude)
5. Test thoroughly

### From LINQ-to-SQL to Dapper

**When to consider**:
- Need micro-ORM performance
- Want more SQL control
- Reduce ORM complexity

**Example**:
```csharp
// LINQ-to-SQL
using (var db = new MyDataContext())
{
    return db.Users.Where(u => u.IsActive).ToList();
}

// Dapper
using (var conn = new SqlConnection(connectionString))
{
    return conn.Query<User>("SELECT * FROM Users WHERE IsActive = 1").ToList();
}
```

## Debugging LINQ-to-SQL

### View Generated SQL

**Method 1: Log Property**
```csharp
db.Log = Console.Out; // Writes SQL to console
var users = db.Users.Where(u => u.IsActive).ToList();
```

**Method 2: SQL Server Profiler**
- Capture SQL statements
- View execution plans
- Identify performance issues

**Method 3: ToString() Method**
```csharp
var query = db.Users.Where(u => u.IsActive);
var sql = query.ToString(); // Get SQL before execution
```

### Common Issues

**Issue 1: Lazy Loading NullReferenceException**
```csharp
// Problem: DataContext disposed before accessing navigation property
User user;
using (var db = new MyDataContext())
{
    user = db.Users.FirstOrDefault(u => u.UserId == 1);
}
var orders = user.Orders; // NullReferenceException! DataContext disposed
```

**Fix**: Eager load or access inside using block
```csharp
using (var db = new MyDataContext())
{
    var dlo = new DataLoadOptions();
    dlo.LoadWith<User>(u => u.Orders);
    db.LoadOptions = dlo;

    user = db.Users.FirstOrDefault(u => u.UserId == 1);
    var orders = user.Orders; // Works! Loaded with user
}
```

## LINQ-to-SQL Best Practices Checklist

- [ ] Use short-lived DataContext (method scope, request scope)
- [ ] Dispose DataContext properly (using statement)
- [ ] Use DataLoadOptions for related entities
- [ ] Project to DTOs when change tracking not needed
- [ ] Filter in database (.Where before .ToList)
- [ ] Use compiled queries for frequently-used queries
- [ ] Batch Insert/Update/Delete operations
- [ ] Log SQL during development (db.Log)
- [ ] Use stored procedures for complex queries
- [ ] Avoid N+1 query problems
- [ ] Don't load entire tables into memory
- [ ] Use indexes on filtered/joined columns
- [ ] Test with realistic data volumes
- [ ] Monitor SQL Server execution plans

## Key Takeaways

1. **DataContext is short-lived**: Create, use, dispose quickly
2. **Eager load related entities**: Use DataLoadOptions to prevent N+1
3. **Filter in database**: .Where before .ToList
4. **Project when possible**: Select only needed columns
5. **Compiled queries for performance**: Cache query translation
6. **Monitor generated SQL**: Use db.Log or SQL Profiler
7. **Batch operations**: InsertAllOnSubmit, SubmitChanges once
8. **Consider stored procedures**: For complex or critical queries

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: .NET/Legacy Stack
