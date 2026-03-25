# M8: OUTCOME-KIT — Learning Loops

**Time**: 15 minutes  
**Goal**: Close the loop between decisions and reality

---

## The Mindset Shift

| From | To |
|------|-----|
| "We shipped it, done" | "Outcome check scheduled for March 15" |
| "That didn't work" | "Assumption audit: what did we believe wrong?" |
| "Who knew?" | "Dissent audit: Marcus predicted this at line 3" |

---

## What is OUTCOME?

**OUTCOME** is DMG's learning primitive. It closes the loop:

```
Decision → Action → Reality → Learning → Better Decisions
```

Without OUTCOME:
- Assumptions go unaudited
- Predictions are never verified
- Dissent is never vindicated or refuted
- Organizations repeat mistakes

With OUTCOME:
- Every decision has a scheduled reality check
- Predictions are compared to actuals
- Dissent quality is measured
- Precedent is built from real outcomes

---

## OUTCOME Object Structure

```json
{
  "outcome": {
    "outcome_id": "outcome-001",
    "next_check_date": "2026-03-24",
    "checks": [
      {
        "check_date": "2026-02-24",
        "actual_result": "Integration took 4 weeks, not 2",
        "assumptions_audit": [...],
        "dissent_audit": [...],
        "expected_outcomes_audit": [...],
        "verdict": "adjust",
        "next_action": "Extend timeline; add buffer to future estimates"
      }
    ]
  }
}
```

---

## The Three Audits

### 1. Assumptions Audit
> What did we believe that turned out to be wrong?

```json
{
  "assumption": "Integration will take 2 weeks",
  "accurate": false,
  "learning": "Add 100% buffer for vendor integrations"
}
```

### 2. Dissent Audit
> Who saw this coming?

```json
{
  "dissent_id": "dissent-001",
  "vindicated": true,
  "note": "Marcus predicted timeline overrun; his estimate was closer"
}
```

### 3. Expected Outcomes Audit
> How did our predictions compare to reality?

```json
{
  "metric": "User adoption",
  "predicted": "70%",
  "confidence": 0.7,
  "actual": "45%",
  "delta": "-25%"
}
```

---

## Verdict: Keep / Adjust / Reverse

After an outcome check, you must declare:

| Verdict | Meaning | Action |
|---------|---------|--------|
| `keep` | Decision stands | Continue as planned |
| `adjust` | Minor corrections | Document changes |
| `reverse` | Undo the decision | Trigger COMMIT state change |

---

## Required for All Final Decisions

When `commit.state` = `Final` or `Approved`:

✅ `outcome.next_check_date` must be set

No scheduled check = decision cannot be finalized.

---

## Exercise: Run an Outcome Check (10 min)

Think of a decision you made recently. Run a retrospective:

```markdown
## OUTCOME Check

**Decision**: [What was decided]
**Check Date**: [Today]

### Actual Result
[What actually happened?]

### Assumptions Audit
| Assumption | Accurate? | Learning |
|------------|-----------|----------|
| | | |
| | | |

### Dissent Audit
| Who dissented? | Vindicated? | Notes |
|----------------|-------------|-------|
| | | |

### Expected vs Actual
| Metric | Predicted | Actual | Delta |
|--------|-----------|--------|-------|
| | | | |

### Verdict
- [ ] Keep
- [ ] Adjust
- [ ] Reverse

### Next Action
[What should we do now?]
```

---

## The Calibration Loop

OUTCOME is where DMG becomes a **learning system**:

1. **Before decision**: State assumptions + predictions with confidence
2. **After outcome**: Compare to reality
3. **Learning**: What was wrong? Who saw it?
4. **Precedent**: Tag for future reference

Over time, your predictions improve (calibration) and your dissent quality increases.

---

## Key Takeaway

> Decisions without outcome checks are just opinions with deadlines.

OUTCOME turns every decision into a learning opportunity.

---

## Next Step

→ [M9: Integration — Full DMG Workflow](./M9_INTEGRATION.md)
