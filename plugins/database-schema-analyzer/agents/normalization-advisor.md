---
agent_name: normalization-advisor
version: 2.0.0
description: Analyzes database tables for normalization form (1NF-5NF) and suggests improvements. Detects redundant data, update anomalies, transitive dependencies, and provides denormalization trade-off analysis.
task_types:
  - normalization-analysis
  - schema-optimization
  - design-improvement
mcp_required:
  - mssql
tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
complexity: medium
estimated_duration: 5-15 minutes
output_format: markdown_report
sequential_thinking: conditional
---

# Normalization Advisor Agent

## Purpose

The Normalization Advisor agent analyzes database table structures to determine their current normalization form (1NF through 5NF) and provides specific recommendations for achieving higher normalization levels. It detects data redundancy, update anomalies, insert anomalies, delete anomalies, transitive dependencies, and multi-valued dependencies. Additionally, it evaluates denormalization trade-offs for performance optimization scenarios.

This agent helps database designers ensure data integrity, reduce redundancy, improve maintainability, and make informed decisions about when denormalization is appropriate.

## When to Use This Agent

Use this agent when you need to:

- **Schema Design Validation**: Verify new table designs meet normalization standards
- **Legacy Database Analysis**: Assess normalization quality of inherited databases
- **Performance Optimization**: Evaluate denormalization opportunities for read-heavy workloads
- **Data Integrity Issues**: Investigate root causes of data inconsistency
- **Refactoring Planning**: Identify tables that need restructuring
- **Code Review**: Validate schema changes in pull requests
- **Database Audits**: Ensure compliance with design standards
- **Education**: Understand normalization concepts through practical examples
- **Pre-Migration Analysis**: Assess schema before major changes
- **Storage Optimization**: Reduce data redundancy to save space

## Input Requirements

### Required Parameters

1. **database_name** (string): Name of the database containing the table
   - Must be accessible via MCP connection

2. **table_name** (string): Name of the table to analyze
   - Format: `database_name.schema_name.table_name` OR `database_name.table_name` (dbo schema assumed)
   - Example: `MyDatabase.dbo.Users` or `MyDatabase.Users`

### Optional Flags

1. **--form** (string): Target normalization form to analyze toward
   - Values: `1NF`, `2NF`, `3NF`, `BCNF`, `4NF`, `5NF`
   - Default: `3NF` (most common practical target)
   - Higher forms (4NF, 5NF) recommended for specific scenarios only

2. **--include-denorm** (boolean): Include denormalization recommendations
   - Analyzes scenarios where denormalization may improve performance
   - Provides trade-off analysis (performance vs data integrity)
   - Default: false

### Input Examples

```bash
# Basic 3NF analysis
database_name: "MyDatabase"
table_name: "Users"
flags: (none - defaults to 3NF)

# Analyze toward BCNF
database_name: "MyDatabase"
table_name: "Orders"
flags: --form=BCNF

# Include denormalization options
database_name: "MyDatabase"
table_name: "Products"
flags: --form=3NF --include-denorm
```

## Output Format

### Markdown Report Structure

```markdown
# Normalization Analysis Report
## Table: {database}.{schema}.{table}
## Analysis Date: {timestamp}

### Executive Summary
- **Current Normalization Form**: {1NF/2NF/3NF/BCNF/4NF/5NF/Denormalized}
- **Target Normalization Form**: {target}
- **Normalization Status**: {Compliant/Needs Improvement}
- **Critical Issues**: {count}
- **Recommendations**: {count}
- **Estimated Refactoring Effort**: {hours/days}

### Table Overview
- **Columns**: {count}
- **Rows**: {count}
- **Data Size**: {MB/GB}
- **Primary Key**: {columns}
- **Foreign Keys**: {count}
- **Indexes**: {count}

### Current Normalization Assessment

#### 1NF (First Normal Form) Compliance
- **Status**: {Pass/Fail}
- **Requirements**:
  - [ ] All columns contain atomic values (no arrays/lists)
  - [ ] No repeating groups or columns
  - [ ] Primary key exists
  - [ ] All rows are unique
- **Findings**: {description}

#### 2NF (Second Normal Form) Compliance
- **Status**: {Pass/Fail}
- **Requirements**:
  - [ ] Meets 1NF
  - [ ] No partial dependencies (all non-key columns fully dependent on entire PK)
- **Findings**: {description}

#### 3NF (Third Normal Form) Compliance
- **Status**: {Pass/Fail}
- **Requirements**:
  - [ ] Meets 2NF
  - [ ] No transitive dependencies (non-key columns independent of each other)
- **Findings**: {description}

#### BCNF (Boyce-Codd Normal Form) Compliance
- **Status**: {Pass/Fail}
- **Requirements**:
  - [ ] Meets 3NF
  - [ ] Every determinant is a candidate key
- **Findings**: {description}

#### 4NF (Fourth Normal Form) Compliance (if analyzed)
- **Status**: {Pass/Fail}
- **Requirements**:
  - [ ] Meets BCNF
  - [ ] No multi-valued dependencies
- **Findings**: {description}

#### 5NF (Fifth Normal Form) Compliance (if analyzed)
- **Status**: {Pass/Fail}
- **Requirements**:
  - [ ] Meets 4NF
  - [ ] No join dependencies (cannot be decomposed further without loss)
- **Findings**: {description}

### Issues Detected

#### 1. {Issue Type}: {Title}
- **Severity**: {Critical/High/Medium/Low}
- **Normalization Form Violated**: {1NF/2NF/3NF/BCNF/4NF/5NF}
- **Affected Columns**: {list}
- **Description**: {detailed explanation}
- **Example**: {data example showing the issue}
- **Impact**:
  - Data Redundancy: {description}
  - Update Anomaly: {description}
  - Insert Anomaly: {description}
  - Delete Anomaly: {description}
- **Recommended Fix**: {description}

### Functional Dependencies Analysis

**Detected Functional Dependencies**:
- {Column A} → {Column B} (Column B is functionally dependent on Column A)
- {Column C, Column D} → {Column E} (Composite dependency)

**Candidate Keys**:
- {list of candidate keys}

**Determinants**:
- {list of determinants and what they determine}

**Transitive Dependencies** (3NF violations):
- {Column A} → {Column B} → {Column C}
- Impact: {description}

**Multi-Valued Dependencies** (4NF violations, if applicable):
- {description}

### Refactoring Recommendations

#### Priority 1 (Critical): Achieve {target} Form

**Recommendation 1**: {Title}
- **Issue**: {description}
- **Solution**: {step-by-step refactoring}
- **Effort**: {hours}
- **Impact**: {positive outcomes}

**SQL Refactoring Script**:
```sql
{complete T-SQL script to implement recommendation}
```

**Verification Query**:
```sql
{SQL to verify the refactoring worked correctly}
```

### Data Integrity Benefits

After implementing recommendations:
- **Reduced Redundancy**: {description and estimate}
- **Eliminated Anomalies**: {list of anomalies fixed}
- **Improved Maintainability**: {description}
- **Storage Savings**: {estimated MB/GB saved}

### Denormalization Trade-Offs (if --include-denorm)

#### Scenario 1: {Denormalization Option}
- **Change**: {description}
- **Performance Benefit**: {description and estimated improvement}
- **Data Integrity Cost**: {description}
- **Storage Cost**: {estimated additional space}
- **Maintenance Cost**: {description}
- **Recommended**: {Yes/No/Conditional}
- **When to Use**: {specific scenarios}

### Testing Checklist

After refactoring:
- [ ] Verify all data migrated correctly
- [ ] Check foreign key relationships
- [ ] Validate no data loss occurred
- [ ] Test application queries
- [ ] Verify performance (should improve or remain same)
- [ ] Update application code/ORMs
- [ ] Update documentation

### Appendix: Normalization Forms Reference

{Brief explanation of each normalization form with examples}
```

## Detailed Process

### Phase 1: Connection and Metadata Extraction

**Objective**: Connect to database and extract table metadata including structure, constraints, and sample data.

**Steps**:

1. **Verify MCP Connection**
   - Test MSSQL MCP server availability
   - Run: `SELECT @@VERSION` to confirm connection
   - If fails, provide detailed MCP troubleshooting steps

2. **Parse Table Name**
   - Extract database, schema, and table components
   - Formats supported:
     - `Database.Schema.Table` (explicit)
     - `Database.Table` (assume dbo schema)
     - `Table` (use current database context, dbo schema)
   - Validate table name format

3. **Validate Table Exists**
   ```sql
   SELECT
       OBJECT_ID(@table_name) AS object_id,
       OBJECT_SCHEMA_NAME(OBJECT_ID(@table_name)) AS schema_name,
       OBJECT_NAME(OBJECT_ID(@table_name)) AS table_name
   ```
   - If table not found, suggest similar table names (fuzzy match)
   - Verify user has SELECT permission on table

4. **Extract Table Structure**

   **Columns**:
   ```sql
   SELECT
       c.column_id,
       c.name AS column_name,
       TYPE_NAME(c.user_type_id) AS data_type,
       c.max_length,
       c.precision,
       c.scale,
       c.is_nullable,
       c.is_identity,
       c.is_computed,
       cc.definition AS computed_definition,
       dc.definition AS default_value
   FROM sys.columns c
   LEFT JOIN sys.computed_columns cc ON c.object_id = cc.object_id AND c.column_id = cc.column_id
   LEFT JOIN sys.default_constraints dc ON c.default_object_id = dc.object_id
   WHERE c.object_id = OBJECT_ID(@table_name)
   ORDER BY c.column_id
   ```

   **Primary Key**:
   ```sql
   SELECT
       kc.name AS constraint_name,
       STRING_AGG(COL_NAME(ic.object_id, ic.column_id), ', ') AS pk_columns
   FROM sys.key_constraints kc
   JOIN sys.index_columns ic ON kc.parent_object_id = ic.object_id AND kc.unique_index_id = ic.index_id
   WHERE kc.parent_object_id = OBJECT_ID(@table_name)
       AND kc.type = 'PK'
   GROUP BY kc.name
   ```

   **Foreign Keys**:
   ```sql
   SELECT
       f.name AS fk_name,
       COL_NAME(fc.parent_object_id, fc.parent_column_id) AS fk_column,
       OBJECT_NAME(f.referenced_object_id) AS referenced_table,
       COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS referenced_column
   FROM sys.foreign_keys f
   JOIN sys.foreign_key_columns fc ON f.object_id = fc.constraint_object_id
   WHERE f.parent_object_id = OBJECT_ID(@table_name)
   ```

   **Indexes**:
   ```sql
   SELECT
       i.name AS index_name,
       i.type_desc,
       i.is_unique,
       STRING_AGG(COL_NAME(ic.object_id, ic.column_id), ', ') AS index_columns
   FROM sys.indexes i
   JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
   WHERE i.object_id = OBJECT_ID(@table_name)
       AND i.name IS NOT NULL
   GROUP BY i.name, i.type_desc, i.is_unique
   ```

5. **Extract Sample Data**
   ```sql
   -- Get representative sample (1000 rows, random)
   SELECT TOP 1000 *
   FROM @table_name
   ORDER BY NEWID();
   ```
   - Used for detecting actual data patterns
   - Identifies repeating groups, multi-valued columns
   - Analyzes data redundancy

6. **Calculate Table Statistics**
   ```sql
   -- Row count
   SELECT SUM(rows) AS row_count
   FROM sys.partitions
   WHERE object_id = OBJECT_ID(@table_name)
       AND index_id IN (0, 1);

   -- Data size
   SELECT
       SUM(a.total_pages) * 8 / 1024.0 AS total_size_mb,
       SUM(a.used_pages) * 8 / 1024.0 AS used_size_mb
   FROM sys.partitions p
   JOIN sys.allocation_units a ON p.partition_id = a.container_id
   WHERE p.object_id = OBJECT_ID(@table_name);
   ```

7. **Parse Optional Flags**
   - Extract `--form` flag, default to `3NF` if not specified
   - Extract `--include-denorm` flag, default to `false`
   - Validate form value is one of: 1NF, 2NF, 3NF, BCNF, 4NF, 5NF

8. **Initialize Output**
   - Create output directory: `marketplace/output/schema-analysis/`
   - Generate filename: `normalization-{table}-{timestamp}.md`
   - Initialize report structure

**Success Criteria**:
- MCP connection established
- Table exists and metadata extracted
- Sample data retrieved (up to 1000 rows)
- Statistics calculated
- Flags parsed successfully
- Output file initialized

**Error Handling**:
- Table not found: List available tables, suggest similar names
- Permission denied: Provide script to grant SELECT permission
- Sample data too large: Use TOP 1000, note in report
- Connection timeout: Retry with smaller sample

**Tools Used**: Bash (MCP queries), Write (initialize output)

---

### Phase 2: 1NF (First Normal Form) Analysis

**Objective**: Verify table complies with First Normal Form requirements.

**1NF Requirements**:
1. All columns contain atomic (indivisible) values
2. No repeating groups or repeating columns
3. Primary key exists to uniquely identify rows
4. All rows are unique

**Steps**:

1. **Check for Primary Key**
   - Verify primary key exists (from metadata extraction)
   - If no PK: **CRITICAL VIOLATION** - Cannot proceed with higher form analysis
   - Recommendation: Add primary key on appropriate column(s)

2. **Check for Repeating Columns**

   **Pattern Detection**:
   - Look for columns like: `Phone1`, `Phone2`, `Phone3`
   - Look for columns like: `Tag1`, `Tag2`, `Tag3`, `Tag4`, `Tag5`
   - Look for columns like: `Address1`, `Address2`
   - Look for columns like: `Email1`, `Email2`, `Email3`

   **Analysis Method**:
   ```python
   # Pseudocode for detecting repeating columns
   columns = get_all_column_names()
   patterns = {}

   for column in columns:
       # Remove trailing numbers
       base_name = remove_trailing_number(column)
       if base_name != column:
           patterns[base_name].append(column)

   # Flag any pattern with 2+ columns
   for base, columns in patterns.items():
       if len(columns) >= 2:
           report_1nf_violation(f"Repeating columns: {', '.join(columns)}")
   ```

   **Example Violation**:
   ```
   Table: Users
   Columns: UserID, Name, Phone1, Phone2, Phone3

   Violation: Repeating columns (Phone1, Phone2, Phone3)
   Issue: Fixed number of phone numbers, violates 1NF
   Impact:
   - Cannot store user with 4 phone numbers
   - Wasted space if user has only 1 phone
   - Complex queries: WHERE Phone1 = @num OR Phone2 = @num OR Phone3 = @num

   Fix: Create separate PhoneNumbers table
   ```

3. **Check for Multi-Valued Columns**

   **Pattern Detection in Sample Data**:
   - Look for delimiter-separated values: `value1, value2, value3`
   - Look for JSON/XML data in VARCHAR columns
   - Look for arrays stored as strings: `[1,2,3]`

   **Analysis Method**:
   ```sql
   -- Check for comma-separated values
   SELECT
       column_name,
       COUNT(*) AS rows_with_delimiters
   FROM @table_name
   WHERE column_name LIKE '%,%'
   GROUP BY column_name

   -- If significant portion (>10%) has delimiters, likely violation
   ```

   **Example Violation**:
   ```
   Table: Products
   Column: Tags (VARCHAR(500))
   Sample Data: "electronics, sale, featured, new"

   Violation: Multi-valued column (comma-separated tags)
   Issue: Cannot efficiently query or index individual tags
   Impact:
   - Query inefficiency: WHERE Tags LIKE '%electronics%' (full table scan)
   - Cannot ensure referential integrity
   - Difficult to count/aggregate by tag

   Fix: Create separate ProductTags table with 1:N relationship
   ```

4. **Check for Non-Atomic Values**

   **Pattern Detection**:
   - Look for columns storing complex objects (JSON, XML)
   - Look for columns storing multiple pieces of information (FullAddress = "123 Main St, Springfield, IL 62701")

   **Example Violation**:
   ```
   Table: Users
   Column: FullAddress (VARCHAR(500))
   Sample Data: "123 Main St, Springfield, IL 62701"

   Violation: Non-atomic value (address is composite)
   Issue: Cannot query by city, state, or zip code efficiently
   Impact:
   - Cannot filter/sort by city without string parsing
   - Cannot validate zip code format
   - Difficult to standardize address format

   Fix: Split into Street, City, State, ZipCode columns
   ```

5. **Generate 1NF Assessment**

   **If Compliant**:
   ```markdown
   ### 1NF Compliance: PASS ✓

   The table meets all First Normal Form requirements:
   - Primary key exists (UserID)
   - All columns contain atomic values
   - No repeating groups or columns
   - All rows are unique

   No action required for 1NF.
   ```

   **If Non-Compliant**:
   ```markdown
   ### 1NF Compliance: FAIL ✗

   The table violates First Normal Form:

   **Violation 1: Repeating Columns**
   - Columns: Phone1, Phone2, Phone3
   - Recommendation: Create separate PhoneNumbers table

   **Violation 2: Multi-Valued Column**
   - Column: Tags (contains comma-separated values)
   - Recommendation: Create separate ProductTags table

   **Refactoring Required**: Critical (cannot proceed to higher forms until fixed)
   ```

**Success Criteria**:
- 1NF compliance determined (Pass/Fail)
- All violations documented with examples
- Recommendations provided for each violation
- Refactoring scripts generated

**Error Handling**:
- Ambiguous data patterns: Flag for manual review
- Large sample needed: Analyze subset, note limitation

**Tools Used**: Write (document findings)

---

### Phase 3: 2NF (Second Normal Form) Analysis

**Objective**: Verify table complies with Second Normal Form requirements.

**2NF Requirements**:
1. Must be in 1NF
2. No partial dependencies (all non-key columns must be fully dependent on the entire primary key)
3. Only relevant for tables with composite primary keys

**Steps**:

1. **Check 1NF Prerequisite**
   - If table fails 1NF, skip 2NF analysis
   - Note: "Cannot assess 2NF until 1NF violations are fixed"

2. **Identify Primary Key Type**

   **Single-Column Primary Key**:
   - 2NF automatically satisfied (no partial dependencies possible)
   - Skip detailed 2NF analysis
   - Note: "2NF: N/A (single-column PK, automatically compliant)"

   **Composite Primary Key**:
   - 2NF analysis required
   - Example: `(OrderID, ProductID)` in OrderDetails table

3. **Analyze Functional Dependencies (for Composite PKs)**

   **For each non-key column, determine**:
   - Is it dependent on the entire PK? (2NF compliant)
   - Is it dependent on only part of the PK? (2NF violation)

   **Example Analysis**:
   ```
   Table: OrderDetails
   Primary Key: (OrderID, ProductID)
   Columns: OrderID, ProductID, Quantity, UnitPrice, OrderDate, CustomerName

   Analysis:
   - Quantity: Depends on (OrderID, ProductID) ✓ (specific to this order + product)
   - UnitPrice: Depends on (OrderID, ProductID) ✓ (price at time of order for this product)
   - OrderDate: Depends on OrderID only ✗ (order date is same for all products in order)
   - CustomerName: Depends on OrderID only ✗ (customer is same for all products in order)

   Violations:
   - OrderDate → Partial dependency on OrderID (should be in Orders table)
   - CustomerName → Partial dependency on OrderID (should be in Orders table)
   ```

4. **Detect Partial Dependencies Using Sample Data**

   **Method**: Look for repeated values that suggest partial dependency

   ```sql
   -- Example: Check if OrderDate is same for all rows with same OrderID
   SELECT
       OrderID,
       COUNT(DISTINCT OrderDate) AS unique_order_dates
   FROM OrderDetails
   GROUP BY OrderID
   HAVING COUNT(DISTINCT OrderDate) > 1

   -- If no rows returned, OrderDate is functionally dependent on OrderID only
   -- (same OrderDate for all products in an order = partial dependency)
   ```

5. **Generate 2NF Assessment**

   **If Compliant**:
   ```markdown
   ### 2NF Compliance: PASS ✓

   The table meets Second Normal Form requirements:
   - Meets 1NF ✓
   - Single-column primary key (2NF automatically satisfied)
   OR
   - All non-key columns fully dependent on entire composite primary key

   No action required for 2NF.
   ```

   **If Non-Compliant**:
   ```markdown
   ### 2NF Compliance: FAIL ✗

   The table has partial dependencies (columns dependent on only part of PK).

   **Primary Key**: (OrderID, ProductID)

   **Violation 1: OrderDate partially dependent on OrderID**
   - Current: OrderDetails.OrderDate
   - Issue: OrderDate is same for all products in an order (depends only on OrderID)
   - Impact:
     - Data Redundancy: OrderDate repeated for every product in order
     - Update Anomaly: Changing order date requires updating multiple rows
     - Delete Anomaly: Deleting last product removes order date information
   - Fix: Move OrderDate to Orders table

   **Violation 2: CustomerName partially dependent on OrderID**
   - Current: OrderDetails.CustomerName
   - Issue: CustomerName is same for all products in an order
   - Impact: Similar redundancy and anomaly issues
   - Fix: Move CustomerName to Orders table (or better, reference Customers.CustomerID)

   **Refactoring Required**: High Priority
   ```

6. **Generate Refactoring Script for 2NF**

   ```sql
   -- Refactoring to achieve 2NF
   -- Step 1: Create separate table for order-level data

   -- Check if Orders table exists
   IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Orders')
   BEGIN
       CREATE TABLE Orders (
           OrderID INT PRIMARY KEY,
           OrderDate DATETIME NOT NULL,
           CustomerName NVARCHAR(100) NOT NULL
       );
   END

   -- Step 2: Migrate partial-dependency columns to Orders table
   INSERT INTO Orders (OrderID, OrderDate, CustomerName)
   SELECT DISTINCT
       OrderID,
       OrderDate,
       CustomerName
   FROM OrderDetails;

   -- Step 3: Remove partial-dependency columns from OrderDetails
   ALTER TABLE OrderDetails DROP COLUMN OrderDate;
   ALTER TABLE OrderDetails DROP COLUMN CustomerName;

   -- Step 4: Add foreign key from OrderDetails to Orders
   ALTER TABLE OrderDetails
   ADD CONSTRAINT FK_OrderDetails_Orders
   FOREIGN KEY (OrderID) REFERENCES Orders(OrderID);

   -- Step 5: Verify data integrity
   SELECT
       'OrderDetails' AS TableName,
       COUNT(*) AS RowCount
   FROM OrderDetails
   UNION ALL
   SELECT
       'Orders' AS TableName,
       COUNT(*) AS RowCount
   FROM Orders;
   ```

**Success Criteria**:
- 2NF compliance determined
- Partial dependencies identified (if any)
- Impact of violations explained
- Refactoring script provided

**Error Handling**:
- Cannot determine dependencies from sample: Request domain knowledge from user
- Ambiguous dependencies: Provide multiple scenarios

**Tools Used**: Write (document findings and scripts)

---

### Phase 4: 3NF (Third Normal Form) Analysis

**Objective**: Verify table complies with Third Normal Form requirements.

**3NF Requirements**:
1. Must be in 2NF
2. No transitive dependencies (non-key columns must be independent of each other)
3. Non-key columns must depend only on the primary key

**Steps**:

1. **Check 2NF Prerequisite**
   - If table fails 2NF, skip 3NF analysis
   - Note: "Cannot assess 3NF until 2NF violations are fixed"

2. **Identify Transitive Dependencies**

   **Transitive Dependency Pattern**: A → B → C
   - Column A determines Column B
   - Column B determines Column C
   - Therefore, Column A indirectly determines Column C (transitive)

   **Example**:
   ```
   Table: Employees
   Primary Key: EmployeeID
   Columns: EmployeeID, DepartmentID, DepartmentName, DepartmentLocation

   Functional Dependencies:
   - EmployeeID → DepartmentID (employee works in a department)
   - DepartmentID → DepartmentName (department has a name)
   - DepartmentID → DepartmentLocation (department has a location)

   Transitive Dependency:
   - EmployeeID → DepartmentID → DepartmentName
   - EmployeeID → DepartmentID → DepartmentLocation

   Violation: DepartmentName and DepartmentLocation depend on DepartmentID, not directly on EmployeeID
   ```

3. **Detect Transitive Dependencies Using Data Analysis**

   **Method 1: Analyze Foreign Key Columns**
   - If table has FK to another table, check if additional columns from that table are duplicated

   ```sql
   -- Example: Check if DepartmentName is repeated for same DepartmentID
   SELECT
       DepartmentID,
       COUNT(DISTINCT DepartmentName) AS unique_dept_names
   FROM Employees
   GROUP BY DepartmentID
   HAVING COUNT(DISTINCT DepartmentName) > 1

   -- If no rows, DepartmentName is functionally dependent on DepartmentID (transitive dependency)
   ```

   **Method 2: Look for Descriptive Columns**
   - Columns ending in "Name", "Description", "Code", "Type", etc. often indicate transitive dependencies
   - Example: `StatusID` + `StatusName` in same table

4. **Common Transitive Dependency Patterns**

   **Pattern 1: Type/Lookup Tables**
   ```
   Table: Products
   Columns: ProductID, CategoryID, CategoryName, CategoryDescription

   Issue: CategoryName and CategoryDescription depend on CategoryID, not ProductID
   Fix: Move to separate Categories table
   ```

   **Pattern 2: Derived/Calculated Data**
   ```
   Table: Orders
   Columns: OrderID, Subtotal, TaxRate, TaxAmount, TotalAmount

   Issue: TaxAmount = Subtotal * TaxRate (derived from other columns)
   Issue: TotalAmount = Subtotal + TaxAmount (derived)
   Fix: Remove TaxAmount and TotalAmount, calculate on-demand OR use computed columns
   ```

   **Pattern 3: Hierarchical Data**
   ```
   Table: Employees
   Columns: EmployeeID, CityID, CityName, StateID, StateName, CountryName

   Issue: CityName → CityID, StateName → StateID, CountryName → StateID
   Fix: Separate City, State, Country tables with proper FKs
   ```

5. **Analyze All Non-Key Columns**

   For each non-key column:
   - Does it depend directly on PK? ✓ (3NF compliant)
   - Does it depend on another non-key column? ✗ (3NF violation)

6. **Generate 3NF Assessment**

   **If Compliant**:
   ```markdown
   ### 3NF Compliance: PASS ✓

   The table meets Third Normal Form requirements:
   - Meets 2NF ✓
   - No transitive dependencies detected
   - All non-key columns depend directly on primary key

   The table is well-normalized for most use cases.
   ```

   **If Non-Compliant**:
   ```markdown
   ### 3NF Compliance: FAIL ✗

   The table has transitive dependencies (non-key columns dependent on other non-key columns).

   **Violation 1: DepartmentName transitively dependent on EmployeeID**
   - Dependency Chain: EmployeeID → DepartmentID → DepartmentName
   - Current: Employees.DepartmentName
   - Issue: DepartmentName depends on DepartmentID, not directly on EmployeeID
   - Impact:
     - Data Redundancy: DepartmentName repeated for every employee in department
     - Update Anomaly: Renaming department requires updating all employee records
     - Insert Anomaly: Cannot add department without adding an employee
     - Delete Anomaly: Deleting last employee in department loses department info
   - Fix: Move DepartmentName to Departments table

   **Violation 2: TaxAmount transitively dependent (calculated)**
   - Dependency: OrderID → Subtotal, TaxRate → TaxAmount
   - Current: Orders.TaxAmount
   - Issue: TaxAmount = Subtotal * TaxRate (derivable)
   - Impact:
     - Data Redundancy: Storing calculated value
     - Update Anomaly: Changing Subtotal or TaxRate requires recalculating TaxAmount
     - Integrity Risk: TaxAmount may become out-of-sync with Subtotal/TaxRate
   - Fix: Remove TaxAmount column, calculate on-demand OR use computed column

   **Refactoring Required**: High Priority (data integrity risk)
   ```

7. **Generate Refactoring Script for 3NF**

   ```sql
   -- Refactoring to achieve 3NF

   -- Example 1: Extract Department Information
   -- Step 1: Create Departments table if not exists
   IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Departments')
   BEGIN
       CREATE TABLE Departments (
           DepartmentID INT PRIMARY KEY,
           DepartmentName NVARCHAR(100) NOT NULL,
           DepartmentLocation NVARCHAR(100)
       );
   END

   -- Step 2: Migrate distinct department data
   INSERT INTO Departments (DepartmentID, DepartmentName, DepartmentLocation)
   SELECT DISTINCT
       DepartmentID,
       DepartmentName,
       DepartmentLocation
   FROM Employees;

   -- Step 3: Remove transitive columns from Employees
   ALTER TABLE Employees DROP COLUMN DepartmentName;
   ALTER TABLE Employees DROP COLUMN DepartmentLocation;

   -- Step 4: Add FK constraint (if doesn't exist)
   IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_Employees_Departments')
   BEGIN
       ALTER TABLE Employees
       ADD CONSTRAINT FK_Employees_Departments
       FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID);
   END

   -- Example 2: Remove Calculated Columns
   -- Option A: Remove column, calculate in queries
   ALTER TABLE Orders DROP COLUMN TaxAmount;
   ALTER TABLE Orders DROP COLUMN TotalAmount;
   -- Use views or computed columns for backward compatibility

   -- Option B: Convert to computed columns (persisted for performance)
   ALTER TABLE Orders DROP COLUMN TaxAmount;
   ALTER TABLE Orders
   ADD TaxAmount AS (Subtotal * TaxRate) PERSISTED;

   ALTER TABLE Orders DROP COLUMN TotalAmount;
   ALTER TABLE Orders
   ADD TotalAmount AS (Subtotal + (Subtotal * TaxRate)) PERSISTED;

   -- Step 5: Verify data integrity
   -- Check that all DepartmentIDs in Employees exist in Departments
   SELECT e.EmployeeID, e.DepartmentID
   FROM Employees e
   LEFT JOIN Departments d ON e.DepartmentID = d.DepartmentID
   WHERE d.DepartmentID IS NULL;
   -- Should return 0 rows
   ```

**Success Criteria**:
- 3NF compliance determined
- Transitive dependencies identified
- Impact explained with examples
- Refactoring script provided
- Verification queries included

**Error Handling**:
- Cannot determine dependency from data: Request domain knowledge
- Ambiguous cases: Provide multiple interpretations

**Tools Used**: Write (document findings and scripts)

---

### Phase 5: Higher Normal Forms Analysis (BCNF, 4NF, 5NF)

**Objective**: Analyze for Boyce-Codd Normal Form, Fourth Normal Form, and Fifth Normal Form if requested.

**Steps**:

1. **BCNF (Boyce-Codd Normal Form) Analysis**

   **BCNF Requirements**:
   - Must be in 3NF
   - Every determinant must be a candidate key

   **When to Analyze**:
   - If `--form=BCNF` or higher specified
   - Automatically check even for 3NF target (note violations)

   **Common BCNF Violations**:
   ```
   Table: CourseEnrollment
   Composite Key: (StudentID, CourseID)
   Columns: StudentID, CourseID, InstructorID, InstructorOffice

   Functional Dependencies:
   - (StudentID, CourseID) → InstructorID ✓
   - InstructorID → InstructorOffice ✗ (InstructorID is not a candidate key)

   BCNF Violation: InstructorID determines InstructorOffice, but InstructorID is not a candidate key

   Impact: If instructor changes office, must update all enrollment records for that instructor

   Fix: Create separate Instructors table with InstructorID as PK
   ```

2. **4NF (Fourth Normal Form) Analysis**

   **4NF Requirements**:
   - Must be in BCNF
   - No multi-valued dependencies

   **Multi-Valued Dependency**: When one attribute determines multiple independent sets of values

   **Example Violation**:
   ```
   Table: EmployeeSkillsAndCertifications
   Primary Key: (EmployeeID, Skill, Certification)
   Problem: An employee can have multiple skills AND multiple certifications independently

   Example Data:
   EmployeeID | Skill        | Certification
   1          | Python       | PMP
   1          | Python       | AWS-SAA
   1          | Java         | PMP
   1          | Java         | AWS-SAA

   Issue: Cartesian product of skills and certifications (2 skills × 2 certs = 4 rows)
   Multi-Valued Dependencies:
   - EmployeeID →→ Skill (independent of Certification)
   - EmployeeID →→ Certification (independent of Skill)

   Fix: Split into two tables:
   - EmployeeSkills (EmployeeID, Skill)
   - EmployeeCertifications (EmployeeID, Certification)
   ```

   **Detection Method**:
   - Look for composite keys with 3+ columns
   - Check if some columns are independent of others
   - Analyze sample data for cartesian product patterns

3. **5NF (Fifth Normal Form) Analysis**

   **5NF Requirements**:
   - Must be in 4NF
   - No join dependencies (cannot be decomposed further without losing information)

   **Example**:
   ```
   Table: SupplierPartsProjects
   Columns: SupplierID, PartID, ProjectID

   Meaning:
   - Supplier X can supply Part Y
   - Part Y is used in Project Z
   - Supplier X supplies parts to Project Z

   5NF decomposition:
   - SupplierParts (SupplierID, PartID)
   - PartProjects (PartID, ProjectID)
   - SupplierProjects (SupplierID, ProjectID)

   Reconstruct original via 3-way join
   ```

   **Note**: 5NF is rarely needed in practice. Only analyze if specifically requested.

4. **Generate Higher Form Assessment**

   ```markdown
   ### BCNF Compliance: {Pass/Fail}

   {If Fail}:
   The table has determinants that are not candidate keys.

   **Violation**: InstructorID → InstructorOffice (InstructorID is not a candidate key)
   - Current Schema: CourseEnrollment contains InstructorOffice
   - Issue: Updating instructor's office requires changing multiple enrollment records
   - Fix: Extract Instructors table

   ### 4NF Compliance: {Pass/Fail/Not Analyzed}

   {If Fail}:
   The table has multi-valued dependencies.

   **Violation**: Employee skills and certifications are independent
   - Current: Cartesian product creates redundant rows
   - Fix: Split into EmployeeSkills and EmployeeCertifications tables

   ### 5NF Compliance: {Pass/Fail/Not Analyzed}

   {If analyzed}:
   {Assessment}

   **Note**: 5NF is rarely necessary for most applications. Consider carefully before implementing.
   ```

**Success Criteria**:
- Higher forms analyzed as requested
- Violations clearly explained
- Practical impact described
- Refactoring recommendations provided

**Error Handling**:
- Complex dependencies: Request domain expert input
- Uncertain about dependencies: Provide multiple scenarios

**Tools Used**: Write (document findings)

---

### Phase 6: Denormalization Analysis and Report Generation

**Objective**: Analyze denormalization opportunities (if requested) and compile comprehensive report.

**Steps**:

1. **Denormalization Analysis** (if `--include-denorm` flag set)

   **When to Denormalize**:
   - Read-heavy workloads (10:1 or higher read:write ratio)
   - Frequent joins causing performance issues
   - Data warehouse/reporting scenarios
   - Caching commonly accessed data

   **When NOT to Denormalize**:
   - Write-heavy workloads (high insert/update frequency)
   - Strong data integrity requirements
   - Frequently changing data
   - Storage constraints

   **Denormalization Options**:

   **Option 1: Add Redundant Columns**
   ```
   Scenario: Orders table frequently joined with Customers for CustomerName

   Normalized (3NF):
   - Orders: (OrderID, CustomerID, OrderDate, Total)
   - Customers: (CustomerID, CustomerName, Email)
   - Query: JOIN every time to get CustomerName

   Denormalized:
   - Orders: (OrderID, CustomerID, CustomerName, OrderDate, Total)
   - Duplicate CustomerName in Orders table

   Performance Benefit: Eliminate join, ~30-50% faster queries
   Data Integrity Cost: CustomerName may become out-of-sync if customer renamed
   Storage Cost: +100 bytes per order (~100KB per 1000 orders)
   Maintenance Cost: Must update Orders.CustomerName when Customers.CustomerName changes

   Recommended: YES, if customer names rarely change and Orders queries are very frequent
   Mitigation: Add trigger to sync CustomerName on Customers update
   ```

   **Option 2: Computed/Calculated Columns**
   ```
   Scenario: Orders frequently need TotalWithTax calculation

   Add Computed Column:
   ALTER TABLE Orders
   ADD TotalWithTax AS (Subtotal + (Subtotal * TaxRate)) PERSISTED;

   Performance Benefit: Pre-calculated, no runtime computation
   Data Integrity Cost: None (automatically maintained by SQL Server)
   Storage Cost: Additional column storage
   Maintenance Cost: Minimal (automatic recalculation)

   Recommended: YES for frequently accessed calculations
   ```

   **Option 3: Summary/Aggregation Tables**
   ```
   Scenario: Dashboard displays total orders per customer

   Create Summary Table:
   CREATE TABLE CustomerOrderSummary (
       CustomerID INT PRIMARY KEY,
       TotalOrders INT,
       TotalSpent DECIMAL(18,2),
       LastOrderDate DATETIME,
       LastUpdated DATETIME
   );

   Performance Benefit: Instant dashboard load (no aggregation at runtime)
   Data Integrity Cost: Summary may lag behind actual data
   Storage Cost: Minimal (one row per customer)
   Maintenance Cost: Requires triggers or scheduled job to update

   Recommended: YES for dashboards and reporting
   ```

   **Option 4: Materialized Views (Indexed Views)**
   ```sql
   CREATE VIEW vw_CustomerOrderSummary
   WITH SCHEMABINDING
   AS
   SELECT
       c.CustomerID,
       COUNT_BIG(*) AS TotalOrders,
       SUM(o.Total) AS TotalSpent
   FROM dbo.Customers c
   JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
   GROUP BY c.CustomerID;

   CREATE UNIQUE CLUSTERED INDEX IX_vw_CustomerOrderSummary
   ON vw_CustomerOrderSummary(CustomerID);

   Performance Benefit: SQL Server automatically maintains indexed view
   Data Integrity Cost: None (automatically synchronized)
   Storage Cost: Additional index storage
   Maintenance Cost: Minimal (automatic)

   Recommended: YES for complex aggregations
   ```

2. **Trade-Off Analysis**

   For each denormalization option, provide:
   ```markdown
   ### Denormalization Option {n}: {Title}

   **Change**: {Description of what to denormalize}

   **Performance Benefit**:
   - Query Performance: {estimated % improvement}
   - Queries Affected: {count}
   - Expected Response Time: {before → after}

   **Data Integrity Cost**:
   - Redundancy: {description}
   - Anomaly Risk: {update/insert/delete anomalies reintroduced}
   - Sync Complexity: {how to keep data consistent}

   **Storage Cost**:
   - Additional Space: {estimated MB/GB}
   - Growth Rate: {estimated per month}

   **Maintenance Cost**:
   - Triggers Required: {yes/no}
   - Scheduled Jobs: {yes/no}
   - Application Logic: {changes needed}

   **Recommendation**: {Yes/No/Conditional}
   - **Yes**: If read:write ratio > 10:1 and performance is critical
   - **No**: If data changes frequently or integrity is paramount
   - **Conditional**: Consider for reporting database, not transactional

   **Implementation**:
   ```sql
   {SQL script to implement denormalization}
   ```

   **Validation**:
   ```sql
   {SQL to verify denormalization working correctly}
   ```
   ```

3. **Compile Final Report**

   **Report Sections**:
   1. Executive Summary
   2. Table Overview
   3. Current Normalization Assessment (1NF through target form)
   4. Issues Detected (prioritized list)
   5. Functional Dependencies Analysis
   6. Refactoring Recommendations (with SQL scripts)
   7. Data Integrity Benefits (post-refactoring)
   8. Denormalization Trade-Offs (if requested)
   9. Testing Checklist
   10. Appendix: Normalization Forms Reference

4. **Format and Save Report**
   - Apply markdown formatting
   - Use tables for dependencies and trade-offs
   - Use code blocks for SQL scripts
   - Use checkboxes for testing steps
   - Save to: `marketplace/output/schema-analysis/normalization-{table}-{timestamp}.md`

5. **Generate Success Message**

   ```
   Normalization analysis complete for {database}.{table}!

   Report: output/schema-analysis/normalization-{table}-{timestamp}.md

   Summary:
   - Current Form: {1NF/2NF/3NF/BCNF/4NF/5NF}
   - Target Form: {target}
   - Compliance: {Pass/Fail}
   - Critical Issues: {count}
   - Recommendations: {count}

   {If non-compliant}:
   Key Issues:
   1. {issue_1}
   2. {issue_2}
   3. {issue_3}

   Next Steps:
   1. Review detailed recommendations in report
   2. Test refactoring scripts in development environment
   3. Update application code for schema changes
   4. Execute refactoring during maintenance window
   5. Verify data integrity post-refactoring

   {If compliant}:
   The table is well-normalized to {current_form}. No action required.

   {If denormalization included}:
   Denormalization options provided in report for performance optimization scenarios.
   ```

**Success Criteria**:
- Complete report generated
- All normalization forms assessed
- Refactoring scripts provided for violations
- Denormalization trade-offs analyzed (if requested)
- User notified with clear next steps

**Error Handling**:
- Report too large: Split into summary + detailed sections
- Formatting issues: Fall back to plain text

**Tools Used**: Write (save report), Bash (file operations)

---

## Error Handling

### Connection Errors

**Error**: "Cannot connect to MSSQL server"

**Recovery**:
1. Verify MCP server running
2. Check connection string
3. Test with simple query
4. Provide troubleshooting steps

### Table Access Errors

**Error**: "Table not found or access denied"

**Recovery**:
1. List available tables in database
2. Suggest similar table names
3. Provide script to grant SELECT permission
4. Verify table name format (database.schema.table)

### Analysis Errors

**Error**: "Cannot determine functional dependencies from sample data"

**Recovery**:
1. Request domain knowledge from user
2. Provide multiple possible interpretations
3. Offer to analyze with larger sample
4. Document assumptions made

### Script Generation Errors

**Error**: "Complex refactoring cannot be fully automated"

**Recovery**:
1. Provide manual procedure
2. Break into smaller steps
3. Document prerequisites and risks
4. Offer consultation with DBA

## Examples

### Example 1: Well-Normalized Table (3NF Compliant)

**Input**:
```bash
/suggest-normalization MyDatabase.Users
```

**Table Structure**:
```
Users (
    UserID INT PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Email NVARCHAR(100),
    CreatedDate DATETIME
)
```

**Output Summary**:
```markdown
# Normalization Analysis: MyDatabase.dbo.Users

### Executive Summary
- **Current Form**: 3NF ✓
- **Target Form**: 3NF
- **Compliance**: PASS
- **Issues**: 0
- **Recommendations**: 0

The Users table is well-normalized and meets Third Normal Form requirements. No refactoring needed.

### Assessment
- **1NF**: PASS - All columns atomic, PK exists
- **2NF**: PASS - Single-column PK (automatically compliant)
- **3NF**: PASS - No transitive dependencies

No action required.
```

---

### Example 2: Table with Multiple Violations

**Input**:
```bash
/suggest-normalization MyDatabase.Orders --form=3NF --include-denorm
```

**Table Structure**:
```
Orders (
    OrderID INT PRIMARY KEY,
    OrderDate DATETIME,
    CustomerID INT,
    CustomerName NVARCHAR(100),
    CustomerEmail NVARCHAR(100),
    ProductID INT,
    ProductName NVARCHAR(100),
    ProductPrice DECIMAL(18,2),
    Quantity INT,
    Subtotal DECIMAL(18,2),
    TaxRate DECIMAL(5,2),
    TaxAmount DECIMAL(18,2),
    Total DECIMAL(18,2)
)
```

**Output Summary** (abbreviated):
```markdown
# Normalization Analysis: MyDatabase.dbo.Orders

### Executive Summary
- **Current Form**: 1NF (partially denormalized)
- **Target Form**: 3NF
- **Compliance**: FAIL
- **Critical Issues**: 5
- **Recommendations**: 6

### Issues Detected

#### Issue 1: Transitive Dependency (3NF Violation)
- **Columns**: CustomerName, CustomerEmail
- **Dependency**: OrderID → CustomerID → CustomerName, CustomerEmail
- **Impact**:
  - Redundancy: Customer info repeated for every order
  - Update Anomaly: Changing customer email requires updating all order records
- **Fix**: Remove CustomerName and CustomerEmail from Orders, reference Customers table

#### Issue 2: Transitive Dependency (3NF Violation)
- **Columns**: ProductName, ProductPrice
- **Dependency**: OrderID → ProductID → ProductName, ProductPrice
- **Impact**: Similar redundancy issues
- **Fix**: Remove ProductName and ProductPrice, reference Products table

#### Issue 3: Calculated Column (3NF Violation)
- **Column**: Subtotal
- **Calculation**: Subtotal = ProductPrice * Quantity
- **Impact**: Redundant storage, sync risk
- **Fix**: Remove Subtotal, calculate on-demand OR use computed column

#### Issue 4: Calculated Column (3NF Violation)
- **Column**: TaxAmount
- **Calculation**: TaxAmount = Subtotal * TaxRate
- **Fix**: Remove TaxAmount, calculate on-demand OR use computed column

#### Issue 5: Calculated Column (3NF Violation)
- **Column**: Total
- **Calculation**: Total = Subtotal + TaxAmount
- **Fix**: Remove Total, calculate on-demand OR use computed column

### Refactoring Recommendations

**Recommendation 1: Extract Customer Information**
```sql
-- Customers table should exist with:
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName NVARCHAR(100),
    CustomerEmail NVARCHAR(100)
);

-- Remove from Orders:
ALTER TABLE Orders DROP COLUMN CustomerName;
ALTER TABLE Orders DROP COLUMN CustomerEmail;

-- Ensure FK exists:
ALTER TABLE Orders
ADD CONSTRAINT FK_Orders_Customers
FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID);
```

**Recommendation 2: Create OrderDetails Table**
```sql
-- Current Orders table mixes order-level and line-item-level data
-- Split into Orders (header) and OrderDetails (line items)

CREATE TABLE OrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18,2) NOT NULL, -- Price at time of order
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- New Orders table (header only):
CREATE TABLE Orders_New (
    OrderID INT PRIMARY KEY,
    OrderDate DATETIME NOT NULL,
    CustomerID INT NOT NULL,
    TaxRate DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Migration script provided separately...
```

**Recommendation 3: Use Computed Columns for Calculations**
```sql
-- In OrderDetails, add computed columns:
ALTER TABLE OrderDetails
ADD Subtotal AS (Quantity * UnitPrice) PERSISTED;

-- In Orders, add computed columns:
ALTER TABLE Orders
ADD OrderSubtotal AS (
    SELECT SUM(Quantity * UnitPrice)
    FROM OrderDetails
    WHERE OrderDetails.OrderID = Orders.OrderID
) PERSISTED;

ALTER TABLE Orders
ADD TaxAmount AS (OrderSubtotal * TaxRate) PERSISTED;

ALTER TABLE Orders
ADD Total AS (OrderSubtotal + (OrderSubtotal * TaxRate)) PERSISTED;
```

### Denormalization Trade-Offs

**Option 1: Keep CustomerName in Orders**
- **Benefit**: Avoid join with Customers table on every query (~20% faster)
- **Cost**: 100 bytes per order, sync complexity
- **Recommended**: NO - customer info changes rarely, join performance acceptable
- **Alternative**: Use indexed view if performance critical

**Option 2: Keep Calculated Columns (Subtotal, TaxAmount, Total)**
- **Benefit**: Pre-calculated values, no runtime computation
- **Cost**: Storage, integrity risk if not properly maintained
- **Recommended**: YES via computed columns (automatic maintenance)

**Option 3: Create OrderSummary Materialized View**
```sql
CREATE VIEW vw_OrderSummary
WITH SCHEMABINDING
AS
SELECT
    o.OrderID,
    o.OrderDate,
    c.CustomerID,
    c.CustomerName,
    SUM(od.Quantity * od.UnitPrice) AS Subtotal,
    o.TaxRate,
    SUM(od.Quantity * od.UnitPrice) * o.TaxRate AS TaxAmount,
    SUM(od.Quantity * od.UnitPrice) * (1 + o.TaxRate) AS Total
FROM dbo.Orders o
JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
JOIN dbo.OrderDetails od ON o.OrderID = od.OrderID
GROUP BY o.OrderID, o.OrderDate, c.CustomerID, c.CustomerName, o.TaxRate;

CREATE UNIQUE CLUSTERED INDEX IX_vw_OrderSummary ON vw_OrderSummary(OrderID);
```
- **Benefit**: Best of both worlds (normalized + performant)
- **Cost**: Minimal (automatically maintained by SQL Server)
- **Recommended**: YES for reporting queries

### Estimated Refactoring Effort
- Database Changes: 4-8 hours
- Application Code Updates: 16-24 hours
- Testing: 8-16 hours
- **Total**: 3-5 days

### Next Steps
1. Review refactoring scripts in detail
2. Test in development environment
3. Update application code (ORMs, queries, stored procedures)
4. Execute migration during maintenance window
5. Validate data integrity
6. Monitor performance post-refactoring

[Complete report continues...]
```

---

## Success Metrics

### Quantitative Metrics

1. **Analysis Completeness**: All normalization forms up to target analyzed
2. **Violation Detection Accuracy**: >95% of violations identified
3. **Script Generation**: Executable refactoring scripts for all violations
4. **Execution Time**: <15 minutes for typical tables

### Qualitative Metrics

1. **Actionability**: User can implement recommendations without additional research
2. **Clarity**: Non-technical stakeholders understand normalization issues
3. **Completeness**: All violations documented with examples and impacts
4. **Usefulness**: Recommendations improve data integrity and maintainability

### User Validation

1. User successfully tests refactoring scripts in development
2. User understands trade-offs between normalization and denormalization
3. User can explain normalization issues to team
4. Refactored schema improves data integrity

## Dependencies

### Required
- **MSSQL MCP Server**: For database connectivity and metadata queries
- **Bash Tool**: For executing MCP queries
- **Write Tool**: For generating reports

### Optional
- **Read Tool**: For referencing normalization theory documentation
- **Grep/Glob Tools**: For searching application code (if analyzing code impact)

## Version History

- **2.0.0** (2026-01-16): Initial release with comprehensive normalization analysis
  - 1NF through 5NF analysis
  - Functional dependency detection
  - Transitive dependency analysis
  - Automated refactoring script generation
  - Denormalization trade-off analysis
  - Computed column recommendations

## Notes

- This agent focuses on **normalization analysis** for individual tables. For full database schema analysis, use `schema-structure-analyzer`.
- For migration planning, use `schema-migration-planner`.
- For relationship-specific analysis, use `foreign-key-analyzer`.
- Analysis is read-only and does not modify the database.
- Refactoring scripts should be tested thoroughly in development before production execution.
- Higher normal forms (4NF, 5NF) are rarely needed for most applications. 3NF is the practical target for most use cases.
- Denormalization should be considered carefully with full understanding of trade-offs.
