---
description: "Recommend design patterns for specific problems and use cases"
argument-hint: "<problem-description> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write]
---

# Command: /suggest-patterns

## Usage

```
/suggest-patterns <problem-description> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **problem-description**: Description of problem or challenge
  - Example: "Need flexible authentication with multiple providers"
  - Example: "How to decouple UI from business logic"
  - Can include constraints and requirements

### Optional Flags

- **--async**: Execute in background
- **--wait**: Execute synchronously (default)
- **--report=full|summary**: Report level (full by default)

## Examples

```bash
# Get pattern recommendations (synchronous)
/suggest-patterns "Need flexible authentication with multiple providers" --wait

# Background analysis
/suggest-patterns "How to manage cache invalidation?" --async

# Quick summary
/suggest-patterns "Decouple UI from business logic" --report=summary
```

## Implementation

### Step 1: Parse Arguments
- Extract problem description
- Identify key challenges
- Set execution mode
- Set report level

### Step 2: Analyze Problem
- Understand domain
- Identify constraints
- Recognize pattern context

### Step 3: Queue/Execute Task
- For async: Create task, return task ID
- For sync: Delegate to design-pattern-advisor agent

### Step 4: Delegate to Agent
- Identify candidate patterns
- Analyze pattern fit
- Evaluate trade-offs
- Provide code examples
- Generate recommendations

### Step 5: Return Response

**Async**:
```
Task ID: task-20251030-190030-pattern-xyz
Estimated time: 8-12 minutes
```

**Sync**:
```
# Pattern Recommendation: Authentication

[Pattern analysis with recommendations]

Report: marketplace/output/reviews/auth-pattern-recommendation.md
```

## Output Locations

- Recommendations: `marketplace/output/reviews/<problem>-pattern-recommendation.md`
- Summary: `marketplace/output/reviews/<problem>-pattern-summary.md`
- Status: `.claude/task-status/<task-id>.md`

## Typical Analysis Time

- Simple problem: 5-8 minutes
- Complex problem: 8-15 minutes
- Ambiguous problem: 12-20 minutes

## Common Pattern Questions

```bash
# Structural patterns
/suggest-patterns "Need to organize complex UI components"

# Behavioral patterns
/suggest-patterns "How to handle different payment methods?"

# Creational patterns
/suggest-patterns "Need flexible object creation"

# Architectural patterns
/suggest-patterns "Should we use microservices?"
```

## What It Covers

- **Structural Patterns**: Adapter, Bridge, Composite, Decorator, Facade, Proxy
- **Behavioral Patterns**: Observer, Strategy, State, Command, Template Method, Iterator
- **Creational Patterns**: Factory, Abstract Factory, Builder, Singleton, Prototype
- **Architectural Patterns**: Layered, MVC, Microservices, Event-Driven, CQRS

## FAQ

**Q: Can I describe a problem I'm facing?**
A: Yes, that's exactly what this is for

**Q: Will you recommend just one pattern?**
A: Usually multiple candidates with comparison

**Q: Will you provide code examples?**
A: Yes, with before/after code showing pattern use

**Q: What if no pattern fits?**
A: Will explain why and suggest alternatives

**Q: Where are reports saved?**
A: `marketplace/output/reviews/`

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Delegated To**: design-pattern-advisor agent
**Task Coverage**: Task #8
