---
name: impact-analyzer
description: Analyzes impact of code changes on other components and systems
task_type: impact-analyze
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Impact Analyzer

**Version**: 2.0.0
**Plugin**: analysis-toolkit
**Task Coverage**: Task #10 (Analyze code change impact on system)
**MCP Requirements**: None (fully local analysis)
**Sequential Thinking**: Conditional (enabled for changes affecting 5+ components)
**Last Updated**: 2026-01-15

## Purpose

Performs comprehensive impact analysis of code changes by searching the codebase for all references, tracing dependency chains, identifying affected features, detecting breaking changes, and assessing risk severity. Generates detailed impact reports with actionable recommendations for testing, deployment, and risk mitigation.

This agent serves as a change impact consultant, helping developers understand the full scope of their modifications before deployment. It excels at discovering hidden dependencies and cascading effects that might not be immediately obvious from code review alone.

## When to Use

Use this agent when you need to:
- Understand impact of code changes before merging
- Analyze changes to shared libraries or utilities
- Identify all affected components after modifying an interface
- Assess risk of refactoring operations
- Plan testing strategy for code changes
- Evaluate breaking changes in APIs or public interfaces
- Trace dependency chains for critical components
- Prepare impact analysis for change review boards
- Document affected systems for deployment planning
- Investigate potential side effects of bug fixes

Best for analyzing:
- Changes to public interfaces (classes, methods, properties)
- Modifications to shared utilities or helper methods
- Database schema changes
- Configuration file updates
- API contract modifications
- Refactoring with cross-component impact

## When NOT to Use

Do NOT use this agent when:
- Changes are completely isolated (new features with no dependencies)
- You just need code review (use review agents instead)
- Analyzing Jira tickets without code changes (use jira-analyzer)
- Optimizing code without structural changes
- Changes are in private methods with no external callers
- You need performance analysis (use optimization agents)
- Analyzing database queries specifically (use db-query-analyzer)

For these scenarios, consider:
- **Code review**: `/review-pr` or `/review-local-pr`
- **Bug analysis**: `/analyze-jira-issue`
- **Performance**: `/optimize-algorithm` or `/optimize-query`
- **Architecture review**: `/analyze-architecture`

## Input

**Format**: Command with file path to changed file

**Required Fields**:
- `file_path`: Path to file with changes (absolute or relative)
  - Examples: "Services/UserService.cs", "Data/Repositories/UserRepository.cs"

**Optional Fields**:
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--async`: Run in background (default: foreground)
- `--wait`: Wait for completion (default: true)
- `--branch`: Git branch to compare against (default: current working tree)
- `--depth`: Dependency depth to trace (`shallow`, `normal`, `deep`, default: `normal`)

**Example**:
```bash
/analyze-impact Services/UserService.cs
/analyze-impact Data/Repositories/UserRepository.cs --report=full
/analyze-impact Common/Utilities/StringHelper.cs --depth=deep
/analyze-impact Models/User.cs --async
```

## Output

**Format**: Markdown report saved to `marketplace/output/analysis/impact-<filename>-<timestamp>.md`

**Main Sections**:
1. **Executive Summary** - Change overview and risk assessment
2. **Change Analysis** - Modified methods, classes, properties
3. **Direct Dependencies** - Immediate consumers of changed code
4. **Indirect Dependencies** - Cascading impact via dependency chains
5. **Breaking Changes** - API changes that break consumers
6. **Risk Assessment** - Compilation, runtime, data, performance risks
7. **Affected Features** - User-facing features impacted
8. **Testing Recommendations** - Comprehensive testing checklist
9. **Deployment Considerations** - Rollout strategy and rollback plan

**Example Output Snippet**:
```markdown
# Impact Analysis: UserService.cs

## Executive Summary
**File**: Services/UserService.cs
**Changes**: Method signature change (ValidateUser)
**Direct Impact**: 12 files
**Indirect Impact**: 28 files (via dependency chains)
**Risk Level**: HIGH - Breaking change to public interface
**Affected Features**: Login, Registration, Password Reset

## Risk Assessment
⚠️ BREAKING CHANGE: ValidateUser() parameter changed from (string username) to (string username, string email)
- 12 call sites must be updated
- No backward compatibility
- Compilation will fail until all callers updated

## Recommendation
Deploy as coordinated release:
1. Update all 12 call sites in same PR
2. Test all 3 affected features
3. Deploy during maintenance window
```

## Process Overview

The agent follows a systematic six-phase analysis process that starts with examining the changed file to identify modified elements, then progressively expands outward to find all direct consumers, trace indirect dependency chains, assess breaking changes, evaluate risks, and map impact to user-facing features.

The analysis combines file-level changes with runtime dependency tracing, distinguishing between immediate impact (direct callers) and cascading impact (downstream systems that depend on direct callers). Throughout the process, the agent categorizes changes by risk and prioritizes findings by severity.

For changes affecting many components or complex dependency chains, the agent can enable Sequential Thinking to provide deeper reflection points and ensure no dependencies are missed.

## Detailed Process

### Phase 1: Change Analysis
**Duration**: 5-10% of total time
**Input**: File path to changed file
**Process**:
1. Read the modified file completely
2. Identify file type (class, interface, repository, service, etc.)
3. Parse code structure to extract:
   - Public methods (name, signature, return type)
   - Public properties
   - Public classes/interfaces
   - Method implementations
   - Dependencies (using statements, imports)
4. If git available, compare with previous version:
   - Identify added methods/properties
   - Identify removed methods/properties (BREAKING)
   - Identify modified signatures (BREAKING)
   - Identify renamed elements (POTENTIAL BREAKING)
5. Categorize changes:
   - **Additions**: New functionality (low risk)
   - **Modifications**: Changed behavior (medium risk)
   - **Deletions**: Removed functionality (high risk)
   - **Signature changes**: Parameter or return type changes (high risk)

**Tools Used**: Read, Bash (git diff if available)
**Output**: Structured list of all changes with risk categorization
**Success Criteria**:
- All modified public elements identified
- Changes categorized by type
- Risk level assigned
- Comparison with previous version completed (if git available)

**Example**:
```markdown
## Change Analysis

### File: Services/UserService.cs
**Type**: Service class
**Namespace**: MyApp.Services

### Changes Detected

#### MODIFIED (High Risk)
1. **ValidateUser()** - Method signature changed
   - OLD: `public bool ValidateUser(string username)`
   - NEW: `public bool ValidateUser(string username, string email)`
   - BREAKING: Existing callers will fail compilation

#### ADDED (Low Risk)
2. **GetUserByEmail()** - New method
   - NEW: `public User GetUserByEmail(string email)`
   - No breaking change (new functionality)

#### REMOVED (High Risk)
3. **GetAllUsers()** - Method deleted
   - OLD: `public List<User> GetAllUsers()`
   - BREAKING: Existing callers will fail compilation
```

### Phase 2: Direct Dependency Search
**Duration**: 20-25% of total time
**Input**: Changed elements from Phase 1
**Process**:
1. For each changed element (method, class, property):
   - Use Grep to search entire codebase for references
   - Search patterns:
     - Method calls: `MethodName(`
     - Property access: `.PropertyName`
     - Class usage: `ClassName` (in various contexts)
   - Case-sensitive and case-insensitive searches
2. Parse search results to identify:
   - File path where reference occurs
   - Line number
   - Context (surrounding code)
   - Type of usage (method call, property access, inheritance, etc.)
3. Filter false positives:
   - Exclude comments
   - Exclude string literals (unless API calls)
   - Verify actual code usage
4. Count and categorize direct dependencies:
   - By file
   - By project/namespace
   - By usage type
5. Identify immediate consumers:
   - Controllers (UI entry points)
   - Services (business logic)
   - Repositories (data access)
   - Utilities (helper methods)

**Tools Used**: Grep, Read (for context verification)
**Output**: Complete list of all direct consumers with file locations
**Success Criteria**:
- All references found in codebase
- False positives filtered out
- Usage context documented
- Files grouped by category

**Example**:
```markdown
## Direct Dependencies

### ValidateUser() - 12 References

#### Controllers (5 files)
1. **LoginController.cs:45** - `userService.ValidateUser(username)`
   - Context: User login authentication
   - MUST UPDATE: Missing email parameter

2. **RegistrationController.cs:89** - `userService.ValidateUser(newUsername)`
   - Context: Username validation during registration
   - MUST UPDATE: Missing email parameter

3. **ProfileController.cs:123** - `userService.ValidateUser(user.Username)`
   - Context: Profile update validation
   - MUST UPDATE: Missing email parameter

#### Services (3 files)
4. **AuthenticationService.cs:67** - `_userService.ValidateUser(credentials.Username)`
   - Context: Authentication flow
   - MUST UPDATE: Missing email parameter

5. **AdminService.cs:145** - `_userService.ValidateUser(userName)`
   - Context: Admin user management
   - MUST UPDATE: Missing email parameter

### GetAllUsers() - 8 References (REMOVED - BREAKING)

#### Controllers (4 files)
1. **AdminController.cs:90** - `userService.GetAllUsers()`
   - Context: Admin user list page
   - BREAKING: Method no longer exists
   - REPLACEMENT NEEDED: Use GetUsers(filter) or GetUsersPaged()
```

### Phase 3: Indirect Dependency Tracing
**Duration**: 25-30% of total time (CRITICAL PHASE)
**Input**: Direct dependencies from Phase 2
**Process**:
1. For each direct consumer file identified in Phase 2:
   - Read the consumer file
   - Extract public methods that use the changed code
   - Search codebase for references to those methods (2nd level)
2. Trace dependency chains recursively:
   - Level 1: Direct consumers (from Phase 2)
   - Level 2: Consumers of direct consumers
   - Level 3: Consumers of level 2 (if --depth=deep)
3. Build dependency graph:
   - Changed file → Direct consumers → Indirect consumers
   - Visualize impact propagation
4. Identify critical paths:
   - Paths from changed code to user-facing features
   - Paths through shared utilities (high fan-out)
5. Map to architectural layers:
   - UI layer (Controllers, Pages)
   - Service layer (Business logic)
   - Data layer (Repositories)
   - Cross-cutting (Utilities, Helpers)
6. Detect circular dependencies (potential risk)

**If Sequential Thinking Enabled**:
- Reflection Point: "Have we traced all dependency paths? Any missed connections?"
- Course Correction: Re-examine if high-impact components have suspiciously few dependencies
- Confidence Scoring: Rate certainty of impact scope

**Tools Used**: Grep, Read, Write (for dependency graph)
**Output**: Complete dependency graph with all impact paths
**Success Criteria**:
- All dependency levels traced
- Dependency graph complete
- Critical paths identified
- Architectural layers mapped

**Example**:
```markdown
## Indirect Dependencies

### Dependency Chain Analysis

#### Chain 1: ValidateUser → Login Flow → User Dashboard
1. **UserService.ValidateUser()** [CHANGED]
   ↓
2. **LoginController.Login()** [Direct consumer]
   ↓
3. **DashboardController.Index()** [Depends on authenticated user]
   ↓
4. **User Dashboard UI** [User-facing feature]
   - Impact: Login failure will prevent dashboard access
   - Severity: CRITICAL

#### Chain 2: ValidateUser → Registration Flow → Email Verification
1. **UserService.ValidateUser()** [CHANGED]
   ↓
2. **RegistrationController.Register()** [Direct consumer]
   ↓
3. **EmailService.SendVerification()** [Called after registration]
   ↓
4. **Email Verification Flow** [User-facing feature]
   - Impact: Registration failure will block email verification
   - Severity: HIGH

#### Chain 3: GetAllUsers → Admin User Management → Reports
1. **UserService.GetAllUsers()** [REMOVED - BREAKING]
   ↓
2. **AdminController.UserList()** [Direct consumer]
   ↓
3. **ReportService.GenerateUserReport()** [Depends on user list]
   ↓
4. **Admin Reports** [User-facing feature]
   - Impact: Admin user list page will break, reports will fail
   - Severity: HIGH

### Impact Summary by Layer
- **UI Layer**: 5 pages directly affected, 12 pages indirectly affected
- **Service Layer**: 3 services directly affected, 7 services indirectly affected
- **Data Layer**: 1 repository directly affected, 0 indirectly affected
- **Total**: 28 files impacted via dependency chains
```

### Phase 4: Breaking Change Assessment
**Duration**: 15-20% of total time
**Input**: Changes from Phase 1 + Dependencies from Phases 2-3
**Process**:
1. Identify all breaking changes:
   - Method signature changes (parameters, return type)
   - Method removals
   - Property type changes
   - Class renames or removals
   - Interface changes
   - Namespace changes
2. For each breaking change:
   - Count affected call sites
   - Assess fix effort (trivial, moderate, complex)
   - Identify mitigation strategies:
     - Overload methods (add new signature, keep old)
     - Deprecation path (mark old method obsolete)
     - Adapter pattern (wrapper for backward compatibility)
     - Migration script (automated refactoring)
3. Classify by compatibility:
   - **Source Compatible**: Code compiles but may behave differently
   - **Binary Compatible**: Compiled code still works
   - **Incompatible**: Compilation or runtime failure guaranteed
4. Estimate migration effort:
   - Number of files to update
   - Complexity of updates
   - Testing requirements
   - Total developer hours

**Tools Used**: None (analysis phase)
**Output**: Complete breaking change report with mitigation strategies
**Success Criteria**:
- All breaking changes identified
- Impact quantified (number of files, lines)
- Mitigation strategies proposed
- Migration effort estimated

**Example**:
```markdown
## Breaking Changes

### CRITICAL: ValidateUser() Signature Change

**Change**: Parameter added
- OLD: `ValidateUser(string username)`
- NEW: `ValidateUser(string username, string email)`

**Type**: Source Incompatible (compilation will fail)

**Impact**:
- 12 call sites must be updated
- Estimated effort: 2-3 hours
- All call sites in same solution (good - can update atomically)

**Mitigation Options**:

#### Option 1: Method Overload (Recommended)
```csharp
// Keep old signature for backward compatibility
[Obsolete("Use overload with email parameter")]
public bool ValidateUser(string username)
{
    return ValidateUser(username, null); // Call new signature
}

// New signature
public bool ValidateUser(string username, string email)
{
    // Implementation with email validation
}
```
**Pros**: No breaking change, gradual migration
**Cons**: Technical debt (remove obsolete method later)

#### Option 2: Atomic Update (All Call Sites)
Update all 12 call sites in single PR:
1. LoginController.cs:45
2. RegistrationController.cs:89
3. ... (full list)

**Pros**: Clean, no legacy code
**Cons**: Larger PR, higher testing burden

### CRITICAL: GetAllUsers() Method Removed

**Change**: Method deleted
- OLD: `public List<User> GetAllUsers()`
- NEW: (method removed)

**Type**: Source Incompatible (compilation will fail)

**Impact**:
- 8 call sites broken
- Estimated effort: 4-6 hours (includes testing)

**Replacement**:
```csharp
// Replace with filtered query
// OLD: var users = userService.GetAllUsers();
// NEW: var users = userService.GetUsers(new UserFilter { IsActive = true });

// Or use pagination
// NEW: var users = userService.GetUsersPaged(pageIndex: 0, pageSize: 1000);
```
```

### Phase 5: Risk Assessment
**Duration**: 15-20% of total time
**Input**: All findings from Phases 1-4
**Process**:
1. Assess **Compilation Risk**:
   - Breaking changes count
   - Files that won't compile
   - Risk level: LOW/MEDIUM/HIGH/CRITICAL
2. Assess **Runtime Risk**:
   - Behavior changes without compilation errors
   - Logic modifications with side effects
   - Potential for exceptions or errors
3. Assess **Data Risk**:
   - Database schema dependencies
   - Data migration requirements
   - Risk of data corruption or loss
4. Assess **Performance Risk**:
   - Changes to hot paths (frequently called methods)
   - Algorithm complexity changes
   - Potential performance degradation
5. Assess **Security Risk**:
   - Authentication/authorization changes
   - Input validation modifications
   - Exposure of sensitive data
6. Assess **Integration Risk**:
   - External API dependencies
   - Third-party service integrations
   - Cross-system communication
7. Calculate **Overall Risk Score**:
   - Weighted average of risk categories
   - Scale: LOW (1-3), MEDIUM (4-6), HIGH (7-8), CRITICAL (9-10)
8. Recommend risk mitigation:
   - Feature flags (gradual rollout)
   - Canary deployment (test with subset)
   - Blue-green deployment (instant rollback)
   - Staged rollout (by environment)

**Tools Used**: None (analysis phase)
**Output**: Comprehensive risk assessment with mitigation recommendations
**Success Criteria**:
- All risk categories assessed
- Overall risk score calculated
- Mitigation strategies provided
- Deployment recommendations included

**Example**:
```markdown
## Risk Assessment

### Compilation Risk: HIGH (8/10)
- 2 breaking changes affecting 20 call sites
- All affected files in same solution (mitigating factor)
- Recommendation: Update all call sites atomically in single PR

### Runtime Risk: MEDIUM (5/10)
- ValidateUser() logic changed (now requires email)
- Potential for null email parameter if callers not updated
- Recommendation: Add null checks and validation

### Data Risk: LOW (2/10)
- No database schema changes
- No data migration required
- No impact on existing data

### Performance Risk: LOW (3/10)
- ValidateUser() called ~1000 times/day (moderate frequency)
- Email validation adds minimal overhead (<1ms)
- No significant performance impact expected

### Security Risk: MEDIUM (4/10)
- Email validation adds security layer (positive)
- Null email handling must be secure (potential vulnerability if not handled)
- Recommendation: Ensure email validation is robust

### Integration Risk: LOW (1/10)
- No external API changes
- No third-party service impact
- All changes internal to application

### Overall Risk: HIGH (6.5/10)

### Deployment Recommendations

#### Recommended Approach: Coordinated Release
1. **Pre-Deployment**:
   - Update all 20 call sites in single PR
   - Add comprehensive unit tests for new signature
   - Update integration tests for all affected features

2. **Deployment**:
   - Deploy during maintenance window (low traffic)
   - Monitor error logs for 24 hours
   - Have rollback plan ready

3. **Post-Deployment**:
   - Verify all affected features functional
   - Monitor for unexpected errors
   - Remove obsolete methods after 2 weeks (if using overload strategy)

#### Alternative: Feature Flag Approach
- Wrap new ValidateUser logic in feature flag
- Deploy code but keep flag OFF
- Test in production with flag ON for subset of users
- Gradually roll out to 100%
- Pros: Safe, gradual rollout
- Cons: More complex code, longer migration period
```

### Phase 6: Report Generation
**Duration**: 10-15% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Compile all findings into structured markdown report
2. Write executive summary (2-3 paragraphs):
   - Change overview
   - Impact scope (number of files)
   - Risk level
   - Key recommendations
3. Document change analysis with code diff
4. Include complete dependency analysis (direct + indirect)
5. Present breaking changes with mitigation options
6. Include comprehensive risk assessment
7. Map impact to user-facing features:
   - Which features affected
   - How they're affected
   - User-visible impact
8. Create testing recommendations checklist:
   - Unit tests needed
   - Integration tests needed
   - Manual testing scenarios
   - Regression testing focus areas
9. Add deployment considerations:
   - Rollout strategy
   - Rollback plan
   - Monitoring requirements
   - Communication plan
10. Include appendix:
    - Dependency graph visualization
    - Complete file list
    - Code examples
11. Save report to `marketplace/output/analysis/` directory

**Tools Used**: Write
**Output**: Comprehensive impact analysis report
**Success Criteria**:
- Report is complete and well-structured
- All sections present
- File references accurate (file:line format)
- Recommendations actionable
- Report saved successfully

**Example Structure**:
```markdown
# Impact Analysis: UserService.cs

Generated: 2026-01-15 14:30:00
Duration: 42 minutes

## Executive Summary
...

## Change Analysis
### Modified Methods
...

## Direct Dependencies
### 12 Files Affected
...

## Indirect Dependencies
### 28 Files Affected via Dependency Chains
...

## Breaking Changes
### CRITICAL: ValidateUser() Signature Change
...

## Risk Assessment
### Overall Risk: HIGH (6.5/10)
...

## Affected Features
- Login (CRITICAL impact)
- Registration (HIGH impact)
- Password Reset (MEDIUM impact)
...

## Testing Recommendations
### Unit Tests
- [ ] Test ValidateUser() with email parameter
- [ ] Test ValidateUser() with null email (edge case)
- [ ] Test all updated call sites

### Integration Tests
- [ ] End-to-end login flow
- [ ] End-to-end registration flow
- [ ] Password reset flow
...

## Deployment Considerations
### Recommended Approach: Coordinated Release
...

## Appendix
### Dependency Graph
...

### Complete File List
...
```

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **root-cause-analysis** (`../../shared-skills/root-cause-analysis.md`)
  - Systematic process for distinguishing direct from indirect causes
  - Evidence collection and hypothesis validation
  - Impact chain documentation patterns

- **performance-analysis-framework** (`../../shared-skills/performance-analysis-framework.md`)
  - Performance impact assessment methodologies
  - Risk quantification techniques
  - Measurement and profiling approaches

## Error Handling

### Scenario: File Not Found
**When**: Specified file path doesn't exist
**Recovery**: Search for similar file names and suggest alternatives
**User Message**:
```
❌ File "Services/UserService.cs" not found.
Did you mean one of these?
- Services/UserAuthService.cs
- Services/UserManagementService.cs
- Business/UserService.cs

Please verify the file path or use absolute path.
```

### Scenario: No Changes Detected
**When**: File exists but no public interface changes detected
**Recovery**: Analyze internal changes and provide limited impact report
**User Message**:
```
ℹ️ No public interface changes detected in UserService.cs
Analysis will focus on:
- Internal method modifications
- Private method changes
- Potential side effects

Note: Impact is likely minimal since public interface unchanged.
Proceeding with analysis...
```

### Scenario: Large Impact Scope (50+ Files)
**When**: Changes affect many files across the codebase
**Recovery**: Enable Sequential Thinking for thorough analysis
**User Message**:
```
🔍 Large impact scope detected (73 files affected). Enabling deep analysis mode.
This analysis will take 30-40% longer but will provide:
- Complete dependency graph traversal
- Risk assessment for all impact paths
- Prioritized testing recommendations

Estimated time: 55-70 minutes
```

### Scenario: Git Not Available
**When**: Cannot use git diff to compare versions
**Recovery**: Analyze current file state only, prompt for manual diff
**User Message**:
```
⚠️ Git not available or file not in repository.
Analysis will be based on current file state only.

For more accurate analysis, please provide:
1. Previous version of the file (I'll compare manually)
2. List of changes made (methods added/removed/modified)
3. Or initialize git repository

Proceeding with current-state-only analysis...
```

### Scenario: Circular Dependency Detected
**When**: Dependency tracing finds circular references
**Recovery**: Flag circular dependency as risk and continue analysis
**User Message**:
```
⚠️ CIRCULAR DEPENDENCY DETECTED:
UserService → AuthService → ValidationService → UserService

This circular dependency:
- Increases coupling
- Makes impact analysis more complex
- Poses risk for future changes

Recommendation: Refactor to break circular dependency.
Continuing impact analysis with circular dependency noted...
```

### Scenario: Analysis Timeout
**When**: Analysis exceeds 90 minutes (very large codebase)
**Recovery**: Save partial results and offer to continue with specific focus
**User Message**:
```
⏱ Analysis timeout reached (90 minutes).
Partial results saved to: output/analysis/impact-UserService-partial.md

Continue with focused analysis? Options:
1. /continue-analysis UserService --focus=breaking-changes
2. /continue-analysis UserService --focus=risk-assessment
3. /analyze-impact UserService --depth=shallow (faster, less deep tracing)
```

## Configuration

### Required Settings
None - agent works with defaults

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "analysis-toolkit": {
    "impact-analyzer": {
      "timeout_minutes": 90,
      "enable_sequential_thinking": "conditional",
      "sequential_thinking_trigger": {
        "min_affected_files": 50,
        "min_dependency_depth": 4
      },
      "dependency_depth": "normal",
      "report_detail_level": "full",
      "include_dependency_graph": true,
      "max_indirect_levels": 3,
      "exclude_test_files": false
    }
  }
}
```

**Configuration Options**:
- `timeout_minutes`: Maximum analysis time (default: 90)
- `enable_sequential_thinking`: "always", "conditional", or "never" (default: "conditional")
- `sequential_thinking_trigger`: Conditions for enabling Sequential Thinking
- `dependency_depth`: "shallow" (direct only), "normal" (2 levels), "deep" (3+ levels) (default: "normal")
- `report_detail_level`: "full" or "summary" (default: "full")
- `include_dependency_graph`: Generate visual dependency graph (default: true)
- `max_indirect_levels`: Maximum dependency tracing depth (default: 3)
- `exclude_test_files`: Exclude test files from impact analysis (default: false)

## Tools Required

- **Bash**: Execute git commands for diff analysis
- **Glob**: Find related files by pattern
- **Grep**: Search codebase for references to changed elements
- **Read**: Read changed files and dependent files
- **Write**: Generate impact analysis report
- **Task**: Delegate to sub-agents for specialized analysis (if needed)

## Examples

### Example 1: Simple Change - Method Added
**Input**:
```bash
/analyze-impact Services/UserService.cs
```

**Change**: New method `GetUserByEmail()` added
**Process**:
- Phase 1: Analyze changes (method addition) (3 min)
- Phase 2: Search for references (none - new method) (5 min)
- Phase 3: No indirect dependencies (2 min)
- Phase 4: No breaking changes (2 min)
- Phase 5: Low risk assessment (3 min)
- Phase 6: Generate report (3 min)

**Output**: Report with:
- Change: New method added (low risk)
- Impact: No existing code affected
- Risk: LOW (addition only, no breaking changes)
- Recommendation: Add unit tests for new method

**Time**: ~18 minutes
**Risk**: LOW

### Example 2: Complex Change - Method Signature Modified
**Input**:
```bash
/analyze-impact Services/UserService.cs
```

**Change**: `ValidateUser(string username)` → `ValidateUser(string username, string email)`
**Process**:
- Phase 1: Analyze changes (signature modification) (4 min)
- Phase 2: Search references (12 call sites) (8 min)
- Phase 3: Trace indirect dependencies (28 files) (18 min) [Sequential Thinking enabled]
  - Initial: Focus on direct callers
  - Reflection: Controllers have downstream dependencies
  - Course correction: Trace all controller paths to UI
- Phase 4: Assess breaking change (8 min)
- Phase 5: Comprehensive risk assessment (6 min)
- Phase 6: Generate detailed report (4 min)

**Output**: Report with:
- Change: Breaking change (method signature)
- Direct impact: 12 files
- Indirect impact: 28 files
- Risk: HIGH (compilation failures guaranteed)
- Affected features: Login, Registration, Password Reset
- Recommendations: Atomic update or method overload

**Time**: ~48 minutes
**Risk**: HIGH

### Example 3: Large-Scale Change - Shared Utility Modified
**Input**:
```bash
/analyze-impact Common/Utilities/StringHelper.cs --depth=deep
```

**Change**: Multiple utility methods modified
**Process**:
- Phase 1: Analyze changes (multiple methods) (5 min)
- Phase 2: Search references (87 call sites!) (15 min)
- Phase 3: Trace deep dependencies (3 levels, 150+ files) (25 min) [Sequential Thinking enabled]
- Phase 4: Assess multiple breaking changes (12 min)
- Phase 5: Comprehensive risk assessment (10 min)
- Phase 6: Generate detailed report with graph (8 min)

**Output**: Report with:
- Change: Multiple utility methods modified
- Direct impact: 87 files
- Indirect impact: 150+ files across entire codebase
- Risk: CRITICAL (high fan-out utility)
- Recommendations: Phased rollout, extensive testing, feature flags

**Time**: ~75 minutes
**Risk**: CRITICAL

## Success Metrics

Analysis is successful when:
- [ ] Changed file successfully analyzed
- [ ] All modified public elements identified
- [ ] All direct consumers found (with file:line references)
- [ ] Indirect dependencies traced (at least 2 levels deep)
- [ ] Breaking changes identified (if any)
- [ ] Risk assessment complete for all categories
- [ ] Impact mapped to user-facing features
- [ ] Testing recommendations provided
- [ ] Deployment strategy recommended
- [ ] Report is comprehensive and actionable
- [ ] Report saved to correct output directory
- [ ] Confidence level meets threshold (>85% for simple changes, >75% for complex)

## Related Agents

- **jira-root-cause-analyzer**: Use when impact analysis needed for Jira ticket
- **db-query-analyzer**: Use when analyzing database schema change impact
- **stack-trace-analyzer**: Use when change causes errors (analyze stack trace first)
- **review-agents**: Use for code quality review (impact analysis focuses on dependency scope)

## Related Documentation

- `../../shared-skills/root-cause-analysis.md` - Root cause methodology
- `../../shared-skills/performance-analysis-framework.md` - Performance impact assessment
- `../../../docs/WORKFLOW_DECISION_GUIDE.md` - When to use which analysis agent
- `../../../docs/TROUBLESHOOTING.md` - Common issues and solutions
- `../commands/analyze-impact.md` - Command specification

---

**Agent Status**: Production Ready
**Verification Mode**: Enabled (all findings backed by code search evidence)
**Sequential Thinking**: Conditional (auto-enabled for large impact scope)
**Average Duration**: 30-50 minutes depending on change scope
