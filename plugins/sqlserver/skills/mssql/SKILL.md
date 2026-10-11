---
name: mssql
description: SQL Server work - live schema audit and fix migrations (EF Core or SQL), and migration/DDL safety review. Read-only sqlcmd queries run by a Haiku runner. Loads one focused reference per task.
argument-hint: "[audit | migration file | table]"
disable-model-invocation: true
---
# SQL Server

Read only the reference that matches the task:

| Task | Read |
|---|---|
| Audit a live database and write fix migrations (`audit`) | [schema-fix.md](schema-fix.md) |
| Migration or DDL review (EF Core or SQL) | [migration-safety.md](migration-safety.md) |

## Querying a live database
Without a database, work from the SQL, migrations, and code alone, and say that findings are unverified.

Connection: ask once for the server and database if they aren't known (CLAUDE.md, `appsettings*.json` connection strings, or the user). Examples: `(localdb)\MSSQLLocalDB`, `.\SQLEXPRESS`, `db01.corp.local`.
- **Windows authentication (`-E`)** is preferred.
- **SQL logins:** use `-U <user>` with the password in the `SQLCMDPASSWORD` environment variable, which the user sets. Never put a password in a command or a file.
- **Recommend a read-only login** (`db_datareader` + `VIEW DEFINITION`). sqlcmd has no session-level read-only switch, so the login is the real guarantee.

Send SQL to `core:runner` as a work order. Every ad-hoc query runs inside a transaction that is rolled back:
```text
WORK ORDER
goal: <what the rows are for>
steps:
  1. sqlcmd -S "<server>" -d <db> -E -b -h -1 -W -s "|" -t 30 -Q "SET NOCOUNT ON; SET LOCK_TIMEOUT 5000; BEGIN TRAN; <select>; ROLLBACK;" | head -n 60
return: rows as printed (at most 60 lines)
on-error: BLOCKED: <sqlcmd error line>
```
- Only SELECTs against tables and `sys.*` views. Never DDL, DML, or `EXEC`, even inside the rolled-back transaction.
- Batch several queries into one work order rather than one runner per query.
- If `sqlcmd` isn't installed, ask the user to install it (the `go-sqlcmd` or ODBC tools). Don't fall back to a GUI or an MCP in the main session.

## Output
Lead with the finding and the change (SQL or C#), then the evidence, then how to verify. Keep it under 50 lines unless the user asks for more.
