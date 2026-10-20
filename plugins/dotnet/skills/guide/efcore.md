# EF Core

## Check the version first
- Read the `Microsoft.EntityFrameworkCore*` package version (csproj or `Directory.Packages.props`) before using an API marked "EF n+" below. Don't suggest an upgrade just to use one.
- `System.Data.Entity` / `EntityFramework` 6.x is EF6, a different library. `AsSplitQuery`, `ExecuteUpdate`, `ToQueryString`, and `FromSql` don't exist there, and lazy loading is on by default (virtual navigations). `AsNoTracking` and `Include` do exist.

## Read queries
- Read-only entity queries: `AsNoTracking()` (or `AsNoTrackingWithIdentityResolution()` (EF 5+) when the same entity repeats in a graph). For a read-heavy context, set `UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking)` and opt in with `AsTracking()`.
- Project to what you need: `.Select(x => new Dto { ... })` rather than loading entities and mapping in memory. A projection also makes `Include` unnecessary. A projection of scalars isn't tracked, so `AsNoTracking()` adds nothing there, but entity instances inside a projection (`new { o, o.Customer }`) are tracked.
- Write the projection inline or as an `Expression<Func<T, Dto>>`. `Select(x => MapToDto(x))` with a C# method can't be translated, so EF loads every column of the entity and maps in memory.
- Filter, sort, and page in the database: `Where`, `OrderBy`, `Skip`/`Take` before `ToList()`. `AsEnumerable()` or `ToList()` before `Where` pulls the whole table.
- Large result sets: stream with `AsAsyncEnumerable()`. Keyset pagination (`WHERE Id > @last ORDER BY Id`) instead of large `Skip`.
- Existence checks: `AnyAsync()`, not `CountAsync() > 0` and not loading the row.
- Use the async operators (`ToListAsync`, `FirstOrDefaultAsync`) in request paths and pass the `CancellationToken`.

## LINQ translation
- Untranslatable expressions throw (EF 3+) unless they sit in the final `Select`. Rewrite them in a translatable form; don't add `AsEnumerable()`/`ToList()` earlier to make the error go away.
- Keep `IQueryable<T>` and `Expression<Func<T, bool>>` in repository and helper signatures. A `Func<T, bool>` predicate or an `IEnumerable<T>` parameter binds to `Enumerable.Where` and filters in memory after loading the table.
- String comparisons: `string.Equals(a, b, StringComparison.X)` doesn't translate. `x.Name.ToLower() == s` translates but can't use a plain index on the column. Rely on the column collation, or use `EF.Functions.Collate` (EF 5+) or `EF.Functions.ILike` (Npgsql).
- `list.Contains(x.Id)` becomes `IN`. On SQL Server, EF 8 and 9 send the list as one JSON parameter (`OPENJSON`), which needs compatibility level 130 or higher; on older databases configure `UseCompatibilityLevel(120)`.
- Query plans are cached by expression shape. Use variables, not values spliced into dynamically built expressions, so EF parameterizes them.

## Pagination
- Every list endpoint pages on the server, unless the list is small and bounded (a lookup table). Clamp the client's page size to a server-side maximum, and reject `page < 1`.
- `Skip`/`Take` need an `OrderBy` with a unique key (add `.ThenBy(x => x.Id)` as a tie-breaker), or rows repeat or vanish between pages. EF logs a warning when the `OrderBy` is missing.
- Default shape: `Where` → `OrderBy` → `Skip`/`Take` → `Select` → `ToListAsync`.

## N+1 and includes
- Symptom: one query per row in the logs. Without lazy loading (off by default in EF Core), an unloaded navigation is `null`, not an extra query. N+1 comes from lazy-loading proxies, explicit `Entry(x).Reference(...).LoadAsync()`, or a query inside a loop.
- Fix: `Include`/`ThenInclude`, or a projection (preferred when only some fields are needed). Filtered includes (`Include(x => x.Items.Where(...))`, EF 5+) load part of a collection.
- With two or more collection includes, use `AsSplitQuery()` (EF 5+) to avoid a cartesian explosion; set `UseQuerySplittingBehavior` globally if it's common. One collection include is usually fine as a single query. Split queries run several round trips and aren't a consistent snapshot unless they run in a serializable or snapshot transaction.
- Disable lazy loading unless there's a clear reason to keep it. In Web APIs, load related data explicitly.

## Writes
- Bulk changes: `ExecuteUpdateAsync` / `ExecuteDeleteAsync` (EF 7+) instead of load-modify-save loops. In EF 10+ `ExecuteUpdateAsync` takes a regular lambda, so setters can be added conditionally.
- They run immediately, outside `SaveChanges`. They skip the change tracker (tracked entities go stale), `SaveChanges` interceptors and auditing, and the `SaveChanges` transaction. Don't use them where auditing, domain events, or soft-delete logic run through `SaveChanges`. To combine them with `SaveChanges` atomically, wrap both in `BeginTransactionAsync`.
- Batch inserts: `AddRange` + one `SaveChangesAsync`. For very large loads, use the provider's bulk API (Npgsql binary COPY, `SqlBulkCopy`).
- Concurrency: use a concurrency token (`[Timestamp]` on SQL Server; on PostgreSQL the `xmin` system column, configured per your Npgsql version) and handle `DbUpdateConcurrencyException`.

## Indexes
- Columns that are filtered, joined, or sorted often need an index: `HasIndex(x => new { x.CustomerId, x.CreatedAt })` or `[Index]` (EF 5+). EF creates indexes on foreign keys itself.
- Every index slows writes and costs storage. Add one for a real query pattern, not for every column.

## Seeing the SQL
- `query.ToQueryString()` (EF 5+), or `LogTo(Console.WriteLine, LogLevel.Information)` (EF 5+) plus `EnableSensitiveDataLogging()` in development only. Check the SQL and measure before and after an optimization.
- Compiled queries (`EF.CompileAsyncQuery`) only for a hot path where measurement shows translation cost matters. EF already caches translated queries.

## Raw SQL
- `FromSql($"... {param}")` (EF 7+), `FromSqlInterpolated`, and `Database.SqlQuery<T>` (EF 7+ scalars, EF 8+ unmapped types) are parameterized. `FromSqlRaw` with string concatenation is SQL injection.

## DbContext lifetime
- Scoped (one per request). Never a singleton, never shared across threads or parallel tasks. For background work, use `IDbContextFactory<T>` and create one per unit of work.
- `AddDbContextPool` for high-throughput apps. The context must hold no state between uses.

## Migrations
- One logical change per migration. Review the generated SQL with `dotnet ef migrations script <from> <to> --idempotent`.
- Renames: EF may generate drop + add, which loses data. Check, and use `RenameColumn`.
- Creating an index on a big table, adding a NOT NULL column, or changing a type risks locks and table rewrites. On PostgreSQL see `postgresql:pg` → migration-safety (`CONCURRENTLY` needs `migrationBuilder.Sql(..., suppressTransaction: true)`).
- Apply migrations in the deploy pipeline with a bundle (`dotnet ef migrations bundle`) or a script. Avoid `Database.Migrate()` at app startup when several instances may start at once.
