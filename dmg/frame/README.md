# FRAME-KIT

> Phase 1 of the DMG Lifecycle: **Structure the question and options**

## What is FRAME?

**FRAME** is the first phase of the DMG Lifecycle. It ensures every decision starts with:

- ≥3 distinct options (including status quo)
- Clear question formulation
- Structured context
- RAMP level suggestion

## Quick Start

```python
from dmg.frame import FrameBuilder, FrameValidator

# Build a frame
frame = (
    FrameBuilder()
    .from_question("Should we migrate to microservices?", context="5-year monolith, team of 8")
    .add_option("Incremental migration", description="Extract services one at a time")
    .add_option("Big bang rewrite", description="Replace entire system")
    .set_owner("sarah.chen")
    .build()
)

# Validate
result = FrameValidator().validate(frame)
print(f"Valid: {result.valid}, Score: {result.score}/100")

# Convert to MEMO for next phases
memo = frame.to_memo()
```

## Templates

Use pre-built templates for common decision patterns:

```python
from dmg.frame.templates import apply_template, list_templates

# See available templates
print(list_templates())
# ['build_vs_buy', 'technology_migration', 'resource_allocation', ...]

# Apply a template
frame_data = apply_template("build_vs_buy", feature="customer analytics")
```

### Available Templates

| Template | Use Case |
|----------|----------|
| `build_vs_buy` | Build in-house vs purchase decision |
| `technology_migration` | Moving between technology stacks |
| `resource_allocation` | Distributing limited resources |
| `process_change` | Changing organizational processes |
| `vendor_selection` | Choosing between vendors |
| `go_no_go` | Binary decision with mitigations |

## Validation

The `FrameValidator` checks:

| Code | Check | Level |
|------|-------|-------|
| F001 | Question is non-empty (≥5 chars) | All |
| F002 | At least 3 options present | All |
| F003 | Options have distinct titles | All |
| F004 | Context is provided | Standard+ |
| F005 | Status quo option exists | Strict |
| F006 | Options have rationale | Strict |

```python
from dmg.frame import FrameValidator, FrameValidationLevel

# Strict validation
validator = FrameValidator(level=FrameValidationLevel.STRICT)
result = validator.validate(frame)

if not result.valid:
    for error in result.errors:
        print(f"[{error.code}] {error.message}")
```

## Integration with DMG Lifecycle

```
FRAME → TRACE → SPAR → RAMP → COMMIT → OUTCOME
  ↑
  │ You are here
  │
  └── Produces MEMO (Draft) for subsequent phases
```

The FRAME phase produces a **MEMO** object that flows into:
- **TRACE**: Evidence retrieval for each option
- **SPAR**: Structured deliberation to compare options

## Why ≥3 Options?

DMG requires at least 3 options to prevent false binary framing:

| ❌ Bad Framing | ✅ Good Framing |
|----------------|-----------------|
| "Should we do X?" | "What's the best approach to achieve Y?" |
| Yes / No | Option A / Option B / Option C / Status Quo |

Binary framing leads to:
- Anchoring bias
- Missed alternatives
- Premature commitment

## API Reference

### FrameBuilder

```python
FrameBuilder()
    .from_question(question: str, context: str = "") -> FrameBuilder
    .add_option(title: str, description: str = "", pros: List[str] = None, cons: List[str] = None) -> FrameBuilder
    .set_context(constraints: List[str] = None, ...) -> FrameBuilder
    .set_recommendation(recommendation: str) -> FrameBuilder
    .set_owner(owner: str) -> FrameBuilder
    .build() -> Frame
    .suggest_ramp_level() -> int
```

### FrameValidator

```python
FrameValidator(level: FrameValidationLevel = FrameValidationLevel.STANDARD)
    .validate(frame: Frame | dict) -> FrameValidationResult
```

### Frame

```python
Frame
    .question: str
    .options: List[FrameOption]
    .context: FrameContext
    .recommendation: Optional[str]
    .owner: Optional[str]
    .to_memo() -> dict
```

---

*FRAME-KIT is part of the [DMG Open Standard](../README.md).*
