# DMG OSS/IP Boundary Policy

**Version**: 1.0  
**License**: MIT (for OSS components)  
**Date**: January 2026

---

## 1. Purpose

DMG (Decision Moment Graph) is an **open standard** for decision governance.

This policy defines what is **Open Source (MIT)** vs **Proprietary IP**.

---

## 2. Guiding Principles

1. **DMG must be implementable without permission.** The standard and reference tooling are MIT.
2. **Interoperability over lock-in.** DMG data must be portable.
3. **Trust & governance at scale are product value.** Enterprise-grade controls are commercial.

---

## 3. What is OSS (MIT)

### A) The DMG Standard
- DMG Core Specification (`/spec/`)
- JSON Schemas (`/schema/`)
- Examples + Fixtures (`/examples/`)
- Conformance Tests (`/conformance/`)
- Public glossary + terminology

### B) Reference Implementations
- Parsers/serializers (dmg-js, dmg-py)
- Validator CLI
- Converters (DMG ⇄ Markdown/PDF)
- Local-first single-user app

### C) Education & Community
- Online course (`/course/`)
- Workshop materials
- Facilitator kits
- DIP process

### D) SPAR Integration
- SPAR-to-DMG adapter spec
- Arena templates
- Minimal SPAR runner (local, single-user)

---

## 4. What is Proprietary IP

### A) Hosted / Managed Services
- Hosted MOMENT Ledger
- Notary / Anchoring services
- Sync, sharing, workspace infrastructure
- Reliability tooling (rate limiting, billing)

### B) Enterprise Governance & Controls
- Permissions, RBAC, approvals at scale
- RAMP enforcement engines
- Enterprise integrations (SSO/SCIM, DLP, SIEM)
- Compliance features (retention, legal hold, redaction)

### C) Premium Product UX
- Team workflow orchestration
- Advanced DISSENT governance
- Organization-wide analytics dashboards

### D) Proprietary Datasets
- Curated precedent libraries ("case law")
- Private templates, scoring models
- Evaluation benchmarks

### E) SPAR (Commercial Components)
- Best-in-class SPAR orchestration (multi-model, STASH modes)
- Enterprise SPAR governance (approval gates, policy enforcement)
- Hosted provenance integrity
- Curated personas and domain packs

---

## 5. Trademarks

Even when code/spec is MIT:

- **Trademarks are not granted**
- Names and logos ("DMG", "Decision Moment Graph", "DMG Certified") are protected
- You may implement DMG freely but may not claim "official" or "certified" without permission

---

## 6. The Boundary Rule of Thumb

> **If it helps everyone implement DMG → OSS (MIT)**
>
> **If it helps operate DMG at scale with trust, governance, and compliance → Proprietary IP**

---

## 7. What You Can Expect

- DMG Core will remain open (MIT)
- Reference tooling will remain open (MIT)
- Commercial layers may evolve without being open sourced
- All implementations must maintain DMG compatibility

---

*Published by SYNTHAI TECH PTY LTD*
