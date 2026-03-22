---
description: "Analyze existing system architecture and provide recommendations"
argument-hint: "<directory-path> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write]
---

# Command: /analyze-architecture

## Usage

```
/analyze-architecture <directory-path> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **directory-path**: Path to project root or code directory
  - Example: `/analyze-architecture src/`
  - Example: `/analyze-architecture C:\Projects\MyApp`

### Optional Flags

- **--async**: Execute in background
- **--wait**: Execute synchronously (default)
- **--report=full|summary**: Report level (full by default)

## Examples

```bash
# Analyze project architecture (synchronous)
/analyze-architecture src/ --wait

# Background analysis
/analyze-architecture . --async

# Summary only
/analyze-architecture C:\Projects\MyApp --report=summary
```

## Implementation

### Step 1: Parse Arguments
- Extract directory path
- Validate path exists
- Set execution mode
- Set report level

### Step 2: Validate Directory
- Check directory is readable
- Verify contains code files
- Detect project type

### Step 3: Queue/Execute Task
- For async: Create task, return task ID
- For sync: Delegate to architecture-analyzer agent

### Step 4: Delegate to Agent
- Analyze codebase structure
- Identify architectural patterns
- Evaluate architecture quality
- Detect anti-patterns
- Generate recommendations

### Step 5: Return Response

**Async**:
```
Task ID: task-20251030-190000-arch-abc
Estimated time: 12-20 minutes
```

**Sync**:
```
# Architecture Analysis: MyApp

[Detailed architecture report]

Report: marketplace/output/reviews/MyApp-architecture-analysis.md
```

## Output Locations

- Analysis: `marketplace/output/reviews/<project>-architecture-analysis.md`
- Summary: `marketplace/output/reviews/<project>-architecture-summary.md`
- Status: `.claude/task-status/<task-id>.md`

## Typical Analysis Time

- Small project: 8-12 minutes
- Medium project: 12-20 minutes
- Large project: 20-30 minutes

**Recommendation**: Use `--async` for large projects.

## FAQ

**Q: What languages are supported?**
A: C#, JavaScript, Python, Java - detected automatically

**Q: What does it analyze?**
A: Structure, patterns, SOLID principles, anti-patterns, issues

**Q: Will it modify code?**
A: No, analysis only - read-only

**Q: Where are reports saved?**
A: `marketplace/output/reviews/`

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Delegated To**: architecture-analyzer agent
**Task Coverage**: Task #7
