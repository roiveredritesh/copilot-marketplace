---
name: migrate-telerik
description: Migrate Telerik WebForms controls to Blazor or modern alternatives
delegated_to: telerik-migration-advisor
---

# Command: /migrate-telerik

Migrate Telerik WebForms controls to Blazor, React, or Angular with comprehensive migration plan.

## Usage

```bash
/migrate-telerik <file|directory> [flags]
```

## Arguments

- `<file|directory>`: File or directory containing Telerik controls
  - Examples: `Pages/Users.aspx`, `src/Pages`, `.`

## Flags

- `--target=<blazor|react|angular>`: Target framework (default: `blazor`)
- `--strategy=<full|incremental>`: Migration strategy (default: `incremental`)
- `--async`: Run in background
- `--wait`: Wait for completion (default)

## Examples

### Single Page Migration
```bash
# Migrate page to Blazor
/migrate-telerik Pages/Users.aspx --target=blazor

# Migrate to React
/migrate-telerik Pages/Orders.aspx --target=react

# Migrate to Angular
/migrate-telerik Pages/Dashboard.aspx --target=angular
```

### Directory Migration
```bash
# Incremental Blazor migration (default)
/migrate-telerik src/Pages --target=blazor

# Full rewrite to React
/migrate-telerik src --target=react --strategy=full

# Incremental Angular migration
/migrate-telerik . --target=angular --strategy=incremental
```

### Background Execution
```bash
# Large project - run in background
/migrate-telerik . --target=blazor --async
```

## Output

Migration plan saved to: `output/reviews/<target>-telerik-migration-plan-<timestamp>.md`

**Sections**:
- Migration Summary (scope, effort, timeline)
- Control Inventory
- Control Mapping (Telerik → Modern)
- Migration Strategy (phases)
- Migration Steps (detailed)
- Code Examples (before/after)
- Effort Estimation
- Risk Assessment
- Testing Strategy

## Execution Time

- Single page: 30-40 minutes
- Multiple pages: 40-60 minutes
- Full application: 60-90 minutes

## Migration Targets

### Blazor
**Best for**: .NET teams, gradual migration
**Alternatives**: Telerik Blazor, native Blazor components

### React
**Best for**: JavaScript teams, modern UI
**Alternatives**: KendoReact, AG-Grid, React-Select, free libraries

### Angular
**Best for**: Enterprise apps, TypeScript teams
**Alternatives**: Kendo Angular, Angular Material, AG-Grid

## Migration Strategies

### Incremental (Default)
- Migrate page by page
- Coexist WebForms + modern framework
- Lower risk, gradual transition
- Recommended for production apps

### Full
- Rewrite entire application
- Complete replacement
- Higher risk, faster completion
- Recommended for smaller apps

## Effort Estimation

Agent provides detailed effort breakdown:
- Per control type
- Architecture setup
- API development
- Testing time
- 20% buffer for issues

## Troubleshooting

### No Telerik Controls Found
```
Info: "No Telerik controls found"
Solution: Verify path contains Telerik controls
```

### Unsupported Control
```
Warning: "RadRotator has no direct equivalent"
Solution: Custom implementation or alternative suggested
```

## Related Commands

- `/troubleshoot-telerik` - Fix issues before migration
- `/analyze-telerik-config` - Optimize before migration

---

**Delegates To**: telerik-migration-advisor agent
**Command Version**: 2.0.0
**Status**: Production Ready
