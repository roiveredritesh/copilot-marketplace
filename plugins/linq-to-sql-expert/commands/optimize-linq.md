# /optimize-linq Command

## Description

Optimize LINQ-to-SQL query performance using DataLoadOptions for eager loading, efficient projections, compiled queries for repeated executions, batch operations, and caching strategies. Transforms working LINQ queries into high-performance implementations.

## Usage

```bash
/optimize-linq <file-path> [--report=full|summary]
```

## Parameters

### Required

- **`<file-path>`**: Path to the C# file containing LINQ-to-SQL queries to optimize
  - Must be a valid C# source file (.cs extension)
  - File should contain working LINQ-to-SQL queries
  - Example: `src/DataAccess/OrderRepository.cs`

### Optional Flags

- **`--report=full|summary`**: Report detail level (default: `full`)
  - `full` - Comprehensive optimization report with metrics, implementation guide, and testing
  - `summary` - Concise optimization summary with before/after code

## Examples

### Example 1: Optimize Repository with N+1 Queries

```bash
/optimize-linq src/DataAccess/OrderRepository.cs --report=full
```

**Input Code** (working but slow):
```csharp
public List<Order> GetOrdersWithCustomers()
{
    using (var db = new DataContext())
    {
        var orders = db.Orders.Where(o => o.IsActive).ToList();

        foreach (var order in orders)
        {
            Console.WriteLine($"Order {order.Id} - {order.Customer.Name}");
        }

        return orders;
    }
}
```

**Optimized Code**:
```csharp
public List<Order> GetOrdersWithCustomers()
{
    using (var db = new DataContext())
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.Customer);
        db.LoadOptions = dlo;

        var orders = db.Orders.Where(o => o.IsActive).ToList();

        foreach (var order in orders)
        {
            Console.WriteLine($"Order {order.Id} - {order.Customer.Name}");
        }

        return orders;
    }
}
```

**Improvements**:
- **Query Count**: 101 queries → 1 query (99% reduction)
- **Execution Time**: ~5 seconds → ~150ms (97% faster)
- **Database Load**: 100 fewer round trips

**Output**: `marketplace/output/linq-analysis/linq-optimization-OrderRepository-20260115-143022.md`

---

### Example 2: Add Projection for Efficient Data Transfer

```bash
/optimize-linq src/DataAccess/CustomerRepository.cs --report=full
```

**Input Code** (loads all columns):
```csharp
public List<Customer> GetCustomersForDropdown()
{
    using (var db = new DataContext())
    {
        return db.Customers
            .Where(c => c.IsActive)
            .OrderBy(c => c.Name)
            .ToList(); // Loads ALL columns (20+)
    }
}
```

**Optimized Code**:
```csharp
public class CustomerDropdownDto
{
    public int Id { get; set; }
    public string Name { get; set; }
}

public List<CustomerDropdownDto> GetCustomersForDropdown()
{
    using (var db = new DataContext())
    {
        return db.Customers
            .Where(c => c.IsActive)
            .Select(c => new CustomerDropdownDto
            {
                Id = c.Id,
                Name = c.Name
            })
            .OrderBy(c => c.Name)
            .ToList(); // Only 2 columns
    }
}
```

**Improvements**:
- **Data Transfer**: 500 KB → 50 KB (90% reduction)
- **Memory Usage**: 70% less
- **Query Performance**: 40% faster

**Output**: `marketplace/output/linq-analysis/linq-optimization-CustomerRepository-20260115-143022.md`

---

### Example 3: Create Compiled Query for High-Frequency Method

```bash
/optimize-linq src/DataAccess/ProductRepository.cs --report=full
```

**Input Code** (called 1000+ times):
```csharp
public Product GetProductById(int id)
{
    using (var db = new DataContext())
    {
        return db.Products.FirstOrDefault(p => p.Id == id);
        // Query compiled EVERY time (expensive)
    }
}
```

**Optimized Code**:
```csharp
// Compiled query - compile once, reuse many times
private static readonly Func<DataContext, int, Product> GetProductByIdCompiled =
    CompiledQuery.Compile((DataContext db, int id) =>
        db.Products.FirstOrDefault(p => p.Id == id));

public Product GetProductById(int id)
{
    using (var db = new DataContext())
    {
        return GetProductByIdCompiled(db, id);
        // Reuses compiled query plan
    }
}
```

**Improvements**:
- **First Call**: ~50ms (compilation + execution)
- **Subsequent Calls**: ~10ms (execution only)
- **Improvement**: 80% faster on repeat calls
- **For 1000 calls**: 50 seconds → 10 seconds

**Output**: `marketplace/output/linq-analysis/linq-optimization-ProductRepository-20260115-143022.md`

---

### Example 4: Optimize Batch Operations

```bash
/optimize-linq src/Services/OrderImportService.cs --report=full
```

**Input Code** (slow batch insert):
```csharp
public void ImportOrders(List<Order> orders)
{
    using (var db = new DataContext())
    {
        foreach (var order in orders)
        {
            db.Orders.InsertOnSubmit(order);
            db.SubmitChanges(); // 100 round trips for 100 orders
        }
    }
}
```

**Optimized Code**:
```csharp
public void ImportOrders(List<Order> orders)
{
    const int batchSize = 1000;

    for (int i = 0; i < orders.Count; i += batchSize)
    {
        var batch = orders.Skip(i).Take(batchSize).ToList();

        using (var db = new DataContext())
        {
            db.Orders.InsertAllOnSubmit(batch);
            db.SubmitChanges(); // Single batch operation
        }
    }
}
```

**Improvements**:
- **Round Trips**: 100 → 1 (per 1000 records)
- **Execution Time**: 50 seconds → 5 seconds (90% faster)
- **Database Load**: Significantly reduced

**Output**: `marketplace/output/linq-analysis/linq-optimization-OrderImportService-20260115-143022.md`

---

## Optimization Types Applied

### 1. DataLoadOptions (Eager Loading)
- **Problem**: N+1 queries from lazy loading
- **Solution**: Configure `DataLoadOptions` to eager load navigation properties
- **Benefit**: 90-99% query reduction, 80-97% faster

### 2. Efficient Projections
- **Problem**: Loading entire entities when only few fields needed
- **Solution**: Use `.Select()` to project only required fields into DTOs
- **Benefit**: 60-90% less data transfer, 30-50% faster, lower memory usage

### 3. Compiled Queries
- **Problem**: Query compilation overhead on repeated executions
- **Solution**: Use `CompiledQuery.Compile()` for frequently called queries
- **Benefit**: 80% faster on repeat calls, consistent performance

### 4. Batch Operations
- **Problem**: Multiple round trips for bulk inserts/updates/deletes
- **Solution**: Use `InsertAllOnSubmit()`, batch operations, single `SubmitChanges()`
- **Benefit**: 90%+ faster for bulk operations, reduced database load

### 5. Query Caching (when appropriate)
- **Problem**: Repeated queries for static data
- **Solution**: Cache results for lookup data, categories, etc.
- **Benefit**: Near-instant retrieval, reduced database load

## Report Contents

### Full Report Includes:

1. **Executive Summary**
   - Total optimizations applied
   - Overall performance improvement estimate
   - Breakdown by optimization type

2. **Optimizations Section**
   For each optimization:
   - **Title**: Descriptive name
   - **Type**: DataLoadOptions, Projection, Compiled Query, Batch, Cache
   - **Location**: Method name, line numbers
   - **Performance Gain**: Estimated improvement (query count, time, data transfer)
   - **Effort**: Low/Medium/High
   - **Priority**: Critical/High/Medium/Low
   - **Before Code**: Current implementation
   - **After Code**: Optimized implementation
   - **Explanation**: Why optimization works
   - **Metrics**: Detailed performance metrics

3. **Performance Metrics**
   - **Query Count**: Before vs. After
   - **Execution Time**: Estimated improvement
   - **Data Transfer**: Size reduction
   - **Memory Usage**: Reduction estimate

4. **Implementation Guide**
   - Step-by-step implementation instructions
   - Order of implementation (prioritized)
   - Testing requirements for each optimization
   - Rollback plan

5. **Code Examples**
   - Complete before/after examples
   - Helper classes/methods
   - Reusable patterns (DataLoadOptions factory, compiled query repository)

6. **Verification Checklist**
   - Unit tests to create
   - Performance benchmarks to run
   - Integration tests
   - Monitoring setup

7. **Recommendations**
   - Immediate actions (critical optimizations)
   - Short-term improvements
   - Long-term enhancements

### Summary Report Includes:
1. **Optimizations Applied**
   - Count and types
   - Overall improvement estimate

2. **Code Changes**
   - Before/after for each optimization

3. **Next Steps**
   - Quick implementation checklist

## Output Location

All reports are saved to:
```
marketplace/output/linq-analysis/linq-optimization-{filename}-{timestamp}.md
```

Example:
```
marketplace/output/linq-analysis/linq-optimization-OrderRepository-20260115-143022.md
```

## Delegation

This command delegates to the **`linq-optimizer`** agent, which performs:
1. Query analysis for optimization opportunities
2. DataLoadOptions generation
3. Projection optimization
4. Compiled query creation
5. Batch operation optimization
6. Report generation

See `agents/linq-optimizer.md` for detailed agent specification.

## When to Use This Command

Use `/optimize-linq` when you need to:
- **Improve slow page loads** caused by inefficient LINQ queries
- **Reduce database load** from excessive queries
- **Prepare for production** by optimizing data access layer
- **Scale application** to handle more users
- **Meet performance SLAs** for critical operations
- **Reduce costs** by minimizing database resource usage
- **Optimize before launch** to ensure good performance from day one

## When NOT to Use

Don't use this command when:
- Queries are already performing well (don't over-optimize)
- You need to fix bugs first (use `/fix-linq-bug` instead)
- You want to analyze issues first (use `/analyze-linq` instead)
- Optimization would sacrifice maintainability significantly
- You need to convert to stored procedures (use `/convert-linq-to-sql` instead)

## Performance Impact

### Optimization Process
- **Analysis Time**: 10-20 minutes depending on file complexity
- **No Runtime Impact**: Optimization is code generation only

### Expected Performance Gains
- **N+1 Query Fixes**: 90-99% query reduction, 80-97% faster
- **Projection Optimizations**: 60-90% less data transfer, 30-50% faster
- **Compiled Queries**: 80% faster on repeat calls
- **Batch Operations**: 90%+ faster for bulk operations

## Common Optimization Patterns

### Pattern 1: DataLoadOptions for N+1 Prevention
```csharp
// Helper factory pattern
public static class DataLoadOptionsFactory
{
    public static DataLoadOptions ForOrders()
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.Customer);
        dlo.LoadWith<Order>(o => o.OrderDetails);
        dlo.LoadWith<OrderDetail>(d => d.Product);
        return dlo;
    }
}

// Usage
using (var db = new DataContext())
{
    db.LoadOptions = DataLoadOptionsFactory.ForOrders();
    var orders = db.Orders.Where(o => o.IsActive).ToList();
}
```

### Pattern 2: Projection DTOs
```csharp
// Create lightweight DTO
public class OrderSummaryDto
{
    public int Id { get; set; }
    public DateTime OrderDate { get; set; }
    public string CustomerName { get; set; }
    public decimal TotalAmount { get; set; }
}

// Use projection
return db.Orders
    .Select(o => new OrderSummaryDto
    {
        Id = o.Id,
        OrderDate = o.OrderDate,
        CustomerName = o.Customer.Name,
        TotalAmount = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
    })
    .ToList();
```

### Pattern 3: Compiled Query Repository
```csharp
public static class CompiledQueries
{
    public static readonly Func<DataContext, int, Order> GetOrderById =
        CompiledQuery.Compile((DataContext db, int id) =>
            db.Orders.FirstOrDefault(o => o.Id == id));

    public static readonly Func<DataContext, string, IEnumerable<Order>> GetOrdersByStatus =
        CompiledQuery.Compile((DataContext db, string status) =>
            db.Orders.Where(o => o.Status == status));
}
```

### Pattern 4: Batched Operations
```csharp
public void BulkInsert<T>(List<T> entities) where T : class
{
    const int batchSize = 1000;

    for (int i = 0; i < entities.Count; i += batchSize)
    {
        var batch = entities.Skip(i).Take(batchSize).ToList();

        using (var db = new DataContext())
        {
            db.GetTable<T>().InsertAllOnSubmit(batch);
            db.SubmitChanges();
        }
    }
}
```

## Follow-Up Actions

After receiving optimization report:

1. **Review Optimizations**
   - Understand each optimization
   - Verify it doesn't break functionality

2. **Implement in Priority Order**
   - Start with critical optimizations (highest impact)
   - Test each optimization independently
   - Commit changes incrementally

3. **Performance Test**
   ```csharp
   // Before optimization
   var sw = Stopwatch.StartNew();
   var orders = GetOrders();
   sw.Stop();
   Console.WriteLine($"Before: {sw.ElapsedMilliseconds}ms");

   // After optimization
   sw.Restart();
   var orders = GetOrdersOptimized();
   sw.Stop();
   Console.WriteLine($"After: {sw.ElapsedMilliseconds}ms");
   ```

4. **Benchmark with Real Data**
   - Test with production-like data volume
   - Measure query count using SQL Profiler
   - Monitor memory usage

5. **Deploy and Monitor**
   - Deploy to staging first
   - Monitor performance metrics
   - Deploy to production after validation

## Common Use Cases

### Use Case 1: Optimize Slow Dashboard
```bash
# Dashboard loading slow due to N+1 queries
/optimize-linq src/DataAccess/DashboardRepository.cs --report=full

# Implement DataLoadOptions optimizations
# Test with production data volume
# Deploy to staging and monitor
```

### Use Case 2: Optimize Before Production Launch
```bash
# Optimize all data access before launch
/optimize-linq src/DataAccess/OrderRepository.cs --report=full
/optimize-linq src/DataAccess/CustomerRepository.cs --report=full
/optimize-linq src/DataAccess/ProductRepository.cs --report=full

# Review reports, implement critical optimizations
# Performance test all optimizations
# Deploy with confidence
```

### Use Case 3: Reduce Database Load
```bash
# Database CPU at 80%, investigate queries
/analyze-linq src/DataAccess/ReportRepository.cs --report=full
/optimize-linq src/DataAccess/ReportRepository.cs --report=full

# Apply optimizations
# Monitor database CPU reduction
```

## Tips

1. **Analyze first**: Run `/analyze-linq` before optimizing to understand issues
2. **Test thoroughly**: Performance test each optimization
3. **Prioritize**: Implement high-impact optimizations first
4. **Measure**: Use SQL Profiler to verify query count reduction
5. **Incremental**: Apply optimizations one at a time and test
6. **Monitor**: Set up performance monitoring in production

## Benchmarking Example

```csharp
using System.Diagnostics;

public class PerformanceBenchmark
{
    public void ComparePerformance()
    {
        // Test original version
        var sw = Stopwatch.StartNew();
        var originalOrders = GetOrders_Original();
        sw.Stop();
        var originalTime = sw.ElapsedMilliseconds;
        var originalQueryCount = GetQueryCount(); // Use SQL Profiler

        // Test optimized version
        sw.Restart();
        var optimizedOrders = GetOrders_Optimized();
        sw.Stop();
        var optimizedTime = sw.ElapsedMilliseconds;
        var optimizedQueryCount = GetQueryCount(); // Use SQL Profiler

        // Report results
        Console.WriteLine($"Original: {originalTime}ms, {originalQueryCount} queries");
        Console.WriteLine($"Optimized: {optimizedTime}ms, {optimizedQueryCount} queries");
        Console.WriteLine($"Improvement: {(1 - (double)optimizedTime / originalTime) * 100:F1}% faster");
        Console.WriteLine($"Query reduction: {originalQueryCount - optimizedQueryCount} queries saved");
    }
}
```

## Troubleshooting

### "No optimization opportunities found"
- Queries are already well-optimized (great!)
- File may not contain LINQ-to-SQL queries
- Try analyzing other files

### "Optimization would reduce maintainability"
- Agent detected trade-off between performance and code clarity
- Review report for alternative approaches
- Consider if optimization is truly needed

### "Performance gain less than expected"
- Data volume may be different than tested
- Database may have other bottlenecks
- Review execution plans to verify optimization

## Related Commands

- **`/analyze-linq`** - Analyze queries before optimizing
- **`/fix-linq-bug`** - Fix bugs before optimizing
- **`/convert-linq-to-sql`** - Convert to stored procedures for ultimate control

## Support

For issues or questions:
- Review the optimization report for detailed guidance
- Check `agents/linq-optimizer.md` for agent details
- See `docs/TROUBLESHOOTING.md` for common issues
- Consult `skills/linq-to-sql-patterns.md` for best practices

---

**Command Version**: 2.0.0
**Agent**: linq-optimizer
**Plugin**: linq-to-sql-expert
