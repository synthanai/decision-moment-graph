# M6: TRACE-KIT — Evidence

**Time**: 10 minutes  
**Goal**: Link claims to sources with strength ratings

---

## The Mindset Shift

| From | To |
|------|-----|
| "Users prefer X" | "Users prefer X (Source: Q4 survey, 67% response, strong)" |
| "Research shows..." | "Research shows [link], retrieved Jan 20, strength: medium" |
| "I heard that..." | "Claim lacks source — marked as weak" |

---

## What is TRACE?

**TRACE** is DMG's evidence provenance layer. It links claims to sources with:

- **What** the claim is
- **Where** the evidence comes from
- **When** it was retrieved
- **How strong** the evidence is

---

## Why TRACE Matters

Most decisions rely on claims like:
- "The market is moving toward X"
- "Users want Y"
- "Competitors are doing Z"

Without TRACE:
- Claims are asserted without verification
- Weak evidence looks as strong as rigorous data
- Post-mortems can't distinguish "bad luck" from "bad data"

With TRACE:
- Every claim has a provenance pointer
- Strength is explicit and auditable
- Learning can trace which sources were reliable

---

## TRACE Object Structure

```json
{
  "trace_id": "trace-001",
  "claim": "Structured onboarding improves retention by 82%",
  "source": {
    "type": "research",
    "uri": "https://example.com/onboarding-study-2025",
    "retrieved_at": "2026-01-20T10:00:00Z"
  },
  "strength": "strong",
  "quote_index": "Organizations with structured onboarding see 82% improvement in 90-day retention"
}
```

---

## Source Types

| Type | Examples |
|------|----------|
| `research` | Academic papers, industry reports |
| `survey` | Customer surveys, market research |
| `analytics` | Internal data, dashboards |
| `interview` | User interviews, expert conversations |
| `observation` | Personal experience, team observation |
| `assumption` | Educated guess, hypothesis |

---

## Strength Levels

| Strength | Meaning | When to Use |
|----------|---------|-------------|
| **strong** | Direct evidence, verified, replicable | Research, large surveys, internal analytics |
| **medium** | Indirect or partially verified | Small sample interviews, dated research |
| **weak** | Anecdotal, unverified, or assumed | Hearsay, single observation, hypothesis |

**Rule**: Weak evidence isn't forbidden, but it must be labeled.

---

## Exercise: Add TRACE to Claims (5 min)

For each claim, identify source and strength:

### Claim 1
> "Users prefer dark mode"

**Source**: ___  
**Strength**: ___  
**Why**: ___

### Claim 2
> "Our main competitor raised $50M last quarter"

**Source**: ___  
**Strength**: ___  
**Why**: ___

### Claim 3
> "The team is burned out"

**Source**: ___  
**Strength**: ___  
**Why**: ___

---

## Best Practices

### Do: Be honest about strength
Weak evidence that's labeled correctly is better than strong-sounding claims with no backing.

### Do: Include retrieval date
Evidence ages. "Market report from 2020" may not apply in 2026.

### Do: Quote the specific passage
`quote_index` lets others verify without reading the whole source.

### Don't: Skip TRACE for "obvious" claims
If it's shaping a decision, it needs a source.

---

## Key Takeaway

> Confidence ≠ evidence. TRACE forces the distinction.

When you add TRACE:
- Strong claims with weak evidence get scrutiny
- Weak claims with strong evidence get attention
- Decision quality improves

---

## Next Step

→ [M7: COMMIT-KIT, State Transitions](./M7_COMMIT_KIT.md)
