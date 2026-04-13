# DMG Principles

## The 7 Foundational Principles

These principles are **axiomatic**. They are not negotiable and form the foundation of all DMG design decisions.

---

## Principle 1: Decisions Are First-Class Objects

### Statement
A decision is not the conclusion of a conversation. It is a **structured, versioned, inspectable artifact** with its own identity.

### Rationale
When decisions live in chat threads, they:
- Cannot be queried
- Cannot be versioned
- Cannot be linked
- Cannot be audited
- Cannot be learned from

### Implementation in DMG
- Every decision has a `memo_id` (unique identifier)
- Every decision has a `version` (monotonically increasing)
- Every decision has `created_at` and `updated_at` (temporal identity)
- The MEMO object is the portable projection of the decision

### Violation Examples
- ❌ "We decided in Slack to go with option A"
- ❌ "Check the meeting notes for our decision"
- ❌ "I think we agreed on something?"

---

## Principle 2: Dissent Is Data, Not Drama

### Statement
Disagreement captured structurally becomes **learning fuel**. Disagreement suppressed becomes **failure seeds**.

### Rationale
Most organizations treat dissent as:
- Political inconvenience
- Consensus failure
- Something to "get past"

But dissent carries signal:
- **What could go wrong** (if the dissenter is right)
- **What to monitor** (the dissenter's concerns)
- **When to reverse** (conditions the dissenter named)

### Implementation in DMG
- Every DISSENT has an `author` (named accountability)
- Every DISSENT has `conditions_to_change_mind` (testable criteria)
- Every DISSENT has a `resolution` (accepted/mitigated/deferred/rejected)
- RAMP ≥3 requires at least 1 DISSENT for finalization

### Violation Examples
- ❌ "Everyone agreed" (no dissent recorded)
- ❌ "John had concerns but we moved on" (unstructured)
- ❌ "We'll figure it out later" (no conditions)

---

## Principle 3: Governance Scales With Reversibility

### Statement
The rigor required for a decision should be **proportional to how hard it is to undo**.

### Rationale
Under-governance: Critical decisions get shipped without review, causing expensive failures.
Over-governance: Trivial decisions get bureaucratic overhead, killing velocity.

RAMP solves this by indexing rigor to **time-to-reverse**.

### Implementation in DMG
- **L1** (Minutes): Config change, feature flag → Minimal review
- **L2** (Hours-Days): Pricing tweak, copy change → Light review
- **L3** (Weeks): Roadmap priority, hiring → DISSENT + DOORS required
- **L4** (Months): Architecture, partnership → Full approval chain
- **L5** (Years/Never): M&A, compliance commitments → Maximum rigor

### Violation Examples
- ❌ "It's just a database schema change" → Migration takes a month
- ❌ "We need legal review for this typo fix" → Over-governance
- ❌ "L1 for everything" → Under-governance

---

## Principle 4: Reversibility Must Be Concrete

### Statement
A decision without a rollback plan is not a decision, it's a **gamble**.

### Rationale
Hope is not a strategy. "We can always reverse it" is meaningless unless:
- Someone owns the reversal (named person)
- There's a plan (documented steps)
- There are signals (what triggers reversal)
- There are thresholds (when to act)

### Implementation in DMG
- **D**eclare: What exactly are we committing to?
- **O**bserve: What metrics will we monitor?
- **O**wn: Who owns rollback? (A name, not "the team")
- **R**eady: What's the rollback procedure?
- **S**ignal: What thresholds trigger reversal?

### Violation Examples
- ❌ "We'll figure out rollback if needed"
- ❌ "The team will handle it"
- ❌ "We'll know when to stop"

---

## Principle 5: Predictions Are Testable

### Statement
If you cannot state **what you expect to happen** with **what confidence**, you are not deciding, you are **hoping**.

### Rationale
Predictions make judgment measurable. Without them:
- There's no way to know if the decision was "right"
- There's no calibration feedback
- There's no learning loop

### Implementation in DMG
- `expected_outcomes[]` captures predictions
- Each outcome has `metric`, `expected`, `confidence`, `horizon`
- OUTCOME checks compare predicted vs actual
- Calibration improves over time

### Violation Examples
- ❌ "This will be successful" (not quantified)
- ❌ "Users will love it" (not measurable)
- ❌ "70% confident" (without saying what you're confident about)

---

## Principle 6: Every Decision Deserves An Outcome Check

### Statement
A decision without a scheduled review is **fire and forget**. Learning happens when you compare prediction to reality.

### Rationale
Most organizations:
- Make decisions
- Move on
- Repeat mistakes

OUTCOME checks create a feedback loop:
- What did we predict?
- What actually happened?
- Who saw it coming? (Dissent audit)
- What assumptions failed? (Assumptions audit)
- What should we do differently?

### Implementation in DMG
- `outcome.next_check_date` is required for Final/Approved decisions
- `outcome.checks[]` logs each review
- Each check has `verdict` (keep/adjust/reverse)
- Each check audits assumptions and dissents

### Violation Examples
- ❌ "We shipped it, we're done"
- ❌ "That didn't work, who knew?"
- ❌ "No one predicted this" (when someone did, but wasn't captured)

---

## Principle 7: Provenance Is Non-Negotiable

### Statement
Every change to a decision must be **logged, timestamped, and attributable**. MOMENT makes decisions inspectable, technically and legally.

### Rationale
Without provenance:
- "Who changed this?" → Unknown
- "What did we originally decide?" → Lost
- "When was this approved?" → Unverifiable
- "Is this tamper-proof?" → No

With MOMENT:
- Every change is an event
- Events are numbered sequentially
- Hash-chain makes tampering detectable
- Full audit trail for compliance

### Implementation in DMG
- `moment.events[]` is append-only
- Each event has `seq`, `ts`, `actor`, `type`, `payload`
- Events are hash-chained (`prev_hash` + `hash`)
- Events cannot be edited, only new events added

### Violation Examples
- ❌ Editing an event in place
- ❌ Deleting event history
- ❌ Having no event log at all

---

## Summary Table

| # | Principle | Primitive | Required For |
|---|-----------|-----------|--------------|
| 1 | Decisions are first-class objects | MEMO | All |
| 2 | Dissent is data | DISSENT | RAMP ≥3 |
| 3 | Governance scales with reversibility | RAMP | All |
| 4 | Reversibility must be concrete | DOORS | RAMP ≥3 |
| 5 | Predictions are testable | Expected Outcomes | RAMP ≥3 |
| 6 | Every decision deserves review | OUTCOME | All Final |
| 7 | Provenance is non-negotiable | MOMENT | All |

---

*These principles are encoded in the DMG validator and enforced programmatically.*
