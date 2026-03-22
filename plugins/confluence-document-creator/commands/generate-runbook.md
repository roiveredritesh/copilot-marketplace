---
name: generate-runbook
description: Generate operational runbook for services
delegated_to: runbook-generator
---

# Command: /generate-runbook

Generate operational runbook with deployment, troubleshooting, monitoring, and incident response procedures.

## Usage

```bash
/generate-runbook <service-name|directory> [flags]
```

## Arguments

- `<service-name|directory>`: Service name, application name, or directory
  - Examples: `UserService`, `.`, `src/OrderService`

## Flags

- `--format=<markdown|confluence>`: Output format (default: `markdown`)
- `--publish`: Auto-publish to Confluence (requires Confluence MCP)
- `--async`: Run in background
- `--wait`: Wait for completion (default)
- `--include-troubleshooting`: Include troubleshooting section (default: `true`)

## Examples

### Basic Usage
```bash
# Generate runbook for service
/generate-runbook UserService

# Generate for current directory
/generate-runbook .
```

### Publishing
```bash
# Generate Confluence runbook
/generate-runbook OrderService --format=confluence

# Generate and auto-publish
/generate-runbook PaymentService --format=confluence --publish
```

### Background Execution
```bash
# Complex service - run in background
/generate-runbook . --async
```

## Output

Documentation saved to: `output/documentation/<service-name>-runbook-<timestamp>.md`

**Sections**:
- Service Overview
- Deployment Procedures
- Configuration Management
- Service Operations (start/stop/restart)
- Health Checks
- Monitoring & Alerts
- Troubleshooting Guide
- Backup & Restore
- Rollback Procedures
- Incident Response
- Maintenance Windows

## Execution Time

- Simple service: 20-30 minutes
- Standard service: 30-45 minutes
- Complex service: 45-60 minutes

## Requirements

- **MCP**: None (Confluence optional for `--publish`)
- **Tools**: Bash, Glob, Grep, Read, Write

## Runbook Includes

### Deployment
- Pre-deployment checklist
- Step-by-step deployment
- Post-deployment verification
- Rollback procedures

### Operations
- Start/stop/restart commands
- Health check verification
- Log locations
- Configuration file locations

### Troubleshooting
- Common issues and solutions
- Diagnostic commands
- Log analysis
- Error code reference

### Monitoring
- Key metrics to monitor
- Alert thresholds
- Dashboard setup
- Log aggregation

## Troubleshooting

### No Deployment Files
```
Issue: "No automated deployment found"
Solution: Generated manual runbook. Consider implementing CI/CD.
```

### Minimal Logging
```
Issue: "Limited logging detected"
Solution: Basic troubleshooting guide created. Add comprehensive logging.
```

## Related Commands

- `/generate-architecture-doc` - For architecture context
- `/generate-api-docs` - For API reference
- `/analyze-stacktrace` - For debugging production issues

---

**Delegates To**: runbook-generator agent
**Command Version**: 2.0.0
**Status**: Production Ready
