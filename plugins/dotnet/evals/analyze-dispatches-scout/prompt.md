---
model: sonnet
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Agent, AskUserQuestion, TodoWrite]
---

/dotnet:analyze Orders with a total above 10,000 must wait for manager approval before they count as placed. Add an approval status to orders and an endpoint for a manager to approve or reject. Source: user details. No Jira.
