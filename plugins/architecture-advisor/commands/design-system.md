---
description: "Design system architecture for new applications or features"
argument-hint: "<requirements-file> [--async|--wait] [--report=full|summary]"
allowed-tools: [Bash, Read, Write]
---

# Command: /design-system

## Usage

```
/design-system <requirements-file> [--async|--wait] [--report=full|summary]
```

## Arguments

### Required Arguments

- **requirements-file**: Path to requirements document
  - Format: Markdown, text, or specification file
  - Example: `/design-system requirements.md`
  - Example: `/design-system project-spec.txt`

### Optional Flags

- **--async**: Execute in background
- **--wait**: Execute synchronously (default)
- **--report=full|summary**: Report level (full by default)

## Examples

```bash
# Design system based on requirements (synchronous)
/design-system requirements.md --wait

# Background design analysis
/design-system project-spec.txt --async

# Quick summary
/design-system specifications.md --report=summary
```

## Implementation

### Step 1: Parse Arguments
- Extract requirements file path
- Validate file exists
- Set execution mode
- Set report level

### Step 2: Validate File
- Check file is readable
- Verify contains requirements
- Detect file type

### Step 3: Queue/Execute Task
- For async: Create task, return task ID
- For sync: Delegate to system-designer agent

### Step 4: Delegate to Agent
- Analyze requirements
- Design architecture
- Define components
- Plan data flows
- Specify non-functional aspects
- Generate design document

### Step 5: Return Response

**Async**:
```
Task ID: task-20251030-190045-design-abc
Estimated time: 15-25 minutes
```

**Sync**:
```
# System Design: E-Commerce Platform

[Comprehensive design document]

Report: marketplace/output/reviews/ecommerce-system-design.md
```

## Output Locations

- System Design: `marketplace/output/reviews/<system>-system-design.md`
- Summary: `marketplace/output/reviews/<system>-design-summary.md`
- Status: `.claude/task-status/<task-id>.md`

## Typical Analysis Time

- Simple system: 10-15 minutes
- Medium system: 15-25 minutes
- Complex system: 25-40 minutes

**Recommendation**: Use `--async` for complex systems.

## Requirements File Format

Provide requirements including:
- Functional requirements (features, use cases)
- Non-functional requirements (performance, scalability, security)
- Constraints (technology, team, budget, timeline)
- External integrations
- Data requirements
- User volume expectations

Example:
```
# E-Commerce Platform Requirements

## Functional
- Product catalog browsing
- Shopping cart management
- Checkout and payment
- Order tracking
- Admin dashboard

## Non-Functional
- 100K concurrent users
- < 200ms response time
- 99.9% availability
- PCI compliance

## Constraints
- ASP.NET Core, React
- SQL Server
- AWS infrastructure

## Integrations
- Stripe for payments
- SendGrid for email
- Google Analytics
```

## Output Includes

- Architecture diagram
- Component descriptions
- Data models
- Request/response flows
- Security design
- Scalability plan
- Resilience strategy
- Deployment architecture
- Implementation roadmap
- Development checklist

## FAQ

**Q: Can I provide requirements as text?**
A: Yes, markdown or plain text works

**Q: How detailed should requirements be?**
A: More detail = better design. Rough requirements OK.

**Q: Will it generate code?**
A: No, architecture design only

**Q: Can I iterate on design?**
A: Yes, refine requirements and redesign

**Q: What technology stacks does it support?**
A: All major stacks - you specify in requirements

**Q: Where are designs saved?**
A: `marketplace/output/reviews/`

---

**Command Version**: 1.0.0
**Last Updated**: 2025-10-30
**Delegated To**: system-designer agent
**Task Coverage**: Task #9
