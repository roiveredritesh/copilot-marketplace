-- Schema audit: read-only catalog queries. Output: severity|check|object|detail
-- Run: PGOPTIONS="-c default_transaction_read_only=on -c statement_timeout=30000" psql -X -A -t -F'|' -v ON_ERROR_STOP=1 -f audit.sql
WITH tbl AS (
  SELECT c.oid, c.relname, n.nspname
  FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relkind IN ('r', 'p') AND n.nspname NOT IN ('pg_catalog', 'information_schema') AND n.nspname NOT LIKE 'pg_toast%'
),
col AS (
  SELECT t.oid AS relid, a.attnum, a.attname, a.atttypid, a.attnotnull, a.attidentity,
         pg_get_expr(d.adbin, d.adrelid) AS def, format('%s.%I', t.oid::regclass, a.attname) AS obj
  FROM tbl t JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum > 0 AND NOT a.attisdropped
  LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
),
fk AS (
  SELECT c.oid, c.conname, c.conrelid, c.confrelid, c.conkey, c.convalidated
  FROM pg_constraint c JOIN tbl t ON t.oid = c.conrelid WHERE c.contype = 'f'
),
fkcols AS (
  SELECT f.oid, string_agg(a.attname, ',' ORDER BY k.ord) AS names
  FROM fk f CROSS JOIN LATERAL unnest(f.conkey) WITH ORDINALITY k(attnum, ord)
  JOIN pg_attribute a ON a.attrelid = f.conrelid AND a.attnum = k.attnum GROUP BY f.oid
),
idx AS (
  SELECT i.indexrelid, i.indrelid, i.indisunique, i.indisprimary, i.indisvalid,
         string_to_array(i.indkey::text, ' ')::int2[] AS keys, i.indclass::text AS cls,
         coalesce(pg_get_expr(i.indexprs, i.indrelid), '') AS exprs, coalesce(pg_get_expr(i.indpred, i.indrelid), '') AS pred
  FROM pg_index i JOIN tbl t ON t.oid = i.indrelid
),
findings(sev, chk, obj, detail) AS (
  -- foreign key with no index whose leading columns are the FK columns
  SELECT 'high', 'fk_without_index', f.conrelid::regclass::text, f.conname || ' (' || fc.names || ') -> ' || f.confrelid::regclass
  FROM fk f JOIN fkcols fc ON fc.oid = f.oid
  WHERE NOT EXISTS (SELECT 1 FROM idx i WHERE i.indrelid = f.conrelid
                    AND i.keys[1:cardinality(f.conkey)] @> f.conkey AND i.keys[1:cardinality(f.conkey)] <@ f.conkey)
  UNION ALL
  SELECT 'high', 'no_primary_key', t.oid::regclass::text, ''
  FROM tbl t WHERE NOT EXISTS (SELECT 1 FROM pg_constraint p WHERE p.conrelid = t.oid AND p.contype = 'p')
  UNION ALL
  SELECT 'high', 'invalid_index', i.indexrelid::regclass::text, 'indisvalid = false (failed CREATE INDEX CONCURRENTLY?)'
  FROM idx i WHERE NOT i.indisvalid
  UNION ALL
  SELECT 'high', 'float_money', c.obj, format_type(c.atttypid, NULL)
  FROM col c WHERE c.atttypid IN ('float4'::regtype, 'float8'::regtype)
    AND c.attname ~* '(price|amount|total|cost|balance|fee|tax|salary|money|rate)'
  UNION ALL
  SELECT 'high', 'sequence_near_max', s.schemaname || '.' || s.sequencename,
         format('last_value %s of max %s (%s%%)', s.last_value, s.max_value, round(100.0 * s.last_value / s.max_value))
  FROM pg_sequences s WHERE s.last_value IS NOT NULL AND s.last_value > 0.8 * s.max_value
  UNION ALL
  SELECT 'med', 'missing_fk_candidate', c.obj,
         'no FK constraint; table ' || r.oid::regclass || ' exists'
  FROM col c
  JOIN tbl r ON r.relname IN (regexp_replace(c.attname, '_id$', ''), regexp_replace(c.attname, '_id$', '') || 's',
                              regexp_replace(c.attname, '_id$', '') || 'es')
  WHERE c.attname ~ '_id$' AND c.atttypid IN ('int2'::regtype, 'int4'::regtype, 'int8'::regtype, 'uuid'::regtype)
    AND NOT EXISTS (SELECT 1 FROM fk f WHERE f.conrelid = c.relid AND c.attnum = ANY (f.conkey))
  UNION ALL
  SELECT 'med', 'duplicate_index', i2.indexrelid::regclass::text, 'same definition as ' || i1.indexrelid::regclass
  FROM idx i1 JOIN idx i2 ON i1.indrelid = i2.indrelid AND i1.indexrelid < i2.indexrelid
   AND i1.keys = i2.keys AND i1.cls = i2.cls AND i1.exprs = i2.exprs AND i1.pred = i2.pred
  UNION ALL
  SELECT 'med', 'constraint_not_validated', c.conrelid::regclass::text, c.conname || ' is NOT VALID'
  FROM pg_constraint c JOIN tbl t ON t.oid = c.conrelid WHERE NOT c.convalidated
  UNION ALL
  SELECT 'med', 'timestamp_without_tz', c.obj, 'timestamp without time zone'
  FROM col c WHERE c.atttypid = 'timestamp'::regtype
  UNION ALL
  SELECT 'low', 'nullable_fk', c.obj, 'FK column allows NULL (fine if the relation is optional)'
  FROM col c WHERE NOT c.attnotnull AND EXISTS (SELECT 1 FROM fk f WHERE f.conrelid = c.relid AND c.attnum = ANY (f.conkey))
  UNION ALL
  SELECT 'low', 'json_not_jsonb', c.obj, 'json' FROM col c WHERE c.atttypid = 'json'::regtype
  UNION ALL
  SELECT 'low', 'money_type', c.obj, 'money (locale-dependent)' FROM col c WHERE c.atttypid = 'money'::regtype
  UNION ALL
  SELECT 'low', 'char_n', c.obj, format_type(c.atttypid, NULL) FROM col c WHERE c.atttypid = 'bpchar'::regtype
  UNION ALL
  SELECT 'low', 'serial_not_identity', c.obj, c.def
  FROM col c WHERE c.attidentity = '' AND c.def LIKE 'nextval(%'
  UNION ALL
  SELECT 'low', 'unused_index', s.indexrelid::regclass::text,
         'idx_scan = 0 since stats reset ' || coalesce((SELECT stats_reset::date::text FROM pg_stat_database WHERE datname = current_database()), 'never')
  FROM pg_stat_user_indexes s JOIN idx i ON i.indexrelid = s.indexrelid
  WHERE s.idx_scan = 0 AND NOT i.indisunique AND NOT i.indisprimary
)
SELECT sev, chk, obj, detail FROM findings
ORDER BY CASE sev WHEN 'high' THEN 1 WHEN 'med' THEN 2 ELSE 3 END, chk, obj;
