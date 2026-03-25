# M10: Calibration Track — Predictions

**Time**: 15 minutes  
**Goal**: Add predictions to decisions and learn to calibrate judgment

---

## The Mindset Shift

| From | To |
|------|-----|
| "I think this will work" | "Prediction: 70% chance of success (here's why)" |
| "We'll see what happens" | "Expected: 40% adoption by Week 4 (confidence: 0.6)" |
| "Who knew it would fail?" | "Confidence calibration: we overestimated by 25%" |

---

## What is Calibration?

**Calibration** = How well your predictions match reality.

A well-calibrated decision-maker:
- When they say "70% confident," they're right ~70% of the time
- They know when they don't know
- Their judgment improves with feedback

DMG enables calibration by:
1. Capturing predictions with confidence scores
2. Comparing predictions to outcomes
3. Tracking accuracy over time

---

## Expected Outcomes Structure

```json
{
  "expected_outcomes": [
    {
      "metric": "User adoption rate",
      "horizon": "4 weeks",
      "expected": "40%",
      "confidence": 0.7,
      "notes": "Based on similar feature launches"
    },
    {
      "metric": "Support ticket volume",
      "horizon": "2 weeks",
      "expected": "< 20/day",
      "confidence": 0.5,
      "notes": "Uncertain; new user segment"
    }
  ]
}
```

**Key fields**:
- `metric`: What you're predicting
- `expected`: Your prediction (quantified)
- `confidence`: 0.0 to 1.0 (how certain are you?)
- `horizon`: When to check

---

## Confidence Calibration

### What Confidence Means

| Score | Meaning |
|-------|---------|
| 0.9 | I'd be shocked if wrong |
| 0.7 | Pretty confident; some uncertainty |
| 0.5 | Coin flip; could go either way |
| 0.3 | Probably wrong, but possible |
| 0.1 | Would be surprised if right |

### Common Mistakes

**Overconfidence**: Saying 0.9 when you're really at 0.6
- Fix: Track your history; reality humbles quickly

**Underconfidence**: Saying 0.5 for everything
- Fix: Force yourself to take a position

**Avoiding predictions**: "I don't know"
- Fix: Estimate anyway; add low confidence. Learning requires predictions.

---

## Required for RAMP ≥ 3

When a decision is RAMP 3+ and marked Final:

✅ At least 1 `expected_outcome` with `confidence` must exist

This forces you to make a testable prediction.

---

## The Calibration Loop

```
1. Make prediction (before action)
       ↓
2. Take action
       ↓
3. Observe reality (OUTCOME check)
       ↓
4. Compare: predicted vs actual
       ↓
5. Calculate calibration (over time)
       ↓
6. Adjust future predictions
```

---

## Exercise: Add Predictions (10 min)

For a decision you're making:

### Step 1: List 2-3 Measurable Outcomes

| What will you measure? |
|-----------------------|
| 1. |
| 2. |
| 3. |

### Step 2: Make Predictions

For each:

| Metric | Expected | Confidence | Horizon |
|--------|----------|------------|---------|
| | | | |
| | | | |
| | | | |

### Step 3: Schedule Check

When will you compare predictions to reality?

**Check date**: ___

---

## Tracking Calibration Over Time

Keep a simple log:

| Decision | Prediction | Confidence | Actual | Accurate? |
|----------|------------|------------|--------|-----------|
| Feature X launch | 40% adoption | 0.7 | 35% | ✅ (close) |
| Vendor timeline | 2 months | 0.8 | 3 months | ❌ |
| Hiring success | 90-day retention | 0.6 | Retained | ✅ |

After 10+ predictions:
- What's your accuracy at each confidence level?
- Where do you over/underestimate?
- What domain are you best/worst at?

---

## The Three Calibration Questions

At every OUTCOME check, ask:

### 1. What did we predict?
Pull out the `expected_outcomes` from the MEMO.

### 2. What actually happened?
Log the `actual` value in the OUTCOME audit.

### 3. What's the delta?
Calculate: `actual - predicted`

Over time, patterns emerge:
- "We always underestimate timelines by 30%"
- "We overestimate user enthusiasm by 20%"
- "Our technical estimates are well-calibrated"

---

## Calibration as Skill

Good judgment isn't magic—it's trained through:

1. **Prediction forcing**: No "I don't know"
2. **Feedback loops**: Compare predictions to outcomes
3. **Explicit confidence**: Force yourself to quantify uncertainty
4. **Pattern recognition**: Learn your biases

DMG provides the infrastructure. You provide the reps.

---

## Key Takeaway

> Prediction without confidence is hope. Confidence without feedback is delusion.

The Calibration Track turns every decision into a training sample for better judgment.

---

## Next Step

→ [Capstone: Real Decision Project](./CAPSTONE.md)
