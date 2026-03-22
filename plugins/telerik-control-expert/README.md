# Telerik Control Expert Plugin

Telerik RadControls troubleshooting, migration to modern alternatives, and optimization for ASP.NET WebForms.

## Overview

The Telerik Control Expert plugin provides comprehensive support for diagnosing, optimizing, and migrating Telerik RadControls in ASP.NET WebForms applications. Whether you're troubleshooting production issues, planning a migration to Blazor, or optimizing control configurations, this plugin has you covered.

## Features

### Troubleshooting
- Comprehensive diagnostics for all major Telerik controls
- Root cause analysis for common issues
- Configuration validation
- ViewState and AJAX analysis
- JavaScript error diagnostics
- Step-by-step solutions with code examples
- Prevention measures and best practices

### Migration Planning
- Control mapping to Blazor, React, or Angular
- Migration strategy formulation (full or incremental)
- Effort estimation with detailed breakdown
- Risk assessment and mitigation strategies
- Code examples showing before/after
- Testing and rollout strategies
- Architecture recommendations

### Configuration Analysis
- Property validation and optimization
- Deprecated property detection
- Performance analysis and recommendations
- Best practice validation
- Version compatibility checking
- Security configuration review
- Quick wins identification

## Installation

Already installed in: `marketplace/plugins/telerik-control-expert/`

## Quick Start

### Troubleshoot Telerik Control
```bash
# Diagnose specific control issue
/troubleshoot-telerik RadGrid --issue="Paging not working"

# Analyze file for issues
/troubleshoot-telerik Pages/Users.aspx

# General RadComboBox diagnostics
/troubleshoot-telerik RadComboBox
```

### Plan Migration
```bash
# Migrate page to Blazor
/migrate-telerik Pages/Users.aspx --target=blazor

# Full application migration to React
/migrate-telerik src/Pages --target=react --strategy=full

# Incremental migration plan
/migrate-telerik . --target=blazor --strategy=incremental
```

### Analyze Configuration
```bash
# Full configuration analysis
/analyze-telerik-config Pages/Orders.aspx

# Performance-focused analysis
/analyze-telerik-config Pages/Dashboard.aspx --check=performance

# Best practices review
/analyze-telerik-config Pages/Reports.aspx --check=best-practices
```

## Components

### Agents

#### Telerik Troubleshooter
- **File**: `agents/telerik-troubleshooter.md`
- **Purpose**: Diagnose and solve Telerik control issues
- **Output**: Troubleshooting report with solutions
- **Time**: 18-30 minutes
- **Covers**: RadGrid, RadComboBox, RadEditor, RadAjax, RadWindow, and more

#### Telerik Migration Advisor
- **File**: `agents/telerik-migration-advisor.md`
- **Purpose**: Plan migration to modern frameworks
- **Output**: Comprehensive migration plan with control mapping
- **Time**: 40-75 minutes
- **Sequential Thinking**: Enabled
- **Targets**: Blazor, React, Angular

#### Telerik Property Analyzer
- **File**: `agents/telerik-property-analyzer.md`
- **Purpose**: Analyze and optimize control configurations
- **Output**: Configuration analysis with recommendations
- **Time**: 12-25 minutes

### Commands

#### /troubleshoot-telerik
- **Usage**: `/troubleshoot-telerik <control-type|file> [--issue=description] [--report=full|summary]`
- **Flags**: `--issue`, `--report`, `--async`, `--wait`
- **Delegates To**: telerik-troubleshooter

#### /migrate-telerik
- **Usage**: `/migrate-telerik <file|directory> [--target=blazor|react|angular] [--strategy=full|incremental]`
- **Flags**: `--target`, `--strategy`, `--async`, `--wait`
- **Delegates To**: telerik-migration-advisor

#### /analyze-telerik-config
- **Usage**: `/analyze-telerik-config <file> [--check=performance|compatibility|best-practices]`
- **Flags**: `--check`, `--report`, `--async`, `--wait`
- **Delegates To**: telerik-property-analyzer

### Skills

#### Telerik Controls Guide
- **File**: `skills/telerik-controls-guide.md`
- **Purpose**: Comprehensive Telerik control reference
- **Used By**: All agents

#### WebForms Modernization
- **File**: `skills/webforms-modernization.md`
- **Purpose**: WebForms modernization strategies
- **Used By**: All agents

## Supported Controls

### Data Controls
- RadGrid (full support)
- RadListView
- RadDataPager

### Input Controls
- RadComboBox (full support)
- RadDropDownList
- RadTextBox, RadNumericTextBox, RadMaskedTextBox
- RadDatePicker, RadTimePicker, RadDateTimePicker
- RadColorPicker
- RadSlider
- RadRating

### Rich Controls
- RadEditor (full support)
- RadScheduler
- RadChart, RadHtmlChart
- RadImageGallery
- RadMediaPlayer

### Navigation Controls
- RadMenu
- RadTreeView
- RadPanelBar
- RadTabStrip + RadMultiPage
- RadSiteMap
- RadBreadcrumb

### Layout Controls
- RadWindow (full support)
- RadSplitter + RadPane
- RadDock
- RadNotification
- RadTooltip

### AJAX Controls
- RadAjaxManager (full support)
- RadAjaxPanel
- RadAjaxLoadingPanel

## Output Structure

```
marketplace/output/reviews/
├── <control>-telerik-troubleshooting-<timestamp>.md
├── <target>-telerik-migration-plan-<timestamp>.md
├── <filename>-telerik-config-analysis-<timestamp>.md
└── ...
```

## Common Use Cases

### Production Issue Troubleshooting
```bash
# RadGrid not paging
/troubleshoot-telerik RadGrid --issue="Paging buttons not working"

# RadComboBox not loading data
/troubleshoot-telerik Pages/Orders.aspx --issue="ComboBox empty"

# RadAjax errors
/troubleshoot-telerik RadAjax --issue="Full postback instead of AJAX"
```

### Pre-Migration Assessment
```bash
# Assess migration to Blazor
/migrate-telerik . --target=blazor --strategy=incremental

# Compare migration options
/migrate-telerik src --target=react
/migrate-telerik src --target=angular
```

### Performance Optimization
```bash
# Analyze ViewState issues
/analyze-telerik-config Pages/Dashboard.aspx --check=performance

# Pre-deployment review
/analyze-telerik-config Pages/Orders.aspx --check=best-practices
```

### Version Upgrade Preparation
```bash
# Check for deprecated properties
/analyze-telerik-config Pages/Users.aspx --check=compatibility

# Full analysis before upgrade
/analyze-telerik-config src/Pages --report=full
```

## Common Issues Solved

### RadGrid Issues
- Paging not working
- Sorting broken
- Filtering not applying
- Edit mode errors
- Data binding failures
- Performance with large datasets
- ViewState size issues
- Export problems

### RadComboBox Issues
- Items not loading
- Cascading broken
- Selected value lost on postback
- Client-side operations failing
- LoadOnDemand issues
- Template rendering problems

### RadEditor Issues
- Content not saving
- Toolbar missing or incomplete
- Image upload failures
- Content filtering issues
- Paste from Word problems
- Height/width not applying

### RadAjax Issues
- Partial postback not working
- Loading icon stuck or missing
- Full postback instead of AJAX
- JavaScript errors after AJAX update
- UpdatePanel conflicts

## Migration Paths

### Blazor Migration
**Recommended for**: Teams staying in .NET ecosystem
**Pros**: Similar component model, .NET skillset reuse, Telerik Blazor available
**Cons**: Blazor learning curve, server vs WebAssembly decision

### React Migration
**Recommended for**: Teams with JavaScript expertise, modern UI needs
**Pros**: Rich ecosystem, KendoReact or free alternatives, strong community
**Cons**: Complete paradigm shift, API development needed

### Angular Migration
**Recommended for**: Enterprise applications, teams with Angular expertise
**Pros**: Kendo Angular available, TypeScript, strong structure
**Cons**: Learning curve, verbose compared to React

## Configuration

### Optional Settings (`.claude/settings.local.json`)
```json
{
  "telerik-control-expert": {
    "default_target_framework": "blazor",
    "default_migration_strategy": "incremental",
    "include_code_examples": true,
    "check_viewstate": true,
    "check_ajax": true,
    "check_javascript": true
  }
}
```

## FAQ

**Q: Which Telerik controls are supported?**
A: All major Telerik UI for ASP.NET AJAX controls including RadGrid, RadComboBox, RadEditor, RadAjax, RadWindow, RadScheduler, and more.

**Q: Can it help with Telerik version upgrades?**
A: Yes, `/analyze-telerik-config` detects deprecated properties and version compatibility issues.

**Q: Does migration require Telerik Blazor license?**
A: No, migration advisor suggests both Telerik Blazor and free alternatives.

**Q: How accurate are migration effort estimates?**
A: Based on industry averages and control complexity. Actual effort may vary by team and requirements.

**Q: Can it fix issues automatically?**
A: No, it provides diagnosis and solutions that you implement.

**Q: Does it work with Telerik for ASP.NET WebForms (classic)?**
A: Primarily designed for Telerik UI for ASP.NET AJAX, but many principles apply.

## Integration with Other Plugins

- **Analysis Toolkit**: Use for broader code analysis
- **Review Suite**: Review Telerik code changes
- **Optimization Engine**: Optimize queries used by Telerik controls
- **Development Suite**: Generate Telerik control code

## Troubleshooting

### Control Not Found
```
Issue: "RadGrid not found in codebase"
Solution: Verify control exists, check spelling, provide file path
```

### Version Detection Failed
```
Issue: "Telerik version not detected"
Solution: Check web.config for Telerik assemblies, verify installation
```

### Migration Estimates Too High
```
Issue: "Migration estimate seems excessive"
Solution: Review control complexity, consider incremental migration
```

## Best Practices

### Troubleshooting
1. **Provide Specific Issue Description**: Helps narrow diagnosis
2. **Include Error Messages**: Copy exact error text
3. **Note Recent Changes**: What changed before issue started
4. **Check Telerik Version**: Version-specific issues exist

### Migration
1. **Start Small**: Pilot migration on simple pages
2. **Incremental Approach**: Migrate page by page
3. **API First**: Build API layer before UI migration
4. **Test Thoroughly**: Each migrated page needs testing
5. **Train Team**: Ensure team knows target framework

### Configuration
1. **Regular Analysis**: Run before each release
2. **Address Critical Items**: Fix critical issues immediately
3. **Performance First**: ViewState and AJAX optimization crucial
4. **Document Decisions**: Explain configuration choices

## Plugin Status

- **Version**: 2.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-01-16
- **Tasks Covered**: Telerik troubleshooting, migration, configuration analysis
- **MCP Servers**: None required

## What's New in v2.0.0

- Initial production release
- 3 comprehensive agents with 6-phase processes
- Support for all major Telerik controls
- Blazor, React, and Angular migration paths
- Deprecated property detection
- Performance analysis with ViewState optimization
- AJAX configuration validation
- JavaScript diagnostics
- Migration effort estimation
- Sequential Thinking for migration planning

## Support

For issues or suggestions:
1. Review this README
2. Check agent documentation in `agents/`
3. Review skills in `skills/`
4. Consult Telerik official documentation

---

**Part of the Claude Code Marketplace**
Telerik Control Expert Plugin v2.0.0 (2026-01-16)
