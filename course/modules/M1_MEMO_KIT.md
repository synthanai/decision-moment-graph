# M1: MEMO-KIT — The Decision Brief

**Time**: 15 minutes  
**Goal**: Create a shareable decision brief with ≥3 options

---

## The Mindset Shift

| From | To |
|------|-----|
| "We decided to do X" | "Here's the MEMO with options, risks, and rationale" |
| "It's obvious" | "Options include doing nothing and the contrarian path" |
| "The team agreed" | "Named owners, explicit review date" |

---

## What is a MEMO?

A **MEMO** is DMG's core artifact: a versioned decision brief that captures:

- What you decided
- What options you considered (≥3)
- Why you chose this path
- Who owns it
- When to revisit

> Think of it as a "court ruling" for your decision—portable, quotable, defensible.

---

## Required Fields

| Field | Why |
|-------|-----|
| `title` | What decision is this? |
| `decision` | Clear statement of what you're committing to |
| `options` (≥3) | Proof you considered alternatives |
| `recommendation` | Your chosen path + rationale |
| `ramp` | How reversible is this? (covered in M3) |

---

## The 2-Option Trap

> "If you have only 2 options, you have 0."

Binary framing ("do it or don't") hides better paths. Always add:
- **Do nothing**: What if we wait?
- **Contrarian**: What's the opposite of our instinct?
- **Hybrid**: Can we combine elements?

---

## Exercise: Build a MEMO (10 min)

Use a real decision you're facing. Fill in:

```markdown
## MEMO: [Title]

**Decision**: [Clear statement of what you're committing to]

### Options Considered

1. **Option A: [Name]**
   - Description: [What is this?]
   - Pros: [Why consider it?]
   - Cons: [What's the downside?]

2. **Option B: [Name]**
   - Description:
   - Pros:
   - Cons:

3. **Option C: [Name]**
   - Description:
   - Pros:
   - Cons:

4. **Option D: Do Nothing**
   - Description: Maintain status quo
   - Pros:
   - Cons:

### Recommendation

[Which option and why? What made it better than the others?]

### Owners

- Decision Owner: [Name]
- Reviewer: [Name]

### Review Date

[When should we revisit this decision?]
```

---

## Check Your Work

Score your MEMO:

| Criterion | Points |
|-----------|--------|
| ≥3 options (including "do nothing" or contrarian) | 3 |
| Decision statement is clear and testable | 2 |
| Pros/cons for each option | 2 |
| Recommendation explains the choice | 2 |
| Named owner (not "the team") | 2 |
| Review date or trigger | 1 |
| **Total** | **/12** |

**Target**: 9+ to pass

---

## Weak vs Strong Examples

### ❌ Weak MEMO

```
Title: Feature Launch

We decided to launch the feature. Everyone agreed it was ready.
```

**Problems**: No options, no rationale, no owner, no review.

### ✅ Strong MEMO

```
Title: Q2 Feature Launch Timing

Decision: Launch privacy dashboard to 10% of users by March 15

Options:
1. Launch to 100% immediately — Fast, but risky
2. Launch to 10% (chosen) — Validates before scale
3. Delay to Q3 — Safer, but loses momentum
4. Do nothing — Leaves gap in compliance story

Recommendation: Option 2. We get real-world validation while
limiting blast radius. If metrics hold, expand Week 4.

Owner: Sarah Chen (Product)
Reviewer: Marcus Lee (Eng)
Review Date: March 22 (after 1 week of data)
```

**Strengths**: Clear options, rationale for choice, named owner, scheduled review.

---

## Key Takeaway

> A MEMO isn't paperwork. It's a decision made inspectable.

When you have a MEMO, you can answer:
- What did we decide?
- What alternatives did we consider?
- Why did we choose this?
- Who's accountable?
- When do we check if it worked?

---

## Next Step

→ [M2: MOMENT-KIT — Provenance](./M2_MOMENT_KIT.md)
