# Test patterns

## xUnit unit test (adapt to NUnit `[Test]`/`[TestCase]` or MSTest `[TestMethod]`/`[DataRow]`)
```csharp
public class PriceCalculatorTests
{
    [Theory]
    [InlineData(100, 0, 100)]
    [InlineData(100, 10, 90)]
    public void Total_AppliesDiscount(decimal price, int pct, decimal expected)
        => Assert.Equal(expected, new PriceCalculator().Total(price, pct));

    [Fact]
    public void Total_NegativeDiscount_Throws()
        => Assert.Throws<ArgumentOutOfRangeException>(() => new PriceCalculator().Total(100, -1));
}
```

## Mocks (only for I/O boundaries)
```csharp
var repo = Substitute.For<IOrderRepository>();            // NSubstitute
repo.GetAsync(42, Arg.Any<CancellationToken>()).Returns(order);
// Moq: var repo = new Mock<IOrderRepository>(); repo.Setup(r => r.GetAsync(42, It.IsAny<CancellationToken>())).ReturnsAsync(order);
```
Time: inject `TimeProvider` (.NET 8+) and use `FakeTimeProvider` in tests. Never `DateTime.Now` inside logic under test.

## ASP.NET Core integration test
```csharp
public class OrdersApiTests(WebApplicationFactory<Program> factory) : IClassFixture<WebApplicationFactory<Program>>
{
    [Fact]
    public async Task Get_UnknownOrder_Returns404()
    {
        var client = factory.WithWebHostBuilder(b => b.ConfigureTestServices(s =>
            s.AddSingleton<IOrderRepository>(new FakeOrderRepository()))).CreateClient();
        var res = await client.GetAsync("/orders/999");
        Assert.Equal(HttpStatusCode.NotFound, res.StatusCode);
    }
}
```
Needs `public partial class Program;` in the app when it uses top-level statements, plus the `Microsoft.AspNetCore.Mvc.Testing` package.

## PostgreSQL with Testcontainers
```csharp
public class PgFixture : IAsyncLifetime
{
    public PostgreSqlContainer Db { get; } = new PostgreSqlBuilder().WithImage("postgres:17-alpine").Build();
    public Task InitializeAsync() => Db.StartAsync();
    public Task DisposeAsync() => Db.DisposeAsync().AsTask();
}
// In tests: options.UseNpgsql(fixture.Db.GetConnectionString()); then context.Database.MigrateAsync()
```
Requires Docker. One container per test class or collection (not per test). Reset data between tests with transactions or Respawn.

## Legacy .NET Framework
MSTest or NUnit via packages.config is common. Keep the existing framework, and avoid features newer than the project's C# version. `dotnet.sh test` runs them through vstest.console.
