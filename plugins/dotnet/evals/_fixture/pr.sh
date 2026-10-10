#!/usr/bin/env bash
# Shop repo with PR #7 (feat/discounts) and its review threads, already rendered the way the
# pr-comments fetch writes them. The fake gh (evals/fakebin/gh) serves these files.
set -e
d0=${BASH_SOURCE[0]//\\//}
bash "${d0%/*}/shop.sh"
g() { git -c core.autocrlf=false -c user.name=dev1 -c user.email=dev1@example.com "$@"; }
g branch -m main 2>/dev/null || true
g checkout -qb feat/discounts
cat > src/Shop.Api/Services/DiscountService.cs <<'X'
namespace Shop.Api.Services;
public class DiscountService
{
    public decimal ApplyDiscount(decimal total, decimal percent)
    {
        var d = total * percent / 100;
        return total - d;
    }
}
X
g add -A && g commit -qm "Add order discounts"
d=.git/eval-fake; mkdir -p "$d"; : > "$d/calls.log"
echo 7 > "$d/pr"; echo feat/discounts > "$d/head"
echo "7 Add order discounts | feat/discounts -> main | author dev1" > "$d/pr-line.txt"
cat > "$d/threads.txt" <<'X'
THREAD PRRT_k1 src/Shop.Api/Services/DiscountService.cs:4 | 2 comments | alice: percent isn't validated: a negative percent increases the total and anything over 100 makes
--- [1001] alice:
percent isn't validated: a negative percent increases the total and anything over 100 makes it negative. Throw ArgumentOutOfRangeException when percent is outside 0..100.
--- [1002] bob:
I disagree with throwing here. percent comes straight from a promo code form, so clamp it to 0..100 instead of returning a 500 to the customer.
END THREAD

THREAD PRRT_k2 src/Shop.Api/Services/DiscountService.cs:7 | 1 comments | carol: Name it properly:
--- [1003] carol:
Name it properly:
```suggestion
        var discount = total * percent / 100;
        return total - discount;
```
END THREAD

THREAD PRRT_k3 src/Shop.Api/Services/OrderService.cs:9 | 1 comments | dave: This never saves the order to the database, so it's lost after the request ends.
--- [1004] dave:
This never saves the order to the database, so it's lost after the request ends.
END THREAD

THREAD PRRT_k4 src/Shop.Api/Services/OrderService.cs:9 | 1 comments | alice: Why DateTime.UtcNow here and not DateTime.Now?
--- [1005] alice:
Why DateTime.UtcNow here and not DateTime.Now?
END THREAD

THREAD PRRT_k5 src/Shop.Api/Controllers/OrdersController.cs:12 | 2 comments | bob: Should this return 200 OK instead of 201?
--- [1006] bob:
Should this return 200 OK instead of 201?
--- [1007] bob:
Never mind, 201 Created with a Location is right for a POST. Ignore this one.
END THREAD

THREAD PRRT_k6 src/Shop.Api/Services/OrderService.cs:8 | 1 comments | carol: unitPrice isn't validated. A negative unit price creates an order with a negative
--- [1008] carol:
unitPrice isn't validated. A negative unit price creates an order with a negative total. Reject unitPrice <= 0 like quantity.
END THREAD
X
printf 'REVIEW alice CHANGES_REQUESTED\nPlease sort out the validation comments before merge.\nEND\n' > "$d/conversation.txt"
