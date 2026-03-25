# DMG Protocol Specification

## Overview

The DMG Protocol defines **how decision artifacts are created, evolved, and validated**. This document specifies the protocol steps, state transitions, and validation rules.

---

## Protocol Phases

```
┌─────────────────────────────────────────────────────────────┐
│                    DMG PROTOCOL PHASES                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: FRAME          Phase 2: DELIBERATE                │
│  ┌─────────────┐         ┌─────────────┐                    │
│  │ Create      │         │ Capture     │                    │
│  │ MEMO        │────────>│ DISSENT     │                    │
│  │ (Draft)     │         │ + TRACE     │                    │
│  └─────────────┘         └─────────────┘                    │
│        │                       │                             │
│        └───────────┬───────────┘                             │
│                    ▼                                         │
│  Phase 3: GOVERN         Phase 4: COMMIT                    │
│  ┌─────────────┐         ┌─────────────┐                    │
│  │ Set RAMP    │         │ Validate    │                    │
│  │ + DOORS     │────────>│ + Finalize  │                    │
│  │             │         │             │                    │
│  └─────────────┘         └─────────────┘                    │
│                                │                             │
│                                ▼                             │
│  Phase 5: EXECUTE        Phase 6: LEARN                     │
│  ┌─────────────┐         ┌─────────────┐                    │
│  │ Action +    │         │ OUTCOME     │                    │
│  │ MOMENT      │────────>│ Check       │                    │
│  │ logging     │         │             │                    │
│  └─────────────┘         └─────────────┘                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: FRAME

### Purpose
Create the initial decision artifact with options and context.

### Required Actions
1. Create MEMO object with `memo_id`
2. Define `title` (decision question)
3. Add ≥3 `options[]`
4. Set initial `ramp.level`
5. Log `MEMO_CREATED` event

### State Transition
```
None → Draft
```

### Validation Rules
- `title` must be non-empty
- `options` must have ≥3 entries
- `ramp.level` must be 1-5

---

## Phase 2: DELIBERATE

### Purpose
Capture evidence, arguments, and structured disagreement.

### Required Actions
1. Add TRACE objects for key claims
2. Capture DISSENT from stakeholders
3. Record assumptions in `context.assumptions[]`
4. Link sources with strength ratings

### State Transition
```
Draft → Draft (no state change)
```

### Validation Rules (for RAMP ≥3)
- At least 1 DISSENT required before finalization
- Each DISSENT must have `conditions_to_change_mind`

---

## Phase 3: GOVERN

### Purpose
Set governance parameters and reversibility.

### Required Actions
1. Confirm RAMP level with justification
2. Complete DOORS checklist:
   - **D**eclare commitment
   - **O**bserve metrics
   - **O**wn rollback (named person)
   - **R**eady rollback plan
   - **S**ignal thresholds
3. Set `expected_outcomes[]` with confidence
4. Schedule `outcome.next_check_date`

### State Transition
```
Draft → Proposed
```

### Validation Rules (for RAMP ≥3)
- `doors.own.name` required
- `doors.signals` must have ≥2 entries
- `expected_outcomes` must have ≥1 entry with `confidence`

---

## Phase 4: COMMIT

### Purpose
Validate and finalize the decision.

### Required Actions
1. Run validator (`dmg_validate.py`)
2. Resolve any blocking errors
3. Set `commit.state` to `Approved` or `Final`
4. Log `COMMIT_STATE_CHANGED` event

### State Transition
```
Proposed → Approved → Final
```

### Validation Rules (Finalization Gate)

| Rule | Applies To |
|------|------------|
| `outcome.next_check_date` required | All Final/Approved |
| ≥1 DISSENT | RAMP ≥3, Final/Approved |
| `doors.own.name` exists | RAMP ≥3, Final/Approved |
| `doors.signals` ≥2 | RAMP ≥3, Final/Approved |
| `expected_outcomes` ≥1 with confidence | RAMP ≥3, Final/Approved |

---

## Phase 5: EXECUTE

### Purpose
Take action while logging provenance.

### Required Actions
1. Execute the decision
2. Log relevant MOMENT events:
   - `ACTION_TAKEN`
   - `STATUS_UPDATE`
   - Any modifications
3. Monitor DOORS signals

### State Transition
```
Final → Final (execution phase)
      → Reversed (if signals triggered)
```

### Event Types (Execution Phase)
- `ACTION_TAKEN`: Execution step completed
- `STATUS_UPDATE`: Progress logged
- `SIGNAL_TRIGGERED`: DOORS threshold crossed
- `REVIEW_SCHEDULED`: Outcome check approaching

---

## Phase 6: LEARN

### Purpose
Compare predictions to reality and update calibration.

### Required Actions
1. Conduct OUTCOME check on `next_check_date`
2. Complete audits:
   - **Assumptions Audit**: What was accurate/inaccurate?
   - **Dissent Audit**: Who was vindicated?
   - **Expected Outcomes Audit**: Predicted vs actual
3. Declare verdict: `keep` / `adjust` / `reverse`
4. Log `OUTCOME_RECORDED` event
5. Schedule next check (optional)

### State Transition
```
Final → Final (keep)
Final → Final + adjustments (adjust)
Final → Reversed (reverse)
```

### Verdict Definitions

| Verdict | Definition | Action |
|---------|------------|--------|
| `keep` | Decision stands as-is | Continue execution |
| `adjust` | Minor corrections needed | Document changes, continue |
| `reverse` | Undo the decision | Trigger rollback, update state |

---

## State Machine

```
                  ┌─────────┐
                  │  Draft  │
                  └────┬────┘
                       │
                       ▼
                  ┌─────────┐
                  │Proposed │
                  └────┬────┘
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
      ┌─────────┐           ┌─────────┐
      │Approved │           │ (Back to│
      └────┬────┘           │  Draft) │
           │                └─────────┘
           ▼
      ┌─────────┐
      │  Final  │◄─────────────────┐
      └────┬────┘                  │
           │                       │
      ┌────┴────────┬──────────┐  │
      ▼             ▼          ▼  │
┌─────────┐   ┌─────────┐ ┌─────────┐
│Reversed │   │Superseded│ │(keep)   │──┘
└─────────┘   └─────────┘ └─────────┘
```

### Transition Rules
1. `Draft` → `Proposed`: Governance complete
2. `Proposed` → `Draft`: Reviewer requests changes
3. `Proposed` → `Approved`: Authority sign-off
4. `Approved` → `Final`: Commitment begins
5. `Final` → `Reversed`: Outcome check or signal trigger
6. `Final` → `Superseded`: Replaced by new decision

---

## Event Logging Protocol

### Event Structure
```json
{
  "event_id": "evt-001",
  "seq": 1,
  "ts": "2026-01-25T00:00:00Z",
  "type": "EVENT_TYPE",
  "actor": "user.id",
  "payload": {},
  "prev_hash": "...",
  "hash": "..."
}
```

### Standard Event Types

| Event Type | When | Payload |
|------------|------|---------|
| `MEMO_CREATED` | Phase 1 | title |
| `MEMO_UPDATED` | Any modification | version |
| `OPTION_ADDED` | Option created | option details |
| `RAMP_SET` | Governance level assigned | level |
| `DOORS_UPDATED` | Reversibility updated | doors fields |
| `DISSENT_ADDED` | Objection recorded | dissent details |
| `DISSENT_RESOLVED` | Objection addressed | resolution type |
| `SOURCE_ATTACHED` | Evidence linked | trace details |
| `COMMIT_STATE_CHANGED` | State transition | old_state, new_state |
| `APPROVAL_GRANTED` | Sign-off recorded | approver |
| `OUTCOME_RECORDED` | Reality check logged | verdict |
| `SIGNAL_TRIGGERED` | Threshold crossed | signal, value |

---

## Hash Chain Protocol

### Hash Computation
```
hash = SHA256(seq + type + JSON(payload) + prev_hash)[0:12]
```

### Chain Validation
1. Retrieve all events for a MEMO
2. Sort by `seq` ascending
3. For each event after first:
   - Recompute expected hash
   - Compare to stored hash
   - If mismatch: **chain broken, tampering detected**

---

## Protocol Compliance Levels

### Level 0: Minimal
- Valid JSON structure
- Required fields present
- No governance requirements

### Level 1: Basic
- Level 0 +
- RAMP level declared
- ≥3 options

### Level 2: Standard
- Level 1 +
- Outcome check scheduled
- MOMENT events logged

### Level 3: Full Governance
- Level 2 +
- DISSENT captured (for RAMP ≥3)
- DOORS complete (for RAMP ≥3)
- Expected outcomes with confidence (for RAMP ≥3)

### Level 4: Audit-Ready
- Level 3 +
- Hash chain valid
- All events timestamped with ISO 8601
- Actor attribution on all events

---

## Protocol Extensions

The DMG Protocol is extensible via DIPs. Current extension points:

1. **Custom Event Types**: Add domain-specific events
2. **Custom Fields**: Extend MEMO with additional metadata
3. **Integration Hooks**: Trigger external systems on events
4. **Validation Rules**: Add domain-specific validation

See [DIP Process](../community/dips/TEMPLATE.md) for proposing extensions.
