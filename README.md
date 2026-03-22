# ABC Marketplace

This repository is a local plugin marketplace for both GitHub Copilot CLI and Claude Code.

- Copilot CLI marketplace manifest: `marketplace.json`
- Claude Code marketplace manifest: `.claude-plugin/marketplace.json`

Important: a marketplace is only a catalog. Adding the marketplace does not install every plugin automatically. The documented flow for both tools is:

1. Add the marketplace.
2. Browse or list available plugins.
3. Install individual plugins from that marketplace.

## Included Plugins

- `analysis-toolkit`
- `optimization-engine`
- `review-suite`
- `development-suite`
- `architecture-advisor`
- `planning-suite`
- `brainstorming-suite`
- `linq-to-sql-expert`
- `root-cause-analyzer`
- `database-schema-analyzer`
- `confluence-document-creator`
- `telerik-control-expert`

## Prerequisites

1. Clone this repository to a stable local path.
2. Keep the current folder structure unchanged.
3. Use a recent version of GitHub Copilot CLI or Claude Code with plugin marketplace support enabled.

Example path used below:

```text
D:\n8n\abc_marketplace
```

## Install In GitHub Copilot CLI

GitHub’s documented marketplace flow for Copilot CLI is:

1. Add a marketplace.
2. Browse plugins in that marketplace.
3. Install the specific plugin you want.

### 1. Add This Marketplace

From PowerShell:

```powershell
copilot plugin marketplace add D:\n8n\abc_marketplace
```

Or from an interactive Copilot session:

```text
/plugin marketplace add D:\n8n\abc_marketplace
```

### 2. Confirm The Marketplace Was Added

```powershell
copilot plugin marketplace list
```

Or:

```text
/plugin marketplace list
```

The marketplace name defined by this repository is:

```text
ritesh-marketplace
```

### 3. Browse Available Plugins

```powershell
copilot plugin marketplace browse ritesh-marketplace
```

### 4. Install A Plugin

Example:

```powershell
copilot plugin install analysis-toolkit@ritesh-marketplace
```

You can repeat that for any plugin in this repository, for example:

```powershell
copilot plugin install review-suite@ritesh-marketplace
copilot plugin install architecture-advisor@ritesh-marketplace
copilot plugin install brainstorming-suite@ritesh-marketplace
```

### 5. Manage Installed Plugins

List installed plugins:

```powershell
copilot plugin list
```

Update one plugin:

```powershell
copilot plugin update analysis-toolkit
```

Uninstall one plugin:

```powershell
copilot plugin uninstall analysis-toolkit
```

### Install A Plugin Directly From A Local Path

If you do not want to add the marketplace first, Copilot CLI also supports direct local installation from a plugin folder:

```powershell
copilot plugin install .\plugins\analysis-toolkit
```

## Install In Claude Code

Claude Code follows the same model: add the marketplace first, then install plugins individually.

### Important Path Note For This Repository

Claude Code expects plugin paths in `.claude-plugin/marketplace.json` to resolve relative to `.claude-plugin`. This manifest uses sources like:

```text
./plugins/analysis-toolkit
```

Because this repository stores the real plugin folders in the root `plugins/` directory, you should create `.claude-plugin\plugins` junctions that point to those root folders before adding the marketplace locally.

### 1. Prepare The Claude Plugin Paths

Run this once in PowerShell:

```powershell
$repoRoot = 'D:\n8n\abc_marketplace'
$sourceRoot = Join-Path $repoRoot 'plugins'
$claudePlugins = Join-Path $repoRoot '.claude-plugin\plugins'

New-Item -ItemType Directory -Path $claudePlugins -Force | Out-Null

Get-ChildItem -Path $sourceRoot -Directory | ForEach-Object {
    $target = Join-Path $claudePlugins $_.Name
    if (-not (Test-Path $target)) {
        New-Item -ItemType Junction -Path $target -Target $_.FullName | Out-Null
    }
}
```

### 2. Add This Marketplace

From Claude Code:

```text
/plugin marketplace add D:\n8n\abc_marketplace
```

Claude Code also supports adding a direct marketplace file path. For this repository, that is:

```text
D:\n8n\abc_marketplace\.claude-plugin\marketplace.json
```

### 3. Open The Plugin Manager Or List Marketplaces

Use the interactive manager:

```text
/plugin
```

Or list marketplaces directly:

```text
/plugin marketplace list
```

### 4. Install A Plugin

Example:

```text
/plugin install analysis-toolkit@ritesh-marketplace
```

Other examples:

```text
/plugin install review-suite@ritesh-marketplace
/plugin install architecture-advisor@ritesh-marketplace
/plugin install brainstorming-suite@ritesh-marketplace
```

If you install through the `/plugin` UI, Claude Code lets you choose the installation scope:

- User scope
- Project scope
- Local scope

### 5. Reload Plugins

After installing, enabling, or disabling plugins, reload them without restarting:

```text
/reload-plugins
```

### 6. Manage Installed Plugins

Disable a plugin:

```text
/plugin disable analysis-toolkit@ritesh-marketplace
```

Enable it again:

```text
/plugin enable analysis-toolkit@ritesh-marketplace
```

Uninstall it:

```text
/plugin uninstall analysis-toolkit@ritesh-marketplace
```

Update marketplace listings:

```text
/plugin marketplace update ritesh-marketplace
```

Remove the marketplace:

```text
/plugin marketplace remove ritesh-marketplace
```

## Verify Installation

After installing a plugin, test one of its commands.

Examples:

- `analysis-toolkit`: `/analyze-query`
- `review-suite`: `/review-pr`
- `architecture-advisor`: `/analyze-architecture`
- `brainstorming-suite`: `/brainstorm-feature`

## Troubleshooting

### Copilot CLI Marketplace Problems

1. Run `copilot plugin marketplace list` and confirm `ritesh-marketplace` exists.
2. Make sure you added the repository directory, not a random parent folder.
3. Keep `marketplace.json` beside the root `plugins/` directory.

### Claude Code Marketplace Problems

1. Run `/plugin marketplace list` and confirm `ritesh-marketplace` exists.
2. Make sure `.claude-plugin/marketplace.json` is present.
3. Make sure `.claude-plugin\plugins\<plugin-name>` exists for each plugin you want Claude Code to install.
4. Run `/reload-plugins` after install or configuration changes.

### Plugin Does Not Appear

1. Confirm the plugin name exactly matches the marketplace entry.
2. Re-run the marketplace add command if the local path changed.
3. Update the marketplace listing and install again.

## Repository Layout

```text
abc_marketplace/
|-- marketplace.json
|-- .claude-plugin/
|   |-- marketplace.json
|   \-- plugins/                # Junctions for Claude Code plugin sources
\-- plugins/
    |-- analysis-toolkit/
    |-- architecture-advisor/
    |-- brainstorming-suite/
    |-- confluence-document-creator/
    |-- database-schema-analyzer/
    |-- development-suite/
    |-- linq-to-sql-expert/
    |-- optimization-engine/
    |-- planning-suite/
    |-- review-suite/
    |-- root-cause-analyzer/
    \-- telerik-control-expert/
```