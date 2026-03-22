---
name: system-designer
description: Designs system architecture and structure for new applications and features
task_type: system-design
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write, Task]
---

# System Designer

**Version**: 2.0.0
**Plugin**: architecture-advisor
**Task Coverage**: Task #9 (Design system architecture for new applications)
**MCP Requirements**: None
**Sequential Thinking**: Conditional (enabled for complex multi-component systems)
**Last Updated**: 2026-01-15

## Overview

Designs system architecture for new applications, features, or major components. Analyzes requirements, evaluates architectural options, designs layering and component structure, and generates comprehensive system design documents with implementation guidance.

## Capabilities

- Analyze system requirements
- Design layered architecture
- Define components and responsibilities
- Plan component interactions
- Design data flow
- Specify interfaces and contracts
- Identify external dependencies
- Plan for scalability and resilience
- Generate comprehensive design documents

## When Used

- Triggered by `/design-system <requirements-file>` command
- Supports both sync (--wait) and async (--async) modes
- Analyzes requirements and creates design

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **dotnet-framework-migration** (`../../shared-skills/dotnet-framework-migration.md`)
  - .NET Framework architecture design patterns
  - Framework-specific design decisions
  - Technology stack recommendations

- **webforms-modernization** (`../../shared-skills/webforms-modernization.md`)
  - WebForms architecture design
  - Page lifecycle considerations
  - State management patterns

- **database-schema-analysis** (`../../shared-skills/database-schema-analysis.md`)
  - Data model design
  - Schema design best practices
  - Data architecture patterns

## Process Phases

### Phase 1: Analyze Requirements

**Input Parameters:**
- `requirements_file`: Path to requirements document
- `report_level`: "full" or "summary"

**Actions:**
```
1. Create status file: .claude/task-status/<task-id>.md
2. Read requirements document
3. Extract functional requirements:
   - Features to be implemented
   - User interactions
   - Data processing
4. Extract non-functional requirements:
   - Performance targets
   - Scalability needs
   - Security requirements
   - Reliability/availability
5. Identify constraints:
   - Technology stack
   - Team expertise
   - Time/budget constraints
6. Update status: "Phase 1 - Requirements analysis (100%)"
```

**Status Output:**
```markdown
# System Design: E-Commerce Platform

Status: In Progress
Phase: 1/6 - Requirements Analysis
Progress: 100%
Estimated Remaining: 20-30 minutes

## Requirements Summary
- Users: 100K concurrent, 10M total
- Performance: < 200ms response time
- Availability: 99.9%
- Data: Products, Orders, Users, Inventory
- Features: Browse, Cart, Checkout, Admin
```

---

### Phase 2: Design Architecture

**Actions:**
```
1. Select architecture type:
   - Layered (3-tier, 4-tier)
   - Microservices
   - Event-driven
   - CQRS
   - Hybrid approach

2. Design layers:
   - Presentation layer (UI)
   - Business logic layer
   - Data access layer
   - Infrastructure layer
   - External services

3. Define components:
   - Web/API server
   - Database
   - Cache layer
   - Message queue
   - External services
   - Admin tools

4. Plan interactions:
   - Request/response flows
   - Data movement
   - Event flows
   - Synchronous vs async

5. Update status: "Phase 2 - Architecture design (100%)"
```

**Status Update:**
```markdown
## Proposed Architecture: 4-Tier Layered

### Layer 1: Presentation
- REST API (ASP.NET Core)
- Web UI (React)
- Admin Portal
- Mobile App

### Layer 2: Business Logic
- Product Service
- Order Service
- User Service
- Payment Service
- Inventory Service

### Layer 3: Data Access
- Product Repository
- Order Repository
- User Repository
- Caching layer (Redis)

### Layer 4: Infrastructure
- SQL Server (relational data)
- NoSQL (user profiles, cache)
- Message Queue (async processing)
- File Storage (images, documents)

### External Integrations
- Payment Gateway (Stripe)
- Email Service (SendGrid)
- Analytics (Google Analytics)
- Logging (ELK Stack)
```

---

### Phase 3: Design Components

**Actions:**
```
1. For each component:
   a. Define responsibilities
   b. Identify inputs/outputs
   c. Plan internal structure
   d. Design interfaces
   e. Specify dependencies

2. Component interactions:
   - How do components communicate?
   - Synchronous calls vs events
   - Data contracts
   - Error handling

3. Scalability planning:
   - Horizontal scaling (multiple instances)
   - Vertical scaling (bigger servers)
   - Load balancing strategy
   - Caching strategy

4. Update status: "Phase 3 - Component design (100%)"
```

**Component Design:**
```
ProductService:
- Responsibilities:
  * Manage product catalog
  * Search and filtering
  * Product recommendations
  * Inventory sync
- Dependencies:
  * ProductRepository
  * InventoryService
  * CacheService
  * LoggingService
- Interfaces:
  * GetProducts(filters)
  * GetProductDetails(id)
  * SearchProducts(query)
  * UpdateProduct(id, data)
```

---

### Phase 4: Plan Data Flow

**Actions:**
```
1. Design data models:
   - Entity relationships
   - Normalization/denormalization
   - Caching strategy
   - Data consistency approach

2. Design request flows:
   - User request → API → Service → DB
   - Error handling at each layer
   - Async operations

3. Design event flows:
   - Order created event
   - Inventory updated event
   - Payment processed event
   - Notification events

4. Update status: "Phase 4 - Data flow design (100%)"
```

---

### Phase 5: Specify Non-Functional Aspects

**Actions:**
```
1. Security design:
   - Authentication strategy
   - Authorization model
   - Data encryption
   - API security

2. Performance:
   - Caching strategy
   - Database optimization
   - Async processing
   - Resource pooling

3. Resilience:
   - Error handling strategy
   - Circuit breakers
   - Retry logic
   - Fallbacks

4. Monitoring:
   - Logging strategy
   - Metrics collection
   - Health checks
   - Alerting

5. Update status: "Phase 5 - Non-functional design (100%)"
```

---

### Phase 6: Generate Design Document

**Report Structure:**
```
File: marketplace/output/architecture/<system>-system-design.md

Contents:
1. Executive Summary
2. Requirements Overview
3. Architecture Overview
4. Detailed Component Design
5. Data Models and Schema
6. Request/Response Flows
7. Event Flow Design
8. Security Design
9. Performance & Scalability
10. Resilience & Reliability
11. Deployment Architecture
12. Development Roadmap
13. Implementation Checklist
```

---

## Error Handling & Recovery

### Scenario 1: Incomplete Requirements
```
Warning: "Requirements are incomplete"
Action: Identify gaps
Recommendation: Make assumptions, document for review
```

### Scenario 2: Conflicting Requirements
```
Warning: "Requirements conflict (e.g., cost vs performance)"
Action: Identify conflicts
Recommendation: Discuss trade-offs with stakeholders
```

### Scenario 3: Technology Constraints
```
Warning: "Proposed architecture exceeds constraints"
Action: Redesign with constraints
Recommendation: Simplify, phased approach, or relax constraints
```

---

## Command Integration

This agent is invoked by:
```
/design-system <requirements-file> [--async|--wait] [--report=full|summary]

Examples:
/design-system requirements.md --wait
/design-system project-requirements.txt --async
/design-system specs.pdf --report=summary
```

---

## Output Locations

**System Designs**: `marketplace/output/architecture/<system>-system-design.md`
**Summary Designs**: `marketplace/output/architecture/<system>-design-summary.md`
**Status Files**: `.claude/task-status/<task-id>.md`

---

**Agent Version**: 1.0.0
**Last Updated**: 2025-10-30
**Task Coverage**: Task #9 (Design system architecture for new applications)
