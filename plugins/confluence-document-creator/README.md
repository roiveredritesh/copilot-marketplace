# Confluence Document Creator Plugin

Automated technical documentation generation for Confluence - API docs, architecture docs, runbooks, and release notes.

## Overview

The Confluence Document Creator plugin automatically generates production-quality technical documentation by analyzing codebases, git history, and configuration files. It produces Confluence-ready or Markdown documentation that stays synchronized with your code.

## Features

### API Documentation
- Automatic endpoint discovery from controllers/routes
- Parameter and response schema extraction
- Authentication and authorization documentation
- Code examples in multiple languages (cURL, C#, JavaScript)
- Error response documentation
- Request/response model analysis
- Validation rule extraction

### Architecture Documentation
- System context diagrams (Mermaid)
- Component dependency mapping
- Layer architecture analysis
- Data architecture and schema extraction
- External integration documentation
- Design decision records
- Technology stack documentation

### Operational Runbooks
- Deployment procedure documentation
- Configuration management guides
- Health check and monitoring setup
- Troubleshooting guides
- Backup and restore procedures
- Incident response procedures
- Rollback procedures

### Release Notes
- Git history analysis
- Conventional Commits parsing
- Breaking change detection
- Migration guide generation
- Categorized changes (features, fixes, improvements)
- Upgrade instructions
- Contributor acknowledgment

## Installation

Already installed in: `marketplace/plugins/confluence-document-creator/`

## Quick Start

### Generate API Documentation
```bash
# Generate markdown API docs
/generate-api-docs src/Controllers

# Generate and publish to Confluence
/generate-api-docs api/routes --format=confluence --publish

# Background generation
/generate-api-docs Services/API --async
```

### Generate Architecture Documentation
```bash
# Generate architecture docs
/generate-architecture-doc .

# Comprehensive analysis with diagrams
/generate-architecture-doc src --depth=comprehensive

# Publish to Confluence
/generate-architecture-doc . --format=confluence --publish
```

### Generate Operational Runbook
```bash
# Generate runbook for service
/generate-runbook UserService

# Publish to Confluence
/generate-runbook OrderService --format=confluence --publish
```

### Generate Release Notes
```bash
# Generate release notes for version
/generate-release-notes 2.0.0

# Specify git range
/generate-release-notes v3.0.0 --from=v2.5.0 --to=HEAD

# Publish to Confluence
/generate-release-notes 1.5.0 --format=confluence --publish
```

## Components

### Agents

#### API Documentation Generator
- **File**: `agents/api-documentation-generator.md`
- **Purpose**: Generate comprehensive API documentation from code
- **Output**: API reference with endpoints, parameters, examples
- **Time**: 30-60 minutes

#### Architecture Doc Generator
- **File**: `agents/architecture-doc-generator.md`
- **Purpose**: Create architecture documentation with diagrams
- **Output**: Architecture overview with Mermaid diagrams
- **Time**: 45-75 minutes
- **Sequential Thinking**: Enabled

#### Runbook Generator
- **File**: `agents/runbook-generator.md`
- **Purpose**: Generate operational runbooks
- **Output**: Deployment, troubleshooting, monitoring guides
- **Time**: 30-45 minutes

#### Release Notes Generator
- **File**: `agents/release-notes-generator.md`
- **Purpose**: Create release notes from git history
- **Output**: Categorized changes with upgrade instructions
- **Time**: 20-35 minutes

### Commands

#### /generate-api-docs
- **Usage**: `/generate-api-docs <directory|file> [--format=confluence|markdown] [--publish]`
- **Flags**: `--format`, `--publish`, `--async`, `--wait`
- **Delegates To**: api-documentation-generator

#### /generate-architecture-doc
- **Usage**: `/generate-architecture-doc <directory> [--format=confluence|markdown] [--publish]`
- **Flags**: `--format`, `--publish`, `--async`, `--wait`, `--depth`
- **Delegates To**: architecture-doc-generator

#### /generate-runbook
- **Usage**: `/generate-runbook <service-name|directory> [--format=confluence|markdown] [--publish]`
- **Flags**: `--format`, `--publish`, `--async`, `--wait`
- **Delegates To**: runbook-generator

#### /generate-release-notes
- **Usage**: `/generate-release-notes <version> [--from=tag|commit] [--to=tag|commit] [--format=confluence|markdown] [--publish]`
- **Flags**: `--from`, `--to`, `--format`, `--publish`, `--async`, `--wait`
- **Delegates To**: release-notes-generator

### Skills

#### Confluence Documentation Templates
- **File**: `skills/confluence-documentation-templates.md`
- **Purpose**: Standard templates and formatting for Confluence
- **Used By**: All agents

#### Technical Writing Guide
- **File**: `skills/technical-writing-guide.md`
- **Purpose**: Best practices for clear technical writing
- **Used By**: All agents

## Output Structure

```
marketplace/output/documentation/
├── <api-name>-api-docs-<timestamp>.md
├── <project-name>-architecture-<timestamp>.md
├── <service-name>-runbook-<timestamp>.md
├── <version>-release-notes-<timestamp>.md
└── ...
```

## Typical Generation Time

### API Documentation
- Small API (10-20 endpoints): 20-30 minutes
- Medium API (20-50 endpoints): 30-50 minutes
- Large API (50+ endpoints): 50-90 minutes

### Architecture Documentation
- Small project: 30-45 minutes
- Medium project: 45-65 minutes
- Large/complex project: 65-90 minutes

### Runbooks
- Simple service: 20-30 minutes
- Standard service: 30-45 minutes
- Complex service: 45-60 minutes

### Release Notes
- Small release (10-20 commits): 15-20 minutes
- Medium release (20-50 commits): 20-30 minutes
- Large release (50+ commits): 30-45 minutes

**Recommendation**: Use `--async` for large documentation tasks.

## MCP Requirements

### Confluence (Optional)
Required only for `--publish` flag to auto-publish to Confluence.

```json
{
  "confluence": {
    "command": "confluence-mcp-server",
    "args": ["--space", "DEV"],
    "env": {
      "CONFLUENCE_URL": "https://your-instance.atlassian.net",
      "CONFLUENCE_USERNAME": "your-email",
      "CONFLUENCE_API_TOKEN": "your-api-token"
    }
  }
}
```

Without Confluence MCP, all documentation is generated locally in Markdown format.

## Supported Frameworks

### API Frameworks
- ASP.NET WebAPI (C#)
- ASP.NET MVC/WebForms
- Express.js (JavaScript/TypeScript)
- Flask, FastAPI (Python)
- Spring Boot (Java)

### Documentation Formats
- Markdown (default)
- Confluence markup
- Mermaid diagrams (for architecture)

### Version Control
- Git (required for release notes)

## Common Use Cases

### Onboarding New Developers
```bash
/generate-architecture-doc . --depth=comprehensive
/generate-api-docs src/Controllers
/generate-runbook UserService
```

### Preparing for Release
```bash
/generate-release-notes 2.0.0 --from=v1.5.0
/generate-api-docs src/API --format=confluence --publish
```

### Production Handoff
```bash
/generate-runbook OrderService --publish
/generate-architecture-doc . --format=confluence --publish
```

### API Documentation Updates
```bash
/generate-api-docs src/Controllers --format=confluence --publish
```

## Configuration

### Optional Settings (`.claude/settings.local.json`)
```json
{
  "confluence-document-creator": {
    "default_format": "markdown",
    "confluence_space": "DEV",
    "confluence_parent_page": "Documentation",
    "include_diagrams": true,
    "include_examples": true
  }
}
```

## FAQ

**Q: Can I generate docs without Confluence MCP?**
A: Yes, Markdown output works without any MCP.

**Q: How accurate is the generated documentation?**
A: Very high - all information is extracted from actual code.

**Q: Can I edit the generated documentation?**
A: Yes, output is Markdown or Confluence markup you can edit.

**Q: Will it work with my API framework?**
A: Supports ASP.NET, Express, Flask, FastAPI, Spring Boot, and generic REST APIs.

**Q: How do I update documentation after code changes?**
A: Re-run the same command to regenerate updated documentation.

**Q: Can I customize the output format?**
A: Yes, templates in `skills/` can be customized.

**Q: Does it support multi-language code examples?**
A: Yes, API docs include cURL, C#, and JavaScript examples.

## Integration with Other Plugins

- **Analysis Toolkit**: Use for code analysis before documentation
- **Review Suite**: Review API changes before documenting
- **Architecture Advisor**: Cross-reference with architecture designs

## Best Practices

1. **Keep Commits Clean**: Use Conventional Commits for better release notes
2. **Add XML Comments**: Improves API documentation quality
3. **Document Breaking Changes**: Use BREAKING CHANGE: in commit messages
4. **Update Regularly**: Re-generate docs after significant changes
5. **Review Before Publishing**: Check generated docs before Confluence publish
6. **Use --async for Large Projects**: Background generation for large codebases

## Troubleshooting

### No Files Found
```
Issue: "No API files found"
Solution: Verify directory path, check file naming conventions
```

### Poor Documentation Quality
```
Issue: Generated docs lack descriptions
Solution: Add XML comments to code, improve commit messages
```

### Confluence Publish Fails
```
Issue: Cannot publish to Confluence
Solution: Verify Confluence MCP configuration, check credentials
```

## Plugin Status

- **Version**: 2.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-01-16
- **Tasks Covered**: API documentation, architecture docs, runbooks, release notes
- **MCP Servers**: confluence (optional)

## What's New in v2.0.0

- Initial production release
- 4 comprehensive agents with 6-phase processes
- Confluence and Markdown output support
- Sequential Thinking for complex analyses
- Conventional Commits support
- Breaking change detection
- Mermaid diagram generation
- Multi-language code examples
- Comprehensive error handling

## Support

For issues or suggestions:
1. Review this README
2. Check agent documentation in `agents/`
3. Review skills in `skills/`
4. Consult troubleshooting section

---

**Part of the Claude Code Marketplace**
Confluence Document Creator Plugin v2.0.0 (2026-01-16)
