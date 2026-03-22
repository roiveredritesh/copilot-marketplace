---
command_name: analyze-schema
version: 2.0.0
description: Analyze SQL Server database schema structure including tables, indexes, constraints, and stored procedures
delegated_to: schema-structure-analyzer
requires_mcp: true
async_capable: true
---

# /analyze-schema Command

## Overview

The `/analyze-schema` command provides comprehensive analysis of SQL Server database schema structure. It examines tables, columns, data types, indexes, constraints, triggers, stored procedures, and views to provide detailed insights into database design. The command identifies design patterns, anti-patterns, and provides actionable recommendations for schema optimization.

## Syntax

```bash
/analyze-schema <database-name> [--report=full|summary] [--include=components] [--format=markdown|json]
```

## Parameters

### Required

- **database-name** (string): Name of the SQL Server database to analyze
  - Must be accessible via configured MSSQL MCP server
  - Example: `MyDatabase`, `ProductionDB`, `AnalyticsDB`

### Optional Flags

#### --report

Controls the level of detail in the analysis report.

**Values**:
- `full` (default): Comprehensive analysis with all details, recommendations, and SQL scripts
- `summary`: High-level overview with critical issues and top recommendations only

**Examples**:
```bash
/analyze-schema MyDatabase --report=full
/analyze-schema MyDatabase --report=summary
```

#### --include

Specifies which database components to include in the analysis.

**Values** (comma-separated list):
- `tables`: Table structures and columns
- `views`: View definitions and dependencies
- `procs`: Stored procedures
- `triggers`: Triggers
- `indexes`: Index analysis
- `constraints`: Constraint validation
- `all` (default): Include all components

**Examples**:
```bash
/analyze-schema MyDatabase --include=tables,indexes
/analyze-schema MyDatabase --include=all
```

#### --format

Specifies the output format for the analysis report.

**Values**:
- `markdown` (default): Human-readable Markdown report
- `json`: Machine-parseable JSON format for automation/CI/CD

**Examples**:
```bash
/analyze-schema MyDatabase --format=markdown
/analyze-schema MyDatabase --format=json
```

## Usage Examples

### Example 1: Full Analysis (Default)

```bash
/analyze-schema ProductionDB
```

Performs comprehensive analysis of all components in ProductionDB database and generates a detailed Markdown report.

**Output**: `marketplace/marketplace/output/schema-analysis/schema-structure-ProductionDB-{timestamp}.md`

---

### Example 2: Summary Report for Quick Review

```bash
/analyze-schema TestDB --report=summary
```

Generates a high-level summary report with critical issues and top 10 recommendations only. Useful for quick health checks.

**Output**: `marketplace/marketplace/output/schema-analysis/schema-structure-TestDB-{timestamp}.md` (abbreviated)

---

### Example 3: Analyze Specific Components

```bash
/analyze-schema MyDatabase --include=tables,indexes,constraints
```

Focuses analysis on tables, indexes, and constraints only. Excludes stored procedures, triggers, and views. Useful for performance-focused analysis.

---

### Example 4: JSON Output for Automation

```bash
/analyze-schema AnalyticsDB --format=json
```

Generates JSON-formatted output suitable for CI/CD pipelines, automated quality gates, or custom tooling.

**Output**: `marketplace/marketplace/output/schema-analysis/schema-structure-AnalyticsDB-{timestamp}.json`

**Sample JSON Structure**:
```json
{
  "database": "AnalyticsDB",
  "analysis_date": "2026-01-16T14:30:00Z",
  "summary": {
    "total_tables": 45,
    "health_score": 88,
    "critical_issues": 0,
    "high_priority_issues": 2
  },
  "tables": [...],
  "recommendations": [...]
}
```

---

### Example 5: Component-Specific Analysis

```bash
/analyze-schema LegacyDB --include=procs,triggers --report=full
```

Deep dive into stored procedures and triggers only. Useful when investigating logic embedded in database objects.

---

## What Gets Analyzed

### Tables
- Table structure (columns, data types, nullability)
- Naming conventions
- Table sizes and row counts
- Wide tables (>50 columns)
- Heap tables (no clustered index)
- Tables without primary keys

### Columns
- Data type appropriateness
- Deprecated data types (text, ntext, image)
- Oversized data types
- Nullable column patterns
- Identity columns
- Computed columns

### Indexes
- Clustered index strategy
- Missing indexes (high-impact recommendations)
- Unused indexes
- Duplicate/overlapping indexes
- Index fragmentation
- Covering indexes
- Filtered indexes

### Constraints
- Primary key coverage
- Foreign key relationships
- Unique constraints
- Check constraints
- Default constraints
- Disabled constraints

### Stored Procedures (if included)
- Naming conventions
- Parameter usage and SQL injection risk
- SET options
- Error handling (TRY/CATCH)
- Dynamic SQL usage
- Deprecated T-SQL syntax

### Triggers (if included)
- Trigger count per table
- Recursive trigger risk
- Complex business logic in triggers
- Performance impact on large tables

### Views (if included)
- View definitions
- Indexed views
- View dependencies

## Design Patterns Detected

- **Audit Trail Pattern**: CreatedDate, CreatedBy, ModifiedDate, ModifiedBy
- **Soft Delete Pattern**: IsDeleted, DeletedDate, DeletedBy
- **Type-Subtype Pattern**: TypeID FK to lookup tables
- **Hierarchy Pattern**: Self-referential FKs (ParentID)
- **Many-to-Many Pattern**: Junction tables
- **Version Control Pattern**: VersionNumber, IsCurrent, EffectiveDate

## Anti-Patterns Detected

- **God Table**: Tables with >50 columns
- **EAV (Entity-Attribute-Value)**: Generic attribute tables
- **Polymorphic Association**: Generic FKs with type discriminator
- **Fear of NULL**: Using empty strings or 0 instead of NULL
- **Multicolumn Attributes**: Tag1, Tag2, Tag3 columns
- **Metadata Tribbles**: Table_2024, Table_2025 pattern
- **CHAR(1) for Boolean**: Using CHAR instead of BIT

## Output Report Structure

### Executive Summary
- Database properties (size, compatibility level)
- Object counts (tables, indexes, constraints)
- Overall health score (0-100)
- Critical issues requiring immediate attention
- Quick wins (easy high-impact fixes)
- Estimated effort for recommendations

### Detailed Analysis
- Component-by-component breakdown
- Issues categorized by severity
- Metrics and statistics
- Visual diagrams where applicable

### Recommendations
- Prioritized by severity (Critical > High > Medium > Low)
- Each recommendation includes:
  - Issue description
  - Impact explanation
  - Step-by-step solution
  - Executable SQL script
  - Testing procedure
  - Rollback steps

### Appendices
- Complete table listing with metrics
- Index fragmentation report
- Missing index recommendations
- Unused index listing

## Prerequisites

### MCP Configuration

The MSSQL MCP server must be configured in Claude Code:

```json
{
  "mcpServers": {
    "mssql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mssql"],
      "env": {
        "MSSQL_CONNECTION_STRING": "Server=localhost;Database=master;Trusted_Connection=True;"
      }
    }
  }
}
```

### Required Permissions

The database user must have:
- `VIEW DEFINITION` permission on the database
- `SELECT` permission on system catalogs (sys.tables, sys.columns, etc.)

**Grant permissions**:
```sql
USE [DatabaseName];
GRANT VIEW DEFINITION TO [UserName];
```

## Error Handling

### Common Errors and Solutions

#### Error: "Cannot connect to MSSQL server"
**Cause**: MCP server not running or misconfigured

**Solution**:
1. Check MCP server status in Claude Code settings
2. Verify connection string in MCP configuration
3. Test SQL Server connectivity independently
4. Restart Claude Code after configuration changes

---

#### Error: "Database 'XYZ' not found"
**Cause**: Database name incorrect or not accessible

**Solution**:
1. Verify database name spelling
2. Check if database is online: `SELECT name, state_desc FROM sys.databases`
3. Ensure user has access to database
4. Use three-part naming if needed: `Server.Database.Schema.Table`

---

#### Error: "Permission denied - VIEW DEFINITION required"
**Cause**: Insufficient database permissions

**Solution**:
Grant required permissions:
```sql
USE [DatabaseName];
GRANT VIEW DEFINITION TO [UserName];
GRANT SELECT ON SCHEMA::sys TO [UserName];
```

---

#### Error: "Analysis timeout on large database"
**Cause**: Database too large (>500 tables) for full analysis within timeout

**Solution**:
1. Use `--include` flag to analyze specific components
2. Use `--report=summary` for faster execution
3. Run during low-usage period
4. Increase timeout in plugin configuration

---

## Performance Considerations

### Typical Execution Times

- **Small Database** (<50 tables): 2-3 minutes
- **Medium Database** (50-200 tables): 5-10 minutes
- **Large Database** (200-500 tables): 10-20 minutes
- **Very Large Database** (>500 tables): 20-30 minutes or timeout

### Optimization Tips

1. **Use --include flag** for targeted analysis
2. **Use --report=summary** for quick checks
3. **Run during low-load periods** to minimize system catalog contention
4. **Analyze critical tables individually** if full database analysis times out

## Integration with Other Commands

### Workflow: Database Health Check

```bash
# Step 1: Analyze overall schema structure
/analyze-schema MyDatabase --report=summary

# Step 2: Analyze normalization for specific tables
/suggest-normalization MyDatabase.Users
/suggest-normalization MyDatabase.Orders

# Step 3: Validate relationships and foreign keys
/analyze-relationships MyDatabase
```

### Workflow: Pre-Migration Assessment

```bash
# Step 1: Analyze source database
/analyze-schema SourceDB --format=json > source_analysis.json

# Step 2: Analyze target database
/analyze-schema TargetDB --format=json > target_analysis.json

# Step 3: Plan migration
/plan-schema-migration SourceDB TargetDB --generate-scripts
```

## Tips and Best Practices

1. **Run Regular Health Checks**: Execute monthly to track schema evolution
2. **Track Health Score**: Monitor improvements over time
3. **Fix Critical Issues First**: Prioritize based on severity
4. **Test in Development**: Always test recommendations in non-production first
5. **Document Changes**: Keep analysis reports for audit trail
6. **Use JSON for Automation**: Integrate into CI/CD for quality gates
7. **Component-Specific Analysis**: Use --include for focused reviews

## Related Commands

- **`/suggest-normalization`**: Detailed normalization analysis for specific tables
- **`/analyze-relationships`**: Foreign key and relationship analysis
- **`/plan-schema-migration`**: Migration planning between database versions

## Output Location

All reports are saved to:
```
marketplace/output/schema-analysis/schema-structure-{database}-{timestamp}.{ext}
```

Examples:
- `marketplace/marketplace/output/schema-analysis/schema-structure-MyDatabase-20260116-143022.md`
- `marketplace/marketplace/output/schema-analysis/schema-structure-TestDB-20260116-150530.json`

## Version History

- **2.0.0** (2026-01-16): Initial release
  - Full schema structure analysis
  - Design pattern and anti-pattern detection
  - Multiple output formats (Markdown, JSON)
  - Configurable component inclusion
  - Summary and detailed report modes

## Support

For issues or questions:
1. Check [README.md](../README.md) for troubleshooting guide
2. Review agent specification: [schema-structure-analyzer.md](../agents/schema-structure-analyzer.md)
3. Verify MCP configuration and permissions
4. Check Claude Code logs for detailed error messages

---

**Command Type**: Analysis
**Delegation**: This command delegates to the `schema-structure-analyzer` agent
**MCP Required**: Yes (MSSQL)
**Async Capable**: Yes
**Estimated Duration**: 5-10 minutes (medium databases)
