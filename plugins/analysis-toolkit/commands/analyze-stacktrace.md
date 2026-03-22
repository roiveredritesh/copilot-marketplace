---
description: "Analyze error stack trace to identify root cause and solutions using parallel task execution"
argument-hint: "[--report=full|summary]"
allowed-tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Command: /analyze-stacktrace

## Usage

```
/analyze-stacktrace [--report=full|summary]
```

## Arguments

### No Required Arguments
- Stack trace is entered interactively or piped from file

### Optional Flags

- **--report=full|summary**: Report level (full by default)

## Examples

```bash
/analyze-stacktrace
[Paste error stack trace]

/analyze-stacktrace --report=summary
[Paste stack trace]
```

## Execution Model

**Parallel Sync Execution**: 3 tasks run concurrently for 2x faster analysis
- Total time: 4-6 minutes (vs 10-15 min sequential)
- All results synthesized into comprehensive root cause analysis
- Progress tracked in real-time

## Implementation

### Step 1: Parse Arguments
- Extract optional flags
- Set defaults
- Set report level
- Set output directory: `marketplace/output/analysis/stacktrace-<timestamp>/`

### Step 2: Get Stack Trace Input
- Prompt for input
- Read user input (multiple lines)
- Validate stack trace is present
- Extract error type for naming

### Step 3: Create Output Directory
- Create `marketplace/output/analysis/stacktrace-<timestamp>/` if not exists
- Save stack trace to file for reference
- Initialize progress tracking

### Step 4: Execute Parallel Analysis

⚠️ **CRITICAL**: You MUST invoke ALL 3 Task tools below in a SINGLE message to enable parallel execution. Do NOT invoke them sequentially. Send all Task tool calls in one message block.

**Task 1: Parse Stack Trace**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a stack trace parser. Analyze the provided stack trace and extract: error type, error message, call stack frames, file paths, line numbers, method names. Identify the immediate exception point and the full call chain. Detect language/framework (.NET, Java, Python, etc.). Save structured analysis to: marketplace/output/analysis/stacktrace-<timestamp>/parsed-trace.md with formatted breakdown of each frame."
- Expected output: `marketplace/output/analysis/stacktrace-<timestamp>/parsed-trace.md`
- Estimated time: 1-2 minutes

**Task 2: Find Error Source Code**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a source code locator. Use Grep to find the source files mentioned in the stack trace. For each file and line number in the trace, locate the actual code. Extract surrounding context (10 lines before/after). Read the code to understand what operation failed. Save findings to: marketplace/output/analysis/stacktrace-<timestamp>/source-code.md with code snippets and line numbers from the trace."
- Expected output: `marketplace/output/analysis/stacktrace-<timestamp>/source-code.md`
- Estimated time: 2-3 minutes

**Task 3: Search Similar Errors**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a similar error finder. Use Grep to search the codebase for similar error patterns, exception types, and error messages. Search for: same exception type, similar error messages, related catch blocks, previous fixes. Look in: logs, documentation, comments, git history. Save findings to: marketplace/output/analysis/stacktrace-<timestamp>/similar-errors.md with patterns, known solutions, and related issues."
- Expected output: `marketplace/output/analysis/stacktrace-<timestamp>/similar-errors.md`
- Estimated time: 2-3 minutes

### Step 5: Synthesize Final Report

After ALL 3 parallel tasks complete:
1. Read all 3 output files from `marketplace/output/analysis/stacktrace-<timestamp>/`
2. Combine findings into root cause analysis
3. Trace from exception point to actual root cause (not just symptom)
4. Identify contributing factors (data, timing, configuration, etc.)
5. Generate 3 solution approaches:
   - Quick fix (immediate workaround)
   - Proper fix (correct solution)
   - Prevention (avoid future occurrence)
6. Add code examples for each solution
7. Include testing recommendations
8. Save final report to: `marketplace/output/analysis/stacktrace-<timestamp>/analysis.md`

### Step 6: Display Progress and Results

Display execution progress in real-time:
```
Starting parallel stack trace analysis...

[1/3] ⏳ Parsing stack trace...
[2/3] ⏳ Finding error source code...
[3/3] ⏳ Searching similar errors...

[1/3] ✓ Parsed trace (1 min)
[2/3] ✓ Found source code (2 min)
[3/3] ✓ Searched similar errors (2 min)

Synthesizing results...
✓ Final report generated

# Stack Trace Analysis Summary

- **Error Type**: [exception type]
- **Root Cause**: [identified cause]
- **Impact**: [severity assessment]
- **Solution**: [recommended fix]

Full report: marketplace/output/analysis/stacktrace-<timestamp>/analysis.md
```

### Step 7: Return Response

Display completion status:
```
# ✓ Stack Trace Analysis Complete

**Execution Time**: 4-6 minutes (parallel)

**Output Files**:
- Full Analysis: marketplace/output/analysis/stacktrace-<timestamp>/analysis.md
- Parsed Trace: marketplace/output/analysis/stacktrace-<timestamp>/parsed-trace.md
- Source Code: marketplace/output/analysis/stacktrace-<timestamp>/source-code.md
- Similar Errors: marketplace/output/analysis/stacktrace-<timestamp>/similar-errors.md

**Root Cause Summary**:
- Error: [type]
- Cause: [root cause]
- Solution: [approach]

**Next Steps**:
1. Review the analysis.md for detailed root cause
2. Implement the recommended solution
3. Add tests to prevent recurrence
4. Update error handling if needed
5. Document the fix for future reference
```

## Supported Stack Trace Formats

- .NET (C#)
- Java
- JavaScript/Node.js
- Python
- Generic formats

## Output Locations

- Full Analysis: `marketplace/output/analysis/stacktrace-<timestamp>/analysis.md`
- Parsed Trace: `marketplace/output/analysis/stacktrace-<timestamp>/parsed-trace.md`
- Source Code: `marketplace/output/analysis/stacktrace-<timestamp>/source-code.md`
- Similar Errors: `marketplace/output/analysis/stacktrace-<timestamp>/similar-errors.md`

## Execution Time Comparison

**Parallel Execution (v2.0.0)**:
- Simple error: 3-4 minutes
- Complex stack: 4-6 minutes
- Deep analysis: 6-8 minutes

**Sequential Execution (v1.0.0)**:
- Simple error: 5-8 minutes
- Complex stack: 10-15 minutes
- Deep analysis: 15-20 minutes

**Speed improvement**: 2x faster with parallel execution

## FAQ

**Q: What formats are supported?**
A: .NET, Java, JavaScript, Python, and generic formats

**Q: Can it find root cause?**
A: Yes, traces through call stack to find actual root cause (not just symptom)

**Q: Will it suggest code changes?**
A: Yes, three levels: quick fix, proper fix, prevention

**Q: How does parallel execution work?**
A: 3 tasks (parse trace, find source, search similar) run concurrently, then results are synthesized

**Q: What if a parallel task fails?**
A: Other tasks continue. Synthesis step will note missing data and provide partial analysis

**Q: Can I paste from email/log?**
A: Yes, any stack trace format works

**Q: Where are reports saved?**
A: `marketplace/output/analysis/stacktrace-<timestamp>/analysis.md`

---

**Command Version**: 2.0.0
**Last Updated**: 2025-11-04
**Execution Model**: Parallel Sync (3 concurrent tasks)
**Expected Duration**: 4-6 minutes
**Uses Tasks**: Yes (3 parallel Task tool invocations)
