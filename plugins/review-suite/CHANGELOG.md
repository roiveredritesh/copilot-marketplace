# Review Suite Plugin - Changelog

All notable changes to the Review Suite plugin are documented in this file.

## [2.0.0] - 2026-01-15

### Changed

**Skills Integration**
- Migrated to shared skills library
- Replaced local `code-review-checklist` skill with shared `code-review-best-practices` skill
- Added reference to shared `performance-analysis-framework` skill
- All agents now reference shared skills for methodology

**Agent Specifications**
- Updated all 4 agents to v2.0.0
- Enhanced agent specifications with Sequential Thinking support (Conditional)
- Added "Skills Referenced" section to all agents
- Improved error handling patterns
- Enhanced documentation structure

**Plugin Configuration**
- Updated plugin.json with structured metadata
- Added compatibility field: "Claude Code 1.0+"
- Added changelog field reference
- Added mcp_servers and dependencies arrays
- Changed status to "production"
- Updated author field

### Added

**Shared Skills References**
- code-review-best-practices (../../shared-skills/code-review-best-practices.md)
- performance-analysis-framework (../../shared-skills/performance-analysis-framework.md)

**Enhanced Features**
- Sequential Thinking integration (conditional mode)
- Improved cross-plugin skill sharing
- Better error handling and recovery
- Enhanced documentation and examples

### Improved

**Agent Quality**
- All agents follow consistent template structure
- Enhanced process phase documentation
- Better success criteria definitions
- Improved error handling sections
- More detailed best practices

**Documentation**
- Updated README with v2.0.0 information
- Added "What's New in v2.0.0" section
- Enhanced plugin status information
- Improved feature descriptions

### Removed

**Local Skills**
- Removed `skills/code-review-checklist.md` (replaced by shared skill)

### Migration Notes

**For Plugin Users**
- No command syntax changes - all commands work identically
- Skills now located in `shared-skills/` directory
- All functionality preserved with improved quality
- No breaking changes to command interface

**For Plugin Developers**
- Skills reference updated in plugin.json
- Agent specifications follow new template structure
- Sequential Thinking support documented
- All agents include "Skills Referenced" section

### Technical Details

**Files Updated**
- plugin.json (v2.0.0, shared skills, metadata)
- CHANGELOG.md (v2.0.0 entry)
- README.md (v2.0.0, what's new section)
- agents/local-pr-reviewer.md (v2.0.0)
- agents/pr-comprehensive-reviewer.md (v2.0.0)
- agents/remote-pr-local-analyzer.md (v2.0.0)
- agents/solution-validator.md (v2.0.0)

**Files Removed**
- skills/code-review-checklist.md

**Skills Referenced**
- Shared: code-review-best-practices
- Shared: performance-analysis-framework

---

## [1.1.0] - 2025-10-30

### Added

#### New Agents
- **local-pr-reviewer** - Review local Git branch changes without GitHub access
  - Works entirely offline with Git commands (no network needed)
  - 6-phase workflow: Initialize → Fetch Changes → Review Quality → Impact Analysis → Test/Docs → Report
  - Applies comprehensive CLAUDE.md code review standards
  - Detects security issues (SQL injection, XSS, hardcoded secrets)
  - Identifies performance problems (N+1 queries, memory leaks, inefficient async)
  - Assesses architecture compliance (SOLID principles, design patterns)
  - Evaluates code quality (naming, complexity, duplication)
  - Analyzes impact of changes on codebase
  - Generates comprehensive markdown reports to `marketplace/output/reviews/`
  - Processing time: 5-10 minutes for typical changes

- **remote-pr-local-analyzer** - Deep PR review combining GitHub context with local impact analysis
  - Fetches GitHub PR metadata and comments via GitHub MCP
  - Auto-fetches and checks out PR branch locally
  - 6-phase workflow with advanced analysis capabilities
  - **Cross-file reference detection**: Find all code that calls changed methods/classes
  - **Dependency tracing**: Map how changes ripple through the codebase
  - **Breaking change detection**: Identify API/signature changes that could break callers
  - **Test coverage verification**: Ensure impacted code has test coverage
  - Combines GitHub context (PR description, comments, reviews) with local analysis
  - Generates comprehensive report with all findings and impact assessment
  - Processing time: 15-25 minutes for comprehensive analysis

#### New Commands
- **/review-local-pr** - Review local Git branch changes offline
  - Syntax: `/review-local-pr <base-branch> [compare-branch] [--async|--wait] [--report=full|summary]`
  - Supports multiple scenarios:
    - Branch-to-branch comparison: `review-local-pr main feature-branch`
    - Uncommitted changes: `review-local-pr HEAD`
    - Commit range: `review-local-pr HEAD~5 HEAD`
  - No network required (works offline)
  - Ideal for pre-push self-review
  - Processing time: 5-10 minutes
  - Full and summary report modes

- **/review-pr-local** - Deep PR review by pulling branch locally
  - Syntax: `/review-pr-local <owner/repo> <pr-number> [--async|--wait] [--report=full|summary]`
  - Auto-fetches PR branch for local analysis
  - Requires GitHub MCP for PR metadata
  - Comprehensive impact analysis with cross-file references
  - Breaking change detection and risk assessment
  - Processing time: 15-25 minutes
  - Ideal for important/risky PRs, security changes, architectural changes

#### New Features
- **Three-Tier PR Review System**: Choose the right review depth:
  - `/review-pr` (5-10 min): Quick GitHub API review
  - `/review-local-pr` (5-10 min): Local offline review
  - `/review-pr-local` (15-25 min): Deep local analysis with impact

- **Pre-push Quality Gate**: Review uncommitted changes before committing
- **Offline Capability**: Full code review without network access
- **Deep Impact Analysis**: Understand how changes affect the entire codebase
- **Cross-file Reference Search**: Find all callers using Git grep patterns
- **Breaking Change Alerts**: Identify API/signature changes that break code
- **Dependency Impact Mapping**: Visualize which components are affected
- **Test Coverage Checking**: Verify new/modified code has adequate tests
- **Async Deep Analysis**: Background processing for comprehensive reviews

#### Enhanced Features
- **plugin.json** updated to v1.1.0
  - Added 2 new agents (local-pr-reviewer, remote-pr-local-analyzer)
  - Added 2 new commands (/review-local-pr, /review-pr-local)
  - Updated features list with new capabilities
  - Marked new items with `"new_in_v1": "1.1.0"`
  - Added processing time specifications

- **README.md** significantly expanded
  - New overview highlighting three-tier review system
  - New "Three-Tier PR Review" feature section
  - Expanded "Quick Start" with distinct review workflows
  - New "PR Review Decision Matrix" for command selection
  - Updated agent and command descriptions with processing times
  - Decision guide for choosing between review commands

### Technical Specifications

#### Local PR Reviewer (agents/local-pr-reviewer.md)
- **6 Phases**: Initialize (1m) → Fetch (2-3m) → Review (3-4m) → Impact (1-2m) → Test/Docs (1m) → Report (1m)
- **Review Areas**: Security, Performance, Architecture, Code Quality
- **Search Patterns**:
  - SQL Injection: `grep -r "ExecuteQuery.*+.*"`, `grep -r "string.*sql.*="`
  - Hardcoded Secrets: `grep -r -i "password.*=.*\"`, `grep -r -i "apikey.*=.*\"`
  - N+1 Queries: `grep -r "foreach.*{" -A 5 | grep -i "query|execute|select"`
  - Blocking Async: `grep -r "\.Result\|\.Wait()"`
  - Missing Disposal: `grep -r "new.*Disposable" | grep -v "using"`
- **Output**: Markdown report with Executive Summary, Findings (by severity), Impact Analysis, Recommendations

#### Remote PR Local Analyzer (agents/remote-pr-local-analyzer.md)
- **6 Phases**: Initialize (2m) → Auto-Fetch (2-3m) → Code Review (5-7m) → Impact Analysis (4-6m) → Compile Context (1-2m) → Report (2-3m)
- **Git Operations**: `git fetch origin pull/{number}/head:pr-{number}`, `git diff`, `git log`
- **Impact Analysis**:
  - Cross-file references: Find all usages via grep with context
  - Dependency tracing: Map imports and component relationships
  - Breaking changes: Detect removed/changed public methods, signature changes
  - Test coverage: Verify test files exist for changed code
- **Output**: Comprehensive markdown report combining GitHub metadata + local analysis

### Documentation Changes
- 2 new agent specification files (13,000+ lines total)
- 2 new command specification files (7,000+ lines total)
- Updated README.md with new features, examples, and decision matrix
- Updated plugin.json with version 1.1.0
- This CHANGELOG documenting v1.1.0 changes

### Backward Compatibility
✅ Fully backward compatible - no breaking changes
- Existing `/review-pr` command works unchanged
- Existing `/validate-solution` command unchanged
- New commands are purely additive

### Performance Improvements
- Local PR review optimized for fast feedback (5-10 min)
- Deep analysis with async support for long-running reviews
- Memory-efficient processing for large codebases
- Search patterns optimized for common issues

### Error Handling
- Not a Git repository detection
- Missing branch error handling with suggestions
- Binary file detection with warnings
- Merge conflict detection
- Network connectivity issues (for GitHub MCP)

### Integration
- Works with existing Review Suite commands
- Complementary to Analysis Toolkit for deep dives
- Part of three-tier PR review ecosystem
- Supports async processing with task status tracking

---

## [1.0.0] - 2025-10-30

### Added

#### Agents
- **pr-comprehensive-reviewer** - Comprehensive analysis of GitHub pull requests
  - Fetches PR details and code changes from GitHub MCP
  - Security vulnerability detection (SQL injection, XSS, auth bypass, hardcoded secrets)
  - Architecture assessment (SOLID principles, design patterns, code organization)
  - Performance analysis (N+1 queries, memory leaks, async patterns, LOH usage)
  - Testing and documentation review
  - Detailed review reports with line-by-line feedback
  - Risk assessment with severity levels
  - Markdown report generation to `marketplace/output/reviews/`

- **solution-validator** - Validation of proposed code solutions
  - Analyzes solution file structure and logic
  - Logic correctness checking (parameter validation, edge cases, null handling)
  - Architecture and design assessment (SOLID, patterns, code organization)
  - Code quality evaluation (readability, complexity, duplication, documentation)
  - Performance analysis (algorithms, database queries, memory usage)
  - Security assessment (input validation, secrets, vulnerabilities)
  - Generates validation reports with issues categorized by severity
  - Provides alternative approaches with pros/cons analysis
  - Risk assessment (correctness, performance, maintainability, testability, security)

#### Commands
- **/review-pr** - Comprehensive GitHub pull request review
  - Syntax: `/review-pr <owner>/<repo> <pr-number> [--async|--wait] [--report=full|summary]`
  - Supports synchronous (--wait) and asynchronous (--async) execution
  - Optional report level selection (full or summary)
  - Validates GitHub repository format and PR number
  - Queues tasks in background task coordinator for async execution
  - Returns task ID for tracking async reviews
  - Generates comprehensive or summary reports
  - Error handling for invalid inputs, missing repositories, unavailable GitHub MCP

- **/validate-solution** - Solution file validation
  - Syntax: `/validate-solution <file-path> [--async|--wait] [--report=full|summary]`
  - Supports relative and absolute file paths
  - Works with C#, SQL, JavaScript, and other languages
  - Language-specific validation rules
  - Supports synchronous and asynchronous execution
  - Report level selection (full or summary)
  - File existence and permission validation
  - Queues tasks in background task coordinator
  - Error handling for missing files, permission issues, unsupported types

#### Skills
- **code-review-checklist** - Comprehensive code review guidelines
  - Pre-review setup and context gathering checklist
  - Critical priorities checklist:
    - Security vulnerabilities (SQL injection, XSS, auth, secrets)
    - Breaking changes (API, database schema, configuration, dependencies)
    - Performance regressions (N+1 queries, memory, async, algorithms, resources)
    - Integration risks (external services, transactions, dependencies)
    - Error handling gaps (exceptions, logging, rollback)
  - Detailed review checklist covering:
    - Code quality (naming, organization, methods, classes, constants)
    - SOLID principles (all 5 principles with guidance)
    - Design patterns (appropriate patterns, anti-patterns to avoid)
    - Type safety (null handling, conversions, collections)
    - C# specific (modern features, async, exceptions, logging, disposal)
    - ASP.NET WebForms specific (lifecycle, ViewState, binding, validation, session, Telerik)
    - Repository & Service pattern (data access, business logic, DI)
    - LINQ to SQL (query efficiency, concurrency, transactions)
    - Testing (presence, quality, test data)
    - Documentation (comments, XML docs, PR description, README)
    - Performance (algorithms, database, memory, caching)
    - Scalability (concurrency, load handling)
    - Maintainability (readability, complexity, flexibility)
  - Review comment guidelines (positive, constructive, types)
  - Review conclusion options (APPROVE, REQUEST CHANGES, COMMENT)
  - Common issues quick reference table
  - Timing guidelines for different review types
  - Continuous improvement recommendations

### Features

- **Comprehensive PR Analysis**: Full security, architecture, performance, and quality assessment
- **Multi-Language Support**: C#, SQL, JavaScript, and generic language support
- **Detailed Reports**: Markdown-formatted reports with specific findings and recommendations
- **Risk Assessment**: Severity-based issue categorization and impact analysis
- **SOLID Principles**: Dedicated SOLID principles evaluation
- **Design Pattern Review**: Recognition and guidance on design patterns and anti-patterns
- **Security Focus**: SQL injection, XSS, authentication, authorization, and secret detection
- **Performance Analysis**: N+1 queries, memory leaks, async patterns, LOH usage
- **Testing Assessment**: Test coverage and quality evaluation
- **Documentation Review**: Code comments, XML docs, PR descriptions, README updates
- **Async Execution**: Background processing with task status tracking
- **Sync Execution**: Immediate execution with blocking wait
- **Report Options**: Full comprehensive reports or quick summary reports
- **Error Handling**: Graceful error handling with helpful guidance
- **MCP Integration**: GitHub MCP for PR data fetching
- **Task Tracking**: Real-time progress updates via status files

### Documentation

- **README.md**: Comprehensive plugin documentation including:
  - Feature overview
  - Quick start guide with examples
  - Component descriptions
  - Review standards reference
  - Output structure
  - Analysis time estimates
  - Integration with other plugins
  - MCP requirements
  - Usage examples
  - FAQ
  - Troubleshooting guide
  - Related commands

- **CHANGELOG.md**: Version history and changes (this file)

### Supported Review Standards

Reviews are based on CLAUDE.md standards:
- Critical priorities (security, breaking changes, performance, integration, error handling)
- Domain-specific areas (memory management, ASP.NET WebForms, Repository & Service, architecture)
- Review context requirements (complete code review, not just diffs)
- SOLID principles assessment
- Design pattern evaluation
- Code quality metrics

### Output Locations

- Full PR reviews: `marketplace/output/reviews/<repo>-pr-<number>-review.md`
- Summary PR reviews: `marketplace/output/reviews/<repo>-pr-<number>-summary.md`
- Full solution validations: `marketplace/output/reviews/<filename>-validation.md`
- Summary validations: `marketplace/output/reviews/<filename>-validation-summary.md`
- Task status: `.claude/task-status/<task-id>.md`

### Integration Points

- Integrates with background task coordinator for async execution
- Delegated to by `/review-pr` and `/validate-solution` commands
- Works with GitHub MCP for PR data (optional)
- Supports all task queue mechanisms

### Task Coverage

- **Task #3**: Review PRs on GitHub (via pr-comprehensive-reviewer and /review-pr)
- **Task #11**: Find correct maintainable solutions (via solution-validator and /validate-solution)

## [0.1.0] - 2025-10-30 (Initial Development)

### Planned
- Plugin structure and configuration
- Agent and command templates
- Skill framework

---

## Version Strategy

This plugin follows semantic versioning:
- **MAJOR** (1.0, 2.0): Breaking changes to command syntax or report format
- **MINOR** (1.1, 1.2): New features or commands, backward compatible
- **PATCH** (1.0.1, 1.0.2): Bug fixes and documentation updates

## Known Limitations

### Current Version (1.0.0)

1. **GitHub PR Analysis**
   - Requires GitHub token with appropriate repository access
   - Large PRs (>1000 lines) may take longer
   - Draft PRs supported but noted as drafts

2. **Solution Validation**
   - Language-specific validation limited to detected file types
   - Very large files (>5000 lines) may have timeout warnings
   - Syntax errors in files may limit analysis completeness

3. **Performance**
   - Analysis time varies based on PR/file complexity
   - Estimated times are approximations
   - Very large codebases may need --async mode

### Future Enhancements

- [ ] Support for GitLab, Bitbucket in addition to GitHub
- [ ] Custom review criteria per team/project
- [ ] Review history and tracking across PRs
- [ ] Batch PR review with comparative analysis
- [ ] Integration with CI/CD for automatic PR reviews
- [ ] Team-based review consensus features
- [ ] Code review metrics and trends
- [ ] Custom checklist creation
- [ ] Review comment templates
- [ ] Automated fixes for common issues

## Migration Guide

### From Previous Versions
This is the first version (1.0.0). No migration needed.

## Contributors

- **Created**: 2025-10-30
- **Version 1.0.0**: Initial production release

## Support

For issues, suggestions, or contributions:
1. Review the README.md for usage examples
2. Check the FAQ section in README
3. Consult command documentation in `/commands` directory
4. Review agent documentation in `/agents` directory

## Related Plugins

- **Analysis Toolkit**: Stack trace analysis, Jira issue analysis, query optimization
- **Optimization Engine**: Query and algorithm optimization, performance tuning
- **Architecture Advisor**: Architecture analysis, design pattern guidance
- **Development Suite**: Code generation, debugging, refactoring

---

**Last Updated**: 2025-10-30
**Maintainer**: Claude Code Marketplace
**License**: MIT
