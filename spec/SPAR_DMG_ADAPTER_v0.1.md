# SPAR → DMG Adapter Specification

**Version**: 0.1  
**Status**: Draft  
**Date**: January 2026

---

## Overview

The SPAR → DMG Adapter converts SPAR debate outputs into DMG-compliant decision artifacts.

```
┌─────────────────┐        ┌─────────────────┐
│   SPAR Engine   │        │   DMG Artifact  │
│  (deliberation) │───────>│  (decision obj) │
└─────────────────┘        └─────────────────┘
        │                          │
        ▼                          ▼
   transcripts                   MEMO
   positions                   MOMENT
   synthesis                  DISSENT
   critique                    TRACE
```

---

## Mapping: SPAR → DMG

| SPAR Component | DMG Object | Mapping Logic |
|----------------|------------|---------------|
| Question/Arena | `memo.title` | Decision question becomes title |
| Context | `memo.context.constraints` | Constraints passed to debate |
| Positions (N/E/S/W) | `memo.options[]` | Each position → option |
| Synthesis recommendation | `memo.recommendation` | Arbiter's final recommendation |
| Dissenting positions | `objects.dissents[]` | Unresolved tensions → DISSENT |
| Transcript events | `moment.events[]` | Debate turns → MOMENT events |
| Citations/evidence | `objects.traces[]` | Sources → TRACE objects |
| Confidence score | `memo.expected_outcomes[].confidence` | Synthesis confidence |
| PROBE critique | (validation) | Validates MEMO quality |

---

## Implementation

### Input: SPAR Output JSON

```json
{
  "spar_id": "spar-abc123",
  "question": "Should we build or buy the analytics feature?",
  "context": "We have 3 engineers available; $50k budget",
  "config": {
    "pattern": "dialectic",
    "depth": "clash",
    "style": "steelman"
  },
  "positions": [
    {
      "agent": "north",
      "role": "Champion",
      "position": "Build in-house for control",
      "arguments": ["Full customization", "No vendor lock-in"],
      "evidence": []
    },
    {
      "agent": "east",
      "role": "Challenger",
      "position": "Buy vendor solution for speed",
      "arguments": ["Faster time-to-value", "Lower risk"],
      "evidence": [{"type": "case_study", "uri": "..."}]
    },
    {
      "agent": "south",
      "role": "Steelman Critic",
      "position": "Hybrid: buy core, customize edges",
      "arguments": ["Best of both worlds"],
      "evidence": []
    },
    {
      "agent": "west",
      "role": "Contrarian",
      "position": "Do nothing; validate need first",
      "arguments": ["Unclear if feature is needed"],
      "evidence": []
    }
  ],
  "synthesis": {
    "recommendation": "Buy vendor solution (Mixpanel) with custom integration layer",
    "confidence": 0.75,
    "rationale": "Speed outweighs control given timeline constraints",
    "key_tensions": [
      "Lock-in risk acknowledged but mitigated with exit clause"
    ],
    "conditions_to_reverse": [
      "If integration exceeds 3 months",
      "If vendor pricing increases > 30%"
    ]
  },
  "probe": {
    "plurality": 9,
    "rigor": 8,
    "origin": 9,
    "basis": 8,
    "execution": 7
  },
  "transcript": [
    {"seq": 1, "ts": "...", "agent": "north", "type": "position", "content": "..."},
    {"seq": 2, "ts": "...", "agent": "east", "type": "rebuttal", "content": "..."}
  ]
}
```

### Output: DMG Object

```json
{
  "dmg_version": "0.1",
  "memo": {
    "memo_id": "dmg-from-spar-abc123",
    "title": "Should we build or buy the analytics feature?",
    "arena_id": "build-vs-buy",
    "decision": "Buy vendor solution (Mixpanel) with custom integration layer",
    "context": {
      "constraints": ["3 engineers available", "$50k budget"],
      "assumptions": []
    },
    "options": [
      {
        "name": "Build in-house",
        "description": "Build in-house for control",
        "pros": ["Full customization", "No vendor lock-in"],
        "cons": [],
        "source": "spar:north"
      },
      {
        "name": "Buy vendor solution",
        "description": "Buy vendor solution for speed",
        "pros": ["Faster time-to-value", "Lower risk"],
        "cons": [],
        "source": "spar:east"
      },
      {
        "name": "Hybrid approach",
        "description": "Buy core, customize edges",
        "pros": ["Best of both worlds"],
        "cons": [],
        "source": "spar:south"
      },
      {
        "name": "Do nothing",
        "description": "Validate need first",
        "pros": ["Unclear if feature is needed"],
        "cons": [],
        "source": "spar:west"
      }
    ],
    "recommendation": "Buy vendor solution (Mixpanel) with custom integration layer. Speed outweighs control given timeline constraints.",
    "ramp": {
      "level": 3,
      "justification": "Auto-assigned; review recommended"
    },
    "expected_outcomes": [
      {
        "metric": "Decision confidence",
        "expected": "Successful implementation",
        "confidence": 0.75,
        "notes": "From SPAR synthesis"
      }
    ]
  },
  "moment": {
    "moment_id": "moment-from-spar-abc123",
    "memo_id": "dmg-from-spar-abc123",
    "events": [
      {
        "event_id": "evt-001",
        "seq": 1,
        "ts": "...",
        "type": "MEMO_CREATED",
        "actor": "spar-adapter",
        "payload": {"source": "spar", "spar_id": "spar-abc123"}
      },
      {
        "event_id": "evt-002",
        "seq": 2,
        "ts": "...",
        "type": "BLOCK_ADDED",
        "actor": "spar:north",
        "payload": {"type": "position", "content": "..."}
      }
    ]
  },
  "objects": {
    "dissents": [
      {
        "dissent_id": "dissent-from-north",
        "author": "spar:north",
        "claim": "Build in-house for control, vendor lock-in is real risk",
        "evidence": ["Full customization", "No vendor lock-in"],
        "conditions_to_change_mind": "If integration exceeds 3 months"
      }
    ],
    "traces": [
      {
        "trace_id": "trace-001",
        "claim": "Buy is faster",
        "source": {"type": "case_study", "uri": "..."},
        "strength": "medium"
      }
    ],
    "commit": {
      "state": "Proposed"
    },
    "outcome": {
      "outcome_id": "outcome-001",
      "next_check_date": null
    }
  }
}
```

---

## Adapter API

### Python

```python
from dmg.adapters import SPARAdapter

adapter = SPARAdapter()

# Convert SPAR output to DMG
spar_output = {...}  # From SPAR engine
dmg = adapter.convert(spar_output)

# Save to file
dmg.save('decision.dmg.json')

# Validate
from dmg import validate
result = validate(dmg)
```

### JavaScript

```javascript
import { SPARAdapter } from '@dmg/adapters';

const adapter = new SPARAdapter();

// Convert SPAR output to DMG
const sparOutput = {...};
const dmg = adapter.convert(sparOutput);

// Export
exportDMG(dmg);
```

---

## RAMP Auto-Assignment

The adapter can suggest RAMP levels based on SPAR context:

| SPAR Signal | RAMP Suggestion |
|-------------|-----------------|
| Arena type = "tactical" | L1-L2 |
| Arena type = "strategic" | L3-L4 |
| Horizon = "legacy" | L4-L5 |
| Confidence < 0.5 | Bump +1 level |
| High tension count (>3) | Bump +1 level |

Human always confirms RAMP before finalizing.

---

## DOORS Auto-Population

From SPAR synthesis:

- `doors.declare` ← synthesis.recommendation
- `doors.signals` ← synthesis.conditions_to_reverse
- `doors.observe` ← inferred from context (needs human)
- `doors.own` ← **requires human input**
- `doors.ready` ← **requires human input**

---

## Integration Points

### 1. SPAR-Arena (ARANGAM)
When a SPAR session completes, offer "Export to DMG" button.

### 2. DMG App
When creating a new MEMO, offer "Start with SPAR" to run deliberation first.

### 3. CLI

```bash
# Convert existing SPAR output
dmg import-spar session.spar.json -o decision.dmg.json

# Run SPAR then convert
spar "Should we X?" --output-dmg decision.dmg.json
```

---

## Future Extensions

1. **SPAR → DMG streaming**: Real-time MOMENT events as debate progresses
2. **Bi-directional**: DMG decisions can trigger follow-up SPARs
3. **Learning loop**: OUTCOME checks can reference original SPAR disagreements
4. **Multi-SPAR**: Link multiple debates to one DMG decision

---

*This adapter makes SPAR the deliberation engine for DMG governance.*


---

## RAPS REVIEW

| Field | Value |
|-------|-------|
| Review Tier | Lite |
| Review Due | TBD (needs confidence score) |
| Review Status | Pending |
| Verdict Status | Unknown |
| Evidence | - |
| Corrective Action | - |
| Reviewed By | - |
| Review Date | - |
