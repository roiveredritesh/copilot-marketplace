---
name: generate-release-notes
description: Create release notes from git history
delegated_to: release-notes-generator
---

# Command: /generate-release-notes

Create release notes from git commit history with categorized changes, breaking changes, and upgrade instructions.

## Usage

```bash
/generate-release-notes <version> [flags]
```

## Arguments

- `<version>`: Version number for the release
  - Examples: `2.0.0`, `v1.5.3`, `1.0.0-beta`

## Flags

- `--from=<tag|commit>`: Starting git tag or commit (default: last tag)
- `--to=<tag|commit>`: Ending git tag or commit (default: HEAD)
- `--format=<markdown|confluence>`: Output format (default: `markdown`)
- `--publish`: Auto-publish to Confluence (requires Confluence MCP)
- `--async`: Run in background
- `--wait`: Wait for completion (default)
- `--include-authors`: Include contributor list (default: `true`)
- `--group-by=<type|scope|author>`: Group commits by (default: `type`)

## Examples

### Basic Usage
```bash
# Generate release notes for version
/generate-release-notes 2.0.0

# Generate with version prefix
/generate-release-notes v1.5.0
```

### Specifying Git Range
```bash
# From specific tag to HEAD
/generate-release-notes 3.0.0 --from=v2.5.0

# Between two tags
/generate-release-notes 2.1.0 --from=v2.0.0 --to=v2.1.0-rc1

# From specific commit
/generate-release-notes 1.6.0 --from=abc123def
```

### Publishing
```bash
# Generate Confluence release notes
/generate-release-notes 2.0.0 --format=confluence

# Generate and auto-publish
/generate-release-notes 3.0.0 --format=confluence --publish
```

### Grouping Options
```bash
# Group by scope (functional area)
/generate-release-notes 2.0.0 --group-by=scope

# Group by author
/generate-release-notes 2.0.0 --group-by=author
```

## Output

Documentation saved to: `output/documentation/<version>-release-notes-<timestamp>.md`

**Sections**:
- Release Summary
- What's New (highlights)
- Breaking Changes (with migration guides)
- Features
- Improvements
- Bug Fixes
- Performance
- Security
- Deprecations
- Known Issues
- Upgrade Instructions
- Contributors

## Execution Time

- Small release (10-20 commits): 15-20 minutes
- Medium release (20-50 commits): 20-30 minutes
- Large release (50+ commits): 30-45 minutes

## Requirements

- **MCP**: None (Confluence optional for `--publish`)
- **Tools**: Bash, Glob, Grep, Read, Write
- **Git**: Repository must have git history

## Conventional Commits Support

Supports Conventional Commits format for automatic categorization:

```
feat: New feature → Features section
fix: Bug fix → Bug Fixes section
perf: Performance → Performance section
refactor: Code improvement → Improvements section
docs: Documentation → Documentation section
test: Tests → Not included in user-facing notes
chore: Maintenance → Not included in user-facing notes
```

Breaking changes detected via:
```
BREAKING CHANGE: Description
feat!: Breaking feature
```

## Troubleshooting

### No Git History
```
Error: "No git history found"
Solution: Ensure repository has commits and tags
```

### No Changes
```
Info: "No changes detected since last release"
Solution: Release notes will indicate no changes
```

### Poor Commit Messages
```
Warning: "Many commits lack conventional format"
Solution: Release notes generated but may need manual editing
```

## Best Practices

1. **Use Conventional Commits**: Enables automatic categorization
2. **Document Breaking Changes**: Use `BREAKING CHANGE:` in commit footer
3. **Reference Issues**: Include JIRA-123 or #456 in commit messages
4. **Write Clear Commit Messages**: Improve release note quality

## Related Commands

- `/generate-api-docs` - For API change details
- `/generate-architecture-doc` - For architectural changes
- `/review-pr-local` - Review changes before releasing

---

**Delegates To**: release-notes-generator agent
**Command Version**: 2.0.0
**Status**: Production Ready
