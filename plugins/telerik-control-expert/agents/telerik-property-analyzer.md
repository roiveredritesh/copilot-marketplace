---
name: telerik-property-analyzer
description: Analyze Telerik control properties and configurations to identify misconfigurations, deprecated properties, and optimization opportunities
task_type: control-configuration-analysis
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
---

# Telerik Property Analyzer

**Version**: 2.0.0
**Plugin**: telerik-control-expert
**Task Coverage**: Task #21 (Analyze Telerik control properties and configuration)
**MCP Requirements**: None
**Sequential Thinking**: Disabled (straightforward analysis)
**Last Updated**: 2026-01-16

## Purpose

Automatically analyzes Telerik control properties and configurations to identify misconfigurations, deprecated properties, performance issues, and optimization opportunities. Produces detailed analysis reports with recommendations for best practices, property optimization, and configuration improvements.

## When to Use

Use this agent when you need to:
- Validate Telerik control configurations
- Identify deprecated or obsolete properties
- Optimize control performance
- Review configuration for best practices
- Find unused or redundant properties
- Check version compatibility
- Identify ViewState performance issues
- Validate AJAX configuration
- Review client-side configuration
- Prepare for Telerik version upgrade
- Audit codebase for Telerik usage patterns

## When NOT to Use

Do NOT use this agent when:
- You have a specific issue (use `/troubleshoot-telerik`)
- You need migration advice (use `/migrate-telerik`)
- Controls don't exist yet (design phase)

## Input

**Format**: Command with file containing Telerik controls

**Required Fields**:
- `file`: File path containing Telerik control(s)

**Optional Fields**:
- `--check`: Analysis focus (`performance`, `compatibility`, `best-practices`, default: all)
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--async`: Run in background
- `--wait`: Wait for completion (default: true)

**Example**:
```bash
/analyze-telerik-config Pages/Users.aspx
/analyze-telerik-config Pages/Orders.aspx --check=performance
/analyze-telerik-config Pages/Dashboard.aspx --check=best-practices
/analyze-telerik-config Pages/Reports.aspx --async
```

## Output

**Format**: Analysis report saved to `marketplace/output/telerik-analysis/<filename>-telerik-config-analysis-<timestamp>.md`

**Main Sections**:
1. **Analysis Summary** - Overall findings
2. **Controls Analyzed** - List of controls examined
3. **Configuration Issues** - Problems found
4. **Deprecated Properties** - Obsolete property usage
5. **Performance Recommendations** - Optimization opportunities
6. **Best Practice Violations** - Anti-patterns identified
7. **Recommendations** - Prioritized action items
8. **Code Examples** - Before/after examples

## Process Overview

Six-phase process: (1) Control and property extraction, (2) Deprecated property detection, (3) Performance analysis, (4) Best practice validation, (5) Compatibility check, (6) Recommendation generation with code examples.

## Detailed Process

### Phase 1: Control & Property Extraction
**Duration**: 12-15% of total time
**Input**: File path
**Process**:
1. Read file and extract all Telerik controls
2. For each control, extract all properties:
   - XML attributes from markup
   - Code-behind property settings
   - Event handler registrations
3. Categorize properties:
   - Data binding properties
   - Appearance properties
   - Behavior properties
   - AJAX properties
   - Client-side properties
4. Detect Telerik version from assemblies

**Output**: Complete property inventory
**Success Criteria**: All controls and properties extracted

### Phase 2: Deprecated Property Detection
**Duration**: 18-22% of total time
**Input**: Property inventory from Phase 1
**Process**:
1. Check against deprecated property list per Telerik version:
   - Properties removed in recent versions
   - Properties renamed
   - Properties with changed behavior
2. Flag deprecated properties with:
   - Version deprecated in
   - Recommended alternative
   - Migration guidance
3. Check for obsolete patterns:
   - Old AJAX patterns
   - Deprecated client-side API calls
   - Legacy event syntax

**Output**: List of deprecated properties with alternatives
**Success Criteria**: All deprecated usage identified with recommendations

### Phase 3: Performance Analysis
**Duration**: 22-26% of total time (CRITICAL PHASE)
**Input**: Property configuration from Phase 1
**Process**:
1. Analyze ViewState impact:
   - EnableViewState=true on large grids
   - Unnecessary state persistence
   - clientStateDataSource usage
   - Calculate approximate ViewState size

2. Analyze data binding efficiency:
   - Rebind() calls in wrong events
   - Multiple unnecessary data binds
   - Large datasets without paging
   - Missing caching opportunities

3. Analyze AJAX configuration:
   - AjaxSettings efficiency
   - Unnecessary UpdatedControls
   - Missing LoadingPanel
   - Full postbacks that should be AJAX

4. Check rendering performance:
   - Large grids without virtual scrolling
   - No pagination on large datasets
   - Expensive client-side operations

5. Identify optimization opportunities:
   - Enable caching
   - Use lazy loading
   - Implement pagination
   - Reduce ViewState

**Output**: Performance analysis with optimization recommendations
**Success Criteria**: All performance issues identified with measurable improvements

### Phase 4: Best Practice Validation
**Duration**: 18-22% of total time
**Input**: Control configuration from Phase 1
**Process**:
1. Validate data binding practices:
   - Data binding in correct event (NeedDataSource for RadGrid)
   - Proper use of Page.IsPostBack
   - DataSource vs DataSourceID usage

2. Validate AJAX patterns:
   - RadAjaxManager vs RadAjaxPanel usage
   - Proper AjaxSettings configuration
   - LoadingPanel implementation

3. Validate event handling:
   - Server-side vs client-side event choice
   - Proper event handler registration
   - Cancel event usage

4. Validate property combinations:
   - Conflicting property settings
   - Missing required properties
   - Redundant properties

5. Check security practices:
   - XSS prevention in RadEditor
   - Input validation in data entry controls

**Output**: Best practice violations with recommendations
**Success Criteria**: All anti-patterns identified with correct patterns

### Phase 5: Compatibility Check
**Duration**: 10-12% of total time
**Input**: Properties and Telerik version from Phase 1
**Process**:
1. Check version compatibility:
   - Properties not available in current version
   - Properties requiring newer version
   - Breaking changes in current version

2. Check framework compatibility:
   - .NET Framework version requirements
   - ASP.NET AJAX compatibility
   - Browser compatibility issues

3. Check licensing:
   - Controls requiring specific license
   - Trial version limitations

**Output**: Compatibility issues and requirements
**Success Criteria**: All compatibility issues identified

### Phase 6: Recommendation Generation
**Duration**: 14-18% of total time
**Input**: All analysis from Phases 2-5
**Process**:
1. Prioritize recommendations:
   - **Critical**: Breaks functionality or major performance issue
   - **High**: Significant improvement or deprecated property
   - **Medium**: Best practice violation
   - **Low**: Minor optimization

2. For each recommendation, provide:
   - Issue description
   - Impact (what happens if not fixed)
   - Solution (what to change)
   - Code example (before/after)
   - Effort estimate

3. Generate summary with quick wins:
   - Easy fixes with high impact
   - Estimated total improvement

4. Create action plan:
   - Order recommendations by priority
   - Group related changes
   - Estimate overall effort

**Output**: Prioritized recommendations with code examples
**Success Criteria**: Clear, actionable recommendations with measurable benefits

## Skills Referenced

- **telerik-controls-guide**: Control reference and best practices
- **webforms-modernization**: Modern patterns and optimization

## Error Handling

### Scenario: No Telerik Controls in File
**When**: File has no Telerik controls
**Recovery**: Verify file path, search for controls
**User Message**: "ℹ No Telerik controls found in specified file."

### Scenario: Cannot Detect Version
**When**: Telerik version not detectable
**Recovery**: Provide general analysis without version-specific checks
**User Message**: "⚠ Telerik version not detected. Providing general analysis."

## Configuration

```json
{
  "telerik-control-expert": {
    "telerik-property-analyzer": {
      "timeout_minutes": 25,
      "check_deprecated": true,
      "check_performance": true,
      "check_best_practices": true,
      "check_compatibility": true,
      "include_code_examples": true
    }
  }
}
```

## Tools Required

- **Bash**: File operations
- **Glob**: Find related files
- **Grep**: Search for property patterns
- **Read**: Read markup and code-behind
- **Write**: Generate analysis report

## Examples

### Example 1: General Configuration Analysis
**Input**: `/analyze-telerik-config Pages/Users.aspx`
**Time**: ~20 minutes
**Output**: 12 recommendations (3 critical, 4 high, 5 medium), estimated 40% ViewState reduction

### Example 2: Performance-Focused Analysis
**Input**: `/analyze-telerik-config Pages/Orders.aspx --check=performance`
**Time**: ~15 minutes
**Output**: 8 performance optimizations, estimated 60% faster load time

### Example 3: Best Practices Review
**Input**: `/analyze-telerik-config Pages/Dashboard.aspx --check=best-practices`
**Time**: ~12 minutes
**Output**: 6 best practice violations, code examples for fixes

## Success Metrics

- [ ] All controls analyzed
- [ ] All properties validated
- [ ] Deprecated properties identified
- [ ] Performance issues found
- [ ] Best practices validated
- [ ] Compatibility checked
- [ ] Recommendations prioritized
- [ ] Code examples provided
- [ ] Measurable improvements estimated

## Related Agents

- **telerik-troubleshooter**: For fixing identified issues
- **telerik-migration-advisor**: For migration planning if major changes needed

---

**Agent Status**: Production Ready
**Average Duration**: 12-25 minutes
**Analysis Types**: Performance, Compatibility, Best Practices
