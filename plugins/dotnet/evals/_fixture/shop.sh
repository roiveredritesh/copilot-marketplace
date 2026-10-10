#!/usr/bin/env bash
# Tiny ASP.NET Core repo for eval cases. Runs in the empty eval workspace.
set -e
mkdir -p src/Shop.Api/Controllers src/Shop.Api/Services src/Shop.Api/Data tests/Shop.Tests
cat > src/Shop.Api/Shop.Api.csproj <<'X'
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><Nullable>enable</Nullable></PropertyGroup>
  <ItemGroup><PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.8" /></ItemGroup>
</Project>
X
cat > src/Shop.Api/Data/ShopDbContext.cs <<'X'
using Microsoft.EntityFrameworkCore;
namespace Shop.Api.Data;
public class Order
{
    public int Id { get; set; }
    public string CustomerId { get; set; } = "";
    public int Quantity { get; set; }
    public decimal Total { get; set; }
    public DateTime PlacedAt { get; set; }
}
public class ShopDbContext(DbContextOptions<ShopDbContext> options) : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();
}
X
cat > src/Shop.Api/Services/OrderService.cs <<'X'
using Shop.Api.Data;
namespace Shop.Api.Services;
public interface IOrderService { Task<Order> PlaceAsync(string customerId, int quantity, decimal unitPrice); }
public class OrderService(ShopDbContext db) : IOrderService
{
    public async Task<Order> PlaceAsync(string customerId, int quantity, decimal unitPrice)
    {
        if (quantity <= 0) throw new ArgumentOutOfRangeException(nameof(quantity), "Quantity must be positive.");
        var order = new Order { CustomerId = customerId, Quantity = quantity, Total = quantity * unitPrice, PlacedAt = DateTime.UtcNow };
        db.Orders.Add(order);
        await db.SaveChangesAsync();
        return order;
    }
}
X
cat > src/Shop.Api/Controllers/OrdersController.cs <<'X'
using Microsoft.AspNetCore.Mvc;
using Shop.Api.Services;
namespace Shop.Api.Controllers;
[ApiController, Route("api/orders")]
public class OrdersController(IOrderService orders) : ControllerBase
{
    public record PlaceOrder(string CustomerId, int Quantity, decimal UnitPrice);
    [HttpPost]
    public async Task<IActionResult> Place(PlaceOrder req)
    {
        var order = await orders.PlaceAsync(req.CustomerId, req.Quantity, req.UnitPrice);
        return Created($"/api/orders/{order.Id}", order);
    }
}
X
cat > tests/Shop.Tests/OrderServiceTests.cs <<'X'
namespace Shop.Tests;
public class OrderServiceTests
{
    [Fact] public async Task Place_rejects_zero_quantity() { /* ... */ await Task.CompletedTask; }
}
X
git init -q && git -c user.name=eval -c user.email=eval@example.com add -A && git -c user.name=eval -c user.email=eval@example.com commit -qm "initial shop"
