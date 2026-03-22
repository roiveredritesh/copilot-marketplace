---
description: "Generate comprehensive QA testing guide with full codebase verification"
argument-hint: "<ticket-id|file-path> [--from-analysis] [--report=full|summary]"
allowed-tools: [Bash, Glob, Grep, Read, Write, Task]
---

# Command: /generate-qa-guide

Generates comprehensive QA testing guides by scanning and verifying the actual codebase. Only includes test steps that can be verified in the code. Automatically corrects discrepancies and identifies testing gaps.

## Usage

```bash
/generate-qa-guide <ticket-id|file-path> [--from-analysis] [--report=full|summary]
```

## Arguments

### Required Arguments

- **ticket-id OR file-path**:
  - Jira ticket ID (e.g., `PROJ-1234`) when using `--from-analysis` flag
  - File path (e.g., `src/Pages/UserRegistration.aspx`) for standalone analysis
  - Comma-separated paths for multiple files (e.g., `"src/Services/User*.cs,src/Repository/*.cs"`)

### Optional Flags

- **--from-analysis**: Read existing Jira analysis and build QA guide from it (requires `/analyze-jira-issue` run first)
- **--report=full|summary**: Report detail level
  - `full`: Complete guide with all scenarios, gaps, evidence (DEFAULT)
  - `summary`: Quick overview with key scenarios only

## Examples

### Generate QA Guide from Jira Analysis
```bash
# Analysis must exist first
/analyze-jira-issue PROJ-1234 --wait

# Then generate QA guide
/generate-qa-guide PROJ-1234 --from-analysis

# Output: marketplace/output/qa-guides/PROJ-1234/QA-TESTING-GUIDE.md
```

### Generate QA Guide from Code (Standalone)
```bash
# Analyze single page
/generate-qa-guide src/Pages/UserRegistration.aspx

# Analyze multiple related files
/generate-qa-guide "src/Pages/UserRegistration.aspx,src/Services/UserService.cs"

# Output: marketplace/output/qa-guides/UserRegistration/QA-TESTING-GUIDE.md
```

### Generate Summary Report
```bash
# Quick overview without detailed scenarios
/generate-qa-guide PROJ-1234 --from-analysis --report=summary

# Output: marketplace/output/qa-guides/PROJ-1234/QA-TESTING-GUIDE-SUMMARY.md
```

### Background Execution
```bash
# Run in background
# /generate-qa-guide PROJ-1234 --from-analysis --async
```

## How It Works

### Mode 1: Integration with Jira Analysis (--from-analysis)

```
User: /generate-qa-guide PROJ-1234 --from-analysis

↓

1. Check if analysis exists: marketplace/output/analysis/PROJ-1234-analysis.md
2. If not found: Error - "Run /analyze-jira-issue PROJ-1234 first"
3. If found: Read technical analysis
4. Extract: Root cause, affected files, solution details
5. Invoke: qa-testing-guide-generator agent
   - Input: Analysis file + extracted details
   - Mode: Integration (use analysis context)
6. Agent scans actual code:
   - Verify affected files exist
   - Extract UI components
   - Find validation rules
   - Trace workflows
   - Analyze database changes
7. Generate: QA testing guide backed by code verification
8. Output: marketplace/output/qa-guides/PROJ-1234/
```

### Mode 2: Standalone Analysis (No --from-analysis)

```
User: /generate-qa-guide src/Pages/UserRegistration.aspx

↓

1. Validate file path exists
2. Invoke: qa-testing-guide-generator agent
   - Input: File path(s)
   - Mode: Standalone (fresh analysis)
3. Agent scans codebase:
   - Find related files (code-behind, services, repository)
   - Extract UI components
   - Find validation rules
   - Trace workflows
   - Analyze database
4. Generate: QA testing guide from code analysis
5. Output: marketplace/output/qa-guides/[feature-name]/
```

## What Gets Scanned

### Phase 1: Scope Definition
- Identifies all related files
- Determines analysis boundaries
- Maps file relationships

### Phase 2: UI Component Verification (Grep Patterns)
- Scans for: `<asp:Button`, `<telerik:RadButton`, `<asp:TextBox`, `<telerik:RadTextBox`, etc.
- Extracts: Control IDs, text, properties
- Verifies: Component actually exists in .aspx

### Phase 3: Validation Rule Detection (Grep + Read)
- Finds: `<asp:RequiredFieldValidator`, `<asp:RegularExpressionValidator`
- Searches: `[Required]`, `[StringLength]`, `[RegularExpression]` attributes
- Extracts: Error messages, patterns, business rules
- Locates: Custom validation methods in .cs files

### Phase 4: Workflow Path Tracing (Grep + Read)
- Finds: `protected void btnSubmit_Click(`
- Traces: Service calls, repository operations
- Maps: `Response.Redirect`, `Server.Transfer` navigation
- Identifies: Conditional paths (if/else branches)
- Result: Complete user journey from button click to result

### Phase 5: Database Schema Analysis (Glob + Read)
- Finds: Migration files (`*CreateUsers*.cs`, `*Add*Constraint*.cs`)
- Extracts: Table definitions, column specs
- Maps: Primary keys, foreign keys, unique constraints
- Identifies: NOT NULL, default values, relationships

### Phase 6-12: Test Generation & Verification
- Generates: Only scenarios with verified code backing
- Auto-Corrects: Button text, field names, error messages
- Detects: Untested code paths (gaps)
- Scores: Confidence level per scenario
- Extracts: Test data requirements
- Documents: All evidence and corrections

## Output Structure

### Directory Layout
```
marketplace/output/qa-guides/PROJ-1234/
├── QA-TESTING-GUIDE.md          # Master comprehensive guide
├── feature-impact-map.md         # Features affected
├── user-workflows.md             # User journeys
├── regression-areas.md           # Regression scope
├── test-scenarios.md             # Detailed test cases
├── test-data.md                  # Test data specifications
└── verification-report.md        # Scanning results
```

### Document Contents

#### QA-TESTING-GUIDE.md (Master Guide)
- Executive summary
- Verification summary (% verified)
- Test scenarios (only 50%+ confidence)
- Test coverage gaps
- Test data requirements
- Environment setup
- Auto-corrections applied
- Verification evidence appendix

#### Key Sections in Guide

**Executive Summary**:
```markdown
## Executive Summary

### Verification Status
✅ UI Components: 100% verified (12/12 controls found)
✅ Validation Rules: 95% verified (19/20 rules extracted)
✅ Workflow Paths: 90% verified (9/10 traced)
✅ Database Constraints: 100% verified (5/5 constraints)

### Testing Scope
- Total Test Scenarios: 8 verified, 3 excluded (low confidence)
- Coverage: 12 code paths tested
- Gaps Identified: 4 untested workflows
- Overall Confidence: 95%
```

**Test Scenario Example**:
```markdown
### [100% VERIFIED] Scenario 1: Successful User Registration

**Verified Elements**:
✅ btnSubmit exists in UserRegistration.aspx:45
✅ txtUsername, txtEmail, txtPassword verified
✅ btnSubmit_Click handler traced to line 89
✅ Response.Redirect("~/Pages/RegistrationSuccess.aspx") verified
✅ UNIQUE(Email) constraint verified in migration

**Test Steps**:
1. Navigate to /Pages/UserRegistration.aspx
2. Enter valid username in txtUsername
3. Enter valid email in txtEmail
4. Click "Submit Registration" button
   [VERIFIED: button text at UserRegistration.aspx:45]
5. Verify redirect to /Pages/RegistrationSuccess.aspx
   [VERIFIED: Response.Redirect at line 104]

**Expected Results**:
- Success message displays [Verified in code]
- User created in database [UNIQUE constraint verified]
- Email sent [Verified in UserService.cs:110]
- Session["UserId"] set [Verified at line 102]

**Verification Confidence**: 100%
**Evidence**: See Appendix Evidence #1-4
```

**Gap Analysis Example**:
```markdown
## Test Coverage Gaps

### CRITICAL - Password Reset Flow (UNTESTED)
- Location: UserRegistration.aspx.cs, Line 145
- Handler: lnkForgotPassword_Click
- Code Path: lnkForgotPassword_Click → UserService.SendPasswordReset()
- Reason: Not included in initial scope
- Recommendation: Add test scenario for "User initiates password reset"

### HIGH - Admin User Creation (UNTESTED)
- Location: UserRegistration.aspx.cs, Line 180
- Condition: if (IsAdmin)
- Code Path: Alternative branch not tested
- Reason: Conditional path not covered by scenarios
- Recommendation: Add test for "Admin creates privileged user"
```

## Verification Confidence Levels

| Confidence | Status | Inclusion |
|-----------|--------|-----------|
| 100% | Fully Verified | ✅ INCLUDED |
| 90-99% | Mostly Verified | ✅ INCLUDED |
| 75-89% | Substantially Verified | ✅ INCLUDED |
| 50-74% | Partially Verified | ✅ INCLUDED |
| Below 50% | Insufficient Verification | ❌ EXCLUDED |

**Confidence Calculation**:
```
Confidence = (Verified Elements / Total Elements) × 100

Example: Scenario has 8 total elements
- UI Components: 4 verified
- Validation: 3 verified
- Workflow: 1 verified
- Database: 0 found (not applicable)
= 8/8 = 100% verified
```

## Auto-Corrections Examples

The guide automatically fixes discrepancies between initial planning and actual code:

### Correction 1: Button Text
```markdown
BEFORE (Initial Plan): "Click 'Save' button"
AFTER (Corrected): "Click 'Submit Registration' button (btnSubmit)"

Evidence: UserRegistration.aspx, Line 45
Code: <telerik:RadButton ID="btnSubmit" Text="Submit Registration" />

[AUTO-CORRECTED: Button text verified in actual code]
```

### Correction 2: Field Name
```markdown
BEFORE: "Fill in UserName field"
AFTER: "Fill in txtUsername field"

Evidence: UserRegistration.aspx, Line 12
Code: <telerik:RadTextBox ID="txtUsername" runat="server" />

[AUTO-CORRECTED: Control ID verified in actual code]
```

### Correction 3: Error Message
```markdown
BEFORE: "Verify error message displays"
AFTER: "Verify error message: 'Email already registered'"

Evidence: UserRegistrationService.cs, Line 110
Code: throw new DuplicateEmailException("Email already registered")

[AUTO-CORRECTED: Exact error message from code]
```

### Correction 4: Navigation Target
```markdown
BEFORE: "Verify redirect to success page"
AFTER: "Verify redirect to /Pages/RegistrationSuccess.aspx"

Evidence: UserRegistration.aspx.cs, Line 104
Code: Response.Redirect("~/Pages/RegistrationSuccess.aspx")

[VERIFIED: Navigation target confirmed in code]
```

## When to Use This Command

✅ **Use /generate-qa-guide when**:
- You want comprehensive QA testing guide for a feature
- You need test scenarios backed by actual code analysis
- You want to identify untested code paths (gaps)
- You want auto-correction of discrepancies
- You want to ensure test coverage is complete

❌ **Don't use when**:
- You only need quick impact analysis (use `/analyze-impact` instead)
- You need code-level technical details (use `/analyze-jira-issue` instead)
- You're not ready to test yet (plan first, test guide later)

## Tips for Best Results

1. **Run Analysis First**: Use `/analyze-jira-issue PROJ-456 --wait` before generating QA guide with `--from-analysis`

2. **Be Specific**: More specific feature names help scope analysis
   - Good: "User Registration page"
   - Better: "UserRegistration.aspx"

3. **Use Full Mode**: Use default `--report=full` for comprehensive guide, `--report=summary` for quick reference

4. **Review Gaps**: Always check "Test Coverage Gaps" section to understand what's not tested

5. **Check Confidence**: Look for low-confidence scenarios and determine why they're not fully verified

6. **Use Evidence**: Reference the verification evidence appendix when discussing test scenarios with team

## Output Files Reference

| File | Purpose | Audience |
|------|---------|----------|
| QA-TESTING-GUIDE.md | Complete testing guide | QA Engineers, Testers |
| test-scenarios.md | Detailed test cases | QA Test Execution |
| test-data.md | Test data specs | QA/Test Data Team |
| regression-areas.md | Regression scope | QA Lead |
| verification-report.md | Scanning results | QA/Dev Communication |

## Troubleshooting

### "Analysis file not found"
**Error**: `marketplace/output/analysis/PROJ-1234-analysis.md not found`
**Solution**: Run `/analyze-jira-issue PROJ-1234 --wait` first, then run `/generate-qa-guide PROJ-1234 --from-analysis`

### "File path not found"
**Error**: `File path does not exist: src/Pages/UserRegistration.aspx`
**Solution**: Verify file path is correct relative to repository root

### "Low confidence scenarios"
**Reason**: Some test scenarios couldn't be fully verified in code
**Action**: Review "Verification Confidence" section to understand why, may need manual QA review

### "Gaps detected"
**Reason**: Code paths found that have no test coverage
**Action**: Review "Test Coverage Gaps" section and add tests for critical gaps

## Integration with Other Tools

### With Analysis Toolkit
```bash
# Complete workflow
/analyze-jira-issue PROJ-456 --wait
/generate-qa-guide PROJ-456 --from-analysis
# Result: QA guide informed by technical analysis
```

### With Planning Suite
```bash
# Development workflow
/plan "Implement user registration" --detailed
/generate-qa-guide "User Registration"
# Result: Implementation plan + QA testing guide
```

## Advanced Options (Future)

Future versions may include:
- `--template=<name>` - Use predefined test template
- `--coverage=<percent>` - Minimum confidence threshold
- `--export=<format>` - Export to TestRail, Zephyr, etc.
- `--browser-automation` - Generate Selenium/Cypress tests

---

**Command Version**: 1.0.0
**Plugin**: Analysis Toolkit
**Agent**: qa-testing-guide-generator
**Output Location**: marketplace/output/qa-guides/
**Verification**: Full codebase scanning enabled
