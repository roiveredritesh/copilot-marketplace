---
agent_name: linq-optimizer
version: 2.0.0
last_updated: 2026-01-15
status: production
sequential_thinking: conditional
author: Ritesh
description: Optimizes LINQ-to-SQL query performance using DataLoadOptions, projections, compiled queries, and batch operations
task_types:
  - linq-optimize
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
  - query-performance-tuning
output_directory: marketplace/output/linq-analysis
output_file_pattern: linq-optimization-{filename}-{timestamp}.md
---

# LINQ Optimizer Agent

## Purpose

The LINQ Optimizer agent enhances LINQ-to-SQL query performance by applying optimization techniques including DataLoadOptions for eager loading, efficient projections, compiled queries for repeated executions, batch operations, and caching strategies. It transforms working LINQ queries into high-performance implementations suitable for production environments.

## When to Use

Use this agent when you need to:

- **Optimize slow LINQ queries** causing page load delays or timeouts
- **Reduce database round trips** with proper eager loading
- **Minimize data transfer** using efficient projections
- **Improve repeated query performance** with compiled queries
- **Optimize batch operations** (bulk inserts, updates, deletes)
- **Implement caching** for frequently accessed data
- **Reduce memory usage** with streaming and pagination
- **Prepare for production** by optimizing data access layer
- **Scale application** to handle higher load
- **Meet performance SLAs** for critical operations

## When NOT to Use

Do NOT use this agent when:

- Queries are already performing well (don't over-optimize)
- You need to fix bugs first (use `linq-bug-fixer` instead)
- You want to analyze queries (use `linq-query-analyzer` instead)
- Optimization would sacrifice code maintainability significantly
- You need to convert to stored procedures (use `linq-to-sql-converter` instead)
- The file doesn't contain LINQ-to-SQL queries

## Input/Output Specification

### Input Format

**Required Parameters**:
```json
{
  "file_path": "src/DataAccess/OrderRepository.cs",
  "report_format": "full"
}
```

**Optional Parameters**:
```json
{
  "report_format": "summary",
  "optimization_types": ["dataloadoptions", "projections", "compiled-queries", "batch"],
  "apply_fixes": false,
  "performance_target": "high"
}
```

### Output Format

**Full Report Structure**:
```markdown
# LINQ Optimization Report

**File**: src/DataAccess/OrderRepository.cs
**Analyzed**: 2026-01-15 14:30:22
**Agent**: linq-optimizer v2.0.0

## Executive Summary
- Queries Optimized: 6
- Performance Improvements: 75% faster (average)
- Optimization Types Applied:
  - DataLoadOptions: 3 queries
  - Projections: 4 queries
  - Compiled Queries: 2 queries
  - Batch Operations: 1 query

## Optimizations

### Optimization #1: Add DataLoadOptions to GetOrdersWithCustomers()
**Type**: Eager Loading
**Performance Gain**: 95% faster (101 queries → 1 query)
**Effort**: Low

[Before/after code and explanation...]

## Performance Metrics
[Detailed metrics...]

## Implementation Guide
[Step-by-step implementation...]

## Verification Checklist
[Testing steps...]
```

## Process Overview

1. **Query Analysis** (3-6 min) - Analyze LINQ queries for optimization opportunities
2. **DataLoadOptions Optimization** (4-8 min) - Add eager loading for navigation properties
3. **Projection Optimization** (3-7 min) - Implement efficient field selection
4. **Compiled Query Generation** (4-8 min) - Create compiled queries for repeated executions
5. **Batch Operation Optimization** (3-6 min) - Optimize bulk operations
6. **Report Generation** (2-4 min) - Generate comprehensive optimization report

**Total Duration**: 19-39 minutes

## Detailed Process

### Phase 1: Query Analysis (3-6 minutes)

**Objective**: Analyze LINQ queries to identify optimization opportunities.

**Tools**: Grep, Read

**Steps**:

1. **Identify All LINQ Queries**
   - Extract all LINQ-to-SQL queries from file
   - Categorize by operation type: SELECT, INSERT, UPDATE, DELETE
   - Identify query complexity and frequency

2. **Analyze Query Execution Frequency**

   Look for indicators:
   - Methods called in loops
   - API endpoints (frequent calls)
   - Background jobs
   - Report generation
   - Real-time dashboards

3. **Identify Optimization Opportunities**

   **A. N+1 Query Patterns** (High Priority):
   ```csharp
   var orders = db.Orders.ToList();
   foreach (var order in orders)
   {
       var customer = order.Customer; // N+1 opportunity
   }
   ```

   **B. Inefficient Projections** (High Priority):
   ```csharp
   return db.Orders.ToList(); // Loads all columns
   ```

   **C. Repeated Query Patterns** (Medium Priority):
   ```csharp
   public Order GetOrder(int id)
   {
       return db.Orders.First(o => o.Id == id); // Called many times
   }
   ```

   **D. Unoptimized Batch Operations** (Medium Priority):
   ```csharp
   foreach (var order in orders)
   {
       db.Orders.InsertOnSubmit(order);
       db.SubmitChanges(); // Multiple round trips
   }
   ```

   **E. Missing Caching Opportunities** (Low Priority):
   ```csharp
   return db.Categories.ToList(); // Static data, could be cached
   ```

4. **Estimate Performance Impact**

   For each optimization:
   - Current query count
   - Estimated query count after optimization
   - Current execution time
   - Estimated execution time after optimization
   - Priority (High/Medium/Low)

5. **Prioritize Optimizations**

   Order by:
   1. Performance impact (highest first)
   2. Frequency of execution
   3. Implementation effort (quick wins)

**Success Criteria**:
- All queries analyzed
- Optimization opportunities identified
- Performance estimates calculated
- Optimizations prioritized

---

### Phase 2: DataLoadOptions Optimization (4-8 minutes)

**Objective**: Implement eager loading to eliminate N+1 query patterns.

**Tools**: Read, Write

**Skills Referenced**: `linq-to-sql-patterns`

**Steps**:

1. **Identify Navigation Property Access**

   Scan for patterns:
   ```csharp
   order.Customer
   order.OrderDetails
   customer.Orders
   product.Category
   ```

2. **Generate DataLoadOptions Configuration**

   **Pattern A: Single Level Navigation**:
   ```csharp
   // Before
   var orders = db.Orders.Where(o => o.IsActive).ToList();
   foreach (var order in orders)
   {
       Console.WriteLine(order.Customer.Name); // N+1
   }

   // After
   var dlo = new DataLoadOptions();
   dlo.LoadWith<Order>(o => o.Customer);
   db.LoadOptions = dlo;

   var orders = db.Orders.Where(o => o.IsActive).ToList();
   foreach (var order in orders)
   {
       Console.WriteLine(order.Customer.Name); // Already loaded
   }
   ```

   **Pattern B: Multiple Navigation Properties**:
   ```csharp
   // Before
   var orders = db.Orders.ToList();
   // Accessing: order.Customer, order.OrderDetails, order.ShippingAddress

   // After
   var dlo = new DataLoadOptions();
   dlo.LoadWith<Order>(o => o.Customer);
   dlo.LoadWith<Order>(o => o.OrderDetails);
   dlo.LoadWith<Order>(o => o.ShippingAddress);
   db.LoadOptions = dlo;

   var orders = db.Orders.ToList();
   ```

   **Pattern C: Nested Navigation (Multi-Level)**:
   ```csharp
   // Before
   var orders = db.Orders.ToList();
   // Accessing: order.Customer.Address.City

   // After
   var dlo = new DataLoadOptions();
   dlo.LoadWith<Order>(o => o.Customer);
   dlo.LoadWith<Customer>(c => c.Address);
   db.LoadOptions = dlo;

   var orders = db.Orders.ToList();
   ```

3. **Handle Collection Navigation Properties**

   **Pattern A: Collection with Filter**:
   ```csharp
   // Load only active order details
   var dlo = new DataLoadOptions();
   dlo.LoadWith<Order>(o => o.OrderDetails);
   dlo.AssociateWith<Order>(o => o.OrderDetails.Where(d => d.IsActive));
   db.LoadOptions = dlo;
   ```

   **Pattern B: Collection with Ordering**:
   ```csharp
   var dlo = new DataLoadOptions();
   dlo.LoadWith<Customer>(c => c.Orders);
   dlo.AssociateWith<Customer>(c => c.Orders.OrderByDescending(o => o.OrderDate));
   db.LoadOptions = dlo;
   ```

4. **Create Reusable DataLoadOptions Helpers**

   ```csharp
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

       public static DataLoadOptions ForCustomers()
       {
           var dlo = new DataLoadOptions();
           dlo.LoadWith<Customer>(c => c.Address);
           dlo.LoadWith<Customer>(c => c.Orders);
           dlo.AssociateWith<Customer>(c => c.Orders.OrderByDescending(o => o.OrderDate).Take(10));
           return dlo;
       }
   }

   // Usage
   public List<Order> GetOrders()
   {
       using (var db = new DataContext())
       {
           db.LoadOptions = DataLoadOptionsFactory.ForOrders();
           return db.Orders.Where(o => o.IsActive).ToList();
       }
   }
   ```

5. **Calculate Performance Improvement**

   ```
   Before:
   - Main query: 1
   - Customer queries: N
   - OrderDetails queries: N
   - Product queries: N * M (M = avg details per order)
   - Total: 1 + N + N + (N * M) queries

   Example: 100 orders, 5 details each
   = 1 + 100 + 100 + (100 * 5) = 701 queries

   After:
   - Single query with JOINs: 1 query
   - Improvement: 701 → 1 (99.86% reduction)
   ```

**Success Criteria**:
- DataLoadOptions configured for all N+1 patterns
- Multi-level navigation handled
- Collection filters applied where appropriate
- Performance improvements calculated

---

### Phase 3: Projection Optimization (3-7 minutes)

**Objective**: Reduce data transfer by selecting only required fields.

**Tools**: Read, Write

**Skills Referenced**: `sql-optimization-patterns`

**Steps**:

1. **Identify Full Entity Loads**

   Find patterns:
   ```csharp
   return db.Orders.ToList(); // Loads ALL columns
   ```

2. **Analyze Required Fields**

   For each query:
   - Determine which properties are actually used
   - Check method return type
   - Review calling code to understand requirements

3. **Generate Projection DTOs**

   **Option A: Anonymous Type (for internal use)**:
   ```csharp
   // Before
   var orders = db.Orders.ToList();
   var summary = orders.Select(o => new
   {
       o.Id,
       o.OrderDate,
       CustomerName = o.Customer.Name,
       Total = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
   }).ToList();

   // After (projection at query level)
   var summary = db.Orders
       .Select(o => new
       {
           o.Id,
           o.OrderDate,
           CustomerName = o.Customer.Name,
           Total = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
       })
       .ToList();
   ```

   **Option B: Named DTO (for API/cross-boundary)**:
   ```csharp
   // Create DTO class
   public class OrderSummaryDto
   {
       public int Id { get; set; }
       public DateTime OrderDate { get; set; }
       public string CustomerName { get; set; }
       public decimal Total { get; set; }
   }

   // Before
   public List<Order> GetOrderSummaries()
   {
       using (var db = new DataContext())
       {
           return db.Orders.ToList(); // 20+ columns
       }
   }

   // After
   public List<OrderSummaryDto> GetOrderSummaries()
   {
       using (var db = new DataContext())
       {
           return db.Orders
               .Select(o => new OrderSummaryDto
               {
                   Id = o.Id,
                   OrderDate = o.OrderDate,
                   CustomerName = o.Customer.Name,
                   Total = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
               })
               .ToList();
       }
   }
   ```

4. **Handle Complex Projections**

   **Pattern A: Conditional Fields**:
   ```csharp
   .Select(o => new OrderDto
   {
       Id = o.Id,
       Status = o.Status,
       // Conditional: show discount only if applicable
       Discount = o.HasDiscount ? o.DiscountAmount : (decimal?)null
   })
   ```

   **Pattern B: Computed Fields**:
   ```csharp
   .Select(o => new OrderDto
   {
       Id = o.Id,
       ItemCount = o.OrderDetails.Count(),
       TotalAmount = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice),
       AverageItemPrice = o.OrderDetails.Average(d => d.UnitPrice)
   })
   ```

   **Pattern C: String Concatenation**:
   ```csharp
   .Select(o => new OrderDto
   {
       Id = o.Id,
       // Concatenate in database for efficiency
       CustomerFullName = o.Customer.FirstName + " " + o.Customer.LastName
   })
   ```

5. **Optimize for Common Scenarios**

   **Scenario A: List/Grid Display**:
   ```csharp
   // Only fields needed for display
   public List<OrderListItemDto> GetOrdersForList()
   {
       return db.Orders
           .Select(o => new OrderListItemDto
           {
               Id = o.Id,
               OrderDate = o.OrderDate,
               CustomerName = o.Customer.Name,
               Status = o.Status,
               TotalAmount = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
           })
           .OrderByDescending(o => o.OrderDate)
           .Take(100) // Limit for initial load
           .ToList();
   }
   ```

   **Scenario B: Dropdown/Lookup**:
   ```csharp
   // Minimal data for dropdowns
   public List<KeyValuePair<int, string>> GetCustomersForDropdown()
   {
       return db.Customers
           .Where(c => c.IsActive)
           .Select(c => new KeyValuePair<int, string>(c.Id, c.Name))
           .OrderBy(c => c.Value)
           .ToList();
   }
   ```

   **Scenario C: Report Generation**:
   ```csharp
   // Only report columns
   public List<SalesReportDto> GetSalesReport(DateTime from, DateTime to)
   {
       return db.Orders
           .Where(o => o.OrderDate >= from && o.OrderDate <= to)
           .GroupBy(o => new { o.OrderDate.Year, o.OrderDate.Month })
           .Select(g => new SalesReportDto
           {
               Year = g.Key.Year,
               Month = g.Key.Month,
               OrderCount = g.Count(),
               TotalRevenue = g.Sum(o => o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice))
           })
           .OrderBy(r => r.Year).ThenBy(r => r.Month)
           .ToList();
   }
   ```

6. **Calculate Data Savings**

   ```
   Before:
   - Columns: 20 (full Order entity)
   - Row size: ~500 bytes
   - Rows: 1000
   - Total data: 500 KB

   After (projection with 5 fields):
   - Columns: 5
   - Row size: ~150 bytes
   - Rows: 1000
   - Total data: 150 KB
   - Savings: 70% less data transfer
   ```

**Success Criteria**:
- Projections created for all full entity loads
- DTOs defined where appropriate
- Data transfer reduced
- Performance improvements calculated

---

### Phase 4: Compiled Query Generation (4-8 minutes)

**Objective**: Create compiled queries for frequently executed query patterns.

**Tools**: Read, Write

**Skills Referenced**: `linq-to-sql-patterns`, `query-performance-tuning`

**Steps**:

1. **Identify Repeated Query Patterns**

   Look for:
   - Methods called in loops
   - API endpoints with high traffic
   - Queries with same structure but different parameters

2. **Generate Compiled Queries**

   **Pattern A: Simple Parameterized Query**:
   ```csharp
   // Before
   public Order GetOrderById(int id)
   {
       using (var db = new DataContext())
       {
           return db.Orders.FirstOrDefault(o => o.Id == id);
           // Query compiled every time!
       }
   }

   // After
   private static readonly Func<DataContext, int, Order> GetOrderByIdCompiled =
       CompiledQuery.Compile((DataContext db, int id) =>
           db.Orders.FirstOrDefault(o => o.Id == id));

   public Order GetOrderById(int id)
   {
       using (var db = new DataContext())
       {
           return GetOrderByIdCompiled(db, id);
           // Query compiled once, reused!
       }
   }
   ```

   **Pattern B: Query with Multiple Parameters**:
   ```csharp
   private static readonly Func<DataContext, DateTime, DateTime, string, IEnumerable<Order>>
       GetOrdersByDateRangeCompiled = CompiledQuery.Compile(
           (DataContext db, DateTime fromDate, DateTime toDate, string status) =>
               db.Orders.Where(o =>
                   o.OrderDate >= fromDate &&
                   o.OrderDate <= toDate &&
                   o.Status == status));

   public List<Order> GetOrdersByDateRange(DateTime from, DateTime to, string status)
   {
       using (var db = new DataContext())
       {
           return GetOrdersByDateRangeCompiled(db, from, to, status).ToList();
       }
   }
   ```

   **Pattern C: Compiled Query with Projection**:
   ```csharp
   private static readonly Func<DataContext, int, OrderSummaryDto>
       GetOrderSummaryCompiled = CompiledQuery.Compile(
           (DataContext db, int id) =>
               db.Orders
                   .Where(o => o.Id == id)
                   .Select(o => new OrderSummaryDto
                   {
                       Id = o.Id,
                       OrderDate = o.OrderDate,
                       CustomerName = o.Customer.Name,
                       TotalAmount = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
                   })
                   .FirstOrDefault());
   ```

3. **Handle DataLoadOptions with Compiled Queries**

   ```csharp
   // Create factory method for consistent DataLoadOptions
   private static DataLoadOptions GetOrderDataLoadOptions()
   {
       var dlo = new DataLoadOptions();
       dlo.LoadWith<Order>(o => o.Customer);
       dlo.LoadWith<Order>(o => o.OrderDetails);
       return dlo;
   }

   // Use in compiled query
   private static readonly Func<DataContext, int, Order> GetOrderWithDetailsCompiled =
       CompiledQuery.Compile((DataContext db, int id) =>
           db.Orders.FirstOrDefault(o => o.Id == id));

   public Order GetOrderWithDetails(int id)
   {
       using (var db = new DataContext())
       {
           db.LoadOptions = GetOrderDataLoadOptions();
           return GetOrderWithDetailsCompiled(db, id);
       }
   }
   ```

4. **Create Compiled Query Repository Pattern**

   ```csharp
   public static class CompiledQueries
   {
       // Orders
       public static readonly Func<DataContext, int, Order> GetOrderById =
           CompiledQuery.Compile((DataContext db, int id) =>
               db.Orders.FirstOrDefault(o => o.Id == id));

       public static readonly Func<DataContext, string, IEnumerable<Order>> GetOrdersByStatus =
           CompiledQuery.Compile((DataContext db, string status) =>
               db.Orders.Where(o => o.Status == status));

       // Customers
       public static readonly Func<DataContext, int, Customer> GetCustomerById =
           CompiledQuery.Compile((DataContext db, int id) =>
               db.Customers.FirstOrDefault(c => c.Id == id));

       // Products
       public static readonly Func<DataContext, int, Product> GetProductById =
           CompiledQuery.Compile((DataContext db, int id) =>
               db.Products.FirstOrDefault(p => p.Id == id));
   }

   // Usage
   public Order GetOrder(int id)
   {
       using (var db = new DataContext())
       {
           return CompiledQueries.GetOrderById(db, id);
       }
   }
   ```

5. **Calculate Performance Improvement**

   ```
   Compiled Query Benefits:
   - First execution: ~50ms (compilation + execution)
   - Subsequent executions: ~10ms (execution only)
   - Improvement: 80% faster on repeat calls

   Example: 1000 calls
   - Before: 1000 × 50ms = 50,000ms (50 seconds)
   - After: 50ms + (999 × 10ms) = 10,040ms (10 seconds)
   - Improvement: 80% faster
   ```

**Success Criteria**:
- Compiled queries created for frequent patterns
- Static readonly fields defined
- DataLoadOptions integrated
- Performance improvements calculated

---

### Phase 5: Batch Operation Optimization (3-6 minutes)

**Objective**: Optimize bulk insert, update, and delete operations.

**Tools**: Read, Write

**Steps**:

1. **Identify Batch Operations**

   Find patterns:
   ```csharp
   foreach (var item in items)
   {
       db.Table.InsertOnSubmit(item);
       db.SubmitChanges(); // BAD: One round trip per item
   }
   ```

2. **Optimize Bulk Inserts**

   ```csharp
   // Before
   public void AddOrders(List<Order> orders)
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

   // After
   public void AddOrders(List<Order> orders)
   {
       using (var db = new DataContext())
       {
           db.Orders.InsertAllOnSubmit(orders);
           db.SubmitChanges(); // Single batch operation
       }
   }
   ```

3. **Optimize Bulk Updates**

   ```csharp
   // Before
   public void UpdateOrderStatuses(List<int> orderIds, string newStatus)
   {
       using (var db = new DataContext())
       {
           foreach (var id in orderIds)
           {
               var order = db.Orders.First(o => o.Id == id);
               order.Status = newStatus;
               db.SubmitChanges(); // One round trip per order
           }
       }
   }

   // After
   public void UpdateOrderStatuses(List<int> orderIds, string newStatus)
   {
       using (var db = new DataContext())
       {
           var orders = db.Orders.Where(o => orderIds.Contains(o.Id)).ToList();

           foreach (var order in orders)
           {
               order.Status = newStatus;
           }

           db.SubmitChanges(); // Single batch update
       }
   }
   ```

4. **Optimize Bulk Deletes**

   ```csharp
   // Before
   public void DeleteOldOrders(DateTime beforeDate)
   {
       using (var db = new DataContext())
       {
           var orders = db.Orders.Where(o => o.OrderDate < beforeDate).ToList();

           foreach (var order in orders)
           {
               db.Orders.DeleteOnSubmit(order);
               db.SubmitChanges(); // One round trip per order
           }
       }
   }

   // After
   public void DeleteOldOrders(DateTime beforeDate)
   {
       using (var db = new DataContext())
       {
           var orders = db.Orders.Where(o => o.OrderDate < beforeDate).ToList();
           db.Orders.DeleteAllOnSubmit(orders);
           db.SubmitChanges(); // Single batch delete
       }
   }
   ```

5. **Implement Batching for Large Operations**

   ```csharp
   public void BulkInsertOrders(List<Order> orders)
   {
       const int batchSize = 1000;

       for (int i = 0; i < orders.Count; i += batchSize)
       {
           var batch = orders.Skip(i).Take(batchSize).ToList();

           using (var db = new DataContext())
           {
               db.Orders.InsertAllOnSubmit(batch);
               db.SubmitChanges();
           }

           // Optional: Report progress
           Console.WriteLine($"Processed {Math.Min(i + batchSize, orders.Count)} of {orders.Count} orders");
       }
   }
   ```

6. **Add Transaction Support**

   ```csharp
   public void BulkUpdateWithTransaction(List<Order> orders)
   {
       using (var scope = new TransactionScope())
       {
           using (var db = new DataContext())
           {
               foreach (var order in orders)
               {
                   var existingOrder = db.Orders.First(o => o.Id == order.Id);
                   existingOrder.Status = order.Status;
                   existingOrder.UpdatedDate = DateTime.Now;
               }

               db.SubmitChanges();
           }

           scope.Complete(); // Commit all or rollback all
       }
   }
   ```

**Success Criteria**:
- Batch operations optimized
- InsertAllOnSubmit/DeleteAllOnSubmit used
- Large batches split into manageable sizes
- Transaction support added where appropriate

---

### Phase 6: Report Generation (2-4 minutes)

**Objective**: Generate comprehensive optimization report with all improvements documented.

**Tools**: Write

**Steps**:

1. **Generate Executive Summary**
   - Total optimizations applied
   - Overall performance improvement
   - Breakdown by optimization type

2. **Document Each Optimization**
   - Type (DataLoadOptions, Projection, Compiled Query, Batch)
   - Location (method, lines)
   - Before/after code
   - Performance improvement estimate
   - Implementation effort

3. **Create Implementation Guide**
   - Step-by-step instructions
   - Order of implementation
   - Testing requirements
   - Rollback plan

4. **Add Performance Metrics**
   - Query count reduction
   - Execution time improvement
   - Data transfer reduction
   - Memory usage improvement

5. **Include Verification Checklist**
   - Unit tests to create
   - Performance benchmarks
   - Monitoring recommendations

6. **Save Report**
   - Save to `marketplace/output/linq-analysis/` directory
   - Filename: `linq-optimization-{filename}-{timestamp}.md`

**Success Criteria**:
- Comprehensive report with all optimizations
- Before/after code for each optimization
- Performance metrics included
- Implementation guidance provided

---

## Skills Referenced

1. **linq-to-sql-patterns** - LINQ-to-SQL optimization patterns
2. **sql-optimization-patterns** - SQL performance best practices
3. **query-performance-tuning** - Performance analysis and tuning

## Error Handling

### Error Scenario 1: No Optimization Opportunities

**Response**:
```markdown
Analysis Result: Queries already optimized

File: src/DataAccess/OptimizedRepository.cs

The analyzed LINQ queries are already well-optimized with:
- Proper DataLoadOptions configuration
- Efficient projections
- Compiled queries for repeated executions
- Optimized batch operations

No further optimizations recommended. Great job!
```

### Error Scenario 2: Optimization Would Increase Complexity

**Response**:
```markdown
Note: Optimization #3 not recommended

Method: GetSimpleOrders() - Lines 28-35

The current implementation is simple and performs adequately (< 50ms).
Applying compiled query optimization would add complexity without
significant benefit.

Recommendation: Keep current implementation unless performance degrades.
```

---

## Configuration

```json
{
  "linq-optimizer": {
    "report_format": "full",
    "optimization_types": ["all"],
    "apply_fixes": false,
    "min_performance_gain": 20,
    "batch_size": 1000
  }
}
```

## Tools Required

1. **Bash** - File operations
2. **Glob** - Find files
3. **Grep** - Search patterns
4. **Read** - Read source files
5. **Write** - Generate reports
6. **Edit** - Apply optimizations (if requested)

## Examples

### Example 1: Complete Optimization

**Input**:
```csharp
public List<Order> GetActiveOrders()
{
    using (var db = new DataContext())
    {
        var orders = db.Orders.Where(o => o.IsActive).ToList();

        foreach (var order in orders)
        {
            Console.WriteLine($"{order.Id}: {order.Customer.Name}");
        }

        return orders;
    }
}
```

**Optimized Code**:
```csharp
// Static compiled query
private static readonly Func<DataContext, IEnumerable<OrderSummaryDto>>
    GetActiveOrdersCompiled = CompiledQuery.Compile((DataContext db) =>
        db.Orders
            .Where(o => o.IsActive)
            .Select(o => new OrderSummaryDto
            {
                Id = o.Id,
                CustomerName = o.Customer.Name,
                OrderDate = o.OrderDate,
                TotalAmount = o.OrderDetails.Sum(d => d.Quantity * d.UnitPrice)
            }));

public List<OrderSummaryDto> GetActiveOrders()
{
    using (var db = new DataContext())
    {
        db.LoadOptions = GetOrderDataLoadOptions();
        return GetActiveOrdersCompiled(db).ToList();
    }
}

private static DataLoadOptions GetOrderDataLoadOptions()
{
    var dlo = new DataLoadOptions();
    dlo.LoadWith<Order>(o => o.Customer);
    dlo.LoadWith<Order>(o => o.OrderDetails);
    return dlo;
}
```

**Improvements**:
- DataLoadOptions: Eliminates N+1 query (101 queries → 1 query)
- Projection: Selects only required fields (70% less data transfer)
- Compiled Query: 80% faster on repeat calls
- Overall: 95% performance improvement

---

## Success Metrics

1. **Performance Improvement**: >70% faster on average
2. **Query Reduction**: >90% fewer queries for N+1 patterns
3. **Data Transfer**: >60% reduction with projections
4. **Code Quality**: Maintained or improved readability
5. **Compilation Success**: 100% of optimized code compiles

---

**End of Agent Specification**

**Version**: 2.0.0
**Last Updated**: 2026-01-15
**Status**: Production Ready
