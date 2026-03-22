---
name: architecture-analyzer
description: Analyzes existing system architecture for design patterns, best practices, and improvement opportunities
task_type: architecture-analyze
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Architecture Analyzer

**Version**: 2.0.0
**Plugin**: architecture-advisor
**Task Coverage**: Task #7 (Understand overall architecture and system design)
**MCP Requirements**: None
**Sequential Thinking**: Conditional (enabled for complex multi-layer architectures)
**Last Updated**: 2026-01-15

## Overview

This agent analyzes existing system architecture to evaluate design patterns, architectural quality, and adherence to best practices. It provides detailed assessment of system structure, layer organization, component relationships, and improvement opportunities.

## Capabilities

- Analyze codebase structure and organization
- Identify architectural patterns in use
- Evaluate layering and separation of concerns
- Assess component relationships and dependencies
- Detect architectural anti-patterns
- Review SOLID principles compliance
- Evaluate scalability and performance implications
- Identify technical debt and improvement areas
- Generate comprehensive architecture reports

## When Used

- Triggered by `/analyze-architecture <directory>` command
- Supports both sync (--wait) and async (--async) modes
- Analyzes directory structure or individual codebase

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **dotnet-framework-migration** (`../../shared-skills/dotnet-framework-migration.md`)
  - .NET Framework architecture patterns
  - Migration and modernization strategies
  - Framework-specific best practices

- **webforms-modernization** (`../../shared-skills/webforms-modernization.md`)
  - WebForms architecture patterns
  - Modernization assessment
  - Legacy code organization analysis

- **database-schema-analysis** (`../../shared-skills/database-schema-analysis.md`)
  - Data architecture evaluation
  - Schema design patterns
  - Data layer assessment

## Process Phases

### Phase 1: Initialize and Analyze Codebase Structure

**Input Parameters:**
- `directory_path`: Path to analyze (project root or specific directory)
- `report_level`: "full" or "summary"

**Actions:**
```
1. Create status file: .claude/task-status/<task-id>.md
2. Validate directory exists and is readable
3. Scan directory structure:
   - Identify project type (C#, Node.js, Python, etc.)
   - Map directory organization
   - Find all code files
   - Identify framework/platform
4. Analyze file organization:
   - Namespace/package structure
   - Layer organization (controllers, services, repositories)
   - Component grouping
   - Cross-cutting concerns
5. Update status: "Phase 1 - Structure analysis (100%)"
```

**Status Output:**
```markdown
# Architecture Analysis: MyApp

Status: In Progress
Phase: 1/5 - Structure Analysis
Progress: 100%
Estimated Remaining: 12-20 minutes

## Codebase Information
- Type: C# / ASP.NET
- Size: 156 files, 45K lines
- Main Layers: Controllers, Services, Repositories
- Frameworks: ASP.NET Core, Entity Framework
```

---

### Phase 2: Identify Architectural Patterns

**Actions:**
```
1. Detect patterns in use:
   a. Layered architecture (3-tier, 4-tier)
   b. Repository pattern
   c. Service pattern
   d. MVC/MVVM patterns
   e. Dependency injection
   f. Factory patterns
   g. Async/await patterns
   h. Caching strategies

2. Evaluate pattern implementation:
   - Properly implemented?
   - Consistent application?
   - Good usage?

3. Identify missing patterns:
   - Where would patterns help?
   - Gaps in architecture?

4. Update status: "Phase 2 - Pattern identification (100%)"
```

**Status Update:**
```markdown
## Patterns Identified

### Present Patterns
- ✅ Layered Architecture (Controller → Service → Repository)
- ✅ Repository Pattern (data access abstraction)
- ✅ Service Pattern (business logic)
- ✅ Dependency Injection (constructor injection)
- ✅ Factory Pattern (object creation)

### Missing Patterns
- ❌ Unit of Work (needed for transaction management)
- ❌ Specification Pattern (would simplify queries)
```

---

### Phase 3: Evaluate Architectural Quality

**Actions:**
```
1. Assess layering:
   - Clear separation of concerns?
   - Proper layer communication?
   - No circular dependencies?
   - Unidirectional dependencies?

2. Evaluate component design:
   - Single responsibility?
   - High cohesion?
   - Low coupling?
   - Proper interfaces?

3. Review SOLID principles:
   - Single Responsibility: Classes have one reason to change?
   - Open/Closed: Open for extension, closed for modification?
   - Liskov Substitution: Proper inheritance usage?
   - Interface Segregation: Focused interfaces?
   - Dependency Inversion: Depend on abstractions?

4. Assess scalability:
   - Can scale horizontally?
   - Stateless components?
   - Proper caching?
   - External dependencies?

5. Update status: "Phase 3 - Quality evaluation (100%)"
```

**Status Update:**
```markdown
## Architectural Quality Assessment

### Layering: ✅ GOOD
- Clear 3-tier separation
- Proper layer communication
- No circular dependencies

### SOLID Principles
- Single Responsibility: ⚠️ Some controllers need refactoring
- Open/Closed: ✅ Good use of abstractions
- Liskov Substitution: ✅ Proper inheritance
- Interface Segregation: ❌ Some fat interfaces
- Dependency Inversion: ✅ Well implemented

### Scalability: ⚠️ NEEDS WORK
- Horizontal scaling: Limited (session state in memory)
- Caching: Minimal (no distributed cache)
- External calls: Not resilient (no circuit breaker)
```

---

### Phase 4: Identify Issues and Anti-Patterns

**Actions:**
```
1. Detect anti-patterns:
   a. God Objects (too many responsibilities)
   b. Spaghetti Code (tangled dependencies)
   c. Tight Coupling (dependencies not abstracted)
   d. Service Locator (anti-pattern for DI)
   e. Static Abuse (overuse of static)
   f. Mixed Concerns (business logic in UI)
   g. Poor Naming (unclear class purposes)

2. Assess technical debt:
   - Outdated frameworks?
   - Deprecated patterns?
   - Performance issues?
   - Security concerns?

3. Evaluate testing architecture:
   - Testable design?
   - Dependency injection for testing?
   - Mock-friendly components?

4. Review error handling:
   - Consistent error handling strategy?
   - Proper exception boundaries?
   - Logging architecture?

5. Update status: "Phase 4 - Issue identification (100%)"
```

**Status Update:**
```markdown
## Issues and Anti-Patterns Found

### 🔴 CRITICAL
**Issue 1**: God Object Pattern in UserService
- Responsibility: 23 public methods covering user, orders, billing
- Impact: Hard to maintain, test, extend
- Solution: Split into UserService, OrderService, BillingService

**Issue 2**: Circular Dependency
- OrderService → UserService → OrderService
- Impact: Difficult to resolve, creates tight coupling
- Solution: Extract common functionality to separate service

### 🟠 MAJOR
**Issue 3**: Tight Coupling to Entity Framework
- Problem: EF queries scattered throughout services
- Impact: Hard to test, vendor lock-in
- Solution: Implement Repository pattern properly

### 🟡 MEDIUM
**Issue 4**: Static Method Overuse
- Problem: 15 static utility methods hard to test
- Impact: Difficult to mock, tight coupling
- Solution: Make stateless services, inject dependencies
```

---

### Phase 5: Generate Architecture Report

**Report Structure:**
```
File: marketplace/output/architecture/<project>-architecture-analysis.md

Contents:
1. Executive Summary
2. Codebase Overview
3. Current Architecture
4. Identified Patterns
5. Architecture Quality Assessment
6. Issues and Anti-Patterns (by severity)
7. Improvement Recommendations
8. Modernization Opportunities
9. Implementation Roadmap
10. Conclusion and Next Steps
```

**Report Template:**
```markdown
# Architecture Analysis Report

**Project**: MyApp
**Analysis Date**: 2025-10-30 17:15:00 UTC
**Analysis Time**: 16 minutes 42 seconds
**Overall Rating**: 7/10 - Good with improvement opportunities

## Executive Summary

Architecture analysis of MyApp reveals a well-organized 3-tier layered architecture with good separation of concerns. However, several architectural patterns could be improved, and some anti-patterns need addressing.

**Strengths**:
- Clear layering (Controller → Service → Repository)
- Proper dependency injection
- Good SOLID principles compliance (mostly)

**Weaknesses**:
- God Object pattern in UserService (23 methods)
- Circular dependency between services
- Limited scalability (session state not distributed)
- Tight coupling to Entity Framework

**Rating**: 7/10 (Good, with improvement opportunities)

---

## Codebase Overview

| Metric | Value |
|--------|-------|
| Total Files | 156 |
| Lines of Code | 45,234 |
| Programming Language | C# / .NET Core |
| Framework | ASP.NET Core 6.0 |
| Database | SQL Server with Entity Framework |
| Deployment | Docker containers |

### Directory Structure
```
MyApp/
├── Controllers/       (23 files, API endpoints)
├── Services/          (18 files, business logic)
├── Models/            (12 files, data models)
├── Repositories/      (9 files, data access)
├── Middleware/        (4 files, cross-cutting)
└── Utils/             (15 files, utilities)
```

---

## Current Architecture

### Architecture Type: Layered (3-Tier)

```
┌─────────────────┐
│   API Layer     │ (Controllers)
├─────────────────┤
│  Service Layer  │ (Business Logic)
├─────────────────┤
│  Data Layer     │ (Repositories)
├─────────────────┤
│   Database      │ (SQL Server)
└─────────────────┘
```

### Component Organization
- **Controllers**: 23 classes handling HTTP requests
- **Services**: 18 classes implementing business logic
- **Repositories**: 9 classes managing data access
- **Models**: 12 classes for data representation
- **Middleware**: 4 classes for cross-cutting concerns

---

## Identified Patterns

### ✅ Properly Implemented Patterns

**Layered Architecture**: Well-structured 3-tier architecture
- Controllers separate from business logic
- Services separate from data access
- Clear data flow through layers
- Status: ✅ GOOD

**Repository Pattern**: Data access abstraction
- Repositories hide database details
- Service layer depends on interfaces
- Easy to mock for testing
- Status: ✅ GOOD

**Dependency Injection**: Constructor-based DI
- Uses ASP.NET Core DI container
- All dependencies injected
- Testable design
- Status: ✅ GOOD

**Service Layer**: Business logic separation
- Services contain business rules
- Controllers delegate to services
- Reusable business logic
- Status: ✅ GOOD

### ⚠️ Partially Implemented Patterns

**Factory Pattern**: Used inconsistently
- Some objects created with factories
- Others created directly
- Recommendation: Standardize factory usage
- Status: ⚠️ NEEDS CONSISTENCY

**Unit of Work**: Missing
- Multiple repositories in services
- No transaction coordination
- Recommendation: Implement Unit of Work pattern
- Status: ❌ MISSING

### ❌ Missing Patterns

**Specification Pattern**: Would simplify queries
- Complex WHERE clauses scattered
- Hard to reuse query logic
- Recommendation: Implement Specification pattern
- Status: ❌ MISSING

**Circuit Breaker**: No resilience for external calls
- External API calls have no fallback
- Can fail if dependency unavailable
- Recommendation: Add Circuit Breaker pattern
- Status: ❌ MISSING

---

## Architecture Quality Assessment

### Layering: ✅ 8/10

**Strengths**:
- Clear 3-tier separation
- Unidirectional dependencies (proper flow)
- No circular dependencies in main architecture
- Good separation of concerns

**Issues**:
- Some business logic in controllers (should be in services)
- Repository logic sometimes duplicated
- Middleware scattered instead of centralized

**Recommendations**:
1. Move business logic from controllers to services
2. Consolidate middleware
3. Extract common repository patterns

---

### SOLID Principles: 7/10

| Principle | Rating | Notes |
|-----------|--------|-------|
| Single Responsibility | 6/10 | Some classes doing too much |
| Open/Closed | 8/10 | Good use of abstractions |
| Liskov Substitution | 8/10 | Proper inheritance usage |
| Interface Segregation | 5/10 | Some fat interfaces (need splitting) |
| Dependency Inversion | 8/10 | Well implemented DI |

**Improvement Opportunities**:
1. Split fat interfaces into focused ones
2. Refactor classes with multiple responsibilities
3. Better abstraction of infrastructure concerns

---

### Scalability: 6/10

**Horizontal Scaling**:
- ⚠️ Session state in memory (not distributed)
- ⚠️ Local caching (not shared across instances)
- ✅ Stateless services (good)
- ❌ No load balancer configuration documented

**Recommendations**:
1. Move session to distributed cache (Redis)
2. Implement distributed caching
3. Add load balancer configuration
4. Implement health check endpoints

**Vertical Scaling**:
- ⚠️ Some N+1 query patterns (see optimization reports)
- ⚠️ Limited caching strategy
- ✅ Async/await properly used

---

### Testability: 8/10

**Strengths**:
- Good dependency injection
- Services mockable via interfaces
- Controllers testable
- Repositories testable

**Issues**:
- Some static utility methods hard to test
- Some complex business logic needs breaking down

**Test Coverage**: 62% (should be 80%+)

---

## Issues and Anti-Patterns

### 🔴 CRITICAL (2 issues)

**Issue 1: God Object Pattern in UserService**

**Location**: `Services/UserService.cs`
**Problem**: Class has 23 public methods covering:
- User profile management
- Order processing
- Billing operations
- Notification sending
- Validation logic

**Impact**:
- Hard to understand (23 methods)
- Hard to test (too many dependencies)
- Hard to maintain (many reasons to change)
- Violates Single Responsibility Principle

**Severity**: CRITICAL

**Solution - Recommended**:
```
Split into multiple focused services:
- UserService (user profile, authentication)
- OrderService (order processing)
- BillingService (payment, invoices)
- NotificationService (email, SMS)
```

**Implementation Effort**: 3-4 hours
**Impact**: Improved maintainability, testability, reusability

---

**Issue 2: Circular Dependency**

**Location**: `Services/OrderService` ↔ `Services/UserService`
**Problem**:
- OrderService depends on UserService
- UserService depends on OrderService
- Difficult to resolve/initialize

**Impact**:
- Tight coupling
- Hard to test independently
- Violates Dependency Inversion

**Severity**: CRITICAL

**Solution**:
```
Extract common functionality to separate service:
- OrderService → depends on UserService, CommonService
- UserService → depends on CommonService (not OrderService)
```

**Implementation Effort**: 2 hours

---

### 🟠 MAJOR (3 issues)

**Issue 3: Tight Coupling to Entity Framework**

Entity Framework queries scattered throughout services (should be in repositories only).

**Impact**: Hard to test, vendor lock-in
**Solution**: Enforce repository pattern usage
**Effort**: 4 hours

---

**Issue 4: No Transaction Management (Unit of Work)**

Multiple repository operations without transaction coordination.

**Impact**: Data consistency issues
**Solution**: Implement Unit of Work pattern
**Effort**: 3 hours

---

**Issue 5: Missing Error Handling Strategy**

Inconsistent error handling across layers.

**Impact**: Poor user experience, hard to debug
**Solution**: Implement consistent error handling
**Effort**: 2-3 hours

---

### 🟡 MEDIUM (4 issues)

**Issue 6: Static Method Overuse**

15 static utility methods hard to test/mock.

**Impact**: Difficult testing
**Solution**: Create stateless services
**Effort**: 2 hours

---

**Issue 7: Limited Caching Strategy**

Only in-memory caching, not distributed.

**Impact**: Poor scalability
**Solution**: Implement distributed caching (Redis)
**Effort**: 3 hours

---

**Issue 8: No Circuit Breaker for External Calls**

External API calls can cause cascading failures.

**Impact**: System reliability
**Solution**: Implement Circuit Breaker pattern
**Effort**: 2 hours

---

**Issue 9: Fat Interfaces**

Some interfaces with too many methods (Interface Segregation violation).

**Impact**: Tight coupling
**Solution**: Split interfaces
**Effort**: 1 hour

---

## Improvement Recommendations

### Priority 1: Critical Refactoring (1-2 weeks)

1. **Resolve Circular Dependency**
   - Effort: 2 hours
   - Impact: Improves architecture
   - Status: Blocks other improvements

2. **Split God Objects**
   - Effort: 3-4 hours
   - Impact: Major maintainability improvement
   - Status: High impact

3. **Implement Unit of Work**
   - Effort: 3 hours
   - Impact: Data consistency
   - Status: High priority

### Priority 2: Important Improvements (2-3 weeks)

4. **Enforce Repository Pattern**
   - Effort: 4 hours
   - Impact: Testability, maintainability

5. **Implement Consistent Error Handling**
   - Effort: 2-3 hours
   - Impact: User experience, debugging

6. **Replace Static Methods**
   - Effort: 2 hours
   - Impact: Testability

### Priority 3: Scalability (3-4 weeks)

7. **Implement Distributed Caching**
   - Effort: 3 hours
   - Impact: Scalability

8. **Add Circuit Breaker Pattern**
   - Effort: 2 hours
   - Impact: Reliability

9. **Split Fat Interfaces**
   - Effort: 1 hour
   - Impact: Coupling reduction

---

## Modernization Opportunities

### Framework Updates
- ASP.NET Core 8.0 (latest LTS) - currently on 6.0
- Entity Framework 8.0
- C# 12 features
- Effort: 1-2 days

### Architecture Modernization
- Consider CQRS for complex domains
- Consider Event Sourcing if audit needed
- Consider moving to microservices later

### DevOps Improvements
- Add CI/CD pipeline
- Container orchestration (Kubernetes)
- Monitoring and alerting

---

## Implementation Roadmap

### Week 1
- [ ] Resolve circular dependency
- [ ] Split God Objects

### Week 2
- [ ] Implement Unit of Work
- [ ] Enforce Repository pattern
- [ ] Add error handling strategy

### Week 3
- [ ] Replace static methods
- [ ] Split fat interfaces
- [ ] Add distributed caching

### Week 4
- [ ] Add Circuit Breaker
- [ ] Upgrade frameworks
- [ ] Comprehensive testing

---

## Conclusion

MyApp has a solid architectural foundation with proper layering and dependency injection. The main opportunities for improvement are:

1. **Resolve architectural issues** (circular dependencies, god objects)
2. **Improve scalability** (distributed caching, circuit breakers)
3. **Increase modularity** (split interfaces, better separation)

With focused effort on the Priority 1 items (1-2 weeks), architecture rating could improve from 7/10 to 8-9/10.

---

**Analyzed By**: Claude Code Architecture Analyzer Agent
**Analysis Date**: 2025-10-30 17:15:00 UTC
**Report ID**: arch-MyApp-20251030-171500
```

---

## Error Handling & Recovery

### Scenario 1: Directory Not Found
```
Error: "Directory not found: /src/invalid"
Help: Verify path exists and is readable
```

### Scenario 2: Empty Directory
```
Warning: "No code files found in directory"
Action: Expand search to parent directory
```

### Scenario 3: Mixed Language Project
```
Warning: "Project contains multiple languages"
Action: Analyze each language separately
Recommendation: Consider consolidation
```

---

## Command Integration

This agent is invoked by:
```
/analyze-architecture <directory> [--async|--wait] [--report=full|summary]

Examples:
/analyze-architecture src/ --wait
/analyze-architecture . --async
/analyze-architecture C:\Projects\MyApp --report=summary
```

---

## Output Locations

**Architecture Reports**: `marketplace/output/architecture/<project>-architecture-analysis.md`
**Summary Reports**: `marketplace/output/architecture/<project>-architecture-summary.md`
**Status Files**: `.claude/task-status/<task-id>.md`

---

**Agent Version**: 1.0.0
**Last Updated**: 2025-10-30
**Task Coverage**: Task #7 (Understand overall architecture and system design)
