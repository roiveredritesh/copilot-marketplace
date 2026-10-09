namespace Shop;

public static class PriceCalculator
{
    public static decimal ApplyDiscount(decimal price, decimal percent)
    {
        if (percent < 0 || percent > 100) throw new ArgumentOutOfRangeException(nameof(percent));
        return RoundMoney(price * (100 - percent) / 100);
    }

    public static decimal CartTotal(IReadOnlyList<(decimal Price, int Quantity)> lines, decimal discountPercent)
    {
        decimal total = 0;
        foreach (var line in lines)
            total += line.Price * line.Quantity;
        return ApplyDiscount(total, discountPercent);
    }

    private static decimal RoundMoney(decimal value) => Math.Round(value, 2, MidpointRounding.AwayFromZero);
}
