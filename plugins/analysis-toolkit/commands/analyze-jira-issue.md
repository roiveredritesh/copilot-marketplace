---
description: "Analyze Jira issue and extract bug/issue information with root cause analysis"
argument-hint: "<ticket-number> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write]
---

# Command: /analyze-jira-issue

## Usage

```
/analyze-jira-issue <ticket-number> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **ticket-number**: Jira ticket ID (e.g., PROJ-1234)
  - Format: PROJECT-NUMBER
  - Example: `/analyze-jira-issue PROJ-1234`

### Optional Flags

- **--async**: Execute in background
- **--wait**: Execute synchronously (default)
- **--report=full|summary**: Report level (full by default)

## Examples

```bash
# Analyze Jira ticket (synchronous)
/analyze-jira-issue PROJ-1234 --wait

# Background analysis
/analyze-jira-issue PROJ-5678 --async

# Summary only
/analyze-jira-issue PROJ-9012 --report=summary
```

## Implementation

### Step 1: Parse Arguments
- Extract ticket number
- Validate format (PROJECT-NUMBER)
- Set execution mode (async/sync)
- Set report level (full/summary)

### Step 2: Validate Jira MCP
- Check Jira MCP is configured
- Verify credentials
- Test connection

### Step 3: Queue/Execute Task
- For async: Create task in queue, return task ID
- For sync: Delegate to jira-root-cause-analyzer agent

### Step 4: Delegate to Agent
- Fetch Jira ticket details
- Analyze issue description
- Investigate code
- Trace root cause
- Generate report

### Step 5: Return Response

**Async**:
```
Status: Queued
Task ID: task-20251030-180000-jira-abc123
Estimated time: 10-15 minutes
```

**Sync**:
```
# Jira Issue Analysis: PROJ-1234

[Full analysis report]

Report: marketplace/output/analysis/PROJ-1234-analysis.md
```

## Output Locations

- Full analysis: `marketplace/output/analysis/<ticket-id>-analysis.md`
- Summary: `marketplace/output/analysis/<ticket-id>-summary.md`
- Status: `.claude/task-status/<task-id>.md`

## Typical Analysis Time

- Simple issue: 5-10 minutes
- Complex issue: 15-30 minutes
- Very complex: 30-45 minutes

**Recommendation**: Use `--async` for complex issues.

## FAQ

**Q: What Jira server is supported?**
A: Any JIRA server configured in .mcp.json

**Q: Can I analyze closed issues?**
A: Yes, any accessible issue

**Q: Where are reports saved?**
A: `marketplace/output/analysis/`

**Q: What if Jira is unavailable?**
A: Use --wait for error message with guidance

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Delegated To**: jira-root-cause-analyzer agent
**Task Coverage**: Task #1
