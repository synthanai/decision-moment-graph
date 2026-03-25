# M2: MOMENT-KIT — Provenance

**Time**: 15 minutes  
**Goal**: Understand append-only event streams and why provenance matters

---

## The Mindset Shift

| From | To |
|------|-----|
| "We updated the decision" | "Here's the MOMENT trail showing what changed, when, and why" |
| "Trust me, this is accurate" | "Here's the hash-linked event chain" |
| "Who changed this?" | "Event #4: Marcus, 2pm, added risk mitigation" |

---

## What is MOMENT?

A **MOMENT** is DMG's provenance layer: an append-only log of every event that shaped a decision.

Think of it as the "Git history" for a decision:
- Every change creates an event
- Events are numbered sequentially
- Each event records: what, who, when
- Hash-chaining makes tampering detectable

> A MEMO is what you share. A MOMENT is how you prove it.

---

## Why Append-Only?

**The problem with editable history**:
- "Who changed this?" → Unknown
- "What did we originally decide?" → Lost
- "Was this approval real?" → Unprovable

**Append-only solves this**:
- Every change is a new event
- Previous events are immutable
- The current MEMO is a *projection* of all events

---

## Event Types

| Event Type | Description |
|------------|-------------|
| `MEMO_CREATED` | Initial draft created |
| `MEMO_UPDATED` | Version bump |
| `BLOCK_ADDED` | New content section |
| `BLOCK_UPDATED` | Content modified |
| `RAMP_SET` | Governance level assigned |
| `DOORS_UPDATED` | Reversibility updated |
| `DISSENT_ADDED` | Objection recorded |
| `DISSENT_RESOLVED` | Objection addressed |
| `SOURCE_ATTACHED` | Evidence linked |
| `COMMIT_STATE_CHANGED` | State transition |
| `APPROVAL_GRANTED` | Sign-off recorded |
| `OUTCOME_RECORDED` | Reality check logged |

---

## Event Structure

Each event contains:

```json
{
  "event_id": "evt-003",
  "seq": 3,
  "ts": "2026-01-24T12:00:00Z",
  "type": "DISSENT_ADDED",
  "actor": "marcus.lee",
  "payload": {
    "dissent_id": "dissent-001",
    "claim": "Timeline is too aggressive"
  },
  "prev_hash": "b2c3d4e5f6a1",
  "hash": "c3d4e5f6a1b2"
}
```

**Key fields**:
- `seq`: Monotonically increasing sequence number
- `ts`: ISO 8601 timestamp
- `actor`: Who performed the action
- `prev_hash` + `hash`: Creates tamper-evident chain

---

## Exercise: Read a MOMENT Trail (5 min)

Look at this event sequence:

```
Event 1: MEMO_CREATED by sarah.chen at 10:00
Event 2: RAMP_SET (level: 3) by sarah.chen at 11:00
Event 3: DISSENT_ADDED by marcus.lee at 12:00
Event 4: DISSENT_RESOLVED by sarah.chen at 13:00
Event 5: COMMIT_STATE_CHANGED (Draft → Final) by sarah.chen at 14:00
```

Answer these questions:
1. Who created the decision?
2. How long did deliberation take?
3. Was dissent captured before finalizing?
4. Who had the final say?

---

## Check Your Understanding

| Question | Answer |
|----------|--------|
| Can you edit event #3? | No — you can only add new events |
| How do you correct a mistake? | Add a new event that documents the correction |
| What if someone tampers with an event? | Hash chain breaks; detected during validation |

---

## Weak vs Strong Examples

### ❌ Weak (No MOMENT)

```
Decision: Launch feature by March 15
Status: Approved
```

**Problems**: No history. No actors. No timeline. No evidence of deliberation.

### ✅ Strong (With MOMENT)

```
Decision: Launch feature by March 15

MOMENT Trail:
- Jan 20, 10:00: Created by sarah.chen
- Jan 20, 14:00: Added 3 options
- Jan 21, 09:00: RAMP set to L3 (sarah.chen)
- Jan 21, 11:00: Dissent from marcus.lee: "Timeline too aggressive"
- Jan 21, 14:00: Dissent mitigated: "Added fallback milestone"
- Jan 21, 16:00: Approved by exec.sponsor
- Jan 22, 10:00: Finalized by sarah.chen
```

**Strengths**: Complete history. Clear actors. Visible deliberation.

---

## Key Takeaway

> MOMENT makes decisions **inspectable**—technically and legally.

When you have MOMENT:
- Auditors can trace every change
- Disputes can be resolved with evidence
- Learning can reference "what we knew when"

---

## Next Step

→ [M3: RAMP-KIT — Proportional Governance](./M3_RAMP_KIT.md)
