# DMS Core Specification v0.2

**Status**: Draft  
**Version**: 0.2.0  
**Date**: January 2026

---

## 1. Introduction

### 1.1 Purpose

The **Decision Moment Standard (DMS)** defines the normative requirements for valid, auditable decision governance. It establishes the **MERIT** criteria that distinguish a true organizational decision from a simple chat log or document.

While **DMS** defines the rules (the "What"), the **Decision Moment Graph (DMG)** is the reference implementation (the "How") that provides the JSON schemas and validators.

### 1.2 Scope

This specification covers:
- **Normative Rules**: The MERIT criteria (Measured, Evidenced, Reversible, Inspectable, Traceable).
- **Protocol Suite**: The 4-step protocol (DCP → DMP → DRP → DGP).
- **Data Model**: The reference DMG schema for compliance.
- **Conformance**: Levels of adherence (Bronze to Platinum).

### 1.3 Terminology & Taxonomy

#### The Architecture
| Component | Acronym | Role | Relationship |
|-----------|---------|------|--------------|
| **Decision Moment Standard** | **DMS** | Normative Spec | The "Law" (Interface) |
| **Decision Moment Graph** | **DMG** | Reference Kit | The "Tool" (Implementation) |

#### The Protocol Suite
| Protocol | Full Name | Role | Phase |
|----------|-----------|------|-------|
| **DCP** | **Decision Context Protocol** | Upstream Framing | Frame (Scope, Stakeholders) |
| **DMP** | **Decision Moment Protocol** | The Event Gate | Commit ("We decide now") |
| **DRP** | **Decision Record Protocol** | Downstream Artifact | Record (The JSON File) |
| **DGP** | **Decision Gate Protocol** | Governance Logic | Route (Approvals) |

#### Core Primitives (MERIT)
| Primitive | Definition | MERIT Principle |
|-----------|------------|-----------------|
| **OUTCOME** | Predictions to verify reality | **M**easured |
| **MEMO** | Versioned decision brief (≥3 options) | **E**videnced |
| **DOORS** | Reversibility checklist & owners | **R**eversible |
| **MOMENT** | Append-only event hash chain | **I**nspectable |
| **TRACE** | Evidence links & citation graph | **T**raceable |

### 1.5 The Decision Lifecycle

DMS defines a **7-Step Heptagon** lifecycle that maps phases to the primitives they produce.

> **Cycle**: **FRAME → SPAR → GATE → COMMIT → ENACT → YIELD → GAUGE**

| Step | Phase | Primitive | Kit/Module | Action |
|------|-------|-----------|------------|--------|
| 1 | **FRAME** | `MEMO` | `dmg/frame` | Define context & options |
| 2 | **SPAR** | `DISSENT` | `spar-kit` | Deliberate & Challenge |
| 3 | **GATE** | `RAMP` | `dmg/gate` | Check Governance & Reversibility |
| 4 | **COMMIT** | `MOMENT` | `dmg/core` | Sign & Hash (The "Capture") |
| 5 | **ENACT** | — | — | Execute instructions |
| 6 | **YIELD** | `OUTCOME` | `dmg/yield` | Measure results |
| 7 | **GAUGE** | `RETRO` | `dmg/gauge` | Calibrate confidence & learn |

*Note: In the DMG implementation, these "Primitives" are represented as JSON Objects defined in the unified Schema.*

*Note: Phases are the human workflow steps. Protocols are the formal rules. Primitives are the artifacts.*

#### Quick Validator Logic (Reference)

```javascript
/* DMS Conformance Check */
const checkMerit = (decision) => ({
  M: hasOutcomes(decision),     // Measured
  E: hasOptions(decision, 3),   // Evidenced
  R: hasReversibility(decision),// Reversible
  I: hasHashChain(decision),    // Inspectable
  T: hasEvidence(decision)      // Traceable
});
```

**Validator Command**:
```bash
dmg validate --merit decision.dmg.json
```

---

## 2. The Decision Record (DRP)

### 2.1 DRP Container (The Artifact)

A **Decision Record** (often encoded as a `.dmg.json` file) is a container containing:

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
  "dissent_vault_ref": "vault://hash/sha256/...", 
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

**Zero-Knowledge Dissent**:
If `dissent_vault_ref` is present, the sensitive `claim` and `evidence` fields MAY be redacted/hashed in the core record, with full content stored in a Vault-Kit compliant vault.

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

## 3. DGP: Decision Gate Protocol (Governance)

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
### 4.3 Zero-Knowledge Dissent (ZK-Dissent)

DMS mandates that the **existence** of dissent must be recorded (MERIT - Inspectable), but the **content** may be sensitive.

- **Standard Pattern**: Record full text in `DISSENT` object.
- **ZK Pattern**: Record `dissent_vault_ref` (URI/Hash) in `DISSENT` object. Store content in Vault-Kit.
- The `MOMENT` chain MUST record the `DISSENT_ADDED` event with the hash of the content, ensuring provenance even if content is off-chain.

---

## 5. DMS Conformance

### 5.1 Conformance Levels

Implementations (like DMG) are graded on their ability to enforce MERIT.
 
 | Level | Requirements | MERIT Mapping |
 |-------|-------------|---------------|
 | **Bronze** | Valid MEMO (Options/Rationale) | **E** (Evidenced) |
 | **Silver** | Bronze + MOMENT (Audit Chain) | **E** + **I** (Inspectable) |
 | **Gold** | Silver + RAMP/DOORS | **E** + **I** + **R** (Reversible) |
 | **Platinum** | Gold + OUTCOME + TRACE | All 5 (**M**easured + **T**raceable) |
 
 ### 5.2 MERIT-to-Conformance Matrix
 
 | MERIT Principle | Verified By | Conformance Level |
 |-----------------|-------------|-------------------|
 | **M**easured | OUTCOME.checks[] | Platinum |
 | **E**videnced | MEMO.options (≥3) | Bronze |
 | **R**eversible | DOORS.own + ready | Gold |
 | **I**nspectable | MOMENT events + hash chain | Silver |
 | **T**raceable | objects.traces[].source | Platinum |

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
