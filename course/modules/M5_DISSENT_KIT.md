# M5: DISSENT-KIT — Productive Disagreement

**Time**: 15 minutes  
**Goal**: Capture structured disagreement with conditions to change mind

---

## The Mindset Shift

| From | To |
|------|-----|
| "Everyone agreed" | "Dissent was recorded; here's what would change our minds" |
| "Objections were overruled" | "Dissent was mitigated with specific response" |
| "We had a debate" | "Structured objection with evidence and conditions" |

---

## What is DISSENT?

**DISSENT** is DMG's primitive for structured disagreement.

Most organizations treat disagreement as:
- Drama to minimize
- Political maneuvering
- Something to "get past"

DMG treats dissent as **data**:
- A claim with evidence
- Conditions that would validate it
- A resolution that addresses it

---

## The Key Innovation: Conditions to Change Mind

The most powerful field in a DISSENT object:

> **"I'd change my mind if..."**

This transforms conflict into actionable signals:
- If the condition occurs, the dissenter was right
- If it doesn't, the decision was vindicated
- Either way, you learn

---

## DISSENT Object Structure

```json
{
  "dissent_id": "dissent-001",
  "author": "marcus.lee",
  "claim": "4 weeks is too long for senior hires who already know the domain",
  "evidence": [
    "Last 2 senior hires were contributing within 2 weeks",
    "Industry data shows senior hires ramp 40% faster"
  ],
  "conditions_to_change_mind": "If we see senior hires struggling at week 2, I'd support the full 4 weeks",
  "resolution": {
    "type": "mitigated",
    "response": "Added 'fast-track' path for senior hires: can exit at week 2 if milestones met",
    "resolved_by": "sarah.chen",
    "resolved_at": "2026-01-24T13:00:00Z"
  }
}
```

---

## Required Fields

| Field | Purpose |
|-------|---------|
| `author` | Who raised the dissent |
| `claim` | What they disagree with |
| `conditions_to_change_mind` | What would prove them wrong (or right) |

## Optional but Valuable

| Field | Purpose |
|-------|---------|
| `evidence` | Supporting data for the claim |
| `resolution` | How the dissent was addressed |

---

## Resolution Types

| Type | Meaning |
|------|---------|
| `accepted` | Dissent changed the decision |
| `mitigated` | Risk was addressed; decision unchanged |
| `deferred` | Will revisit at outcome check |
| `rejected` | Explicitly overruled (with rationale) |

**Rule**: Even `rejected` dissent must include a response explaining why.

---

## Required for RAMP ≥ 3

When a decision is RAMP 3 or higher and marked Final/Approved:

✅ At least 1 DISSENT must exist

No dissent recorded = decision cannot be finalized at L3+.

---

## Exercise: Write a DISSENT (10 min)

Think of a decision you disagreed with (or might). Structure it:

```markdown
## DISSENT

**Author**: [Your name]

**Claim**: [What you disagree with]

**Evidence**:
1. [Supporting point 1]
2. [Supporting point 2]

**Conditions to change my mind**:
[What would prove you wrong? Be specific and measurable]

---

**Resolution** (if resolved):
- Type: [accepted / mitigated / deferred / rejected]
- Response: [How it was addressed]
- Resolved by: [Who]
```

---

## The DISSENT Drill

Practice this in your next meeting:

When someone disagrees, ask:
1. "What's your specific claim?"
2. "What evidence supports it?"
3. "What would change your mind?"

This transforms debate into data.

---

## Weak vs Strong Examples

### ❌ Weak DISSENT

```
Author: Marcus
Claim: I don't think this will work
Evidence: [none]
Conditions: [none]
```

**Problems**: Vague, no evidence, no conditions.

### ✅ Strong DISSENT

```
Author: Marcus Lee

Claim: The 2-week timeline underestimates integration complexity
by at least 50%

Evidence:
- Prior integration (Project Alpha) estimated 2 weeks, took 5
- Vendor hasn't provided API documentation yet
- QA team is already at capacity

Conditions to change my mind:
- If vendor delivers docs by Feb 1 and QA gets temp support,
  I'd agree 2 weeks is achievable

Resolution:
- Type: mitigated
- Response: Extended timeline to 3 weeks; QA contractor approved
- Resolved by: sarah.chen
```

**Strengths**: Specific claim, evidence, testable conditions, documented resolution.

---

## Key Takeaway

> DISSENT isn't drama. It's missing data.

The goal isn't to eliminate disagreement. It's to **capture it structurally** so you can learn from outcomes.

---

## Next Step

→ [M6: TRACE-KIT — Evidence](./M6_TRACE_KIT.md)
