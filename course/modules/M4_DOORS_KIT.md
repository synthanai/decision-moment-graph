# M4: DOORS-KIT — Reversibility

**Time**: 15 minutes  
**Goal**: Build reversibility into every commitment

---

## The Mindset Shift

| From | To |
|------|-----|
| "We'll figure out rollback if needed" | "Rollback plan documented before commit" |
| "Someone will handle it" | "Named rollback owner" |
| "We'll know when to stop" | "Specific signals + thresholds" |

---

## What is DOORS?

**DOORS** is the reversibility checklist that makes every decision *rollback-ready*.

| Letter | Question | Output |
|--------|----------|--------|
| **D**eclare | What are we committing to? | Clear commitment statement |
| **O**bserve | What will we monitor? | Metrics/signals to watch |
| **O**wn | Who owns rollback? | Named person (not "the team") |
| **R**eady | Is rollback ready? | Documented plan |
| **S**ignal | What triggers reversal? | Thresholds + horizons |

---

## Why DOORS Matters

Most decisions fail not because of bad judgment, but because:
- No one owned the reversal
- There were no clear signals
- The rollback plan didn't exist

DOORS makes **reversibility concrete** before you commit.

---

## DOORS Object Structure

```json
{
  "doors": {
    "declare": "We commit to Option B: phased launch to 10% of users",
    "observe": [
      "Error rate",
      "User satisfaction (NPS)",
      "Support ticket volume"
    ],
    "own": {
      "name": "Sarah Chen",
      "role": "Product Lead"
    },
    "ready": "Rollback plan: revert feature flag + notify users via in-app message",
    "signals": [
      {
        "metric": "Error rate",
        "threshold": "> 2%",
        "horizon": "24 hours",
        "action": "Pause rollout"
      },
      {
        "metric": "NPS",
        "threshold": "< 30",
        "horizon": "7 days",
        "action": "Trigger review meeting"
      }
    ]
  }
}
```

---

## The 5 DOORS Questions

### D — Declare
> "What exactly are we committing to?"

Be specific. Not "improve onboarding" but "implement 4-week structured program for next 3 hires."

### O — Observe
> "What will tell us if this is working?"

List 2-4 metrics/signals you'll monitor. If you can't observe it, you can't govern it.

### O — Own
> "Who owns rollback if we need to reverse?"

A **name**, not a team. This person is accountable for executing the rollback.

### R — Ready
> "Is the rollback plan documented?"

Write it down. "Revert feature flag" is fine for L1. L4-L5 needs a detailed plan.

### S — Signal
> "What threshold triggers reversal?"

Be specific:
- **Metric**: What are you measuring?
- **Threshold**: What value is unacceptable?
- **Horizon**: How long do you wait before checking?
- **Action**: What happens if threshold is crossed?

---

## Required for RAMP ≥ 3

When a decision is RAMP 3 or higher and marked Final/Approved:

✅ `doors.own.name` must exist (rollback owner)  
✅ `doors.signals` must have ≥2 entries

---

## Exercise: Build a DOORS Checklist (10 min)

Pick a decision you're currently facing. Fill in:

```markdown
## DOORS Checklist

### D — Declare
What we're committing to:
[Your answer]

### O — Observe
Metrics we'll monitor:
1. [Metric 1]
2. [Metric 2]
3. [Metric 3]

### O — Own
Rollback owner: [Name + Role]

### R — Ready
Rollback plan:
[How would we undo this?]

### S — Signal
Triggers for reversal:

| Signal | Metric | Threshold | Horizon | Action |
|--------|--------|-----------|---------|--------|
| 1 | | | | |
| 2 | | | | |
```

---

## Weak vs Strong Examples

### ❌ Weak DOORS

```
Declare: Launch the feature
Observe: We'll keep an eye on things
Own: The team will handle it
Ready: We can always revert
Signal: If it breaks, we'll know
```

**Problems**: Vague, no accountability, no thresholds.

### ✅ Strong DOORS

```
Declare: Launch privacy dashboard to 10% of users by March 15

Observe:
- Dashboard load time (< 2s target)
- Privacy settings adoption rate
- Support tickets mentioning "privacy"

Own: Marcus Lee (Engineering Lead)

Ready: Rollback = disable feature flag + email to affected users

Signal:
- If load time > 5s for 1 hour: pause rollout
- If adoption < 5% after 3 days: review with product
- If support tickets > 50/day: trigger incident review
```

**Strengths**: Specific metrics, named owner, concrete thresholds.

---

## Key Takeaway

> DOORS makes reversibility **concrete before you commit**.

If you can't fill out DOORS, you're not ready to finalize the decision.

---

## Next Step

→ [M5: DISSENT-KIT — Productive Disagreement](./M5_DISSENT_KIT.md)
