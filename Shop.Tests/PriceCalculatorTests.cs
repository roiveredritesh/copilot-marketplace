namespace Shop.Tests;

public class PriceCalculatorTests
{
    [Theory]
    [InlineData(100, 10, 90)]
    [InlineData(19.99, 15, 16.99)]
    public void ApplyDiscount_ReducesPrice(decimal price, decimal percent, decimal expected)
        => Assert.Equal(expected, Shop.PriceCalculator.ApplyDiscount(price, percent));

    [Fact]
    public void ApplyDiscount_RejectsPercentAbove100()
        => Assert.Throws<ArgumentOutOfRangeException>(() => Shop.PriceCalculator.ApplyDiscount(10, 101));
}
