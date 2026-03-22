---
description: "Analyze impact of code changes on other components using parallel task execution"
argument-hint: "<file-path> [--report=full|summary]"
allowed-tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Command: /analyze-impact

## Usage

```
/analyze-impact <file-path> [--report=full|summary]
```

## Arguments

### Required Arguments

- **file-path**: Path to changed file (e.g., src/Services/UserService.cs)

### Optional Flags

- **--report=full|summary**: Report level (full by default)

## Examples

```bash
/analyze-impact src/Services/UserService.cs
/analyze-impact Models/User.cs --report=summary
/analyze-impact Repository/DataAccess.cs
```

## Execution Model

**Parallel Sync Execution**: 4 tasks run concurrently for 2-3x faster analysis
- Total time: 8-10 minutes (vs 20-30 min sequential)
- All results synthesized into comprehensive impact report
- Progress tracked in real-time

## Implementation

### Step 1: Parse Arguments
- Extract file path: `${FILE_PATH}`
- Validate path exists and is readable
- Parse optional report level flag
- Set output directory: `marketplace/output/analysis/impact-<filename>/`

### Step 2: Validate File
- Check file exists
- Verify readable
- Confirm it's code
- Extract filename for reporting

### Step 3: Create Output Directory
- Create `marketplace/output/analysis/impact-<filename>/` if not exists
- Initialize progress tracking

### Step 4: Execute Parallel Analysis

⚠️ **CRITICAL**: You MUST invoke ALL 4 Task tools below in a SINGLE message to enable parallel execution. Do NOT invoke them sequentially. Send all Task tool calls in one message block.

**Task 1: Search Dependencies**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a dependency analyzer. Search the codebase for all import/using statements and dependencies related to ${FILE_PATH}. Use Grep to find: imports, using statements, package references. Identify all files that depend on this file and what classes/methods they use. Save findings to: marketplace/output/analysis/impact-<filename>/dependencies.md with structured list of dependent files and their usage patterns."
- Expected output: `marketplace/output/analysis/impact-<filename>/dependencies.md`
- Estimated time: 2-3 minutes

**Task 2: Trace References**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a reference tracer. Use Grep to find all references to classes, methods, and properties defined in ${FILE_PATH}. Search across entire codebase for usages. Include line numbers and context. Identify: method calls, property accesses, class instantiations, inheritance relationships. Save to: marketplace/output/analysis/impact-<filename>/references.md with file paths, line numbers, and usage context."
- Expected output: `marketplace/output/analysis/impact-<filename>/references.md`
- Estimated time: 3-4 minutes

**Task 3: Check Imports and Relationships**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are an import relationship analyzer. Use Grep to search for files that import/reference ${FILE_PATH}. Find: namespace usages, class references, method signatures that match. Build dependency graph showing which components would be affected by changes. Save to: marketplace/output/analysis/impact-<filename>/import-relationships.md with hierarchical structure of dependencies."
- Expected output: `marketplace/output/analysis/impact-<filename>/import-relationships.md`
- Estimated time: 2-3 minutes

**Task 4: Assess Breaking Change Risk**
- Use: Task tool with subagent_type: "general-purpose"
- Prompt: "You are a breaking change analyzer. Read ${FILE_PATH} and analyze its public interface: public methods, properties, classes, interfaces. Identify what changes would break existing consumers. Use Grep to find callers of each public member. Assess risk level (HIGH/MEDIUM/LOW) for changes to each member. Save to: marketplace/output/analysis/impact-<filename>/breaking-change-risk.md with risk assessment for each public member."
- Expected output: `marketplace/output/analysis/impact-<filename>/breaking-change-risk.md`
- Estimated time: 3-4 minutes

### Step 5: Synthesize Final Report

After ALL 4 parallel tasks complete:
1. Read all 4 output files from `marketplace/output/analysis/impact-<filename>/`
2. Combine findings into comprehensive impact analysis
3. Calculate total impact radius (number of affected files/components)
4. Identify high-risk areas and breaking changes
5. Generate impact severity assessment (critical/high/medium/low)
6. Provide recommendations:
   - Safe changes (low risk)
   - Changes requiring updates (medium risk)
   - Breaking changes requiring migration (high risk)
7. Add mitigation strategies and testing recommendations
8. Save final report to: `marketplace/output/analysis/impact-<filename>/analysis.md`

### Step 6: Display Progress and Results

Display execution progress in real-time:
```
Starting parallel impact analysis of ${FILE_PATH}...

[1/4] ⏳ Searching dependencies...
[2/4] ⏳ Tracing references...
[3/4] ⏳ Checking imports and relationships...
[4/4] ⏳ Assessing breaking change risk...

[1/4] ✓ Searched dependencies (2 min)
[2/4] ✓ Traced references (3 min)
[3/4] ✓ Checked imports (2 min)
[4/4] ✓ Assessed breaking changes (3 min)

Synthesizing results...
✓ Final report generated

# Impact Analysis Summary for ${FILE_PATH}

- **Files Affected**: [count] files
- **Components Impacted**: [list of components]
- **Breaking Changes**: [HIGH/MEDIUM/LOW risk]
- **Recommendation**: [safe to change / requires updates / migration needed]

Full report: marketplace/output/analysis/impact-<filename>/analysis.md
```

### Step 7: Return Response

Display completion status:
```
# ✓ Impact Analysis Complete: ${FILE_PATH}

**Execution Time**: 8-10 minutes (parallel)

**Output Files**:
- Full Analysis: marketplace/output/analysis/impact-<filename>/analysis.md
- Dependencies: marketplace/output/analysis/impact-<filename>/dependencies.md
- References: marketplace/output/analysis/impact-<filename>/references.md
- Import Relationships: marketplace/output/analysis/impact-<filename>/import-relationships.md
- Breaking Change Risk: marketplace/output/analysis/impact-<filename>/breaking-change-risk.md

**Impact Summary**:
- Files Affected: [count]
- Components: [list]
- Risk Level: [assessment]

**Next Steps**:
1. Review the analysis.md for detailed impact assessment
2. Identify all files that need updates
3. Plan migration strategy if breaking changes
4. Update tests to cover affected areas
5. Communicate changes to team if high impact
```

## Output Locations

- Full Analysis: `marketplace/output/analysis/impact-<filename>/analysis.md`
- Dependencies: `marketplace/output/analysis/impact-<filename>/dependencies.md`
- References: `marketplace/output/analysis/impact-<filename>/references.md`
- Import Relationships: `marketplace/output/analysis/impact-<filename>/import-relationships.md`
- Breaking Change Risk: `marketplace/output/analysis/impact-<filename>/breaking-change-risk.md`

## Execution Time Comparison

**Parallel Execution (v2.0.0)**:
- Small file: 6-8 minutes
- Medium file: 8-10 minutes
- Large file: 10-12 minutes

**Sequential Execution (v1.0.0)**:
- Small file: 10-15 minutes
- Medium file: 15-20 minutes
- Large file: 20-30 minutes

**Speed improvement**: 2-3x faster with parallel execution

## FAQ

**Q: What types of changes are analyzed?**
A: All code changes - methods, classes, properties, interfaces, etc.

**Q: How accurate is the impact assessment?**
A: Very accurate - searches entire codebase for references and dependencies

**Q: Can it detect breaking changes?**
A: Yes, identifies changes to public interfaces that would break consumers

**Q: How does parallel execution work?**
A: 4 tasks (dependencies, references, imports, breaking changes) run concurrently, then results are synthesized

**Q: What if a parallel task fails?**
A: Other tasks continue. Synthesis step will note missing data and provide partial analysis

**Q: Can I run this command multiple times in parallel?**
A: Yes, each invocation uses separate output directories

---

**Command Version**: 2.0.0
**Last Updated**: 2025-11-04
**Execution Model**: Parallel Sync (4 concurrent tasks)
**Expected Duration**: 8-10 minutes
**Uses Tasks**: Yes (4 parallel Task tool invocations)
