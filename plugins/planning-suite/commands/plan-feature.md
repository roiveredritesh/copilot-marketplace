---
description: "Create a comprehensive feature development plan with all implementation details"
argument-hint: "<feature-description> [--detailed] [--async]"
allowed-tools: [Task, Read, Write, Grep, Glob, Bash]
---

# Command: /plan-feature

Creates a comprehensive feature development plan with architecture design, component breakdown, code-level implementation guidance, and complete integration strategy.

## Usage

```bash
/plan-feature <feature-description> [--detailed] [--async]
```

## Arguments

### Required Arguments

- `feature-description`: Description of the feature to plan
  - Examples: "Add user export to CSV and Excel"
  - "Implement real-time notifications"
  - "Build admin dashboard with analytics"

### Optional Flags

- `--detailed`: Generate comprehensive analysis with all edge cases and detailed testing (10-15+ minutes). Default is medium depth
- `--async`: Execute in background. Default is synchronous

## How It Works

1. **Feature Comprehension**: Understand requirements and scope
2. **Architecture Design**: Plan system components and patterns
3. **Component Breakdown**: List all files to create/modify with details
4. **Dependency Analysis**: Map dependencies and integration order
5. **Implementation Planning**: Create phased implementation plan
6. **Code-Level Design**: Provide method signatures and key code snippets
7. **Testing Strategy**: Plan unit tests, integration tests, regression tests
8. **Generate Documentation**: Create comprehensive feature plan

## Examples

### Basic Feature Planning

```bash
# Plan a new feature
/plan-feature "Add user export functionality"

# Feature from Jira ticket
/plan-feature "PROJ-789 - Implement real-time notifications"
```

### Detailed Planning

```bash
# Comprehensive feature analysis
/plan-feature "Build admin dashboard with analytics and reporting" --detailed

# Background comprehensive planning
/plan-feature "Implement multi-tenant support across all APIs" --detailed --async
```

## Output Documents

### Main Plan Documents
- `<feature-name>-overview.md` - Feature architecture and approach
- `<feature-name>-components.md` - Component breakdown with code snippets
- `<feature-name>-implementation-plan.md` - Phased execution plan
- `<feature-name>-dependencies.md` - Dependency graph and integration order
- `<feature-name>-testing.md` - Test planning and validation

### Additional Detail Documents (--detailed only)
- `<feature-name>-risks.md` - Risk assessment and mitigation
- `<feature-name>-timeline.md` - Detailed effort breakdown
- `<feature-name>-deployment.md` - Deployment strategy

## Plan Includes

### Feature Overview
- Feature scope and objectives
- Success criteria
- Out-of-scope items

### Architecture Design
- System architecture diagram (text-based)
- Design patterns to use
- Technology decisions
- Why alternatives were not chosen

### Component Breakdown
For each component:
- File to create/modify
- Purpose and responsibility
- Dependencies
- Estimated lines of code
- Key methods/properties

### Implementation Plan

#### Phase 1: Foundation
- Create core entities and models
- Setup database/schema
- Create base repository and service

#### Phase 2: Core Functionality
- Implement main business logic
- Create API endpoints or UI
- Setup data access patterns

#### Phase 3: Integration
- Integrate with existing systems
- Setup dependency injection
- Configure cross-cutting concerns

#### Phase 4: Enhancement
- Add validation and error handling
- Implement caching if needed
- Add logging and monitoring

#### Phase 5: Testing & Deployment
- Create unit tests
- Create integration tests
- Deploy and validate

### Code-Level Details
Actual code snippets for:
- Key class structures
- Important method signatures
- Core algorithm implementations
- Integration points
- Configuration examples

### Dependency Analysis
- Component dependency graph
- File creation/modification order
- Integration sequence
- External service integration points

### Testing Strategy

#### Unit Tests
- Test data models
- Test business logic in services
- Test repository methods
- Example test cases with code

#### Integration Tests
- Test feature end-to-end
- Test API endpoints or UI workflows
- Test database interactions
- Test external service calls

#### Regression Tests
- Areas to verify for breaking changes
- Existing functionality to validate

### Timeline & Effort
- Effort per phase (hours)
- Total project effort
- Recommended schedule
- Dependency-based sequencing

## Depth Levels

### Default (Medium)
- Thorough architecture design
- Component details with code signatures
- Phased implementation steps
- Standard testing plan
- Key code snippets

### Deep (--detailed)
- Very detailed architecture
- Complete code snippets for all components
- Comprehensive testing strategy
- Risk assessment and mitigation
- Performance considerations
- Scalability planning
- Deployment strategy
- Monitoring and observability

## Integration with Other Plugins

If available:
- **architecture-advisor**: Pattern recommendations
- **development-suite**: Code generation references
- **analysis-toolkit**: Impact analysis if related features exist

## When to Use

- Before implementing a new feature
- To estimate effort and timeline
- To communicate approach to team
- To ensure architecture alignment
- To plan testing strategy

## Tips

1. **Start with /plan-feature** for new features (not generic `/plan`)
2. **Use --detailed** for complex or critical features
3. **Reference related analysis** if available
4. **Review components** before implementation begins
5. **Share with team** for alignment and feedback

## See Also

- `/plan` - For general task planning
- `/plan-refactor` - For refactoring work
- `/plan-phases` - For phase-by-phase with approvals

---

**Command Type**: Feature Planning
**Default Mode**: Synchronous
**Default Depth**: Medium
**Best For**: New feature implementations, significant enhancements
**Output Location**: marketplace/output/planning/features/
