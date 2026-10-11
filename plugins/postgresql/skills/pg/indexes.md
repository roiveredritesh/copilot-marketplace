# Indexes

## Choosing
- B-tree, multi-column: equality columns first, then range or sort columns. `(tenant_id, created_at)` serves `WHERE tenant_id = $1 ORDER BY created_at DESC`.
- Covering index: `INCLUDE (col)` enables index-only scans without widening the key.
- Partial index: `WHERE deleted_at IS NULL` or `WHERE status = 'pending'` when queries always filter the same way. Smaller and faster.
- Expression index: `(lower(email))` when the query uses the expression.
- GIN: `jsonb` (`jsonb_path_ops` for `@>` only), arrays, full-text `tsvector`, `pg_trgm` for `LIKE '%x%'`.
- BRIN: huge append-only tables filtered by a naturally ordered column (time). Tiny, but lossy.
- Foreign keys are **not** indexed automatically. Index the referencing column when you join on it or delete from the parent.

## Catalog queries (send to runner)
Unindexed foreign keys (checks the leading FK column against each index's leading column):
```sql
SELECT c.conrelid::regclass AS tbl, a.attname AS fk_col
FROM pg_constraint c JOIN pg_attribute a ON a.attrelid=c.conrelid AND a.attnum=c.conkey[1]
WHERE c.contype='f' AND NOT EXISTS (
  SELECT 1 FROM pg_index i WHERE i.indrelid=c.conrelid AND i.indkey[0]=c.conkey[1]);
```
Unused indexes (check every replica before dropping; the stats reset with `pg_stat_reset`):
```sql
SELECT s.relname AS tbl, s.indexrelname AS idx, s.idx_scan, pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s JOIN pg_index i USING (indexrelid)
WHERE s.idx_scan = 0 AND NOT i.indisunique AND NOT i.indisprimary
ORDER BY pg_relation_size(s.indexrelid) DESC LIMIT 20;
```
Duplicate or prefix-redundant indexes:
```sql
SELECT indrelid::regclass AS tbl, array_agg(indexrelid::regclass) AS idxs, indkey::text
FROM pg_index GROUP BY indrelid, indkey::text HAVING count(*) > 1;
```
Also treat an index on `(a)` as redundant when `(a, b)` exists, unless `(a)` is unique.

## Costs of an index
Every index slows writes and takes space and vacuum time. Each new index must name the query it serves. Create indexes in production with `CREATE INDEX CONCURRENTLY` (see migration-safety.md).
