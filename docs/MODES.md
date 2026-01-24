# DMG Modes

## Operating Modes for Different Decision Contexts

DMG supports multiple operating modes to match the context, urgency, and complexity of decisions.

---

## Mode Matrix

| Mode | RAMP | Agents | Time | Use Case |
|------|------|--------|------|----------|
| **Express** | 1-2 | Solo | 5 min | Quick tactical choices |
| **Standard** | 3 | 1-3 | 30 min | Regular team decisions |
| **Governed** | 3-4 | 3-7 | 1-3 days | Cross-functional decisions |
| **Strategic** | 4-5 | 5+ | 1-2 weeks | Major commitments |
| **Crisis** | Any | 2-4 | ASAP | Emergency response |

---

## Mode 1: Express

### Characteristics
- **RAMP**: L1-L2
- **Participants**: Solo or 2 people
- **Time**: 5-15 minutes
- **Governance**: Minimal

### When to Use
- Feature flag changes
- Copy/content decisions
- Bug prioritization
- Meeting scheduling
- Small budget (<$500)

### Required Elements
- Title (decision question)
- 3 options (can be brief)
- RAMP level declared
- Outcome check (optional but recommended)

### Express Template

```json
{
  "title": "Should I use pagination or infinite scroll?",
  "options": [
    {"name": "Pagination", "description": "Classic page numbers"},
    {"name": "Infinite", "description": "Load on scroll"},
    {"name": "Hybrid", "description": "Load more button"}
  ],
  "ramp": {"level": 2},
  "recommendation": "Pagination for performance"
}
```

---

## Mode 2: Standard

### Characteristics
- **RAMP**: L3
- **Participants**: 1-3 stakeholders
- **Time**: 30 min - 2 hours
- **Governance**: Basic DISSENT + DOORS

### When to Use
- Sprint priorities
- Hiring decisions (junior)
- Vendor selection (low-medium)
- Process changes
- Feature scope decisions

### Required Elements
- Complete MEMO with context
- ≥3 substantive options
- At least 1 DISSENT
- DOORS checklist complete
- Expected outcomes defined
- Outcome check scheduled

### Standard Process

```
Day 0: Owner creates MEMO, shares for input
Day 1: Stakeholders add options, raise concerns
Day 2: Owner resolves concerns, captures DISSENT
Day 3: Finalize, set outcome check
```

---

## Mode 3: Governed

### Characteristics
- **RAMP**: L3-L4
- **Participants**: 3-7 stakeholders + approvers
- **Time**: 1-3 days
- **Governance**: Full chain

### When to Use
- Architecture decisions
- Team structure changes
- Partnership agreements
- Policy changes
- Budget allocation (medium-large)
- Hiring decisions (senior)

### Required Elements
- Complete MEMO with extensive context
- SPAR deliberation recommended
- Multiple DISSENT captured
- Full DOORS with named owner
- Formal approval chain
- Explicit expected outcomes with confidence
- Scheduled outcome checks

### Governed Process

```
Week 1, Day 1-2: Frame + Initial SPAR
Week 1, Day 3-4: Stakeholder input + DISSENT capture
Week 1, Day 5:   DOORS complete + governance review
Week 2, Day 1:   Approver review
Week 2, Day 2:   Final sign-off
```

### Approval Chain
1. **Owner**: Creates and owns the MEMO
2. **Stakeholders**: Contribute options, dissent
3. **Reviewers**: Verify governance completeness
4. **Approvers**: Final authority sign-off

---

## Mode 4: Strategic

### Characteristics
- **RAMP**: L4-L5
- **Participants**: 5+ stakeholders across functions
- **Time**: 1-2 weeks
- **Governance**: Maximum rigor

### When to Use
- M&A decisions
- Major product pivots
- Market entry/exit
- Org restructures
- Multi-year commitments
- Regulatory compliance

### Required Elements
- Extensive MEMO with full context
- Deep SPAR (8 agents, steelman style)
- Multiple structured DISSENT
- TRACE for all major claims
- Complete DOORS with executive owner
- Multi-phase OUTCOME schedule
- External review (legal, finance, etc.)

### Strategic Process

```
Week 1: Frame + Deep Context
├── Comprehensive situation analysis
├── Stakeholder interviews
└── Initial MEMO draft

Week 2: Deliberate
├── Deep SPAR with 8 agents
├── External expert input
├── Multi-perspective DISSENT capture
└── Evidence gathering (TRACE)

Week 3: Govern
├── DOORS complete with exec owner
├── Legal/finance review
├── Expected outcomes with scenarios
└── Multi-year outcome check schedule

Week 4: Commit
├── Board/executive review
├── Final approvals
└── Communication plan
```

---

## Mode 5: Crisis

### Characteristics
- **RAMP**: Any (context-dependent)
- **Participants**: 2-4 decision-makers
- **Time**: Hours, not days
- **Governance**: Streamlined but documented

### When to Use
- Production outages
- Security incidents
- PR crises
- Market shocks
- Emergency personnel issues

### Crisis Protocol

```
┌─────────────────────────────────────────┐
│ Hour 0: Recognize                       │
│ → Incident declared                     │
│ → Decision owner identified             │
├─────────────────────────────────────────┤
│ Hour 0-1: Assess                        │
│ → Quick RAMP assessment                 │
│ → 2-3 options generated                 │
│ → No "perfect option" paralysis         │
├─────────────────────────────────────────┤
│ Hour 1-2: Decide                        │
│ → Fast SPAR (crisis preset)             │
│ → Key dissent noted (not resolved)      │
│ → DOORS: Who reverses if wrong?         │
├─────────────────────────────────────────┤
│ Hour 2+: Execute                        │
│ → Action begins immediately             │
│ → MOMENT logging in real-time           │
│ → Hourly signal checks                  │
├─────────────────────────────────────────┤
│ Post-Crisis: Document                   │
│ → Full MEMO created retroactively       │
│ → OUTCOME check scheduled               │
│ → Post-mortem learning                  │
└─────────────────────────────────────────┘
```

### Crisis Shortcuts (Allowed)
- Skip lengthy option analysis
- Accept single senior DISSENT
- Simplified DOORS (just owner + signal)
- Shorter outcome check cycle

### Crisis Non-Negotiables (Required)
- Decision owner named
- Key action logged
- Rollback signal defined
- Post-crisis documentation

---

## Mode Transitions

### Escalation (Mode Up)
When a decision becomes more consequential:

```
Express → Standard: Discovered broader impact
Standard → Governed: Found cross-team implications
Governed → Strategic: Identified multi-year commitment
Any → Crisis: Urgent situation emerges
```

### De-escalation (Mode Down)
When context changes:

```
Strategic → Governed: Scope reduced
Governed → Standard: Fewer stakeholders needed
Standard → Express: Lower impact than thought
Crisis → Any: Immediate threat resolved
```

---

## Mode Selection Guide

### Ask These Questions

1. **How long to undo?**
   - Minutes → Express
   - Hours/Days → Standard
   - Weeks → Governed
   - Months/Years → Strategic

2. **Who is affected?**
   - Just me → Express
   - My team → Standard
   - Multiple teams → Governed
   - Whole org/external → Strategic

3. **What's the budget?**
   - <$1K → Express
   - $1K-$50K → Standard
   - $50K-$500K → Governed
   - >$500K → Strategic

4. **What's the time pressure?**
   - Must decide today → Crisis (or Express)
   - This week → Standard
   - This month → Governed
   - Can take time → Strategic

5. **What's the risk profile?**
   - Easily recoverable → Express/Standard
   - Recoverable with effort → Governed
   - Hard to recover → Strategic
   - Immediate danger → Crisis

---

## Mode Configuration Examples

### Express Config
```json
{
  "mode": "express",
  "ramp": {"level": 2},
  "governance": {
    "require_dissent": false,
    "require_doors": false,
    "require_outcome_check": "optional"
  },
  "time_box": "15m"
}
```

### Governed Config
```json
{
  "mode": "governed",
  "ramp": {"level": 4},
  "governance": {
    "require_dissent": true,
    "require_doors": true,
    "require_outcome_check": true,
    "require_approval": ["manager", "domain_lead"]
  },
  "time_box": "3d"
}
```

### Strategic Config
```json
{
  "mode": "strategic",
  "ramp": {"level": 5},
  "governance": {
    "require_dissent": true,
    "require_doors": true,
    "require_outcome_check": true,
    "require_approval": ["director", "legal", "finance", "executive"],
    "require_spar": "deep",
    "require_external_review": true
  },
  "time_box": "14d"
}
```

### Crisis Config
```json
{
  "mode": "crisis",
  "ramp": {"level": "dynamic"},
  "governance": {
    "require_dissent": "simplified",
    "require_doors": "owner_only",
    "require_outcome_check": true,
    "post_crisis_documentation": true
  },
  "time_box": "ASAP"
}
```
