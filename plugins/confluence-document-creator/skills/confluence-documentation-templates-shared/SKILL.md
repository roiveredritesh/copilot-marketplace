# Skill: Confluence Documentation Templates

## Overview

Effective documentation is critical for knowledge sharing, onboarding, and maintaining software systems. This skill provides comprehensive templates for common documentation types in Confluence, including API documentation, architecture decision records, runbooks, technical specifications, how-to guides, and troubleshooting guides.

## When to Use This Skill

- **Creating API documentation**: Document endpoints, parameters, responses
- **Recording architectural decisions**: Capture why decisions were made
- **Writing operational runbooks**: Document procedures for operations team
- **Documenting technical specifications**: Design documents for new features
- **Creating how-to guides**: Step-by-step instructions for common tasks
- **Building troubleshooting guides**: Help team resolve common issues
- **Onboarding new team members**: Comprehensive documentation repository
- **Knowledge transfer**: Preserve tribal knowledge

## Template 1: API Documentation

### Purpose
Document REST APIs, including endpoints, authentication, request/response formats, error codes, and usage examples.

### Template Structure

```markdown
# API Name: [Service/Module Name] API

## Overview
[Brief description of the API's purpose and scope]

**Base URL**: `https://api.example.com/v1`
**Version**: 1.0
**Last Updated**: 2026-01-15
**Owner**: [Team/Person Name]

---

## Authentication

### Authentication Method
[Bearer Token | API Key | OAuth 2.0 | Basic Auth]

### How to Authenticate
```http
GET /api/resource HTTP/1.1
Host: api.example.com
Authorization: Bearer {your_access_token}
```

### Getting Access Token
[Steps to obtain authentication credentials]

---

## Endpoints

### 1. [Endpoint Name]

**Purpose**: [What this endpoint does]

**HTTP Method**: `GET` | `POST` | `PUT` | `DELETE` | `PATCH`

**URL**: `/api/v1/resource/{id}`

**Authentication Required**: Yes | No

#### Request Parameters

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Unique identifier of the resource |

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number for pagination |
| pageSize | integer | No | 20 | Number of items per page |
| filter | string | No | - | Filter criteria |

**Request Headers**:
| Header | Required | Description |
|--------|----------|-------------|
| Content-Type | Yes | application/json |
| Authorization | Yes | Bearer token |

**Request Body** (for POST/PUT/PATCH):
```json
{
  "name": "string",
  "description": "string",
  "isActive": true,
  "metadata": {
    "key": "value"
  }
}
```

**Field Descriptions**:
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| name | string | Yes | Max 100 chars | Resource name |
| description | string | No | Max 500 chars | Resource description |
| isActive | boolean | Yes | - | Active status |
| metadata | object | No | - | Additional metadata |

#### Response

**Success Response** (200 OK):
```json
{
  "id": 123,
  "name": "Example Resource",
  "description": "This is an example",
  "isActive": true,
  "createdAt": "2026-01-15T10:30:00Z",
  "updatedAt": "2026-01-15T10:30:00Z",
  "metadata": {
    "key": "value"
  }
}
```

**Field Descriptions**:
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| name | string | Resource name |
| createdAt | datetime | ISO 8601 creation timestamp |
| updatedAt | datetime | ISO 8601 last update timestamp |

**Error Responses**:

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 400 Bad Request | Invalid input | `{"error": "Invalid field", "message": "Name is required"}` |
| 401 Unauthorized | Missing/invalid token | `{"error": "Unauthorized", "message": "Invalid token"}` |
| 404 Not Found | Resource not found | `{"error": "Not Found", "message": "Resource with id 123 not found"}` |
| 500 Internal Server Error | Server error | `{"error": "Internal Error", "message": "Please try again"}` |

#### Example Usage

**cURL Example**:
```bash
curl -X GET "https://api.example.com/v1/resource/123?page=1&pageSize=20" \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json"
```

**JavaScript Example**:
```javascript
const response = await fetch('https://api.example.com/v1/resource/123', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your_access_token',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

**C# Example**:
```csharp
var client = new HttpClient();
client.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", "your_access_token");

var response = await client.GetAsync("https://api.example.com/v1/resource/123");
var content = await response.Content.ReadAsStringAsync();
```

---

## Rate Limiting

**Limits**: 1000 requests per hour per API key
**Headers Returned**:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp when limit resets

**Exceeding Limit**: Returns `429 Too Many Requests`

---

## Common Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| 400 | Bad Request | Check request format and required fields |
| 401 | Unauthorized | Verify authentication token is valid |
| 403 | Forbidden | Check permissions for this resource |
| 404 | Not Found | Verify resource ID exists |
| 422 | Unprocessable Entity | Check field validation rules |
| 429 | Too Many Requests | Wait for rate limit to reset |
| 500 | Internal Server Error | Contact support if persists |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-15 | Initial API release |

---

## Support

**Documentation**: [Link to full docs]
**Support Email**: api-support@example.com
**Slack Channel**: #api-support
```

---

## Template 2: Architecture Decision Record (ADR)

### Purpose
Document significant architectural decisions, capturing context, options considered, decision made, and consequences.

### Template Structure

```markdown
# ADR-[Number]: [Decision Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Date**: 2026-01-15
**Decision Makers**: [Names or team]
**Consulted**: [Stakeholders consulted]
**Informed**: [People/teams informed of decision]

---

## Context and Problem Statement

[Describe the context and problem that requires a decision]

**Current Situation**:
[What is the current state? Why is this decision needed?]

**Requirements**:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Constraints**:
- [Technical constraint 1]
- [Business constraint 1]
- [Time/budget constraint]

---

## Decision Drivers

[Forces that influenced the decision]

**Must Have**:
- [Critical requirement 1]
- [Critical requirement 2]

**Should Have**:
- [Important requirement 1]
- [Important requirement 2]

**Nice to Have**:
- [Optional requirement 1]

**Key Considerations**:
- Performance requirements
- Scalability needs
- Team expertise
- Time to market
- Maintenance burden
- Cost

---

## Options Considered

### Option 1: [Option Name]

**Description**:
[Detailed description of this option]

**Pros**:
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]
- [Disadvantage 3]

**Cost/Effort**: [High | Medium | Low]

**Risk**: [High | Medium | Low]

---

### Option 2: [Option Name]

[Same structure as Option 1]

---

### Option 3: [Option Name]

[Same structure as Option 1]

---

## Decision Outcome

**Chosen Option**: [Selected option and brief reason]

**Rationale**:
[Detailed explanation of why this option was chosen]

- Addresses all critical requirements
- Best balance of [factors]
- Team has expertise in this approach
- [Other reasons]

**Expected Consequences**:

**Positive**:
- [Benefit 1]
- [Benefit 2]

**Negative**:
- [Trade-off 1 and how we'll mitigate it]
- [Trade-off 2 and how we'll mitigate it]

**Risks**:
- [Risk 1 and mitigation strategy]
- [Risk 2 and mitigation strategy]

---

## Implementation Plan

**High-Level Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Timeline**: [Estimated implementation timeframe]

**Dependencies**:
- [Dependency 1]
- [Dependency 2]

---

## Validation and Success Metrics

**How we'll know this was the right decision**:
- [Metric 1: Target value]
- [Metric 2: Target value]
- [Qualitative success criteria]

**Review Date**: [When to review this decision]

---

## References

- [Link to related documentation]
- [Link to spike/prototype]
- [Link to related ADRs]
- [External resources that informed decision]

---

## Notes

[Any additional context, discussions, or updates]
```

---

## Template 3: Operational Runbook

### Purpose
Document operational procedures for deployment, monitoring, troubleshooting, and maintenance tasks.

### Template Structure

```markdown
# Runbook: [System/Process Name]

**System**: [System name]
**Owner**: [Team/Person responsible]
**Last Updated**: 2026-01-15
**On-Call Contact**: [Contact information]

---

## System Overview

**Purpose**: [What this system does]

**Architecture**:
[Brief description or diagram of system architecture]

**Key Components**:
- Component 1: [Description]
- Component 2: [Description]
- Component 3: [Description]

**Dependencies**:
- External Service 1
- Database: [Database name]
- Message Queue: [Queue name]

**Monitoring Dashboards**:
- [Link to primary dashboard]
- [Link to logs]
- [Link to alerts]

---

## Deployment Procedures

### Prerequisites
- [ ] Code reviewed and approved
- [ ] Tests passing in CI/CD
- [ ] Database migrations tested
- [ ] Configuration updated
- [ ] Stakeholders notified

### Deployment Steps

#### 1. Pre-Deployment
```bash
# Backup current version
git tag backup-$(date +%Y%m%d-%H%M%S)

# Verify health checks
curl https://api.example.com/health
```

#### 2. Deployment
```bash
# Deploy to staging
./deploy.sh staging

# Run smoke tests
./smoke-tests.sh staging

# Deploy to production
./deploy.sh production
```

#### 3. Post-Deployment
- [ ] Verify application is running
- [ ] Check error logs for new errors
- [ ] Monitor dashboard for anomalies
- [ ] Test critical user flows
- [ ] Update deployment log

**Deployment Checklist**:
```
[ ] Code deployed successfully
[ ] Database migrations applied
[ ] Configuration changes verified
[ ] Health checks passing
[ ] No error spike in logs
[ ] Performance metrics normal
[ ] Rollback plan ready
```

### Rollback Procedure
```bash
# If issues detected, rollback immediately
./rollback.sh production

# Verify rollback successful
curl https://api.example.com/health

# Notify team
# Investigate root cause
```

---

## Monitoring and Alerts

### Key Metrics to Monitor

| Metric | Normal Range | Warning Threshold | Critical Threshold | Action |
|--------|--------------|-------------------|-------------------|---------|
| Response Time | < 200ms | > 500ms | > 1000ms | Investigate performance |
| Error Rate | < 0.1% | > 1% | > 5% | Check logs, rollback if needed |
| CPU Usage | < 60% | > 80% | > 95% | Scale up or investigate |
| Memory Usage | < 70% | > 85% | > 95% | Check for memory leaks |

### Alert Response

**Critical Alert Received**:
1. Acknowledge alert in monitoring system
2. Check system status dashboard
3. Review recent changes (deployments, config)
4. Check error logs for patterns
5. Follow troubleshooting guide below
6. Escalate if not resolved in 15 minutes

---

## Troubleshooting Guide

### Issue: High Error Rate

**Symptoms**:
- Error rate > 5%
- Alerts firing
- User reports of failures

**Diagnostic Steps**:
```bash
# Check recent deployments
git log --oneline -10

# Check error logs
tail -f /var/log/application/error.log | grep ERROR

# Check database connectivity
psql -h db-host -U username -d database -c "SELECT 1"

# Check external service dependencies
curl https://external-api.com/health
```

**Common Causes**:
1. Recent deployment introduced bug → Rollback
2. Database connection pool exhausted → Restart app
3. External service down → Enable circuit breaker
4. Rate limit exceeded → Contact external service

**Resolution Steps**:
[Specific steps based on root cause]

---

### Issue: Slow Response Times

**Symptoms**:
- Response time > 1000ms
- Timeouts reported
- User complaints about slowness

**Diagnostic Steps**:
```bash
# Check database query performance
# (Log into database)
SELECT * FROM pg_stat_activity WHERE state = 'active';

# Check for long-running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

# Check application performance
# (Access APM dashboard)
```

**Common Causes**:
1. Slow database queries → Optimize queries
2. High load → Scale horizontally
3. Memory leak → Restart application
4. External API slow → Increase timeout, add caching

---

## Maintenance Procedures

### Daily Tasks
- [ ] Review error logs for anomalies
- [ ] Check dashboard for performance trends
- [ ] Verify backups completed successfully

### Weekly Tasks
- [ ] Review and close resolved alerts
- [ ] Update dependencies if needed
- [ ] Review capacity trends

### Monthly Tasks
- [ ] Review and update runbook
- [ ] Analyze performance trends
- [ ] Update disaster recovery plan
- [ ] Security patch review

---

## Emergency Contacts

| Role | Name | Primary Contact | Secondary Contact |
|------|------|----------------|-------------------|
| On-Call Engineer | [Name] | [Phone] | [Email] |
| Team Lead | [Name] | [Phone] | [Email] |
| Database Admin | [Name] | [Phone] | [Email] |
| Infrastructure | [Name] | [Phone] | [Email] |

**Escalation Path**:
1. On-Call Engineer (respond within 15 min)
2. Team Lead (if not resolved in 30 min)
3. Director of Engineering (if critical and not resolved in 1 hour)

---

## Related Documentation

- [Architecture diagram]
- [API documentation]
- [Database schema]
- [Configuration management]
```

---

## Template 4: Technical Specification

### Purpose
Document technical design for new features or major changes before implementation.

### Template Structure

```markdown
# Technical Specification: [Feature Name]

**Author**: [Name]
**Status**: [Draft | In Review | Approved | Implemented]
**Created**: 2026-01-15
**Last Updated**: 2026-01-15
**Reviewers**: [Names]
**Related Tickets**: [JIRA-123, JIRA-456]

---

## Executive Summary

[One paragraph overview of the feature and why it's being built]

**Problem Statement**: [What problem are we solving?]

**Proposed Solution**: [High-level description of the solution]

**Success Metrics**:
- [Metric 1]
- [Metric 2]

---

## Background and Context

**Current State**:
[Description of how things work currently]

**Why This Change**:
[Business justification, user need, technical debt]

**User Impact**:
[How this affects end users]

---

## Requirements

### Functional Requirements
1. **[Requirement 1]**: [Description]
   - Acceptance Criteria: [Criteria]
2. **[Requirement 2]**: [Description]
   - Acceptance Criteria: [Criteria]

### Non-Functional Requirements
- **Performance**: [Target response time, throughput]
- **Scalability**: [Expected load, scaling requirements]
- **Security**: [Authentication, authorization, data protection]
- **Availability**: [Uptime requirements, SLA]
- **Compatibility**: [Browser support, API versions]

### Out of Scope
[Explicitly list what this spec does NOT cover]

---

## Proposed Solution

### High-Level Architecture

```
[ASCII diagram or reference to architecture diagram]

┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │─────▶│   API       │─────▶│  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  Cache      │
                     └─────────────┘
```

**Component Descriptions**:
- **Component 1**: [Responsibility and implementation details]
- **Component 2**: [Responsibility and implementation details]

### Data Model

**New Tables**:
```sql
CREATE TABLE FeatureData (
    Id INT PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    CreatedAt DATETIME2 NOT NULL,
    -- ...
);
```

**Modified Tables**:
```sql
ALTER TABLE ExistingTable
ADD NewColumn VARCHAR(50) NULL;
```

### API Changes

**New Endpoints**:
- `POST /api/v1/feature` - Create new feature item
- `GET /api/v1/feature/{id}` - Retrieve feature item

**Modified Endpoints**:
- `GET /api/v1/existing` - Added new query parameter `filter`

**Deprecated Endpoints**:
- `GET /api/v1/old-endpoint` - Deprecated in v1.5, removed in v2.0

### Business Logic

**Key Algorithms**:
1. **[Algorithm Name]**: [Description and pseudocode if complex]

**Validation Rules**:
- Field X must be between 1 and 100
- Field Y is required when Z is true

---

## Implementation Plan

### Phase 1: Foundation (Sprint 1)
- Database schema changes
- Basic CRUD operations
- Unit tests

### Phase 2: Core Features (Sprint 2)
- Business logic implementation
- API endpoints
- Integration tests

### Phase 3: Polish (Sprint 3)
- Error handling
- Performance optimization
- Documentation

**Dependencies**:
- [External library version X.Y]
- [Team B completing task Z]

**Risks**:
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High | Medium | [Mitigation strategy] |
| [Risk 2] | Medium | Low | [Mitigation strategy] |

---

## Testing Strategy

**Unit Tests**:
- [Component] logic
- [Validation] rules
- [Edge cases]

**Integration Tests**:
- [End-to-end flow]
- [External service integration]

**Performance Tests**:
- [Load scenario]: X concurrent users
- [Target]: Response time < Y ms

**Security Tests**:
- Authorization checks
- Input validation
- SQL injection prevention

---

## Deployment Strategy

**Rollout Plan**:
1. Deploy to staging environment
2. QA testing (2 days)
3. Deploy to production (off-peak hours)
4. Monitor for 24 hours
5. Feature flag enabled for 10% of users
6. Gradual rollout to 100% over 1 week

**Rollback Plan**:
- Feature flag can disable feature instantly
- Database migrations are backward compatible
- Previous version can run alongside new schema

---

## Monitoring and Success Metrics

**Key Metrics**:
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Response Time | < 200ms | APM dashboard |
| Error Rate | < 0.1% | Application logs |
| Adoption | > 50% in 30 days | Analytics |

**Alerts**:
- Error rate > 1% → Immediate notification
- Response time > 500ms → Warning

---

## Open Questions

1. **[Question 1]**: [Context and options]
   - **Decision**: [To be determined | Decided on X]
2. **[Question 2]**: [Context]

---

## References

- [Design mockups]
- [Related ADR]
- [External documentation]
- [Spike/prototype]

---

## Appendix

### Alternative Approaches Considered

**Approach 1**: [Description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]
```

---

## Template 5: How-To Guide

### Purpose
Step-by-step instructions for completing specific tasks.

### Template Structure

```markdown
# How To: [Task Name]

**Purpose**: [What this guide helps you accomplish]
**Audience**: [Who should use this guide]
**Estimated Time**: [How long this takes]
**Last Updated**: 2026-01-15

---

## Prerequisites

**Required Access**:
- [ ] Access to [system/tool]
- [ ] Permissions: [specific permissions needed]

**Required Tools**:
- [ ] [Tool 1] version X.Y or higher
- [ ] [Tool 2]

**Required Knowledge**:
- Basic understanding of [concept]
- Familiarity with [system]

---

## Overview

[Brief description of what you'll accomplish]

**Steps at a Glance**:
1. [High-level step 1]
2. [High-level step 2]
3. [High-level step 3]

---

## Step 1: [First Step]

**What you'll do**: [Brief description]

**Instructions**:
1. Navigate to [location]
2. Click [button/link]
3. Enter [information]

**Screenshot**:
[Include annotated screenshot]

**Expected Result**:
[What success looks like]

**Troubleshooting**:
- **Issue**: [Common problem]
  - **Solution**: [How to resolve]

---

## Step 2: [Second Step]

[Same structure as Step 1]

---

## Verification

**How to verify it worked**:
1. [Verification step 1]
2. [Verification step 2]

**Expected Output**:
```
[Example of successful output]
```

---

## Troubleshooting

### Problem: [Common issue]
**Symptoms**: [What you see when this happens]
**Solution**: [How to fix]

---

## Related Documentation

- [Link to related guide]
- [Link to system documentation]

---

## Need Help?

**Support Channels**:
- Slack: #team-channel
- Email: support@example.com
- Office Hours: Tuesdays 2-3 PM
```

---

## Template 6: Troubleshooting Guide

### Purpose
Help team members diagnose and resolve common issues.

### Template Structure

```markdown
# Troubleshooting Guide: [System/Feature Name]

**System**: [System name]
**Last Updated**: 2026-01-15
**Owner**: [Team/Person]

---

## Quick Diagnostic Checklist

**Start here for any issue**:
- [ ] Check system status page
- [ ] Review recent deployments (last 24 hours)
- [ ] Check error logs for patterns
- [ ] Verify external dependencies are up
- [ ] Check monitoring dashboards for anomalies

---

## Common Issues

### Issue 1: [Issue Name]

**Symptoms**:
- [Symptom 1]
- [Symptom 2]
- Error message: `[Exact error text]`

**Severity**: 🔴 Critical | 🟡 High | 🔵 Medium | ⚪ Low

**Common Causes**:
1. [Most likely cause]
2. [Second likely cause]
3. [Less common cause]

**Diagnostic Steps**:
```bash
# Step 1: Check system status
curl https://api.example.com/health

# Step 2: Check logs
tail -100 /var/log/app/error.log | grep ERROR

# Step 3: Verify database connection
psql -h localhost -U user -c "SELECT 1"
```

**Resolution**:

**If [condition]**:
```bash
# Solution steps
command1
command2
```

**If [other condition]**:
```bash
# Alternative solution
command3
```

**Verification**:
[How to confirm the issue is resolved]

**Prevention**:
[How to prevent this in the future]

---

## Error Messages

### Error: "Connection timeout"

**Full Error**:
```
System.TimeoutException: The operation has timed out.
   at System.Net.HttpWebRequest.GetResponse()
```

**Meaning**: [What this error indicates]

**Quick Fix**: [Immediate action to take]

**Root Cause Investigation**: [Deeper analysis steps]

---

## Escalation Matrix

| Severity | Response Time | Who to Contact | Escalation After |
|----------|---------------|----------------|------------------|
| 🔴 Critical | Immediate | On-call engineer | 15 minutes |
| 🟡 High | < 1 hour | Team lead | 2 hours |
| 🔵 Medium | < 4 hours | Team channel | 1 day |
| ⚪ Low | < 1 day | Regular ticket | N/A |

---

## Logs and Monitoring

**Log Locations**:
- Application logs: `/var/log/application/`
- Error logs: `/var/log/application/error.log`
- Access logs: `/var/log/nginx/access.log`

**Useful Log Queries**:
```bash
# Find errors in last hour
grep ERROR /var/log/application/error.log | \
  grep "$(date -d '1 hour ago' '+%Y-%m-%d %H')"

# Count errors by type
grep ERROR /var/log/application/error.log | \
  awk '{print $5}' | sort | uniq -c | sort -rn
```

**Dashboards**:
- [Primary monitoring dashboard]
- [Error tracking dashboard]
- [Performance dashboard]
```

---

## Documentation Best Practices

### Writing Effective Documentation

1. **Be concise**: Get to the point quickly
2. **Use examples**: Show, don't just tell
3. **Include screenshots**: Visual aids help understanding
4. **Keep updated**: Review and update regularly
5. **Use templates**: Consistency aids navigation
6. **Link related docs**: Create documentation web
7. **Test your docs**: Have someone else follow your instructions
8. **Version control**: Track changes over time

### Confluence Formatting Tips

**Code Blocks**:
```
Use ``` for multi-line code
Use ` for inline code
```

**Callouts**:
- 💡 **Tip**: Use for helpful hints
- ⚠️ **Warning**: Use for important caveats
- ❌ **Danger**: Use for critical warnings
- ✅ **Success**: Use for positive outcomes

**Tables**:
- Use tables for structured data
- Keep tables simple and scannable
- Use header row for column names

## Key Takeaways

1. **Choose the right template**: Match template to documentation purpose
2. **Fill in all sections**: Incomplete documentation is confusing
3. **Update regularly**: Documentation rots quickly if not maintained
4. **Link related docs**: Help readers find related information
5. **Include examples**: Real examples are more valuable than abstract descriptions
6. **Make it scannable**: Use headers, lists, and tables
7. **Test your documentation**: Have someone else follow your steps
8. **Set ownership**: Clear ownership ensures maintenance

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Documentation & Communication
