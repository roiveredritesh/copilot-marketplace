---
allowed-tools: [Task, Read, Write, Grep, Glob, Bash]
argument-hint: <problem-description> [--async|--wait] [--depth=shallow|medium|deep]
description: Collaboratively solve technical challenges
---

# Command: /solve-problem

Collaboratively explores solutions to technical challenges with root cause analysis, multiple solution approaches, and implementation guidance.

## Usage

```
/solve-problem <problem-description> [--async|--wait] [--depth=shallow|medium|deep]
```

## Arguments

### Required Arguments

- **problem-description**: The technical challenge to solve
  - `/solve-problem "database queries are getting slow"`
  - `/solve-problem "handling concurrent user requests efficiently"`
  - `/solve-problem "reducing memory consumption in background service"`
  - `/solve-problem "managing distributed transaction consistency"`

### Optional Flags

- **--async**: Execute in background (recommended for complex problems)
- **--wait**: Execute synchronously (default, waits for completion)
- **--depth**: Analysis depth
  - `shallow`: Quick solutions overview, 5-10 minutes
  - `medium`: Balanced analysis with recommendations (default, 10-20 minutes)
  - `deep`: Comprehensive root cause and multi-faceted solutions, 20-30 minutes

## Examples

```bash
# Solve database performance issue
/solve-problem "database queries are getting slow"

# In-depth concurrent request handling analysis
/solve-problem "handling concurrent user requests efficiently" --async --depth=deep

# Quick memory optimization suggestions
/solve-problem "reducing memory consumption" --depth=shallow

# Background problem-solving session
/solve-problem "distributed transaction consistency" --async
```

## How It Works

The agent will:

1. **Understand the Problem**:
   - Extract key challenge details
   - Research existing codebase context
   - Identify root causes vs symptoms

2. **Root Cause Analysis**:
   - Find actual cause of the problem
   - Identify contributing factors
   - Map dependencies and impacts

3. **Explore Multiple Solutions**:
   - Generate 4-6 solution approaches
   - Quick-fix vs proper solutions
   - Systemic improvements

4. **Evaluate Each Solution**:
   - Implementation complexity
   - Time to implement
   - Resource requirements
   - Risk assessment
   - Performance impact
   - Maintenance burden

5. **Provide Recommendations**:
   - Best fit solution for your constraints
   - Phased implementation approach
   - Fallback strategies

6. **Create Implementation Guide**:
   - Step-by-step implementation
   - Testing strategy
   - Validation checklist
   - Rollback plan

## Output Locations

- Problem analysis: `marketplace/output/brainstorming/<problem>-analysis.md`
- Solution approaches: `marketplace/output/brainstorming/<problem>-solutions.md`
- Implementation guide: `marketplace/output/brainstorming/<problem>-implementation.md`

## Typical Analysis Time

- Shallow: 5-10 minutes
- Medium: 10-20 minutes (default)
- Deep: 20-30 minutes (comprehensive analysis)

**Recommendation**: Use `--async --depth=deep` for critical problems requiring thorough analysis.

## Output Format

The problem-solving session includes:

- **Problem Summary**: Challenge description and context
- **Root Cause Analysis**:
  - Actual cause (not just symptoms)
  - Contributing factors
  - Evidence and research
  - Impact assessment

- **Solution Approaches** (4-6 options):
  - Solution title and overview
  - How it solves the problem
  - Implementation complexity (1-5)
  - Time estimate
  - Resource requirements
  - Risk level
  - Performance impact

- **Solution Comparison Table**:
  - All approaches side-by-side
  - Key metrics and trade-offs
  - Suitability score

- **Recommended Solution**:
  - Why this approach best fits
  - Key advantages
  - Potential risks and mitigation
  - Success criteria

- **Implementation Roadmap**:
  - Phase 1: Foundation and setup
  - Phase 2: Core implementation
  - Phase 3: Testing and validation
  - Phase 4: Deployment (if applicable)
  - Estimated timeline for each phase

- **Testing Strategy**:
  - Unit test approach
  - Integration test approach
  - Performance test approach
  - Edge cases to test

- **Validation Checklist**:
  - Pre-implementation checklist
  - Implementation verification steps
  - Post-implementation validation
  - Success metrics

- **Rollback Plan**:
  - How to revert if needed
  - Safety measures
  - Data consistency concerns

- **Monitoring & Maintenance**:
  - What to monitor post-implementation
  - Alert thresholds
  - Maintenance requirements
  - Future optimization opportunities

- **Related Problems**: Similar challenges and their solutions
- **References**: Articles, patterns, tools relevant to solution

## Problem Categories Covered

- **Performance Issues**: Query optimization, caching, indexing
- **Scalability Challenges**: Horizontal scaling, load balancing, distributed systems
- **Concurrency Problems**: Race conditions, deadlocks, synchronization
- **Memory Issues**: Leaks, optimization, allocation strategies
- **Data Consistency**: Transactions, distributed consensus, eventual consistency
- **Architecture Challenges**: Service boundaries, integration patterns, data flow
- **Integration Problems**: API design, synchronization, compatibility
- **Security Concerns**: Vulnerabilities, authentication, authorization
- **Maintainability**: Code structure, testing, documentation
- **Deployment Challenges**: CI/CD, rollout strategies, monitoring

## Implementation Notes

This command delegates to the `problem-solver-agent` which:
- Analyzes the technical challenge deeply
- Identifies root causes
- Generates multiple solution approaches
- Evaluates feasibility and trade-offs
- Provides detailed implementation guidance
- Saves comprehensive problem-solving report
