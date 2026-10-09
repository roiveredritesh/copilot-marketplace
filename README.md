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
- an isolated `publisher` agent owns the Confluence/Jira/GitHub MCP servers, so their tools stay out of the main session

Restart Claude Code afterwards. Install `postgresql`, `dotnet-legacy`, and `docs-kit` with **project scope**, only in the repos that need them.

To try the plugins from a local checkout before they reach `main`: `/plugin marketplace add "<path to this repo>"`.

## Plugins: enable per repo

| Plugin | Enable in | Gives you |
|---|---|---|
| `core` | everywhere (required) | `scout` (code + web), `runner` (Haiku), `reviewer` (Sonnet), `/core:setup` |
| `dotnet` | every .NET repo | the full SDLC loop, below |
| `postgresql` | repos using PostgreSQL | `pg` skill: query tuning, indexes, schema review, lock-safe migrations, diagnostics (read-only `psql`) |
| `dotnet-legacy` | WebForms / .NET Framework 4.x repos | `/dotnet-legacy:modernize` inventory and migration plan |
| `docs-kit` | where you write Confluence or read Jira | `/docs-kit:confluence <type> <space\|page>`, `jira <KEY>` |

### SDLC coverage (`dotnet` + friends)

| Phase | Command |
|---|---|
| **All phases, gated** | `/dotnet:flow <KEY \| details> [--no-tdd]`: runs every phase below in order and waits for your approval after each one (spec-driven) |
| Intake | `/docs-kit:jira PROJ-123` |
| Analysis | `/dotnet:analyze <PROJ-123 \| details>`: goal, current behavior, acceptance criteria, impacted areas, open questions → an analysis file for `/dotnet:plan` |
| Spike / research | `/dotnet:spike <question> [--poc]`: existing code or new tech, with sourced facts and an option matrix |
| Plan / design | `/dotnet:plan <goal>` · ADR via `/docs-kit:confluence adr` · `dotnet:guide` (auto) · `/dotnet-legacy:modernize` |
| Implement | `/dotnet:implement <plan or task> [--no-tdd]`: TDD by default (failing test → code → green), or code-first with `--no-tdd`; Haiku build/test gate after every step |
| Tests | `/dotnet:tests <target> [--coverage]` |
| Build / test | `/dotnet:build [build\|test]` |
| Review | `/dotnet:review [base\|PR#]` |
| Commit / PR | `/dotnet:pr [base] [--draft]` |
| PR feedback | `/dotnet:pr-comments [PR#] [--draft-only]`: verify each unresolved comment, fix, draft replies, post after approval |
| CI/CD | `/dotnet:ci triage [run\|PR#]` · `/dotnet:ci generate [github\|azure]` |
| Security / deps | `/dotnet:audit`: vulnerable/deprecated/outdated NuGet, secret locations, framework support dates |
| Debug / RCA | `/dotnet:debug <trace\|error\|failing test>` |
| Database | `postgresql:pg` (auto, or `/postgresql:pg`) |
| Docs / release | `/docs-kit:confluence <api\|adr\|runbook\|release-notes\|qa-guide> <space\|page>` |

`postgresql`, `dotnet-legacy`, and `docs-kit` are off by default. A disabled plugin costs zero tokens. Turn one on for a repo in its `.claude/settings.json`:
```json
{ "enabledPlugins": { "postgresql@ritesh-marketplace": true } }
```

## Plugins in detail

Each command below names who does the work. **Main** = your session model, which judges and writes code. **Haiku** = the `scout`/`runner` executors, which search, run commands, and condense output. Commands marked *auto* can also be picked up by Claude without a slash command. The rest run only when you invoke them, so they cost nothing until then.

### `core`: required everywhere
The shared executors that every other plugin dispatches to, plus the one-time setup.

| Piece | What it does | Use it when |
|---|---|---|
| `/core:setup` | Sets subagents and Explore to Haiku. Moves Confluence/Jira/GitHub MCP servers into an isolated `publisher` agent. Asks before each change. | Once, right after install. |
| `scout` agent (Haiku) | Read-only code and web search. It takes an exact work order and returns facts with `path:line` or URL. A vague order returns `BLOCKED: work order missing <field>`. | Skills use it to map code, find callers, and research libraries. You can also dispatch it: *"use core:scout: scope src/Orders/\*\*, terms OrderService, IOrderRepository; list callers with path:line"*. |
| `runner` agent (Haiku) | Runs exact shell commands: git, gh, dotnet/msbuild, read-only psql. Returns condensed output only. | Builds, tests, git history, CI logs, DB queries. |
| `reviewer` agent (Sonnet) | Reviews one chunk of a very large diff. | Only `/dotnet:review` uses it, when a diff is too big for one session. |

### `dotnet`: every .NET repo (Core and Framework)
The full SDLC loop. Builds and tests go through `scripts/dotnet.sh`. It detects SDK-style vs legacy projects, finds MSBuild through vswhere, restores `packages.config`, and prints only errors and failed tests.

| Command | Use case | Example |
|---|---|---|
| `/dotnet:spike <question> [--poc]` | Research before you commit to a direction. Covers existing code ("how does X work, what breaks if we change Y") or new tech ("which library"). Haiku gathers code, git, web, and NuGet facts. Main builds an option matrix where every cell has a source, then recommends. `--poc` builds a throwaway experiment in a separate worktree. | `/dotnet:spike IMemoryCache, HybridCache or output caching for the catalog page?` |
| `/dotnet:flow <KEY \| details> [--no-tdd]` | **Spec-driven development in one command.** Runs analyze, spike (only if research is needed), plan, implement, tests (code-first only), review, and pr. After every step it shows a short summary and asks you to **Approve** (next step), **Revise** (redo this step with your feedback), or **Pause**. Specs live in `.reports/<KEY>/` (`analysis.md`, `plan.md`, `progress.md`). `/dotnet:flow resume <KEY>` continues in a fresh session, which is cheaper than one long session. `/dotnet:flow status <KEY>` shows progress. | `/dotnet:flow PROJ-123` · `/clear` then `/dotnet:flow resume PROJ-123` |
| `/dotnet:analyze <KEY \| details>` | Requirement analysis before planning, from a Jira ticket key (fetched by the Haiku `publisher`) or details you give. Haiku finds where the behavior lives today and the recent git history. Main separates facts (`path:line`, ticket text) from assumptions, writes acceptance criteria (marked *proposed* when the ticket lacks them), lists impacted areas, risks, and open questions, and asks you any blocking question. Output: `.reports/analysis-<KEY>.md`. | `/dotnet:analyze PROJ-123` or `/dotnet:analyze users need a wishlist on the catalog page` |
| `/dotnet:plan <analysis file \| goal>` | Turns an analysis file, feature, refactor, or migration into a file-level step plan. Haiku maps the relevant code first. With an analysis file it doesn't re-ask settled questions, and the acceptance criteria become the test plan. | `/dotnet:plan .reports/analysis-PROJ-123.md` |
| `/dotnet:implement <plan or task> [--no-tdd]` | Executes a plan step by step. **TDD (default):** failing test, then code, then green. **Code-first (`--no-tdd`, or just say "without TDD"):** code, then the existing suite must stay green; no new tests, and untested behaviors are listed at the end for `/dotnet:tests`. In both modes Haiku builds and tests after every step, and it stops on red instead of piling on changes. | `/dotnet:implement the plan above` · `/dotnet:implement --no-tdd add CatalogItem.IsFree` |
| `/dotnet:tests <target> [--coverage]` | Writes tests in the repo's existing style (xUnit/NUnit/MSTest, its mocking and assertion libraries), runs them, and can report coverage. | `/dotnet:tests OrderService.Cancel --coverage` |
| `/dotnet:build [build\|test]` *auto* | "Does it build / do the tests pass?" You get back only compiler errors or failing tests, for .NET Core or .NET Framework. | `/dotnet:build test` |
| `/dotnet:review [base\|PR#]` | Reviews the branch or a GitHub PR for bugs, security issues, and breaking changes, while Haiku runs the tests in parallel. | `/dotnet:review main` or `/dotnet:review 42` |
| `/dotnet:debug <trace\|error\|test>` | Root cause of an exception, stack trace, failing test, or bug report. Haiku locates the code and searches git history (which commit broke it). | `/dotnet:debug NullReferenceException at BasketService.cs:57` |
| `/dotnet:pr [base] [--draft]` | Commits in the repo's message convention and opens a PR with a generated description. Asks once, showing the files, the commit message, the push target, and the PR; no PR option when `origin` isn't on GitHub. | `/dotnet:pr main --draft` |
| `/dotnet:pr-comments [PR#] [--draft-only]` | Works through review feedback on a GitHub PR. Haiku saves **every** unresolved thread (all pages, full text) plus review and conversation comments to `.reports/pr-<n>/` and returns only an index, so nothing is dropped or summarized. Main reads each whole thread and the code at its `path:line` (reviewers can be wrong, threads may be withdrawn or already fixed) and classifies it as **fix / answer / push back / defer / done / decide** (conflicting reviewers). It applies `suggestion` blocks verbatim. **You choose** which fixes to apply (all, some, or drafts only) and whether behavior fixes get regression tests. Then it fixes, runs the tests, and drafts one short reply per thread. Commit+push and posting replies each need a separate yes. Threads are resolved only when you ask. `--draft-only` never posts. | `/dotnet:pr-comments 42` |
| `/dotnet:ci triage\|generate` | `triage`: Haiku condenses failed GitHub Actions or Azure DevOps logs to the failing step and error. `generate`: writes a CI pipeline for .NET Core or Framework. | `/dotnet:ci triage 42` · `/dotnet:ci generate github` |
| `/dotnet:audit` | Vulnerable, deprecated, and outdated NuGet packages (including `packages.config`), likely committed secrets, and target-framework end-of-support dates, ranked by priority. | `/dotnet:audit` before a release |
| `dotnet:guide` *auto* | EF Core (queries, migrations), ASP.NET Core (DI, middleware, HttpClient), async and C# performance. Loads only the one reference that matches the task. | Picked up automatically when you work on that kind of code. |

### `postgresql`: repos that use PostgreSQL
One skill, `pg` (*auto*, or `/postgresql:pg`). It loads one focused reference per task: query tuning, indexes, schema review, migration safety, live diagnostics, Npgsql.

- **Slow query:** `/postgresql:pg <SQL>`. Haiku runs `EXPLAIN (ANALYZE, BUFFERS)` and Main reads the plan and proposes a rewrite or index.
- **Index advice / schema review:** `/postgresql:pg orders table`
- **Lock-safe migrations (incl. EF Core):** `/postgresql:pg Migrations/20261001_AddStatus.cs` flags table rewrites and long locks, and suggests the safe sequence (e.g. `CREATE INDEX CONCURRENTLY`, add the column, then backfill).
- **Production symptoms:** blocking, long transactions, bloat, vacuum, connection exhaustion.
- **Safety:** every query runs in a server-enforced read-only session with a 15 s statement timeout. The connection comes from your libpq settings (`PGSERVICE`, `PGHOST`/`.pgpass`, or a `DATABASE_URL` you name). No passwords go into commands.

### `dotnet-legacy`: WebForms / .NET Framework 4.x repos
`/dotnet-legacy:modernize [assess | webforms | framework | <area>] [--save]`

- **Assess:** Haiku inventories the projects, TFMs, non-SDK csproj files, `.aspx/.ascx/.asmx/.svc` counts, and blocking APIs (`System.Web`, `HttpContext.Current`, ViewState/Session, EF6, WCF, Remoting, BinaryFormatter, Telerik...). Main produces a risk-ranked migration assessment.
- **WebForms:** choosing between Blazor, Razor Pages, and MVC, and a page-by-page migration approach.
- **Framework to modern .NET:** SDK-style conversion, `packages.config` to PackageReference, `web.config` to `appsettings`, and replacements for EF6, WCF, and other removed APIs.
- Hand each phase to `/dotnet:plan` for a file-level plan.

### `docs-kit`: Confluence and Jira
MCP calls run in the isolated Haiku `publisher`, so Atlassian tools never load into your main session.

| Command | Use case |
|---|---|
| `/docs-kit:jira PROJ-123` *auto* | Pulls a ticket as a short summary to feed `/dotnet:plan` or `/dotnet:debug`. |
| `/docs-kit:confluence api <space>` | API reference generated from the endpoints in code. |
| `/docs-kit:confluence adr <space>` | Architecture decision record, e.g. from a `/dotnet:spike` result. |
| `/docs-kit:confluence runbook <space>` | Config keys, health checks, background services, external dependencies. |
| `/docs-kit:confluence release-notes <space>` | Built from `git log` and merged PRs between two refs. |
| `/docs-kit:confluence qa-guide <space>` | Inputs, validators, workflow branches, and error paths for testers. |

Pass a page URL or id instead of a space to update an existing page.

### Typical flows
- **New feature, gated end to end:** `/dotnet:flow PROJ-1`. Approve after each step. After reviewers comment, run `/dotnet:flow resume PROJ-1` (or `/dotnet:pr-comments <PR#>`) to address the feedback. `/clear` + `/dotnet:flow resume PROJ-1` between phases keeps the cost down.
- **New feature, step by step:** `/dotnet:analyze PROJ-1`, then `/dotnet:plan <analysis file>`, `/dotnet:implement`, `/dotnet:review`, and `/dotnet:pr`.
- **Quick change, no TDD:** `/dotnet:implement --no-tdd <task>`, then `/dotnet:tests <target>` later if needed, and `/dotnet:pr`.
- **Production bug:** `/dotnet:debug <stack trace>`, then `/dotnet:tests <fix area>` and `/dotnet:pr`.
- **Tech decision:** `/dotnet:spike <question> --poc`, then `/docs-kit:confluence adr <space>`.
- **Legacy migration:** `/dotnet-legacy:modernize assess`, then `/dotnet:plan <phase 1>` and `/dotnet:implement`.
- **Slow endpoint on PostgreSQL:** `/postgresql:pg <query>`, then `/dotnet:implement` for the index migration.

## How cost is controlled
1. **Model tiering.** Your main session (Sonnet 5.5 recommended) judges. Haiku executors do I/O at about 1/40 of the Opus 5.5 token price. Nothing pins Opus.
2. **Small fixed overhead.** 5 plugins and a handful of skills. Heavy workflows are user-invoked only (`disable-model-invocation`), so they cost nothing until you call them. Guidance loads one reference file at a time.
3. **Bounded returns.** Executors return 30–40 lines max. Build and test output is condensed by `dotnet.sh` before any model sees it.
4. **Cache-friendly.** Static agent and skill bodies, no inline model switches, MCP servers isolated in a subagent.
5. **Reports go to chat.** Files (`--save`, analysis, flow specs) go to `.reports/` at the repo root. The skills add it to the repo's local git exclude, so nothing is committed by accident.
6. **GitHub: `gh` first, MCP as fallback.** `gh` adds no tool schemas, and `--json`/`--jq` keep the output small. The GitHub MCP is used only when `gh` can't be (PR creation or metadata), and only inside the isolated `publisher`. `/core:setup` offers to remove it from the main session.

Check the overhead in any session with `/context`.

## Benchmark: old 12 plugins vs these 5
Eight SDLC tasks, run on eShopOnWeb (.NET 8) and eShopLegacyWebForms (.NET Framework 4.7.2) with bugs planted as ground truth. Main model Sonnet 5.5.

| Task | Old $ | New $ | Quality |
|---|---|---|---|
| review (core / legacy) | 0.201 / 0.208 | **0.085 / 0.085** | both found 4/4 planted bugs; new also runs the tests |
| debug (core / legacy) | 0.173 / 0.139 | **0.067 / 0.125** | both found the root cause |
| spike (core / legacy) | 0.158 / 0.251 | 0.184 / **0.116** | new cites sources (URLs, `path:line`). On legacy, old missed EF6 (3/4) and new found 4/4 |
| implement (core / legacy) | 0.140 / 0.332 | **0.125 / 0.314** | both green; new follows TDD |
| **Total** | **$1.60** | **$1.10 (−31%)** | new equal or better on every task |

The fixed overhead per request is **+381 tokens instead of +4,510**, and you pay it on every turn of every session. New is slower in wall time because it runs tests during review, sources its research, and works TDD. Details: [docs/RESEARCH.md §12](docs/RESEARCH.md).

## Requirements
- A recent Claude Code (tested on 2.1.295). Its default compaction already keeps Haiku requests under 100K tokens.
- `bash` (Git Bash on Windows), plus the .NET SDK and/or Visual Studio Build Tools for legacy projects.
- Optional: `psql` (PostgreSQL), `gh` (GitHub PRs), the Atlassian remote MCP (docs-kit).

## Development
`scripts/validate.sh` runs `claude plugin validate --strict` on the marketplace and every plugin. The design and the decisions behind it are in [docs/RESEARCH.md](docs/RESEARCH.md).
