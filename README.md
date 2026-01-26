# DMG — Decision Moment Graph

> **Store decision moments, not raw chats, objects or data.**
> *Decision graphs for the AI era — so LLMs synthesize auditable, reversible decisions, not just summarize documents.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conformance Tests](https://img.shields.io/badge/conformance-passing-green.svg)](#conformance)

---

## What is DMG?

**DMG** is the **Open Standard** for decision governance in the AI era.

It enforces the **MERIT** Standard. Every valid decision must be:

| Principle | Verified By | Grade |
|-----------|-------------|-------|
| 📐 **M**easured | `OUTCOME` checks vs predictions | Platinum |
| 🔍 **E**videnced | `MEMO` options (≥3) & rationale | Bronze |
| 🔙 **R**eversible | `DOORS` owner & rollback plan | Gold |
| 👁️ **I**nspectable | `MOMENT` event hash chain | Silver |
| 🔗 **T**raceable | `TRACE` source citations | Platinum |

> **"If it doesn't have MERIT, it's just a chat log."**

---

## The DMG Lifecycle

DMG implements MERIT through a rigorous 6-phase lifecycle:

> **FRAME → TRACE → SPAR → RAMP → COMMIT → OUTCOME**

---

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
# For embeddings: pip install sentence-transformers
```

### 2. Run DMG Lifecycle

```bash
python dmg/cli/lifecycle.py "Should we migrate to microservices?" --dry-run
```

Output:
```
📍 Phase 1: FRAME — Structure question & options
📍 Phase 2: TRACE — Retrieve prior decisions & evidence
📍 Phase 3: SPAR — Run structured deliberation
📍 Phase 4: RAMP — Governance gate (RAMP/DOORS)
📍 Phase 5: COMMIT — Finalize & execute
📍 Phase 6: OUTCOME — Verify predictions vs reality
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

The decision lifecycle maps directly to DMG kits and objects:

> **FRAME → TRACE → SPAR → RAMP → COMMIT → OUTCOME**

| Phase | Kit/Object | Action | Produces |
|-------|------------|--------|----------|
| **1. FRAME** | FRAME-KIT | Frame the question & options | `MEMO` (Draft) |
| **2. TRACE** | TRACE-KIT | Trace prior decisions & evidence | `MEMO` (Context) + `TRACE` |
| **3. SPAR** | SPAR-KIT | Run structured deliberation | `DISSENT` + Synthesis |
| **4. RAMP** | RAMP-KIT | Assess governance & reversibility | `RAMP` + `DOORS` |
| **5. COMMIT** | COMMIT | Finalize state transition | `COMMIT` (Final) + `MOMENT` |
| **6. OUTCOME** | OUTCOME | Verify predictions vs reality | `OUTCOME` checks |

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

## Agentic Integration (MCP)

DMG provides a **Context Engine** MCP Server for AI Agents:
- **Tools**:
  - `validate_moment(path)`: Run MERIT validation on any file
  - `create_moment_scaffold(title)`: Generate compliant JSON
- **Resources**: `dmg://graph/active`, `dmg://moment/{id}`
- **Setup**: Run `pip install mcp` and point your client to `dmg/mcp/server.py`.


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
