# EF Core

## Read queries
- Read-only: `AsNoTracking()` (or `AsNoTrackingWithIdentityResolution()` when the same entity repeats in a graph).
- Project to what you need: `.Select(x => new Dto { ... })` rather than loading entities and mapping in memory. A projection also makes `Include` unnecessary.
- Filter, sort, and page in the database: `Where`, `OrderBy`, `Skip`/`Take` before `ToList()`. `AsEnumerable()` or `ToList()` before `Where` pulls the whole table.
- Large result sets: stream with `AsAsyncEnumerable()`. Keyset pagination (`WHERE Id > @last ORDER BY Id`) instead of large `Skip`.
- Existence checks: `AnyAsync()`, not `CountAsync() > 0` and not loading the row.

## N+1 and includes
- Symptom: one query per row in the logs, or lazy-loading proxies accessed in a loop.
- Fix: `Include`/`ThenInclude`, or a projection. With several collection includes, use `AsSplitQuery()` to avoid a cartesian explosion (set `UseQuerySplittingBehavior` globally if it's common).
- Disable lazy loading unless there's a clear reason to keep it.

## Writes
- Bulk changes: `ExecuteUpdateAsync` / `ExecuteDeleteAsync` (EF 7+) instead of load-modify-save loops.
- Batch inserts: `AddRange` + one `SaveChangesAsync`. For very large loads, use the provider's bulk API (Npgsql binary COPY).
- Concurrency: use a concurrency token (`[Timestamp]` on SQL Server; on PostgreSQL the `xmin` system column, configured per your Npgsql version) and handle `DbUpdateConcurrencyException`.

## Seeing the SQL
- `query.ToQueryString()`, or `LogTo(Console.WriteLine, LogLevel.Information)` plus `EnableSensitiveDataLogging()` in development only.
- Very frequent identical queries: `EF.CompileAsyncQuery` saves translation cost.

## Raw SQL
- `FromSql($"... {param}")`, `FromSqlInterpolated`, and `SqlQuery<T>` are parameterized. `FromSqlRaw` with string concatenation is SQL injection.

## DbContext lifetime
- Scoped (one per request). Never a singleton, never shared across threads or parallel tasks. For background work, use `IDbContextFactory<T>` and create one per unit of work.
- `AddDbContextPool` for high-throughput apps. The context must hold no state between uses.

## Migrations
- One logical change per migration. Review the generated SQL with `dotnet ef migrations script <from> <to> --idempotent`.
- Renames: EF may generate drop + add, which loses data. Check, and use `RenameColumn`.
- Creating an index on a big table, adding a NOT NULL column, or changing a type risks locks and table rewrites. On PostgreSQL see `postgresql:pg` → migration-safety (`CONCURRENTLY` needs `migrationBuilder.Sql(..., suppressTransaction: true)`).
- Apply migrations in the deploy pipeline with a bundle (`dotnet ef migrations bundle`) or a script. Avoid `Database.Migrate()` at app startup when several instances may start at once.
