# /convert-linq-to-sql Command

## Description

Convert LINQ-to-SQL queries to optimized SQL stored procedures with comprehensive parameter mapping, type conversion, C# integration code, and test plans. Enables migration from LINQ-to-SQL to stored procedures for better performance control and query plan caching.

## Usage

```bash
/convert-linq-to-sql <file-path> <query-name> [--report=full|summary]
```

## Parameters

### Required

- **`<file-path>`**: Path to the C# file containing the LINQ query
  - Must be a valid C# source file (.cs extension)
  - File must contain the target method with LINQ-to-SQL query
  - Example: `src/DataAccess/OrderRepository.cs`

- **`<query-name>`**: Name of the method containing the LINQ query to convert
  - Must match method name exactly (case-sensitive)
  - Example: `GetOrdersWithDetails`

### Optional Flags

- **`--report=full|summary`**: Report detail level (default: `full`)
  - `full` - Comprehensive conversion report with test plan and deployment guide
  - `summary` - Concise conversion summary with SQL and C# code

## Examples

### Example 1: Convert Order Query to Stored Procedure

```bash
/convert-linq-to-sql src/DataAccess/OrderRepository.cs GetOrdersWithDetails --report=full
```

**Input Method**:
```csharp
public List<OrderWithDetails> GetOrdersWithDetails(
    DateTime fromDate,
    DateTime toDate,
    string status)
{
    using (var db = new NorthwindDataContext())
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.Customer);
        dlo.LoadWith<Order>(o => o.OrderDetails);
        db.LoadOptions = dlo;

        return db.Orders
            .Where(o => o.OrderDate >= fromDate
                && o.OrderDate <= toDate
                && o.Status == status)
            .Select(o => new OrderWithDetails
            {
                OrderId = o.Id,
                OrderDate = o.OrderDate,
                CustomerName = o.Customer.Name,
                TotalItems = o.OrderDetails.Count(),
                TotalAmount = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
            })
            .ToList();
    }
}
```

**What it generates**:

1. **SQL Stored Procedure**:
```sql
CREATE PROCEDURE [dbo].[usp_GetOrdersWithDetails]
    @FromDate DATETIME,
    @ToDate DATETIME,
    @Status NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        o.Id AS OrderId,
        o.OrderDate,
        c.Name AS CustomerName,
        COUNT(od.Id) AS TotalItems,
        SUM(od.Quantity * od.UnitPrice) AS TotalAmount
    FROM Orders o
    INNER JOIN Customers c ON o.CustomerId = c.Id
    LEFT JOIN OrderDetails od ON o.Id = od.OrderId
    WHERE o.OrderDate >= @FromDate
        AND o.OrderDate <= @ToDate
        AND o.Status = @Status
    GROUP BY o.Id, o.OrderDate, c.Name
    ORDER BY o.OrderDate DESC
END
```

2. **Parameter Mapping Table**
3. **C# Integration Code** (ADO.NET, Dapper, Async versions)
4. **Test Plan** with sample data
5. **Performance Comparison**
6. **Deployment Instructions**

**Output**: `marketplace/output/linq-analysis/linq-to-sql-conversion-GetOrdersWithDetails-20260115-143022.md`

---

### Example 2: Convert Simple Lookup Query

```bash
/convert-linq-to-sql src/DataAccess/UserRepository.cs GetActiveUsers --report=full
```

**Input Method**:
```csharp
public List<User> GetActiveUsers()
{
    using (var db = new AppDataContext())
    {
        return db.Users
            .Where(u => u.IsActive)
            .OrderBy(u => u.LastName)
            .ToList();
    }
}
```

**Generated Stored Procedure**:
```sql
CREATE PROCEDURE [dbo].[usp_GetActiveUsers]
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        u.Id,
        u.FirstName,
        u.LastName,
        u.Email,
        u.IsActive,
        u.CreatedDate
    FROM Users u
    WHERE u.IsActive = 1
    ORDER BY u.LastName ASC
END
```

**Output**: `marketplace/output/linq-analysis/linq-to-sql-conversion-GetActiveUsers-20260115-143022.md`

---

### Example 3: Convert Complex Report Query with Aggregations

```bash
/convert-linq-to-sql src/DataAccess/ReportRepository.cs GetMonthlySalesReport --report=full
```

**Input Method**:
```csharp
public List<MonthlySalesDto> GetMonthlySalesReport(int year, int month)
{
    using (var db = new SalesDataContext())
    {
        return db.Orders
            .Where(o => o.OrderDate.Year == year && o.OrderDate.Month == month)
            .GroupBy(o => o.Customer.Region)
            .Select(g => new MonthlySalesDto
            {
                Region = g.Key,
                TotalOrders = g.Count(),
                TotalRevenue = g.Sum(o => o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice))
            })
            .OrderByDescending(s => s.TotalRevenue)
            .ToList();
    }
}
```

**Generated Stored Procedure** (with aggregations, GROUP BY, subqueries):
```sql
CREATE PROCEDURE [dbo].[usp_GetMonthlySalesReport]
    @Year INT,
    @Month INT
AS
BEGIN
    SET NOCOUNT ON;

    IF @Month < 1 OR @Month > 12
        THROW 50001, 'Month must be between 1 and 12', 1;

    SELECT
        c.Region,
        COUNT(DISTINCT o.Id) AS TotalOrders,
        SUM(od.Quantity * od.UnitPrice) AS TotalRevenue
    FROM Orders o
    INNER JOIN Customers c ON o.CustomerId = c.Id
    INNER JOIN OrderDetails od ON o.Id = od.OrderId
    WHERE YEAR(o.OrderDate) = @Year
        AND MONTH(o.OrderDate) = @Month
    GROUP BY c.Region
    ORDER BY TotalRevenue DESC
END
```

**Output**: `marketplace/output/linq-analysis/linq-to-sql-conversion-GetMonthlySalesReport-20260115-143022.md`

---

## What This Command Generates

### 1. SQL Stored Procedure
- Optimized T-SQL code
- Proper parameter types with correct sizes
- Error handling and validation
- Index recommendations in comments
- Transaction support (if needed)

### 2. Parameter Mapping
- Complete mapping table: C# types → SQL types
- Nullable handling
- Default values
- Size specifications for strings
- Notes on special conversions

### 3. C# Integration Code

**ADO.NET Version**:
```csharp
public List<OrderDto> GetOrders(DateTime from, DateTime to)
{
    var results = new List<OrderDto>();

    using (var connection = new SqlConnection(connectionString))
    {
        using (var command = new SqlCommand("usp_GetOrders", connection))
        {
            command.CommandType = CommandType.StoredProcedure;
            command.Parameters.AddWithValue("@FromDate", from);
            command.Parameters.AddWithValue("@ToDate", to);

            connection.Open();

            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    results.Add(new OrderDto
                    {
                        Id = reader.GetInt32(0),
                        OrderDate = reader.GetDateTime(1),
                        // ... map all columns
                    });
                }
            }
        }
    }

    return results;
}
```

**Dapper Version**:
```csharp
using Dapper;

public List<OrderDto> GetOrders(DateTime from, DateTime to)
{
    using (var connection = new SqlConnection(connectionString))
    {
        return connection.Query<OrderDto>(
            "usp_GetOrders",
            new { FromDate = from, ToDate = to },
            commandType: CommandType.StoredProcedure
        ).ToList();
    }
}
```

**Async Version**:
```csharp
public async Task<List<OrderDto>> GetOrdersAsync(DateTime from, DateTime to)
{
    // Async implementation provided
}
```

### 4. Test Plan
- Unit test templates
- Integration test scenarios
- Performance test guidance
- Sample test data SQL
- Expected results

### 5. Performance Comparison
- Estimated execution time: LINQ vs Stored Procedure
- Query plan caching benefits
- Network round trip reduction
- Advantages and trade-offs

### 6. Deployment Instructions
- Step-by-step deployment guide
- Rollback plan
- Verification checklist
- Configuration requirements

## Report Contents

### Full Report Includes:
1. **Executive Summary**
   - Conversion status
   - Parameter count
   - MCP validation status (if available)
   - Complexity assessment

2. **Original LINQ Query**
   - Full C# code
   - Highlighted key operations

3. **Generated Stored Procedure**
   - Complete T-SQL code
   - Inline comments
   - Index recommendations

4. **Parameter Mapping**
   - Detailed mapping table
   - Type conversions
   - Validation rules

5. **C# Integration Code**
   - ADO.NET implementation
   - Dapper alternative
   - Async version
   - Connection string config

6. **Test Plan**
   - Test scenarios
   - Sample data
   - Expected results

7. **Performance Comparison**
   - Metrics table
   - Advantages of stored procedure
   - Trade-offs to consider

8. **Deployment Instructions**
   - 5-step deployment process
   - Rollback plan
   - Verification checklist

### Summary Report Includes:
1. **Stored Procedure Code**
2. **C# Integration Code**
3. **Parameter Mapping**
4. **Quick Deployment Steps**

## Output Location

All reports are saved to:
```
marketplace/output/linq-analysis/linq-to-sql-conversion-{query-name}-{timestamp}.md
```

Example:
```
marketplace/output/linq-analysis/linq-to-sql-conversion-GetOrdersWithDetails-20260115-143022.md
```

## MCP Integration

If the **MSSQL MCP server** is configured, the agent will:
- Validate SQL syntax
- Check table and column names exist
- Verify parameter types match database schema
- Analyze query execution plan
- Recommend missing indexes

If MCP is not available:
- Conversion proceeds without validation
- Report notes "MCP validation skipped"
- Manual testing recommended

See `docs/MCP_CONFIGURATION_GUIDE.md` for MCP setup.

## Delegation

This command delegates to the **`linq-to-sql-converter`** agent, which performs:
1. LINQ query parsing
2. SQL stored procedure generation
3. Parameter mapping
4. C# integration code generation
5. MCP validation (if available)
6. Report generation

See `agents/linq-to-sql-converter.md` for detailed agent specification.

## When to Use This Command

Use `/convert-linq-to-sql` when:
- **Critical queries** need better performance control
- **Query plan caching** is desired for consistent performance
- **DBA optimization** required without code redeployment
- **Stored procedure architecture** is preferred
- **Security requirements** demand parameterized stored procedures
- **Legacy system integration** requires stored procedures
- **Performance SLAs** are not met by LINQ queries

## When NOT to Use

Don't use this command when:
- LINQ queries already perform well
- Dynamic query requirements make stored procedures impractical
- Team lacks SQL Server stored procedure expertise
- Query logic changes frequently (better kept in code)
- You need to analyze queries first (use `/analyze-linq` instead)

## Follow-Up Actions

After conversion:

1. **Review Generated Code**
   - Verify SQL logic matches LINQ intent
   - Check parameter types and sizes
   - Review error handling

2. **Test Stored Procedure**
   ```sql
   -- Test in SQL Server Management Studio
   EXEC usp_GetOrdersWithDetails
       @FromDate = '2026-01-01',
       @ToDate = '2026-01-31',
       @Status = 'Active'
   ```

3. **Deploy to Database**
   ```sql
   -- Execute CREATE PROCEDURE statement
   -- in target database
   ```

4. **Update C# Code**
   - Replace LINQ query with ADO.NET/Dapper code
   - Update connection string
   - Test locally

5. **Performance Test**
   ```bash
   # Compare LINQ vs Stored Procedure performance
   # Run benchmarks with production-like data
   ```

## Performance Impact

### Conversion Process
- **Analysis Time**: 8-15 minutes depending on query complexity
- **No Runtime Impact**: Conversion is offline code generation

### Expected Performance Gains
- **Query Plan Caching**: 10-30% faster on repeat executions
- **Reduced Round Trips**: Up to 60% faster for multi-query LINQ
- **DBA Optimization**: Potential for further optimization post-deployment

## Common Use Cases

### Use Case 1: Optimize Critical Report Query
```bash
# Convert slow report query to stored procedure
/convert-linq-to-sql src/DataAccess/ReportRepository.cs GetQuarterlySalesReport --report=full
# Review report, deploy stored procedure, update C# code
```

### Use Case 2: Prepare for Production Scale
```bash
# Convert high-frequency queries before launch
/convert-linq-to-sql src/DataAccess/OrderRepository.cs GetRecentOrders --report=full
/convert-linq-to-sql src/DataAccess/CustomerRepository.cs GetCustomerDashboard --report=full
```

### Use Case 3: DBA Optimization Required
```bash
# Convert to stored procedure so DBA can optimize
/convert-linq-to-sql src/DataAccess/AnalyticsRepository.cs GetUserActivityReport --report=full
```

## Tips

1. **Analyze first**: Run `/analyze-linq` before converting to understand the query
2. **Test thoroughly**: Compare results between LINQ and stored procedure versions
3. **Performance test**: Benchmark with production-like data volume
4. **Keep LINQ code**: Comment out original LINQ code for rollback purposes
5. **Version control**: Store generated SQL in version control with application code

## Troubleshooting

### "Method 'GetOrdersWithDetails' not found"
- Verify method name is exact match (case-sensitive)
- Check method exists in specified file
- Ensure method contains LINQ-to-SQL query

### "Cannot convert dynamic LINQ expression"
- Dynamic LINQ expressions cannot be statically converted
- Consider multiple stored procedures for common filter combinations
- Or use dynamic SQL in stored procedure (with caution)

### "MCP validation failed"
- Review SQL syntax errors in report
- Check table and column names match database
- Verify parameter types are compatible
- Fix issues and re-run conversion

### "Complex query - manual review required"
- Query uses features not directly translatable to SQL
- Review generated SQL with TODO markers
- Complete manual implementation
- Test thoroughly

## Related Commands

- **`/analyze-linq`** - Analyze query before conversion
- **`/optimize-linq`** - Optimize LINQ query instead of converting
- **`/fix-linq-bug`** - Fix bugs before conversion

## Support

For issues or questions:
- Review the conversion report for detailed guidance
- Check `agents/linq-to-sql-converter.md` for agent details
- See `docs/MCP_CONFIGURATION_GUIDE.md` for MCP setup
- Consult `docs/TROUBLESHOOTING.md` for common issues

---

**Command Version**: 2.0.0
**Agent**: linq-to-sql-converter
**Plugin**: linq-to-sql-expert
