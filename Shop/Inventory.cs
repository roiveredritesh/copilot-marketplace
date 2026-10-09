namespace Shop;

public class Inventory
{
    private readonly Dictionary<string, int> _stock = new();

    public void Add(string sku, int quantity)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(quantity);
        _stock[sku] = _stock.GetValueOrDefault(sku) + quantity;
    }

    public bool TryReserve(string sku, int quantity)
    {
        var available = _stock.GetValueOrDefault(sku);
        if (available < quantity) return false;
        _stock[sku] = available - quantity;
        return true;
    }

    public int Available(string sku) => _stock.GetValueOrDefault(sku);
}
