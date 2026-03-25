# DMS Taxonomy & Definitions

> **Canonical definitions for the Decision Moment Standard ecosystem.**

---

## 🏗️ The Architecture: Standards & Kits

The ecosystem uses a "Standard (Spec) vs Kit (Tool)" architecture.

| Layer | Acronym | Full Name | Role |
|-------|---------|-----------|------|
| **Standard** | **DMS** | **Decision Moment Standard** | The normative rules (MERIT). "What good looks like." |
| **Graph** | **DMG** | **Decision Moment Graph** | The reference implementation (JSON Schema). "How we store it." |
| **Protocol** | **DCP** | **Decision Context Protocol** | Upstream framing (scope, stakeholders, constraints). |
| **Protocol** | **DMP** | **Decision Moment Protocol** | The live gate ritual ("we are deciding now"). |
| **Protocol** | **DRP** | **Decision Record Protocol** | Downstream logging (rationale, links, commitments). |
| **Protocol** | **DGP** | **Decision Gate Protocol** | Governance gates (Risk-based approval flows). |
| **Practice** | **DICE** | **Decision Intelligence Context Engineering** | The discipline/craft (training, playbooks). |

---

## 🧱 Primitives vs. Protocols

The ecosystem distinguishes between the *Verb* (Protocol) and the *Noun* (Primitive).

> **Equation**: `Protocol(Context) + Energy = Primitive(State)`

### What is a Primitive?
A **Primitive** is an **Atomic, Schema-Defined Object** that reifies a specific **MERIT Principle**. It is the immutable build-block of the decision.

| MERIT Principle | Reified Primitive | Definition |
|-----------------|-------------------|------------|
| 📐 **M**easured | **OUTCOME** | The Reality Check (Predictions vs Actuals) |
| 🔍 **E**videnced | **MEMO** | The Projection (Choices & Rationale) |
| 🔙 **R**eversible | **DOORS** | The Safeguard (Rollback Locks & Keys) |
| 👁️ **I**nspectable | **MOMENT** | The Provenance (Hash-chained Event Log) |
| 🔗 **T**raceable | **TRACE** | The Linkage (Evidence Graph) |

### Subsidiary Primitives
- **DISSENT**: Structured disagreement object (can include ZK-Vault reference).
- **RAMP**: Governance level object.
- **COMMIT**: State transition object.

---

## 📖 Key Definitions

### DMS (The Standard)
The **Decision Moment Standard** is the normative specification defining what constitutes a valid, auditable decision. It enforces the **MERIT** criteria (Measured, Evidenced, Reversible, Inspectable, Traceable). It is implementation-agnostic (can be SQL, Graph, or Ledger).

### DMG (The Graph)
The **Decision Moment Graph** is the reference encoding of DMS. It uses a specific JSON Schema to represent decisions as hash-chained event streams (`MOMENT`) with versioned projections (`MEMO`).

### DRP (The Record) - *Formerly "Decision Capture"*
The **Decision Record Protocol** defines the artifact produced by the decision process. It is the file you write to disk (e.g., `decision-001.dmg.json`). It replaces the term "DCaP" or "Decision Capture" to avoid collision with DCP.

### Zero-Knowledge Dissent (ZK-Dissent)
A privacy pattern where the *fact* of dissent is cryptographically recorded in the DMG (satisfying MERIT), but the *content* of the dissent is stored in a secure vault (Vault-Kit) to limit liability or leakage.

---

## 🔄 Protocol Flow

1. **DCP (Context)**: You Frame the decision.
2. **SPAR (Method)**: You Deliberate (North/East/South/West).
3. **DMP (Moment)**: You commit at the Gate.
4. **DRP (Record)**: You write the artifact to the DMG.

---

## ⚠️ Common Confusions to Avoid

- **DMS vs DMG**: DMS is the rulebook (like HTML spec). DMG is the tool/format (like DOM).
- **DCP vs DRP**: DCP is about *framing* the question (Start). DRP is about *recording* the answer (Finish).
- **DICE**: This is the *human skill* of running these protocols, not a software tool.
