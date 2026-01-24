# DIP-001: Add OUTCOME Object as First-Class Primitive

**Status**: Accepted  
**Created**: 2026-01-24  
**Author**: SYNTHAI Core Team

---

## Summary

Add `OUTCOME` as a required first-class object in the DMG specification, enabling dialectical learning by tracking what actually happened after decisions were made.

## Motivation

> "Store decision objects, not chats."

Current decision systems capture the *decision* but not the *learning*. Without structured outcome tracking:

- Assumptions go unaudited
- Predictions are never verified
- Dissent is never vindicated or refuted
- Organizations repeat mistakes

OUTCOME closes the loop.

## Specification

### New Object: `objects.outcome`

```json
{
  "outcome_id": "string",
  "next_check_date": "date",
  "checks": [
    {
      "check_date": "date",
      "actual_result": "string",
      "assumptions_audit": [...],
      "dissent_audit": [...],
      "expected_outcomes_audit": [...],
      "verdict": "keep|adjust|reverse",
      "next_action": "string"
    }
  ]
}
```

### New Governance Rule

For decisions with `commit.state` = `Final` or `Approved`:

✅ `outcome.next_check_date` MUST be set

### New RAMP ≥ 3 Rule

For decisions with `ramp.level` >= 3 AND `commit.state` = `Final`/`Approved`:

✅ `memo.expected_outcomes[]` MUST have at least 1 prediction with `confidence` (0-1)

## Rationale

This enables the **calibration loop**:

1. Make prediction → 2. Observe outcome → 3. Audit assumptions → 4. Update precedent

Without this, DMG documents but doesn't learn.

## Backward Compatibility

- Existing DMG files without `outcome` are valid at Bronze/Silver conformance
- Gold/Platinum conformance requires `outcome`

## Implementation

1. Add schema definition (✅ Done)
2. Add validator rules (✅ Done)
3. Add conformance fixtures (✅ Done)
4. Update course materials

## References

- DMG Core Spec v0.1
- ChatGPT SPAR Session: "Store decisions, not chats"

---

*DIP-001 was accepted and merged into DMG Core v0.1*
