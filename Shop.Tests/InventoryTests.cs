namespace Shop.Tests;

public class InventoryTests
{
    [Fact]
    public void TryReserve_ReducesAvailable()
    {
        var inv = new Inventory();
        inv.Add("A", 5);
        Assert.True(inv.TryReserve("A", 2));
        Assert.Equal(3, inv.Available("A"));
    }

    [Fact]
    public void TryReserve_ReturnsFalseAndKeepsStock_WhenInsufficient()
    {
        var inv = new Inventory();
        inv.Add("A", 2);
        Assert.False(inv.TryReserve("A", 5));
        Assert.Equal(2, inv.Available("A"));
    }

    [Fact]
    public void TryReserve_ReturnsFalse_ForUnknownSku()
        => Assert.False(new Inventory().TryReserve("X", 1));

    [Theory]
    [InlineData(0)]
    [InlineData(-3)]
    public void Add_RejectsNonPositiveQuantity(int quantity)
        => Assert.Throws<ArgumentOutOfRangeException>(() => new Inventory().Add("A", quantity));
}
