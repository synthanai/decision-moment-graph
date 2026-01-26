# DMG — Decision Moment Graph

> **Store decision moments, not raw chats, objects or data.**
> *Decision graphs for the AI era — so LLMs synthesize auditable, reversible decisions, not just summarize documents.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conformance Tests](https://img.shields.io/badge/conformance-passing-green.svg)](#conformance)

---

## What is DMG?

**DMG** is the **Open Standard** for decision governance in the AI era.
It enforces the **MERIT** Standard:

- 📐 **Measured** — expected outcomes defined
- 🔍 **Evidenced** — traces & citations
- 🔙 **Reversible** — rollback plans (DOORS)
- 👁️ **Inspectable** — open audit logs
- 🔗 **Traceable** — provenance chain

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

## MERIT Conformance Matrix

How DMG objects map to the **MERIT** standard:

| Principle | Verified By | Conformance Level |
|-----------|-------------|-------------------|
| 📐 **M**easured | `OUTCOME` checks vs predictions | Platinum |
| 🔍 **E**videnced | `MEMO` options (≥3) & rationale | Bronze |
| 🔙 **R**eversible | `DOORS` owner & rollback plan | Gold |
| 👁️ **I**nspectable | `MOMENT` event hash chain | Silver |
| 🔗 **T**raceable | `TRACE` source citations | Platinum |

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
📍 Phase 1: DRAFT — Define scope
📍 Phase 2: ENRICH — Check memory for prior decisions
📍 Phase 3: DELIBERATE — Run SPAR process
📍 Phase 4: GATE — Governance check (RAMP/DOORS)
📍 Phase 5: COMMIT — Finalize & Execute
📍 Phase 6: VERIFY — Observe result
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

## The DMG Lifecycle

The decision lifecycle is rigorous and linear, mapping directly to DMG primitives:

> **Draft** → **Enrich** → **Deliberate** → **Gate** → **Commit** → **Verify**

| Phase | Action | Object Created/Updated |
|-------|--------|------------------------|
| **1. DRAFT** | Define context & options | `MEMO` (Draft) |
| **2. ENRICH** | Retrieve history & evidence | `MEMO` (Context) + `TRACE` |
| **3. DELIBERATE** | Argue options & record dissent | `MEMO` (Analysis) + `DISSENT` |
| **4. GATE** | Apply RAMP & DOORS checks | `RAMP` + `DOORS` |
| **5. COMMIT** | Finalize & Execute | `COMMIT` (Final) + `MOMENT` |
| **6. VERIFY** | Measure actual results | `OUTCOME` |

### SDK Modules

| Module | Purpose |
|--------|---------|
| `agentic_adapter.py` | Core DMG Lifecycle adapter |
| `spar_adapter.py` | Converts SPAR to DMG |
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

## The Open Protocol

**DMG is the open standard. ARANGAM provides premium infrastructure.**

| What You Get | DMG Standard (OSS) | ARANGAM Platform |
|--------------|--------------------|------------------|
| DMG Core Spec + Schemas | ✅ | ✅ |
| Validator CLI | ✅ | ✅ |
| Reference Libraries | ✅ | ✅ |
| **Hosted MOMENT Ledger** | ❌ | ✅ Hash-chained audit trail |
| **Team Collaboration** | ❌ | ✅ Approvals + workflows |
| **Enterprise Governance** | ❌ | ✅ SSO + retention policies |

> *The standard is free. The infrastructure is premium.*

See [ATTRIBUTION.md](ATTRIBUTION.md) for attribution guidelines.

---

## The SYNTHAI Ecosystem

| Component | Role |
| :--- | :--- |
| **[Decision Moment Graph](https://github.com/synthanai/decision-moment-graph)** | The **Standard** for reversible, auditable decisions. |
| **[VAULT-KIT](https://github.com/synthanai/vault-kit)** | The **Protocol** for privacy-first coordination. |
| **[agentic-kit](https://github.com/synthanai/agentic-kit)** | The **Infrastructure** for reliable agent systems. |

> *Built by [SYNTHAI](https://synthai.tech) — Decision Intelligence for the AI Era.*
