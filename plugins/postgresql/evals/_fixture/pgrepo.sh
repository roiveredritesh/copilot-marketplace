#!/usr/bin/env bash
# Small Dapper + Npgsql repo (no EF, no migration tool) and the canned audit rows the fake psql
# (evals/fakebin/psql) returns. The rows match a database with planted problems.
set -e
fx=${BASH_SOURCE[0]//\\//}; fx=${fx%/*}
mkdir -p src/Orders
cat > src/Orders/Orders.csproj <<'X'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Npgsql" Version="8.0.5" />
    <PackageReference Include="Dapper" Version="2.1.35" />
  </ItemGroup>
</Project>
X
cat > src/Orders/OrderRepository.cs <<'X'
using Dapper;
using Npgsql;
namespace Orders;
public class OrderRepository(NpgsqlDataSource db)
{
    public async Task<long> AddLineAsync(long orderId, int productId, int quantity, double unitPrice)
    {
        await using var conn = await db.OpenConnectionAsync();
        return await conn.ExecuteScalarAsync<long>(
            "insert into order_lines(order_id, product_id, quantity, unit_price) values (@orderId, @productId, @quantity, @unitPrice) returning id",
            new { orderId, productId, quantity, unitPrice });
    }
}
X
printf '# Orders service\nPostgreSQL, accessed with Dapper. Schema changes are applied by hand by the DBA.\n' > README.md
g() { git -c core.autocrlf=false -c user.name=eval -c user.email=eval@example.com "$@"; }
g init -q && g add -A && g commit -qm "orders service"
d=.git/eval-fake; mkdir -p "$d"; : > "$d/calls.log"
mkdir -p "$d/bin" && cp "$fx/../../../../evals/fakebin/"* "$d/bin/" && chmod +x "$d/bin/"*  # run with PATH=".git/eval-fake/bin:$PATH"
cat > "$d/audit.txt" <<'X'
high|no_primary_key|public.audit_log|no primary key and no unique NOT NULL key
high|fk_without_index|public.orders.customer_id|orders_customer_id_fkey has no index starting with (customer_id)
high|fk_without_index|public.order_lines.order_id|order_lines_order_id_fkey has no index starting with (order_id)
high|float_money|public.products.price|double precision on a money-like column
high|float_money|public.order_lines.unit_price|double precision on a money-like column
high|sequence_near_max|public.tickets_id_seq|last_value 2000000000 of max 2147483647 (93%)
med|missing_fk_candidate|public.order_lines.product_id|integer NOT NULL, looks like a reference to public.products(id) but has no FK
med|duplicate_index|public.idx_customers_email_dup|same columns as public.idx_customers_email
med|constraint_not_validated|public.tickets.tickets_qty_positive|CHECK (qty > 0) NOT VALID
med|timestamp_without_tz|public.orders.created_at|timestamp without time zone
low|nullable_fk|public.order_lines.order_id|FK column allows NULL
low|json_not_jsonb|public.customers.prefs|json instead of jsonb
low|serial_not_identity|public.customers.id|serial (nextval default) instead of identity
low|unused_index|public.idx_customers_email|0 scans since the stats reset
X
