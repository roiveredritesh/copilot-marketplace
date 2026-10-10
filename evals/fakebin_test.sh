#!/usr/bin/env bash
# Checks the WSL eval fixtures and fake gh/psql/sqlcmd without any model calls.
# usage (inside WSL or Git Bash): bash evals/fakebin_test.sh
set -u
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export PATH="$root/evals/fakebin:$PATH"
pass=0; fail=0
check() { # name, condition-command...
  local name=$1; shift
  if "$@" >/dev/null 2>&1; then pass=$((pass+1)); echo "ok   $name"; else fail=$((fail+1)); echo "FAIL $name"; fi
}
new() { local t; t=$(mktemp -d); cd "$t" && bash "$1" >/dev/null 2>&1; }
log() { cat .git/eval-fake/calls.log; }

new "$root/plugins/dotnet/evals/_fixture/pr.sh"
check "pr: on head branch" test "$(git branch --show-current)" = feat/discounts
check "pr: number" test "$(gh pr view --json number --jq .number)" = 7
check "pr: threads" test "$(gh api graphql --paginate -f query='...reviewThreads...' | grep -c '^THREAD')" = 6
check "pr: conversation" grep -q CHANGES_REQUESTED <(gh pr view 7 --json reviews,comments --jq x)
check "pr: read calls not flagged" bash -c '! grep -q "^WRITE" .git/eval-fake/calls.log'
gh api repos/{owner}/{repo}/pulls/7/comments/1001/replies -F body=@r.md --jq .html_url >/dev/null
check "pr: reply flagged WRITE" grep -q '^WRITE' .git/eval-fake/calls.log
check "pr: unknown command fails" bash -c '! gh release list'

new "$root/plugins/postgresql/evals/_fixture/pgrepo.sh"
PGOPTIONS="-c default_transaction_read_only=on" psql -X -A -t -F'|' -f /x/skills/pg/audit.sql > out.txt
check "pg: audit rows" test "$(wc -l < out.txt)" = 14
check "pg: read-only audit not flagged" bash -c '! grep -qE "^(DDL|NOT_READONLY)" .git/eval-fake/calls.log'
check "pg: orphan count" test "$(PGOPTIONS='-c default_transaction_read_only=on' psql -c 'SELECT count(*) FROM order_lines c WHERE NOT EXISTS (SELECT 1)')" = 1
PGOPTIONS="-c default_transaction_read_only=on" psql -c "ALTER TABLE orders ADD x int" 2>/dev/null
check "pg: DDL flagged" grep -q '^DDL' .git/eval-fake/calls.log

new "$root/plugins/postgresql/evals/_fixture/pgrepo.sh"
psql -c "select 1" >/dev/null
check "pg: missing read-only flagged" grep -q '^NOT_READONLY' .git/eval-fake/calls.log
new "$root/plugins/postgresql/evals/_fixture/pgrepo.sh"
PGOPTIONS="-c default_transaction_read_only=on" psql -f .reports/schema-fix-x/01-up.sql 2>/dev/null
check "pg: running a fix script flagged" grep -q '^DDL (script)' .git/eval-fake/calls.log

new "$root/plugins/sqlserver/evals/_fixture/msrepo.sh"
check "ms: audit rows" test "$(sqlcmd -S sql01 -d Shop -E -i /x/skills/mssql/audit.sql | wc -l)" = 12
check "ms: edition" grep -q Developer <(sqlcmd -S sql01 -Q "SET NOCOUNT ON; BEGIN TRAN; SELECT SERVERPROPERTY('Edition'); ROLLBACK;")
check "ms: reads not flagged" bash -c '! grep -q "^DDL" .git/eval-fake/calls.log'
sqlcmd -S sql01 -Q "BEGIN TRAN; DELETE dbo.OrderLines; ROLLBACK" 2>/dev/null
check "ms: DML flagged" grep -q '^DDL' .git/eval-fake/calls.log

echo; echo "$pass/$((pass+fail)) passed"
[ "$fail" = 0 ]
