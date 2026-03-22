# Changelog - Confluence Document Creator Plugin

All notable changes to this plugin will be documented in this file.

## [2.0.0] - 2026-01-16

### Added
- Initial production release
- API Documentation Generator agent with comprehensive endpoint analysis
- Architecture Documentation Generator agent with Mermaid diagram support
- Runbook Generator agent for operational documentation
- Release Notes Generator agent with git history analysis
- Confluence and Markdown output format support
- Auto-publish capability with Confluence MCP integration
- 4 commands for documentation generation
- 2 shared skills for documentation best practices
- Sequential Thinking support for complex analyses
- Conventional Commits parsing for release notes
- Breaking change detection and migration guide generation
- Code example generation for API documentation
- Error handling and troubleshooting extraction for runbooks
- Layer architecture analysis for architecture docs

### Technical Details
- **Agents**: 4 (api-documentation-generator, architecture-doc-generator, runbook-generator, release-notes-generator)
- **Commands**: 4 (/generate-api-docs, /generate-architecture-doc, /generate-runbook, /generate-release-notes)
- **Skills**: 2 (confluence-documentation-templates, technical-writing-guide)
- **MCP Servers**: confluence (optional)
- **Tools Used**: Bash, Glob, Grep, Read, Write, Task
- **Output Location**: marketplace/output/documentation/

### Documentation
- Complete agent specifications following v2.0.0 template
- 6-phase processes for all agents
- Error handling scenarios documented
- Configuration options provided
- Comprehensive examples included

### Supported Frameworks
- ASP.NET WebAPI, WebForms, MVC
- Express.js, Node.js
- Flask, FastAPI (Python)
- Spring Boot (Java)
- Generic REST APIs

### Supported Output Formats
- Markdown (default)
- Confluence markup
- Mermaid diagrams for architecture docs

---

**Plugin Status**: Production Ready
**Version**: 2.0.0
**Release Date**: 2026-01-16
**Compatibility**: Claude Code 1.0+
