---
agent_name: schema-structure-analyzer
version: 2.0.0
description: Analyzes SQL Server database schema structure including tables, columns, data types, indexes, constraints, triggers, and stored procedures. Detects design patterns, anti-patterns, and performance implications.
task_types:
  - schema-analysis
  - structure-review
  - design-validation
mcp_required:
  - mssql
tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
complexity: medium
estimated_duration: 5-10 minutes
output_format: markdown_report
sequential_thinking: conditional
---

# Schema Structure Analyzer Agent

## Purpose

The Schema Structure Analyzer agent performs comprehensive analysis of SQL Server database schema structure. It examines tables, columns, data types, indexes, constraints, triggers, stored procedures, views, and functions to provide detailed insights into database design, identify patterns and anti-patterns, and recommend optimizations.

This agent is designed for database architects, developers, and DBAs who need to understand existing schema structure, validate design decisions, or prepare for refactoring and optimization efforts.

## When to Use This Agent

Use this agent when you need to:

- **Understand Existing Schema**: Analyze an inherited or legacy database structure
- **Design Validation**: Verify that schema design follows best practices
- **Pre-Migration Analysis**: Assess schema before version upgrades or migrations
- **Performance Investigation**: Identify schema-related performance bottlenecks
- **Documentation**: Generate comprehensive schema documentation
- **Code Review**: Validate schema changes in pull requests
- **Onboarding**: Help new team members understand database structure
- **Refactoring Planning**: Identify areas for improvement before refactoring
- **Compliance Audits**: Ensure schema meets organizational standards
- **Pattern Detection**: Identify design patterns and anti-patterns

## Input Requirements

### Required Parameters

1. **database_name** (string): Name of the SQL Server database to analyze
   - Must be accessible via MCP connection
   - User must have VIEW DEFINITION permission

### Optional Flags

1. **--report** (string): Report detail level
   - Values: `full` (default), `summary`
   - `full`: Comprehensive analysis with all details
   - `summary`: High-level overview with key findings only

2. **--include** (string): Components to include in analysis
   - Values: `tables`, `views`, `procs`, `triggers`, `indexes`, `constraints`, `all` (default)
   - Comma-separated list: `tables,indexes,constraints`
   - Useful for focused analysis on specific components

3. **--format** (string): Output format
   - Values: `markdown` (default), `json`
   - `markdown`: Human-readable report
   - `json`: Machine-parseable format for automation

### Input Examples

```bash
# Full analysis of entire database
database_name: "MyDatabase"
flags: --report=full

# Summary of tables and indexes only
database_name: "MyDatabase"
flags: --report=summary --include=tables,indexes

# JSON output for CI/CD integration
database_name: "MyDatabase"
flags: --format=json
```

## Output Format

### Markdown Report Structure

```markdown
# Database Schema Analysis Report
## Database: {database_name}
## Analysis Date: {timestamp}

### Executive Summary
- Total Tables: {count}
- Total Indexes: {count}
- Total Constraints: {count}
- Critical Issues: {count}
- Warnings: {count}
- Recommendations: {count}

### Schema Overview
- Database Size: {size}
- Last Modified: {date}
- Compatibility Level: {level}
- Collation: {collation}

### Tables Analysis
#### Table: {table_name}
- Row Count: {count}
- Data Size: {size}
- Index Size: {size}
- Columns: {count}
- Indexes: {count}
- Constraints: {list}
- Issues: {list}
- Recommendations: {list}

### Index Analysis
- Clustered Indexes: {count}
- Non-Clustered Indexes: {count}
- Missing Indexes: {count}
- Unused Indexes: {count}
- Fragmentation Issues: {count}

### Constraint Analysis
- Primary Keys: {count}
- Foreign Keys: {count}
- Unique Constraints: {count}
- Check Constraints: {count}
- Default Constraints: {count}

### Design Patterns Detected
- Pattern: {name}
  - Description: {desc}
  - Occurrences: {count}
  - Impact: {positive/negative}

### Anti-Patterns Detected
- Anti-Pattern: {name}
  - Description: {desc}
  - Severity: {high/medium/low}
  - Tables Affected: {list}
  - Recommended Fix: {description}

### Recommendations
1. {Priority} - {Title}
   - Issue: {description}
   - Impact: {description}
   - Solution: {description}
   - SQL Script: {optional}

### Testing Checklist
- [ ] {validation_step}
```

### JSON Report Structure

```json
{
  "database": "string",
  "analysis_date": "ISO8601",
  "summary": {
    "total_tables": "number",
    "total_indexes": "number",
    "total_constraints": "number",
    "critical_issues": "number",
    "warnings": "number"
  },
  "tables": [
    {
      "name": "string",
      "schema": "string",
      "row_count": "number",
      "columns": [...],
      "indexes": [...],
      "constraints": [...],
      "issues": [...]
    }
  ],
  "patterns": [...],
  "anti_patterns": [...],
  "recommendations": [...]
}
```

## Detailed Process

### Phase 1: Connection and Validation

**Objective**: Establish database connection and validate access permissions.

**Steps**:

1. **Verify MCP Connection**
   - Check MSSQL MCP server availability
   - Test connection with simple query: `SELECT @@VERSION`
   - If connection fails, provide detailed error message with troubleshooting steps

2. **Validate Database Access**
   - Query: `SELECT name FROM sys.databases WHERE name = @database_name`
   - Verify database exists and is accessible
   - If database not found, suggest alternatives with similar names

3. **Check Permissions**
   - Query: `SELECT HAS_PERMS_BY_NAME(@database_name, 'DATABASE', 'VIEW DEFINITION')`
   - Verify VIEW DEFINITION permission
   - If insufficient permissions, list required permissions

4. **Parse Flags**
   - Extract and validate `--report` flag (full/summary)
   - Extract and validate `--include` flag (parse comma-separated list)
   - Extract and validate `--format` flag (markdown/json)
   - Set defaults for missing flags

5. **Initialize Output**
   - Create output directory: `marketplace/output/schema-analysis/`
   - Generate output filename: `schema-structure-{database}-{timestamp}.{ext}`
   - Initialize report structure based on format flag

**Success Criteria**:
- MCP connection established
- Database exists and is accessible
- Permissions validated
- Flags parsed successfully
- Output file initialized

**Error Handling**:
- Connection failure: Provide MCP troubleshooting steps
- Database not found: Suggest available databases
- Permission denied: List required permissions
- Invalid flags: Provide valid options and examples

**Tools Used**: Bash (MCP queries), Write (initialize output file)

---

### Phase 2: Metadata Extraction

**Objective**: Extract comprehensive schema metadata from SQL Server system catalogs.

**Steps**:

1. **Extract Table Metadata**
   - Query `sys.tables` joined with `sys.schemas`
   - Get table names, schemas, create dates, modify dates
   - Calculate row counts: `SELECT object_id, SUM(rows) FROM sys.partitions WHERE index_id IN (0,1) GROUP BY object_id`
   - Calculate data/index sizes from `sys.dm_db_partition_stats`
   - Store in structured format

2. **Extract Column Metadata**
   - Query `sys.columns` joined with `sys.types`
   - Get column names, data types, nullability, defaults, computed columns
   - Identify identity columns from `sys.identity_columns`
   - Check for deprecated data types (text, ntext, image)
   - Store column details for each table

3. **Extract Index Metadata**
   - Query `sys.indexes` with index columns from `sys.index_columns`
   - Get index names, types (clustered/non-clustered), uniqueness, included columns
   - Query `sys.dm_db_index_physical_stats` for fragmentation
   - Identify missing indexes from `sys.dm_db_missing_index_details`
   - Check for unused indexes from `sys.dm_db_index_usage_stats`

4. **Extract Constraint Metadata**
   - Primary Keys: `sys.key_constraints` WHERE type = 'PK'
   - Foreign Keys: `sys.foreign_keys` with referenced tables
   - Unique Constraints: `sys.key_constraints` WHERE type = 'UQ'
   - Check Constraints: `sys.check_constraints` with definitions
   - Default Constraints: `sys.default_constraints` with definitions

5. **Extract Stored Procedure Metadata** (if `--include` contains procs)
   - Query `sys.procedures` for procedure names, create/modify dates
   - Extract procedure definitions from `sys.sql_modules`
   - Analyze parameters from `sys.parameters`
   - Check for recompilation hints and SET options

6. **Extract Trigger Metadata** (if `--include` contains triggers)
   - Query `sys.triggers` for trigger names and types
   - Get trigger definitions from `sys.sql_modules`
   - Identify enabled/disabled state
   - Check for INSTEAD OF vs AFTER triggers

7. **Extract View Metadata** (if `--include` contains views)
   - Query `sys.views` for view names
   - Get view definitions from `sys.sql_modules`
   - Identify indexed views
   - Check for view dependencies

**Success Criteria**:
- All requested components extracted successfully
- Metadata stored in structured format
- No SQL errors during extraction
- Row counts and sizes calculated accurately

**Error Handling**:
- Query timeout: Break into smaller chunks, provide partial results
- Access denied on specific objects: Skip and note in report
- Large result sets: Implement pagination or sampling
- System catalog unavailable: Suggest SQL Server version compatibility check

**Tools Used**: Bash (MCP SQL queries), Write (store intermediate results)

---

### Phase 3: Structure Analysis

**Objective**: Analyze extracted metadata to identify structure characteristics and potential issues.

**Steps**:

1. **Table Structure Analysis**
   - **Naming Conventions**: Check for consistent naming (PascalCase, snake_case, etc.)
   - **Schema Organization**: Verify logical schema grouping (dbo, app, security, etc.)
   - **Table Sizes**: Identify very large tables (>10M rows) that may need partitioning
   - **Wide Tables**: Flag tables with >50 columns as potential design issues
   - **No Primary Key**: Identify tables without primary keys (critical issue)
   - **Heap Tables**: Find tables without clustered indexes
   - **Empty Tables**: Identify tables with 0 rows (may be unused)

2. **Column Analysis**
   - **Data Type Appropriateness**: Check for oversized data types (varchar(max) when varchar(100) would suffice)
   - **Deprecated Types**: Flag text, ntext, image (recommend varchar(max), nvarchar(max), varbinary(max))
   - **Nullable Columns**: Excessive nullability may indicate poor design
   - **Default Values**: Check for meaningful defaults vs NULL
   - **Computed Columns**: Verify appropriate use and persistence
   - **Identity Columns**: Check for proper seed/increment and risk of overflow

3. **Index Analysis**
   - **Clustered Index Strategy**: Verify appropriate clustering key (sequential, unique, narrow)
   - **Missing Indexes**: Analyze `sys.dm_db_missing_index_details` for high-impact missing indexes
   - **Unused Indexes**: Identify indexes with no seeks/scans/lookups
   - **Duplicate Indexes**: Find indexes with identical or overlapping key columns
   - **Fragmentation**: Flag indexes with >30% fragmentation
   - **Index Coverage**: Check for missing covering indexes on frequent queries
   - **Filtered Indexes**: Verify appropriate use for partial data sets

4. **Constraint Analysis**
   - **Primary Key Coverage**: Ensure all tables have primary keys
   - **Foreign Key Coverage**: Check for referential integrity implementation
   - **Cascade Rules**: Validate CASCADE DELETE/UPDATE appropriateness
   - **Check Constraints**: Verify data validation rules are in place
   - **Unique Constraints**: Check for proper uniqueness enforcement
   - **Disabled Constraints**: Flag constraints that are disabled (integrity risk)

5. **Stored Procedure Analysis** (if included)
   - **Naming Conventions**: Check for consistent naming (sp_, usp_, etc.)
   - **Parameter Usage**: Verify proper parameterization (avoid SQL injection)
   - **SET Options**: Check for proper SET NOCOUNT ON, XACT_ABORT, etc.
   - **Error Handling**: Verify TRY/CATCH blocks and error logging
   - **Dynamic SQL**: Flag dynamic SQL as potential security risk
   - **Deprecated Features**: Check for deprecated T-SQL syntax

6. **Trigger Analysis** (if included)
   - **Trigger Count**: Flag tables with multiple triggers (complexity risk)
   - **Recursive Triggers**: Check for potential infinite loops
   - **Trigger Logic**: Analyze for complex business logic (consider moving to stored procs)
   - **Performance Impact**: Note triggers on large tables (performance concern)

**Success Criteria**:
- All tables analyzed for structure issues
- Columns validated for appropriate data types
- Indexes evaluated for effectiveness
- Constraints checked for completeness
- Issues categorized by severity (critical/warning/info)

**Error Handling**:
- Analysis timeout: Prioritize critical checks, defer optional ones
- Incomplete metadata: Note gaps in report
- Ambiguous patterns: Request user clarification or make conservative assumptions

**Tools Used**: Read (reference best practices), Write (document findings)

---

### Phase 4: Pattern Detection

**Objective**: Identify design patterns and anti-patterns in the schema.

**Steps**:

1. **Detect Design Patterns**

   **Audit Trail Pattern**:
   - Look for: CreatedDate, CreatedBy, ModifiedDate, ModifiedBy columns
   - Benefit: Change tracking and compliance
   - Tables implementing: {list}

   **Soft Delete Pattern**:
   - Look for: IsDeleted, DeletedDate, DeletedBy columns
   - Benefit: Data recovery and audit trail
   - Tables implementing: {list}

   **Type-Subtype Pattern**:
   - Look for: Tables with TypeID FK to *Type tables
   - Benefit: Extensible classification system
   - Examples: {list}

   **Hierarchy Pattern**:
   - Look for: Self-referential FKs (ParentID to same table)
   - Benefit: Tree structures (org charts, categories)
   - Examples: {list}

   **Many-to-Many Pattern**:
   - Look for: Junction tables with two FKs as composite PK
   - Benefit: Proper modeling of M:N relationships
   - Examples: {list}

   **Version Control Pattern**:
   - Look for: VersionNumber, IsCurrent, EffectiveDate columns
   - Benefit: Historical data tracking
   - Tables implementing: {list}

2. **Detect Anti-Patterns**

   **God Table Anti-Pattern**:
   - Detect: Tables with >50 columns
   - Issue: Violates Single Responsibility Principle
   - Impact: Maintenance difficulty, performance issues
   - Affected tables: {list}
   - Recommendation: Decompose into related tables

   **EAV (Entity-Attribute-Value) Anti-Pattern**:
   - Detect: Tables like (EntityID, AttributeName, AttributeValue)
   - Issue: Loses type safety, hard to query
   - Impact: Poor performance, complex queries
   - Affected tables: {list}
   - Recommendation: Consider JSON columns or proper schema

   **Polymorphic Association Anti-Pattern**:
   - Detect: Generic FKs (e.g., ParentID + ParentType varchar)
   - Issue: Breaks referential integrity
   - Impact: Orphaned records, data integrity issues
   - Affected tables: {list}
   - Recommendation: Separate FKs for each parent type

   **Fear of NULL Anti-Pattern**:
   - Detect: Columns with DEFAULT '' or DEFAULT 0 that should be NULL
   - Issue: NULL has semantic meaning (unknown/inapplicable)
   - Impact: Ambiguous data, incorrect aggregations
   - Affected columns: {list}
   - Recommendation: Allow NULL where appropriate

   **Multicolumn Attributes Anti-Pattern**:
   - Detect: Columns like Tag1, Tag2, Tag3 or Phone1, Phone2, Phone3
   - Issue: Fixed number of values, violates 1NF
   - Impact: Query complexity, wasted space
   - Affected tables: {list}
   - Recommendation: Create related table with 1:N relationship

   **Metadata Tribbles Anti-Pattern**:
   - Detect: Tables created dynamically (Table_2024, Table_2025, etc.)
   - Issue: Schema changes over time, union queries needed
   - Impact: Maintenance nightmare, query complexity
   - Affected tables: {list}
   - Recommendation: Use partitioning or add date column

   **CHAR(1) for Boolean Anti-Pattern**:
   - Detect: CHAR(1) columns with CHECK IN ('Y', 'N')
   - Issue: SQL Server has BIT type for booleans
   - Impact: Wastes space, less clear intent
   - Affected columns: {list}
   - Recommendation: Use BIT type

3. **Calculate Pattern Metrics**
   - **Pattern Coverage**: Percentage of tables implementing positive patterns
   - **Anti-Pattern Density**: Number of anti-patterns per 100 tables
   - **Consistency Score**: How consistently patterns are applied
   - **Maintainability Index**: Weighted score based on patterns and anti-patterns

**Success Criteria**:
- Design patterns identified with table counts
- Anti-patterns detected with severity levels
- Metrics calculated for overall schema quality
- Recommendations generated for each anti-pattern

**Error Handling**:
- Ambiguous patterns: Document assumptions made
- Edge cases: Flag for manual review
- False positives: Provide reasoning for detection

**Tools Used**: Read (pattern definitions), Write (document patterns)

---

### Phase 5: Recommendation Generation

**Objective**: Generate prioritized, actionable recommendations based on analysis findings.

**Steps**:

1. **Categorize Issues by Severity**

   **Critical (Fix Immediately)**:
   - Tables without primary keys
   - Disabled foreign key constraints
   - Orphaned foreign key references
   - SQL injection vulnerabilities in stored procedures
   - Deprecated data types in production tables

   **High (Fix Soon)**:
   - Missing foreign key indexes
   - Highly fragmented indexes (>50%)
   - Tables without clustered indexes (heaps)
   - Missing indexes with high impact score
   - Polymorphic association anti-pattern

   **Medium (Plan to Fix)**:
   - Unused indexes consuming space
   - Duplicate indexes
   - God table anti-pattern
   - Inconsistent naming conventions
   - Missing audit trail columns

   **Low (Consider)**:
   - Oversized data types (varchar(max) when not needed)
   - Nullable columns that should have defaults
   - Potential denormalization opportunities
   - Documentation improvements

2. **Generate Specific Recommendations**

   For each issue, provide:
   - **Title**: Concise description
   - **Issue**: Detailed explanation of the problem
   - **Impact**: What will happen if not fixed (performance, data integrity, maintenance)
   - **Solution**: Step-by-step fix procedure
   - **SQL Script**: Executable T-SQL code (when applicable)
   - **Testing**: How to verify the fix worked
   - **Rollback**: How to undo if needed

   Example recommendation:
   ```markdown
   ### Critical - Add Primary Key to UserSessions Table

   **Issue**: The UserSessions table has no primary key, making it difficult to uniquely identify rows and causing performance issues with updates and deletes.

   **Impact**:
   - Queries use table scans instead of seeks (slow)
   - Cannot create foreign keys referencing this table
   - Risk of duplicate records
   - Merge replication cannot be used

   **Solution**:
   1. Identify appropriate primary key column(s)
   2. Verify uniqueness of selected column(s)
   3. Add primary key constraint
   4. Create supporting indexes if needed

   **SQL Script**:
   ```sql
   -- Verify uniqueness first
   SELECT SessionID, COUNT(*)
   FROM UserSessions
   GROUP BY SessionID
   HAVING COUNT(*) > 1;

   -- If no duplicates, add primary key
   ALTER TABLE UserSessions
   ADD CONSTRAINT PK_UserSessions PRIMARY KEY CLUSTERED (SessionID);
   ```

   **Testing**:
   - Verify constraint created: `SELECT * FROM sys.key_constraints WHERE parent_object_id = OBJECT_ID('UserSessions')`
   - Test query performance improvement with execution plans
   - Attempt to insert duplicate (should fail)

   **Rollback**:
   ```sql
   ALTER TABLE UserSessions DROP CONSTRAINT PK_UserSessions;
   ```
   ```

3. **Prioritize Recommendations**
   - Sort by severity (Critical > High > Medium > Low)
   - Within severity, sort by impact (data integrity > performance > maintainability)
   - Consider dependencies (fix PK before adding FKs)
   - Estimate effort (quick wins vs major refactoring)

4. **Create Implementation Plan**
   - Group related recommendations into phases
   - Suggest implementation order
   - Estimate time for each recommendation
   - Identify recommendations that can be batched
   - Note recommendations requiring downtime

5. **Generate Summary Metrics**
   - Total recommendations: {count}
   - Critical: {count}, High: {count}, Medium: {count}, Low: {count}
   - Estimated total effort: {hours/days}
   - Quick wins (< 1 hour): {count}
   - Major refactoring (> 1 day): {count}

**Success Criteria**:
- All issues have recommendations
- Recommendations are specific and actionable
- SQL scripts provided where applicable
- Prioritization is clear and justified
- Implementation plan is realistic

**Error Handling**:
- Complex issues: Break into smaller steps
- Ambiguous solutions: Provide multiple options with trade-offs
- Cannot auto-generate script: Provide manual procedure

**Tools Used**: Write (generate recommendations), Read (reference SQL patterns)

---

### Phase 6: Report Generation and Output

**Objective**: Compile analysis findings into a comprehensive, well-formatted report.

**Steps**:

1. **Compile Report Sections**

   **Executive Summary**:
   - Database name and analysis date
   - Total objects analyzed (tables, indexes, constraints, etc.)
   - Overall health score (0-100 based on issues found)
   - Critical issues requiring immediate attention
   - Quick wins (easy high-impact fixes)
   - Estimated effort for all recommendations

   **Schema Overview**:
   - Database properties (size, compatibility level, collation)
   - Object counts by type
   - Largest tables by row count and size
   - Schema distribution (tables by schema)

   **Detailed Analysis by Component**:
   - Tables: Structure, naming, issues
   - Indexes: Coverage, fragmentation, missing/unused
   - Constraints: Completeness, enforcement
   - Stored Procedures: Design, security, performance (if analyzed)
   - Triggers: Count, complexity, risks (if analyzed)
   - Views: Usage, indexing (if analyzed)

   **Design Patterns**:
   - Positive patterns detected with examples
   - Pattern adoption metrics
   - Consistency across schema

   **Anti-Patterns**:
   - Anti-patterns detected with affected objects
   - Severity and impact assessment
   - Recommended fixes

   **Recommendations**:
   - Prioritized list by severity
   - Each recommendation with full details (issue, impact, solution, script)
   - Implementation phases

   **Appendices**:
   - Complete table listing with key metrics
   - Index fragmentation report
   - Missing index recommendations
   - Unused index listing

2. **Format Report Based on --format Flag**

   **Markdown Format**:
   - Use headings, bullet points, code blocks
   - Include tables for structured data
   - Add horizontal rules for section separation
   - Use blockquotes for important notes
   - Syntax highlighting for SQL code blocks

   **JSON Format**:
   - Structured JSON with nested objects
   - Include all data in machine-parseable format
   - Follow JSON schema for consistency
   - Suitable for CI/CD integration or custom tooling

3. **Apply --report Flag**

   **Full Report**:
   - Include all sections
   - Detailed analysis for every table
   - Complete recommendation list
   - All SQL scripts and examples

   **Summary Report**:
   - Executive summary only
   - Critical and high-priority issues only
   - Top 10 recommendations
   - Abbreviated appendices (top 10 tables, indexes)

4. **Write Output File**
   - Save to: `marketplace/output/schema-analysis/schema-structure-{database}-{timestamp}.md` (or .json)
   - Verify file written successfully
   - Display file path to user
   - Generate file size and line count

5. **Generate Success Message**
   ```
   Schema analysis complete for database '{database}'.

   Report saved to: output/schema-analysis/schema-structure-{database}-{timestamp}.md

   Summary:
   - Tables analyzed: {count}
   - Issues found: {count} ({critical} critical, {high} high, {medium} medium, {low} low)
   - Patterns detected: {count}
   - Anti-patterns detected: {count}
   - Recommendations: {count}

   Top Priority Actions:
   1. {critical_issue_1}
   2. {critical_issue_2}
   3. {critical_issue_3}

   Review the full report for detailed findings and SQL scripts.
   ```

6. **Handle --format=json Output**
   - If JSON format requested, also display JSON summary to console
   - Provide example of parsing the JSON file
   - Suggest tools for JSON analysis (jq, PowerShell ConvertFrom-Json)

**Success Criteria**:
- Report generated successfully in requested format
- All analysis findings included
- Report is well-formatted and readable
- Output file saved to correct location
- User notified of completion with key metrics

**Error Handling**:
- File write failure: Retry with alternate location or display report to console
- Formatting errors: Fall back to plain text format
- Large report (>10MB): Offer to split into multiple files

**Tools Used**: Write (save report), Bash (file operations)

---

## Error Handling

### MCP Connection Errors

**Error**: "Cannot connect to MSSQL server via MCP"

**Recovery**:
1. Check MCP server status in Claude Code
2. Verify MSSQL MCP configuration in settings
3. Test connection string independently
4. Provide detailed troubleshooting steps in error message
5. Suggest offline analysis mode (if available)

### Database Access Errors

**Error**: "Database '{database}' not found"

**Recovery**:
1. Query available databases: `SELECT name FROM sys.databases`
2. Suggest similar database names (fuzzy match)
3. Ask user to verify database name spelling
4. Check if database is offline or restoring

**Error**: "Permission denied - VIEW DEFINITION required"

**Recovery**:
1. List current user permissions
2. Provide SQL script to grant required permissions:
   ```sql
   USE [DatabaseName];
   GRANT VIEW DEFINITION TO [UserName];
   ```
3. Suggest contacting DBA for permissions
4. Document minimum required permissions in error message

### Analysis Errors

**Error**: "Query timeout during metadata extraction"

**Recovery**:
1. Return partial results with note about incompleteness
2. Suggest analyzing components separately with `--include` flag
3. Offer to retry with increased timeout
4. Recommend analyzing during low-usage period

**Error**: "Insufficient memory for large database analysis"

**Recovery**:
1. Switch to streaming/incremental analysis
2. Analyze tables in batches
3. Reduce metadata collection scope
4. Suggest using `--report=summary` for lighter analysis

### Output Errors

**Error**: "Cannot write to output directory"

**Recovery**:
1. Check directory permissions
2. Try alternate output location (temp directory)
3. Offer to display report to console instead of file
4. Create output directory if missing

## Examples

### Example 1: Full Database Analysis

**Input**:
```bash
/analyze-schema ProductionDB --report=full
```

**Process**:
1. Connect to ProductionDB via MCP
2. Extract metadata for all components (tables, indexes, constraints, procs, triggers, views)
3. Analyze structure and detect patterns
4. Generate comprehensive recommendations
5. Save detailed report to `marketplace/output/schema-analysis/schema-structure-ProductionDB-20260116-143022.md`

**Output Highlights**:
```markdown
# Database Schema Analysis Report
## Database: ProductionDB
## Analysis Date: 2026-01-16 14:30:22

### Executive Summary
- Total Tables: 87
- Total Indexes: 234
- Total Constraints: 156
- Critical Issues: 3
- Warnings: 12
- Recommendations: 18
- Overall Health Score: 76/100

### Critical Issues
1. **UserSessions table has no primary key** - Fix immediately to enable referential integrity and improve performance
2. **Disabled foreign key FK_Orders_Customers** - Re-enable to ensure data consistency
3. **SQL injection vulnerability in GetUserData stored procedure** - Security risk requiring immediate attention

### Quick Wins (< 1 hour effort, high impact)
1. Add missing index on Orders.CustomerID (impacts 45% of queries)
2. Update deprecated 'text' columns to 'varchar(max)' in 3 tables
3. Enable PK on UserSessions table

[... detailed analysis continues ...]
```

---

### Example 2: Summary Analysis for Quick Review

**Input**:
```bash
/analyze-schema TestDB --report=summary --include=tables,indexes
```

**Process**:
1. Connect to TestDB via MCP
2. Extract metadata for tables and indexes only
3. Perform high-level analysis
4. Generate summary report with top issues only
5. Save to `marketplace/output/schema-analysis/schema-structure-TestDB-20260116-143500.md`

**Output**:
```markdown
# Schema Analysis Summary: TestDB

**Analysis Date**: 2026-01-16 14:35:00
**Tables Analyzed**: 23
**Indexes Analyzed**: 67

## Health Overview
- Overall Score: 82/100
- Critical Issues: 0
- High Priority Issues: 2
- Medium Priority Issues: 5

## Top 3 Recommendations
1. **High** - Add missing index on Products.CategoryID
   - Impact: 38% of queries will improve
   - Effort: 5 minutes
   - SQL: `CREATE NONCLUSTERED INDEX IX_Products_CategoryID ON Products(CategoryID) INCLUDE (ProductName, Price)`

2. **High** - Rebuild fragmented index IX_Orders_OrderDate
   - Impact: Range queries on OrderDate currently slow
   - Effort: 15 minutes (depends on table size)
   - SQL: `ALTER INDEX IX_Orders_OrderDate ON Orders REBUILD`

3. **Medium** - Remove unused index IX_Customers_LastName
   - Impact: Saves space, reduces insert overhead
   - Effort: 5 minutes
   - SQL: `DROP INDEX IX_Customers_LastName ON Customers`

[... summary continues with top 10 items only ...]
```

---

### Example 3: JSON Output for Automation

**Input**:
```bash
/analyze-schema AnalyticsDB --format=json
```

**Process**:
1. Perform full analysis
2. Generate structured JSON output
3. Save to `marketplace/output/schema-analysis/schema-structure-AnalyticsDB-20260116-144000.json`

**Output Sample**:
```json
{
  "database": "AnalyticsDB",
  "analysis_date": "2026-01-16T14:40:00Z",
  "summary": {
    "total_tables": 45,
    "total_indexes": 123,
    "total_constraints": 89,
    "health_score": 88,
    "critical_issues": 0,
    "high_priority_issues": 1,
    "medium_priority_issues": 4,
    "low_priority_issues": 8
  },
  "tables": [
    {
      "name": "Users",
      "schema": "dbo",
      "row_count": 1520000,
      "data_size_mb": 450.2,
      "index_size_mb": 120.5,
      "columns": 18,
      "has_primary_key": true,
      "has_clustered_index": true,
      "foreign_keys": 2,
      "issues": []
    },
    {
      "name": "Sessions",
      "schema": "dbo",
      "row_count": 8940000,
      "data_size_mb": 2340.8,
      "index_size_mb": 890.3,
      "columns": 12,
      "has_primary_key": true,
      "has_clustered_index": true,
      "foreign_keys": 1,
      "issues": [
        {
          "severity": "high",
          "type": "missing_index",
          "description": "Missing index on UserID (high impact query)",
          "recommendation": "CREATE NONCLUSTERED INDEX IX_Sessions_UserID ON Sessions(UserID)"
        }
      ]
    }
  ],
  "patterns": [
    {
      "name": "Audit Trail Pattern",
      "tables_implementing": ["Users", "Orders", "Products"],
      "coverage_percentage": 35
    }
  ],
  "anti_patterns": [
    {
      "name": "God Table Anti-Pattern",
      "severity": "medium",
      "tables_affected": ["UserProfiles"],
      "description": "UserProfiles table has 67 columns",
      "recommendation": "Decompose into Users, Preferences, and Profile tables"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "title": "Add missing index on Sessions.UserID",
      "category": "performance",
      "impact": "High-frequency queries will improve by ~40%",
      "effort_hours": 0.25,
      "sql_script": "CREATE NONCLUSTERED INDEX IX_Sessions_UserID ON Sessions(UserID) INCLUDE (SessionStart, SessionEnd)"
    }
  ]
}
```

---

## Success Metrics

### Quantitative Metrics

1. **Analysis Completion Rate**: 100% of requested components analyzed
2. **Accuracy**: >95% of identified issues are true positives
3. **Execution Time**: <10 minutes for databases with <100 tables
4. **Report Quality**: All sections present with no missing data

### Qualitative Metrics

1. **Actionability**: Every recommendation includes specific SQL script or procedure
2. **Clarity**: Non-technical stakeholders can understand the executive summary
3. **Completeness**: All schema components are covered in the analysis
4. **Usefulness**: Developers can implement recommendations without additional research

### User Validation

1. User confirms report is comprehensive and accurate
2. User successfully implements at least one recommendation
3. User reports improved understanding of database structure
4. Report is referenced in future development decisions

## Dependencies

### Required
- **MSSQL MCP Server**: For SQL Server connectivity and query execution
- **Bash Tool**: For executing MCP queries and file operations
- **Write Tool**: For generating and saving reports

### Optional
- **Read Tool**: For referencing best practices documentation
- **Grep/Glob Tools**: For searching related configuration files (if analyzing local SQL scripts)

## Version History

- **2.0.0** (2026-01-16): Initial release with comprehensive schema analysis capabilities
  - Full table, index, and constraint analysis
  - Design pattern and anti-pattern detection
  - Automated recommendation generation
  - Multiple output formats (markdown, JSON)
  - Configurable report detail levels

## Notes

- This agent focuses on **structure analysis**. For normalization analysis, use the `normalization-advisor` agent.
- For relationship-specific analysis, use the `foreign-key-analyzer` agent.
- For migration planning, use the `schema-migration-planner` agent.
- Analysis is read-only and does not modify the database.
- Large databases (>500 tables) may require increased timeout or component-specific analysis with `--include` flag.
- For optimal performance, run during low-usage periods when system catalogs are less contended.
