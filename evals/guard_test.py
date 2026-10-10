"""Unit tests for plugins/core/hooks/guard.sh. No model calls, free to run.
usage: python evals/guard_test.py"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(ROOT, "plugins", "core", "hooks", "guard.sh")
AUDIT_MS = "D:/x/plugins/sqlserver/skills/mssql/audit.sql"
RO = 'PGOPTIONS="-c default_transaction_read_only=on -c statement_timeout=15000" '

CASES = [
    # (command, expected decision)
    ("ls -la", "allow"),
    ("git status --short", "allow"),
    ("git log -n 5 --format=%s", "allow"),
    ("git commit -m 'push the button'", "allow"),
    ("git push -u origin feat/x", "ask"),
    ("git -C /repo push", "ask"),
    ("cd repo && git push --force-with-lease", "ask"),
    ("rtk git push origin main", "ask"),
    ("gh pr view 3 --json title", "allow"),
    ("gh pr diff 3", "allow"),
    ("gh pr create --base main --title t --body-file b.md", "ask"),
    ("gh pr comment 3 --body-file r.md", "ask"),
    ("gh pr merge 3 --squash", "ask"),
    ("gh run list --limit 5", "allow"),
    ("gh run view 123 --log-failed", "allow"),
    ("gh api repos/{owner}/{repo}/pulls/3/comments", "allow"),
    ("gh api graphql -F owner='{owner}' -f query='query{viewer{login}}'", "allow"),
    ("gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -F id=X", "ask"),
    ("gh api repos/{owner}/{repo}/pulls/3/comments/9/replies -F body=@r.md --jq .html_url", "ask"),
    ("gh api -X DELETE repos/o/r/git/refs/heads/x", "ask"),
    (RO + 'psql -X -A -c "select 1"', "allow"),
    (RO + '"C:/Program Files/PostgreSQL/18/bin/psql.exe" -X -f audit.sql', "allow"),
    ('psql -X -c "select 1"', "deny"),
    ('psql -X -c "DROP TABLE orders"', "deny"),
    ('"C:/Program Files/PostgreSQL/18/bin/psql.exe" -f 01-up.sql', "deny"),
    ("psql --version", "allow"),
    ("dropdb shop", "deny"),
    ("pg_restore -d shop dump.bak", "deny"),
    ("pg_dump -s shop > schema.sql", "allow"),
    ('sqlcmd -S "(localdb)\\\\MSSQLLocalDB" -d Shop -E -b -i "' + AUDIT_MS + '"', "allow"),
    ('sqlcmd -S . -d Shop -E -Q "SET NOCOUNT ON; BEGIN TRAN; SELECT COUNT(*) FROM dbo.Orders; ROLLBACK;"', "allow"),
    ('sqlcmd -S . -d Shop -E -Q "SELECT COUNT(*) FROM dbo.Orders"', "deny"),
    ('sqlcmd -S . -d Shop -E -Q "BEGIN TRAN; DELETE dbo.Orders; COMMIT"', "deny"),
    ('sqlcmd -S . -d Shop -E -i 02-up.sql', "deny"),
    ("echo psql is great", "allow"),
    ("bash -c 'psql -f up.sql'", "deny"),
    ("cd db && psql -f up.sql", "deny"),
    ("rtk psql -c 'delete from t'", "deny"),
]


def run(command, env_extra=None):
    payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash",
                          "tool_input": {"command": command, "description": "push it"}})
    env = {**os.environ, **(env_extra or {})}
    env.pop("CLAUDE_ALLOW_DB_WRITES", None) if not env_extra else None
    out = subprocess.run(["bash", GUARD], input=payload, capture_output=True, text=True, env=env).stdout.strip()
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"


def main():
    failed = 0
    for command, want in CASES:
        got = run(command)
        ok = got == want
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {want:5} {got:5} {command[:90]}")
    # opt-out switch
    got = run('psql -X -c "DROP TABLE t"', {"CLAUDE_ALLOW_DB_WRITES": "1"})
    failed += got != "allow"
    print(f"{'ok  ' if got == 'allow' else 'FAIL'} allow {got:5} CLAUDE_ALLOW_DB_WRITES=1 psql DROP")
    print(f"\n{len(CASES) + 1 - failed}/{len(CASES) + 1} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
