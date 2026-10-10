#!/usr/bin/env bash
# Small Dapper + SqlClient repo (no EF, no SQL project) and the canned audit rows the fake sqlcmd
# (evals/fakebin/sqlcmd) returns. The rows match a database with planted problems.
set -e
mkdir -p src/Orders
cat > src/Orders/Orders.csproj <<'X'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Data.SqlClient" Version="5.2.2" />
    <PackageReference Include="Dapper" Version="2.1.35" />
  </ItemGroup>
</Project>
X
cat > src/Orders/OrderRepository.cs <<'X'
using Dapper;
using Microsoft.Data.SqlClient;
namespace Orders;
public class OrderRepository(string connectionString)
{
    public async Task<int> AddLineAsync(int orderId, int productId, int quantity, double unitPrice)
    {
        await using var conn = new SqlConnection(connectionString);
        return await conn.ExecuteScalarAsync<int>(
            "INSERT dbo.OrderLines(OrderId, ProductId, Quantity, UnitPrice) OUTPUT inserted.Id VALUES (@orderId, @productId, @quantity, @unitPrice)",
            new { orderId, productId, quantity, unitPrice });
    }
}
X
printf '# Orders service\nSQL Server database Shop on server sql01, Windows auth. Schema changes are applied by hand by the DBA.\n' > README.md
g() { git -c core.autocrlf=false -c user.name=eval -c user.email=eval@example.com "$@"; }
g init -q && g add -A && g commit -qm "orders service"
d=.git/eval-fake; mkdir -p "$d"; : > "$d/calls.log"
cat > "$d/audit.txt" <<'X'
high|no_primary_key|dbo.AuditLog|no primary key
high|heap|dbo.AuditLog|no clustered index
high|fk_without_index|dbo.Orders.CustomerId|FK_Orders_Customers has no index starting with (CustomerId)
high|fk_without_index|dbo.OrderLines.OrderId|FK_OrderLines_Orders has no index starting with (OrderId)
high|float_money|dbo.Products.Price|float on a money-like column
high|float_money|dbo.OrderLines.UnitPrice|float on a money-like column
high|identity_near_max|dbo.Tickets.Id|last_value 2000000000 of max 2147483647 (93%)
med|untrusted_fk|dbo.OrderLines.FK_OrderLines_Orders|created WITH NOCHECK, not trusted
med|missing_fk_candidate|dbo.OrderLines.ProductId|int NOT NULL, looks like a reference to dbo.Products(Id) but has no FK
med|duplicate_index|dbo.Customers.IX_Customers_Email2|same key columns as IX_Customers_Email
med|deprecated_type|dbo.Customers.Notes|ntext
low|nullable_fk|dbo.OrderLines.OrderId|FK column allows NULL
X
