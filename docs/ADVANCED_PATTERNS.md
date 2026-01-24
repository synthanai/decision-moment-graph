# DMG Advanced Patterns

## Sophisticated Usage Patterns for Complex Decision Scenarios

This document covers advanced patterns for organizations with mature DMG adoption.

---

## Pattern 1: Decision Cascades

### Problem
One decision triggers multiple dependent decisions.

### Pattern
Create a **decision tree** where parent decisions spawn child MEMOs.

```
┌─────────────────────────────────────────┐
│ MEMO: Should we enter the EU market?   │
│ (Strategic, RAMP L5)                    │
├─────────────────────────────────────────┤
│ Outcome: YES                            │
│ Spawns:                                 │
├─────────────────────────────────────────┤
│  ├── MEMO: Which country first?         │
│  │   (Governed, RAMP L4)               │
│  │   └── Outcome: Germany               │
│  │       └── MEMO: Office or remote?    │
│  │           (Standard, RAMP L3)       │
│  │                                       │
│  ├── MEMO: Hire locally or relocate?    │
│  │   (Governed, RAMP L4)               │
│  │                                       │
│  └── MEMO: Which legal entity?          │
│      (Strategic, RAMP L5)              │
└─────────────────────────────────────────┘
```

### Implementation
```json
{
  "memo_id": "dmg-child-001",
  "title": "Which EU country should we enter first?",
  "context": {
    "parent_decision": "dmg-parent-001",
    "depends_on": ["dmg-parent-001"],
    "unlocked_by": "EU market entry approved on 2026-01-15"
  }
}
```

### Best Practices
- Parent decision must be Final before child can be Final
- Child inherits minimum RAMP of parent (can be higher, not lower)
- Reversing parent may invalidate children

---

## Pattern 2: Parallel Deliberation

### Problem
Multiple stakeholders need to deliberate independently before synthesis.

### Pattern
Run multiple SPAR sessions, then merge into unified MEMO.

```
┌─────────────────────────────────────────┐
│ Question: Should we rewrite the core?   │
├─────────────────────────────────────────┤
│                                          │
│  ┌─────────────┐  ┌─────────────┐       │
│  │ Engineering │  │ Product     │       │
│  │ SPAR        │  │ SPAR        │       │
│  │ (8 agents)  │  │ (4 agents)  │       │
│  └──────┬──────┘  └──────┬──────┘       │
│         │                │               │
│         └────────┬───────┘               │
│                  ▼                       │
│         ┌─────────────┐                  │
│         │ Synthesis   │                  │
│         │ SPAR        │                  │
│         │ (positions  │                  │
│         │ from both)  │                  │
│         └─────────────┘                  │
│                  ▼                       │
│         ┌─────────────┐                  │
│         │ Unified     │                  │
│         │ MEMO        │                  │
│         └─────────────┘                  │
│                                          │
└─────────────────────────────────────────┘
```

### Implementation
```json
{
  "memo_id": "dmg-unified-001",
  "deliberation_sources": [
    {
      "source_type": "spar",
      "spar_id": "spar-eng-001",
      "perspective": "Engineering",
      "key_positions": ["rewrite enables scaling", "risk of 6-month blackout"]
    },
    {
      "source_type": "spar",
      "spar_id": "spar-product-001",
      "perspective": "Product",
      "key_positions": ["customers need stability", "rewrite enables new features"]
    }
  ],
  "synthesis_method": "cross-functional SPAR with representatives"
}
```

---

## Pattern 3: Conditional Branching

### Problem
Decision outcome depends on external events not yet resolved.

### Pattern
Create **conditional branches** with different paths.

```
┌─────────────────────────────────────────┐
│ MEMO: Should we launch feature X?       │
├─────────────────────────────────────────┤
│ Branches:                                │
│                                          │
│ IF competitor launches first:            │
│   → Fast-follow strategy (MEMO-A)        │
│                                          │
│ IF we launch first:                      │
│   → Premium positioning (MEMO-B)         │
│                                          │
│ IF market shifts to Y:                   │
│   → Pivot to Y (MEMO-C)                  │
│                                          │
│ Current State: Watching competitor       │
└─────────────────────────────────────────┘
```

### Implementation
```json
{
  "memo_id": "dmg-conditional-001",
  "title": "Feature X launch strategy",
  "conditional_branches": [
    {
      "condition": "Competitor launches first",
      "trigger_signal": "competitor_feature_release",
      "action_memo": "dmg-fast-follow-001",
      "status": "monitoring"
    },
    {
      "condition": "We launch first",
      "trigger_signal": "our_feature_ready",
      "action_memo": "dmg-premium-001",
      "status": "preparing"
    }
  ],
  "monitoring": {
    "check_frequency": "weekly",
    "signals": ["competitor_blog", "competitor_changelog", "market_reports"]
  }
}
```

---

## Pattern 4: Rolling Decisions

### Problem
Decision needs to be made repeatedly (e.g., quarterly planning).

### Pattern
Create a **decision template** that generates new MEMOs each cycle.

```
┌─────────────────────────────────────────┐
│ Template: Quarterly OKR Setting          │
├─────────────────────────────────────────┤
│ Generates:                               │
│                                          │
│ Q1 2026 → MEMO-Q1-26 (Final)            │
│           └── Outcome check: Q2         │
│                                          │
│ Q2 2026 → MEMO-Q2-26 (Final)            │
│           └── References Q1 learning    │
│           └── Outcome check: Q3         │
│                                          │
│ Q3 2026 → MEMO-Q3-26 (Draft)            │
│           └── References Q1+Q2 learning │
└─────────────────────────────────────────┘
```

### Implementation
```json
{
  "template_id": "tmpl-quarterly-okrs",
  "name": "Quarterly OKR Setting",
  "frequency": "quarterly",
  "base_memo": {
    "title_pattern": "{quarter} {year} OKRs",
    "ramp": {"level": 4},
    "required_fields": ["options", "expected_outcomes", "dissent"],
    "outcome_check_offset": "+90d"
  },
  "learning_aggregation": {
    "include_previous_outcomes": 4,
    "highlight_calibration_drift": true
  },
  "instances": [
    {"period": "Q1 2026", "memo_id": "dmg-okr-q1-26", "state": "Final"},
    {"period": "Q2 2026", "memo_id": "dmg-okr-q2-26", "state": "Final"},
    {"period": "Q3 2026", "memo_id": "dmg-okr-q3-26", "state": "Draft"}
  ]
}
```

---

## Pattern 5: Red Team Review

### Problem
Need adversarial review before high-stakes commitment.

### Pattern
Assign a **Red Team** to challenge the decision.

```
┌─────────────────────────────────────────┐
│ MEMO: Acquire company X for $50M        │
├─────────────────────────────────────────┤
│ State: Proposed                          │
│                                          │
│ Before → Approved:                       │
│                                          │
│ ┌─────────────────────────────────────┐ │
│ │ Red Team Review                     │ │
│ ├─────────────────────────────────────┤ │
│ │ Assigned: CFO, External Advisor     │ │
│ │                                     │ │
│ │ Mission:                            │ │
│ │ - Find 5 reasons this could fail    │ │
│ │ - Challenge every assumption        │ │
│ │ - Propose alternative valuations    │ │
│ │ - Identify hidden liabilities       │ │
│ │                                     │ │
│ │ Output: Red Team Report             │ │
│ │         → Added as DISSENT block    │ │
│ │         → Each concern addressed    │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ After Red Team → State: Approved         │
└─────────────────────────────────────────┘
```

### Implementation
```json
{
  "memo_id": "dmg-acquisition-001",
  "red_team_review": {
    "required": true,
    "assignees": ["cfo@company.com", "advisor@external.com"],
    "mission": "Adversarial review before final approval",
    "deliverables": [
      "5 failure scenarios",
      "Alternative valuation",
      "Hidden liability scan",
      "Market risk assessment"
    ],
    "status": "in_progress",
    "due_date": "2026-02-01"
  },
  "red_team_report": {
    "submitted_at": "2026-02-01T10:00:00Z",
    "concerns": [
      {
        "concern": "Customer concentration risk - 40% revenue from 2 customers",
        "severity": "high",
        "mitigation": "Negotiate retention bonuses for key account managers",
        "addressed": true
      }
    ]
  }
}
```

---

## Pattern 6: Pre-Mortem

### Problem
Need to surface hidden failure modes before commitment.

### Pattern
Assume the decision **failed**. Work backwards to identify causes.

```
┌─────────────────────────────────────────┐
│ Decision: Launch new product line       │
├─────────────────────────────────────────┤
│                                          │
│ Pre-Mortem Exercise (SPAR --premortem)  │
│                                          │
│ "It's 1 year from now. The product      │
│  launch was a disaster. What happened?" │
│                                          │
│ Failure Modes Identified:                │
│                                          │
│ 1. Manufacturing delays (3 agents)      │
│    → Mitigation: Dual supplier strategy │
│                                          │
│ 2. Customer confusion (2 agents)        │
│    → Mitigation: Clear positioning docs │
│                                          │
│ 3. Sales cannibalization (2 agents)     │
│    → Mitigation: Tiered pricing         │
│                                          │
│ 4. Competitor response (1 agent)        │
│    → Mitigation: Speed to market        │
│                                          │
│ Each failure mode → DISSENT + DOORS     │
│                                          │
└─────────────────────────────────────────┘
```

### SPAR Pre-Mortem Command
```bash
/sparkit --challenge --style=premortem "We launched the new product line and it failed spectacularly. Why?"
```

---

## Pattern 7: Calibration Tracking

### Problem
Individual and team judgment needs continuous improvement.

### Pattern
Track prediction accuracy over time for calibration.

```
┌─────────────────────────────────────────┐
│ Calibration Dashboard                    │
├─────────────────────────────────────────┤
│                                          │
│ Decision Maker: @naveen                  │
│ Period: Last 12 months                   │
│ Decisions Finalized: 47                  │
│ Outcome Checks Complete: 39              │
│                                          │
│ Calibration Scores:                      │
│ ┌─────────────────────────────────────┐ │
│ │ Confidence | Predicted | Actual    │ │
│ ├─────────────────────────────────────┤ │
│ │ 50%        | 12        | 7 (58%)   │ │
│ │ 70%        | 18        | 11 (61%)  │ │
│ │ 90%        | 9         | 8 (89%)   │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ Insight: Overconfident at 70% tier       │
│ Action: Increase skepticism for medium   │
│         confidence predictions           │
│                                          │
│ Trend: Improving (was 55% at 70%, now 61%)
│                                          │
└─────────────────────────────────────────┘
```

### Implementation
```json
{
  "calibration_tracker": {
    "user_id": "naveen",
    "period_start": "2025-01-01",
    "period_end": "2025-12-31",
    "decisions_tracked": 47,
    "outcomes_recorded": 39,
    "confidence_buckets": [
      {
        "bucket": "50%",
        "predictions": 12,
        "accurate": 7,
        "rate": 0.58
      },
      {
        "bucket": "70%",
        "predictions": 18,
        "accurate": 11,
        "rate": 0.61
      },
      {
        "bucket": "90%",
        "predictions": 9,
        "accurate": 8,
        "rate": 0.89
      }
    ],
    "brier_score": 0.18,
    "trend": "improving"
  }
}
```

---

## Pattern 8: Decision Debt Tracking

### Problem
Decisions pile up with pending outcome checks, unresolved dissent.

### Pattern
Track **decision debt** like technical debt.

```
┌─────────────────────────────────────────┐
│ Decision Debt Dashboard                  │
├─────────────────────────────────────────┤
│                                          │
│ Overdue Outcome Checks: 12              │
│ ├── Critical (>30 days): 3              │
│ ├── Warning (15-30 days): 5             │
│ └── Recent (<15 days): 4                │
│                                          │
│ Unresolved Dissent: 7                   │
│ ├── Deferred: 4 (need follow-up)        │
│ ├── Acknowledged: 2 (no mitigation)     │
│ └── Stale: 1 (>90 days old)             │
│                                          │
│ Missing DOORS: 3                        │
│ └── RAMP ≥3 but no rollback plan        │
│                                          │
│ Total Debt Score: 67 (Medium)           │
│                                          │
│ Recommended Actions:                     │
│ 1. Complete 3 critical outcome checks   │
│ 2. Review deferred dissents             │
│ 3. Add DOORS to RAMP ≥3 decisions       │
│                                          │
└─────────────────────────────────────────┘
```

### Debt Categories

| Category | Weight | Description |
|----------|--------|-------------|
| Overdue check (critical) | 10 | >30 days past due |
| Overdue check (warning) | 5 | 15-30 days past due |
| Overdue check (recent) | 2 | <15 days past due |
| Unresolved dissent | 3 | Deferred or acknowledged |
| Stale dissent | 5 | >90 days unaddressed |
| Missing DOORS (RAMP ≥3) | 8 | No rollback plan |
| Missing outcome date | 4 | Final without check scheduled |

---

## Pattern 9: Cross-MEMO Analysis

### Problem
Need to identify patterns across multiple decisions.

### Pattern
Aggregate and analyze MEMOs for systemic insights.

### Analysis Types

**1. Option Recurrence**
```
Top 5 Recurring Options (last 6 months):
1. "Do Nothing / Status Quo" - 89% of MEMOs
2. "Buy vs Build" - 34% of MEMOs
3. "Hire External vs Internal" - 28% of MEMOs
4. "Speed vs Quality tradeoff" - 22% of MEMOs
5. "Centralize vs Decentralize" - 18% of MEMOs
```

**2. Dissent Pattern Analysis**
```
Most Common Dissent Themes:
1. Timeline concerns (42%)
2. Resource constraints (38%)
3. Technical feasibility (28%)
4. Market assumptions (24%)
5. Team capacity (19%)

Dissenters Most Often Vindicated:
1. @security_lead - 67% vindication rate
2. @ops_manager - 54% vindication rate
```

**3. Reversal Analysis**
```
Decisions Reversed: 8 (of 156)
Reversal Rate: 5.1%

Common Reversal Causes:
1. External market shift (3)
2. Resource reallocation (2)
3. Technical discovery (2)
4. Stakeholder change (1)

Average Time to Reversal: 47 days
```

---

## Pattern 10: AI Integration Patterns

### Problem
LLMs need structured decision context, not chat history.

### Pattern
Feed DMG artifacts to LLMs for enhanced reasoning.

### Use Cases

**1. Decision RAG**
```
Query: "What did we decide about EU expansion?"

LLM Response (with DMG RAG):
"Based on MEMO dmg-eu-001 (approved 2025-11-15):
- Decision: Enter EU market via Germany first
- Key dissent: Legal team raised GDPR concerns, mitigated via DPA appointment
- Expected outcome: 1000 customers by Q4 2026 (70% confidence)
- Outcome check due: 2026-06-15
- Current status: In execution"
```

**2. Decision Advisor**
```
User: "Should we acquire this company?"

LLM (with DMG context):
"Based on 3 similar past acquisitions in your DMG history:
- Average time to integrate: 14 months (you predicted 9)
- Culture clash mentioned in 2/3 pre-mortems, was vindicated in 1
- Recommendation: Add 'culture integration plan' to DOORS
- Suggested RAMP: L5 based on pattern match"
```

**3. Outcome Predictor**
```
Query: "Based on our historical accuracy, what's realistic for this prediction?"

LLM Response:
"Your team's 80% confidence predictions have come true 62% of the time.
Suggested recalibration: State 65% confidence for this prediction.
Key factors: Similar decisions in past had timeline slippage (3/5 cases)."
```

---

## Anti-Patterns to Avoid

### ❌ Pattern Cargo Culting
Using advanced patterns without understanding why.
**Fix**: Start simple, add complexity only when needed.

### ❌ Over-Engineering
Creating cascades when a single MEMO would suffice.
**Fix**: Match pattern complexity to decision complexity.

### ❌ Pattern Zombie
Templates running on autopilot without reflection.
**Fix**: Periodic pattern review, sunset unused templates.

### ❌ Analysis Paralysis via Pattern
Using cross-MEMO analysis to avoid making new decisions.
**Fix**: Time-box analysis, force forward progress.
