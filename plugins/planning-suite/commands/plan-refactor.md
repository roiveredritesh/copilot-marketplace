---
description: "Create a safe refactoring plan with dependency analysis and risk mitigation"
argument-hint: "<refactoring-scope> [--detailed] [--async]"
allowed-tools: [Task, Read, Write, Grep, Glob, Bash]
---

# Command: /plan-refactor

Creates a safe, comprehensive refactoring plan with complete dependency analysis, before/after code comparisons, risk assessment, and rollback strategies.

## Usage

```bash
/plan-refactor <refactoring-scope> [--detailed] [--async]
```

## Arguments

### Required Arguments

- `refactoring-scope`: Description of what to refactor
  - Examples: "Extract payment service from UserService"
  - "Optimize database queries in UserRepository"
  - "Rename IUserService methods for consistency"
  - "Refactor authentication logic"

### Optional Flags

- `--detailed`: Generate comprehensive analysis with risk assessment, edge cases, and detailed rollback plan (10-15+ minutes). Default is medium
- `--async`: Execute in background. Default is synchronous

## How It Works

1. **Scope Analysis**: Understand current code and refactoring target
2. **Dependency Mapping**: Find all callers and trace complete usage
3. **Breaking Change Detection**: Identify interface changes and impacts
4. **Refactoring Design**: Plan target state and intermediate steps
5. **Risk Assessment**: Identify risks and plan mitigation
6. **Implementation Sequencing**: Order changes to minimize breaking changes
7. **Code Comparison**: Show before/after for changed components
8. **Testing Strategy**: Plan regression and validation tests
9. **Generate Documentation**: Create refactoring plan

## Examples

### Simple Refactoring Planning

```bash
# Plan a small refactoring
/plan-refactor "Rename GetUser to GetUserAsync"

# Refactoring from Jira ticket
/plan-refactor "PERF-555 - Optimize slow queries"
```

### Complex Refactoring Planning

```bash
# Complex refactoring with detailed analysis
/plan-refactor "Extract payment service into separate module" --detailed

# Large refactoring in background
/plan-refactor "Refactor repository pattern across all data access layers" --detailed --async
```

## Output Documents

### Main Plan Documents
- `<refactoring-name>-plan.md` - Overall refactoring strategy
- `<refactoring-name>-dependencies.md` - Complete dependency analysis
- `<refactoring-name>-changes.md` - Before/after code comparisons
- `<refactoring-name>-risks.md` - Risk assessment and mitigation
- `<refactoring-name>-rollback.md` - Rollback and recovery plan

### Additional Documents (--detailed only)
- `<refactoring-name>-testing.md` - Comprehensive test strategy
- `<refactoring-name>-timeline.md` - Effort and timeline

## Plan Includes

### Refactoring Overview
- Current state analysis
- Target state description
- Why refactoring is needed
- Expected benefits

### Dependency Analysis

#### Component Dependencies
- What depends on the code being refactored
- Call graph and usage patterns
- Integration points
- Number of affected files

#### Breaking Changes
- Interface changes
- Method signature changes
- Behavior changes
- API contract changes

#### Impact Assessment
- Affected components (count and names)
- Risk level (low/medium/high)
- Mitigation strategies

### Refactoring Design

#### Approach
- Refactoring strategy (big bang vs incremental)
- Intermediate steps if phased
- Pattern to use in new code
- Why this approach

#### Target Architecture
- New code structure
- Design improvements
- Code quality improvements
- Performance improvements

### Implementation Plan

#### Before Code
```csharp
// Current implementation
public User GetUser(int id) { ... }
private void ProcessPayment(decimal amount) { ... }
```

#### After Code
```csharp
// New implementation
public async Task<User> GetUserAsync(int id) { ... }
// Payment service extracted
public class PaymentService : IPaymentService { ... }
```

#### Implementation Steps
1. Identify all call sites
2. Create new implementation
3. Update callers (ordered by dependency)
4. Remove old implementation
5. Update tests
6. Verify no regressions

### Risk Assessment

#### High Risks
- Risk 1: [description]
  - Likelihood: Low/Medium/High
  - Impact: Low/Medium/High
  - Mitigation: [strategy]

#### Medium Risks
[Similar structure]

#### Low Risks
[Similar structure]

### Rollback Strategy

#### When to Rollback
- Breaking changes cause production issues
- Tests fail after deployment
- Performance degrades unexpectedly

#### Rollback Steps
1. Revert code changes
2. Clear caches if needed
3. Restart services
4. Verify system health

#### Rollback Validation
- [ ] All services started
- [ ] No error logs
- [ ] Health checks pass
- [ ] Critical paths working

### Testing Strategy

#### Unit Tests
- Test new implementation
- Test edge cases
- Mock dependencies
- Example test code

#### Integration Tests
- Test refactored component with dependents
- Test end-to-end workflows
- Test external integrations

#### Regression Tests
- Areas to verify for breaking changes
- Existing functionality to validate
- Performance benchmarks

## Depth Levels

### Default (Medium)
- Complete dependency analysis
- Before/after code samples
- Implementation steps
- Risk assessment
- Testing strategy
- Rollback plan

### Deep (--detailed)
- Very detailed dependency tracing
- Complete code comparisons
- Comprehensive risk mitigation
- Detailed test cases with code
- Effort estimation
- Timeline with sequencing
- Performance impact analysis
- Monitoring strategy

## Refactoring Types Supported

- **Rename**: Renaming methods, classes, or properties
- **Extract**: Extract methods, classes, or services
- **Inline**: Inline methods or small utilities
- **Move**: Move code between files or classes
- **Replace**: Replace algorithm or implementation
- **Optimize**: Optimize performance-critical code
- **Redesign**: Major architectural changes

## Integration with Other Plugins

If available:
- **analysis-toolkit**: Performance analysis if performance refactoring
- **architecture-advisor**: Architecture validation
- **development-suite**: Code generation for new patterns

## When to Use

- Before starting significant refactoring
- To plan breaking changes safely
- To estimate refactoring effort
- To communicate approach to team
- To ensure no production issues
- To plan testing and validation

## Tips

1. **Analyze dependencies first** - understand full impact
2. **Use --detailed** for breaking changes or large refactoring
3. **Plan testing thoroughly** - regressions are main risk
4. **Order changes carefully** - minimize simultaneous breaking changes
5. **Have rollback ready** - before deploying to production

## See Also

- `/plan` - For general task planning
- `/plan-feature` - For feature implementation
- `/plan-phases` - For phase-by-phase planning

---

**Command Type**: Refactoring Planning
**Default Mode**: Synchronous
**Default Depth**: Medium
**Best For**: Code refactoring, architectural changes, optimization
**Output Location**: marketplace/output/planning/refactoring/
**Risk Level**: High - comprehensive planning recommended
