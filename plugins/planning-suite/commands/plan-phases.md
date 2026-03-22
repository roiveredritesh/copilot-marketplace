---
description: "Create a phase-by-phase implementation plan with approval gates"
argument-hint: "<description> [--async]"
allowed-tools: [Task, Read, Write, Grep, Glob, Bash, AskUserQuestion]
---

# Command: /plan-phases

Creates a phase-by-phase implementation plan with approval gates between phases. This allows you to plan incrementally, get approval for each phase before moving to the next, and adjust approach based on feedback.

## Usage

```bash
/plan-phases <description> [--async]
```

## Arguments

### Required Arguments

- `description`: What you want to plan in phases
  - Examples: "Implement user authentication system"
  - "Build reporting dashboard"
  - "Migrate to new database schema"
  - "Refactor payment processing"

### Optional Flags

- `--async`: Execute in background. Default is synchronous (interactive)

## How It Works

1. **Initial Assessment**: Understand the scope and complexity
2. **Phase Decomposition**: Break into independent phases
3. **Phase Planning** (repeating for each phase):
   - Design phase scope
   - Plan implementation
   - Ask for approval
   - Refine based on feedback
4. **Dependency Resolution**: Ensure correct phase ordering
5. **Generate Documentation**: Create phase-by-phase plan

## Examples

### Interactive Phase Planning (Recommended)

```bash
# Plan a complex feature in phases
/plan-phases "Implement user authentication system"

# Plan a refactoring with approvals
/plan-phases "Migrate to async/await throughout codebase"

# Plan a multi-component feature
/plan-phases "Build complete admin dashboard with multiple sections"
```

### Background Planning

```bash
# Plan in background, get results later
/plan-phases "Redesign database schema with data migration" --async

# Large multi-phase project in background
/plan-phases "Build REST API for mobile application" --async
```

## Interactive Process

```
You: /plan-phases "Implement user registration and login"

↓

Agent analyzes scope and creates Phase 1

↓

Agent: "I've planned Phase 1: Create database schema and user model.
         Files: User.cs (create), UserRepository.cs (create)
         Estimated effort: 4 hours
         Approve Phase 1?"

You select: [Approve] [Request Changes] [Cancel]

↓ (if Approve)

Agent plans Phase 2 and asks for approval again

↓

Process repeats until all phases planned
```

## Output Documents

### Main Plan Documents
- `<plan-name>-phases.md` - Complete phase overview with all details
- `<plan-name>-phase-1.md` - First phase detailed plan
- `<plan-name>-phase-2.md` - Second phase detailed plan
- `<plan-name>-phase-N.md` - Additional phases
- `<plan-name>-dependencies.md` - Inter-phase dependencies

### Content of Phase-Phases Overview

```markdown
# Implementation Plan: [Project Name]

## Phase Breakdown

### Phase 1: [Name] (4 hours)
**Objective**: [What this phase accomplishes]
- File 1: Create/Modify/Delete
- File 2: Create/Modify/Delete
**Depends on**: None
**Unblocks**: Phase 2
**Approval Status**: Pending/Approved/Requested Changes

### Phase 2: [Name] (6 hours)
**Objective**: [What this phase accomplishes]
- File 3: Create/Modify/Delete
**Depends on**: Phase 1
**Unblocks**: Phase 3
**Approval Status**: Pending/Approved

### Phase 3: [Name] (3 hours)
[Similar structure]

## Timeline
Total: 13 hours (estimated 2-3 days with testing)
Dependencies allow some parallel work: Phase 2 and Phase 2b can run in parallel

## Approval Checklist
- [ ] Phase 1 Approved
- [ ] Phase 2 Approved
- [ ] Phase 3 Approved
- [ ] Ready to Start Implementation
```

### Content of Phase-Specific Plans

Each phase plan includes:
- **Objective**: What phase accomplishes
- **Files to Change**:
  - Files to create with purpose
  - Files to modify with changes
  - Files to delete if any
- **Implementation Steps**: Detailed step-by-step
- **Code Examples**: Key code snippets
- **Testing**: What to test in this phase
- **Effort Estimate**: Hours for this phase
- **Dependencies**: What must be done before
- **Risks**: Phase-specific risks
- **Validation Checklist**: How to verify phase completion

## Phase Design Patterns

### Sequential Phases (Most Common)
```
Phase 1: Database Schema
    ↓
Phase 2: Repository Layer
    ↓
Phase 3: Service Layer
    ↓
Phase 4: API Endpoints
    ↓
Phase 5: Testing & Validation
```

### Parallel Phases (Where Possible)
```
Phase 1: Database Schema
    ├─→ Phase 2a: Repository Layer
    │   └─→ Phase 4: Service Layer
    │
    └─→ Phase 2b: UI Components
        └─→ Phase 4: Integration
```

### Phased Enhancement Pattern
```
Phase 1: MVP - Basic functionality
    ↓
Phase 2: Validation - Input validation and error handling
    ↓
Phase 3: Performance - Optimization and caching
    ↓
Phase 4: Features - Additional features and polish
```

## Approval Gates

### What Triggers Approval Request

After planning each phase, you're asked to:

```
Approve this phase plan?
[✓ Approve and continue]
[✗ Request changes]
[◆ Cancel planning]
```

### If You Request Changes

Agent will ask:
- What needs to change
- What's missing
- Different approach preference

Then replans the phase with feedback.

### If You Approve

Agent moves to planning next phase.

## Benefits of Phase-Based Planning

✅ **Iterative Refinement** - Adjust approach as you learn more
✅ **Team Alignment** - Get approval before implementation
✅ **Risk Reduction** - Identify issues early per phase
✅ **Flexibility** - Change course if circumstances change
✅ **Clear Checkpoints** - Know when to validate each phase
✅ **Effort Tracking** - Monitor progress per phase
✅ **Parallel Work** - Identify what can be done in parallel

## Comparison with Other Commands

| Aspect | `/plan` | `/plan-feature` | `/plan-refactor` | `/plan-phases` |
|--------|---------|-----------------|------------------|---|
| Planning Style | Automatic | Comprehensive | Detailed | Interactive |
| User Input | Optional (flags) | Minimal | Minimal | Required (approval) |
| Best For | Quick plans | Complex features | Refactoring | Large projects |
| Depth | Shallow/Medium/Deep | Medium/Deep | Medium/Deep | Full detail |
| Approval | None | None | None | Per phase |
| Modification | No | No | No | Yes (with changes) |

## When to Use

- **For complex projects** with multiple components
- **For team coordination** - need alignment before each phase
- **For large refactoring** - want to break into manageable parts
- **For uncertain scope** - may adjust approach as you learn
- **For high-risk work** - want approval gates
- **To track progress** - phase completion checkpoints

## Workflow Recommendations

### Recommended Workflow

```
1. Run /plan-phases for initial planning
2. Review Phase 1 plan
3. Approve Phase 1
4. Implement Phase 1
5. Validate Phase 1 (run tests)
6. Review Phase 2 plan (informed by Phase 1 results)
7. Repeat for each phase
```

### Tips

1. **Don't skip phases** - Take time to review and approve
2. **Adjust as needed** - If circumstances change, replan subsequent phases
3. **Validate between phases** - Test before moving to next phase
4. **Document changes** - Note any deviations from plan
5. **Keep phase sizes reasonable** - 3-8 hours each phase is good

## Integration with Other Plugins

If available:
- **analysis-toolkit**: Use before phase planning for context
- **architecture-advisor**: Get pattern recommendations per phase
- **development-suite**: Reference code generators per phase

## See Also

- `/plan` - For quick single-plan approach
- `/plan-feature` - For feature planning
- `/plan-refactor` - For refactoring planning

---

**Command Type**: Incremental Planning
**Default Mode**: Interactive (Synchronous with approvals)
**Depth**: Automatic (full detail for each phase)
**Best For**: Complex projects, team coordination, incremental delivery
**Output Location**: marketplace/output/planning/incremental/
**Key Feature**: Approval gates between phases
