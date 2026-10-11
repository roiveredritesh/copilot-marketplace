---
model: sonnet
max_turns: 6
allowed_tools: [Agent]
---

Dispatch the core:scout agent with exactly this work order, then print its reply verbatim and stop:

WORK ORDER
goal: locate order placement and its validation
scope: src/Shop.Api/**/*.cs | terms: PlaceAsync, Quantity, Orders
steps:
  1. Find where orders are placed (controller action and service method).
  2. Find validation rules on quantity.
  3. Find the DbSet for orders.
return: one line per fact as `<fact> - <path>:<line>`, at most 10 lines
on-error: BLOCKED: <one line>
