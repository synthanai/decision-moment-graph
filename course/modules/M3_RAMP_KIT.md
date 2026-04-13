# M3: RAMP-KIT — Proportional Governance

**Time**: 15 minutes  
**Goal**: Apply rigor proportional to reversibility

---

## The Mindset Shift

| From | To |
|------|-----|
| "Everything needs approval" | "Rigor scales with reversibility" |
| "Just ship it, we'll fix later" | "What's the time to undo?" |
| "It's fine, trust me" | "RAMP level declares the stakes" |

---

## What is RAMP?

**RAMP** = Risk-proportional governance based on **time to reverse**.

The core insight:
> A decision that takes 5 minutes to undo shouldn't require the same process as one that takes 5 years.

RAMP creates **proportional rigor**: more process for harder-to-reverse decisions, less for trivial ones.

---

## The 5 RAMP Levels

| Level | Time to Undo | Examples | Rigor |
|-------|--------------|----------|-------|
| **L1** | Minutes | Feature flag, config change | Minimal |
| **L2** | Hours-Days | Pricing tweak, copy change | Light review |
| **L3** | Weeks | Roadmap priority, hiring | DISSENT + DOORS required |
| **L4** | Months | Architecture, partnership | Approval + signals |
| **L5** | Years/Never | M&A, compliance commitment | Full governance |

---

## Why RAMP Matters

**Without RAMP**:
- Trivial decisions get over-processed (slow)
- Critical decisions get under-processed (risky)
- Teams argue about "how much review is enough"

**With RAMP**:
- Governance is predictable
- Speed and safety coexist
- Teams know the rules

---

## RAMP Object Structure

```json
{
  "ramp": {
    "level": 3,
    "justification": "Affects Q2 roadmap; 2-week reversal window",
    "time_to_undo": "2 weeks"
  }
}
```

**Required for all MEMOs**: `level`  
**Recommended**: `justification`, `time_to_undo`

---

## Governance Rules by RAMP Level

| Requirement | L1-L2 | L3+ |
|-------------|-------|-----|
| ≥3 options | ✅ | ✅ |
| RAMP level declared | ✅ | ✅ |
| At least 1 DISSENT | - | ✅ |
| Rollback owner (DOORS) | - | ✅ |
| ≥2 reversal signals | - | ✅ |
| Expected outcomes | - | ✅ |
| Scheduled outcome check | - | ✅ |

---

## Exercise: Calibrate RAMP Levels (10 min)

For each decision, assign a RAMP level (1-5) and justify:

### Decision 1
> "Change the button color from blue to green"

**Your RAMP**: ___  
**Time to undo**: ___  
**Justification**: ___

### Decision 2
> "Move from AWS to GCP for our primary infrastructure"

**Your RAMP**: ___  
**Time to undo**: ___  
**Justification**: ___

### Decision 3
> "Hire a new VP of Engineering"

**Your RAMP**: ___  
**Time to undo**: ___  
**Justification**: ___

### Decision 4
> "Sign a 3-year exclusive partnership with Vendor X"

**Your RAMP**: ___  
**Time to undo**: ___  
**Justification**: ___

---

## Calibration Answers

| Decision | RAMP | Time to Undo | Notes |
|----------|------|--------------|-------|
| Button color | L1 | Minutes | Feature flag or quick deploy |
| AWS→GCP migration | L4-L5 | 6-12 months | Major infrastructure; contracts, data |
| VP of Engineering | L3-L4 | Months | Cultural impact; severance |
| 3-year exclusive | L5 | 3 years (contractual) | Legal commitment; nearly irreversible |

---

## Common RAMP Mistakes

### ❌ Under-calibrating
> "It's just a database schema change" → But migration takes a month

**Ask**: How long until we can *actually* undo this?

### ❌ Over-calibrating
> "We need full review for this typo fix" → Stalls velocity

**Ask**: If this is wrong, can we fix it in minutes?

### ❌ Ignoring hidden reversibility costs
> "We can always revert" → But retraining users takes weeks

**Ask**: What are the second-order reversal costs?

---

## Key Takeaway

> RAMP makes governance **proportional**, not bureaucratic.

Low RAMP = move fast.  
High RAMP = move carefully.  
Always know which you're in.

---

## Next Step

→ [M4: DOORS-KIT, Reversibility](./M4_DOORS_KIT.md)
