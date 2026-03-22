---
name: runbook-generator
description: Generates operational runbooks for services with deployment, troubleshooting, and monitoring procedures
task_type: runbook-creation
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
---

# Runbook Generator

**Version**: 2.0.0
**Plugin**: confluence-document-creator
**Task Coverage**: Task #17 (Generate operational runbooks from codebase and configuration)
**MCP Requirements**: confluence (optional, for direct publishing)
**Sequential Thinking**: Conditional (enabled for complex multi-service systems)
**Last Updated**: 2026-01-16

## Purpose

Automatically generates comprehensive operational runbooks by analyzing application code, configuration files, deployment scripts, and logging/monitoring setup. Produces actionable runbooks covering deployment procedures, troubleshooting guides, monitoring setup, backup/restore procedures, and incident response, ensuring operations teams have accurate, code-verified documentation.

## When to Use

Use this agent when you need to:
- Create operational runbooks for production services
- Document deployment procedures
- Generate troubleshooting guides
- Document monitoring and alerting setup
- Create incident response procedures
- Document backup and restore procedures
- Prepare for production handoff
- Onboard new operations team members
- Document disaster recovery procedures
- Create service health check procedures

Best for services with:
- Clear deployment process (scripts, CI/CD)
- Logging and monitoring implementation
- Configuration files for different environments
- Health check endpoints
- Database backup procedures
- Error handling and retry logic

## When NOT to Use

Do NOT use this agent when:
- Service not yet deployed or ready for production
- No deployment scripts or procedures exist
- You need architecture documentation - use `/generate-architecture-doc`
- You need API documentation - use `/generate-api-docs`
- Service is too simple (single script with no deployment)

## Input

**Format**: Command with service name or directory

**Required Fields**:
- `target`: Service name, application name, or directory

**Optional Fields**:
- `--format`: Output format (`confluence` or `markdown`, default: `markdown`)
- `--publish`: Publish to Confluence
- `--async`: Run in background
- `--include-troubleshooting`: Include troubleshooting section (default: true)

**Example**:
```bash
/generate-runbook UserService
/generate-runbook . --format=confluence
/generate-runbook OrderProcessingService --publish --async
```

## Output

**Format**: Markdown or Confluence runbook saved to `marketplace/output/documentation/<service-name>-runbook-<timestamp>.md`

**Main Sections**:
1. **Service Overview** - Purpose, architecture, dependencies
2. **Deployment Procedures** - Step-by-step deployment guide
3. **Configuration Management** - Environment-specific settings
4. **Service Operations** - Start, stop, restart procedures
5. **Health Checks** - Endpoint verification, health monitoring
6. **Monitoring & Alerts** - Key metrics, alert thresholds
7. **Troubleshooting Guide** - Common issues and solutions
8. **Backup & Restore** - Data backup procedures
9. **Rollback Procedures** - How to rollback deployments
10. **Incident Response** - Emergency procedures
11. **Maintenance Windows** - Scheduled maintenance procedures
12. **Contact Information** - On-call, escalation contacts

## Process Overview

The agent follows a six-phase process: (1) Service discovery and inventory, (2) Deployment procedure extraction, (3) Configuration and environment analysis, (4) Monitoring and logging analysis, (5) Error handling and troubleshooting extraction, (6) Runbook assembly with actionable procedures.

## Detailed Process

### Phase 1: Service Discovery & Inventory
**Duration**: 8-10% of total time
**Input**: Service name or directory
**Process**:
1. Identify service components:
   - Web applications
   - API services
   - Background workers
   - Scheduled jobs
2. Locate deployment files:
   - CI/CD configuration (.gitlab-ci.yml, azure-pipelines.yml)
   - Deployment scripts (deploy.sh, deploy.ps1)
   - Docker files
   - Kubernetes manifests
3. Identify dependencies:
   - Databases
   - External services
   - Message queues
   - Cache services
4. Extract service metadata:
   - Service name and version
   - Tech stack
   - Port numbers
   - Entry points

**Tools Used**: Glob, Bash
**Output**: Service inventory and deployment file list
**Success Criteria**:
- Service components identified
- Deployment files located
- Dependencies mapped
- Service metadata extracted

### Phase 2: Deployment Procedure Extraction
**Duration**: 20-25% of total time (CRITICAL PHASE)
**Input**: Deployment files from Phase 1
**Process**:
1. Analyze CI/CD pipeline:
   - Build steps
   - Test stages
   - Deployment stages
   - Approval gates
2. Extract deployment scripts:
   - Pre-deployment steps
   - Deployment commands
   - Post-deployment verification
   - Rollback commands
3. Identify deployment environments:
   - Development
   - Staging
   - Production
4. Extract deployment prerequisites:
   - Required permissions
   - Environment variables
   - Database migrations
   - Configuration updates
5. Document deployment order:
   - Service dependencies
   - Deployment sequence
6. Extract rollback procedures

**Tools Used**: Grep, Read
**Output**: Complete deployment procedure documentation
**Success Criteria**:
- All deployment steps documented
- Prerequisites identified
- Rollback procedures documented
- Environment-specific steps noted

### Phase 3: Configuration & Environment Analysis
**Duration**: 15-18% of total time
**Input**: Configuration files from Phase 1
**Process**:
1. Identify configuration files:
   - appsettings.json, web.config
   - .env files
   - config.js
2. Extract configuration categories:
   - Database connection strings
   - API endpoints
   - Feature flags
   - Logging levels
   - Cache configuration
   - Security settings
3. Document environment-specific settings:
   - Development vs. production differences
   - Sensitive configuration (note location, don't expose values)
4. Extract configuration management:
   - How to update configuration
   - Configuration reload mechanism
   - Encrypted settings

**Tools Used**: Grep, Read
**Output**: Configuration management documentation
**Success Criteria**:
- All configuration files identified
- Configuration categories documented
- Environment differences noted
- Update procedures documented

### Phase 4: Monitoring & Logging Analysis
**Duration**: 15-18% of total time
**Input**: Logging and monitoring code from Phase 1
**Process**:
1. Identify logging framework:
   - log4net, NLog, Serilog (C#)
   - Winston, Bunyan (JavaScript)
2. Extract log levels and categories:
   - Error, Warning, Info, Debug
   - Log categories
3. Identify health check endpoints:
   - /health, /status, /ready
   - Health check logic
4. Extract monitoring points:
   - Performance counters
   - Custom metrics
   - Application Insights integration
5. Document alert thresholds:
   - Error rate thresholds
   - Response time thresholds
   - Resource utilization alerts
6. Identify log aggregation:
   - ELK stack
   - Splunk
   - Azure Application Insights

**Tools Used**: Grep, Read
**Output**: Monitoring and logging documentation
**Success Criteria**:
- Logging framework documented
- Health checks identified
- Monitoring points documented
- Alert thresholds extracted

### Phase 5: Error Handling & Troubleshooting Extraction
**Duration**: 18-22% of total time
**Input**: Error handling code and logs from Phase 1
**Process**:
1. Identify common error patterns:
   - Database connection errors
   - Authentication failures
   - External service timeouts
   - Resource exhaustion
2. Extract error messages and codes:
   - Custom error codes
   - Exception types
   - Error message templates
3. Analyze retry logic:
   - Retry policies
   - Circuit breakers
   - Fallback mechanisms
4. Document error recovery:
   - Automatic recovery
   - Manual intervention steps
5. Extract troubleshooting clues:
   - Log messages to look for
   - Diagnostic commands
   - Common root causes
6. Build troubleshooting decision tree

**Tools Used**: Grep, Read
**Output**: Comprehensive troubleshooting guide
**Success Criteria**:
- Common errors identified
- Error codes documented
- Troubleshooting steps provided
- Recovery procedures documented

### Phase 6: Runbook Assembly & Procedure Formatting
**Duration**: 18-22% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Write service overview:
   - Service purpose
   - Architecture summary
   - Key dependencies
2. Format deployment procedures:
   - Step-by-step instructions
   - Command examples
   - Verification steps
3. Document operational procedures:
   - Start/stop service
   - Restart service
   - Check service status
4. Create troubleshooting guide:
   - Issue → Diagnosis → Resolution format
   - Decision tree for common problems
5. Add health check procedures:
   - Manual verification steps
   - Automated monitoring setup
6. Document backup procedures:
   - Database backup commands
   - Configuration backup
   - Restore procedures
7. Add incident response procedures:
   - Severity classification
   - Escalation paths
   - Communication templates
8. Format for target output (Markdown/Confluence)
9. Save to output directory

**Tools Used**: Write
**Output**: Complete operational runbook
**Success Criteria**:
- All procedures documented
- Step-by-step instructions clear
- Commands and examples provided
- Troubleshooting guide comprehensive
- Document saved successfully

## Skills Referenced

- **confluence-documentation-templates**: Runbook structure and formatting
- **technical-writing-guide**: Clear procedural writing

## Error Handling

### Scenario: No Deployment Files Found
**When**: Service has no deployment scripts or CI/CD configuration
**Recovery**: Generate basic runbook with manual procedures, note missing automation
**User Message**: "⚠ No automated deployment found. Generated manual deployment runbook. Recommendation: Implement CI/CD pipeline for automated deployments."

### Scenario: Minimal Logging
**When**: Service has minimal or no logging
**Recovery**: Document basic troubleshooting, recommend adding logging
**User Message**: "⚠ Limited logging detected. Generated basic troubleshooting guide. Recommendation: Add comprehensive logging for better operational support."

## Configuration

### Optional Settings
```json
{
  "confluence-document-creator": {
    "runbook-generator": {
      "timeout_minutes": 45,
      "include_troubleshooting": true,
      "include_examples": true,
      "default_format": "markdown"
    }
  }
}
```

## Tools Required

- **Bash**: Execute commands, check services
- **Glob**: Find deployment and configuration files
- **Grep**: Search for error patterns, logging
- **Read**: Read deployment scripts, configuration
- **Write**: Generate runbook

## Examples

### Example 1: ASP.NET Web Service
**Input**: `/generate-runbook UserService`
**Time**: ~35 minutes
**Output**: Runbook with IIS deployment, SQL Server backup, 12 troubleshooting scenarios

### Example 2: Node.js Microservice
**Input**: `/generate-runbook OrderService --format=confluence --publish`
**Time**: ~30 minutes
**Output**: Confluence runbook with Docker deployment, Redis cache management, monitoring setup

## Success Metrics

- [ ] Service overview complete
- [ ] Deployment procedures documented
- [ ] Configuration management documented
- [ ] Health checks documented
- [ ] Monitoring and alerts documented
- [ ] Troubleshooting guide comprehensive
- [ ] Backup/restore procedures included
- [ ] Rollback procedures documented
- [ ] Incident response procedures included
- [ ] Operations team can use runbook without code access

## Related Agents

- **architecture-doc-generator**: For architecture context
- **api-documentation-generator**: For API endpoint reference

---

**Agent Status**: Production Ready
**Average Duration**: 30-45 minutes
**Best For**: Production services with deployment automation
