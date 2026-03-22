# Brainstorming Suite Plugin - Changelog

All notable changes to this plugin will be documented in this file.

## [2.0.0] - 2026-01-15

### Changed
- **BREAKING**: Migrated to shared skills library for better maintainability
- Updated all agent specifications to latest template with enhanced error handling
- Improved Sequential Thinking integration across all agents

### Added
- Reference to shared skill: `technical-writing-guide` for ideation documentation standards
- Enhanced agent documentation with detailed process phases
- Improved brainstorming templates
- Better documentation standards for ideation outputs

### Improved
- All agents now follow standardized specification template
- Enhanced brainstorming methodologies
- Better integration with shared documentation standards
- Consistent output format across all agents
- Updated documentation with v2.0.0 features
- Sequential Thinking now conditional for complex scenarios

### Migration Notes
- Skills now referenced from `../../shared-skills/` directory
- No changes to command interface - all commands work identically
- Existing outputs remain compatible
- Brainstorming outputs enhanced with documentation standards

## [1.0.0] - 2025-10-30

### Added

#### Agents

**feature-ideation-agent** - Feature brainstorming and ideation
- Generates innovative feature ideas with user impact analysis
- Explores multiple feature concepts and variations
- Analyzes feasibility and value propositions
- Provides implementation considerations

**architecture-explorer-agent** - Architecture exploration
- Explores multiple architectural approaches and design patterns
- Compares architecture options with trade-offs
- Evaluates scalability and maintainability
- Provides pattern recommendations

**problem-solver-agent** - Problem-solving brainstorming
- Collaborative exploration of technical solutions
- Multiple solution approaches with analysis
- Trade-off evaluation
- Implementation guidance

**code-alternatives-agent** - Code implementation alternatives
- Generates multiple code implementations for requirements
- Compares approaches with pros/cons
- Analyzes performance and maintainability
- Provides recommendations

#### Commands

**/brainstorm-feature** - Brainstorm feature ideas
- Syntax: `/brainstorm-feature <context>`
- Generates creative feature concepts
- Async support enabled

**/brainstorm-architecture** - Explore architectural approaches
- Syntax: `/brainstorm-architecture <requirements>`
- Compares architecture options
- Async support enabled

**/solve-problem** - Collaborative problem-solving
- Syntax: `/solve-problem <problem-description>`
- Multiple solution approaches
- Async support enabled

**/generate-alternatives** - Code implementation alternatives
- Syntax: `/generate-alternatives <requirement>`
- Multiple code approaches with analysis
- Async support enabled

### Features

- **Creative Ideation**: Multiple innovative approaches for features and architecture
- **Comparative Analysis**: Side-by-side comparison of alternatives
- **Trade-off Evaluation**: Detailed pros/cons for each option
- **Implementation Guidance**: Practical next steps for chosen approach
- **Async Support**: Background processing for complex brainstorming
- **Flexible Output**: Detailed brainstorming reports with recommendations

### Documentation

- **plugin.json**: Plugin metadata and configuration
- Each agent has detailed process documentation
- Each command has usage examples

### Output Structure

- Reports: `marketplace/output/brainstorming/`
- Report formats: Comprehensive markdown with analysis

### Integration Points

- Works standalone or with other plugins
- Complements planning and development suites
- Supports creative exploration before implementation

---

**Last Updated**: 2026-01-15
**Maintainer**: Claude Code Marketplace
**License**: MIT
