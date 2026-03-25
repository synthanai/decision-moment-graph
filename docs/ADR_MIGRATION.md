# Migrating from ADRs to DMG

A practical guide for teams already using Architecture Decision Records (ADRs).

---

## Why Migrate?

| ADR Limitation | DMG Solution |
|----------------|--------------|
| Static documents | Living decision lifecycle |
| No outcome tracking | Built-in OUTCOME checks |
| No dissent capture | Formal DISSENT with resolution |
| No governance gates | RAMP levels + DOORS framework |
| No audit trail | MOMENT hash chain |

---

## Migration Levels

### Level 1: Parallel Operation
Keep ADRs, add DMG for new strategic decisions.

### Level 2: Gradual Conversion
Convert high-impact ADRs to DMG format.

### Level 3: Full Migration
All decisions in DMG, ADRs archived.

---

## ADR → DMG Mapping

| ADR Field | DMG Field | Notes |
|-----------|-----------|-------|
| Title | `memo.title` | Direct mapping |
| Status | `objects.commit.state` | Proposed→Draft, Accepted→Final |
| Context | `memo.context.constraints` | Split into constraints/assumptions |
| Decision | `memo.decision` | Direct mapping |
| Consequences | `memo.expected_outcomes` | Add confidence scores |
| Date | `moment.events[0].ts` | First event timestamp |
| Authors | `moment.events[0].actor` | Creator of MEMO |

---

## Conversion Script

```python
#!/usr/bin/env python3
"""Convert ADR markdown to DMG JSON."""

import re
import json
from datetime import datetime
from pathlib import Path

def convert_adr_to_dmg(adr_path: Path) -> dict:
    """Convert a single ADR file to DMG format."""
    content = adr_path.read_text()
    
    # Parse ADR fields
    title = re.search(r"#\s*(.+)", content)
    status = re.search(r"\*\*Status[:\s]*\*\*\s*(\w+)", content, re.I)
    context = re.search(r"##\s*Context\n+(.+?)(?=##|\Z)", content, re.S)
    decision = re.search(r"##\s*Decision\n+(.+?)(?=##|\Z)", content, re.S)
    consequences = re.search(r"##\s*Consequences\n+(.+?)(?=##|\Z)", content, re.S)
    
    # Map status
    status_map = {
        "proposed": "Draft",
        "accepted": "Final",
        "deprecated": "Superseded",
        "superseded": "Superseded"
    }
    
    commit_state = status_map.get(
        status.group(1).lower() if status else "proposed", 
        "Draft"
    )
    
    # Build DMG
    dmg = {
        "dmg_version": "0.1",
        "memo": {
            "memo_id": adr_path.stem,
            "title": title.group(1).strip() if title else adr_path.stem,
            "decision": decision.group(1).strip()[:500] if decision else "Migrated from ADR",
            "options": [
                {"id": "chosen", "title": "Chosen approach", "rationale": "As documented in ADR"},
                {"id": "alternative1", "title": "Alternative 1", "rationale": "Considered but rejected"},
                {"id": "alternative2", "title": "Alternative 2", "rationale": "Considered but rejected"}
            ],
            "recommendation": "chosen",
            "ramp": {
                "level": 3,
                "justification": "Architectural decision (migrated from ADR)",
                "time_to_undo": "Unknown"
            },
            "context": {
                "constraints": [context.group(1).strip()[:200]] if context else [],
                "assumptions": []
            }
        },
        "moment": {
            "moment_id": f"{adr_path.stem}-log",
            "memo_id": adr_path.stem,
            "events": [
                {
                    "event_id": "e1",
                    "seq": 1,
                    "ts": datetime.now().isoformat() + "Z",
                    "type": "MEMO_CREATED",
                    "actor": "adr-migration@system",
                    "payload": {"source": str(adr_path)},
                    "prev_hash": "",
                    "hash": "migrated"
                }
            ]
        },
        "objects": {
            "commit": {
                "state": commit_state,
                "changed_at": datetime.now().isoformat() + "Z",
                "changed_by": "adr-migration@system"
            },
            "outcome": {
                "outcome_id": "o1",
                "next_check_date": None,
                "checks": []
            }
        }
    }
    
    # Add consequences as expected outcomes
    if consequences:
        dmg["memo"]["expected_outcomes"] = [
            {"metric": "Consequence", "predicted": consequences.group(1).strip()[:200], "confidence": 0.5}
        ]
    
    return dmg


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python adr_to_dmg.py <adr_file.md>")
        sys.exit(1)
    
    adr_path = Path(sys.argv[1])
    dmg = convert_adr_to_dmg(adr_path)
    
    output_path = adr_path.with_suffix(".dmg.json")
    output_path.write_text(json.dumps(dmg, indent=2))
    print(f"✅ Converted: {adr_path} → {output_path}")


if __name__ == "__main__":
    main()
```

---

## Post-Migration Checklist

After converting an ADR:

- [ ] Add at least 3 options (ADRs typically only document the chosen option)
- [ ] Assign RAMP level appropriate to decision impact
- [ ] Set `outcome.next_check_date` if decision is Final
- [ ] Add DOORS ownership for reversibility tracking
- [ ] Add TRACE sources for key claims

---

## Side-by-Side Comparison

### ADR Format
```markdown
# ADR 1: Use PostgreSQL for persistence

**Status**: Accepted

## Context
We need a database for our application...

## Decision
We will use PostgreSQL...

## Consequences
- Good: ACID compliance
- Bad: Operational complexity
```

### DMG Format
```json
{
  "dmg_version": "0.1",
  "memo": {
    "memo_id": "adr-001-postgresql",
    "title": "Use PostgreSQL for persistence",
    "decision": "We will use PostgreSQL",
    "options": [
      {"id": "postgres", "title": "PostgreSQL", "rationale": "ACID, mature, extensions"},
      {"id": "mysql", "title": "MySQL", "rationale": "Popular, simple"},
      {"id": "mongodb", "title": "MongoDB", "rationale": "Document model, flexible"}
    ],
    "recommendation": "postgres",
    "ramp": {"level": 4, "justification": "Core infrastructure", "time_to_undo": "6 months"},
    "expected_outcomes": [
      {"metric": "Query latency p99", "predicted": "< 50ms", "confidence": 0.8}
    ]
  },
  "objects": {
    "doors": {
      "declare": "Adopting PostgreSQL as primary database",
      "observe": ["Query latency", "Connection pool utilization"],
      "own": {"name": "Platform Team", "role": "Database Owner"},
      "ready": "Migration path to different DB exists via ORM abstraction"
    },
    "outcome": {
      "outcome_id": "o1",
      "next_check_date": "2026-07-26"
    }
  }
}
```

---

*End of ADR Migration Guide*
