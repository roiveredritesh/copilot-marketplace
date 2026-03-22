---
allowed-tools: [Task, Read, Write, Grep, Glob, Bash]
argument-hint: <topic> [--async|--wait] [--depth=shallow|medium|deep]
description: Brainstorm innovative feature ideas with impact analysis
---

# Command: /brainstorm-feature

Generates and explores innovative feature ideas with user impact analysis, implementation complexity assessment, and strategic recommendations.

## Usage

```
/brainstorm-feature <topic> [--async|--wait] [--depth=shallow|medium|deep]
```

## Arguments

### Required Arguments

- **topic**: The feature topic or area to brainstorm
  - `/brainstorm-feature "user authentication"`
  - `/brainstorm-feature "real-time notifications"`
  - `/brainstorm-feature "advanced search capabilities"`
  - `/brainstorm-feature "mobile app support"`

### Optional Flags

- **--async**: Execute in background (good for comprehensive brainstorming)
- **--wait**: Execute synchronously (default, waits for completion)
- **--depth**: Analysis depth
  - `shallow`: Quick ideas, 5-10 minutes
  - `medium`: Balanced ideas with assessment (default, 10-15 minutes)
  - `deep`: Comprehensive exploration with detailed analysis, 15-25 minutes

## Examples

```bash
# Quick feature brainstorming (synchronous, medium depth)
/brainstorm-feature "user authentication"

# In-depth brainstorming in background
/brainstorm-feature "advanced search capabilities" --async --depth=deep

# Quick shallow ideas
/brainstorm-feature "mobile app support" --depth=shallow

# Medium depth in background
/brainstorm-feature "real-time notifications" --async
```

## How It Works

The agent will:

1. **Understand Context**: Analyze the feature topic and domain
2. **Generate Ideas**: Create 5-8 innovative feature variations
3. **Assess Each Idea**:
   - User impact and value
   - Implementation complexity (1-5 scale)
   - Time estimate
   - Resource requirements
   - Risk assessment
   - Scalability considerations
4. **Identify Gaps**: Find missing opportunities
5. **Provide Recommendations**: Suggest best approaches based on trade-offs
6. **Create Action Items**: Next steps for implementation

## Output Locations

- Brainstorming session: `marketplace/output/brainstorming/<topic>-ideas.md`
- Feature comparison: `marketplace/output/brainstorming/<topic>-comparison.md`
- Recommendations: `marketplace/output/brainstorming/<topic>-recommendations.md`

## Typical Brainstorming Time

- Shallow: 5-10 minutes
- Medium: 10-15 minutes (default)
- Deep: 15-25 minutes

**Recommendation**: Use `--async` for deep analysis to avoid blocking your workflow.

## Output Format

The brainstorming session includes:

- **Topic Summary**: Context and scope
- **Generated Ideas**: 5-8 feature variations with descriptions
- **Idea Assessment Table**:
  - User Impact (High/Medium/Low)
  - Implementation Complexity (1-5)
  - Time Estimate
  - Risk Level
  - Scalability Rating
- **Trade-offs Analysis**: Pros and cons of each approach
- **Gap Analysis**: Missing opportunities and considerations
- **Recommendations**: Top 2-3 recommended approaches with rationale
- **Action Items**: Next steps for implementation
- **Related Features**: How ideas connect to existing features
- **Timeline Estimates**: Implementation timeline for recommended approach

## Implementation Notes

This command delegates to the `feature-ideation-agent` which:
- Researches the feature domain
- Generates creative, innovative ideas
- Assesses feasibility and impact
- Provides structured recommendations
- Saves comprehensive brainstorming report
