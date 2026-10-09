# ritesh-marketplace

Cost-optimized Claude Code plugins for .NET (Core **and** Framework) and PostgreSQL. Skills stay thin in the main session. Exploration, git, build/test, and MCP calls run on **Haiku 5.5 executors** that take an exact work order and return only condensed results.

## Setup

```text
/plugin marketplace add roiveredritesh/copilot-marketplace
/plugin install core@ritesh-marketplace
/plugin install dotnet@ritesh-marketplace
/core:setup
```
`/core:setup` runs once. It shows every change and asks before applying it:
- subagents default to Haiku
- the built-in Explore agent runs on Haiku
- Haiku compacts at 100K tokens (its price rises 5x above that)
- an isolated `publisher` agent owns the Confluence/Jira/GitHub MCP servers, so their tools stay out of the main session

Restart Claude Code afterwards.

## Plugins: enable per repo

| Plugin | Enable in | Gives you |
|---|---|---|
| `core` | everywhere (required) | `scout`, `runner` (Haiku), `reviewer` (Sonnet), `/core:setup` |
| `dotnet` | every .NET repo | the full SDLC loop, below |
| `postgresql` | repos using PostgreSQL | `pg` skill: query tuning, indexes, schema review, lock-safe migrations, diagnostics (read-only `psql`) |
| `dotnet-legacy` | WebForms / .NET Framework 4.x repos | `/dotnet-legacy:modernize` inventory and migration plan |
| `docs-kit` | where you write Confluence or read Jira | `/docs-kit:confluence <type> <space\|page>`, `jira <KEY>` |

### SDLC coverage (`dotnet` + friends)

| Phase | Command |
|---|---|
| Intake | `/docs-kit:jira PROJ-123` |
| Plan / design | `/dotnet:plan <goal>` · ADR via `/docs-kit:confluence adr` · `dotnet:guide` (auto) · `/dotnet-legacy:modernize` |
| Implement (TDD) | `/dotnet:implement <plan or task>`: failing test → code → green, Haiku build/test gate after every step |
| Tests | `/dotnet:tests <target> [--coverage]` |
| Build / test | `/dotnet:build [build\|test]` |
| Review | `/dotnet:review [base\|PR#]` |
| Commit / PR | `/dotnet:pr [base] [--draft]` |
| CI/CD | `/dotnet:ci triage [run\|PR#]` · `/dotnet:ci generate [github\|azure]` |
| Security / deps | `/dotnet:audit`: vulnerable/deprecated/outdated NuGet, secret locations, framework support dates |
| Debug / RCA | `/dotnet:debug <trace\|error\|failing test>` |
| Database | `postgresql:pg` (auto, or `/postgresql:pg`) |
| Docs / release | `/docs-kit:confluence <api\|adr\|runbook\|release-notes\|qa-guide> <space\|page>` |

`postgresql`, `dotnet-legacy`, and `docs-kit` are off by default. A disabled plugin costs zero tokens. Turn one on for a repo in its `.claude/settings.json`:
```json
{ "enabledPlugins": { "postgresql@ritesh-marketplace": true } }
```

## How cost is controlled
1. **Model tiering.** Your main session (Sonnet 5.5 recommended) judges. Haiku executors do I/O at about 1/40 of the Opus 5.5 token price. Nothing pins Opus.
2. **Small fixed overhead.** 5 plugins and a handful of skills. Heavy workflows are user-invoked only (`disable-model-invocation`), so they cost nothing until you call them. Guidance loads one reference file at a time.
3. **Bounded returns.** Executors return 30–40 lines max. Build and test output is condensed by `dotnet.sh` before any model sees it.
4. **Cache-friendly.** Static agent and skill bodies, no inline model switches, MCP servers isolated in a subagent.
5. **Reports go to chat.** `--save` writes to `~/.claude/reports/<repo>/`, never into your repo.

Check the overhead in any session with `/context`.

## Requirements
- Claude Code 2.1.288+ (per-model compaction window).
- `bash` (Git Bash on Windows), plus the .NET SDK and/or Visual Studio Build Tools for legacy projects.
- Optional: `psql` (PostgreSQL), `gh` (GitHub PRs), the Atlassian remote MCP (docs-kit).

## Development
`scripts/validate.sh` runs `claude plugin validate --strict` on the marketplace and every plugin. The design and the decisions behind it are in [docs/RESEARCH.md](docs/RESEARCH.md).
