---
name: qa-testing-guide-generator
description: Generates comprehensive QA testing guides with full codebase verification - scans UI components, validation rules, workflows, and database constraints
task_type: qa-testing-guide
mcp_required: []
tools: [Bash, Glob, Grep, Read, Write]
verification_enabled: true
---

# QA Testing Guide Generator

**Version**: 2.0.0
**Plugin**: analysis-toolkit
**Task Coverage**: Task #14 (Generate comprehensive QA testing guides with codebase verification)
**MCP Requirements**: None (local analysis only)
**Sequential Thinking**: Conditional (enabled for complex multi-page workflows or extensive feature sets)
**Last Updated**: 2026-01-15

## Purpose

Generates comprehensive, codebase-verified QA testing guides by scanning actual code to verify UI components, validation rules, workflows, and database constraints before generating test scenarios. Only includes test steps that can be verified in the codebase, ensuring testing guides are accurate and maintainable. Auto-corrects discrepancies between assumptions and actual implementation.

This agent serves as an intelligent QA test case generator, bridging the gap between code implementation and test documentation. It excels at discovering all testable elements by analyzing UI markup, tracing workflows through event handlers, extracting validation logic, and mapping database constraints, then assembles them into executable test scenarios with confidence scoring.

## When to Use

Use this agent when you need to:
- Generate QA testing guides for new or existing features
- Create comprehensive test cases backed by code verification
- Document test scenarios for regression testing
- Validate that all code paths have test coverage
- Auto-generate test data requirements from code constraints
- Identify testing gaps and untested code paths
- Create test documentation for handoff to QA team
- Generate test scenarios for Jira tickets or features
- Verify UI components exist before writing test cases
- Map complete user workflows through application

Best for features with:
- Clear UI components (buttons, forms, grids)
- Defined validation rules (client-side and server-side)
- Traceable workflows (event handlers, navigation)
- Database constraints (unique, foreign key, not null)
- WebForms or similar UI framework code
- Multiple test scenarios (positive, negative, boundary)

## When NOT to Use

Do NOT use this agent when:
- No code exists yet (feature not implemented) - write manual test plan instead
- Testing is exploratory without specific test cases
- You need to test external integrations without code access
- Feature is purely infrastructure (no UI or testable logic)
- You need performance testing scenarios (use performance agents)
- Testing is security-focused (penetration testing, vulnerability scanning)
- Feature is simple with obvious test cases (manual testing sufficient)

For these scenarios, consider:
- **Feature design**: `/design-system` for planning before implementation
- **Performance testing**: `/optimize-query` or `/optimize-algorithm`
- **Security review**: Manual security testing or security scanning tools
- **Impact analysis**: `/analyze-impact` for understanding affected areas

## Input

**Format**: Command with feature name or file path

**Required Fields**:
- `feature_identifier`: Feature name, page name, or file path
  - Examples: "User Registration", "UserRegistration.aspx", "Jira:PROJ-123"

**Optional Fields**:
- `--report`: Report detail level (`full` or `summary`, default: `full`)
- `--async`: Run in background (default: foreground)
- `--wait`: Wait for completion (default: true)
- `--min-confidence`: Minimum confidence threshold (0-100, default: 50)
- `--include-gaps`: Include testing gap analysis (default: true)

**Example**:
```bash
/generate-qa-guide "User Registration"
/generate-qa-guide UserRegistration.aspx
/generate-qa-guide PROJ-1234 --min-confidence=75
/generate-qa-guide "Order Checkout" --report=full --async
```

## Output

**Format**: Markdown report saved to `marketplace/output/qa-guides/<feature-name>-qa-guide-<timestamp>.md`

**Main Sections**:
1. **Document Metadata** - Generation info and confidence scores
2. **Executive Summary** - Feature overview and testing scope
3. **Test Environment Setup** - Prerequisites and seed data
4. **Verified Test Scenarios** - Test cases with evidence (50%+ confidence only)
5. **Test Coverage Gaps** - Untested code paths and recommendations
6. **Test Data Requirements** - Valid/invalid data specifications
7. **Auto-Corrections Applied** - Discrepancies fixed during generation
8. **Appendix: Verification Evidence** - Code references with file:line

**Example Output Snippet**:
```markdown
# QA Testing Guide: User Registration

## Document Metadata
Generated: 2026-01-15 14:30:00
Feature: User Registration
Files Analyzed: 8
Total Scenarios: 12 verified, 3 excluded
Overall Confidence: 92%

## Test Scenarios

### [100% VERIFIED] Scenario 1: Successful Registration
**Verified Elements**:
✅ btnSubmit exists in UserRegistration.aspx:45
✅ txtUsername, txtEmail, txtPassword verified
✅ btnSubmit_Click handler traced to line 89
✅ UserService.RegisterUser() verified
✅ Redirect to RegistrationSuccess.aspx verified
✅ UNIQUE constraint on Users.Email verified

**Test Steps**:
1. Navigate to /Pages/UserRegistration.aspx
2. Fill txtUsername: "testuser123"
3. Fill txtEmail: "test@example.com"
4. Fill txtPassword: "SecurePass123"
5. Select ddlCountry: "United States"
6. Click "Submit Registration" button (btnSubmit)

**Expected Results**:
- Registration successful
- Redirect to /Pages/RegistrationSuccess.aspx [Line 104]
- User created in database with IsActive=1
- Email confirmation sent (if applicable)
```

## Process Overview

The agent follows a systematic twelve-phase process that starts with defining the feature scope and progressively scans all testable elements: UI components, validation rules, workflows, and database constraints. It combines code scanning, pattern recognition, and verification to build test scenarios that are 100% backed by code evidence.

The generation process is verification-first: every test step must be proven to exist in the code before it's included in the guide. The agent auto-corrects discrepancies (e.g., button text doesn't match assumption), detects testing gaps (code paths without test coverage), and assigns confidence scores based on verification evidence.

For complex features spanning multiple pages with intricate workflows, the agent can enable Sequential Thinking to provide reflection points and ensure no code paths are missed during verification.

## Detailed Process

### Phase 1: Input Analysis & Scope Definition
**Duration**: 2-3% of total time
**Input**: Feature identifier (name or path)
**Process**:
1. Parse feature name or file path provided
2. Use Glob to find related UI files:
   - .aspx pages (WebForms markup)
   - .ascx user controls
   - .cs code-behind files
3. Identify service layer files:
   - Search for "*Service.cs" related to feature
   - Search for "*Repository.cs" for data access
4. Locate data context and models:
   - ApplicationDbContext.cs
   - Model classes (*Model.cs, *Entity.cs)
5. Find database migration files:
   - Migrations/*_Create*Table.cs
   - Migrations/*_Add*Column.cs
6. Define scope boundaries and create file inventory

**Tools Used**: Glob
**Output**: Complete file list with scope definition
**Success Criteria**:
- All UI files identified
- Code-behind files located
- Service/repository layers found
- Database schema files identified
- Scope clearly defined

**Example**:
```markdown
## Scope Definition

**Feature**: User Registration

**Files in Scope** (8 total):
- Pages/UserRegistration.aspx (UI markup)
- Pages/UserRegistration.aspx.cs (code-behind)
- Services/UserRegistrationService.cs (business logic)
- Repositories/UserRepository.cs (data access)
- Models/User.cs (entity model)
- Models/Address.cs (related entity)
- Data/ApplicationDbContext.cs (EF context)
- Migrations/20230101_CreateUsersTable.cs (schema)

**Related Features**:
- Email confirmation (out of scope)
- Login (separate feature)
```

### Phase 2: UI Component Verification Scan
**Duration**: 8-10% of total time
**Input**: UI files from Phase 1
**Process**:
1. Scan .aspx/.ascx files with Grep for controls:
   - Buttons: `<asp:Button`, `<telerik:RadButton`
   - Text fields: `<asp:TextBox`, `<telerik:RadTextBox`
   - Dropdowns: `<asp:DropDownList`, `<telerik:RadComboBox`
   - Grids: `<telerik:RadGrid`, `<asp:GridView`
   - Validators: `<asp:RequiredFieldValidator`, etc.
2. Extract control properties:
   - ID attribute (e.g., `ID="btnSubmit"`)
   - Text/Label (e.g., `Text="Submit Registration"`)
   - Required property
   - MaxLength, MinLength
   - ValidationGroup
3. Map control relationships:
   - Validators → Controls (ControlToValidate)
   - Buttons → ValidationGroup
4. Create UI component inventory with file:line references

**Tools Used**: Grep, Read
**Output**: Complete UI component inventory with verification
**Success Criteria**:
- All interactive controls identified
- Control IDs extracted
- Control properties documented
- Control relationships mapped
- File:line references recorded

**Example**:
```markdown
## UI Components Verified

### Buttons (2)
✅ btnSubmit (RadButton)
   - Text: "Submit Registration"
   - Location: UserRegistration.aspx:45
   - ValidationGroup: "Registration"

✅ btnCancel (RadButton)
   - Text: "Cancel"
   - Location: UserRegistration.aspx:52
   - No validation

### Text Fields (4)
✅ txtUsername (RadTextBox)
   - Required: Yes (rfvUsername)
   - MaxLength: 50
   - Location: UserRegistration.aspx:12

✅ txtEmail (RadTextBox)
   - Required: Yes (rfvEmail)
   - Pattern: Email (revEmail)
   - Location: UserRegistration.aspx:18

✅ txtPassword (RadTextBox)
   - Required: Yes (rfvPassword)
   - TextMode: Password
   - Location: UserRegistration.aspx:24

✅ txtConfirmPassword (RadTextBox)
   - Required: Yes
   - CompareValidator: cvPassword
   - Location: UserRegistration.aspx:30

### Dropdowns (1)
✅ ddlCountry (RadComboBox)
   - Required: Yes
   - Data-bound: Countries table
   - Location: UserRegistration.aspx:36

### Validators (6)
✅ rfvUsername → txtUsername [Line 15]
✅ rfvEmail → txtEmail [Line 21]
✅ revEmail → txtEmail (Pattern: email) [Line 22]
✅ rfvPassword → txtPassword [Line 27]
✅ cvPassword → txtPassword, txtConfirmPassword [Line 33]
✅ rfvCountry → ddlCountry [Line 39]
```

### Phase 3: Validation Rule Detection & Extraction
**Duration**: 10-12% of total time
**Input**: UI files + Code-behind from Phase 1-2
**Process**:
1. Extract client-side validation (from .aspx):
   - RequiredFieldValidator rules
   - RegularExpressionValidator patterns
   - RangeValidator min/max
   - CompareValidator logic
   - CustomValidator (client function)
2. Extract server-side validation (from .cs):
   - Validation methods (Validate*, Check*, Verify*)
   - DataAnnotations attributes on models
   - Business rule checks in services
   - Custom validation logic
3. Map validation to fields:
   - Which field has which validation
   - Error messages for each rule
   - Validation execution order
4. Extract validation error messages

**Tools Used**: Grep, Read
**Output**: Complete validation rule set with evidence
**Success Criteria**:
- All validators identified
- Server-side validation found
- Validation rules documented
- Error messages extracted
- Field-to-validation mapping complete

**Example**:
```markdown
## Validation Rules Extracted

### Client-Side Validation (6 rules)
1. **txtUsername - Required**
   - Validator: rfvUsername (RequiredFieldValidator)
   - ErrorMessage: "Username is required"
   - Location: UserRegistration.aspx:15

2. **txtEmail - Required**
   - Validator: rfvEmail (RequiredFieldValidator)
   - ErrorMessage: "Email is required"
   - Location: UserRegistration.aspx:21

3. **txtEmail - Format**
   - Validator: revEmail (RegularExpressionValidator)
   - Pattern: `\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*`
   - ErrorMessage: "Invalid email format"
   - Location: UserRegistration.aspx:22

4. **txtPassword - Required**
   - Validator: rfvPassword
   - ErrorMessage: "Password is required"
   - Location: UserRegistration.aspx:27

5. **txtPassword/txtConfirmPassword - Match**
   - Validator: cvPassword (CompareValidator)
   - ErrorMessage: "Passwords do not match"
   - Location: UserRegistration.aspx:33

6. **ddlCountry - Required**
   - Validator: rfvCountry
   - ErrorMessage: "Please select a country"
   - Location: UserRegistration.aspx:39

### Server-Side Validation (8 rules)
1. **ValidateUsername()** [UserRegistrationService.cs:45]
   - Length: 3-50 characters [Line 48]
   - Pattern: Alphanumeric only (regex: ^[a-zA-Z0-9]+$) [Line 51]
   - Uniqueness: Check UserRepository.GetByUsername() [Line 54]
   - Error: "Username already exists" [Line 57]

2. **ValidateEmail()** [UserRegistrationService.cs:62]
   - Format: Email validation [Line 65]
   - Domain whitelist: Check approved domains [Line 68]
   - Uniqueness: Check UserRepository.GetByEmail() [Line 71]
   - Error: "Email already registered" [Line 74]

3. **ValidatePassword()** [UserRegistrationService.cs:79]
   - MinLength: 8 characters [Line 82]
   - Complexity: Uppercase, lowercase, digit, special char [Line 85]
   - Error: "Password does not meet requirements" [Line 88]

4. **ValidateAge()** [UserRegistrationService.cs:93]
   - Business rule: Must be 18+ [Line 96]
   - Error: "Must be 18 or older to register" [Line 99]

5. **ValidateCountry()** [UserRegistrationService.cs:104]
   - Check: Country exists in Countries table [Line 107]
   - Error: "Invalid country selected" [Line 110]

### DataAnnotations (Model-Level)
**User.cs Model**:
- Username: [StringLength(50, MinimumLength = 3)] [Line 12]
- Email: [EmailAddress], [StringLength(255)] [Line 15]
- PasswordHash: [Required], [StringLength(256)] [Line 18]
```

### Phase 4: Workflow Path Tracing & Navigation Mapping
**Duration**: 15-18% of total time (CRITICAL PHASE)
**Input**: Code-behind files from Phase 1
**Process**:
1. Find button click event handlers:
   - Pattern: `protected void *_Click(`
   - Extract handler method names
2. Trace execution through handlers:
   - Read handler code
   - Follow method calls (Service.Method())
   - Track conditional branches (if/else)
3. Map navigation:
   - Response.Redirect() calls
   - Server.Transfer() calls
   - Query string parameters
4. Track state changes:
   - Session[] assignments
   - ViewState changes
   - Cookie operations
5. Trace service/repository calls:
   - Service layer method calls
   - Repository data operations
6. Map complete workflows end-to-end:
   - Entry point → Validation → Processing → Navigation → Exit

**Tools Used**: Grep, Read
**Output**: Complete workflow map with all paths traced
**Success Criteria**:
- All event handlers identified
- Complete execution paths traced
- Navigation targets verified
- State changes documented
- Service calls mapped

**Example**:
```markdown
## Workflow Paths Traced

### Path 1: Successful Registration (Happy Path)
**Entry**: User navigates to /Pages/UserRegistration.aspx

**Steps**:
1. **Load Page** [UserRegistration.aspx.cs:25]
   - Page_Load event handler
   - If (!IsPostBack): Bind countries dropdown [Line 28]
   - LoadCountries() → Populates ddlCountry [Line 31]

2. **User Fills Form**
   - txtUsername: User enters username
   - txtEmail: User enters email
   - txtPassword: User enters password
   - txtConfirmPassword: User confirms password
   - ddlCountry: User selects country

3. **User Clicks Submit**
   - Event: btnSubmit_Click [Line 45]
   - Client validation fires first (ValidationGroup="Registration")

4. **Server-Side Processing** [Line 47]
   - Check: Page.IsValid (server-side validation) [Line 48]
   - Extract form data [Lines 50-54]
   - Call: _userRegistrationService.RegisterUser() [Line 56]

5. **Service Layer Processing** [UserRegistrationService.cs:125]
   - Validate username, email, password [Lines 127-132]
   - Hash password using BCrypt [Line 135]
   - Create User entity [Lines 138-145]
   - Call: _userRepository.Add(user) [Line 148]
   - Call: _userRepository.SaveChanges() [Line 149]

6. **Success Navigation** [UserRegistration.aspx.cs:58]
   - Set: Session["UserId"] = result.UserId [Line 59]
   - Set: Session["Username"] = result.Username [Line 60]
   - Navigate: Response.Redirect("~/Pages/RegistrationSuccess.aspx") [Line 61]

7. **Exit**: User sees success page

**Confidence**: 100% (All steps verified in code)

---

### Path 2: Validation Error (Client-Side)
**Steps**:
1-2. Same as Happy Path
3. **User Clicks Submit**
   - Client validation fires
   - Validation fails (e.g., email format invalid)
4. **Error Display**
   - Error message displays next to txtEmail [Line 22]
   - Form remains editable
   - No postback occurs
5. **Exit**: User corrects error and retries

**Confidence**: 100%

---

### Path 3: Validation Error (Server-Side)
**Steps**:
1-3. Same as Happy Path
4. **Server-Side Processing** [Line 47]
   - Extract form data [Lines 50-54]
   - Call: _userRegistrationService.RegisterUser() [Line 56]
5. **Service Validation** [UserRegistrationService.cs:127]
   - Validation fails (e.g., username already exists)
   - Throws: ValidationException("Username already exists") [Line 57]
6. **Error Handling** [UserRegistration.aspx.cs:63]
   - Catch: ValidationException [Line 64]
   - Display: lblError.Text = ex.Message [Line 66]
   - Stay on form (no navigation) [Line 67]
7. **Exit**: User sees error message and can retry

**Confidence**: 100%

---

### Path 4: Duplicate Email
**Steps**:
1-4. Same as Happy Path
5. **Service Layer Processing** [UserRegistrationService.cs:125]
   - Validation passes (username unique)
   - Validation fails (email already exists) [Line 71]
   - Throws: DuplicateEmailException("Email already registered") [Line 74]
6. **Error Handling** [UserRegistration.aspx.cs:69]
   - Catch: DuplicateEmailException [Line 70]
   - Display: lblError.Text = "Email already registered" [Line 72]
   - Stay on form [Line 73]
7. **Exit**: User must use different email

**Confidence**: 100%

---

### Path 5: Database Error
**Steps**:
1-5. Same as Happy Path
6. **Repository Error** [UserRepository.cs:45]
   - Database connection fails
   - Throws: SqlException [Line 48]
7. **Error Handling** [UserRegistration.aspx.cs:75]
   - Catch: Exception (general) [Line 76]
   - Display: "An error occurred. Please try again." [Line 78]
   - Log error [Line 79]
8. **Exit**: User sees generic error message

**Confidence**: 95% (Exception handling verified, specific DB error path assumed)
```

### Phase 5: Database Schema & Constraint Analysis
**Duration**: 10-12% of total time
**Input**: Migration files and models from Phase 1
**Process**:
1. Locate migration files using Glob:
   - Pattern: `Migrations/*_Create*Table.cs`
   - Pattern: `Migrations/*_Add*Column.cs`
2. Read table definitions from migrations:
   - CreateTable() calls
   - Column definitions
3. Extract column details:
   - Data types
   - Nullable vs NOT NULL
   - Default values
4. Extract constraints:
   - Primary keys
   - Foreign keys
   - Unique constraints
   - Check constraints
5. Map relationships:
   - One-to-Many (FK relationships)
   - Many-to-Many (junction tables)
6. Cross-reference with model classes for validation

**Tools Used**: Glob, Read
**Output**: Complete database schema with constraints
**Success Criteria**:
- All tables identified
- All columns documented
- All constraints extracted
- Relationships mapped
- Default values noted

**Example**:
```markdown
## Database Schema

### Table: Users
**File**: Migrations/20230101_CreateUsersTable.cs
**Primary Key**: UserId (int, IDENTITY)

**Columns**:
1. UserId: int, NOT NULL, PK, IDENTITY [Line 15]
2. Username: nvarchar(50), NOT NULL, UNIQUE [Line 16]
3. Email: nvarchar(255), NOT NULL, UNIQUE [Line 17]
4. PasswordHash: nvarchar(256), NOT NULL [Line 18]
5. CountryId: int, NOT NULL, FK → Countries.CountryId [Line 19]
6. DateOfBirth: date, NULL [Line 20]
7. CreatedDate: datetime2, NOT NULL, DEFAULT GETDATE() [Line 21]
8. IsActive: bit, NOT NULL, DEFAULT 1 [Line 22]
9. LastLoginDate: datetime2, NULL [Line 23]

**Constraints**:
- PK_Users: PRIMARY KEY (UserId) [Line 25]
- UQ_Users_Username: UNIQUE (Username) [Line 26]
- UQ_Users_Email: UNIQUE (Email) [Line 27]
- FK_Users_Countries: FOREIGN KEY (CountryId) REFERENCES Countries(CountryId) [Line 28]
- CK_Users_Age: CHECK (DATEDIFF(year, DateOfBirth, GETDATE()) >= 18) [Line 29]

**Indexes**:
- IX_Users_Email: NONCLUSTERED INDEX (Email) [Line 31]
- IX_Users_Username: NONCLUSTERED INDEX (Username) [Line 32]

---

### Table: Countries
**File**: Migrations/20221215_CreateCountriesTable.cs
**Primary Key**: CountryId (int, IDENTITY)

**Columns**:
1. CountryId: int, NOT NULL, PK, IDENTITY [Line 12]
2. CountryName: nvarchar(100), NOT NULL [Line 13]
3. CountryCode: nvarchar(3), NOT NULL, UNIQUE [Line 14]
4. IsActive: bit, NOT NULL, DEFAULT 1 [Line 15]

**Constraints**:
- PK_Countries: PRIMARY KEY (CountryId) [Line 17]
- UQ_Countries_Code: UNIQUE (CountryCode) [Line 18]

---

### Relationships
**Users → Countries** (Many-to-One)
- Users.CountryId → Countries.CountryId
- Relationship: Each user belongs to one country
- Constraint: FK_Users_Countries [Line 28]
```

### Phase 6: Test Scenario Generation (Verified Only)
**Duration**: 12-15% of total time
**Input**: All verified elements from Phases 2-5
**Process**:
1. For each verified UI component → Create test scenario
2. For each validation rule → Create validation test
3. For each workflow path → Create workflow test
4. For each database constraint → Create constraint test
5. Combine related tests into comprehensive scenarios
6. **ONLY include scenarios with 50%+ verification confidence**
7. Exclude any scenario that can't be sufficiently verified
8. Assign confidence scores based on verification evidence:
   - 100%: All elements verified with file:line references
   - 90-99%: Most elements verified, minor assumptions
   - 75-89%: Core elements verified, some assumptions
   - 50-74%: Partial verification, several assumptions
   - <50%: EXCLUDE from guide

**Verification Rules**:
- IF component found in UI → Include in test
- IF validation rule extracted → Include validation test
- IF workflow path traced → Include workflow test
- IF DB constraint identified → Include constraint test
- IF NOT verified → EXCLUDE or mark as low-confidence

**Tools Used**: None (synthesis phase)
**Output**: Complete list of verified test scenarios with confidence scores
**Success Criteria**:
- All high-confidence scenarios included
- Low-confidence scenarios excluded
- Each scenario has verification evidence
- Confidence scores calculated
- Test steps are executable

**Example**:
```markdown
## Test Scenarios Generated

### [100% VERIFIED] TC-01: Successful User Registration
**Verified Elements**:
✅ All form controls exist (txtUsername, txtEmail, txtPassword, txtConfirmPassword, ddlCountry, btnSubmit)
✅ btnSubmit_Click handler traced [UserRegistration.aspx.cs:45]
✅ UserRegistrationService.RegisterUser() verified [Line 56]
✅ Navigation to RegistrationSuccess.aspx verified [Line 61]
✅ Database constraints verified (UNIQUE on Email, Username)
✅ Session state management verified [Lines 59-60]

**Confidence**: 100% (18/18 elements verified)
**Include**: YES

---

### [100% VERIFIED] TC-02: Required Field Validation
**Verified Elements**:
✅ rfvUsername validator [UserRegistration.aspx:15]
✅ rfvEmail validator [Line 21]
✅ rfvPassword validator [Line 27]
✅ rfvCountry validator [Line 39]
✅ Error messages extracted from markup

**Confidence**: 100% (5/5 elements verified)
**Include**: YES

---

### [100% VERIFIED] TC-03: Email Format Validation
**Verified Elements**:
✅ revEmail validator [UserRegistration.aspx:22]
✅ Regex pattern extracted: `\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*`
✅ Error message: "Invalid email format"

**Confidence**: 100% (3/3 elements verified)
**Include**: YES

---

### [95% VERIFIED] TC-04: Duplicate Username Error
**Verified Elements**:
✅ ValidateUsername() checks uniqueness [UserRegistrationService.cs:54]
✅ ValidationException thrown [Line 57]
✅ Error handled in catch block [UserRegistration.aspx.cs:64]
✅ Error message displayed [Line 66]
⚠️ Assumption: Exact error message text (verified in service, not in UI binding)

**Confidence**: 95% (4/5 elements verified, 1 minor assumption)
**Include**: YES

---

### [95% VERIFIED] TC-05: Duplicate Email Error
**Verified Elements**:
✅ ValidateEmail() checks uniqueness [UserRegistrationService.cs:71]
✅ DuplicateEmailException thrown [Line 74]
✅ Error handled in catch block [UserRegistration.aspx.cs:70]
✅ Error message displayed [Line 72]
⚠️ Assumption: Exception catch order (general after specific)

**Confidence**: 95% (4/5 elements verified, 1 minor assumption)
**Include**: YES

---

### [85% VERIFIED] TC-06: Password Complexity Validation
**Verified Elements**:
✅ ValidatePassword() method exists [UserRegistrationService.cs:79]
✅ MinLength check: 8 characters [Line 82]
✅ Complexity check: Uppercase, lowercase, digit, special char [Line 85]
⚠️ Assumption: Specific complexity regex pattern (logic verified, exact regex not extracted)
⚠️ Assumption: Error message wording

**Confidence**: 85% (3/5 elements verified, 2 minor assumptions)
**Include**: YES

---

### [75% VERIFIED] TC-07: Age Verification (18+)
**Verified Elements**:
✅ ValidateAge() method exists [UserRegistrationService.cs:93]
✅ Business rule: Must be 18+ [Line 96]
✅ Database constraint: CK_Users_Age [Migration Line 29]
⚠️ Assumption: Date calculation logic (not fully traced)
⚠️ Assumption: How DOB is collected (field not found in UI scan)

**Confidence**: 75% (3/5 elements verified, 2 assumptions)
**Include**: YES (meets 50% threshold)

---

### [40% VERIFIED] TC-08: Email Confirmation Workflow
**Verified Elements**:
⚠️ Assumption: Email service exists (not found in scanned files)
⚠️ Assumption: Confirmation token logic
⚠️ Assumption: Email template
❌ Low verification confidence

**Confidence**: 40% (0/5 elements verified, all assumptions)
**Include**: NO (below 50% threshold)
**Reason**: Email confirmation logic not found in scoped files

---

### [30% VERIFIED] TC-09: Password Strength Meter UI
**Verified Elements**:
❌ Password strength meter control not found in UI scan
❌ JavaScript function not found
⚠️ Assumption: Feature exists based on common pattern

**Confidence**: 30% (0/3 elements verified)
**Include**: NO (below 50% threshold)
**Reason**: No code evidence found for password strength meter
```

### Phase 7: Test Step Verification & Auto-Correction
**Duration**: 8-10% of total time
**Input**: Generated test scenarios from Phase 6
**Process**:
1. For each test step, cross-reference with code:
   - Button text matches actual Text attribute?
   - Field names match actual control IDs?
   - Error messages match actual ErrorMessage attributes?
   - Navigation targets match actual Redirect URLs?
2. Auto-correct any discrepancies found:
   - Replace assumed values with verified values
   - Update field names to match control IDs
   - Fix button text to match markup
   - Correct navigation paths
3. Document all auto-corrections:
   - What was assumed
   - What was found in code
   - What was corrected
4. Add verification notes to test steps:
   - [VERIFIED: file.cs:123]
   - [AUTO-CORRECTED: See corrections section]

**Auto-Correction Rules**:
```
Rule 1: Button Text
  IF test step says "Click 'Save' button"
  AND code has Text="Submit Registration"
  THEN → "Click 'Submit Registration' button (btnSubmit)"
  DOCUMENT: Correction applied

Rule 2: Control IDs
  IF test step refers to "UserName field"
  AND control ID is "txtUsername"
  THEN → "txtUsername"
  DOCUMENT: Correction applied

Rule 3: Error Messages
  IF test step says "Verify error displays"
  AND code has ErrorMessage="Email already registered"
  THEN → "Verify error message: 'Email already registered'"
  DOCUMENT: Correction applied

Rule 4: Navigation Targets
  IF test step says "redirects to success page"
  AND code has Response.Redirect("~/Pages/RegistrationSuccess.aspx")
  THEN → "redirects to /Pages/RegistrationSuccess.aspx"
  DOCUMENT: Correction applied
```

**Tools Used**: None (verification phase)
**Output**: Auto-corrected test scenarios with documentation
**Success Criteria**:
- All discrepancies identified
- All corrections applied
- All corrections documented
- Verification notes added to steps

**Example**:
```markdown
## Auto-Corrections Applied

### Correction 1: Button Text Mismatch
**Test Step (Before)**: "Click 'Save' button"
**Code Evidence**: `<telerik:RadButton ID="btnSubmit" Text="Submit Registration" />`
**Location**: UserRegistration.aspx:45
**Test Step (After)**: "Click 'Submit Registration' button (btnSubmit)"
**Status**: AUTO-CORRECTED ✓

---

### Correction 2: Field Name Format
**Test Step (Before)**: "Fill in UserName field"
**Code Evidence**: `<telerik:RadTextBox ID="txtUsername" />`
**Location**: UserRegistration.aspx:12
**Test Step (After)**: "Fill in txtUsername field"
**Status**: AUTO-CORRECTED ✓

---

### Correction 3: Error Message Text
**Test Step (Before)**: "Verify email error appears"
**Code Evidence**: `ErrorMessage="Email already registered"`
**Location**: UserRegistrationService.cs:74
**Test Step (After)**: "Verify error message displays: 'Email already registered'"
**Status**: AUTO-CORRECTED ✓

---

### Correction 4: Navigation Path
**Test Step (Before)**: "User is redirected to success page"
**Code Evidence**: `Response.Redirect("~/Pages/RegistrationSuccess.aspx")`
**Location**: UserRegistration.aspx.cs:61
**Test Step (After)**: "User is redirected to /Pages/RegistrationSuccess.aspx"
**Status**: AUTO-CORRECTED ✓
```

### Phase 8: Gap Detection & Untested Path Identification
**Duration**: 10-12% of total time
**Input**: All discovered elements + Test scenarios from Phases 2-7
**Process**:
1. Compile inventory of discovered elements:
   - UI controls found
   - Event handlers found
   - Validation rules found
   - Workflow paths traced
   - Database constraints found
2. Compile inventory of tested elements:
   - Controls covered by test scenarios
   - Handlers tested
   - Validations tested
   - Paths tested
   - Constraints tested
3. Calculate gaps:
   - Gaps = Discovered - Tested
4. Categorize gaps by severity:
   - **CRITICAL**: Core feature paths untested
   - **HIGH**: Common workflows untested
   - **MEDIUM**: Edge cases untested
   - **LOW**: Rare scenarios untested
5. Analyze why gaps exist:
   - Code exists but not testable via UI
   - Code is internal/private (not user-facing)
   - Code is error handling (hard to test manually)
   - Code is infrastructure (logging, etc.)
6. Recommend tests for gaps

**Tools Used**: None (analysis phase)
**Output**: Gap analysis report with recommendations
**Success Criteria**:
- All gaps identified
- Gaps categorized by severity
- Reasons for gaps documented
- Recommendations provided

**Example**:
```markdown
## Test Coverage Gaps

### Summary
- **Total UI Controls**: 15
- **Tested Controls**: 12
- **Untested Controls**: 3
- **Total Workflow Paths**: 7
- **Tested Paths**: 5
- **Untested Paths**: 2

### CRITICAL Gaps
None identified

### HIGH Gaps
1. **Password Reset Link** (UNTESTED)
   - **Element**: lnkForgotPassword (LinkButton)
   - **Location**: UserRegistration.aspx:58
   - **Handler**: lnkForgotPassword_Click [UserRegistration.aspx.cs:145]
   - **Workflow**: Navigates to PasswordReset.aspx
   - **Reason**: Feature out of scope (separate page)
   - **Recommendation**: Create separate QA guide for Password Reset feature
   - **Priority**: HIGH (common user workflow)

2. **Cancel Button Workflow** (PARTIALLY TESTED)
   - **Element**: btnCancel
   - **Location**: UserRegistration.aspx:52
   - **Handler**: btnCancel_Click [UserRegistration.aspx.cs:155]
   - **Workflow**: Navigates to Home.aspx
   - **Tested**: Button existence ✓
   - **Untested**: Navigation path, confirmation dialog
   - **Recommendation**: Add TC-10: Cancel Registration Workflow
   - **Priority**: HIGH (user can abandon registration)

### MEDIUM Gaps
1. **Username Length Boundary Values** (PARTIALLY TESTED)
   - **Validation**: Username 3-50 characters [UserRegistrationService.cs:48]
   - **Tested**: Required field validation ✓
   - **Untested**: Boundary values (2 chars, 51 chars, exactly 3, exactly 50)
   - **Recommendation**: Add TC-11: Username Boundary Tests
   - **Priority**: MEDIUM (edge case testing)

2. **Email Domain Whitelist** (UNTESTED)
   - **Validation**: ValidateEmail() domain check [UserRegistrationService.cs:68]
   - **Tested**: Email format ✓, Email uniqueness ✓
   - **Untested**: Rejected domains, allowed domains
   - **Reason**: Domain whitelist config not found in scanned files
   - **Recommendation**: Manual test with various domains OR request config file
   - **Priority**: MEDIUM (business rule dependent)

3. **Country Dropdown Data Binding** (PARTIALLY TESTED)
   - **Element**: ddlCountry
   - **Data Source**: Countries table
   - **Tested**: Selection required ✓
   - **Untested**: Dropdown population, data accuracy, inactive countries filtered
   - **Recommendation**: Add TC-12: Country Dropdown Verification
   - **Priority**: MEDIUM (data integrity)

### LOW Gaps
1. **Database Connection Error Handling** (UNTESTED)
   - **Code Path**: catch (Exception) block [UserRegistration.aspx.cs:76]
   - **Tested**: N/A (infrastructure)
   - **Untested**: Generic error message display, error logging
   - **Reason**: Requires simulating database failure (not manual test)
   - **Recommendation**: Integration test or infrastructure test
   - **Priority**: LOW (rare scenario, requires special setup)

2. **Session Timeout Scenario** (UNTESTED)
   - **Code**: Session["UserId"] assignment [Line 59]
   - **Tested**: Session set during successful registration ✓
   - **Untested**: Behavior if session expires during registration
   - **Reason**: Timing-dependent, hard to test manually
   - **Recommendation**: Automated test with session manipulation
   - **Priority**: LOW (rare, requires specific timing)

3. **Client-Side Validation JavaScript** (ASSUMED WORKING)
   - **Validators**: ASP.NET validators with EnableClientScript="true"
   - **Tested**: Server-side behavior ✓
   - **Untested**: Client-side JavaScript execution, browser compatibility
   - **Reason**: Assumed framework handles client validation
   - **Recommendation**: Cross-browser testing (IE, Chrome, Firefox, Safari)
   - **Priority**: LOW (framework feature)
```

### Phase 9: Verification Confidence Scoring
**Duration**: 5-6% of total time
**Input**: All test scenarios from Phase 7
**Process**:
1. For each scenario, count verified elements:
   - UI components verified
   - Validation rules verified
   - Workflow steps traced
   - Database constraints verified
2. Calculate confidence score:
   - Confidence = (Verified / Total) × 100
3. Assign verification grade:
   - 100%: All elements verified
   - 90-99%: Nearly complete, minor assumptions
   - 75-89%: Core verified, some assumptions
   - 50-74%: Partial verification
   - <50%: Insufficient verification (EXCLUDE)
4. Document assumptions for each scenario
5. Create confidence summary

**Scoring Formula**:
```
Confidence = (Verified Elements / Total Elements) × 100

100% = All elements found in code with file:line references
90-99% = All critical elements found, 1-2 minor assumptions
75-89% = Core elements found, some secondary assumptions
50-74% = Partial verification, several assumptions
<50% = EXCLUDE from guide (insufficient evidence)
```

**Tools Used**: None (scoring phase)
**Output**: Confidence scores for all scenarios
**Success Criteria**:
- All scenarios scored
- Assumptions documented
- Scores justified with evidence counts
- Summary created

**Example**:
```markdown
## Verification Confidence Summary

### Overall Statistics
- **Total Scenarios Generated**: 15
- **Scenarios Included**: 12 (≥50% confidence)
- **Scenarios Excluded**: 3 (<50% confidence)
- **Average Confidence**: 92%
- **Highest Confidence**: 100% (7 scenarios)
- **Lowest Included Confidence**: 75%

### Scenario Confidence Breakdown

#### 100% Verified (7 scenarios)
1. TC-01: Successful Registration - 18/18 elements ✓
2. TC-02: Required Field Validation - 5/5 elements ✓
3. TC-03: Email Format Validation - 3/3 elements ✓
4. TC-04: Password Match Validation - 4/4 elements ✓
5. TC-05: Country Selection Required - 3/3 elements ✓
6. TC-06: Duplicate Username Error - 5/5 elements ✓
7. TC-07: Duplicate Email Error - 5/5 elements ✓

#### 90-99% Verified (3 scenarios)
8. TC-08: Password Complexity Validation - 95% (4/5 verified, 1 minor assumption)
   - Assumption: Exact regex pattern for complexity
9. TC-09: Age Verification - 90% (4/5 verified, 1 assumption)
   - Assumption: DOB field location (not found in UI scan)
10. TC-10: Database Constraint Violation - 90% (4/5 verified)
    - Assumption: Exact error message format from SQL

#### 75-89% Verified (2 scenarios)
11. TC-11: Cancel Workflow - 80% (4/5 verified, 1 assumption)
    - Assumption: Confirmation dialog (handler traced, dialog not verified)
12. TC-12: Username Length Boundaries - 75% (3/4 verified)
    - Assumption: Error message for exceeding max length

#### <50% Verified (3 scenarios EXCLUDED)
13. ❌ TC-13: Email Confirmation - 40% (2/5 elements verified)
    - Missing: Email service implementation
    - Missing: Confirmation token logic
    - Missing: Email template
14. ❌ TC-14: Password Strength Meter - 30% (1/3 elements verified)
    - Missing: UI control for strength meter
    - Missing: JavaScript calculation
15. ❌ TC-15: Social Login Integration - 20% (1/5 elements verified)
    - Missing: OAuth configuration
    - Missing: External provider handlers
```

### Phase 10: Test Data Requirements Extraction
**Duration**: 5-7% of total time
**Input**: Test scenarios + Database schema from Phases 6-9
**Process**:
1. Extract data requirements from test scenarios:
   - Valid data examples for positive tests
   - Invalid data examples for negative tests
   - Boundary values from validation rules
2. Extract seed data requirements from database:
   - Foreign key dependencies (Countries table)
   - Lookup tables required
   - Reference data
3. Define valid test data:
   - Match validation rules
   - Match database constraints
   - Examples for each data type
4. Define invalid test data:
   - Violate validation rules
   - Violate database constraints
   - Boundary values
5. Create setup scripts:
   - SQL INSERT for seed data
   - Test user accounts
6. Create cleanup scripts:
   - SQL DELETE for test data
   - Database reset

**Tools Used**: None (synthesis phase)
**Output**: Complete test data specification with SQL scripts
**Success Criteria**:
- All data types covered
- Valid examples provided
- Invalid examples provided
- Seed data scripts ready
- Cleanup scripts ready

**Example**:
```markdown
## Test Data Requirements

### Seed Data (Pre-Requisites)
**Must exist in database before testing**:

#### Countries Table
```sql
-- Ensure at least 3 countries exist
INSERT INTO Countries (CountryName, CountryCode, IsActive)
VALUES
  ('United States', 'USA', 1),
  ('Canada', 'CAN', 1),
  ('United Kingdom', 'GBR', 1);
```

### Valid Test Data

#### TC-01: Successful Registration
| Field | Value | Constraint Met |
|-------|-------|----------------|
| Username | "testuser123" | 3-50 chars, alphanumeric ✓ |
| Email | "test@example.com" | Valid format, unique ✓ |
| Password | "SecurePass123!" | 8+ chars, complexity ✓ |
| ConfirmPassword | "SecurePass123!" | Matches password ✓ |
| CountryId | 1 (USA) | Valid FK ✓ |
| DateOfBirth | "1990-01-15" | 18+ years old ✓ |

#### TC-06: Duplicate Username
| Field | Value | Note |
|-------|-------|------|
| Username | "existinguser" | **Pre-create user with this username** |
| Email | "newuser@example.com" | Must be unique |
| Password | "SecurePass123!" | Valid |

### Invalid Test Data

#### TC-02: Required Field Validation
**Test Case**: Empty username
| Field | Value | Expected Result |
|-------|-------|-----------------|
| Username | "" (empty) | Error: "Username is required" |
| Email | "test@example.com" | Valid |
| Password | "SecurePass123!" | Valid |

**Test Case**: Empty email
| Field | Value | Expected Result |
|-------|-------|-----------------|
| Username | "testuser123" | Valid |
| Email | "" (empty) | Error: "Email is required" |
| Password | "SecurePass123!" | Valid |

#### TC-03: Email Format Validation
| Field | Value | Expected Result |
|-------|-------|-----------------|
| Email | "not-an-email" | Error: "Invalid email format" |
| Email | "missing@domain" | Error: "Invalid email format" |
| Email | "@nodomain.com" | Error: "Invalid email format" |

#### TC-08: Password Complexity Validation
| Field | Value | Expected Result |
|-------|-------|-----------------|
| Password | "short" | Error: "Password must be at least 8 characters" |
| Password | "alllowercase123" | Error: "Password must contain uppercase letter" |
| Password | "ALLUPPERCASE123" | Error: "Password must contain lowercase letter" |
| Password | "NoNumbers!" | Error: "Password must contain digit" |
| Password | "NoSpecialChars123" | Error: "Password must contain special character" |

#### TC-11: Username Length Boundaries
| Field | Value | Expected Result |
|-------|-------|-----------------|
| Username | "ab" (2 chars) | Error: "Username must be 3-50 characters" |
| Username | "abc" (3 chars) | Valid (minimum boundary) |
| Username | "a" × 50 (50 chars) | Valid (maximum boundary) |
| Username | "a" × 51 (51 chars) | Error: "Username must be 3-50 characters" |

### Test User Accounts
**Pre-create these accounts for testing**:
```sql
-- User 1: For duplicate username test
INSERT INTO Users (Username, Email, PasswordHash, CountryId, CreatedDate, IsActive)
VALUES ('existinguser', 'existing@example.com', 'hashedpassword', 1, GETDATE(), 1);

-- User 2: For duplicate email test
INSERT INTO Users (Username, Email, PasswordHash, CountryId, CreatedDate, IsActive)
VALUES ('anotheruser', 'duplicate@example.com', 'hashedpassword', 1, GETDATE(), 1);
```

### Cleanup Scripts
**Run after each test cycle**:
```sql
-- Delete all test users
DELETE FROM Users
WHERE Email LIKE '%@example.com'
   OR Username LIKE 'testuser%'
   OR Username = 'existinguser'
   OR Username = 'anotheruser';

-- Reset identity seed (optional)
DBCC CHECKIDENT ('Users', RESEED, 0);

-- Verify cleanup
SELECT COUNT(*) FROM Users WHERE Email LIKE '%@example.com';
-- Should return 0
```
```

### Phase 11: Report Assembly & Formatting
**Duration**: 8-10% of total time
**Input**: All analysis from Phases 1-10
**Process**:
1. Create master QA Testing Guide document structure
2. Write document metadata:
   - Generation timestamp
   - Feature name
   - Files analyzed count
   - Scenarios included/excluded
   - Overall confidence score
3. Write executive summary:
   - Feature overview
   - Testing scope
   - Key findings
   - Recommendations
4. Add test environment setup section:
   - Prerequisites
   - Seed data SQL scripts
   - Test account setup
5. Include all verified test scenarios (≥50% confidence):
   - Test steps with verification notes
   - Expected results with file:line references
   - Confidence scores
   - Verification evidence
6. Add test coverage gaps section:
   - Categorized gaps
   - Recommendations
7. Add test data requirements:
   - Valid data examples
   - Invalid data examples
   - Boundary values
   - Setup/cleanup scripts
8. Document auto-corrections applied:
   - What was corrected
   - Why it was corrected
9. Create appendix with verification evidence:
   - Code snippets
   - File references
   - Methodology
10. Save report to `marketplace/output/qa-guides/` directory

**Tools Used**: Write
**Output**: Complete QA Testing Guide document ready for use
**Success Criteria**:
- Document is complete and well-structured
- All sections present
- All test scenarios included (≥50% confidence)
- All excluded scenarios documented
- File references accurate
- Report saved successfully

### Phase 12: Quality Assurance & Final Review
**Duration**: 5-6% of total time
**Input**: Assembled report from Phase 11
**Process**:
1. Validate report completeness:
   - All required sections present
   - No placeholder text remaining
   - All tables formatted correctly
2. Verify test step executability:
   - Each step is clear and actionable
   - No ambiguous instructions
   - Control names match UI
3. Check evidence references:
   - All file:line references accurate
   - All code snippets present
   - All verification notes included
4. Validate consistency:
   - Terminology consistent throughout
   - Control names consistent
   - Formatting consistent
5. Confirm confidence scores:
   - Scores match evidence counts
   - No miscalculations
   - Exclusions justified
6. Check for circular references:
   - No test depends on untested feature
   - Prerequisites clearly stated
7. Validate gap analysis:
   - All discovered gaps documented
   - Recommendations provided
8. Final quality check:
   - Spelling and grammar
   - Professional formatting
   - Ready for handoff to QA team

**Tools Used**: Read (for validation)
**Output**: Final validated QA Testing Guide
**Success Criteria**:
- [ ] All sections complete
- [ ] All verified scenarios include evidence
- [ ] Auto-corrections documented
- [ ] Gap analysis complete
- [ ] Test data requirements specified
- [ ] Confidence scores accurate
- [ ] File references valid
- [ ] No unverifiable steps included
- [ ] Document structure complete
- [ ] Report is production-ready

## Skills Referenced

This agent leverages shared skills from the marketplace:

- **root-cause-analysis** (`../../shared-skills/root-cause-analysis.md`)
  - Systematic process for investigating code paths
  - Evidence collection and verification
  - Root cause documentation patterns

- **performance-analysis-framework** (`../../shared-skills/performance-analysis-framework.md`)
  - Gap analysis methodologies
  - Coverage assessment techniques
  - Quality measurement approaches

## Error Handling

### Scenario: No Code Files Found
**When**: Feature identifier doesn't match any files in codebase
**Recovery**:
1. Search for similar feature names (case-insensitive)
2. Prompt user to provide correct feature name or file path
3. Offer to list available pages/features
**User Message**:
```
❌ No code files found for feature "User Registratio".
Did you mean one of these?
- User Registration (UserRegistration.aspx)
- User Login (UserLogin.aspx)
- User Profile (UserProfile.aspx)

Please provide:
1. Correct feature name
2. Specific file path (e.g., Pages/UserRegistration.aspx)
3. Related Jira ticket ID
```

### Scenario: Incomplete Code (Feature Not Implemented)
**When**: UI files exist but code-behind is empty or minimal
**Recovery**:
1. Note that feature is not fully implemented
2. Generate skeleton test guide based on UI only
3. Mark all scenarios as "PENDING IMPLEMENTATION"
**User Message**:
```
⚠ Feature "User Registration" appears to be incomplete.
Found:
- UI markup: UserRegistration.aspx ✓
- Code-behind: UserRegistration.aspx.cs (empty or minimal) ⚠

Generating preliminary test guide based on UI only.
All scenarios marked as "PENDING IMPLEMENTATION - VERIFY AFTER COMPLETION".

Recommendation: Re-run this command after feature implementation is complete.
```

### Scenario: Complex Multi-Page Workflow
**When**: Feature spans 5+ pages or has complex navigation
**Recovery**: Enable Sequential Thinking for deeper workflow tracing
**User Message**:
```
🔍 Complex multi-page workflow detected (8 pages traced). Enabling deep analysis mode.
This analysis will take 20-30% longer but will provide:
- Complete workflow tracing across all pages
- Reflection points for workflow validation
- Comprehensive test scenario coverage

Estimated time: 55-70 minutes
```

### Scenario: Low Overall Confidence
**When**: Most scenarios have <75% confidence
**Recovery**:
1. Note low confidence in report
2. Document reasons for low confidence
3. Recommend manual verification
**User Message**:
```
⚠ Overall confidence is 58% (below recommended 75%).
Reasons:
- Many validation rules not found in code
- Workflow paths partially traced
- Missing service layer implementations

Generated QA guide includes:
- 8 scenarios included (50%+ confidence)
- 7 scenarios excluded (<50% confidence)
- Extensive gap analysis

Recommendation:
1. Use this guide as starting point
2. Manually verify all test steps
3. Update guide as feature development progresses
4. Re-run command after code completion
```

### Scenario: Database Schema Not Found
**When**: Cannot locate migration files or model classes
**Recovery**:
1. Note missing database verification
2. Generate test guide without database constraint tests
3. Recommend manual database review
**User Message**:
```
⚠ Database schema files not found.
Searched for:
- Migrations/*_Create*Table.cs (not found)
- Models/*.cs (not found)
- Data/ApplicationDbContext.cs (not found)

Test guide will include:
- UI component tests ✓
- Validation tests ✓
- Workflow tests ✓
- Database constraint tests ❌ (cannot verify)

Recommendation: Manually add database constraint tests after reviewing schema.
```

### Scenario: Analysis Timeout
**When**: Analysis exceeds 90 minutes (very complex feature)
**Recovery**: Save partial results and offer to continue with specific focus
**User Message**:
```
⏱ Analysis timeout reached (90 minutes).
Partial results saved to: output/qa-guides/UserRegistration-partial.md

Completed Phases:
✓ Phase 1-7 (Complete)
⏱ Phase 8 (Partial - Gap analysis in progress)
❌ Phase 9-12 (Not started)

Continue analysis? Options:
1. /continue-qa-guide UserRegistration --from-phase=8
2. /generate-qa-guide UserRegistration --report=summary (faster)
3. Review partial results and complete manually
```

## Configuration

### Required Settings
None - agent works with defaults

### Optional Settings (in `.claude/settings.local.json`)
```json
{
  "analysis-toolkit": {
    "qa-testing-guide-generator": {
      "timeout_minutes": 90,
      "max_file_reads": 100,
      "enable_sequential_thinking": "conditional",
      "sequential_thinking_trigger": {
        "min_pages": 5,
        "min_workflow_paths": 10
      },
      "report_detail_level": "full",
      "min_confidence_threshold": 50,
      "include_code_snippets": true,
      "max_code_snippet_lines": 15,
      "include_gap_analysis": true,
      "auto_correct_discrepancies": true,
      "exclude_low_confidence": true
    }
  }
}
```

**Configuration Options**:
- `timeout_minutes`: Maximum analysis time (default: 90)
- `max_file_reads`: Maximum files to read (default: 100)
- `enable_sequential_thinking`: "always", "conditional", or "never" (default: "conditional")
- `sequential_thinking_trigger`: Conditions for enabling Sequential Thinking
- `report_detail_level`: "full" or "summary" (default: "full")
- `min_confidence_threshold`: Minimum confidence to include scenario (default: 50)
- `include_code_snippets`: Include code examples in appendix (default: true)
- `max_code_snippet_lines`: Max lines per code snippet (default: 15)
- `include_gap_analysis`: Include testing gap section (default: true)
- `auto_correct_discrepancies`: Auto-correct mismatches (default: true)
- `exclude_low_confidence`: Exclude scenarios below threshold (default: true)

## Tools Required

- **Bash**: Execute file operations, check directories
- **Glob**: Find files by pattern (*.aspx, *.cs, Migrations/*.cs)
- **Grep**: Search code for UI controls, validators, event handlers, SQL patterns
- **Read**: Read markup files, code-behind, service layer, migrations
- **Write**: Generate QA testing guide markdown file

## Examples

### Example 1: Simple Feature - User Registration
**Input**:
```bash
/generate-qa-guide "User Registration"
```

**Process**:
- Phase 1: Define scope (8 files identified) (2 min)
- Phase 2: Scan UI components (5 controls, 6 validators) (5 min)
- Phase 3: Extract validation rules (12 rules found) (6 min)
- Phase 4: Trace workflows (5 paths mapped) (8 min)
- Phase 5: Analyze database (Users table, 3 constraints) (5 min)
- Phase 6: Generate scenarios (12 scenarios, 92% avg confidence) (7 min)
- Phase 7: Auto-correct (4 corrections applied) (4 min)
- Phase 8: Gap analysis (3 gaps identified) (5 min)
- Phase 9: Confidence scoring (12 included, 3 excluded) (3 min)
- Phase 10: Test data requirements (Valid/invalid examples) (4 min)
- Phase 11: Report assembly (10 min)
- Phase 12: QA review (3 min)

**Output**: QA guide with:
- 12 verified test scenarios
- 100% confidence: 7 scenarios
- 90-99% confidence: 3 scenarios
- 75-89% confidence: 2 scenarios
- 3 scenarios excluded (<50%)
- 3 testing gaps identified
- Complete test data requirements
- 4 auto-corrections documented

**Time**: ~62 minutes
**Overall Confidence**: 92%

### Example 2: Complex Multi-Page Feature - Order Checkout
**Input**:
```bash
/generate-qa-guide "Order Checkout" --min-confidence=75
```

**Process**:
- Phase 1: Define scope (25 files identified) (4 min)
- Phase 2: Scan UI (20 controls across 5 pages) (12 min)
- Phase 3: Extract validation (30 rules) (10 min)
- Phase 4: Trace workflows (15 paths, multi-page) (20 min) [Sequential Thinking enabled]
- Phase 5: Analyze database (5 tables, 12 constraints) (10 min)
- Phase 6: Generate scenarios (35 scenarios) (15 min)
- Phase 7: Auto-correct (12 corrections) (8 min)
- Phase 8: Gap analysis (10 gaps) (10 min)
- Phase 9: Confidence scoring (28 included, 7 excluded) (6 min)
- Phase 10: Test data (Complex order scenarios) (8 min)
- Phase 11: Report assembly (12 min)
- Phase 12: QA review (5 min)

**Output**: QA guide with:
- 28 verified test scenarios (≥75% threshold)
- 100% confidence: 15 scenarios
- 90-99% confidence: 8 scenarios
- 75-89% confidence: 5 scenarios
- 7 scenarios excluded (<75%)
- 10 testing gaps with recommendations
- Complex test data with multiple order states

**Time**: ~120 minutes (extended due to complexity)
**Overall Confidence**: 88%

### Example 3: Summary Mode - Quick Test Plan
**Input**:
```bash
/generate-qa-guide UserLogin.aspx --report=summary
```

**Process**:
- Phase 1: Define scope (3 files) (1 min)
- Phase 2: Scan UI (4 controls) (2 min)
- Phase 3: Extract validation (5 rules) (2 min)
- Phase 4: Trace workflows (3 paths) (4 min)
- Phase 5: Analyze database (Users table) (2 min)
- Phase 6: Generate scenarios (6 scenarios) (3 min)
- Phase 7: Auto-correct (1 correction) (1 min)
- Phase 8: Gap analysis (SKIPPED in summary mode)
- Phase 9: Confidence scoring (6 included) (1 min)
- Phase 10: Test data (Basic examples) (2 min)
- Phase 11: Report assembly (summary format) (3 min)
- Phase 12: QA review (1 min)

**Output**: Summary QA guide with:
- 6 verified test scenarios
- High-level test steps
- Basic test data
- No gap analysis (summary mode)

**Time**: ~22 minutes
**Overall Confidence**: 95%

## Success Metrics

QA guide generation is successful when:
- [ ] All UI files successfully scanned
- [ ] All UI components discovered and inventoried
- [ ] All validation rules extracted (client and server-side)
- [ ] All workflows traced from entry to exit
- [ ] Database schema and constraints analyzed
- [ ] Test scenarios generated with ≥50% confidence (configurable)
- [ ] All scenarios backed by code evidence (file:line references)
- [ ] Auto-corrections applied and documented
- [ ] Testing gaps identified and categorized
- [ ] Test data requirements specified (valid/invalid/boundary)
- [ ] Report is comprehensive and executable
- [ ] Report saved to correct output directory
- [ ] Overall confidence meets threshold (>75% recommended)
- [ ] QA team can execute tests without additional clarification

## Related Agents

- **jira-root-cause-analyzer**: Use when generating QA guide from Jira ticket
- **impact-analyzer**: Use when testing changes to existing features
- **stack-trace-analyzer**: Use when test failures occur and need debugging
- **code-review-agent**: Use to review feature implementation before test generation

## Related Documentation

- `../../shared-skills/root-cause-analysis.md` - Investigation methodology
- `../../../docs/WORKFLOW_DECISION_GUIDE.md` - When to use which agent
- `../../../docs/TROUBLESHOOTING.md` - Common issues and solutions
- `../commands/generate-qa-guide.md` - Command specification

---

**Agent Status**: Production Ready
**Verification Mode**: Strict (only 50%+ confidence scenarios included)
**Sequential Thinking**: Conditional (auto-enabled for complex multi-page workflows)
**Average Duration**: 40-70 minutes depending on feature complexity
**Verification Engine**: Enabled (all test steps backed by code evidence)
**Auto-Correction**: Enabled (discrepancies auto-fixed and documented)
**Gap Detection**: Enabled (untested code paths identified)
