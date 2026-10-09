---
name: build
description: Build or test any .NET solution (SDK-style .NET or legacy .NET Framework) and get back only compiler errors or failing tests. Use after code changes or when asked whether it builds or tests pass.
argument-hint: "[build|test] [solution-or-project]"
context: fork
agent: core:runner
background: false
disable-model-invocation: true
---
WORK ORDER
goal: build or test the .NET code in the current repository
inputs: arguments = "$ARGUMENTS" (empty means "build")
steps:
  1. bash "${CLAUDE_PLUGIN_ROOT}/scripts/dotnet.sh" <arguments, or "build" if empty>
return: the script output exactly as printed (it is already condensed; it starts with "STATUS:")
on-error: if bash or the script cannot start, return "BLOCKED: <error line>"
