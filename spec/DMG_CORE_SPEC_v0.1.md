# DMG Core Specification v0.1

**Status**: Draft  
**Version**: 0.1.0  
**Date**: January 2026

---

## 1. Introduction

### 1.1 Purpose

The Decision Moment Graph (DMG) specification defines a standard format for representing decisions as structured, temporal, inspectable artifacts.

### 1.2 Scope

This specification covers:
- Core data model (objects and relationships)
- Event types and provenance
- Governance primitives
- Conformance requirements

### 1.3 Terminology

| Term | Definition |
|------|------------|
| **MEMO** | A versioned decision brief (projection) |
| **MOMENT** | An append-only event stream (provenance) |
| **RAMP** | Risk-proportional governance levels (1-5) |
| **DOORS** | Reversibility checklist (Declare/Observe/Own/Ready/Signal) |
| **DISSENT** | Structured disagreement with conditions |
| **TRACE** | Evidence links with source strength |
| **COMMIT** | State transition boundary |
| **OUTCOME** | Post-decision reality check |

### 1.4 The MERIT Principles

DMG decisions are validated against five core principles, collectively known as **MERIT**. Each principle maps directly to a DMG primitive:

> *"DMG decisions have MERIT — Measured with OUTCOME, Evidenced via MEMO, Reversible thru DOORS, Inspectable in MOMENT, Traceable by TRACE."*

#### MERIT × DMG Primitive Mapping

| Principle | Primitive | Definition | Validator Check |
|-----------|-----------|------------|-----------------|
| **M**easured | OUTCOME | Outcomes are quantified and linked to predictions | `outcome.checks[]` exists with `expected_outcomes_audit` |
| **E**videnced | MEMO | Decision is documented with options and rationale | `memo.options[]` ≥ 3 with reasoning |
| **R**eversible | DOORS | Rollback plan and ownership are defined | `doors.own.name` AND `doors.ready` populated |
| **I**nspectable | MOMENT | Audit trail exists and is cryptographically valid | `moment.events[]` exists with valid hash chain |
| **T**raceable | TRACE | Evidence sources are linked with provenance | `traces[]` exists with `source.uri` or `source.type` |

#### MERIT Compliance Levels

| Level | Requirements |
|-------|-------------|
| **MERIT-Partial** | At least 3 of 5 principles satisfied |
| **MERIT-Valid** | All 5 principles satisfied |
| **MERIT-Certified** | MERIT-Valid + external audit verification |

#### Quick Validator Logic

```javascript
const checkMerit = (dmg) => ({
  M: !!dmg.objects?.outcome?.checks?.length,
  E: !!dmg.memo?.options?.length && dmg.memo.options.length >= 3,
  R: !!dmg.objects?.doors?.own?.name && !!dmg.objects?.doors?.ready,
  I: !!dmg.moment?.events?.length && verifyHashChain(dmg.moment.events),
  T: !!dmg.objects?.traces?.length
});
```

**Validation Command**:
```bash
dmg validate --merit decision.dmg.json
```

---

## 2. Core Objects

### 2.1 DMG Container

A DMG file is a JSON document containing:

```json
{
  "dmg_version": "0.1",
  "memo": { ... },
  "moment": { ... },
  "objects": {
    "dissents": [ ... ],
    "traces": [ ... ],
    "commit": { ... },
    "outcome": { ... }
  }
}
```

### 2.2 MEMO Object

The human-readable decision brief.

**Required fields**:
- `memo_id` (string): Unique identifier
- `title` (string): Decision title
- `decision` (string): Clear decision statement
- `options` (array): At least 3 options considered
- `recommendation` (string): Chosen option with rationale
- `ramp` (object): Governance level

**Optional fields**:
- `arena_id` (string): Template reference
- `context` (object): Constraints + assumptions
- `risks` (array): Identified risks
- `mitigations` (array): Risk mitigations
- `owners` (array): Accountable parties
- `review_date` (string, ISO 8601): Next review trigger
- `expected_outcomes` (array): Predictions with confidence

### 2.3 MOMENT Object

The append-only provenance log.

**Structure**:
```json
{
  "moment_id": "string",
  "memo_id": "string",
  "events": [
    {
      "event_id": "string",
      "seq": 1,
      "ts": "2026-01-24T12:00:00Z",
      "type": "MEMO_CREATED",
      "actor": "string",
      "payload": { ... },
      "prev_hash": "string",
      "hash": "string"
    }
  ]
}
```

**Event Types**:
- `MEMO_CREATED` - Initial creation
- `MEMO_UPDATED` - Version change
- `BLOCK_ADDED` - Content addition
- `BLOCK_UPDATED` - Content modification
- `RAMP_SET` - Governance level assigned
- `DOORS_UPDATED` - Reversibility checklist updated
- `DISSENT_ADDED` - Objection recorded
- `DISSENT_RESOLVED` - Objection addressed
- `SOURCE_ATTACHED` - Evidence linked
- `COMMIT_STATE_CHANGED` - State transition
- `APPROVAL_GRANTED` - Approval recorded
- `EXPORTED` - Export generated
- `OUTCOME_RECORDED` - Reality check logged

### 2.4 RAMP Object

Risk-proportional governance.

```json
{
  "level": 3,
  "justification": "Affects Q2 roadmap; 2-week reversal window",
  "time_to_undo": "2 weeks"
}
```

**Levels**:
| Level | Time to Undo | Examples |
|-------|-------------|----------|
| 1 | Minutes | Config change, feature flag |
| 2 | Hours-Days | Pricing tweak, copy change |
| 3 | Weeks | Roadmap priority, hiring |
| 4 | Months | Architecture, partnership |
| 5 | Years/Never | M&A, compliance commitment |

### 2.5 DOORS Object

Reversibility checklist.

```json
{
  "declare": "We are committing to Option B",
  "observe": ["User engagement metrics", "Support ticket volume"],
  "own": {
    "name": "Jane Smith",
    "role": "Product Lead"
  },
  "ready": "Rollback plan documented in wiki",
  "signals": [
    {
      "metric": "NPS",
      "threshold": "< 30",
      "horizon": "4 weeks",
      "action": "Trigger review meeting"
    }
  ]
}
```

### 2.6 DISSENT Object

Structured disagreement.

```json
{
  "dissent_id": "string",
  "author": "string",
  "claim": "Option B underestimates integration cost",
  "evidence": ["Engineering estimate was 2 weeks; similar projects took 6"],
  "conditions_to_change_mind": "If integration completes in < 3 weeks",
  "resolution": {
    "type": "acknowledged",
    "response": "Added buffer to timeline",
    "resolved_by": "string",
    "resolved_at": "2026-01-24T14:00:00Z"
  }
}
```

**Resolution Types**:
- `accepted` - Dissent changed the decision
- `mitigated` - Risk addressed but decision unchanged
- `deferred` - Will revisit at outcome check
- `rejected` - Explicitly overruled with rationale

### 2.7 TRACE Object

Evidence provenance.

```json
{
  "trace_id": "string",
  "claim": "Users prefer mobile-first",
  "source": {
    "type": "survey",
    "uri": "https://example.com/survey-results",
    "retrieved_at": "2026-01-20T10:00:00Z"
  },
  "strength": "strong",
  "quote_index": "67% of respondents..."
}
```

**Strength Levels**:
- `strong` - Direct evidence, verified
- `medium` - Indirect or partially verified
- `weak` - Anecdotal or unverified

### 2.8 COMMIT Object

State transitions.

```json
{
  "state": "Final",
  "changed_at": "2026-01-24T15:00:00Z",
  "changed_by": "string",
  "conditions_to_stay_committed": [
    "Q2 budget remains approved",
    "No competing priority from leadership"
  ]
}
```

**States**:
- `Draft` - Work in progress
- `Proposed` - Ready for review
- `Approved` - Signed off
- `Final` - Committed
- `Reversed` - Decision changed
- `Superseded` - Replaced by new decision

### 2.9 OUTCOME Object

Reality check.

```json
{
  "outcome_id": "string",
  "next_check_date": "2026-03-24",
  "checks": [
    {
      "check_date": "2026-02-24",
      "actual_result": "Integration took 4 weeks",
      "assumptions_audit": [
        {
          "assumption": "2 weeks integration",
          "accurate": false,
          "learning": "Add 100% buffer for integrations"
        }
      ],
      "dissent_audit": [
        {
          "dissent_id": "d-001",
          "vindicated": true,
          "note": "Engineering estimate was correct"
        }
      ],
      "expected_outcomes_audit": [
        {
          "metric": "User adoption",
          "predicted": "70%",
          "confidence": 0.7,
          "actual": "65%",
          "delta": "-5%"
        }
      ],
      "verdict": "adjust",
      "next_action": "Extend timeline by 2 weeks"
    }
  ]
}
```

**Verdicts**:
- `keep` - Decision stands
- `adjust` - Minor corrections needed
- `reverse` - Undo the decision

---

## 3. Governance Rules

### 3.1 Mandatory Fields by RAMP Level

| Field | RAMP 1-2 | RAMP 3+ |
|-------|----------|---------|
| `decision` | ✅ | ✅ |
| `options` (≥3) | ✅ | ✅ |
| `ramp.level` | ✅ | ✅ |
| `dissents` (≥1) | - | ✅ |
| `doors.own.name` | - | ✅ |
| `doors.signals` (≥2) | - | ✅ |
| `expected_outcomes` (≥1) | - | ✅ |
| `outcome.next_check_date` | - | ✅ |

### 3.2 State Transition Rules

- `Draft` → `Proposed` → `Approved` → `Final`
- `Final` → `Reversed` (requires OUTCOME check)
- `Final` → `Superseded` (requires new MEMO link)
- Cannot transition to `Final`/`Approved` without passing governance gates

---

## 4. Integrity

### 4.1 Event Hashing

Each MOMENT event includes:
- `prev_hash`: Hash of previous event (empty for first)
- `hash`: SHA-256 of `event_id + ts + type + payload + prev_hash`

This creates a tamper-evident chain.

### 4.2 Versioning

- MEMO versions are numbered sequentially (v1, v2, ...)
- Each version change creates a `MEMO_UPDATED` event
- Previous versions are immutable

---

## 5. Conformance

### 5.1 Conformance Levels

| Level | Requirements | MERIT Mapping |
|-------|-------------|---------------|
| **Bronze** | Valid MEMO with required fields | S (Structured) |
| **Silver** | Bronze + MOMENT events | S + I (Inspectable) |
| **Gold** | Silver + RAMP/DOORS | S + I + R (Reversible) |
| **Platinum** | Gold + DISSENT + OUTCOME + TRACE | All MERIT principles |

### 5.2 MERIT-to-Conformance Matrix

| MERIT Principle | Verified By | Conformance Level |
|-----------------|-------------|-------------------|
| **M**easured | OUTCOME.checks[].expected_outcomes_audit | Platinum |
| **E**videnced | objects.traces[].source | Gold+ |
| **R**eversible | objects.doors + ramp.time_to_undo | Gold+ |
| **I**nspectable | moment.events[] + hash chain | Silver+ |
| **T**raceable | moment.events[].prev_hash chain | Silver+ |

### 5.3 Validation Requirements

A conformant implementation MUST:

1. **Schema Validation**: Validate against JSON Schema (`/schema/dmg-core-v0.1.schema.json`)
2. **Governance Enforcement**: Apply mandatory fields by RAMP level (see §3.1)
3. **State Machine**: Reject invalid state transitions (see §3.2)
4. **Hash Chain**: Verify event hash chain integrity
5. **MERIT Scoring**: Compute principle satisfaction (0-5 score)

### 5.4 MERIT Validation Algorithm

```
MERIT_SCORE = 0

IF outcome.checks[] exists AND len > 0:
    MERIT_SCORE += 1  # Measured

IF objects.traces[] exists AND all have source.uri:
    MERIT_SCORE += 1  # Evidenced

IF objects.doors exists AND doors.own.name AND doors.ready:
    MERIT_SCORE += 1  # Reversible

IF moment.events[] exists AND hash_chain_valid():
    MERIT_SCORE += 1  # Inspectable

IF moment.events[] has no gaps AND first event is MEMO_CREATED:
    MERIT_SCORE += 1  # Traceable

RETURN {
  score: MERIT_SCORE,
  level: MERIT_SCORE >= 5 ? "MERIT-Valid" : 
         MERIT_SCORE >= 3 ? "MERIT-Partial" : "MERIT-None"
}
```

---

## 6. Extensions

### 6.1 Vendor Extensions

Custom fields MUST use the `x_vendor_` prefix:

```json
{
  "memo": {
    "x_acme_priority": "high"
  }
}
```

### 6.2 Extension Registration

Standard extensions may be proposed via DIP process.

---

## Appendix A: JSON Schema Reference

See `/schema/dmg-core-v0.1.schema.json`

## Appendix B: Example DMG Files

See `/examples/`

---

*End of DMG Core Specification v0.1*
