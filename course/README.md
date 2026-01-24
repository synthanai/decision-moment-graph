# DMG Online Course

> **Stop storing chats. Store decision objects.**

A self-paced course to master Decision Moment Graph — the open standard for decision governance.

---

## Course Overview

| Stat | Value |
|------|-------|
| **Modules** | 12 (M0-M10 + Capstone) |
| **Total Time** | ~3 hours |
| **Format** | Self-paced |
| **Prerequisites** | A real decision to make |

---

## Module Map

| Module | Title | Time | Learn To |
|--------|-------|------|----------|
| **M0** | [Start Here](./modules/M0_START_HERE.md) | 5 min | Understand DMG; build your first MEMO skeleton |
| **M1** | [MEMO-KIT](./modules/M1_MEMO_KIT.md) | 15 min | Create a shareable decision brief with ≥3 options |
| **M2** | [MOMENT-KIT](./modules/M2_MOMENT_KIT.md) | 15 min | Understand append-only provenance |
| **M3** | [RAMP-KIT](./modules/M3_RAMP_KIT.md) | 15 min | Apply proportional governance (L1-L5) |
| **M4** | [DOORS-KIT](./modules/M4_DOORS_KIT.md) | 15 min | Build reversibility into every commitment |
| **M5** | [DISSENT-KIT](./modules/M5_DISSENT_KIT.md) | 15 min | Capture structured disagreement |
| **M6** | [TRACE-KIT](./modules/M6_TRACE_KIT.md) | 10 min | Link claims to evidence |
| **M7** | [COMMIT-KIT](./modules/M7_COMMIT_KIT.md) | 10 min | Manage decision state transitions |
| **M8** | [OUTCOME-KIT](./modules/M8_OUTCOME_KIT.md) | 15 min | Close the learning loop |
| **M9** | [Integration](./modules/M9_INTEGRATION.md) | 20 min | Connect all 8 kits in a full workflow |
| **M10** | [Calibration Track](./modules/M10_CALIBRATION_TRACK.md) | 15 min | Add predictions and calibrate judgment |
| **Capstone** | [Real Decision Project](./modules/CAPSTONE.md) | 30 min | Apply everything to a real decision |

---

## Learning Path

```
M0 Start Here
    │
    ├── M1 MEMO-KIT ────────┐
    │                       │
    ├── M2 MOMENT-KIT       │
    │                       │
    ├── M3 RAMP-KIT ────────┼── Governance
    │                       │   Layer
    ├── M4 DOORS-KIT ───────┘
    │
    ├── M5 DISSENT-KIT ─────┐
    │                       │
    ├── M6 TRACE-KIT        ├── Evidence
    │                       │   Layer
    ├── M7 COMMIT-KIT ──────┘
    │
    ├── M8 OUTCOME-KIT ─────── Learning
    │                          Layer
    ├── M9 Integration ─────── Full
    │                          Workflow
    ├── M10 Calibration ────── Advanced
    │
    └── Capstone ──────────── Apply
                               It All
```

---

## Pedagogy: Do → See → Name

Each module follows the same pattern:

1. **Do**: Build an artifact first
2. **See**: Compare weak vs strong examples
3. **Name**: Understand the concept

Don't memorize definitions. **Build artifacts.**

---

## The 8 Kits At a Glance

| Kit | Purpose | Required Fields |
|-----|---------|-----------------|
| **MEMO** | Decision brief | title, decision, options (≥3), recommendation, ramp |
| **MOMENT** | Provenance log | events with seq, ts, actor, type |
| **RAMP** | Governance level | level (1-5) |
| **DOORS** | Reversibility | declare, observe, own, ready, signals |
| **DISSENT** | Disagreement | author, claim, conditions_to_change_mind |
| **TRACE** | Evidence | claim, source, strength |
| **COMMIT** | State | state (Draft→Final→Reversed) |
| **OUTCOME** | Learning | next_check_date, checks |

---

## Governance Gates

When finalizing a decision:

### All Decisions
- ✅ `outcome.next_check_date` required

### RAMP ≥ 3 Decisions
- ✅ At least 1 DISSENT
- ✅ Rollback owner (DOORS.own.name)
- ✅ ≥2 reversal signals (DOORS.signals)
- ✅ At least 1 expected outcome with confidence

---

## After the Course

### Practice
- Run the capstone on 3-5 more decisions
- Track your prediction calibration

### Teach
- Facilitate a team workshop
- Use the [Facilitator Kit](../assets/facilitator_kit.md)

### Contribute
- Submit DIPs (DMG Improvement Proposals)
- Improve documentation
- Build tools on the standard

---

## Resources

| Resource | Description |
|----------|-------------|
| [DMG Core Spec](../spec/DMG_CORE_SPEC_v0.1.md) | Full specification |
| [JSON Schema](../schema/dmg-core-v0.1.schema.json) | Machine-readable schema |
| [Validator CLI](../cli/dmg_validate.py) | Validate DMG files |
| [Example DMG](../examples/onboarding_decision.dmg.json) | Complete example |
| [The 8 Kits](../docs/KITS.md) | Kit reference |

---

## License

This course is MIT licensed. Share freely.

**Trademarks**: "DMG" and "Decision Moment Graph" are trademarks of SYNTHAI TECH PTY LTD.

---

*Start now: [M0: Start Here](./modules/M0_START_HERE.md)*
