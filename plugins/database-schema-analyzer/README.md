# Database Schema Analyzer Plugin

**Version**: 2.0.0
**Category**: Database
**MCP Required**: MSSQL Server

## Overview

The Database Schema Analyzer is a comprehensive plugin for SQL Server schema analysis, migration planning, relationship mapping, and normalization analysis. It provides deep insights into database design, helps plan schema evolution, and ensures referential integrity and optimal normalization.

## Features

### Core Capabilities

1. **Schema Structure Analysis**
   - Table and column analysis with data type validation
   - Index analysis and optimization recommendations
   - Constraint validation (PK, FK, CHECK, UNIQUE, DEFAULT)
   - Trigger and stored procedure analysis
   - View dependency mapping
   - Design pattern and anti-pattern detection

2. **Migration Planning**
   - Source-to-target schema comparison
   - Breaking change detection
   - Data migration strategy generation
   - Backward compatibility analysis
   - Automated migration script generation
   - Rollback plan creation

3. **Normalization Analysis**
   - Current normalization form detection (1NF-5NF)
   - Redundant data identification
   - Update anomaly detection
   - Transitive dependency analysis
   - Denormalization trade-off analysis
   - Refactoring recommendations

4. **Relationship Mapping**
   - Foreign key constraint analysis
   - Missing foreign key detection
   - Orphaned record identification
   - Cascade rule validation
   - ERD generation (text/visual)
   - Relationship pattern analysis

## Installation

### Prerequisites

1. **Claude Code**: Version 1.0.0 or higher
2. **MCP Server**: MSSQL Server configured and running
3. **SQL Server Access**: Permissions to query system catalogs and metadata

### MCP Configuration

Add the MSSQL MCP server to your Claude Code configuration:

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

### Plugin Installation

The plugin is automatically discovered when placed in the `plugins/` directory. No manual installation required.

## Commands

### 1. /analyze-schema

Analyze SQL Server database schema structure including tables, indexes, constraints, and stored procedures.

**Usage**:
```bash
/analyze-schema <database-name> [flags]
```

**Flags**:
- `--report=full|summary` - Report detail level (default: full)
- `--include=tables,views,procs,triggers,indexes` - Components to include (default: all)
- `--format=markdown|json` - Output format (default: markdown)

**Examples**:
```bash
# Full schema analysis
/analyze-schema MyDatabase

# Summary report with specific components
/analyze-schema MyDatabase --report=summary --include=tables,indexes

# JSON output for automation
/analyze-schema MyDatabase --format=json
```

**Output**: `marketplace/output/schema-analysis/schema-structure-{database}-{timestamp}.md`

---

### 2. /plan-schema-migration

Plan database schema migration from source to target version with migration scripts and rollback plans.

**Usage**:
```bash
/plan-schema-migration <source-db> <target-db> [flags]
```

**Flags**:
- `--analyze-data` - Include data migration analysis
- `--generate-scripts` - Generate T-SQL migration scripts
- `--check-compatibility` - Perform backward compatibility check

**Examples**:
```bash
# Basic migration plan
/plan-schema-migration MyDB_v1 MyDB_v2

# Full migration with scripts and data analysis
/plan-schema-migration MyDB_v1 MyDB_v2 --analyze-data --generate-scripts

# Compatibility-focused migration
/plan-schema-migration OldDB NewDB --check-compatibility
```

**Output**: `marketplace/output/schema-analysis/migration-plan-{source}-to-{target}-{timestamp}.md`

---

### 3. /suggest-normalization

Analyze table normalization and suggest improvements for better database design.

**Usage**:
```bash
/suggest-normalization <database-name>.<table-name> [flags]
```

**Flags**:
- `--form=1NF|2NF|3NF|BCNF|4NF|5NF` - Target normalization form (default: 3NF)
- `--include-denorm` - Include denormalization recommendations

**Examples**:
```bash
# Basic normalization analysis
/suggest-normalization MyDatabase.Users

# Target specific normalization form
/suggest-normalization MyDatabase.Orders --form=3NF

# Include denormalization trade-offs
/suggest-normalization MyDatabase.Products --include-denorm
```

**Output**: `marketplace/output/schema-analysis/normalization-{table}-{timestamp}.md`

---

### 4. /analyze-relationships

Map and analyze database relationships, foreign keys, and referential integrity.

**Usage**:
```bash
/analyze-relationships <database-name> [flags]
```

**Flags**:
- `--include-orphans` - Check for orphaned records
- `--map-type=erd|text|json` - Relationship map format (default: text)
- `--depth=1|2|3` - Relationship traversal depth (default: 2)

**Examples**:
```bash
# Basic relationship analysis
/analyze-relationships MyDatabase

# Include orphan detection with ERD
/analyze-relationships MyDatabase --include-orphans --map-type=erd

# Deep relationship traversal
/analyze-relationships MyDatabase --depth=3
```

**Output**: `marketplace/output/schema-analysis/relationships-{database}-{timestamp}.md`

## Agents

### 1. schema-structure-analyzer

**Purpose**: Comprehensive analysis of SQL Server database schema structure.

**Capabilities**:
- Table and column structure analysis
- Data type validation and recommendations
- Index analysis with optimization suggestions
- Constraint validation (PK, FK, CHECK, UNIQUE, DEFAULT)
- Trigger and stored procedure analysis
- View dependency mapping
- Design pattern detection

**Process**:
1. Connect to SQL Server via MCP
2. Query system catalog (sys.tables, sys.columns, sys.indexes, etc.)
3. Analyze schema components
4. Detect patterns and anti-patterns
5. Generate recommendations
6. Create comprehensive report

**Output**: Markdown report with schema structure, analysis findings, and recommendations.

---

### 2. schema-migration-planner

**Purpose**: Plan and execute schema migrations between database versions.

**Capabilities**:
- Schema comparison between source and target
- Breaking change detection
- Data migration needs analysis
- Backward compatibility validation
- Migration script generation (T-SQL)
- Rollback plan creation

**Process**:
1. Connect to source and target databases
2. Extract and compare schemas
3. Identify structural changes
4. Analyze data migration requirements
5. Generate migration scripts
6. Create rollback procedures

**Output**: Migration plan with scripts, data strategies, and testing checklists.

---

### 3. normalization-advisor

**Purpose**: Analyze normalization and suggest database design improvements.

**Capabilities**:
- Normalization form detection (1NF-5NF)
- Redundant data identification
- Update anomaly detection
- Transitive dependency analysis
- Denormalization trade-off evaluation
- Refactoring step generation

**Process**:
1. Connect to database via MCP
2. Query table structure and sample data
3. Analyze functional dependencies
4. Determine current normalization form
5. Identify violations and anomalies
6. Generate refactoring recommendations

**Output**: Normalization analysis with improvement steps and SQL refactoring scripts.

---

### 4. foreign-key-analyzer

**Purpose**: Analyze relationships and ensure referential integrity.

**Capabilities**:
- Foreign key constraint validation
- Missing foreign key detection
- Orphaned record identification
- Cascade rule analysis
- Relationship pattern detection
- ERD generation

**Process**:
1. Connect to database via MCP
2. Query foreign key metadata
3. Analyze relationship patterns
4. Check for orphaned records
5. Validate cascade rules
6. Generate relationship map

**Output**: Relationship analysis with integrity issues, missing FKs, and visual ERD.

## Shared Skills

### 1. database-schema-analysis

Comprehensive methodology for analyzing database schema structure, including:
- System catalog querying techniques
- Metadata extraction patterns
- Design pattern recognition
- Anti-pattern detection
- Performance implication analysis

### 2. sql-optimization-patterns

SQL Server optimization patterns including:
- Indexing strategies (clustered, non-clustered, covering, filtered)
- Query optimization techniques
- Execution plan analysis
- Statistics management
- Partitioning strategies

### 3. query-performance-tuning

Advanced performance tuning techniques:
- Execution plan interpretation
- Index usage analysis
- Query rewriting strategies
- Parameterization techniques
- Caching and materialization

## Output Structure

All reports are saved to `marketplace/output/schema-analysis/` with descriptive filenames:

```
output/schema-analysis/
├── schema-structure-MyDatabase-20260116-143022.md
├── migration-plan-v1-to-v2-20260116-150035.md
├── normalization-Users-20260116-160145.md
└── relationships-MyDatabase-20260116-170230.md
```

### Report Format

Each report follows this structure:

1. **Executive Summary**
   - Key findings
   - Critical issues
   - Recommended actions

2. **Detailed Analysis**
   - Component-by-component breakdown
   - Metrics and statistics
   - Visual diagrams (when applicable)

3. **Recommendations**
   - Prioritized action items
   - Implementation steps
   - SQL scripts (when applicable)

4. **Testing Checklist**
   - Validation steps
   - Rollback procedures
   - Success criteria

## Workflows

### Database Design Review Workflow

1. `/analyze-schema MyDatabase` - Analyze current schema
2. `/suggest-normalization MyDatabase.Orders` - Check normalization
3. `/analyze-relationships MyDatabase` - Validate relationships
4. Implement recommended changes
5. Re-run analysis to verify improvements

### Database Migration Workflow

1. `/analyze-schema SourceDB` - Understand source schema
2. `/analyze-schema TargetDB` - Understand target schema
3. `/plan-schema-migration SourceDB TargetDB --generate-scripts` - Create migration plan
4. Review and test migration scripts
5. Execute migration with rollback plan ready
6. `/analyze-schema TargetDB` - Verify migration success

### Performance Optimization Workflow

1. `/analyze-schema MyDatabase --include=tables,indexes` - Analyze current state
2. Identify missing indexes and constraints
3. `/analyze-relationships MyDatabase` - Ensure proper FKs for join optimization
4. Implement index and FK recommendations
5. Validate performance improvements

### New Feature Integration Workflow

1. `/analyze-schema MyDatabase` - Understand existing schema
2. Design new tables/changes
3. `/suggest-normalization MyDatabase.NewTable` - Validate design
4. `/plan-schema-migration Current Proposed` - Plan integration
5. Execute migration scripts
6. `/analyze-relationships MyDatabase` - Verify integrity

## Configuration

The plugin uses these default settings (configurable in plugin.json):

```json
{
  "output_directory": "output/schema-analysis",
  "default_report_format": "markdown",
  "max_table_depth": 3,
  "include_system_objects": false,
  "timeout_seconds": 300
}
```

## Troubleshooting

### MCP Connection Issues

**Problem**: "Cannot connect to MSSQL server"

**Solution**:
1. Verify MCP server is running: Check Claude Code MCP status
2. Validate connection string in MCP configuration
3. Ensure SQL Server is accessible and running
4. Check network/firewall settings

### Permission Errors

**Problem**: "Access denied to system catalogs"

**Solution**:
1. Ensure SQL Server login has VIEW DEFINITION permission
2. Grant db_datareader role for metadata queries
3. For migration planning, ensure access to both databases

### Timeout Issues

**Problem**: "Analysis timeout on large database"

**Solution**:
1. Increase timeout in plugin configuration
2. Use `--include` flag to analyze specific components
3. Use `--report=summary` for faster execution
4. Consider analyzing one table at a time for normalization

### Missing MCP Server

**Problem**: "MSSQL MCP server not configured"

**Solution**:
1. Follow MCP Configuration section above
2. Install @modelcontextprotocol/server-mssql package
3. Restart Claude Code after configuration
4. Verify MCP server shows as "Connected"

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Support

For issues, questions, or feature requests:
1. Check this README and troubleshooting section
2. Review [CHANGELOG.md](CHANGELOG.md) for known issues
3. Consult agent specifications in `agents/` directory
4. Review shared skills in `skills/` directory

## License

MIT License - See repository root for details.

## Contributing

This plugin follows the Claude Code Plugin v2.0.0 specification. When contributing:
1. Follow agent specification template
2. Update plugin.json for new components
3. Add examples to documentation
4. Update CHANGELOG.md
5. Test all commands with sample databases

## Author

Claude Code Marketplace Team

---

**Last Updated**: 2026-01-16
**Plugin Version**: 2.0.0
**Compatibility**: Claude Code >=1.0.0, SQL Server 2016+
