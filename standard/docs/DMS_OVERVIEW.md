# DMS Overview: The Decision Moment Standard

## 🎯 The Purpose

The decision is the fundamental unit of organizational work. Yet, unlike code (commits), finance (txns), or design (props), **decisions have no standard format**. They are lost in emails, chat logs, and meeting minutes.

**DMS** provides a universal standard to **encode decision lineage**.

It ensures that AI systems, humans, and auditors can verify *how* a decision was made, not just *what* was decided.

---

## 🏛️ The MERIT Framework

DMS enforces the **MERIT** criteria. If a decision record does not satisfy these, it is not a "Decision", it is just a suggestion.

### 1. Measured (M)
*Requirement*: Must explicitly state what will happen if this decision works.
*Primitive*: `OUTCOME`
*Checks*: Baseline vs Target, Confidence %.

### 2. Evidenced (E)
*Requirement*: Must show alternatives were considered.
*Primitive*: `MEMO` (Options Array)
*Checks*: ≥3 Options, Trade-off matrix.

### 3. Reversible (R)
*Requirement*: Must define how to undo this decision.
*Primitive*: `DOORS` (Reversibility & Rollback)
*Checks*: Named Rollback Owner, Trigger conditions.

### 4. Inspectable (I)
*Requirement*: Must be tamper-evident.
*Primitive*: `MOMENT` (Hash Chain)
*Checks*: Cryptographic lineage of updates.

### 5. Traceable (T)
*Requirement*: Must link to facts, not just opinions.
*Primitive*: `TRACE` (Linkage)
*Checks*: Citation graph, Evidence strength.

---

## 🏗️ The 4 Protocols

DMS is composed of four protocols that cover the decision lifecycle.

### 1. DCP: Decision Context Protocol (The Frame)
* "What are we deciding?"
* "Who is the decider?"
* "What is the constraint?"

### 2. DMP: Decision Moment Protocol (The Gate)
* "Is this ready?"
* "Do we commit?"
* "Are we safe to try?"

### 3. DRP: Decision Record Protocol (The Artifact)
* The JSON/Schema output.
* The formal "Receipt" of the decision.

### 4. DGP: Decision Gate Protocol (The Flow)
* Logic for approval routing.
* "Does this need CEO approval or Team Lead?"

---

## 🧠 Why "Standard" vs "Kit"?

We separated **DMS (Standard)** from **DMG (Graph Kit)** to allow multiple implementations:
- **DMG**: The JSON-Graph implementation (Default).
- **SQL-DMS**: A relational implementation (Hypothetical).
- **On-Chain DMS**: A smart contract implementation (Hypothetical).

DMS is the "HTTP Spec". DMG is "Chrome".
