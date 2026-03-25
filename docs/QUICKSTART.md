# DMG Quickstart — Your First Decision in 5 Minutes

Get from zero to your first **MERIT-valid** decision in 5 minutes.

## Prerequisites

- Node.js 18+ or Python 3.9+
- A text editor

---

## Step 1: Install the CLI (30 seconds)

```bash
# Python
pip install dmg-cli

# Or npm
npm install -g @dmg/cli
```

---

## Step 2: Create Your First Decision (2 minutes)

Create `my_decision.dmg.json`:

```json
{
  "dmg_version": "0.1",
  "memo": {
    "memo_id": "my-first-decision",
    "title": "Should we adopt TypeScript?",
    "decision": "Adopt TypeScript for all new projects",
    "options": [
      {
        "id": "ts-full",
        "title": "Full TypeScript adoption",
        "rationale": "Maximum type safety, better tooling, easier refactoring"
      },
      {
        "id": "ts-gradual",
        "title": "Gradual TypeScript migration",
        "rationale": "Lower risk, team can learn incrementally"
      },
      {
        "id": "js-stay",
        "title": "Stay with JavaScript",
        "rationale": "No migration cost, JSDoc provides some type hints"
      }
    ],
    "recommendation": "ts-gradual",
    "ramp": {
      "level": 3,
      "justification": "Affects entire codebase over 6 months",
      "time_to_undo": "3 months"
    }
  },
  "moment": {
    "moment_id": "my-first-decision-log",
    "memo_id": "my-first-decision",
    "events": [
      {
        "event_id": "e1",
        "seq": 1,
        "ts": "2026-01-26T10:00:00Z",
        "type": "MEMO_CREATED",
        "actor": "you@example.com",
        "payload": {},
        "prev_hash": "",
        "hash": "abc123"
      }
    ]
  },
  "objects": {
    "doors": {
      "declare": "We will adopt TypeScript gradually",
      "observe": ["Build times", "Developer velocity", "Bug rates"],
      "own": {
        "name": "Your Name",
        "role": "Tech Lead"
      },
      "ready": "Can revert by removing TS from tsconfig",
      "signals": [
        {
          "metric": "Build time",
          "threshold": "> 5 minutes",
          "horizon": "4 weeks",
          "action": "Review TS compilation strategy"
        }
      ]
    },
    "traces": [
      {
        "trace_id": "t1",
        "claim": "TypeScript reduces bugs by 15%",
        "source": {
          "type": "study",
          "uri": "https://example.com/ts-study"
        },
        "strength": "strong"
      }
    ],
    "outcome": {
      "outcome_id": "o1",
      "next_check_date": "2026-04-26",
      "checks": []
    }
  }
}
```

---

## Step 3: Validate (30 seconds)

```bash
# Validate schema
dmg validate my_decision.dmg.json

# Check MERIT compliance
dmg validate --merit my_decision.dmg.json
```

**Expected output:**
```
✅ Schema: Valid
✅ MERIT Level: MERIT-Valid (5/5)
   M: Measured    ✓ (OUTCOME exists)
   E: Evidenced   ✓ (MEMO with 3+ options)
   R: Reversible  ✓ (DOORS complete)
   I: Inspectable ✓ (MOMENT with events)
   T: Traceable   ✓ (TRACE with sources)
```

---

## Step 4: Commit to Git (1 minute)

```bash
mkdir decisions
mv my_decision.dmg.json decisions/
git add decisions/
git commit -m "decision(typescript): Adopt TypeScript gradually"
```

---

## Step 5: Schedule Outcome Check (30 seconds)

Add to your calendar: **"TypeScript Adoption Review"** in 3 months.

When the date arrives, update the `outcome.checks[]` array:

```json
{
  "check_date": "2026-04-26",
  "actual_result": "Build time stayed under 2 minutes",
  "assumptions_audit": [
    {
      "assumption": "Team can learn TS in 3 months",
      "accurate": true
    }
  ],
  "verdict": "keep"
}
```

---

## 🎉 Done!

You just created a **MERIT-valid** decision with:

- ✅ **M**easured outcomes (OUTCOME scheduled)
- ✅ **E**videnced reasoning (MEMO with 3 options)
- ✅ **R**eversible path (DOORS with rollback)
- ✅ **I**nspectable history (MOMENT event log)
- ✅ **T**raceable sources (TRACE with citations)

---

## Next Steps

- [Full Specification](./spec/DMG_CORE_SPEC_v0.1.md)
- [MERIT Validation Rules](./spec/MERIT_VALIDATOR_SPEC.md)
- [Course: DMG Fundamentals](./course/README.md)
- [Example Decisions](./examples/)
