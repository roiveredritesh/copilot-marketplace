# Async and C# performance

## Async
- Async all the way down. `.Result`, `.Wait()`, and `GetAwaiter().GetResult()` deadlock in classic ASP.NET and UI apps (which have a SynchronizationContext) and starve the thread pool in ASP.NET Core.
- `ConfigureAwait(false)` in library code that may run under a SynchronizationContext (.NET Framework apps, WinForms/WPF). ASP.NET Core app code doesn't need it.
- `async void` only for event handlers. For fire-and-forget, hand the work to a queue or a `BackgroundService`, or at least observe its exceptions.
- `ValueTask` only on hot paths that usually complete synchronously. Never await a `ValueTask` twice.
- Parallel I/O: `Task.WhenAll` over a bounded set, or `Parallel.ForEachAsync` with `MaxDegreeOfParallelism`. Wrapping async I/O in `Task.Run` adds nothing.
- Pass a `CancellationToken` through every async I/O call.

## Allocations and hot paths
- Use `StringBuilder`, `string.Create`, or interpolated string handlers instead of `+=` in loops.
- Use `Span<T>` / `ReadOnlySpan<char>` for parsing and slicing, and `ArrayPool<T>.Shared` for large temporary buffers.
- Use plain loops instead of LINQ in tight loops, which allocate enumerators and delegates.
- Avoid boxing: use generic constraints instead of `object`, and keep value types out of non-generic collections.
- `static` lambdas avoid closure allocations. Cache delegates that are used repeatedly.

## Collections
- Pre-size them: `new List<T>(capacity)`, `new Dictionary<K,V>(capacity)`.
- Use `Dictionary`/`HashSet` lookups (O(1)) instead of `List.Contains` inside loops (O(n²) overall).
- Read-mostly lookup tables: `FrozenDictionary` / `FrozenSet` (.NET 8+).
- Use `StringComparer.Ordinal` / `OrdinalIgnoreCase` for keys that aren't human-language text.

## Measuring
- BenchmarkDotNet with `[MemoryDiagnoser]` for micro-benchmarks. `dotnet-counters monitor` for live GC, thread-pool, and exception rates. `dotnet-trace` with PerfView or Speedscope for CPU.
- On .NET Framework, use PerfView. Expect the gains from `async` and `Span` to be smaller than on modern .NET.
