# Planning Suite Plugin

**Version**: 2.0.0
**Status**: Production
**Last Updated**: 2026-01-15

A comprehensive planning toolkit that creates detailed execution plans with code-level changes, file modifications, and step-by-step implementation guidance. Automatically integrates with existing Jira analysis to turn findings into actionable implementation plans.

## What's New in v2.0.0

- **Enhanced Documentation Standards**: Integrated technical writing guide for better plan documentation
- **Confluence Templates**: Direct access to documentation templates for planning artifacts
- **Conditional Sequential Thinking**: Smarter reasoning for complex planning scenarios
- **Shared Skills Integration**: Centralized knowledge base for better consistency
- **Improved Planning Templates**: Enhanced with documentation best practices
- **Better Output Formats**: Standardized plan structure and formatting

## Overview

Planning Suite helps you create thorough, actionable execution plans **before** you start coding. It automatically:

- ✅ Detects and integrates existing Jira analysis
- ✅ Generates detailed file-level and code-level changes
- ✅ Plans execution steps with dependencies
- ✅ Provides code snippets and patterns
- ✅ Creates testing strategies
- ✅ Assesses risks and mitigation approaches
- ✅ Estimates effort and timeline

## Quick Start

### Most Common: Plan a Task
```bash
/plan "Fix user login timeout issue"

# Plan with existing analysis
/plan "PROJ-456"

# Get more details
/plan "Add two-factor authentication" --detailed

# Run in background
/plan "Major refactoring" --detailed --async
```

### Plan a Feature
```bash
/plan-feature "Add user export to CSV and Excel"

/plan-feature "Implement real-time notifications" --detailed
```

### Plan Refactoring
```bash
/plan-refactor "Extract payment service from UserService"

/plan-refactor "Optimize slow database queries" --detailed
```

### Phase-by-Phase Planning (with Approvals)
```bash
/plan-phases "Implement user authentication system"

# Planner will ask for approval after each phase
```

## Features

### 🎯 Automatic Analysis Integration
- Detects Jira ticket references (PROJ-123)
- Finds and reads existing analysis automatically
- Incorporates findings into the plan
- Saves duplicate investigation work

### 📋 Comprehensive Planning
- File-level changes (create, modify, delete)
- Code-level implementation details with snippets
- Dependency analysis and integration points
- Execution order with dependencies
- Risk assessment and mitigation
- Testing strategy
- Rollback procedures
- Timeline estimation

### 🔄 Multiple Execution Modes
- **Autonomous**: Complete plan without interaction
- **Interactive**: Phase-by-phase with approval gates
- **Integrated**: Works with existing analysis automatically

### 📊 Adjustable Detail Levels
- **Shallow**: Quick plan (3-5 minutes)
- **Medium**: Detailed plan (5-10 minutes) - DEFAULT
- **Deep**: Comprehensive with all details (10-15+ minutes)

### 📚 Template-Based Planning
Use templates for common scenarios:
- **new-entity**: CRUD entity with service layer
- **api-endpoint**: REST API or WebForms page
- **bug-fix**: Bug fix with root cause analysis
- **performance-optimization**: Performance improvements
- **architecture-change**: Major system changes

### 🔗 Plugin Integration
Works with other marketplace plugins:
- **analysis-toolkit**: Leverage impact analysis findings
- **architecture-advisor**: Get pattern recommendations
- **development-suite**: Reference code generators
- **brainstorming-suite**: Link to ideation outputs

## Agents

### Task Execution Planner
Creates detailed execution plans for specific tasks (bug fixes, enhancements, configurations).
- 8 structured phases
- Automatic analysis detection and integration
- Code-level guidance with snippets
- Testing and validation strategy
- Used by: `/plan` command

### Feature Development Planner
Comprehensive feature implementation planning with architecture design.
- 8 structured phases
- Complete component breakdown
- Phased implementation approach
- Code examples and patterns
- Used by: `/plan-feature` command

### Refactoring Planner
Safe refactoring planning with dependency analysis and risk mitigation.
- 9 structured phases
- Complete dependency tracing
- Before/after code comparisons
- Risk assessment with mitigations
- Rollback strategies
- Used by: `/plan-refactor` command

### Incremental Planner
Phase-by-phase planning with approval gates for interactive planning.
- Decompose into independent phases
- Ask for approval after each phase
- Refine based on feedback
- Clear phase sequencing
- Used by: `/plan-phases` command

## Commands

### `/plan <description> [--detailed] [--async]`
Most flexible planning command with automatic type detection.

**Examples**:
```bash
/plan "Fix authentication timeout bug"
/plan "PROJ-456"
/plan "Implement user dashboard" --detailed
/plan "Database migration planning" --detailed --async
```

### `/plan-feature <description> [--detailed] [--async]`
Feature-specific planning for new features and enhancements.

**Examples**:
```bash
/plan-feature "Add CSV export functionality"
/plan-feature "Implement caching layer for APIs" --detailed
```

### `/plan-refactor <scope> [--detailed] [--async]`
Refactoring-specific planning with safety emphasis.

**Examples**:
```bash
/plan-refactor "Extract payment service"
/plan-refactor "Migrate to async/await patterns" --detailed
```

### `/plan-phases <description> [--async]`
Phase-by-phase planning with interactive approval gates.

**Examples**:
```bash
/plan-phases "Build REST API for mobile app"
/plan-phases "Redesign authentication system" --async
```

## Output Format

Plans include:

```markdown
# [Task/Feature/Refactoring] Plan: [Name]

## Executive Summary
[Overview of what plan accomplishes]

## Scope & Objectives
[In scope, out of scope, success criteria]

## Analysis Summary
[If analysis was found and integrated]

## Architecture & Design
[Design decisions, patterns, alternatives]

## File-Level Changes
[Files to create, modify, delete]

## Code-Level Details
[Code snippets, method signatures]

## Dependency Analysis
[Component dependencies, integration order]

## Implementation Plan
[Step-by-step with code and effort]

## Testing Strategy
[Unit tests, integration tests, validation]

## Risk Assessment
[Identified risks with mitigation]

## Rollback Strategy
[How to revert if needed]

## Timeline
[Effort estimates per phase/step]
```

## Integration with Analysis

### Automatic Analysis Integration

If you've already analyzed a Jira ticket:

```bash
# First: Analyze the ticket
/analyze-jira-issue PROJ-456 --wait

# Then: Create execution plan with analysis integrated
/plan "PROJ-456"

# Or reference the analysis explicitly
/plan "Implement fix from PROJ-456 analysis"
```

The planning agent will:
1. Find the analysis output
2. Read root cause findings
3. Extract affected files
4. Incorporate recommendations
5. Build detailed plan from analysis

## Workflow Examples

### Example 1: Bug Fix Based on Analysis
```bash
# Step 1: Analyze the issue
/analyze-jira-issue PROJ-789

# Step 2: Plan the fix using analysis
/plan "PROJ-789"

# Output includes:
# - Root cause from analysis
# - Affected files already identified
# - Recommended solution approach
# - Step-by-step fix plan
# - Testing strategy
```

### Example 2: Complex Feature Planning
```bash
# Plan feature with full detail
/plan-feature "Implement user authentication with OAuth" --detailed

# Output includes:
# - Architecture with OAuth flow
# - All components to create
# - Database schema changes
# - Dependency graph
# - Phased implementation steps
# - Complete code examples
# - Comprehensive testing plan
```

### Example 3: Safe Refactoring
```bash
# Plan refactoring with safety
/plan-refactor "Extract payment service into separate module" --detailed

# Output includes:
# - Current architecture analysis
# - All dependencies identified
# - Breaking changes documented
# - Risk assessment with mitigations
# - Implementation sequence
# - Before/after code samples
# - Rollback procedures
```

### Example 4: Interactive Phase Planning
```bash
# Plan with approvals
/plan-phases "Implement real-time notifications"

# Interaction:
# ✅ Approve Phase 1: Database schema
# ✅ Approve Phase 2: Service layer
# ✅ Approve Phase 3: Notification service
# ✅ Approve Phase 4: API integration
# ✅ Approve Phase 5: Client-side handling

# Result: Phase-by-phase plan with all approvals documented
```

## Depth Levels Explained

### Shallow (3-5 minutes)
Use when:
- Quick reference needed
- Simple fixes
- Clear scope

Includes:
- Basic analysis
- High-level steps
- Minimal code examples

### Medium - DEFAULT (5-10 minutes)
Use when:
- Standard task or feature
- Need good detail but not exhaustive
- Typical planning needs

Includes:
- Thorough analysis
- Detailed steps with code signatures
- Code snippet examples
- Standard testing plan

### Deep (10-15+ minutes)
Use when:
- Complex feature
- Risky changes
- Critical tasks
- Need everything documented

Includes:
- Very detailed analysis
- Complete code implementations
- Before/after comparisons
- Comprehensive testing with code
- Risk mitigation details
- Performance considerations
- Edge case handling

## Tips & Best Practices

### Before Planning
1. **Have context**: Read related documentation
2. **Check analysis**: See if Jira analysis exists
3. **Know constraints**: Timeline, tech choices, etc.

### During Planning
1. **Be specific**: "Fix login timeout" not "Fix login"
2. **Reference analysis**: Mention ticket number if analysis exists
3. **Choose right command**: Use `/plan-feature` for features, `/plan-refactor` for refactoring
4. **Use --detailed for complex work**: Gets comprehensive planning

### After Planning
1. **Review output**: Read generated plan documents
2. **Ask questions**: If plan is unclear, ask for clarification
3. **Share with team**: Get feedback before implementation
4. **Follow the plan**: Use it as implementation guide
5. **Update as needed**: Adjust if circumstances change

## When to Use Each Command

| Need | Command | Depth | Time |
|------|---------|-------|------|
| Quick fix plan | `/plan` | medium | 5-10 min |
| New feature plan | `/plan-feature` | medium | 10-15 min |
| Refactoring plan | `/plan-refactor` | medium | 10-15 min |
| Complex feature | `/plan-feature` | deep | 15-25 min |
| Large refactoring | `/plan-refactor` | deep | 15-25 min |
| Team alignment | `/plan-phases` | full | 20-40 min |
| Quick reference | `/plan` | shallow | 3-5 min |

## Output Locations

Plans are saved to:
- **Task plans**: `marketplace/output/planning/tasks/`
- **Feature plans**: `marketplace/output/planning/features/`
- **Refactoring plans**: `marketplace/output/planning/refactoring/`
- **Phase plans**: `marketplace/output/planning/incremental/`

## Skills & Methodology

The plugin includes a planning methodology skill (`planning-methodology.md`) with:
- Core planning principles
- Dependency analysis techniques
- Effort estimation approaches
- Risk assessment frameworks
- Testing strategy development
- Common planning mistakes and solutions

## Support for Technologies

**Languages**:
- C#
- JavaScript
- Python
- Java

**Frameworks**:
- .NET Framework 4.8
- ASP.NET WebForms
- React
- Angular

**Scenarios**:
- Task execution planning
- Feature development
- Refactoring
- Bug fixes
- Performance optimization
- Architecture changes

## Related Plugins

- **analysis-toolkit**: Run analysis first, planning uses findings
- **architecture-advisor**: Get pattern recommendations during planning
- **development-suite**: Reference code generators in plans
- **brainstorming-suite**: Brainstorm before planning for complex features

## Troubleshooting

### Plan seems too long
- Use `--async` to run in background
- Use `--shallow` for quick reference (if you need less detail)

### Plan missing some details
- Use `--detailed` flag for comprehensive analysis
- Check if analysis exists for related ticket

### Need approval before starting
- Use `/plan-phases` for interactive approval gates
- Get team review of generated plan

## Contributing

To suggest improvements or report issues, check the CHANGELOG.md for version history and known limitations.

---

**Plugin Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-10
**Marketplace**: Available in Claude Code marketplace

For detailed technical documentation, see individual agent and command files in the plugin directory.
