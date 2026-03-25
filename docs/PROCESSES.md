# DMG Processes

## Standard Operating Procedures for Decision Governance

This document defines the **repeatable processes** for using DMG in daily practice.

---

## Process 1: Solo Decision (Personal MEMO)

**When**: You're making a decision alone and want to track it.

### Steps

```
┌─────────────────────────────────────────┐
│ 1. Ask: "What am I deciding?"           │
│    → Write the decision question        │
├─────────────────────────────────────────┤
│ 2. Generate 3+ options                  │
│    → Always include "Do Nothing"        │
├─────────────────────────────────────────┤
│ 3. Set RAMP level                       │
│    → How long to undo?                  │
├─────────────────────────────────────────┤
│ 4. Argue with yourself                  │
│    → Create at least 1 DISSENT          │
├─────────────────────────────────────────┤
│ 5. State your prediction                │
│    → "I expect X with Y% confidence"    │
├─────────────────────────────────────────┤
│ 6. Set outcome check date               │
│    → When will you know?                │
├─────────────────────────────────────────┤
│ 7. Decide and commit                    │
│    → Mark as Final                      │
└─────────────────────────────────────────┘
```

### Time Required
- L1-L2: 5 minutes
- L3: 15 minutes
- L4-L5: 30+ minutes

---

## Process 2: SPAR → MEMO (Deliberation-First)

**When**: You want structured deliberation before deciding.

### Steps

```
┌─────────────────────────────────────────┐
│ 1. Frame the question                   │
│    → Clear decision question            │
├─────────────────────────────────────────┤
│ 2. Run SPAR                             │
│    → Quick (2 agents) / Balanced (4)    │
│    → Deep (8) / Crisis / Challenge      │
├─────────────────────────────────────────┤
│ 3. Review synthesis                     │
│    → Read recommendation                │
│    → Note key tensions                  │
├─────────────────────────────────────────┤
│ 4. Convert to MEMO                      │
│    → Auto-populates options from SPAR   │
│    → Captures DISSENT from positions    │
│    → Sets RAMP from confidence          │
├─────────────────────────────────────────┤
│ 5. Complete governance                  │
│    → Fill in DOORS                      │
│    → Add expected outcomes              │
├─────────────────────────────────────────┤
│ 6. Finalize                             │
│    → Set outcome check                  │
│    → Commit                             │
└─────────────────────────────────────────┘
```

### When to Use SPAR
- Complex decisions with many stakeholders
- High-stakes (RAMP 4-5)
- When you want to stress-test your thinking
- Before major announcements

---

## Process 3: Team Decision

**When**: Multiple people need to align on a decision.

### Roles
- **Owner**: Creates MEMO, drives to conclusion
- **Stakeholders**: Contribute options, dissents
- **Approvers**: Sign off on Final state

### Steps

```
Day 0: Frame
├── Owner creates MEMO
├── Shares with stakeholders
└── Collects initial options

Day 1-3: Deliberate
├── Stakeholders add DISSENT
├── Evidence linked via TRACE
└── Options refined

Day 3-5: Govern
├── RAMP level confirmed by Owner
├── DOORS completed
├── Expected outcomes defined
└── Outcome check scheduled

Day 5-7: Commit
├── Approvers review
├── Final sign-off
└── State → Final
```

### Async vs Sync
- **Async**: Document everything in MEMO, comment via DISSENT
- **Sync**: Use meeting to resolve tensions, document result

---

## Process 4: Escalation

**When**: A decision needs higher authority.

### Triggers
- RAMP ≥4
- Budget above threshold
- Policy change
- Legal/compliance impact

### Steps

```
┌─────────────────────────────────────────┐
│ 1. Owner marks as "Needs Escalation"    │
│    → State remains Proposed             │
├─────────────────────────────────────────┤
│ 2. Escalation target identified         │
│    → Who needs to approve?              │
├─────────────────────────────────────────┤
│ 3. Package prepared                     │
│    → Export MEMO as DMG JSON            │
│    → Include summary brief              │
├─────────────────────────────────────────┤
│ 4. Escalation target reviews            │
│    → May request changes                │
│    → May add DISSENT                    │
├─────────────────────────────────────────┤
│ 5. Approval or rejection                │
│    → Logged as MOMENT event             │
│    → State → Approved or Draft          │
├─────────────────────────────────────────┤
│ 6. Continue to Final                    │
│    → If approved                        │
└─────────────────────────────────────────┘
```

---

## Process 5: Outcome Check

**When**: `outcome.next_check_date` arrives.

### Steps

```
┌─────────────────────────────────────────┐
│ 1. Retrieve MEMO                        │
│    → Review original predictions        │
├─────────────────────────────────────────┤
│ 2. Document actual results              │
│    → What actually happened?            │
├─────────────────────────────────────────┤
│ 3. Assumptions Audit                    │
│    → Check each assumption              │
│    → Mark accurate/inaccurate           │
├─────────────────────────────────────────┤
│ 4. Dissent Audit                        │
│    → Was any dissenter vindicated?      │
│    → Were concerns valid?               │
├─────────────────────────────────────────┤
│ 5. Variance Analysis                    │
│    → Expected vs Actual                 │
│    → Confidence calibration             │
├─────────────────────────────────────────┤
│ 6. Verdict                              │
│    → KEEP: Decision stands              │
│    → ADJUST: Minor corrections          │
│    → REVERSE: Undo decision             │
├─────────────────────────────────────────┤
│ 7. Schedule next check (if needed)      │
│    → Learning continues                 │
└─────────────────────────────────────────┘
```

### Verdict Decision Tree

```
Did the decision achieve its expected outcomes?
├── Yes (within tolerance) → KEEP
├── Partially (minor gaps) → ADJUST
└── No (significant failure)
    ├── Is reversal possible? → REVERSE
    └── Not possible → ADJUST + Lessons Learned
```

---

## Process 6: Emergency Reversal

**When**: DOORS signal triggered or crisis situation.

### Steps

```
┌─────────────────────────────────────────┐
│ 1. Signal detected                      │
│    → Threshold crossed                  │
│    → Or crisis identified               │
├─────────────────────────────────────────┤
│ 2. Notify DOORS owner                   │
│    → Named rollback owner activated     │
├─────────────────────────────────────────┤
│ 3. Confirm reversal need                │
│    → Quick assessment                   │
│    → Above threshold = reverse          │
├─────────────────────────────────────────┤
│ 4. Execute rollback plan                │
│    → From DOORS.ready section           │
├─────────────────────────────────────────┤
│ 5. Update MEMO                          │
│    → State → Reversed                   │
│    → Log SIGNAL_TRIGGERED event         │
│    → Log COMMIT_STATE_CHANGED event     │
├─────────────────────────────────────────┤
│ 6. Post-mortem                          │
│    → What triggered reversal?           │
│    → Update learnings                   │
└─────────────────────────────────────────┘
```

---

## Process 7: Decision Supersession

**When**: A new decision replaces an old one.

### Steps

```
┌─────────────────────────────────────────┐
│ 1. Create new MEMO                      │
│    → Reference old decision in context  │
├─────────────────────────────────────────┤
│ 2. Complete new decision process        │
│    → All normal phases                  │
├─────────────────────────────────────────┤
│ 3. Link decisions                       │
│    → Old MEMO gets "supersedes" link    │
│    → New MEMO gets "superseded_by" link │
├─────────────────────────────────────────┤
│ 4. Update old MEMO state                │
│    → State → Superseded                 │
│    → Log event with new MEMO ID         │
├─────────────────────────────────────────┤
│ 5. Finalize new MEMO                    │
│    → Becomes the active decision        │
└─────────────────────────────────────────┘
```

---

## Process Checklists

### Pre-Commit Checklist (all RAMP levels)

- [ ] Title is a clear question
- [ ] ≥3 options considered
- [ ] RAMP level set with justification
- [ ] Outcome check date scheduled

### Governance Checklist (RAMP ≥3)

- [ ] At least 1 DISSENT captured
- [ ] DOORS owner named (not "team")
- [ ] Rollback signals defined (≥2)
- [ ] Expected outcomes stated with confidence
- [ ] Review date scheduled

### Finalization Checklist

- [ ] All blocking validation errors resolved
- [ ] Approvers have signed off
- [ ] COMMIT state is Final
- [ ] MOMENT events logged

---

## Process Metrics

Track these to improve decision quality:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Options coverage** | ≥3 per decision | `options.length` |
| **Dissent rate** | ≥1 per RAMP ≥3 | `dissents.length` |
| **Calibration score** | Improving trend | OUTCOME check accuracy |
| **Reversal rate** | <10% | Reversed / Final decisions |
| **Check completion** | 100% | Checks done / Checks scheduled |
| **Time to decision** | By RAMP tier | Draft to Final duration |

---

## Process Anti-Patterns

### ❌ HIPPO Decision
"Highest Paid Person's Opinion" wins with no dissent.

**Fix**: Require DISSENT before HIPPO speaks.

### ❌ Analysis Paralysis
Endless option generation, never committing.

**Fix**: Set deadline in MEMO, time-box deliberation.

### ❌ False Consensus
"Everyone agrees" when no one challenged.

**Fix**: Explicitly ask for dissent, reward it.

### ❌ Fire and Forget
Decision made, never reviewed.

**Fix**: Enforce OUTCOME check date, block if missing.

### ❌ CYA Documentation
MEMO created retroactively to justify what already happened.

**Fix**: MOMENT timestamps prove sequence.
