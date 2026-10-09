# .NET review checklist

Check what the diff touches; skip sections that don't apply.

## Correctness
- Null handling: nullable reference warnings suppressed with `!` without reason; `FirstOrDefault()` result used without a check.
- Off-by-one, inverted conditions, missing `else`/`default` branches, swallowed exceptions (`catch { }`, `catch (Exception) { return null; }`).
- `DateTime.Now` vs `UtcNow`; `DateTime.Kind` mixing; culture-sensitive parse/format (`ToString()`/`Parse` without `CultureInfo.InvariantCulture` for machine data).
- Equality: `==` on strings with different casing rules, floating-point equality, `GetHashCode` overridden without `Equals`.

## Async and concurrency
- `.Result`, `.Wait()`, `GetAwaiter().GetResult()` on async code (deadlock risk in classic ASP.NET / UI contexts; thread-pool starvation in ASP.NET Core).
- `async void` outside event handlers; fire-and-forget tasks without error handling.
- Missing `CancellationToken` flow on I/O paths; `Task.Run` wrapping async I/O.
- Shared mutable state in singletons, static fields, or `HttpContext` captured across threads.

## Data access (EF Core, Dapper, ADO.NET)
- Queries in loops (N+1); `ToList()` before `Where` (filtering in memory); missing `AsNoTracking()` on read-only queries.
- String-concatenated SQL (injection). `FromSqlRaw` with interpolation must be `FromSqlInterpolated`/parameters.
- New queries on large tables without an index; migrations that lock big tables (see the postgresql plugin's migration-safety notes).
- `DbContext` lifetime: never singleton, never shared across threads.

## Security
- Secrets, connection strings, or tokens in code or committed config.
- Missing `[Authorize]` / policy on new endpoints; authorization checked on the client only; IDOR (resource ids not scoped to the caller).
- Unvalidated input reaching file paths, SQL, shell, redirects, or deserialization (`TypeNameHandling`, `BinaryFormatter`).
- Sensitive data in logs.

## API and compatibility
- Changed public signatures, DTO properties, JSON names, routes, or DB columns without callers and clients updated.
- Behavior changes without a test; deleted tests.

## Resources and performance
- `IDisposable` not disposed (`using`); `new HttpClient()` per call (use `IHttpClientFactory`).
- Large allocations in hot paths, `string +=` in loops, LINQ in tight loops, sync I/O in request paths.
