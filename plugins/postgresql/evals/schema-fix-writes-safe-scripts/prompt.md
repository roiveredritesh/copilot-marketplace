---
model: sonnet
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, TodoWrite]
---

/postgresql:pg audit the live database. The connection is already configured through the PG* environment variables. I can't answer questions during this run, so here are my decisions up front: Fix all, except leave unused_index alone. Orphaned order_lines rows: delete them. The timestamp column stores UTC. Put the sequence change in its own file.
