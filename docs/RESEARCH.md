# ritesh-marketplace: Review and Redesign Research

> Status: **draft for discussion**. Nothing has been changed yet.
> Date: 2026-10-09 · Baseline commit: `ab9197b`
> Goals: (1) list corrections, (2) make it cheap to run on metered billing, (3) add PostgreSQL and .NET Core plugins, (4) send exploration, git and build/test work to Haiku 5.5 subagents, (5) make it work on any .NET repo, both SDK-style (.NET Core/5+) and legacy .NET Framework, (6) keep setup to one or two commands.

---

## 1. Current state at a glance

| Metric | Value |
|---|---|
| Plugins | 12 |
| Agents / commands | 43 / 43 |
| Skill files | 36 copies of **13 unique** skills, plus 6 stray `.md` files that never load |
| Total prompt text | **~2.38 MB ≈ 600k tokens** |
| Largest agent prompt | `schema-migration-planner.md`, 64 KB ≈ 16k tokens |
| Typical command prompt | 4–17 KB ≈ 1–4k tokens, loaded into the **main** (most expensive) context |
| Agents with `model:` set | 8 of 43, all `sonnet`. The other 35 inherit the main model |
| PostgreSQL coverage | ~0 (12 passing mentions). SQL Server: ~300 mentions |
| `dotnet build` / `dotnet test` coverage | 1 mention |
| EF Core / ASP.NET Core coverage | ~0. The focus is LINQ-to-SQL, WebForms, Telerik and .NET Framework |
| Validation / CI / evals | none |
| Paid on **every request** of every session (listing) | ~17 KB of agent/command/skill descriptions ≈ **5–6k tokens**, whether or not any of it is used |

**Verdict:** the content has real domain value (SQL tuning, LINQ-to-SQL, WebForms migration). The *wiring* is mostly broken or ignored by Claude Code, and the *cost profile* is the worst possible: large prompts, everything on the main model, and fan-out to `general-purpose` agents that inherit Opus.

---

## 2. Corrections (prioritized)

Severity: 🔴 broken or very costly · 🟠 wrong or misleading · 🟡 hygiene

| # | Sev | Finding | Evidence | Fix |
|---|---|---|---|---|
| C1 | 🔴 | **Commands never use the plugin's own agents.** They spawn `subagent_type: "general-purpose"` with an inline prompt, so the 43 agent files are dead weight for every command flow. | e.g. `analysis-toolkit/commands/analyze-query.md` Step 4 (3× general-purpose) | Dispatch named agents (`<plugin>:<agent>`) or use skills with `context: fork` + `agent:` |
| C2 | 🔴 | **No model pinning.** `general-purpose` and the 35 agents without `model:` inherit the main session model (Opus/Fable when that's the main model). Grep, git log and build log reading are billed at top-tier rates. | frontmatter scan | `model: haiku` on worker agents, `model: sonnet` only where judgment is needed (see §4) |
| C3 | 🔴 | **Huge prompts.** Agents run 300–1,640 lines. Each spawn pays that full system prompt. Commands put 1–4k tokens into the main context, where they persist for the rest of the conversation. | §1 sizes | Agents ≤ 120 lines, skills ≤ 150 lines, detail moved to `references/*.md` that load only when needed |
| C4 | 🔴 | **Hand-off through files.** Subagents write `marketplace/output/...md` and the main agent reads them back, so the tokens are paid twice. The files also land inside the user's repo and pollute git. | 100+ `marketplace/output/` refs | Subagents return a bounded summary (≤ 40 lines). Write a file only when the user asks for a report |
| C5 | 🔴 | **Leaf agents can spawn agents.** 21 agents have `Task`, and nesting is allowed 3 levels deep, so one command can cascade into many Opus subagents. | `tools: [..., Task]` | Remove `Task`/`Agent` from every leaf agent. Only the orchestrating skill fans out |
| C6 | 🟠 | **`plugin.json` is in the wrong place.** It must be at `<plugin>/.claude-plugin/plugin.json`. Today it sits at the plugin root and is ignored, so author, keywords and descriptions are lost. | all 12 plugins | Move it, or delete it and rely on the marketplace entry |
| C7 | 🟠 | **Skills lack frontmatter.** 30 `SKILL.md` files have no `name`/`description`, so auto-triggering is weak. 6 loose files (`skills/*.md` that aren't `<name>/SKILL.md`) are **never loaded**. | e.g. `confluence-document-creator/skills/technical-writing-guide.md` | Add frontmatter. Delete the strays (they're older copies) |
| C8 | 🟠 | **Broken references** to `../../shared-skills/*.md`. That directory doesn't exist, and a `..` path escaping the plugin root can't work after install because plugins are copied to a cache. | `db-query-analyzer.md:537` and others | Refer to skills by name, or use `${CLAUDE_PLUGIN_ROOT}` for files inside the same plugin |
| C9 | 🟠 | **Skill duplication**: 13 skills copied into up to 4 plugins each (~700 KB). They will drift, and each copy adds its own skill-listing entry to every session. | md5 scan | One owner plugin per skill. Others declare `dependencies` |
| C10 | 🟠 | **Fake features**: `--async/--wait` flags, hard-coded progress bars ("6–8 minutes"), "Effort to Implement: 3–4 hours", "Status: Production Ready", "Sequential Thinking" (no MCP declared). The model may imitate these or report fabricated timings. | review-suite, analysis-toolkit | Delete |
| C11 | 🟠 | **Wrong MCP usage**: "Use Bash with MSSQL MCP". MCP tools aren't called through Bash. No `.mcp.json` ships, and the `mssql`/`jira` requirements are undocumented. | `analyze-query.md` Task 1/2 | Either bundle `.mcp.json` with setup docs, or use the CLI (`sqlcmd`/`psql`) through Bash |
| C12 | 🟠 | **Non-standard frontmatter** (`task_type`, `mcp_required`, `sequential_thinking`, `async_capable`, `output_directory`, `status`, `last_updated`, ...) is silently ignored. It adds noise and suggests behavior that doesn't exist. | frontmatter scan | Remove. Use real fields: `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills` |
| C13 | 🟠 | **Overprivileged agents**: 41 of 43 agents have Write/Edit, including pure analyzers. | frontmatter scan | Analyzers and workers get read-only tools |
| C14 | 🟠 | **Overlapping plugins**: RCA appears twice (analysis-toolkit, root-cause-analyzer), query optimization three times (analysis-toolkit, optimization-engine, linq-to-sql-expert), schema twice, brainstorming next to planning. Users can't tell which one to use. | plugin list | Consolidate (see §3) |
| C15 | 🟡 | Two marketplace manifests (`marketplace.json` for Copilot, `.claude-plugin/marketplace.json` for Claude Code) that will drift. Versions are duplicated in marketplace entries and `plugin.json`, and the manifest version wins. | root | Keep one source of truth (open question Q1) |
| C16 | 🟡 | Placeholder `owner.email: ritesh@example.com`. The README is a single line (`# copilot-marketplace`). The marketplace description's counts are wrong (it says "12 shared skills"). | root | Fix |
| C17 | 🟡 | No `claude plugin validate --strict`, no evals, no CI. | — | Add a validate script, and later `claude plugin eval` for 3–4 core skills |
| C18 | 🟡 | Per-plugin README/CHANGELOG files are ~20 KB each, stale, and describe fake features. They aren't loaded into context, so they don't add cost. | — | Collapse into the root README |
| C19 | 🔴 | **Everything is listed in every session**: 12 plugins × agents/commands/skills ≈ 5–6k tokens on every request, no matter the repo or task. Nothing is opt-in, nothing uses `disable-model-invocation` or `paths`. | §1 | §4.6 |
| C20 | 🔴 | **No caching/compaction design**: big command bodies stay in context and are re-read every turn. Large tool results (Confluence pages, full logs) land in the main context. Specialized agents each pay their own cache write. | §2 C3/C4 | §4.7–4.9 |
| C21 | 🟠 | **MCP actions run in the expensive context**: Confluence create/update and Jira fetch happen in the main session or in Opus-inherited agents, and full page bodies get echoed back. | confluence-document-creator, analysis-toolkit/jira | `publisher` work orders (§4.8) |

---

## 3. Target architecture

### 3.1 Principle: split plugins by stack, not by function

A disabled plugin costs **zero** tokens. An enabled plugin costs its skill and agent *descriptions* in every session. So group by technology. A repo enables only what it uses.

```
ritesh-marketplace/
├── .claude-plugin/marketplace.json
├── README.md                      # 2-command setup
├── scripts/validate.sh            # claude plugin validate --strict on every plugin
└── plugins/
    ├── core/                      # executors, stack-agnostic, reused by every plugin (D6)
    │   ├── .claude-plugin/plugin.json
    │   ├── agents/
    │   │   ├── scout.md           # haiku: read-only locate/read/grep
    │   │   ├── runner.md          # haiku: shell work orders (git, gh, dotnet, msbuild, psql)
    │   │   └── reviewer.md        # sonnet: large-diff review chunks only
    │   └── skills/setup/          # /core:setup: global settings + user-level publisher (D7, D11)
    ├── dotnet/                    # any .NET repo (Core + Framework). depends: core
    │   ├── scripts/
    │   │   ├── dotnet-detect.ps1 / .sh   # SDK-style vs legacy, TFMs, test projects
    │   │   └── dotnet-build.ps1 / .sh    # right toolchain + condensed output
    │   └── skills/
    │       ├── build/   test/   review/   debug/   plan/
    │       ├── efcore/        (SKILL.md + references/)
    │       ├── aspnetcore/    (SKILL.md + references/)
    │       └── csharp-perf/   (async, allocations, DI lifetimes)
    ├── postgresql/                # NEW. depends: core. psql via runner + optional .mcp.json (D3)
    │   └── skills/ pg-query-tune/  pg-index-advisor/  pg-schema-review/
    │               pg-migration-safety/  pg-diagnose/
    ├── dotnet-legacy/             # opt-in: WebForms modernization + Framework→.NET migration only (D13)
    │   └── skills/ webforms-modernization/  framework-migration/
    └── docs-kit/                  # opt-in: Confluence pages, Jira ticket intake. depends: core
        └── skills/ confluence-publish/  jira-intake/  (work orders → user-level publisher)
```

12 plugins → **5**. Current-to-new mapping:

| Current | → New |
|---|---|
| review-suite, development-suite, root-cause-analyzer, analysis-toolkit (stacktrace/impact/RCA), planning-suite, brainstorming-suite, architecture-advisor (generic parts) | `dotnet` (skills: review, debug, plan) |
| architecture-advisor (WebForms + Framework migration skills) | `dotnet-legacy` |
| confluence-document-creator, analysis-toolkit (qa-testing-guide, jira) | `docs-kit` |
| linq-to-sql-expert, optimization-engine (SQL Server parts), database-schema-analyzer, telerik-control-expert, analysis-toolkit/db-query-analyzer | **dropped** (D12, D13) |
| (new) | `core`, `postgresql` |

### 3.2 Execution model: thin orchestrator, cheap workers

```
user: /dotnet:review main
   │
   ▼  skill body (~80 lines) runs in the MAIN session (the model the user picked)
   │    !`git diff --stat main...HEAD`        ← injected by the shell, no model turn
   │
   ├──► runner (haiku, work order: git log/diff per file)   → "changed files + 1-line each, ≤40 lines"
   ├──► runner (haiku, work order: build+test script)       → "build OK / 3 errors at file:line, tests 212/214"
   │
   ▼  main session reads ≤80 lines of results and does the judgment
   └──► (only if diff > N files) reviewer (sonnet) per chunk
```

Rules:
1. **Workers gather, the main session judges.** Haiku handles anything that is mostly I/O: grep, read, git, build logs, psql output.
2. **Bounded returns.** Every worker prompt ends with an output contract such as "≤ 40 lines, `file:line` refs, no code blocks over 10 lines". The return lands in the expensive context, so it must stay small.
3. **Fan out only when the work is big.** Each subagent spawn has a fixed overhead (system prompt + tool definitions). For small diffs, one Bash call in the main session is cheaper than three agents.
4. **Do deterministic work in scripts, not the model.** Detection, toolchain choice and log filtering are code (`scripts/*.ps1|.sh`). Haiku runs one command and interprets about 30 lines.
5. **Skills over commands.** `commands/` still works, but skills add `context: fork`, `agent:`, `model:`, `effort:`, `disable-model-invocation` and supporting files.

---

## 4. Cost optimization (metered billing)

### 4.1 Model tiering

| Tier | Where | Settings |
|---|---|---|
| **Haiku 5.5** | scout, runner, publisher (**execution only**, §4.8) | `model: haiku`, `effort: medium`, `maxTurns: 6–12`, minimal `tools`, no `Agent` |
| **Sonnet 5.5** | `reviewer` (large diffs only), deep RCA if delegated | `model: sonnet`, `maxTurns: 15` |
| **Main session** | orchestration + final judgment | the user's choice. Recommend Sonnet as the default and Opus only when needed |
| **Opus** | never pinned in the plugins | — |

Use the alias `haiku`, not a full model ID, so the plugin follows future Haiku releases.

### 4.2 Token-level levers (by expected impact)

1. **Pin models** (C2). This is the biggest lever: about 90% of the token volume in these flows is exploration and log reading.
2. **Shrink prompts** (C3). 600k → target **< 60k** total prompt text. Agent spawns become ~5–10× cheaper in system-prompt cost.
3. **No file round-trips** (C4). Removes one write plus one read of every intermediate artifact.
4. **Bounded worker output.** Keeps the expensive context small for the rest of the conversation, which also lowers the cost of cached re-reads on every later turn.
5. **`!` shell injection** for cheap facts (`git diff --stat`, `dotnet --list-sdks`). Never inject a *full* diff or log; give it to a worker instead.
6. **Condensed build/test output**: `dotnet build -nologo -v q -clp:ErrorsOnly`, `dotnet test --no-build -nologo -v q --logger "console;verbosity=minimal"`. This complements the user's RTK hook.
7. **`disable-model-invocation: true`** on heavy workflows (review, plan, migration). They then run only when the user types the slash command, so the model can't start a costly flow on its own.
8. **CLI over MCP** by default (`psql`, `gh`). There are no always-on tool schemas, and safety is enforced through connection options (§6.2). The Postgres MCP stays optional (D3), and the GitHub MCP is a fallback only (D14).
9. **Stable prompt prefixes.** Keep skill and agent bodies static, with no timestamps or dates, so prompt caching hits.

### 4.3 Global defaults that the setup applies (user opt-in, see Q7)

```jsonc
// ~/.claude/settings.json (approved: D7)
{
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" }         // any agent without a model pin → haiku
}                                                          // no compaction setting: the default already stays < 100K (§12)
```
The built-in `Explore` agent ignores `CLAUDE_CODE_SUBAGENT_MODEL` and runs on the main model. To make Explore cheap, place a user-level override at `~/.claude/agents/Explore.md` with `model: haiku`. A plugin agent can't do this because plugin agents are namespaced (`dotnet:Explore`), so the file has to be user-level. Plugin `settings.json` can't set `env` (only `agent` and `subagentStatusLine`), so these values can't ship inside the plugin and must go in user settings.

### 4.4 Measuring it (before/after)

Run the same 4 tasks on one sample Core repo and one Framework repo, with `claude -p "<task>" --output-format json` (it reports usage/cost), before and after:
`review a 10-file diff`, `why does build fail`, `tune this slow EF/PG query`, `explain module X`.
Also run `/context` in a fresh session before and after to see the fixed per-session overhead.
Target: **≥ 60% cost reduction** at equal or better answer quality. That number is a target to verify, not a promise.

### 4.5 Reference prices (Anthropic API, per MTok, cached 2026-10-06)

| Model | Input | Output | Cache read | Context |
|---|---|---|---|---|
| Opus 5.5 | $4.00 | $20.00 | $0.20 | 1M |
| Sonnet 5.5 | $2.00 | $10.00 | $0.20 | 1M |
| **Haiku 5.5** | **$0.10** (prompt ≤ 100K) → **$0.50** (> 100K) | **$0.50** → **$2.50** | — | 1M |

Two consequences:
- Haiku 5.5 is **40× cheaper than Opus 5.5** per token, **while its prompt stays ≤ 100K**. Moving execution work to Haiku is the single biggest saving.
- Above 100K, Haiku's per-token price **steps up 5×**. That step is why Haiku contexts must stay under 100K (§4.7).

### 4.6 Session-start cost: load by use case, not up front

**What actually loads at session start.** For every *enabled* plugin, the listing loads: the name and description of each agent, skill and command. Full agent bodies load only when that agent is spawned. Full skill/command bodies load only when invoked. Today the listing is ~5–6k tokens per session, and it rides along in **every request**. Most of it is billed as cached reads, but it is never free and almost none of it gets used.

Controls, from biggest effect to smallest:

| Control | Effect | Used for |
|---|---|---|
| **Enable plugins per project** (`enabledPlugins` in the repo's `.claude/settings.json`) plus `defaultEnabled: false` on opt-in plugins | a disabled plugin costs **0 tokens** | `postgresql` only in PG repos. `dotnet-legacy` only in Framework/WebForms repos. `docs-kit` only where Confluence is used |
| **`disable-model-invocation: true`** on skills | removes the skill from the listing entirely. It loads only when the user types `/name` | all heavy workflows: review, plan, rca, migration, confluence-publish |
| **`paths:` globs** on skills | auto-load only when matching files are involved | `efcore` → `**/*DbContext*.cs, **/Migrations/**`. `pg-*` → `**/*.sql`. `aspnetcore` → `**/Program.cs, **/*Controller.cs` |
| **Few agents, one-line descriptions** | agents have no defer mechanism, so the count and length of descriptions is the only lever | 4 agents total in `dotnet`. Worker descriptions are like "Executes a shell work order from the dotnet skills. Not for direct use." (~15 tokens) |
| **MCP tool search** (on by default) | MCP tool *schemas* are deferred, and only tool names sit in context | Atlassian / Postgres MCP if used |

Target: the fixed listing goes from **~5–6k → < 1k tokens** in a typical .NET repo. Measure it with `/context`.

### 4.7 Compaction strategy

| Context | Strategy |
|---|---|
| **Haiku workers** | **Primary: never reach 100K by design.** One work order per spawn, so every spawn starts fresh. `maxTurns` 6–12. Scripts condense output (errors only, `head -n`). The main session splits big jobs into chunks (per project, per folder, per 20 files). **Safety net (D10):** Claude Code's default compaction, which already keeps Haiku under 100K. The per-model `autoCompactWindow` setting was tested and has no effect (§12). |
| **Main session** | Bounded worker returns (≤ 40 lines) keep the context small, so compaction is needed much less often. Skills end each phase with a 5-line state summary so `/compact` keeps what matters. Guidance in the README: `/clear` between unrelated tasks (cheapest), `/compact <focus>` at phase boundaries |
| **Skill bodies after compaction** | Claude Code re-attaches the first 5k tokens of each invoked skill (25k total). Keeping skills ≤ 150 lines means they survive compaction intact |

### 4.8 Haiku = execution only: the work-order pattern

The main model does **all** of the reasoning: what to do, which files, the exact commands, and the exact payload. Haiku receives a **work order** and executes it literally.

```text
WORK ORDER
goal:      run tests for the changed projects
steps:     1. pwsh ${CLAUDE_PLUGIN_ROOT}/scripts/dotnet-build.ps1 -Target test -Projects src/Api/Api.csproj
inputs:    (paths, page ids, payload files)
return:    status | failures as `path:line message` | ≤ 30 lines
on-error:  retry once, then return "BLOCKED: <one line>"
```

Agent prompt rules (identical in all three executors):
1. Execute the steps in order. **No design decisions, no extra exploration, no fixing code.**
2. If a step is ambiguous or fails twice → return `BLOCKED: <reason>`. Never guess.
3. Return only what `return:` asks for. Never echo large tool output (page bodies, full logs, full diffs).
4. Minor reasoning is allowed only for **condensing**: dedupe errors, pick the relevant lines, map an error to `file:line`.

**Three generic executors instead of many specialists.** Fewer descriptions in the listing, and an executor's system prompt and tool list stay the same on every spawn. So **repeated spawns reuse the same prompt cache** for that agent's prefix, while ten specialized agents would each pay their own cache write.

| Agent | Tools | Typical work orders |
|---|---|---|
| `scout` | Read, Grep, Glob | "find all callers of X", "read these 5 files and return signatures only" |
| `runner` | Bash, Read | git log/diff/blame, `dotnet`/`msbuild`/`vstest` scripts, read-only `psql` |
| `publisher` | named MCP tools only (e.g. `mcp__atlassian__createConfluencePage`, `...updateConfluencePage`, `...getConfluencePage`, Jira read) + Read | create or update Confluence pages, fetch a Jira ticket condensed to ≤ 30 lines |

**Confluence and other MCP writes through `publisher`:**
1. The main model writes the final page content once to a temp file (e.g. `%TEMP%/ritesh/<slug>.md`, outside the repo) and sends a work order with `space`, `parentId` or `pageId`, `title`, and the file path.
2. Haiku reads the file. For an update, it fetches the page's current version number only. Then it calls create/update and returns **only** `pageId | version | url`.
3. The main context never sees the page body echoed back from the API. With today's design, a Confluence `get` result (large storage-format HTML) lands in the expensive context.

**Full isolation (D11).** Claude Code ignores `mcpServers` in *plugin* agent frontmatter, so `publisher` is **not** a plugin agent. `/core:setup` installs it as a user-level agent at `~/.claude/agents/publisher.md`, from `templates/publisher.md`, with inline servers:
- **Atlassian**: the official remote server (Confluence + Jira). The URL is copied from your existing config.
- **GitHub**: fallback only. PR and git work go through `gh` via `runner` first (D14).

After that, setup **removes** those servers from the main config (`~/.claude.json` / `.mcp.json`), with a backup and only after confirmation. Otherwise the main session would still load them. Risks to verify in P1: (1) whether the remote server's OAuth token is reused when the subagent connects, or whether it asks to log in again; (2) inline servers connect on every spawn, which adds a little startup time per publish.

### 4.9 Prompt-caching rules for this marketplace

Claude Code caches automatically. The plugins must avoid breaking it:

| Rule | Why |
|---|---|
| **No `model:` on skills that run inline** in the main session | the cache is per model. Switching the turn's model re-reads the whole conversation **uncached** on the new model. Cheap work goes to a forked agent (`context: fork` + `agent:`) or an executor, never through an inline model switch |
| **No mid-session effort/model changes** in the main session | invalidates the message cache |
| **Static agent/skill bodies** (no dates, versions or counters) | executors' prefixes stay byte-identical, so they hit the cache across spawns |
| **`!` injections only at the end of a skill body** and small (`--stat`, not full diffs) | everything before the dynamic part stays cacheable |
| **Don't toggle plugins/MCP mid-session** | the tool list is the first thing in the prefix. Changing it invalidates everything |
| **Fork vs fresh agent** | a *fork* reuses the parent's cache but runs on the parent's (expensive) model, so use it only for reasoning-heavy delegation. **Executors are fresh Haiku agents** with a short work order. Their cache is separate but tiny and repeatable |
| **Cache TTL** | 5-minute default. For long sessions with idle gaps, `CLAUDE_CODE_PROMPT_CACHE_TTL=1h` (main) and `experimental.cacheTtl: 1h` (agents that respawn often over a long session) avoid repeated cache writes. A 1h write costs more than a 5m write, so it pays off only if the cache is reused after the 5-minute window (verify that `experimental.cacheTtl` is honored for plugin agents) |

---

## 5. Base `dotnet` plugin: works on Core and Framework

### 5.1 Detection (script, deterministic)

| Signal | Meaning |
|---|---|
| `*.slnx` / `*.sln` | entry point (prefer `.slnx`, then `.sln`, then a single `*.csproj`) |
| `<Project Sdk="...">` | SDK-style. Build with `dotnet`, even when the TFM is `net48` |
| `ToolsVersion=` without `Sdk` | legacy (non-SDK) .NET Framework project |
| `packages.config` | needs `nuget restore` / `msbuild -t:restore -p:RestorePackagesConfig=true` |
| `<TargetFramework(s)>` `net4x` vs `net6.0+` | Framework vs modern runtime |
| `global.json` | pinned SDK. Check it with `dotnet --list-sdks` |
| refs to xunit / nunit / MSTest | test projects |

The script prints about 10 lines of JSON so the agent never has to parse `.csproj` itself.

### 5.2 Toolchain matrix

| Project type | Build | Test |
|---|---|---|
| SDK-style (any TFM) | `dotnet build <sln> -nologo -v q -clp:ErrorsOnly` | `dotnet test <sln> --no-build -nologo -v q --logger "console;verbosity=minimal"` |
| Legacy Framework (Windows) | `msbuild` found via `vswhere -latest -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\MSBuild.exe`, run with `-m -nologo -v:q -clp:ErrorsOnly` | `vstest.console.exe` (via vswhere) on test DLLs |
| Legacy Framework (non-Windows) | report "needs Windows/VS Build Tools". Don't guess | — |
| Mixed solution | if any legacy project exists → msbuild for the whole solution | per project type |

### 5.3 Worker agent sketch (illustrative)

```yaml
---
name: runner
description: Executes a shell work order from the dotnet/postgresql skills. Not for direct use.
model: haiku
effort: medium
maxTurns: 8
tools: Bash, Read
omitClaudeMd: true        # work order carries everything; saves CLAUDE.md tokens per spawn (verify for plugin agents)
---
You execute WORK ORDERS literally. Run the listed steps in order.
Do not explore, decide, design, or edit files. If a step is ambiguous or fails twice,
stop and return "BLOCKED: <one line>". Return exactly the `return:` format, ≤ 30 lines.
Condense only: dedupe errors, `path:line CODE message`, first assertion line per failed test.
Never paste full logs, diffs, or query results.
```
The build/test skill (main session) chooses the toolchain from the detect script (§5.1) and writes the work order. The runner only runs it.

### 5.4 .NET Core skill content (new, concise)

- **efcore**: N+1 (`Include` vs split queries vs projection), `AsNoTracking`, `ToQueryString()` / logging to see SQL, compiled queries, bulk `ExecuteUpdate/ExecuteDelete`, migrations hygiene, DbContext lifetime.
- **aspnetcore**: DI lifetimes (captive dependencies), middleware order, minimal APIs vs controllers, `IHttpClientFactory`, options pattern, health checks, logging and `ProblemDetails`.
- **csharp-perf**: sync-over-async / `.Result` deadlocks (classic ASP.NET), `ConfigureAwait`, allocations, `Span<T>`, `ValueTask`, cancellation tokens.
- **review / debug / plan**: rewritten from the existing review-suite, RCA and planning content, ≤ 150 lines each, with checklists in `references/`.

---

## 6. New `postgresql` plugin

### 6.1 Skills

| Skill | Covers |
|---|---|
| `pg-query-tune` | `EXPLAIN (ANALYZE, BUFFERS)` reading, seq vs index scans, row-estimate errors, `work_mem` spills, `pg_stat_statements` top-N |
| `pg-index-advisor` | missing FK indexes, unused (`pg_stat_user_indexes`), duplicate or overlapping, partial and covering (`INCLUDE`), GIN for `jsonb`/arrays |
| `pg-schema-review` | types (`text` vs `varchar`, `timestamptz`), constraints, identity vs serial, naming, partitioning candidates |
| `pg-migration-safety` | lock-safe DDL: `CREATE INDEX CONCURRENTLY`, `lock_timeout`, adding `NOT NULL`/defaults safely, EF Core migrations that need `suppressTransaction` |
| `pg-diagnose` | blocking (`pg_blocking_pids`), long transactions, bloat and autovacuum lag, connection saturation |
| (in efcore refs) Npgsql specifics | `timestamptz` + `DateTime.Kind` (Npgsql 6+), snake_case naming convention, pooling and multiplexing, retry on failure, `jsonb` mapping |

### 6.2 Access: safe and free of configuration

- Use standard libpq configuration (`PGSERVICE` + `pg_service.conf` + `.pgpass`, or `DATABASE_URL`). The plugin stores **no secrets**.
- The `runner` (haiku) gets psql work orders that always run:
  `PGOPTIONS="-c default_transaction_read_only=on -c statement_timeout=15000" psql -X -A -F'|' ...`
  This is read-only at the server-session level, not just in the prompt.
- `EXPLAIN ANALYZE` actually executes the statement, so for DML the agent wraps it in `BEGIN; ... ROLLBACK;` or uses plain `EXPLAIN`. The read-only flag blocks writes regardless.
- An MCP Postgres server is an **optional** `.mcp.json` for users who prefer it (Q3).

---

## 7. Setup UX (target: 3 commands)

```text
/plugin marketplace add <github-user>/ritesh-marketplace     (or a local path)
/plugin install core@ritesh-marketplace dotnet@ritesh-marketplace   (+ postgresql / dotnet-legacy / docs-kit per repo)
/core:setup                                                   (one time: global settings + user-level publisher)
```
`/core:setup` is user-invoked only. It shows a diff of every global change (§4.3, D7, D11), backs up the files it touches, and applies only after confirmation. It's idempotent, so re-running it changes nothing.

Per-repo enablement goes in the repo's `.claude/settings.json` (`enabledPlugins`). The README gives a ready snippet per stack.

Root README: one table "which plugin for which repo", the commands above, and a 5-line "how costs are controlled" section.

---

## 8. Phased plan

| Phase | Scope | Risk |
|---|---|---|
| **P0 Fix-ups + cleanup** | delete root `marketplace.json` (D1) and the old 12 plugins (D2, after P1–P3 content is salvaged), `scripts/validate.sh` | low |
| **P1 `core` + `dotnet`** | scout/runner/reviewer, `templates/publisher.md`, `/core:setup`; detect/build scripts (ps1 + sh); build/test/review/debug/plan + efcore/aspnetcore/csharp-perf. **Verify:** Haiku per-model compaction applies to subagents; Atlassian OAuth inside a user-level agent; `omitClaudeMd` / `experimental.cacheTtl` honored for plugin agents | medium |
| **P2 `postgresql`** | 5 skills, psql work orders via `runner`, optional `.mcp.json` (disabled by default) | low |
| **P3 `dotnet-legacy` + `docs-kit`** | WebForms + Framework migration skills (trimmed, with `references/`); confluence-publish + jira-intake via publisher work orders | low |
| **P4 Measure** | §4.4 on public samples (D9): an eShop-style .NET Core repo + a public WebForms/.NET Framework sample. `/context` before/after, `claude -p --output-format json` cost per task, `claude plugin eval` for review, build, pg-query-tune | low |

Implementation note: P1–P3 are file-heavy but independent per plugin. They can run as parallel subagents with one plugin per agent, and I review each result.

---

## 9. Decisions (2026-10-09)

| # | Topic | Decision |
|---|---|---|
| D1 | Copilot CLI | **Claude Code only.** Delete the root `marketplace.json` |
| D2 | Old 12 plugins | **Remove outright** once content is salvaged |
| D3 | Postgres access | **psql via `runner`** (read-only `PGOPTIONS`) + **optional** Postgres MCP config |
| D4 | Main-session model | **Sonnet 5.5**. Synthesis stays in the main session, and `reviewer` (Sonnet) is used only for very large diffs |
| D5 | Configured MCPs | GitHub, Confluence, Jira, PostgreSQL. **No MSSQL** |
| D6 | Executors location | separate **`core`** plugin, reusable by any future plugin |
| D7 | Global settings via setup | approved: `CLAUDE_CODE_SUBAGENT_MODEL=haiku`, Explore → Haiku override, Haiku `autoCompactWindow` |
| D8 | Reports | **chat only**. `--save` writes a file outside the repo (or a gitignored folder) |
| D9 | Benchmark | public sample repos (one .NET Core, one .NET Framework/WebForms) |
| D10 | Haiku 100K compaction | **`modelSettings.haiku.autoCompactWindow: 100000`**, applied by `/core:setup` (§14). It was dropped once on 2.1.295 (§12), but on 2.1.302 the default lets Haiku run to ~967K. Design limits in §4.7 stay |
| D11 | MCP isolation | **full isolation**: user-level `publisher` with inline Atlassian (+ GitHub fallback). The servers are removed from the main config |
| D12 | Atlassian MCP | official Atlassian remote server |
| D13 | SQL Server / legacy scope | **SQL Server dropped** (LINQ-to-SQL, MSSQL query/schema tools, Telerik dropped too). `dotnet-legacy` keeps only **WebForms modernization** + **.NET Framework → .NET migration** |
| D14 | GitHub | **`gh` CLI via `runner` first** (pr, review, ci, release notes). GitHub MCP only as a fallback inside `publisher` (PR creation, PR metadata), never in the main session. review falls back to `git fetch pull/<n>/head`; ci requires `gh` |
| D15 | `mssql-to-pg` | **Not needed.** No SQL Server → PostgreSQL migration skill |

---

## 10. Implementation notes (P1–P3, as built)

Where the build deviates from the plan above, and why:

| Plan | As built | Why |
|---|---|---|
| `templates/` at the repo root | `plugins/core/templates/` (Explore.md, publisher.md) | only the plugin directory is installed, so `${CLAUDE_PLUGIN_ROOT}` must reach the templates |
| `dotnet-detect` + `dotnet-build`, each as `.ps1` + `.sh` | one `plugins/dotnet/scripts/dotnet.sh` (`detect`/`build`/`test`) | Claude Code's Bash tool runs bash on every OS (Git Bash on Windows); one script, half the code |
| efcore / aspnetcore / csharp-perf as 3 skills | one `dotnet:guide` skill (`paths`-gated) + 3 reference files | one listing entry instead of three; references load only when needed |
| 5 pg skills + `pg-inspector` agent | one `postgresql:pg` skill + 6 reference files; live SQL goes to `core:runner` | one listing entry, no extra agent, prompt cache shared with the other runner work |
| optional Postgres `.mcp.json` | not shipped; the skill falls back to an existing Postgres MCP when `psql` is missing | you already have a Postgres MCP; shipping a config would load it in every session |
| `dotnet-legacy` with two skills | one `modernize` skill + `webforms.md` + `framework-to-net.md` | same reason |
| docs-kit `confluence-publish`, `jira-intake` | `docs-kit:confluence` (user-invoked) and `docs-kit:jira` | shorter commands |

Skill invocation modes:
- **`context: fork` into Haiku:** `dotnet:build`.
- **Model-invocable (in the listing):** `dotnet:guide` (only on matching paths), `postgresql:pg`, `docs-kit:jira`. *(Superseded: since 9c935fc every skill is user-invoked; `paths:` was removed from `dotnet:guide` in §17.)*
- **User-invoked only (not in the listing):** `dotnet:review`, `dotnet:debug`, `dotnet:plan`, `dotnet-legacy:modernize`, `docs-kit:confluence`, `core:setup`.

### Verified
- `claude plugin validate --strict`: marketplace + all 5 plugins pass.
- `dotnet.sh` on a .NET 9 SDK solution: detect; a build with 2 compiler errors comes back condensed to 2 lines; a failing xUnit test shows its name, expected/actual, and the `file:line`.
- `dotnet.sh` on a legacy non-SDK `v4.8` project: MSBuild found via vswhere; build OK and build-error paths.
- Live run: `claude -p "/dotnet:build test"` with the plugins loaded forked straight into `core:runner` on Haiku 5.5 and returned the condensed failure. **Cost: $0.0013**, with no main-model turns.
- The modernize inventory commands, and the `gh ... --jq` release-notes command syntax.

### Measured: fixed overhead per request (Sonnet 5.5, `claude -p "Reply with OK."`, 2026-10-09)
| Setup | Input tokens per request | Plugin overhead |
|---|---|---|
| no plugins from this marketplace (your other global plugins/MCPs only) | 44,216 | — |
| old 12 plugins (ab9197b) | 48,726 | **+4,510** |
| new: all 5 plugins enabled | 44,770 | **+554** (−88%) |
| new: core + dotnet (the typical .NET repo) | 44,597 | **+381** (−92%) |

The ~44K baseline comes from other global plugins, MCPs, and CLAUDE.md, not from this marketplace. It's now the larger lever (see `/context`).

### Not yet verified (needs your environment or P4)
- The legacy test path (`vstest.console.exe` on a packages.config test project). No such sample was available offline.
- The PostgreSQL catalog/diagnostic SQL against a live server (no `psql` or database on this machine).
- `/core:setup` end to end: the Atlassian/GitHub MCP servers aren't configured on this machine (`claude mcp list` shows neither), and whether the remote Atlassian OAuth works from a user-level agent with inline `mcpServers`.
- ~~Whether `modelSettings.claude-haiku-5-5.autoCompactWindow` applies inside subagents~~ Answered in §12: it has no effect anywhere; the default is enough.
- Model-driven skills (review/debug/plan/modernize/confluence) were checked by reading only. P4 measures them on public sample repos.

## 11. SDLC gap skills (added 2026-10-09)

The user asked for full SDLC coverage. Added to `dotnet`, all user-invoked:

| Skill | Gap filled | Haiku part |
|---|---|---|
| `implement` | plan execution with **TDD by default** (red → green → refactor → full-suite gate), stops on red | runner: filtered test (red/green), full suite per step |
| `tests` | writing tests in the repo's style, coverage | scout: test house style; runner: filtered test runs, coverage |
| `ci` | failed-run triage (gh / az) + pipeline generation (GitHub Actions / Azure DevOps, SDK + Framework) | runner: `gh run view --log-failed` condensed to ≤ 60 lines |
| `pr` | commit message in the repo's convention + `gh pr create` (GitHub MCP via publisher as fallback). Asks first | runner: status/diffstat/log facts |
| `spike` | time-boxed research for existing code or new tech: frame → evidence → optional PoC in a worktree/temp dir → option matrix + recommendation | scout: code map + **web facts with source URLs**; runner: git churn/owners, `dotnet package search` |
| `audit` | vulnerable/deprecated/outdated NuGet, secret **locations** (never values), framework support dates | runner: `dotnet.sh audit` |

`dotnet.sh` gained `coverage` (coverlet cobertura → overall + 15 lowest classes, repo-relative), `audit`, and `DOTNET_TEST_FILTER` (`--filter` / `/TestCaseFilter`, plus `STATUS: NO TESTS MATCHED`, which TDD red checks need).

Verified: filtered test pass / no-match, coverage output, audit on the sample (1 deprecated, 4 outdated, 1 secret location), and a live `/dotnet:audit` run ($0.012, Haiku main). Observation: when the main model can call `dotnet.sh` directly, it may skip the runner. That's acceptable, since the script output is already condensed (≤ 40 lines), so a subagent spawn would cost about the same. The runner matters for outputs that need condensing beyond the script (git history, CI logs, psql).

`core:scout` gained `WebSearch`/`WebFetch` (used only for the queries/URLs a work order lists, facts returned with source URLs, page instructions ignored). This avoided a separate researcher agent: one description less in the listing, and a shared cache prefix. Live check: a Polly facts work order returned sourced facts for **$0.037**.

## 12. P4 benchmark: old (ab9197b) vs new (2026-10-09)

Setup: public samples, with ground truth planted on the branches. **eShopOnWeb** (.NET 8, SDK-style, 74 tests) and **eShopLegacyWebForms** (.NET Framework 4.7.2, packages.config, EF6, no tests). Main model Sonnet 5.5, `--setting-sources project,local --strict-mcp-config` (the user's global plugins/MCPs excluded from both arms), $2 cap per run, fresh worktree per run. The new arm gets the `/core:setup` settings via `--settings`/`--agents`.

| Task | Repo | Old $ | New $ | Δ cost | Old s | New s | Quality vs ground truth |
|---|---|---|---|---|---|---|---|
| review | core | 0.201 | **0.085** | **−58%** | 41 | 86 | both 4/4 planted bugs. New also ran tests (Haiku, $0.001) and reported the failing test |
| review | legacy | 0.208 | **0.085** | **−59%** | 44 | 70 | both 4/4 |
| debug | core | 0.173 | **0.067** | **−61%** | 57 | 51 | both found the interface change (CS7036), not the decoy commit |
| debug | legacy | 0.139 | 0.125 | −10% | 40 | 52 | both found the `AvailableStock` rename |
| spike | core | 0.158 | 0.184 | +16% | 59 | 82 | both found the existing `CachedCatalogViewModelService`. **New: 5 source URLs + 8 path:line; old: 0 URLs** |
| spike | legacy | 0.251 | **0.116** | **−54%** | 65 | 81 | **old 3/4 (missed EF6), new 4/4**, 10 path:line |
| implement | core | 0.143 | 0.158 | +10% | 69 | 159 | both green. New followed TDD (red first), 9 cases |
| implement | legacy | 0.289 | 0.325 | +12% | 139 | 224 | both green and both created an MSTest project. New: TDD, 25 cases |
| **Total** | | **1.562** | **1.145** | **−27%** | 514 | 805 | new ≥ old on every task |

Plus the fixed per-request overhead (§10): +4,510 → +381 tokens. That saving applies to **every turn** of an interactive session, which these single-shot runs understate.

### Findings and fixes from the benchmark
- **Bugs found and fixed in `dotnet.sh`:**
  - vswhere picked SSMS 22, so `-requires Microsoft.Component.MSBuild` is now passed.
  - packages.config wasn't restored with `-restore`, so restore now runs as a separate `-t:restore` step.
  - TFMs weren't read from `Directory.Packages.props`.
  - The test summary was capped at 3 assemblies.
  - **The test filter reported `NO TESTS MATCHED` in multi-project solutions.** Other test projects print "No test matches"; a bash precedence bug made that count. This cost implement-new extra turns. It's fixed and verified (match / no-match / unfiltered); implement wasn't re-measured.
- The old commands **didn't fan out** to `general-purpose` agents in these runs (0 subagents). Sonnet ran the large command bodies inline, which is why the old cost was lower than feared.
- The new arm's Haiku share was small ($0.069 of $1.145), but it did the web research (spike), the test runs (review), and the inventories. In implement and core-debug, the main session ran `dotnet.sh` itself instead of dispatching the runner. The cost is equivalent because the script output is pre-condensed (see §11).
- New is **~57% slower** in wall time: the review runs tests, the spike does web research, and implement runs the TDD loops. Quality is the trade.
- Each cell is a single run. Read the deltas as indicative, not statistically conclusive.

### Work-order contract validation (§4.8, after the benchmark)
- A vague scout order ("find whatever is causing the performance problems") returned `BLOCKED: work order missing scope`.
- A vague runner order ("check the logs") returned `BLOCKED: work order missing steps`.
- A scoped scout order returned 10 `path:line` citations, **10/10 verified exact** against the files.

### Haiku compaction check (D10, 2026-10-09, Claude Code 2.1.295; superseded by §14)
Five 1,600-line files were read in 800-line chunks, about 25K tokens per read. Each arm also ran without the desktop app's inherited `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.

| Run | Setting | Compactions at preTokens | Largest Haiku request |
|---|---|---|---|
| scout subagent | none | 95.1K, 97.0K, 96.6K | 83.4K |
| scout subagent | `autoCompactWindow` 60000 | 95.3K, 97.4K, 97.1K | 83.8K |
| main session, Haiku | none | 100.8K, 99.1K, 99.1K | 87.3K |
| main session, Haiku | `autoCompactWindow` 60000 | 100.8K, 99.5K, 99.5K | 87.3K |

`modelSettings.<model>.autoCompactWindow` changed nothing: 60K and the default compact at the same point. The default already keeps every Haiku request under 100K, so `/core:setup` no longer writes this setting.

Side effect: after compaction, scout lost its place and re-read files until it hit `maxTurns`. This is one more reason to keep work orders small (§4.7). One order should stay well under ~80K.

### Implement re-run after the test-filter fix (2026-10-09)
Same tasks, a fresh clone, both arms run again the same day. The new arm uses the `/core:setup` settings without the compaction setting.

| Repo | Old $ | New $ | Δ | Old s | New s | Turns old / new | Result |
|---|---|---|---|---|---|---|---|
| core | 0.140 | **0.125** | **−11%** (was +10%) | 58 | 127 | 8 / 10 (new was 12) | both green; new TDD (red first), +7 cases; old +10 |
| legacy | 0.332 | **0.314** | **−5%** (was +12%) | 114 | 196 | 14 / 17 (new was 20) | both green; new TDD, 25 cases; old 33 |

After the fix the main session no longer burns turns on a false `NO TESTS MATCHED`. With these implement numbers the 8-task total is **old $1.60 vs new $1.10 (−31%)**. The old arm itself varied between runs ($0.289 → $0.332 on legacy), so read single-run deltas of ±10% as noise. New stays slower in wall time because of the TDD loop.

## 13. Auto-delegation without naming the agent (2026-10-18)

Problem: outside a slash command, Claude never used `scout`/`runner`. The user had to write "use core:scout". Causes: every skill is `disable-model-invocation`, so nothing in a plain session said when the executors beat inline work; the agent descriptions described the input contract ("Send a WORK ORDER", "Not for open-ended exploration") rather than when to use them; and both executors blocked any order without a return format, which is how ad-hoc dispatches are usually written.

Changes:
- `core` ships a `SessionStart` hook (`hooks/delegation.sh`, matchers `startup|clear|compact`) whose stdout is a short delegation policy: scout for lookups over ~3 files or several searches, runner for noisy shell output, reviewer for diffs over ~600 lines, inline for a single grep or a short command. It also says that `core:scout` in a skill means the Agent tool with that `subagent_type`. `CLAUDE_CORE_DELEGATION=0` disables it.
- Agent descriptions start with "Use proactively for ..." (the trigger wording the subagent docs recommend).
- scout and runner fall back to their default line-capped return when an order has none. They still block an order with no concrete scope or no runnable command (`scout-blocks-vague-order` still passes 2/2).

Eval `core/evals/delegates-without-being-named` (Sonnet main, plain request to map Quantity/PlaceAsync usages, 3 runs each, Claude Code 2.1.302):

| Variant | scout dispatched | $/run |
|---|---|---|
| before | 0/3 | 0.042 |
| new descriptions only (hook stubbed out) | 0/3 | 0.045 |
| descriptions + SessionStart policy | **3/3** | 0.066 |

The hook is what moves it. On this 5-file fixture delegating costs more than doing it inline, because the spawn and the verification reads cost more than three greps. The saving shows on real repos, where inline search pulls whole files into the main context and every later turn re-reads them. Fixed overhead measured with `claude -p "Reply with OK."`: +418 input tokens per request with the hook (36,046 → 36,464), plus ~50 for the longer descriptions.

## 14. Haiku-only compaction under 100K (2026-10-18, Claude Code 2.1.302)

Haiku 5.5 bills $0.10/$0.50 per MTok for prompts up to 100K tokens and $0.50/$2.50 above (5x). It runs with a 1M window, and the current docs say Haiku sessions auto-compact at about 967K by default. So §12's conclusion ("the default already compacts Haiku below 100K") no longer holds. Two likely reasons it looked different then: §12's test window of 60000 is below the setting's 100000 minimum, so it was ignored; and the default compaction point has since moved.

Test: five 1,600-line files read in 400-line chunks (~19K tokens per read, 20 reads). Every run used a clean environment (`env -i`, so nothing inherited such as `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`), with settings passed through `--settings`. Prompt size = input + cache read + cache write per request, taken from the transcript.

| Arm | Setting | Requests > 100K | Largest prompt | Compactions at | Cost |
|---|---|---|---|---|---|
| Haiku main | default | 16/21 | 393K | none | $0.517 |
| Haiku main | `modelSettings.claude-haiku-5-5.autoCompactWindow: 100000` | 0/14 | 71K | 80.4K, 79.8K, 80.2K, 80.1K | $0.072 |
| scout subagent (Haiku) | default | 7/12 | 195K | none | — |
| scout subagent (Haiku) | `modelSettings.claude-haiku-5-5…: 100000` | 0/12 | 64K | 71.4K, 73.2K, 73.6K | $0.044 |
| scout subagent (Haiku) | `modelSettings.haiku…: 100000` (alias key) | 0/11 | 65K | 71.3K, 73.3K, 73.9K | — |
| Sonnet 5.5 main | `modelSettings.haiku…: 100000` | 4/9 | 165K | none (unaffected) | $0.707 |

Conclusions:
- The per-model window applies to Haiku main sessions **and** subagents, and leaves other models alone. The alias key `haiku` works, so `/core:setup` writes `modelSettings.haiku` and it follows future Haiku releases.
- Compaction fires at ~72-80K with a 100K window, which leaves ~20K of headroom for the compaction request itself. One tool result larger than that could still push the compaction call past 100K, so keep scout reads to ranges (rule 2) and work orders small. Resolved in §15.
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW` overrides per-model windows for every model, and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` also applies to every model, so neither works as a Haiku-only setting.
- As in §12, a compacted Haiku can lose its place in a long mechanical task (the main arm stopped after 13 of 20 reads). The answer is still small work orders, not a larger window. Resolved in §15.
- Plugins can't set `modelSettings`: plugin `settings.json` takes only `agent` and `subagentStatusLine`. So the setting goes in user settings via `/core:setup`, and a SessionStart check (`hooks/haiku_window.py`) prints a one-line note only when it's missing, above 100K, or overridden by `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.

## 15. Haiku context guard: no compaction overflow, no lost place (2026-10-18)

§14 left two gaps. (1) Compaction fires at ~80K, and the compaction request carries the whole context plus the latest tool result, so a result over ~20K could push that request past 100K. (2) A compacted Haiku can lose its place: the §14 main arm stopped after 13 of 20 reads.

`hooks/haiku_guard.py` (PreToolUse on every tool, and SessionStart `compact`) acts only when the transcript's latest request ran on Haiku:
- **Projection.** The last recorded request size, plus the tool results written since, plus this call's estimate. A Read is estimated from the requested lines at 1.9 chars/token (measured on Haiku 5.5: shell 1.9, Markdown 2.4, Python 2.6, with Read's line prefixes), capped at 25K because Read refuses larger results; Bash is 10K, Grep 4K. Subagent transcripts are at `<session>/subagents/agent-<agent_id>.jsonl`; PreToolUse input carries `agent_id` and `agent_type` inside a subagent (verified).
- **Transcripts lag the hook.** In every live call the message holding the current tool_use wasn't on disk yet, main and subagent alike. A first version added that message's calls as if pending and denied a normal read after compaction (111K projected; the real figure was ~54K). Fixed: when the current call isn't in the transcript, count the tool results already written instead. When a compact boundary follows the last recorded request, allow, because the context was just reset.
- **Executors (any Haiku subagent): stop at 60K** (`CLAUDE_CORE_HAIKU_BUDGET`), below the ~72K where subagents compact. The deny reason tells the agent to make no more calls and return its findings plus `not done: <steps>`. scout, runner, publisher and Explore have a matching rule, and the delegation policy tells the main session to send a fresh order for just those steps. An executor never compacts, so it can't lose its place, and no executor request reaches 100K.
- **Main Haiku session: a Read past 95K is denied** with a line count that fits, so compaction runs on a request under 100K.
- **Resume point.** After a compaction in a Haiku session, SessionStart re-injects the user's last request verbatim (up to 1,500 chars) and the tool calls made since (up to 40, one line each).

Live runs (same 20-read fixture as §14, `modelSettings.haiku.autoCompactWindow: 100000`, `CLAUDE_CORE_HAIKU_GUARD_LOG` for the projections):

| Arm | Result | Requests > 100K | Largest prompt | Compactions | Cost |
|---|---|---|---|---|---|
| Haiku main, window only (§14) | stopped after 13/20 reads | 0 | 71K | 4 | $0.072 |
| Haiku main, window + guard + resume point | **all 20/20 reads**, all 5 MARKERs | 0 | 72K | 6 at ~80.8K | $0.110 |
| scout, window + guard | denied at 64K projected; returned `not done: data1.txt offset 801 onward, data2-5` | 0 | 43K | **none** | $0.007 |

The projections before each main-session compaction were ~92K, about what the compaction request really carries with ~20K reads. So the gap was real, and the 95K cap closes it with ~5K left for the summary prompt. Core evals afterwards: delegates-without-being-named 1/1, scout-blocks-vague-order 1/1, scout-runs-full-order 2/3 (one run's LLM judge failed the answer; the 2 re-runs passed).

## 16. Remaining gaps closed (2026-10-18)

| Gap | Evidence | Fix | Verified |
|---|---|---|---|
| An executor that hits `maxTurns` returns nothing | §14 arm C: "hit its 12-turn limit… no MARKER lines" | The guard counts the subagent's requests against `maxTurns` from its agent file. On the next-to-last turn it adds a factual note ("turn 11 of 12, the next reply is the last"); the agent's own rule says what to do. | eval `scout-answers-at-turn-limit` 4/4 + 3/3 + 2/2 (11 of 15 markers plus `not done: f12…f15`, $0.004/run) |
| Haiku ignored that note as a prompt injection when the note held the instruction ("it came from inside the tool output… I'm ignoring it") | first version, 1/2 then 2/3 | The hook states only the fact. The instruction lives in the system prompt of scout, runner, publisher and Explore, which the agent trusts. The budget deny already worked this way. | as above |
| Without `/core:setup`, the main-session read limit fired forever (Haiku compacts at ~967K, so every Read past 95K was denied) | code reading | The main-session rule runs only when `haiku_window.check()` finds the 100K window set | `haiku_guard_test` "window not set" |
| An image read counted as its base64 size (~100K+), so the next call was falsely denied | code reading | Image blocks count 1,600 tokens | `haiku_guard_test` "image result" |
| The Bash estimate (10K) was below the real cap | measured: up to ~25K chars inline (one char per token for repeated characters), larger output saved behind a 2.3K preview | 16K | — |
| The "smaller range" line count came from a capped estimate | code reading | Uses the uncapped estimate | — |
| ~110 ms per tool call in every session (4 MB transcript parse) | timed on a 2.4 MB transcript | A 256 KB tail first; non-Haiku sessions exit after the model check | ~45 ms per call |
| User-level Explore/publisher from an older `/core:setup` lacked the new rules, unnoticed | code reading | The SessionStart check flags our templates (by their text) that lack the context-budget rule | `haiku_window_test` 17/17 |
| No official eval covered the guard | — | `scout-stops-at-context-budget`, `scout-answers-at-turn-limit` | 2/2 + 3/3, 9/9 |
| `scout-runs-full-order` was flaky | A/B on 4 runs each: original scout prompt 2/4, current 4/4; the failing answers were correct (all three files with line numbers), and the Haiku LLM judge split FAIL FAIL PASS | Exact-line regex graders replace the LLM judge (`OrdersController.cs:9-11`, `OrderService.cs:8`, `ShopDbContext.cs:13`) | 4/4 |

Still open, by design or low value (all four resolved in §17):
- A main Haiku session's MCP results (up to 25K tokens) aren't limited, so near compaction one could push the compaction request just past 100K. MCP output can't be asked to shrink, and this marketplace routes MCP through `publisher`, a subagent the budget covers.
- The Haiku-window check reads user, project and local settings files only. A window passed with `--settings` or in managed settings gets a false "not set" note, and the main-session read rule stays off (fail-open).
- The dotnet, postgresql and sqlserver evals still use LLM judges for some graders (e.g. `cites-code`, `triage-correct`), with the same flakiness risk.
- `dotnet:guide` has `paths:` and `disable-model-invocation: true` together. The `paths:` gate is dead: the skill loads only through `/dotnet:guide`.

## 17. The four open items, resolved (2026-10-18)

| Item | Fix | Verified |
|---|---|---|
| MCP results in a main Haiku session weren't limited | The main-session rule covers every tool. MCP is estimated at `MAX_MCP_OUTPUT_TOKENS` (default 25K). A Read gets a line range, Bash `\| head -n 100` (a command already ending in `\| head/tail -n N` is estimated from N, so the retry passes), and MCP or other tools a subagent. Agent is never denied. If the last request is already past ~85K, compaction isn't running, so the guard allows instead of denying every call. | `haiku_guard_test` 29/29 |
| The window check saw only the three settings files | It also reads the session's `--settings` (inline JSON, a file path, or `--settings=`), from the nearest `claude` process's argv: exact via `/proc` on Linux/WSL, best-effort via `ps` on macOS. An outer claude's flags are ignored. It also reads `managed-settings.json` plus `managed-settings.d/*.json` in the system directory and the cached server-managed `~/.claude/remote-settings.json`, in precedence order. MDM profiles and the Windows registry are still not read. | `haiku_window_test` 25/25; live: no note with `--settings` as a file or inline, note without |
| LLM judges in the dotnet/postgresql evals | `pr-comments` triage: 7 row-level regexes on the gate table (path:line + class cell). pg gate: 3 regexes (unused index kept and never in a `DROP INDEX`, orphans never set to NULL on a NOT NULL column). analyze: `tool_used: Write` input matches (the old `focus: {file: glob}` grader **threw on every run**, because file targets don't take globs). brainstorm: matrix, recommendation and `options=` regexes, plus one LLM grader kept for "options differ in kind", run with `--judge-model sonnet`. Each new grader was checked against a real passing output, and mutation-tested to FAIL when its fact was broken (10/10). | analyze 2/2, brainstorm 2/2, pr-comments 2/2, pg gate 4/4 |
| `dotnet:guide` `paths:` | Measured: a `paths:` skill adds 0 tokens at session start, but on 2.1.302 it never entered the skill listing, even after `.cs` files were read (comma-string and YAML-list forms, 2 Sonnet + 2 Haiku runs). Removed as dead config. `implement` and `review` already read the guide's references directly. | — |

Found while doing this: the fake `psql` had no answers for the verification queries `schema-fix.md` prescribes (columns, sizes, index definitions, time zone, date ranges). Sonnet then inspected the stub and in one run refused to reach the gate, which made the pg gate case flaky. It now answers each statement in a `-c` in `psql -A -F'|'` shape, with the label column the skill's queries use, and returns no rows (not a "no canned answer" message) for anything else. Pg gate 4/4 with no run mentioning a stub; `schema-fix-writes-safe-scripts` 2/2; `fakebin_test` 29/29. A `controller` regex in `scout-runs-full-order` was too narrow (a correct answer cited `OrdersController.cs:8-10`); it now accepts lines 8-12 or a range ending there, 4/4.

## 18. Real-repo test: eShopOnWeb with planted bugs (2026-10-18)

Setup (`evals/realrepo/`): eShopOnWeb at `4da8212` (.NET 8, 10 projects, 254 `.cs` files) with four bugs on `feature/checkout-tweaks`: B1 `AddQuantity`→`SetQuantity`, B2 removed null guard, B3 SQL injection via `SqlQueryRaw` + interpolation, B4 `.Result` on async. Sonnet 5.5 main, the `/core:setup` settings, core + dotnet plugins, a clean environment, a fresh worktree per run. **The sandbox's network policy blocks `api.nuget.org`**, so nothing restored: build and test paths were exercised only up to the restore failure.

| Run | Result | Cost (Haiku share) |
|---|---|---|
| `/dotnet:review main` | **4/4 planted bugs**, ranked, correct fixes; read `RESTORE FAILED` as "network, not code" | $0.080 ($0.0008) |
| `/dotnet:debug <NRE trace>` | root cause B2 + the right commit + the fix + a regression test, plus B3 and B4 flagged | $0.150 → $0.101 after the fixes below |
| plain bug report (B1), no slash command | right cause, line and commit from 2 inline `git` commands (Claude Code's recent-commits context gave the commit away) | $0.046 |
| `/dotnet:build test` | forked into the Haiku runner, `RESTORE FAILED` | $0.001 |
| `/dotnet:implement --no-tdd` fix B3 | correct `SqlQuery` fix; step gate blocked and honestly reported, nothing claimed green | $0.061 |
| `/dotnet:audit` | `AUDIT INCOMPLETE` reported as not checked; .NET 8 end of support (2026-11-10) flagged; secret locations only | $0.051 |
| `/dotnet:plan` 10-unit cap | grounded plan; found B1 as a prerequisite | $0.115 ($0.005) |
| Haiku main session, whole-repo overview | 4 parallel scouts, no compaction, max prompt 40K; 38/43 citations exact (the rest were parser artifacts or ambiguous) | $0.040 |
| repo-wide "every place quantity is read or changed" | ~20 correct locations; scout dispatched 4/4 after G8 (0/1 before), cost $0.082–0.120 vs $0.092 inline | — |

Gaps found while running, and fixed:
| # | Gap | Fix |
|---|---|---|
| G1 | A NuGet restore failure was reported as `BUILD FAILED`, inviting code "fixes" | Restore is its own step: `RESTORE FAILED (package source unreachable: <url>) - a network or feed problem, not a code error` |
| G2 | An unreachable feed took **4m44s** to fail (NuGet retries) | One retry (`NUGET_ENHANCED_MAX_NETWORK_TRY_COUNT=2` unless set): 1m06s |
| G3 | The Steps check counted only `Read` calls for `verified=`, so verification through `sed`/`grep`/`git show` was falsely blocked, and **the final message became the hook correction instead of the RCA** | Shell reads (sed/cat/head/tail/grep/git show…) and Grep content count |
| G4 | **Scout citations off by one**: `Read` with `offset: 0` numbers lines from 0 | PreToolUse rewrites `offset: 0` to `1` via `updatedInput` (no permission decision), for every model |
| G5 | The Steps check missed false claims when the final message wasn't in the transcript yet (R1: claimed `verified=3` with 0 reads, not caught) | Reads the Steps line from the Stop hook's `last_assistant_message` |
| G6 | The runner re-ran `dotnet.sh` after `RESTORE FAILED` (network looked "transient"): a minute wasted | A script that printed a `STATUS:` line has finished; never re-run it |
| G7 | **`dotnet.sh audit` reported `vulnerable: 0` when it couldn't restore**: a false clean security result | Collects first; `STATUS: AUDIT INCOMPLETE (not checked: …) - do not report these as clean`, per-check `NOT CHECKED (reason)`; the audit skill reports them as not checked |
| G8 | A repo-wide lookup stayed inline because the policy said "inline for a single Grep" | Scout for results spanning more than ~3 files "even when one repo-wide Grep would find them"; inline only for 1-3 known files |
| G10 | After delegating, the main session sometimes re-ran the scout's whole search (R6b: $0.120) | Policy: open the 1-2 decisive refs, don't re-run the executor's search ($0.089 ×2 after) |

Observations, not changed:
- `/dotnet:implement` ran its step gate with `dotnet.sh` inline rather than through `core:runner`, and wrote `runner-checks=1`. The script output is pre-condensed, so the cost is the same (§11), but the key name over-claims.
- For one lookup on a repo this size, delegation is cost-neutral ($0.089 vs $0.092). It keeps the main context smaller (26K vs 29K), which pays off over a longer session.
- My planted commit messages were too telling: Claude Code's recent-commit context let the plain-prompt run find B1 from the history alone. Plant with neutral messages to test code reasoning.
- Not exercised: anything after a successful restore (TDD red/green, coverage, test-failure condensing on a real suite), `/dotnet:pr` and `/dotnet:pr-comments` on a real GitHub PR, `/dotnet:ci`, `postgresql` and `sqlserver` against a live database.

## 19. Regression check against main (2026-10-18)

The question: does anything that works on `main` stop working with this branch?

- **main's own tests on this branch's plugins** (main's `evals/` with this branch's `plugins/`): `guard_test` 57/57, `steps_check_test` 15/15 (through the fallback for older Claude Code without `last_assistant_message`), `frontmatter_test` 107/107.
- **A/B on the shipped cases this branch hadn't run before** (same case, `main` checkout vs this branch, fresh runs):
  - `flow-gates-after-analyze`: main **1/3**, branch **3/3**. Main's failures stopped to ask questions before showing the Approve / Revise / Pause gate.
  - `sqlserver schema-fix-writes-safe-scripts`: main 2/3, branch 2/2 completed (a third run hit the account's usage limit). The `no-nocheck-fk` failure happens on main too. It flags a `WITH NOCHECK` in the down script, which restores the original untrusted FK, so the grader is arguably too broad. `plugins/sqlserver` is unchanged by this branch.
- **Permissions:** the `offset: 0` → `1` rewrite returns `updatedInput` without a permission decision. A read outside the project still needs permission (denied in `-p`, the same with and without the plugin); a read inside is numbered from 1.

Found and fixed in the process:
| Risk | Fix |
|---|---|
| The branch exported `NUGET_ENHANCED_MAX_NETWORK_TRY_COUNT=2` for the whole script, so a flaky network that `main` recovers from by retrying could fail, and the runner no longer re-runs a `STATUS` script | The first restore runs without retries. Only a definitive answer (401/403/407, DNS, refused) stops there; anything possibly transient re-runs with NuGet's normal retries, exactly as `main`. No script-wide override; a user's own setting wins. Blocked feed: 16s (main 4m44s) |
| Hook launchers `exec`'d Python, so a crash exiting 2 passed through, and **exit 2 from a hook blocks the tool call or stop it guards**. A bare relative path made the launcher look for `<script>.sh/<file>.py` and exit 2. `main`'s `steps-check.sh` has the same flaw | All three launchers resolve their directory for relative paths and always exit 0 |
| With `last_assistant_message` present but no Steps line, the check fell back to a lagging transcript that could still hold an older Steps line | The field, when present, is the final message; the transcript is the fallback only for older Claude Code |

New free tests: `evals/hooks_failopen_test.sh` (39: no Python, malformed input, missing transcript, relative path, a Python exit 2), and `dotnet_sh_test.sh` grew to 17 (definitive vs transient restore failures).

Hook cost per tool call: about 45 ms (Python start-up) for `haiku-guard` on every tool, plus `guard.sh` on Bash as before. Not tested here: Windows Git Bash and macOS (`ps` instead of `/proc` for `--settings`).
