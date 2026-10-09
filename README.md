# PR-comments test fixture
Temporary branch for testing /dotnet:pr-comments. Deleted after the test.

## CartTotal example
```csharp
var lines = new List<(decimal Price, int Quantity)> { (10m, 2), (5m, 1) };
decimal total = PriceCalculator.CartTotal(lines, discountPercent: 10); // 22.50
```
