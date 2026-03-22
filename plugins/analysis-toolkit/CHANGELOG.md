# Analysis Toolkit - Changelog

All notable changes to this plugin will be documented in this file.

## [2.0.0] - 2026-01-15

### Changed
- **BREAKING**: Migrated to shared skills library for better maintainability
- Updated all agent specifications to latest template with enhanced error handling
- Improved Sequential Thinking integration across all agents
- Plugin-specific `root-cause-analysis` skill moved to `shared-skills/`

### Added
- Reference to shared skill: `sql-optimization-patterns` for database query analysis
- Reference to shared skill: `query-performance-tuning` for performance optimization
- Reference to shared skill: `performance-analysis-framework` for bottleneck identification
- Enhanced agent documentation with detailed process phases
- Improved error handling for MCP server unavailability
- Better fallback strategies when MCP services are offline

### Improved
- All agents now follow standardized specification template
- Enhanced error messages and recovery strategies
- Better integration with shared methodology
- Consistent output format across all agents
- Updated documentation with v2.0.0 features

### Migration Notes
- Skills now referenced from `../../shared-skills/` directory
- No changes to command interface - all commands work identically
- Existing reports and output remain compatible
- MCP configuration unchanged

## [1.1.0] - 2025-11-10

### Added
- **Agent: qa-testing-guide-generator** - Generates comprehensive QA testing guides with full codebase verification
- **Command: /generate-qa-guide** - Generate QA testing guides with verified test scenarios
- Comprehensive 12-phase codebase scanning process
- UI component detection with Grep patterns for ASP.NET/Telerik controls
- Validation rule extraction and workflow tracing
- Database constraint and schema analysis
- Auto-correction of test step discrepancies
- Gap detection for untested code paths
- Confidence scoring system (>=50% threshold for scenario inclusion)

### Features
- Codebase scanning for UI components, validation rules, and workflows
- Verification-backed test scenarios (only verified steps included)
- Auto-correction of button text, field names, error messages, navigation targets
- Integration with Jira analysis via --from-analysis flag
- Standalone mode for direct code analysis
- Gap identification and reporting
- Test data specification generation
- Full and summary report modes

### Improvements
- Enhanced plugin to include system testing focus (not just technical analysis)
- Plugin now covers 5 core analysis/testing tasks
- Added test verification and gap analysis capabilities
- Extended MCP integration for QA workflow

## [1.0.0] - 2025-10-29

### Added
- Initial release of Analysis Toolkit plugin
- **Agent: jira-root-cause-analyzer** - Analyzes Jira tickets for root causes
- **Agent: db-query-analyzer** - Analyzes database queries and views
- **Agent: impact-analyzer** - Analyzes impact of code changes
- **Agent: stack-trace-analyzer** - Analyzes error stack traces
- **Command: /analyze-jira-issue** - Analyze Jira tickets
- **Command: /analyze-query** - Analyze database queries
- **Command: /analyze-impact** - Analyze code change impact
- **Command: /analyze-stacktrace** - Analyze error traces
- **Skill: root-cause-analysis** - Root cause analysis methodology
- Support for async/sync execution modes
- Support for full/summary report levels
- MCP integration for Jira and MSSQL
- Comprehensive status tracking
- Real-time progress updates

### Features
- Root cause identification from Jira tickets
- Database query analysis and optimization recommendations
- Code change impact assessment
- Error stack trace diagnosis with solution recommendations
- Async background processing (up to 10 concurrent)
- Real-time status updates
- Comprehensive markdown reports
- Multiple solution options (quick fix, proper fix, prevention)

### Notes
- Requires MCP servers configured in `.mcp.json`
- Jira MCP required for /analyze-jira-issue
- MSSQL MCP required for /analyze-query
- Stack trace and impact analysis work without external MCP servers
