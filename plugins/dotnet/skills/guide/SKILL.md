---
name: guide
description: .NET performance and correctness guidance - EF Core queries and migrations, ASP.NET Core (DI, middleware, HttpClient), async and C# performance. Load the one reference that matches the task.
paths: "**/*.cs, **/*.csproj, **/appsettings*.json"
disable-model-invocation: true
---
# .NET guide

Read only the reference that matches the task:

| Task | Read |
|---|---|
| EF Core queries, N+1, tracking, migrations, DbContext lifetime, raw SQL | [efcore.md](efcore.md) |
| ASP.NET Core: DI lifetimes, middleware order, HttpClient, options, auth, errors | [aspnetcore.md](aspnetcore.md) |
| async/await pitfalls, allocations, collections, hot paths | [csharp-perf.md](csharp-perf.md) |

Rules that always apply:
- Measure before optimizing: log the generated SQL (`ToQueryString()`), use `dotnet-counters` or `dotnet-trace`, or BenchmarkDotNet for micro-benchmarks.
- Prefer the framework's built-in feature over a new dependency.
- After a change, verify with `/dotnet:build test`.
