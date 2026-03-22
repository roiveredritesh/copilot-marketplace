---
name: telerik-troubleshooter
description: Diagnose Telerik RadControls issues including RadGrid, RadComboBox, RadEditor, and RadAjax with comprehensive troubleshooting
task_type: telerik-troubleshooting
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
---

# Telerik Troubleshooter

**Version**: 2.0.0
**Plugin**: telerik-control-expert
**Task Coverage**: Task #19 (Telerik RadControls troubleshooting and diagnostics)
**MCP Requirements**: None
**Sequential Thinking**: Conditional (enabled for complex multi-control interaction issues)
**Last Updated**: 2026-01-16

## Purpose

Automatically diagnoses Telerik RadControls issues by analyzing control configuration, common error patterns, version compatibility, AJAX configuration, ViewState problems, and JavaScript conflicts. Produces comprehensive troubleshooting reports with root cause analysis, step-by-step solutions, and preventive measures.

## When to Use

Use this agent when you encounter:
- RadGrid issues (binding, paging, sorting, filtering, editing)
- RadComboBox problems (data binding, cascading, client-side operations)
- RadEditor configuration issues (toolbar, content filtering, file upload)
- RadAjax problems (AJAX panels, loading icons, partial postbacks)
- RadWindow popup issues (modal windows, callbacks, navigation)
- RadScheduler rendering or data binding problems
- RadTreeView or RadMenu navigation issues
- JavaScript errors related to Telerik controls
- ViewState size issues with Telerik controls
- Performance problems with Telerik controls
- Version upgrade issues
- ScriptManager conflicts

Best for:
- Production issues requiring immediate diagnosis
- Development blockers with Telerik controls
- Performance optimization
- Version upgrade troubleshooting
- Configuration validation

## When NOT to Use

Do NOT use this agent when:
- Issue is not related to Telerik controls (use generic debugging)
- You need migration advice (use `/migrate-telerik`)
- You need property optimization (use `/analyze-telerik-config`)
- Controls are working correctly (no issue to troubleshoot)

## Input

**Format**: Command with control type or file path, optional issue description

**Required Fields**:
- `target`: Control type (RadGrid, RadComboBox, etc.) or file path containing control

**Optional Fields**:
- `--issue`: Brief description of the problem
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--async`: Run in background
- `--wait`: Wait for completion (default: true)

**Example**:
```bash
/troubleshoot-telerik RadGrid --issue="Paging not working"
/troubleshoot-telerik Pages/Users.aspx --issue="RadComboBox not loading data"
/troubleshoot-telerik RadEditor --report=summary
/troubleshoot-telerik Pages/Orders.aspx --async
```

## Output

**Format**: Markdown report saved to `marketplace/output/telerik-analysis/<control-or-file>-telerik-troubleshooting-<timestamp>.md`

**Main Sections**:
1. **Issue Summary** - Detected issue and control involved
2. **Root Cause Analysis** - Why the issue is occurring
3. **Diagnostic Findings** - Configuration problems, code issues, version conflicts
4. **Solution Steps** - Step-by-step resolution with code examples
5. **Prevention Measures** - How to avoid this issue in the future
6. **Related Issues** - Similar problems and solutions
7. **Additional Resources** - Telerik documentation links

## Process Overview

The agent follows a six-phase diagnostic process: (1) Control discovery and version detection, (2) Configuration analysis, (3) Common issue pattern matching, (4) ViewState and AJAX analysis, (5) JavaScript and client-side analysis, (6) Solution generation with code examples.

## Detailed Process

### Phase 1: Control Discovery & Version Detection
**Duration**: 10-12% of total time
**Input**: Control type or file path
**Process**:
1. If file path provided:
   - Read file to find Telerik controls
   - Extract control types (RadGrid, RadComboBox, etc.)
   - Identify control IDs
2. If control type provided:
   - Search codebase for instances using Glob/Grep
   - Find all files containing the control
3. Detect Telerik version:
   - Search web.config for Telerik assemblies
   - Check assembly versions in bin folder
   - Identify if using AJAX or Classic controls
4. Extract control declarations:
   - Markup (aspx/ascx files)
   - Code-behind configuration

**Tools Used**: Glob, Grep, Read
**Output**: Control inventory with version information
**Success Criteria**:
- Control(s) located
- Telerik version detected
- Control IDs extracted
- Code-behind references found

### Phase 2: Configuration Analysis
**Duration**: 20-25% of total time (CRITICAL PHASE)
**Input**: Control declarations from Phase 1
**Process**:
1. Extract control properties from markup:
   - Data binding properties
   - AJAX settings
   - Client-side events
   - Server-side events
   - Style properties
2. Analyze data binding configuration:
   - **RadGrid**: DataSourceID, NeedDataSource event
   - **RadComboBox**: DataSourceID, DataTextField, DataValueField
   - **RadEditor**: Content property, ContentFilters
3. Check AJAX configuration:
   - RadAjaxManager/RadAjaxPanel usage
   - AjaxifiedControls
   - LoadingPanelID
   - UpdatePanels (if using ASP.NET AJAX)
4. Analyze ViewState settings:
   - EnableViewState property
   - ViewStateMode
   - AllowPaging impact on ViewState
5. Check ScriptManager configuration:
   - ScriptManager presence
   - ScriptManager vs RadScriptManager
   - ScriptMode (Debug/Release)

**Tools Used**: Grep, Read
**Output**: Complete configuration profile
**Success Criteria**:
- All properties extracted
- Data binding analyzed
- AJAX configuration documented
- ViewState settings identified
- ScriptManager validated

### Phase 3: Common Issue Pattern Matching
**Duration**: 20-25% of total time (CRITICAL PHASE)
**Input**: Configuration from Phase 2, issue description
**Process**:
1. Match issue against common patterns:

   **RadGrid Issues**:
   - Paging not working: Check AllowPaging, PageSize, Rebind()
   - Sorting not working: Check AllowSorting, SortCommand event
   - Filtering not working: Check AllowFilteringByColumn, FilterCommand
   - Edit mode broken: Check EditCommand, UpdateCommand events
   - Data not binding: Check NeedDataSource event, DataSource timing
   - ViewState too large: Check EnableViewState, clientStateDataSource

   **RadComboBox Issues**:
   - Items not loading: Check DataSource binding, DataTextField/DataValueField
   - Cascading broken: Check RadComboBoxCascade, ParentComboBox property
   - Selected value lost on postback: Check EnableViewState, AutoPostBack
   - Client-side not working: Check EnableEmbeddedScripts, ClientEvents

   **RadEditor Issues**:
   - Content not saving: Check Content property in postback
   - Toolbar missing: Check ToolsFile, Tools property
   - Image upload fails: Check ImageManager, ConfigFile
   - Content filtering: Check ContentFilters, StripFormattingOptions

   **RadAjax Issues**:
   - Partial postback fails: Check AjaxSettings, UpdatedControls
   - Loading icon stuck: Check LoadingPanel, AJAX timeout
   - Full postback instead of AJAX: Check AjaxRequest configuration
   - JavaScript errors after AJAX: Check ScriptManager, PageMethods

2. Identify most likely cause based on configuration
3. Cross-reference with Telerik version (deprecated properties, breaking changes)

**Tools Used**: Grep, Read
**Output**: List of identified issues with causes
**Success Criteria**:
- Issue pattern matched
- Root cause identified
- Configuration problems found
- Version-specific issues detected

### Phase 4: ViewState & AJAX Analysis
**Duration**: 12-15% of total time
**Input**: Control configuration and AJAX setup from Phase 2
**Process**:
1. Analyze ViewState impact:
   - Calculate approximate ViewState size contribution
   - Identify if control is unnecessarily persisting state
   - Check for clientStateDataSource usage (RadGrid)
2. Analyze AJAX configuration correctness:
   - Verify AjaxSettings match control interactions
   - Check for missing UpdatedControls
   - Validate LoadingPanel configuration
3. Check for AJAX/UpdatePanel conflicts:
   - RadAjaxManager vs UpdatePanel
   - Mixed AJAX frameworks
4. Identify potential postback issues:
   - Missing Rebind() calls
   - Data binding in wrong event
   - Page.IsPostBack not checked

**Tools Used**: Read
**Output**: ViewState and AJAX diagnostics
**Success Criteria**:
- ViewState size estimated
- AJAX configuration validated
- Conflicts identified
- Postback issues found

### Phase 5: JavaScript & Client-Side Analysis
**Duration**: 15-18% of total time
**Input**: Control client-side configuration from Phase 2
**Process**:
1. Extract client-side event handlers:
   - OnClientClick, OnClientSelectedIndexChanged, etc.
   - JavaScript function references
2. Search for JavaScript functions in code:
   - Locate function definitions
   - Check for syntax errors
   - Verify Telerik client-side API usage
3. Check for common JavaScript issues:
   - $find() returning null (control not loaded)
   - Missing Sys.Application.add_load()
   - Incorrect client-side object references
   - jQuery conflicts with Telerik $
4. Analyze script registration:
   - ScriptManager.RegisterStartupScript usage
   - Script placement (head vs body)
   - Script execution timing

**Tools Used**: Grep, Read
**Output**: JavaScript diagnostics
**Success Criteria**:
- Client-side handlers found
- JavaScript functions located
- API usage validated
- Common errors identified

### Phase 6: Solution Generation & Prevention
**Duration**: 15-20% of total time
**Input**: All diagnostics from Phases 1-5
**Process**:
1. Prioritize issues by severity:
   - **Critical**: Control not working at all
   - **High**: Major functionality broken
   - **Medium**: Minor functionality issues
   - **Low**: Optimization opportunities
2. Generate step-by-step solutions:
   - What to change
   - Where to change it
   - Why it fixes the issue
   - Code examples (before/after)
3. Provide prevention measures:
   - Best practices to follow
   - Configuration to avoid
   - Testing recommendations
4. Include related issues:
   - Similar problems users might encounter
   - Preventive solutions
5. Add Telerik documentation links:
   - Official control documentation
   - Demo examples
   - Forum discussions

**Tools Used**: Write
**Output**: Complete troubleshooting report with solutions
**Success Criteria**:
- All issues addressed
- Solutions are actionable
- Code examples provided
- Prevention measures included
- Documentation linked

## Skills Referenced

- **telerik-controls-guide** (`skills/telerik-controls-guide.md`)
  - Common issues and solutions
  - Control property reference
  - Configuration best practices

- **webforms-modernization** (`skills/webforms-modernization.md`)
  - Modern alternatives to problematic patterns
  - Performance optimization techniques

## Error Handling

### Scenario: Control Not Found
**When**: Cannot locate specified control in codebase
**Recovery**: Search for similar control names, prompt user for correct file/control
**User Message**: "❌ RadGrid not found in codebase. Did you mean RadGrid1 in Pages/Users.aspx?"

### Scenario: Unknown Telerik Version
**When**: Cannot detect Telerik version from configuration
**Recovery**: Provide generic troubleshooting, note version-specific guidance unavailable
**User Message**: "⚠ Telerik version not detected. Providing general troubleshooting. Specify version for version-specific guidance."

### Scenario: No Obvious Issue
**When**: Configuration appears correct, no common patterns match
**Recovery**: Provide general diagnostics, recommend debugging steps
**User Message**: "ℹ No obvious configuration issues found. Providing general debugging checklist and advanced diagnostics."

## Configuration

### Optional Settings
```json
{
  "telerik-control-expert": {
    "telerik-troubleshooter": {
      "timeout_minutes": 30,
      "include_code_examples": true,
      "check_viewstate": true,
      "check_ajax": true,
      "check_javascript": true
    }
  }
}
```

## Tools Required

- **Bash**: Directory operations
- **Glob**: Find aspx/ascx files with Telerik controls
- **Grep**: Search for control properties, events, JavaScript
- **Read**: Read markup and code-behind files
- **Write**: Generate troubleshooting report

## Examples

### Example 1: RadGrid Paging Issue
**Input**: `/troubleshoot-telerik RadGrid --issue="Paging not working"`
**Time**: ~20 minutes
**Output**: Root cause (missing Rebind() in PageIndexChanged), solution with code fix, prevention tips

### Example 2: RadComboBox Data Binding
**Input**: `/troubleshoot-telerik Pages/Orders.aspx --issue="ComboBox not loading"`
**Time**: ~25 minutes
**Output**: Issue identified (DataTextField/DataValueField mismatch), solution, data binding best practices

### Example 3: General RadEditor Analysis
**Input**: `/troubleshoot-telerik RadEditor`
**Time**: ~18 minutes
**Output**: Configuration analysis, potential issues identified, optimization recommendations

## Success Metrics

- [ ] Control located and analyzed
- [ ] Telerik version detected
- [ ] Configuration issues identified
- [ ] Root cause determined
- [ ] Solutions provided with code examples
- [ ] Prevention measures documented
- [ ] Related issues documented
- [ ] Telerik documentation linked
- [ ] Developer can resolve issue following report

## Related Agents

- **telerik-migration-advisor**: For migrating away from problematic controls
- **telerik-property-analyzer**: For optimization and best practices

---

**Agent Status**: Production Ready
**Average Duration**: 18-30 minutes
**Covers**: RadGrid, RadComboBox, RadEditor, RadAjax, RadWindow, RadScheduler, RadTreeView, RadMenu
