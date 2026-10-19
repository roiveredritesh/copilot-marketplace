---
name: setup
description: One-time cost setup for this marketplace - Haiku defaults, a Haiku-only auto-compact window under 100K, Explore on Haiku, and the isolated publisher agent for Confluence/Jira/GitHub.
disable-model-invocation: true
---
# Marketplace cost setup

Apply each change below only after showing the user exactly what will change and getting a yes (use AskUserQuestion, one question per change, "skip" allowed). Before editing any existing file, copy it to `<file>.bak-<yyyymmdd>`. Never print tokens, header values, or other secrets: refer to them as `<redacted>`. Skip a step that is already in place and say so. Finish with a summary table: change | status (applied / already set / skipped).

## 1. User settings (`~/.claude/settings.json`)
Merge both, keeping every other key (and every other model's entry under `modelSettings`):
```json
{
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" },
  "modelSettings": { "haiku": { "autoCompactWindow": 100000 } }
}
```
- `CLAUDE_CODE_SUBAGENT_MODEL`: subagents without their own model pin run on Haiku.
- `modelSettings.haiku.autoCompactWindow`: Haiku 5.5 bills prompts over 100K tokens at 5x, and Claude Code otherwise lets Haiku run to ~967K before compacting. With this, Haiku main sessions and subagents compact at ~72-80K, and other models keep their own windows (RESEARCH.md §14). If an existing `claude-haiku-*` entry under `modelSettings` has an `autoCompactWindow` above 100000, set it to 100000 too.
- If `CLAUDE_CODE_AUTO_COMPACT_WINDOW` is set (`echo $CLAUDE_CODE_AUTO_COMPACT_WINDOW`, or in the `env` block of any settings file), tell the user: it overrides the per-model window for every model, so remove it unless they want every model compacting at that size.

## 2. Explore on Haiku
Copy `${CLAUDE_PLUGIN_ROOT}/templates/Explore.md` to `~/.claude/agents/Explore.md`. If that file exists and differs, show the diff and ask before replacing it.

## 3. Isolated publisher (Confluence / Jira / GitHub)
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
   Replace the `# {{GITHUB_SERVER}}` comment line with that entry. If GitHub isn't configured, leave the comment as is.
4. Write `~/.claude/agents/publisher.md` from `${CLAUDE_PLUGIN_ROOT}/templates/publisher.md`, filling `{{ATLASSIAN_URL}}` and the GitHub line.
5. Ask whether to remove the Atlassian and GitHub servers from the main session (`claude mcp remove <name> -s <scope>`). This is what keeps their tools out of every main-session request. Before removing, save the output of `claude mcp get <name>` to `~/.claude/mcp-backup-<yyyymmdd>.txt` with secrets redacted, and tell the user the re-add command (`claude mcp add ...`) in case the publisher cannot authenticate on its own.

## 4. Finish
Tell the user to restart Claude Code so the settings and agents load. Then suggest a smoke test: `/docs-kit:jira <KEY>` if docs-kit is enabled.
