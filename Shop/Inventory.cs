namespace Shop;

public class Inventory
{
    private readonly Dictionary<string, int> _stock = new();

    public void Add(string sku, int quantity)
    {
        _stock[sku] = _stock.GetValueOrDefault(sku) + quantity;
    }

    public void Reserve(string sku, int quantity)
    {
        int available = _stock.GetValueOrDefault(sku);
        _stock[sku] = available - quantity;
    }

    public int Available(string sku) => _stock[sku];
}
