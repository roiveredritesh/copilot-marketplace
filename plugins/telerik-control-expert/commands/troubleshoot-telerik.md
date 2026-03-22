---
name: troubleshoot-telerik
description: Diagnose and troubleshoot Telerik RadControls issues
delegated_to: telerik-troubleshooter
---

# Command: /troubleshoot-telerik

Diagnose Telerik RadControls issues with comprehensive root cause analysis and step-by-step solutions.

## Usage

```bash
/troubleshoot-telerik <control-type|file> [flags]
```

## Arguments

- `<control-type|file>`: Telerik control type (RadGrid, RadComboBox, etc.) or file path containing control
  - Examples: `RadGrid`, `RadComboBox`, `Pages/Users.aspx`

## Flags

- `--issue=<description>`: Brief description of the problem
- `--report=<full|summary>`: Report detail level (default: `full`)
- `--async`: Run in background
- `--wait`: Wait for completion (default)

## Examples

### By Control Type
```bash
# Diagnose RadGrid issues
/troubleshoot-telerik RadGrid --issue="Paging not working"

# General RadComboBox diagnostics
/troubleshoot-telerik RadComboBox

# RadEditor with issue description
/troubleshoot-telerik RadEditor --issue="Toolbar missing"
```

### By File
```bash
# Analyze specific page
/troubleshoot-telerik Pages/Users.aspx --issue="ComboBox not loading"

# Full file analysis
/troubleshoot-telerik Pages/Orders.aspx

# Background analysis
/troubleshoot-telerik Pages/Dashboard.aspx --async
```

### Different Report Levels
```bash
# Summary report
/troubleshoot-telerik RadGrid --report=summary

# Full detailed report
/troubleshoot-telerik Pages/Users.aspx --report=full
```

## Output

Report saved to: `output/reviews/<control-or-file>-telerik-troubleshooting-<timestamp>.md`

**Sections**:
- Issue Summary
- Root Cause Analysis
- Diagnostic Findings
- Solution Steps (with code examples)
- Prevention Measures
- Related Issues
- Additional Resources

## Execution Time

- Simple issue: 15-20 minutes
- Standard issue: 20-25 minutes
- Complex multi-control issue: 25-35 minutes

## Common Issues Solved

### RadGrid
- Paging, sorting, filtering not working
- Edit mode errors
- Data binding failures
- ViewState size issues
- Export problems

### RadComboBox
- Items not loading
- Cascading broken
- Selected value lost
- Client-side operations failing

### RadEditor
- Content not saving
- Toolbar issues
- Image upload failures
- Content filtering problems

### RadAjax
- Partial postback not working
- Loading icon issues
- JavaScript errors after AJAX

## Troubleshooting

### Control Not Found
```
Error: "RadGrid not found in codebase"
Solution: Verify control exists, check spelling
```

### Version Not Detected
```
Warning: "Telerik version not detected"
Solution: Provide general troubleshooting, check web.config
```

## Related Commands

- `/migrate-telerik` - If issue is difficult to fix, consider migration
- `/analyze-telerik-config` - For configuration optimization

---

**Delegates To**: telerik-troubleshooter agent
**Command Version**: 2.0.0
**Status**: Production Ready
