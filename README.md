# DMG — Decision Moment Graph

> **The Reference Implementation of the [Decision Moment Standard (DMS)](../decision-moment-standard).**
> *Store decision moments, not raw chats, objects or data.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conformance Tests](https://img.shields.io/badge/conformance-passing-green.svg)](#conformance)

---

## What is DMG?

**DMG** is the **standard graph encoding** for the **[DMS Standard](../decision-moment-standard)**.

It provides the schemas, SDKs, and validators to ensure your decisions are **MERIT-compliant**:

| Principle | Verified By | Grade |
|-----------|-------------|-------|
| 📐 **M**easured | `OUTCOME` checks vs predictions | Platinum |
| 🔍 **E**videnced | `MEMO` options (≥3) & rationale | Bronze |
| 🔙 **R**eversible | `DOORS` owner & rollback plan | Gold |
| 👁️ **I**nspectable | `MOMENT` event hash chain | Silver |
| 🔗 **T**raceable | `TRACE` source citations | Platinum |

> **"DMS defines the rules. DMG stores the proof."**

---

## The DMG Lifecycle

## The DMG Lifecycle

DMG implements the **7-Step Heptagon** lifecycle defined by DMS:

> **FRAME → SPAR → GATE → COMMIT → ENACT → YIELD → GAUGE**

---

## Quick Start

### 1. Install

```bash
pip install decision-moment-graph
# For embeddings: pip install sentence-transformers
```

### 2. Run DMG Lifecycle

```bash
python dmg/cli/lifecycle.py "Should we migrate to microservices?" --dry-run
```

Output:
```
📍 Phase 1: FRAME, Structure question & options
📍 Phase 2: SPAR, Deliberate & Challenge
📍 Phase 3: GATE, Check Governance & Reversibility
📍 Phase 4: COMMIT, Sign & Hash (The "Capture")
📍 Phase 5: ENACT, Execute instructions
📍 Phase 6: YIELD, Measure results
📍 Cycle Complete: GAUGE, Calibrate confidence & learn
```

### 3. Use as Library

```python
from decision_moment_graph import AgenticSPARAdapter
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

> **FRAME → SPAR → GATE → COMMIT → ENACT → YIELD → GAUGE**

| Step | Phase | Primitive | Kit/Module | Action |
|-------|-------|-----------|------------|--------|
| 1 | **FRAME** | `MEMO` | `dmg/frame` | Define context & options |
| 2 | **SPAR** | `DISSENT` | `spar-kit` | Deliberate & Challenge |
| 3 | **GATE** | `RAMP` | `dmg/gate` | Check Governance & Reversibility |
| 4 | **COMMIT** | `MOMENT` | `dmg/core` | Sign & Hash (The "Capture") |
| 5 | **ENACT** | — | — | Execute instructions |
| 6 | **YIELD** | `OUTCOME` | `dmg/yield` | Measure results |
| 7 | **GAUGE** | `RETRO` | `dmg/gauge` | Calibrate confidence & learn |

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
decision-moment-graph/
├── dmg/                     # Python Package
│   ├── schema/              # JSON Schema definitions
│   ├── sdk/                 # Reference implementations
│   └── cli/                 # Validator CLI
├── conformance/             # Test fixtures + runner
└── docs/                    # Implementation Docs
```

> **Note**: Normative specs have moved to `decision-moment-standard/spec`.

## Agentic Integration (MCP)

DMG provides a **Context Engine** MCP Server for AI Agents:
- **Tools**:
  - `validate_moment(path)`: Run MERIT validation on any file
  - `create_moment_scaffold(title)`: Generate compliant JSON
- **Resources**: `dmg://graph/active`, `dmg://moment/{id}`
- **Setup**: Run `pip install mcp` and point your client to `dmg/mcp/server.py`.

### New Modules (Jan 2026)

| Module | Path | Purpose |
|--------|------|---------|
| **GAUGE Emitter** | `src/gauge-emitter.js` | Ecosystem event emission at phase completion |
| **Decision Replay** | `src/replay.js` | Counterfactual analysis and training data |

```javascript
// Decision replay example
const { captureSnapshot, replayDecision, REPLAY_MODES } = require('dmg/src/replay');

const snapshotId = captureSnapshot(decision);
const replay = replayDecision(snapshotId, {
    mode: REPLAY_MODES.COUNTERFACTUAL,
    modifications: { context: { budget: newBudget } }
});
```


---

## Governance Gates

For consequential decisions (RAMP ≥ 3) marked Final/Approved:

✅ Scheduled outcome check required  
✅ At least 1 dissent captured (or ZK-Dissent ref)  
✅ Rollback owner named  
✅ ≥2 reversal signals defined  
✅ At least 1 prediction with confidence  

---

## The Open Protocol

**DMG is the open standard toolkit. ARANGAM provides premium infrastructure.**

| What You Get | DMG (OSS Kit) | ARANGAM Platform |
|--------------|--------------------|------------------|
| DMG Core Schemas | ✅ | ✅ |
| Validator CLI | ✅ | ✅ |
| Reference Libraries | ✅ | ✅ |
| **Hosted MOMENT Ledger** | ❌ | ✅ Hash-chained audit trail |
| **Team Collaboration** | ❌ | ✅ Approvals + workflows |
| **Enterprise Governance** | ❌ | ✅ SSO + retention policies |

> *The kit is free. The infrastructure is premium.*

See [ATTRIBUTION.md](ATTRIBUTION.md) for attribution guidelines.

---

## The SYNTHAI Ecosystem

| Component | Role |
| :--- | :--- |
| **[Decision Moment Graph](https://github.com/synthanai/decision-moment-graph)** | The **Standard** for reversible, auditable decisions. |
| **[VAULT-KIT](https://github.com/synthanai/vault-kit)** | The **Protocol** for privacy-first coordination. |
| **[agentic-kit](https://github.com/synthanai/agentic-kit)** | The **Infrastructure** for reliable agent systems. |

> *Built by [SYNTHAI](https://synthai.tech), Decision Intelligence for the AI Era.*
