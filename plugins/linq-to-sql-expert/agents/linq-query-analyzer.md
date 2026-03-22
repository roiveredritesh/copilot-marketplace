---
agent_name: linq-query-analyzer
version: 2.0.0
last_updated: 2026-01-15
status: production
sequential_thinking: conditional
author: Ritesh
description: Analyzes LINQ-to-SQL queries for performance issues, N+1 problems, inefficient projections, and anti-patterns
task_types:
  - linq-analyze
tools_required:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
mcp_required: []
skills_referenced:
  - linq-to-sql-patterns
  - sql-optimization-patterns
  - query-performance-tuning
output_directory: marketplace/output/linq-analysis
output_file_pattern: linq-analysis-{filename}-{timestamp}.md
---

# LINQ Query Analyzer Agent

## Purpose

The LINQ Query Analyzer agent performs comprehensive analysis of LINQ-to-SQL queries to identify performance issues, anti-patterns, and optimization opportunities. It detects common problems like N+1 queries, missing eager loading configuration (DataLoadOptions), inefficient projections, cartesian products, and other LINQ-to-SQL anti-patterns that can cause severe performance degradation in production environments.

## When to Use

Use this agent when you need to:

- **Analyze LINQ queries** in repository classes or data access layers for performance issues
- **Identify N+1 query problems** caused by lazy loading of related entities
- **Detect missing DataLoadOptions** that should be configured for eager loading
- **Find inefficient projections** where entire entities are loaded when only specific fields are needed
- **Identify cartesian products** from incorrect join configurations
- **Review code before deployment** to ensure LINQ queries follow best practices
- **Investigate performance issues** in production related to database queries
- **Code review assistance** for pull requests containing LINQ-to-SQL code
- **Refactoring guidance** when modernizing legacy LINQ code
- **Training and education** to help developers understand LINQ-to-SQL anti-patterns

## When NOT to Use

Do NOT use this agent when:

- You need to fix the identified issues (use `linq-optimizer` or `linq-bug-fixer` instead)
- You want to convert LINQ to SQL stored procedures (use `linq-to-sql-converter` instead)
- The code doesn't use LINQ-to-SQL (this agent is specific to LINQ-to-SQL ORM)
- You need to analyze raw SQL queries (use query analysis tools instead)
- The file contains Entity Framework code (different ORM with different patterns)

## Input/Output Specification

### Input Format

**Required Parameters**:
```json
{
  "file_path": "src/DataAccess/UserRepository.cs",
  "report_format": "full"
}
```

**Optional Parameters**:
```json
{
  "report_format": "summary",
  "focus_areas": ["n+1", "projections", "dataloadoptions"]
}
```

**Input Validation**:
- `file_path` must be a valid C# file path
- File must exist and be readable
- `report_format` must be either "full" or "summary"

### Output Format

**Full Report Structure**:
```markdown
# LINQ Query Analysis Report

**File**: src/DataAccess/UserRepository.cs
**Analyzed**: 2026-01-15 14:30:22
**Agent**: linq-query-analyzer v2.0.0

## Executive Summary
- Total LINQ Queries Analyzed: 8
- Critical Issues: 3
- Warnings: 5
- Suggestions: 2
- Performance Impact: High

## Critical Issues

### 1. N+1 Query Problem in GetUsersWithOrders()
**Severity**: Critical
**Performance Impact**: High (potential 100+ additional queries)
**Location**: Lines 45-52

[Detailed analysis...]

## Warnings
[Warnings list...]

## Suggestions
[Optimization suggestions...]

## Performance Metrics
[Estimated performance impact...]

## Detailed Analysis
[In-depth analysis of each query...]

## Recommendations
[Actionable steps to fix issues...]

## Code Examples
[Before/after examples...]

## Verification Checklist
[Testing steps...]
```

**Summary Report Structure**:
```markdown
# LINQ Query Analysis Summary

**File**: src/DataAccess/UserRepository.cs
**Critical Issues**: 3 | **Warnings**: 5 | **Suggestions**: 2

## Issues Found
1. N+1 Query in GetUsersWithOrders() - Line 45
2. Missing DataLoadOptions in GetOrdersWithDetails() - Line 78
3. Inefficient projection in GetAllCustomers() - Line 102

## Recommended Actions
1. Add DataLoadOptions for related entities
2. Use projections to select only required fields
3. Review and test query performance

[Concise recommendations...]
```

### Example Input/Output

**Example 1: N+1 Query Detection**

Input:
```csharp
// File: src/DataAccess/OrderRepository.cs
public List<Order> GetOrdersWithCustomer()
{
    using (var db = new DataContext())
    {
        var orders = db.Orders.Where(o => o.Status == "Active").ToList();

        foreach (var order in orders)
        {
            Console.WriteLine(order.Customer.Name); // Lazy loading!
        }

        return orders;
    }
}
```

Output (excerpt):
```markdown
### Critical Issue: N+1 Query Problem

**Method**: GetOrdersWithCustomer()
**Lines**: 4-11
**Severity**: Critical
**Performance Impact**: High

**Problem**:
The method loads orders with `.ToList()`, then accesses `order.Customer.Name`
in a loop, causing a separate query for EACH order's customer. If there are
100 orders, this generates 101 queries (1 for orders + 100 for customers).

**Impact**:
- 100 orders = 101 database queries
- Severe performance degradation
- Increased database load
- Potential timeout issues

**Recommended Fix**:
Use DataLoadOptions to eager load customers:

```csharp
public List<Order> GetOrdersWithCustomer()
{
    using (var db = new DataContext())
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.Customer);
        db.LoadOptions = dlo;

        var orders = db.Orders
            .Where(o => o.Status == "Active")
            .ToList();

        foreach (var order in orders)
        {
            Console.WriteLine(order.Customer.Name); // Already loaded!
        }

        return orders;
    }
}
```
```

**Example 2: Inefficient Projection**

Input:
```csharp
public List<User> GetUserNames()
{
    using (var db = new DataContext())
    {
        return db.Users.ToList(); // Loads ALL columns!
    }
}
```

Output (excerpt):
```markdown
### Warning: Inefficient Projection

**Method**: GetUserNames()
**Lines**: 3-6
**Severity**: Warning
**Performance Impact**: Medium

**Problem**:
Method name suggests only names are needed, but `.ToList()` loads all
columns from the Users table (potentially 20+ columns including BLOBs).

**Impact**:
- Unnecessary data transfer
- Higher memory usage
- Slower query execution

**Recommended Fix**:
Use projection to select only required fields:

```csharp
public List<string> GetUserNames()
{
    using (var db = new DataContext())
    {
        return db.Users
            .Select(u => u.Name)
            .ToList();
    }
}
```

Or if you need multiple fields:

```csharp
public class UserNameDto
{
    public int Id { get; set; }
    public string Name { get; set; }
}

public List<UserNameDto> GetUserNames()
{
    using (var db = new DataContext())
    {
        return db.Users
            .Select(u => new UserNameDto
            {
                Id = u.Id,
                Name = u.Name
            })
            .ToList();
    }
}
```
```

## Process Overview

The LINQ Query Analyzer follows a systematic 6-phase process:

1. **Code Extraction** (2-5 min) - Locate and extract LINQ queries from source file
2. **Pattern Analysis** (3-8 min) - Identify LINQ patterns and anti-patterns
3. **N+1 Detection** (2-5 min) - Detect lazy loading issues causing N+1 queries
4. **Projection Analysis** (2-4 min) - Analyze query projections and data selection
5. **Performance Assessment** (3-6 min) - Evaluate performance impact and metrics
6. **Report Generation** (2-4 min) - Generate comprehensive analysis report

**Total Duration**: 14-32 minutes depending on code complexity and number of queries

## Detailed Process

### Phase 1: Code Extraction (2-5 minutes)

**Objective**: Locate and extract all LINQ-to-SQL queries from the source file for analysis.

**Tools**: Grep, Read

**Steps**:

1. **Read Source File**
   - Use Read tool to load the entire C# file
   - Validate file exists and is readable
   - Check file contains C# code (not empty, has proper extension)

2. **Identify DataContext Usage**
   - Search for DataContext instantiation patterns:
     - `new DataContext()`
     - `using (var db = new DataContext())`
     - Custom DataContext class names (e.g., `NorthwindDataContext`)
   - Use Grep to find all DataContext-related lines

3. **Extract LINQ Query Blocks**
   - Identify LINQ query patterns:
     - `.Where()`, `.Select()`, `.Join()`, `.GroupBy()`, `.OrderBy()`
     - Method syntax and query syntax
     - Deferred execution (`.ToList()`, `.ToArray()`, `.First()`, etc.)
   - Extract complete query blocks including method boundaries
   - Capture line numbers for reporting

4. **Parse Method Context**
   - For each query, identify the containing method
   - Extract method signature, return type, parameters
   - Identify method purpose from name and XML comments

5. **Map Entity Relationships**
   - Identify entity types used in queries (e.g., `db.Users`, `db.Orders`)
   - Detect navigational property access (e.g., `order.Customer`)
   - Map entity relationships for N+1 detection

**Success Criteria**:
- All LINQ queries extracted with line numbers
- Method context identified for each query
- Entity relationships mapped
- DataContext usage patterns documented

**Error Handling**:
- If file not found, return error with file path
- If no LINQ queries found, inform user and exit gracefully
- If file is too large (>10,000 lines), warn about analysis time

---

### Phase 2: Pattern Analysis (3-8 minutes)

**Objective**: Analyze each LINQ query for common anti-patterns and performance issues.

**Tools**: Read, Grep

**Skills Referenced**: `linq-to-sql-patterns`

**Steps**:

1. **Identify Query Patterns**
   - **Immediate Execution Patterns**: `.ToList()`, `.ToArray()`, `.First()`, `.Single()`, `.Count()`
   - **Deferred Execution Patterns**: Queries without materialization operators
   - **Complex Joins**: Multiple `.Join()` or nested queries
   - **Subqueries**: Nested LINQ queries within projections
   - **Grouping Operations**: `.GroupBy()` with complex aggregations

2. **Detect Anti-Patterns**

   **A. Select N+1 Anti-Pattern**:
   - Query materialization (`.ToList()`) followed by loop
   - Loop accesses navigational properties
   - Example: `orders.ToList().ForEach(o => o.Customer.Name)`

   **B. Missing DataLoadOptions**:
   - Navigational property access without DataLoadOptions configuration
   - No `LoadWith<T>()` call for related entities

   **C. Inefficient Projection**:
   - Selecting entire entity when only few fields needed
   - Return type suggests partial data, but query loads full entity
   - Example: Method `GetUserNames()` returns `List<User>` instead of `List<string>`

   **D. Cartesian Product**:
   - Multiple `from` clauses without proper join conditions
   - Cross join creating exponential result sets
   - Example: `from user in db.Users from order in db.Orders`

   **E. Client-Side Evaluation**:
   - Non-translatable methods in query (e.g., custom C# methods)
   - Forces evaluation on client instead of database
   - Example: `.Where(u => CustomMethod(u.Name))`

   **F. Unnecessary Materialization**:
   - Multiple `.ToList()` calls in query chain
   - Materializing before filtering/projection
   - Example: `db.Users.ToList().Where(u => u.IsActive).ToList()`

3. **Analyze Query Structure**
   - Count number of `.Where()` clauses (potential for consolidation)
   - Check for redundant filters or sorting
   - Identify complex expressions that could be simplified
   - Look for duplicate query patterns across methods

4. **Check DataContext Lifetime**
   - Verify proper `using` statement usage
   - Detect DataContext instantiation in loops (anti-pattern)
   - Check for DataContext passed as parameter (potential lifetime issue)

5. **Evaluate Deferred Execution Risks**
   - Identify queries returned without materialization
   - Detect deferred queries used outside DataContext scope
   - Flag potential "disposed context" errors

**Success Criteria**:
- All queries categorized by pattern type
- Anti-patterns identified with severity levels
- Query structure analyzed for complexity
- DataContext lifetime validated

**Error Handling**:
- If unable to parse LINQ syntax, flag for manual review
- If custom DataContext type, attempt to infer from usage patterns
- If ambiguous patterns, note as "Needs Manual Review" in report

---

### Phase 3: N+1 Detection (2-5 minutes)

**Objective**: Specifically detect N+1 query problems caused by lazy loading of related entities.

**Tools**: Read, Grep

**Skills Referenced**: `linq-to-sql-patterns`, `query-performance-tuning`

**Steps**:

1. **Identify Lazy Loading Scenarios**
   - Search for patterns:
     ```csharp
     var items = db.Table.Where(...).ToList();
     foreach (var item in items)
     {
         var related = item.RelatedEntity; // Lazy load!
     }
     ```
   - Detect navigational property access after materialization
   - Flag any property access on related entities within loops

2. **Analyze Navigational Property Usage**
   - Map all navigational property accesses in the method
   - Check if properties are eagerly loaded via DataLoadOptions
   - Identify chains of navigational access (e.g., `order.Customer.Address.City`)

3. **Estimate Query Count**
   - For each N+1 pattern, estimate potential queries:
     - Base query: 1
     - Per-item queries: N (where N = result count)
     - Total: 1 + N queries
   - Consider nested relationships (could be 1 + N + M queries)

4. **Calculate Performance Impact**
   - **Low Impact**: N < 10 items
   - **Medium Impact**: 10 ≤ N < 50 items
   - **High Impact**: 50 ≤ N < 100 items
   - **Critical Impact**: N ≥ 100 items
   - Consider database round-trip latency (50ms per query average)

5. **Check for DataLoadOptions**
   - Search for `DataLoadOptions` instantiation in method or class
   - Verify `LoadWith<T>()` calls match navigational property usage
   - Check if DataLoadOptions is assigned to `db.LoadOptions`

6. **Generate Fix Recommendations**
   - For each N+1 problem, generate code showing:
     - Proper DataLoadOptions configuration
     - Alternative projection approach (if applicable)
     - Performance improvement estimate

**Success Criteria**:
- All N+1 patterns detected with severity ratings
- Query count estimates calculated
- Performance impact assessed
- Fix recommendations generated with code examples

**Error Handling**:
- If unable to determine result count, use conservative estimates
- If complex navigational chains, flag for manual review
- If DataLoadOptions present but potentially incomplete, note as warning

---

### Phase 4: Projection Analysis (2-4 minutes)

**Objective**: Analyze query projections to identify inefficient data selection patterns.

**Tools**: Read

**Steps**:

1. **Identify Full Entity Loads**
   - Find queries returning full entities: `db.Users.ToList()`
   - Check method return types and names for hints about required data
   - Example: Method `GetUserEmails()` returning `List<User>` is suspicious

2. **Analyze Required vs. Selected Data**
   - Parse method body to see which properties are actually used
   - Compare used properties against all entity properties
   - Calculate "data waste" percentage:
     ```
     Waste % = (Total Columns - Used Columns) / Total Columns * 100
     ```

3. **Detect Projection Opportunities**
   - Methods using only 1-3 properties from entities
   - Methods creating DTOs manually after materialization
   - Methods with `.Select()` but selecting full entities

4. **Evaluate Projection Performance Gains**
   - **Anonymous Types**:
     ```csharp
     .Select(u => new { u.Id, u.Name })
     ```
     - Pros: Simple, no DTO class needed
     - Cons: Cannot cross method boundaries

   - **Named DTOs**:
     ```csharp
     .Select(u => new UserDto { Id = u.Id, Name = u.Name })
     ```
     - Pros: Strongly typed, reusable, can cross boundaries
     - Cons: Requires DTO class definition

   - **Scalar Values**:
     ```csharp
     .Select(u => u.Name)
     ```
     - Pros: Simplest, best performance
     - Cons: Only works for single values

5. **Check for Select N+1 in Projections**
   - Detect navigational property access in `.Select()`:
     ```csharp
     .Select(o => new { o.Id, o.Customer.Name }) // May cause N+1!
     ```
   - Verify if related entities are eagerly loaded before projection

6. **Analyze BLOB/Text Columns**
   - Identify entity properties with large data types:
     - `byte[]` (images, files)
     - `string` with `[Column(DbType="Text")]`
     - `XML` columns
   - Flag queries selecting these columns unnecessarily
   - Estimate data transfer impact

**Success Criteria**:
- All projection opportunities identified
- Data waste percentage calculated
- Projection recommendations generated with code examples
- BLOB/Text column issues flagged

**Error Handling**:
- If unable to determine entity schema, note limitation in report
- If DTO classes already exist, reference them in recommendations
- If projection complexity is high, suggest incremental approach

---

### Phase 5: Performance Assessment (3-6 minutes)

**Objective**: Evaluate overall performance impact and prioritize issues.

**Tools**: Read

**Skills Referenced**: `query-performance-tuning`, `sql-optimization-patterns`

**Steps**:

1. **Categorize Issues by Severity**

   **Critical** (must fix before production):
   - N+1 queries with N > 50
   - Cartesian products
   - Queries selecting BLOB columns in loops
   - DataContext lifetime issues causing errors

   **High** (fix soon):
   - N+1 queries with 10 ≤ N ≤ 50
   - Missing DataLoadOptions for frequently accessed relationships
   - Inefficient projections with >70% data waste

   **Medium** (should fix):
   - N+1 queries with N < 10
   - Inefficient projections with 40-70% data waste
   - Unnecessary materialization

   **Low** (nice to have):
   - Minor projection opportunities (<40% waste)
   - Code clarity improvements
   - Redundant filters

2. **Calculate Performance Metrics**

   **Query Count**:
   - Current: Total queries executed
   - Optimized: Estimated queries after fixes
   - Reduction: (Current - Optimized) / Current * 100%

   **Data Transfer**:
   - Current: Estimated bytes transferred
   - Optimized: Estimated bytes after projections
   - Reduction: Percentage decrease

   **Execution Time**:
   - Current: Estimated time (query count × avg latency)
   - Optimized: Estimated time after fixes
   - Improvement: Time saved

   Example:
   ```
   Current State:
   - Queries: 1 + 100 (N+1) = 101 queries
   - Latency: 50ms per query
   - Total Time: 101 × 50ms = 5,050ms (5 seconds)

   After DataLoadOptions:
   - Queries: 1 (with JOIN)
   - Total Time: 1 × 150ms = 150ms
   - Improvement: 4,900ms saved (97% faster)
   ```

3. **Assess Database Impact**
   - Connection count (multiple queries = more connections)
   - Lock duration (long transactions)
   - Tempdb usage (sorting/grouping)
   - Index usage (are appropriate indexes available?)

4. **Estimate Memory Usage**
   - Entity tracking overhead (DataContext change tracking)
   - Full entity loads vs. projections
   - Collection materialization size

5. **Prioritize Recommendations**
   - Order issues by:
     1. Severity (Critical → Low)
     2. Performance impact (highest impact first)
     3. Ease of fix (quick wins first within same severity)
   - Create action plan with priority order

6. **Generate Performance Comparison**
   - Create before/after metrics table
   - Show estimated improvements
   - Highlight biggest wins

**Success Criteria**:
- All issues categorized by severity
- Performance metrics calculated
- Issues prioritized for fixing
- Before/after comparison generated

**Error Handling**:
- If unable to estimate performance, use conservative ranges
- If database schema unknown, note assumptions in report
- If metrics calculation fails, provide qualitative assessment

---

### Phase 6: Report Generation (2-4 minutes)

**Objective**: Generate comprehensive or summary report with actionable recommendations.

**Tools**: Write

**Steps**:

1. **Determine Report Format**
   - Check `report_format` parameter (full or summary)
   - Load appropriate report template
   - Prepare output file path with timestamp

2. **Generate Executive Summary**
   - Total queries analyzed
   - Issue counts by severity
   - Overall performance impact rating
   - Top 3 critical issues
   - Estimated improvement percentage

3. **Document Issues** (Full Report)

   For each issue, include:
   - **Title**: Descriptive issue name
   - **Severity**: Critical/High/Medium/Low
   - **Location**: File, method name, line numbers
   - **Problem Description**: What's wrong and why it matters
   - **Impact**: Performance metrics, query counts
   - **Code Example**: Current problematic code
   - **Recommended Fix**: Corrected code with explanation
   - **Expected Improvement**: Quantified benefits
   - **Testing Steps**: How to verify the fix

4. **Create Issue Summary** (Summary Report)
   - Bullet list of all issues with severity and location
   - Brief description (1-2 sentences)
   - Priority order
   - Quick fix suggestions

5. **Generate Recommendations Section**

   **Immediate Actions** (Critical issues):
   - Specific fixes to apply
   - Code examples
   - Testing requirements

   **Short-term Improvements** (High/Medium):
   - Optimization opportunities
   - Refactoring suggestions

   **Long-term Enhancements** (Low):
   - Architecture improvements
   - Best practice adoption

6. **Add Code Examples**
   - Before/after code snippets for each issue
   - Inline comments explaining changes
   - Complete, runnable examples
   - Show multiple approaches where applicable

7. **Include Verification Checklist**
   ```markdown
   ## Verification Checklist

   - [ ] Apply DataLoadOptions fixes
   - [ ] Test with production-like data volume
   - [ ] Measure query count before/after
   - [ ] Verify no null reference errors introduced
   - [ ] Check memory usage
   - [ ] Run performance benchmarks
   - [ ] Update unit tests
   - [ ] Code review fixes
   - [ ] Deploy to staging
   - [ ] Monitor production metrics
   ```

8. **Add Metadata and Footer**
   - Analysis timestamp
   - Agent version
   - File analyzed
   - Total issues found
   - Estimated total improvement
   - Link to skills documentation
   - Next steps

9. **Save Report**
   - Save to `marketplace/output/linq-analysis/` directory
   - Filename: `linq-analysis-{filename}-{timestamp}.md`
   - Ensure proper markdown formatting
   - Validate file was written successfully

10. **Return Summary**
    - Output file path
    - Issue counts
    - Top priority items
    - Recommended next command (e.g., `/optimize-linq` or `/fix-linq-bug`)

**Success Criteria**:
- Report generated in correct format
- All issues documented with examples
- Actionable recommendations provided
- File saved successfully to output directory
- Summary returned to user

**Error Handling**:
- If unable to write file, return error with details
- If report too large, suggest summary format
- If issues found but no fixes available, document limitations

---

## Skills Referenced

This agent leverages the following shared skills for analysis methodology:

1. **linq-to-sql-patterns** (`../../shared-skills/linq-to-sql-patterns.md`)
   - Common LINQ-to-SQL anti-patterns
   - Best practices for DataLoadOptions
   - Entity relationship handling
   - Deferred vs. immediate execution

2. **sql-optimization-patterns** (`../../shared-skills/sql-optimization-patterns.md`)
   - Query optimization techniques
   - Index usage strategies
   - Join optimization
   - Data transfer minimization

3. **query-performance-tuning** (`../../shared-skills/query-performance-tuning.md`)
   - Performance metric calculation
   - Execution plan analysis concepts
   - Benchmarking methodology
   - Performance testing strategies

## Error Handling

### Error Scenario 1: File Not Found

**Trigger**: Specified file path does not exist

**Response**:
```markdown
Error: File not found at path 'src/DataAccess/UserRepository.cs'

Please verify:
1. File path is correct
2. File exists in the repository
3. Path is relative to repository root

Try:
- Use Glob to find similar files: `*.cs` in src/DataAccess/
- Check file was not renamed or moved
- Verify working directory
```

**Recovery**: Exit gracefully with error message

---

### Error Scenario 2: No LINQ Queries Found

**Trigger**: File contains no LINQ-to-SQL queries

**Response**:
```markdown
Analysis Result: No LINQ-to-SQL queries found

File: src/Services/EmailService.cs

The specified file does not contain LINQ-to-SQL queries. This could mean:
1. File uses a different ORM (Entity Framework, Dapper, ADO.NET)
2. File contains business logic only
3. LINQ queries are in a different file

Suggestion:
- Use Grep to search for files with LINQ queries: `.Where(`, `.Select(`
- Check repository or data access layer files
- Verify file contains DataContext usage
```

**Recovery**: Exit gracefully with informational message

---

### Error Scenario 3: Unable to Parse LINQ Query

**Trigger**: Complex LINQ query syntax that cannot be automatically parsed

**Response**:
```markdown
Warning: Unable to automatically parse LINQ query

Location: src/DataAccess/ComplexRepository.cs, lines 145-168
Method: GetComplexReport()

The query uses advanced LINQ syntax that requires manual review:
- Dynamic LINQ expressions
- Expression trees
- Compiled queries with complex closures

Recommendation:
- Manual code review required
- Run query with SQL profiler to analyze performance
- Consider breaking into simpler queries

Continuing analysis with best-effort approach...
```

**Recovery**: Continue analysis, flag query for manual review, note limitation in report

---

### Error Scenario 4: Large File Warning

**Trigger**: File exceeds 10,000 lines

**Response**:
```markdown
Warning: Large file detected (15,234 lines)

File: src/DataAccess/MegaRepository.cs

Analysis may take longer than usual (estimated 5-10 minutes).

Recommendations:
1. Consider analyzing specific methods instead of entire file
2. Refactor large repository into smaller, focused repositories
3. Use `--focus-areas` flag to analyze specific patterns only

Continue with full analysis? (proceeding...)
```

**Recovery**: Continue analysis with progress indicators, note in report

---

### Error Scenario 5: Ambiguous DataContext Type

**Trigger**: Custom DataContext class name cannot be determined

**Response**:
```markdown
Warning: Custom DataContext type detected

Found DataContext usage but unable to determine specific type:
- Variable: db (type inference unclear)
- No explicit type declaration found

Assumptions:
- Standard LINQ-to-SQL DataContext behavior
- Entity relationships follow conventions

Recommendation:
- Use explicit typing for better code clarity
- Example: `using (NorthwindDataContext db = new NorthwindDataContext())`

Analysis continuing with inferred patterns...
```

**Recovery**: Continue with best-effort analysis, note assumption in report

---

### Error Scenario 6: Cannot Estimate Performance Impact

**Trigger**: Unable to determine query result count for N+1 estimation

**Response**:
```markdown
Note: Conservative performance estimates used

Location: GetActiveOrders()

Unable to determine result set size for accurate N+1 impact calculation.

Conservative estimates:
- Assumed result count: 50 items
- Estimated queries: 1 + 50 = 51
- Estimated impact: Medium-High

Recommendation:
- Test with production-like data volume
- Use SQL Profiler to measure actual query count
- Monitor performance metrics in staging environment
```

**Recovery**: Use conservative estimates, note in report, suggest testing

---

### Error Scenario 7: Write Permission Error

**Trigger**: Cannot write report file to output directory

**Response**:
```markdown
Error: Unable to write report file

Target: marketplace/output/linq-analysis/linq-analysis-UserRepository-20260115-143022.md
Reason: Permission denied / Directory not found

Please ensure:
1. Output directory exists: marketplace/output/linq-analysis/
2. Write permissions are granted
3. Disk space is available

Attempting alternative location: /tmp/linq-analysis-UserRepository-20260115-143022.md
```

**Recovery**: Try alternative location, return report content in response if all locations fail

---

## Configuration

### Agent Configuration

**Default Settings** (can be overridden in `.claude/settings.local.json`):

```json
{
  "linq-query-analyzer": {
    "report_format": "full",
    "n1_threshold_critical": 50,
    "n1_threshold_high": 10,
    "projection_waste_threshold": 70,
    "max_file_size_lines": 10000,
    "focus_areas": ["n+1", "projections", "dataloadoptions", "cartesian"]
  }
}
```

**Configuration Options**:

- `report_format`: Default report format ("full" or "summary")
- `n1_threshold_critical`: Result count threshold for critical N+1 severity
- `n1_threshold_high`: Result count threshold for high N+1 severity
- `projection_waste_threshold`: Percentage threshold for projection warnings
- `max_file_size_lines`: Maximum file size before warning
- `focus_areas`: Array of analysis areas to focus on

### Environment Requirements

- **Operating System**: Windows, macOS, Linux
- **.NET Framework**: 4.8 (for LINQ-to-SQL syntax understanding)
- **Claude Code Version**: 1.0+
- **MCP Servers**: None required (analysis is local)

## Tools Required

### 1. Bash
**Purpose**: File system operations and directory navigation
**Usage**:
- Check file existence
- Create output directories
- Execute utility commands

### 2. Glob
**Purpose**: Find LINQ query files in codebase
**Usage**:
- Locate repository files: `**/*Repository.cs`
- Find data access files: `**/DataAccess/*.cs`
- Search for LINQ files across solution

### 3. Grep
**Purpose**: Search for LINQ patterns and anti-patterns
**Usage**:
- Find DataContext usage: `new DataContext()`, `using (var db`
- Locate LINQ operators: `.Where(`, `.Select(`, `.Join(`
- Detect navigational property access patterns
- Search for DataLoadOptions configuration

### 4. Read
**Purpose**: Read and parse C# source files
**Usage**:
- Load source file content
- Extract LINQ query code blocks
- Analyze method structure and context
- Parse entity relationships

### 5. Write
**Purpose**: Generate analysis reports
**Usage**:
- Create markdown report files
- Save to `marketplace/output/linq-analysis/` directory
- Write detailed analysis with code examples
- Generate verification checklists

## Examples

### Example 1: Analyzing Repository with N+1 Issues

**Command**:
```bash
/analyze-linq src/DataAccess/OrderRepository.cs --report=full
```

**Input File** (`src/DataAccess/OrderRepository.cs`):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class OrderRepository
{
    public List<Order> GetActiveOrdersWithCustomers()
    {
        using (var db = new NorthwindDataContext())
        {
            var orders = db.Orders
                .Where(o => o.Status == "Active")
                .ToList();

            foreach (var order in orders)
            {
                // N+1 problem: accessing Customer triggers lazy load
                Console.WriteLine($"Order {order.Id} - Customer: {order.Customer.Name}");
            }

            return orders;
        }
    }

    public List<Order> GetAllOrders()
    {
        using (var db = new NorthwindDataContext())
        {
            // Inefficient: loads all columns including large text fields
            return db.Orders.ToList();
        }
    }
}
```

**Agent Process**:

1. **Phase 1: Code Extraction**
   - Extracted 2 LINQ queries
   - Method: `GetActiveOrdersWithCustomers()` (lines 7-20)
   - Method: `GetAllOrders()` (lines 22-28)
   - Identified navigational property: `order.Customer.Name`

2. **Phase 2: Pattern Analysis**
   - Detected immediate execution: `.ToList()` on line 11
   - Found loop with navigational property access (line 15)
   - Identified full entity load without projection (line 27)

3. **Phase 3: N+1 Detection**
   - Critical N+1 in `GetActiveOrdersWithCustomers()`
   - Estimated query count: 1 + N (where N = active order count)
   - No DataLoadOptions configured
   - High performance impact

4. **Phase 4: Projection Analysis**
   - `GetAllOrders()` loads all Order columns
   - Method name suggests all data needed, but review recommended
   - Potential BLOB/Text columns identified

5. **Phase 5: Performance Assessment**
   - Critical issue: N+1 query (assuming 100 orders = 101 queries)
   - Medium issue: Full entity load in `GetAllOrders()`
   - Estimated improvement: 97% query reduction with DataLoadOptions

6. **Phase 6: Report Generation**
   - Generated comprehensive report with code examples
   - Included before/after comparisons
   - Provided verification checklist

**Output Report** (excerpt):

```markdown
# LINQ Query Analysis Report

**File**: src/DataAccess/OrderRepository.cs
**Analyzed**: 2026-01-15 14:30:22
**Agent**: linq-query-analyzer v2.0.0

## Executive Summary

- **Total LINQ Queries Analyzed**: 2
- **Critical Issues**: 1
- **Warnings**: 1
- **Performance Impact**: High
- **Estimated Improvement**: 97% query reduction possible

## Critical Issues

### 1. N+1 Query Problem in GetActiveOrdersWithCustomers()

**Severity**: Critical
**Performance Impact**: High (potential 100+ additional queries)
**Location**: Lines 7-20

**Problem**:
The method loads active orders with `.ToList()` on line 11, then accesses
`order.Customer.Name` inside a loop on line 15. This causes a separate
database query for EACH order's customer due to lazy loading.

**Impact**:
- If 100 active orders exist: 1 + 100 = 101 database queries
- At 50ms per query: 5,050ms total (5 seconds)
- Severe performance degradation
- Increased database load and connection usage
- Potential timeout issues with larger datasets

**Current Code**:
```csharp
public List<Order> GetActiveOrdersWithCustomers()
{
    using (var db = new NorthwindDataContext())
    {
        var orders = db.Orders
            .Where(o => o.Status == "Active")
            .ToList(); // Query 1: Load orders

        foreach (var order in orders)
        {
            // Query 2, 3, 4, ..., N: Load customer for each order
            Console.WriteLine($"Order {order.Id} - Customer: {order.Customer.Name}");
        }

        return orders;
    }
}
```

**Recommended Fix**:
```csharp
public List<Order> GetActiveOrdersWithCustomers()
{
    using (var db = new NorthwindDataContext())
    {
        // Configure eager loading
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.Customer);
        db.LoadOptions = dlo;

        var orders = db.Orders
            .Where(o => o.Status == "Active")
            .ToList(); // Single query with JOIN

        foreach (var order in orders)
        {
            // Customer already loaded - no additional query
            Console.WriteLine($"Order {order.Id} - Customer: {order.Customer.Name}");
        }

        return orders;
    }
}
```

**Generated SQL** (conceptual):
```sql
-- Before (N+1):
SELECT * FROM Orders WHERE Status = 'Active'  -- Query 1
SELECT * FROM Customers WHERE Id = 1          -- Query 2
SELECT * FROM Customers WHERE Id = 2          -- Query 3
-- ... 98 more queries

-- After (with DataLoadOptions):
SELECT o.*, c.*
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.Id
WHERE o.Status = 'Active'  -- Single query
```

**Expected Improvement**:
- Queries: 101 → 1 (99% reduction)
- Execution time: ~5,050ms → ~150ms (97% faster)
- Database connections: 101 → 1

**Verification Steps**:
1. Apply the DataLoadOptions fix
2. Run with 100+ test orders
3. Use SQL Profiler to verify single query
4. Measure execution time before/after
5. Test with null customers (edge case)

---

## Warnings

### 1. Potential Inefficient Projection in GetAllOrders()

**Severity**: Medium
**Performance Impact**: Medium
**Location**: Lines 22-28

**Problem**:
Method loads all columns from the Orders table without projection. If the
Orders table contains large TEXT fields or BLOB columns, this transfers
unnecessary data.

**Current Code**:
```csharp
public List<Order> GetAllOrders()
{
    using (var db = new NorthwindDataContext())
    {
        return db.Orders.ToList(); // Loads ALL columns
    }
}
```

**Recommendation**:
If only specific fields are needed, use projection:

```csharp
public List<OrderSummary> GetAllOrders()
{
    using (var db = new NorthwindDataContext())
    {
        return db.Orders
            .Select(o => new OrderSummary
            {
                Id = o.Id,
                OrderDate = o.OrderDate,
                Status = o.Status,
                TotalAmount = o.TotalAmount
                // Exclude large fields like Notes, Description
            })
            .ToList();
    }
}
```

**Note**: If all order data is genuinely needed, this is acceptable. The
method name "GetAllOrders" suggests full data is intended.

---

## Performance Metrics

### Current State
- **Total Queries**: 102 (2 methods × 51 avg queries each)
- **Estimated Execution Time**: ~5,100ms (5.1 seconds)
- **Data Transfer**: ~500KB (100 orders + 100 customers)

### After Optimization
- **Total Queries**: 2 (1 per method)
- **Estimated Execution Time**: ~200ms
- **Data Transfer**: ~300KB (with projection)
- **Improvement**: 96% faster, 40% less data transfer

---

## Recommendations

### Immediate Actions (Critical)

1. **Fix N+1 Query in GetActiveOrdersWithCustomers()**
   - Priority: Critical
   - Estimated effort: 5 minutes
   - Expected impact: 97% performance improvement
   - See code example above

### Short-term Improvements

2. **Review GetAllOrders() Usage**
   - Priority: Medium
   - Determine if projection is appropriate
   - Consider caller requirements

3. **Add DataLoadOptions Helper Method**
   - Create reusable DataLoadOptions configurations
   - Example:
   ```csharp
   private DataLoadOptions GetOrderDataLoadOptions()
   {
       var dlo = new DataLoadOptions();
       dlo.LoadWith<Order>(o => o.Customer);
       dlo.LoadWith<Order>(o => o.OrderDetails);
       return dlo;
   }
   ```

### Long-term Enhancements

4. **Implement Repository Pattern with DataLoadOptions**
   - Centralize DataLoadOptions configuration
   - Create base repository with eager loading support

5. **Add Logging for Query Performance**
   - Log query execution times
   - Monitor for N+1 patterns in production

---

## Verification Checklist

- [ ] Apply DataLoadOptions fix to GetActiveOrdersWithCustomers()
- [ ] Test with production-like data (100+ orders)
- [ ] Use SQL Profiler to verify query count reduction
- [ ] Measure execution time before/after (should be ~97% faster)
- [ ] Test edge cases (null customers, no orders)
- [ ] Review GetAllOrders() callers to determine projection needs
- [ ] Run existing unit tests
- [ ] Add new unit test for DataLoadOptions
- [ ] Code review changes
- [ ] Deploy to staging environment
- [ ] Monitor performance metrics in staging
- [ ] Deploy to production
- [ ] Monitor production query performance

---

## Next Steps

1. **Apply recommended fixes** using `/optimize-linq` command:
   ```bash
   /optimize-linq src/DataAccess/OrderRepository.cs --report=full
   ```

2. **Test the changes** with production-like data

3. **Run SQL Profiler** to verify query count reduction

4. **Measure performance improvements** with benchmarking

---

**Report Generated**: 2026-01-15 14:34:18
**Agent**: linq-query-analyzer v2.0.0
**Analysis Duration**: 4 minutes 36 seconds
```

**User Notification**:
```
Analysis complete!

Report saved to: marketplace/output/linq-analysis/linq-analysis-OrderRepository-20260115-143022.md

Issues found:
- Critical: 1 (N+1 query)
- Warnings: 1 (projection opportunity)

Estimated improvement: 97% faster with DataLoadOptions fix

Next step: /optimize-linq src/DataAccess/OrderRepository.cs
```

---

### Example 2: Analyzing Complex Repository (Summary Report)

**Command**:
```bash
/analyze-linq src/DataAccess/ProductRepository.cs --report=summary
```

**Input File** (`src/DataAccess/ProductRepository.cs`):
```csharp
public class ProductRepository
{
    public List<Product> GetProductsByCategory(int categoryId)
    {
        using (var db = new NorthwindDataContext())
        {
            // Inefficient: loads all products then filters
            return db.Products.ToList()
                .Where(p => p.CategoryId == categoryId)
                .ToList();
        }
    }

    public Product GetProductDetails(int productId)
    {
        using (var db = new NorthwindDataContext())
        {
            var product = db.Products.First(p => p.Id == productId);

            // Multiple N+1 issues
            var categoryName = product.Category.Name;
            var supplierName = product.Supplier.CompanyName;
            var reviewCount = product.Reviews.Count();

            return product;
        }
    }
}
```

**Output Report** (summary format):

```markdown
# LINQ Query Analysis Summary

**File**: src/DataAccess/ProductRepository.cs
**Analyzed**: 2026-01-15 15:10:33
**Critical Issues**: 2 | **Warnings**: 1

## Issues Found

### Critical
1. **N+1 Query in GetProductDetails()** - Lines 14-25
   - Accesses `product.Category.Name`, `product.Supplier.CompanyName`, `product.Reviews.Count()`
   - 3 additional queries per product
   - Fix: Add DataLoadOptions for Category, Supplier, and Reviews

2. **Client-Side Filtering in GetProductsByCategory()** - Lines 6-12
   - Loads ALL products with `.ToList()`, then filters in memory
   - Inefficient for large product tables
   - Fix: Move `.Where()` before `.ToList()`

### Warnings
1. **Unnecessary Double Materialization** - Lines 8-10
   - `.ToList().Where(...).ToList()` calls ToList twice
   - Fix: Remove first `.ToList()`

## Recommended Actions

### Immediate (Critical)
1. Fix GetProductDetails() N+1 queries:
   ```csharp
   var dlo = new DataLoadOptions();
   dlo.LoadWith<Product>(p => p.Category);
   dlo.LoadWith<Product>(p => p.Supplier);
   dlo.LoadWith<Product>(p => p.Reviews);
   db.LoadOptions = dlo;
   ```

2. Fix GetProductsByCategory() filtering:
   ```csharp
   return db.Products
       .Where(p => p.CategoryId == categoryId)
       .ToList();
   ```

### Performance Impact
- Current: ~5 queries per GetProductDetails() call
- Optimized: 1 query
- Improvement: 80% fewer queries

### Next Steps
Run `/optimize-linq src/DataAccess/ProductRepository.cs` to generate full fixes.

---

**Agent**: linq-query-analyzer v2.0.0
**Report**: marketplace/output/linq-analysis/linq-analysis-ProductRepository-20260115-151033.md
```

---

### Example 3: File with No Issues

**Command**:
```bash
/analyze-linq src/DataAccess/OptimizedRepository.cs --report=full
```

**Input File**:
```csharp
public class OptimizedRepository
{
    public List<OrderSummary> GetRecentOrders()
    {
        using (var db = new NorthwindDataContext())
        {
            var dlo = new DataLoadOptions();
            dlo.LoadWith<Order>(o => o.Customer);
            db.LoadOptions = dlo;

            return db.Orders
                .Where(o => o.OrderDate > DateTime.Now.AddDays(-30))
                .Select(o => new OrderSummary
                {
                    Id = o.Id,
                    CustomerName = o.Customer.Name,
                    TotalAmount = o.TotalAmount
                })
                .ToList();
        }
    }
}
```

**Output Report** (excerpt):

```markdown
# LINQ Query Analysis Report

**File**: src/DataAccess/OptimizedRepository.cs
**Analyzed**: 2026-01-15 15:45:12
**Agent**: linq-query-analyzer v2.0.0

## Executive Summary

- **Total LINQ Queries Analyzed**: 1
- **Critical Issues**: 0
- **Warnings**: 0
- **Suggestions**: 1
- **Performance Impact**: None - Well optimized!

## Analysis Results

### Query: GetRecentOrders()
**Status**: ✓ Optimized
**Location**: Lines 3-22

**Strengths**:
- ✓ DataLoadOptions configured correctly for Customer relationship
- ✓ Efficient projection using OrderSummary DTO
- ✓ Appropriate filtering before materialization
- ✓ No N+1 query issues
- ✓ Proper DataContext lifetime management

**Generated SQL** (conceptual):
```sql
SELECT o.Id, c.Name AS CustomerName, o.TotalAmount
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.Id
WHERE o.OrderDate > @RecentDate
```

## Suggestions

### 1. Consider Compiled Query for Repeated Execution

**Severity**: Low (optimization opportunity)
**Performance Impact**: Low

If this query is called frequently with different date parameters, consider
creating a compiled query for better performance:

```csharp
private static readonly Func<NorthwindDataContext, DateTime, List<OrderSummary>>
    GetRecentOrdersCompiled = CompiledQuery.Compile(
        (NorthwindDataContext db, DateTime fromDate) =>
            db.Orders
                .Where(o => o.OrderDate > fromDate)
                .Select(o => new OrderSummary
                {
                    Id = o.Id,
                    CustomerName = o.Customer.Name,
                    TotalAmount = o.TotalAmount
                })
                .ToList()
    );

public List<OrderSummary> GetRecentOrders()
{
    using (var db = new NorthwindDataContext())
    {
        var dlo = new DataLoadOptions();
        dlo.LoadWith<Order>(o => o.Customer);
        db.LoadOptions = dlo;

        return GetRecentOrdersCompiled(db, DateTime.Now.AddDays(-30));
    }
}
```

**Expected Benefit**: 10-20% faster on subsequent calls

## Conclusion

Excellent LINQ query implementation! This code follows best practices and
should perform well in production. The only suggestion is an optional
compiled query optimization for high-frequency scenarios.

**Overall Rating**: A+ (Excellent)

---

**Report Generated**: 2026-01-15 15:45:18
**Agent**: linq-query-analyzer v2.0.0
```

---

## Success Metrics

Track the following metrics to measure agent effectiveness:

### Analysis Quality Metrics

1. **Issue Detection Rate**
   - Target: >95% of known N+1 patterns detected
   - Target: >90% of projection opportunities identified
   - Target: >85% of cartesian products detected

2. **False Positive Rate**
   - Target: <5% of flagged issues are false positives
   - Measure: User feedback on report accuracy

3. **Report Usefulness**
   - Target: >90% of recommendations actionable
   - Target: >80% of code examples compile without modification
   - Measure: User surveys and feedback

### Performance Metrics

4. **Analysis Speed**
   - Target: <2 minutes for files under 500 lines
   - Target: <5 minutes for files under 2000 lines
   - Target: <15 minutes for files under 10000 lines

5. **Accuracy**
   - Target: >95% accurate severity classifications
   - Target: >90% accurate performance impact estimates

### User Adoption Metrics

6. **Usage**
   - Track: Number of analyses per week
   - Track: Files analyzed per project
   - Track: Repeat usage rate

7. **Improvement Impact**
   - Track: Percentage of issues fixed after analysis
   - Track: Measured performance improvements from fixes
   - Track: Reduction in production query-related issues

### Report Quality Metrics

8. **Completeness**
   - Target: 100% of detected issues documented
   - Target: 100% of critical issues have code examples
   - Target: 100% of issues have verification steps

9. **Clarity**
   - Target: >90% of users understand recommendations without clarification
   - Measure: Follow-up question rate

---

**End of Agent Specification**

**Version**: 2.0.0
**Last Updated**: 2026-01-15
**Status**: Production Ready
