-- Schema audit: read-only catalog queries (SQL Server 2017+). Output: severity|check|object|detail
-- Run: sqlcmd -S <server> -d <db> -E -b -h -1 -W -s "|" -t 60 -i audit.sql
SET NOCOUNT ON;
SET LOCK_TIMEOUT 5000;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

WITH tbl AS (
  SELECT t.object_id, QUOTENAME(SCHEMA_NAME(t.schema_id)) + '.' + QUOTENAME(t.name) AS obj, t.name
  FROM sys.tables t WHERE t.is_ms_shipped = 0
),
col AS (
  SELECT c.object_id, c.column_id, c.name, c.is_nullable, ty.name AS typ, t.obj + '.' + QUOTENAME(c.name) AS obj
  FROM sys.columns c JOIN tbl t ON t.object_id = c.object_id JOIN sys.types ty ON ty.user_type_id = c.user_type_id
),
fkc AS (
  SELECT fk.object_id AS fk_id, fk.parent_object_id AS tid, fk.referenced_object_id AS rid, fk.name, fk.is_not_trusted, fk.is_disabled,
         STRING_AGG(CAST(c.parent_column_id AS varchar(10)), ',') WITHIN GROUP (ORDER BY c.constraint_column_id) AS cols,
         STRING_AGG(CAST(pc.name AS nvarchar(max)), ',') WITHIN GROUP (ORDER BY c.constraint_column_id) AS names
  FROM sys.foreign_keys fk JOIN sys.foreign_key_columns c ON c.constraint_object_id = fk.object_id
  JOIN sys.columns pc ON pc.object_id = c.parent_object_id AND pc.column_id = c.parent_column_id
  GROUP BY fk.object_id, fk.parent_object_id, fk.referenced_object_id, fk.name, fk.is_not_trusted, fk.is_disabled
),
ix AS (
  SELECT i.object_id AS tid, i.index_id, i.name, i.is_unique, i.is_primary_key, i.is_disabled, i.filter_definition,
         STRING_AGG(CAST(ic.column_id AS varchar(10)), ',') WITHIN GROUP (ORDER BY ic.key_ordinal) AS cols
  FROM sys.indexes i JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.key_ordinal > 0
  JOIN tbl t ON t.object_id = i.object_id
  GROUP BY i.object_id, i.index_id, i.name, i.is_unique, i.is_primary_key, i.is_disabled, i.filter_definition
),
incl AS (
  SELECT ic.object_id AS tid, ic.index_id,
         STRING_AGG(CAST(ic.column_id AS varchar(10)), ',') WITHIN GROUP (ORDER BY ic.column_id) AS cols
  FROM sys.index_columns ic WHERE ic.is_included_column = 1 GROUP BY ic.object_id, ic.index_id
),
findings (sev, chk, obj, detail) AS (
  SELECT 'high', 'fk_without_index', t.obj, f.name + ' (' + f.names + ') -> ' + OBJECT_NAME(f.rid)
  FROM fkc f JOIN tbl t ON t.object_id = f.tid
  WHERE NOT EXISTS (SELECT 1 FROM ix i WHERE i.tid = f.tid AND (i.cols = f.cols OR i.cols LIKE f.cols + ',%'))
  UNION ALL
  SELECT 'high', 'no_primary_key', t.obj, '' FROM tbl t WHERE OBJECTPROPERTY(t.object_id, 'TableHasPrimaryKey') = 0
  UNION ALL
  SELECT 'high', 'heap', t.obj, 'no clustered index'
  FROM tbl t WHERE EXISTS (SELECT 1 FROM sys.indexes i WHERE i.object_id = t.object_id AND i.index_id = 0)
  UNION ALL
  SELECT 'high', 'float_money', c.obj, c.typ
  FROM col c WHERE c.typ IN ('float', 'real')
    AND (LOWER(c.name) LIKE '%price%' OR LOWER(c.name) LIKE '%amount%' OR LOWER(c.name) LIKE '%total%' OR LOWER(c.name) LIKE '%cost%'
         OR LOWER(c.name) LIKE '%balance%' OR LOWER(c.name) LIKE '%fee%' OR LOWER(c.name) LIKE '%tax%' OR LOWER(c.name) LIKE '%salary%')
  UNION ALL
  SELECT 'high', 'identity_near_max', t.obj + '.' + QUOTENAME(ic.name),
         CONCAT('last_value ', CAST(ic.last_value AS bigint), ' of max ', m.mx, ' (', CAST(100.0 * CAST(ic.last_value AS bigint) / m.mx AS int), '%)')
  FROM sys.identity_columns ic JOIN tbl t ON t.object_id = ic.object_id JOIN sys.types ty ON ty.user_type_id = ic.user_type_id
  CROSS APPLY (SELECT CASE ty.name WHEN 'tinyint' THEN 255 WHEN 'smallint' THEN 32767 WHEN 'int' THEN 2147483647
                                   ELSE 9223372036854775807 END AS mx) m
  WHERE ic.last_value IS NOT NULL AND CAST(ic.last_value AS bigint) > 0.8 * m.mx
  UNION ALL
  SELECT 'med', 'untrusted_fk', t.obj, f.name + CASE WHEN f.is_disabled = 1 THEN ' is disabled' ELSE ' is not trusted (created or enabled WITH NOCHECK)' END
  FROM fkc f JOIN tbl t ON t.object_id = f.tid WHERE f.is_not_trusted = 1 OR f.is_disabled = 1
  UNION ALL
  SELECT 'med', 'untrusted_check', t.obj, cc.name + ' is not trusted'
  FROM sys.check_constraints cc JOIN tbl t ON t.object_id = cc.parent_object_id WHERE cc.is_not_trusted = 1 OR cc.is_disabled = 1
  UNION ALL
  SELECT 'med', 'missing_fk_candidate', c.obj, 'no FK constraint; table ' + r.obj + ' exists'
  FROM col c JOIN tbl r ON r.name IN (LEFT(c.name, LEN(c.name) - 2), LEFT(c.name, LEN(c.name) - 2) + 's', LEFT(c.name, LEN(c.name) - 2) + 'es')
  WHERE c.name LIKE '%Id' AND LEN(c.name) > 2 AND c.typ IN ('int', 'bigint', 'smallint', 'uniqueidentifier')
    AND r.object_id <> c.object_id
    AND NOT EXISTS (SELECT 1 FROM sys.foreign_key_columns k WHERE k.parent_object_id = c.object_id AND k.parent_column_id = c.column_id)
  UNION ALL
  SELECT 'med', 'duplicate_index', OBJECT_NAME(i2.tid) + '.' + i2.name, 'same keys as ' + i1.name
  FROM ix i1 JOIN ix i2 ON i1.tid = i2.tid AND i1.index_id < i2.index_id AND i1.cols = i2.cols
   AND ISNULL(i1.filter_definition, '') = ISNULL(i2.filter_definition, '')
  LEFT JOIN incl n1 ON n1.tid = i1.tid AND n1.index_id = i1.index_id
  LEFT JOIN incl n2 ON n2.tid = i2.tid AND n2.index_id = i2.index_id
  WHERE ISNULL(n1.cols, '') = ISNULL(n2.cols, '')
  UNION ALL
  SELECT 'med', 'disabled_index', OBJECT_NAME(i.tid) + '.' + i.name, 'is_disabled = 1' FROM ix i WHERE i.is_disabled = 1
  UNION ALL
  SELECT 'med', 'deprecated_type', c.obj, c.typ FROM col c WHERE c.typ IN ('text', 'ntext', 'image')
  UNION ALL
  SELECT 'low', 'datetime_not_datetime2', c.obj, c.typ FROM col c WHERE c.typ IN ('datetime', 'smalldatetime')
  UNION ALL
  SELECT 'low', 'nullable_fk', c.obj, 'FK column allows NULL (fine if the relation is optional)'
  FROM col c WHERE c.is_nullable = 1
    AND EXISTS (SELECT 1 FROM sys.foreign_key_columns k WHERE k.parent_object_id = c.object_id AND k.parent_column_id = c.column_id)
  UNION ALL
  SELECT 'low', 'money_type', c.obj, c.typ FROM col c WHERE c.typ IN ('money', 'smallmoney')
)
SELECT sev + '|' + chk + '|' + obj + '|' + detail
FROM findings
ORDER BY CASE sev WHEN 'high' THEN 1 WHEN 'med' THEN 2 ELSE 3 END, chk, obj;
