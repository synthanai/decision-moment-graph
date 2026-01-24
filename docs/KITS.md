# DMG Primitives: The 8 Kits

DMG is a **single standard** with **8 first-class primitives**, each documented as a "kit" for clarity.

> **Architecture Decision**: All primitives live in one repository (`dmg-open-standard`) because they are tightly coupled by design. The "kit" naming is a documentation and branding strategy, not a repo structure.

---

## The 8 Kits

| Kit | Purpose | Depends On |
|-----|---------|------------|
| **MEMO-KIT** | The shareable decision brief (projection) | MOMENT, RAMP |
| **MOMENT-KIT** | Append-only event stream (provenance) | — (core) |
| **RAMP-KIT** | Risk-proportional governance levels (1-5) | DOORS |
| **DOORS-KIT** | Reversibility checklist (Declare/Observe/Own/Ready/Signal) | — |
| **DISSENT-KIT** | Structured disagreement with conditions | TRACE |
| **TRACE-KIT** | Evidence links with source strength | — |
| **COMMIT-KIT** | State transition boundary | RAMP, OUTCOME |
| **OUTCOME-KIT** | Post-decision reality check | DISSENT |

---

## Dependency Graph

```
                    ┌─────────────────────┐
                    │      MEMO-KIT       │
                    │   (decision brief)  │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ MOMENT-KIT  │     │  RAMP-KIT   │     │ DISSENT-KIT │
    │ (provenance)│     │ (governance)│     │  (dissent)  │
    └─────────────┘     └──────┬──────┘     └──────┬──────┘
                               │                   │
                               ▼                   ▼
                        ┌─────────────┐     ┌─────────────┐
                        │ DOORS-KIT   │     │ TRACE-KIT   │
                        │(reversibility)    │ (evidence)  │
                        └─────────────┘     └─────────────┘
                               │
                               ▼
                        ┌─────────────┐
                        │ COMMIT-KIT  │
                        │  (states)   │
                        └──────┬──────┘
                               │
                               ▼
                        ┌─────────────┐
                        │ OUTCOME-KIT │
                        │ (learning)  │
                        └─────────────┘
```

---

## Kit Summaries

### MEMO-KIT
The human-readable decision artifact. Contains decision statement, options, recommendation, owners, and review triggers.

**Required fields**: `memo_id`, `title`, `decision`, `options` (≥3), `recommendation`, `ramp`

### MOMENT-KIT
The append-only provenance log. Every change to a decision creates an immutable event with timestamps, actors, and hash-chaining.

**Core primitive**: Everything flows through MOMENT.

### RAMP-KIT
Risk-proportional governance. Decisions are classified L1-L5 based on reversibility time window.

| Level | Time to Undo | Example |
|-------|--------------|---------|
| 1 | Minutes | Feature flag |
| 2 | Hours-Days | Pricing tweak |
| 3 | Weeks | Roadmap priority |
| 4 | Months | Architecture |
| 5 | Years/Never | M&A |

### DOORS-KIT
The reversibility checklist. Ensures every decision has:
- **D**eclare: What are we committing to?
- **O**bserve: What will we monitor?
- **O**wn: Who owns rollback?
- **R**eady: Is the rollback plan documented?
- **S**ignal: What triggers reversal?

### DISSENT-KIT
Structured disagreement with:
- Clear claim
- Supporting evidence
- **Conditions to change mind** (key innovation)
- Resolution type (accepted/mitigated/deferred/rejected)

### TRACE-KIT
Evidence provenance. Links claims to sources with:
- Source type and URI
- Retrieval timestamp
- Strength rating (strong/medium/weak)
- Quote index

### COMMIT-KIT
State transitions: `Draft` → `Proposed` → `Approved` → `Final` → `Reversed`|`Superseded`

Includes conditions-to-stay-committed.

### OUTCOME-KIT
The learning loop:
- Scheduled outcome checks
- Assumption audits (what did we believe wrong?)
- Dissent audits (who saw it coming?)
- Expected outcomes audits (prediction vs reality)
- Verdict: keep/adjust/reverse

---

## Why One Repo?

From the [SPARKIT architectural decision](./decisions/ADR-001_monorepo.md):

1. **Primitives are coupled**: MEMO without MOMENT is incomplete; RAMP without DOORS is useless
2. **Maintenance**: 8 repos = 8× overhead without 8× value
3. **Adoption**: Users want `npm install dmg`, not 8 package choices
4. **Coherence**: DMG is one standard, not 8 standards

### When to Reconsider

- Different teams own different primitives
- Enterprise demands isolated security audits
- Release cycles diverge
- 10+ active contributors

---

## Usage

All kits are accessed from the single `dmg` package:

```javascript
// JavaScript/TypeScript
import { Memo, Moment, Ramp, Doors, Dissent, Trace, Commit, Outcome } from '@dmg/core';

// Create a MEMO
const memo = new Memo({
  title: "Quarterly Planning",
  decision: "Focus on enterprise features",
  options: [...],
  ramp: { level: 3 }
});

// Validate governance rules
const validator = new DMGValidator();
const { valid, errors } = validator.validate(memo);
```

```python
# Python
from dmg import Memo, Moment, Ramp, validate

memo = Memo(
    title="Quarterly Planning",
    decision="Focus on enterprise features",
    options=[...],
    ramp={"level": 3}
)

result = validate(memo)
```

---

*The 8 kits are one standard. Install once, use progressively.*
