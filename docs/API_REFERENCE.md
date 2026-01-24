# DMG API Reference

## Data Structures

This document provides a complete reference for all DMG data structures and their fields.

---

## Core Objects

### DMG Root Object

```json
{
  "dmg_version": "0.1",
  "memo": { ... },
  "moment": { ... },
  "objects": { ... }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dmg_version` | string | ✓ | DMG specification version (e.g., "0.1") |
| `memo` | object | ✓ | The decision record |
| `moment` | object | ○ | Provenance events |
| `objects` | object | ○ | Related objects (dissents, traces, etc.) |

---

## MEMO Object

The core decision record.

```json
{
  "memo_id": "string",
  "title": "string",
  "arena_id": "string",
  "decision": "string",
  "context": { ... },
  "options": [ ... ],
  "recommendation": "string",
  "ramp": { ... },
  "doors": { ... },
  "expected_outcomes": [ ... ],
  "owners": [ ... ],
  "review_date": "YYYY-MM-DD",
  "version": 1,
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `memo_id` | string | Unique identifier (UUID recommended) |
| `title` | string | Decision question or name |
| `options` | array | Decision options (≥3 required) |
| `ramp.level` | integer | RAMP level 1-5 |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `arena_id` | string | Domain/category of decision |
| `decision` | string | Final decision statement |
| `context` | object | Constraints, assumptions, background |
| `recommendation` | string | Recommended option with rationale |
| `doors` | object | Reversibility checklist |
| `expected_outcomes` | array | Predictions with confidence |
| `owners` | array | Decision stakeholders |
| `review_date` | string | Scheduled review date |
| `version` | integer | MEMO version number |
| `created_at` | string | Creation timestamp (ISO 8601) |
| `updated_at` | string | Last update timestamp (ISO 8601) |

---

## Context Object

```json
{
  "constraints": ["string", "..."],
  "assumptions": ["string", "..."],
  "background": "string",
  "links": [
    {"title": "string", "uri": "string"}
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `constraints` | string[] | Hard limits (budget, timeline, etc.) |
| `assumptions` | string[] | Beliefs that must hold for decision to work |
| `background` | string | Additional context narrative |
| `links` | object[] | Related documents/resources |

---

## Option Object

```json
{
  "name": "string",
  "description": "string",
  "pros": ["string", "..."],
  "cons": ["string", "..."],
  "source": "string",
  "estimated_cost": "string",
  "estimated_effort": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Short option name |
| `description` | string | ○ | Full option description |
| `pros` | string[] | ○ | Arguments in favor |
| `cons` | string[] | ○ | Arguments against |
| `source` | string | ○ | Where option came from (e.g., "spar:north") |
| `estimated_cost` | string | ○ | Cost estimate |
| `estimated_effort` | string | ○ | Effort estimate |

---

## RAMP Object

```json
{
  "level": 3,
  "justification": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `level` | integer | ✓ | 1-5 (time to reverse) |
| `justification` | string | ○ | Why this level |

### RAMP Level Definitions

| Level | Time to Reverse | Governance Required |
|-------|-----------------|---------------------|
| L1 | Minutes | Minimal |
| L2 | Hours-Days | Basic |
| L3 | Weeks | DISSENT + DOORS |
| L4 | Months | Full approval chain |
| L5 | Years/Never | Maximum rigor |

---

## DOORS Object

```json
{
  "declare": "string",
  "observe": ["string", "..."],
  "own": {
    "name": "string",
    "role": "string",
    "email": "string"
  },
  "ready": "string",
  "signals": [
    {
      "metric": "string",
      "threshold": "string",
      "action": "string"
    }
  ]
}
```

| Field | Type | Required (RAMP ≥3) | Description |
|-------|------|-------------------|-------------|
| `declare` | string | ○ | What we're committing to |
| `observe` | string[] | ○ | Metrics to monitor |
| `own.name` | string | ✓ | Named rollback owner |
| `own.role` | string | ○ | Owner's role |
| `own.email` | string | ○ | Contact info |
| `ready` | string | ○ | Rollback plan |
| `signals` | object[] | ✓ (≥2) | Reversal triggers |

### Signal Object

| Field | Type | Description |
|-------|------|-------------|
| `metric` | string | What to measure |
| `threshold` | string | When to act (e.g., ">500ms") |
| `action` | string | What to do when triggered |

---

## Expected Outcome Object

```json
{
  "metric": "string",
  "expected": "string",
  "confidence": 0.75,
  "horizon": "string",
  "notes": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `metric` | string | ✓ | What you're predicting |
| `expected` | string | ✓ | The prediction |
| `confidence` | number | ○ | 0.0-1.0 confidence level |
| `horizon` | string | ○ | When to measure (e.g., "Q3 2026") |
| `notes` | string | ○ | Additional context |

---

## Owner Object

```json
{
  "name": "string",
  "role": "string",
  "email": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Person's name |
| `role` | string | ○ | Role in decision (e.g., "Decision Owner") |
| `email` | string | ○ | Contact email |

---

## MOMENT Object

```json
{
  "moment_id": "string",
  "memo_id": "string",
  "events": [ ... ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `moment_id` | string | ✓ | Unique identifier |
| `memo_id` | string | ✓ | Associated MEMO |
| `events` | array | ✓ | Append-only event log |

### Event Object

```json
{
  "event_id": "string",
  "seq": 1,
  "ts": "ISO8601",
  "type": "string",
  "actor": "string",
  "payload": {},
  "prev_hash": "string",
  "hash": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_id` | string | ✓ | Unique event identifier |
| `seq` | integer | ✓ | Sequence number (monotonic) |
| `ts` | string | ✓ | Timestamp (ISO 8601) |
| `type` | string | ✓ | Event type (see below) |
| `actor` | string | ✓ | Who/what triggered event |
| `payload` | object | ○ | Event-specific data |
| `prev_hash` | string | ○ | Previous event's hash |
| `hash` | string | ○ | This event's hash |

### Event Types

| Type | Description |
|------|-------------|
| `MEMO_CREATED` | Initial MEMO creation |
| `MEMO_UPDATED` | MEMO modified |
| `OPTION_ADDED` | Option added |
| `OPTION_REMOVED` | Option removed |
| `RAMP_SET` | RAMP level assigned |
| `DOORS_UPDATED` | DOORS fields changed |
| `DISSENT_ADDED` | Dissent recorded |
| `DISSENT_RESOLVED` | Dissent addressed |
| `SOURCE_ATTACHED` | TRACE linked |
| `COMMIT_STATE_CHANGED` | State transition |
| `APPROVAL_GRANTED` | Approval recorded |
| `OUTCOME_RECORDED` | Outcome check logged |
| `SIGNAL_TRIGGERED` | DOORS signal fired |

---

## Objects Container

```json
{
  "dissents": [ ... ],
  "traces": [ ... ],
  "commit": { ... },
  "outcome": { ... }
}
```

---

## DISSENT Object

```json
{
  "dissent_id": "string",
  "author": "string",
  "claim": "string",
  "evidence": ["string", "..."],
  "conditions_to_change_mind": "string",
  "resolution": "string",
  "resolution_notes": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dissent_id` | string | ✓ | Unique identifier |
| `author` | string | ✓ | Who raised the dissent |
| `claim` | string | ✓ | The objection/concern |
| `evidence` | string[] | ○ | Supporting evidence |
| `conditions_to_change_mind` | string | ✓* | What would resolve this |
| `resolution` | string | ○ | accepted/mitigated/deferred/rejected |
| `resolution_notes` | string | ○ | How it was addressed |

*Required for finalization

---

## TRACE Object

```json
{
  "trace_id": "string",
  "claim": "string",
  "source": {
    "type": "string",
    "uri": "string",
    "title": "string",
    "retrieved_at": "ISO8601"
  },
  "strength": "string",
  "verifier": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trace_id` | string | ✓ | Unique identifier |
| `claim` | string | ✓ | What claim this supports |
| `source` | object | ✓ | Evidence source |
| `source.type` | string | ✓ | article/study/expert/etc |
| `source.uri` | string | ✓ | Link to source |
| `source.title` | string | ○ | Source title |
| `source.retrieved_at` | string | ○ | When accessed |
| `strength` | string | ○ | strong/moderate/weak |
| `verifier` | string | ○ | Who verified this |

---

## COMMIT Object

```json
{
  "state": "string",
  "approvals": [ ... ],
  "changed_at": "ISO8601",
  "changed_by": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `state` | string | ✓ | Current state (see below) |
| `approvals` | array | ○ | List of approvals |
| `changed_at` | string | ○ | Last state change |
| `changed_by` | string | ○ | Who changed state |

### State Values

| State | Description |
|-------|-------------|
| `Draft` | Work in progress |
| `Proposed` | Ready for review |
| `Approved` | Approved, not yet executed |
| `Final` | Committed, in execution |
| `Reversed` | Decision undone |
| `Superseded` | Replaced by newer decision |

### Approval Object

```json
{
  "actor": "string",
  "approved_at": "ISO8601",
  "notes": "string"
}
```

---

## OUTCOME Object

```json
{
  "outcome_id": "string",
  "next_check_date": "YYYY-MM-DD",
  "checks": [ ... ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `outcome_id` | string | ✓ | Unique identifier |
| `next_check_date` | string | ✓* | Next scheduled check |
| `checks` | array | ○ | History of outcome checks |

*Required for Final/Approved state

### Outcome Check Object

```json
{
  "check_date": "YYYY-MM-DD",
  "actual_result": "string",
  "assumptions_audit": [ ... ],
  "dissent_audit": [ ... ],
  "expected_outcomes_audit": [ ... ],
  "verdict": "string",
  "next_action": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `check_date` | string | When check was performed |
| `actual_result` | string | What actually happened |
| `assumptions_audit` | array | Which assumptions held |
| `dissent_audit` | array | Which dissenters were vindicated |
| `expected_outcomes_audit` | array | Predicted vs actual |
| `verdict` | string | keep/adjust/reverse |
| `next_action` | string | What to do next |

---

## Validation Rules Summary

### Schema Rules (All)
- `dmg_version` required
- `memo.memo_id` required
- `memo.title` required
- `memo.options` array required
- `memo.ramp.level` must be 1-5

### Governance Rules (RAMP ≥3 + Final/Approved)
- `options.length` ≥ 3
- `dissents.length` ≥ 1
- `doors.own.name` exists
- `doors.signals.length` ≥ 2
- `expected_outcomes.length` ≥ 1 with confidence

### Finalization Rules (Final/Approved)
- `outcome.next_check_date` required
