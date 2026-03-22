---
name: generate-api-docs
description: Generate comprehensive API documentation from code
delegated_to: api-documentation-generator
---

# Command: /generate-api-docs

Generate comprehensive API documentation from codebase with endpoints, parameters, responses, and code examples.

## Usage

```bash
/generate-api-docs <directory|file> [flags]
```

## Arguments

- `<directory|file>`: Directory containing API controllers/routes, or specific API file
  - Examples: `src/Controllers`, `api/routes`, `Services/WebAPI/UserController.cs`

## Flags

- `--format=<markdown|confluence>`: Output format (default: `markdown`)
- `--publish`: Auto-publish to Confluence (requires Confluence MCP)
- `--async`: Run in background
- `--wait`: Wait for completion (default)
- `--include-internal`: Include internal/private endpoints (default: `false`)
- `--include-examples`: Include code examples (default: `true`)
- `--group-by=<controller|tag|path>`: Group endpoints by (default: `controller`)

## Examples

### Basic Usage
```bash
# Generate API docs for controllers directory
/generate-api-docs src/Controllers

# Generate for specific file
/generate-api-docs src/Controllers/UserController.cs
```

### With Formatting
```bash
# Generate Confluence-formatted docs
/generate-api-docs api/routes --format=confluence

# Generate and auto-publish to Confluence
/generate-api-docs src/API --format=confluence --publish
```

### Background Execution
```bash
# Large API - run in background
/generate-api-docs Services/API --async
```

### Advanced Options
```bash
# Include internal endpoints
/generate-api-docs src/Controllers --include-internal

# Group by functional area (tag)
/generate-api-docs src/API --group-by=tag

# Minimal docs without examples
/generate-api-docs api/routes --include-examples=false
```

## Output

Documentation saved to: `output/documentation/<api-name>-api-docs-<timestamp>.md`

**Sections**:
- API Overview (base URL, version, auth)
- Endpoints (grouped by controller/tag/path)
- Authentication guide
- Common parameters
- Response codes
- Error handling
- Code examples (cURL, C#, JavaScript)

## Execution Time

- Small API (10-20 endpoints): 20-30 minutes
- Medium API (20-50 endpoints): 30-50 minutes
- Large API (50+ endpoints): 50-90 minutes

Use `--async` for large APIs.

## Requirements

- **MCP**: None (Confluence optional for `--publish`)
- **Tools**: Bash, Glob, Grep, Read, Write

## Supported Frameworks

- ASP.NET WebAPI, MVC, WebForms
- Express.js, Node.js
- Flask, FastAPI
- Spring Boot
- Generic REST APIs

## Troubleshooting

### No API Files Found
```
Error: "No API files found in directory"
Solution: Verify path, check file naming (*Controller.cs, routes/*.js)
```

### Poor Documentation Quality
```
Issue: Generated docs lack descriptions
Solution: Add XML comments to controllers and methods
```

### Confluence Publish Fails
```
Error: "Confluence MCP unavailable"
Solution: Configure Confluence MCP or remove --publish flag
```

## Related Commands

- `/generate-architecture-doc` - For system architecture documentation
- `/generate-runbook` - For operational documentation
- `/generate-release-notes` - For release change documentation

---

**Delegates To**: api-documentation-generator agent
**Command Version**: 2.0.0
**Status**: Production Ready
