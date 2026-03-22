# Skill: Database Schema Analysis

## Overview

Database schema analysis is the systematic evaluation of database structure, relationships, normalization, and design patterns. This skill covers schema design principles, normalization forms, relationship modeling, data type selection, and schema evolution strategies to ensure maintainable, performant, and scalable database architectures.

## When to Use This Skill

- **Designing new database schemas**: Creating tables and relationships from requirements
- **Analyzing existing schemas**: Understanding legacy database structures
- **Performance troubleshooting**: Schema design causing performance issues
- **Database refactoring**: Improving schema design without losing data
- **Schema migrations**: Evolving schema to support new features
- **Code review**: Evaluating proposed schema changes
- **Normalization assessment**: Determining appropriate normalization level
- **Data integrity issues**: Missing constraints, orphaned records

## Database Normalization

### Why Normalization Matters

**Benefits**:
- Reduces data redundancy
- Prevents update anomalies
- Ensures data consistency
- Simplifies maintenance
- Improves data integrity

**Trade-offs**:
- More tables = more JOINs
- Can impact query performance
- More complex queries
- Sometimes denormalization is appropriate

### First Normal Form (1NF)

**Requirements**:
1. Each column contains atomic (indivisible) values
2. Each row is unique (has primary key)
3. No repeating groups or arrays

**Violation Example**:
```sql
-- BAD: Multiple phones in one column
CREATE TABLE Customers (
    CustomerId INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    PhoneNumbers VARCHAR(500) -- "555-1234, 555-5678, 555-9012"
);
```

**1NF Compliant**:
```sql
-- GOOD: Separate table for phone numbers
CREATE TABLE Customers (
    CustomerId INT PRIMARY KEY,
    CustomerName VARCHAR(100)
);

CREATE TABLE CustomerPhones (
    PhoneId INT PRIMARY KEY,
    CustomerId INT FOREIGN KEY REFERENCES Customers(CustomerId),
    PhoneNumber VARCHAR(20),
    PhoneType VARCHAR(20) -- 'Mobile', 'Home', 'Work'
);
```

### Second Normal Form (2NF)

**Requirements**:
1. Must be in 1NF
2. No partial dependencies on composite key
3. All non-key columns depend on entire primary key

**Violation Example**:
```sql
-- BAD: Composite key (OrderId, ProductId), but ProductName only depends on ProductId
CREATE TABLE OrderDetails (
    OrderId INT,
    ProductId INT,
    ProductName VARCHAR(100), -- Depends only on ProductId, not OrderId!
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    PRIMARY KEY (OrderId, ProductId)
);
```

**2NF Compliant**:
```sql
-- GOOD: ProductName moved to Products table
CREATE TABLE Products (
    ProductId INT PRIMARY KEY,
    ProductName VARCHAR(100)
);

CREATE TABLE OrderDetails (
    OrderId INT,
    ProductId INT FOREIGN KEY REFERENCES Products(ProductId),
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    PRIMARY KEY (OrderId, ProductId)
);
```

### Third Normal Form (3NF)

**Requirements**:
1. Must be in 2NF
2. No transitive dependencies
3. Non-key columns depend only on primary key, not on other non-key columns

**Violation Example**:
```sql
-- BAD: ShippingCost depends on ShippingMethod, not OrderId
CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT,
    OrderDate DATETIME,
    ShippingMethod VARCHAR(50), -- 'Standard', 'Express', 'Overnight'
    ShippingCost DECIMAL(10,2)  -- Depends on ShippingMethod!
);
```

**3NF Compliant**:
```sql
-- GOOD: ShippingCost moved to ShippingMethods table
CREATE TABLE ShippingMethods (
    ShippingMethodId INT PRIMARY KEY,
    MethodName VARCHAR(50),
    Cost DECIMAL(10,2)
);

CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT,
    OrderDate DATETIME,
    ShippingMethodId INT FOREIGN KEY REFERENCES ShippingMethods(ShippingMethodId)
);
```

### Boyce-Codd Normal Form (BCNF)

**Requirements**:
1. Must be in 3NF
2. For every functional dependency X → Y, X must be a superkey

**Violation Example**:
```sql
-- BAD: CourseId, InstructorId is candidate key
-- But InstructorId → Department (instructor determines department)
-- InstructorId is not a superkey
CREATE TABLE CourseInstructors (
    CourseId INT,
    InstructorId INT,
    Department VARCHAR(50), -- Depends on InstructorId
    PRIMARY KEY (CourseId, InstructorId)
);
```

**BCNF Compliant**:
```sql
-- GOOD: Department moved to Instructors table
CREATE TABLE Instructors (
    InstructorId INT PRIMARY KEY,
    InstructorName VARCHAR(100),
    Department VARCHAR(50)
);

CREATE TABLE CourseInstructors (
    CourseId INT,
    InstructorId INT FOREIGN KEY REFERENCES Instructors(InstructorId),
    PRIMARY KEY (CourseId, InstructorId)
);
```

### Fourth Normal Form (4NF)

**Requirements**:
1. Must be in BCNF
2. No multi-valued dependencies
3. No independent many-to-many relationships in same table

**Violation Example**:
```sql
-- BAD: Student has multiple phones AND multiple addresses
-- These are independent multi-valued facts
CREATE TABLE StudentContact (
    StudentId INT,
    PhoneNumber VARCHAR(20),
    Address VARCHAR(200),
    PRIMARY KEY (StudentId, PhoneNumber, Address)
);

-- Problem: To add new phone, must duplicate all addresses
-- To add new address, must duplicate all phones
```

**4NF Compliant**:
```sql
-- GOOD: Separate tables for independent multi-valued facts
CREATE TABLE StudentPhones (
    StudentId INT,
    PhoneNumber VARCHAR(20),
    PRIMARY KEY (StudentId, PhoneNumber)
);

CREATE TABLE StudentAddresses (
    StudentId INT,
    Address VARCHAR(200),
    PRIMARY KEY (StudentId, Address)
);
```

### Fifth Normal Form (5NF)

**Requirements**:
1. Must be in 4NF
2. No join dependencies
3. Cannot be decomposed further without losing information

**Violation Example**:
```sql
-- BAD: Three-way relationship with join dependency
CREATE TABLE SupplierProductStore (
    SupplierId INT,
    ProductId INT,
    StoreId INT,
    PRIMARY KEY (SupplierId, ProductId, StoreId)
);

-- If Supplier S1 supplies Product P1
-- And Product P1 is sold at Store ST1
-- And Supplier S1 supplies to Store ST1
-- Then (S1, P1, ST1) must exist
```

**5NF Compliant**:
```sql
-- GOOD: Decompose into binary relationships
CREATE TABLE SupplierProducts (
    SupplierId INT,
    ProductId INT,
    PRIMARY KEY (SupplierId, ProductId)
);

CREATE TABLE ProductStores (
    ProductId INT,
    StoreId INT,
    PRIMARY KEY (ProductId, StoreId)
);

CREATE TABLE SupplierStores (
    SupplierId INT,
    StoreId INT,
    PRIMARY KEY (SupplierId, StoreId)
);
```

**Note**: 5NF is rarely used in practice. Most schemas stop at 3NF/BCNF.

## Strategic Denormalization

### When to Denormalize

Denormalization can be appropriate for:
- **Read-heavy workloads**: Far more reads than writes
- **Performance critical queries**: Joining many tables is too slow
- **Aggregated data**: Pre-calculated summaries
- **Historical snapshots**: Data that should not change
- **Reporting databases**: Separate from transactional database

### Denormalization Patterns

**Pattern 1: Calculated Columns**

```sql
-- Normalized (3NF)
CREATE TABLE OrderDetails (
    OrderDetailId INT PRIMARY KEY,
    OrderId INT,
    ProductId INT,
    Quantity INT,
    UnitPrice DECIMAL(10,2)
);

-- Query requires calculation
SELECT OrderId, SUM(Quantity * UnitPrice) as OrderTotal
FROM OrderDetails
GROUP BY OrderId;
```

**Denormalized**:
```sql
CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT,
    OrderDate DATETIME,
    OrderTotal DECIMAL(10,2) -- Denormalized calculated field
);

CREATE TABLE OrderDetails (
    OrderDetailId INT PRIMARY KEY,
    OrderId INT,
    ProductId INT,
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    LineTotal AS (Quantity * UnitPrice) PERSISTED -- Computed column
);

-- Trigger to update OrderTotal
CREATE TRIGGER trg_UpdateOrderTotal
ON OrderDetails
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    UPDATE Orders
    SET OrderTotal = (
        SELECT SUM(Quantity * UnitPrice)
        FROM OrderDetails
        WHERE OrderId = Orders.OrderId
    )
    WHERE OrderId IN (
        SELECT OrderId FROM inserted
        UNION
        SELECT OrderId FROM deleted
    );
END;
```

**Trade-offs**:
- **Pros**: Faster reads (no calculation needed)
- **Cons**: More complex writes, potential inconsistency, more storage

**Pattern 2: Lookup Value Denormalization**

```sql
-- Normalized
CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT FOREIGN KEY REFERENCES Customers(CustomerId),
    OrderDate DATETIME
);

-- Every query needs JOIN to get customer name
SELECT o.OrderId, c.CustomerName
FROM Orders o
INNER JOIN Customers c ON o.CustomerId = c.CustomerId;
```

**Denormalized**:
```sql
CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT FOREIGN KEY REFERENCES Customers(CustomerId),
    CustomerName VARCHAR(100), -- Denormalized for faster reads
    OrderDate DATETIME
);

-- No JOIN needed for common queries
SELECT OrderId, CustomerName FROM Orders;
```

**When appropriate**:
- Customer name rarely changes
- Reading orders is very frequent
- Join performance is critical

**Pattern 3: Historical Snapshot**

```sql
-- Normalized: Current price in Products table
CREATE TABLE Products (
    ProductId INT PRIMARY KEY,
    ProductName VARCHAR(100),
    CurrentPrice DECIMAL(10,2)
);

CREATE TABLE OrderDetails (
    OrderDetailId INT PRIMARY KEY,
    OrderId INT,
    ProductId INT FOREIGN KEY REFERENCES Products(ProductId),
    Quantity INT
    -- How to track price at time of order?
);
```

**Denormalized (Correct)**:
```sql
CREATE TABLE OrderDetails (
    OrderDetailId INT PRIMARY KEY,
    OrderId INT,
    ProductId INT,
    ProductName VARCHAR(100),  -- Snapshot of name
    UnitPrice DECIMAL(10,2),   -- Snapshot of price at order time
    Quantity INT
);
```

**Why necessary**: Historical data should not change when current product price changes.

## Relationship Modeling

### One-to-One Relationships

**Implementation**:
```sql
-- Option 1: Separate tables with FK
CREATE TABLE Users (
    UserId INT PRIMARY KEY,
    Username VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE UserProfiles (
    UserId INT PRIMARY KEY FOREIGN KEY REFERENCES Users(UserId),
    Bio TEXT,
    AvatarUrl VARCHAR(500),
    DateOfBirth DATE
);

-- Option 2: Single table (if always together)
CREATE TABLE Users (
    UserId INT PRIMARY KEY,
    Username VARCHAR(50),
    Email VARCHAR(100),
    Bio TEXT,
    AvatarUrl VARCHAR(500),
    DateOfBirth DATE
);
```

**When to use separate tables**:
- Optional relationship (not all users have profile)
- Large columns (TEXT, BLOB) that slow down main table scans
- Different security requirements
- Frequently updated vs rarely updated data

### One-to-Many Relationships

**Implementation**:
```sql
-- Foreign key in "many" table
CREATE TABLE Customers (
    CustomerId INT PRIMARY KEY,
    CustomerName VARCHAR(100)
);

CREATE TABLE Orders (
    OrderId INT PRIMARY KEY,
    CustomerId INT FOREIGN KEY REFERENCES Customers(CustomerId),
    OrderDate DATETIME
);
```

**Best Practices**:
- Always add foreign key constraint (data integrity)
- Index foreign key column (join performance)
- Consider ON DELETE behavior (CASCADE, SET NULL, NO ACTION)

```sql
-- Example with cascade options
ALTER TABLE Orders
ADD CONSTRAINT FK_Orders_Customers
FOREIGN KEY (CustomerId)
REFERENCES Customers(CustomerId)
ON DELETE CASCADE      -- Delete orders when customer deleted
ON UPDATE CASCADE;     -- Update orders when customer ID changes
```

### Many-to-Many Relationships

**Implementation**:
```sql
-- Junction/Bridge table
CREATE TABLE Students (
    StudentId INT PRIMARY KEY,
    StudentName VARCHAR(100)
);

CREATE TABLE Courses (
    CourseId INT PRIMARY KEY,
    CourseName VARCHAR(100)
);

CREATE TABLE StudentCourses (
    StudentId INT FOREIGN KEY REFERENCES Students(StudentId),
    CourseId INT FOREIGN KEY REFERENCES Courses(CourseId),
    EnrollmentDate DATE,
    Grade VARCHAR(2),
    PRIMARY KEY (StudentId, CourseId)
);
```

**Best Practices**:
- Composite primary key on both FKs
- Index both foreign keys
- Can add additional attributes to junction table
- Name junction table descriptively (StudentCourses, OrderProducts)

### Self-Referencing Relationships

**Implementation**:
```sql
-- Hierarchical data (employees and managers)
CREATE TABLE Employees (
    EmployeeId INT PRIMARY KEY,
    EmployeeName VARCHAR(100),
    ManagerId INT FOREIGN KEY REFERENCES Employees(EmployeeId)
);

-- Example data
-- John (ID: 1, ManagerId: NULL) - CEO
-- Jane (ID: 2, ManagerId: 1)    - Reports to John
-- Bob  (ID: 3, ManagerId: 2)    - Reports to Jane
```

**Querying Hierarchies**:
```sql
-- Recursive CTE to get organization hierarchy
WITH EmployeeHierarchy AS (
    -- Anchor: Top level (CEO)
    SELECT EmployeeId, EmployeeName, ManagerId, 0 as Level
    FROM Employees
    WHERE ManagerId IS NULL

    UNION ALL

    -- Recursive: Employees reporting to previous level
    SELECT e.EmployeeId, e.EmployeeName, e.ManagerId, eh.Level + 1
    FROM Employees e
    INNER JOIN EmployeeHierarchy eh ON e.ManagerId = eh.EmployeeId
)
SELECT * FROM EmployeeHierarchy
ORDER BY Level, EmployeeName;
```

## Data Type Selection

### Choosing Appropriate Data Types

**Integer Types**:
```sql
TINYINT     -- 0 to 255 (1 byte) - Use for small enums, flags
SMALLINT    -- -32,768 to 32,767 (2 bytes) - Rare use
INT         -- -2B to 2B (4 bytes) - Standard integer
BIGINT      -- Large numbers (8 bytes) - IDs for huge tables
```

**Guideline**: Use smallest type that fits your data range

**String Types**:
```sql
CHAR(n)        -- Fixed length - Use for fixed codes (country codes, status)
VARCHAR(n)     -- Variable length - Most common string type
VARCHAR(MAX)   -- Up to 2GB - Use sparingly (performance impact)
NCHAR(n)       -- Unicode fixed - For international characters
NVARCHAR(n)    -- Unicode variable - For international text
NVARCHAR(MAX)  -- Unicode large - Use sparingly
```

**Best Practices**:
```sql
-- GOOD: Appropriate sizing
CustomerName NVARCHAR(100)    -- Names can be international
Email VARCHAR(254)            -- Max valid email length
CountryCode CHAR(2)           -- ISO 2-letter codes (US, UK, CA)
Description NVARCHAR(500)     -- Reasonable limit
LongText NVARCHAR(MAX)        -- Only when truly needed

-- BAD: Over-sizing
CustomerName NVARCHAR(MAX)    -- Wastes space, hurts performance
Email VARCHAR(1000)           -- Unnecessary size
```

**Decimal Types**:
```sql
DECIMAL(p, s)  -- Exact numeric - ALWAYS use for money
FLOAT          -- Approximate - Scientific calculations only
REAL           -- Approximate - Rare use
MONEY          -- Money (avoid - use DECIMAL instead)
```

**Money Fields**:
```sql
-- GOOD: Use DECIMAL for money
UnitPrice DECIMAL(10, 2)  -- 10 digits, 2 decimal places
                           -- Max: 99,999,999.99

-- Why not FLOAT?
-- FLOAT: 0.1 + 0.2 = 0.30000000000000004 (rounding errors)
-- DECIMAL: 0.1 + 0.2 = 0.3 (exact)
```

**Date/Time Types**:
```sql
DATE           -- Date only (2025-01-15)
TIME           -- Time only (14:30:00)
DATETIME       -- Date and time (legacy, less precise)
DATETIME2      -- Date and time (more precise, preferred)
DATETIMEOFFSET -- Date, time, timezone offset
```

**Best Practice**:
```sql
-- Use DATETIME2 for new development
CreatedDate DATETIME2(0)        -- No fractional seconds
UpdatedDate DATETIME2(3)        -- Millisecond precision
PreciseTimestamp DATETIME2(7)   -- Full precision

-- Use DATETIMEOFFSET for global applications
EventTime DATETIMEOFFSET(0)     -- Includes timezone
```

**Boolean/Bit**:
```sql
BIT            -- True/False, 0/1
IsActive BIT DEFAULT 1
IsDeleted BIT DEFAULT 0
```

**GUID/Uniqueidentifier**:
```sql
UNIQUEIDENTIFIER  -- Globally unique identifier

-- Pros: Globally unique, good for distributed systems, merge scenarios
-- Cons: Larger (16 bytes), random (poor clustering), slower lookups than INT

-- Use when:
-- - Distributed systems generating IDs independently
-- - External system integration
-- - Security (non-sequential IDs)

-- Avoid when:
-- - Simple single-database application
-- - Performance critical (INT is faster)
```

### Data Type Anti-Patterns

**Anti-Pattern 1: VARCHAR(MAX) Everywhere**
```sql
-- BAD
CustomerName VARCHAR(MAX)
Email VARCHAR(MAX)
PhoneNumber VARCHAR(MAX)

-- GOOD
CustomerName NVARCHAR(100)
Email VARCHAR(254)
PhoneNumber VARCHAR(20)
```

**Why bad**: Affects indexing, sorting, performance

**Anti-Pattern 2: Storing Dates as Strings**
```sql
-- BAD
OrderDate VARCHAR(50)  -- '2025-01-15' or '01/15/2025' or '15-Jan-2025'

-- GOOD
OrderDate DATETIME2(0)
```

**Why bad**: No date validation, cannot sort properly, cannot use date functions

**Anti-Pattern 3: Storing Multiple Values in One Column**
```sql
-- BAD
Tags VARCHAR(500)  -- 'electronics,computers,laptops,dell'

-- GOOD - Separate table
CREATE TABLE ProductTags (
    ProductId INT,
    Tag VARCHAR(50),
    PRIMARY KEY (ProductId, Tag)
);
```

## Schema Migration Strategies

### Versioning Approach

**Database Schema Version Table**:
```sql
CREATE TABLE SchemaVersion (
    Version INT PRIMARY KEY,
    AppliedDate DATETIME2 DEFAULT GETDATE(),
    Description VARCHAR(500)
);
```

### Migration Types

**Type 1: Additive Changes (Safe)**
```sql
-- Adding nullable column
ALTER TABLE Customers
ADD PhoneNumber VARCHAR(20) NULL;

-- Adding table
CREATE TABLE CustomerPreferences (
    CustomerId INT PRIMARY KEY,
    EmailNotifications BIT DEFAULT 1
);

-- Adding index
CREATE INDEX IX_Orders_OrderDate ON Orders(OrderDate);
```

**Type 2: Breaking Changes (Risky)**
```sql
-- Renaming column (breaks existing code)
EXEC sp_rename 'Customers.CustomerName', 'FullName', 'COLUMN';

-- Changing data type (may lose data)
ALTER TABLE Orders
ALTER COLUMN OrderTotal DECIMAL(12,2);  -- Was DECIMAL(10,2)

-- Dropping column (data loss)
ALTER TABLE Customers
DROP COLUMN OldColumn;
```

### Safe Migration Pattern

**Three-Phase Migration**:

**Phase 1: Add New Structure (Additive)**
```sql
-- Add new column (nullable)
ALTER TABLE Customers
ADD FullName NVARCHAR(200) NULL;

-- Populate from old columns
UPDATE Customers
SET FullName = FirstName + ' ' + LastName;
```

**Phase 2: Transition Period**
- Deploy code that writes to both old and new columns
- Verify new column working correctly
- Monitor for issues

**Phase 3: Remove Old Structure**
```sql
-- Make new column NOT NULL
ALTER TABLE Customers
ALTER COLUMN FullName NVARCHAR(200) NOT NULL;

-- Drop old columns
ALTER TABLE Customers
DROP COLUMN FirstName, LastName;
```

### Rollback Strategy

```sql
-- Always script rollback before migration
-- Migration (up):
ALTER TABLE Orders ADD ShippingCost DECIMAL(10,2) NULL;

-- Rollback (down):
ALTER TABLE Orders DROP COLUMN ShippingCost;
```

## Schema Analysis Checklist

- [ ] All tables have primary keys
- [ ] Foreign keys defined for relationships
- [ ] Appropriate indexes on foreign keys
- [ ] Indexes on WHERE/JOIN/ORDER BY columns
- [ ] NOT NULL constraints on required fields
- [ ] DEFAULT values for optional fields
- [ ] CHECK constraints for business rules
- [ ] Appropriate data types (not oversized)
- [ ] DECIMAL for money (not FLOAT)
- [ ] DATETIME2 for dates (not VARCHAR)
- [ ] NVARCHAR for international text
- [ ] Normalization appropriate (3NF typical)
- [ ] Denormalization justified and documented
- [ ] No multi-valued columns (violates 1NF)
- [ ] No partial dependencies (violates 2NF)
- [ ] No transitive dependencies (violates 3NF)
- [ ] Junction tables for many-to-many
- [ ] Consistent naming conventions
- [ ] Schema documentation exists
- [ ] Migration scripts version controlled

## Key Takeaways

1. **Normalize to 3NF by default**: Eliminates most redundancy and anomalies
2. **Denormalize strategically**: Only when performance requires it, document why
3. **Choose smallest appropriate data type**: Saves space and improves performance
4. **DECIMAL for money, never FLOAT**: Avoid rounding errors in financial calculations
5. **Foreign keys enforce integrity**: Always define relationships in database
6. **Index foreign keys**: Critical for join performance
7. **VARCHAR(MAX) is expensive**: Use only when truly needed
8. **Migrate safely**: Additive changes first, breaking changes later
9. **Version your schema**: Track changes with migration scripts
10. **Document denormalization**: Future developers need to understand trade-offs

---

**Last Updated**: 2026-01-15
**Version**: 1.0.0
**Category**: Database & Architecture
