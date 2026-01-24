# M9: Integration — Full DMG Workflow

**Time**: 20 minutes  
**Goal**: Connect all 8 kits into a single decision workflow

---

## The Complete Picture

You've learned the 8 DMG primitives:

| Kit | What It Does |
|-----|--------------|
| MEMO | The shareable decision brief |
| MOMENT | Provenance trail |
| RAMP | Proportional governance |
| DOORS | Reversibility checklist |
| DISSENT | Structured disagreement |
| TRACE | Evidence links |
| COMMIT | State transitions |
| OUTCOME | Learning loops |

Now let's see how they work **together**.

---

## The DMG Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        DECISION LIFECYCLE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. FRAME                    2. DELIBERATE                       │
│  ┌─────────────┐            ┌─────────────┐                     │
│  │   Create    │            │   Capture   │                     │
│  │   MEMO      │───────────▶│   DISSENT   │                     │
│  │   (options) │            │   + TRACE   │                     │
│  └─────────────┘            └─────────────┘                     │
│        │                           │                             │
│        │                           │                             │
│        ▼                           ▼                             │
│  3. GOVERN                   4. COMMIT                          │
│  ┌─────────────┐            ┌─────────────┐                     │
│  │  Set RAMP   │            │   State:    │                     │
│  │  + DOORS    │───────────▶│   Final     │                     │
│  │  (signals)  │            │ (governance │                     │
│  └─────────────┘            │   gates)    │                     │
│                             └─────────────┘                     │
│                                    │                             │
│                                    │                             │
│                                    ▼                             │
│  5. EXECUTE                  6. LEARN                           │
│  ┌─────────────┐            ┌─────────────┐                     │
│  │   Action    │            │  OUTCOME    │                     │
│  │     +       │───────────▶│   check     │                     │
│  │   MOMENT    │            │ (audits +   │                     │
│  │   events    │            │  verdict)   │                     │
│  └─────────────┘            └─────────────┘                     │
│                                    │                             │
│                                    │                             │
│                                    ▼                             │
│                            ┌─────────────┐                      │
│                            │  Precedent  │                      │
│                            │ (case law)  │                      │
│                            └─────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Putting It Together: A Real Example

Let's walk through a complete DMG cycle for:

> **Decision**: Should we build feature X in-house or buy a vendor solution?

### Step 1: Frame (MEMO)

```markdown
## MEMO: Build vs Buy — Customer Analytics Feature

**Decision**: Buy vendor solution (Mixpanel) with custom integration layer

**Options**:
1. Build in-house (6 months, 3 engineers)
2. Buy Mixpanel + integrate (2 months, 1 engineer) ← Chosen
3. Buy Amplitude as alternative
4. Do nothing; use existing basic analytics

**Recommendation**: Option 2. Faster time-to-value; preserves
engineering capacity for core product.

**Owner**: Sarah Chen (Product)
**Review Date**: March 24, 2026
```

### Step 2: Deliberate (DISSENT + TRACE)

```markdown
## DISSENT #1
**Author**: Marcus Lee (Engineering Lead)
**Claim**: Vendor lock-in risk is underestimated; switching
costs will exceed build costs within 18 months

**Evidence**:
- Prior vendor (Segment) took 4 months to replace
- Mixpanel pricing increases 20% annually

**Conditions to change mind**: If we can exit Mixpanel
with < 2 weeks migration effort, vendor is acceptable

**Resolution**: mitigated — Added 6-month exit clause to contract
```

```markdown
## TRACE #1
**Claim**: Mixpanel implementation takes 2 months
**Source**: Mixpanel case study (retrieved Jan 20)
**Strength**: medium (vendor-provided, may be optimistic)
```

### Step 3: Govern (RAMP + DOORS)

```markdown
## RAMP
**Level**: 3
**Time to undo**: 2-3 months (contract minimum + data migration)

## DOORS
**D - Declare**: We commit to Mixpanel with custom integration layer
**O - Observe**: Implementation timeline, data accuracy, support quality
**O - Own**: Marcus Lee (Engineering Lead)
**R - Ready**: Migration script to BigQuery; contract exit clause

**S - Signals**:
| Metric | Threshold | Horizon | Action |
|--------|-----------|---------|--------|
| Implementation delay | > 1 month | 8 weeks | Trigger review |
| Data accuracy | < 95% | 4 weeks | Investigate or exit |
```

### Step 4: Commit

```markdown
## COMMIT
**State**: Final
**Changed at**: 2026-01-24T16:00:00Z
**Changed by**: Sarah Chen

**Conditions to stay committed**:
- Budget remains <$50k/year
- Core feature work not impacted
- No acquisition/pricing change at Mixpanel
```

### Step 5: Execute + Log (MOMENT)

The MOMENT trail records:
```
Event 1: MEMO_CREATED (Jan 20)
Event 2: DISSENT_ADDED (Jan 21, Marcus)
Event 3: DISSENT_RESOLVED (Jan 22)
Event 4: RAMP_SET (level 3, Jan 22)
Event 5: DOORS_UPDATED (Jan 22)
Event 6: SOURCE_ATTACHED (Mixpanel case study)
Event 7: COMMIT_STATE_CHANGED (Draft → Final, Jan 24)
```

### Step 6: Learn (OUTCOME)

Two months later:

```markdown
## OUTCOME Check (March 24, 2026)

**Actual Result**: Implementation took 3 months (50% overrun)

### Assumptions Audit
| Assumption | Accurate? | Learning |
|------------|-----------|----------|
| 2-month implementation | ❌ | Vendor estimates need 50% buffer |
| 1 engineer sufficient | ❌ | Integration required 1.5 FTEs |

### Dissent Audit
| Dissent | Vindicated? | Notes |
|---------|-------------|-------|
| Marcus: lock-in risk | Partial | Exit clause helped; timeline was right |

### Expected vs Actual
| Metric | Predicted | Actual | Delta |
|--------|-----------|--------|-------|
| Timeline | 2 months | 3 months | +50% |
| Cost | $40k | $55k | +37% |

### Verdict: Adjust
Added 50% buffer to all future vendor implementation estimates.
```

---

## Exercise: Full DMG Cycle (15 min)

Pick a decision you're facing. Build a complete DMG:

1. **MEMO**: Title, decision, ≥3 options, recommendation, owner
2. **TRACE**: Add 1-2 evidence links
3. **DISSENT**: Add 1 structured objection (you can argue with yourself)
4. **RAMP + DOORS**: Level, justification, rollback owner, 2 signals
5. **COMMIT**: State, conditions to stay committed
6. **OUTCOME**: Schedule a check date

Don't skip sections—see how they connect.

---

## The Validation Checkpoint

Before marking a decision Final, run through:

| Check | Question | Required For |
|-------|----------|--------------|
| ≥3 options | Did we consider alternatives? | All |
| RAMP level | How reversible is this? | All |
| DISSENT ≥1 | Is disagreement captured? | RAMP ≥3 |
| DOORS owner | Who owns rollback? | RAMP ≥3 |
| DOORS signals ≥2 | What triggers reversal? | RAMP ≥3 |
| Expected outcome | What do we predict? | RAMP ≥3 |
| Outcome check | When do we review? | All Final |

---

## Key Takeaway

> DMG isn't 8 separate tools. It's one coherent system.

When all kits work together:
- Decisions are structured (MEMO)
- Evidence is traceable (TRACE)
- Disagreement is productive (DISSENT)
- Governance is proportional (RAMP)
- Reversibility is concrete (DOORS)
- States are explicit (COMMIT)
- History is inspectable (MOMENT)
- Learning is inevitable (OUTCOME)

---

## Next Step

→ [M10: Calibration Track — Predictions](./M10_CALIBRATION_TRACK.md)
