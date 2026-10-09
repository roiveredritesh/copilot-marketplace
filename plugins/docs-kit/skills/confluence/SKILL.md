---
name: confluence
description: Create or update a Confluence page (API doc, ADR, runbook, release notes, QA test guide) from the codebase; the page is published by the isolated Haiku publisher agent.
argument-hint: "<api|adr|runbook|release-notes|qa-guide> <space-key or page URL/id> [parent page id] [topic]"
disable-model-invocation: true
---
# Publish a Confluence page

The `publisher` agent (installed by `/core:setup` at `~/.claude/agents/publisher.md`) is the only thing that talks to Confluence. If it doesn't exist, stop and tell the user to run `/core:setup`.

## 1. Inputs
From the arguments: doc type, target (a space key + optional parent id for a new page, or a page URL/id to update), and topic. Ask once (AskUserQuestion) for anything missing.

## 2. Gather facts with cheap agents (one message, parallel where independent)
| Doc type | Work orders |
|---|---|
| api | `core:scout`: "scope: <API project dir> | terms: Map(Get|Post|Put|Delete), [Http*], [Route. List endpoints: route, HTTP verb, request/response type, auth attribute, path:line; at most 60 lines" |
| adr | none, unless the decision references code: `core:scout` for the affected components |
| runbook | `core:scout`: "scope: <host project dir>, appsettings*.json, Program.cs. List config keys (appsettings*, env vars), health check endpoints, background services, external dependencies (connection strings/HttpClient names), with path:line" |
| release-notes | `core:runner` with the two commands below (at most 80 lines) |
| qa-guide | `core:scout`: "scope: <dirs of the feature> | terms: <page/endpoint/type names>. For the feature: UI inputs and validators (client and server, DataAnnotations), workflow branches and error paths, DB constraints that reject input, with path:line; at most 80 lines" |

Release-notes commands (the second one only when `gh` is authenticated):
```bash
git log <from>..<to> --no-merges --format='%h %s (%an)'
gh pr list --state merged --search "merged:>=<yyyy-mm-dd>" --limit 100 --json number,title,labels --jq '.[] | "#\(.number) \(.title) [\(.labels|map(.name)|join(","))]"'
```

Write only facts the agents returned or you verified. Mark anything assumed with "(to confirm)".

**Verify before you rely on it:** subagents only see the work order. Give them exact paths, symbols, and commands, never "look around". Before stating a subagent finding as fact in the report, open the 1-2 most decision-critical `path:line` references yourself (a small range each). Drop or label anything that doesn't check out.

## 3. Write the page body once
Use the matching structure in [templates.md](templates.md). Write it in Markdown to `~/.claude/reports/<repo-folder-name>/confluence-<slug>.md` with the Write tool. That one file is the payload. Don't repeat the body in chat; show a 5-line outline instead.

## 4. Publish: dispatch `publisher`
```text
WORK ORDER
goal: <create|update> Confluence page "<title>"
inputs: body file = <absolute path>; space = <key>; parent = <id or none>; page = <id or none>
steps:
  1. Read the body file.
  2. create: create the page in <space> under <parent> with title "<title>" and the body.
     update: get page <id> (version number only), then update it with the body, version + 1, same title unless "<new title>" is given.
     If the tool takes a content format/representation, use markdown.
return: id | version | url
on-error: BLOCKED: <one line>
```

## 5. Report
Print the page URL and the local body file path. If BLOCKED with an auth error, tell the user to check the Atlassian login (the `/core:setup` notes show how to re-add the server to the main session if the subagent can't authenticate).
