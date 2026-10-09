---
name: pg
description: PostgreSQL work - slow query tuning (EXPLAIN), index advice, schema review, lock-safe migrations (incl. EF Core), live diagnostics (locks, bloat, vacuum), Npgsql specifics. Loads one focused reference per task.
argument-hint: "[query | table | migration file | symptom]"
---
# PostgreSQL

Read only the reference that matches the task:

| Task | Read |
|---|---|
| Slow query, EXPLAIN output, pg_stat_statements | [query-tuning.md](query-tuning.md) |
| Which index to add or drop | [indexes.md](indexes.md) |
| Table and type design review | [schema-review.md](schema-review.md) |
| Migration or DDL review (EF Core or SQL) | [migration-safety.md](migration-safety.md) |
| Blocking, long transactions, bloat, vacuum, connections | [diagnose.md](diagnose.md) |
| Npgsql / EF Core provider behavior | [npgsql.md](npgsql.md) |

## Querying a live database
Without a database, work from the SQL, migrations, and code alone, and say that numbers are unverified.

Send SQL to `core:runner` as a work order. It runs **read-only at the server level**:
```text
WORK ORDER
goal: <what the numbers are for>
steps:
  1. PGOPTIONS="-c default_transaction_read_only=on -c statement_timeout=15000" psql -X -A -F'|' -P footer=off -v ON_ERROR_STOP=1 -c "<sql>" | head -n 60
return: rows as printed (at most 60 lines); for EXPLAIN, the full plan up to 80 lines
on-error: BLOCKED: <psql error line>
```
- Connection: psql reads the standard libpq settings (`PGSERVICE` + `pg_service.conf`, `PGHOST`/`PGDATABASE`/`PGUSER` + `.pgpass`, or a `DATABASE_URL` the user names). Never put a password in a command. If nothing is configured, ask the user for a service name.
- `EXPLAIN (ANALYZE, BUFFERS)` runs the statement. Use it only for SELECTs. For INSERT/UPDATE/DELETE use plain `EXPLAIN` (the read-only session rejects writes anyway).
- Batch several catalog queries into one work order rather than one runner per query.
- If `psql` isn't installed but a PostgreSQL MCP is available, run the same read-only SQL through the MCP, with `LIMIT`s, in the main session.

## Output
Lead with the finding and the change (SQL or C#), then the evidence (plan lines, stats), then how to verify. Keep it under 50 lines unless the user asks for more.
