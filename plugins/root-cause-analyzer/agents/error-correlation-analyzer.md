---
name: error-correlation-analyzer
description: Correlates multiple errors to identify common root causes and shared code paths
task_type: error-correlation
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
---

# Error Correlation Analyzer

**Version**: 2.0.0
**Plugin**: root-cause-analyzer
**Task Coverage**: Multi-error correlation and common root cause identification
**MCP Requirements**: None (local analysis only)
**Sequential Thinking**: Conditional (enabled for complex correlation patterns or ambiguous root causes)
**Last Updated**: 2026-01-16

## Purpose

Performs comprehensive multi-error analysis to correlate seemingly unrelated errors and identify common root causes. Analyzes multiple error logs, stack traces, and exception patterns to find shared code paths, common dependencies, and underlying issues that manifest as different symptoms across the system.

This agent serves as a pattern detective, uncovering hidden relationships between errors that appear unrelated on the surface. It excels at identifying systemic issues (resource exhaustion, configuration problems, architectural flaws) that cause cascading failures across multiple components.

## When to Use

Use this agent when you need to:
- Correlate multiple different errors that seem related
- Find common root cause for a batch of production errors
- Investigate cascading failures across components
- Analyze error patterns during incidents
- Identify systemic issues (connection pools, memory leaks, timeouts)
- Understand error relationships and dependencies
- Prioritize fixes for maximum impact
- Document multi-error incidents for postmortems
- Find which fix will resolve multiple errors
- Analyze error logs from production incidents

Best for scenarios with:
- Multiple errors occurring around the same time
- Errors across different components or layers
- Suspicion of common underlying cause
- Cascading failures (one error triggers others)
- Resource exhaustion patterns
- Integration or infrastructure issues
- Need to understand error relationships

## When NOT to Use

Do NOT use this agent when:
- Only a single error needs analysis (use `/analyze-stacktrace`)
- Errors are clearly unrelated (analyze separately)
- Need to find similar bug patterns (use `/analyze-bug-pattern`)
- Need to identify when regression occurred (use `/find-regression`)
- Errors are from different time periods (not related)
- You need Jira ticket analysis (use `/analyze-jira-issue`)
- Focus is on performance optimization (use optimization agents)

For these scenarios, consider:
- **Single error**: `/analyze-stacktrace`
- **Pattern matching**: `/analyze-bug-pattern`
- **Regression tracking**: `/find-regression`
- **Jira context**: `/analyze-jira-issue`
- **Performance**: `/optimize-query`, `/optimize-algorithm`

## Input

**Format**: Command with error list or log file paths

**Required Fields**:
- `error_list`: Either:
  - Multiple error descriptions (comma-separated or newline-separated)
  - File path(s) to error logs
  - Directory containing error logs

**Optional Fields**:
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--time-window`: Time window for correlation (e.g., "1 hour", "24 hours", default: "24 hours")
- `--min-correlation`: Minimum correlation score (0.0-1.0, default: 0.6)
- `--max-errors`: Maximum errors to analyze (default: 15)

**Example**:
```bash
/correlate-errors "Error1: Timeout in OrderService, Error2: Deadlock in PaymentService, Error3: Connection pool exhausted"

/correlate-errors logs/production-2026-01-15.log

/correlate-errors logs/*.log --time-window="1 hour"

/correlate-errors "logs/error-batch-*.log" --min-correlation=0.7 --report=summary
```

## Output

**Format**: Markdown report saved to `marketplace/output/root-cause-analysis/error-correlation-<timestamp>.md`

**Main Sections**:
1. **Executive Summary** - Overview and key findings
2. **Error Collection** - All errors analyzed with metadata
3. **Correlation Matrix** - How errors relate to each other
4. **Common Code Paths** - Shared execution paths
5. **Dependency Analysis** - Shared dependencies and resources
6. **Root Cause Identification** - Common underlying cause
7. **Fix Strategy** - Prioritized approach to resolve all errors
8. **Prevention Recommendations** - Avoid similar cascading failures

**Example Output Snippet**:
```markdown
# Error Correlation Analysis: Database Connection Issues

## Executive Summary
**Errors Analyzed**: 5 distinct errors
**Time Window**: 2026-01-15 14:00-15:00 (1 hour)
**Correlation Score**: 0.92 (Very High)
**Common Root Cause**: Database connection pool exhaustion
**Impact**: 3 services affected (Order, Payment, Inventory)
**Fix Priority**: CRITICAL - Single fix resolves all 5 errors

## Correlation Matrix

| Error | Order Timeout | Payment Deadlock | Inventory Failure | DB Connection | Pool Exhausted |
|-------|---------------|------------------|-------------------|---------------|----------------|
| Order Timeout | 1.00 | 0.85 | 0.78 | 0.95 | 0.98 |
| Payment Deadlock | 0.85 | 1.00 | 0.72 | 0.88 | 0.91 |
| Inventory Failure | 0.78 | 0.72 | 1.00 | 0.90 | 0.85 |
| DB Connection | 0.95 | 0.88 | 0.90 | 1.00 | 0.99 |
| Pool Exhausted | 0.98 | 0.91 | 0.85 | 0.99 | 1.00 |

**Correlation Insight**: All errors highly correlated (>0.85) → Single root cause likely

## Common Root Cause
**Issue**: Database connection pool exhausted due to connections not being disposed
**Evidence**:
- All errors occur when connection count reaches limit (100)
- All errors resolve after connection timeout (30 seconds)
- All affected services use SqlConnection without proper disposal
```

## Process Overview

The agent follows a systematic six-phase analysis process that starts with collecting and normalizing error data, then progressively identifies patterns, shared code paths, dependencies, and ultimately the common root cause. It combines stack trace analysis, code path tracing, dependency mapping, and statistical correlation to build a complete picture of error relationships.

The analysis begins by parsing all error logs and extracting structured error data. Then it identifies patterns in exception types, messages, timing, and affected components. For each error, it traces execution paths and identifies dependencies. Through correlation analysis, it determines which errors share common causes. Finally, it synthesizes findings into a single root cause explanation and provides a unified fix strategy.

For complex scenarios with subtle correlations or ambiguous root causes, the agent can enable Sequential Thinking to provide deeper reflection on causality and course-correct if early hypotheses don't align with all evidence.

## Detailed Process

### Phase 1: Error Collection & Normalization
**Duration**: 10-12% of total time
**Input**: Error list or log file paths from user
**Process**:
1. Parse input to identify error sources:
   - **Direct input**: Error descriptions from command
   - **Log files**: Read files specified by path or glob pattern
   - **Directory**: Scan directory for error logs
2. Extract error data from each source:
   - **Exception type**: NullReferenceException, SqlException, TimeoutException, etc.
   - **Error message**: Full error text
   - **Stack trace**: Call stack if available
   - **Timestamp**: When error occurred
   - **Component**: Service, controller, method affected
   - **Severity**: ERROR, WARN, FATAL
   - **Context**: Request ID, user ID, session data
3. Normalize error format:
   - Standardize exception type names
   - Extract core error message (remove variable data)
   - Normalize stack traces (remove line numbers, just method names)
   - Convert timestamps to common format (ISO 8601)
4. Filter errors by time window:
   - Keep errors within specified time window (default: 24 hours)
   - Group errors by time proximity
   - Identify error bursts or spikes
5. Deduplicate errors:
   - Remove exact duplicates (same exception, message, stack)
   - Group similar errors (same exception type, similar message)
   - Keep representative examples
6. Assign error IDs and metadata:
   - Error ID (E1, E2, E3, etc.)
   - Error category (database, network, logic, resource)
   - Affected component (OrderService, PaymentService, etc.)

**Tools Used**: Bash (for file reading), Grep (for log parsing)
**Output**: Normalized list of distinct errors with metadata
**Success Criteria**:
- All error sources processed
- Errors extracted with complete metadata
- Timestamp and component information captured
- Duplicates removed
- Errors categorized

**Example**:
```markdown
## Error Collection

### Input Sources
- logs/production-2026-01-15.log (1,247 log lines)
- logs/payment-service-2026-01-15.log (856 log lines)
- logs/order-service-2026-01-15.log (1,034 log lines)

### Extraction Results
**Total Log Lines**: 3,137
**Error Lines Identified**: 87
**Unique Errors After Deduplication**: 5

### Time Window
- **Start**: 2026-01-15 14:00:00
- **End**: 2026-01-15 15:00:00
- **Duration**: 1 hour
- **Error Count**: 5 distinct errors, 87 occurrences

### Normalized Errors

#### Error E1: Order Timeout
**Exception Type**: System.TimeoutException
**Normalized Message**: "Timeout waiting for database response"
**Original Messages** (variations):
- "Timeout waiting for database response (30s)"
- "Timeout waiting for database response after 30000ms"
**First Occurrence**: 2026-01-15 14:05:23
**Last Occurrence**: 2026-01-15 14:58:45
**Occurrence Count**: 32 times
**Component**: OrderService.CreateOrder
**Severity**: ERROR
**Stack Trace Summary**:
```
OrderService.CreateOrder
  → SqlConnection.Open
    → ConnectionPool.GetConnection
      → [Timeout]
```

#### Error E2: Payment Deadlock
**Exception Type**: System.Data.SqlClient.SqlException (Deadlock)
**Normalized Message**: "Transaction was deadlocked on lock resources"
**First Occurrence**: 2026-01-15 14:12:10
**Last Occurrence**: 2026-01-15 14:55:32
**Occurrence Count**: 18 times
**Component**: PaymentService.ProcessPayment
**Severity**: ERROR
**Stack Trace Summary**:
```
PaymentService.ProcessPayment
  → SqlCommand.ExecuteNonQuery
    → [Deadlock]
```

#### Error E3: Inventory Failure
**Exception Type**: System.InvalidOperationException
**Normalized Message**: "ExecuteReader requires an open connection"
**First Occurrence**: 2026-01-15 14:18:45
**Last Occurrence**: 2026-01-15 14:59:01
**Occurrence Count**: 23 times
**Component**: InventoryService.CheckStock
**Severity**: ERROR
**Stack Trace Summary**:
```
InventoryService.CheckStock
  → SqlCommand.ExecuteReader
    → [Connection not open]
```

#### Error E4: Database Connection Failure
**Exception Type**: System.InvalidOperationException
**Normalized Message**: "Connection pool reached maximum size"
**First Occurrence**: 2026-01-15 14:05:15
**Last Occurrence**: 2026-01-15 14:58:50
**Occurrence Count**: 8 times (explicit messages)
**Component**: Multiple services
**Severity**: WARN → ERROR
**Context**: Connection pool limit = 100

#### Error E5: Connection Pool Exhausted
**Exception Type**: System.InvalidOperationException
**Normalized Message**: "Timeout waiting for available connection from pool"
**First Occurrence**: 2026-01-15 14:05:20
**Last Occurrence**: 2026-01-15 14:58:55
**Occurrence Count**: 6 times
**Component**: Multiple services
**Severity**: ERROR
**Context**: All available connections in use
```

### Phase 2: Stack Trace Pattern Extraction
**Duration**: 18-22% of total time
**Input**: Normalized errors from Phase 1
**Process**:
1. For each error, parse stack trace:
   - Extract method call chain
   - Identify entry point (controller, API endpoint)
   - Identify error point (where exception thrown)
   - Identify intermediate methods
2. Normalize stack traces:
   - Remove line numbers (focus on methods)
   - Remove parameter details (focus on method signatures)
   - Group similar stacks (same call chain, different data)
3. Identify stack trace patterns:
   - **Common prefix**: Do multiple errors start in same method?
   - **Common suffix**: Do multiple errors end in same framework method?
   - **Common middle**: Do errors share intermediate methods?
4. Extract code locations:
   - Files involved in each error
   - Methods involved
   - Classes involved
   - Namespaces/packages
5. Map errors to code components:
   - Service layer methods
   - Repository/data access methods
   - Controller/API methods
   - External integration points
6. Build call graph for each error:
   - Entry point → intermediate → error point
   - Visualize as tree/graph structure

**Tools Used**: Grep (to find code files), Read (to understand methods)
**Output**: Stack trace patterns with common elements identified
**Success Criteria**:
- Stack traces parsed for all errors
- Patterns identified (common methods, files)
- Code components mapped
- Call graphs constructed

**Example**:
```markdown
## Stack Trace Pattern Analysis

### Error E1: Order Timeout
**Call Chain**:
```
1. OrderController.CreateOrder (Entry Point)
2. OrderService.CreateOrder
3. OrderRepository.SaveOrder
4. SqlConnection.Open  ← Common pattern
5. ConnectionPool.GetConnection  ← Common pattern
6. [Timeout waiting for connection]  ← Error Point
```

**Code Locations**:
- OrderController.cs:45
- OrderService.cs:120
- OrderRepository.cs:78
- [Framework] System.Data.SqlClient.SqlConnection

### Error E2: Payment Deadlock
**Call Chain**:
```
1. PaymentController.ProcessPayment (Entry Point)
2. PaymentService.ProcessPayment
3. PaymentRepository.UpdatePaymentStatus
4. SqlCommand.ExecuteNonQuery  ← Common pattern
5. [Deadlock on table lock]  ← Error Point
```

**Code Locations**:
- PaymentController.cs:67
- PaymentService.cs:89
- PaymentRepository.cs:134
- [Framework] System.Data.SqlClient.SqlCommand

### Error E3: Inventory Failure
**Call Chain**:
```
1. InventoryController.CheckStock (Entry Point)
2. InventoryService.CheckStock
3. InventoryRepository.GetStockLevel
4. SqlCommand.ExecuteReader
5. [Connection not open]  ← Error Point
```

**Code Locations**:
- InventoryController.cs:23
- InventoryService.cs:56
- InventoryRepository.cs:91
- [Framework] System.Data.SqlClient.SqlCommand

### Pattern Identification

#### Common Suffix (All 3 errors)
```
SqlConnection/SqlCommand operations
  ↓
Database access failure
```

**Observation**: All errors terminate in database access operations

#### Common Code Path Segments
**Segment A**: Service → Repository → Database
- Present in: E1, E2, E3 (100%)
- Pattern: All errors follow same architectural pattern

**Segment B**: SqlConnection/SqlCommand usage
- Present in: E1, E2, E3 (100%)
- Pattern: All errors involve SQL client operations

**Segment C**: Connection/Command error handling
- Present in: E1, E2, E3 (100%)
- Pattern: All errors indicate connection/command issues

### Code Component Mapping

#### Repositories (Data Access Layer)
- OrderRepository.cs
- PaymentRepository.cs
- InventoryRepository.cs
**Common Pattern**: All use SqlConnection directly

#### Services (Business Logic Layer)
- OrderService.cs
- PaymentService.cs
- InventoryService.cs
**Common Pattern**: All call repositories for data access

#### Controllers (Presentation Layer)
- OrderController.cs
- PaymentController.cs
- InventoryController.cs
**Common Pattern**: All entry points for user requests
```

### Phase 3: Common Code Path Identification
**Duration**: 20-25% of total time (CRITICAL PHASE)
**Input**: Stack trace patterns from Phase 2
**Process**:
1. Identify shared code paths across errors:
   - Methods called by multiple error stacks
   - Files touched by multiple errors
   - Classes involved in multiple errors
2. Use Grep to search for shared patterns:
   - Search for SqlConnection usage across files
   - Search for connection pool access
   - Search for transaction handling
   - Search for resource disposal patterns
3. Read shared code locations:
   - Read repository files (OrderRepository, PaymentRepository, etc.)
   - Analyze connection management
   - Check for using statements or Dispose calls
   - Verify error handling
4. Identify missing patterns:
   - Are connections being disposed?
   - Are there using statements?
   - Is connection pooling configured?
   - Are there connection leaks?
5. Build evidence for common cause:
   - Code pattern: How connections are used
   - Missing pattern: What protective code is absent
   - Impact: How this affects multiple services
6. Map code paths to errors:
   - Error E1 uses OrderRepository → SqlConnection (not disposed)
   - Error E2 uses PaymentRepository → SqlConnection (not disposed)
   - Error E3 uses InventoryRepository → SqlConnection (not disposed)

**If Sequential Thinking Enabled**:
- Reflection Point: "Is missing disposal the true root cause or just correlated?"
- Course Correction: Verify by checking connection pool metrics, timing
- Confidence Check: Rate certainty based on evidence

**Tools Used**: Grep, Read
**Output**: Common code paths with evidence of shared issue
**Success Criteria**:
- Shared code paths identified
- Evidence collected from code
- Missing patterns documented
- Root cause hypothesis formed

**Example**:
```markdown
## Common Code Path Identification

### Shared Pattern: Database Connection Usage

#### Repository Pattern Analysis

**OrderRepository.cs** (Lines 75-85):
```csharp
public void SaveOrder(Order order)
{
    var connection = new SqlConnection(_connectionString);  // ← Created
    connection.Open();
    var command = new SqlCommand("INSERT INTO Orders...", connection);
    command.Parameters.AddWithValue("@OrderId", order.Id);
    command.ExecuteNonQuery();
    // ← CONNECTION NOT CLOSED/DISPOSED
}
```

**PaymentRepository.cs** (Lines 130-140):
```csharp
public void UpdatePaymentStatus(int paymentId, string status)
{
    var connection = new SqlConnection(_connectionString);  // ← Created
    connection.Open();
    var command = new SqlCommand("UPDATE Payments...", connection);
    command.Parameters.AddWithValue("@PaymentId", paymentId);
    command.ExecuteNonQuery();
    // ← CONNECTION NOT CLOSED/DISPOSED
}
```

**InventoryRepository.cs** (Lines 88-98):
```csharp
public int GetStockLevel(int productId)
{
    var connection = new SqlConnection(_connectionString);  // ← Created
    connection.Open();
    var command = new SqlCommand("SELECT Stock FROM Inventory...", connection);
    command.Parameters.AddWithValue("@ProductId", productId);
    var result = (int)command.ExecuteScalar();
    return result;
    // ← CONNECTION NOT CLOSED/DISPOSED
}
```

### Common Issue: Connection Leaks

**Pattern Identified**: All repositories create SqlConnection without disposal

**Evidence**:
1. ✅ No `using` statement wrapping SqlConnection
2. ✅ No explicit `connection.Close()` or `connection.Dispose()`
3. ✅ Connections created for every operation
4. ✅ No connection reuse or pooling management

**Impact**:
- Connections opened: ~100-200 per minute (high load)
- Connections disposed: 0 per minute (no disposal)
- Connection pool limit: 100 connections
- Result: **Pool exhaustion within 30 seconds**

### Connection Pool Configuration

**Search Pattern**: "connection pool" OR "Max Pool Size"
**Search Location**: Web.config, appsettings.json, connection strings

**Found**: Web.config
```xml
<connectionStrings>
  <add name="DefaultConnection"
       connectionString="Server=...;Database=...;Max Pool Size=100;..."
       providerName="System.Data.SqlClient" />
</connectionStrings>
```

**Pool Limit**: 100 connections (default)

### Timeline Correlation

**Hypothesis**: Connection leaks → Pool exhaustion → Multiple error types

**Timeline Evidence**:
```
14:00:00 - System normal (50 concurrent users)
14:05:00 - Load increases (100 concurrent users)
14:05:15 - First "Pool limit reached" warning (Error E4)
14:05:20 - Connection timeout errors start (Error E5, E1)
14:12:10 - Deadlocks appear (Error E2) ← Connections held too long
14:18:45 - Connection state errors (Error E3) ← Pool completely exhausted
```

**Observation**: Errors cascade as pool fills up:
1. Pool limit warnings (E4)
2. Timeout waiting for connections (E5, E1)
3. Deadlocks from long-held connections (E2)
4. Invalid connection state (E3)

### Root Cause Hypothesis

**Primary Cause**: Connection leaks due to missing disposal
**Mechanism**:
1. Each request creates new SqlConnection
2. Connection not disposed after use
3. Connection remains in pool indefinitely (or until GC)
4. Pool fills up (100 connection limit)
5. New requests timeout waiting for connection (E1, E5)
6. Long-held connections cause deadlocks (E2)
7. Invalid connection states from exhausted pool (E3)

**Confidence**: 95% (high evidence from code + timeline)
```

### Phase 4: Dependency Analysis
**Duration**: 15-18% of total time
**Input**: Common code paths from Phase 3
**Process**:
1. Identify shared dependencies across errors:
   - **External systems**: Database, APIs, message queues
   - **Shared resources**: Connection pools, thread pools, caches
   - **Configuration**: App settings, connection strings
   - **Infrastructure**: Network, disk, memory
2. Analyze resource usage patterns:
   - Connection pool metrics (if available)
   - Memory usage trends
   - Thread count
   - File handle count
3. Check for resource exhaustion:
   - Pool limits (database, thread, connection)
   - Memory limits
   - File descriptor limits
   - Network socket limits
4. Review configuration:
   - Connection string settings (pool size, timeout)
   - Resource limits in app config
   - Infrastructure limits (database max connections)
5. Identify shared failure points:
   - Single database instance (SPOF)
   - Shared connection pool
   - Single network path
   - Shared cache or state
6. Map dependencies to errors:
   - Error E1: Depends on connection pool availability
   - Error E2: Depends on database locks (affected by pool)
   - Error E3: Depends on connection pool state
   - All: Depend on same database connection pool

**Tools Used**: Bash (for config file reading), Read (for config analysis)
**Output**: Dependency map showing shared resources
**Success Criteria**:
- Shared dependencies identified
- Resource limits documented
- Failure points mapped
- Configuration reviewed

**Example**:
```markdown
## Dependency Analysis

### Shared Dependencies

#### Database (SQL Server)
**Instance**: production-db-01.database.windows.net
**Users**: All services (OrderService, PaymentService, InventoryService)
**Connection Method**: SqlConnection via connection pool

**Dependency Mapping**:
- Error E1 (Order Timeout): ✓ Uses production-db-01
- Error E2 (Payment Deadlock): ✓ Uses production-db-01
- Error E3 (Inventory Failure): ✓ Uses production-db-01
- Error E4 (Pool Limit): ✓ Related to production-db-01 pool
- Error E5 (Pool Exhausted): ✓ Related to production-db-01 pool

**Observation**: 100% of errors depend on same database instance

#### Connection Pool
**Type**: ADO.NET SqlConnection Pool
**Limit**: Max Pool Size = 100
**Shared By**: All services in application
**Management**: Automatic (ADO.NET runtime)

**Pool Configuration**:
```xml
Max Pool Size=100
Min Pool Size=5
Connection Timeout=30
```

**Pool State (inferred from errors)**:
- 14:05:00: ~50 connections in use (normal)
- 14:05:15: ~95 connections in use (near limit)
- 14:05:20: 100 connections in use (LIMIT REACHED)
- 14:05:23 onwards: Pool exhausted (all subsequent operations timeout)

### Resource Exhaustion Evidence

#### Connection Pool Exhaustion
**Symptoms**:
- "Pool reached maximum size" (Error E4)
- "Timeout waiting for connection" (Error E5)
- Order/Payment/Inventory timeouts (E1, E2, E3)

**Timeline**:
```
Connections in Pool (estimated):
100 ┤                    ████████████████████████
    │                ████
    │            ████
 50 ┤        ████
    │    ████
    │████
  0 ┤──────────────────────────────────────────────
    14:00    14:05    14:10    14:15    14:20
            ↑ Load spike
                  ↑ Pool exhausted
```

**Root Cause**: Connections not released back to pool (missing disposal)

### Single Point of Failure

**SPOF**: Database connection pool (Max Pool Size=100)

**Impact**:
- If pool exhausted: All services fail simultaneously
- Cascading failure: One slow query blocks all operations
- No isolation: Payment failure affects Order and Inventory

**Risk**: HIGH - Single shared resource with hard limit

### Configuration Review

#### Connection String
```xml
<add name="DefaultConnection"
     connectionString="
       Server=production-db-01.database.windows.net;
       Database=ProductionDB;
       User Id=app_user;
       Password=...;
       Max Pool Size=100;           ← Limit (too low for load)
       Min Pool Size=5;
       Connection Timeout=30;       ← 30-second timeout
       Connection Lifetime=0;       ← Connections never expire
       Pooling=true;
     "
     providerName="System.Data.SqlClient" />
```

**Issues**:
- Max Pool Size too low for concurrent load (100 < 150 peak requests)
- Connection Lifetime=0 (connections never recycled)
- No connection leak detection

#### Infrastructure Limits
**Database Server**: SQL Server 2019
**Max Connections**: 32,767 (server limit)
**Current Connections**: ~100 (pool limit, not server limit)

**Observation**: Database server has capacity, but application pool limit is bottleneck
```

### Phase 5: Correlation Matrix Generation
**Duration**: 12-15% of total time
**Input**: All analysis from Phases 1-4
**Process**:
1. Build correlation matrix for all errors:
   - For each pair of errors, calculate correlation score
   - Correlation factors:
     - **Time proximity** (0-0.3): How close in time?
     - **Code path overlap** (0-0.3): Shared methods/files?
     - **Dependency overlap** (0-0.2): Shared resources?
     - **Exception similarity** (0-0.2): Similar exception types?
2. Calculate correlation score for each pair:
   - Score = weighted sum of factors
   - Range: 0.0 (unrelated) to 1.0 (identical cause)
   - Threshold: 0.6 for "correlated" designation
3. Identify correlation clusters:
   - Errors with high correlation (>0.8) to each other
   - Errors with medium correlation (0.6-0.8) to cluster
   - Errors with low correlation (<0.6) outliers
4. Visualize correlation matrix:
   - Table format with scores
   - Color coding (high=red, medium=yellow, low=green)
   - Heatmap visualization
5. Interpret correlation patterns:
   - All highly correlated → Single root cause
   - Clustered correlation → Multiple related causes
   - Low correlation → Unrelated errors
6. Rank errors by centrality:
   - Which error has highest average correlation to others?
   - Which error is "center" of correlation cluster?
   - This error likely closest to root cause

**Tools Used**: None (calculation phase)
**Output**: Correlation matrix with scores and clustering
**Success Criteria**:
- Matrix complete for all error pairs
- Correlation scores calculated
- Clusters identified
- Central error identified

**Example**:
```markdown
## Correlation Matrix

### Pairwise Correlation Scores

|  | E1: Order Timeout | E2: Payment Deadlock | E3: Inventory Fail | E4: Pool Limit | E5: Pool Timeout |
|---|---|---|---|---|---|
| **E1: Order Timeout** | 1.00 | 0.85 | 0.78 | 0.95 | 0.98 |
| **E2: Payment Deadlock** | 0.85 | 1.00 | 0.72 | 0.88 | 0.91 |
| **E3: Inventory Fail** | 0.78 | 0.72 | 1.00 | 0.90 | 0.85 |
| **E4: Pool Limit** | 0.95 | 0.88 | 0.90 | 1.00 | 0.99 |
| **E5: Pool Timeout** | 0.98 | 0.91 | 0.85 | 0.99 | 1.00 |

### Correlation Score Breakdown (Example: E1 ↔ E4)

**E1 (Order Timeout) ↔ E4 (Pool Limit)**:
- **Time Proximity** (0.3): 0.29
  - E1 first: 14:05:23
  - E4 first: 14:05:15
  - Delta: 8 seconds (very close)
  - Score: 0.29 (near maximum 0.3)

- **Code Path Overlap** (0.3): 0.28
  - E1 path: OrderService → OrderRepository → SqlConnection
  - E4 path: Multiple services → SqlConnection
  - Shared: SqlConnection, ConnectionPool
  - Overlap: 95%
  - Score: 0.28

- **Dependency Overlap** (0.2): 0.20
  - E1 depends: Database, Connection Pool
  - E4 depends: Connection Pool
  - Shared: Connection Pool (100%)
  - Score: 0.20 (maximum)

- **Exception Similarity** (0.2): 0.18
  - E1: TimeoutException (waiting for connection)
  - E4: InvalidOperationException (pool limit)
  - Similarity: Both connection-related
  - Score: 0.18

**Total Correlation**: 0.29 + 0.28 + 0.20 + 0.18 = **0.95** (Very High)

### Correlation Clustering

#### Cluster 1: Connection Pool Issues (All Errors)
**Members**: E1, E2, E3, E4, E5
**Average Correlation**: 0.88 (Very High)
**Interpretation**: All errors stem from same root cause

**Cluster Characteristics**:
- All errors occur in same time window (1 hour)
- All errors involve database connections
- All errors resolve when connection pool resets
- All errors disappear after connection leak fix

### Centrality Ranking

**Most Central Error** (highest average correlation):
1. **E5: Pool Timeout** (0.93 avg) ← Most correlated with all others
2. **E4: Pool Limit** (0.92 avg)
3. **E1: Order Timeout** (0.89 avg)
4. **E2: Payment Deadlock** (0.84 avg)
5. **E3: Inventory Fail** (0.81 avg)

**Interpretation**:
- E5 (Pool Timeout) is center of correlation cluster
- E5 is symptomatic of root cause (pool exhaustion)
- Fixing pool exhaustion will resolve E5 and cascading errors (E1-E4)

### Correlation Heatmap

```
        E1    E2    E3    E4    E5
E1   [███] [██░] [██░] [███] [███]
E2   [██░] [███] [██░] [██░] [██░]
E3   [██░] [██░] [███] [██░] [██░]
E4   [███] [██░] [██░] [███] [███]
E5   [███] [██░] [██░] [███] [███]

Legend: [███] >0.9  [██░] 0.7-0.9  [█░░] 0.5-0.7  [░░░] <0.5
```

**Observation**: Dense correlation (mostly dark) → Single root cause
```

### Phase 6: Root Cause Identification & Fix Strategy
**Duration**: 15-18% of total time
**Input**: Correlation matrix + all previous analysis
**Process**:
1. Synthesize all evidence into root cause statement:
   - What is the underlying issue?
   - Why does it cause multiple errors?
   - How do errors cascade from root cause?
2. Build causality chain:
   - Root cause → Primary symptoms → Secondary symptoms
   - Connection leak → Pool exhaustion → Timeouts/Deadlocks/Failures
3. Explain each error in context of root cause:
   - E1: Timeout because pool exhausted
   - E2: Deadlock because connections held too long
   - E3: Invalid state because pool corrupted
4. Generate unified fix strategy:
   - **Fix 1**: Address root cause (add connection disposal)
   - **Fix 2**: Increase resilience (increase pool size, add retry)
   - **Fix 3**: Improve monitoring (connection pool metrics, alerts)
5. Prioritize fixes by impact:
   - Which fix resolves most errors?
   - Which fix is fastest to implement?
   - Which fix prevents recurrence?
6. Provide implementation guidance:
   - Code changes needed
   - Testing approach
   - Deployment strategy
   - Rollback plan
7. Add prevention recommendations:
   - Code review checklist
   - Static analysis rules
   - Monitoring dashboards
   - Incident response playbook

**Tools Used**: Write
**Output**: Root cause statement + unified fix strategy
**Success Criteria**:
- Root cause clearly articulated
- Causality chain documented
- All errors explained by root cause
- Unified fix strategy provided
- Implementation guidance complete

**Example**:
```markdown
## Root Cause Identification

### Unified Root Cause Statement

**Root Cause**: Database connections not properly disposed after use, leading to connection pool exhaustion and cascading failures across multiple services.

**Mechanism**:
1. Repository classes create SqlConnection without `using` statement or explicit disposal
2. Connections remain open after method completes
3. Connection pool fills up (Max Pool Size = 100)
4. New requests wait for available connection (30-second timeout)
5. Timeouts occur → Primary errors (E1, E5)
6. Long-held connections cause database locks → Secondary errors (E2)
7. Invalid connection states from exhausted pool → Tertiary errors (E3)
8. Pool limit warnings → Diagnostic errors (E4)

### Causality Chain

```
ROOT CAUSE: Missing connection disposal
              ↓
       Connection leaks accumulate
              ↓
    Connection pool fills up (100/100)
              ↓
          ┌───┴────┬────────┬──────────┐
          ↓        ↓        ↓          ↓
    E5: Timeout  E1: Order  E4: Pool  E3: Invalid
    waiting for  timeout    limit     connection
    connection               warning   state
          ↓        ↓
          └────┬───┘
               ↓
        E2: Deadlocks
        (long-held
        connections)
```

### Error Explanations

#### Primary Errors (Direct symptoms of pool exhaustion)

**E1: Order Timeout**
- **Symptom**: Orders timeout waiting for database
- **Cause**: Connection pool exhausted, no available connections
- **Evidence**: Error occurs when pool count reaches 100
- **Resolution**: Fix connection leak → Pool available → No timeouts

**E5: Pool Timeout**
- **Symptom**: Explicit "timeout waiting for connection from pool"
- **Cause**: Connection pool exhausted, waiting 30 seconds times out
- **Evidence**: Same timing as E1, same root cause
- **Resolution**: Fix connection leak → Pool available → No timeouts

#### Secondary Errors (Cascading effects)

**E2: Payment Deadlock**
- **Symptom**: Database deadlocks on Payment table
- **Cause**: Connections held too long (not released), database locks accumulate
- **Evidence**: Deadlocks occur after timeouts start, correlate with pool exhaustion
- **Resolution**: Fix connection leak → Connections released quickly → No deadlocks

#### Tertiary Errors (Downstream effects)

**E3: Inventory Failure**
- **Symptom**: "ExecuteReader requires open connection"
- **Cause**: Connection pool in invalid state, connections corrupted
- **Evidence**: Occurs during peak pool exhaustion
- **Resolution**: Fix connection leak → Pool healthy → No state errors

**E4: Pool Limit Warning**
- **Symptom**: "Pool reached maximum size" warning
- **Cause**: Diagnostic message as pool approaches limit
- **Evidence**: First warning appears before errors cascade
- **Resolution**: Fix connection leak → Pool never reaches limit

### Impact Analysis

**Errors Resolved by Single Fix**: 5/5 (100%)

**User Impact**:
- Before Fix: Orders fail (100% for 1 hour), Payments fail (50% for 1 hour), Inventory checks fail (75% for 1 hour)
- After Fix: All errors resolve immediately

**Business Impact**:
- Before: $50,000 revenue loss (failed orders), Customer support load +400%
- After: Normal operations

---

## Fix Strategy

### Fix Level 1: Immediate Hotfix (2 hours)

**Objective**: Stop the bleeding - add connection disposal to critical paths

**Changes**:

**OrderRepository.cs**:
```csharp
// BEFORE (BROKEN)
public void SaveOrder(Order order)
{
    var connection = new SqlConnection(_connectionString);
    connection.Open();
    var command = new SqlCommand("INSERT INTO Orders...", connection);
    command.ExecuteNonQuery();
}

// AFTER (FIXED)
public void SaveOrder(Order order)
{
    using (var connection = new SqlConnection(_connectionString))
    {
        connection.Open();
        var command = new SqlCommand("INSERT INTO Orders...", connection);
        command.ExecuteNonQuery();
    }  // ← Connection automatically disposed here
}
```

**Apply same fix to**:
- PaymentRepository.cs (3 methods)
- InventoryRepository.cs (2 methods)
- OrderRepository.cs (4 methods)

**Total Methods to Fix**: 9 methods

**Implementation Time**: ~15 min per method = 2 hours

**Testing**:
- Load test with 100 concurrent users
- Monitor connection pool count (should stay <20)
- Verify no timeouts or deadlocks

**Deployment**:
- Deploy to production immediately
- Monitor for 2 hours
- Rollback plan: Revert commits if issues persist

---

### Fix Level 2: Proper Solution (1-2 days)

**Objective**: Comprehensive fix + increase resilience

**Step 1: Repository Pattern Improvement**
Create base repository with proper connection management:

```csharp
public abstract class BaseRepository
{
    protected readonly string _connectionString;

    protected BaseRepository(string connectionString)
    {
        _connectionString = connectionString;
    }

    protected T Execute<T>(Func<SqlConnection, T> operation)
    {
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            return operation(connection);
        }
    }

    protected void Execute(Action<SqlConnection> operation)
    {
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            operation(connection);
        }
    }
}
```

**Refactor all repositories to inherit from BaseRepository**:

```csharp
public class OrderRepository : BaseRepository
{
    public void SaveOrder(Order order)
    {
        Execute(connection =>
        {
            var command = new SqlCommand("INSERT INTO Orders...", connection);
            command.Parameters.AddWithValue("@OrderId", order.Id);
            command.ExecuteNonQuery();
        });
    }
}
```

**Step 2: Increase Pool Size**
```xml
<!-- Web.config -->
<connectionStrings>
  <add name="DefaultConnection"
       connectionString="...;Max Pool Size=200;..."  ← Increased from 100
       providerName="System.Data.SqlClient" />
</connectionStrings>
```

**Step 3: Add Connection Retry Logic**
```csharp
protected T ExecuteWithRetry<T>(Func<SqlConnection, T> operation, int maxRetries = 3)
{
    for (int i = 0; i < maxRetries; i++)
    {
        try
        {
            return Execute(operation);
        }
        catch (SqlException ex) when (IsTransient(ex) && i < maxRetries - 1)
        {
            Thread.Sleep(TimeSpan.FromSeconds(Math.Pow(2, i)));  // Exponential backoff
        }
    }
    throw new Exception("Max retries exceeded");
}
```

**Step 4: Add Unit Tests**
```csharp
[TestClass]
public class ConnectionManagementTests
{
    [TestMethod]
    public void SaveOrder_ShouldDisposeConnection()
    {
        // Arrange
        var order = new Order { Id = 1, Total = 100 };
        var initialPoolCount = GetConnectionPoolCount();

        // Act
        _orderRepository.SaveOrder(order);

        // Assert
        var finalPoolCount = GetConnectionPoolCount();
        Assert.AreEqual(initialPoolCount, finalPoolCount, "Connection not returned to pool");
    }
}
```

**Implementation Time**: 1-2 days (refactor + test + deploy)

---

### Fix Level 3: Comprehensive Prevention (1 week)

**Objective**: Prevent all resource leak issues long-term

**Step 1: Enable Nullable Reference Types & Code Analysis**
```xml
<!-- .csproj -->
<PropertyGroup>
  <Nullable>enable</Nullable>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>

<ItemGroup>
  <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="7.0.0" />
</ItemGroup>
```

**Step 2: Add Resource Leak Detection**
```xml
<!-- Code analysis rules -->
<PropertyGroup>
  <EnableNETAnalyzers>true</EnableNETAnalyzers>
  <AnalysisLevel>latest</AnalysisLevel>
</PropertyGroup>

<!-- Enable rules -->
<PropertyGroup>
  <CA2000>error</CA2000>  <!-- Dispose objects before losing scope -->
  <CA2213>error</CA2213>  <!-- Disposable fields should be disposed -->
</PropertyGroup>
```

**Step 3: Add Connection Pool Monitoring**
```csharp
// Monitoring middleware
public class ConnectionPoolMonitor
{
    private static readonly PerformanceCounter _poolCounter =
        new PerformanceCounter(".NET Data Provider for SqlServer",
                               "NumberOfActiveConnections",
                               "Your.App.exe");

    public static void LogPoolStatus()
    {
        var activeConnections = _poolCounter.NextValue();
        _logger.LogInformation($"Active connections: {activeConnections}");

        if (activeConnections > 80)  // 80% of max (100)
        {
            _logger.LogWarning($"Connection pool near capacity: {activeConnections}/100");
        }
    }
}
```

**Step 4: Add Alerting**
```yaml
# Azure Monitor Alert (or similar)
alert:
  name: "Connection Pool Exhaustion Warning"
  condition: "activeConnections > 80"
  action: "Send email to ops team"
  severity: "Warning"
```

**Step 5: Add Automated Testing (Load Tests)**
```csharp
[TestClass]
public class LoadTests
{
    [TestMethod]
    public void ConcurrentOrders_ShouldNotExhaustConnectionPool()
    {
        // Arrange
        var tasks = new List<Task>();
        for (int i = 0; i < 150; i++)  // Exceed previous pool limit
        {
            tasks.Add(Task.Run(() => _orderService.CreateOrder(new Order())));
        }

        // Act
        Task.WaitAll(tasks.ToArray());

        // Assert
        var poolCount = GetConnectionPoolCount();
        Assert.IsTrue(poolCount < 100, $"Pool count too high: {poolCount}");
    }
}
```

**Step 6: Team Training**
- Proper IDisposable usage
- Using statements for resource management
- Connection pooling best practices
- Monitoring and alerting

**Implementation Time**: 1 week (analysis + monitoring + tests + training)

---

## Prevention Recommendations

### Code Review Checklist
- [ ] All SqlConnection usage wrapped in `using` statement
- [ ] All IDisposable objects properly disposed
- [ ] No manual connection management (use base repository)
- [ ] Connection pool metrics monitored
- [ ] Load tests pass with 150+ concurrent users

### CI/CD Pipeline
- [ ] Code analysis enabled (CA2000, CA2213)
- [ ] Resource leak detection in build
- [ ] Load tests run on every deploy
- [ ] Connection pool metrics visible in dashboard

### Monitoring & Alerting
- [ ] Connection pool count tracked in real-time
- [ ] Alert at 80% capacity
- [ ] Alert at 95% capacity (critical)
- [ ] Dashboard shows pool trends

### Incident Response Playbook
- [ ] "Connection Pool Exhaustion" runbook created
- [ ] Steps to identify connection leaks
- [ ] Steps to increase pool size temporarily
- [ ] Steps to restart application pool

**Estimated Time Savings**: Future incidents resolved in 10 minutes vs 4+ hours
```

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **root-cause-analysis** (`../../shared-skills/root-cause-analysis.md`)
  - Multi-factor analysis
  - Evidence synthesis
  - Causality determination

- **performance-analysis-framework** (`../../shared-skills/performance-analysis-framework.md`)
  - Resource exhaustion patterns
  - Correlation analysis
  - Impact assessment

- **code-review-best-practices** (`../../shared-skills/code-review-best-practices.md`)
  - Resource management patterns
  - Defensive programming
  - Best practice identification

## Error Handling

### Scenario: Too Few Errors (< 2)
**When**: Only 1 error provided
**Recovery**: Suggest single error analysis
**User Message**:
```
⚠ Correlation requires at least 2 errors.

Provided: 1 error

For single error analysis, use:
/analyze-stacktrace

Cannot correlate with only 1 error.
```

### Scenario: Errors Too Dissimilar (No Correlation)
**When**: All correlation scores < 0.5
**Recovery**: Report low correlation, analyze separately
**User Message**:
```
✓ Correlation analysis complete - No strong correlation found.

**Errors Analyzed**: 5
**Average Correlation**: 0.32 (Low)
**Interpretation**: Errors appear unrelated (different root causes)

**Recommendation**:
Analyze each error individually using:
- /analyze-stacktrace (for single error deep dive)
- /analyze-bug-pattern (for pattern-based analysis)

Including detailed analysis of each error in report...
```

### Scenario: Incomplete Stack Traces
**When**: Errors lack stack traces
**Recovery**: Use error messages and timing for correlation
**User Message**:
```
⚠ Some errors lack stack traces (3 out of 5).

**With Stack Traces**: E1, E2
**Without Stack Traces**: E3, E4, E5

Correlation analysis will rely on:
- Error messages
- Timing proximity
- Component information

Results may be less precise.
Proceeding with available data...
```

### Scenario: Large Time Window (> 24 hours)
**When**: Errors span > 24 hours
**Recovery**: Suggest narrowing window, proceed with caution
**User Message**:
```
⚠ Error time window is large (72 hours).

Errors separated by long time periods may not be correlated.

**Suggestion**: Narrow to incident window (e.g., --time-window="1 hour")

Proceeding with full window, but results may include false correlations...
```

### Scenario: Too Many Errors (> 15)
**When**: More than 15 distinct errors
**Recovery**: Filter to most frequent or recent, analyze top errors
**User Message**:
```
⚠ Too many errors to analyze (42 errors found).

Filtering to top 15 most frequent errors:
- E1: 87 occurrences (included)
- E2: 56 occurrences (included)
- ...
- E15: 12 occurrences (included)
- E16: 8 occurrences (excluded)

Analyzing top 15 errors. Full list available in report appendix.
```

### Scenario: Complex Multi-Root-Cause
**When**: Multiple correlation clusters (multiple root causes)
**Recovery**: Enable Sequential Thinking for deep analysis
**User Message**:
```
🔍 Found multiple correlation clusters (2+ root causes).

Enabling deep analysis mode to identify all root causes.

**Cluster 1**: E1, E2, E3 (correlation: 0.92)
**Cluster 2**: E4, E5 (correlation: 0.89)
**Between clusters**: correlation: 0.45 (low)

Analyzing each cluster separately...
Estimated time: 25-30 minutes
```

## Configuration

### Required Settings
None - agent works with defaults

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "root-cause-analyzer": {
    "error-correlation-analyzer": {
      "default_time_window_hours": 24,
      "min_correlation_score": 0.6,
      "max_errors_to_correlate": 15,
      "enable_sequential_thinking": "conditional",
      "sequential_thinking_trigger": {
        "multiple_clusters": true,
        "low_avg_correlation": 0.7
      },
      "correlation_weights": {
        "time_proximity": 0.3,
        "code_path_overlap": 0.3,
        "dependency_overlap": 0.2,
        "exception_similarity": 0.2
      },
      "timeout_minutes": 45,
      "include_diagnostic_errors": true,
      "search_git_history_for_fixes": true
    }
  }
}
```

**Configuration Options**:
- `default_time_window_hours`: Default window if not specified (default: 24)
- `min_correlation_score`: Minimum score for correlation (default: 0.6)
- `max_errors_to_correlate`: Maximum errors to analyze (default: 15)
- `enable_sequential_thinking`: "always", "conditional", or "never" (default: "conditional")
- `correlation_weights`: Weights for scoring (must sum to 1.0)
- `timeout_minutes`: Maximum analysis time (default: 45)
- `include_diagnostic_errors`: Include WARN-level errors (default: true)
- `search_git_history_for_fixes`: Look for previous fixes in git (default: true)

## Tools Required

- **Bash**: Read log files, parse timestamps, execute git commands
- **Glob**: Find log files by pattern (*.log, error-*.log)
- **Grep**: Parse error logs, extract stack traces, search code for patterns
- **Read**: Read source files to understand shared code paths
- **Write**: Generate comprehensive correlation report

## Examples

### Example 1: Simple Correlation (Single Root Cause)
**Input**:
```bash
/correlate-errors "Timeout in OrderService, Deadlock in PaymentService, Connection pool exhausted"
```

**Process**:
- Phase 1: Extract 3 errors from description, normalize (5 min)
- Phase 2: Parse stack traces, identify patterns (7 min)
- Phase 3: Find shared code path (SqlConnection usage) (8 min)
- Phase 4: Analyze connection pool dependency (6 min)
- Phase 5: Calculate correlation matrix (avg: 0.88) (5 min)
- Phase 6: Identify root cause (connection leak), generate fix (6 min)

**Output**: Report with:
- Root cause: Connection leak → Pool exhaustion
- Correlation: 0.88 (Very High)
- Fix: Add using statements (2 hours)
- Impact: Resolves all 3 errors

**Time**: ~37 minutes
**Confidence**: 95%

### Example 2: Complex Correlation (Multiple Clusters)
**Input**:
```bash
/correlate-errors logs/production-2026-01-15.log --time-window="2 hours"
```

**Process**:
- Phase 1: Parse log file, extract 8 errors (7 min)
- Phase 2: Parse 8 stack traces (10 min)
- Phase 3: Identify 2 distinct code path groups (12 min)
- Phase 4: Analyze dependencies for each group (10 min)
- Phase 5: Calculate matrix, find 2 clusters (8 min) [Sequential Thinking enabled]
  - Cluster 1: Database errors (E1-E4, correlation: 0.91)
  - Cluster 2: Cache errors (E5-E8, correlation: 0.87)
  - Cross-cluster correlation: 0.35 (unrelated)
  - Reflection: "Are these truly separate root causes or related?"
  - Conclusion: 2 independent root causes
- Phase 6: Generate 2 fix strategies (10 min)

**Output**: Report with:
- Root cause 1: Connection leak (E1-E4)
- Root cause 2: Cache expiration bug (E5-E8)
- Fix 1: Connection disposal (resolves E1-E4)
- Fix 2: Cache configuration (resolves E5-E8)

**Time**: ~57 minutes
**Confidence**: 88% (Sequential Thinking for complex analysis)

### Example 3: Cascading Failure
**Input**:
```bash
/correlate-errors logs/incident-*.log --time-window="30 minutes"
```

**Process**:
- Phase 1: Parse 3 log files, extract 12 errors (8 min)
- Phase 2: Parse stack traces, find cascading pattern (9 min)
- Phase 3: Identify primary error triggers cascading failures (11 min)
- Phase 4: Analyze domino effect (database → cache → API) (9 min)
- Phase 5: Build timeline of cascading errors (6 min)
- Phase 6: Generate fix addressing primary trigger (7 min)

**Output**: Report with:
- Primary error: Database connection timeout
- Cascading: Cache miss → API overload → Full system failure
- Fix: Increase connection timeout + add circuit breaker
- Timeline: Shows 30-minute cascade from first error to full outage

**Time**: ~50 minutes
**Confidence**: 92%

## Success Metrics

Analysis is successful when:
- [ ] All errors collected and normalized
- [ ] Stack traces parsed (if available)
- [ ] Common code paths identified
- [ ] Shared dependencies documented
- [ ] Correlation matrix calculated
- [ ] Correlation scores > threshold for related errors
- [ ] Root cause(s) identified with high confidence (>85%)
- [ ] All errors explained by root cause(s)
- [ ] Unified fix strategy provided (resolves multiple errors)
- [ ] Implementation guidance complete
- [ ] Prevention recommendations actionable
- [ ] Report comprehensive and well-structured
- [ ] Report saved to correct output directory

## Related Agents

- **codebase-pattern-analyzer**: Use to find similar patterns after identifying root cause
- **regression-analyzer**: Use to find when root cause was introduced via git history
- **stack-trace-analyzer**: Use for detailed analysis of individual errors before correlation
- **impact-analyzer**: Use to assess impact of proposed fixes

## Related Documentation

- `../../shared-skills/root-cause-analysis.md` - Root cause methodology
- `../../shared-skills/performance-analysis-framework.md` - Correlation analysis techniques
- `../commands/correlate-errors.md` - Command specification
- `../../../docs/WORKFLOW_DECISION_GUIDE.md` - When to use which analysis agent

---

**Agent Status**: Production Ready
**Verification Mode**: Enabled (all findings backed by error log evidence and code analysis)
**Sequential Thinking**: Conditional (auto-enabled for multiple correlation clusters or ambiguous root causes)
**Average Duration**: 35-55 minutes depending on error count and correlation complexity
