# Npgsql and EF Core on PostgreSQL

## Date and time (Npgsql 6+)
- `timestamptz` ↔ `DateTime` with `Kind=Utc` (or `DateTimeOffset` with offset 0). Writing a `Local` or `Unspecified` DateTime to `timestamptz` throws.
- `timestamp` (without time zone) ↔ `DateTime` with `Kind=Unspecified`/`Local`.
- The fix is to normalize to UTC at the boundary, not to set `Npgsql.EnableLegacyTimestampBehavior` (a temporary escape hatch only).
- `DateOnly`/`TimeOnly` map to `date`/`time`.

## Connections and pooling
- The pool is per connection string per process: `Maximum Pool Size` (default 100) × app instances must stay under the server's `max_connections`, or go through PgBouncer.
- With PgBouncer in transaction mode: disable prepared-statement-dependent features, or use PgBouncer 1.21+ with prepared statement support. Set `No Reset On Close=true` only if you understand the session-state implications.
- `NpgsqlDataSource` (Npgsql 7+) is the modern entry point: build it once (singleton) and register it with `AddNpgsqlDataSource`.
- Transient failures: `UseNpgsql(cs, o => o.EnableRetryOnFailure())`. Retries require transactions to be wrapped in the execution strategy.

## Mapping
- Naming: `UseSnakeCaseNamingConvention()` (EFCore.NamingConventions) to avoid quoted PascalCase identifiers.
- `jsonb`: map POCOs with `.ToJson()` (EF 8+ owned JSON) or `HasColumnType("jsonb")`; LINQ over JSON properties translates to `->>` / `@>`.
- Arrays: `List<T>`/`T[]` map to PostgreSQL arrays, and `Contains` translates to `= ANY(...)`.
- Enums: map to PostgreSQL enums with `MapEnum<T>()` on the data source, or store them as text with a check constraint.
- Concurrency token: the `xmin` system column (configuration varies by Npgsql version; check the provider docs for yours).
- Case-insensitive comparisons: `EF.Functions.ILike(...)`, `citext` columns, or collations. `ToLower()` in queries needs a matching expression index.

## Bulk and performance
- Large inserts: binary COPY (`NpgsqlConnection.BeginBinaryImport`) is 10–100x faster than `SaveChanges`.
- Very many tiny commands: Npgsql batches statements in one round-trip with `NpgsqlBatch`, and EF batches `SaveChanges` automatically.
- Multiplexing (`Multiplexing=true`) can raise throughput for high-concurrency apps with short queries. Not compatible with some features (e.g. transaction-scoped session state).
