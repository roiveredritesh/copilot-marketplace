---
model: sonnet
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, TodoWrite]
---

/postgresql:pg audit the live database. The connection is already configured through the PG* environment variables.
