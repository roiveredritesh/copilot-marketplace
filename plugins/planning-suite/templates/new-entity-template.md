---
template-name: new-entity
description: Template for planning creation of new entity with repository and service layers
applies-to: [entity-creation, feature-with-data-model]
required-inputs: [entity-name, key-properties, business-rules]
---

# Template: New Entity Planning

## When to Use
Use this template when you need to create a new entity (data model) with full CRUD operations, repository layer, and service layer.

**Examples**:
- Add a new `Product` entity to your system
- Create `CustomerSegment` model with data persistence
- Implement new `Invoice` entity with business rules

## Required Inputs

1. **Entity Name**: What is the entity called? (e.g., "Product", "Order", "Customer")
2. **Key Properties**: What properties does it have? (e.g., id, name, price, description)
3. **Business Rules**: What rules apply? (e.g., "price must be > 0", "name is required")
4. **Related Entities**: Does it relate to other entities? (e.g., "Product belongs to Category")

## Planning Structure

### Phase 1: Database Design (1-2 hours)

**Create**: Migration file to add table
**Files**:
- `Migrations/00X_Add[EntityName]Table.cs`

**Steps**:
1. Create migration class
2. Define table columns
3. Add primary key
4. Add foreign keys if needed
5. Add indexes if needed
6. Create down() method for rollback

**Code Template**:
```csharp
public partial class Add[EntityName]Table : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "[EntityName]",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:ValueGenerationStrategy",
                        SqlServerValueGenerationStrategy.IdentityColumn),
                Name = table.Column<string>(maxLength: 255, nullable: false),
                // Add other properties
                CreatedAt = table.Column<DateTime>(nullable: false),
                UpdatedAt = table.Column<DateTime>(nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_[EntityName]", x => x.Id);
                // Add foreign keys here if needed
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "[EntityName]");
    }
}
```

### Phase 2: Create Model Class (30 minutes)

**Create**: Entity model class
**Files**:
- `Models/[EntityName].cs`

**Code Template**:
```csharp
namespace MyApp.Models
{
    public class [EntityName]
    {
        public int Id { get; set; }
        public string Name { get; set; }
        // Add other properties
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }

        // Navigation properties if needed
        // public ICollection<[RelatedEntity]> [RelatedEntities] { get; set; }
    }
}
```

### Phase 3: Create Repository Interface (30 minutes)

**Create**: Repository interface
**Files**:
- `Data/Repositories/I[EntityName]Repository.cs`

**Code Template**:
```csharp
namespace MyApp.Data.Repositories
{
    public interface I[EntityName]Repository
    {
        Task<[EntityName]> GetByIdAsync(int id);
        Task<IEnumerable<[EntityName]>> GetAllAsync();
        Task<[EntityName]> CreateAsync([EntityName] entity);
        Task<[EntityName]> UpdateAsync([EntityName] entity);
        Task DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
    }
}
```

### Phase 4: Create Repository Implementation (1 hour)

**Create**: Repository implementation
**Files**:
- `Data/Repositories/[EntityName]Repository.cs`

**Code Template**:
```csharp
namespace MyApp.Data.Repositories
{
    public class [EntityName]Repository : I[EntityName]Repository
    {
        private readonly IApplicationDbContext _context;
        private readonly ILogger<[EntityName]Repository> _logger;

        public [EntityName]Repository(
            IApplicationDbContext context,
            ILogger<[EntityName]Repository> logger)
        {
            _context = context ?? throw new ArgumentNullException(nameof(context));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        public async Task<[EntityName]> GetByIdAsync(int id)
        {
            return await _context.[EntityNames]
                .AsNoTracking()
                .FirstOrDefaultAsync(x => x.Id == id);
        }

        public async Task<IEnumerable<[EntityName]>> GetAllAsync()
        {
            return await _context.[EntityNames]
                .AsNoTracking()
                .ToListAsync();
        }

        // Implement other methods...
    }
}
```

### Phase 5: Create Service Interface (30 minutes)

**Create**: Service interface
**Files**:
- `Services/I[EntityName]Service.cs`

**Code Template**:
```csharp
namespace MyApp.Services
{
    public interface I[EntityName]Service
    {
        Task<[EntityName]> GetByIdAsync(int id);
        Task<IEnumerable<[EntityName]>> GetAllAsync();
        Task<[EntityName]> CreateAsync([EntityName] entity);
        Task<[EntityName]> UpdateAsync([EntityName] entity);
        Task DeleteAsync(int id);
    }
}
```

### Phase 6: Create Service Implementation (1-2 hours)

**Create**: Service implementation with business logic
**Files**:
- `Services/[EntityName]Service.cs`

**Code Template**:
```csharp
namespace MyApp.Services
{
    public class [EntityName]Service : I[EntityName]Service
    {
        private readonly I[EntityName]Repository _repository;
        private readonly ILogger<[EntityName]Service> _logger;

        public [EntityName]Service(
            I[EntityName]Repository repository,
            ILogger<[EntityName]Service> logger)
        {
            _repository = repository ?? throw new ArgumentNullException(nameof(repository));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        public async Task<[EntityName]> GetByIdAsync(int id)
        {
            if (id <= 0)
                throw new ArgumentException("Id must be greater than 0", nameof(id));

            return await _repository.GetByIdAsync(id);
        }

        public async Task<[EntityName]> CreateAsync([EntityName] entity)
        {
            // Validate business rules
            ValidateEntity(entity);

            // Create
            var created = await _repository.CreateAsync(entity);
            _logger.LogInformation($"Created [EntityName] with Id: {created.Id}");
            return created;
        }

        private void ValidateEntity([EntityName] entity)
        {
            if (string.IsNullOrWhiteSpace(entity.Name))
                throw new ValidationException("Name is required");

            // Add other business rule validations
        }

        // Implement other methods...
    }
}
```

### Phase 7: Register in Dependency Injection (15 minutes)

**Modify**: DI/Service configuration
**Files**:
- `Configuration/ServiceConfiguration.cs` or `Startup.cs`

**Code Template**:
```csharp
public static void Configure Services(IServiceCollection services)
{
    // Add repository
    services.AddScoped<I[EntityName]Repository, [EntityName]Repository>();

    // Add service
    services.AddScoped<I[EntityName]Service, [EntityName]Service>();
}
```

### Phase 8: Create Unit Tests (1-2 hours)

**Create**: Unit tests for repository and service
**Files**:
- `Tests/[EntityName]RepositoryTests.cs`
- `Tests/[EntityName]ServiceTests.cs`

**Test Template**:
```csharp
public class [EntityName]RepositoryTests
{
    [Test]
    public async Task GetByIdAsync_ValidId_Returns[EntityName]()
    {
        // Arrange
        var mockContext = new Mock<IApplicationDbContext>();
        var repo = new [EntityName]Repository(mockContext.Object, Mock.Of<ILogger>());

        // Act
        var result = await repo.GetByIdAsync(1);

        // Assert
        Assert.NotNull(result);
    }

    [Test]
    public async Task CreateAsync_ValidEntity_Returns CreatedEntity()
    {
        // Arrange, Act, Assert...
    }
}
```

### Phase 9: Update DbContext (15 minutes)

**Modify**: DbContext to include new entity
**Files**:
- `Data/ApplicationDbContext.cs`

**Code Template**:
```csharp
public DbSet<[EntityName]> [EntityNames] { get; set; }

protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // Configure entity
    modelBuilder.Entity<[EntityName]>(entity =>
    {
        entity.HasKey(e => e.Id);
        entity.Property(e => e.Name).HasMaxLength(255).IsRequired();
        // Add other configurations
    });
}
```

### Phase 10: Integration Tests (1-2 hours)

**Create**: Integration tests
**Files**:
- `Tests/Integration/[EntityName]IntegrationTests.cs`

## File-Level Changes Summary

| File | Action | Type | Estimate |
|------|--------|------|----------|
| `Migrations/00X_Add[EntityName]Table.cs` | Create | C# | 30 min |
| `Models/[EntityName].cs` | Create | C# | 15 min |
| `Data/I[EntityName]Repository.cs` | Create | C# | 15 min |
| `Data/[EntityName]Repository.cs` | Create | C# | 45 min |
| `Services/I[EntityName]Service.cs` | Create | C# | 15 min |
| `Services/[EntityName]Service.cs` | Create | C# | 60 min |
| `Configuration/ServiceConfiguration.cs` | Modify | C# | 10 min |
| `Data/ApplicationDbContext.cs` | Modify | C# | 15 min |
| `Tests/[EntityName]RepositoryTests.cs` | Create | C# | 60 min |
| `Tests/[EntityName]ServiceTests.cs` | Create | C# | 60 min |
| `Tests/Integration/[EntityName]IntegrationTests.cs` | Create | C# | 90 min |

## Total Effort: 5-6 hours

## Success Criteria

- [ ] Database migration runs successfully
- [ ] Entity created with all properties
- [ ] Repository CRUD operations work
- [ ] Service validates business rules
- [ ] DI registration complete
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] No errors in logs
- [ ] Code review approved

## Testing Checklist

- [ ] Repository GetByIdAsync works
- [ ] Repository GetAllAsync returns all entities
- [ ] Repository CreateAsync creates entity
- [ ] Repository UpdateAsync updates entity
- [ ] Repository DeleteAsync removes entity
- [ ] Service validates required fields
- [ ] Service enforces business rules
- [ ] Integration test end-to-end

---

**Template Version**: 1.0.0
**Complexity**: Medium
**Best For**: CRUD entities with business logic
**Estimated Time**: 5-6 hours including testing
