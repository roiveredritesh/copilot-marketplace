---
name: modernize
description: Assess and plan the modernization of a legacy .NET Framework app - WebForms to Blazor/Razor Pages/MVC, and .NET Framework 4.x to modern .NET - starting from a Haiku-run inventory.
argument-hint: "[assess | webforms | framework | <area to migrate>] [--save]"
disable-model-invocation: true
---
# Modernize a .NET Framework app

## 1. Inventory: one `core:runner` work order
```text
WORK ORDER
goal: inventory legacy technology in this repo
steps:
  1. P=$(git ls-files | grep -E '\.(cs|vb)proj$'); echo "projects $(echo "$P" | grep -c .) legacy-non-sdk $(echo "$P" | tr '\n' '\0' | xargs -0 grep -LE '<Project[^>]*Sdk=' | grep -c .)"; echo "$P" | tr '\n' '\0' | xargs -0 grep -ohE '<TargetFrameworks?>[^<]+|<TargetFrameworkVersion>[^<]+' | sed 's/.*>//' | sort | uniq -c
  2. for p in '\.aspx$' '\.ascx$' '\.master$' '\.asmx$' '\.svc$' '\.ashx$' 'Global\.asax$' '[Ww]eb\.config$' 'packages\.config$' '\.edmx$'; do printf '%s %s\n' "$p" "$(git ls-files | grep -cE "$p")"; done
  3. for s in 'System\.Web\b' 'HttpContext\.Current' 'ViewState\[' 'Session\[' 'System\.Data\.Entity\b' 'System\.ServiceModel' 'System\.Runtime\.Remoting' 'BinaryFormatter' 'AppDomain\.' 'ConfigurationManager\.' 'System\.Drawing' 'Microsoft\.Win32\.Registry' 'Telerik\.Web' 'AjaxControlToolkit'; do printf '%s %s\n' "$s" "$(git grep -lE "$s" -- '*.cs' '*.vb' '*.aspx' '*.ascx' 2>/dev/null | wc -l)"; done
return: the detect output, then "pattern count" lines (non-zero only), at most 40 lines
on-error: BLOCKED: <reason>
```

## 2. Pick the guidance
| Situation | Read |
|---|---|
| `.aspx`/`.ascx`/`.master` present | [webforms.md](webforms.md) |
| Any .NET Framework project (TFM `v4.x`) | [framework-to-net.md](framework-to-net.md) |

## 3. Produce the assessment / plan (chat)
```
Inventory summary (counts that drive effort)
Blockers: tech with no direct equivalent (WCF server, Remoting, AppDomains, WebForms UI, EF6 EDMX) + chosen replacement
Strategy: in-place upgrade | side-by-side strangler (YARP) | rewrite per area, with the reason
Phases: each one deployable on its own, with exit criteria (builds, tests green, parity checks)
Risks: third-party controls (e.g. Telerik), auth/session sharing, perf parity, team skills
First 3 concrete steps
```
For the file-level plan of one phase, hand off to `/dotnet:plan`. With `--save`, also write the report to `~/.claude/reports/<repo-folder-name>/modernize-<yyyymmdd>.md`.
