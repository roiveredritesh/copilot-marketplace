---
model: sonnet
max_turns: 20
timeout_seconds: 400
allowed_tools: [Read, Glob, Grep, Agent]
---

I'm about to change how order quantity is validated. Map it across the codebase for me: every place that reads or sets an order's Quantity, every caller of PlaceAsync, the validation rules on quantity, and the tests that cover them. Give path:line for each.
