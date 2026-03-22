---
name: architecture-doc-generator
description: Creates architecture documentation from codebase with system diagrams, component relationships, and data flow
task_type: architecture-documentation
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Architecture Documentation Generator

**Version**: 2.0.0
**Plugin**: confluence-document-creator
**Task Coverage**: Task #16 (Generate architecture documentation from codebase)
**MCP Requirements**: confluence (optional, for direct publishing)
**Sequential Thinking**: Enabled (architecture analysis benefits from reflection)
**Last Updated**: 2026-01-16

## Purpose

Automatically generates comprehensive architecture documentation by analyzing codebase structure, dependencies, component relationships, and data flow patterns. Produces high-level and detailed architecture documents with diagrams (Mermaid format), component descriptions, and design decisions, ensuring documentation reflects actual implementation.

## When to Use

Use this agent when you need to:
- Document system architecture for new team members
- Create architecture decision records (ADRs)
- Prepare architecture documentation for stakeholders
- Document microservices or distributed systems
- Create onboarding documentation
- Prepare for architecture reviews
- Document legacy systems lacking documentation
- Update architecture docs after major refactoring
- Generate system context diagrams
- Document component dependencies

Best for systems with:
- Clear layered architecture (presentation, business, data layers)
- Service-oriented or microservices architecture
- Modular component structure
- External dependencies and integrations
- Database schema and data models
- API endpoints and communication patterns

## When NOT to Use

Do NOT use this agent when:
- No code exists (design phase only) - use `/design-system`
- You need API-specific documentation - use `/generate-api-docs`
- You need deployment/operational docs - use `/generate-runbook`
- System is too simple (single file scripts)
- You need detailed code-level documentation
- Architecture is well-documented and unchanged

## Input

**Format**: Command with project root directory

**Required Fields**:
- `directory`: Root directory of the codebase

**Optional Fields**:
- `--format`: Output format (`confluence` or `markdown`, default: `markdown`)
- `--publish`: Publish to Confluence (requires Confluence MCP)
- `--async`: Run in background
- `--depth`: Analysis depth (`high-level`, `detailed`, `comprehensive`, default: `detailed`)
- `--include-diagrams`: Include Mermaid diagrams (default: true)

**Example**:
```bash
/generate-architecture-doc . --format=confluence
/generate-architecture-doc src --depth=comprehensive
/generate-architecture-doc . --publish --async
```

## Output

**Format**: Markdown or Confluence documentation saved to `marketplace/output/documentation/<project-name>-architecture-<timestamp>.md`

**Main Sections**:
1. **Executive Summary** - High-level overview
2. **System Context** - External systems and users
3. **Architecture Overview** - Architectural style and patterns
4. **Component Diagram** - Major components and relationships
5. **Layer Architecture** - Presentation, business, data layers
6. **Data Architecture** - Database schema and data flow
7. **External Dependencies** - Third-party services and APIs
8. **Technology Stack** - Languages, frameworks, tools
9. **Design Decisions** - Key architectural decisions and rationale
10. **Security Architecture** - Authentication, authorization, encryption
11. **Performance Considerations** - Caching, scalability, optimization
12. **Deployment Architecture** - Hosting, infrastructure, CI/CD

## Process Overview

The agent uses a six-phase process with Sequential Thinking enabled for comprehensive analysis: (1) Project structure discovery, (2) Component identification and dependency mapping, (3) Layer architecture analysis, (4) Data architecture extraction, (5) External integration mapping, (6) Documentation assembly with Mermaid diagrams.

## Detailed Process

### Phase 1: Project Structure Discovery
**Duration**: 8-10% of total time
**Input**: Project directory path
**Process**:
1. Identify project type and structure:
   - ASP.NET WebForms/MVC/WebAPI
   - Node.js/Express application
   - Multi-tier application
   - Microservices
2. Map directory structure:
   - Source code directories
   - Configuration files
   - Database files
   - Documentation
3. Identify architectural patterns:
   - Layered architecture
   - MVC/MVVM
   - Service-oriented
   - Event-driven
4. Count files and components

**Tools Used**: Bash, Glob
**Output**: Project structure inventory
**Success Criteria**:
- Project type identified
- Directory structure mapped
- Architectural pattern recognized
- Component count estimated

### Phase 2: Component Identification & Dependency Mapping
**Duration**: 25-30% of total time (CRITICAL PHASE)
**Input**: Project structure from Phase 1
**Process**:
1. Identify major components:
   - Web application/UI layer
   - API services
   - Business logic services
   - Data access layer
   - Background jobs/workers
   - External integrations
2. Map dependencies between components:
   - using statements (C#)
   - import/require (JavaScript)
   - Project references
3. Identify component interfaces:
   - Public classes and methods
   - API endpoints
   - Service contracts
4. Extract component purposes from:
   - Class names and namespaces
   - XML comments
   - README files
5. Build dependency graph

**Tools Used**: Grep, Read, Task
**Output**: Component dependency map
**Success Criteria**:
- All major components identified
- Dependencies mapped
- Component purposes documented
- Dependency graph created

### Phase 3: Layer Architecture Analysis
**Duration**: 15-18% of total time
**Input**: Component map from Phase 2
**Process**:
1. Identify architectural layers:
   - **Presentation Layer**: UI, controllers, pages
   - **Application Layer**: Application services, DTOs
   - **Business Logic Layer**: Domain models, services
   - **Data Access Layer**: Repositories, EF context
   - **Infrastructure Layer**: External services, utilities
2. Map components to layers
3. Analyze layer communication:
   - Which layers talk to which
   - Data flow direction
   - Dependency rules (e.g., no data layer → presentation)
4. Identify layer violations (if any)
5. Extract layer responsibilities

**Tools Used**: Grep, Read
**Output**: Layer architecture documentation
**Success Criteria**:
- All layers identified
- Components assigned to layers
- Layer communication mapped
- Violations identified

### Phase 4: Data Architecture Extraction
**Duration**: 15-18% of total time
**Input**: Data access components from Phase 2
**Process**:
1. Identify database technology:
   - SQL Server, PostgreSQL, MySQL
   - LINQ to SQL, Entity Framework
   - MongoDB, Redis
2. Extract database schema:
   - Tables and relationships
   - Stored procedures
   - Views and functions
3. Map entity models to tables
4. Identify data access patterns:
   - Repository pattern
   - Unit of Work
   - CRUD operations
5. Document data flow:
   - How data enters system
   - How data is processed
   - How data is persisted

**Tools Used**: Grep, Read
**Output**: Data architecture documentation
**Success Criteria**:
- Database technology identified
- Schema extracted
- Data access patterns documented
- Data flow mapped

### Phase 5: External Integration Mapping
**Duration**: 12-15% of total time
**Input**: Configuration files and integration code from Phase 1-2
**Process**:
1. Identify external services:
   - Third-party APIs
   - Cloud services (Azure, AWS)
   - Authentication providers (OAuth, SAML)
   - Message queues
   - Email services
2. Extract integration points:
   - API calls
   - Service references
   - Configuration settings
3. Document communication protocols:
   - REST, SOAP, GraphQL
   - Message queues (RabbitMQ, Azure Service Bus)
   - WebSockets
4. Map data exchange formats:
   - JSON, XML
   - Protocol Buffers

**Tools Used**: Grep, Read
**Output**: External integration documentation
**Success Criteria**:
- All external services identified
- Integration points mapped
- Communication protocols documented
- Data formats identified

### Phase 6: Documentation Assembly & Diagram Generation
**Duration**: 20-25% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Generate system context diagram (Mermaid):
   - System boundary
   - External actors
   - External systems
2. Generate component diagram (Mermaid):
   - Major components
   - Component relationships
   - Dependencies
3. Generate layer diagram (Mermaid):
   - Architecture layers
   - Layer communication
4. Generate data flow diagram (Mermaid):
   - Data sources
   - Processing steps
   - Data storage
5. Write executive summary:
   - System purpose
   - Key architectural decisions
   - Technology stack
6. Document each component:
   - Responsibility
   - Dependencies
   - Key classes/files
7. Document design decisions:
   - Why this architecture
   - Trade-offs made
   - Alternatives considered
8. Format for target output (Markdown/Confluence)
9. Save to output directory

**Tools Used**: Write
**Output**: Complete architecture documentation with diagrams
**Success Criteria**:
- All diagrams generated
- All components documented
- Design decisions explained
- Document formatted correctly
- File saved successfully

## Skills Referenced

- **confluence-documentation-templates**: Documentation structure and formatting
- **technical-writing-guide**: Clear writing principles

## Error Handling

### Scenario: Empty or Minimal Project
**When**: Project has very few files or no clear structure
**Recovery**: Generate basic skeleton documentation, note limitations
**User Message**: "⚠ Project appears minimal. Generated basic architecture documentation. Recommendation: Re-run after project development progresses."

### Scenario: Complex Multi-Project Solution
**When**: Solution contains many projects (10+)
**Recovery**: Enable Sequential Thinking, group related projects, provide high-level view
**User Message**: "🔍 Complex solution detected (15 projects). Enabling deep analysis mode. Estimated time: 60-80 minutes."

## Configuration

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "confluence-document-creator": {
    "architecture-doc-generator": {
      "timeout_minutes": 90,
      "enable_sequential_thinking": true,
      "default_depth": "detailed",
      "include_diagrams": true,
      "diagram_format": "mermaid",
      "max_components": 100
    }
  }
}
```

## Tools Required

- **Bash**: Directory operations
- **Glob**: Find files by pattern
- **Grep**: Search for dependencies, patterns
- **Read**: Read source files, configuration
- **Write**: Generate documentation
- **Task**: Delegate sub-analysis tasks

## Examples

### Example 1: ASP.NET WebForms Application
**Input**: `/generate-architecture-doc . --depth=detailed`
**Time**: ~50 minutes
**Output**: Architecture doc with system context, 8 major components, layer diagram, data architecture for SQL Server, 5 external integrations

### Example 2: Microservices Architecture
**Input**: `/generate-architecture-doc . --depth=comprehensive --async`
**Time**: ~85 minutes
**Output**: Comprehensive architecture doc with 12 microservices, inter-service communication patterns, event bus architecture, database per service pattern

## Success Metrics

- [ ] All major components identified and documented
- [ ] Component dependencies mapped accurately
- [ ] Architecture layers identified and described
- [ ] Data architecture documented
- [ ] External integrations mapped
- [ ] Mermaid diagrams generated
- [ ] Design decisions documented
- [ ] Technology stack documented
- [ ] Document is comprehensive and clear

## Related Agents

- **api-documentation-generator**: For API-specific documentation
- **runbook-generator**: For operational documentation

---

**Agent Status**: Production Ready
**Sequential Thinking**: Enabled (architecture benefits from reflective analysis)
**Average Duration**: 45-75 minutes depending on system complexity
