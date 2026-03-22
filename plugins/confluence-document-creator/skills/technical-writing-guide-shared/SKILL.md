# Skill: Technical Writing Guide

## Overview

Technical writing is the art of communicating complex technical information clearly and concisely to specific audiences. This skill covers clear writing principles, documentation structure, code example guidelines, diagram best practices, audience considerations, and documentation maintenance strategies.

## When to Use This Skill

- **Writing API documentation**: Explaining how to use APIs
- **Creating user guides**: Helping users accomplish tasks
- **Documenting code**: Explaining complex algorithms or architectures
- **Writing release notes**: Communicating changes to users
- **Creating technical specifications**: Designing new features
- **Writing README files**: Introducing projects
- **Producing training materials**: Onboarding new team members
- **Authoring blog posts**: Sharing technical knowledge

## Clear Writing Principles

### Principle 1: Know Your Audience

**Questions to Ask**:
- Who will read this documentation?
- What is their technical level?
- What are they trying to accomplish?
- What do they already know?
- What context do they need?

**Audience Types**:

**Beginner Users**:
- Explain concepts from basics
- Avoid jargon or explain it
- Provide step-by-step instructions
- Include many examples
- Anticipate common mistakes

**Intermediate Users**:
- Assume basic knowledge
- Focus on best practices
- Provide rationale for recommendations
- Include optimization tips
- Link to advanced topics

**Expert Users**:
- Be concise and direct
- Focus on edge cases and gotchas
- Provide technical depth
- Include performance considerations
- Reference source code

**Example - Same Concept, Different Audiences**:

**For Beginners**:
```
A REST API is like a menu at a restaurant. The menu (API documentation)
lists what you can order (endpoints), what you need to provide (request
parameters), and what you'll get back (response). When you place an order
(make a request), the kitchen (server) prepares it and sends it back to you.

To use our API, you'll need an API key, which is like a membership card
that proves you're allowed to use our service.
```

**For Experts**:
```
This REST API follows standard HTTP conventions. Authentication uses
Bearer tokens in the Authorization header. Rate limiting is 1000 req/hour
per token. Responses use HAL+JSON with HATEOAS links for pagination.
```

### Principle 2: Be Concise

**Before (Wordy)**:
```
In order to be able to successfully install the application, you will need
to make sure that you have Node.js version 14 or a higher version installed
on your computer system. If you do not currently have Node.js installed,
you should visit the official Node.js website at nodejs.org and download
the installer that is appropriate for your operating system.
```

**After (Concise)**:
```
Prerequisites:
- Node.js 14 or higher

If Node.js isn't installed, download it from nodejs.org.
```

**Tips for Conciseness**:
- Remove filler words: "in order to", "be able to", "it should be noted"
- Use active voice: "Install the package" not "The package should be installed"
- Cut redundancy: "successfully install" → "install"
- Use lists instead of paragraphs
- One idea per sentence

### Principle 3: Use Active Voice

**Passive Voice (Weaker)**:
- "The file is read by the application"
- "An error will be thrown by the system"
- "The database should be backed up daily"

**Active Voice (Stronger)**:
- "The application reads the file"
- "The system throws an error"
- "Back up the database daily"

**When Passive is Acceptable**:
- When the actor is unknown: "The server was compromised"
- When the actor is irrelevant: "The data is encrypted"
- When you want to emphasize the object: "Your password must be changed"

### Principle 4: Be Specific

**Vague**:
```
The query might be slow with a lot of data. You should probably add
an index if performance is bad.
```

**Specific**:
```
This query performs a table scan, which is slow for tables with
> 100,000 rows. With 1 million rows, expect 5-10 second response times.

Add this index to reduce query time to < 100ms:
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
```

**Be Specific About**:
- Numbers: "< 100ms" not "fast"
- Versions: "Node.js 14+" not "recent version"
- Conditions: "When X > 1000" not "for large values"
- Time: "within 24 hours" not "soon"
- Quantities: "50 concurrent users" not "many users"

### Principle 5: Structure Information Logically

**Poor Structure**:
```
To deploy, run npm build. But first install dependencies with npm install.
Make sure Node.js is installed. Also, create a .env file. After deployment,
check the logs. You'll need access to the server. Set these environment
variables: API_KEY, DATABASE_URL.
```

**Good Structure**:
```
Prerequisites:
- Node.js 14+
- Server access (credentials in vault)

Setup:
1. Clone repository
2. Create .env file with:
   - API_KEY
   - DATABASE_URL
3. Install dependencies: npm install

Deployment:
1. Build: npm build
2. Deploy: npm run deploy
3. Verify: Check logs for errors

Post-Deployment:
- Monitor error rates
- Verify health checks passing
```

**Structural Elements**:
- **Prerequisites** before instructions
- **Steps** in chronological order
- **Examples** after explanations
- **Troubleshooting** at the end
- **Related topics** linked clearly

### Principle 6: Use Consistent Terminology

**Inconsistent**:
```
First, create a customer record. Then, add the user to the database.
Finally, update the client information.
```
(Are customer, user, and client the same thing?)

**Consistent**:
```
First, create a customer record. Then, add the customer to the database.
Finally, update the customer information.
```

**Terminology Best Practices**:
- Choose one term per concept
- Define technical terms on first use
- Maintain a glossary for complex domains
- Avoid synonyms for the same concept
- Use industry-standard terminology

## Documentation Structure

### README Structure

```markdown
# Project Name

Brief one-line description of what this project does.

## Overview
[2-3 paragraphs explaining purpose, key features, use cases]

## Quick Start
```bash
npm install
npm start
```

## Prerequisites
- Node.js 14+
- PostgreSQL 12+
- Redis 6+

## Installation
[Detailed setup instructions]

## Configuration
[Environment variables, config files]

## Usage
[Common usage examples]

## API Documentation
[Link to full API docs or brief inline reference]

## Development
[How to contribute, run tests, build]

## Troubleshooting
[Common issues and solutions]

## License
[License information]

## Support
[How to get help]
```

### API Documentation Structure

See **confluence-documentation-templates.md** for comprehensive API template

**Key Sections**:
1. Overview and authentication
2. Endpoint list with examples
3. Request/response formats
4. Error codes and handling
5. Rate limiting and quotas
6. Changelog and versioning

### User Guide Structure

```markdown
# Feature Name User Guide

## What is [Feature]?
[Brief explanation for non-technical users]

## When to Use [Feature]
[Use cases and scenarios]

## Getting Started
[Simplest possible example]

## Step-by-Step Guide
[Detailed instructions with screenshots]

## Advanced Features
[Power user features]

## FAQs
[Common questions]

## Troubleshooting
[Common problems]
```

## Code Example Guidelines

### Principle 1: Complete, Runnable Examples

**Bad Example (Incomplete)**:
```csharp
var result = ProcessOrder(order);
```
(What is `order`? Where does it come from? What type is `result`?)

**Good Example (Complete)**:
```csharp
// Create an order
var order = new Order
{
    CustomerId = 123,
    OrderDate = DateTime.Now,
    Items = new List<OrderItem>
    {
        new OrderItem { ProductId = 456, Quantity = 2, UnitPrice = 29.99m }
    }
};

// Process the order
var result = orderProcessor.ProcessOrder(order);

// Result is ProcessOrderResult with these properties:
// - OrderId: Unique identifier assigned
// - TotalAmount: Calculated total
// - ConfirmationNumber: Order confirmation code

Console.WriteLine($"Order {result.OrderId} created: {result.ConfirmationNumber}");
```

### Principle 2: Show Real-World Usage

**Toy Example (Not Helpful)**:
```csharp
// Calculate sum
int result = Add(2, 3);
```

**Real-World Example (Helpful)**:
```csharp
// Calculate order total including tax and shipping
var subtotal = order.Items.Sum(item => item.Quantity * item.UnitPrice);
var tax = subtotal * order.TaxRate;
var shipping = CalculateShipping(order.ShippingMethod, order.Weight);
var total = subtotal + tax + shipping;

order.TotalAmount = total;
```

### Principle 3: Annotate Complex Code

```csharp
// Good: Annotated complex algorithm
public List<Product> GetRecommendations(int customerId, int limit)
{
    // Get customer's purchase history
    var purchases = db.Orders
        .Where(o => o.CustomerId == customerId)
        .SelectMany(o => o.Items)
        .Select(i => i.ProductId)
        .Distinct()
        .ToList();

    // Find products frequently bought together (collaborative filtering)
    var recommendations = db.OrderItems
        .Where(item => purchases.Contains(item.ProductId)) // Orders with products customer bought
        .SelectMany(item => item.Order.Items)              // All items from those orders
        .Where(item => !purchases.Contains(item.ProductId)) // Exclude already purchased
        .GroupBy(item => item.ProductId)                   // Group by product
        .OrderByDescending(g => g.Count())                  // Sort by frequency
        .Take(limit)                                        // Limit results
        .Select(g => g.First().Product)                     // Get product details
        .ToList();

    return recommendations;
}
```

### Principle 4: Show Both Good and Bad Examples

```csharp
// ❌ BAD: No input validation
public void ProcessPayment(decimal amount)
{
    chargeCard(amount);
}

// ✅ GOOD: Proper validation
public void ProcessPayment(decimal amount)
{
    if (amount <= 0)
        throw new ArgumentException("Amount must be positive", nameof(amount));

    if (amount > 10000)
        throw new ArgumentException("Amount exceeds maximum allowed", nameof(amount));

    chargeCard(amount);
}
```

### Principle 5: Include Error Handling

```csharp
// Show how to handle errors properly
try
{
    var result = await apiClient.GetCustomerAsync(customerId);
    return result;
}
catch (NotFoundException ex)
{
    // Customer doesn't exist
    logger.LogWarning($"Customer {customerId} not found");
    return null;
}
catch (UnauthorizedException ex)
{
    // Invalid API credentials
    logger.LogError("API authentication failed", ex);
    throw;
}
catch (TimeoutException ex)
{
    // API request timed out
    logger.LogError("API timeout", ex);
    throw new ServiceUnavailableException("Customer service is temporarily unavailable", ex);
}
```

### Code Example Checklist

- [ ] Example is complete and runnable
- [ ] Variable names are descriptive
- [ ] Example shows real-world usage
- [ ] Complex logic has comments
- [ ] Includes error handling
- [ ] Shows both good and bad patterns
- [ ] Specifies required imports/dependencies
- [ ] Expected output is shown
- [ ] Edge cases are addressed

## Diagram Best Practices

### When to Use Diagrams

**Use Diagrams For**:
- System architecture (components and interactions)
- Data flow (how data moves through system)
- Process flow (step-by-step workflows)
- Database schema (tables and relationships)
- Sequence diagrams (API call flows)
- Class hierarchies (inheritance structures)

**Don't Use Diagrams For**:
- Simple lists (use bullet points)
- Linear steps (use numbered lists)
- Anything easily explained in text

### Diagram Types

**Architecture Diagram**:
```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│              │      │              │      │              │
│  React UI    │─────▶│  REST API    │─────▶│  PostgreSQL  │
│              │      │              │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
                             │
                             │
                             ▼
                      ┌──────────────┐
                      │              │
                      │  Redis Cache │
                      │              │
                      └──────────────┘

Legend:
→  HTTP/REST
▶  Database connection
```

**Data Flow Diagram**:
```
User Input
    │
    ▼
Validation
    │
    ├─(valid)──▶ Process
    │              │
    │              ▼
    │           Save to DB
    │              │
    │              ▼
    │           Return Success
    │
    └─(invalid)─▶ Return Error
```

**Sequence Diagram**:
```
Client          API             Database        Email Service
  │              │                 │                 │
  │─────────────▶│                 │                 │
  │ POST /orders │                 │                 │
  │              │────────────────▶│                 │
  │              │ INSERT order    │                 │
  │              │◀────────────────│                 │
  │              │ order_id        │                 │
  │              │─────────────────────────────────▶│
  │              │        Send confirmation          │
  │◀─────────────│                 │                 │
  │ 201 Created  │                 │                 │
```

### Diagram Guidelines

1. **Keep it simple**: Don't show every detail
2. **Use consistent notation**: Same shapes/arrows = same meaning
3. **Label everything**: No mystery boxes or arrows
4. **Include legend**: Explain symbols used
5. **Left-to-right flow**: Follows reading direction
6. **Limit complexity**: Max 7-10 boxes per diagram
7. **Use color sparingly**: Only to highlight important elements
8. **Make it readable**: Large enough font, good contrast

## Audience Consideration

### Writing for Different Audiences

**End Users (Non-Technical)**:
- Avoid technical jargon
- Use screenshots extensively
- Focus on "how" not "why"
- Step-by-step instructions
- Real-world scenarios
- FAQs for common questions

**Developers**:
- Include code examples
- Explain technical concepts
- Show architecture and design
- Link to source code
- API reference details
- Performance considerations

**DevOps/Operations**:
- Focus on deployment and configuration
- Include troubleshooting guides
- Monitoring and alerting setup
- Runbooks for common tasks
- Security considerations
- Disaster recovery procedures

**Management/Stakeholders**:
- High-level overview
- Business value and ROI
- Timeline and milestones
- Risks and mitigation
- Resource requirements
- Success metrics

### Adjusting Technical Depth

**Concept**: Database Index

**For End User**:
```
An index makes searching faster, like the index in a book helps you
find topics quickly without reading every page.
```

**For Developer**:
```
An index is a data structure that improves query performance by allowing
the database to quickly locate rows without scanning the entire table.
B-tree indexes provide O(log n) lookup time.

Example:
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);

This index allows:
WHERE CustomerId = 123  -- Fast: Index seek
Without index: Table scan of all rows
```

**For DBA**:
```
B-tree indexes provide O(log n) lookup with typical 67% page fill factor.
For a table with 1M rows:
- Without index: ~10,000 page reads (full scan)
- With index: ~3-4 page reads (root→branch→leaf)

Index maintenance:
- Fragmentation > 30% → Rebuild
- Update statistics after bulk inserts
- Monitor index usage (sys.dm_db_index_usage_stats)
- Consider filtered indexes for sparse predicates
```

## Documentation Maintenance

### Version Control Documentation

**Best Practices**:
- Store docs with code in same repository
- Review documentation changes in PRs
- Require documentation updates for API changes
- Tag documentation versions with releases
- Keep changelog for documentation

**Example Structure**:
```
/docs
  /api
    /v1
      endpoints.md
    /v2
      endpoints.md
  /guides
    getting-started.md
    advanced-features.md
  /architecture
    system-overview.md
  CHANGELOG.md
```

### Keeping Documentation Current

**Update Triggers**:
- Code changes that affect public APIs
- New features added
- Bugs fixed that had unclear documentation
- User feedback about confusion
- Version releases

**Review Cadence**:
- **Critical docs** (API, getting started): Review every sprint
- **General docs**: Review quarterly
- **Archived docs**: Review annually for retirement

**Documentation Debt**:
- Track outdated documentation like technical debt
- Tag with `[OUTDATED]` if not immediately fixable
- Include documentation tasks in sprint planning
- Assign documentation ownership

### Documentation Quality Metrics

**Measurable Quality Indicators**:
- **Support ticket reduction**: Good docs → fewer questions
- **Time to first contribution**: New developer productivity
- **User satisfaction**: Survey users about documentation
- **Search success rate**: Can users find what they need?
- **Page views**: Are docs being used?
- **Feedback**: Comments, ratings on documentation pages

## Common Technical Writing Mistakes

### Mistake 1: Assuming Knowledge

**Bad**:
```
Configure the JWT middleware in the OWIN pipeline with the appropriate
signing credentials and validation parameters.
```

**Good**:
```
Add JWT authentication to your application:

1. Install package:
   dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer

2. In Startup.cs, add:
   services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
       .AddJwtBearer(options => {
           options.TokenValidationParameters = new TokenValidationParameters
           {
               ValidateIssuer = true,
               ValidIssuer = "https://your-domain.com",
               ValidateAudience = true,
               ValidAudience = "your-api",
               ValidateIssuerSigningKey = true,
               IssuerSigningKey = new SymmetricSecurityKey(
                   Encoding.UTF8.GetBytes(Configuration["Jwt:Key"]))
           };
       });
```

### Mistake 2: Missing Context

**Bad**:
```
Run: kubectl apply -f deployment.yaml
```

**Good**:
```
Deploy the application to Kubernetes:

Prerequisites:
- kubectl installed and configured
- Access to cluster (verify: kubectl cluster-info)
- deployment.yaml in current directory

Deploy:
kubectl apply -f deployment.yaml

Verify:
kubectl get pods
kubectl logs deployment/your-app

Expected output: Pod status should be "Running"
```

### Mistake 3: Vague Instructions

**Bad**:
```
Configure the application appropriately for your environment.
```

**Good**:
```
Configure the application by editing appsettings.json:

{
  "Database": {
    "ConnectionString": "Server=localhost;Database=myapp;User=sa;Password=****"
  },
  "Api": {
    "BaseUrl": "https://api.example.com",
    "Timeout": 30
  }
}

Required settings:
- Database.ConnectionString: Your SQL Server connection string
- Api.BaseUrl: External API endpoint

Optional settings:
- Api.Timeout: Request timeout in seconds (default: 30)
```

### Mistake 4: No Examples

**Bad**:
```
The search API supports filtering by multiple criteria using query parameters.
```

**Good**:
```
The search API supports filtering by multiple criteria:

Basic search:
GET /api/products?name=laptop

Multiple filters:
GET /api/products?category=electronics&minPrice=500&maxPrice=1000

Supported filters:
- name: Product name (partial match)
- category: Product category (exact match)
- minPrice: Minimum price (inclusive)
- maxPrice: Maximum price (inclusive)
- inStock: true/false

Example response:
{
  "products": [
    {"id": 1, "name": "Laptop Pro", "price": 899.99, "category": "electronics"}
  ],
  "totalCount": 1,
  "page": 1
}
```

## Technical Writing Checklist

**Before Publishing**:
- [ ] Clear purpose and audience identified
- [ ] Logical structure with clear sections
- [ ] Active voice used (most of the time)
- [ ] Concise writing (no fluff)
- [ ] Consistent terminology
- [ ] Specific, not vague
- [ ] Complete, runnable code examples
- [ ] Error handling shown
- [ ] Diagrams are clear and labeled
- [ ] Screenshots are current and annotated
- [ ] Prerequisites listed
- [ ] Expected outcomes described
- [ ] Troubleshooting section included
- [ ] Spelling and grammar checked
- [ ] Links tested and working
- [ ] Reviewed by someone else
- [ ] Version/date included

## Key Takeaways

1. **Know your audience**: Write at the appropriate technical level
2. **Be concise**: Every word should add value
3. **Use active voice**: Stronger and clearer than passive
4. **Show, don't just tell**: Include complete, real-world examples
5. **Structure logically**: Prerequisites → Instructions → Examples → Troubleshooting
6. **Be specific**: Numbers, versions, conditions, not vague descriptions
7. **Maintain consistency**: Terminology, formatting, structure
8. **Use visuals wisely**: Diagrams for complexity, screenshots for UI
9. **Keep it current**: Documentation rots quickly if not maintained
10. **Test your documentation**: Have someone else follow your instructions

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Documentation & Communication
