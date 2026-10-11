# Schema audit and fix (live database)

Start with TodoWrite: one item per numbered section below. Mark each done, or skipped with the reason, before moving on.

## 1. Audit: in ONE message, dispatch both
- `core:runner`, two steps:
  1. `sqlcmd -S "<server>" -d <db> -E -b -h -1 -W -s "|" -t 60 -i "${CLAUDE_PLUGIN_ROOT}/skills/mssql/audit.sql"` → rows `severity|check|object|detail`, at most 120 lines.
  2. `sqlcmd -S "<server>" -d <db> -E -b -h -1 -W -Q "SET NOCOUNT ON; BEGIN TRAN; SELECT CONCAT(CAST(SERVERPROPERTY('Edition') AS nvarchar(128)), ' | ', CAST(SERVERPROPERTY('ProductVersion') AS nvarchar(128)), ' | compat ', compatibility_level) FROM sys.databases WHERE name = DB_NAME(); ROLLBACK;"` (the guard hook allows sqlcmd only inside a rolled-back transaction)
  Return both outputs as printed. `audit.sql` needs SQL Server 2017+ (STRING_AGG); on older versions it fails with a syntax error, and you say so.
- `core:scout`: "scope: the whole repo | terms: DbContext, OnModelCreating, IEntityTypeConfiguration, Migrations/, .edmx, DbUp, *.sqlproj, .sql migration folders. Return at most 30 lines: the EF Core (or EF6) context and configuration files (path), the migrations folder, any SQL project or migration tool and its folder, and the EF provider and version from the project file."

## 2. Verify and rank (main session)
- **Online operations:** `ONLINE = ON` exists only on Enterprise, Developer, and Azure SQL. Read the edition from step 2. On Standard and Express, every index and table change below is offline.
- **Check dependencies before proposing a fix:** send one runner work order of rolled-back SELECTs.
  - `missing_fk_candidate` / `untrusted_fk`: the orphan count, `SELECT COUNT(*) FROM <child> c WHERE c.<col> IS NOT NULL AND NOT EXISTS (SELECT 1 FROM <parent> p WHERE p.Id = c.<col>)`.
  - NOT NULL changes: the null count.
  - Table size for anything that rebuilds: `SELECT SUM(row_count) FROM sys.dm_db_partition_stats WHERE object_id = OBJECT_ID('<t>') AND index_id IN (0, 1)`.
  - Columns being retyped: their indexes, default constraints, and computed columns (`sys.index_columns`, `sys.default_constraints`).
- **Group the findings:**
  - **must fix:** integrity, overflow, float money.
  - **should fix:** FK without index, untrusted FK, heap, deprecated types.
  - **optional:** datetime → datetime2, money type.

## 3. Gate: AskUserQuestion
Show `# | severity | object | problem | fix | lock/rebuild impact`. Use exactly these options: `Fix all` / `Fix some` ("type the numbers in Other") / `Report only` / `Cancel`. Ask a decision question for business choices: the `datetime2` precision, and orphans. **Offer only actions that are valid for the column:** set NULL only when it is nullable. The others are delete the rows, reassign them to an existing parent, or skip the FK.

## 4. Write the fix (never run it against the database)
- **EF Core repo:** change the model (`HasIndex`, `HasPrecision(18, 2)`, `HasColumnType("datetime2(3)")`, `HasOne().WithMany().HasForeignKey()`, `HasKey`), then `dotnet ef migrations add <Name>` if `dotnet-ef` is installed. If it isn't, hand-write the migration in the repo's style. Raw steps go through `migrationBuilder.Sql(...)`.
- **EF6 / database-first (.edmx):** write the SQL scripts and list the model refresh steps.
- **SQL project or migration tool:** add the change in its folder and naming scheme.
- **Neither:** write `.reports/schema-fix-<yyyymmdd>/` with `00-precheck.sql`, `01-up.sql`, and `02-down.sql` (plus separate files for window-only work such as an identity change). Before the first write, keep `.reports/` out of git: `p=$(git rev-parse --git-path info/exclude); grep -qx .reports/ "$p" 2>/dev/null || echo .reports/ >> "$p"`.

Start every script with `SET XACT_ABORT ON; SET LOCK_TIMEOUT 5000;`, so blocked DDL fails fast instead of queueing every query behind it.
- **Fail before changing anything.** Wrap each up script in `BEGIN TRAN ... COMMIT`, and open it with the precheck conditions as assertions: `IF (SELECT COUNT(*) FROM ...) <> 0 THROW 50001, 'precheck: ...', 1;`. Data fixes (orphans, nulls) go in the **same** transaction as the constraints that need them, so a failure leaves the data untouched too.
- **Never hard-code system-generated names** (`PK__Tickets__3214EC07...`, `DF__...`, `FK__...`). They differ in every environment. Look them up at run time, e.g. `DECLARE @pk sysname = (SELECT name FROM sys.key_constraints WHERE parent_object_id = OBJECT_ID('dbo.Tickets') AND type = 'PK'); DECLARE @sql nvarchar(max) = N'ALTER TABLE dbo.Tickets DROP CONSTRAINT ' + QUOTENAME(@pk); EXEC sys.sp_executesql @sql;` (build the statement in a variable first: `EXEC('...' + QUOTENAME(...))` is a syntax error). Give every constraint you create an explicit name.

| Finding | Fix | Impact |
|---|---|---|
| fk_without_index | `CREATE INDEX IX_<T>_<Cols> ON <t> (<cols>)`, adding `WITH (ONLINE = ON)` where the edition allows it | Offline nonclustered build: reads continue, writes wait |
| missing_fk_candidate | Index the column first. Handle the orphans (the user's choice). Then `ALTER TABLE <t> WITH CHECK ADD CONSTRAINT FK_<T>_<P> FOREIGN KEY (<col>) REFERENCES <p>(Id)`. Never `WITH NOCHECK`: the constraint ends up untrusted and the optimizer ignores it | Validation scans the child table under a schema lock |
| untrusted_fk / untrusted_check | Fix the violating rows (count them first), then `ALTER TABLE <t> WITH CHECK CHECK CONSTRAINT <name>` | Same scan and lock as above: run it in a quiet window |
| heap / no_primary_key | `ALTER TABLE <t> ADD CONSTRAINT PK_<T> PRIMARY KEY CLUSTERED (<key>)`. With no natural key, first add `Id bigint IDENTITY NOT NULL` | Rebuilds the table and every nonclustered index; offline unless ONLINE |
| duplicate_index | `DROP INDEX <redundant> ON <t>`. Keep the one backing a constraint or used by hints | Brief schema lock |
| disabled_index | `ALTER INDEX <ix> ON <t> REBUILD` if it's needed, else `DROP INDEX` | Rebuild cost |
| float_money | `ALTER TABLE <t> ALTER COLUMN <col> decimal(18, 2) NOT NULL` (keep the existing nullability). First drop and later recreate the dependent indexes and defaults | Size-of-data change under a schema-modification lock. For large tables: new column, batch backfill, swap |
| deprecated_type | `ntext` → `nvarchar(max)`, `text` → `varchar(max)`, `image` → `varbinary(max)` via `ALTER COLUMN`. Optionally follow with `UPDATE <t> SET <col> = <col>` to move small values in-row (heavy log; batch it) | Schema-modification lock |
| datetime_not_datetime2 | `ALTER COLUMN <col> datetime2(3)` (keep nullability). Drop and recreate the default constraint around it | Size-of-data change; `datetime` values round to 3.33 ms, so `datetime2(3)` loses nothing |
| identity_near_max | Plan it as its own migration: `int` → `bigint` on the PK and every referencing FK column (drop and recreate the PK, FKs, and indexes). Short-term relief only: `DBCC CHECKIDENT('<t>', RESEED, -2147483648)`, if negative ids are acceptable to the app | Large rebuild; needs a window |
| nullable_fk → NOT NULL | Check the null count, then `ALTER TABLE <t> ALTER COLUMN <col> <type> NOT NULL` | Scans the table under a schema lock |

Every up step gets a down step, or a note saying it can't be undone (deleted orphans).

## 5. Check the fix
Review your own scripts against [migration-safety.md](migration-safety.md). Then report: findings fixed or skipped, files written, the lock and rebuild impact per step, the edition caveats, and how to apply (staging first, in a window when marked). Offer a re-audit after the user applies it.
Last line, always: `Steps: audit=<n findings> gate=<asked: choice> files=<paths> db-writes=none self-review=<done>`. Fill every key; write `skipped (<reason>)` rather than leaving one out.
