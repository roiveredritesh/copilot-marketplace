---
name: jira
description: Fetch a Jira ticket by key (e.g. PROJ-123) as a condensed summary through the isolated Haiku publisher, ready for /dotnet:debug or /dotnet:analyze.
argument-hint: "<ISSUE-KEY>"
---
# Jira intake

If `~/.claude/agents/publisher.md` doesn't exist, tell the user to run `/core:setup` and stop.

Dispatch `publisher`:
```text
WORK ORDER
goal: fetch Jira issue <KEY> for analysis
steps:
  1. Get issue <KEY> with fields: summary, type, status, priority, assignee, reporter, components, labels, fixVersions, description, comments, linked issues, attachments (names only).
return:
  KEY | type | status | priority | assignee
  Summary: <one line>
  Components/labels/fixVersions: <...>
  Description (first 15 lines, keep stack traces and steps-to-reproduce intact)
  Last 3 comments: <author>: <first 3 lines each>
  Links: <type> <KEY> <summary> (at most 5)
  Attachments: <names>
on-error: BLOCKED: <one line>
```

Then, depending on the ticket:
- Bug with a stack trace or repro steps → suggest `/dotnet:debug` with the extracted trace.
- Story or task → suggest `/dotnet:analyze <KEY>` (writes an analysis file), then `/dotnet:plan` with that file.
Don't paste the full ticket. The condensed form above is the working copy.
