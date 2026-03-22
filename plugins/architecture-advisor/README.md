# Architecture Advisor Plugin

**Version**: 2.0.0
**Status**: Production
**Last Updated**: 2026-01-15

System architecture analysis, design patterns, and architecture design for scalable applications.

## What's New in v2.0.0

- **Framework Expertise**: Integrated .NET Framework migration strategies and WebForms modernization patterns
- **Database Schema Analysis**: Direct access to schema design best practices
- **Enhanced Architecture Templates**: Improved system design methodologies
- **Conditional Sequential Thinking**: Smarter reasoning for complex architecture decisions
- **Shared Skills Integration**: Centralized knowledge base for better consistency
- **Modernization Guidance**: Built-in patterns for legacy system upgrades

## Overview

The Architecture Advisor provides guidance on system design, architecture analysis, and design patterns. Three specialized agents help evaluate existing architectures, recommend patterns, and design new systems.

## Features

### Architecture Analysis
- Analyze existing system structure and organization
- Identify architectural patterns in use
- Evaluate SOLID principles compliance
- Detect anti-patterns and issues
- Assess architecture quality
- Provide improvement recommendations

### Design Pattern Guidance
- Recommend appropriate design patterns for problems
- Analyze pattern trade-offs
- Provide implementation examples
- Suggest pattern combinations
- Show code examples (before/after)
- Assess pattern fit for use case

### System Design
- Design architecture for new applications
- Analyze functional and non-functional requirements
- Define layering and components
- Plan data models and flows
- Design security architecture
- Plan scalability and resilience

## Installation

Already installed: `marketplace/plugins/architecture-advisor/`

## Quick Start

### Analyze Existing Architecture
```bash
/analyze-architecture src/ --wait
/analyze-architecture . --async
```

### Get Design Pattern Recommendations
```bash
/suggest-patterns "Need flexible authentication with multiple providers" --wait
/suggest-patterns "How to decouple UI from business logic?" --async
```

### Design New System
```bash
/design-system requirements.md --wait
/design-system project-spec.txt --async
```

## Components

### Agents

#### Architecture Analyzer
- **File**: `agents/architecture-analyzer.md`
- **Purpose**: Analyze existing system architecture
- **Task**: Task #7 (Understand overall architecture and system design)

#### Design Pattern Advisor
- **File**: `agents/design-pattern-advisor.md`
- **Purpose**: Recommend design patterns for problems
- **Task**: Task #8 (Design pattern guidance and recommendations)

#### System Designer
- **File**: `agents/system-designer.md`
- **Purpose**: Design architecture for new systems
- **Task**: Task #9 (Design system architecture for new applications)

### Commands

#### /analyze-architecture
- **Usage**: `/analyze-architecture <directory> [--async|--wait] [--report=full|summary]`
- **Delegates To**: architecture-analyzer agent
- **Purpose**: Analyze existing system architecture

#### /suggest-patterns
- **Usage**: `/suggest-patterns <problem> [--async|--wait] [--report=full|summary]`
- **Delegates To**: design-pattern-advisor agent
- **Purpose**: Recommend design patterns

#### /design-system
- **Usage**: `/design-system <requirements-file> [--async|--wait] [--report=full|summary]`
- **Delegates To**: system-designer agent
- **Purpose**: Design new system architecture

### Skills

#### Architecture Design
- **File**: `skills/architecture-design.md`
- **Coverage**: Principles, patterns, layering, data design, scalability, resilience, security, trade-offs, checklist

## Output Structure

```
marketplace/output/reviews/
├── <project>-architecture-analysis.md      # Architecture analysis
├── <problem>-pattern-recommendation.md     # Pattern recommendations
├── <system>-system-design.md              # System design
└── ... (summary versions)
```

## Typical Analysis Time

### Architecture Analysis
- Small project: 8-12 minutes
- Medium project: 12-20 minutes
- Large project: 20-30 minutes

### Pattern Recommendations
- Simple problem: 5-8 minutes
- Complex problem: 8-15 minutes

### System Design
- Simple system: 10-15 minutes
- Medium system: 15-25 minutes
- Complex system: 25-40 minutes

**Recommendation**: Use `--async` for complex analysis.

## Supported Patterns

### Structural Patterns
- Adapter, Bridge, Composite, Decorator, Facade, Proxy, Flyweight

### Behavioral Patterns
- Observer, Strategy, State, Command, Template Method, Iterator, Visitor, Mediator, Chain of Responsibility, Interpreter

### Creational Patterns
- Factory, Abstract Factory, Builder, Singleton, Prototype

### Architectural Patterns
- Layered, Microservices, Event-Driven, CQRS, Pipe & Filter, Service Locator, Dependency Injection

## Architecture Quality Assessment

Evaluates:
- **Layering**: Clear separation of concerns
- **SOLID Principles**: All 5 principles assessed
- **Scalability**: Horizontal and vertical scaling potential
- **Testability**: Component testability
- **Maintainability**: Code clarity and organization
- **Security**: Authentication, authorization, data protection
- **Performance**: Efficiency and optimization

## Design Principles

The plugin teaches and applies:
- **Separation of Concerns**: Distinct responsibilities per layer
- **Single Responsibility**: One reason to change
- **SOLID Principles**: 5 key design principles
- **KISS**: Keep It Simple
- **DRY**: Don't Repeat Yourself
- **Extensibility**: Open for extension, closed for modification

## Usage Examples

### Improve Existing Architecture
```bash
# Understand current architecture
/analyze-architecture src/ --wait
# Review issues and recommendations
# Address critical items in priority order
```

### Solve Design Challenges
```bash
# Get pattern recommendations
/suggest-patterns "Decouple components for independent testing" --wait
# Review recommended patterns
# Implement recommended approach
```

### Design New Feature
```bash
# Design new system
/design-system feature-requirements.md --wait
# Review architecture design
# Follow implementation roadmap
```

### Team Learning
```bash
# Analyze team's codebase
/analyze-architecture . --wait
# Share report with team
# Discuss improvements collaboratively
```

## MCP Requirements

No MCP servers required - all analysis is local.

## Integration with Other Plugins

- **Review Suite**: Use PR review to catch architectural issues
- **Analysis Toolkit**: Investigate architectural problems found
- **Optimization Engine**: Optimize architectural performance
- **Development Suite**: Generate code following designed architecture

## Related Commands

- `/task-status <task-id>` - Check analysis progress
- `/analyze-architecture` - Analyze existing architecture
- `/suggest-patterns` - Get pattern recommendations
- `/design-system` - Design new system

## Best Practices

1. **Analyze Regularly**: Review architecture as codebase grows
2. **Document Decisions**: Record why architectural choices were made
3. **Team Alignment**: Involve team in architectural discussions
4. **Incremental Improvement**: Address critical issues first
5. **Pattern Consistency**: Apply selected patterns consistently
6. **Review for Compliance**: Ensure code follows architecture

## FAQ

**Q: What languages are supported?**
A: C#, JavaScript, Python, Java, and others - auto-detected

**Q: Will it modify my code?**
A: No, all analysis is read-only

**Q: How detailed are recommendations?**
A: Very detailed with architecture diagrams, components, flows

**Q: Can I redesign after initial analysis?**
A: Yes, analyze multiple times as design evolves

**Q: What if I disagree with recommendations?**
A: They're guidance - your team decides what to implement

**Q: Where are reports saved?**
A: `marketplace/output/reviews/`

## Plugin Status

- **Version**: 1.0.0
- **Status**: Production Ready
- **Last Updated**: 2025-10-30
- **Tasks Covered**: Task #7, #8, #9
- **MCP Servers**: None required

## Support

For issues or suggestions:
1. Check this README
2. Review FAQ section
3. Review command documentation
4. Consult skill documentation

---

**Part of the Claude Code Marketplace**
Architecture Advisor Plugin v1.0.0 (2025-10-30)
