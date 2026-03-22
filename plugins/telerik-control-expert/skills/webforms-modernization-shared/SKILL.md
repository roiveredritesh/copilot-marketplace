# Skill: WebForms Modernization Guide

## Overview

ASP.NET WebForms has been the foundation of many enterprise applications since 2002, but it's no longer supported in modern .NET. This guide covers strategies for migrating WebForms applications to modern frameworks including Blazor Server, Blazor WebAssembly, Razor Pages, and ASP.NET Core MVC, with focus on control mapping, state management, and gradual migration strategies.

## When to Use This Skill

- **Modernizing legacy WebForms applications**: Moving off unsupported technology
- **Planning migration strategy**: Choosing between Blazor, Razor Pages, or MVC
- **Mapping WebForms controls**: Finding modern equivalents
- **Replacing ViewState**: Modern state management patterns
- **Gradual migration**: Incremental modernization approach
- **Performance improvement**: WebForms to modern high-performance framework
- **Cross-platform deployment**: Moving to Linux/containers

## Understanding WebForms Architecture

### WebForms Key Concepts

**Page Lifecycle**:
```
Init → Load → Control Events → PreRender → Render → Unload
```

**ViewState**:
- Server-side state serialized to hidden field
- Automatically preserves control state across postbacks
- Large ViewState = performance issues

**Postback Model**:
- Every interaction posts entire page to server
- Server processes event, updates controls, renders HTML
- High server load, poor UX for rich interactions

**Server Controls**:
- Abstraction over HTML with server-side processing
- Event-driven programming model
- State management built-in

### Why Migrate Away from WebForms?

**Technical Reasons**:
- Not supported in .NET Core/.NET 8
- Poor performance (large ViewState, full page postbacks)
- Difficult to test (tightly coupled to HTTP context)
- Limited client-side interactivity
- Not suitable for modern SPA patterns
- Cannot run on Linux/containers

**Business Reasons**:
- Difficulty hiring WebForms developers
- No new features or improvements
- End of support/security updates
- Cannot leverage modern tooling (Blazor, React, Angular)

## Migration Target Frameworks

### Option 1: Blazor Server

**Best For**:
- WebForms developers (similar programming model)
- Rich interactive UIs
- Rapid development
- Internal/intranet applications
- Teams with C# expertise, limited JavaScript knowledge

**Architecture**:
```
Browser ←→ SignalR WebSocket ←→ Server (Blazor)
  │                                    │
  │                                    │
  └──── UI rendered on server ─────────┘
       Sent to browser as HTML diffs
```

**Pros**:
- **Similar to WebForms**: Server-side rendering, C# code
- **Real-time updates**: SignalR for live UI updates
- **Small payload**: Only send UI changes, not full page
- **Full .NET API access**: Direct database access, file system
- **Easy learning curve**: For WebForms developers

**Cons**:
- **Server connection required**: No offline support
- **Scalability concerns**: SignalR connection per user
- **Latency**: Every interaction roundtrips to server
- **Not suitable for public internet**: Connection overhead

**Example WebForms → Blazor Server**:

```csharp
// ❌ WebForms (.aspx)
<%@ Page Language="C#" CodeBehind="Customers.aspx.cs" Inherits="MyApp.Customers" %>

<asp:TextBox ID="txtSearch" runat="server" />
<asp:Button ID="btnSearch" runat="server" Text="Search" OnClick="btnSearch_Click" />
<asp:GridView ID="gvCustomers" runat="server" AutoGenerateColumns="false">
    <Columns>
        <asp:BoundField DataField="CustomerName" HeaderText="Name" />
        <asp:BoundField DataField="Email" HeaderText="Email" />
    </Columns>
</asp:GridView>

// Customers.aspx.cs
protected void btnSearch_Click(object sender, EventArgs e)
{
    var searchTerm = txtSearch.Text;
    gvCustomers.DataSource = _customerService.Search(searchTerm);
    gvCustomers.DataBind();
}
```

```razor
@* ✅ Blazor Server (.razor) *@
@page "/customers"
@inject ICustomerService CustomerService

<input @bind="searchTerm" placeholder="Search..." />
<button @onclick="Search">Search</button>

<table class="table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Email</th>
        </tr>
    </thead>
    <tbody>
        @foreach (var customer in customers)
        {
            <tr>
                <td>@customer.CustomerName</td>
                <td>@customer.Email</td>
            </tr>
        }
    </tbody>
</table>

@code {
    private string searchTerm;
    private List<Customer> customers = new();

    private async Task Search()
    {
        customers = await CustomerService.SearchAsync(searchTerm);
    }

    protected override async Task OnInitializedAsync()
    {
        customers = await CustomerService.GetAllAsync();
    }
}
```

### Option 2: Blazor WebAssembly

**Best For**:
- Public-facing SPAs
- Offline support needed
- Client-side performance critical
- Want to reduce server load
- Progressive Web Apps (PWAs)

**Architecture**:
```
Browser (WebAssembly)
  │
  │─── .NET Runtime in Browser
  │─── App runs client-side
  │
  └──→ API (Backend) via HTTP
```

**Pros**:
- **Runs client-side**: No server connection required
- **Offline capable**: Can work without network
- **Server offload**: Less server processing
- **Rich interactivity**: No latency for UI updates
- **PWA support**: Installable, offline-first apps

**Cons**:
- **Large initial download**: ~2MB .NET runtime
- **Slow initial load**: WebAssembly startup time
- **No direct data access**: Must use APIs
- **Browser compatibility**: Requires modern browser
- **Debugging complexity**: Client-side debugging

**When to Choose WebAssembly over Server**:
- Public internet application (many users)
- Need offline functionality
- Want to reduce hosting costs
- Client-side performance important
- Already have backend APIs

### Option 3: Razor Pages

**Best For**:
- Page-focused applications
- Simpler than MVC
- CRUD applications
- Closest WebForms equivalent (page-based)
- Teams wanting simpler architecture than MVC

**Architecture**:
```
Browser ──HTTP──→ Razor Page (Server) ──→ Database
         ←HTML──
```

**Pros**:
- **Page-based**: Similar mental model to WebForms
- **Simpler than MVC**: Less ceremony, easier to learn
- **Server-side rendering**: SEO-friendly
- **Good performance**: Server-side compiled
- **Easy testing**: Better testability than WebForms

**Cons**:
- **Full page reloads**: Not SPA experience
- **Less interactive**: Requires JavaScript for rich UX
- **Server-dependent**: Needs server for every request

**Example WebForms → Razor Pages**:

```csharp
// ❌ WebForms
// CustomerEdit.aspx.cs
public partial class CustomerEdit : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            int customerId = int.Parse(Request.QueryString["id"]);
            var customer = _customerService.GetById(customerId);
            txtName.Text = customer.Name;
            txtEmail.Text = customer.Email;
        }
    }

    protected void btnSave_Click(object sender, EventArgs e)
    {
        var customer = new Customer
        {
            CustomerId = int.Parse(Request.QueryString["id"]),
            Name = txtName.Text,
            Email = txtEmail.Text
        };
        _customerService.Update(customer);
        Response.Redirect("Customers.aspx");
    }
}
```

```csharp
// ✅ Razor Pages
// Pages/Customers/Edit.cshtml.cs
public class EditModel : PageModel
{
    private readonly ICustomerService _customerService;

    public EditModel(ICustomerService customerService)
    {
        _customerService = customerService;
    }

    [BindProperty]
    public Customer Customer { get; set; }

    public async Task<IActionResult> OnGetAsync(int id)
    {
        Customer = await _customerService.GetByIdAsync(id);
        if (Customer == null)
            return NotFound();

        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
            return Page();

        await _customerService.UpdateAsync(Customer);
        return RedirectToPage("./Index");
    }
}
```

```html
@* Pages/Customers/Edit.cshtml *@
@page "{id:int}"
@model EditModel

<form method="post">
    <div class="form-group">
        <label asp-for="Customer.Name"></label>
        <input asp-for="Customer.Name" class="form-control" />
        <span asp-validation-for="Customer.Name"></span>
    </div>
    <div class="form-group">
        <label asp-for="Customer.Email"></label>
        <input asp-for="Customer.Email" class="form-control" />
        <span asp-validation-for="Customer.Email"></span>
    </div>
    <button type="submit" class="btn btn-primary">Save</button>
    <a asp-page="./Index" class="btn btn-secondary">Cancel</a>
</form>
```

### Option 4: ASP.NET Core MVC

**Best For**:
- Large, complex applications
- Need separation of concerns
- RESTful applications
- Teams familiar with MVC pattern
- Want full control over routing and views

**Pros**:
- **Clear separation**: Models, Views, Controllers
- **Flexible routing**: Attribute and convention-based
- **Testable**: Controllers easily unit tested
- **Mature pattern**: Well-understood architecture

**Cons**:
- **More complexity**: More moving parts than Razor Pages
- **Steeper learning curve**: Especially for WebForms devs
- **Verbose**: More code and structure

## Control Mapping Guide

### Common WebForms Controls → Modern Equivalents

#### TextBox / Label / Button

```csharp
// ❌ WebForms
<asp:Label ID="lblMessage" runat="server" Text="Hello" />
<asp:TextBox ID="txtName" runat="server" />
<asp:Button ID="btnSubmit" runat="server" Text="Submit" OnClick="btnSubmit_Click" />

protected void btnSubmit_Click(object sender, EventArgs e)
{
    lblMessage.Text = "Hello " + txtName.Text;
}
```

```razor
@* ✅ Blazor *@
<p>@message</p>
<input @bind="name" />
<button @onclick="Submit">Submit</button>

@code {
    private string message = "Hello";
    private string name;

    private void Submit()
    {
        message = $"Hello {name}";
    }
}
```

```html
<!-- ✅ Razor Pages -->
<p>@Model.Message</p>
<form method="post">
    <input asp-for="Name" />
    <button type="submit">Submit</button>
</form>
```

#### GridView / Repeater

```csharp
// ❌ WebForms GridView
<asp:GridView ID="gvProducts" runat="server" AutoGenerateColumns="false">
    <Columns>
        <asp:BoundField DataField="ProductName" HeaderText="Product" />
        <asp:BoundField DataField="Price" HeaderText="Price" DataFormatString="{0:C}" />
        <asp:TemplateField>
            <ItemTemplate>
                <asp:Button ID="btnEdit" runat="server" Text="Edit"
                    CommandName="Edit" CommandArgument='<%# Eval("ProductId") %>' />
            </ItemTemplate>
        </asp:TemplateField>
    </Columns>
</asp:GridView>

protected void Page_Load(object sender, EventArgs e)
{
    gvProducts.DataSource = _productService.GetAll();
    gvProducts.DataBind();
}
```

```razor
@* ✅ Blazor - Table *@
<table class="table">
    <thead>
        <tr>
            <th>Product</th>
            <th>Price</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        @foreach (var product in products)
        {
            <tr>
                <td>@product.ProductName</td>
                <td>@product.Price.ToString("C")</td>
                <td>
                    <button @onclick="() => Edit(product.ProductId)">Edit</button>
                </td>
            </tr>
        }
    </tbody>
</table>

@code {
    private List<Product> products = new();

    protected override async Task OnInitializedAsync()
    {
        products = await ProductService.GetAllAsync();
    }

    private void Edit(int productId)
    {
        NavigationManager.NavigateTo($"/products/edit/{productId}");
    }
}
```

**Modern Grid Component Libraries**:
- **Telerik Blazor**: Commercial, feature-rich (sorting, filtering, paging)
- **Radzen Blazor**: Free, open-source DataGrid
- **MudBlazor**: Material Design components including table
- **Syncfusion Blazor**: Commercial, comprehensive suite

#### DropDownList / ListBox

```csharp
// ❌ WebForms
<asp:DropDownList ID="ddlCategories" runat="server"
    AutoPostBack="true" OnSelectedIndexChanged="ddlCategories_SelectedIndexChanged" />

protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        ddlCategories.DataSource = _categoryService.GetAll();
        ddlCategories.DataTextField = "CategoryName";
        ddlCategories.DataValueField = "CategoryId";
        ddlCategories.DataBind();
    }
}

protected void ddlCategories_SelectedIndexChanged(object sender, EventArgs e)
{
    int categoryId = int.Parse(ddlCategories.SelectedValue);
    // Load products for category
}
```

```razor
@* ✅ Blazor *@
<select @bind="selectedCategoryId" @bind:after="CategoryChanged">
    <option value="0">Select Category</option>
    @foreach (var category in categories)
    {
        <option value="@category.CategoryId">@category.CategoryName</option>
    }
</select>

@code {
    private List<Category> categories = new();
    private int selectedCategoryId;

    protected override async Task OnInitializedAsync()
    {
        categories = await CategoryService.GetAllAsync();
    }

    private async Task CategoryChanged()
    {
        // Load products for selectedCategoryId
    }
}
```

#### FileUpload

```csharp
// ❌ WebForms
<asp:FileUpload ID="fileUpload" runat="server" />
<asp:Button ID="btnUpload" runat="server" Text="Upload" OnClick="btnUpload_Click" />

protected void btnUpload_Click(object sender, EventArgs e)
{
    if (fileUpload.HasFile)
    {
        string fileName = Path.GetFileName(fileUpload.FileName);
        string path = Server.MapPath("~/Uploads/") + fileName;
        fileUpload.SaveAs(path);
    }
}
```

```razor
@* ✅ Blazor *@
<InputFile OnChange="HandleFileSelected" />
<button @onclick="Upload">Upload</button>

@code {
    private IBrowserFile selectedFile;

    private void HandleFileSelected(InputFileChangeEventArgs e)
    {
        selectedFile = e.File;
    }

    private async Task Upload()
    {
        if (selectedFile != null)
        {
            var path = Path.Combine(env.WebRootPath, "uploads", selectedFile.Name);

            await using FileStream fs = new(path, FileMode.Create);
            await selectedFile.OpenReadStream().CopyToAsync(fs);
        }
    }
}
```

#### Calendar / DatePicker

```csharp
// ❌ WebForms
<asp:Calendar ID="calendar" runat="server" OnSelectionChanged="calendar_SelectionChanged" />
<asp:Label ID="lblSelected" runat="server" />

protected void calendar_SelectionChanged(object sender, EventArgs e)
{
    lblSelected.Text = calendar.SelectedDate.ToShortDateString();
}
```

```razor
@* ✅ Blazor *@
<input type="date" @bind="selectedDate" @bind:after="DateChanged" />
<p>Selected: @selectedDate.ToShortDateString()</p>

@code {
    private DateTime selectedDate = DateTime.Today;

    private void DateChanged()
    {
        // React to date change
    }
}
```

**Modern Date Picker Libraries**:
```razor
@* Using MudBlazor *@
<MudDatePicker @bind-Date="selectedDate" Label="Select Date" />

@* Using Telerik Blazor *@
<TelerikDatePicker @bind-Value="selectedDate" Format="MM/dd/yyyy" />
```

#### Validation Controls

```csharp
// ❌ WebForms
<asp:TextBox ID="txtEmail" runat="server" />
<asp:RequiredFieldValidator ID="rfvEmail" runat="server"
    ControlToValidate="txtEmail" ErrorMessage="Email is required" />
<asp:RegularExpressionValidator ID="revEmail" runat="server"
    ControlToValidate="txtEmail" ErrorMessage="Invalid email"
    ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*" />
```

```razor
@* ✅ Blazor with DataAnnotations *@
<EditForm Model="model" OnValidSubmit="HandleSubmit">
    <DataAnnotationsValidator />

    <InputText @bind-Value="model.Email" />
    <ValidationMessage For="() => model.Email" />

    <button type="submit">Submit</button>
</EditForm>

@code {
    private CustomerModel model = new();

    public class CustomerModel
    {
        [Required(ErrorMessage = "Email is required")]
        [EmailAddress(ErrorMessage = "Invalid email")]
        public string Email { get; set; }
    }

    private void HandleSubmit()
    {
        // Valid submission
    }
}
```

## ViewState Replacement Strategies

### Understanding ViewState

**WebForms ViewState**:
```html
<input type="hidden" name="__VIEWSTATE" value="dDwtMTY3NjQ4OTExNjs7Pgs...5KB of base64..." />
```

**Problems**:
- Large page size (can be 50KB+)
- Security concern (contains application state)
- Performance impact (serialization/deserialization)
- Not scalable (grows with complexity)

### Modern State Management

**1. Component State (Blazor)**

```razor
@* State managed in component *@
@code {
    // Component-scoped state
    private List<Customer> customers = new();
    private Customer selectedCustomer;
    private bool isLoading;

    // State automatically maintained during component lifetime
    // No ViewState needed!
}
```

**2. Scoped Services (Dependency Injection)**

```csharp
// Shared state across components within same scope (page/circuit)
public class CustomerState
{
    public Customer SelectedCustomer { get; set; }
    public List<Customer> Customers { get; set; }
}

// Register as scoped
builder.Services.AddScoped<CustomerState>();

// Use in components
@inject CustomerState State

@code {
    private void SelectCustomer(int id)
    {
        State.SelectedCustomer = State.Customers.FirstOrDefault(c => c.Id == id);
    }
}
```

**3. Browser Storage (Session/Local Storage)**

```razor
@inject Blazored.LocalStorage.ILocalStorageService LocalStorage

@code {
    protected override async Task OnInitializedAsync()
    {
        // Persist state to browser local storage
        var savedState = await LocalStorage.GetItemAsync<CustomerState>("customer-state");
        if (savedState != null)
        {
            // Restore state
        }
    }

    private async Task SaveState()
    {
        await LocalStorage.SetItemAsync("customer-state", currentState);
    }
}
```

**4. Query String / Route Parameters**

```razor
@* Instead of ViewState for page state, use URL *@
@page "/customers/{customerId:int}/orders"

@code {
    [Parameter]
    public int CustomerId { get; set; }

    // State is in URL - bookmarkable, shareable!
}
```

**5. State Container Pattern**

```csharp
// AppState.cs - Application-wide state
public class AppState
{
    private string currentUser;

    public string CurrentUser
    {
        get => currentUser;
        set
        {
            currentUser = value;
            NotifyStateChanged();
        }
    }

    public event Action OnChange;

    private void NotifyStateChanged() => OnChange?.Invoke();
}

// Register as singleton
builder.Services.AddSingleton<AppState>();

// Use in component
@inject AppState AppState
@implements IDisposable

@code {
    protected override void OnInitialized()
    {
        AppState.OnChange += StateHasChanged;
    }

    public void Dispose()
    {
        AppState.OnChange -= StateHasChanged;
    }
}
```

## Gradual Migration Strategies

### Strategy 1: Side-by-Side Migration

**Approach**: Run WebForms and modern app in parallel, migrate pages incrementally

**Setup**:
```
/OldApp (WebForms on IIS)
  ├── Default.aspx (WebForms)
  ├── Customers.aspx (WebForms)
  └── Products.aspx (WebForms)

/NewApp (Blazor/Razor Pages on Kestrel)
  ├── Pages/
  │   ├── Index.razor (Migrated)
  │   └── Customers.razor (Migrated)
  └── Products.aspx still routes to old app
```

**URL Routing (IIS URL Rewrite)**:
```xml
<rewrite>
  <rules>
    <!-- Route migrated pages to new app -->
    <rule name="Customers to New App" stopProcessing="true">
      <match url="^customers(.*)$" />
      <action type="Rewrite" url="http://localhost:5000/customers{R:1}" />
    </rule>

    <!-- All other pages stay in WebForms -->
    <rule name="Default to WebForms" stopProcessing="true">
      <match url=".*" />
      <action type="None" />
    </rule>
  </rules>
</rewrite>
```

**Pros**:
- Low risk (rollback easily)
- Incremental value delivery
- Team learns gradually

**Cons**:
- Complex routing
- Maintain two apps
- Shared authentication complexity

### Strategy 2: Feature-by-Feature Migration

**Approach**: Migrate complete features/modules one at a time

**Example**:
```
Phase 1: Reporting Module → Blazor
Phase 2: Customer Management → Blazor
Phase 3: Order Processing → Blazor
Phase 4: Admin Panel → Blazor
```

**Shared Resources**:
- Database remains shared
- Authentication/Authorization unified
- Shared business logic libraries (.NET Standard)

### Strategy 3: Wrapper/Adapter Pattern

**Approach**: Embed new technology within WebForms initially

**Blazor in WebForms** (Experimental):
```aspx
<%@ Page Language="C#" %>
<!DOCTYPE html>
<html>
<head>
    <base href="/" />
    <script src="_framework/blazor.server.js"></script>
</head>
<body>
    <app>
        <component type="typeof(MyBlazorComponent)" render-mode="ServerPrerendered" />
    </app>

    <!-- WebForms content -->
    <asp:TextBox ID="txt" runat="server" />
</body>
</html>
```

**Note**: This is complex and not officially supported. Better to migrate pages fully.

## Migration Patterns

### Pattern 1: Master Page → Layout

```aspx
@* ❌ WebForms Master Page (Site.Master) *@
<%@ Master Language="C#" %>
<!DOCTYPE html>
<html>
<head runat="server">
    <title>My App</title>
    <asp:ContentPlaceHolder ID="head" runat="server" />
</head>
<body>
    <div id="header"><!-- Header --></div>
    <asp:ContentPlaceHolder ID="MainContent" runat="server" />
    <div id="footer"><!-- Footer --></div>
</body>
</html>

@* Content Page *@
<%@ Page MasterPageFile="~/Site.Master" %>
<asp:Content ContentPlaceHolderID="MainContent" runat="server">
    <!-- Page content -->
</asp:Content>
```

```razor
@* ✅ Blazor Layout (Shared/MainLayout.razor) *@
@inherits LayoutComponentBase

<div class="page">
    <div class="header"><!-- Header --></div>

    <div class="content">
        @Body
    </div>

    <div class="footer"><!-- Footer --></div>
</div>

@* Page using layout *@
@page "/customers"
@layout MainLayout

<h1>Customers</h1>
<!-- Page content -->
```

### Pattern 2: User Controls → Components

```aspx
@* ❌ WebForms User Control (CustomerInfo.ascx) *@
<%@ Control Language="C#" %>
<div>
    <asp:Label ID="lblName" runat="server" />
    <asp:Label ID="lblEmail" runat="server" />
</div>

<script runat="server">
    public Customer Customer
    {
        set
        {
            lblName.Text = value.Name;
            lblEmail.Text = value.Email;
        }
    }
</script>
```

```razor
@* ✅ Blazor Component (CustomerInfo.razor) *@
<div>
    <div>@Customer.Name</div>
    <div>@Customer.Email</div>
</div>

@code {
    [Parameter]
    public Customer Customer { get; set; }
}

@* Usage *@
<CustomerInfo Customer="@selectedCustomer" />
```

### Pattern 3: Code-Behind → Code Block

```csharp
// ❌ WebForms Code-Behind (Products.aspx.cs)
public partial class Products : Page
{
    private ProductService _productService = new ProductService();

    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadProducts();
        }
    }

    private void LoadProducts()
    {
        gvProducts.DataSource = _productService.GetAll();
        gvProducts.DataBind();
    }
}
```

```razor
@* ✅ Blazor Code Block *@
@page "/products"
@inject IProductService ProductService

<h1>Products</h1>
<!-- Product list -->

@code {
    private List<Product> products = new();

    protected override async Task OnInitializedAsync()
    {
        await LoadProducts();
    }

    private async Task LoadProducts()
    {
        products = await ProductService.GetAllAsync();
    }
}
```

## Testing Modernized Applications

### Unit Testing Blazor Components

```csharp
// Using bUnit (Blazor Unit Testing)
using Bunit;
using Xunit;

public class CustomerListTests : TestContext
{
    [Fact]
    public void CustomerList_Renders_Customers()
    {
        // Arrange
        var customers = new List<Customer>
        {
            new Customer { Id = 1, Name = "John" },
            new Customer { Id = 2, Name = "Jane" }
        };

        var mockService = new Mock<ICustomerService>();
        mockService.Setup(s => s.GetAllAsync()).ReturnsAsync(customers);

        Services.AddSingleton(mockService.Object);

        // Act
        var cut = RenderComponent<CustomerList>();

        // Assert
        cut.Find("table").MarkupMatches(
            @"<table>
                <tr><td>John</td></tr>
                <tr><td>Jane</td></tr>
              </table>");
    }
}
```

### Integration Testing

```csharp
public class CustomerPagesTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public CustomerPagesTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task CustomersPage_Returns_Success()
    {
        // Act
        var response = await _client.GetAsync("/customers");

        // Assert
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        Assert.Contains("Customers", content);
    }
}
```

## Migration Checklist

**Assessment**:
- [ ] Inventory all WebForms pages
- [ ] Document custom controls and user controls
- [ ] Identify ViewState dependencies
- [ ] Catalog third-party components (Telerik, DevExpress)
- [ ] Assess JavaScript/jQuery usage
- [ ] Evaluate authentication/authorization
- [ ] Choose target framework (Blazor/Razor Pages/MVC)
- [ ] Plan migration strategy (big bang vs incremental)

**Migration**:
- [ ] Set up new project structure
- [ ] Migrate shared libraries first
- [ ] Create layouts (replace master pages)
- [ ] Migrate user controls to components
- [ ] Convert pages to modern equivalents
- [ ] Replace ViewState with appropriate state management
- [ ] Implement validation with DataAnnotations
- [ ] Migrate authentication/authorization
- [ ] Update routing and navigation
- [ ] Replace server controls with HTML + bindings

**Testing**:
- [ ] Unit test components
- [ ] Integration test pages
- [ ] End-to-end testing
- [ ] Performance testing
- [ ] Accessibility testing
- [ ] Cross-browser testing (Blazor WebAssembly)

**Deployment**:
- [ ] Update hosting (IIS to Kestrel or both)
- [ ] Configure reverse proxy if needed
- [ ] Set up CI/CD pipeline
- [ ] Migration rollback plan
- [ ] Monitor and optimize

## Key Takeaways

1. **Choose the right target**: Blazor Server for internal apps, Blazor WASM for public SPAs, Razor Pages for simpler page-based apps
2. **Gradual migration is lower risk**: Migrate incrementally, page by page or feature by feature
3. **ViewState is obsolete**: Use component state, DI services, or browser storage
4. **Components replace user controls**: Blazor components are more powerful and reusable
5. **Dependency injection everywhere**: Replace `new` with DI for testability
6. **Async is the default**: Use `async`/`await` for all I/O operations
7. **No more PostBack**: State managed client-side or via SignalR, not full page posts
8. **Testing is easier**: Components are testable, no HttpContext dependency
9. **Third-party controls**: Check for Blazor equivalents (Telerik, Radzen, MudBlazor)
10. **Consider architecture redesign**: Don't just port, improve design patterns

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Migration & Modernization
