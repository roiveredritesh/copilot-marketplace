---
model: haiku
max_turns: 6
allowed_tools: [Agent]
---

Dispatch exactly one subagent with the Agent tool, subagent_type "core:scout", with this prompt and nothing else: "WORK ORDER goal: collect markers | scope: f1.txt..f15.txt in the current dir | steps: Read f1.txt, then f2.txt, and so on through f15.txt, one Read per message, no parallel calls, no other tools | return: every MARKER line found, one per line | on-error: BLOCKED". Then print its reply verbatim and stop.
