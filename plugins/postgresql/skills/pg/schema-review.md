# Schema review

## Types
- Text: `text` (or `varchar(n)` only when a real limit is a business rule). They perform the same in PostgreSQL.
- Time: `timestamptz` for instants (store UTC); `timestamp` without a time zone only for wall-clock values like "store opens 09:00". `date` for dates.
- Money: `numeric(p,s)`, never `float`/`real`/`double`. Avoid the `money` type (locale-dependent).
- Ids: `bigint GENERATED ALWAYS AS IDENTITY` (not `serial`). `uuid`: prefer time-ordered UUIDv7 for insert locality.
- Booleans: `boolean`, not `int` flags. Enums: a lookup table or a `CHECK` constraint. Native `enum` types are hard to change (values can't be removed).
- Case-insensitive text (emails, usernames): `citext`, or a nondeterministic ICU collation, or an expression index on `lower()` with queries matching it.
- `jsonb` (not `json`) for semi-structured data. Promote frequently filtered keys to real columns.

## Integrity
- `NOT NULL` by default; nullable only when "unknown" is a real state.
- Foreign keys with explicit `ON DELETE` behavior, and an index on the referencing column.
- `UNIQUE` constraints for business keys (also with a soft delete: a partial unique index `WHERE deleted_at IS NULL`).
- `CHECK` constraints for ranges and states. They are cheap, and the database enforces them even when the app forgets.

## Naming and EF Core
- snake_case identifiers avoid quoting (`"OrderId"` must always be quoted). In EF Core, use `EFCore.NamingConventions` → `UseSnakeCaseNamingConvention()`. Decide this before the first migration.
- Name constraints and indexes explicitly when you'll reference them in operations.

## Scale signals
- Tables expected over ~100M rows or with time-based retention: consider declarative partitioning (range on time). The partition key must be part of the primary key.
- Very wide rows with rarely read large columns: move them to a side table.
- Hot counters updated by many sessions: avoid a single-row counter (lock contention). Use per-shard rows or compute on read.
