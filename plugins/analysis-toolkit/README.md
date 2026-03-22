# Analysis Toolkit Plugin

Root cause analysis, error investigation, and issue diagnosis toolkit for systematic problem-solving.

## Overview

The Analysis Toolkit provides automated analysis capabilities for bugs, errors, performance issues, and system problems. Four specialized agents help investigate root causes, understand impacts, and provide solutions.

## Features

### Jira Issue Analysis
- Fetch ticket details from Jira via MCP
- Analyze issue description and reproduction steps
- Investigate related code sections
- Trace root causes and impacts
- Generate comprehensive analysis reports

### Database Query Analysis
- Analyze MSSQL queries, stored procedures, and views
- Identify performance bottlenecks
- Detect N+1 query patterns
- Check for missing indexes
- Provide optimization recommendations

### Code Change Impact Analysis
- Analyze impact of code changes on other components
- Search for all references and dependencies
- Trace dependency chains
- Identify affected features
- Assess breaking changes and risks

### Stack Trace Analysis
- Parse error stack traces from any language
- Trace execution path to root cause
- Classify error patterns
- Provide 3 solution levels (quick, proper, comprehensive)
- Include testing and prevention recommendations

## Installation

Already installed: `marketplace/plugins/analysis-toolkit/`

## Quick Start

### Analyze a Jira Issue
```bash
/analyze-jira-issue PROJ-1234 --wait
/analyze-jira-issue PROJ-5678 --async
```

### Analyze a Database Query
```bash
/analyze-query sp_GetUsers --wait
/analyze-query sp_Report --async
```

### Analyze Code Change Impact
```bash
/analyze-impact src/Services/UserService.cs --wait
/analyze-impact Models/User.cs --report=summary
```

### Analyze an Error Stack Trace
```bash
/analyze-stacktrace --wait
[Paste stack trace]

/analyze-stacktrace --async < error.log
```

## Components

### Agents

#### Jira Root Cause Analyzer
- **File**: `agents/jira-root-cause-analyzer.md`
- **Purpose**: Analyze Jira tickets for root causes
- **Task**: Task #1 (Analyze issues and identify root causes)

#### Database Query Analyzer
- **File**: `agents/db-query-analyzer.md`
- **Purpose**: Analyze database performance and issues
- **Task**: Task #5 (Database performance analysis)

#### Impact Analyzer
- **File**: `agents/impact-analyzer.md`
- **Purpose**: Analyze code change impacts
- **Task**: Task #10 (Analyze code change impact)

#### Stack Trace Analyzer
- **File**: `agents/stack-trace-analyzer.md`
- **Purpose**: Analyze error stack traces
- **Task**: Task #13 (Stack trace analysis and root cause)

### Commands

#### /analyze-jira-issue
- **Usage**: `/analyze-jira-issue <ticket-id> [--async|--wait] [--report=full|summary]`
- **Delegates To**: jira-root-cause-analyzer agent

#### /analyze-query
- **Usage**: `/analyze-query <query-name> [--async|--wait] [--report=full|summary]`
- **Delegates To**: db-query-analyzer agent

#### /analyze-impact
- **Usage**: `/analyze-impact <file-path> [--async|--wait] [--report=full|summary]`
- **Delegates To**: impact-analyzer agent

#### /analyze-stacktrace
- **Usage**: `/analyze-stacktrace [--async|--wait] [--report=full|summary]`
- **Delegates To**: stack-trace-analyzer agent

### Skills

#### Root Cause Analysis
- **File**: `skills/root-cause-analysis.md`
- **Coverage**: 7-step RCA methodology, common patterns, tools & techniques, checklist

## Output Structure

```
marketplace/output/analysis/
├── <ticket-id>-analysis.md              # Jira issue analysis
├── <query-name>-analysis.md             # Database query analysis
├── impact-<filename>.md                 # Code change impact
├── <ERROR_TYPE>-analysis.md             # Stack trace analysis
└── ... (summary versions)
```

## Typical Analysis Time

### Jira Issues
- Simple: 5-10 minutes
- Complex: 15-30 minutes
- Very complex: 30-45 minutes

### Database Queries
- Simple: 3-5 minutes
- Complex: 8-15 minutes
- Very complex: 15-30 minutes

### Code Impact Analysis
- Small file: 5-10 minutes
- Medium file: 10-20 minutes
- Large file: 20-30 minutes

### Stack Trace Analysis
- Simple error: 2-3 minutes
- Complex trace: 5-10 minutes
- Deep analysis: 10-15 minutes

**Recommendation**: Use `--async` for complex analysis.

## MCP Requirements

### Jira MCP (Optional, for Jira analysis)
```json
{
  "jira": {
    "command": "npx",
    "args": ["@modelcontextprotocol/server-jira"],
    "env": {
      "JIRA_URL": "https://jira.yourcompany.com",
      "JIRA_EMAIL": "your-email@example.com",
      "JIRA_API_TOKEN": "your-api-token"
    }
  }
}
```

### MSSQL MCP (Optional, for database analysis)
```json
{
  "mssql": {
    "command": "node",
    "args": ["@modelcontextprotocol/server-mssql/dist/index.js"],
    "env": {
      "MSSQL_CONNECTION_STRING": "Server=localhost;Database=mydb;..."
    }
  }
}
```

## Usage Examples

### Production Bug Investigation
```bash
# Find root cause of production issue
/analyze-jira-issue PROD-4567 --wait
# Review findings and implement fix
```

### Database Performance Issue
```bash
# Analyze slow query
/analyze-query sp_SlowReport --wait
# Get optimization recommendations
```

### Code Review Preparation
```bash
# Check impact before submitting PR
/analyze-impact src/MyChanges.cs --wait
# Ensure no unexpected impacts
```

### Error Diagnosis
```bash
# Analyze application error
/analyze-stacktrace --wait
[Paste stack trace from logs]
# Get root cause and solutions
```

## FAQ

**Q: What if Jira/MSSQL MCP is unavailable?**
A: Some commands won't work. Others (impact, stacktrace) don't require MCP.

**Q: Can I analyze closed issues?**
A: Yes, any accessible issue can be analyzed.

**Q: How detailed are the reports?**
A: Very detailed with root cause, impact analysis, and 3-level solutions.

**Q: Can I share the reports?**
A: Yes, they're markdown files suitable for sharing and discussion.

**Q: What languages does stack trace analysis support?**
A: .NET, Java, JavaScript, Python, and generic formats.

## Integration with Other Plugins

- **Review Suite**: Use PR review to catch issues before analysis
- **Optimization Engine**: Optimize issues found during analysis
- **Architecture Advisor**: Address architectural issues found

## Related Commands

- `/task-status <task-id>` - Check analysis progress
- `/review-pr` - Code review (complements analysis)
- `/optimize-query` - Query optimization
- `/optimize-algorithm` - Algorithm optimization

## Best Practices

1. **Use for Production Issues**: Diagnose and fix production problems
2. **Analyze Before Changes**: Check impact before code changes
3. **Learn from Issues**: Use reports to understand problems
4. **Share Findings**: Use reports for team discussion
5. **Prevent Recurrence**: Implement prevention recommendations

## Plugin Status

- **Version**: 2.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-01-15
- **Tasks Covered**: Task #1, #5, #10, #13, QA Testing
- **MCP Servers**: Jira, MSSQL (optional)
- **Shared Skills**: 4 (root-cause-analysis, sql-optimization-patterns, query-performance-tuning, performance-analysis-framework)

## What's New in v2.0.0

- **Shared Skills Integration**: Now uses centralized skill library for better consistency
- **Enhanced Agent Specifications**: All agents follow latest template standards
- **Improved Error Handling**: Better fallback strategies when MCP unavailable
- **Sequential Thinking**: Enhanced support for complex reasoning tasks
- **Better Documentation**: Detailed process phases and success criteria

## Support

For issues or suggestions:
1. Check this README
2. Review FAQ section
3. Review command documentation
4. Consult shared skills documentation in `../../shared-skills/`

---

**Part of the Claude Code Marketplace**
Analysis Toolkit Plugin v2.0.0 (2026-01-15)
