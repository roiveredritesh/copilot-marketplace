---
template-name: architecture-change
description: Template for planning architectural modifications and major system changes
applies-to: [architecture-change, design-pattern-change, system-redesign, infrastructure-change]
required-inputs: [current-architecture, target-architecture, migration-constraints]
---

# Template: Architecture Change Planning

## When to Use
Use this template for significant architectural changes, pattern migrations, or system redesigns.

**Examples**:
- Migrate monolithic architecture to microservices
- Implement CQRS pattern
- Switch ORM from Entity Framework to Dapper
- Change authentication mechanism (Windows to OAuth)

## Required Inputs

1. **Current Architecture**: How system currently works
2. **Target Architecture**: How it should work
3. **Migration Constraints**: Timeline, backward compatibility needs, etc.

## Planning Structure

### Phase 1: Architecture Assessment (2-4 hours)

**Current State Analysis**:
- Document current architecture
- Identify components
- Map dependencies
- Understand pain points
- Identify constraints

**Create**:
- Architecture diagram (ASCII or description)
- Component dependency list
- Risk areas identification

**Example Documentation**:
```
Current Architecture:
- Monolithic ASP.NET WebForms application
- Single database
- Synchronous data access
- All logic in code-behind
- Direct database coupling

Pain Points:
- Hard to test
- Can't scale components independently
- Difficult to modify without affecting whole system
```

### Phase 2: Target Architecture Design (3-6 hours)

**Define Target**:
- New component structure
- Layered architecture (API, Service, Data)
- Design patterns to use
- Technology choices
- Dependencies between new components

**Create**:
- New architecture diagram
- Component interactions
- Technology stack
- Trade-off analysis

**Example Target**:
```
Target Architecture:
- Separated layers (Presentation, API, Business, Data)
- Repository pattern for data access
- Dependency injection for loose coupling
- Async/await for non-blocking I/O
- Clean separation of concerns

Benefits:
- Easier to test (mock dependencies)
- Can evolve components independently
- Better performance (async)
- Cleaner code structure
```

### Phase 3: Impact Analysis (2-3 hours)

**Assess**:
- What breaks with new architecture
- Breaking changes needed
- Backward compatibility requirements
- Client impact (if API change)
- Database migration needs

**Output**: Breaking changes list with severity

### Phase 4: Migration Strategy (2-3 hours)

**Plan approach**:

**Option A: Big Bang Migration**
- Rewrite everything at once
- Pros: Clean, no transition code
- Cons: Risky, long implementation

**Option B: Strangler Pattern**
- New architecture alongside old
- Gradually route requests to new
- Maintain both temporarily
- Phase out old
- Pros: Lower risk, can test in production
- Cons: More code, longer timeline

**Option C: Parallel Systems**
- New system for new features only
- Old system continues
- Eventually decommission old
- Pros: Can run independently
- Cons: Data synchronization needed

**Choose and document approach**

### Phase 5: Component Transition Plan (4-8 hours)

**For each component**, plan:
1. New component design
2. New implementation
3. Transition approach (one at a time or batch)
4. Testing strategy
5. Rollback plan

**Phased approach example**:
```
Phase 1: Create Repository layer (without removing direct queries)
Phase 2: Create Service layer (routes through new services)
Phase 3: Update Controllers/Pages (use new services)
Phase 4: Remove direct database access (cleanup)
Phase 5: Verify and optimize
```

### Phase 6: Database Migration Planning (1-3 hours)

**If schema changes**:
- Document schema changes
- Create migration scripts
- Plan data migration
- Backup strategy
- Rollback procedure

**Example**:
```
Migration Steps:
1. Add new columns to support new structure
2. Populate new columns from old data
3. Update queries to use new columns
4. Verify data integrity
5. Drop old columns (in future migration)
```

### Phase 7: Testing Strategy (2-4 hours)

**Test Plan**:
- Unit test new components
- Integration test component interactions
- End-to-end test workflows
- Performance test new architecture
- Backward compatibility tests (if needed)

**Risk Areas**: Extra testing in areas where changes are big

### Phase 8: Performance Validation (1-2 hours)

**Compare**:
- Performance before and after
- Memory usage
- Database load
- API response time

**Success**: Performance equals or better than before

### Phase 9: Deployment Strategy (1-2 hours)

**Plan**:
- Deployment order
- Rollback procedure
- Monitoring plan
- Communication plan

**Considerations**:
- Minimize downtime
- Validate each step
- Customer/user notification
- Support team readiness

### Phase 10: Decommissioning Plan (30 min - 1 hour)

**Plan**:
- When to remove old code
- Data cleanup
- Documentation updates
- Team training

## Phasing Recommendation

For large architecture changes, phase over time:

```
Week 1: Layer foundation (Repository, Service interfaces)
Week 2: Implement services for 1-2 main features
Week 3: Implement services for remaining features
Week 4: Update Controllers/Pages
Week 5: Testing and stabilization
Week 6: Gradual rollout to production
Week 7: Monitor and optimize
Week 8: Cleanup old code
```

## Risk Management

**Major Risks**:
- **Scope Creep**: Adding features during migration
- **Timeline Slip**: Architecture changes take longer
- **Performance Regression**: New design is slower
- **Data Loss**: Migration issues
- **Breaking Changes**: Clients can't upgrade

**Mitigation**:
- Detailed planning upfront
- Test thoroughly
- Parallel systems during transition
- Gradual rollout
- Monitoring and quick rollback ability

## Success Criteria

- [ ] New architecture designed and documented
- [ ] All breaking changes identified
- [ ] Migration strategy clear
- [ ] Phasing plan complete
- [ ] Component transition plans done
- [ ] Database migration planned (if needed)
- [ ] Testing strategy comprehensive
- [ ] Performance acceptable
- [ ] Deployment plan ready
- [ ] Team trained
- [ ] Documentation updated
- [ ] Monitoring in place

## Documentation Required

- [ ] Architecture diagrams (current and target)
- [ ] Component interaction documentation
- [ ] Breaking changes list
- [ ] Migration guide
- [ ] Testing plan
- [ ] Deployment checklist
- [ ] Rollback procedures
- [ ] API documentation (if API changes)
- [ ] Developer guide for new patterns

## Timeline Estimation

| Activity | Effort | Timeline |
|----------|--------|----------|
| Architecture Design | 2-4 weeks | Parallel with other work |
| Component Development | 4-12 weeks | Depends on size |
| Testing | 2-4 weeks | Parallel with development |
| Deployment | 1-2 weeks | Gradual rollout |
| Stabilization | 2-4 weeks | Monitoring and optimization |
| **Total** | **2-4 months** | - |

## Common Architecture Patterns

### Pattern: Layered Architecture
```
Presentation Layer (UI)
    ↓
API/Controller Layer
    ↓
Service/Business Layer
    ↓
Data Access Layer (Repository)
    ↓
Database
```

### Pattern: CQRS (Command Query Responsibility Segregation)
```
Commands (Write) → Service → Database
    ↓
Queries (Read) → Query Handler → View/Cache
```

### Pattern: Event-Driven Architecture
```
Event Producers → Event Bus/Queue → Event Handlers
```

## Questions to Ask

1. **Why**: Why does current architecture not work?
2. **Pain**: What specific pain does new architecture solve?
3. **Cost**: Is benefit worth migration cost?
4. **Timeline**: How long can this take?
5. **Resources**: Who will do the work?
6. **Rollback**: Can we roll back if needed?
7. **Performance**: Will it be faster/better?

---

**Template Version**: 1.0.0
**Complexity**: Very High
**Typical Effort**: 2-4 months
**Risk Level**: Very High
**Recommendation**: Use phased approach, not big bang
**Key Factor**: Comprehensive planning critical
