---
template-name: performance-optimization
description: Template for planning performance improvements and optimizations
applies-to: [performance-optimization, database-optimization, caching, algorithm-improvement]
required-inputs: [performance-problem, current-metrics, target-metrics]
---

# Template: Performance Optimization Planning

## When to Use
Use this template when optimizing performance, improving query speed, or reducing resource usage.

**Examples**:
- Optimize slow database query from 2000ms to 100ms
- Implement caching to reduce API response time
- Optimize algorithm from O(n²) to O(n log n)

## Required Inputs

1. **Performance Problem**: What's slow
2. **Current Metrics**: Current performance (time, throughput, memory)
3. **Target Metrics**: Desired performance
4. **Context**: When is it slow (high load, large data, etc.)

## Planning Structure

### Phase 1: Baseline Measurement (1-2 hours)

**Measure**:
- Current performance with profiler
- Memory usage
- CPU usage
- Database query time
- Network latency if applicable

**Tools**:
- SQL Server Query Analyzer
- .NET Profiler (dotTrace, JetBrains)
- Application Insights
- Custom logging

**Output**: Baseline metrics documented

**Code Example**:
```csharp
// Add timing measurement
var stopwatch = Stopwatch.StartNew();

var results = await GetSlowQuery();

stopwatch.Stop();
_logger.LogInformation($"Query took {stopwatch.ElapsedMilliseconds}ms");
```

### Phase 2: Bottleneck Analysis (1-2 hours)

**Identify**:
- Where time is spent (database, computation, I/O)
- Which parts are slowest
- Scalability limitations
- Resource constraints

**Techniques**:
- Database query analysis (execution plan)
- Code profiling
- Load testing
- Database indexing analysis

**Output**: Bottleneck identified and ranked

### Phase 3: Solution Design (1 hour)

**Choose approach** from options:

**Database Optimization**:
- Add indexes
- Optimize queries (JOINs, WHERE clauses)
- Denormalization for read-heavy data
- Partitioning large tables

**Caching**:
- In-memory cache for frequently accessed data
- Redis for distributed cache
- HTTP caching headers
- Query result caching

**Code Optimization**:
- Algorithm improvement
- Lazy loading instead of eager loading
- Batch processing instead of individual calls
- Async/parallel processing

**Infrastructure**:
- Database connection pooling
- Load balancing
- CDN for static content
- Compression

### Phase 4: Implement Optimization (Variable)

**Example: Database Query Optimization**

```csharp
// BEFORE - Slow query with N+1 problem
public List<Order> GetOrders()
{
    var orders = _context.Orders.ToList(); // Load all orders
    foreach (var order in orders)
    {
        order.Items = _context.OrderItems
            .Where(i => i.OrderId == order.Id)
            .ToList(); // N queries
    }
    return orders;
}

// AFTER - Optimized with eager loading
public List<Order> GetOrders()
{
    return _context.Orders
        .Include(o => o.Items) // Single query with JOIN
        .ToList();
}
```

**Example: Add Caching**

```csharp
// Add caching layer
public async Task<List<Category>> GetCategoriesAsync()
{
    const string cacheKey = "Categories";

    // Try to get from cache
    if (_cache.TryGetValue(cacheKey, out var cached))
        return (List<Category>)cached;

    // Get from database
    var categories = await _context.Categories.ToListAsync();

    // Cache for 1 hour
    _cache.Set(cacheKey, categories, TimeSpan.FromHours(1));

    return categories;
}
```

### Phase 5: Verify Performance Gain (1-2 hours)

**Measure**:
- New performance with same measurement tools
- Calculate improvement percentage
- Verify it meets target metrics

**Success Example**:
```
BEFORE: Query took 2,500 ms
AFTER: Query took 150 ms
Improvement: 94% faster (16x improvement)
Target met: Yes (target was 200ms)
```

### Phase 6: Check for Regressions (1 hour)

**Verify**:
- No performance degradation elsewhere
- Memory usage not significantly increased
- Data still correct
- Edge cases still work

**Tests**:
- Full regression test suite
- Load testing (ensure improvement scales)
- Memory profiling (no leaks)

### Phase 7: Add Monitoring (30 min)

**Add**:
- Performance metrics tracking
- Alerts if performance degrades
- Logging for diagnosis

**Code Example**:
```csharp
using (var activity = Activity.StartActivity("GetOrdersAsync"))
{
    activity?.SetTag("operation.name", "GetOrders");

    var result = await GetOrdersAsync();

    activity?.SetTag("operation.duration", stopwatch.ElapsedMilliseconds);
}
```

### Phase 8: Document Optimization (30 min)

**Document**:
- What was optimized and why
- How much improvement
- Any trade-offs (memory vs speed)
- How to monitor going forward

## Optimization Patterns

### Pattern: Missing Database Index
```
Problem: WHERE clause on unindexed column
Solution: Create index on column
```

### Pattern: N+1 Query Problem
```
Problem: Loading parent, then loading children in loop
Solution: Use Include() for eager loading or single query with JOIN
```

### Pattern: Inefficient LINQ
```csharp
// BEFORE - Inefficient
var expensive = list.Where(x => ComputeExpensiveThing(x)).ToList();

// AFTER - Precompute
var results = ComputeOnce();
var filtered = results.Where(x => x.Flag).ToList();
```

### Pattern: Missing Caching
```
Problem: Recalculating same value repeatedly
Solution: Cache computed value with TTL
```

### Pattern: Synchronous I/O Blocking
```csharp
// BEFORE
var result = asyncCall().Result; // Blocks thread

// AFTER
var result = await asyncCall(); // Non-blocking
```

## File-Level Changes

Typical optimization:
- 1-3 files modified
- 10-100 lines changed
- 1-2 config files updated
- Possible new cache/index files

## Testing Strategy

### Performance Testing

```csharp
[Test]
public void GetOrders_Performance_UnderTarget()
{
    var stopwatch = Stopwatch.StartNew();

    for (int i = 0; i < 1000; i++)
    {
        var orders = _service.GetOrders();
    }

    stopwatch.Stop();

    var avgTime = stopwatch.ElapsedMilliseconds / 1000d;

    // Assert average is under 50ms
    Assert.Less(avgTime, 50);
}

[Test]
public void GetOrders_LoadTest_Scales()
{
    // Load test with varying data sizes
    var sizes = new[] { 100, 1000, 10000 };

    foreach (var size in sizes)
    {
        var stopwatch = Stopwatch.StartNew();
        var results = _service.GetOrdersWithSize(size);
        stopwatch.Stop();

        _logger.LogInformation(
            $"Size {size}: {stopwatch.ElapsedMilliseconds}ms");
    }
}
```

## Success Criteria

- [ ] Baseline metrics established
- [ ] Bottleneck identified
- [ ] Optimization implemented
- [ ] Target performance achieved
- [ ] Regressions verified (none)
- [ ] Memory usage acceptable
- [ ] Tests pass
- [ ] Monitoring in place

## Risk Assessment

**Risks**:
- **Premature optimization** - Optimize wrong thing
- **Cache invalidation** - Stale data
- **Memory leaks** - From caching
- **Scalability changes** - Now works for 1K but fails at 100K

**Mitigation**:
- Profile before optimizing
- Test at scale
- Monitor memory and caches
- Load testing

## Trade-offs to Consider

| Optimization | Speed Gain | Memory Cost | Complexity |
|-------------|-----------|------------|-----------|
| Add Index | High | Low | Low |
| Caching | High | Medium | Medium |
| Query Rewrite | Medium | Low | Low |
| Algorithm Change | Medium/High | Low | Medium/High |
| Parallelization | High | Medium | High |

---

**Template Version**: 1.0.0
**Complexity**: Medium to High
**Typical Effort**: 2-8 hours
**Risk Level**: Medium
**Key Focus**: Measurement & validation
