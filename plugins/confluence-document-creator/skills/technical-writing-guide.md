# Technical Writing Guide

**Version**: 2.0.0
**Plugin**: confluence-document-creator
**Purpose**: Best practices for technical writing including clarity, structure, and audience considerations

## Overview

This skill provides comprehensive guidelines for writing clear, effective technical documentation. Use these principles when generating any technical content - API docs, architecture documentation, runbooks, or release notes.

## Core Principles

### 1. Know Your Audience
- **Developers**: Assume technical knowledge, focus on implementation details
- **Operations**: Focus on procedures, troubleshooting, and monitoring
- **Stakeholders**: High-level overview, business impact, strategic decisions
- **End Users**: Simple language, focus on tasks and outcomes

### 2. Be Clear and Concise
- Use simple, direct language
- Avoid jargon unless necessary (and define it when used)
- One idea per sentence
- Remove unnecessary words
- Get to the point quickly

### 3. Be Accurate
- Verify all technical details
- Test all code examples
- Keep documentation synchronized with code
- Update documentation when code changes
- Include version numbers

### 4. Be Consistent
- Use consistent terminology
- Follow consistent structure
- Use consistent formatting
- Maintain consistent tone
- Apply consistent style rules

### 5. Be Complete
- Cover all necessary information
- Anticipate questions
- Provide context
- Include examples
- Link to related documentation

## Writing Style

### Active Voice
**Good**: "The system processes the request"
**Bad**: "The request is processed by the system"

**Good**: "Click the Save button"
**Bad**: "The Save button should be clicked"

### Present Tense
**Good**: "The API returns a JSON response"
**Bad**: "The API will return a JSON response"

### Second Person
**Good**: "You can configure the timeout value"
**Bad**: "One can configure the timeout value" or "The user can configure..."

### Imperative Mood (for procedures)
**Good**: "Run the deployment script"
**Bad**: "You should run the deployment script"

## Sentence Structure

### Keep Sentences Short
**Good**: "The API validates input parameters. Invalid parameters return a 400 error."
**Bad**: "The API validates input parameters and if they are invalid, it returns a 400 error response to indicate that the request cannot be processed."

### One Idea Per Sentence
**Good**: "Save your changes. Click the Submit button."
**Bad**: "Save your changes and then click the Submit button to submit the form."

### Avoid Complex Sentences
**Good**: "Install Node.js before running the application. Download it from nodejs.org."
**Bad**: "Before running the application, which requires Node.js, you should install it by downloading from nodejs.org."

## Word Choice

### Use Simple Words
| Instead of | Use |
|------------|-----|
| utilize | use |
| implement | do, make |
| in order to | to |
| for the purpose of | to, for |
| at this point in time | now |
| due to the fact that | because |
| in the event that | if |
| subsequent to | after |

### Be Specific
**Good**: "The request times out after 30 seconds"
**Bad**: "The request times out after a while"

**Good**: "Restart the service using: systemctl restart nginx"
**Bad**: "Restart the service"

### Avoid Ambiguity
**Good**: "Enter your username (3-50 characters)"
**Bad**: "Enter your username (must be appropriate length)"

**Good**: "Click the blue Submit button in the top right corner"
**Bad**: "Click the button"

## Technical Content

### Code Examples
```
✅ DO:
- Include complete, working examples
- Add comments to explain complex logic
- Use realistic variable names
- Show expected output
- Format code properly

❌ DON'T:
- Show incomplete code
- Use foo, bar, baz without context
- Assume knowledge of uncommon syntax
- Skip error handling
- Show untested code
```

**Example**:
```csharp
// Good: Complete, realistic example
var client = new HttpClient();
client.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", apiToken);

try
{
    var response = await client.GetAsync("https://api.example.com/users");
    response.EnsureSuccessStatusCode();
    var users = await response.Content.ReadAsAsync<List<User>>();
    return users;
}
catch (HttpRequestException ex)
{
    _logger.LogError(ex, "Failed to fetch users from API");
    throw;
}
```

### API Documentation
```
✅ DO:
- Document all parameters (type, required/optional, default, constraints)
- Show request and response examples
- Document error codes and meanings
- Include authentication requirements
- Provide working code examples

❌ DON'T:
- Assume parameter types are obvious
- Skip error documentation
- Only show happy path
- Use vague descriptions like "data object"
```

### Procedures
```
✅ DO:
- Number steps in sequence
- Start each step with action verb
- Include verification steps
- Show expected results
- Provide troubleshooting for common issues

❌ DON'T:
- Skip steps assuming prior knowledge
- Use vague instructions
- Forget to mention prerequisites
- Omit verification
```

**Example**:
```markdown
## Deploying the Application

### Prerequisites
- Node.js 18+ installed
- Database connection configured
- Environment variables set

### Deployment Steps

1. **Stop the current application**
   ```bash
   pm2 stop myapp
   ```
   Expected output: `[PM2] Process stopped`

2. **Pull latest code**
   ```bash
   git pull origin main
   ```
   Verify: Check that commit hash matches production branch

3. **Install dependencies**
   ```bash
   npm ci --production
   ```
   This may take 2-3 minutes

4. **Run database migrations**
   ```bash
   npm run migrate
   ```
   Expected output: `Migrations complete: 3 applied`

5. **Start the application**
   ```bash
   pm2 start myapp
   ```

6. **Verify deployment**
   ```bash
   curl https://myapp.example.com/health
   ```
   Expected response: `{"status": "healthy"}`

### Troubleshooting

**Issue**: Migration fails with "connection refused"
**Solution**: Verify DATABASE_URL environment variable is set correctly
```

## Structure and Organization

### Information Hierarchy
```
# Page Title (H1)
## Major Section (H2)
### Subsection (H3)
#### Detail Level (H4)

Don't skip levels: H2 → H4 is wrong
```

### Progressive Disclosure
Start with high-level overview, then provide details:

```markdown
## Overview
[What it is, why it matters - 2-3 sentences]

## Quick Start
[Minimal steps to get started]

## Detailed Usage
[Comprehensive information]

## Advanced Topics
[Edge cases, optimization, internals]
```

### Logical Flow
Organize content in logical order:
1. Context (what/why)
2. Prerequisites (what you need)
3. Instructions (how to do it)
4. Verification (how to confirm)
5. Troubleshooting (what if it fails)
6. Next steps (what to do after)

## Common Mistakes to Avoid

### 1. Assuming Knowledge
**Bad**: "Configure the JWT middleware"
**Good**: "Configure JWT (JSON Web Token) authentication middleware to secure API endpoints"

### 2. Using Jargon Without Context
**Bad**: "The SPA uses SSR with hydration"
**Good**: "The Single Page Application (SPA) uses Server-Side Rendering (SSR), which generates HTML on the server and then hydrates it on the client for interactivity"

### 3. Vague Descriptions
**Bad**: "Improve performance"
**Good**: "Reduce API response time from 500ms to 150ms by implementing Redis caching"

### 4. Inconsistent Terminology
**Bad**: "User" in one section, "Account" in another, "Customer" in a third
**Good**: Choose one term and use it consistently

### 5. Wall of Text
**Bad**: Long paragraphs without breaks, headings, or lists
**Good**: Short paragraphs (3-4 sentences), headings, bulleted lists, code blocks

### 6. Missing Context
**Bad**: "Run the script"
**Good**: "Run the deployment script to deploy the application to production. This script connects to the server, pulls latest code, and restarts the service."

## Documentation Types

### API Documentation
- Focus on: Endpoints, parameters, responses, errors
- Audience: Developers integrating with API
- Include: Complete working examples, all error codes
- Tone: Technical, precise

### Architecture Documentation
- Focus on: System structure, components, data flow
- Audience: Developers, architects, stakeholders
- Include: Diagrams, design decisions, trade-offs
- Tone: Technical but accessible

### Runbooks
- Focus on: Procedures, troubleshooting, operations
- Audience: Operations team, on-call engineers
- Include: Step-by-step instructions, commands, verification
- Tone: Procedural, action-oriented

### Release Notes
- Focus on: Changes, new features, breaking changes
- Audience: Developers, users, stakeholders
- Include: What changed, why it matters, how to upgrade
- Tone: Informative, user-focused

## Accessibility

### Plain Language
- Use common words
- Define technical terms
- Explain acronyms on first use
- Keep sentences short
- Use lists for multiple items

### Readable Formatting
- Use headings to break content
- Use bulleted/numbered lists
- Use tables for structured data
- Use code blocks for code
- Use white space effectively

### Universal Design
- Don't rely on color alone (e.g., "click the red button")
- Provide alt text for images
- Use descriptive link text ("view the API documentation" not "click here")
- Ensure sufficient contrast
- Use semantic structure

## Review Checklist

Before publishing documentation:

**Content**
- [ ] Accurate and up-to-date
- [ ] Complete (covers all necessary information)
- [ ] Appropriate for audience
- [ ] Provides context and rationale
- [ ] Includes examples where helpful

**Style**
- [ ] Active voice used
- [ ] Present tense used
- [ ] Simple, clear language
- [ ] Consistent terminology
- [ ] Concise (no unnecessary words)

**Structure**
- [ ] Logical organization
- [ ] Clear headings
- [ ] Table of contents (if long)
- [ ] Related documentation linked
- [ ] Progressive disclosure

**Technical**
- [ ] Code examples tested
- [ ] Commands verified
- [ ] Links working
- [ ] Version numbers correct
- [ ] Prerequisites listed

**Format**
- [ ] Proper heading hierarchy
- [ ] Code blocks formatted with language
- [ ] Tables formatted correctly
- [ ] Lists used appropriately
- [ ] Consistent formatting throughout

**Accessibility**
- [ ] Plain language used
- [ ] Acronyms defined
- [ ] Alt text for images
- [ ] Descriptive link text
- [ ] Good contrast and readability

## Resources

### Style Guides
- Google Developer Documentation Style Guide
- Microsoft Writing Style Guide
- Apple Style Guide

### Tools
- Hemingway Editor (readability)
- Grammarly (grammar and style)
- Vale (automated style checking)
- LanguageTool (grammar checking)

### Best Practice References
- Docs as Code philosophy
- Diátaxis documentation framework
- Plain Language guidelines

---

**Guide Version**: 2.0.0
**Last Updated**: 2026-01-16
**Usage**: Apply these principles to all technical writing
