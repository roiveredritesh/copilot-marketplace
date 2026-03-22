# Skill: Query Performance Tuning

## Overview

Query performance tuning is the systematic process of analyzing and optimizing database queries using execution plans, indexes, and statistics. This skill covers reading execution plans, index tuning strategies, understanding query optimizer decisions, and implementing optimizations for SQL Server databases.

## When to Use This Skill

- **Slow database queries**: Queries taking longer than acceptable
- **High CPU usage on database**: Database server CPU consistently high
- **Timeout errors**: Queries timing out under load
- **Lock contention**: Queries blocking each other
- **High logical/physical reads**: Excessive I/O operations
- **Poor execution plans**: Optimizer choosing suboptimal plans
- **Index fragmentation**: Performance degrading over time
- **Parameter sniffing issues**: Query performance varies by parameters

## Understanding SQL Server Execution Plans

### What is an Execution Plan?

An execution plan is SQL Server's step-by-step strategy for executing a query. It shows:
- How tables are accessed (scans vs seeks)
- Join algorithms used
- Sort operations
- Estimated vs actual row counts
- Resource consumption (CPU, I/O)

### Reading Execution Plans

**Enable Actual Execution Plan in SSMS**:
- Press `Ctrl+M` before running query
- Or click "Include Actual Execution Plan" button
- Plan appears in "Execution Plan" tab after query runs

**Execution Plan Flow**:
- Read from **right to left**
- Top to bottom for parallel operations
- Thickness of arrows indicates row count
- Icons represent operations

**Key Components**:

**Operation Icons**:
```
[Table Scan]        - Reads entire table (BAD for large tables)
[Index Scan]        - Reads entire index (BETTER than table scan)
[Index Seek]        - Seeks to specific rows (GOOD - targeted)
[Clustered Index Seek] - Best for precise lookups
[Key Lookup]        - Additional lookup after index seek (can be expensive)
[Nested Loops]      - Join algorithm (good for small datasets)
[Hash Match]        - Join algorithm (good for large datasets)
[Sort]              - Sorts data (expensive - prefer indexes)
[Filter]            - Applies WHERE clause filters
[Compute Scalar]    - Calculates expressions
```

### Execution Plan Metrics

**Cost Percentages**:
- Shows relative cost of each operation
- Focus on operations with highest cost (> 20%)
- Total plan cost is estimate, not actual time

**Row Count Comparison**:
```
Estimated Rows: 100
Actual Rows: 50,000
```
Large discrepancy indicates **stale statistics** - update statistics!

**I/O Statistics**:
```
Number of Rows Read: 1,000,000
Actual Number of Rows: 10
```
High read-to-return ratio indicates inefficient access

### Execution Plan Analysis Examples

**Example 1: Table Scan (Bad)**

```sql
SELECT * FROM Orders WHERE OrderDate = '2025-01-15';
```

**Execution Plan**:
```
Table Scan [Orders]    Cost: 95%
├─ Rows: 1,000,000
└─ Estimated I/O: 10,000 reads
```

**Problem**: Reading all 1M rows to find matching orders

**Fix**: Add index on OrderDate
```sql
CREATE INDEX IX_Orders_OrderDate ON Orders(OrderDate);
```

**Improved Plan**:
```
Index Seek [IX_Orders_OrderDate]    Cost: 5%
├─ Rows: 100
└─ Estimated I/O: 50 reads
```

**Example 2: Key Lookup (Potentially Bad)**

```sql
SELECT OrderId, OrderDate, CustomerName, TotalAmount
FROM Orders
WHERE OrderDate = '2025-01-15';
```

**Execution Plan**:
```
Nested Loops Join               Cost: 60%
├─ Index Seek [IX_Orders_OrderDate]    Cost: 5%
│  └─ Rows: 100
└─ Key Lookup [PK_Orders]              Cost: 35%
   └─ Rows: 100 (one per seek result)
```

**Problem**: After finding rows via index, needs to lookup additional columns (CustomerName, TotalAmount) from clustered index - 100 additional lookups

**Fix**: Create covering index including all needed columns
```sql
CREATE INDEX IX_Orders_OrderDate_Covering
ON Orders(OrderDate)
INCLUDE (CustomerName, TotalAmount);
```

**Improved Plan**:
```
Index Seek [IX_Orders_OrderDate_Covering]    Cost: 5%
└─ Rows: 100 (all columns in index)
```

**Example 3: Stale Statistics**

```sql
SELECT * FROM Orders WHERE Status = 'Pending';
```

**Execution Plan**:
```
Index Scan [IX_Orders_Status]
├─ Estimated Rows: 1,000
└─ Actual Rows: 500,000
```

**Problem**: Optimizer expected 1,000 rows, got 500,000 - chose wrong plan

**Fix**: Update statistics
```sql
UPDATE STATISTICS Orders;
-- Or specific index:
UPDATE STATISTICS Orders IX_Orders_Status;
```

## Index Tuning Strategies

### Types of Indexes

**Clustered Index**:
- Physical order of data
- One per table
- Leaf nodes contain actual data
- Best for range queries

```sql
CREATE CLUSTERED INDEX IX_Orders_OrderDate
ON Orders(OrderDate);
```

**Non-Clustered Index**:
- Separate structure from data
- Can have multiple per table
- Leaf nodes contain key + row locator
- Best for specific lookups

```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId
ON Orders(CustomerId);
```

**Covering Index**:
- Includes all columns needed by query
- Avoids key lookups
- Uses INCLUDE clause for non-key columns

```sql
CREATE INDEX IX_Orders_CustomerId_Covering
ON Orders(CustomerId)
INCLUDE (OrderDate, TotalAmount, Status);
```

**Filtered Index**:
- Index only subset of rows
- Smaller, more efficient
- Good for queries filtering on specific values

```sql
CREATE INDEX IX_Orders_Active
ON Orders(OrderDate)
WHERE Status IN ('Pending', 'Processing');
```

**Composite Index**:
- Multiple columns in index
- Column order matters (left to right)
- Can support multiple query patterns

```sql
CREATE INDEX IX_Orders_Status_Date
ON Orders(Status, OrderDate);

-- Supports:
-- WHERE Status = 'Pending'
-- WHERE Status = 'Pending' AND OrderDate > '2025-01-01'
-- Not efficient for:
-- WHERE OrderDate > '2025-01-01' (doesn't use Status)
```

### Index Design Patterns

**Pattern 1: Equality + Range**

```sql
-- Query pattern
WHERE Status = 'Active' AND OrderDate >= '2025-01-01'

-- Index design: Equality column first, range column second
CREATE INDEX IX_Orders_Status_OrderDate
ON Orders(Status, OrderDate);
```

**Why**: Index can seek to Status = 'Active', then scan forward on OrderDate

**Pattern 2: Covering Index for Frequent Query**

```sql
-- Frequent query
SELECT CustomerId, OrderDate, TotalAmount
FROM Orders
WHERE Status = 'Pending'
ORDER BY OrderDate DESC;

-- Covering index
CREATE INDEX IX_Orders_Status_OrderDate_Covering
ON Orders(Status, OrderDate DESC)
INCLUDE (CustomerId, TotalAmount);
```

**Benefits**:
- Index seek on Status
- Data already sorted by OrderDate DESC (no sort needed)
- All columns in index (no key lookup)

**Pattern 3: Filtered Index for Sparse Data**

```sql
-- Only 1% of orders are pending, 99% are completed
-- Query frequently searches pending orders
WHERE Status = 'Pending'

-- Filtered index (smaller, faster)
CREATE INDEX IX_Orders_Pending
ON Orders(OrderDate)
WHERE Status = 'Pending';
```

**Benefits**:
- Much smaller than full index
- Faster to scan/seek
- Less maintenance overhead

### Index Maintenance

**Index Fragmentation**:

**Check Fragmentation**:
```sql
SELECT
    OBJECT_NAME(ips.object_id) AS TableName,
    i.name AS IndexName,
    ips.avg_fragmentation_in_percent,
    ips.page_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
INNER JOIN sys.indexes i ON ips.object_id = i.object_id
    AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 10
    AND ips.page_count > 1000
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

**Fragmentation Guidelines**:
- **< 10%**: No action needed
- **10-30%**: REORGANIZE index
- **> 30%**: REBUILD index

**Reorganize vs Rebuild**:

```sql
-- Reorganize (online, less resource intensive)
ALTER INDEX IX_Orders_OrderDate ON Orders REORGANIZE;

-- Rebuild (offline by default, more thorough)
ALTER INDEX IX_Orders_OrderDate ON Orders REBUILD;

-- Rebuild online (Enterprise Edition)
ALTER INDEX IX_Orders_OrderDate ON Orders REBUILD WITH (ONLINE = ON);
```

**Update Statistics**:

```sql
-- Update statistics for entire table
UPDATE STATISTICS Orders;

-- Update statistics for specific index
UPDATE STATISTICS Orders IX_Orders_OrderDate;

-- Update with full scan (more accurate, slower)
UPDATE STATISTICS Orders WITH FULLSCAN;

-- Update with sample
UPDATE STATISTICS Orders WITH SAMPLE 50 PERCENT;
```

### Index Anti-Patterns

**Anti-Pattern 1: Too Many Indexes**

**Problem**:
- Every index slows down INSERT/UPDATE/DELETE
- Indexes consume storage
- Query optimizer can choose wrong index

**Guideline**: Generally 5-10 indexes per table maximum

**Anti-Pattern 2: Duplicate Indexes**

```sql
-- Redundant!
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
CREATE INDEX IX_Orders_CustomerId_OrderDate ON Orders(CustomerId, OrderDate);

-- The second index covers the first - drop the first one
```

**Anti-Pattern 3: Wrong Column Order**

```sql
-- Query: WHERE Status = 'Active' AND CustomerId = 123
-- BAD: Range column first
CREATE INDEX IX_Orders_Bad ON Orders(CustomerId, Status);

-- GOOD: Equality columns first
CREATE INDEX IX_Orders_Good ON Orders(Status, CustomerId);
```

**Anti-Pattern 4: Index on Low Selectivity Column**

```sql
-- BAD: Status has only 3 values (Pending, Processing, Completed)
CREATE INDEX IX_Orders_Status ON Orders(Status);

-- Better: Use filtered index or composite index
CREATE INDEX IX_Orders_Status_OrderDate ON Orders(Status, OrderDate);
```

## Statistics and Cardinality

### Understanding Statistics

**What are Statistics?**:
- Histograms of data distribution
- Used by query optimizer to estimate row counts
- Critical for choosing optimal execution plans

**View Statistics**:
```sql
DBCC SHOW_STATISTICS('Orders', 'IX_Orders_Status');
```

**Output Includes**:
1. **Header**: Last update, rows, rows sampled
2. **Density**: Uniqueness of values
3. **Histogram**: Value distribution (up to 200 steps)

### Cardinality Estimation

**Cardinality**: Number of unique values in a column

**High Cardinality** (Good for indexing):
- CustomerId: 1,000,000 unique values in 1,000,000 rows
- OrderNumber: Unique for each row
- Email addresses, GUIDs, etc.

**Low Cardinality** (Poor for indexing alone):
- Status: 3 values (Pending, Processing, Completed)
- Gender: 2-3 values
- Boolean flags: 2 values (True, False)

### Statistics Issues and Solutions

**Issue 1: Stale Statistics**

**Symptoms**:
- Large difference between estimated and actual rows
- Plan changes unexpectedly
- Query suddenly slow after data changes

**Fix**:
```sql
-- Manual update
UPDATE STATISTICS Orders;

-- Enable auto-update statistics (should be ON)
ALTER DATABASE MyDatabase SET AUTO_UPDATE_STATISTICS ON;

-- Update with full scan for accuracy
UPDATE STATISTICS Orders WITH FULLSCAN;
```

**Issue 2: Ascending Key Problem**

**Problem**: Auto-update statistics doesn't trigger fast enough for rapidly growing tables with ascending keys (identity columns, dates)

**Example**:
```sql
-- Table has OrderId from 1 to 1,000,000
-- Statistics know about OrderId up to 1,000,000
-- New orders added: 1,000,001 to 1,500,000
-- Query: WHERE OrderId > 1,200,000
-- Statistics estimate 0 rows! (thinks max is 1,000,000)
```

**Fix**: Use trace flag 2371 for adaptive statistics update threshold
```sql
DBCC TRACEON(2371, -1); -- Global
```

**Issue 3: Multi-Column Statistics**

**Problem**: Statistics on single columns don't capture correlation between columns

**Example**:
```sql
WHERE Status = 'Completed' AND PaymentMethod = 'CreditCard'

-- Optimizer assumes independence:
-- 50% are Completed, 30% are CreditCard
-- Estimates 15% of rows (50% * 30%)
-- Reality: 80% of completed orders are credit card (24%)
```

**Fix**: Create multi-column statistics
```sql
CREATE STATISTICS ST_Orders_Status_Payment
ON Orders(Status, PaymentMethod);
```

## Query Optimization Techniques

### Technique 1: SARGable Queries

**SARGable** = Search ARGument able (can use index seeks)

**Non-SARGable (Bad)**:
```sql
-- Function on indexed column prevents index seek
WHERE YEAR(OrderDate) = 2025
WHERE UPPER(CustomerName) = 'JOHN DOE'
WHERE OrderAmount * 1.1 > 1000

-- Wrapping in calculation prevents index use
WHERE OrderId + 1 = @OrderId
```

**SARGable (Good)**:
```sql
-- Direct comparison on indexed column
WHERE OrderDate >= '2025-01-01' AND OrderDate < '2026-01-01'
WHERE CustomerName = 'John Doe' -- Case-insensitive collation
WHERE OrderAmount > 1000 / 1.1

-- Direct comparison
WHERE OrderId = @OrderId - 1
```

### Technique 2: JOIN Optimization

**JOIN Types and Performance**:

**Nested Loops Join**:
- Good for small outer table, indexed inner table
- Iterates outer table, seeks inner table for each row

**Hash Match Join**:
- Good for large unsorted datasets
- Builds hash table of smaller input
- Probes hash table with larger input

**Merge Join**:
- Good for large sorted datasets
- Requires both inputs sorted on join key
- Most efficient when data already sorted

**Optimizing JOINs**:

```sql
-- BAD: No indexes on join columns
SELECT o.OrderId, c.CustomerName
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId;
-- Result: Table scans on both tables, Hash Match join

-- GOOD: Indexes on join columns
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
CREATE CLUSTERED INDEX PK_Customers ON Customers(CustomerId);
-- Result: Index seeks, Nested Loops or Merge join
```

### Technique 3: Subquery vs JOIN

**Correlated Subquery (Usually Slow)**:
```sql
-- BAD: Subquery executes for each row
SELECT o.OrderId, o.OrderDate,
    (SELECT CustomerName FROM Customers WHERE CustomerId = o.CustomerId) as CustomerName
FROM Orders o;
```

**JOIN (Usually Faster)**:
```sql
-- GOOD: Single join operation
SELECT o.OrderId, o.OrderDate, c.CustomerName
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId;
```

**When Subquery is Better**:
```sql
-- Exists check (stops at first match)
WHERE EXISTS (SELECT 1 FROM OrderDetails WHERE OrderId = o.OrderId)

-- Better than:
WHERE OrderId IN (SELECT DISTINCT OrderId FROM OrderDetails)
```

### Technique 4: Pagination Optimization

**Offset-Fetch (Bad for Large Offsets)**:
```sql
-- Page 1000 (offset 99,000)
SELECT OrderId, OrderDate
FROM Orders
ORDER BY OrderDate DESC
OFFSET 99000 ROWS
FETCH NEXT 100 ROWS ONLY;

-- Still reads and sorts first 99,100 rows!
```

**Keyset Pagination (Better)**:
```sql
-- First page
SELECT TOP 100 OrderId, OrderDate
FROM Orders
WHERE OrderDate < @LastOrderDate -- Last date from previous page
ORDER BY OrderDate DESC;

-- Much faster - uses index seek instead of scanning
```

### Technique 5: Avoid SELECT *

```sql
-- BAD: Returns all columns (more I/O, network traffic)
SELECT * FROM Orders WHERE OrderDate = '2025-01-15';

-- GOOD: Select only needed columns
SELECT OrderId, OrderDate, TotalAmount FROM Orders WHERE OrderDate = '2025-01-15';

-- Benefit: Can use covering index
CREATE INDEX IX_Orders_OrderDate_Covering
ON Orders(OrderDate) INCLUDE (OrderId, TotalAmount);
```

## Wait Statistics Analysis

### Understanding Wait Statistics

**What are Wait Statistics?**:
- Time SQL Server waits for resources
- Identifies bottlenecks (CPU, I/O, locks, memory)

**Common Wait Types**:

**PAGEIOLATCH_** (I/O waits):
- Waiting for data pages to be read from disk
- **Fix**: Add indexes, increase memory, faster storage

**CXPACKET** (Parallelism waits):
- Waiting for parallel query threads to synchronize
- **Fix**: Usually benign, but excessive waits indicate inefficient parallelism

**LCK_M_** (Lock waits):
- Waiting to acquire locks
- **Fix**: Optimize queries, use proper isolation levels, reduce transaction scope

**SOS_SCHEDULER_YIELD** (CPU pressure):
- CPU is the bottleneck
- **Fix**: Optimize queries, add CPU, reduce load

**PAGELATCH_** (Memory contention):
- Contention on in-memory pages
- **Fix**: Reduce allocation contention, normalize data

**Query Wait Statistics**:
```sql
SELECT TOP 20
    wait_type,
    wait_time_ms / 1000.0 AS wait_time_sec,
    waiting_tasks_count,
    wait_time_ms / waiting_tasks_count AS avg_wait_time_ms
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    -- Filter out benign waits
    'CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE',
    'SLEEP_TASK', 'SLEEP_SYSTEMTASK', 'SQLTRACE_BUFFER_FLUSH',
    'WAITFOR', 'LOGMGR_QUEUE', 'CHECKPOINT_QUEUE'
)
ORDER BY wait_time_ms DESC;
```

## Query Performance Anti-Patterns

### Anti-Pattern 1: N+1 Query Problem

```sql
-- BAD: Separate query for each order's details
foreach (var order in orders)
{
    var details = db.ExecuteQuery("SELECT * FROM OrderDetails WHERE OrderId = " + order.OrderId);
}
-- 1 query for orders + N queries for details = N+1 queries
```

**Fix**: Single query with JOIN
```sql
-- GOOD: Single query
SELECT o.*, od.*
FROM Orders o
LEFT JOIN OrderDetails od ON o.OrderId = od.OrderId;
```

### Anti-Pattern 2: Implicit Conversion

```sql
-- BAD: Column is VARCHAR, parameter is INT
SELECT * FROM Orders WHERE OrderNumber = 123;
-- Implicit conversion prevents index use: CONVERT(INT, OrderNumber) = 123

-- GOOD: Match data types
SELECT * FROM Orders WHERE OrderNumber = '123';
```

### Anti-Pattern 3: OR Conditions on Different Columns

```sql
-- BAD: Cannot efficiently use indexes
WHERE CustomerId = 123 OR Status = 'Pending';
-- Results in index scans or table scans

-- GOOD: Use UNION if selective
SELECT * FROM Orders WHERE CustomerId = 123
UNION
SELECT * FROM Orders WHERE Status = 'Pending';
-- Can use index seeks on both queries
```

### Anti-Pattern 4: Leading Wildcard in LIKE

```sql
-- BAD: Cannot use index
WHERE CustomerName LIKE '%Smith';

-- GOOD: If possible, use trailing wildcard
WHERE CustomerName LIKE 'Smith%';

-- Alternative: Full-text search for contains operations
```

## Query Tuning Checklist

- [ ] Execution plan reviewed and understood
- [ ] Table scans identified and resolved
- [ ] Missing indexes identified (check plan warnings)
- [ ] Existing indexes evaluated for usefulness
- [ ] Key lookups identified (consider covering indexes)
- [ ] Statistics up to date
- [ ] Estimated vs actual row counts match (within 10x)
- [ ] SARGable predicates used
- [ ] No implicit conversions
- [ ] JOIN columns indexed
- [ ] WHERE clause columns indexed
- [ ] ORDER BY columns indexed or covered
- [ ] No functions on indexed columns
- [ ] SELECT only needed columns (not SELECT *)
- [ ] Wait statistics reviewed
- [ ] Index fragmentation checked
- [ ] Query hints avoided (unless necessary)

## Key Takeaways

1. **Read execution plans right to left**: Understand query execution flow
2. **Seek good, scan bad**: Index seeks are targeted, scans read entire structures
3. **Statistics must be current**: Stale statistics = bad execution plans
4. **Column order matters in indexes**: Equality before range, most selective first
5. **Covering indexes eliminate key lookups**: Include all needed columns
6. **SARGable queries use indexes**: No functions on indexed columns
7. **Wait statistics reveal bottlenecks**: I/O, CPU, locks, memory
8. **Update statistics after large data changes**: Especially on indexed columns
9. **Test with production data volumes**: Performance different with realistic data
10. **Monitor and maintain indexes**: Regular defragmentation and statistics updates

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Database & Performance
