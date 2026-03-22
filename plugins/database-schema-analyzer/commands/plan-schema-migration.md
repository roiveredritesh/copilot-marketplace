---
command_name: plan-schema-migration
version: 2.0.0
description: Plan database schema migration from source to target version with migration scripts and rollback plans
delegated_to: schema-migration-planner
requires_mcp: true
async_capable: true
---

# /plan-schema-migration Command

## Overview

The `/plan-schema-migration` command automates the planning and strategy development for database schema migrations. It compares source and target database schemas, identifies all differences, detects breaking changes, analyzes data migration requirements, generates executable T-SQL migration scripts, creates rollback procedures, and provides comprehensive deployment checklists. This command is essential for safe, repeatable database version upgrades and schema evolution.

## Syntax

```bash
/plan-schema-migration <source-db> <target-db> [--analyze-data] [--generate-scripts] [--check-compatibility]
```

## Parameters

### Required

- **source-db** (string): Name of the source/current database
  - Represents the "before" state
  - Must be accessible via MSSQL MCP server
  - Example: `MyDB_v1`, `ProductionDB`, `LegacyDB`

- **target-db** (string): Name of the target/new database
  - Represents the "after" state
  - Must be accessible via MSSQL MCP server
  - Can be on same server or different server (if MCP configured)
  - Example: `MyDB_v2`, `ProductionDB_NextVersion`, `RefactoredDB`

### Optional Flags

#### --analyze-data

Includes data migration analysis by sampling data from both databases.

**What it does**:
- Analyzes sample data to detect transformation needs
- Checks data type compatibility (actual data vs target schema)
- Identifies potential data loss scenarios (e.g., varchar(100) → varchar(50))
- Estimates data migration duration
- Generates data validation queries

**When to use**:
- Schema changes involve column data type changes
- Tables are being split or merged
- Data transformations are needed (e.g., string to numeric)
- Ensuring no data loss during migration

**Example**:
```bash
/plan-schema-migration MyDB_v1 MyDB_v2 --analyze-data
```

---

#### --generate-scripts

Generates executable T-SQL migration scripts (default: enabled).

**What it generates**:
- **Forward migration script** (deploy.sql): All schema changes
- **Rollback script** (rollback.sql): Reverses all changes
- **Pre-migration validation script**: Checks before running migration
- **Post-migration validation script**: Verifies migration success
- **Data migration scripts** (if needed): ETL transformations

**Features**:
- Transaction handling (ROLLBACK on error)
- Error handling (TRY/CATCH blocks)
- Progress logging (PRINT statements)
- Validation checks (data integrity, row counts)

**Example**:
```bash
/plan-schema-migration CurrentDB NewDB --generate-scripts
```

---

#### --check-compatibility

Performs backward compatibility analysis (default: enabled).

**What it checks**:
- Breaking changes (deleted tables/columns)
- Data type changes that may break applications
- Stored procedure signature changes
- View definition changes
- Application impact assessment

**Output**:
- List of breaking changes with severity
- Affected application components (estimated)
- Minimum application version required post-migration
- Runtime errors expected if old code runs on new schema

**Example**:
```bash
/plan-schema-migration OldDB NewDB --check-compatibility
```

---

## Usage Examples

### Example 1: Basic Migration Plan

```bash
/plan-schema-migration MyDB_v1 MyDB_v2
```

**Scenario**: Planning a minor version upgrade with few changes.

**What happens**:
1. Compares schemas of MyDB_v1 and MyDB_v2
2. Identifies new, modified, and deleted objects
3. Detects breaking changes
4. Generates migration scripts (forward and rollback)
5. Checks backward compatibility (default enabled)
6. Creates deployment checklist

**Output**: `marketplace/marketplace/output/schema-analysis/migration-plan-MyDB_v1-to-MyDB_v2-{timestamp}.md`

---

### Example 2: Full Migration with Data Analysis

```bash
/plan-schema-migration ProductionDB ProductionDB_NextVersion --analyze-data --generate-scripts
```

**Scenario**: Major migration involving schema changes that affect data.

**What happens**:
1. Full schema comparison
2. Samples data from both databases to check compatibility
3. Identifies data transformations needed
4. Estimates data migration duration
5. Generates schema migration scripts
6. Generates data migration scripts
7. Creates validation queries

**Use case**: When columns are changing data types or tables are being split/merged.

---

### Example 3: Compatibility-Focused Analysis

```bash
/plan-schema-migration CurrentDB ProposedDB --check-compatibility
```

**Scenario**: Assessing impact of proposed schema changes before implementation.

**What happens**:
1. Schema comparison focusing on breaking changes
2. Detailed compatibility assessment
3. Application impact analysis
4. Minimum application version determination
5. Runtime error prediction

**Use case**: Pre-approval review to understand risks and required application changes.

---

### Example 4: Simple Migration (No Data Analysis)

```bash
/plan-schema-migration DevDB StagingDB --generate-scripts
```

**Scenario**: Quick migration between environments with identical data.

**What happens**:
1. Schema-only comparison (no data sampling)
2. Migration script generation
3. Basic compatibility check
4. Deployment plan

**Use case**: Promoting schema changes from dev to staging (data already migrated separately).

---

## What Gets Analyzed

### Schema Comparison

**Tables**:
- New tables (added in target)
- Deleted tables (removed from source)
- Modified tables (structural changes)

**Columns**:
- New columns (nullable/with default = non-breaking, NOT NULL without default = breaking)
- Deleted columns (breaking change)
- Modified columns (data type, length, nullability, defaults)
- Renamed columns (appears as delete + add)

**Indexes**:
- New indexes (performance improvement)
- Deleted indexes (potential performance regression)
- Modified indexes (different columns or properties)

**Constraints**:
- New constraints (may fail if existing data violates)
- Deleted constraints (reduces data integrity enforcement)
- Modified constraints (e.g., changed cascade rules)

**Stored Procedures, Functions, Views, Triggers**:
- New objects (non-breaking)
- Deleted objects (breaking if application uses them)
- Modified objects (may be breaking if signatures change)

### Breaking Change Detection

The command identifies and categorizes breaking changes:

**Critical Breaking Changes**:
- Deleted tables
- Deleted columns
- Column data type narrowing (e.g., varchar(100) → varchar(50))
- NOT NULL constraint added without default value
- Deleted stored procedures/functions (if application calls them)
- Parameter changes in stored procedures

**High-Risk Changes**:
- Modified column data types (widening usually safe, narrowing risky)
- New constraints on existing tables (may fail if data violates)
- Modified constraint cascade rules
- Modified stored procedure logic

**Medium-Risk Changes**:
- New NOT NULL columns without defaults
- Deleted indexes (performance impact)
- Modified indexes

**Low-Risk Changes**:
- New tables
- New nullable columns or columns with defaults
- New indexes
- New stored procedures

### Data Migration Analysis (if --analyze-data)

**Data Compatibility Checks**:
- Verify data fits in new data types (e.g., no truncation)
- Identify records that violate new constraints
- Detect NULL values in columns that will become NOT NULL
- Check referential integrity for new foreign keys

**Transformation Requirements**:
- Column mapping (old columns → new columns)
- Data type conversions (string → numeric, date format changes)
- Data cleaning (trim, uppercase, standardize formats)
- Calculated/derived values for new columns
- Default values for new required columns

**Estimates**:
- Total rows to migrate
- Estimated migration duration
- Storage requirements

## Output Report Structure

### Executive Summary
- Migration type (major/minor/patch)
- Risk level (high/medium/low)
- Breaking changes count
- New/modified/deleted objects count
- Data migration required (yes/no)
- Estimated downtime
- Recommended approach (blue-green/incremental/offline)

### Breaking Changes (CRITICAL)
Detailed list of each breaking change with:
- Change description
- Impact on applications
- Affected application components
- Mitigation strategy
- Prerequisites before migration

### Schema Comparison
- **New Objects**: List of additions
- **Modified Objects**: List of changes with before/after comparison
- **Deleted Objects**: List of deletions with data preservation strategy

### Data Migration Strategy (if --analyze-data)
- Migration approach (in-place, ETL, dual-write, staged)
- Data transformations required
- Estimated duration
- Validation queries
- Rollback capability assessment

### Migration Scripts

**Forward Migration Script** (deploy.sql):
```sql
-- Complete T-SQL script with:
-- - Transaction handling
-- - Error handling (TRY/CATCH)
-- - Pre-migration validation
-- - Schema changes (phased: add first, modify next, delete last)
-- - Data migration (if needed)
-- - Post-migration validation
```

**Rollback Script** (rollback.sql):
```sql
-- Complete T-SQL script to reverse changes
-- NOTE: Data added after migration may be lost
```

### Deployment Plan

**Phase-by-Phase Checklist**:
- Pre-deployment (1-2 weeks before)
- Day before deployment
- Migration day (2 hours before)
- Migration execution
- Post-migration validation (within 1 hour)
- Monitoring (within 24 hours)

### Rollback Plan
- Rollback window (time period where rollback is safe)
- Rollback trigger conditions (when to rollback)
- Rollback steps
- Data recovery strategy

### Compatibility Assessment (if --check-compatibility)
- Can existing applications work without changes? (Yes/No/Partially)
- Minimum application version required
- Expected runtime errors
- Query compatibility analysis
- Deployment approach recommendations (zero-downtime possible?)

### Risk Assessment
- High/Medium/Low risks with descriptions
- Mitigation strategies for each risk
- Overall risk level with justification

### Recommendations
- Recommended migration approach (blue-green, incremental, offline)
- Optimal maintenance window timing
- Application code changes required
- Database configuration recommendations
- Monitoring and alerting setup

## Migration Strategies

The command recommends one of these strategies based on analysis:

### Offline Migration (Direct)
**When**: Non-breaking changes, small database, acceptable downtime

**Process**:
1. Put application in maintenance mode
2. Execute migration script
3. Validate
4. Resume application

**Downtime**: Minutes to hours
**Rollback**: Execute rollback script

---

### Blue-Green Deployment
**When**: Breaking changes, zero-downtime required, high-availability system

**Process**:
1. Deploy target schema to separate database (green)
2. Implement dual-write (write to both blue and green)
3. Migrate historical data to green
4. Cutover (switch reads to green)
5. Decommission blue after monitoring period

**Downtime**: Zero (or seconds for cutover)
**Rollback**: Switch back to blue database

---

### Incremental Migration (Expand-Contract)
**When**: Breaking changes, gradual transition preferred

**Process**:
1. **Expand**: Add new structures (non-breaking)
2. **Dual-Write**: Write to old and new structures
3. **Migrate**: Migrate historical data
4. **Switch Reads**: Change application to read from new structures
5. **Contract**: Remove old structures

**Downtime**: Zero
**Rollback**: Reverse each phase

---

### Staged Migration
**When**: Very large database (>1TB), high-risk migration

**Process**:
1. Migrate 10% of data, validate
2. Migrate 50% of data, validate
3. Migrate remaining data
4. Final validation

**Downtime**: Varies
**Rollback**: Depends on stage

---

## Prerequisites

### MCP Configuration

MSSQL MCP server must be configured with access to both source and target databases:

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

Database user must have:
- `VIEW DEFINITION` permission on both source and target databases
- `SELECT` permission (if using --analyze-data)

```sql
USE [SourceDB];
GRANT VIEW DEFINITION TO [UserName];

USE [TargetDB];
GRANT VIEW DEFINITION TO [UserName];
```

## Error Handling

### Common Errors

**Error: "Cannot access source/target database"**
- Verify database names are correct
- Check MCP connection
- Ensure databases are online
- Verify user has access to both databases

**Error: "Timeout during schema comparison"**
- Databases too large (>500 tables)
- Run during low-usage period
- Use component-specific analysis if available
- Increase timeout in plugin configuration

**Error: "Cannot generate migration script"**
- Complex transformation may require manual intervention
- Review report for partial script
- Consult DBA for complex scenarios

## Performance Considerations

**Typical Execution Times**:
- **Simple Migration** (few changes): 5-10 minutes
- **Complex Migration** (many changes): 10-20 minutes
- **With Data Analysis**: +5-10 minutes

**Factors Affecting Duration**:
- Number of tables in databases
- Complexity of schema differences
- Data sampling (if --analyze-data used)
- Network latency (if databases on different servers)

## Tips and Best Practices

1. **Always Test in Development First**: Run migration in dev/staging before production
2. **Review Scripts Thoroughly**: Never execute generated scripts blindly
3. **Take Full Backup**: Always backup before migration
4. **Test Rollback**: Verify rollback script works in test environment
5. **Monitor Closely**: Enhanced monitoring during and after migration
6. **Plan Maintenance Window**: Schedule during low-traffic period
7. **Communicate**: Notify stakeholders of downtime and risks
8. **Have DBA on Standby**: Expert available during migration execution
9. **Use Feature Flags**: Deploy application code with feature flags before schema migration
10. **Document Everything**: Keep migration report and execution log for audit trail

## Integration with Other Commands

### Pre-Migration Workflow

```bash
# Step 1: Analyze source database health
/analyze-schema SourceDB

# Step 2: Analyze target database health
/analyze-schema TargetDB

# Step 3: Plan migration
/plan-schema-migration SourceDB TargetDB --analyze-data --generate-scripts

# Step 4: Review relationships in both databases
/analyze-relationships SourceDB
/analyze-relationships TargetDB
```

## Related Commands

- **`/analyze-schema`**: Analyze individual database schema structure
- **`/suggest-normalization`**: Validate normalization in target schema
- **`/analyze-relationships`**: Understand FK dependencies before migration

## Output Location

Migration plans are saved to:
```
marketplace/output/schema-analysis/migration-plan-{source}-to-{target}-{timestamp}.md
```

Example:
```
marketplace/output/schema-analysis/migration-plan-MyDB_v1-to-MyDB_v2-20260116-143022.md
```

## Version History

- **2.0.0** (2026-01-16): Initial release
  - Schema comparison and difference detection
  - Breaking change analysis
  - Data migration strategy generation
  - T-SQL script generation (forward and rollback)
  - Blue-green and incremental deployment support
  - Comprehensive deployment checklists

## Support

For issues or questions:
1. Check [README.md](../README.md) for troubleshooting
2. Review agent specification: [schema-migration-planner.md](../agents/schema-migration-planner.md)
3. Verify MCP configuration and permissions
4. Consult DBA for complex migration scenarios

---

**Command Type**: Planning/Analysis
**Delegation**: This command delegates to the `schema-migration-planner` agent
**MCP Required**: Yes (MSSQL with access to both databases)
**Async Capable**: Yes
**Estimated Duration**: 10-20 minutes (complex migrations)
