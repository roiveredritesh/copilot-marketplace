# Lock-safe migrations

Any DDL takes a lock. An `ACCESS EXCLUSIVE` lock waiting behind a long transaction blocks **every** later query on that table. Always set a lock timeout in migrations:
```sql
SET lock_timeout = '5s';   -- fail fast and retry, instead of queueing the whole app
SET statement_timeout = '15min';
```

| Operation | Risk | Safe pattern |
|---|---|---|
| `CREATE INDEX` | blocks writes for the whole build | `CREATE INDEX CONCURRENTLY` (can't run in a transaction). Check `pg_index.indisvalid` afterwards, and drop/retry if invalid |
| `DROP INDEX` | ACCESS EXCLUSIVE | `DROP INDEX CONCURRENTLY` |
| `ADD COLUMN` nullable, or with a constant default | fast (11+) | fine |
| `ADD COLUMN ... DEFAULT now()/random()` (volatile) | full table rewrite | add nullable → backfill in batches → set default |
| `SET NOT NULL` | full scan under ACCESS EXCLUSIVE | `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID` → `VALIDATE CONSTRAINT c` → `SET NOT NULL` (12+ uses the check) → drop the check |
| `ADD FOREIGN KEY` | scan, locks both tables | `ADD CONSTRAINT ... NOT VALID` → `VALIDATE CONSTRAINT` separately |
| `ADD CHECK` | full scan under lock | `NOT VALID` → `VALIDATE` |
| `ALTER COLUMN TYPE` | usually a full rewrite (except e.g. varchar(n) → larger/text) | new column → dual write / backfill → swap |
| `RENAME COLUMN/TABLE` | instant, but breaks running app versions | expand/contract: add new → deploy code that uses both → remove old |
| large `UPDATE`/`DELETE` backfill | long transaction, bloat, replication lag | batches of 1–10k rows by key, commit each, pause between them |

## EF Core specifics
- EF wraps each migration in a transaction, and `CONCURRENTLY` fails inside one. Use raw SQL with the transaction suppressed:
  ```csharp
  migrationBuilder.Sql("CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_orders_customer ON orders (customer_id);", suppressTransaction: true);
  ```
  Keep such statements in their own migration.
- Review the SQL before applying it: `dotnet ef migrations script <from> <to> --idempotent`. Look for drop+add where a rename was intended, `ALTER COLUMN TYPE`, and `NOT NULL` on existing tables.
- Data backfills belong in a separate step or job, not inside the schema migration.
- Deploy order: schema expand → app deploy → backfill → schema contract (in a later release).

## Pre-flight check (send to runner)
```sql
SELECT pid, now()-xact_start AS xact_age, state, left(query,80) AS query
FROM pg_stat_activity WHERE xact_start IS NOT NULL ORDER BY xact_start LIMIT 10;
```
Don't run DDL while a long transaction holds the table.
