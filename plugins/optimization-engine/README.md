# Optimization Engine Plugin

Database query and algorithm optimization with comprehensive performance tuning strategies.

## Overview

The Optimization Engine plugin provides advanced optimization capabilities for both database queries and application algorithms, identifying bottlenecks and recommending multi-level optimization approaches.

## Features

### Query Optimization
- MSSQL query, stored procedure, and view analysis
- Execution plan examination
- Missing index identification
- N+1 query pattern detection
- JOIN efficiency assessment
- Multiple optimization levels (quick, proper, comprehensive)
- SQL code with expected improvements

### Algorithm Optimization
- Time and space complexity analysis
- O(n²) nested loop detection
- Data structure efficiency evaluation
- Inefficient pattern recognition
- Multi-language support (C#, SQL, JavaScript, Python, Java, etc.)
- Code examples with before/after comparisons
- Scalability impact assessment

### Comprehensive Reports
- Detailed analysis with severity levels
- Implementation guidance with SQL/code examples
- Expected performance improvements
- Risk assessment for each recommendation
- Testing and monitoring guidance

## Installation

Already installed in: `marketplace/plugins/optimization-engine/`

## Quick Start

### Optimize a Database Query

```bash
# Quick analysis (synchronous)
/optimize-query sp_GetUsers --wait

# Background analysis (asynchronous)
/optimize-query sp_GetUsers --async

# Summary only
/optimize-query sp_GetActiveOrders --report=summary
```

### Optimize an Algorithm

```bash
# Analyze code file (synchronous)
/optimize-algorithm src/Services/UserService.cs --wait

# Background analysis
/optimize-algorithm Models/User.cs --async

# Quick summary
/optimize-algorithm Repository/DataAccess.cs --report=summary
```

## Components

### Agents

#### Query Optimizer
- **File**: `agents/query-optimizer.md`
- **Purpose**: Analyzes MSSQL queries, SPs, and views for performance optimization
- **Output**: `marketplace/output/optimization/<query-name>-optimization.md`
- **Task**: Tasks #4, #5 (Database performance, Query optimization)

#### Algorithm Optimizer
- **File**: `agents/algorithm-optimizer.md`
- **Purpose**: Analyzes code algorithms for complexity and performance improvements
- **Output**: `marketplace/output/optimization/<filename>-algorithm-optimization.md`
- **Task**: Task #6 (Algorithm and code performance optimization)

### Commands

#### /optimize-query
- **Usage**: `/optimize-query <query-name> [--async|--wait] [--report=full|summary]`
- **Delegates To**: query-optimizer agent
- **MCP Required**: MSSQL

#### /optimize-algorithm
- **Usage**: `/optimize-algorithm <file-path> [--async|--wait] [--report=full|summary]`
- **Delegates To**: algorithm-optimizer agent
- **MCP Required**: None

### Skills

#### Performance Tuning
- **File**: `skills/performance-tuning.md`
- **Coverage**:
  - Measurement and baseline principles
  - Bottleneck identification methodology
  - Root cause analysis for performance issues
  - Common problems and solutions
  - Database, application, memory, network optimization
  - Performance testing approaches
  - Quick reference optimization patterns
  - Tool recommendations

## Output Structure

```
marketplace/output/optimization/
├── <query-name>-optimization.md              # Full query optimization
├── <query-name>-optimization-summary.md      # Summary
├── <filename>-algorithm-optimization.md      # Full algorithm optimization
├── <filename>-algorithm-optimization-summary.md  # Summary
└── ...
```

## Typical Analysis Time

### Query Optimization
- Simple query: 3-5 minutes
- Medium complexity: 8-15 minutes
- Complex query: 15-30 minutes
- Very complex: 30-45 minutes

### Algorithm Optimization
- Small file (< 100 lines): 2-4 minutes
- Medium file (100-500 lines): 5-10 minutes
- Large file (500-2000 lines): 10-20 minutes
- Very large file (> 2000 lines): 20-30 minutes

**Recommendation**: Use `--async` for complex queries/files.

## Common Optimizations Addressed

### Database
- Missing indexes
- Full table scans
- N+1 query patterns
- Inefficient JOINs
- Non-sargable predicates
- Correlated subqueries
- Index fragmentation

### Application
- O(n²) nested loops
- Inefficient data structures
- Repeated calculations
- String concatenation loops
- Linear searches (vs binary search)
- List.Contains() inefficiency
- Unnecessary iterations

## MCP Requirements

### MSSQL (Required for Query Optimization)
```json
{
  "mssql": {
    "command": "node",
    "args": ["@modelcontextprotocol/server-mssql/dist/index.js"],
    "env": {
      "MSSQL_CONNECTION_STRING": "Server=localhost;Database=mydb;..."
    }
  }
}
```

## Usage Examples

### Pre-Optimization Baseline
```bash
# Establish current performance
/optimize-query sp_GetUsers --wait
# Review current execution time
# Note as baseline for comparison
```

### Identify High-Impact Issues
```bash
# Get quick summary
/optimize-query sp_LargeReport --report=summary
# See primary bottleneck
# Prioritize high-impact fixes
```

### Algorithm Performance Check
```bash
# Analyze proposed algorithm
/optimize-algorithm src/Algorithms/NewSort.cs --wait
# Review complexity analysis
# Choose implementation approach
```

### Batch Optimization
```bash
# Queue multiple queries
/optimize-query sp_Query1 --async
/optimize-query sp_Query2 --async
/optimize-query sp_Query3 --async
# Check progress: /task-status <task-id>
```

## FAQ

**Q: What databases do you support?**
A: Currently MSSQL (SQL Server). Other databases may be added.

**Q: Can I optimize views?**
A: Yes, both stored procedures and views.

**Q: Will optimization change results?**
A: No, optimizations produce identical results, just faster.

**Q: How confident are recommendations?**
A: Very high, based on execution plans and algorithm analysis.

**Q: What if I disagree?**
A: Recommendations are guidance. You decide implementation.

**Q: Can I get estimates of improvement?**
A: Yes, reports include expected improvement percentages.

**Q: Where are reports saved?**
A: `marketplace/output/optimization/`

**Q: Can I share reports?**
A: Yes, they're markdown files suitable for sharing.

## Optimization Approaches

Each report provides multiple approaches:

**Quick Fix** (Minimal effort, moderate improvement)
- Example: Add missing index (5 minutes, 40-60% improvement)

**Proper Fix** (Moderate effort, good improvement)
- Example: Multiple indexes + restructure (25 minutes, 60-80% improvement)

**Comprehensive** (Major effort, maximum improvement)
- Example: Full redesign + caching (2+ hours, 80-95% improvement)

Choose based on your needs and constraints.

## Integration with Other Plugins

- **Analysis Toolkit**: Use stack trace analysis on optimization-revealed errors
- **Review Suite**: Use PR review to catch performance issues
- **Architecture Advisor**: Get architectural guidance on major optimizations

## Related Commands

- `/task-status <task-id>` - Check optimization progress
- `/review-pr` - Review code for performance issues
- `/validate-solution` - Validate optimized code
- `/analyze-impact` - Analyze impact of optimizations

## Troubleshooting

### MSSQL MCP Not Available
```
Solution: Configure MSSQL MCP in .mcp.json
Verify: Connection string and credentials
Check: Database is accessible
```

### Query Not Found
```
Solution: Verify query name is correct (case-sensitive)
Check: Query exists in current database
Try: List available queries in database
```

### Timeout
```
Solution: Use --async flag for large files
Tip: Break complex queries into parts
Note: Very large files may take longer
```

## Best Practices

1. **Measure Baseline**: Know current performance before optimizing
2. **Prioritize Impact**: Focus on high-impact optimizations first
3. **Test Changes**: Verify optimizations work correctly
4. **Monitor Results**: Confirm improvements in production
5. **Document Why**: Explain optimization decisions
6. **Share Knowledge**: Help team learn optimization patterns

## Performance Tuning Principles

- **Measure First**: Don't guess bottlenecks, profile them
- **Target High-Impact**: 80% of time in 20% of code
- **Consider Trade-offs**: Speed vs. complexity vs. maintainability
- **Solve at Right Level**: Database, application, or system?
- **Test Thoroughly**: Verify no regressions

## Plugin Status

- **Version**: 2.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-01-15
- **Tasks Covered**: Task #4, #5, #6
- **MCP Servers**: MSSQL (optional, for query optimization)
- **Shared Skills**: 4 (performance-analysis-framework, sql-optimization-patterns, query-performance-tuning, linq-to-sql-patterns)

## What's New in v2.0.0

- **Shared Skills Integration**: Now uses centralized skill library for better consistency
- **Enhanced Agent Specifications**: All agents follow latest template standards
- **Improved Error Handling**: Better fallback strategies when MCP unavailable
- **Sequential Thinking**: Enhanced support for complex optimization analysis
- **Better Documentation**: Detailed process phases and success criteria
- **LINQ-to-SQL Support**: Added LINQ query optimization patterns

## Support

For issues or suggestions:
1. Review this README
2. Check FAQ section
3. Review command documentation
4. Consult shared skills documentation in `../../shared-skills/`

---

**Part of the Claude Code Marketplace**
Optimization Engine Plugin v2.0.0 (2026-01-15)
