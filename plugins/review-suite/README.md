# Review Suite Plugin

Comprehensive code review and solution validation for quality assurance across your development workflow.

## What's New in v2.0.0

**Shared Skills Integration**: Review Suite now leverages the shared skills library for consistent methodology across all plugins:
- Migrated to shared `code-review-best-practices` skill
- Added `performance-analysis-framework` reference
- Enhanced agent specifications with Sequential Thinking support
- Improved error handling and documentation

**No Breaking Changes**: All commands work identically. Skills are now centralized for better cross-plugin consistency.

## Overview

The Review Suite plugin provides automated code review capabilities with four specialized agents:

1. **PR Comprehensive Reviewer** - Fast GitHub API-based analysis of pull requests (5-10 min)
2. **Local PR Reviewer** - Reviews local Git branches without GitHub access (5-10 min, offline)
3. **Remote PR Local Analyzer** - Deep impact analysis by pulling PR branch locally (15-25 min, comprehensive)
4. **Solution Validator** - Validates proposed code solutions for correctness, maintainability, and best practices

The plugin offers **three-tier PR review capability**: quick remote review, local offline review, and deep local analysis with comprehensive impact assessment. Combined with the code review checklist skill, this plugin ensures consistent, thorough review standards across your team.

## Features

### Three-Tier PR Review System
- **Quick Remote Review** (`/review-pr`): Fast GitHub API-based analysis (5-10 min)
- **Local Offline Review** (`/review-local-pr`): Review local branches without network (5-10 min, works offline)
- **Deep Local Analysis** (`/review-pr-local`): Auto-fetch PR branch + comprehensive impact analysis (15-25 min)

### Automated Code Review
- **GitHub PR Analysis**: Comprehensive review of GitHub pull requests with metadata context
- **Local Branch Review**: Review local Git branches before pushing to remote
- **Remote PR Local Review**: Pull remote PR branch locally for deep impact analysis
- **Security Assessment**: Detects SQL injection, XSS, authentication issues, hardcoded secrets
- **Architecture Review**: SOLID principles, design patterns, code organization
- **Performance Analysis**: N+1 queries, memory leaks, inefficient async patterns
- **Testing Assessment**: Test coverage, test quality, edge case validation
- **Documentation Review**: Comments, API documentation, breaking changes
- **Cross-File Reference Detection**: Find all callers of changed methods
- **Breaking Change Detection**: Identify API signature changes that could break callers
- **Dependency Tracing**: Map how changes ripple through the codebase
- **Test Coverage Verification**: Ensure impacted areas have test coverage

### Solution Validation
- **Logic Correctness**: Edge cases, control flow, null handling
- **Design Assessment**: SOLID principles, design patterns, architecture
- **Code Quality**: Readability, complexity, duplication, documentation
- **Performance**: Algorithms, database queries, memory usage
- **Security**: Input validation, secrets, vulnerability patterns

### Comprehensive Reports
- Full detailed reports with specific line-by-line feedback
- Summary reports for quick overviews
- Risk assessments with severity levels
- Actionable recommendations
- Alternative approaches with pros/cons

## Installation

The Review Suite plugin is part of the marketplace ecosystem:

```bash
# Already installed in: marketplace/plugins/review-suite/
# Ready to use immediately
```

## Quick Start

### Three-Tier PR Review

**Choose the right review for your needs:**

```bash
# 1️⃣ Quick GitHub API review (5-10 min, requires GitHub MCP)
/review-pr my-org/my-repo 42 --wait

# 2️⃣ Local branch review offline (5-10 min, no network needed)
/review-local-pr main feature-branch --wait

# 3️⃣ Deep PR analysis with local impact (15-25 min, auto-fetches branch)
/review-pr-local my-org/my-repo 42 --wait
```

**Decision Guide:**
- **Use `/review-pr`** for quick feedback on GitHub PRs during review
- **Use `/review-local-pr`** for pre-push self-review of local changes
- **Use `/review-pr-local`** for comprehensive impact analysis on important/risky PRs

### Review a GitHub PR (Fast)

```bash
# Quick review (synchronous, full report)
/review-pr microsoft/dotnet 12345 --wait

# Background review (asynchronous)
/review-pr microsoft/dotnet 12345 --async

# Quick summary
/review-pr my-org/my-repo 567 --report=summary
```

### Review Local Branch Changes

```bash
# Review uncommitted changes
/review-local-pr HEAD --wait

# Review feature branch against main
/review-local-pr main feature-auth --wait

# Async review for large changes
/review-local-pr main big-refactor --async
```

### Deep PR Review with Impact Analysis

```bash
# Pull PR locally and perform deep analysis
/review-pr-local my-org/my-repo 42 --wait

# Async deep review for complex changes
/review-pr-local my-org/my-repo 99 --async --report=full
```

### Validate a Solution

```bash
# Validate a solution file (synchronous)
/validate-solution src/Services/UserService.cs --wait

# Background validation
/validate-solution src/Services/UserService.cs --async

# Quick validation summary
/validate-solution Models/User.cs --report=summary
```

## Components

### Agents

#### PR Comprehensive Reviewer
- **File**: `agents/pr-comprehensive-reviewer.md`
- **Purpose**: Fast GitHub API-based analysis of pull requests
- **Process**:
  1. Fetch PR details from GitHub MCP
  2. Analyze code changes and diffs
  3. Assess security, architecture, performance
  4. Review testing and documentation
  5. Generate detailed review report
- **Output**: `marketplace/output/reviews/<repo>-pr-<number>-review.md`
- **Task Coverage**: Task #3 (Review PRs on GitHub)
- **Processing Time**: 5-10 minutes

#### Local PR Reviewer
- **File**: `agents/local-pr-reviewer.md`
- **Purpose**: Review local Git branch changes without GitHub access
- **Process**:
  1. Validate Git repository and branches
  2. Fetch and analyze diffs
  3. Review code quality (security, performance, architecture)
  4. Analyze impact of changes
  5. Verify test coverage and documentation
  6. Generate comprehensive markdown report
- **Output**: `marketplace/output/reviews/local-pr-{timestamp}.md`
- **Task Coverage**: Local PR review (pre-push quality gate)
- **Processing Time**: 5-10 minutes
- **MCP Required**: None (offline capability)

#### Remote PR Local Analyzer
- **File**: `agents/remote-pr-local-analyzer.md`
- **Purpose**: Deep code review with comprehensive local impact analysis for GitHub PRs
- **Process**:
  1. Fetch PR metadata from GitHub
  2. Auto-fetch and checkout PR branch locally
  3. Review code quality (security, performance, architecture)
  4. Advanced impact analysis:
     - Cross-file reference search (find all callers)
     - Dependency tracing (map ripple effects)
     - Breaking change detection (API compatibility)
     - Test coverage verification
  5. Compile GitHub context (metadata, comments)
  6. Generate comprehensive report with all findings
- **Output**: `marketplace/output/reviews/pr-local-{owner}-{repo}-{number}-{timestamp}.md`
- **Task Coverage**: Deep PR review with impact analysis
- **Processing Time**: 15-25 minutes
- **MCP Required**: GitHub (for PR metadata and fetch)

#### Solution Validator
- **File**: `agents/solution-validator.md`
- **Purpose**: Validate proposed code solutions
- **Process**:
  1. Analyze solution file structure
  2. Check logic correctness and edge cases
  3. Assess architecture and design patterns
  4. Evaluate code quality
  5. Generate validation report
- **Output**: `marketplace/output/reviews/<filename>-validation.md`
- **Task Coverage**: Task #11 (Find correct maintainable solutions)
- **Processing Time**: 8-15 minutes

### Commands

#### /review-pr (Quick Remote Review)
- **Usage**: `/review-pr <owner>/<repo> <pr-number> [--async|--wait] [--report=full|summary]`
- **File**: `commands/review-pr.md`
- **Purpose**: Fast GitHub API-based PR review
- **Delegates To**: pr-comprehensive-reviewer agent
- **Processing Time**: 5-10 minutes
- **MCP Required**: GitHub
- **When to Use**: Quick feedback during code review, real-time collaboration
- **Examples**:
  ```bash
  /review-pr microsoft/dotnet 12345 --wait
  /review-pr my-org/my-repo 567 --async
  /review-pr anthropics/claude-code 89 --report=summary
  ```

#### /review-local-pr (Local Offline Review)
- **Usage**: `/review-local-pr <base-branch> [compare-branch] [--async|--wait] [--report=full|summary]`
- **File**: `commands/review-local-pr.md`
- **Purpose**: Review local Git branch changes without network
- **Delegates To**: local-pr-reviewer agent
- **Processing Time**: 5-10 minutes
- **MCP Required**: None (works offline)
- **When to Use**: Pre-push self-review, uncommitted changes, no network access
- **Examples**:
  ```bash
  /review-local-pr main feature-auth --wait          # Review branch
  /review-local-pr HEAD --wait                        # Review uncommitted changes
  /review-local-pr main feature-branch --async        # Async review
  ```

#### /review-pr-local (Deep Local Analysis)
- **Usage**: `/review-pr-local <owner/repo> <pr-number> [--async|--wait] [--report=full|summary]`
- **File**: `commands/review-pr-local.md`
- **Purpose**: Deep PR review by pulling branch locally with comprehensive impact analysis
- **Delegates To**: remote-pr-local-analyzer agent
- **Processing Time**: 15-25 minutes
- **MCP Required**: GitHub
- **When to Use**: Important/risky PRs, security changes, architectural changes, impact analysis needed
- **Features**:
  - Auto-fetches PR branch locally
  - Cross-file reference search
  - Breaking change detection
  - Dependency tracing
  - Test coverage verification
  - GitHub context (metadata, comments)
- **Examples**:
  ```bash
  /review-pr-local my-org/my-repo 42 --wait          # Deep analysis, synchronous
  /review-pr-local my-org/my-repo 99 --async         # Deep analysis, background
  /review-pr-local acme/backend 1 --report=full      # Full detailed report
  ```

#### /validate-solution
- **Usage**: `/validate-solution <file-path> [--async|--wait] [--report=full|summary]`
- **File**: `commands/validate-solution.md`
- **Purpose**: Validate proposed solution code
- **Delegates To**: solution-validator agent
- **Processing Time**: 8-15 minutes
- **MCP Required**: None
- **Examples**:
  ```bash
  /validate-solution src/Services/UserService.cs --wait
  /validate-solution Models/User.cs --async
  /validate-solution Repository/DataAccess.cs --report=summary
  ```

### Skills

Review Suite leverages shared skills for consistent methodology:

#### Code Review Best Practices (Shared)
- **File**: `../../shared-skills/code-review-best-practices.md`
- **Purpose**: Best practices for conducting thorough code reviews
- **Contents**:
  - Security vulnerability detection
  - Performance issue identification
  - SOLID principles assessment
  - Design pattern evaluation
  - Testing and documentation standards

#### Performance Analysis Framework (Shared)
- **File**: `../../shared-skills/performance-analysis-framework.md`
- **Purpose**: Framework for identifying and analyzing performance bottlenecks
- **Contents**:
  - Database query optimization
  - Memory management patterns
  - Async/await best practices
  - N+1 query detection
  - Resource utilization analysis

## Review Standards Applied

The Review Suite follows standards from CLAUDE.md:

### Critical Priorities (Review Order)
1. **Security Vulnerabilities** – SQL injection, XSS, auth bypass, hardcoded secrets
2. **Breaking Changes** – API compatibility, database schema changes, dependency impacts
3. **Performance Regressions** – N+1 queries, memory leaks, inefficient async patterns, LOH usage
4. **Integration Risks** – External service calls, transaction boundaries, dependency changes
5. **Error Handling Gaps** – Missing exception handling, logging, transaction rollback

### Domain-Specific Review Areas
- **Memory Management**: IDisposable pattern, disposal usage, memory-heavy objects, StringBuilder, LOH
- **ASP.NET WebForms**: Page lifecycle, ViewState, postback flow, Session, Telerik control patterns
- **Repository & Service Pattern**: UnitOfWork coordination, async methods, AsNoTracking(), concurrency
- **Architecture & Performance**: SOLID principles, DI usage, async flows, request/response cycle

## Output Structure

Reviews and validations are saved to organized directories:

```
marketplace/output/reviews/
├── <repo>-pr-<number>-review.md          # Full PR review
├── <repo>-pr-<number>-summary.md         # Summary PR review
├── <filename>-validation.md              # Full solution validation
├── <filename>-validation-summary.md      # Summary validation
└── ...
```

Status files for async tasks:
```
.claude/task-status/
├── task-20251030-160000-pr-abc123.md     # PR review progress
├── task-20251030-160030-val-xyz789.md    # Solution validation progress
└── ...
```

## Typical Analysis Time

### PR Reviews
- **Small PR** (< 100 lines): 3-8 minutes
- **Medium PR** (100-500 lines): 8-15 minutes
- **Large PR** (> 500 lines): 15-30 minutes
- **Complex PR** (architecture changes): 20-45 minutes

### Solution Validations
- **Small file** (< 100 lines): 2-4 minutes
- **Medium file** (100-500 lines): 5-10 minutes
- **Large file** (500-2000 lines): 10-20 minutes
- **Very large file** (> 2000 lines): 20-30 minutes

**Recommendation**: Use `--async` for large reviews/validations to avoid timeouts.

## Integration with Other Plugins

- **Analysis Toolkit**: Use `/analyze-stacktrace` to analyze errors found during review
- **Optimization Engine**: Use `/optimize-query` for database query recommendations from reviews
- **Architecture Advisor**: Use `/analyze-architecture` for major architectural concerns found in reviews

## MCP Requirements

### GitHub MCP (Required for PR Reviews)
- Server: `github`
- Provides PR details, code diffs, commit information
- Configuration:
  ```json
  {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
  ```

### Local File Access (Required for Solution Validation)
- No MCP required
- Reads local solution files directly
- Works with any file type

## Usage Examples

### Pre-Implementation Review
Validate your approach before starting work:
```bash
/validate-solution src/ProposedApproach.cs --wait
# Review recommendations
# Refine approach if needed
# Start implementation
```

### Self-Review Before PR
Self-review before requesting team review:
```bash
/validate-solution src/MyChanges.cs --wait
# Fix issues found
# Submit PR with confidence
```

### PR Review
Get comprehensive feedback on GitHub PR:
```bash
/review-pr my-org/my-repo 1234 --wait
# Review findings
# Respond to feedback
# Make improvements
```

### Batch Reviews
Queue multiple reviews:
```bash
/review-pr my-org/my-repo 1234 --async
/review-pr my-org/my-repo 1235 --async
/review-pr my-org/my-repo 1236 --async
/task-status task-id  # Check progress later
```

### Design Review
Get feedback on proposed design:
```bash
/validate-solution src/NewArchitecture.cs --wait
# Share report with team
# Discuss findings together
# Refine design
```

## FAQ

**Q: What if a file has syntax errors?**
A: The validation identifies syntax errors and may provide limited analysis. Fix syntax errors first if possible.

**Q: Can I review private repositories?**
A: Yes, if your GitHub token has access to the private repository. Ensure GITHUB_TOKEN is configured.

**Q: How is this different from GitHub's built-in review?**
A: Much more comprehensive:
- GitHub: Basic comments on code
- This plugin: Security, architecture, performance, testing, documentation, design patterns, SOLID principles, risk assessment

**Q: Can I customize the review standards?**
A: Review standards follow CLAUDE.md. Contact your team lead to customize standards.

**Q: What if the PR has conflicts?**
A: The review analyzes the code changes. Merge conflicts are noted if present.

**Q: Can reviewers override the agent's findings?**
A: Yes, the agent's review is guidance. Human reviewers have final say on code quality standards.

**Q: Are there language-specific considerations?**
A: Yes! The plugin includes specific checks for:
- C#/.NET (SOLID, async/await, IDisposable, LINQ)
- ASP.NET WebForms (lifecycle, ViewState, Telerik controls)
- SQL (query optimization, joins, indexes)
- And more...

## Troubleshooting

### GitHub MCP Not Available
Ensure GitHub MCP is configured in `.mcp.json`:
```json
{
  "github": {
    "command": "npx",
    "args": ["@modelcontextprotocol/server-github"],
    "env": { "GITHUB_TOKEN": "your-token" }
  }
}
```

### File Not Found
Verify file path is correct and relative to project root:
```bash
/validate-solution src/Services/UserService.cs  # ✅ Correct
/validate-solution ./Services/UserService.cs    # ✅ Also correct
```

### Timeout
Very large files/PRs may timeout. Use `--async` flag:
```bash
/review-pr my-org/my-repo 1234 --async
```

## Related Commands

- `/analyze-stacktrace` - Analyze error traces from reviews
- `/analyze-impact <file>` - Analyze impact of code changes
- `/validate-solution` - Validate proposed solutions
- `/review-pr` - Review GitHub PRs
- `/task-status <task-id>` - Check async review progress

## PR Review Decision Matrix

Choose the right review command for your use case:

| Aspect | /review-pr | /review-local-pr | /review-pr-local |
|--------|-----------|-----------------|------------------|
| **Speed** | 5-10 min | 5-10 min | 15-25 min |
| **Network Required** | Yes | No | Yes |
| **GitHub Context** | Yes | No | Yes |
| **Cross-file References** | No | Limited | Yes |
| **Breaking Changes** | Limited | Limited | Yes |
| **Dependency Tracing** | No | No | Yes |
| **Test Coverage Check** | Limited | Yes | Yes |
| **Best For** | Quick feedback | Pre-push review | Impact analysis |
| **MCP Required** | GitHub | None | GitHub |
| **Use When** | Reviewing on GitHub | Before committing | Important/risky PRs |

## Plugin Status

- **Version**: 2.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-01-15
- **Tasks Covered**: Task #3, Task #11, Local PR review, Deep analysis
- **Agents**: 4 (PR Comprehensive Reviewer, Local PR Reviewer, Remote PR Local Analyzer, Solution Validator)
- **Commands**: 4 (review-pr, review-local-pr, review-pr-local, validate-solution)
- **Skills**: 2 shared (code-review-best-practices, performance-analysis-framework)
- **MCP Servers**: GitHub (required for /review-pr and /review-pr-local), None (local/offline commands)

## Contributing

To improve this plugin:
1. Update agent markdown files (`agents/*.md`)
2. Modify command definitions (`commands/*.md`)
3. Enhance skill documentation (`skills/*.md`)
4. Test with various code samples
5. Gather team feedback

Changes take effect immediately - no restart required.

## Support

For issues or suggestions:
1. Check this README
2. Review FAQ section
3. Check command documentation
4. Contact your development team

---

**Part of the Claude Code Marketplace**
Review Suite Plugin v2.0.0 (2026-01-15)
