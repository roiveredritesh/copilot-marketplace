---
allowed-tools: [Task, Read, Write, Grep, Glob, Bash]
argument-hint: <component> [--async|--wait] [--depth=shallow|medium|deep]
description: Explore architectural approaches and design patterns
---

# Command: /brainstorm-architecture

Explores multiple architectural approaches and design patterns for system components with comprehensive trade-off analysis and recommendations.

## Usage

```
/brainstorm-architecture <component> [--async|--wait] [--depth=shallow|medium|deep]
```

## Arguments

### Required Arguments

- **component**: The component or system to design
  - `/brainstorm-architecture "authentication system"`
  - `/brainstorm-architecture "caching layer"`
  - `/brainstorm-architecture "message queue implementation"`
  - `/brainstorm-architecture "data persistence"`

### Optional Flags

- **--async**: Execute in background (recommended for deep architecture work)
- **--wait**: Execute synchronously (default, waits for completion)
- **--depth**: Analysis depth
  - `shallow`: 3-4 architecture options, 5-10 minutes
  - `medium`: 5-6 approaches with detailed analysis (default, 10-15 minutes)
  - `deep`: 7-8 approaches with architecture diagrams and detailed trade-offs, 20-30 minutes

## Examples

```bash
# Explore authentication architectures
/brainstorm-architecture "authentication system"

# In-depth caching architecture exploration
/brainstorm-architecture "caching layer" --async --depth=deep

# Quick message queue options
/brainstorm-architecture "message queue implementation" --depth=shallow

# Medium depth data persistence patterns
/brainstorm-architecture "data persistence" --async
```

## How It Works

The agent will:

1. **Analyze Current Context**: Review existing codebase and architecture
2. **Generate Approaches**: Create 5-8 architectural variations
3. **Design Each Approach**:
   - Architecture diagram
   - Component structure
   - Technology choices
   - Data flow
   - Scalability path
   - Security considerations
4. **Compare Trade-offs**:
   - Performance implications
   - Maintenance complexity
   - Resource requirements
   - Team skill requirements
   - Migration path
   - Cost implications
5. **Recommend Best Fit**: Based on project needs and constraints
6. **Provide Implementation Roadmap**: Step-by-step implementation plan

## Output Locations

- Architecture exploration: `marketplace/output/brainstorming/<component>-architectures.md`
- Comparison matrix: `marketplace/output/brainstorming/<component>-comparison.md`
- Recommended approach: `marketplace/output/brainstorming/<component>-recommendation.md`

## Typical Analysis Time

- Shallow: 5-10 minutes
- Medium: 10-15 minutes (default)
- Deep: 20-30 minutes (comprehensive with diagrams)

**Recommendation**: Use `--async --depth=deep` for critical architecture decisions to get comprehensive analysis without blocking.

## Output Format

The architecture exploration includes:

- **Component Summary**: Context and requirements
- **Architecture Approaches**: 5-8 distinct architectures with descriptions
- **Architecture Comparison Table**:
  - Technology Stack
  - Scalability Rating (1-5)
  - Performance Impact
  - Maintenance Complexity (1-5)
  - Cost (Low/Medium/High)
  - Security Level
  - Team Skill Required
- **Detailed Designs** (for deep analysis):
  - ASCII/text architecture diagrams
  - Component interactions
  - Data flow explanations
  - Technology justification
- **Trade-offs Analysis**:
  - Performance vs Complexity
  - Cost vs Features
  - Scalability vs Maintenance
  - Security vs Usability
- **Recommended Approach**:
  - Why this approach best fits your needs
  - Key advantages
  - Potential risks
  - Mitigation strategies
- **Implementation Roadmap**:
  - Phase 1: Setup and foundation
  - Phase 2: Core functionality
  - Phase 3: Optimization and scaling
  - Timeline estimates
- **Related Architectural Patterns**: How this fits with other components
- **Technology Stack Details**: Specific tool and version recommendations
- **Risk Assessment**: Potential issues and mitigation plans

## Architectural Patterns Covered

- **Layered/N-Tier Architecture**
- **Microservices**
- **Event-Driven Architecture**
- **CQRS (Command Query Responsibility Segregation)**
- **Repository Pattern**
- **Pub/Sub Pattern**
- **Circuit Breaker Pattern**
- **Service Locator Pattern**
- **Factory Pattern**
- **Adapter Pattern**
- And more based on component type

## Implementation Notes

This command delegates to the `architecture-explorer-agent` which:
- Examines existing codebase architecture
- Generates creative architectural approaches
- Evaluates feasibility and fit
- Provides detailed comparative analysis
- Saves comprehensive architecture exploration report
