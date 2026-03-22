---
description: "Analyze and optimize algorithm or code performance"
argument-hint: "<file-path> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write]
---

# Command: /optimize-algorithm

## Usage

```
/optimize-algorithm <file-path> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **file-path**: Path to code file to analyze
  - Can be relative or absolute path
  - Supports C#, JavaScript, Python, Java, and other languages
  - Examples:
    - `src/Services/UserService.cs`
    - `algorithms/SortHelper.js`
    - `utils/DataProcessor.py`

### Optional Flags

- **--async**: Execute in background
  - Returns immediately with task ID
  - Analysis happens asynchronously
  - Example: `/optimize-algorithm src/Services/UserService.cs --async`

- **--wait**: Execute synchronously, block until complete
  - Waits for analysis to complete
  - Returns full report
  - Example: `/optimize-algorithm src/Services/UserService.cs --wait`
  - Default if neither flag specified

- **--report=full|summary**
  - `full`: Comprehensive optimization report (default)
  - `summary`: Brief summary of findings
  - Example: `/optimize-algorithm src/Services/UserService.cs --report=summary`

## Examples

### Example 1: Quick Analysis (Sync, Full Report)
```
/optimize-algorithm src/Services/UserService.cs --wait
```
Output:
```
Analyzing algorithm: src/Services/UserService.cs
[Parsing code structure...]
[Analyzing complexity...]
[Identifying bottlenecks...]
[Generating recommendations...]

✅ Analysis Complete!

Report: marketplace/output/reviews/UserService-algorithm-optimization.md

Key Findings:
- O(n²) nested loop in ProcessUsers (95% improvement possible)
- O(n) linear search in FindUser (could be O(log n))
- Repeated calculation in ValidateUsers (75% improvement)

Quick Fix (15 min, +95% faster):
- Replace nested loop with HashSet lookup
- Cache calculation result
```

### Example 2: Background Analysis (Async)
```
/optimize-algorithm Models/User.cs --async
```
Output:
```
Starting background analysis...

Task ID: task-20251030-170030-algo-xyz789
Status: Queued
Estimated time: 8-15 minutes

Check progress:
  /task-status task-20251030-170030-algo-xyz789

When complete:
  marketplace/output/reviews/User-algorithm-optimization.md
```

### Example 3: Quick Summary (Async)
```
/optimize-algorithm Repository/DataAccess.cs --async --report=summary
```
Output:
```
Starting background analysis (summary only)...

Task ID: task-20251030-170045-algo-abc123
Estimated time: 5-8 minutes

Summary will be saved to:
  marketplace/output/reviews/DataAccess-algorithm-optimization-summary.md
```

---

## Implementation

### Step 1: Parse and Validate Arguments

```
1. Parse input:
   - Extract file-path
   - Extract flags (--async, --wait, --report)
   - Normalize path

2. Validate parameters:
   - file-path not empty
   - Flags are recognized
   - No conflicting flags

3. Set execution mode:
   - If --async: mode = async
   - If --wait: mode = sync
   - If neither: mode = sync (default)

4. Set report level:
   - If --report=summary: level = summary
   - If --report=full or not specified: level = full
```

### Step 2: File Validation

```
1. Check file exists:
   - Resolve path
   - Verify file exists
   - If not found: Return error

2. Check file readable:
   - Verify read permissions
   - Check not locked
   - If unreadable: Return error

3. Detect language:
   - Check file extension
   - Identify language type
   - Get appropriate analysis rules

4. Check file size:
   - If > 5000 lines: Warn, suggest --async
   - If > 10000 lines: Warn about completeness
   - Proceed anyway
```

### Step 3: Queue or Execute Analysis Task

**For Async Execution:**
```
1. Create task entry:
   {
     "task_id": "task-20251030-170030-algo-xyz789",
     "type": "algorithm-optimize",
     "file_path": "src/Services/UserService.cs",
     "report_level": "full",
     "created": "2025-10-30T17:00:30Z",
     "estimated_completion": "2025-10-30T17:15:00Z"
   }

2. Return immediately:
   Task ID: task-20251030-170030-algo-xyz789
   Status: Queued
   Estimated time: 8-15 minutes

3. Background coordinator processes:
   - Reads code file
   - Analyzes algorithm complexity
   - Identifies bottlenecks
   - Suggests optimizations
   - Generates optimization report
```

**For Sync Execution:**
```
1. Display progress:
   Analyzing algorithm: src/Services/UserService.cs
   [Parsing code structure...]
   [Analyzing complexity...]
   [Identifying bottlenecks...]
   [Generating recommendations...]

2. Delegate to algorithm-optimizer agent
   - Wait for completion
   - Receive analysis data

3. Display report or summary
   - Full: Show all analysis
   - Summary: Show key findings

4. Return completion with report location
```

### Step 4: Return Response

**Async Response:**
```
Status: Queued
Task ID: task-20251030-170030-algo-xyz789
Estimated time: 8-15 minutes

Check progress:
  /task-status task-20251030-170030-algo-xyz789

Report will be saved to:
  marketplace/output/reviews/UserService-algorithm-optimization.md
```

**Sync Response (Full Report):**
```
# Algorithm Optimization Report

**File**: src/Services/UserService.cs
**Analysis Time**: 12 minutes

## Key Findings
1. O(n²) nested loop (95% improvement possible)
2. O(n) linear search (could be O(log n))
3. Repeated calculation (75% improvement)

[Full report content...]

Report saved to: marketplace/output/reviews/UserService-algorithm-optimization.md
```

---

## Input Validation

### Valid Inputs
```
✅ /optimize-algorithm src/Services/UserService.cs
✅ /optimize-algorithm src/Services/UserService.cs --wait
✅ /optimize-algorithm src/Services/UserService.cs --async
✅ /optimize-algorithm src/Services/UserService.cs --async --report=summary
✅ /optimize-algorithm ./Models/User.cs
✅ /optimize-algorithm algorithms/Sort.js
```

### Invalid Inputs
```
❌ /optimize-algorithm                           (no file path)
❌ /optimize-algorithm ""                        (empty path)
❌ /optimize-algorithm nonexistent.cs            (file doesn't exist)
❌ /optimize-algorithm src/file.cs --wait --async  (conflicting)
❌ /optimize-algorithm src/file.cs --report=invalid (bad report type)
```

### Error Messages

**Missing File Path:**
```
Error: File path required
Usage: /optimize-algorithm <file-path> [--async|--wait] [--report=full|summary]
Example: /optimize-algorithm src/Services/UserService.cs
```

**File Not Found:**
```
Error: Code file not found: src/Services/UserService.cs
Current directory: C:\Projects\MyApp

Try:
  1. Check file path is correct
  2. Use absolute path if needed
  3. Verify file exists

Examples:
  /optimize-algorithm ./src/Services/UserService.cs
  /optimize-algorithm C:\Projects\MyApp\src\Services\UserService.cs
```

**Permission Denied:**
```
Error: Cannot read file (permission denied)
Path: src/Services/UserService.cs

Solution:
1. Check file is not locked
2. Verify read permissions
3. Try closing in editor
```

**File Too Large:**
```
Warning: File is very large (5234 lines)
Analysis may take longer or be less complete.

Recommendation: Use --async for better timeout handling
```

---

## Output Locations

### Report Files
```
Full Analysis:     marketplace/output/reviews/<filename>-algorithm-optimization.md
Summary:           marketplace/output/reviews/<filename>-algorithm-optimization-summary.md
Status:            .claude/task-status/<task-id>.md
```

### Examples
```
marketplace/output/reviews/UserService-algorithm-optimization.md
marketplace/output/reviews/Sort-algorithm-optimization-summary.md
.claude/task-status/task-20251030-170030-algo-xyz789.md
```

---

## Typical Analysis Time

- **Small file** (< 100 lines): 2-4 minutes
- **Medium file** (100-500 lines): 5-10 minutes
- **Large file** (500-2000 lines): 10-20 minutes
- **Very large file** (> 2000 lines): 20-30 minutes

**Recommendation**: Use `--async` for files larger than 500 lines.

---

## What Gets Analyzed

### Complexity Analysis
- Time complexity (O(1), O(n), O(n²), etc.)
- Space complexity
- Nested operations
- Recursive calls

### Performance Bottlenecks
- O(n²) nested loops
- Inefficient data structures
- Repeated expensive operations
- Linear searches (when binary search possible)
- String concatenation in loops

### Code Quality
- Algorithm efficiency
- Data structure choices
- Memory usage
- Resource management

### Optimization Recommendations
- Quick fix (minimal effort, significant improvement)
- Proper fix (moderate effort, good improvement)
- Comprehensive solution (major refactoring, maximum improvement)

---

## Supported Languages

### C# / .NET
```
Extensions: .cs
Analysis includes:
- LINQ efficiency
- Async/await patterns
- Collection usage (List vs HashSet)
- Method complexity
- Loop optimization
```

### JavaScript / TypeScript
```
Extensions: .js, .ts
Analysis includes:
- Array operations efficiency
- Nested loop detection
- Sorting usage
- Promise/async patterns
- Algorithm complexity
```

### Python
```
Extensions: .py
Analysis includes:
- List comprehension efficiency
- Loop optimization
- Algorithm complexity
- Data structure choices
```

### Java
```
Extensions: .java
Analysis includes:
- Collection usage
- Algorithm complexity
- Loop efficiency
- Object creation patterns
```

### Other Languages
```
Generic analysis available for any language
- Algorithm complexity assessment
- Loop and condition analysis
- Method/function efficiency
- Data structure evaluation
```

---

## Common Optimizations

### Optimization 1: Replace Nested Loop
```
Problem: O(n²) nested loop
Solution: Use HashSet for O(1) lookup
Impact: 100K items: 12 sec → 0.06 sec (99% faster)
```

### Optimization 2: Use Correct Data Structure
```
Problem: List.Contains() in loop O(n)
Solution: Use HashSet.Contains() O(1)
Impact: 100K items: 12 sec → 0.06 sec (99% faster)
```

### Optimization 3: Cache Expensive Calculation
```
Problem: Repeated calculation in loop
Solution: Calculate once, reuse
Impact: 100 items: 50ms → 5ms (90% faster)
```

### Optimization 4: Binary Search
```
Problem: Linear search on sorted data O(n)
Solution: Use binary search O(log n)
Impact: 10K items: 80ms → 2ms (97% faster)
```

### Optimization 5: String StringBuilder
```
Problem: String concatenation in loop
Solution: Use StringBuilder
Impact: 1000 items: 150ms → 2ms (98% faster)
```

---

## Related Commands

- `/task-status <task-id>` - Check analysis progress
- `/optimize-query <query-name>` - Optimize database queries
- `/analyze-impact <file>` - Analyze code change impact
- `/validate-solution <file>` - Validate solution correctness

---

## FAQ

**Q: What languages are supported?**
A: C#, JavaScript, Python, Java, and generic analysis for others.

**Q: Can it suggest specific code?**
A: Yes! Reports include optimized code examples.

**Q: How accurate are recommendations?**
A: Very accurate! Based on algorithm analysis and complexity theory.

**Q: Will optimization change logic?**
A: No! Optimizations produce same results, just faster.

**Q: What if I disagree with recommendation?**
A: You decide what to implement. Recommendations are guidance.

**Q: Can I optimize while writing code?**
A: Yes! Get feedback early on algorithm choices.

**Q: Where are recommendations saved?**
A: `marketplace/output/reviews/<filename>-algorithm-optimization.md`

**Q: What if the file has errors?**
A: Analysis will note errors and may provide limited feedback.

---

## Pro Tips

**Tip 1: Analyze Early**
Get performance feedback before finishing implementation.

**Tip 2: Compare Approaches**
Report shows multiple optimization levels to choose from.

**Tip 3: Quick Wins First**
Implement quick fixes for immediate improvement.

**Tip 4: Learn Patterns**
Use report to understand optimization patterns.

**Tip 5: Share Results**
Save reports to document optimization decisions.

---

## Troubleshooting

### File Not Found
```
Solution:
1. Check file path is correct
2. Use relative path from project root
3. Try absolute path if needed
```

### Permission Denied
```
Solution:
1. Check file is not locked in editor
2. Verify read permissions
3. Close file if open and retry
```

### Very Large File
```
Solution:
1. Use --async for better handling
2. Consider breaking into smaller methods
3. Analysis may take longer
```

### Unknown Language
```
Solution:
1. Generic analysis still applies
2. Language-specific optimizations unavailable
3. Results may be less detailed
```

---

## Command Lifecycle

```
1. User: /optimize-algorithm src/UserService.cs --wait

2. Command validates:
   - File path provided
   - File exists and is readable
   - Flags are recognized

3. Delegates to algorithm-optimizer agent:
   - Reads code file
   - Analyzes algorithm complexity
   - Identifies bottlenecks
   - Suggests optimizations
   - Generates report

4. Report saved:
   marketplace/output/reviews/UserService-algorithm-optimization.md

5. User reviews:
   - Examines recommendations
   - Understands complexity
   - Implements improvements
   - Tests performance
```

---

## Best Practices

1. **Analyze Early**: Don't wait until code is deployed
2. **Test Changes**: Verify optimizations work correctly
3. **Measure Impact**: Before/after performance comparison
4. **Document**: Explain why optimization was made
5. **Code Review**: Have team review optimization changes
6. **Monitor**: Watch for performance regressions

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Associated Plugin**: Optimization Engine
**Delegated To**: algorithm-optimizer agent
**Task Coverage**: Task #6 (Optimize algorithms and code performance)
