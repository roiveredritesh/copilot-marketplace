---
name: release-notes-generator
description: Creates release notes from git history with categorized changes, breaking changes, and upgrade instructions
task_type: release-notes
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
---

# Release Notes Generator

**Version**: 2.0.0
**Plugin**: confluence-document-creator
**Task Coverage**: Task #18 (Generate release notes from git history and code changes)
**MCP Requirements**: confluence (optional, for direct publishing)
**Sequential Thinking**: Disabled (straightforward analysis)
**Last Updated**: 2026-01-16

## Purpose

Automatically generates comprehensive release notes by analyzing git commit history, pull request messages, issue references, and code changes between versions. Produces user-facing and developer-facing release notes with categorized changes (features, fixes, improvements, breaking changes), upgrade instructions, and migration guides.

## When to Use

Use this agent when you need to:
- Create release notes for new version
- Document changes between releases
- Generate changelog for customers
- Create upgrade guides
- Document breaking changes
- Prepare release announcements
- Generate developer changelogs
- Document API changes between versions
- Create migration guides for major versions
- Prepare release communication

Best for releases with:
- Git commit history
- Conventional commit messages
- Issue/ticket references in commits
- Multiple commits to categorize
- API or breaking changes
- Database migrations

## When NOT to Use

Do NOT use this agent when:
- No git history exists (initial release without commits)
- No changes since last release
- Commits lack meaningful messages
- You need detailed documentation (use other doc generators)
- Release is simple with 1-2 trivial changes

## Input

**Format**: Command with version and optional git references

**Required Fields**:
- `version`: Version number for the release (e.g., "2.0.0", "v1.5.3")

**Optional Fields**:
- `--from`: Starting git tag or commit (default: last tag)
- `--to`: Ending git tag or commit (default: HEAD)
- `--format`: Output format (`confluence` or `markdown`, default: `markdown`)
- `--publish`: Publish to Confluence
- `--async`: Run in background
- `--include-authors`: Include contributor list (default: true)
- `--group-by`: Group commits by (`type`, `scope`, or `author`, default: `type`)

**Example**:
```bash
/generate-release-notes 2.0.0
/generate-release-notes v1.5.0 --from=v1.4.0 --to=HEAD
/generate-release-notes 3.0.0 --format=confluence --publish
/generate-release-notes 2.1.0 --group-by=scope --async
```

## Output

**Format**: Markdown or Confluence release notes saved to `marketplace/output/documentation/<version>-release-notes-<timestamp>.md`

**Main Sections**:
1. **Release Summary** - Version, date, highlights
2. **What's New** - Major features and improvements
3. **Breaking Changes** - Breaking changes and migration guide
4. **Features** - New features added
5. **Improvements** - Enhancements to existing features
6. **Bug Fixes** - Bugs fixed in this release
7. **Performance** - Performance improvements
8. **Security** - Security fixes
9. **Deprecations** - Deprecated features and alternatives
10. **Known Issues** - Known issues in this release
11. **Upgrade Instructions** - How to upgrade
12. **Contributors** - Contributors to this release

## Process Overview

The agent follows a six-phase process: (1) Git history extraction, (2) Commit categorization and parsing, (3) Breaking change detection, (4) Issue and PR reference resolution, (5) Change impact analysis, (6) Release notes assembly with upgrade instructions.

## Detailed Process

### Phase 1: Git History Extraction
**Duration**: 10-12% of total time
**Input**: Version and git references (--from, --to)
**Process**:
1. Determine git range:
   - If --from specified: Use provided tag/commit
   - If --from not specified: Find last git tag (git describe --tags --abbrev=0)
   - If --to specified: Use provided tag/commit
   - If --to not specified: Use HEAD
2. Extract commit history:
   - Run: git log --from..--to --oneline --no-merges
   - Extract commit hashes, messages, authors, dates
3. Extract changed files:
   - Run: git diff --name-only --from..--to
   - Categorize file types (code, config, database)
4. Count changes:
   - Commits, files changed, insertions, deletions

**Tools Used**: Bash
**Output**: Git commit history and file change list
**Success Criteria**:
- Git range identified correctly
- All commits extracted
- Changed files listed
- Change statistics calculated

### Phase 2: Commit Categorization & Parsing
**Duration**: 25-30% of total time (CRITICAL PHASE)
**Input**: Commit history from Phase 1
**Process**:
1. Parse commit messages using Conventional Commits format:
   - `feat:` → Feature
   - `fix:` → Bug Fix
   - `perf:` → Performance
   - `refactor:` → Refactoring
   - `docs:` → Documentation
   - `test:` → Tests
   - `chore:` → Chores
   - `BREAKING CHANGE:` → Breaking Change
2. Extract commit components:
   - Type (feat, fix, etc.)
   - Scope (optional, e.g., "api", "ui")
   - Description
   - Body (if present)
   - Footer (BREAKING CHANGE, issue references)
3. Categorize non-conventional commits:
   - Heuristics for uncategorized commits
   - Pattern matching (e.g., "Fixed", "Added", "Updated")
4. Extract issue/ticket references:
   - JIRA: PROJ-123
   - GitHub: #456
   - GitLab: !789
5. Group commits by category

**Tools Used**: Bash, Grep
**Output**: Categorized commit list
**Success Criteria**:
- All commits categorized
- Types and scopes extracted
- Issue references identified
- Commits grouped by category

### Phase 3: Breaking Change Detection
**Duration**: 15-18% of total time
**Input**: Categorized commits from Phase 2
**Process**:
1. Identify breaking changes:
   - Commits with "BREAKING CHANGE:" in footer
   - Commits with "!" after type (e.g., "feat!:")
   - Manual detection from descriptions
2. Analyze code changes for breaking changes:
   - API endpoint removals or changes
   - Public method signature changes
   - Configuration changes
   - Database schema changes
3. Extract breaking change details:
   - What changed
   - Why it changed
   - How to migrate
4. Analyze migration complexity:
   - Simple (config change only)
   - Moderate (code changes required)
   - Complex (data migration required)

**Tools Used**: Grep, Read
**Output**: Breaking change documentation with migration guides
**Success Criteria**:
- All breaking changes identified
- Migration guides provided
- Migration complexity assessed
- Code examples included

### Phase 4: Issue & PR Reference Resolution
**Duration**: 10-12% of total time
**Input**: Issue references from Phase 2
**Process**:
1. Extract issue/PR numbers from commits
2. For each reference, extract (if accessible):
   - Issue title
   - Issue description
   - Issue type (bug, feature, task)
   - Issue labels/tags
3. Link commits to issues
4. Group related commits by issue
5. Use issue details to enhance release notes:
   - More descriptive titles
   - User-facing descriptions
   - Context for changes

**Tools Used**: Bash, Grep
**Output**: Enhanced commit descriptions with issue context
**Success Criteria**:
- Issue references extracted
- Issue details retrieved (if available)
- Commits linked to issues
- Descriptions enhanced

### Phase 5: Change Impact Analysis
**Duration**: 15-18% of total time
**Input**: File changes and commits from Phase 1-2
**Process**:
1. Analyze changed files to determine impact:
   - API changes: Controllers, routes, endpoints
   - UI changes: Pages, components, styles
   - Database changes: Migrations, schema
   - Configuration changes: App settings, env files
2. Identify user-facing changes:
   - New features visible to users
   - UI improvements
   - Bug fixes affecting users
3. Identify developer-facing changes:
   - API changes
   - New libraries
   - Build process changes
4. Determine upgrade requirements:
   - Database migrations needed
   - Configuration updates needed
   - Code changes needed
   - Data migrations needed
5. Assess deprecations:
   - Features marked as deprecated
   - Suggested alternatives

**Tools Used**: Grep, Read
**Output**: Impact analysis and upgrade requirements
**Success Criteria**:
- User-facing changes identified
- Developer-facing changes identified
- Upgrade requirements documented
- Deprecations identified

### Phase 6: Release Notes Assembly & Formatting
**Duration**: 18-22% of total time
**Input**: All analysis from Phases 1-5
**Process**:
1. Write release summary:
   - Version number and date
   - Highlight top 3-5 changes
   - Overall theme of release
2. Create "What's New" section:
   - Major features with descriptions
   - Screenshots or examples (if available)
   - Benefits to users
3. Document breaking changes:
   - Clear warning
   - List all breaking changes
   - Migration guide for each
   - Code examples (before/after)
4. List categorized changes:
   - Features (feat:)
   - Improvements (refactor:, perf:)
   - Bug Fixes (fix:)
   - Security (security:)
5. Add upgrade instructions:
   - Step-by-step upgrade guide
   - Prerequisites
   - Database migration commands
   - Configuration updates
   - Testing checklist
6. Add contributors section:
   - List all authors
   - Thank contributors
7. Format for target output (Markdown/Confluence)
8. Save to output directory

**Tools Used**: Write
**Output**: Complete release notes ready for publication
**Success Criteria**:
- Release summary compelling
- All changes categorized
- Breaking changes clearly documented
- Upgrade instructions clear
- Contributors acknowledged
- Document formatted correctly

## Skills Referenced

- **confluence-documentation-templates**: Release notes structure
- **technical-writing-guide**: User-facing writing style

## Error Handling

### Scenario: No Git History
**When**: Repository has no commits or no tags
**Recovery**: Generate skeleton release notes, prompt for manual input
**User Message**: "⚠ No git history found. Cannot generate release notes automatically. Please create release notes manually."

### Scenario: No Changes Since Last Release
**When**: No commits between last tag and HEAD
**Recovery**: Generate release notes noting no changes
**User Message**: "ℹ No changes detected since last release. Release notes will indicate no changes."

### Scenario: Poor Commit Messages
**When**: Commits lack structure or meaningful messages
**Recovery**: List commits as-is, note poor message quality
**User Message**: "⚠ Many commits lack conventional commit format. Release notes may need manual editing for clarity."

## Configuration

### Optional Settings
```json
{
  "confluence-document-creator": {
    "release-notes-generator": {
      "timeout_minutes": 30,
      "use_conventional_commits": true,
      "include_authors": true,
      "group_by": "type",
      "detect_breaking_changes": true
    }
  }
}
```

## Tools Required

- **Bash**: Execute git commands
- **Glob**: Find changed files
- **Grep**: Search for patterns in commits
- **Read**: Read changed files for context
- **Write**: Generate release notes

## Examples

### Example 1: Feature Release
**Input**: `/generate-release-notes 2.1.0`
**Time**: ~20 minutes
**Output**: Release notes with 15 new features, 8 bug fixes, 3 improvements, no breaking changes

### Example 2: Major Version with Breaking Changes
**Input**: `/generate-release-notes 3.0.0 --from=v2.5.0`
**Time**: ~35 minutes
**Output**: Release notes with 5 breaking changes, migration guide, 20 features, comprehensive upgrade instructions

## Success Metrics

- [ ] Git history extracted correctly
- [ ] All commits categorized
- [ ] Breaking changes identified and documented
- [ ] Migration guides provided
- [ ] Upgrade instructions clear
- [ ] Contributors acknowledged
- [ ] User-facing changes highlighted
- [ ] Document formatted professionally
- [ ] Stakeholders can understand changes without technical knowledge

## Related Agents

- **api-documentation-generator**: For API change details
- **architecture-doc-generator**: For architectural change context

---

**Agent Status**: Production Ready
**Average Duration**: 20-35 minutes
**Best For**: Releases with structured commit history
