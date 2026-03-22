---
description: "Find similar bug patterns across codebase using pattern analysis"
argument-hint: "<error-pattern> [--report=full|summary]"
allowed-tools: [Bash, Glob, Grep, Read, Write]
---

# Command: /analyze-bug-pattern

## Usage

```
/analyze-bug-pattern <error-pattern> [--report=full|summary] [--similarity-threshold=0.75] [--max-results=20]
```

## Arguments

### Required Arguments

- **error-pattern**: Description of the bug pattern to search for
  - Can be exception type (e.g., "NullReferenceException")
  - Can be code pattern (e.g., "Missing null check on User.Address")
  - Can be structural issue (e.g., "Unclosed database connections")
  - Can be anti-pattern (e.g., "Multiple identical catch blocks")

### Optional Flags

- **--report=full|summary**: Report level (default: `full`)
  - `full`: Comprehensive analysis with all findings and code examples
  - `summary`: Condensed key findings and action items

- **--similarity-threshold=0.0-1.0**: Minimum similarity score (default: `0.75`)
  - Higher values: More strict matching (fewer results, higher confidence)
  - Lower values: More lenient matching (more results, may include false positives)

- **--max-results=N**: Maximum patterns to report (default: `20`)
  - Limits output to top N most similar patterns

## Examples

```bash
# Find all null reference patterns similar to User.Address
/analyze-bug-pattern "NullReferenceException accessing User.Address.City"

# Find validation gaps with summary report
/analyze-bug-pattern "Missing validation on optional navigation properties" --report=summary

# Find resource leaks with strict matching
/analyze-bug-pattern "Database connection not disposed properly" --similarity-threshold=0.85

# Find anti-patterns with limited results
/analyze-bug-pattern "Catch exception without logging" --max-results=10
```

## Implementation

### Step 1: Parse Arguments
- Extract error pattern description
- Extract optional flags
- Set defaults (report=full, threshold=0.75, max-results=20)

### Step 2: Delegate to Agent
Load and execute **codebase-pattern-analyzer** agent with parameters:
- error_pattern: User-provided pattern description
- report_level: full or summary
- similarity_threshold: Numeric threshold
- max_patterns: Maximum results

### Step 3: Execute Agent Process
Agent performs 6-phase analysis:
1. **Pattern Extraction & Formalization** (8-10% of time)
   - Parse pattern description
   - Formalize into searchable characteristics
   - Generate search strategies

2. **Codebase-Wide Pattern Search** (25-30% of time)
   - Execute Grep searches with multiple patterns
   - Find all potential matches
   - Deduplicate and filter results

3. **Similarity Scoring & Ranking** (20-25% of time)
   - Score each match for similarity
   - Rank by similarity score
   - Filter by threshold

4. **Code Context Analysis** (20-25% of time)
   - Read code at each match location
   - Analyze root cause
   - Identify contributing factors

5. **Risk & Impact Assessment** (15-18% of time)
   - Assess risk level for each match
   - Calculate impact metrics
   - Prioritize by risk score

6. **Remediation Recommendations** (12-15% of time)
   - Generate 3-level fix recommendations
   - Provide code examples
   - Estimate effort

### Step 4: Generate Report
Write comprehensive markdown report to:
`marketplace/output/root-cause/bug-pattern-<timestamp>.md`

Report includes:
- Executive summary with key findings
- Pattern definition and search strategy
- All matching locations with similarity scores
- Code context for each match
- Risk assessment and prioritization
- 3-level remediation (quick fix, proper fix, prevention)
- Code examples for solutions
- Implementation guidance

### Step 5: Return Results
Display completion status with:
- Number of patterns found
- Similarity score range
- Risk level distribution
- Report location
- Next steps

## Output Locations

- **Full Report**: `marketplace/output/root-cause/bug-pattern-<timestamp>.md`
- **Summary Report**: `marketplace/output/root-cause/bug-pattern-<timestamp>-summary.md`

## Expected Duration

**Simple Pattern** (e.g., specific null check):
- Pattern extraction: 2 minutes
- Codebase search: 5 minutes
- Scoring: 6 minutes
- Context analysis: 7 minutes
- Risk assessment: 4 minutes
- Remediation: 6 minutes
- **Total**: ~30 minutes

**Complex Pattern** (e.g., anti-pattern across multiple files):
- Pattern extraction: 3 minutes
- Codebase search: 7 minutes
- Scoring: 12 minutes (Sequential Thinking may enable)
- Context analysis: 10 minutes
- Risk assessment: 6 minutes
- Remediation: 8 minutes
- **Total**: ~46 minutes

## Success Criteria

Command is successful when:
- [ ] Pattern description successfully parsed
- [ ] Codebase search executed across all relevant files
- [ ] Similar patterns identified with confidence scores
- [ ] Code context analyzed for each match
- [ ] Risk assessment completed
- [ ] 3-level remediation provided
- [ ] Report generated and saved
- [ ] User receives actionable recommendations

## Output Format

```
# ✓ Bug Pattern Analysis Complete

**Pattern**: NullReferenceException accessing optional navigation properties
**Execution Time**: 30 minutes

## Summary
- **Instances Found**: 12 locations across 6 files
- **Average Similarity**: 87%
- **Risk Level**: 3 HIGH, 6 MEDIUM, 3 LOW
- **Estimated Fix Time**: Quick (2 hrs), Proper (6 hrs), Prevention (9 hrs)

## Top Matches
1. UserService.cs:150 - Similarity: 100% - Risk: HIGH
2. OrderService.cs:234 - Similarity: 98% - Risk: HIGH
3. PaymentService.cs:89 - Similarity: 92% - Risk: HIGH
4. ProfileController.cs:56 - Similarity: 88% - Risk: MEDIUM
5. ReportGenerator.cs:123 - Similarity: 85% - Risk: MEDIUM
... (7 more)

## Output Files
- **Full Analysis**: marketplace/output/root-cause/bug-pattern-20260116-115023.md
- **Summary**: marketplace/output/root-cause/bug-pattern-20260116-115023-summary.md

## Recommended Action
1. Review top 3 HIGH-risk matches (UserService, OrderService, PaymentService)
2. Apply Quick Fix (2 hours) for immediate production safety
3. Schedule Proper Fix (6 hours) for next sprint
4. Plan Prevention Strategy (9 hours) as technical debt initiative

## Next Steps
- Implement fixes using code examples from report
- Add unit tests for null scenarios
- Update code review checklist
- Monitor for similar patterns in future code
```

## FAQ

**Q: How accurate is pattern matching?**
A: 90%+ accuracy with default threshold (0.75). Adjust --similarity-threshold for stricter/looser matching.

**Q: Will it find patterns in test files?**
A: No by default (test files excluded). Configure in settings if needed.

**Q: How many patterns will it find?**
A: Depends on codebase size and pattern prevalence. Limited to --max-results (default: 20).

**Q: Can I run this proactively?**
A: Yes! Run after finding any bug to catch similar issues before they surface.

**Q: What if pattern description is vague?**
A: Agent will attempt broad search and may request clarification for better results.

**Q: How long does it take?**
A: 20-40 minutes depending on pattern complexity and codebase size.

## Integration with Other Commands

### After Bug Discovery
```bash
# Step 1: Analyze single error
/analyze-stacktrace

# Step 2: Find similar patterns
/analyze-bug-pattern "Pattern identified from stack trace"

# Step 3: Fix all instances
# ... apply recommendations from report ...
```

### Before Code Review
```bash
# Proactively find potential issues
/analyze-bug-pattern "Missing null checks on optional properties"

# Address findings before submitting PR
/review-local-pr feature-branch
```

### After Deployment Issue
```bash
# Find all instances of production bug
/analyze-bug-pattern "Pattern from production error"

# Identify when it was introduced
/find-regression "Feature affected by bug"

# Fix comprehensively
# ... apply prevention strategy from report ...
```

## Related Commands

- `/analyze-stacktrace` - Analyze single error in detail
- `/find-regression` - Find when bug was introduced
- `/correlate-errors` - Find common root cause across errors
- `/refactor-code` - Improve code quality after identifying patterns

---

**Command Version**: 2.0.0
**Last Updated**: 2026-01-16
**Delegated To**: codebase-pattern-analyzer agent
**Expected Duration**: 20-40 minutes
**MCP Requirements**: None (local analysis only)
