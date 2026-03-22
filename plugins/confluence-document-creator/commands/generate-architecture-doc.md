---
name: generate-architecture-doc
description: Create architecture documentation from codebase
delegated_to: architecture-doc-generator
---

# Command: /generate-architecture-doc

Create comprehensive architecture documentation with diagrams, component relationships, and design decisions.

## Usage

```bash
/generate-architecture-doc <directory> [flags]
```

## Arguments

- `<directory>`: Root directory of project or codebase
  - Examples: `.`, `src`, `/path/to/project`

## Flags

- `--format=<markdown|confluence>`: Output format (default: `markdown`)
- `--publish`: Auto-publish to Confluence (requires Confluence MCP)
- `--async`: Run in background
- `--wait`: Wait for completion (default)
- `--depth=<high-level|detailed|comprehensive>`: Analysis depth (default: `detailed`)
- `--include-diagrams`: Include Mermaid diagrams (default: `true`)

## Examples

### Basic Usage
```bash
# Generate architecture docs for current project
/generate-architecture-doc .

# Generate for specific directory
/generate-architecture-doc src
```

### With Depth Control
```bash
# High-level overview only
/generate-architecture-doc . --depth=high-level

# Comprehensive deep dive
/generate-architecture-doc src --depth=comprehensive
```

### Publishing
```bash
# Generate and publish to Confluence
/generate-architecture-doc . --format=confluence --publish

# Background generation for large project
/generate-architecture-doc . --async
```

## Output

Documentation saved to: `output/documentation/<project-name>-architecture-<timestamp>.md`

**Sections**:
- Executive Summary
- System Context Diagram (Mermaid)
- Component Diagram (Mermaid)
- Layer Architecture
- Data Architecture
- External Dependencies
- Technology Stack
- Design Decisions
- Security Architecture
- Performance Considerations
- Deployment Architecture

## Execution Time

- Small project: 30-45 minutes
- Medium project: 45-65 minutes
- Large/complex project: 65-90 minutes

Use `--async` for complex projects.

## Requirements

- **MCP**: None (Confluence optional for `--publish`)
- **Tools**: Bash, Glob, Grep, Read, Write, Task
- **Sequential Thinking**: Enabled (for comprehensive analysis)

## Diagram Support

Generates Mermaid diagrams for:
- System context (external systems and users)
- Component relationships (dependencies)
- Layer architecture (presentation, business, data)
- Data flow (data movement through system)

## Troubleshooting

### Minimal Project
```
Issue: "Project appears minimal"
Solution: Wait until project has sufficient structure
```

### Complex Solution
```
Issue: Analysis takes too long
Solution: Use --async flag, or --depth=high-level for overview
```

## Related Commands

- `/generate-api-docs` - For API-specific documentation
- `/generate-runbook` - For operational procedures
- `/design-system` - For architecture design (before implementation)

---

**Delegates To**: architecture-doc-generator agent
**Command Version**: 2.0.0
**Status**: Production Ready
