---
description: "Validate proposed solution for correctness and maintainability"
argument-hint: "<file-path> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write, Task]
---

# Command: /validate-solution

## Usage

```
/validate-solution <file-path> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **file-path**: Path to solution file to validate
  - Can be relative or absolute path
  - Supports C#, SQL, JavaScript, and other languages
  - Examples:
    - `src/Services/UserService.cs`
    - `Models/User.cs`
    - `Repository/UserRepository.cs`
    - `scripts/schema.sql`

### Optional Flags

- **--async**: Execute in background
  - Returns immediately with task ID
  - Validation happens asynchronously
  - Example: `/validate-solution src/Services/UserService.cs --async`

- **--wait**: Execute synchronously, block until complete
  - Waits for validation to complete
  - Returns full report
  - Example: `/validate-solution src/Services/UserService.cs --wait`
  - Default if neither flag specified

- **--report=full|summary**
  - `full`: Comprehensive validation report (default)
  - `summary`: Brief summary only
  - Example: `/validate-solution src/Services/UserService.cs --report=summary`

## Examples

### Example 1: Quick Validation (Sync, Full Report)
```
/validate-solution src/Services/UserService.cs --wait
```
Output:
```
Validating solution: src/Services/UserService.cs
[Analyzing code structure...]
[Checking logic correctness...]
[Assessing architecture...]
[Evaluating code quality...]
[Generating report...]

✅ Validation Complete!

Report: marketplace/output/reviews/UserService-validation.md

Key Findings:
- Correctness: ✅ PASS
- Architecture: ⚠️ Minor issues
- Code Quality: ✅ GOOD
- Overall Status: ⚠️ NEEDS IMPROVEMENT
```

### Example 2: Background Validation (Async)
```
/validate-solution Models/User.cs --async
```
Output:
```
Starting background validation...

Task ID: task-20251030-160030-val-xyz789
Status: Queued
Estimated time: 5-10 minutes

Check progress:
  /task-status task-20251030-160030-val-xyz789

When complete:
  marketplace/output/reviews/User-validation.md
```

### Example 3: Quick Summary (Async)
```
/validate-solution src/Repositories/UserRepository.cs --async --report=summary
```
Output:
```
Starting background validation (summary only)...

Task ID: task-20251030-160045-val-abc123
Estimated time: 3-6 minutes

Summary will be saved to:
  marketplace/output/reviews/UserRepository-validation-summary.md
```

### Example 4: Relative Path
```
/validate-solution ./Services/NewFeature.cs
```

### Example 5: SQL Script Validation
```
/validate-solution database/migrations/001-add-users-table.sql --wait
```

---

## Implementation

### Step 1: Parse and Validate Arguments

```
1. Parse input:
   - Extract file-path
   - Extract flags (--async, --wait, --report)
   - Normalize path (relative to current directory)

2. Validate parameters:
   - file-path not empty
   - Path doesn't contain invalid characters
   - Flags are recognized
   - No conflicting flags (--async and --wait together)

3. Set execution mode:
   - If --async: mode = async
   - If --wait: mode = sync
   - If neither: mode = sync (default)

4. Set report level:
   - If --report=summary: report_level = summary
   - If --report=full or not specified: report_level = full
```

### Step 2: File Existence and Access Check

```
1. Check file exists:
   - Resolve path to absolute
   - Verify file exists
   - If not found: Return error

2. Check file readable:
   - Verify read permissions
   - Check not locked by another process
   - If unreadable: Return permission error

3. Detect language/type:
   - Check file extension
   - Map to language (.cs=C#, .sql=SQL, .js=JavaScript, etc.)
   - Get appropriate rules for validation

4. Check file size:
   - If > 5000 lines: Return warning, suggest async
   - If > 10000 lines: Return warning about analysis completeness
   - Proceed anyway
```

### Step 3: Queue or Execute Validation Task

**For Async Execution:**
```
1. Create task entry in .claude/task-queue.json:
   {
     "task_id": "task-20251030-160030-val-xyz789",
     "type": "solution-validate",
     "status": "queued",
     "file_path": "src/Services/UserService.cs",
     "report_level": "full",
     "created": "2025-10-30T16:00:30Z",
     "estimated_completion": "2025-10-30T16:08:00Z"
   }

2. Return immediately:
   Task ID: task-20251030-160030-val-xyz789
   Status: Queued
   Estimated time: 5-10 minutes
   Check: /task-status task-20251030-160030-val-xyz789

3. Background task coordinator processes the task
   - Reads solution file
   - Analyzes code structure
   - Checks logic correctness
   - Assesses architecture
   - Evaluates code quality
   - Generates comprehensive report
   - Updates task status
```

**For Sync Execution:**
```
1. Display progress:
   Validating solution: src/Services/UserService.cs
   [Analyzing code structure...]
   [Checking logic correctness...]
   [Assessing architecture...]
   [Evaluating code quality...]
   [Generating report...]

2. Delegate to solution-validator agent
   - Wait for agent to complete
   - Receive report data

3. Display report or summary
   - Full report: Show all details
   - Summary: Show key findings only

4. Return completion message with report location
```

### Step 4: Return Response

**Async Response:**
```
Status: Queued
Task ID: task-20251030-160030-val-xyz789
Estimated time: 5-10 minutes

Check progress:
  /task-status task-20251030-160030-val-xyz789

Report will be saved to:
  marketplace/output/reviews/UserService-validation.md
```

**Sync Response (Full Report):**
```
# Solution Validation Report

**Solution File**: src/Services/UserService.cs
[Full report content]

Report saved to: marketplace/output/reviews/UserService-validation.md
```

**Sync Response (Summary):**
```
# Solution Validation Summary

**File**: src/Services/UserService.cs

## Key Assessment
- Correctness: ⚠️ ISSUES FOUND
- Architecture: ✅ GOOD
- Code Quality: ✅ GOOD

## Critical Issues
1. Null reference at line 42
2. Off-by-one error at line 67

## Recommendations
- Fix critical issues before use
- Consider interface segregation

Full report: marketplace/output/reviews/UserService-validation.md
```

---

## Input Validation

### Valid Inputs
```
✅ /validate-solution src/Services/UserService.cs
✅ /validate-solution src/Services/UserService.cs --wait
✅ /validate-solution src/Services/UserService.cs --async
✅ /validate-solution src/Services/UserService.cs --async --report=summary
✅ /validate-solution ./Models/User.cs
✅ /validate-solution C:\Projects\App\Services\Service.cs
✅ /validate-solution database/schema.sql
```

### Invalid Inputs
```
❌ /validate-solution                    (no file path)
❌ /validate-solution ""                 (empty path)
❌ /validate-solution nonexistent.cs     (file doesn't exist)
❌ /validate-solution src/file.cs --wait --async  (conflicting flags)
❌ /validate-solution src/file.cs --report=invalid (invalid report type)
```

### Error Messages

**Missing File Path:**
```
Error: File path required
Usage: /validate-solution <file-path> [--async|--wait] [--report=full|summary]
Example: /validate-solution src/Services/UserService.cs
```

**File Not Found:**
```
Error: Solution file not found
Path: src/Services/UserService.cs
Current directory: C:\Projects\MyApp

Tip: Use relative path from project root or absolute path
```

**Permission Denied:**
```
Error: Cannot read file (permission denied)
Path: src/Services/UserService.cs

Solution:
1. Check file permissions
2. Ensure file is not locked
3. Try again
```

**File Too Large:**
```
Warning: File is very large (5234 lines)
Analysis may take longer and be less detailed.

Recommendation: Use --async for better timeout handling
```

**Unknown File Type:**
```
Warning: Unknown file type (.xyz)
Will apply generic code review principles.
Language-specific checks may be limited.
```

---

## Output Locations

### Validation Reports
```
Full Report:   marketplace/output/reviews/<filename>-validation.md
Summary:       marketplace/output/reviews/<filename>-validation-summary.md
Status:        .claude/task-status/<task-id>.md
```

### Example Paths
```
marketplace/output/reviews/UserService-validation.md
marketplace/output/reviews/User-validation-summary.md
.claude/task-status/task-20251030-160030-val-xyz789.md
```

---

## Typical Analysis Time

- **Small file** (< 100 lines): 2-4 minutes
- **Medium file** (100-500 lines): 5-10 minutes
- **Large file** (500-2000 lines): 10-20 minutes
- **Very large file** (> 2000 lines): 20-30 minutes

**Recommendation**: Use `--async` for files larger than 500 lines.

---

## Supported Languages

### C# / .NET
```
Extensions: .cs
Features:
- SOLID principles assessment
- Async/await validation
- LINQ query optimization
- Memory management review
- Exception handling analysis
- Design pattern evaluation
```

### SQL
```
Extensions: .sql
Features:
- Query correctness analysis
- Performance optimization suggestions
- Index recommendations
- JOIN efficiency assessment
- NULL handling review
```

### JavaScript
```
Extensions: .js, .ts
Features:
- Logic correctness
- Async pattern validation
- Memory leak detection
- Performance analysis
- Code quality assessment
```

### Other Languages
```
Extensions: Any others (.py, .java, .go, etc.)
Features:
- Generic code quality analysis
- Logic correctness
- Code organization
- Maintainability assessment
```

---

## Validation Areas

### Logic & Correctness
- Parameter validation
- Return value handling
- Edge case coverage
- Off-by-one errors
- Infinite loops
- Null reference handling

### Architecture & Design
- SOLID principles (C#)
- Design patterns
- Separation of concerns
- Testability
- Extensibility
- Code organization

### Code Quality
- Readability
- Complexity
- Duplication
- Documentation
- Naming conventions
- Code formatting

### Performance
- Algorithm efficiency
- Database query optimization
- Memory usage
- Caching strategies
- Resource management

### Security
- Input validation
- Hardcoded secrets
- SQL injection risks
- XSS prevention
- Authentication/authorization

---

## Integration with Development

### Validation Triggers

1. **Before Implementation**
   ```
   /validate-solution src/NewFeature.cs
   Review issues before implementing
   ```

2. **Before PR Submission**
   ```
   /validate-solution src/ChangedFile.cs
   Self-review before asking for review
   ```

3. **Design Review**
   ```
   /validate-solution architecture/NewComponent.cs
   Get feedback on new design
   ```

4. **Code Refactoring**
   ```
   /validate-solution src/Refactored.cs
   Ensure refactoring maintains quality
   ```

---

## Report Contents

A comprehensive validation report includes:

1. **Executive Summary**
   - Overall assessment
   - Severity of issues
   - Key recommendations

2. **Correctness Assessment**
   - Logic analysis
   - Edge cases
   - Control flow

3. **Architecture Assessment**
   - SOLID principles
   - Design patterns
   - Code organization

4. **Code Quality**
   - Readability
   - Complexity
   - Documentation

5. **Issues By Severity**
   - Critical (must fix)
   - Major (should fix)
   - Minor (nice to fix)

6. **Recommendations**
   - Before implementation
   - Design improvements
   - Testing recommendations

7. **Alternative Approaches**
   - Different solutions
   - Pros/cons analysis

8. **Risk Assessment**
   - Implementation risk
   - Maintainability risk
   - Performance risk

---

## Related Commands

- `/task-status <task-id>` - Check validation progress
- `/review-pr <owner>/<repo> <number>` - Review GitHub PRs
- `/analyze-stacktrace` - Analyze error traces
- `/analyze-impact <file>` - Analyze code change impact

---

## FAQ

**Q: What file types are supported?**
A: C#, SQL, JavaScript, and other languages. Each has language-specific checks.

**Q: How deep is the validation?**
A: Very thorough! Covers correctness, architecture, quality, performance, and security.

**Q: What if I have errors in my code?**
A: The validation identifies errors and suggests fixes. It's designed to help improve code.

**Q: Can I validate multiple files?**
A: Yes! Run the command for each file. Use `--async` to queue multiple validations.

**Q: How long does validation take?**
A: Typical times:
- Small file: 2-4 minutes
- Medium file: 5-10 minutes
- Large file: 10-20 minutes

**Q: What if the file has syntax errors?**
A: The validation will note syntax errors and may provide limited analysis.

**Q: Can I export the validation report?**
A: Yes! Reports are markdown files in `marketplace/output/reviews/`.

**Q: How is this different from a linter?**
A: More comprehensive than linters:
- Linters check style and basic correctness
- Validation covers correctness, architecture, design, quality, and risk

**Q: Can I validate while developing?**
A: Yes! Validate incomplete work to get feedback early.

**Q: What if the file uses patterns I don't want to follow?**
A: The validation is based on industry best practices. Discuss with your team about customization.

---

## Pro Tips

**Tip 1: Use Async for Large Files**
Large files take longer. Use `--async`:
```
/validate-solution src/LargeService.cs --async
```

**Tip 2: Quick Assessment**
Need just key findings? Use summary:
```
/validate-solution src/Service.cs --report=summary
```

**Tip 3: Validate Early**
Get feedback before full implementation:
```
/validate-solution src/NewFeature.cs
```

**Tip 4: Batch Validations**
Queue multiple validations:
```
/validate-solution src/Service1.cs --async
/validate-solution src/Service2.cs --async
/validate-solution src/Service3.cs --async
```

**Tip 5: Check Progress**
Monitor async validations:
```
/task-status task-20251030-160030-val-xyz789
```

**Tip 6: Design Review**
Use validation for architecture discussion:
1. Run validation on proposed design
2. Share report with team
3. Discuss findings together

**Tip 7: Self-Review Before PR**
Validate before requesting review:
```
/validate-solution src/MyChange.cs --wait
Fix issues
Submit PR with confidence
```

---

## Troubleshooting

### File Not Found
```
Error: Solution file not found
Path: src/Services/Service.cs

Solution:
1. Check file path is correct
2. Verify file exists
3. Use absolute path if needed
```

### Permission Denied
```
Error: Cannot read file (permission denied)

Solution:
1. Check file is not locked
2. Verify read permissions
3. Close file in editor if open
```

### Timeout (Async)
```
Error: Validation timed out after 30 minutes

Solution:
1. Very large files may timeout
2. Try splitting into smaller files
3. Check file has no infinite loops
```

### Unknown Language
```
Warning: Unknown file type (.xyz)

Solution:
1. Validation still works with generic analysis
2. Language-specific checks won't apply
3. Results may be less detailed
```

---

## Command Lifecycle

```
1. User runs: /validate-solution src/UserService.cs

2. Command validates:
   - File path provided
   - File exists and readable
   - Flags recognized

3. Command queues task:
   - Creates task entry in queue
   - Sets status to "queued"
   - Assigns task ID

4. Background coordinator processes:
   - Picks up task from queue
   - Delegates to solution-validator agent
   - Agent analyzes solution
   - Agent generates report

5. Report saved:
   - marketplace/output/reviews/UserService-validation.md

6. User checks progress:
   - /task-status <task-id>
   - Views report when ready
```

---

## Best Practices

1. **Validate Early**
   - Validate before implementation
   - Get feedback while designing

2. **Read Full Report**
   - Don't just look at summary
   - Understand all recommendations

3. **Act on Critical Issues**
   - Fix all critical/major issues
   - Discuss minor issues with team

4. **Use for Learning**
   - Validation helps improve skills
   - Learn from recommendations

5. **Share Findings**
   - Share reports with team
   - Discuss improvements together

6. **Iterate**
   - Implement recommendations
   - Revalidate if major changes
   - See improvement over time

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Associated Plugin**: Review Suite
**Delegated To**: solution-validator agent
**Task Coverage**: Task #11 (Find correct maintainable solutions)
