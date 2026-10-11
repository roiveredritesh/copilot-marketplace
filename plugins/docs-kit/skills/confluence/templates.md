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

## spike - Spike report
```
# Spike: <question>
Summary: answer/recommendation in 2-3 lines | confidence: high/medium/low | time-boxed to <n>h | <date> | ticket <KEY link> | author
## Question: what was unclear and which decision it unblocks
## Constraints and criteria: must-haves and how options were judged
## Options compared
| Criterion | Option A | Option B | ... |   (every cell backed by a source link or code reference)
## Findings: key facts, each with its source (docs/release-notes links, NuGet, file:line)
## PoC: what was built, what it proved and what it didn't, branch or repo link (omit if none)
## Recommendation: the choice and the deciding reasons
## Risks, assumptions, open questions: label assumptions as such
## Next steps: tickets to create, an ADR if the decision is accepted, owners
## Sources: links
```

## findings - Ticket findings (bug investigation or story analysis)
```
# <KEY>: <ticket summary> - findings
Summary: status (root cause found | analysis complete | decision needed) | conclusion in 2-3 lines | <date> | <Jira link> | author
## Problem: what was reported, impact (who, how many, since when), environment/version
## Investigation
| Check | Evidence (log line, query, file:line, commit) | Result |
## Root cause (bug) / Analysis (story): explanation with file:line and commit references
## Fix or proposal: what changes where, risk, PR link if one exists
## Verification: how it was or will be tested (test names, steps), how to confirm in production
## Decisions needed / open questions
## Follow-ups: tickets, monitoring/alerts, docs to update
```
