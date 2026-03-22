# ABC Marketplace

This repository is a local plugin marketplace for both GitHub Copilot CLI and Claude Code.

- Copilot CLI marketplace manifest: `marketplace.json`
- Claude Code marketplace manifest: `.claude-plugin/marketplace.json`

GitHub repository for this marketplace:

```text
roiveredritesh/copilot-marketplace
```

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

1. Use a recent version of GitHub Copilot CLI or Claude Code with plugin marketplace support enabled.
2. If you use the GitHub install flow, you do not need to clone this repository locally.
3. If you use the local-path flow, keep the current folder structure unchanged.

Example path used below:

```text
D:\n8n\abc_marketplace
```

## Install In GitHub Copilot CLI

GitHub’s documented marketplace flow for Copilot CLI is:

1. Add a marketplace.
2. Browse plugins in that marketplace.
3. Install the specific plugin you want.

### Install From GitHub Marketplace

This is the preferred setup if you want to install from GitHub without cloning the repository.

#### 1. Add This Marketplace From GitHub

From PowerShell:

```powershell
copilot plugin marketplace add roiveredritesh/copilot-marketplace
```

Or from an interactive Copilot session:

```text
/plugin marketplace add roiveredritesh/copilot-marketplace
```

#### 2. Confirm The Marketplace Was Added

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

#### 3. Browse Available Plugins

```powershell
copilot plugin marketplace browse ritesh-marketplace
```

#### 4. Install A Plugin

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

### Install A Copilot CLI Plugin Directly From GitHub

Copilot CLI also supports installing a plugin directly from a repository path without first adding the marketplace.

Example:

```powershell
copilot plugin install roiveredritesh/copilot-marketplace:plugins/analysis-toolkit
```

Additional examples:

```powershell
copilot plugin install roiveredritesh/copilot-marketplace:plugins/review-suite
copilot plugin install roiveredritesh/copilot-marketplace:plugins/architecture-advisor
```

### Install From A Local Path Instead

Use this only if you specifically want to install from a checked-out local copy.

#### 1. Add This Marketplace

From PowerShell:

```powershell
copilot plugin marketplace add D:\n8n\abc_marketplace
```

Or from an interactive Copilot session:

```text
/plugin marketplace add D:\n8n\abc_marketplace
```

#### 2. Confirm The Marketplace Was Added

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

#### 3. Browse Available Plugins

```powershell
copilot plugin marketplace browse ritesh-marketplace
```

#### 4. Install A Plugin

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

### Manage Installed Copilot CLI Plugins

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

For this repository, the GitHub marketplace flow is the recommended setup. You do not need to clone the repository locally or prepare any local plugin paths when installing from GitHub.

### Install From GitHub Marketplace

This is the preferred setup if you want to install from GitHub without cloning the repository.

#### 1. Add This Marketplace From GitHub

From Claude Code:

```text
/plugin marketplace add roiveredritesh/copilot-marketplace
```

#### 2. Open The Plugin Manager Or List Marketplaces

Use the interactive manager:

```text
/plugin
```

Or list marketplaces directly:

```text
/plugin marketplace list
```

The marketplace name defined by this repository is:

```text
ritesh-marketplace
```

#### 3. Install A Plugin

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

#### 4. Reload Plugins

After installing, enabling, or disabling plugins, reload them without restarting:

```text
/reload-plugins
```

### Manage Installed Claude Code Plugins

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
2. If using GitHub install, make sure you added `roiveredritesh/copilot-marketplace`.
3. If using local install, make sure you added the repository directory, not a random parent folder.
4. Keep `marketplace.json` beside the root `plugins/` directory for local-path installs.

### Claude Code Marketplace Problems

1. Run `/plugin marketplace list` and confirm `ritesh-marketplace` exists.
2. If using GitHub install, make sure you added `roiveredritesh/copilot-marketplace`.
3. Run `/reload-plugins` after install or configuration changes.
4. If installation fails, verify the repository is accessible and that `.claude-plugin/marketplace.json` exists in the GitHub repository.

### Plugin Does Not Appear

1. Confirm the plugin name exactly matches the marketplace entry.
2. Re-run the marketplace add command if the local path changed.
3. Update the marketplace listing and install again.

## Repository Layout

```text
abc_marketplace/
|-- marketplace.json
|-- .claude-plugin/
|   \-- marketplace.json
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