# Changelog

All notable changes to the LINQ-to-SQL Expert plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-15

### Added
- Initial release of LINQ-to-SQL Expert plugin
- **linq-query-analyzer** agent for detecting LINQ performance issues and anti-patterns
  - N+1 query detection
  - Missing DataLoadOptions identification
  - Inefficient projection analysis
  - Cartesian product detection
  - Lazy loading issue identification
- **linq-to-sql-converter** agent for migrating LINQ to SQL stored procedures
  - LINQ query parsing and analysis
  - SQL stored procedure generation
  - Parameter mapping with type conversion
  - Test plan creation
  - MCP integration for SQL Server validation
- **linq-bug-fixer** agent for fixing common LINQ-to-SQL bugs
  - Null reference exception fixes
  - Lazy loading issue resolution
  - DataContext lifetime management
  - Change tracking problems
  - Deferred execution issues
- **linq-optimizer** agent for query performance optimization
  - DataLoadOptions implementation
  - Projection optimization
  - Compiled query generation
  - Batch operation optimization
  - Query result caching strategies

### Commands
- `/analyze-linq` - Analyze LINQ queries for performance issues and anti-patterns
- `/convert-linq-to-sql` - Convert LINQ queries to SQL stored procedures with parameter mapping
- `/fix-linq-bug` - Identify and fix common LINQ-to-SQL bugs
- `/optimize-linq` - Optimize LINQ query performance with best practices

### Skills Referenced
- `linq-to-sql-patterns` - LINQ-to-SQL best practices and anti-patterns
- `sql-optimization-patterns` - SQL Server optimization strategies
- `query-performance-tuning` - Query performance analysis using execution plans

### Features
- Support for .NET Framework 4.8 LINQ-to-SQL
- Integration with MSSQL MCP server for stored procedure testing
- Comprehensive error handling and fallback strategies
- Detailed analysis reports with actionable recommendations
- Code examples with before/after comparisons
- Performance metrics and benchmarking guidance

### Documentation
- Complete README with use cases and examples
- Agent specifications following v2.0.0 template standards
- Command specifications with detailed usage examples
- Skills integration for methodology guidance

### Compatibility
- Claude Code 1.0+
- .NET Framework 4.8
- SQL Server 2014+
- LINQ-to-SQL ORM

### Notes
- All agents support both full and summary report formats
- MCP server (mssql) required only for `linq-to-sql-converter` agent
- Output reports saved to `marketplace/output/linq-analysis/` directory
- Sequential thinking enabled for complex analysis scenarios
