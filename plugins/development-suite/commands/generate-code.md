# Command: /generate-code

Generates production-ready code snippets, modules, and components from requirements and specifications.

**Task Coverage**: Task #2 (Generate code snippets or modules from requirements)

## Usage

```
/generate-code <requirement-spec> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **requirement-spec**: Description of code to generate
  - Feature specification or requirements
  - Component type (entity, repository, service, controller, tests)
  - Example: `/generate-code "Create User entity with validation, repository, and service"`
  - Example: `/generate-code "Generate payment processing service with error handling"`
  - Can reference file: `/generate-code requirements.md`

### Optional Flags

- **--async**: Execute in background
- **--wait**: Execute synchronously (default)
- **--report=full|summary**: Report detail level (full by default)

## Examples

```bash
# Generate code with wait (default)
/generate-code "User service with async methods and error handling" --wait

# Background code generation
/generate-code "Product repository with LINQ queries" --async

# Quick summary
/generate-code "Shopping cart controller" --report=summary

# Generate from specification file
/generate-code spec.md --wait

# Generate specific component type
/generate-code "Generate unit tests for UserService" --wait
```

## Implementation

### Step 1: Parse Arguments
- Extract requirement specification text or file path
- Read file if path provided
- Validate file exists and is readable
- Set execution mode (async/wait)
- Set report level (full/summary)
- Identify component type from description

**Process**:
1. If argument starts with `{path}/`, treat as file path
2. Validate file exists
3. Read file contents
4. Use file contents as specification
5. Extract component type from specification
6. Validate specification is meaningful (not empty)

**Outputs**: Execution mode, report level, component type, specification text

### Step 2: Analyze Requirements

- Parse requirement text for component details:
  - Component type (entity, repository, service, controller, tests, all)
  - Key responsibilities and methods
  - Properties and data structure
  - Integration points and dependencies
  - Performance or security requirements
  - Technology stack (default: C# .NET Framework 4.8)

**Process**:
1. Extract component type from description
2. Identify methods/features needed
3. Recognize integration requirements
4. Note any constraints or non-functional requirements
5. Determine if generating single component or complete set

**Outputs**: Component type, feature list, dependencies, constraints

### Step 3: Queue/Execute Task

**For Async Mode**:
1. Create new task ID with pattern: `task-YYYYMMDD-HHMMSS-gen-{random}`
2. Create status file: `.claude/task-status/{task-id}.md`
3. Queue task to background coordinator with:
   - Task type: `code-generation`
   - Specification: full requirement text
   - Component type: identified component
   - Report level: full or summary
4. Return immediate response with task ID
5. File structure for task coordination

**For Sync Mode**:
1. Delegate to code-generator agent
2. Wait for completion
3. Return final report

**Async Response**:
```
Task ID: task-20251030-145300-gen-abc123
Status: Queued
Estimated time: 10-15 minutes

Monitor progress with: /task-status task-20251030-145300-gen-abc123
```

### Step 4: Delegate to Agent

**For sync mode**, invoke the code-generator agent with:
- Input: Full specification text
- Context: Project conventions (C# .NET 4.8, Repository/Service patterns)
- Expected output: Complete code with tests and documentation
- Report level: Full or summary as specified

**Agent Tasks**:
1. Parse requirements and component type
2. Analyze architectural patterns
3. Generate code with SOLID principles
4. Create unit tests
5. Document with XML comments
6. Generate integration guide
7. Create comprehensive report

### Step 5: Return Response

**Sync Mode Response**:
```
# Code Generation: User Service

[Generated code components]

Report: marketplace/output/reviews/user-service-code-generation.md

Integration Guide: marketplace/output/reviews/user-service-integration-guide.md
```

**Response includes**:
- What was generated
- Generated code snippets (for copy-paste)
- Integration step-by-step instructions
- Files to create/modify
- Configuration needed
- Testing instructions
- Where full report is saved

## Output Locations

- Full report: `marketplace/output/reviews/<component>-code-generation.md`
- Integration guide: `marketplace/output/reviews/<component>-integration-guide.md`
- Summary: `marketplace/output/reviews/<component>-summary.md`
- Task status: `.claude/task-status/<task-id>.md`

## Typical Generation Time

- Simple entity/model: 3-5 minutes
- Repository + Service: 8-12 minutes
- Complete set with tests: 15-20 minutes

**Recommendation**: Use `--async` for complex components.

## What Can Be Generated

### Entity Models
- Entity class with properties
- Validation attributes
- Relationships and navigation properties
- ToString and equality overrides
- XML documentation

### Repository
- Interface definition
- Implementation with LINQ queries
- Read methods (GetById, GetAll, Query)
- Write methods (Add, Update, Delete)
- Async variants
- Exception handling
- Proper disposal

### Service Layer
- Interface definition
- Implementation with business logic
- Dependency injection
- Input validation
- Transaction handling
- Error handling with logging
- Async/await patterns

### API Endpoint/Page Handler
- HTTP methods (GET, POST, PUT, DELETE)
- Parameter binding
- Request/response models
- Error responses
- Authorization attributes
- Input validation
- Dependency injection wiring

### Unit Tests
- Test fixtures and setup
- Happy path tests
- Edge case tests
- Error scenario tests
- Mock dependencies
- Assert validations
- Coverage for each component

### Complete Modules
- All of above together
- Full integration example
- Configuration guide
- Deployment considerations

## Code Quality Standards

Generated code includes:
- ✓ Consistent naming conventions
- ✓ Proper indentation and formatting
- ✓ XML doc comments on all public members
- ✓ SOLID principles application
- ✓ No magic numbers (uses constants)
- ✓ Async/await where appropriate
- ✓ Specific exception handling
- ✓ Input validation and guards
- ✓ Unit tests with good coverage
- ✓ Security best practices

## Integration Requirements

Generated code requires:
- Project uses Dependency Injection
- Service container registration (Unity/Autofac)
- DbContext or data context configured
- NUnit or MSTest for testing
- Moq for mocking dependencies

## FAQ

**Q: Will the code work immediately?**
A: Yes, it's production-ready code that follows your project conventions.

**Q: Do I have to use all of it?**
A: Use what you need. Pick individual components or use the complete set.

**Q: Can I modify the generated code?**
A: Yes, treat it as a starting point. Code is fully documented.

**Q: Are tests included?**
A: Yes, unit tests are generated following NUnit and Moq conventions.

**Q: What about async database calls?**
A: All database operations use async/await patterns.

**Q: How detailed should my specification be?**
A: Brief description works: "Create user service with validation"

**Q: Can it generate for other technologies?**
A: Primary stack is C# .NET Framework 4.8, but can generate for JavaScript, Python, Java if specified.

**Q: Where is the generated code saved?**
A: Full code is in marketplace/output/reviews/ with copy-paste instructions.

**Q: What's the difference between full and summary reports?**
A: Full includes all code, explanations, and detailed integration guide. Summary is condensed version.

**Q: Can I generate multiple components at once?**
A: Yes, describe all needed components in specification.

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Delegated To**: code-generator agent
**Task Coverage**: Task #2
