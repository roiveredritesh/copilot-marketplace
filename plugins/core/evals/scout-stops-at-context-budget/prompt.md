---
model: haiku
max_turns: 6
allowed_tools: [Agent]
---

Dispatch exactly one subagent with the Agent tool, subagent_type "core:scout", with this prompt and nothing else: "WORK ORDER goal: read files fully | scope: data1.txt..data5.txt in the current dir | steps: for each file in order, Read it four times: offset 1, 401, 801, 1201, each with limit 400; one Read per message, no parallel calls, no other tools | return: the five MARKER lines, at most 5 lines | on-error: BLOCKED". Then print its reply verbatim and stop.
