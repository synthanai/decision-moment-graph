# DMG — Decision Moment Graph

> **Store decision moments, not raw chats, objects or data.**

DMG is an open standard for decision governance in the AI era.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conformance Tests](https://img.shields.io/badge/conformance-passing-green.svg)](#conformance)

---

## What is DMG?

**Decision Moment Graph** makes decisions:
- **Structured** — not narratives
- **Auditable** — provenance chain
- **Reversible** — governance gates
- **Learnable** — outcome loops

### The One-Liner

> "Decision graphs for the AI era — so LLMs synthesize auditable, reversible decisions, not just summarize documents."

---

## Core Objects

| Object | Purpose |
|--------|---------|
| **MEMO** | The shareable decision brief |
| **MOMENT** | Append-only provenance log |
| **RAMP** | Risk-proportional governance (L1-L5) |
| **DOORS** | Reversibility checklist |
| **DISSENT** | Structured disagreement + conditions |
| **TRACE** | Evidence links + citations |
| **COMMIT** | State transitions (Draft→Final) |
| **OUTCOME** | What actually happened |

---

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
# For embeddings: pip install sentence-transformers
```

### 2. Run RESOLVE Loop

```bash
python cli/resolve.py "Should we migrate to microservices?" --dry-run
```

Output:
```
📍 Phase 1: RECON — Define scope
📍 Phase 2: ENRICH — Check memory for prior decisions
📍 Phase 3: SPAR — Deliberate
📍 Phase 4: OKAY — Governance gate
📍 Phase 5: LAUNCH — Execute
📍 Phase 6: VERIFY — Observe
📍 Phase 7: ENCODE — Store to memory
```

### 3. Use as Library

```python
from sdk.python import AgenticSPARAdapter
from agentic_kit.dispatchers import LoggingDispatcher

adapter = AgenticSPARAdapter()
dispatcher = LoggingDispatcher()

result = adapter.run_loop(
    spar_output,
    action_executor=dispatcher.execute,
    auto_execute=True
)
```

---

## RESOLVE: The Agentic Loop

> **R**econ → **E**nrich → **S**PAR → **O**kay → **L**aunch → **V**erify → **E**ncode

| Phase | Purpose |
|-------|---------|
| **RECON** | Define decision boundaries |
| **ENRICH** | Retrieve prior decisions from memory |
| **SPAR** | Run structured deliberation |
| **OKAY** | Check governance gates |
| **LAUNCH** | Execute validated action |
| **VERIFY** | Observe actual outcome |
| **ENCODE** | Write back to memory |

### SDK Modules

| Module | Purpose |
|--------|---------|
| `agentic_adapter.py` | Core RESOLVE adapter (uses `agentic-kit`) |
| `spar_adapter.py` | Converts SPAR output to DMG |
| `sparkit_runner.py` | Embedded SPAR runner |
| `swarm_coordinator.py` | Parallel agent swarm orchestration |
| `audit_export.py` | Compliance reports |

> **Note:** Core primitives (`Memory`, `Dispatchers`, `Hub`, `Reflection`) are now imported from [`agentic-kit`](https://github.com/synthanai/agentic-kit).

## Repository Structure

```
dmg-open-standard/
├── spec/                    # DMG Core Specification
├── schema/                  # JSON Schema definitions
├── conformance/             # Test fixtures + runner
├── sdk/                     # Reference implementations
│   ├── js/                  # dmg-js
│   └── python/              # dmg-py
├── cli/                     # Validator CLI
├── examples/                # Sample DMG files
├── course/                  # Online learning content
│   ├── modules/            # M0-M10 + capstone
│   ├── assets/             # Downloadable materials
│   └── slides/             # Workshop decks
├── community/               # Governance
│   ├── dips/               # DMG Improvement Proposals
│   └── cohorts/            # Facilitator playbooks
└── docs/                    # Documentation site
```

---

## Governance Gates

For consequential decisions (RAMP ≥ 3) marked Final/Approved:

✅ Scheduled outcome check required  
✅ At least 1 dissent captured  
✅ Rollback owner named  
✅ ≥2 reversal signals defined  
✅ At least 1 prediction with confidence  

---

## 🆓 OSS vs 💎 Platform

**DMG is the open standard. ARANGAM provides premium infrastructure.**

| What You Get | DMG Standard (OSS) | ARANGAM Platform |
|--------------|--------------------|------------------|
| DMG Core Spec + Schemas | ✅ | ✅ |
| Validator CLI | ✅ | ✅ |
| Reference Libraries | ✅ | ✅ |
| Course + Workshop Materials | ✅ | ✅ |
| **Hosted MOMENT Ledger** | ❌ | ✅ Hash-chained audit trail |
| **Team Collaboration** | ❌ | ✅ Approvals + workflows |
| **DMG Certification** | ❌ | ✅ Official credential |
| **Enterprise Governance** | ❌ | ✅ SSO + retention policies |
| **Priority Support** | ❌ | ✅ |

> **The standard is free. The infrastructure is premium.**

See [ATTRIBUTION.md](ATTRIBUTION.md) for attribution guidelines.

---

## Learn DMG

| Resource | Description |
|----------|-------------|
| [7-Day Email Course](course/assets/email-course.md) | Daily lessons |
| [Online Course](course/modules/) | 10 modules + capstone |
| [Workshop Kit](course/slides/) | Run your own sessions |
| [Video Syllabus](course/assets/video-syllabus.md) | 30-day YouTube/TikTok plan |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### DMG Improvement Proposals (DIPs)

All spec changes go through the DIP process. See [community/dips/](community/dips/).

---

## License

MIT — see [LICENSE](LICENSE).

**Trademarks**: "DMG", "Decision Moment Graph", and related logos are trademarks of SYNTHAI TECH PTY LTD.

---

## The Movement

> DMG makes decisions computable and learnable.
> SPAR makes them dialectically robust.
> OUTCOME loops make them a compounding cognition engine.

**Isolated reasoning is the enemy.**
