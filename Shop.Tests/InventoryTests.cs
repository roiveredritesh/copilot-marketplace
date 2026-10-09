namespace Shop.Tests;

public class InventoryTests
{
    [Fact]
    public void Reserve_ReducesAvailable()
    {
        var inv = new Inventory();
        inv.Add("A", 5);
        inv.Reserve("A", 2);
        Assert.Equal(3, inv.Available("A"));
    }
}
