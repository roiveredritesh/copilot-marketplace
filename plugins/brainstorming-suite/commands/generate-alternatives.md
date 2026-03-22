---
allowed-tools: [Task, Read, Write, Grep, Glob, Bash]
argument-hint: <requirement> [--async|--wait] [--language=csharp|python|javascript] [--depth=shallow|medium|deep]
description: Generate alternative implementations with trade-offs
---

# Command: /generate-alternatives

Generates multiple alternative implementations for requirements with detailed trade-off analysis, performance comparisons, and recommendations for different use cases.

## Usage

```
/generate-alternatives <requirement> [--async|--wait] [--language=csharp|python|javascript] [--depth=shallow|medium|deep]
```

## Arguments

### Required Arguments

- **requirement**: The feature or functionality to implement
  - `/generate-alternatives "user authentication system"`
  - `/generate-alternatives "data caching mechanism"`
  - `/generate-alternatives "file upload handling"`
  - `/generate-alternatives "real-time notification delivery"`

### Optional Flags

- **--async**: Execute in background (recommended for comprehensive analysis)
- **--wait**: Execute synchronously (default, waits for completion)
- **--language**: Target programming language
  - `csharp`: C# / .NET (default)
  - `python`: Python
  - `javascript`: JavaScript/TypeScript
- **--depth**: Code detail level
  - `shallow`: Pseudo-code and sketches, 5-10 minutes
  - `medium`: Working code examples (default, 10-20 minutes)
  - `deep`: Production-ready code with tests and comments, 20-30 minutes

## Examples

```bash
# Generate auth implementations in C#
/generate-alternatives "user authentication system"

# Python caching implementations with deep analysis
/generate-alternatives "data caching mechanism" --language=python --depth=deep --async

# Quick file upload sketches in JavaScript
/generate-alternatives "file upload handling" --language=javascript --depth=shallow

# Production-ready notification examples
/generate-alternatives "real-time notification delivery" --depth=deep --async
```

## How It Works

The agent will:

1. **Understand Requirement**: Analyze what needs to be built
2. **Generate Approaches**: Create 4-6 distinct implementation strategies
3. **Code Implementation**: For each approach, provide working code
4. **Analyze Trade-offs**:
   - Performance characteristics
   - Code complexity
   - Maintenance burden
   - Scalability potential
   - Security implications
   - Testing complexity
5. **Provide Recommendations**: Best fit for different scenarios
6. **Create Comparison**: Side-by-side comparison with metrics

## Output Locations

- Alternative implementations: `marketplace/output/brainstorming/<requirement>-alternatives.md`
- Code examples: `marketplace/output/brainstorming/<requirement>-code.md`
- Comparison analysis: `marketplace/output/brainstorming/<requirement>-comparison.md`

## Typical Analysis Time

- Shallow: 5-10 minutes
- Medium: 10-20 minutes (default)
- Deep: 20-30 minutes (production-ready code)

**Recommendation**: Use `--async --depth=deep` for critical features to get thoroughly tested implementations.

## Output Format

The alternatives document includes:

- **Requirement Summary**: What needs to be implemented
- **Alternative Approaches** (4-6 options):
  - Approach name and description
  - Architecture overview
  - Key technology choices
  - Code implementation (pseudo-code to full code depending on depth)
  - Pros and cons
  - Complexity rating (1-5)

- **Code Examples** (provided for each approach):
  - Core implementation
  - Usage examples
  - Error handling
  - Tests (if deep analysis)
  - Comments and documentation

- **Trade-offs Analysis Table**:
  - Performance (Speed, Memory, Throughput)
  - Complexity (Lines of Code, Time to Implement, Maintenance)
  - Features (Extensibility, Flexibility, Customization)
  - Reliability (Error handling, Edge cases)
  - Security (Vulnerabilities, Protection mechanisms)
  - Scalability (Single server, Distributed, Cloud-ready)

- **Performance Comparison** (if applicable):
  - Benchmarking results or estimates
  - Memory usage profiles
  - Throughput comparisons
  - Latency characteristics

- **Use Case Recommendations**:
  - When to use Approach A
  - When to use Approach B
  - Specific scenario recommendations
  - Team skill requirements

- **Recommendation**:
  - Best all-around approach
  - Best for performance
  - Best for maintainability
  - Best for learning
  - Best for rapid development

- **Migration Path**:
  - How to start simple and evolve
  - Refactoring strategies
  - Upgrade paths between approaches

- **Testing Strategies**:
  - Unit test approach for each implementation
  - Integration test considerations
  - Edge cases to test
  - Performance test approach (if applicable)

- **Production Considerations**:
  - Deployment aspects
  - Configuration management
  - Monitoring and observability
  - Security hardening
  - Performance tuning

- **Common Pitfalls**:
  - Implementation mistakes to avoid
  - Performance anti-patterns
  - Security vulnerabilities to watch for
  - Scaling challenges

- **Resources & References**:
  - Documentation links
  - Pattern references
  - Community examples
  - Tools and libraries

## Supported Languages

- **C# / .NET Framework**: Primary support with ASP.NET WebForms examples
- **Python**: Full language support
- **JavaScript/TypeScript**: Client and server-side implementations
- Other languages available on request

## Implementation Categories

- **Authentication & Authorization**
- **Data Persistence & Caching**
- **API Design & Integration**
- **Real-time Communication**
- **File Handling**
- **State Management**
- **Error Handling & Logging**
- **Testing Approaches**
- **Performance Optimization**
- **Security Implementation**
- And more based on requirement

## Implementation Notes

This command delegates to the `code-alternatives-agent` which:
- Analyzes the requirement comprehensively
- Generates creative implementation approaches
- Provides working code examples
- Evaluates trade-offs thoroughly
- Recommends best fit for different scenarios
- Saves comprehensive alternatives document with code examples

**Depth Selection Guide**:
- **Shallow**: When you want quick ideas and concepts
- **Medium**: When you want working examples you can use immediately
- **Deep**: When you need production-ready code with comprehensive tests and documentation
