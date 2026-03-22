# Command: /refactor-code

Analyzes code for refactoring opportunities, provides before-and-after examples, and guides incremental code improvements.

**Task Coverage**: Task #12 (Code improvement and refactoring)

## Usage

```
/refactor-code <file-path> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **file-path**: Path to code file or code snippet
  - File path: `/refactor-code src/Services/UserService.cs`
  - Method reference: `/refactor-code UserService.cs:45` (line 45)
  - Class reference: `/refactor-code UserRepository.cs:GetUsers`
  - Code snippet: Paste code directly (auto-detected)

### Optional Flags

- **--async**: Execute in background (recommended for large files)
- **--wait**: Execute synchronously (default)
- **--report=full|summary**: Report detail level (full by default)

## Examples

```bash
# Analyze file with wait
/refactor-code src/Services/UserService.cs --wait

# Background analysis for large file
/refactor-code src/Data/UserRepository.cs --async

# Quick summary of issues
/refactor-code Controllers/UserController.cs --report=summary

# Analyze specific method (line range)
/refactor-code UserService.cs:20-50 --wait

# Analyze specific method by name
/refactor-code UserService.cs:GetUserAsync --wait

# Paste code directly for analysis
/refactor-code --wait
[paste code here, Ctrl+D or Ctrl+Z to end]
```

## Implementation

### Step 1: Parse Arguments & Read Code

- Extract file path or detect code snippet input
- Validate file exists if path provided
- Read file contents
- Extract specific method/class if line range given
- Validate code is readable C#

**Process**:
1. If argument is file path (contains . or /):
   - Validate file exists
   - Check file is readable
   - Determine if specific method requested (line number or method name)
   - Read entire file or extract method
2. If argument is empty:
   - Enter interactive mode
   - Prompt for code input
   - Read until user signals end
3. If argument contains code:
   - Treat as inline code snippet
   - Parse as C# code

**Outputs**: Source code, file context, scope (full file or method)

### Step 2: Analyze Code Quality

- Scan for code smells and issues
- Measure complexity metrics
- Check SOLID principle compliance
- Identify anti-patterns
- Assess maintainability

**Process**:
1. Detect code smells:
   - Long methods (>30 lines)
   - Long classes (>200 lines)
   - Duplicate code
   - Long parameter lists
   - Deep nesting
   - Magic numbers
   - Dead code
2. Measure metrics:
   - Cyclomatic complexity
   - Method length
   - Parameter count
   - Nesting depth
3. Check patterns:
   - SOLID principle violations
   - Anti-patterns (God Object, Feature Envy)
   - Design patterns usage
4. Assess quality:
   - Naming clarity
   - Comment adequacy
   - Error handling
   - Test coverage

**Outputs**: Issues found, metrics, complexity assessment

### Step 3: Queue/Execute Task

**For Async Mode**:
1. Create task ID: `task-YYYYMMDD-HHMMSS-refactor-{random}`
2. Create status file: `.claude/task-status/{task-id}.md`
3. Queue to background coordinator with:
   - Task type: `refactoring`
   - Source code: Full code to analyze
   - File path: For context
   - Report level: Full or summary
4. Return task ID and estimated time

**For Sync Mode**:
1. Delegate to refactoring-assistant agent immediately
2. Wait for analysis completion
3. Return final report

**Async Response**:
```
Task ID: task-20251030-160000-refactor-abc
Status: Analyzing code quality
Estimated time: 10-15 minutes

Monitor progress: /task-status task-20251030-160000-refactor-abc
```

### Step 4: Delegate to Agent

**For sync mode**, invoke refactoring-assistant agent with:
- Input: Source code to analyze
- Process: 7-phase refactoring analysis
- Output: Prioritized improvements with code examples
- Report: Complete refactoring guide

**Agent Tasks**:
1. Analyze code and detect smells
2. Categorize refactoring opportunities
3. Design refactoring solutions
4. Create incremental plan
5. Provide before-and-after examples
6. Calculate quality metrics
7. Generate complete refactoring report

### Step 5: Return Response

**Sync Mode Response**:
```
# Refactoring Plan: UserService

## Issues Identified
- Long method: GetUserAsync (45 lines)
- Duplicate code: User validation appears 3 times
- Deep nesting: 4 levels in error handling
- Missing constant: Magic number 5 for retry count

## Refactoring Opportunities (by priority)
1. [Critical] Extract validation to separate method
2. [Major] Introduce retry constant
3. [Major] Simplify conditional logic

## Quality Improvements
- Reduce cyclomatic complexity: 15 → 8
- Reduce method length: 45 → 20 lines
- Improve maintainability: Current 65, Target 82

Report: marketplace/output/reviews/UserService-refactoring-plan.md
```

**Response includes**:
- Code smells identified
- Refactoring opportunities by priority
- Before/after code examples
- Quality improvements projected
- Step-by-step refactoring guide
- Estimated effort
- Risk assessment
- Where full report is saved

## Output Locations

- Full plan: `marketplace/output/reviews/<component>-refactoring-plan.md`
- Step-by-step guide: `marketplace/output/reviews/<component>-refactoring-guide.md`
- Summary: `marketplace/output/reviews/<component>-summary.md`
- Task status: `.claude/task-status/<task-id>.md`

## Typical Analysis Time

- Small method (<50 lines): 5-8 minutes
- Large method/small class: 8-12 minutes
- Large class (>200 lines): 15-20 minutes
- Multiple refactorings: 20-30 minutes

**Recommendation**: Use `--async` for large files or classes.

## Issues Analyzed

### Code Smells
- **Long Method**: Methods >30 lines with multiple responsibilities
- **Long Class**: Classes >200 lines with mixed concerns
- **Duplicate Code**: Same code in multiple places
- **Long Parameter List**: Methods with >5 parameters
- **Deep Nesting**: Code nested >3 levels deep
- **Magic Numbers**: Hard-coded values without explanation
- **Dead Code**: Unused variables, methods, or classes
- **Feature Envy**: Methods using another class's data excessively

### SOLID Violations
- **Single Responsibility**: Multiple reasons to change
- **Open/Closed**: Hard to extend without modification
- **Liskov Substitution**: Subclasses violating contract
- **Interface Segregation**: Fat interfaces with unused methods
- **Dependency Inversion**: Depends on concrete classes

### Anti-Patterns
- **God Object**: Too many responsibilities
- **Data Clumps**: Groups of data always used together
- **Switch Statement**: Repeated switches for type checking
- **Temporary Field**: Field used only in some methods
- **Middle Man**: Class just delegates to another
- **Lazy Class**: Class not earning its existence
- **Speculative Generality**: Over-engineered for unused features

## Refactoring Types

**Safe Refactorings** (low risk):
- Rename method/variable
- Extract method
- Remove dead code
- Extract constant
- Inline method

**Medium Risk Refactorings**:
- Extract class
- Move method to another class
- Replace inheritance with composition
- Introduce interface

**Complex Refactorings** (high risk):
- Modify public API
- Change inheritance hierarchy
- Introduce new design pattern
- Restructure major components

## Quality Metrics Provided

### Complexity Metrics
- **Cyclomatic Complexity**: Number of execution paths (lower is better, target <10)
- **Cognitive Complexity**: Mental burden to understand (lower is better)
- **Method Length**: Lines of code per method (target <30)
- **Nesting Depth**: How deeply nested is code (target <3)

### SOLID Scores
- Single Responsibility: Yes/No + description
- Open/Closed: Yes/No + description
- Liskov Substitution: Yes/No + description
- Interface Segregation: Yes/No + description
- Dependency Inversion: Yes/No + description

### Maintainability Index
- Scale 0-100 (higher is better)
- Below 50: Critical review needed
- 50-70: Should refactor
- 70+: Good maintainability
- Target: >75

## Refactoring Recommendations

### By Priority
1. **Critical**: Blocks testing, security risk, major performance issue
2. **Major**: SOLID violation, significant code smell, maintainability issue
3. **Medium**: Code smell, minor performance, naming clarity
4. **Minor**: Style consistency, documentation

### By Complexity
- **Simple**: 15-30 minutes (extract method, rename, remove dead code)
- **Medium**: 30-60 minutes (extract class, introduce interface)
- **Complex**: 60+ minutes (API changes, major restructuring)

### By Risk
- **Low Risk**: Single file, no public API change, localized impact
- **Medium Risk**: Multiple files, interface change, moderate impact
- **High Risk**: Public API change, widespread impact, complex interaction

## Integration with Other Tools

**Code Generation**:
- Use `/generate-code` to create replacement code
- Generate refactored version as starting point

**Code Review**:
- Use `/review-pr` to review refactored code
- Validate quality improvements

**Testing**:
- Ensure tests pass before and after refactoring
- Add tests for identified issues

**Version Control**:
- One refactoring per commit
- Easy rollback if issues discovered

## FAQ

**Q: Does refactoring change functionality?**
A: No, refactoring preserves behavior while improving code structure.

**Q: Will it break my tests?**
A: No, existing tests should pass. Refactoring doesn't change behavior.

**Q: What if I don't agree with recommendations?**
A: Each suggestion includes rationale. Use professional judgment.

**Q: Can I implement just some recommendations?**
A: Yes, handle highest priority issues first.

**Q: How do I implement the refactoring?**
A: Follow step-by-step guide in the refactoring report.

**Q: What if refactoring breaks something?**
A: Tests should catch breaks. Rollback and try different approach.

**Q: Can I refactor in phases?**
A: Yes, plan breaks refactoring into phases in the report.

**Q: Will refactoring improve performance?**
A: Primarily improves maintainability, but may enable performance improvements.

**Q: How much time will refactoring take?**
A: Estimated in report based on complexity and scope.

**Q: Can you analyze just part of a file?**
A: Yes, specify line range or method name with file path.

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Delegated To**: refactoring-assistant agent
**Task Coverage**: Task #12
