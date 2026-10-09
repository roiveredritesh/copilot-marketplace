namespace Shop;

public static class PriceCalculator
{
    public static decimal ApplyDiscount(decimal price, decimal percent)
    {
        if (percent < 0 || percent > 100) throw new ArgumentOutOfRangeException(nameof(percent));
        return Math.Round(price * (100 - percent) / 100, 2, MidpointRounding.AwayFromZero);
    }
}
