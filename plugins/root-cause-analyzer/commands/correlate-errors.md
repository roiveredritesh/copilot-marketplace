---
description: "Correlate multiple errors to find common root cause"
argument-hint: "<error-list> [--time-window=duration] [--report=full|summary]"
allowed-tools: [Bash, Glob, Grep, Read, Write]
---

# Command: /correlate-errors

## Usage

```
/correlate-errors <error-list> [--time-window=duration] [--min-correlation=score] [--max-errors=N] [--report=full|summary]
```

## Arguments

### Required Arguments

- **error-list**: Errors to correlate (multiple formats supported)
  - **Direct input**: Comma-separated or newline-separated error descriptions
  - **Log file**: File path to error log (e.g., `logs/production-2026-01-15.log`)
  - **Multiple files**: Glob pattern (e.g., `logs/*.log` or `logs/error-*.log`)
  - **Directory**: Directory containing error logs (e.g., `logs/`)

**Examples**:
```bash
# Direct input (comma-separated)
"Error1: Timeout in OrderService, Error2: Deadlock in PaymentService, Error3: Connection pool exhausted"

# Single log file
logs/production-2026-01-15.log

# Multiple log files (glob)
logs/*.log

# Directory
logs/
```

### Optional Flags

- **--time-window=duration**: Time window for correlation
  - Examples: "1 hour", "2 hours", "24 hours"
  - Default: "24 hours"
  - Errors outside window are excluded from correlation

- **--min-correlation=score**: Minimum correlation score (0.0-1.0)
  - Default: 0.6
  - Higher values: Only highly correlated errors included
  - Lower values: More lenient, may include weakly related errors

- **--max-errors=N**: Maximum errors to analyze
  - Default: 15
  - If more errors found, top N most frequent are analyzed

- **--report=full|summary**: Report level (default: `full`)
  - `full`: Comprehensive analysis with correlation matrix and detailed fixes
  - `summary`: Condensed findings with root cause and fix summary

## Examples

```bash
# Correlate errors from description
/correlate-errors "Timeout in OrderService, Deadlock in PaymentService, Connection pool exhausted"

# Correlate errors from single log file
/correlate-errors logs/production-2026-01-15.log

# Correlate errors from multiple logs (1 hour window)
/correlate-errors logs/*.log --time-window="1 hour"

# Correlate with strict correlation (summary)
/correlate-errors "logs/error-batch-*.log" --min-correlation=0.7 --report=summary

# Correlate up to 10 errors from directory
/correlate-errors logs/ --max-errors=10
```

## Implementation

### Step 1: Parse Arguments
- Identify error source type (direct input, file, glob, directory)
- Extract optional flags
- Set defaults (time-window: 24h, min-correlation: 0.6, max-errors: 15, report: full)

### Step 2: Validate Error Sources
Check if files/directories exist:
```bash
# For files
if [[ -f "$file" ]]; then
  # Process file
fi

# For directories
if [[ -d "$directory" ]]; then
  # Find log files in directory
fi
```

If sources don't exist, return error:
```
❌ Error source not found: logs/production.log

Please verify:
- File path is correct
- File exists and is readable
- You have permission to access the file
```

### Step 3: Delegate to Agent
Load and execute **error-correlation-analyzer** agent with parameters:
- error_list: Parsed errors or log file paths
- time_window: Duration for correlation
- min_correlation: Minimum score threshold
- max_errors: Maximum to analyze
- report_level: full or summary

### Step 4: Execute Agent Process
Agent performs 6-phase analysis:
1. **Error Collection & Normalization** (10-12% of time)
   - Parse logs or descriptions
   - Extract error metadata (type, message, timestamp, component)
   - Normalize format
   - Deduplicate
   - Filter by time window

2. **Stack Trace Pattern Extraction** (18-22% of time)
   - Parse stack traces
   - Normalize call chains
   - Identify common patterns
   - Extract code locations

3. **Common Code Path Identification** (20-25% of time) [CRITICAL]
   - Find shared code paths
   - Analyze connection/resource usage
   - Identify missing patterns (disposal, null checks)
   - Build evidence for common cause

4. **Dependency Analysis** (15-18% of time)
   - Identify shared dependencies (database, APIs, resources)
   - Analyze resource usage patterns
   - Check for exhaustion
   - Map dependencies to errors

5. **Correlation Matrix Generation** (12-15% of time)
   - Calculate pairwise correlation scores
   - Identify correlation clusters
   - Visualize as matrix/heatmap
   - Rank errors by centrality

6. **Root Cause Identification & Fix Strategy** (15-18% of time)
   - Synthesize root cause statement
   - Build causality chain
   - Generate unified fix strategy
   - Provide implementation guidance

### Step 5: Generate Report
Write comprehensive markdown report to:
`marketplace/output/root-cause/error-correlation-<timestamp>.md`

Report includes:
- Executive summary with correlation findings
- Error collection details (all errors with metadata)
- Correlation matrix with scores
- Common code paths and shared dependencies
- Root cause identification with evidence
- Causality chain (root cause → symptoms)
- Unified fix strategy (3 levels)
- Prevention recommendations

### Step 6: Return Results
Display completion status with:
- Number of errors analyzed
- Correlation score (average)
- Root cause summary
- Fix impact (how many errors resolved by fix)
- Report location

## Output Locations

- **Full Report**: `marketplace/output/root-cause/error-correlation-<timestamp>.md`
- **Summary Report**: `marketplace/output/root-cause/error-correlation-<timestamp>-summary.md`

## Expected Duration

**Simple Correlation** (2-3 errors, single root cause):
- Error collection: 5 minutes
- Pattern extraction: 7 minutes
- Code paths: 8 minutes
- Dependencies: 6 minutes
- Matrix: 5 minutes
- Fix strategy: 6 minutes
- **Total**: ~37 minutes

**Complex Correlation** (5-8 errors, multiple clusters):
- Error collection: 7 minutes
- Pattern extraction: 10 minutes
- Code paths: 12 minutes
- Dependencies: 10 minutes
- Matrix: 8 minutes (Sequential Thinking may enable)
- Fix strategy: 10 minutes
- **Total**: ~57 minutes

## Success Criteria

Command is successful when:
- [ ] All error sources processed (files read, logs parsed)
- [ ] Errors extracted with complete metadata
- [ ] Stack traces parsed (if available)
- [ ] Correlation matrix calculated for all pairs
- [ ] Correlation scores meaningful (>0.5 for related errors)
- [ ] Common code paths identified
- [ ] Shared dependencies documented
- [ ] Root cause(s) identified with high confidence (>85%)
- [ ] All errors explained by root cause
- [ ] Unified fix strategy provided
- [ ] Report generated and saved

## Output Format

```
# ✓ Error Correlation Analysis Complete

**Errors Analyzed**: 5 distinct errors
**Time Window**: 2026-01-15 14:00-15:00 (1 hour)
**Execution Time**: 37 minutes

## Summary
- **Average Correlation**: 0.88 (Very High)
- **Correlation Pattern**: All errors highly correlated → Single root cause
- **Common Root Cause**: Database connection pool exhaustion
- **Impact**: 3 services affected (Order, Payment, Inventory)
- **Fix Priority**: CRITICAL - Single fix resolves all 5 errors
- **Confidence**: 95%

## Correlation Matrix

| Error | E1 | E2 | E3 | E4 | E5 |
|-------|----|----|----|----|----|
| E1: Order Timeout | 1.00 | 0.85 | 0.78 | 0.95 | 0.98 |
| E2: Payment Deadlock | 0.85 | 1.00 | 0.72 | 0.88 | 0.91 |
| E3: Inventory Fail | 0.78 | 0.72 | 1.00 | 0.90 | 0.85 |
| E4: Pool Limit | 0.95 | 0.88 | 0.90 | 1.00 | 0.99 |
| E5: Pool Timeout | 0.98 | 0.91 | 0.85 | 0.99 | 1.00 |

**Interpretation**: All correlations >0.7 (high) → Strong evidence of single root cause

## Root Cause
**Issue**: Database connections not disposed properly → Pool exhaustion
**Evidence**:
- All repositories create SqlConnection without `using` statement
- Connection pool limit: 100
- Peak concurrent requests: 150+ (exceeds pool)
- All errors occur when pool count reaches 100

## Fix Strategy
1. **Immediate** (2 hours): Add `using` statements to 9 repository methods
2. **Proper** (1-2 days): Refactor with base repository + increase pool size
3. **Comprehensive** (1 week): Prevention strategy (code analysis, monitoring, tests)

**Impact**: All 5 errors resolve with single fix (connection disposal)

## Output Files
- **Full Analysis**: marketplace/output/root-cause/error-correlation-20260116-135530.md
- **Summary**: marketplace/output/root-cause/error-correlation-20260116-135530-summary.md

## Recommended Action
1. **Immediate**: Apply hotfix (add using statements) - deploys in 2 hours
2. **Monitor**: Watch connection pool metrics after deployment
3. **Follow-up**: Implement proper solution and prevention strategy

## Next Steps
- Review full report for detailed fix implementation
- Apply immediate hotfix from report code examples
- Deploy and verify all errors resolve
- Schedule proper fix and prevention work
```

## FAQ

**Q: What if errors are unrelated?**
A: Agent will detect low correlation (<0.5) and analyze separately. Report will indicate no common root cause.

**Q: How many errors can it correlate?**
A: Default: 15 errors. Use --max-errors to adjust. More errors = longer analysis time.

**Q: Does it need stack traces?**
A: Helpful but not required. Correlation uses error types, messages, timing, and components.

**Q: What if errors span long time periods?**
A: Use --time-window to focus on incident window. Large windows may include false correlations.

**Q: Can it handle errors from different services?**
A: Yes, designed for multi-service correlation. Identifies shared dependencies (database, cache, etc.).

**Q: How long does analysis take?**
A: 35-55 minutes depending on error count and correlation complexity.

## Error Scenarios

### Too Few Errors (< 2)
```
⚠ Correlation requires at least 2 errors.

Provided: 1 error

For single error analysis, use:
/analyze-stacktrace

Cannot correlate with only 1 error.
```

### No Strong Correlation Found
```
✓ Correlation analysis complete - No strong correlation found.

Errors analyzed: 5
Average correlation: 0.32 (Low)
Interpretation: Errors appear unrelated (different root causes)

Recommendation: Analyze each error individually using /analyze-stacktrace

Report includes detailed analysis of each error.
```

### Large Time Window Warning
```
⚠ Error time window is large (72 hours).

Errors separated by long time periods may not be correlated.

Suggestion: Narrow to incident window (e.g., --time-window="1 hour")

Proceeding with full window, but results may include false correlations...
```

### Too Many Errors
```
⚠ Too many errors found (42 errors).

Filtering to top 15 most frequent errors:
- E1: 87 occurrences (included)
- E2: 56 occurrences (included)
...
- E15: 12 occurrences (included)
- E16: 8 occurrences (excluded)

Analyzing top 15. Full list in report appendix.
```

### File Not Found
```
❌ Error source not found: logs/production.log

Please verify:
- File path is correct
- File exists and is readable
- You have permission to access the file
```

## Integration with Other Commands

### Post-Incident Analysis Workflow
```bash
# Step 1: Correlate all errors from incident
/correlate-errors logs/incident-*.log --time-window="1 hour"

# Step 2: Find when root cause was introduced
/find-regression "Feature affected by root cause"

# Step 3: Find similar patterns to prevent recurrence
/analyze-bug-pattern "Pattern identified from root cause"

# Step 4: Apply comprehensive fix
# ... use all three reports for complete solution ...
```

### Production Monitoring Workflow
```bash
# Weekly: Correlate recent errors to find systemic issues
/correlate-errors logs/production-*.log --time-window="7 days" --min-correlation=0.7

# Address top correlated issues
# ... apply fixes from report ...

# Verify improvement in next week's analysis
```

### Pre-Release Testing
```bash
# After load testing, correlate any errors
/correlate-errors logs/loadtest-*.log

# Fix any correlated issues before release
# ... apply fixes ...

# Re-run load test to verify
```

## Log File Parsing

Agent can parse standard log formats:

**Supported Formats**:
- Plain text logs with timestamps
- JSON logs (structured)
- CSV logs
- .NET trace logs
- Java log4j logs
- Python logging logs
- Custom formats (auto-detected)

**Example Log Lines**:
```
2026-01-15 14:05:23 ERROR [OrderService] System.TimeoutException: Timeout waiting for database response
2026-01-15 14:12:10 ERROR [PaymentService] System.Data.SqlClient.SqlException: Transaction was deadlocked
2026-01-15 14:18:45 ERROR [InventoryService] System.InvalidOperationException: ExecuteReader requires open connection
```

Agent extracts:
- Timestamp: 2026-01-15 14:05:23
- Severity: ERROR
- Component: OrderService
- Exception: System.TimeoutException
- Message: "Timeout waiting for database response"

## Related Commands

- `/analyze-stacktrace` - Analyze individual error in detail before correlation
- `/find-regression` - Find when root cause was introduced
- `/analyze-bug-pattern` - Find similar patterns after identifying root cause
- `/analyze-impact` - Assess impact of fix before deployment

---

**Command Version**: 2.0.0
**Last Updated**: 2026-01-16
**Delegated To**: error-correlation-analyzer agent
**Expected Duration**: 35-55 minutes
**MCP Requirements**: None (local analysis only)
