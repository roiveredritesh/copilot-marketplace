# Schema audit and fix (live database)

## 1. Audit: in ONE message, dispatch both
- `core:runner`: `PGOPTIONS="-c default_transaction_read_only=on -c statement_timeout=30000" psql -X -A -t -F'|' -v ON_ERROR_STOP=1 -f "${CLAUDE_PLUGIN_ROOT}/skills/pg/audit.sql"` → return the rows as printed, at most 120 lines. It returns `severity|check|object|detail`.
- `core:scout`: "scope: the whole repo | terms: DbContext, OnModelCreating, IEntityTypeConfiguration, Migrations/, .sql migration folders (Flyway V*__*.sql, DbUp, sqitch). Return at most 30 lines: the EF Core context and entity configuration files (path), the migrations folder, any SQL migration tool and its folder, and the Npgsql version from the .csproj."

## 2. Verify and rank (main session)
- `unused_index` means nothing on a fresh database, a replica, or right after a stats reset. Report it as "check in production", never as "drop".
- Before proposing a fix, check what it depends on. Send one runner work order with these SELECTs:
  - `missing_fk_candidate`: the orphan count, `SELECT count(*) FROM <child> c WHERE c.<col> IS NOT NULL AND NOT EXISTS (SELECT 1 FROM <parent> p WHERE p.id = c.<col>)`.
  - `nullable_fk` → NOT NULL: the null count.
  - `no_primary_key`: whether a candidate key is unique and NOT NULL.
  - Table sizes for anything that rewrites: `pg_total_relation_size`.
- Group the findings: **must fix** (data integrity, imminent overflow, float money), **should fix** (missing FK index, untrusted constraint, timestamp without time zone), **optional** (json, serial, char(n)).

## 3. Gate: AskUserQuestion
Show `# | severity | object | problem | fix | lock/rewrite impact`. Use exactly these options: `Fix all` / `Fix some` ("type the numbers in Other") / `Report only` / `Cancel`. Ask a decision question for anything with a business choice: orphans (delete them, set NULL, or keep and skip the FK) and the time zone stored in `timestamp` columns.

## 4. Write the fix (never run it against the database)
- **EF Core repo:** change the model (`HasIndex`, `HasColumnType("timestamptz")`, `HasPrecision(18, 2)`, `HasOne().WithMany().HasForeignKey()`), then `dotnet ef migrations add <Name>` if `dotnet-ef` is installed. If it isn't, hand-write the migration in the repo's migration style. Wrap the non-transactional steps in `migrationBuilder.Sql("...", suppressTransaction: true)`.
- **SQL migration tool:** add the next file in its folder and naming scheme.
- **Neither:** write `.reports/schema-fix-<yyyymmdd>/` with `00-precheck.sql`, `01-up.sql`, and `02-down.sql`.

Lock-safe patterns:

| Finding | Fix |
|---|---|
| fk_without_index | `CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_<t>_<cols> ON <t> (<cols>);` (outside a transaction) |
| missing_fk_candidate | Index the column first. Then `ALTER TABLE <t> ADD CONSTRAINT fk_<t>_<col> FOREIGN KEY (<col>) REFERENCES <p>(id) NOT VALID;` and, after the orphans are handled, `ALTER TABLE <t> VALIDATE CONSTRAINT fk_<t>_<col>;` (SHARE UPDATE EXCLUSIVE, so writes continue) |
| constraint_not_validated | Fix the violating rows (count them first), then `VALIDATE CONSTRAINT` |
| nullable_fk → NOT NULL | `ADD CONSTRAINT <c>_nn CHECK (<col> IS NOT NULL) NOT VALID;` → `VALIDATE CONSTRAINT` → `ALTER COLUMN <col> SET NOT NULL` (PG 12+ skips the scan) → drop the check |
| no_primary_key | `CREATE UNIQUE INDEX CONCURRENTLY` on the key, then `ADD CONSTRAINT <t>_pkey PRIMARY KEY USING INDEX <ix>`. With no natural key, add `id bigint GENERATED ALWAYS AS IDENTITY` (rewrites the table: plan a window) |
| duplicate_index | `DROP INDEX CONCURRENTLY <redundant>`. Keep the one that backs a constraint |
| invalid_index | `DROP INDEX CONCURRENTLY <ix>`, then recreate it with `CONCURRENTLY` |
| float_money | `ALTER COLUMN <col> TYPE numeric(18,2) USING round(<col>::numeric, 2)`. This rewrites the table under ACCESS EXCLUSIVE. For a large table, add a new column, backfill in batches, then swap |
| timestamp_without_tz | `ALTER COLUMN <col> TYPE timestamptz USING <col> AT TIME ZONE '<stored zone>'`. Same rewrite caveat. Npgsql 6+ then maps it to UTC `DateTime` |
| sequence_near_max | `ALTER TABLE <t> ALTER COLUMN id TYPE bigint` (a rewrite, and the FK columns pointing at it too) and `ALTER SEQUENCE <s> AS bigint`. Plan it as its own migration with a window |
| json_not_jsonb, serial_not_identity, char_n | Optional. Same rewrite caveats; usually batch them with other planned work |

Every up step gets a down step, or a note saying it can't be undone (data deleted with orphans). Put `SET lock_timeout = '5s';` at the top of transactional scripts, so a blocked DDL fails fast instead of queueing writes behind it.

## 5. Check the fix
Review your own migration against [migration-safety.md](migration-safety.md). Then report: findings fixed or skipped, files written, the lock and rewrite impact of each step, and how to apply it (staging first). Offer a re-audit after the user applies it.
