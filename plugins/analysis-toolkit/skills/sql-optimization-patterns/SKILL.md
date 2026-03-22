# Skill: SQL Server Optimization Patterns

## Overview

SQL Server query optimization is essential for building performant applications. This skill covers optimization strategies, indexing patterns, execution plan analysis, and best practices for writing efficient SQL queries.

## When to Use This Skill

- **Analyzing slow queries** and stored procedures
- **Optimizing database performance** bottlenecks
- **Reviewing execution plans** for issues
- **Designing indexes** for tables
- **Tuning SQL Server** configuration
- **Code reviewing** database access code

## SQL Server Performance Fundamentals

### Query Execution Process
1. **Parsing**: Check syntax
2. **Binding**: Resolve object names
3. **Optimization**: Generate execution plan
4. **Execution**: Run the plan
5. **Results**: Return data

### Key Performance Metrics
- **Execution time**: How long query takes
- **Logical reads**: Pages read from buffer cache
- **Physical reads**: Pages read from disk
- **CPU time**: Processing time
- **Wait stats**: What query is waiting for

## Common SQL Performance Patterns

### Pattern 1: SARGable Queries

**SARGable** = Search ARGument-able = Can use indexes efficiently

```sql
-- GOOD: SARGable (can use index on LastName)
SELECT * FROM Users
WHERE LastName = 'Smith'

-- BAD: Non-SARGable (cannot use index)
SELECT * FROM Users
WHERE LEFT(LastName, 5) = 'Smith'

-- GOOD: SARGable alternative
SELECT * FROM Users
WHERE LastName LIKE 'Smith%'
```

**Rules for SARGable queries**:
- Don't use functions on indexed columns in WHERE
- Don't use implicit conversions
- Avoid NOT, <>, NOT IN when possible
- Use >= instead of > when appropriate

### Pattern 2: Covering Indexes

```sql
-- Query that benefits from covering index
SELECT UserId, FirstName, LastName, Email
FROM Users
WHERE Department = 'IT' AND IsActive = 1

-- Create covering index
CREATE NONCLUSTERED INDEX IX_Users_Department_IsActive_Includes
ON Users(Department, IsActive)
INCLUDE (UserId, FirstName, LastName, Email)
```

**Benefits**:
- Index contains all needed columns
- No table lookup required (key lookup)
- Faster query execution

### Pattern 3: Proper Index Column Order

```sql
-- Query
SELECT * FROM Orders
WHERE CustomerId = @CustomerId AND OrderDate >= @StartDate

-- GOOD: Most selective column first
CREATE INDEX IX_Orders_CustomerId_OrderDate
ON Orders(CustomerId, OrderDate)

-- LESS OPTIMAL: Less selective first
CREATE INDEX IX_Orders_OrderDate_CustomerId
ON Orders(OrderDate, CustomerId)
```

**Index column order rules**:
1. Equality columns first (=)
2. Inequality columns last (>, <, >=, <=, BETWEEN)
3. Most selective columns first
4. Match query WHERE clause order when possible

### Pattern 4: Avoid SELECT *

```sql
-- BAD: Loads all columns
SELECT * FROM Users WHERE UserId = @UserId

-- GOOD: Only needed columns
SELECT UserId, FirstName, LastName, Email
FROM Users
WHERE UserId = @UserId
```

**Benefits**:
- Reduced data transfer
- Can use covering indexes
- Reduces memory usage
- Clearer intent

### Pattern 5: Use EXISTS Instead of COUNT

```sql
-- BAD: Counts all matching rows
IF (SELECT COUNT(*) FROM Orders WHERE CustomerId = @CustomerId) > 0
    -- Customer has orders

-- GOOD: Stops at first match
IF EXISTS (SELECT 1 FROM Orders WHERE CustomerId = @CustomerId)
    -- Customer has orders
```

**Benefits**:
- Stops after finding first match
- Faster for large result sets
- Clearer intent

## Common Anti-Patterns

### Anti-Pattern 1: N+1 Query Problem

```sql
-- BAD: Separate query for each order
SELECT * FROM Orders WHERE CustomerId = @CustomerId

-- Then for each order:
SELECT * FROM OrderDetails WHERE OrderId = @OrderId
```

**Fix**: Use JOIN
```sql
-- GOOD: Single query
SELECT o.*, od.*
FROM Orders o
INNER JOIN OrderDetails od ON o.OrderId = od.OrderId
WHERE o.CustomerId = @CustomerId
```

### Anti-Pattern 2: Scalar Subqueries in SELECT

```sql
-- BAD: Executes subquery for each row
SELECT
    u.UserId,
    u.FullName,
    (SELECT COUNT(*) FROM Orders WHERE CustomerId = u.UserId) as OrderCount
FROM Users u
```

**Fix**: Use LEFT JOIN with GROUP BY
```sql
-- GOOD: Single scan
SELECT
    u.UserId,
    u.FullName,
    COUNT(o.OrderId) as OrderCount
FROM Users u
LEFT JOIN Orders o ON u.UserId = o.CustomerId
GROUP BY u.UserId, u.FullName
```

### Anti-Pattern 3: Implicit Conversions

```sql
-- BAD: UserId is INT, but comparing to VARCHAR
-- Causes table scan
SELECT * FROM Users WHERE UserId = '123'

-- GOOD: Explicit type match
SELECT * FROM Users WHERE UserId = 123
```

**Problem**: SQL Server converts every row's UserId to VARCHAR, preventing index use

### Anti-Pattern 4: OR with Different Columns

```sql
-- BAD: Cannot efficiently use indexes
SELECT * FROM Users
WHERE LastName = 'Smith' OR FirstName = 'John'
```

**Fix**: Use UNION ALL
```sql
-- GOOD: Can use indexes on each part
SELECT * FROM Users WHERE LastName = 'Smith'
UNION
SELECT * FROM Users WHERE FirstName = 'John'
```

### Anti-Pattern 5: Using IN with Large Lists

```sql
-- BAD: Large IN list
SELECT * FROM Products
WHERE ProductId IN (1, 2, 3, ..., 10000) -- Very large list
```

**Fix**: Use temp table or table-valued parameter
```sql
-- GOOD: Use temp table
CREATE TABLE #ProductIds (ProductId INT)
INSERT INTO #ProductIds VALUES (1), (2), (3), ..., (10000)

SELECT p.*
FROM Products p
INNER JOIN #ProductIds t ON p.ProductId = t.ProductId
```

## Indexing Strategies

### Clustered Index
- One per table
- Physically sorts table data
- Leaf nodes contain actual data rows

**When to use**:
- Primary key (usually)
- Column used in range queries
- Frequently accessed sequential data

```sql
CREATE CLUSTERED INDEX IX_Orders_OrderDate
ON Orders(OrderDate)
```

### Non-Clustered Index
- Multiple per table
- Separate structure from table
- Leaf nodes contain key + row locator

**When to use**:
- Foreign keys
- Frequently filtered columns
- JOIN columns

```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId
ON Orders(CustomerId)
```

### Covering Index
- Non-clustered index with INCLUDE columns
- Contains all columns needed by query

```sql
CREATE NONCLUSTERED INDEX IX_Users_LastName_Covering
ON Users(LastName)
INCLUDE (FirstName, Email, Phone)
```

### Filtered Index
- Index on subset of rows
- Smaller, more efficient

```sql
-- Index only active users
CREATE NONCLUSTERED INDEX IX_Users_Active_LastName
ON Users(LastName)
WHERE IsActive = 1
```

### Columnstore Index
- For data warehouse queries
- Compresses data by column

```sql
CREATE NONCLUSTERED COLUMNSTORE INDEX IX_Sales_ColumnStore
ON Sales(OrderDate, ProductId, Quantity, Amount)
```

## Execution Plan Analysis

### Reading Execution Plans

**Key indicators to look for**:
1. **Table Scan**: Reading entire table (usually bad)
2. **Index Scan**: Reading entire index (sometimes okay)
3. **Index Seek**: Using index efficiently (good)
4. **Key Lookup**: Extra lookup to get missing columns (bad if frequent)
5. **Nested Loops**: Good for small result sets
6. **Hash Match**: Good for large result sets
7. **Merge Join**: Good for pre-sorted data
8. **Parallelism**: Query using multiple threads

### Common Plan Issues

**Issue 1: Table Scan**
```
Table Scan (Users)  Cost: 85%
```
**Fix**: Add index on filtered/joined columns

**Issue 2: Key Lookup**
```
Index Seek (IX_Users_LastName)  Cost: 10%
Key Lookup (Clustered)          Cost: 75%
```
**Fix**: Create covering index with INCLUDE

**Issue 3: Implicit Conversion**
```
Compute Scalar (CONVERT_IMPLICIT)  Cost: 40%
```
**Fix**: Match data types in query and table

**Issue 4: Missing Index Suggestion**
```
Missing Index (Impact: 95%)
CREATE INDEX IX_Suggested ON Table(Col1) INCLUDE (Col2, Col3)
```
**Action**: Evaluate and create suggested index

## Query Optimization Techniques

### Technique 1: Use SET STATISTICS

```sql
SET STATISTICS TIME ON
SET STATISTICS IO ON

SELECT * FROM Users WHERE LastName = 'Smith'

SET STATISTICS TIME OFF
SET STATISTICS IO OFF
```

**Output shows**:
- Execution time
- Logical reads
- Physical reads

### Technique 2: Parameter Sniffing Workaround

**Problem**: Plan optimized for first parameter value may be inefficient for others

```sql
-- Workaround: Use local variables
CREATE PROCEDURE usp_GetOrders
    @CustomerId INT
AS
BEGIN
    DECLARE @LocalCustomerId INT = @CustomerId

    SELECT * FROM Orders
    WHERE CustomerId = @LocalCustomerId
    OPTION (OPTIMIZE FOR UNKNOWN)
END
```

### Technique 3: Use Query Hints Sparingly

```sql
-- Force index usage
SELECT * FROM Users WITH (INDEX(IX_Users_LastName))
WHERE LastName = 'Smith'

-- Force join order
SELECT * FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId
OPTION (FORCE ORDER)

-- Recompile each time
SELECT * FROM Users
WHERE Department = @Department
OPTION (RECOMPILE)
```

**Warning**: Only use hints when necessary, as they override optimizer

### Technique 4: Update Statistics

```sql
-- Update statistics for table
UPDATE STATISTICS Users WITH FULLSCAN

-- Update specific index
UPDATE STATISTICS Users IX_Users_LastName

-- Auto-update statistics (recommended)
ALTER DATABASE MyDb SET AUTO_UPDATE_STATISTICS ON
```

### Technique 5: Use Batch Operations

```sql
-- BAD: Row-by-row inserts
DECLARE @i INT = 1
WHILE @i <= 10000
BEGIN
    INSERT INTO Users VALUES (@i, 'Name' + CAST(@i AS VARCHAR))
    SET @i = @i + 1
END

-- GOOD: Batch insert
INSERT INTO Users (UserId, FullName)
SELECT Id, 'Name' + CAST(Id AS VARCHAR)
FROM Numbers
WHERE Id BETWEEN 1 AND 10000
```

## Stored Procedure Best Practices

### Practice 1: Use SET NOCOUNT ON

```sql
CREATE PROCEDURE usp_GetUsers
AS
BEGIN
    SET NOCOUNT ON  -- Prevents "rows affected" messages

    SELECT * FROM Users WHERE IsActive = 1
END
```

### Practice 2: Error Handling

```sql
CREATE PROCEDURE usp_UpdateUser
    @UserId INT,
    @FullName NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON
    BEGIN TRY
        BEGIN TRANSACTION

        UPDATE Users
        SET FullName = @FullName, LastModified = GETDATE()
        WHERE UserId = @UserId

        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION

        THROW -- Re-throw error
    END CATCH
END
```

### Practice 3: Input Validation

```sql
CREATE PROCEDURE usp_GetUsersByDepartment
    @Department NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON

    -- Validate input
    IF @Department IS NULL OR @Department = ''
    BEGIN
        RAISERROR('Department cannot be null or empty', 16, 1)
        RETURN
    END

    SELECT * FROM Users
    WHERE Department = @Department AND IsActive = 1
END
```

## SQL Server Configuration

### Key Settings

**Max Degree of Parallelism (MAXDOP)**
```sql
-- Limit parallelism to 4 cores
EXEC sp_configure 'max degree of parallelism', 4
RECONFIGURE
```

**Cost Threshold for Parallelism**
```sql
-- Only parallelize queries with cost > 50
EXEC sp_configure 'cost threshold for parallelism', 50
RECONFIGURE
```

**Memory Configuration**
```sql
-- Set max server memory to 16GB
EXEC sp_configure 'max server memory (MB)', 16384
RECONFIGURE
```

## Optimization Checklist

### Query Level
- [ ] Use SARGable predicates
- [ ] Avoid SELECT *
- [ ] Use appropriate JOIN types
- [ ] Filter early in query
- [ ] Avoid scalar subqueries in SELECT
- [ ] Use EXISTS instead of COUNT
- [ ] Proper WHERE clause column order

### Index Level
- [ ] Indexes on foreign keys
- [ ] Indexes on frequently filtered columns
- [ ] Covering indexes for critical queries
- [ ] Remove unused indexes
- [ ] Index column order optimized
- [ ] Statistics up to date
- [ ] Avoid over-indexing

### Stored Procedure Level
- [ ] SET NOCOUNT ON
- [ ] Error handling (TRY/CATCH)
- [ ] Input validation
- [ ] Transaction management
- [ ] Proper parameter data types

### Server Level
- [ ] MAXDOP configured
- [ ] Memory allocation set
- [ ] Auto-update statistics enabled
- [ ] Regular index maintenance
- [ ] Query timeout configured

## Monitoring & Maintenance

### Dynamic Management Views (DMVs)

```sql
-- Top 10 slowest queries
SELECT TOP 10
    qs.execution_count,
    qs.total_elapsed_time / 1000000.0 AS total_elapsed_time_seconds,
    qs.total_elapsed_time / qs.execution_count / 1000.0 AS avg_elapsed_time_ms,
    SUBSTRING(qt.text, (qs.statement_start_offset/2) + 1,
        ((CASE qs.statement_end_offset
            WHEN -1 THEN DATALENGTH(qt.text)
            ELSE qs.statement_end_offset
        END - qs.statement_start_offset)/2) + 1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY qs.total_elapsed_time DESC

-- Missing indexes
SELECT
    migs.avg_user_impact,
    migs.avg_total_user_cost,
    migs.user_seeks,
    mid.statement AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_groups mig
INNER JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
INNER JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
ORDER BY migs.avg_user_impact DESC
```

## Key Takeaways

1. **Indexes are critical**: But don't over-index
2. **SARGable queries**: Avoid functions on indexed columns in WHERE
3. **Execution plans**: Learn to read and interpret
4. **Statistics matter**: Keep them updated
5. **Avoid N+1 patterns**: Use JOINs, not loops
6. **Batch operations**: Better than row-by-row
7. **Monitor performance**: Use DMVs and query store
8. **Test with production data volumes**: Small datasets hide problems

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Database
