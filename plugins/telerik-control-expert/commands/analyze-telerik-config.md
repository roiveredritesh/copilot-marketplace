---
name: analyze-telerik-config
description: Analyze Telerik control properties and configurations
delegated_to: telerik-property-analyzer
---

# Command: /analyze-telerik-config

Analyze Telerik control properties and configurations to identify issues and optimization opportunities.

## Usage

```bash
/analyze-telerik-config <file> [flags]
```

## Arguments

- `<file>`: File containing Telerik controls
  - Examples: `Pages/Users.aspx`, `Pages/Orders.aspx`

## Flags

- `--check=<performance|compatibility|best-practices>`: Analysis focus (default: all)
- `--report=<full|summary>`: Report detail level (default: `full`)
- `--async`: Run in background
- `--wait`: Wait for completion (default)

## Examples

### Full Analysis
```bash
# Analyze all aspects
/analyze-telerik-config Pages/Users.aspx

# Full detailed analysis
/analyze-telerik-config Pages/Orders.aspx --report=full
```

### Focused Analysis
```bash
# Performance only
/analyze-telerik-config Pages/Dashboard.aspx --check=performance

# Best practices only
/analyze-telerik-config Pages/Reports.aspx --check=best-practices

# Compatibility only
/analyze-telerik-config Pages/Users.aspx --check=compatibility
```

### Background Execution
```bash
# Large file - run in background
/analyze-telerik-config Pages/Dashboard.aspx --async
```

## Output

Analysis report saved to: `output/reviews/<filename>-telerik-config-analysis-<timestamp>.md`

**Sections**:
- Analysis Summary
- Controls Analyzed
- Configuration Issues
- Deprecated Properties
- Performance Recommendations
- Best Practice Violations
- Recommendations (prioritized)
- Code Examples (before/after)

## Execution Time

- Simple page: 10-15 minutes
- Standard page: 15-20 minutes
- Complex page: 20-30 minutes

## Analysis Types

### Performance
Checks:
- ViewState size and optimization
- Data binding efficiency
- AJAX configuration
- Pagination and caching
- Client-side performance

### Compatibility
Checks:
- Deprecated property usage
- Version compatibility
- Framework compatibility
- Browser compatibility
- License requirements

### Best Practices
Checks:
- Data binding patterns
- AJAX patterns
- Event handling
- Property combinations
- Security practices

## Recommendations

Agent provides prioritized recommendations:
- **Critical**: Breaking issues
- **High**: Significant improvements
- **Medium**: Best practice violations
- **Low**: Minor optimizations

Each includes:
- Issue description
- Impact
- Solution
- Code example
- Effort estimate

## Troubleshooting

### No Controls Found
```
Info: "No Telerik controls in file"
Solution: Verify file contains Telerik controls
```

### Version Not Detected
```
Warning: "Telerik version not detected"
Solution: General analysis provided, check web.config
```

## Related Commands

- `/troubleshoot-telerik` - Fix identified issues
- `/migrate-telerik` - If major changes needed

---

**Delegates To**: telerik-property-analyzer agent
**Command Version**: 2.0.0
**Status**: Production Ready
