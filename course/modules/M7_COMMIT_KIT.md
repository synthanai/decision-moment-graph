# M7: COMMIT-KIT — State Transitions

**Time**: 10 minutes  
**Goal**: Understand decision lifecycle and state management

---

## The Mindset Shift

| From | To |
|------|-----|
| "We're still discussing" | "Status: Draft" |
| "I think we decided?" | "Status: Final (as of Jan 24)" |
| "We changed our minds" | "Status: Reversed (see OUTCOME check)" |

---

## What is COMMIT?

**COMMIT** tracks the lifecycle state of a decision and records transitions.

Think of it as the "status bar" for a MEMO:
- Is this a draft or final?
- Who made it official?
- What would make us uncommit?

---

## Decision States

| State | Meaning | Can Transition To |
|-------|---------|-------------------|
| `Draft` | Work in progress | Proposed |
| `Proposed` | Ready for review | Approved, Draft |
| `Approved` | Signed off by authority | Final, Reversed |
| `Final` | Committed; now executing | Reversed, Superseded |
| `Reversed` | Decision undone | — |
| `Superseded` | Replaced by new decision | — |

---

## State Transition Rules

```
Draft → Proposed → Approved → Final
                              ↓
                         Reversed
                              or
                         Superseded
```

**Key constraints**:
- Cannot skip states (Draft → Final is invalid)
- `Final` triggers governance checks (RAMP rules)
- `Reversed` requires an OUTCOME check

---

## COMMIT Object Structure

```json
{
  "commit": {
    "state": "Final",
    "changed_at": "2026-01-24T14:00:00Z",
    "changed_by": "sarah.chen",
    "conditions_to_stay_committed": [
      "Q2 budget remains approved",
      "No competing priority from leadership",
      "At least 3 hires in pipeline"
    ]
  }
}
```

---

## Conditions to Stay Committed

A powerful addition to COMMIT: what would make you *uncommit*?

List 2-3 conditions that, if violated, should trigger a review:

```json
"conditions_to_stay_committed": [
  "Customer demand stays above 100 requests/month",
  "Engineering capacity doesn't drop below 2 FTEs",
  "No regulatory change affecting feature"
]
```

This prevents "zombie commitments"—decisions that should have been revisited but weren't.

---

## Governance Gates at Finalization

When `state` changes to `Final` or `Approved`:

**For all decisions**:
- `outcome.next_check_date` must be set

**For RAMP ≥ 3 decisions**:
- ≥1 DISSENT must exist
- DOORS rollback owner must be named
- ≥2 reversal signals must be defined
- ≥1 expected outcome with confidence

These are enforced by the validator.

---

## Exercise: Track State Transitions (5 min)

You have a decision that went through these changes:

1. Sarah drafts the MEMO (Jan 20)
2. Marcus reviews and requests changes (Jan 21)
3. Sarah updates; Marcus approves (Jan 22)
4. Leadership signs off (Jan 23)
5. Team begins execution (Jan 24)
6. Outcome check reveals issues; decision reversed (Feb 15)

Fill in the state at each step:

| Step | Date | State | Changed By |
|------|------|-------|------------|
| 1 | Jan 20 | ___ | sarah.chen |
| 2 | Jan 21 | ___ | — |
| 3 | Jan 22 | ___ | marcus.lee |
| 4 | Jan 23 | ___ | exec.sponsor |
| 5 | Jan 24 | ___ | sarah.chen |
| 6 | Feb 15 | ___ | sarah.chen |

---

## Answer Key

| Step | State |
|------|-------|
| 1 | Draft |
| 2 | (still Draft — review in progress) |
| 3 | Proposed |
| 4 | Approved |
| 5 | Final |
| 6 | Reversed |

---

## Key Takeaway

> COMMIT makes decision state **explicit and traceable**.

You always know:
- Where a decision stands
- Who moved it forward
- What would change it

---

## Next Step

→ [M8: OUTCOME-KIT — Learning Loops](./M8_OUTCOME_KIT.md)
