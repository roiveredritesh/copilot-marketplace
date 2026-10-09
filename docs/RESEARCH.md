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
| **Haiku 5.5** | scout, runner, publisher (**execution only**, §4.8) | `model: haiku`, `effort: low`, `maxTurns: 6–12`, minimal `tools`, no `Agent` |
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
| **Haiku workers** | **Primary: never reach 100K by design.** One work order per spawn, so every spawn starts fresh. `maxTurns` 6–12. Scripts condense output (errors only, `head -n`). The main session splits big jobs into chunks (per project, per folder, per 20 files). **Safety net (D10):** Claude Code's default compaction, which already keeps Haiku under 100K. The per-model `autoCompactWindow` setting was tested and has no effect (§12). It applies only when Haiku is the model, so the main session's window is unchanged. Subagent compaction uses the same logic as the main conversation. Still, the docs don't explicitly say per-model settings apply inside subagents, so P1 verifies it once by checking `compact_boundary` / `preTokens` in a Haiku subagent transcript |
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
effort: low
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
| D10 | Haiku 100K compaction | ~~`modelSettings` autoCompactWindow~~ dropped: no effect, and the default already compacts Haiku below 100K (§12). Design limits in §4.7 stay |
| D11 | MCP isolation | **full isolation**: user-level `publisher` with inline Atlassian (+ GitHub fallback). The servers are removed from the main config |
| D12 | Atlassian MCP | official Atlassian remote server |
| D13 | SQL Server / legacy scope | **SQL Server dropped** (LINQ-to-SQL, MSSQL query/schema tools, Telerik dropped too). `dotnet-legacy` keeps only **WebForms modernization** + **.NET Framework → .NET migration** |
| D14 | GitHub | **`gh` CLI via `runner` first**. GitHub MCP (in `publisher`) only as a fallback |
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
- **Model-invocable (in the listing):** `dotnet:guide` (only on matching paths), `postgresql:pg`, `docs-kit:jira`.
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

### Haiku compaction check (D10, 2026-10-09, Claude Code 2.1.295)
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
