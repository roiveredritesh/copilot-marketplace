---
description: "Analyze and optimize database query or stored procedure"
argument-hint: "<query-name> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write]
---

# Command: /optimize-query

## Usage

```
/optimize-query <query-name> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **query-name**: Name of query, stored procedure, or view
  - Examples: `sp_GetUsers`, `vwActiveOrders`, `GetOrderDetails`
  - Format: Case-sensitive, matches database object name
  - Can reference stored procedures, views, or queries

### Optional Flags

- **--async**: Execute in background
  - Returns immediately with task ID
  - Optimization analysis happens asynchronously
  - Example: `/optimize-query sp_GetUsers --async`

- **--wait**: Execute synchronously, block until complete
  - Waits for optimization analysis to complete
  - Returns full report
  - Example: `/optimize-query sp_GetUsers --wait`
  - Default if neither flag specified

- **--report=full|summary**
  - `full`: Comprehensive optimization report (default)
  - `summary`: Brief summary of findings
  - Example: `/optimize-query sp_GetUsers --report=summary`

## Examples

### Example 1: Quick Analysis (Sync, Full Report)
```
/optimize-query sp_GetUsers --wait
```
Output:
```
Analyzing query: sp_GetUsers
[Fetching query definition...]
[Analyzing structure...]
[Checking execution plan...]
[Identifying bottlenecks...]
[Generating recommendations...]

✅ Analysis Complete!

Report: marketplace/output/reviews/sp_GetUsers-optimization.md

Key Findings:
- Primary Bottleneck: Missing index on Orders.Status (75% of time)
- Impact: 12.3 sec → 1.2 sec possible (90% improvement)
- Recommendation: CREATE INDEX IX_Orders_Status

Quick Fix Options:
1. Add missing index (5 min, +60% faster)
2. Restructure query (20 min, +75% faster)
3. Comprehensive redesign (2 hours, +90% faster)
```

### Example 2: Background Analysis (Async)
```
/optimize-query sp_GetUsers --async
```
Output:
```
Starting background analysis...

Task ID: task-20251030-170000-query-abc123
Status: Queued
Estimated time: 10-15 minutes

Check progress:
  /task-status task-20251030-170000-query-abc123

When complete:
  marketplace/output/reviews/sp_GetUsers-optimization.md
```

### Example 3: Quick Summary (Async)
```
/optimize-query sp_GetOrderDetails --async --report=summary
```
Output:
```
Starting background analysis (summary only)...

Task ID: task-20251030-170015-query-def456
Estimated time: 5-10 minutes

Summary will be saved to:
  marketplace/output/reviews/sp_GetOrderDetails-optimization-summary.md
```

---

## Implementation

### Step 1: Parse and Validate Arguments

```
1. Parse input:
   - Extract query-name
   - Extract flags (--async, --wait, --report)
   - Validate format

2. Validate parameters:
   - query-name not empty
   - query-name contains valid characters
   - Flags are recognized
   - No conflicting flags

3. Set execution mode:
   - If --async: mode = async
   - If --wait: mode = sync
   - If neither: mode = sync (default)

4. Set report level:
   - If --report=summary: level = summary
   - If --report=full or not specified: level = full
```

### Step 2: Verify MSSQL MCP Availability

```
1. Check MSSQL MCP configuration:
   - Verify .mcp.json has mssql server
   - Check connection string
   - Validate credentials

2. If available:
   - Proceed to Step 3

3. If unavailable:
   - Return error: "MSSQL MCP not configured"
   - Provide setup instructions
```

### Step 3: Queue or Execute Optimization Task

**For Async Execution:**
```
1. Create task entry:
   {
     "task_id": "task-20251030-170000-query-abc123",
     "type": "query-optimize",
     "query_name": "sp_GetUsers",
     "report_level": "full",
     "created": "2025-10-30T17:00:00Z",
     "estimated_completion": "2025-10-30T17:15:00Z"
   }

2. Return immediately:
   Task ID: task-20251030-170000-query-abc123
   Status: Queued
   Estimated time: 10-15 minutes

3. Background coordinator processes:
   - Fetches query definition via MSSQL MCP
   - Analyzes structure and complexity
   - Checks execution plan
   - Identifies bottlenecks
   - Generates optimization report
```

**For Sync Execution:**
```
1. Display progress:
   Analyzing query: sp_GetUsers
   [Fetching query definition...]
   [Analyzing structure...]
   [Checking execution plan...]
   [Generating recommendations...]

2. Delegate to query-optimizer agent
   - Wait for completion
   - Receive analysis data

3. Display report or summary
   - Full: Show all analysis
   - Summary: Show key findings

4. Return completion with report location
```

### Step 4: Return Response

**Async Response:**
```
Status: Queued
Task ID: task-20251030-170000-query-abc123
Estimated time: 10-15 minutes

Check progress:
  /task-status task-20251030-170000-query-abc123

Report will be saved to:
  marketplace/output/reviews/sp_GetUsers-optimization.md
```

**Sync Response (Full Report):**
```
# Query Optimization Report

**Query Name**: sp_GetUsers
**Analysis Time**: 12 minutes
**Primary Bottleneck**: Missing index on Orders.Status

## Summary
Current execution time: 3.1 seconds
Recommended fix: Create index on Orders.Status
Expected improvement: 60% (to 1.2 seconds)

[Full report content...]

Report saved to: marketplace/output/reviews/sp_GetUsers-optimization.md
```

---

## Input Validation

### Valid Inputs
```
✅ /optimize-query sp_GetUsers
✅ /optimize-query sp_GetUsers --wait
✅ /optimize-query sp_GetUsers --async
✅ /optimize-query sp_GetUsers --async --report=summary
✅ /optimize-query vwActiveOrders
✅ /optimize-query GetOrderDetails
```

### Invalid Inputs
```
❌ /optimize-query                  (no query name)
❌ /optimize-query ""               (empty name)
❌ /optimize-query sp_NonExistent   (query doesn't exist)
❌ /optimize-query sp_Users --wait --async  (conflicting)
❌ /optimize-query sp_Users --report=invalid (bad report type)
```

### Error Messages

**Missing Query Name:**
```
Error: Query name required
Usage: /optimize-query <query-name> [--async|--wait] [--report=full|summary]
Example: /optimize-query sp_GetUsers
```

**Query Not Found:**
```
Error: Query 'sp_GetUsers' not found in database

Available stored procedures:
  - sp_GetActiveUsers
  - sp_GetUserOrders
  - sp_GenerateReport

Tip: Query names are case-sensitive
Try: /optimize-query sp_GetActiveUsers
```

**MSSQL MCP Not Available:**
```
Error: MSSQL MCP server not configured

To use this command, configure MSSQL MCP:

1. Add to .mcp.json:
   "mssql": {
     "command": "node",
     "args": ["@modelcontextprotocol/server-mssql/dist/index.js"],
     "env": {
       "MSSQL_CONNECTION_STRING": "Server=localhost;Database=mydb;..."
     }
   }

2. Restart Claude Code
```

---

## Output Locations

### Report Files
```
Full Optimization:  marketplace/output/reviews/<query-name>-optimization.md
Summary:           marketplace/output/reviews/<query-name>-optimization-summary.md
Status:            .claude/task-status/<task-id>.md
```

### Examples
```
marketplace/output/reviews/sp_GetUsers-optimization.md
marketplace/output/reviews/vwActiveOrders-optimization-summary.md
.claude/task-status/task-20251030-170000-query-abc123.md
```

---

## Typical Analysis Time

- **Simple Query** (< 5 tables, no subqueries): 3-5 minutes
- **Medium Complexity** (5-10 tables, some subqueries): 8-15 minutes
- **Complex Query** (10+ tables, multiple subqueries): 15-30 minutes
- **Very Complex** (nested, recursive, CTE): 30-45 minutes

**Recommendation**: Use `--async` for complex queries.

---

## What Gets Analyzed

### Query Structure
- Tables and views used
- JOIN conditions and types
- WHERE clause predicates
- GROUP BY and HAVING
- ORDER BY and DISTINCT
- Subqueries and CTEs

### Execution Plan
- Index usage
- Scan vs seek operations
- Join strategies
- Aggregate methods
- Sort operations
- Predicate pushdown

### Performance Issues
- Missing indexes
- Full table scans
- N+1 query patterns
- Inefficient JOINs
- Non-sargable predicates
- Correlated subqueries
- Index fragmentation

### Optimization Recommendations
- Quick fix (5-15 minutes, moderate improvement)
- Proper fix (20-30 minutes, good improvement)
- Comprehensive solution (1-3 hours, maximum improvement)

---

## Related Commands

- `/task-status <task-id>` - Check optimization progress
- `/optimize-algorithm <file>` - Optimize application algorithms
- `/analyze-query <query-name>` - Analyze without optimization
- `/review-pr` - Review code including query quality

---

## FAQ

**Q: What databases are supported?**
A: MSSQL (SQL Server). Other databases may be added in future versions.

**Q: Can I optimize views?**
A: Yes! The command optimizes stored procedures, views, and queries.

**Q: How accurate are the recommendations?**
A: Very accurate! Based on actual execution plans and query analysis.

**Q: Will optimization change query results?**
A: No! Optimizations maintain exact same results, just faster.

**Q: Can I benchmark before/after?**
A: Yes! The report includes SQL to run benchmarks.

**Q: What if the query is very complex?**
A: Use `--async` for thorough analysis without timeouts.

**Q: Can I get just the quick fix?**
A: Yes! Use `--report=summary` for quick recommendations.

**Q: Where are recommendations saved?**
A: `marketplace/output/reviews/<query-name>-optimization.md`

---

## Pro Tips

**Tip 1: Check Index Recommendations**
The report suggests missing indexes with creation scripts.

**Tip 2: Test Before Production**
Always test optimizations in staging first.

**Tip 3: Monitor After Deployment**
Watch query execution times to verify improvements.

**Tip 4: Use Full Report for Documentation**
Save reports to document optimization decisions.

**Tip 5: Batch Multiple Optimizations**
Queue multiple queries with `--async` for parallel analysis.

---

## Troubleshooting

### MSSQL MCP Not Available
```
Solution:
1. Verify .mcp.json has mssql configuration
2. Check connection string is correct
3. Ensure database is accessible
4. Restart Claude Code
```

### Query Not Found
```
Solution:
1. Verify query name is correct (case-sensitive)
2. Check query exists in current database
3. Ensure you have permissions to view it
```

### Timeout
```
Solution:
1. Very large queries may timeout
2. Use --async for better timeout handling
3. Consider analyzing in parts
```

---

## Command Lifecycle

```
1. User: /optimize-query sp_GetUsers --wait

2. Command validates:
   - Query name provided
   - MSSQL MCP available
   - Query exists in database

3. Delegates to query-optimizer agent:
   - Fetches query definition
   - Analyzes structure
   - Checks execution plan
   - Generates recommendations
   - Creates optimization report

4. Report saved:
   marketplace/output/reviews/sp_GetUsers-optimization.md

5. User reviews:
   - Examines recommendations
   - Selects optimization approach
   - Implements changes
   - Tests improvements
```

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Associated Plugin**: Optimization Engine
**Delegated To**: query-optimizer agent
**Task Coverage**: Task #4 (Analyze database performance), Task #5 (Optimize database queries)
