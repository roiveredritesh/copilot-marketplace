# /analyze-linq Command

## Description

Analyze LINQ-to-SQL queries for performance issues, anti-patterns, and optimization opportunities. Detects N+1 queries, missing DataLoadOptions, inefficient projections, cartesian products, and other common LINQ-to-SQL problems.

## Usage

```bash
/analyze-linq <file-path> [--report=full|summary]
```

## Parameters

### Required

- **`<file-path>`**: Path to the C# file containing LINQ-to-SQL queries to analyze
  - Must be a valid C# source file (.cs extension)
  - File must contain LINQ-to-SQL queries using DataContext
  - Example: `src/DataAccess/OrderRepository.cs`

### Optional Flags

- **`--report=full|summary`**: Report detail level (default: `full`)
  - `full` - Comprehensive analysis with detailed explanations, code examples, and recommendations
  - `summary` - Concise summary of issues with quick fix suggestions

## Examples

### Example 1: Full Analysis of Repository File

```bash
/analyze-linq src/DataAccess/OrderRepository.cs --report=full
```

**What it does**:
- Scans all LINQ queries in OrderRepository.cs
- Identifies N+1 query patterns
- Detects missing DataLoadOptions
- Finds inefficient projections
- Checks for cartesian products
- Generates comprehensive report with:
  - Executive summary
  - Detailed issue analysis
  - Code examples (before/after)
  - Performance impact estimates
  - Verification checklist

**Output**: `marketplace/output/linq-analysis/linq-analysis-OrderRepository-20260115-143022.md`

---

### Example 2: Quick Summary of Service File

```bash
/analyze-linq src/Services/CustomerService.cs --report=summary
```

**What it does**:
- Analyzes LINQ queries in CustomerService.cs
- Generates concise summary report with:
  - Issue count by severity
  - Quick list of problems
  - Brief fix recommendations

**Output**: `marketplace/output/linq-analysis/linq-analysis-CustomerService-20260115-143022.md`

---

### Example 3: Analyze Business Logic Layer

```bash
/analyze-linq src/BusinessLogic/OrderProcessor.cs --report=full
```

**What it does**:
- Analyzes LINQ queries in business logic layer
- Identifies performance issues that could affect business operations
- Provides detailed optimization guidance

**Output**: `marketplace/output/linq-analysis/linq-analysis-OrderProcessor-20260115-143022.md`

---

## What This Command Detects

### Critical Issues
- **N+1 Query Problems**: Lazy loading in loops causing multiple database queries
- **Cartesian Products**: Incorrect joins creating exponential result sets
- **Client-Side Evaluation**: Non-translatable methods forcing evaluation on client

### High Priority Issues
- **Missing DataLoadOptions**: Navigation properties accessed without eager loading
- **Inefficient Projections**: Loading entire entities when only few fields needed
- **Unnecessary Materialization**: Multiple `.ToList()` calls in query chain

### Medium Priority Issues
- **DataContext Lifetime Issues**: Queries executing outside DataContext scope
- **Deferred Execution Risks**: Queries returned without materialization
- **Redundant Filters**: Multiple `.Where()` clauses that could be consolidated

### Low Priority Issues
- **Code Clarity**: Complex LINQ expressions that could be simplified
- **Potential Caching**: Static data queries that could benefit from caching

## Report Contents

### Full Report Includes:
1. **Executive Summary**
   - Total queries analyzed
   - Issue counts by severity
   - Overall performance impact
   - Top 3 critical issues

2. **Critical Issues Section**
   - Detailed problem description
   - Location (file, method, line numbers)
   - Impact analysis (query count, execution time)
   - Current code example
   - Recommended fix with code
   - Expected improvement metrics
   - Testing steps

3. **Warnings Section**
   - Medium/high priority issues
   - Optimization opportunities
   - Best practice violations

4. **Suggestions Section**
   - Low priority improvements
   - Code quality enhancements
   - Long-term recommendations

5. **Performance Metrics**
   - Current vs. optimized query counts
   - Estimated execution time improvements
   - Data transfer reduction estimates

6. **Recommendations**
   - Prioritized action items
   - Implementation guidance
   - Testing requirements

7. **Verification Checklist**
   - Step-by-step testing guide
   - Performance benchmarking steps
   - Deployment checklist

### Summary Report Includes:
1. **Issue Summary**
   - Count by severity
   - Quick list of problems with line numbers

2. **Recommended Actions**
   - Top 3-5 fixes to apply
   - Priority order

3. **Next Steps**
   - Command to run for fixes (`/optimize-linq` or `/fix-linq-bug`)

## Output Location

All reports are saved to:
```
marketplace/output/linq-analysis/linq-analysis-{filename}-{timestamp}.md
```

Example:
```
marketplace/output/linq-analysis/linq-analysis-OrderRepository-20260115-143022.md
```

## Delegation

This command delegates to the **`linq-query-analyzer`** agent, which performs:
1. Code extraction and LINQ query identification
2. Pattern analysis for anti-patterns
3. N+1 query detection
4. Projection analysis
5. Performance assessment
6. Report generation

See `agents/linq-query-analyzer.md` for detailed agent specification.

## When to Use This Command

Use `/analyze-linq` when you need to:
- **Review code before deployment** to catch performance issues
- **Investigate slow pages** caused by inefficient queries
- **Code review assistance** for pull requests with LINQ code
- **Refactoring guidance** when modernizing legacy code
- **Training and education** to learn LINQ-to-SQL best practices
- **Proactive optimization** before issues reach production

## When NOT to Use

Don't use this command when:
- You need to **fix** issues (use `/optimize-linq` or `/fix-linq-bug` instead)
- You want to **convert to stored procedures** (use `/convert-linq-to-sql` instead)
- File doesn't contain LINQ-to-SQL queries
- You need to analyze raw SQL or Entity Framework code

## Follow-Up Commands

After analyzing, you typically want to:

1. **If issues found**: Fix them
   ```bash
   /optimize-linq src/DataAccess/OrderRepository.cs --report=full
   ```

2. **If bugs detected**: Fix bugs specifically
   ```bash
   /fix-linq-bug src/DataAccess/OrderRepository.cs --report=full
   ```

3. **If critical performance issues**: Consider converting to stored procedures
   ```bash
   /convert-linq-to-sql src/DataAccess/OrderRepository.cs GetOrdersWithDetails --report=full
   ```

## Performance Impact

- **Analysis Time**: 5-15 minutes depending on file size and complexity
- **File Size Limit**: Up to 10,000 lines (warning issued for larger files)
- **No Runtime Impact**: Analysis is static code inspection only

## Common Use Cases

### Use Case 1: Pre-Deployment Code Review
```bash
# Analyze all repository files before deploying
/analyze-linq src/DataAccess/OrderRepository.cs --report=full
/analyze-linq src/DataAccess/CustomerRepository.cs --report=full
/analyze-linq src/DataAccess/ProductRepository.cs --report=full
```

### Use Case 2: Performance Investigation
```bash
# User reports slow order page - analyze the query
/analyze-linq src/DataAccess/OrderRepository.cs --report=full
# Review report to identify N+1 or projection issues
```

### Use Case 3: Quick Health Check
```bash
# Quick check of all data access files
/analyze-linq src/DataAccess/UserRepository.cs --report=summary
```

## Tips

1. **Start with full report** to understand all issues in detail
2. **Use summary report** for quick health checks or when you're familiar with common issues
3. **Address critical issues first** - they have the biggest impact
4. **Test after applying fixes** using the verification checklist in the report
5. **Re-run analysis after fixes** to verify improvements

## Troubleshooting

### "File not found"
- Verify the file path is correct and relative to repository root
- Check file has `.cs` extension
- Ensure file exists in working directory

### "No LINQ queries found"
- File may not contain LINQ-to-SQL code
- File might use Entity Framework or another ORM
- LINQ queries might be in other files

### "Analysis taking too long"
- File may be very large (>5000 lines)
- Consider breaking large repository files into smaller, focused classes

## Related Commands

- **`/optimize-linq`** - Apply optimizations to fix detected issues
- **`/fix-linq-bug`** - Fix specific LINQ-to-SQL bugs
- **`/convert-linq-to-sql`** - Convert LINQ query to stored procedure

## Support

For issues or questions:
- Review the full report for detailed explanations
- Check `agents/linq-query-analyzer.md` for agent details
- See `docs/TROUBLESHOOTING.md` in marketplace root

---

**Command Version**: 2.0.0
**Agent**: linq-query-analyzer
**Plugin**: linq-to-sql-expert
