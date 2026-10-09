---
name: ci
description: Triage a failed CI run (GitHub Actions via gh, Azure DevOps via az) with Haiku condensing the logs, or generate a CI pipeline for a .NET Core or .NET Framework repo.
argument-hint: "triage [run-id | PR# | branch] | generate [github | azure]"
disable-model-invocation: true
---
# CI/CD

## triage
1. `core:runner` work order (GitHub):
   ```text
   steps:
     1. gh run list <--branch X | --commit $(gh pr view N --json headRefOid --jq .headRefOid)> --limit 5 --json databaseId,name,status,conclusion,headBranch,createdAt --jq '.[] | "\(.databaseId) \(.name) \(.conclusion) \(.headBranch) \(.createdAt)"'
     2. For the newest failed run id R (or the given run id): gh run view R --json jobs --jq '.jobs[] | select(.conclusion=="failure") | "\(.name): " + ([.steps[] | select(.conclusion=="failure") | .name] | join(", "))'
     3. gh run view R --log-failed | sed -E 's/^[^\t]*\t[^\t]*\t[0-9TZ:.-]+ //' | grep -iE 'error|fail|exception|exit code|##\[error\]' | awk '!seen[$0]++' | head -n 60
   return: failed run (id, workflow, branch), failed jobs/steps, then the condensed error lines (at most 60)
   on-error: BLOCKED: <one line> (e.g. gh not authenticated)
   ```
   Azure DevOps: the same shape with `az pipelines runs list --branch X --top 5 -o table` and `az pipelines runs show --id R`. If `az` isn't installed, ask the user to paste the failing step's log.
2. Main session: classify the failure as code (compile or test), environment (SDK version, missing secret, service container), flaky (timing, ordering), or infrastructure. For code failures, reproduce locally with `/dotnet:build test`. Give the fix and, if it's flaky, the evidence (e.g. the same test passing on a re-run: `gh run rerun R --failed` only with the user's OK).

## generate
1. Run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" detect` yourself (about 8 lines) and check for `global.json`, test projects, Npgsql or EF usage (`git grep -l Npgsql -- '*.csproj'`), and existing pipelines (`.github/workflows/`, `azure-pipelines.yml`).
2. Start from the matching template in [templates.md](templates.md). Adapt the solution path, SDK version, test filters, and services (a Postgres service container if Npgsql integration tests exist), and remove what doesn't apply.
3. Write the file, explain each job in one line, and list the secrets or variables the user must create. Don't push or enable anything.
