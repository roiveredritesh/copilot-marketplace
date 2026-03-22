---
description: "Create a detailed execution plan with automatic type detection and analysis integration"
argument-hint: "<description> [--detailed] [--async]"
allowed-tools: [Task, Read, Write, Grep, Glob, Bash]
---

# Command: /plan

Creates a detailed, actionable execution plan for any task. Automatically detects the type of planning needed (task, feature, or refactoring) and intelligently integrates with existing Jira analysis if available.

## Usage

```bash
/plan <description> [--detailed] [--async]
```

## Arguments

### Required Arguments

- `description`: What you want to plan. Can be:
  - A task description: "Fix login validation bug"
  - A ticket number: "PROJ-456"
  - A combination: "Implement fix for PROJ-456 based on analysis"
  - A feature description: "Add user export functionality"
  - A refactoring scope: "Extract payment service into separate module"

### Optional Flags

- `--detailed`: Generate deep analysis (10-15+ minutes) with all details, edge cases, and comprehensive testing strategy. Default is medium (5-10 minutes)
- `--async`: Execute in background and return task ID. Default is synchronous (--wait)

## How It Works

1. **Parse Input**: Analyzes your description to understand what you need planned
2. **Auto-Detect Type**: Determines if this is a task, feature, or refactoring
3. **Find Analysis**:
   - If you mention a ticket (PROJ-123), automatically finds existing analysis
   - If analysis exists, incorporates findings into the plan
4. **Generate Plan**: Creates comprehensive execution plan with:
   - File-level changes (create, modify, delete)
   - Code-level implementation details
   - Dependency analysis
   - Execution order with dependencies
   - Testing strategy
   - Risk assessment
5. **Save Output**: Saves plan to `marketplace/output/planning/`

## Examples

### Simple Task Planning

```bash
# Quick plan for a bug fix
/plan "Fix authentication timeout issue"

# Plan based on existing Jira analysis
/plan "PROJ-456"

# Plan with existing analysis reference
/plan "Implement fix from PROJ-456 analysis"
```

### Feature Planning

```bash
# Plan a new feature
/plan "Add user export functionality to CSV and Excel"

# Feature planning with deep analysis
/plan "Implement caching layer for API responses" --detailed
```

### Refactoring Planning

```bash
# Plan code refactoring
/plan "Refactor UserRepository to improve query performance"

# Deep refactoring plan with comprehensive risk analysis
/plan "Extract payment service into separate module" --detailed
```

### Background Execution

```bash
# Generate plan in background
/plan "Add two-factor authentication support" --async

# Deep plan in background
/plan "Major database schema redesign" --detailed --async
```

## Output

The command generates multiple detailed documents:

### Files Generated (Default - Medium Depth)
- `<name>-plan.md` - Complete execution plan
- `<name>-files.md` - File-level changes with code snippets
- `<name>-dependencies.md` - Dependency analysis and integration points

### Additional Files (With --detailed)
- `<name>-validation.md` - Comprehensive testing strategy
- `<name>-risks.md` - Risk assessment and mitigation
- `<name>-timeline.md` - Detailed effort estimation

### Files Saved To
```
marketplace/output/planning/tasks/    (for task plans)
marketplace/output/planning/features/ (for feature plans)
marketplace/output/planning/refactoring/ (for refactoring plans)
```

## Plan Content Includes

### Executive Summary
Overview of what the plan accomplishes

### Scope & Objectives
What's in scope, what's out, and success criteria

### Architecture & Design
Design decisions, patterns used, and alternatives considered

### File-Level Changes
Exact files to create, modify, or delete with descriptions

### Code-Level Details
Actual code snippets, method signatures, and patterns to use

### Dependency Analysis
Component dependencies, integration points, and potential conflicts

### Implementation Plan
Step-by-step execution with code examples

### Testing Strategy
Unit tests, integration tests, and validation approach

### Risk Assessment
Potential risks, likelihood, impact, and mitigation

### Rollback Strategy
How to revert if needed

### Timeline
Effort estimates for each phase/step

## Integration with Existing Analysis

If you reference a Jira ticket and analysis exists:

```
/plan "PROJ-456"

↓

Planner finds: marketplace/output/analysis/PROJ-456-root-cause-analysis.md

↓

Plan incorporates:
- Root cause findings
- Affected files from analysis
- Recommended solutions
- Dependencies discovered

↓

Output plan references the analysis
```

## Depth Levels

### Default (Medium - No Flag)
**Time: 5-10 minutes**
- Thorough analysis
- Detailed implementation steps
- Code snippets with method signatures
- Standard testing plan
- Basic risk assessment

### Shallow (implicit with quick descriptions)
**Time: 3-5 minutes**
- Quick analysis
- High-level steps
- Minimal code snippets
- Essential files only

### Deep (--detailed flag)
**Time: 10-15+ minutes**
- Very comprehensive analysis
- Complete code snippets
- Before/after comparisons
- Detailed test cases
- Comprehensive risk mitigation
- Rollback procedures
- Edge case handling

## When to Use

- **Plan before implementing** to understand scope and impact
- **After analysis** to turn findings into actionable steps
- **For complex tasks** to ensure nothing is missed
- **To estimate effort** before committing to work
- **To document approach** for team collaboration

## Tips

1. **Be specific**: "Fix login timeout" is better than "Fix login"
2. **Reference analysis**: Mention ticket numbers when analysis exists
3. **Use --detailed** for complex features or refactoring
4. **Use --async** for large plans so you can continue working
5. **Review the generated files** before starting implementation

## See Also

- `/plan-feature` - Detailed feature planning command
- `/plan-refactor` - Refactoring-specific planning
- `/plan-phases` - Phase-by-phase planning with approvals
- `/analyze-jira-issue` - Run analysis first if needed

---

**Command Type**: Planning & Analysis
**Default Mode**: Synchronous (use --async for background)
**Default Depth**: Medium (use --detailed for comprehensive analysis)
**Output Location**: marketplace/output/planning/
