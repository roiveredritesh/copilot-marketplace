# LINQ-to-SQL Expert Plugin

**Version**: 2.0.0
**Status**: Production Ready
**Compatibility**: Claude Code 1.0+

## Overview

The LINQ-to-SQL Expert plugin provides comprehensive LINQ-to-SQL optimization, bug fixing, and SQL stored procedure migration capabilities for .NET Framework 4.8 applications. This plugin helps developers analyze LINQ queries for performance issues, convert complex LINQ queries to optimized SQL stored procedures, fix common LINQ-to-SQL bugs, and apply performance optimization techniques.

## Features

### 1. LINQ Query Analysis
- **N+1 Query Detection** - Identifies expensive lazy loading patterns that generate multiple queries
- **DataLoadOptions Missing** - Detects missing eager loading configurations
- **Inefficient Projections** - Finds queries that select entire entities when only specific fields are needed
- **Cartesian Product Detection** - Identifies accidental cross joins causing performance issues
- **Anti-Pattern Identification** - Detects common LINQ-to-SQL anti-patterns

### 2. LINQ to SQL Conversion
- **LINQ Query Parsing** - Analyzes complex LINQ query structure and intent
- **SQL Stored Procedure Generation** - Creates optimized T-SQL stored procedures
- **Parameter Mapping** - Generates accurate parameter mapping with type conversion
- **Test Plan Creation** - Provides comprehensive testing strategy
- **MCP Integration** - Validates generated SQL against actual SQL Server instance

### 3. LINQ Bug Fixing
- **Null Reference Exception Fixes** - Resolves null reference issues in LINQ queries
- **Lazy Loading Issues** - Fixes lazy loading problems and N+1 queries
- **DataContext Lifetime Management** - Corrects DataContext disposal and scope issues
- **Change Tracking Problems** - Resolves entity state tracking issues
- **Deferred Execution Issues** - Fixes problems with deferred query execution

### 4. LINQ Performance Optimization
- **DataLoadOptions Implementation** - Adds proper eager loading configuration
- **Projection Optimization** - Converts entity queries to efficient projections
- **Compiled Query Generation** - Creates compiled queries for repeated executions
- **Batch Operation Optimization** - Optimizes bulk insert/update/delete operations
- **Query Result Caching** - Implements caching strategies for expensive queries

## Quick Start

### Analyze LINQ Query for Issues

```bash
/analyze-linq src/DataAccess/UserRepository.cs --report=full
```

**Output**: Comprehensive analysis report identifying N+1 queries, missing DataLoadOptions, inefficient projections, and recommended fixes.

**Use Case**: Before deploying to production, analyze all LINQ queries in your repository classes for potential performance issues.

---

### Convert LINQ Query to SQL Stored Procedure

```bash
/convert-linq-to-sql src/DataAccess/OrderRepository.cs GetOrdersWithDetails --report=full
```

**Output**:
- Generated SQL stored procedure with optimized T-SQL
- Parameter mapping with type conversion
- C# method to call the stored procedure
- Test plan with sample data

**Use Case**: Migrate critical LINQ queries to stored procedures for better performance and query plan control.

---

### Fix LINQ-to-SQL Bug

```bash
/fix-linq-bug src/Services/ProductService.cs --report=full
```

**Output**:
- Identified bugs (null references, lazy loading issues, DataContext problems)
- Fixed code with detailed explanations
- Before/after comparison
- Testing recommendations

**Use Case**: Resolve production bugs related to LINQ-to-SQL, such as "Object reference not set to an instance of an object" or N+1 query performance issues.

---

### Optimize LINQ Query Performance

```bash
/optimize-linq src/DataAccess/CustomerRepository.cs --report=full
```

**Output**:
- Performance analysis with metrics
- Optimized LINQ code with DataLoadOptions, projections, and compiled queries
- Before/after execution plan comparison
- Benchmarking guidance

**Use Case**: Optimize slow LINQ queries causing page load delays or timeouts.

## Commands Reference

### `/analyze-linq <file-path> [--report=full|summary]`

Analyzes LINQ queries in the specified file for performance issues and anti-patterns.

**Parameters**:
- `<file-path>` - Path to the C# file containing LINQ queries

**Flags**:
- `--report=full` (default) - Generate comprehensive analysis report
- `--report=summary` - Generate concise summary report

**Delegated to**: `linq-query-analyzer` agent

**Output**: `marketplace/output/linq-analysis/linq-analysis-{filename}-{timestamp}.md`

---

### `/convert-linq-to-sql <file-path> <query-name> [--report=full|summary]`

Converts a LINQ query to an optimized SQL stored procedure with parameter mapping.

**Parameters**:
- `<file-path>` - Path to the C# file containing the LINQ query
- `<query-name>` - Name of the method or query to convert

**Flags**:
- `--report=full` (default) - Generate comprehensive conversion report with test plan
- `--report=summary` - Generate concise conversion report

**Delegated to**: `linq-to-sql-converter` agent

**Output**: `marketplace/output/linq-analysis/linq-to-sql-conversion-{query-name}-{timestamp}.md`

**MCP Required**: `mssql` (optional, for validation)

---

### `/fix-linq-bug <file-path> [--report=full|summary]`

Identifies and fixes common LINQ-to-SQL bugs in the specified file.

**Parameters**:
- `<file-path>` - Path to the C# file with LINQ-to-SQL code

**Flags**:
- `--report=full` (default) - Generate comprehensive bug fix report
- `--report=summary` - Generate concise bug fix summary

**Delegated to**: `linq-bug-fixer` agent

**Output**: `marketplace/output/linq-analysis/linq-bug-fix-{filename}-{timestamp}.md`

---

### `/optimize-linq <file-path> [--report=full|summary]`

Optimizes LINQ query performance with DataLoadOptions, projections, and compiled queries.

**Parameters**:
- `<file-path>` - Path to the C# file containing LINQ queries

**Flags**:
- `--report=full` (default) - Generate comprehensive optimization report
- `--report=summary` - Generate concise optimization summary

**Delegated to**: `linq-optimizer` agent

**Output**: `marketplace/output/linq-analysis/linq-optimization-{filename}-{timestamp}.md`

## Use Cases

### Scenario 1: Production Performance Issue
**Problem**: Customers report slow page load times on the Orders page.

**Solution**:
1. `/analyze-linq src/DataAccess/OrderRepository.cs` - Identify N+1 queries
2. `/optimize-linq src/DataAccess/OrderRepository.cs` - Apply DataLoadOptions and projections
3. Test the optimized code in staging environment
4. Monitor performance metrics post-deployment

---

### Scenario 2: Migrate to Stored Procedures
**Problem**: Need to migrate critical LINQ queries to stored procedures for better performance control.

**Solution**:
1. `/analyze-linq src/DataAccess/ReportRepository.cs` - Understand current query structure
2. `/convert-linq-to-sql src/DataAccess/ReportRepository.cs GetMonthlyReport` - Generate stored procedure
3. Review and test the generated stored procedure
4. Deploy to SQL Server and update C# code

---

### Scenario 3: Null Reference Exception
**Problem**: Production error: "Object reference not set to an instance of an object" in LINQ query.

**Solution**:
1. `/fix-linq-bug src/Services/CustomerService.cs` - Identify null reference issues
2. Review the fixed code with null checks and safe navigation
3. Test edge cases with null data
4. Deploy the fix

---

### Scenario 4: Code Review Before Merge
**Problem**: Pull request contains new LINQ queries; need to ensure they follow best practices.

**Solution**:
1. `/analyze-linq src/DataAccess/NewFeatureRepository.cs` - Check for anti-patterns
2. `/optimize-linq src/DataAccess/NewFeatureRepository.cs` - Apply optimizations if needed
3. Review the report and provide feedback to the developer
4. Approve the pull request after fixes

## Skills Referenced

This plugin leverages the following shared skills for methodology and best practices:

1. **linq-to-sql-patterns** (`../../shared-skills/linq-to-sql-patterns.md`)
   - LINQ-to-SQL best practices
   - Common anti-patterns and how to avoid them
   - Performance optimization techniques
   - Entity relationship handling

2. **sql-optimization-patterns** (`../../shared-skills/sql-optimization-patterns.md`)
   - SQL Server optimization strategies
   - Index usage and design
   - Query plan analysis
   - T-SQL best practices

3. **query-performance-tuning** (`../../shared-skills/query-performance-tuning.md`)
   - Execution plan analysis
   - Index recommendations
   - Statistics management
   - Performance benchmarking

## Plugin Status

- **Version**: 2.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-01-15
- **Compatibility**: Claude Code 1.0+, .NET Framework 4.8, SQL Server 2014+

## Architecture

### Agents

1. **linq-query-analyzer** - Analyzes LINQ queries for performance issues
   - Tools: Bash, Glob, Grep, Read, Write
   - MCP Required: None
   - Sequential Thinking: Conditional

2. **linq-to-sql-converter** - Converts LINQ to SQL stored procedures
   - Tools: Bash, Glob, Grep, Read, Write, Edit
   - MCP Required: mssql (optional)
   - Sequential Thinking: Conditional

3. **linq-bug-fixer** - Fixes common LINQ-to-SQL bugs
   - Tools: Bash, Glob, Grep, Read, Write, Edit
   - MCP Required: None
   - Sequential Thinking: Conditional

4. **linq-optimizer** - Optimizes LINQ query performance
   - Tools: Bash, Glob, Grep, Read, Write, Edit
   - MCP Required: None
   - Sequential Thinking: Conditional

### Output Directory

All reports are saved to: `marketplace/output/linq-analysis/`

**File naming convention**:
- `linq-analysis-{filename}-{timestamp}.md`
- `linq-to-sql-conversion-{query-name}-{timestamp}.md`
- `linq-bug-fix-{filename}-{timestamp}.md`
- `linq-optimization-{filename}-{timestamp}.md`

## Configuration

### MCP Server Setup (Optional)

For the `/convert-linq-to-sql` command to validate generated SQL stored procedures, configure the MSSQL MCP server:

1. See `docs/MCP_CONFIGURATION_GUIDE.md` in the marketplace root
2. Configure the `mssql` MCP server with your SQL Server connection details
3. The agent will automatically use MCP if available, or skip validation if not configured

### Report Format

Configure default report format in `.claude/settings.local.json`:

```json
{
  "linq-to-sql-expert": {
    "default_report_format": "full"
  }
}
```

## Troubleshooting

### Issue: "MCP server 'mssql' not available"
**Solution**: This is informational only. The `linq-to-sql-converter` agent will skip SQL validation but still generate the stored procedure code. Configure MCP if you want automatic validation.

### Issue: "Could not find LINQ query in file"
**Solution**: Ensure the file contains LINQ-to-SQL queries (using `DataContext`). The agent searches for LINQ query patterns like `.Where()`, `.Select()`, `.Join()`, etc.

### Issue: "Query name not found"
**Solution**: For `/convert-linq-to-sql`, ensure the query name matches a method name in the file. Use exact case-sensitive matching.

## Support

For issues, feature requests, or questions:
- Check `docs/TROUBLESHOOTING.md` in the marketplace root
- Review agent specifications in `agents/` directory
- Consult `CHANGELOG.md` for version-specific notes

## License

MIT License - See LICENSE file in marketplace root directory.

## Author

Ritesh

## Version History

- **2.0.0** (2026-01-15) - Initial release with 4 agents and 4 commands
