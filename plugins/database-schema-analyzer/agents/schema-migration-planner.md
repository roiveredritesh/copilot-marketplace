---
agent_name: schema-migration-planner
version: 2.0.0
description: Plans schema migrations between database versions. Analyzes source and target schemas, detects breaking changes, data migration needs, backward compatibility issues, and generates migration scripts with rollback plans.
task_types:
  - migration-planning
  - version-upgrade
  - schema-evolution
mcp_required:
  - mssql
tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
complexity: high
estimated_duration: 10-20 minutes
output_format: markdown_report
sequential_thinking: enabled
---

# Schema Migration Planner Agent

## Purpose

The Schema Migration Planner agent automates the planning and execution strategy for database schema migrations. It compares source and target database schemas, identifies structural differences, detects breaking changes, analyzes data migration requirements, generates T-SQL migration scripts, creates rollback procedures, and provides comprehensive testing checklists.

This agent is essential for database version upgrades, schema refactoring projects, multi-environment deployments, and ensuring safe, repeatable database migrations with minimal downtime.

## When to Use This Agent

Use this agent when you need to:

- **Version Upgrades**: Plan migration from one database version to another
- **Schema Refactoring**: Execute major schema changes safely
- **Environment Promotion**: Deploy schema changes from dev to staging to production
- **Database Merging**: Combine schemas from multiple sources
- **Backward Compatibility**: Ensure new schema supports existing applications
- **Breaking Change Analysis**: Identify changes that will break existing code
- **Data Migration**: Plan for data transformation and transfer
- **Zero-Downtime Deployments**: Create incremental migration strategies
- **Rollback Planning**: Prepare for potential migration failures
- **Compliance**: Document schema change audit trails

## Input Requirements

### Required Parameters

1. **source_database** (string): Name of the source/current database
   - Must be accessible via MCP connection
   - Represents the "before" state

2. **target_database** (string): Name of the target/new database
   - Must be accessible via MCP connection
   - Represents the "after" state
   - Can be on same server or different server

### Optional Flags

1. **--analyze-data** (boolean): Include data migration analysis
   - Analyzes sample data to detect transformation needs
   - Checks for data type compatibility
   - Identifies potential data loss scenarios
   - Default: false (schema-only comparison)

2. **--generate-scripts** (boolean): Generate executable T-SQL migration scripts
   - Creates forward migration scripts
   - Creates rollback scripts
   - Includes error handling and transactions
   - Default: true

3. **--check-compatibility** (boolean): Perform backward compatibility analysis
   - Identifies breaking changes for existing applications
   - Checks for removed columns/tables
   - Validates data type changes
   - Default: true

### Input Examples

```bash
# Basic migration plan
source_database: "MyDB_v1"
target_database: "MyDB_v2"
flags: --generate-scripts

# Full migration with data analysis
source_database: "ProductionDB"
target_database: "ProductionDB_NextVersion"
flags: --analyze-data --generate-scripts --check-compatibility

# Compatibility check only
source_database: "CurrentDB"
target_database: "ProposedDB"
flags: --check-compatibility
```

## Output Format

### Markdown Report Structure

```markdown
# Schema Migration Plan
## Source: {source_database} → Target: {target_database}
## Plan Date: {timestamp}

### Executive Summary
- Migration Type: {major/minor/patch}
- Breaking Changes: {count}
- New Objects: {count}
- Modified Objects: {count}
- Deleted Objects: {count}
- Data Migration Required: {yes/no}
- Estimated Downtime: {duration}
- Risk Level: {high/medium/low}

### Migration Overview
- Total Changes: {count}
- Schema Differences: {list}
- Recommended Approach: {blue-green/incremental/offline}

### Breaking Changes (CRITICAL)
1. **{change_type}**: {description}
   - Impact: {description}
   - Affected Applications: {list}
   - Mitigation: {strategy}
   - Must Complete Before: {prerequisite}

### Schema Comparison

#### New Objects
- **Tables**: {list with descriptions}
- **Columns**: {list with table.column}
- **Indexes**: {list}
- **Constraints**: {list}
- **Stored Procedures**: {list}

#### Modified Objects
- **Table**: {name}
  - Changed: {description}
  - Reason: {explanation}
  - Compatibility: {breaking/non-breaking}
  - Migration Script: {reference}

#### Deleted Objects (HIGH RISK)
- **Table**: {name}
  - Reason for Deletion: {explanation}
  - Data Preservation: {strategy}
  - Application Impact: {description}

### Data Migration Strategy
- Approach: {in-place/ETL/dual-write}
- Data Transformations Required: {count}
- Estimated Duration: {time}
- Rollback Capability: {yes/no}

#### Data Transformations
1. **{table_name}**: {transformation_description}
   - SQL Script: {script}
   - Validation Query: {query}

### Migration Scripts

#### Forward Migration (deploy.sql)
```sql
{full migration script}
```

#### Rollback Script (rollback.sql)
```sql
{full rollback script}
```

### Deployment Plan

#### Phase 1: Pre-Migration
- [ ] Backup production database
- [ ] Verify backup restoration
- [ ] Test migration in staging
- [ ] Notify stakeholders

#### Phase 2: Migration Execution
- [ ] Put application in maintenance mode
- [ ] Run forward migration script
- [ ] Validate schema changes
- [ ] Run data migration (if needed)

#### Phase 3: Validation
- [ ] Run validation queries
- [ ] Test application connectivity
- [ ] Verify data integrity
- [ ] Check performance

#### Phase 4: Completion
- [ ] Remove maintenance mode
- [ ] Monitor for errors
- [ ] Document completion
- [ ] Archive migration artifacts

### Rollback Plan
- Rollback Window: {duration}
- Rollback Trigger: {conditions}
- Rollback Steps: {list}
- Data Recovery: {strategy}

### Testing Checklist
- [ ] {test_description}

### Risk Assessment
- **High Risks**: {list with mitigation}
- **Medium Risks**: {list with mitigation}
- **Low Risks**: {list}

### Recommendations
1. {recommendation with rationale}
```

## Detailed Process

### Phase 1: Connection and Schema Extraction

**Objective**: Connect to both databases and extract complete schema metadata for comparison.

**Steps**:

1. **Validate MCP Connection**
   - Test MSSQL MCP server availability
   - Verify connection to SQL Server instance
   - If connection fails, provide detailed error with troubleshooting steps

2. **Validate Source Database**
   - Query: `SELECT name FROM sys.databases WHERE name = @source_database`
   - Verify database exists and is accessible
   - Check user has VIEW DEFINITION permission
   - Record source database properties (collation, compatibility level, size)

3. **Validate Target Database**
   - Query: `SELECT name FROM sys.databases WHERE name = @target_database`
   - Verify database exists and is accessible
   - Check user has VIEW DEFINITION permission
   - Record target database properties
   - Verify target is on compatible SQL Server version

4. **Extract Source Schema Metadata**

   **Tables**:
   ```sql
   SELECT
       s.name AS SchemaName,
       t.name AS TableName,
       t.create_date,
       t.modify_date,
       SUM(p.rows) AS RowCount
   FROM sys.tables t
   JOIN sys.schemas s ON t.schema_id = s.schema_id
   LEFT JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0,1)
   GROUP BY s.name, t.name, t.create_date, t.modify_date
   ORDER BY s.name, t.name
   ```

   **Columns**:
   ```sql
   SELECT
       OBJECT_SCHEMA_NAME(c.object_id) AS SchemaName,
       OBJECT_NAME(c.object_id) AS TableName,
       c.name AS ColumnName,
       TYPE_NAME(c.user_type_id) AS DataType,
       c.max_length,
       c.precision,
       c.scale,
       c.is_nullable,
       c.is_identity,
       dc.definition AS DefaultValue
   FROM sys.columns c
   LEFT JOIN sys.default_constraints dc ON c.default_object_id = dc.object_id
   WHERE OBJECTPROPERTY(c.object_id, 'IsUserTable') = 1
   ORDER BY SchemaName, TableName, c.column_id
   ```

   **Indexes**:
   ```sql
   SELECT
       OBJECT_SCHEMA_NAME(i.object_id) AS SchemaName,
       OBJECT_NAME(i.object_id) AS TableName,
       i.name AS IndexName,
       i.type_desc AS IndexType,
       i.is_unique,
       i.is_primary_key,
       STRING_AGG(COL_NAME(ic.object_id, ic.column_id), ', ') AS IndexColumns
   FROM sys.indexes i
   JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
   WHERE OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1
   GROUP BY i.object_id, i.name, i.type_desc, i.is_unique, i.is_primary_key
   ORDER BY SchemaName, TableName, IndexName
   ```

   **Constraints**:
   ```sql
   -- Primary Keys
   SELECT SchemaName, TableName, ConstraintName, 'PRIMARY KEY' AS ConstraintType
   FROM sys.key_constraints WHERE type = 'PK'

   -- Foreign Keys
   SELECT
       OBJECT_SCHEMA_NAME(f.parent_object_id) AS SchemaName,
       OBJECT_NAME(f.parent_object_id) AS TableName,
       f.name AS ConstraintName,
       'FOREIGN KEY' AS ConstraintType,
       OBJECT_NAME(f.referenced_object_id) AS ReferencedTable,
       f.delete_referential_action_desc AS DeleteAction,
       f.update_referential_action_desc AS UpdateAction
   FROM sys.foreign_keys f

   -- Check Constraints
   SELECT
       OBJECT_SCHEMA_NAME(cc.parent_object_id) AS SchemaName,
       OBJECT_NAME(cc.parent_object_id) AS TableName,
       cc.name AS ConstraintName,
       'CHECK' AS ConstraintType,
       cc.definition
   FROM sys.check_constraints cc
   ```

   **Stored Procedures**:
   ```sql
   SELECT
       OBJECT_SCHEMA_NAME(p.object_id) AS SchemaName,
       p.name AS ProcedureName,
       p.create_date,
       p.modify_date,
       m.definition
   FROM sys.procedures p
   LEFT JOIN sys.sql_modules m ON p.object_id = m.object_id
   ORDER BY SchemaName, ProcedureName
   ```

   **Triggers, Views, Functions** (similar queries)

5. **Extract Target Schema Metadata**
   - Run identical queries on target database
   - Store target metadata separately for comparison

6. **Parse Optional Flags**
   - Check if `--analyze-data` is present
   - Check if `--generate-scripts` is present (default true)
   - Check if `--check-compatibility` is present (default true)

7. **Initialize Output**
   - Create output directory: `marketplace/output/schema-analysis/`
   - Generate filename: `migration-plan-{source}-to-{target}-{timestamp}.md`
   - Initialize report structure

**Success Criteria**:
- Both databases accessible via MCP
- Complete schema metadata extracted for source and target
- Metadata stored in comparable structures
- Flags parsed successfully
- Output file initialized

**Error Handling**:
- Database not found: List available databases, ask user to verify names
- Permission denied: Provide script to grant VIEW DEFINITION permission
- Connection timeout: Retry with increased timeout, suggest analyzing during low-load period
- Different SQL Server versions: Warn about compatibility, continue if versions compatible

**Tools Used**: Bash (MCP queries), Write (store metadata)

---

### Phase 2: Schema Comparison and Difference Detection

**Objective**: Compare source and target schemas to identify all differences at object and attribute levels.

**Steps**:

1. **Compare Tables**

   **New Tables** (in target, not in source):
   ```
   target_tables - source_tables = new_tables
   ```
   - List all new tables with schemas
   - Indicate purpose/reason if derivable from naming
   - Mark as non-breaking (additions are generally safe)

   **Deleted Tables** (in source, not in target):
   ```
   source_tables - target_tables = deleted_tables
   ```
   - List all deleted tables
   - **Mark as BREAKING CHANGE**
   - Check for foreign key dependencies
   - Analyze data preservation needs

   **Modified Tables** (in both but with changes):
   - Tables present in both but with column/constraint differences
   - Requires deep column-level comparison

2. **Compare Columns (for modified tables)**

   **New Columns**:
   - Columns in target table not in source table
   - Check if nullable or has default (non-breaking)
   - Check if NOT NULL without default (BREAKING - requires data population)

   **Deleted Columns**:
   - Columns in source table not in target table
   - **Mark as BREAKING CHANGE**
   - Application may be reading/writing this column
   - Data preservation strategy needed

   **Modified Columns**:
   - Same column name but different attributes
   - Compare: data type, length, precision, scale, nullability, default, identity

   **Breaking Column Changes**:
   - Data type narrowing (varchar(100) → varchar(50)) - potential data loss
   - Precision reduction (decimal(18,4) → decimal(10,2)) - data loss risk
   - NOT NULL added without default - existing NULL values invalid
   - Default removed - application may rely on it

   **Non-Breaking Column Changes**:
   - Data type widening (varchar(50) → varchar(100))
   - NULL allowed on previously NOT NULL column
   - Default value added
   - Precision increase

3. **Compare Indexes**

   **New Indexes**:
   - Indexes in target not in source
   - Generally non-breaking (performance improvement)
   - May impact insert/update/delete performance slightly

   **Deleted Indexes**:
   - Indexes in source not in target
   - May impact query performance negatively
   - Check if application relies on specific index for performance

   **Modified Indexes**:
   - Same index name but different columns or properties
   - Treat as delete + create (requires drop and recreate)

4. **Compare Constraints**

   **New Constraints**:
   - Primary keys added: Check uniqueness of existing data first
   - Foreign keys added: Check referential integrity of existing data first
   - Check constraints added: Validate existing data against check condition
   - Unique constraints added: Check for duplicate data first
   - **Potentially BREAKING if existing data violates constraint**

   **Deleted Constraints**:
   - Primary key removed: High risk, application may rely on uniqueness
   - Foreign key removed: Referential integrity no longer enforced
   - Generally non-breaking but reduces data quality

   **Modified Constraints**:
   - Cascade rules changed on FK: May cause unexpected deletes/updates
   - Check constraint condition changed: Validate existing data

5. **Compare Stored Procedures, Functions, Views, Triggers**

   **New Objects**:
   - List new objects
   - Generally non-breaking (additions)

   **Deleted Objects**:
   - **BREAKING if application calls these objects**
   - List deleted objects with warning

   **Modified Objects**:
   - Compare definitions (difficult to assess impact)
   - Flag as "requires manual review"
   - Check for signature changes (parameter changes are breaking)

6. **Categorize All Changes**

   **BREAKING CHANGES (Critical)**:
   - Deleted tables
   - Deleted columns
   - Column data type narrowing
   - NOT NULL constraint added without default
   - Deleted stored procedures/functions
   - Stored procedure parameter changes

   **HIGH RISK (Review Required)**:
   - Modified column data types
   - New constraints on existing tables
   - Modified constraint cascade rules
   - Modified stored procedure logic

   **MEDIUM RISK (Test Thoroughly)**:
   - New columns (NOT NULL without default)
   - Deleted indexes
   - Modified indexes

   **LOW RISK (Generally Safe)**:
   - New tables
   - New columns (nullable or with default)
   - New indexes
   - New stored procedures

7. **Calculate Migration Complexity**
   - **Major Migration**: Breaking changes > 5 OR deleted tables > 2
   - **Minor Migration**: Breaking changes 1-5 OR significant modifications
   - **Patch Migration**: Only non-breaking changes

**Success Criteria**:
- All object types compared (tables, columns, indexes, constraints, etc.)
- All differences identified and categorized
- Breaking changes clearly marked
- Compatibility risks assessed
- Migration complexity level determined

**Error Handling**:
- Large schema: Compare in batches, provide progress updates
- Ambiguous changes: Flag for manual review
- Metadata extraction incomplete: Note gaps in comparison

**Tools Used**: Write (document differences)

---

### Phase 3: Breaking Change Analysis and Compatibility Assessment

**Objective**: Analyze breaking changes in detail and assess impact on backward compatibility.

**Steps**:

1. **Assess Each Breaking Change**

   For each breaking change identified in Phase 2:

   **Deleted Table**:
   - **Impact**: Any application reading/writing this table will break
   - **Data Preservation**:
     - Option 1: Retain table as archive (rename to Old_TableName)
     - Option 2: Export data to flat files before deletion
     - Option 3: Create view with same name pointing to new structure
   - **Application Impact**:
     - Query for FK references to assess dependency scope
     - Estimate number of queries/procedures affected
   - **Mitigation**:
     - Provide deprecation period (keep table, mark as deprecated)
     - Create compatibility shim (view or synonym)
     - Update all application code before migration

   **Deleted Column**:
   - **Impact**: SELECT *, INSERT without column list, UPDATE statements affected
   - **Data Preservation**:
     - Option 1: Retain column but stop populating (deprecated)
     - Option 2: Extract data to separate table before deletion
   - **Application Impact**:
     - Search codebase for column references (provide Grep pattern)
     - Check ORM mappings
   - **Mitigation**:
     - Update application to stop using column
     - Add column back as computed column if derivable
     - Create view with old structure for backward compatibility

   **Column Data Type Narrowing**:
   - **Impact**: Existing data may not fit in new type (truncation/overflow)
   - **Data Validation**:
     ```sql
     -- Check for data that won't fit
     SELECT *
     FROM SourceTable
     WHERE LEN(ColumnName) > {new_max_length}
     -- or
     WHERE ColumnName > {new_max_value}
     ```
   - **Mitigation**:
     - Clean data first (truncate/convert)
     - Add validation to prevent future violations
     - Consider keeping wider data type if data justifies it

   **NOT NULL Constraint Added**:
   - **Impact**: Existing NULL values violate constraint
   - **Data Validation**:
     ```sql
     SELECT COUNT(*)
     FROM SourceTable
     WHERE ColumnName IS NULL
     ```
   - **Mitigation**:
     - Populate NULL values with defaults before adding constraint
     - Add DEFAULT constraint along with NOT NULL
     - Staged approach: Add column as nullable, populate, then alter to NOT NULL

2. **Generate Compatibility Matrix**

   Create table showing compatibility for each change:

   | Change | Object | Breaking | Impact Level | Applications Affected | Mitigation Available |
   |--------|--------|----------|--------------|----------------------|---------------------|
   | Deleted | Users.LegacyID column | Yes | High | UserService, ReportingAPI | Add computed column |
   | Modified | Orders.TotalAmount (decimal narrowing) | Yes | Medium | OrderService | Validate data first |
   | Added | Products.CategoryID NOT NULL | Yes | Medium | ProductService | Add default value |

3. **Backward Compatibility Assessment**

   If `--check-compatibility` flag is set:

   **Application Compatibility**:
   - Can existing applications continue to work without code changes? (Yes/No/Partially)
   - What is the minimum application version required after migration?
   - Are there any runtime errors expected?

   **Query Compatibility**:
   - Will existing SQL queries work? (Identify queries that will break)
   - Will stored procedure calls work? (Check for signature changes)
   - Will ORMs work? (Check for entity mapping issues)

   **Deployment Compatibility**:
   - Can migration happen while application is running? (Online migration possible?)
   - Is zero-downtime deployment possible?
   - Estimated downtime required: {duration}

4. **Risk Assessment**

   **High Risk Factors**:
   - Multiple breaking changes (>5)
   - Large data volumes requiring migration (>1M rows)
   - Complex data transformations needed
   - Limited rollback capability
   - Production database with high availability requirements

   **Medium Risk Factors**:
   - Few breaking changes (1-5)
   - Moderate data volumes (100K-1M rows)
   - Simple data transformations
   - Partial rollback capability

   **Low Risk Factors**:
   - No breaking changes
   - Small data volumes (<100K rows)
   - No data transformations
   - Full rollback capability

   **Overall Risk Level**: High / Medium / Low

5. **Mitigation Strategies**

   For each breaking change, provide mitigation options:

   **Blue-Green Deployment**:
   - Deploy new schema to separate database
   - Use dual-write pattern during transition
   - Cut over when ready
   - Rollback = switch back to old database

   **Incremental Migration**:
   - Phase 1: Add new structures (non-breaking)
   - Phase 2: Dual-write to old and new
   - Phase 3: Switch reads to new structure
   - Phase 4: Remove old structures

   **Feature Flags**:
   - Deploy code with new schema support behind feature flag
   - Migrate schema
   - Enable feature flag
   - Rollback = disable feature flag

   **Compatibility Shims**:
   - Create views with old structure pointing to new
   - Create wrapper stored procedures
   - Maintain for deprecation period

**Success Criteria**:
- All breaking changes analyzed in detail
- Impact assessment completed for each change
- Compatibility matrix generated
- Risk level determined with justification
- Mitigation strategies provided for each breaking change

**Error Handling**:
- Unable to determine impact: Flag for manual analysis
- Complex dependencies: Request application code access for deeper analysis
- Ambiguous compatibility: Provide multiple scenarios with trade-offs

**Tools Used**: Write (document analysis), Read (reference patterns)

---

### Phase 4: Data Migration Strategy Development

**Objective**: Develop comprehensive strategy for migrating data from source to target schema (if `--analyze-data` flag is set).

**Steps**:

1. **Identify Data Migration Needs**

   **Tables Requiring Data Migration**:
   - Tables that exist in both source and target but have structural changes
   - Tables being split (denormalization → normalization)
   - Tables being merged (normalization → denormalization)
   - Tables with data transformations needed

2. **Analyze Sample Data** (if `--analyze-data` is set)

   For each table requiring migration:

   **Sample Data Extraction**:
   ```sql
   -- Get representative sample (top 1000 rows, stratified if possible)
   SELECT TOP 1000 *
   FROM SourceTable
   ORDER BY NEWID(); -- Random sample
   ```

   **Data Quality Analysis**:
   - NULL value percentage per column
   - Data type compatibility check (actual data vs target type)
   - Value range analysis (min/max for numeric, length for strings)
   - Identify data anomalies (outliers, unexpected formats)

   **Data Transformation Needs**:
   - Column mapping (source column → target column)
   - Data type conversions needed
   - Data cleaning required (trim, uppercase, format)
   - Calculated/derived values needed
   - Default values for new columns

3. **Define Data Migration Approach**

   **In-Place Migration** (suitable when possible):
   - Migrate schema and data in single transaction
   - Minimal downtime (seconds to minutes)
   - Limited rollback capability
   - Best for: Non-breaking changes, small datasets

   **ETL Migration**:
   - Extract data from source
   - Transform according to new schema
   - Load into target tables
   - Longer process but more control
   - Full rollback capability (keep source intact)
   - Best for: Complex transformations, large datasets

   **Dual-Write Migration**:
   - Write to both old and new schemas during transition
   - Gradual cutover from old to new
   - Zero-downtime migration possible
   - Best for: High-availability systems, large datasets

   **Staged Migration**:
   - Phase 1: Migrate 10% of data, validate
   - Phase 2: Migrate 50% of data, validate
   - Phase 3: Migrate remaining data
   - Best for: Very large datasets, high-risk migrations

4. **Create Data Transformation Scripts**

   For each table requiring data migration:

   **Example: Column Renaming**:
   ```sql
   -- Source: Users table has FirstName, LastName
   -- Target: Users table has FullName

   INSERT INTO Target.dbo.Users (UserID, FullName, Email, CreatedDate)
   SELECT
       UserID,
       FirstName + ' ' + LastName AS FullName,
       Email,
       CreatedDate
   FROM Source.dbo.Users;
   ```

   **Example: Data Type Conversion**:
   ```sql
   -- Source: TotalAmount VARCHAR(50)
   -- Target: TotalAmount DECIMAL(18,2)

   INSERT INTO Target.dbo.Orders (OrderID, TotalAmount)
   SELECT
       OrderID,
       CAST(REPLACE(TotalAmount, ',', '') AS DECIMAL(18,2)) AS TotalAmount
   FROM Source.dbo.Orders
   WHERE ISNUMERIC(REPLACE(TotalAmount, ',', '')) = 1;

   -- Handle invalid data separately
   INSERT INTO Target.dbo.OrdersInvalidData (OrderID, TotalAmount, ErrorReason)
   SELECT
       OrderID,
       TotalAmount,
       'Invalid numeric format'
   FROM Source.dbo.Orders
   WHERE ISNUMERIC(REPLACE(TotalAmount, ',', '')) = 0;
   ```

   **Example: Table Splitting** (denormalization → normalization):
   ```sql
   -- Source: Users table has Address1, Address2, City, State, Zip
   -- Target: Users table + separate Addresses table

   -- Migrate Users
   INSERT INTO Target.dbo.Users (UserID, FirstName, LastName, Email)
   SELECT UserID, FirstName, LastName, Email
   FROM Source.dbo.Users;

   -- Migrate Addresses
   INSERT INTO Target.dbo.Addresses (UserID, AddressLine1, AddressLine2, City, State, ZipCode)
   SELECT UserID, Address1, Address2, City, State, Zip
   FROM Source.dbo.Users
   WHERE Address1 IS NOT NULL; -- Only migrate non-empty addresses
   ```

5. **Create Data Validation Queries**

   For each migration, provide validation:

   **Row Count Validation**:
   ```sql
   -- Verify row counts match
   SELECT
       'Source' AS Source, COUNT(*) AS RowCount FROM Source.dbo.Users
   UNION ALL
   SELECT
       'Target' AS Source, COUNT(*) AS RowCount FROM Target.dbo.Users;
   ```

   **Data Integrity Validation**:
   ```sql
   -- Verify no data loss during type conversion
   SELECT
       s.UserID,
       s.TotalAmount AS SourceValue,
       t.TotalAmount AS TargetValue
   FROM Source.dbo.Users s
   JOIN Target.dbo.Users t ON s.UserID = t.UserID
   WHERE ABS(CAST(s.TotalAmount AS DECIMAL(18,2)) - t.TotalAmount) > 0.01;
   ```

   **Referential Integrity Validation**:
   ```sql
   -- Verify all FKs are valid after migration
   SELECT COUNT(*)
   FROM Target.dbo.Orders o
   LEFT JOIN Target.dbo.Customers c ON o.CustomerID = c.CustomerID
   WHERE c.CustomerID IS NULL;
   -- Should return 0 (no orphaned orders)
   ```

6. **Estimate Data Migration Duration**

   Based on:
   - Total row count across all tables
   - Data transformation complexity
   - Available server resources
   - Historical migration performance

   Formula:
   ```
   Estimated Duration = (Total Rows / Throughput) * Complexity Multiplier
   Throughput = 10,000 rows/second (baseline)
   Complexity Multiplier:
     - Simple (column mapping): 1.0x
     - Moderate (type conversions): 2.0x
     - Complex (calculations, splits): 4.0x
   ```

**Success Criteria**:
- Data migration approach selected with justification
- Transformation scripts generated for all affected tables
- Validation queries provided
- Duration estimated
- Rollback data strategy documented

**Error Handling**:
- Invalid data encountered: Create separate error table to capture
- Transformation failures: Provide fallback values or skip logic
- Large dataset timeout: Implement batching with progress tracking

**Tools Used**: Write (document strategy and scripts)

---

### Phase 5: Migration Script Generation

**Objective**: Generate complete, executable T-SQL scripts for forward migration and rollback.

**Steps**:

1. **Generate Forward Migration Script (deploy.sql)**

   **Script Structure**:
   ```sql
   /*
   ============================================================================
   Database Schema Migration Script
   Source: {source_database} → Target: {target_database}
   Generated: {timestamp}
   ============================================================================

   IMPORTANT:
   - Review this script thoroughly before execution
   - Execute in a test environment first
   - Ensure full backup is taken before running
   - Estimated execution time: {duration}

   Migration Type: {major/minor/patch}
   Breaking Changes: {count}
   Risk Level: {high/medium/low}
   ============================================================================
   */

   -- Set execution options
   SET NOCOUNT ON;
   SET XACT_ABORT ON; -- Rollback on any error

   -- Verify we're on the correct database
   USE [{target_database}];
   GO

   IF DB_NAME() <> '{target_database}'
   BEGIN
       RAISERROR('Script must be run on {target_database} database', 16, 1);
       RETURN;
   END
   GO

   -- Pre-migration validation
   PRINT 'Starting pre-migration validation...';

   -- Check SQL Server version
   IF CAST(SERVERPROPERTY('ProductMajorVersion') AS INT) < 13 -- SQL Server 2016
   BEGIN
       RAISERROR('SQL Server 2016 or higher required', 16, 1);
       RETURN;
   END

   -- Check database compatibility level
   IF (SELECT compatibility_level FROM sys.databases WHERE name = DB_NAME()) < 130
   BEGIN
       RAISERROR('Database compatibility level 130 (SQL Server 2016) or higher required', 16, 1);
       RETURN;
   END

   -- Check free space
   DECLARE @FreeSpaceMB DECIMAL(18,2);
   SELECT @FreeSpaceMB = size/128.0 - CAST(FILEPROPERTY(name, 'SpaceUsed') AS INT)/128.0
   FROM sys.database_files WHERE type_desc = 'ROWS';

   IF @FreeSpaceMB < 1000 -- Require at least 1GB free
   BEGIN
       RAISERROR('Insufficient free space (1GB required)', 16, 1);
       RETURN;
   END

   PRINT 'Pre-migration validation passed.';
   GO

   -- Start transaction
   BEGIN TRANSACTION MigrationTransaction;

   BEGIN TRY

       -- ================================================================
       -- PHASE 1: ADD NEW OBJECTS (Non-Breaking)
       -- ================================================================
       PRINT 'Phase 1: Adding new objects...';

       -- Add new tables
       IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'NewTable1')
       BEGIN
           CREATE TABLE dbo.NewTable1 (
               ID INT IDENTITY(1,1) NOT NULL,
               Name NVARCHAR(100) NOT NULL,
               CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
               CONSTRAINT PK_NewTable1 PRIMARY KEY CLUSTERED (ID)
           );
           PRINT '  ✓ Created table NewTable1';
       END

       -- Add new columns (nullable or with defaults)
       IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.Users') AND name = 'NewColumn')
       BEGIN
           ALTER TABLE dbo.Users
           ADD NewColumn NVARCHAR(50) NULL;
           PRINT '  ✓ Added column Users.NewColumn';
       END

       -- Add new indexes
       IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Users_NewColumn')
       BEGIN
           CREATE NONCLUSTERED INDEX IX_Users_NewColumn
           ON dbo.Users(NewColumn)
           INCLUDE (UserID, Email);
           PRINT '  ✓ Created index IX_Users_NewColumn';
       END

       PRINT 'Phase 1 complete.';

       -- ================================================================
       -- PHASE 2: MODIFY EXISTING OBJECTS (Potentially Breaking)
       -- ================================================================
       PRINT 'Phase 2: Modifying existing objects...';

       -- Alter column data types (widening is safe)
       ALTER TABLE dbo.Users
       ALTER COLUMN Email NVARCHAR(200) NOT NULL; -- Was NVARCHAR(100)
       PRINT '  ✓ Expanded Users.Email column';

       -- Add constraints (validate data first)
       IF NOT EXISTS (SELECT * FROM sys.key_constraints WHERE name = 'PK_UserSessions')
       BEGIN
           -- Check for duplicates first
           IF NOT EXISTS (
               SELECT SessionID, COUNT(*)
               FROM dbo.UserSessions
               GROUP BY SessionID
               HAVING COUNT(*) > 1
           )
           BEGIN
               ALTER TABLE dbo.UserSessions
               ADD CONSTRAINT PK_UserSessions PRIMARY KEY CLUSTERED (SessionID);
               PRINT '  ✓ Added primary key PK_UserSessions';
           END
           ELSE
           BEGIN
               RAISERROR('Cannot add PK: duplicate SessionID values exist', 16, 1);
           END
       END

       PRINT 'Phase 2 complete.';

       -- ================================================================
       -- PHASE 3: DATA MIGRATION (if required)
       -- ================================================================
       {data_migration_scripts_if_any}

       -- ================================================================
       -- PHASE 4: REMOVE OLD OBJECTS (Breaking - Do Last)
       -- ================================================================
       PRINT 'Phase 4: Removing deprecated objects...';

       -- Drop old columns (WARNING: Breaking change)
       IF EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.Users') AND name = 'OldColumn')
       BEGIN
           ALTER TABLE dbo.Users
           DROP COLUMN OldColumn;
           PRINT '  ✓ Dropped column Users.OldColumn';
       END

       -- Drop old tables (WARNING: Breaking change)
       IF EXISTS (SELECT * FROM sys.tables WHERE name = 'DeprecatedTable')
       BEGIN
           DROP TABLE dbo.DeprecatedTable;
           PRINT '  ✓ Dropped table DeprecatedTable';
       END

       PRINT 'Phase 4 complete.';

       -- ================================================================
       -- POST-MIGRATION VALIDATION
       -- ================================================================
       PRINT 'Running post-migration validation...';

       -- Verify critical tables exist
       IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
       BEGIN
           RAISERROR('Validation failed: Users table missing', 16, 1);
       END

       -- Verify row counts (example)
       DECLARE @UserCount INT;
       SELECT @UserCount = COUNT(*) FROM dbo.Users;
       IF @UserCount < 100 -- Expected minimum
       BEGIN
           RAISERROR('Validation failed: Unexpected row count in Users table', 16, 1);
       END

       PRINT 'Post-migration validation passed.';

       -- ================================================================
       -- COMMIT TRANSACTION
       -- ================================================================
       COMMIT TRANSACTION MigrationTransaction;
       PRINT '';
       PRINT '============================================';
       PRINT 'Migration completed successfully!';
       PRINT 'Database: ' + DB_NAME();
       PRINT 'Timestamp: ' + CAST(GETDATE() AS NVARCHAR(50));
       PRINT '============================================';

   END TRY
   BEGIN CATCH
       -- Rollback on any error
       IF @@TRANCOUNT > 0
           ROLLBACK TRANSACTION MigrationTransaction;

       -- Log error details
       DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
       DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
       DECLARE @ErrorState INT = ERROR_STATE();
       DECLARE @ErrorLine INT = ERROR_LINE();

       PRINT '';
       PRINT '============================================';
       PRINT 'MIGRATION FAILED!';
       PRINT '============================================';
       PRINT 'Error: ' + @ErrorMessage;
       PRINT 'Line: ' + CAST(@ErrorLine AS NVARCHAR(10));
       PRINT 'Severity: ' + CAST(@ErrorSeverity AS NVARCHAR(10));
       PRINT 'State: ' + CAST(@ErrorState AS NVARCHAR(10));
       PRINT '';
       PRINT 'Transaction has been rolled back.';
       PRINT 'Database is unchanged.';
       PRINT '============================================';

       -- Re-throw error
       RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
   END CATCH;
   GO
   ```

2. **Generate Rollback Script (rollback.sql)**

   **Script Structure**:
   ```sql
   /*
   ============================================================================
   Database Schema Rollback Script
   Reverts: {target_database} → {source_database}
   Generated: {timestamp}
   ============================================================================

   IMPORTANT:
   - This script reverts the forward migration
   - Data added after migration may be lost
   - Review carefully before execution
   - Take backup before rollback

   ============================================================================
   */

   SET NOCOUNT ON;
   SET XACT_ABORT ON;

   USE [{target_database}];
   GO

   BEGIN TRANSACTION RollbackTransaction;

   BEGIN TRY

       PRINT 'Starting rollback...';

       -- ================================================================
       -- PHASE 1: RESTORE REMOVED OBJECTS
       -- ================================================================
       PRINT 'Phase 1: Restoring removed objects...';

       -- Restore dropped tables
       IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'DeprecatedTable')
       BEGIN
           CREATE TABLE dbo.DeprecatedTable (
               -- Original structure
               ID INT PRIMARY KEY,
               Data NVARCHAR(100)
           );
           PRINT '  ✓ Restored table DeprecatedTable';
       END

       -- Restore dropped columns
       IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.Users') AND name = 'OldColumn')
       BEGIN
           ALTER TABLE dbo.Users
           ADD OldColumn VARCHAR(50) NULL;
           PRINT '  ✓ Restored column Users.OldColumn';
       END

       -- ================================================================
       -- PHASE 2: REVERT MODIFICATIONS
       -- ================================================================
       PRINT 'Phase 2: Reverting modifications...';

       -- Revert column data type changes
       ALTER TABLE dbo.Users
       ALTER COLUMN Email NVARCHAR(100) NOT NULL; -- Back to original size
       PRINT '  ✓ Reverted Users.Email column';

       -- ================================================================
       -- PHASE 3: REMOVE ADDED OBJECTS
       -- ================================================================
       PRINT 'Phase 3: Removing newly added objects...';

       -- Drop new indexes
       IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Users_NewColumn')
       BEGIN
           DROP INDEX IX_Users_NewColumn ON dbo.Users;
           PRINT '  ✓ Dropped index IX_Users_NewColumn';
       END

       -- Drop new columns
       IF EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.Users') AND name = 'NewColumn')
       BEGIN
           ALTER TABLE dbo.Users
           DROP COLUMN NewColumn;
           PRINT '  ✓ Dropped column Users.NewColumn';
       END

       -- Drop new tables
       IF EXISTS (SELECT * FROM sys.tables WHERE name = 'NewTable1')
       BEGIN
           DROP TABLE dbo.NewTable1;
           PRINT '  ✓ Dropped table NewTable1';
       END

       -- ================================================================
       -- COMMIT ROLLBACK
       -- ================================================================
       COMMIT TRANSACTION RollbackTransaction;
       PRINT '';
       PRINT '============================================';
       PRINT 'Rollback completed successfully!';
       PRINT 'Database: ' + DB_NAME();
       PRINT 'Timestamp: ' + CAST(GETDATE() AS NVARCHAR(50));
       PRINT '============================================';

   END TRY
   BEGIN CATCH
       IF @@TRANCOUNT > 0
           ROLLBACK TRANSACTION RollbackTransaction;

       DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
       PRINT 'ROLLBACK FAILED: ' + @ErrorMessage;

       RAISERROR(@ErrorMessage, 16, 1);
   END CATCH;
   GO
   ```

3. **Generate Pre-Migration Validation Script**

   ```sql
   -- Pre-migration checks
   -- Run this before executing migration

   -- Check 1: Verify database backups exist
   SELECT
       database_name,
       backup_finish_date,
       DATEDIFF(hour, backup_finish_date, GETDATE()) AS HoursSinceBackup
   FROM msdb.dbo.backupset
   WHERE database_name = '{target_database}'
       AND type = 'D' -- Full backup
   ORDER BY backup_finish_date DESC;
   -- Ensure recent backup exists (< 24 hours old)

   -- Check 2: Verify no active connections (for exclusive access migrations)
   SELECT
       session_id,
       login_name,
       program_name,
       status
   FROM sys.dm_exec_sessions
   WHERE database_id = DB_ID('{target_database}')
       AND session_id <> @@SPID;
   -- Should return 0 rows for safe migration

   -- Check 3: Verify disk space
   EXEC sp_spaceused;
   -- Ensure sufficient free space for migration

   -- Check 4: Verify SQL Server version
   SELECT
       SERVERPROPERTY('ProductVersion') AS Version,
       SERVERPROPERTY('ProductLevel') AS ServicePack,
       SERVERPROPERTY('Edition') AS Edition;
   -- Verify compatibility
   ```

4. **Generate Post-Migration Validation Script**

   ```sql
   -- Post-migration validation
   -- Run this after executing migration

   -- Check 1: Verify all expected tables exist
   SELECT name FROM sys.tables ORDER BY name;
   -- Manually verify against expected list

   -- Check 2: Verify row counts
   SELECT
       t.name AS TableName,
       SUM(p.rows) AS RowCount
   FROM sys.tables t
   JOIN sys.partitions p ON t.object_id = p.object_id
   WHERE p.index_id IN (0,1)
   GROUP BY t.name
   ORDER BY t.name;
   -- Compare against pre-migration counts

   -- Check 3: Verify constraints
   SELECT
       OBJECT_NAME(parent_object_id) AS TableName,
       name AS ConstraintName,
       type_desc AS ConstraintType
   FROM sys.objects
   WHERE type IN ('PK', 'F', 'C', 'UQ')
   ORDER BY TableName, ConstraintType;
   -- Ensure critical constraints exist

   -- Check 4: Check for invalid foreign keys
   DBCC CHECKCONSTRAINTS WITH ALL_CONSTRAINTS;
   -- Should return 0 rows (no violations)

   -- Check 5: Update statistics
   EXEC sp_updatestats;
   PRINT 'Statistics updated.';
   ```

**Success Criteria**:
- Forward migration script generated with all changes
- Rollback script generated with reverse changes
- Scripts include transaction handling and error catching
- Validation scripts provided for pre/post migration
- Scripts are executable and well-commented

**Error Handling**:
- Complex transformations: Include detailed comments
- Conditional logic: Use IF EXISTS checks extensively
- Large operations: Include progress PRINT statements

**Tools Used**: Write (save all scripts to report)

---

### Phase 6: Report Compilation and Delivery

**Objective**: Compile all analysis into comprehensive migration plan report with scripts and checklists.

**Steps**:

1. **Compile Executive Summary**
   - Migration type (major/minor/patch)
   - Risk level (high/medium/low)
   - Breaking changes count
   - New/modified/deleted objects count
   - Data migration required (yes/no)
   - Estimated downtime
   - Recommended approach

2. **Compile Detailed Sections**
   - Migration overview
   - Breaking changes (detailed list)
   - Schema comparison (new/modified/deleted objects)
   - Compatibility assessment
   - Data migration strategy
   - Migration scripts (forward/rollback)
   - Pre-migration checklist
   - Deployment plan
   - Post-migration validation checklist
   - Rollback plan
   - Risk assessment
   - Recommendations

3. **Embed Scripts in Report**
   - Include full migration script in code block
   - Include full rollback script in code block
   - Include validation scripts
   - Provide download links or file paths if scripts are separate files

4. **Create Deployment Checklist**

   ```markdown
   ### Pre-Deployment Checklist

   #### 1-2 Weeks Before
   - [ ] Review migration plan with team
   - [ ] Test migration in development environment
   - [ ] Test migration in staging environment
   - [ ] Perform load testing on migrated schema
   - [ ] Update application code for breaking changes
   - [ ] Schedule maintenance window
   - [ ] Notify stakeholders of downtime

   #### 1 Day Before
   - [ ] Verify latest database backup
   - [ ] Test backup restoration procedure
   - [ ] Prepare rollback plan
   - [ ] Review migration script line-by-line
   - [ ] Verify monitoring/alerting is active

   #### Migration Day (2 hours before)
   - [ ] Final database backup
   - [ ] Verify backup file integrity
   - [ ] Put application in maintenance mode
   - [ ] Clear application cache
   - [ ] Stop background jobs

   #### Migration Execution
   - [ ] Run pre-migration validation script
   - [ ] Execute forward migration script
   - [ ] Monitor for errors
   - [ ] Run post-migration validation script
   - [ ] Verify row counts match
   - [ ] Check constraint violations
   - [ ] Test database connectivity

   #### Post-Migration (within 1 hour)
   - [ ] Start application
   - [ ] Run smoke tests
   - [ ] Monitor application logs for errors
   - [ ] Verify critical user workflows
   - [ ] Monitor performance metrics
   - [ ] Remove maintenance mode

   #### Post-Migration (within 24 hours)
   - [ ] Monitor for unexpected errors
   - [ ] Gather user feedback
   - [ ] Document lessons learned
   - [ ] Archive migration artifacts
   - [ ] Update documentation
   ```

5. **Create Rollback Decision Matrix**

   ```markdown
   ### When to Rollback

   | Scenario | Severity | Action | Rollback? |
   |----------|----------|--------|-----------|
   | Migration script fails | Critical | Execute rollback immediately | Yes |
   | Application won't start | Critical | Execute rollback immediately | Yes |
   | Data integrity violations found | Critical | Execute rollback immediately | Yes |
   | Performance degradation >50% | High | Investigate, rollback if not fixed in 1 hour | Likely |
   | Unexpected errors in logs | Medium | Monitor, rollback if errors increase | Maybe |
   | Minor UI issues | Low | Fix forward, no rollback | No |

   ### Rollback Window
   - **Immediate Rollback** (0-1 hour after migration): Full rollback possible with minimal data loss
   - **Delayed Rollback** (1-24 hours): Rollback possible but may lose data entered after migration
   - **Late Rollback** (>24 hours): Rollback not recommended, fix forward instead
   ```

6. **Add Recommendations Section**

   Provide specific, actionable recommendations:
   - Recommended migration approach (blue-green, incremental, offline)
   - Optimal maintenance window timing
   - Application code changes needed before migration
   - Database configuration changes recommended
   - Monitoring and alerting setup
   - Performance optimization post-migration

7. **Format and Save Report**
   - Apply markdown formatting
   - Use tables for structured data
   - Use code blocks for SQL scripts
   - Use bullet points and numbered lists
   - Add horizontal rules for section separation
   - Save to: `marketplace/output/schema-analysis/migration-plan-{source}-to-{target}-{timestamp}.md`

8. **Generate Success Message**

   ```
   Schema migration plan generated successfully!

   Source: {source_database}
   Target: {target_database}

   Report: output/schema-analysis/migration-plan-{source}-to-{target}-{timestamp}.md

   Summary:
   - Migration Type: {major/minor/patch}
   - Risk Level: {high/medium/low}
   - Breaking Changes: {count}
   - New Objects: {count}
   - Modified Objects: {count}
   - Deleted Objects: {count}
   - Data Migration: {required/not required}
   - Estimated Downtime: {duration}

   Critical Actions Required:
   1. {action_1}
   2. {action_2}
   3. {action_3}

   Next Steps:
   1. Review full migration plan in detail
   2. Test migration scripts in development environment
   3. Update application code for breaking changes
   4. Schedule maintenance window
   5. Execute migration following deployment checklist

   IMPORTANT: Do not execute migration scripts without thorough testing!
   ```

**Success Criteria**:
- Complete report generated with all sections
- Scripts embedded and formatted correctly
- Checklists are comprehensive and actionable
- Recommendations are specific to this migration
- User is informed of next steps

**Error Handling**:
- Report too large: Split into multiple files (summary + detailed analysis + scripts)
- Formatting issues: Fall back to plain text if needed

**Tools Used**: Write (save report), Bash (file operations)

---

## Error Handling

### Database Connection Errors

**Error**: "Cannot connect to source/target database"

**Recovery**:
1. Verify MCP server connection
2. Check database exists: `SELECT name FROM sys.databases`
3. Verify network connectivity if databases on different servers
4. Check SQL Server authentication/permissions
5. Provide troubleshooting guide in error message

### Permission Errors

**Error**: "Insufficient permissions to compare schemas"

**Recovery**:
1. List current permissions for user
2. Provide script to grant required permissions:
   ```sql
   GRANT VIEW DEFINITION ON DATABASE::[DatabaseName] TO [UserName];
   ```
3. Note that VIEW DEFINITION is minimum required
4. For data analysis, also need SELECT permission

### Schema Extraction Errors

**Error**: "Timeout during metadata extraction"

**Recovery**:
1. Extract metadata in smaller chunks (tables first, then indexes, then constraints)
2. Provide partial comparison with note about incompleteness
3. Suggest running during low-usage period
4. Offer to continue with available data

### Comparison Errors

**Error**: "Ambiguous schema differences"

**Recovery**:
1. Document assumptions made during comparison
2. Flag ambiguous cases for manual review
3. Provide multiple interpretation options
4. Ask user for clarification when critical

### Script Generation Errors

**Error**: "Cannot generate script for complex transformation"

**Recovery**:
1. Provide manual procedure instead of script
2. Break down into smaller steps
3. Offer multiple implementation approaches
4. Document what was attempted and why it failed

## Examples

### Example 1: Simple Version Upgrade

**Input**:
```bash
/plan-schema-migration ProductionDB_v1 ProductionDB_v2 --generate-scripts
```

**Scenario**: Minor version upgrade with few changes

**Changes Detected**:
- 2 new tables added
- 5 new columns added (all nullable)
- 3 new indexes added
- 1 stored procedure modified

**Assessment**:
- Migration Type: Minor
- Breaking Changes: 0
- Risk Level: Low
- Estimated Downtime: 5 minutes

**Output Summary**:
```markdown
# Schema Migration Plan
## ProductionDB_v1 → ProductionDB_v2

### Executive Summary
- **Migration Type**: Minor (non-breaking changes)
- **Risk Level**: Low
- **Breaking Changes**: 0
- **New Objects**: 10 (2 tables, 5 columns, 3 indexes)
- **Modified Objects**: 1 (stored procedure)
- **Data Migration**: Not required
- **Estimated Downtime**: 5 minutes
- **Recommended Approach**: Direct migration (single transaction)

### Key Changes
1. Added CustomerPreferences table for storing user settings
2. Added Products.CategoryID column (nullable) for better categorization
3. Added indexes for improved query performance
4. Updated GetCustomerOrders procedure to include new columns

### Recommendations
- **Low Risk**: All changes are additions, no deletions or modifications
- **No Breaking Changes**: Existing applications will continue to work
- **Quick Migration**: Execute during regular maintenance window
- **No Rollback Needed**: Additions can stay even if issues arise

### Migration Script
[Embedded SQL script with CREATE TABLE, ALTER TABLE, CREATE INDEX statements]

### Deployment Steps
1. Take database backup
2. Execute migration script (5 minutes)
3. Verify objects created
4. Resume application

[Complete report continues...]
```

---

### Example 2: Major Refactoring with Breaking Changes

**Input**:
```bash
/plan-schema-migration LegacyDB RefactoredDB --analyze-data --generate-scripts --check-compatibility
```

**Scenario**: Major schema refactoring with normalization

**Changes Detected**:
- 3 tables deleted (merged into other tables)
- 12 columns deleted (denormalized)
- 5 new tables added (normalization)
- 8 columns modified (data type changes)
- 15 new foreign keys added

**Assessment**:
- Migration Type: Major
- Breaking Changes: 15
- Risk Level: High
- Estimated Downtime: 2 hours

**Output Summary**:
```markdown
# Schema Migration Plan
## LegacyDB → RefactoredDB

### Executive Summary
- **Migration Type**: MAJOR (significant schema refactoring)
- **Risk Level**: HIGH
- **Breaking Changes**: 15 (3 deleted tables, 12 deleted columns)
- **New Objects**: 35
- **Modified Objects**: 18
- **Data Migration**: REQUIRED (complex transformations)
- **Estimated Downtime**: 2 hours
- **Recommended Approach**: Blue-Green Deployment with dual-write

### CRITICAL BREAKING CHANGES

#### 1. Deleted Table: UserAddresses
- **Impact**: Application directly queries this table
- **Reason**: Merged into Users table with 1:M relationship via new Addresses table
- **Data Migration**: Move data to Users + Addresses tables
- **Application Changes**: Update queries from UserAddresses to JOIN Users with Addresses
- **Mitigation**: Create compatibility view named UserAddresses during transition period

#### 2. Deleted Column: Orders.CustomerName
- **Impact**: Reports and exports use this column
- **Reason**: Denormalized data, proper data is in Customers.Name
- **Data Migration**: None (data still available via FK to Customers table)
- **Application Changes**: Change SELECT CustomerName to SELECT c.Name in all queries
- **Mitigation**: Add computed column CustomerName = (SELECT Name FROM Customers WHERE...)

[... 13 more breaking changes detailed ...]

### Compatibility Assessment

**Backward Compatibility**: NO - Breaking changes require application updates

**Application Impact**:
- **OrderService**: Must update 8 queries to use new schema
- **ReportingAPI**: Must update 12 reports to use new columns
- **CustomerPortal**: Must update 3 views to use new Addresses table

**Minimum Application Version**: 2.0.0 (requires code changes)

**Runtime Errors Expected**: Yes, if old application runs against new schema
- UserAddresses table not found
- Orders.CustomerName column not found
- Data type mismatch errors

### Data Migration Strategy

**Approach**: ETL (Extract, Transform, Load)

**Duration**: Estimated 90 minutes for 5M rows

**Transformations Required**:

1. **Split UserAddresses table**:
```sql
-- Migrate user data
INSERT INTO RefactoredDB.dbo.Users (UserID, Name, Email)
SELECT UserID, UserName, Email
FROM LegacyDB.dbo.UserAddresses;

-- Migrate addresses to separate table
INSERT INTO RefactoredDB.dbo.Addresses (UserID, Street, City, State, ZipCode)
SELECT UserID, StreetAddress, City, State, Zip
FROM LegacyDB.dbo.UserAddresses;
```

2. **Convert Orders.TotalAmount from VARCHAR to DECIMAL**:
```sql
-- Migrate valid data
INSERT INTO RefactoredDB.dbo.Orders (OrderID, TotalAmount)
SELECT
    OrderID,
    CAST(REPLACE(TotalAmount, '$', '') AS DECIMAL(18,2))
FROM LegacyDB.dbo.Orders
WHERE ISNUMERIC(REPLACE(TotalAmount, '$', '')) = 1;

-- Log invalid data for manual review
INSERT INTO RefactoredDB.dbo.DataMigrationErrors (Table, Column, Value, Reason)
SELECT
    'Orders', 'TotalAmount', TotalAmount, 'Invalid numeric format'
FROM LegacyDB.dbo.Orders
WHERE ISNUMERIC(REPLACE(TotalAmount, '$', '')) = 0;
```

[... more transformations ...]

### Recommended Migration Approach: Blue-Green Deployment

**Why Blue-Green?**
- Minimizes downtime (near-zero)
- Full rollback capability
- Allows testing with production data before cutover
- Reduces risk for high-impact migration

**Steps**:

1. **Phase 1 - Preparation (1 week)**:
   - Deploy RefactoredDB as separate database
   - Implement dual-write in application (write to both LegacyDB and RefactoredDB)
   - Deploy application v2.0 behind feature flag (disabled)

2. **Phase 2 - Data Sync (2 days)**:
   - Run initial data migration (historical data)
   - Verify data integrity
   - Monitor dual-write performance

3. **Phase 3 - Cutover (10 minutes)**:
   - Enable feature flag (switch reads to RefactoredDB)
   - Monitor for errors
   - If issues, disable feature flag (instant rollback)

4. **Phase 4 - Cleanup (1 week later)**:
   - Stop writing to LegacyDB
   - Archive LegacyDB
   - Remove dual-write code

**Benefits**: Zero downtime, instant rollback, gradual transition

### Migration Scripts

#### Forward Migration Script (deploy.sql)
[Embedded 500-line SQL script with all schema changes]

#### Rollback Script (rollback.sql)
[Embedded rollback script - NOTE: Data added to RefactoredDB will be lost]

#### Data Migration Script (migrate_data.sql)
[Embedded ETL script with all transformations]

### Deployment Checklist

[Comprehensive 50-item checklist covering pre-migration, execution, validation, and post-migration]

### Rollback Plan

**Rollback Window**: 48 hours (after this, too much new data to rollback)

**Rollback Trigger Conditions**:
- Migration script fails completely
- Data integrity violations >1%
- Application errors >5% of requests
- Performance degradation >50%
- Critical functionality broken

**Rollback Steps**:
1. Disable feature flag (switch back to LegacyDB)
2. Stop dual-write to RefactoredDB
3. Verify application is working with LegacyDB
4. Investigate and fix issues
5. Retry migration at later date

**Data Recovery**:
- Data entered during RefactoredDB live time will need to be manually migrated back to LegacyDB (dual-write handles most)
- Provide script to extract and merge data

### Risk Assessment

**HIGH RISKS**:
1. **Data Migration Failures** (20% probability)
   - Mitigation: Extensive testing in staging, have DBA on standby
2. **Application Compatibility** (40% probability)
   - Mitigation: Thorough code review, integration testing
3. **Performance Degradation** (15% probability)
   - Mitigation: Load testing, index optimization

**MEDIUM RISKS**:
1. **Extended Downtime** (30% probability)
   - Mitigation: Blue-green deployment eliminates downtime
2. **Rollback Needed** (25% probability)
   - Mitigation: Feature flag allows instant rollback

### Recommendations

1. **DO NOT attempt direct migration** - Risk too high for production
2. **Use Blue-Green Deployment** - Only safe approach for this scale of changes
3. **Update Application First** - Deploy v2.0 with feature flag BEFORE migration
4. **Test Exhaustively** - Run full migration in staging 3+ times
5. **Have DBA Available** - 24/7 coverage during transition period
6. **Monitor Closely** - Enhanced monitoring for 1 week post-migration
7. **Document Everything** - Full audit trail for compliance

### Timeline

- Week 1: Application v2.0 development and deployment
- Week 2: Staging testing and dual-write implementation
- Week 3: Initial data migration and validation
- Week 4: Production cutover (low-traffic period)
- Week 5: Monitoring and gradual transition
- Week 6: Cleanup and documentation

**Total Timeline**: 6 weeks (not including rollback if needed)

[Complete report continues with appendices...]
```

---

## Success Metrics

### Quantitative Metrics

1. **Comparison Completeness**: 100% of objects compared between source and target
2. **Breaking Change Detection Accuracy**: >95% of breaking changes identified
3. **Script Generation Success**: Executable scripts generated for all changes
4. **Execution Time**: <20 minutes for databases with <200 tables

### Qualitative Metrics

1. **Actionability**: User can execute migration following the plan
2. **Clarity**: Non-technical stakeholders understand risks and approach
3. **Completeness**: All necessary information provided (no gaps requiring additional research)
4. **Safety**: Rollback plan is clear and executable

### User Validation

1. User successfully tests migration in development environment
2. Migration scripts execute without errors
3. User identifies all application code needing updates
4. User feels confident executing migration in production

## Dependencies

### Required
- **MSSQL MCP Server**: For connecting to SQL Server and querying system catalogs
- **Bash Tool**: For executing MCP queries
- **Write Tool**: For generating migration plan report and scripts

### Optional
- **Read Tool**: For referencing migration patterns and best practices
- **Grep/Glob Tools**: For searching related application code (if analyzing codebase)

## Version History

- **2.0.0** (2026-01-16): Initial release with comprehensive migration planning
  - Source and target schema comparison
  - Breaking change detection and analysis
  - Data migration strategy generation
  - T-SQL script generation (forward and rollback)
  - Blue-green and incremental deployment support
  - Comprehensive deployment checklists

## Notes

- This agent focuses on **planning** migrations, not executing them. Scripts must be reviewed and executed by user.
- For analysis of a single schema (not comparing two), use `schema-structure-analyzer` agent.
- For normalization analysis, use `normalization-advisor` agent.
- For relationship analysis, use `foreign-key-analyzer` agent.
- Large migrations (>500 tables) may require extended analysis time.
- Always test migration in non-production environment first.
- Keep MCP connection active throughout analysis (may take 10-20 minutes for large databases).
