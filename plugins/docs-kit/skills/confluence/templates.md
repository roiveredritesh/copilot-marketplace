# Page templates

Keep every page skimmable: a summary first, tables over prose, and code facts with file references. Omit sections that don't apply instead of leaving them empty.

## api - API documentation
```
# <Service> API
Summary: what it does, base URL per environment, owner/team
## Authentication: scheme (OIDC/bearer/API key), how to get a token, required scopes/roles
## Endpoints
| Method | Route | Purpose | Auth/policy | Request | Response | Errors |
(one row per endpoint; details below only for complex ones: example request/response JSON)
## Errors: ProblemDetails shape, status codes and their meaning
## Limits: rate limits, payload sizes, pagination style
## Changelog: date - change - breaking?
```

## adr - Architecture decision record
```
# ADR-<n>: <decision in one line>
Status: proposed | accepted | superseded by ADR-<m>   Date:   Deciders:
## Context: the problem and the constraints (numbers where possible)
## Options: for each, pros / cons / cost / risk (a table works)
## Decision: what was chosen and the deciding reasons
## Consequences: what becomes easier/harder, follow-up work, how success is measured
```

## runbook - Operational runbook
```
# <Service> runbook
Summary: purpose, owners, on-call channel, dashboards, logs location
## Dependencies: DBs, queues, external APIs (with health check endpoints)
## Configuration: key settings and where they live (no secret values)
## Deploy: steps, verification checks, rollback steps (tested?)
## Alerts: alert → meaning → first actions → escalation
## Common issues: symptom → diagnosis query/command → fix
## Maintenance: scheduled jobs, data retention, certificate/secret rotation
```

## release-notes
```
# <Product> <version> - <date>
Highlights: 2-4 user-facing bullets
## New
## Improved
## Fixed
## Breaking changes / migration steps (DB migrations, config changes, API changes)
## Known issues
```
Group commits and PRs by user impact, not by commit. Drop chores and refactors unless they change behavior.

## qa-guide - QA test guide (verified from code)
```
# QA guide: <feature>   Build/branch:   Environment:
## Scope: in / out
## Preconditions and test data
## Scenarios
| # | Scenario | Steps | Expected result | Source (path:line) |
Cover: happy path; each validation rule (client and server, with the exact message); each workflow branch and error path (duplicate, not found, unauthorized, DB failure); boundary values (min/max length, ranges, empty, special characters).
## Regression risks: nearby features touched by the change
```
Every expected message and rule must come from the code (with path:line). Mark anything not found in code as "(to confirm)".
