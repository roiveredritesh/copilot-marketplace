---
model: sonnet
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, TodoWrite]
---

/sqlserver:mssql audit the Shop database on server sql01 (Windows auth). I can't answer questions during this run, so here are my decisions up front: Fix all. Orphaned OrderLines rows: delete them. Plan the identity change as its own file.
