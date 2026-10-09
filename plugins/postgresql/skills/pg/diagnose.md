# Live diagnostics

Send these to `core:runner` in one work order when they're needed together.

## Who is blocking whom
```sql
SELECT a.pid, pg_blocking_pids(a.pid) AS blocked_by, a.state, now()-a.query_start AS running,
       a.wait_event_type, left(a.query,80) AS query
FROM pg_stat_activity a WHERE cardinality(pg_blocking_pids(a.pid)) > 0;
```
Then look up the blocker's `pid` in `pg_stat_activity`. Only the user decides whether to run `pg_cancel_backend(pid)` (cancel the query) or `pg_terminate_backend(pid)` (kill the session). The runner is read-only.

## Long or idle transactions
```sql
SELECT pid, usename, state, now()-xact_start AS xact_age, left(query,80) AS query
FROM pg_stat_activity WHERE state <> 'idle'
ORDER BY xact_start NULLS LAST LIMIT 15;
```
`idle in transaction` sessions hold locks and block vacuum. The usual causes are a missing commit or rollback in app code, or a transaction left open around a network call. Set `idle_in_transaction_session_timeout`.

## Bloat and vacuum health
```sql
SELECT relname, n_live_tup, n_dead_tup,
       round(100.0*n_dead_tup/greatest(n_live_tup+n_dead_tup,1),1) AS dead_pct,
       last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 15;
```
A high `dead_pct` with an old `last_autovacuum` means autovacuum can't keep up or is blocked by long transactions. Lower the table's `autovacuum_vacuum_scale_factor` for big hot tables, and remove whatever holds the old snapshot. `VACUUM FULL` rewrites the table under an exclusive lock, so it's not for production hours (consider `pg_repack`).

## Transaction ID wraparound
```sql
SELECT datname, age(datfrozenxid) AS xid_age FROM pg_database ORDER BY 2 DESC;
```
Plan aggressive vacuum well before it approaches 2 billion. Act above ~1 billion.

## Connections
```sql
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
SHOW max_connections;
```
Close to `max_connections`: put a pooler in front (PgBouncer, transaction mode), and check the Npgsql pool sizes across every app instance (see npgsql.md).

## Cache and I/O
```sql
SELECT relname, heap_blks_read, heap_blks_hit,
       round(100.0*heap_blks_hit/greatest(heap_blks_hit+heap_blks_read,1),1) AS hit_pct
FROM pg_statio_user_tables ORDER BY heap_blks_read DESC LIMIT 10;
```
