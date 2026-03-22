---
command_name: suggest-normalization
version: 2.0.0
description: Analyze table normalization and suggest improvements for better database design
delegated_to: normalization-advisor
requires_mcp: true
async_capable: true
---

# /suggest-normalization Command

## Overview

The `/suggest-normalization` command analyzes database table structures to determine their current normalization form (1NF through 5NF) and provides specific, actionable recommendations for achieving higher normalization levels. It detects data redundancy, update anomalies, insert anomalies, delete anomalies, transitive dependencies, and multi-valued dependencies. The command also evaluates denormalization trade-offs for performance optimization scenarios.

This command is essential for ensuring data integrity, reducing redundancy, improving maintainability, and making informed decisions about when denormalization is appropriate.

## Syntax

```bash
/suggest-normalization <database-name>.<table-name> [--form=1NF|2NF|3NF|BCNF|4NF|5NF] [--include-denorm]
```

## Parameters

### Required

- **database-name.table-name** (string): Fully qualified table name
  - Format: `DatabaseName.SchemaName.TableName` OR `DatabaseName.TableName` (dbo schema assumed)
  - Must be accessible via MSSQL MCP server
  - Examples:
    - `MyDatabase.dbo.Users`
    - `MyDatabase.Users` (assumes dbo schema)
    - `ProductionDB.sales.Orders`

### Optional Flags

#### --form

Specifies the target normalization form to analyze toward.

**Values**:
- `1NF`: First Normal Form (atomic values, no repeating groups, PK exists)
- `2NF`: Second Normal Form (no partial dependencies)
- `3NF`: Third Normal Form (no transitive dependencies) - **default**
- `BCNF`: Boyce-Codd Normal Form (every determinant is a candidate key)
- `4NF`: Fourth Normal Form (no multi-valued dependencies)
- `5NF`: Fifth Normal Form (no join dependencies)

**Recommendation**: Use `3NF` for most practical applications. Higher forms (4NF, 5NF) are rarely needed.

**Examples**:
```bash
/suggest-normalization MyDatabase.Users
/suggest-normalization MyDatabase.Orders --form=3NF
/suggest-normalization MyDatabase.Products --form=BCNF
```

---

#### --include-denorm

Includes denormalization recommendations and trade-off analysis.

**What it does**:
- Analyzes scenarios where denormalization may improve performance
- Provides trade-off analysis (performance vs data integrity)
- Suggests appropriate denormalization strategies (redundant columns, computed columns, summary tables, materialized views)
- Evaluates when denormalization is beneficial and when it's risky

**When to use**:
- Performance optimization for read-heavy workloads
- Preparing data warehouse/reporting database
- Investigating slow queries caused by complex joins
- Evaluating trade-offs between speed and integrity

**Example**:
```bash
/suggest-normalization MyDatabase.Orders --include-denorm
```

---

## Usage Examples

### Example 1: Basic Normalization Analysis (3NF)

```bash
/suggest-normalization MyDatabase.Users
```

**Scenario**: Validating that the Users table follows normalization best practices.

**What happens**:
1. Analyzes table structure (columns, data types, PK, FKs)
2. Checks compliance with 1NF, 2NF, and 3NF
3. Detects violations (repeating columns, partial dependencies, transitive dependencies)
4. Provides refactoring recommendations with SQL scripts
5. Estimates benefits (reduced redundancy, eliminated anomalies)

**Output**: `marketplace/marketplace/output/schema-analysis/normalization-Users-{timestamp}.md`

---

### Example 2: Target Specific Normalization Form

```bash
/suggest-normalization MyDatabase.Orders --form=BCNF
```

**Scenario**: Aiming for Boyce-Codd Normal Form (stricter than 3NF).

**What happens**:
1. Analyzes through all forms up to BCNF
2. Identifies determinants that are not candidate keys
3. Provides recommendations to achieve BCNF
4. Explains trade-offs (BCNF may require more tables than 3NF)

**Use case**: When data integrity is paramount and performance is less critical.

---

### Example 3: Include Denormalization Options

```bash
/suggest-normalization MyDatabase.Products --form=3NF --include-denorm
```

**Scenario**: Table is normalized, but queries are slow due to complex joins.

**What happens**:
1. Validates current normalization (assuming 3NF compliant)
2. Analyzes query patterns (if possible)
3. Suggests strategic denormalization options:
   - Add redundant columns for frequently joined data
   - Create computed columns for calculations
   - Create summary/aggregation tables
   - Use materialized views
4. Provides trade-off analysis for each option
5. Recommends when to denormalize and when not to

**Use case**: Performance optimization without compromising data integrity.

---

### Example 4: Analyze Legacy Denormalized Table

```bash
/suggest-normalization LegacyDB.OrderSummary --form=3NF --include-denorm
```

**Scenario**: Inherited database with denormalized tables, need to understand design and improve.

**What happens**:
1. Identifies current normalization form (likely denormalized/1NF)
2. Lists all normalization violations
3. Provides refactoring roadmap to reach 3NF
4. Evaluates if denormalization was intentional and beneficial
5. Suggests keeping strategic denormalization with safeguards (triggers, computed columns)

**Use case**: Legacy database refactoring or understanding.

---

## What Gets Analyzed

### 1NF (First Normal Form) Compliance

**Requirements**:
- All columns contain atomic (indivisible) values
- No repeating groups or repeating columns (Tag1, Tag2, Tag3)
- Primary key exists to uniquely identify rows
- All rows are unique

**Violations Detected**:
- Missing primary key
- Repeating columns (Phone1, Phone2, Phone3)
- Multi-valued columns (comma-separated values)
- Non-atomic values (JSON, XML in VARCHAR columns, composite addresses)

**Example Violation**:
```
Table: Products
Column: Tags (VARCHAR) contains: "electronics, sale, featured"
Violation: Multi-valued column (comma-separated tags)
Fix: Create ProductTags table with 1:N relationship
```

---

### 2NF (Second Normal Form) Compliance

**Requirements**:
- Must be in 1NF
- No partial dependencies (all non-key columns fully dependent on entire primary key)
- Only relevant for composite primary keys

**Violations Detected**:
- Columns dependent on only part of composite PK
- Order-level data in OrderDetails table (composite PK: OrderID, ProductID)

**Example Violation**:
```
Table: OrderDetails
PK: (OrderID, ProductID)
Column: OrderDate depends only on OrderID (not on full PK)
Violation: Partial dependency
Fix: Move OrderDate to Orders table
```

---

### 3NF (Third Normal Form) Compliance

**Requirements**:
- Must be in 2NF
- No transitive dependencies (non-key columns independent of each other)
- Non-key columns depend only on primary key

**Violations Detected**:
- Transitive dependencies (A → B → C)
- Descriptive columns for foreign keys (CustomerID + CustomerName in Orders)
- Derived/calculated columns (Subtotal + TaxRate → TaxAmount)

**Example Violation**:
```
Table: Employees
Columns: EmployeeID, DepartmentID, DepartmentName
Dependency: EmployeeID → DepartmentID → DepartmentName
Violation: Transitive dependency
Fix: Remove DepartmentName from Employees, reference Departments table
```

---

### BCNF (Boyce-Codd Normal Form) Compliance

**Requirements**:
- Must be in 3NF
- Every determinant must be a candidate key

**Violations Detected**:
- Determinants that are not candidate keys

**Example Violation**:
```
Table: CourseEnrollment
PK: (StudentID, CourseID)
Columns: StudentID, CourseID, InstructorID, InstructorOffice
Dependency: InstructorID → InstructorOffice (InstructorID not a candidate key)
Violation: BCNF violation
Fix: Create Instructors table with InstructorID as PK
```

---

### 4NF (Fourth Normal Form) Compliance

**Requirements**:
- Must be in BCNF
- No multi-valued dependencies (independent sets of values)

**Violations Detected**:
- Cartesian product of independent attributes

**Example Violation**:
```
Table: EmployeeSkillsCertifications
PK: (EmployeeID, Skill, Certification)
Issue: Skills and Certifications are independent (Cartesian product)
Multi-Valued Dependencies:
- EmployeeID →→ Skill
- EmployeeID →→ Certification
Fix: Split into EmployeeSkills and EmployeeCertifications tables
```

---

### 5NF (Fifth Normal Form) Compliance

**Requirements**:
- Must be in 4NF
- No join dependencies (cannot be decomposed further without loss)

**Note**: 5NF is rarely needed and only analyzed if explicitly requested. Most applications stop at 3NF or BCNF.

---

### Denormalization Analysis (if --include-denorm)

**Opportunities Identified**:
1. **Redundant Columns**: Add frequently joined columns (e.g., CustomerName in Orders)
2. **Computed Columns**: Pre-calculate expensive computations
3. **Summary Tables**: Aggregate data for dashboards/reports
4. **Materialized Views**: SQL Server indexed views for complex queries

**Trade-Off Analysis**:
- **Performance Benefit**: Query speed improvement estimate
- **Data Integrity Cost**: Redundancy, update anomalies, sync complexity
- **Storage Cost**: Additional space required
- **Maintenance Cost**: Triggers, scheduled jobs, application logic

**Recommendations**:
- When to denormalize (read-heavy, stable data, dashboards)
- When NOT to denormalize (write-heavy, frequently changing data, transactional systems)
- How to implement safely (computed columns, triggers, materialized views)

---

## Output Report Structure

### Executive Summary
- Current normalization form
- Target normalization form
- Compliance status (Pass/Fail)
- Critical issues count
- Recommendations count
- Estimated refactoring effort

### Table Overview
- Column count, row count, data size
- Primary key, foreign keys, indexes

### Normalization Assessment
- 1NF Compliance (Pass/Fail with findings)
- 2NF Compliance (Pass/Fail with findings)
- 3NF Compliance (Pass/Fail with findings)
- BCNF/4NF/5NF Compliance (if analyzed)

### Issues Detected
For each issue:
- Issue type (1NF/2NF/3NF/BCNF/4NF violation)
- Severity (Critical/High/Medium/Low)
- Affected columns
- Description with example
- Impact (redundancy, anomalies)
- Recommended fix with SQL script

### Functional Dependencies Analysis
- Detected functional dependencies
- Candidate keys
- Determinants
- Transitive dependencies (if any)
- Multi-valued dependencies (if any)

### Refactoring Recommendations
Prioritized recommendations with:
- Issue description
- Step-by-step solution
- SQL refactoring script
- Verification query
- Estimated effort

### Data Integrity Benefits
After implementing recommendations:
- Reduced redundancy estimate
- Eliminated anomalies
- Improved maintainability
- Storage savings estimate

### Denormalization Trade-Offs (if --include-denorm)
For each denormalization option:
- Description
- Performance benefit (estimate)
- Data integrity cost
- Storage cost
- Maintenance cost
- Recommendation (Yes/No/Conditional)
- Implementation SQL script

### Testing Checklist
Steps to verify refactoring:
- Data migration validation
- Foreign key relationship verification
- Application testing
- Performance validation

---

## Prerequisites

### MCP Configuration

MSSQL MCP server must be configured:

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
- `VIEW DEFINITION` permission
- `SELECT` permission on the table

```sql
USE [DatabaseName];
GRANT VIEW DEFINITION TO [UserName];
GRANT SELECT ON [SchemaName].[TableName] TO [UserName];
```

---

## Error Handling

### Common Errors

**Error: "Table not found"**
- Verify table name spelling
- Check schema name (default is dbo)
- Ensure table exists: `SELECT * FROM sys.tables WHERE name = 'TableName'`

**Error: "Cannot sample data from table"**
- Verify SELECT permission
- Check if table is very large (may timeout)
- Reduce sample size if needed

**Error: "Cannot determine functional dependencies"**
- May require domain knowledge
- Review report for assumptions made
- Provide clarification if needed

---

## Performance Considerations

**Typical Execution Times**:
- **Small Table** (<10K rows): 2-5 minutes
- **Medium Table** (10K-1M rows): 5-10 minutes
- **Large Table** (>1M rows): 10-15 minutes

**Factors**:
- Table size (row count, column count)
- Data sampling requirements
- Complexity of dependencies

---

## Tips and Best Practices

1. **Target 3NF for Most Cases**: 3NF is the practical target for most applications
2. **Higher Forms When Needed**: BCNF for strict integrity, 4NF/5NF rarely needed
3. **Test Refactoring in Dev**: Never refactor production tables without testing
4. **Backup Before Refactoring**: Always take full backup
5. **Update Application Code**: Refactoring changes queries, update ORMs
6. **Consider Denormalization Carefully**: Only denormalize with clear performance benefits and safeguards
7. **Use Computed Columns**: Safer than manual redundancy
8. **Materialized Views**: Better than denormalization for read-heavy scenarios
9. **Monitor After Refactoring**: Verify performance and data integrity
10. **Document Decisions**: Keep normalization analysis for reference

---

## Integration with Other Commands

### Complete Schema Review Workflow

```bash
# Step 1: Analyze overall schema
/analyze-schema MyDatabase

# Step 2: Analyze normalization for key tables
/suggest-normalization MyDatabase.Users
/suggest-normalization MyDatabase.Orders
/suggest-normalization MyDatabase.Products

# Step 3: Validate relationships after normalization
/analyze-relationships MyDatabase
```

### Refactoring Workflow

```bash
# Step 1: Analyze current normalization
/suggest-normalization MyDatabase.Orders --form=3NF

# Step 2: Test refactoring in development
# (Execute refactoring scripts in dev environment)

# Step 3: Plan migration to production
/plan-schema-migration MyDB_Current MyDB_Refactored --generate-scripts

# Step 4: Execute migration in production
# (Follow deployment checklist)
```

---

## Related Commands

- **`/analyze-schema`**: Overall database schema analysis
- **`/analyze-relationships`**: Foreign key and relationship validation
- **`/plan-schema-migration`**: Migration planning after normalization changes

---

## Output Location

Reports are saved to:
```
marketplace/output/schema-analysis/normalization-{table}-{timestamp}.md
```

Example:
```
marketplace/output/schema-analysis/normalization-Users-20260116-143022.md
```

---

## Normalization Forms Quick Reference

**1NF**: Atomic values, no repeating groups, PK exists
**2NF**: 1NF + no partial dependencies (composite PK tables)
**3NF**: 2NF + no transitive dependencies (most common target)
**BCNF**: 3NF + every determinant is a candidate key (stricter)
**4NF**: BCNF + no multi-valued dependencies (rare)
**5NF**: 4NF + no join dependencies (very rare)

---

## Version History

- **2.0.0** (2026-01-16): Initial release
  - 1NF through 5NF analysis
  - Functional dependency detection
  - Transitive dependency analysis
  - Automated refactoring script generation
  - Denormalization trade-off analysis
  - Computed column recommendations

---

## Support

For issues or questions:
1. Check [README.md](../README.md) for troubleshooting
2. Review agent specification: [normalization-advisor.md](../agents/normalization-advisor.md)
3. Verify MCP configuration and permissions
4. Consult DBA for complex normalization decisions

---

**Command Type**: Analysis/Design Validation
**Delegation**: This command delegates to the `normalization-advisor` agent
**MCP Required**: Yes (MSSQL)
**Async Capable**: Yes
**Estimated Duration**: 5-15 minutes
