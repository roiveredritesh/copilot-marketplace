---
type: llm
---

PASS if the reply cites OrdersController.cs (the Place action), OrderService.cs (PlaceAsync and the quantity <= 0 check), and ShopDbContext.cs (the Orders DbSet), each with a line number, and invents nothing else.
FAIL if any of the three is missing or a cited file or rule doesn't exist in a tiny ASP.NET Core Shop API.
