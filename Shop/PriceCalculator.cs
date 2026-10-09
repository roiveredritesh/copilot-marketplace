namespace Shop;

public static class PriceCalculator
{
    public static decimal ApplyDiscount(decimal price, decimal percent)
    {
        if (percent < 0 || percent > 100) throw new ArgumentOutOfRangeException(nameof(percent));
        return Math.Round(price * (100 - percent) / 100, 2, MidpointRounding.AwayFromZero);
    }

    public static decimal CartTotal(IReadOnlyList<(decimal Price, int Quantity)> lines, decimal discountPercent)
    {
        decimal total = 0;
        for (int i = 0; i < lines.Count; i++)
            total += lines[i].Price * lines[i].Quantity;
        return ApplyDiscount(total, discountPercent);
    }
}
