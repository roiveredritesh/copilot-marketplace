# Migration safety (SQL Server)

Read the migration (EF Core: `dotnet ef migrations script <from> <to>` for the real SQL) and flag:

| Pattern | Risk | Safer approach |
|---|---|---|
| `ALTER COLUMN` changing type, length, or nullability | Size-of-data change under a schema-modification lock; fails if indexes or defaults depend on it | New column → batch backfill → swap, or schedule a window |
| `CREATE INDEX` without `ONLINE = ON` on a busy table | Writes wait for the whole build | `ONLINE = ON` (Enterprise, Developer, Azure SQL), otherwise a quiet window |
| `ADD CONSTRAINT ... FOREIGN KEY` / `CHECK` on a large table | Validation scan under a schema lock | Clean the data first, then add it `WITH CHECK` in a window. Never leave it `WITH NOCHECK` (untrusted) |
| New `NOT NULL` column | The default and edition decide whether it's instant or a rewrite | Add it as NULL, backfill in batches, then make it NOT NULL. Or add a runtime-constant default and verify the cost on a copy |
| `DROP COLUMN` / `DROP TABLE` / renames | Breaks running app versions during a rolling deploy | Expand → migrate → contract across releases. `sp_rename` breaks dependent code |
| Clustered index or PK change | Rebuilds the table and all nonclustered indexes | Its own migration, in a window |
| Large `UPDATE` / `DELETE` in a migration | Long transaction, log growth, lock escalation (5,000+ locks) | Batches of 1,000–5,000 rows in a loop, outside the schema migration |
| Data migration and DDL in one transaction | Long-held locks | Separate them |
| Missing `SET XACT_ABORT ON` in raw scripts | A partial failure leaves an open transaction | Add `SET XACT_ABORT ON; SET LOCK_TIMEOUT 5000;` |

EF Core specifics:
- Check `Down()`: generated drops of columns or tables lose data.
- Look for column renames that EF scaffolded as drop + add (data loss). Use `RenameColumn`.
- `HasDefaultValueSql` vs `HasDefaultValue`: confirm that the default for existing rows is what the app expects.

Report each finding as `[high|med|low] <statement or file:line> - risk - safer version`.
