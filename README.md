# DMG — Decision Moment Graph

> **Stop storing chats. Store decision objects.**

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

### 1. Install the CLI

```bash
pip install dmg-cli
# or
npm install -g @dmg/cli
```

### 2. Create a MEMO

```bash
dmg init my-decision
dmg memo create --arena "build-vs-buy"
```

### 3. Validate

```bash
dmg validate my-decision.dmg.json
```

### 4. Export

```bash
dmg export my-decision.dmg.json --format pdf
```

---

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

## OSS vs Commercial

**Open (MIT)**:
- DMG Core Spec + schemas
- Validator CLI + conformance tests
- Reference libraries
- Local-first single-user app
- Course + facilitator materials

**Commercial (SYNTHAI platform)**:
- Hosted MOMENT ledger
- Team collaboration + approvals
- Enterprise governance (SSO, retention)
- RAMP enforcement engines

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
