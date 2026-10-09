---
name: setup
description: One-time cost setup for this marketplace - Haiku defaults, Explore on Haiku, Haiku compaction at 100K, and the isolated publisher agent for Confluence/Jira/GitHub.
disable-model-invocation: true
---
# Marketplace cost setup

Apply each change below only after showing the user exactly what will change and getting a yes (use AskUserQuestion, one question per change, "skip" allowed). Before editing any existing file, copy it to `<file>.bak-<yyyymmdd>`. Never print tokens, header values, or other secrets: refer to them as `<redacted>`. Skip a step that is already in place and say so. Finish with a summary table: change | status (applied / already set / skipped).

## 1. Check the version
Run `claude --version`. Per-model `autoCompactWindow` needs 2.1.288 or later. If older, tell the user to update and skip step 2b.

## 2. User settings (`~/.claude/settings.json`)
Merge, keeping every other key:
```json
{
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" },
  "modelSettings": { "claude-haiku-5-5": { "autoCompactWindow": 100000 } }
}
```
a. `env.CLAUDE_CODE_SUBAGENT_MODEL = "haiku"`: subagents without their own model pin run on Haiku.
b. `modelSettings.claude-haiku-5-5.autoCompactWindow = 100000`: Haiku compacts before its prompt crosses 100K tokens, where its per-token price rises 5x. The main session's window is unchanged.

## 3. Explore on Haiku
Copy `${CLAUDE_PLUGIN_ROOT}/templates/Explore.md` to `~/.claude/agents/Explore.md`. If that file exists and differs, show the diff and ask before replacing it.

## 4. Isolated publisher (Confluence / Jira / GitHub)
1. Find the existing server configs: `claude mcp list`, then `claude mcp get <name>` for the Atlassian and GitHub entries. Note each one's scope (user, project, or local).
2. Atlassian URL: use the configured one. If none is configured, propose the official remote server `https://mcp.atlassian.com/v1/mcp` and ask the user to confirm it.
3. GitHub (fallback only; skills use `gh` first): if configured, build a YAML entry with the same type, url, and headers, for example
   ```yaml
     - github:
         type: http
         url: "<url>"
         headers:
           Authorization: "<same value as the existing config>"
   ```
   If it isn't configured, drop the `{{GITHUB_SERVER}}` line.
4. Write `~/.claude/agents/publisher.md` from `${CLAUDE_PLUGIN_ROOT}/templates/publisher.md`, filling `{{ATLASSIAN_URL}}` and `{{GITHUB_SERVER}}`.
5. Ask whether to remove the Atlassian and GitHub servers from the main session (`claude mcp remove <name> -s <scope>`). This is what keeps their tools out of every main-session request. Before removing, save the output of `claude mcp get <name>` to `~/.claude/mcp-backup-<yyyymmdd>.txt` with secrets redacted, and tell the user the re-add command (`claude mcp add ...`) in case the publisher cannot authenticate on its own.

## 5. Finish
Tell the user to restart Claude Code so the settings and agents load. Then suggest a smoke test: `/docs-kit:jira <KEY>` if docs-kit is enabled.
