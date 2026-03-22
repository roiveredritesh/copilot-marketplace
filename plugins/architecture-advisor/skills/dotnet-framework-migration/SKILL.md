# Skill: .NET Framework Migration Guide

## Overview

This guide covers migrating applications from .NET Framework 4.8 to modern .NET (formerly .NET Core, now unified as .NET 6/7/8). It includes migration assessment, compatibility analysis, breaking changes, migration strategies, common challenges, and testing approaches.

## When to Use This Skill

- **Planning .NET Framework to .NET migration**: Understanding scope and effort
- **Assessing compatibility**: Determining if migration is feasible
- **Choosing migration strategy**: Big bang vs incremental approach
- **Resolving breaking changes**: Fixing incompatibilities
- **Performance optimization**: Leveraging modern .NET improvements
- **Modernizing legacy applications**: Taking advantage of new features
- **Container deployment**: Migrating to containerized environments
- **Cross-platform requirements**: Running on Linux or macOS

## Migration Assessment Process

### Phase 1: Inventory Analysis

**Catalog Your Application**:
```
Application Inventory:
├── Project Type: ASP.NET WebForms / MVC / Web API / Windows Service
├── .NET Framework Version: 4.8
├── Target .NET Version: .NET 8 (LTS)
├── Number of Projects: [Count]
├── Lines of Code: [Approximate count]
├── NuGet Packages: [Count]
├── Third-Party Dependencies: [List]
└── Custom Libraries: [List]
```

**Use .NET Portability Analyzer**:
```bash
# Install API Portability Analyzer
dotnet tool install -g Microsoft.DotNet.ApiPort.Console

# Analyze assemblies
ApiPort.exe analyze -f bin\MyApp.dll -t ".NET 8.0"

# Review report (HTML or JSON)
# Shows:
# - Unsupported APIs
# - Compatibility percentage
# - Recommended replacements
```

**Key Metrics to Collect**:
- Portability percentage (target: > 95% for smooth migration)
- Number of unsupported APIs
- Third-party package compatibility
- Windows-specific dependencies
- P/Invoke usage (Windows native calls)

### Phase 2: Compatibility Assessment

**Framework Dependencies**:

| .NET Framework Feature | .NET 8 Status | Alternative |
|------------------------|---------------|-------------|
| System.Web | ❌ Not available | ASP.NET Core |
| AppDomains | ⚠️ Limited | Assembly isolation, separate processes |
| Remoting | ❌ Removed | gRPC, WCF (CoreWCF) |
| WCF Client | ✅ Via CoreWCF | CoreWCF library |
| WCF Server | ⚠️ Limited | CoreWCF (subset of features) |
| WPF | ✅ Windows only | No change needed |
| WinForms | ✅ Windows only | No change needed |
| Binary Serialization | ⚠️ Limited | JSON, Protocol Buffers |
| Code Access Security (CAS) | ❌ Removed | Modern security model |
| Registry | ✅ Windows only | Configuration files, environment variables |

**NuGet Package Compatibility**:

**Check Package Compatibility**:
1. Visit https://www.nuget.org/packages/[PackageName]
2. Check "Frameworks" tab for .NET Standard 2.0+ or .NET 6+
3. Search for package alternatives if not compatible

**Common Package Migrations**:

| .NET Framework Package | .NET 8 Replacement |
|------------------------|-------------------|
| EntityFramework 6 | Entity Framework Core 8 |
| Newtonsoft.Json | System.Text.Json (or keep Newtonsoft) |
| System.Data.SqlClient | Microsoft.Data.SqlClient |
| AutoMapper (old) | AutoMapper 12+ |
| NLog/log4net | Microsoft.Extensions.Logging |

**Code Compatibility Issues**:

```csharp
// ❌ .NET Framework only (System.Web dependency)
using System.Web;
var server = HttpContext.Current.Server;

// ✅ .NET 8 replacement
using Microsoft.AspNetCore.Http;
var server = httpContextAccessor.HttpContext;
```

```csharp
// ❌ .NET Framework only (AppDomain)
AppDomain.CreateDomain("MyDomain");

// ✅ .NET 8 alternative (if needed)
// Use separate process or AssemblyLoadContext
var context = new AssemblyLoadContext("MyContext", isCollectible: true);
```

### Phase 3: Risk Assessment

**Risk Categories**:

**🔴 High Risk**:
- Heavy System.Web usage (WebForms, HttpContext.Current)
- Custom AppDomain usage
- WCF server implementations
- Binary serialization of complex types
- Windows-specific APIs without abstraction
- Large codebase (> 500K LOC) with low test coverage

**🟡 Medium Risk**:
- Entity Framework 6 (upgrade to EF Core)
- Third-party packages with no .NET 8 version
- Moderate System.Web usage (can be refactored)
- Windows Services (migrate to Worker Services)
- Configuration reliance on app.config/web.config

**🟢 Low Risk**:
- ASP.NET Web API (easily migrated)
- .NET Standard 2.0 compatible libraries
- Modern C# code (C# 7+)
- High test coverage
- Minimal Windows-specific code

## Breaking Changes and Workarounds

### System.Web Replacement

**Problem**: System.Web.dll not available in .NET 8

**Breaking Code Examples**:

```csharp
// ❌ .NET Framework
using System.Web;

// HttpContext access
var request = HttpContext.Current.Request;
var response = HttpContext.Current.Response;
var session = HttpContext.Current.Session;

// URL encoding
var encoded = HttpUtility.UrlEncode(value);

// Server operations
var path = HttpContext.Current.Server.MapPath("~/App_Data");
```

**Workarounds**:

```csharp
// ✅ .NET 8 - HttpContext access via dependency injection
public class MyController : ControllerBase
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public MyController(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public IActionResult MyAction()
    {
        var httpContext = _httpContextAccessor.HttpContext;
        var request = httpContext.Request;
        var response = httpContext.Response;
        // Note: Session requires explicit configuration
    }
}

// Register in Program.cs:
builder.Services.AddHttpContextAccessor();
```

```csharp
// ✅ .NET 8 - URL encoding
using System.Web; // Available as NuGet package for encoding utilities
var encoded = System.Web.HttpUtility.UrlEncode(value);

// Or use .NET 8 alternative:
using System.Net;
var encoded = WebUtility.UrlEncode(value);
```

```csharp
// ✅ .NET 8 - Path mapping
using Microsoft.AspNetCore.Hosting;

public class MyService
{
    private readonly IWebHostEnvironment _env;

    public MyService(IWebHostEnvironment env)
    {
        _env = env;
    }

    public string GetDataPath()
    {
        return Path.Combine(_env.ContentRootPath, "App_Data");
    }
}
```

### Configuration System Changes

**Problem**: System.Configuration replaced with Microsoft.Extensions.Configuration

**Breaking Code**:
```csharp
// ❌ .NET Framework
using System.Configuration;

var connString = ConfigurationManager.ConnectionStrings["MyDb"].ConnectionString;
var setting = ConfigurationManager.AppSettings["MySetting"];
```

**Workaround**:
```csharp
// ✅ .NET 8
public class MyService
{
    private readonly IConfiguration _configuration;

    public MyService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public void UseConfiguration()
    {
        var connString = _configuration.GetConnectionString("MyDb");
        var setting = _configuration["MySetting"];

        // Or use strongly-typed configuration
        var myConfig = _configuration.GetSection("MySection").Get<MyConfigClass>();
    }
}
```

**appsettings.json** (replaces app.config/web.config):
```json
{
  "ConnectionStrings": {
    "MyDb": "Server=localhost;Database=MyDb;Trusted_Connection=true;"
  },
  "MySetting": "value",
  "MySection": {
    "Property1": "value1",
    "Property2": 42
  }
}
```

### Binary Serialization Changes

**Problem**: BinaryFormatter is obsolete and dangerous (security risks)

**Breaking Code**:
```csharp
// ❌ .NET Framework
[Serializable]
public class MyData
{
    public string Name { get; set; }
    public int Value { get; set; }
}

var formatter = new BinaryFormatter();
formatter.Serialize(stream, myData);
```

**Workarounds**:

**Option 1: JSON Serialization** (Most Common)
```csharp
// ✅ .NET 8
using System.Text.Json;

public class MyData
{
    public string Name { get; set; }
    public int Value { get; set; }
}

// Serialize
var json = JsonSerializer.Serialize(myData);
File.WriteAllText("data.json", json);

// Deserialize
var json = File.ReadAllText("data.json");
var myData = JsonSerializer.Deserialize<MyData>(json);
```

**Option 2: Protocol Buffers** (Performance Critical)
```csharp
// ✅ .NET 8
using ProtoBuf;

[ProtoContract]
public class MyData
{
    [ProtoMember(1)]
    public string Name { get; set; }

    [ProtoMember(2)]
    public int Value { get; set; }
}

// Serialize
using var stream = File.Create("data.bin");
Serializer.Serialize(stream, myData);

// Deserialize
using var stream = File.OpenRead("data.bin");
var myData = Serializer.Deserialize<MyData>(stream);
```

### Entity Framework 6 to EF Core

**Breaking Changes**:
- Different DbContext initialization
- No automatic lazy loading by default
- Different migration commands
- Some LINQ queries behave differently

**Migration Steps**:

**1. Update DbContext**:
```csharp
// ❌ EF6
public class MyDbContext : DbContext
{
    public MyDbContext() : base("name=MyConnectionString")
    {
    }

    public DbSet<Customer> Customers { get; set; }
}

// ✅ EF Core
public class MyDbContext : DbContext
{
    public MyDbContext(DbContextOptions<MyDbContext> options)
        : base(options)
    {
    }

    public DbSet<Customer> Customers { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure entity mappings
        modelBuilder.Entity<Customer>()
            .ToTable("Customers")
            .HasKey(c => c.CustomerId);
    }
}
```

**2. Register DbContext**:
```csharp
// Program.cs
builder.Services.AddDbContext<MyDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("MyDb")));
```

**3. Update Migrations**:
```bash
# EF6 migrations
Enable-Migrations
Add-Migration InitialCreate
Update-Database

# EF Core migrations
dotnet ef migrations add InitialCreate
dotnet ef database update
```

**4. Handle Lazy Loading**:
```csharp
// EF Core: Explicit loading or eager loading required by default

// Option 1: Eager loading
var customer = context.Customers
    .Include(c => c.Orders)
    .FirstOrDefault(c => c.CustomerId == 1);

// Option 2: Explicit loading
var customer = context.Customers.Find(1);
context.Entry(customer).Collection(c => c.Orders).Load();

// Option 3: Enable lazy loading (requires package)
// Install: Microsoft.EntityFrameworkCore.Proxies
builder.Services.AddDbContext<MyDbContext>(options =>
    options.UseLazyLoadingProxies()
           .UseSqlServer(connectionString));

public class Customer
{
    public virtual ICollection<Order> Orders { get; set; } // Must be virtual
}
```

## Migration Strategies

### Strategy 1: Big Bang Migration

**Description**: Migrate entire application at once

**When to Use**:
- Small to medium applications (< 100K LOC)
- High compatibility score (> 95%)
- Can afford downtime for migration
- Minimal third-party dependencies
- Good test coverage

**Process**:
1. Create feature freeze
2. Create .NET 8 solution structure
3. Migrate all projects simultaneously
4. Fix breaking changes
5. Run full test suite
6. Deploy to production

**Pros**:
- Faster migration (no hybrid state)
- Simpler architecture (no bridging needed)
- Clean cut-over

**Cons**:
- Higher risk
- Longer development cycle before value
- All-or-nothing deployment

**Example Timeline**:
```
Week 1-2:  Setup .NET 8 projects, migrate core libraries
Week 3-4:  Migrate business logic, fix breaking changes
Week 5-6:  Migrate presentation layer (Web/API)
Week 7:    Integration testing
Week 8:    Regression testing
Week 9:    Deployment and monitoring
```

### Strategy 2: Incremental Migration

**Description**: Migrate components gradually over time

**When to Use**:
- Large applications (> 100K LOC)
- Cannot afford long feature freeze
- Multiple teams working on different areas
- Mix of compatible and incompatible code
- Need to deliver value incrementally

**Process**:
1. Identify independent components
2. Migrate libraries to .NET Standard 2.0 first
3. Migrate backend services
4. Migrate APIs
5. Migrate UI layer last

**Layered Approach**:
```
Phase 1: Shared Libraries → .NET Standard 2.0
  ├── Can be used by both .NET Framework and .NET 8
  ├── Migrate utility classes, DTOs, models
  └── No UI or framework-specific code

Phase 2: Data Access Layer → .NET 8
  ├── Migrate to EF Core
  ├── Test thoroughly
  └── Deploy as separate service if needed

Phase 3: Business Logic → .NET 8
  ├── Depends on migrated data layer
  └── Can run alongside .NET Framework

Phase 4: API Layer → .NET 8
  ├── ASP.NET Web API → ASP.NET Core
  └── Run in parallel with legacy API

Phase 5: UI Layer → .NET 8
  ├── MVC/WebForms → ASP.NET Core Razor/Blazor
  └── Final cutover
```

**Pros**:
- Lower risk per phase
- Continuous delivery of value
- Easier to test and validate
- Can pause if issues arise

**Cons**:
- More complex (hybrid architecture)
- Longer overall timeline
- Requires interop between frameworks
- Technical debt of maintaining two versions

### Strategy 3: Strangler Fig Pattern

**Description**: Build new .NET 8 application alongside old, gradually routing traffic

**When to Use**:
- Rewriting vs migrating
- Complex legacy application
- Opportunity to redesign architecture
- Can run systems in parallel
- Need zero-downtime migration

**Process**:
1. Keep .NET Framework app running
2. Build new .NET 8 features alongside
3. Use reverse proxy (YARP, nginx) to route requests
4. Gradually route more traffic to new system
5. Decommission old system when complete

**Example with YARP (Yet Another Reverse Proxy)**:
```csharp
// Program.cs for proxy service
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();
app.MapReverseProxy();
app.Run();
```

```json
// appsettings.json
{
  "ReverseProxy": {
    "Routes": {
      "legacy-route": {
        "ClusterId": "legacy-cluster",
        "Match": {
          "Path": "/legacy/{**catch-all}"
        }
      },
      "modern-route": {
        "ClusterId": "modern-cluster",
        "Match": {
          "Path": "/api/{**catch-all}"
        }
      }
    },
    "Clusters": {
      "legacy-cluster": {
        "Destinations": {
          "legacy": {
            "Address": "http://legacy-app.internal/"
          }
        }
      },
      "modern-cluster": {
        "Destinations": {
          "modern": {
            "Address": "http://modern-app.internal/"
          }
        }
      }
    }
  }
}
```

**Pros**:
- Zero downtime
- Can validate new system with production traffic
- Easy rollback (just route back)
- Gradual risk mitigation

**Cons**:
- Most complex approach
- Running two systems (cost)
- Shared data challenges
- Longest timeline

## Common Migration Challenges

### Challenge 1: WebForms Migration

**Problem**: WebForms has no direct equivalent in .NET 8

**Options**:

**Option A: Migrate to Razor Pages**
```csharp
// .NET Framework WebForms
// MyPage.aspx
<%@ Page Language="C#" CodeBehind="MyPage.aspx.cs" Inherits="MyApp.MyPage" %>
<asp:TextBox ID="txtName" runat="server" />
<asp:Button ID="btnSubmit" runat="server" Text="Submit" OnClick="btnSubmit_Click" />

// MyPage.aspx.cs
protected void btnSubmit_Click(object sender, EventArgs e)
{
    var name = txtName.Text;
    // Process...
}
```

```csharp
// ✅ .NET 8 Razor Pages
// Pages/MyPage.cshtml
@page
@model MyPageModel

<form method="post">
    <input asp-for="Name" />
    <button type="submit">Submit</button>
</form>

// Pages/MyPage.cshtml.cs
public class MyPageModel : PageModel
{
    [BindProperty]
    public string Name { get; set; }

    public void OnPost()
    {
        // Process Name
    }
}
```

**Option B: Migrate to Blazor Server**
```razor
@page "/mypage"

<EditForm Model="@model" OnValidSubmit="HandleSubmit">
    <InputText @bind-Value="model.Name" />
    <button type="submit">Submit</button>
</EditForm>

@code {
    private MyModel model = new();

    private void HandleSubmit()
    {
        // Process model.Name
    }

    public class MyModel
    {
        public string Name { get; set; }
    }
}
```

### Challenge 2: Windows Service Migration

**Problem**: Traditional Windows Services don't exist in .NET 8

**Solution**: Worker Services
```csharp
// ✅ .NET 8 Worker Service
public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;

    public Worker(ILogger<Worker> logger)
    {
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);

            // Do work here

            await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
        }
    }
}

// Program.cs
var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddHostedService<Worker>();

// Can run as Windows Service:
builder.Services.AddWindowsService();

var host = builder.Build();
await host.RunAsync();
```

### Challenge 3: Global.asax Replacement

**Problem**: No Global.asax in ASP.NET Core

**Solution**: Middleware and Program.cs
```csharp
// ❌ .NET Framework Global.asax
protected void Application_Start()
{
    // Startup logic
}

protected void Application_BeginRequest(object sender, EventArgs e)
{
    // Request logic
}

protected void Application_Error(object sender, EventArgs e)
{
    // Error handling
}
```

```csharp
// ✅ .NET 8 Program.cs
var builder = WebApplication.CreateBuilder(args);

// Services configuration (replaces Application_Start)
builder.Services.AddControllers();
builder.Services.AddDbContext<MyDbContext>();

var app = builder.Build();

// Middleware (replaces Application_BeginRequest)
app.Use(async (context, next) =>
{
    // Request logic
    await next();
});

// Error handling middleware (replaces Application_Error)
app.UseExceptionHandler("/Error");

app.MapControllers();
app.Run();
```

## Testing and Validation

### Migration Testing Strategy

**1. Unit Tests**:
- Ensure existing unit tests still pass
- Add tests for refactored code
- Test breaking change workarounds

**2. Integration Tests**:
- Test database connectivity
- Test external service integration
- Test authentication/authorization

**3. Performance Tests**:
- Compare .NET Framework vs .NET 8 performance
- Expected improvements: 2-5x throughput, lower memory
- Load testing with realistic scenarios

**4. Regression Tests**:
- Full end-to-end testing
- Verify all features work as before
- Check edge cases and error handling

### Performance Validation

```bash
# Benchmark .NET Framework vs .NET 8
dotnet run -c Release --framework net48
dotnet run -c Release --framework net8.0

# Expected improvements in .NET 8:
# - Startup time: 2-3x faster
# - Memory usage: 20-40% reduction
# - Throughput: 2-5x higher
# - Response time: 20-50% improvement
```

**Use BenchmarkDotNet**:
```csharp
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

[MemoryDiagnoser]
public class MigrationBenchmark
{
    [Benchmark]
    public void OldFrameworkCode()
    {
        // .NET Framework implementation
    }

    [Benchmark]
    public void NewModernCode()
    {
        // .NET 8 implementation
    }
}

// Run: dotnet run -c Release
BenchmarkRunner.Run<MigrationBenchmark>();
```

## Migration Checklist

**Pre-Migration**:
- [ ] Run .NET Portability Analyzer
- [ ] Document all third-party dependencies
- [ ] Identify Windows-specific code
- [ ] Assess test coverage
- [ ] Choose migration strategy
- [ ] Create migration timeline
- [ ] Set up .NET 8 development environment

**During Migration**:
- [ ] Create new .NET 8 solution/projects
- [ ] Migrate .NET Standard libraries first
- [ ] Update NuGet packages to compatible versions
- [ ] Replace System.Web dependencies
- [ ] Migrate configuration system
- [ ] Update EF6 to EF Core (if applicable)
- [ ] Replace binary serialization
- [ ] Fix breaking changes
- [ ] Update unit tests
- [ ] Add integration tests

**Post-Migration**:
- [ ] Run full test suite
- [ ] Performance testing and comparison
- [ ] Security audit
- [ ] Update deployment pipelines
- [ ] Update documentation
- [ ] Train team on .NET 8 differences
- [ ] Monitor production metrics
- [ ] Gather feedback and iterate

## Key Takeaways

1. **Assess first, migrate second**: Use Portability Analyzer to understand scope
2. **Choose right strategy**: Big bang for small apps, incremental for large
3. **Migrate libraries first**: .NET Standard 2.0 libraries work in both frameworks
4. **System.Web is the biggest hurdle**: Plan for HttpContext, configuration changes
5. **EF Core is different**: Lazy loading, migrations, and LINQ behavior changes
6. **Test extensively**: Unit, integration, performance, and regression tests
7. **Expect performance gains**: 2-5x throughput improvement typical
8. **Plan for breaking changes**: Binary serialization, AppDomains, Remoting all changed
9. **Use .NET 8 LTS**: Long-term support (3 years) vs standard (18 months)
10. **Document everything**: Migration decisions, workarounds, and new patterns

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Migration & Modernization
