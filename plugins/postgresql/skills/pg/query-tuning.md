# Query tuning

## Get the plan
- `EXPLAIN (ANALYZE, BUFFERS, SETTINGS) <select>`. Use plain `EXPLAIN` for writes, or when the query is too slow to run.
- From EF Core: get the SQL with `ToQueryString()` or the command log, and replace parameters with realistic values (the plan depends on them).

## Read the plan, bottom-up
| Look for | Meaning | Usual fix |
|---|---|---|
| estimated `rows` vs actual `rows` off by 10x or more | bad statistics or correlated columns | `ANALYZE <table>`; `CREATE STATISTICS` (dependencies/ndistinct) on correlated columns; raise the column's statistics target |
| `Seq Scan` with `Rows Removed by Filter` large | no usable index for the filter | index on the filter columns (see indexes.md), or the filter isn't sargable |
| `Index Scan` with many `Heap Fetches` | index-only scan defeated by the visibility map | vacuum the table; covering index (`INCLUDE`) |
| `Nested Loop` with a large outer side | misestimate made the planner pick loops | fix the estimate; index the inner join key |
| `Hash` / `Sort` with `Disk:` or `external merge` | `work_mem` too small for this query | reduce the rows earlier; `SET LOCAL work_mem` for this query only |
| `Buffers: shared read` large | cold or large data | more selective index; a covering index |
| `Rows Removed by Join Filter` | join condition not indexable | rewrite the condition; index the expression |

## Non-sargable patterns (the index can't be used)
- A function on the column: `WHERE lower(email) = $1` needs an expression index on `lower(email)`, or the `citext` type.
- `col::text = $1`, or a parameter of a different type than the column (common with EF/Npgsql when a `text` parameter meets a `varchar` or `uuid` column). Match the types.
- `LIKE '%abc'` (leading wildcard) needs a `pg_trgm` GIN index.
- `OR` across different columns: rewrite as `UNION ALL`, or rely on BitmapOr with separate indexes.
- `OFFSET 100000`: use keyset pagination.

## Find the queries worth fixing
```sql
SELECT round(total_exec_time) AS total_ms, calls, round(mean_exec_time::numeric,1) AS mean_ms,
       rows, left(regexp_replace(query, '\s+', ' ', 'g'), 120) AS query
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 15;
```
Needs the `pg_stat_statements` extension. Rank by **total** time, not mean: a 5 ms query called a million times beats a 2 s report.

## Verify
Re-run the plan after the change and compare actual time and buffers. On production-sized data, check that the planner actually uses the new index.
