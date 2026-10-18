#!/usr/bin/env bash
# Real-repo test bed: clone eShopOnWeb (.NET 8) into <dir> and plant four bugs on feature/checkout-tweaks.
# usage: bash evals/realrepo/setup.sh <dir>     Ground truth (keep it away from the runs):
#   B1 Basket.AddItem: AddQuantity -> SetQuantity (adding an existing item overwrites its quantity)
#   B2 OrderService.CreateOrderAsync: Guard.Against.Null(basket) removed (NullReferenceException on basket.Items)
#   B3 BasketQueryService.CountTotalBasketItems: SqlQueryRaw with an interpolated username (SQL injection)
#   B4 BasketViewModelService.GetOrCreateBasketForUser: .Result on an async call (sync over async)
set -e
here=$(cd "$(dirname "$0")" && pwd); dir=${1:?target dir}
git clone -q --depth 1 https://github.com/dotnet-architecture/eShopOnWeb.git "$dir/eShopOnWeb"
cd "$dir/eShopOnWeb"
g() { git -c user.name="Dana Dev" -c user.email=dana@example.com -c core.autocrlf=false "$@"; }
B="python3 $here/brep.py"
g checkout -qb feature/checkout-tweaks
$B src/ApplicationCore/Entities/BasketAggregate/Basket.cs "existingItem.AddQuantity(quantity);" "existingItem.SetQuantity(quantity);"
g commit -qam "Basket: simplify quantity update for existing items"
$B src/ApplicationCore/Services/OrderService.cs $'        Guard.Against.Null(basket, nameof(basket));\n' ""
g commit -qam "OrderService: drop redundant guard (spec already filters by id)"
$B src/Infrastructure/Data/Queries/BasketQueryService.cs $'        var totalItems = await _dbContext.Baskets\n            .Where(basket => basket.BuyerId == username)\n            .SelectMany(item => item.Items)\n            .SumAsync(sum => sum.Quantity);' $'        // one round trip instead of the LINQ SelectMany translation\n        var totalItems = await _dbContext.Database\n            .SqlQueryRaw<int>($"SELECT COALESCE(SUM(i.Quantity), 0) AS Value FROM BasketItems i JOIN Baskets b ON b.Id = i.BasketId WHERE b.BuyerId = \'{username}\'")\n            .SingleAsync();'
g commit -qam "BasketQueryService: faster basket count with a single SQL query"
$B src/Web/Services/BasketViewModelService.cs "var basket = (await _basketRepository.FirstOrDefaultAsync(basketSpec));" "var basket = _basketRepository.FirstOrDefaultAsync(basketSpec).Result;"
g commit -qam "BasketViewModelService: tidy basket lookup"
git diff --stat main...HEAD
