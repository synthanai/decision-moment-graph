# MERIT Validator Specification v1.0

**Status**: Draft  
**Version**: 1.0.0  
**Date**: January 2026  
**Related**: DMG Core Specification v0.1

---

## 1. Overview

The MERIT Validator is the canonical verification tool for assessing DMG decision objects against the five MERIT principles. Each principle maps directly to a DMG primitive:

> *"DMG decisions have MERIT — Measured with OUTCOME, Evidenced via MEMO, Reversible thru DOORS, Inspectable in MOMENT, Traceable by TRACE."*

### MERIT × DMG Primitive Mapping

| Principle | Primitive | What It Verifies |
|-----------|-----------|------------------|
| **M**easured | OUTCOME | Outcomes are quantified and linked to predictions |
| **E**videnced | MEMO | Decision is documented with options and rationale |
| **R**eversible | DOORS | Governance gates and rollback paths exist |
| **I**nspectable | MOMENT | Audit trail is present and cryptographically valid |
| **T**raceable | TRACE | Evidence provenance chain is complete |

---

## 2. Validation Architecture

### 2.1 System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     MERIT Validator                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Schema     │  │   MERIT      │  │   Report     │          │
│  │   Validator  │→ │   Analyzer   │→ │   Generator  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                │                   │                  │
│         ▼                ▼                   ▼                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   JSON       │  │   5 Principle│  │   JSON/MD/   │          │
│  │   Schema     │  │   Checkers   │  │   HTML/Badge │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Validation Pipeline

1. **Schema Validation**: Verify structural conformance
2. **MERIT Analysis**: Run 5 principle checkers
3. **Score Computation**: Calculate MERIT score (0-5)
4. **Report Generation**: Output validation report

---

## 3. MERIT Principle Checkers

### 3.1 M — Measured

**Purpose**: Verify that outcomes are quantified and linked to predictions.

**Checks**:

| Check | Condition | Weight |
|-------|-----------|--------|
| M1 | `objects.outcome` exists | 30% |
| M2 | `outcome.checks[]` has at least 1 entry | 30% |
| M3 | `expected_outcomes_audit[]` exists with `predicted` and `actual` values | 40% |

**Scoring**:
```python
def check_measured(dmg: dict) -> float:
    score = 0.0
    
    # M1: Outcome object exists
    if dmg.get("objects", {}).get("outcome"):
        score += 0.30
        
        outcome = dmg["objects"]["outcome"]
        
        # M2: Has at least one check
        checks = outcome.get("checks", [])
        if len(checks) > 0:
            score += 0.30
            
            # M3: Expected outcomes have predicted/actual
            for check in checks:
                audits = check.get("expected_outcomes_audit", [])
                if audits and all(a.get("predicted") and a.get("actual") for a in audits):
                    score += 0.40
                    break
                    
    return score
```

**Pass Threshold**: ≥ 0.6

---

### 3.2 E — Evidenced

**Purpose**: Verify that decisions are documented with options and rationale via MEMO.

**DMG Primitive**: `memo`

**Checks**:

| Check | Condition | Weight |
|-------|-----------|--------|
| E1 | `memo` exists with `decision` field | 30% |
| E2 | `memo.options[]` has at least 3 options | 40% |
| E3 | Each option has `rationale` or `pros`/`cons` documented | 30% |

**Scoring**:
```python
def check_evidenced(dmg: dict) -> float:
    score = 0.0
    
    memo = dmg.get("memo", {})
    
    # E1: MEMO exists with decision
    if memo and memo.get("decision"):
        score += 0.30
        
        # E2: At least 3 options
        options = memo.get("options", [])
        if len(options) >= 3:
            score += 0.40
            
            # E3: Options have rationale
            if all(opt.get("rationale") or (opt.get("pros") and opt.get("cons")) for opt in options):
                score += 0.30
            
    return score
```

**Pass Threshold**: ≥ 0.7

**Note**: While MEMO provides the decision evidence (E), TRACE provides source provenance for specific claims (T). Both contribute to overall decision transparency.

---

### 3.3 R — Reversible

**Purpose**: Verify that governance gates and rollback paths exist.

**Checks**:

| Check | Condition | Weight |
|-------|-----------|--------|
| R1 | `objects.doors` exists | 25% |
| R2 | `doors.own.name` is populated | 25% |
| R3 | `doors.ready` (rollback plan) is documented | 25% |
| R4 | `memo.ramp.time_to_undo` is specified | 25% |

**Scoring**:
```python
def check_reversible(dmg: dict) -> float:
    score = 0.0
    
    doors = dmg.get("objects", {}).get("doors", {})
    ramp = dmg.get("memo", {}).get("ramp", {})
    
    # R1: DOORS exists
    if doors:
        score += 0.25
        
        # R2: Owner named
        if doors.get("own", {}).get("name"):
            score += 0.25
            
        # R3: Rollback plan documented
        if doors.get("ready"):
            score += 0.25
            
    # R4: Time to undo specified
    if ramp.get("time_to_undo"):
        score += 0.25
        
    return score
```

**Pass Threshold**: ≥ 0.75

---

### 3.4 I — Inspectable

**Purpose**: Verify that audit trail is present and cryptographically valid.

**Checks**:

| Check | Condition | Weight |
|-------|-----------|--------|
| I1 | `moment.events[]` exists and is non-empty | 30% |
| I2 | All events have `hash` and `prev_hash` fields | 30% |
| I3 | Hash chain is valid (each hash correctly references prev) | 40% |

**Scoring**:
```python
import hashlib

def check_inspectable(dmg: dict) -> float:
    score = 0.0
    
    events = dmg.get("moment", {}).get("events", [])
    
    # I1: Events exist
    if len(events) > 0:
        score += 0.30
        
        # I2: All events have hash fields
        if all(e.get("hash") and (e.get("prev_hash") or e.get("seq") == 1) for e in events):
            score += 0.30
            
            # I3: Hash chain valid
            if verify_hash_chain(events):
                score += 0.40
                
    return score

def verify_hash_chain(events: list) -> bool:
    """Verify cryptographic hash chain integrity."""
    for i, event in enumerate(events):
        if i == 0:
            if event.get("prev_hash") not in [None, "", "genesis"]:
                return False
        else:
            if event.get("prev_hash") != events[i-1].get("hash"):
                return False
    return True
```

**Pass Threshold**: ≥ 0.7

---

### 3.5 T — Traceable

**Purpose**: Verify that evidence provenance chain is complete via TRACE objects.

**DMG Primitive**: `objects.traces`

**Checks**:

| Check | Condition | Weight |
|-------|-----------|--------|
| T1 | `objects.traces[]` exists and is non-empty | 40% |
| T2 | All traces have `source.uri` or `source.type` | 30% |
| T3 | At least one trace has `strength: "strong"` | 30% |

**Scoring**:
```python
def check_traceable(dmg: dict) -> float:
    score = 0.0
    
    traces = dmg.get("objects", {}).get("traces", [])
    
    if len(traces) == 0:
        return 0.0
        
    # T1: TRACE objects exist
    score += 0.40
    
    # T2: All traces have source provenance
    if all(t.get("source", {}).get("uri") or t.get("source", {}).get("type") for t in traces):
        score += 0.30
        
    # T3: At least one strong trace
    if any(t.get("strength") == "strong" for t in traces):
        score += 0.30
        
    return score
```

**Pass Threshold**: ≥ 0.7

**Note**: TRACE provides source provenance for claims (T), while MOMENT provides the event audit trail (I). Together they ensure full decision transparency.

---

## 4. Overall MERIT Score

### 4.1 Score Computation

```python
def compute_merit_score(dmg: dict) -> dict:
    """Compute overall MERIT score and level."""
    
    scores = {
        "M": check_measured(dmg),
        "E": check_evidenced(dmg),
        "R": check_reversible(dmg),
        "I": check_inspectable(dmg),
        "T": check_traceable(dmg)
    }
    
    thresholds = {"M": 0.6, "E": 0.7, "R": 0.75, "I": 0.7, "T": 0.7}
    
    passed = sum(1 for k, v in scores.items() if v >= thresholds[k])
    
    if passed == 5:
        level = "MERIT-Valid"
    elif passed >= 3:
        level = "MERIT-Partial"
    else:
        level = "MERIT-None"
        
    return {
        "scores": scores,
        "passed": passed,
        "level": level,
        "details": {
            k: {"score": v, "threshold": thresholds[k], "passed": v >= thresholds[k]}
            for k, v in scores.items()
        }
    }
```

### 4.2 Level Definitions

| Level | Criteria | Badge |
|-------|----------|-------|
| **MERIT-None** | 0-2 principles pass | 🔴 |
| **MERIT-Partial** | 3-4 principles pass | 🟡 |
| **MERIT-Valid** | All 5 principles pass | 🟢 |
| **MERIT-Certified** | MERIT-Valid + third-party audit | 🏆 |

---

## 5. CLI Interface

### 5.1 Basic Usage

```bash
# Validate a single file
dmg validate --merit decision.dmg.json

# Validate with specific output format
dmg validate --merit --format json decision.dmg.json
dmg validate --merit --format markdown decision.dmg.json

# Validate all files in directory
dmg validate --merit --recursive ./decisions/

# Generate badge
dmg validate --merit --badge decision.dmg.json > badge.svg
```

### 5.2 Output Formats

**JSON Output**:
```json
{
  "file": "decision.dmg.json",
  "valid_schema": true,
  "merit": {
    "level": "MERIT-Valid",
    "passed": 5,
    "scores": {
      "M": 1.0,
      "E": 0.85,
      "R": 1.0,
      "I": 0.9,
      "T": 1.0
    },
    "details": {
      "M": {"score": 1.0, "threshold": 0.6, "passed": true, "checks": ["M1", "M2", "M3"]},
      "E": {"score": 0.85, "threshold": 0.7, "passed": true, "checks": ["E1", "E2"]},
      "R": {"score": 1.0, "threshold": 0.75, "passed": true, "checks": ["R1", "R2", "R3", "R4"]},
      "I": {"score": 0.9, "threshold": 0.7, "passed": true, "checks": ["I1", "I2"]},
      "T": {"score": 1.0, "threshold": 0.7, "passed": true, "checks": ["T1", "T2", "T3"]}
    }
  },
  "timestamp": "2026-01-25T05:20:00Z"
}
```

**Markdown Output**:
```markdown
# MERIT Validation Report

**File**: `decision.dmg.json`  
**Level**: 🟢 MERIT-Valid  
**Passed**: 5/5 principles  

## Principle Scores

| Principle | Score | Threshold | Status |
|-----------|-------|-----------|--------|
| **M**easured | 100% | 60% | ✅ Pass |
| **E**videnced | 85% | 70% | ✅ Pass |
| **R**eversible | 100% | 75% | ✅ Pass |
| **I**nspectable | 90% | 70% | ✅ Pass |
| **T**raceable | 100% | 70% | ✅ Pass |

## Recommendations

None — this decision achieves full MERIT compliance.
```

### 5.3 Exit Codes

| Code | Meaning |
|------|---------|
| 0 | MERIT-Valid (all 5 pass) |
| 1 | MERIT-Partial (3-4 pass) |
| 2 | MERIT-None (0-2 pass) |
| 3 | Schema validation failed |
| 4 | File not found / parse error |

---

## 6. Integration Patterns

### 6.1 CI/CD Pipeline

```yaml
# .github/workflows/dmg-validate.yml
name: DMG MERIT Validation

on:
  push:
    paths:
      - 'decisions/**/*.dmg.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install DMG CLI
        run: npm install -g @dmg/cli
        
      - name: Validate MERIT
        run: |
          dmg validate --merit --recursive ./decisions/
          if [ $? -ne 0 ]; then
            echo "::error::MERIT validation failed"
            exit 1
          fi
          
      - name: Generate Badge
        run: dmg validate --merit --badge ./decisions/ > merit-badge.svg
        
      - name: Upload Badge
        uses: actions/upload-artifact@v4
        with:
          name: merit-badge
          path: merit-badge.svg
```

### 6.2 Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

DMG_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.dmg\.json$')

if [ -n "$DMG_FILES" ]; then
    echo "Validating MERIT compliance..."
    
    for file in $DMG_FILES; do
        result=$(dmg validate --merit --format json "$file")
        level=$(echo "$result" | jq -r '.merit.level')
        
        if [ "$level" = "MERIT-None" ]; then
            echo "❌ MERIT-None: $file"
            echo "   Decisions must achieve at least MERIT-Partial to commit."
            exit 1
        fi
        
        echo "✅ $level: $file"
    done
fi

exit 0
```

### 6.3 Editor Integration

```json
// VS Code settings.json
{
  "dmg.validation.enabled": true,
  "dmg.validation.merit": true,
  "dmg.validation.onSave": true,
  "dmg.validation.showBadge": true
}
```

---

## 7. Implementation Reference

### 7.1 Python Reference Implementation

See `/cli/dmg_validate.py` for the canonical implementation.

### 7.2 JavaScript Implementation

```javascript
// merit-validator.js
export function validateMerit(dmg) {
  const scores = {
    M: checkMeasured(dmg),
    E: checkEvidenced(dmg),
    R: checkReversible(dmg),
    I: checkInspectable(dmg),
    T: checkTraceable(dmg)
  };
  
  const thresholds = { M: 0.6, E: 0.7, R: 0.75, I: 0.7, T: 0.7 };
  const passed = Object.entries(scores).filter(([k, v]) => v >= thresholds[k]).length;
  
  let level;
  if (passed === 5) level = 'MERIT-Valid';
  else if (passed >= 3) level = 'MERIT-Partial';
  else level = 'MERIT-None';
  
  return { scores, passed, level };
}
```

---

## Appendix A: Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         MERIT VALIDATION QUICK REFERENCE                       ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  "DMG decisions have MERIT — Measured with OUTCOME, Evidenced via MEMO,       ║
║   Reversible thru DOORS, Inspectable in MOMENT, Traceable by TRACE."          ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  MERIT × PRIMITIVE MAPPING                                                    ║
║  ───────────────────────────────────────────────────────────────              ║
║  M · Measured    ← OUTCOME   outcome.checks[] with predictions/actuals        ║
║  E · Evidenced   ← MEMO      memo.options[] >= 3 with rationale               ║
║  R · Reversible  ← DOORS     doors.own.name + doors.ready populated           ║
║  I · Inspectable ← MOMENT    moment.events[] with valid hash chain            ║
║  T · Traceable   ← TRACE     traces[] with source.uri/type                    ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  LEVELS                                                                       ║
║  ───────────────────────────────────────────────────────────────              ║
║  🔴 MERIT-None     0-2 principles pass                                        ║
║  🟡 MERIT-Partial  3-4 principles pass                                        ║
║  🟢 MERIT-Valid    5/5 principles pass                                        ║
║  🏆 MERIT-Certified MERIT-Valid + third-party audit                           ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  COMMANDS                                                                     ║
║  ───────────────────────────────────────────────────────────────              ║
║  dmg validate --merit <file>           Validate single file                   ║
║  dmg validate --merit --recursive .    Validate all files                     ║
║  dmg validate --merit --badge <file>   Generate SVG badge                     ║
║  dmg validate --merit --ci <dir>       CI mode (exit codes)                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

*End of MERIT Validator Specification v1.0*
