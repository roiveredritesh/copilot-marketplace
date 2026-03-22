---
name: db-query-analyzer
description: Analyzes database queries and stored procedures for optimization and issues
task_type: query-analyze
mcp_required: [mssql]
tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Database Query Analyzer

**Version**: 2.0.0
**Plugin**: analysis-toolkit
**Task Coverage**: Task #5 (Analyze database performance and query issues)
**MCP Requirements**: MSSQL MCP
**Sequential Thinking**: Conditional (enabled for complex queries with multiple subqueries or joins)
**Last Updated**: 2026-01-15

## Purpose

Performs comprehensive analysis of SQL Server queries, stored procedures, and views to identify performance bottlenecks, logical errors, and optimization opportunities. Fetches query definitions via MSSQL MCP, analyzes execution plans, identifies missing indexes, detects N+1 patterns, and generates actionable optimization recommendations with SQL scripts.

This agent serves as a database performance consultant, bridging the gap between slow queries and optimized solutions. It excels at distinguishing between symptoms (slow execution) and root causes (missing indexes, inefficient joins, poor query structure).

## When to Use

Use this agent when you need to:
- Investigate slow database queries or stored procedures
- Analyze query execution plans for bottlenecks
- Identify missing indexes or poorly structured queries
- Debug SQL logic errors or unexpected results
- Optimize complex queries with multiple joins
- Review stored procedure performance
- Investigate N+1 query patterns in application code
- Understand query performance degradation over time
- Prepare queries for production deployment
- Review database view definitions for issues

Best for queries with:
- Long execution times (>1 second)
- High CPU or I/O usage
- Table scans on large tables
- Multiple nested subqueries
- Complex JOIN conditions
- Missing or incorrect indexes

## When NOT to Use

Do NOT use this agent when:
- You need to design a new database schema (use design agents instead)
- Issue is database server configuration, not query code
- You need to analyze entire database architecture (use architecture agents)
- Query is already optimal and you're investigating application-level issues
- Issue is network latency or connection pool exhaustion
- You need to migrate database schema (use migration agents)
- Problem is data quality, not query performance

For these scenarios, consider:
- **Schema design**: `/design-system` with database focus
- **Architecture review**: `/analyze-architecture`
- **Application performance**: `/optimize-algorithm`
- **Impact analysis**: `/analyze-impact` for schema changes

## Input

**Format**: Command with query identifier or file path

**Required Fields**:
- `query_identifier`: Query name, stored procedure name, or file path
  - Examples: "GetUserByEmail", "usp_GetOrders", "Queries/UserQueries.sql"

**Optional Fields**:
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--async`: Run in background (default: foreground)
- `--wait`: Wait for completion (default: true)
- `--include-execution-plan`: Fetch and analyze execution plan (default: true if MCP available)

**Example**:
```bash
/analyze-query GetUserByEmail
/analyze-query usp_ProcessOrders --report=full
/analyze-query Queries/DashboardQuery.sql
/analyze-query GetRecentOrders --async
```

## Output

**Format**: Markdown report saved to `marketplace/output/analysis/<query-name>-analysis.md`

**Main Sections**:
1. **Executive Summary** - Query overview and key findings
2. **Query Analysis** - Query structure, tables, joins, predicates
3. **Execution Plan Analysis** - Bottlenecks, scans vs seeks, index usage
4. **Performance Issues** - Identified problems with severity
5. **Optimization Opportunities** - Missing indexes, query rewrites
6. **Solution Approaches** - Quick fix, proper fix, and comprehensive optimization
7. **SQL Scripts** - Implementation-ready SQL code
8. **Expected Improvements** - Performance metrics and estimates
9. **Testing Guidance** - Validation checklist

**Example Output Snippet**:
```markdown
# Query Analysis: GetUserByEmail

## Executive Summary
**Query**: GetUserByEmail (Stored Procedure)
**Current Performance**: 850ms average execution time
**Primary Issue**: Table scan on Users table (5M rows)
**Root Cause**: Missing index on Email column
**Expected Improvement**: 850ms → 15ms (98% faster)

## Primary Recommendation
Add non-clustered index on Users.Email:
```sql
CREATE NONCLUSTERED INDEX IX_Users_Email
ON Users(Email) INCLUDE (UserId, Username, IsActive);
```
```

## Process Overview

The agent follows a systematic six-phase analysis process that starts with fetching the query definition from MSSQL MCP and progressively drills down from query structure to execution plan analysis to optimization recommendations. It combines SQL parsing, execution plan interpretation, and database best practices to build a complete optimization picture.

The analysis begins by understanding query structure (tables, joins, predicates), then examines how SQL Server executes it (execution plan), identifies bottlenecks (scans, lookups, sorts), and finally generates optimized solutions with concrete SQL scripts.

For complex queries with multiple subqueries, CTEs, or intricate join conditions, the agent can enable Sequential Thinking to provide deeper reflection points and course correction during analysis.

## Detailed Process

### Phase 1: Query Definition Retrieval
**Duration**: 2-5% of total time
**Input**: Query identifier (name or file path)
**Process**:
1. Determine query source (MCP vs file):
   - If name only: Connect to MSSQL via MCP and fetch definition
   - If file path: Read query from file system
2. Retrieve stored procedure, view, or query text
3. Extract query metadata (parameters, return type, dependencies)
4. Identify query type (SELECT, INSERT, UPDATE, DELETE, MERGE)
5. Parse query structure (tables, columns, conditions)
6. Extract comments and annotations

**Tools Used**: MSSQL MCP or Read
**Output**: Complete query definition with metadata
**Success Criteria**:
- Query definition successfully retrieved
- Query type identified
- Tables and columns extracted
- Parameters documented (if applicable)

**Error Handling**: If MSSQL MCP unavailable, prompt user to provide query text directly or specify file path.

### Phase 2: Query Structure Analysis
**Duration**: 15-20% of total time
**Input**: Query definition from Phase 1
**Process**:
1. Parse SQL syntax to extract:
   - SELECT clause: Columns, expressions, aggregates
   - FROM clause: Tables, table aliases
   - JOIN clauses: Join types (INNER, LEFT, RIGHT, FULL), join conditions
   - WHERE clause: Filter predicates, operators
   - GROUP BY clause: Grouping columns
   - HAVING clause: Aggregate filters
   - ORDER BY clause: Sort columns and direction
   - Subqueries and CTEs (Common Table Expressions)
2. Identify table relationships and dependencies
3. Map column usage (selected, filtered, joined, sorted)
4. Detect query complexity indicators:
   - Number of tables (2-3: simple, 4-6: moderate, 7+: complex)
   - Subquery depth (0: none, 1-2: moderate, 3+: high)
   - CTE usage
   - UNION/INTERSECT/EXCEPT operations
5. Check for anti-patterns:
   - SELECT * usage
   - Functions on indexed columns in WHERE
   - OR conditions on different columns
   - NOT IN with nullable columns

**Tools Used**: Grep (for pattern detection), Read
**Output**: Structured query analysis with anti-patterns flagged
**Success Criteria**:
- All query components identified
- Table relationships mapped
- Anti-patterns detected
- Complexity assessed

**Example**:
```markdown
## Query Structure

### Tables Referenced
- Users (alias: u) - Base table
- Orders (alias: o) - INNER JOIN on u.UserId = o.UserId
- OrderItems (alias: oi) - INNER JOIN on o.OrderId = oi.OrderId

### Predicates (WHERE)
- u.Email = @Email (Parameter)
- u.IsActive = 1 (Constant)
- o.OrderDate >= DATEADD(day, -30, GETDATE()) (Function on column - POTENTIAL ISSUE)

### Columns Selected
- u.UserId, u.Username, u.Email
- COUNT(o.OrderId) AS OrderCount
- SUM(oi.Price) AS TotalSpent

### Anti-Patterns Detected
⚠️ Function on indexed column in WHERE: DATEADD on OrderDate
⚠️ SELECT COUNT(*) without covering index
```

### Phase 3: Execution Plan Analysis
**Duration**: 25-30% of total time (CRITICAL PHASE)
**Input**: Query structure from Phase 2
**Process**:
1. Fetch query execution plan via MSSQL MCP (if available):
   - Actual execution plan (if query has run recently)
   - Estimated execution plan (fallback)
2. Parse execution plan XML to identify:
   - **Scan operations**: Table scans, index scans (HIGH COST)
   - **Seek operations**: Index seeks, clustered index seeks (LOW COST)
   - **Join operations**: Nested loops, hash match, merge join
   - **Sort operations**: Sort (high memory usage)
   - **Key lookups**: RID lookups, key lookups (performance hit)
   - **Parallelism**: Parallel execution operators
3. Calculate cost distribution:
   - Identify most expensive operators (>10% of query cost)
   - Find bottleneck operations (>50% of query cost)
4. Analyze index usage:
   - Indexes used (seeks vs scans)
   - Missing index suggestions from SQL Server
   - Unused indexes on queried tables
5. Check statistics:
   - Estimated rows vs actual rows (cardinality estimation issues)
   - Data type mismatches causing implicit conversions

**If Sequential Thinking Enabled**:
- Reflection Point: "Is this the true bottleneck or a symptom of a deeper issue?"
- Course Correction: Re-examine query structure if execution plan doesn't align with expectations
- Confidence Scoring: Rate certainty of bottleneck identification

**Tools Used**: MSSQL MCP (for execution plan), Read, Grep
**Output**: Execution plan analysis with bottlenecks identified
**Success Criteria**:
- Execution plan retrieved (or analyzed manually if unavailable)
- Bottleneck operations identified
- Index usage documented
- Missing index recommendations extracted

**Example**:
```markdown
## Execution Plan Analysis

### Cost Distribution
1. **Table Scan on Users** (75% of query cost) ← PRIMARY BOTTLENECK
   - Scans 5,000,000 rows
   - Predicate: Email = @Email
   - Missing: Index on Email column

2. **Nested Loop Join** (15% of query cost)
   - Join: Users → Orders
   - Efficient (uses clustered index seek on Orders)

3. **Sort Operation** (8% of query cost)
   - Sorts result by Username
   - Memory grant: 10MB

### Index Usage
- ✅ PK_Users (Clustered Index) - Used for output
- ❌ No index on Users.Email - MISSING
- ✅ IX_Orders_UserId - Used efficiently

### SQL Server Recommendations
Missing Index (Impact: 95.5%):
CREATE NONCLUSTERED INDEX IX_Users_Email
ON Users(Email) INCLUDE (UserId, Username, IsActive);
```

### Phase 4: Performance Issue Identification
**Duration**: 15-20% of total time
**Input**: Query structure + Execution plan from Phases 2-3
**Process**:
1. Categorize issues by type:
   - **Missing Indexes** (HIGH IMPACT)
   - **Inefficient Joins** (MEDIUM-HIGH IMPACT)
   - **N+1 Query Patterns** (HIGH IMPACT if in loop)
   - **Unnecessary Sorts** (MEDIUM IMPACT)
   - **Subquery Inefficiencies** (VARIABLE IMPACT)
   - **Data Type Mismatches** (MEDIUM IMPACT)
   - **Logical Errors** (FUNCTIONAL IMPACT)
2. Assess severity for each issue:
   - CRITICAL: Causes timeout or blocks other queries
   - HIGH: >500ms execution time, affects user experience
   - MEDIUM: 100-500ms, noticeable but tolerable
   - LOW: <100ms, optimization nice-to-have
3. Quantify impact:
   - Current execution time
   - Current resource usage (CPU, I/O, memory)
   - Frequency (queries per second)
   - User impact (number of affected users)
4. Identify root causes vs symptoms:
   - Symptom: Query is slow
   - Immediate cause: Table scan on 5M rows
   - Root cause: Missing index on frequently filtered column

**Tools Used**: None (analysis phase)
**Output**: Prioritized list of performance issues with severity
**Success Criteria**:
- All issues identified and categorized
- Severity assigned to each issue
- Root causes distinguished from symptoms
- Impact quantified

**Example**:
```markdown
## Performance Issues

### CRITICAL Issues
None

### HIGH Issues
1. **Missing Index on Users.Email**
   - Impact: 75% of query cost
   - Current: Table scan (5M rows)
   - Expected: Index seek (<100 rows)
   - Improvement: 850ms → 15ms

### MEDIUM Issues
2. **Unnecessary Sort Operation**
   - Impact: 8% of query cost
   - Current: Sorts 1000 rows in memory
   - Potential: Add sort column to covering index
   - Improvement: 15ms → 12ms

### LOW Issues
3. **Function in WHERE Clause**
   - Impact: 2% of query cost
   - Issue: DATEADD on OrderDate prevents index usage
   - Note: Already filtered efficiently by UserId join
```

### Phase 5: Optimization Strategy Generation
**Duration**: 20-25% of total time
**Input**: Performance issues from Phase 4
**Process**:
1. Generate **Quick Fix** (15-30 min implementation):
   - Minimal changes to query or schema
   - Addresses most critical bottleneck
   - Temporary or partial solution
   - Example: Add single-column index

2. Generate **Proper Fix** (1-3 hours implementation):
   - Comprehensive solution addressing all high-priority issues
   - Production-ready implementation
   - Includes testing and validation
   - Example: Add covering index + rewrite subquery

3. Generate **Comprehensive Optimization** (4-8 hours implementation):
   - Complete query and schema optimization
   - Addresses all issues (high, medium, low)
   - Best practices implementation
   - Documentation and monitoring
   - Example: Full indexing strategy + query refactor + statistics update

4. For each solution:
   - Provide complete SQL scripts (ready to execute)
   - Explain trade-offs (query performance vs index maintenance cost)
   - Estimate performance improvement (with metrics)
   - Note prerequisites (e.g., clean up duplicate data first)
   - Identify risks (e.g., index size, maintenance window needed)

**Tools Used**: Write (for generating SQL scripts)
**Output**: Three optimization approaches with SQL implementation
**Success Criteria**:
- All three solutions provided
- Each solution has complete SQL scripts
- Performance improvements estimated
- Trade-offs clearly explained

**Example**:
```markdown
## Optimization Solutions

### 1. Quick Fix (15-30 minutes)
**Approach**: Add single-column index on Email
**SQL Script**:
```sql
-- Impact: 95% query improvement
CREATE NONCLUSTERED INDEX IX_Users_Email
ON Users(Email);
```
**Expected Improvement**: 850ms → 25ms (97% faster)
**Pros**: Fast to implement, immediate improvement
**Cons**: Not optimal (key lookup still required for Username, IsActive)

### 2. Proper Fix (1-3 hours)
**Approach**: Add covering index with INCLUDE columns
**SQL Script**:
```sql
-- Covering index eliminates key lookups
CREATE NONCLUSTERED INDEX IX_Users_Email
ON Users(Email)
INCLUDE (UserId, Username, IsActive);

-- Update statistics for cardinality estimation
UPDATE STATISTICS Users WITH FULLSCAN;
```
**Expected Improvement**: 850ms → 15ms (98% faster)
**Pros**: Optimal index design, no key lookups, accurate statistics
**Cons**: Larger index size (20MB), requires maintenance window for stats update
**Testing**:
```sql
-- Verify index usage
SET STATISTICS IO ON;
EXEC GetUserByEmail @Email = 'test@example.com';
-- Should show: Index Seek on IX_Users_Email, no Key Lookups
```

### 3. Comprehensive Optimization (4-8 hours)
**Approach**: Full indexing strategy + query refactor
**SQL Scripts**:
```sql
-- Step 1: Add covering index (as in Proper Fix)
CREATE NONCLUSTERED INDEX IX_Users_Email
ON Users(Email)
INCLUDE (UserId, Username, IsActive);

-- Step 2: Add index for ORDER BY to eliminate sort
CREATE NONCLUSTERED INDEX IX_Orders_UserId_OrderDate
ON Orders(UserId, OrderDate DESC)
INCLUDE (OrderId);

-- Step 3: Refactor query to remove function in WHERE
-- Instead of: o.OrderDate >= DATEADD(day, -30, GETDATE())
-- Use parameter: @StartDate = DATEADD(day, -30, GETDATE())
-- WHERE o.OrderDate >= @StartDate

-- Step 4: Update all statistics
UPDATE STATISTICS Users WITH FULLSCAN;
UPDATE STATISTICS Orders WITH FULLSCAN;

-- Step 5: Add query monitoring
-- (See monitoring script in appendix)
```
**Expected Improvement**: 850ms → 8ms (99% faster)
**Pros**: Maximum performance, follows best practices, maintainable
**Cons**: Requires schema changes, testing, deployment planning
**Additional Benefits**:
- Eliminates sort operation
- Enables index seek on OrderDate filter
- Improves related queries using same indexes
```

### Phase 6: Report Generation
**Duration**: 10-15% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Compile all findings into structured markdown report
2. Write executive summary (2-3 paragraphs)
3. Document query structure analysis
4. Include execution plan analysis with visual breakdown
5. Present performance issues with severity ratings
6. Include all three optimization approaches with complete SQL
7. Add expected improvement metrics (time, resource usage)
8. Create testing and validation checklist
9. Add monitoring and maintenance recommendations
10. Include appendix with:
    - Full query text
    - Execution plan details
    - Index definitions
    - Statistics queries
11. Save report to `marketplace/output/analysis/` directory

**Tools Used**: Write
**Output**: Comprehensive markdown report with SQL scripts
**Success Criteria**:
- Report is complete and well-structured
- All sections present
- SQL scripts are executable
- Performance estimates included
- Report saved successfully

**Example Structure**:
```markdown
# Query Analysis: GetUserByEmail

Generated: 2026-01-15 14:30:00
Duration: 35 minutes

## Executive Summary
...

## Query Definition
```sql
-- Stored Procedure: GetUserByEmail
...
```

## Query Structure Analysis
...

## Execution Plan Analysis
...

## Performance Issues
...

## Optimization Solutions
...

## Expected Improvements
| Metric | Current | Quick Fix | Proper Fix | Comprehensive |
|--------|---------|-----------|------------|---------------|
| Execution Time | 850ms | 25ms | 15ms | 8ms |
| Logical Reads | 12,500 | 150 | 8 | 5 |
| CPU Time | 780ms | 22ms | 12ms | 6ms |
| Improvement | - | 97% | 98% | 99% |

## Testing Checklist
- [ ] Execute query with sample data
- [ ] Verify index seek (not scan) in execution plan
- [ ] Test with various email formats
- [ ] Check query performance under load
- [ ] Validate result accuracy
- [ ] Monitor index fragmentation
...

## Monitoring & Maintenance
...

## Appendix
...
```

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **root-cause-analysis** (`../../shared-skills/root-cause-analysis.md`)
  - Systematic process for distinguishing symptoms from causes
  - Evidence collection and hypothesis validation
  - Root cause documentation patterns

- **sql-optimization-patterns** (`../../shared-skills/sql-optimization-patterns.md`)
  - SQL Server optimization best practices
  - Index design patterns
  - Query rewriting techniques
  - Common anti-patterns and solutions

- **query-performance-tuning** (`../../shared-skills/query-performance-tuning.md`)
  - Execution plan interpretation
  - Index tuning methodologies
  - Statistics and cardinality estimation
  - Performance baseline establishment

- **performance-analysis-framework** (`../../shared-skills/performance-analysis-framework.md`)
  - Performance impact assessment methodologies
  - Bottleneck identification techniques
  - Measurement and profiling approaches

## Error Handling

### Scenario: MSSQL MCP Server Unavailable
**When**: Cannot connect to MSSQL MCP to fetch query definition
**Recovery**:
1. Retry connection up to 3 times with exponential backoff
2. If still unavailable, prompt user to:
   - Provide query text directly (paste into chat)
   - Specify file path to query (.sql file)
   - Use local SQL Server Management Studio to extract definition
3. Continue analysis without execution plan (structure analysis only)
**User Message**:
```
⚠ MSSQL MCP unavailable. Please provide query text:
1. Paste SQL query directly
2. Provide file path to .sql file
3. Specify stored procedure name (I'll guide manual extraction)

Note: Without MCP, I can analyze query structure but not execution plan.
```

### Scenario: Query Not Found
**When**: Query/stored procedure name doesn't exist in database
**Recovery**: Search for similar names and suggest alternatives
**User Message**:
```
❌ Query "GetUserByEmaill" not found in database.
Did you mean one of these?
- GetUserByEmail (stored procedure)
- GetUsersByEmail (stored procedure)
- fn_GetUserEmail (function)

Please verify the query name or provide the SQL text directly.
```

### Scenario: Execution Plan Unavailable
**When**: Cannot retrieve execution plan (query not cached, MCP limitations)
**Recovery**: Analyze query structure and provide optimization based on best practices
**User Message**:
```
⚠ Execution plan unavailable for this query.
Performing structure-based analysis using SQL Server best practices.

Recommendations will be based on:
- Query structure analysis
- Index existence checks
- Common optimization patterns
- SQL Server best practices

For execution plan analysis, run the query in SQL Server and share the plan.
```

### Scenario: Complex Query with Multiple Subqueries
**When**: Query has 3+ levels of subqueries or 7+ joined tables
**Recovery**: Enable Sequential Thinking for deeper analysis with reflection points
**User Message**:
```
🔍 Complex query detected (8 tables, 3 subquery levels). Enabling deep analysis mode.
This analysis will take 20-30% longer but will provide:
- Reflection points for optimization alternatives
- Step-by-step bottleneck identification
- Multiple solution paths evaluated

Estimated time: 45-55 minutes
```

### Scenario: Logical Error in Query
**When**: Query structure suggests logical error (e.g., incorrect JOIN type, missing GROUP BY column)
**Recovery**: Flag error prominently in report and suggest correction
**User Message**:
```
🚨 LOGICAL ERROR DETECTED in query:
- GROUP BY clause includes u.UserId but SELECT includes u.Email
- This will cause aggregation error

Recommendation: Add u.Email to GROUP BY or remove from SELECT
Proceeding with analysis, but query must be corrected before optimization.
```

### Scenario: Analysis Timeout
**When**: Analysis exceeds 60 minutes (very complex query)
**Recovery**: Save partial results and offer to continue with specific focus
**User Message**:
```
⏱ Analysis timeout reached (60 minutes).
Partial results saved to: output/analysis/GetUserByEmail-partial.md

Continue with focused analysis? Options:
1. /continue-analysis GetUserByEmail --focus=indexes
2. /continue-analysis GetUserByEmail --focus=joins
3. /analyze-query GetUserByEmail --report=summary (faster)
```

## Configuration

### Required Settings
None - agent works with defaults

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "analysis-toolkit": {
    "db-query-analyzer": {
      "timeout_minutes": 60,
      "enable_sequential_thinking": "conditional",
      "sequential_thinking_trigger": {
        "min_tables": 7,
        "min_subquery_depth": 3
      },
      "report_detail_level": "full",
      "include_execution_plan": true,
      "include_sql_scripts": true,
      "estimate_improvements": true,
      "max_index_recommendations": 5
    }
  }
}
```

**Configuration Options**:
- `timeout_minutes`: Maximum analysis time (default: 60)
- `enable_sequential_thinking`: "always", "conditional", or "never" (default: "conditional")
- `sequential_thinking_trigger`: Conditions for enabling Sequential Thinking
- `report_detail_level`: "full" or "summary" (default: "full")
- `include_execution_plan`: Fetch and analyze execution plan (default: true)
- `include_sql_scripts`: Generate executable SQL scripts (default: true)
- `estimate_improvements`: Calculate performance improvement estimates (default: true)
- `max_index_recommendations`: Maximum indexes to recommend (default: 5)

## Tools Required

- **Bash**: Execute sqlcmd commands (if local SQL Server), file operations
- **Glob**: Find query files by pattern (*.sql)
- **Grep**: Search for query patterns, anti-patterns, specific SQL constructs
- **Read**: Read query files from filesystem
- **Write**: Generate analysis report with SQL scripts
- **Task**: Delegate to specialized sub-agents (if needed for complex scenarios)
- **MSSQL MCP**: Fetch query definitions, execution plans, table metadata

## Examples

### Example 1: Simple Query - Missing Index
**Input**:
```bash
/analyze-query GetUserByEmail
```

**Query**:
```sql
SELECT UserId, Username, Email
FROM Users
WHERE Email = @Email AND IsActive = 1;
```

**Process**:
- Phase 1: Fetch stored procedure (2 min)
- Phase 2: Parse structure (3 min)
- Phase 3: Analyze execution plan - finds table scan (8 min)
- Phase 4: Identify missing index (5 min)
- Phase 5: Generate 3 optimization solutions (6 min)
- Phase 6: Create report with SQL scripts (3 min)

**Output**: Report with:
- Root cause: Missing index on Email column
- Quick fix: Single-column index
- Proper fix: Covering index with INCLUDE
- Comprehensive: Full indexing strategy
- Expected: 850ms → 15ms (98% improvement)

**Time**: ~27 minutes
**Confidence**: 95%

### Example 2: Complex Query - N+1 Pattern
**Input**:
```bash
/analyze-query GetOrdersWithItems
```

**Query**: Multi-table join with subqueries
**Process**:
- Phase 1: Fetch stored procedure (3 min)
- Phase 2: Parse complex structure (8 tables, 2 subqueries) (10 min)
- Phase 3: Analyze execution plan (multiple issues) (18 min) [Sequential Thinking enabled]
  - Initial: Focus on table scans
  - Reflection: Inefficient join order also significant
  - Course correction: Prioritize join optimization + indexes
- Phase 4: Identify multiple issues (8 min)
- Phase 5: Generate layered optimization strategy (12 min)
- Phase 6: Create comprehensive report (6 min)

**Output**: Report with:
- Root causes: Missing indexes + inefficient join order + N+1 in calling code
- Multiple optimization layers
- Complete indexing strategy
- Query refactor suggestions
- Expected: 3.2s → 85ms (97% improvement)

**Time**: ~57 minutes
**Confidence**: 90%

### Example 3: Stored Procedure with Logical Error
**Input**:
```bash
/analyze-query usp_GetMonthlySales
```

**Query**: Aggregation with incorrect GROUP BY
**Process**:
- Phase 1: Fetch stored procedure (2 min)
- Phase 2: Parse structure - detect logical error (5 min)
- Phase 3: Cannot analyze execution plan (query errors) (2 min)
- Phase 4: Identify logical error as primary issue (3 min)
- Phase 5: Generate corrected query + optimizations (8 min)
- Phase 6: Create report with correction + optimization (4 min)

**Output**: Report with:
- **PRIMARY ISSUE**: Logical error in GROUP BY clause
- Corrected query
- Optimization recommendations (after correction)
- Testing checklist

**Time**: ~24 minutes
**Report**: Flags error prominently before optimizations

## Success Metrics

Analysis is successful when:
- [ ] Query definition successfully retrieved or provided
- [ ] Query structure fully parsed (tables, joins, predicates, columns)
- [ ] Execution plan analyzed (or structure-based analysis if unavailable)
- [ ] All performance bottlenecks identified
- [ ] Root causes distinguished from symptoms
- [ ] Three optimization solutions provided (quick, proper, comprehensive)
- [ ] All SQL scripts are executable and tested
- [ ] Performance improvements estimated with metrics
- [ ] Report is comprehensive and actionable
- [ ] Report saved to correct output directory
- [ ] Confidence level meets threshold (>85% for simple queries, >75% for complex)

## Related Agents

- **jira-root-cause-analyzer**: Use when query issue is reported in Jira ticket
- **impact-analyzer**: Use to analyze impact of proposed index/schema changes
- **stack-trace-analyzer**: Use when query causes application exception
- **optimization-engine**: Use for application-level query optimization (LINQ to SQL)

## Related Documentation

- `../../shared-skills/sql-optimization-patterns.md` - SQL optimization patterns
- `../../shared-skills/query-performance-tuning.md` - Query tuning methodology
- `../../shared-skills/root-cause-analysis.md` - Root cause methodology
- `../../../docs/WORKFLOW_DECISION_GUIDE.md` - When to use which analysis agent
- `../../../docs/MCP_CONFIGURATION_GUIDE.md` - MSSQL MCP setup
- `../commands/analyze-query.md` - Command specification

---

**Agent Status**: Production Ready
**Verification Mode**: Enabled (all findings backed by execution plan evidence)
**Sequential Thinking**: Conditional (auto-enabled for complex queries)
**Average Duration**: 25-45 minutes depending on query complexity
