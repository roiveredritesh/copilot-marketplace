---
description: "Analyze database query, stored procedure, or view for optimization using parallel task execution"
argument-hint: "<query-name> [--report=full|summary]"
allowed-tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Command: /analyze-query

## Usage

```
/analyze-query <query-name> [--report=full|summary]
```

## Arguments

### Required Arguments

- **query-name**: Name of query/SP/view (e.g., sp_GetUsers)

### Optional Flags

- **--report=full|summary**: Report level (full by default)

## Examples

```bash
/analyze-query sp_GetUsers
/analyze-query vwActiveOrders --report=summary
/analyze-query sp_GenerateReport
```

## Execution Model

**Parallel Sync Execution**: 3 tasks run concurrently for 2x faster analysis
- Total time: 6-8 minutes (vs 15-30 min sequential)
- All results synthesized into comprehensive query analysis
- Progress tracked in real-time

## Implementation

### Step 1: Parse Arguments
- Extract query name: `${QUERY_NAME}`
- Validate format
- Parse optional report level flag
- Set output directory: `marketplace/output/analysis/query-${QUERY_NAME}/`

### Step 2: Validate MSSQL MCP
- Check MSSQL MCP is configured
- Verify connection
- Test database access

### Step 3: Create Output Directory
- Create `marketplace/output/analysis/query-${QUERY_NAME}/` if not exists
- Initialize progress tracking

### Step 4: Execute Parallel Analysis

⚠️ **CRITICAL**: You MUST invoke ALL 3 Task tools below in a SINGLE message to enable parallel execution. Do NOT invoke them sequentially. Send all Task tool calls in one message block.

**Task 1: Fetch Query Definition**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a query definition fetcher. Use Bash with MSSQL MCP to fetch the definition of query/stored procedure/view ${QUERY_NAME}. Extract: complete SQL code, parameters, return values, dependencies. Save to: marketplace/output/analysis/query-${QUERY_NAME}/definition.sql with formatted SQL and metadata comments. Time limit: 2 minutes."
- Expected output: `marketplace/output/analysis/query-${QUERY_NAME}/definition.sql`
- Estimated time: 1-2 minutes

**Task 2: Analyze Structure and Execution Plan**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a query structure analyzer. Fetch execution plan for ${QUERY_NAME} using MSSQL MCP. Analyze: query structure, JOIN types, WHERE clauses, subqueries, CTEs, indexes used, table scans, key lookups, sort operations. Identify performance bottlenecks. Save findings to: marketplace/output/analysis/query-${QUERY_NAME}/execution-plan.md with detailed breakdown of operations and their costs."
- Expected output: `marketplace/output/analysis/query-${QUERY_NAME}/execution-plan.md`
- Estimated time: 3-4 minutes

**Task 3: Check Query Usage in Codebase**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a query usage analyzer. Use Grep to search codebase for references to ${QUERY_NAME}. Find: stored procedure calls, query executions, ORM references, LINQ queries. Identify all files calling this query and their contexts. Analyze how query results are used. Save to: marketplace/output/analysis/query-${QUERY_NAME}/usage.md with file paths, line numbers, and usage patterns."
- Expected output: `marketplace/output/analysis/query-${QUERY_NAME}/usage.md`
- Estimated time: 2-3 minutes

### Step 5: Synthesize Final Report

After ALL 3 parallel tasks complete:
1. Read all 3 output files from `marketplace/output/analysis/query-${QUERY_NAME}/`
2. Combine findings into comprehensive query analysis
3. Identify performance bottlenecks and inefficiencies
4. Calculate potential improvement estimates
5. Generate optimization recommendations:
   - Quick wins (index additions, simple rewrites)
   - Medium improvements (query restructuring)
   - Major optimizations (schema changes, architecture)
6. Provide before/after performance estimates
7. Add implementation guidance with SQL examples
8. Save final report to: `marketplace/output/analysis/query-${QUERY_NAME}/analysis.md`

### Step 6: Display Progress and Results

Display execution progress in real-time:
```
Starting parallel analysis of ${QUERY_NAME}...

[1/3] ⏳ Fetching query definition...
[2/3] ⏳ Analyzing execution plan...
[3/3] ⏳ Checking usage in codebase...

[1/3] ✓ Fetched definition (1 min)
[2/3] ✓ Analyzed execution plan (3 min)
[3/3] ✓ Checked usage (2 min)

Synthesizing results...
✓ Final report generated

# Query Analysis Summary for ${QUERY_NAME}

- **Primary Bottleneck**: [identified issue]
- **Current Performance**: [execution time]
- **Potential Improvement**: [percentage]
- **Recommendation**: [optimization approach]

Full report: marketplace/output/analysis/query-${QUERY_NAME}/analysis.md
```

### Step 7: Return Response

Display completion status:
```
# ✓ Query Analysis Complete: ${QUERY_NAME}

**Execution Time**: 6-8 minutes (parallel)

**Output Files**:
- Full Analysis: marketplace/output/analysis/query-${QUERY_NAME}/analysis.md
- Query Definition: marketplace/output/analysis/query-${QUERY_NAME}/definition.sql
- Execution Plan: marketplace/output/analysis/query-${QUERY_NAME}/execution-plan.md
- Usage Patterns: marketplace/output/analysis/query-${QUERY_NAME}/usage.md

**Performance Summary**:
- Current: [time]
- Potential: [improved time]
- Improvement: [percentage]

**Next Steps**:
1. Review the analysis.md for detailed findings
2. Test recommended optimizations in staging
3. Implement chosen improvements
4. Benchmark before/after performance
5. Deploy to production with monitoring
```

## Output Locations

- Full Analysis: `marketplace/output/analysis/query-<query-name>/analysis.md`
- Query Definition: `marketplace/output/analysis/query-<query-name>/definition.sql`
- Execution Plan: `marketplace/output/analysis/query-<query-name>/execution-plan.md`
- Usage Patterns: `marketplace/output/analysis/query-<query-name>/usage.md`

## Execution Time Comparison

**Parallel Execution (v2.0.0)**:
- Simple query: 4-6 minutes
- Complex query: 6-8 minutes
- Very complex: 8-10 minutes

**Sequential Execution (v1.0.0)**:
- Simple query: 8-15 minutes
- Complex query: 15-30 minutes
- Very complex: 30-45 minutes

**Speed improvement**: 2-3x faster with parallel execution

## FAQ

**Q: What Jira server is supported?**
A: Any MSSQL database configured in MCP

**Q: Can I analyze views and CTEs?**
A: Yes, any database query object

**Q: How does parallel execution work?**
A: 3 tasks (fetch definition, analyze plan, check usage) run concurrently, then results are synthesized

**Q: What if a parallel task fails?**
A: Other tasks continue. Synthesis step will note missing data and provide partial analysis

**Q: Can I run this command multiple times in parallel?**
A: Yes, each invocation uses separate output directories

**Q: What if MSSQL is unavailable?**
A: Tasks 1 and 2 will fail with clear error message. Task 3 will execute on local code

---

**Command Version**: 2.0.0
**Last Updated**: 2025-11-04
**Execution Model**: Parallel Sync (3 concurrent tasks)
**Expected Duration**: 6-8 minutes
**Uses Tasks**: Yes (3 parallel Task tool invocations)
