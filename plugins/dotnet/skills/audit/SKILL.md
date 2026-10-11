---
name: audit
description: Dependency and security audit for a .NET repo - vulnerable, deprecated, and outdated NuGet packages, possible committed secrets, and target-framework support status - run by a Haiku runner, then prioritized.
argument-hint: "[solution-or-project]"
disable-model-invocation: true
---
# Audit dependencies and security

## 1. Run: `core:runner` work order
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" audit $ARGUMENTS` → return the output as printed.
The script prints secret *locations* only (`path:line`), never values. Never open those lines in chat. Tell the user where to look.

## 2. Prioritize (main session)
| Finding | Priority | Action |
|---|---|---|
| vulnerable (High/Critical), direct dependency | now | upgrade to the first patched version; check release notes for breaking changes |
| vulnerable, transitive | now/next | upgrade the direct parent, or pin the patched version with a direct `PackageReference` (or Central Package Management `VersionOverride`) |
| possible secret in git | now | rotate the credential first, then remove it from the code (move to user-secrets, env vars, or a vault). Removing it from history needs the user's decision |
| deprecated (with an alternative) | next | plan the replacement |
| target framework out of support, or ending within ~6 months | next | plan the upgrade |
| outdated major versions | later | batch them; one major upgrade per PR |
| outdated minor/patch | later | batch them; low risk |
| packages.config / legacy projects | note | not covered by `dotnet list package`; migrate to PackageReference (VS: right-click packages.config → Migrate) |

## 3. Target framework support
Check the current dates at https://dotnet.microsoft.com/platform/support/policy/dotnet-core before advising. Known at the time of writing:
- .NET 6 and 7: out of support.
- .NET 8 (LTS) and .NET 9 (STS, extended to 24 months): support ends 2026-11-10.
- .NET 10 (LTS, November 2025): supported until November 2028. The upgrade target for 8 and 9.
- .NET Framework 4.8/4.8.1: supported with Windows, so not urgent. Modernization is a separate decision (`dotnet-legacy:modernize`).

An upgrade within modern .NET (8/9 → 10) means: bump the TFM and `global.json`, update `Microsoft.*` packages to the matching major version, read the breaking-change list for the target version, then `/dotnet:build test`. Hand it to `/dotnet:plan` if more than a few projects are involved.

## 4. Report (at most 30 lines)
A table: priority | finding | package/location | action. Then the top 3 next steps.
Last line, always: `Steps: runner=<dispatched> tfm=<checked>`. Fill every key; write `skipped (<reason>)` rather than leaving one out.
