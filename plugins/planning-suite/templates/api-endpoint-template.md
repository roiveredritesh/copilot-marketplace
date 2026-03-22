---
template-name: api-endpoint
description: Template for planning new API endpoints or WebForms pages
applies-to: [api-endpoint, webforms-page, controller-action]
required-inputs: [endpoint-name, request-response-format, business-logic]
---

# Template: API Endpoint / WebForms Page Planning

## When to Use
Use this template when adding new API endpoints (REST/GraphQL) or new WebForms pages.

**Examples**:
- Add `/api/users` GET endpoint
- Create WebForms page for product management
- Add POST endpoint for order creation

## Required Inputs

1. **Endpoint Name**: `/api/products` or page name like `ProductManagement.aspx`
2. **Request/Response**: What data comes in and goes out
3. **Business Logic**: What service handles this
4. **Authorization**: Who can access (roles/permissions)

## Planning Structure

### Phase 1: Design (1 hour)

**Define**:
- HTTP method (GET, POST, PUT, DELETE)
- Request DTO (Data Transfer Object)
- Response DTO
- Status codes returned
- Authorization requirements
- Validation rules

### Phase 2: Create DTOs (30 minutes)

**Files**:
- `Models/DTOs/Create[Resource]Request.cs`
- `Models/DTOs/[Resource]Response.cs`
- `Models/DTOs/Update[Resource]Request.cs` (if PUT/PATCH)

**Code**:
```csharp
public class CreateProductRequest
{
    [Required]
    [MaxLength(255)]
    public string Name { get; set; }

    [Range(0.01, double.MaxValue)]
    public decimal Price { get; set; }

    public string Description { get; set; }
}

public class ProductResponse
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public string Description { get; set; }
}
```

### Phase 3: Create Controller/Page (1-2 hours)

**For REST API**:
- `Controllers/[Resource]Controller.cs`

**For WebForms**:
- `Pages/[ResourceManagement].aspx`
- `Pages/[ResourceManagement].aspx.cs`

**Code Template (REST)**:
```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(
        IProductService productService,
        ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [HttpGet("{id}")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductResponse>> GetProduct(int id)
    {
        var product = await _productService.GetByIdAsync(id);
        if (product == null)
            return NotFound();

        return Ok(new ProductResponse { /* map */ });
    }

    [HttpPost]
    [Authorize]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<ProductResponse>> CreateProduct(
        [FromBody] CreateProductRequest request)
    {
        var product = await _productService.CreateAsync(
            new Product { Name = request.Name, Price = request.Price });

        return CreatedAtAction(nameof(GetProduct),
            new { id = product.Id },
            new ProductResponse { /* map */ });
    }
}
```

### Phase 4: Add Validation (30 minutes)

**Files**:
- `Validators/CreateProductValidator.cs`

**Code**:
```csharp
public class CreateProductValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(255);

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Price must be greater than 0");
    }
}
```

### Phase 5: Add Authorization (15 minutes)

**Configure**:
- Add `[Authorize]` attributes
- Add role-based access if needed: `[Authorize(Roles = "Admin")]`
- Document who can access

### Phase 6: Add Tests (1-2 hours)

**Files**:
- `Tests/Controllers/ProductsControllerTests.cs`

**Test Categories**:
- Happy path tests
- Validation failure tests
- Authorization tests
- Edge case tests

### Phase 7: Update Routes/Mappings (15 minutes)

**For WebForms**: Register in routing if needed
**For API**: Verify route attributes correct

### Phase 8: Add Documentation (30 minutes)

**Add**:
- XML comments for controller methods
- Swagger/OpenAPI annotations if using
- API documentation or README

### Phase 9: Integration Tests (1 hour)

**Files**:
- `Tests/Integration/ProductControllerIntegrationTests.cs`

**Test**:
- Full request/response cycle
- Database interactions
- Authorization checks

## File-Level Changes

| File | Action | Estimate |
|------|--------|----------|
| `Models/DTOs/Create[Resource]Request.cs` | Create | 15 min |
| `Models/DTOs/[Resource]Response.cs` | Create | 15 min |
| `Controllers/[Resource]Controller.cs` | Create | 60 min |
| `Validators/Create[Resource]Validator.cs` | Create | 20 min |
| `Program.cs` or `Startup.cs` | Modify | 10 min |
| `Tests/Controllers/[Resource]ControllerTests.cs` | Create | 60 min |
| `Tests/Integration/[Resource]IntegrationTests.cs` | Create | 60 min |

## Total Effort: 4-5 hours

## Success Criteria

- [ ] DTOs created and map correctly
- [ ] Endpoint returns correct status codes
- [ ] Validation rules enforced
- [ ] Authorization working
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Error handling in place

---

**Template Version**: 1.0.0
**Complexity**: Medium
**Estimated Time**: 4-5 hours
