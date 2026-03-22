# Changelog

All notable changes to the Database Schema Analyzer plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-16

### Added

#### Core Features
- **Schema Structure Analyzer**: Comprehensive SQL Server schema analysis including tables, columns, indexes, constraints, triggers, and stored procedures
- **Schema Migration Planner**: Automated migration planning between database versions with script generation and rollback plans
- **Normalization Advisor**: Database normalization analysis (1NF-5NF) with refactoring recommendations
- **Foreign Key Analyzer**: Relationship mapping, missing FK detection, and referential integrity validation

#### Commands
- `/analyze-schema` - Analyze database schema structure with customizable report formats
- `/plan-schema-migration` - Plan schema migrations between source and target databases
- `/suggest-normalization` - Analyze table normalization and suggest improvements
- `/analyze-relationships` - Map relationships and validate foreign key constraints

#### Agents
- `schema-structure-analyzer` - Full schema analysis with design pattern detection
- `schema-migration-planner` - Migration planning with breaking change detection
- `normalization-advisor` - Normalization form analysis with improvement suggestions
- `foreign-key-analyzer` - Relationship analysis with orphan detection

#### Shared Skills
- `database-schema-analysis` - Schema analysis methodology
- `sql-optimization-patterns` - SQL Server optimization patterns
- `query-performance-tuning` - Performance tuning techniques

#### Documentation
- Comprehensive README with installation, usage, and troubleshooting
- Detailed agent specifications with 6-phase processes
- Command specifications with examples and use cases
- MCP integration guide for SQL Server connectivity

#### Features by Command

**analyze-schema**:
- Table and column structure analysis
- Data type validation and recommendations
- Index analysis with optimization suggestions
- Constraint validation (PK, FK, CHECK, UNIQUE, DEFAULT)
- Trigger and stored procedure analysis
- View dependency mapping
- Design pattern and anti-pattern detection
- Customizable output formats (markdown, JSON)

**plan-schema-migration**:
- Source-to-target schema comparison
- Breaking change detection with severity levels
- Data migration strategy generation
- Backward compatibility analysis
- Automated T-SQL migration script generation
- Rollback plan creation with safety checks
- Testing checklist generation

**suggest-normalization**:
- Current normalization form detection (1NF-5NF)
- Redundant data identification
- Update anomaly detection
- Transitive dependency analysis
- Denormalization trade-off evaluation
- Refactoring step generation with SQL scripts
- Performance impact analysis

**analyze-relationships**:
- Foreign key constraint validation
- Missing foreign key detection
- Orphaned record identification
- Cascade rule analysis (UPDATE/DELETE)
- Relationship pattern detection
- ERD generation (text, visual formats)
- Circular dependency detection

#### Configuration
- Configurable output directory: `output/schema-analysis`
- Default report format: markdown (JSON available)
- Maximum table traversal depth: 3 levels
- System object exclusion by default
- Timeout configuration: 300 seconds

#### MCP Integration
- MSSQL MCP server integration for schema introspection
- System catalog querying (sys.tables, sys.columns, sys.indexes, etc.)
- Metadata extraction for comprehensive analysis
- Connection validation and error handling

#### Output Reports
- Executive summary with key findings
- Detailed analysis with metrics and statistics
- Visual diagrams (ERD, dependency graphs)
- Prioritized recommendations with action items
- Implementation SQL scripts
- Testing and validation checklists
- Rollback procedures

### Technical Details

#### Supported SQL Server Versions
- SQL Server 2016
- SQL Server 2017
- SQL Server 2019
- SQL Server 2022

#### Compatibility
- Claude Code: >=1.0.0
- Plugin Specification: v2.0.0
- MCP Protocol: v1.0.0

#### Performance
- Typical analysis time: 5-10 minutes (medium databases)
- Migration planning time: 10-20 minutes (complex migrations)
- Timeout handling with partial results
- Incremental analysis for large schemas

### Dependencies
- **Required**: MSSQL MCP server (@modelcontextprotocol/server-mssql)
- **Tools**: Bash, Read, Write, Grep, Glob
- **SQL Server Permissions**: VIEW DEFINITION, db_datareader

### Known Limitations
- Requires MCP server for all commands (no offline mode)
- Large database analysis may timeout (configurable)
- System object analysis disabled by default
- ERD visual generation requires external tools

### Migration Notes
- First release - no migration needed
- Follow MCP configuration guide for setup
- Ensure SQL Server permissions are granted
- Test with non-production databases first

### Security Considerations
- Uses read-only database queries
- No schema modifications without explicit scripts
- Credentials managed by MCP server
- Output reports stored locally

### Future Enhancements (Planned)
- Support for Azure SQL Database
- PostgreSQL and MySQL adapters
- Real-time schema monitoring
- Schema versioning and diff tracking
- Automated index recommendation implementation
- Integration with version control systems
- Schema documentation generation
- Performance baseline tracking

---

## Release Notes

### v2.0.0 - Initial Release

This is the initial production release of the Database Schema Analyzer plugin. It provides comprehensive database schema analysis, migration planning, normalization analysis, and relationship mapping capabilities for SQL Server databases.

**Key Highlights**:
- 4 specialized agents for different analysis types
- 4 user-facing commands with rich flag support
- 3 shared skills for methodology and best practices
- Full MCP integration for SQL Server connectivity
- Comprehensive documentation and examples
- Production-ready with error handling and validation

**Getting Started**:
1. Configure MSSQL MCP server (see README)
2. Verify connectivity to SQL Server
3. Run `/analyze-schema MyDatabase` to test
4. Review output in `output/schema-analysis/`

**Recommended First Steps**:
1. Analyze existing database structure
2. Review normalization recommendations
3. Validate foreign key relationships
4. Plan any needed schema migrations

---

**Plugin Version**: 2.0.0
**Release Date**: 2026-01-16
**Status**: Production Ready
**Maintainer**: Claude Code Marketplace Team
