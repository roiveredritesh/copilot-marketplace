# Skill: Performance Analysis Framework

## Overview

Performance analysis is a systematic methodology for identifying, analyzing, and resolving performance bottlenecks in software systems. This framework provides structured approaches for profiling applications, measuring performance metrics, identifying bottlenecks, and implementing optimizations across CPU, memory, I/O, and network resources.

## When to Use This Skill

- **Slow application response times**: Pages loading slowly or operations timing out
- **High resource consumption**: CPU, memory, or disk usage abnormally high
- **Scalability issues**: Performance degrades with increased load
- **Database query slowness**: Queries taking longer than expected
- **API latency problems**: API calls exceeding SLA thresholds
- **User complaints**: End users reporting sluggish application behavior
- **Pre-release optimization**: Proactive performance tuning before deployment
- **Capacity planning**: Understanding resource requirements for scaling

## Performance Analysis Process

### Phase 1: Establish Performance Baseline

**What to do**:
1. Define performance requirements and SLAs
2. Identify critical user workflows
3. Measure current performance metrics
4. Document baseline measurements
5. Set performance targets

**Key Metrics to Baseline**:
- Response time (p50, p95, p99 percentiles)
- Throughput (requests per second)
- Error rate
- Resource utilization (CPU, memory, disk, network)
- Database query execution time
- API call latency

**Baseline Documentation Template**:
```
Operation: [e.g., Load Order Details Page]
Current Performance:
  - Average Response Time: 2.5s
  - p95 Response Time: 4.2s
  - p99 Response Time: 6.8s
  - Throughput: 10 req/sec
  - CPU Usage: 45%
  - Memory Usage: 1.2GB
Target Performance:
  - Average Response Time: < 1s
  - p95 Response Time: < 2s
  - p99 Response Time: < 3s
  - Throughput: 50 req/sec
```

### Phase 2: Reproduce and Measure

**Reproduce the Issue**:
1. Identify steps to trigger slow performance
2. Isolate the operation or workflow
3. Create repeatable test scenario
4. Ensure test data is realistic (volume, variety)

**Measurement Strategy**:

**Application-Level Timing**:
```csharp
var stopwatch = Stopwatch.StartNew();
try
{
    // Operation to measure
    var result = ProcessOrder(orderId);
    return result;
}
finally
{
    stopwatch.Stop();
    Logger.LogPerformance("ProcessOrder", stopwatch.ElapsedMilliseconds, orderId);
}
```

**Database Query Timing**:
```sql
SET STATISTICS TIME ON;
SET STATISTICS IO ON;

-- Your query here
SELECT * FROM Orders WHERE CustomerId = @CustomerId;

-- Review output:
-- SQL Server Execution Times: CPU time, elapsed time
-- Table scan count, logical reads, physical reads
```

**HTTP Request Timing**:
- Use browser DevTools Network tab
- Record HAR files for analysis
- Use tools like Fiddler or Postman
- Check Server-Timing headers

### Phase 3: Identify Bottleneck Type

**CPU-Bound Bottlenecks**:

**Symptoms**:
- High CPU utilization (> 80%)
- CPU pegged at 100% during operation
- Application slows down under load
- Performance scales poorly with CPU cores

**Common Causes**:
- Inefficient algorithms (poor time complexity)
- Excessive string operations or concatenation
- Complex regular expressions
- Heavy computational logic
- Inefficient loops and iterations
- Lack of caching for computed values

**Investigation Tools**:
- CPU profilers (dotTrace, Visual Studio Profiler, PerfView)
- Performance counters (% Processor Time)
- Sampling profilers to identify hot paths

**Example - Inefficient Algorithm**:
```csharp
// BAD: O(n²) complexity
public List<Order> FindDuplicates(List<Order> orders)
{
    var duplicates = new List<Order>();
    for (int i = 0; i < orders.Count; i++)
    {
        for (int j = i + 1; j < orders.Count; j++)
        {
            if (orders[i].OrderNumber == orders[j].OrderNumber)
                duplicates.Add(orders[j]);
        }
    }
    return duplicates;
}

// GOOD: O(n) complexity using HashSet
public List<Order> FindDuplicates(List<Order> orders)
{
    var seen = new HashSet<string>();
    var duplicates = new List<Order>();

    foreach (var order in orders)
    {
        if (!seen.Add(order.OrderNumber))
            duplicates.Add(order);
    }
    return duplicates;
}
```

**Memory-Bound Bottlenecks**:

**Symptoms**:
- High memory usage (> 80% of available RAM)
- Frequent garbage collections
- OutOfMemoryException
- Application slows down over time
- High Gen 2 GC collections

**Common Causes**:
- Memory leaks (objects not disposed)
- Loading too much data into memory
- Large object allocations (> 85KB)
- Excessive string concatenation
- Event handler leaks
- Static collection growth

**Investigation Tools**:
- Memory profilers (dotMemory, ANTS Memory Profiler)
- Performance counters (Private Bytes, Gen 0/1/2 Collections)
- Memory snapshots and diff analysis
- Heap dump analysis

**Example - Memory Leak**:
```csharp
// BAD: Event handler leak
public class OrderProcessor
{
    public OrderProcessor()
    {
        // Event handler never unsubscribed - keeps OrderProcessor alive
        GlobalEventBus.OnOrderReceived += HandleOrder;
    }

    private void HandleOrder(object sender, OrderEventArgs e)
    {
        // Process order
    }
}

// GOOD: Proper cleanup
public class OrderProcessor : IDisposable
{
    public OrderProcessor()
    {
        GlobalEventBus.OnOrderReceived += HandleOrder;
    }

    public void Dispose()
    {
        GlobalEventBus.OnOrderReceived -= HandleOrder;
    }

    private void HandleOrder(object sender, OrderEventArgs e)
    {
        // Process order
    }
}
```

**I/O-Bound Bottlenecks**:

**Symptoms**:
- High disk queue length
- Slow file operations
- Database query timeouts
- Low CPU usage but slow performance
- High disk % active time

**Common Causes**:
- Synchronous I/O operations
- Excessive database roundtrips (N+1 queries)
- Lack of connection pooling
- Large file reads without streaming
- No caching of frequently accessed data
- Slow network drives or database servers

**Investigation Tools**:
- Disk performance counters (Avg. Disk Queue Length, Disk Bytes/sec)
- Database profilers (SQL Server Profiler, pg_stat_statements)
- Network monitoring tools
- I/O tracing tools

**Example - Synchronous I/O**:
```csharp
// BAD: Synchronous blocking I/O
public string GetFileContent(string path)
{
    return File.ReadAllText(path); // Blocks thread
}

public List<Order> GetOrders()
{
    using (var db = new DataContext())
    {
        return db.Orders.ToList(); // Synchronous database call
    }
}

// GOOD: Asynchronous I/O
public async Task<string> GetFileContentAsync(string path)
{
    return await File.ReadAllTextAsync(path); // Non-blocking
}

public async Task<List<Order>> GetOrdersAsync()
{
    using (var db = new DataContext())
    {
        return await db.Orders.ToListAsync(); // Async database call
    }
}
```

**Network-Bound Bottlenecks**:

**Symptoms**:
- Slow API responses
- High network latency
- Timeout errors
- Inconsistent performance across locations
- High network % utilization

**Common Causes**:
- Chatty API calls (many small requests)
- Large payload sizes
- Missing compression
- No CDN for static assets
- Geographic distance from server
- Network bandwidth limitations

**Investigation Tools**:
- Browser DevTools Network tab
- Fiddler, Charles Proxy, Wireshark
- Network performance counters
- API gateway metrics

**Example - Chatty API**:
```csharp
// BAD: Multiple API calls in loop (N+1 HTTP requests)
public async Task<List<CustomerDetails>> GetCustomerDetailsAsync(List<int> customerIds)
{
    var details = new List<CustomerDetails>();
    foreach (var id in customerIds)
    {
        var response = await httpClient.GetAsync($"/api/customers/{id}"); // N network calls
        var customer = await response.Content.ReadAsAsync<CustomerDetails>();
        details.Add(customer);
    }
    return details;
}

// GOOD: Batch API call (single HTTP request)
public async Task<List<CustomerDetails>> GetCustomerDetailsAsync(List<int> customerIds)
{
    var ids = string.Join(",", customerIds);
    var response = await httpClient.GetAsync($"/api/customers/batch?ids={ids}"); // 1 network call
    return await response.Content.ReadAsAsync<List<CustomerDetails>>();
}
```

### Phase 4: Deep Dive Analysis

**CPU Profiling**:

**Using Visual Studio Profiler**:
1. Debug > Performance Profiler
2. Select "CPU Usage"
3. Start profiling
4. Reproduce the slow operation
5. Stop profiling
6. Analyze hot path (functions consuming most CPU time)
7. Review call tree to find expensive operations

**Key Metrics**:
- **Self Time**: Time spent in function itself (excluding callees)
- **Total Time**: Time spent in function and all callees
- **Call Count**: Number of times function was called
- **Hot Path**: Code path consuming most CPU time

**Memory Profiling**:

**Using dotMemory**:
1. Take memory snapshot (baseline)
2. Perform operation
3. Take another snapshot
4. Compare snapshots to find memory growth
5. Identify objects not being garbage collected
6. Trace object retention path

**Key Metrics**:
- **Total Bytes**: Memory allocated
- **Object Count**: Number of instances
- **Gen 2 Size**: Long-lived objects (potential leaks)
- **Retention Path**: Why object is kept alive

**Database Profiling**:

**Using SQL Server Profiler / Extended Events**:
1. Start trace capturing queries
2. Reproduce slow operation
3. Stop trace
4. Identify slow queries (duration > threshold)
5. Analyze execution plans
6. Check for table scans, missing indexes

**Key Metrics**:
- **Duration**: Total query execution time
- **CPU Time**: CPU time consumed by query
- **Logical Reads**: Number of pages read from cache
- **Physical Reads**: Number of pages read from disk
- **Row Count**: Number of rows returned

**Example - Analyzing Execution Plan**:
```sql
-- Enable actual execution plan in SSMS (Ctrl+M)
SELECT o.OrderId, o.OrderDate, c.CustomerName, SUM(od.Quantity * od.UnitPrice) as Total
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId
LEFT JOIN OrderDetails od ON o.OrderId = od.OrderId
WHERE o.OrderDate >= '2025-01-01'
GROUP BY o.OrderId, o.OrderDate, c.CustomerName
ORDER BY o.OrderDate DESC;

-- Review execution plan:
-- - Look for "Table Scan" (BAD - should be Index Seek)
-- - Check "Estimated Rows" vs "Actual Rows" (indicates stale statistics)
-- - Look for "Sort" operations (can be expensive)
-- - Check for "Hash Match" with warnings
-- - Review "Missing Index" hints
```

### Phase 5: Identify Root Cause

**Ask the 5 Whys**:
1. **Why is the page slow?** Because the database query takes 5 seconds
2. **Why does the query take 5 seconds?** Because it's doing a table scan on 1M rows
3. **Why is it doing a table scan?** Because there's no index on the filtered column
4. **Why is there no index?** Because the column was added recently
5. **Why wasn't the index added?** Because index creation wasn't part of the migration

**Root Cause**: Missing index on new column

**Common Root Causes**:

| Symptom | Common Root Causes |
|---------|-------------------|
| Slow query | Missing indexes, N+1 queries, poor schema design, stale statistics |
| High CPU | Inefficient algorithms, excessive string operations, missing caching |
| High memory | Memory leaks, loading too much data, large object allocations |
| Slow API | Chatty calls, large payloads, network latency, missing compression |
| Slow page load | Too many HTTP requests, large assets, no CDN, blocking JavaScript |

### Phase 6: Develop Optimization Strategy

**Prioritization Matrix**:

| Impact | Effort | Priority | Example |
|--------|--------|----------|---------|
| High | Low | 🔴 **Critical** - Do First | Add missing index |
| High | High | 🟡 **Important** - Plan Carefully | Redesign data model |
| Low | Low | 🔵 **Quick Win** - Do When Possible | Enable compression |
| Low | High | ⚪ **Low Priority** - Defer | Micro-optimization |

**Optimization Strategies by Type**:

**CPU Optimization**:
- Use more efficient algorithms (reduce time complexity)
- Cache computed results
- Use StringBuilder for string concatenation
- Optimize regular expressions
- Parallelize CPU-intensive operations
- Use compiled expressions/queries

**Memory Optimization**:
- Implement proper disposal patterns (IDisposable)
- Use object pooling for frequently allocated objects
- Stream large files instead of loading into memory
- Paginate large result sets
- Use weak references for caches
- Reduce object allocations in hot paths

**I/O Optimization**:
- Use asynchronous I/O operations
- Implement database query caching
- Use connection pooling
- Batch database operations
- Enable query result caching
- Use CDN for static content
- Implement lazy loading

**Network Optimization**:
- Batch API calls
- Enable HTTP compression (gzip, brotli)
- Implement API response caching
- Use CDN for global distribution
- Reduce payload size (minimize JSON, remove unused fields)
- Use HTTP/2 or HTTP/3 for multiplexing

## Performance Testing Strategies

### Load Testing

**Purpose**: Verify system performance under expected load

**Tools**:
- JMeter
- k6
- Gatling
- Azure Load Testing

**Test Scenarios**:
```
Scenario: Order Processing Load Test
- Virtual Users: 100 concurrent users
- Ramp-up: 10 users every 10 seconds
- Duration: 10 minutes
- Operations:
  - Search products (40%)
  - View product details (30%)
  - Add to cart (20%)
  - Checkout (10%)
- Success Criteria:
  - p95 response time < 2s
  - Error rate < 1%
  - Throughput > 50 req/sec
```

### Stress Testing

**Purpose**: Determine breaking point and failure behavior

**Approach**:
1. Start with normal load
2. Gradually increase load beyond expected maximum
3. Identify point where system degrades
4. Observe how system fails (graceful vs catastrophic)
5. Verify recovery after load reduction

### Soak Testing

**Purpose**: Detect memory leaks and performance degradation over time

**Approach**:
1. Run at moderate load (60-80% of max)
2. Duration: 24-48 hours
3. Monitor memory usage over time
4. Check for gradual performance degradation
5. Verify garbage collection patterns

### Spike Testing

**Purpose**: Test system behavior under sudden load increases

**Approach**:
1. Start with normal load
2. Suddenly increase to peak load
3. Hold peak for short period
4. Drop back to normal
5. Verify system handles spike and recovers

## Performance Monitoring Tools

### Application Performance Monitoring (APM)

**Application Insights (Azure)**:
- End-to-end transaction tracing
- Dependency tracking (database, HTTP calls)
- Performance counter collection
- Custom metric tracking
- Automatic anomaly detection

**New Relic**:
- Real-time performance dashboards
- Transaction traces
- Error tracking
- Infrastructure monitoring

**Datadog**:
- Full-stack monitoring
- Log aggregation
- Metric correlation
- Custom dashboards

### Database Monitoring

**SQL Server**:
- SQL Server Profiler (legacy)
- Extended Events (modern)
- Query Store (query performance history)
- Dynamic Management Views (DMVs)
- Performance Dashboard Reports

**Performance Counters**:
```
-- Find most expensive queries
SELECT TOP 10
    qs.execution_count,
    qs.total_elapsed_time / qs.execution_count as avg_elapsed_time,
    qs.total_worker_time / qs.execution_count as avg_cpu_time,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset
            WHEN -1 THEN DATALENGTH(qt.text)
            ELSE qs.statement_end_offset
        END - qs.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;
```

### Code-Level Profiling

**Visual Studio Profiler**:
- CPU Usage
- Memory Usage
- .NET Object Allocation
- Database queries

**dotTrace (JetBrains)**:
- Sampling profiling
- Tracing profiling
- Line-by-line profiling
- Timeline profiling

**PerfView**:
- ETW-based profiling
- CPU sampling
- GC allocation tracking
- Thread time analysis

## Common Performance Patterns

### Pattern 1: Query Result Caching

**Use When**: Data changes infrequently, query is expensive

```csharp
public class ProductRepository
{
    private readonly IMemoryCache _cache;
    private readonly TimeSpan _cacheExpiration = TimeSpan.FromMinutes(15);

    public async Task<List<Product>> GetFeaturedProductsAsync()
    {
        const string cacheKey = "FeaturedProducts";

        if (_cache.TryGetValue(cacheKey, out List<Product> products))
        {
            return products; // Return cached result
        }

        // Cache miss - query database
        using (var db = new DataContext())
        {
            products = await db.Products
                .Where(p => p.IsFeatured)
                .ToListAsync();

            _cache.Set(cacheKey, products, _cacheExpiration);
            return products;
        }
    }
}
```

### Pattern 2: Lazy Loading with Caching

**Use When**: Data might not be needed, but if needed, should be cached

```csharp
public class CustomerService
{
    private readonly Lazy<Dictionary<int, Customer>> _customerCache;

    public CustomerService()
    {
        _customerCache = new Lazy<Dictionary<int, Customer>>(() =>
        {
            using (var db = new DataContext())
            {
                return db.Customers.ToDictionary(c => c.CustomerId);
            }
        });
    }

    public Customer GetCustomer(int customerId)
    {
        // Cache initialized only on first access
        return _customerCache.Value.GetValueOrDefault(customerId);
    }
}
```

### Pattern 3: Pagination for Large Datasets

**Use When**: Returning large result sets

```csharp
public class OrderRepository
{
    public async Task<PagedResult<Order>> GetOrdersPagedAsync(int page, int pageSize)
    {
        using (var db = new DataContext())
        {
            var query = db.Orders.Where(o => o.IsActive);

            var total = await query.CountAsync();

            var orders = await query
                .OrderByDescending(o => o.OrderDate)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return new PagedResult<Order>
            {
                Items = orders,
                TotalCount = total,
                PageNumber = page,
                PageSize = pageSize
            };
        }
    }
}
```

### Pattern 4: Batch Processing

**Use When**: Processing many items individually

```csharp
// BAD: Process items one at a time
foreach (var order in orders)
{
    await ProcessOrderAsync(order); // 1 operation per order
}

// GOOD: Batch processing
const int batchSize = 100;
for (int i = 0; i < orders.Count; i += batchSize)
{
    var batch = orders.Skip(i).Take(batchSize).ToList();
    await ProcessOrderBatchAsync(batch); // 1 operation per 100 orders
}
```

## Performance Analysis Checklist

- [ ] Performance baseline established
- [ ] Critical workflows identified
- [ ] Current metrics measured and documented
- [ ] Performance issue reproduced consistently
- [ ] Bottleneck type identified (CPU/Memory/I/O/Network)
- [ ] Profiling data collected
- [ ] Hot paths or expensive operations identified
- [ ] Root cause analysis completed
- [ ] Optimization strategy developed and prioritized
- [ ] Performance tests created
- [ ] Optimizations implemented
- [ ] Performance improvement verified with metrics
- [ ] Monitoring and alerting configured
- [ ] Documentation updated

## Key Takeaways

1. **Measure first, optimize second**: Don't guess where the problem is - use data
2. **Focus on the bottleneck**: Optimizing non-bottleneck code wastes time
3. **80/20 rule applies**: 20% of code typically causes 80% of performance issues
4. **Profile in production-like environment**: Local dev environment can be misleading
5. **Monitor continuously**: Performance can degrade over time
6. **Set clear targets**: Define what "good performance" means
7. **Consider the full stack**: Performance issues can be anywhere (app, database, network)
8. **Test with realistic data**: Performance with 10 records vs 1M records is very different

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Performance & Optimization
