---
type: llm
focus: { source: file, path: ".reports/analysis-*.md" }
---

PASS if the analysis names the current order flow with file:line references into src/Shop.Api (OrdersController, OrderService, or the Order entity in ShopDbContext) and lists acceptance criteria.
FAIL if it has no file:line references to those files, or invents files that don't exist.
