"""
FRAME Validator

Validates that a frame/MEMO draft meets minimum requirements
before proceeding to TRACE and SPAR phases.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class FrameValidationLevel(Enum):
    """Validation strictness levels."""
    MINIMAL = "minimal"      # Just ≥3 options
    STANDARD = "standard"    # Options + context
    STRICT = "strict"        # Full MERIT requirements


@dataclass
class FrameValidationError:
    """A single validation error."""
    code: str
    message: str
    field: Optional[str] = None
    severity: str = "error"  # error, warning, info


@dataclass
class FrameValidationResult:
    """Result of frame validation."""
    valid: bool
    errors: List[FrameValidationError] = field(default_factory=list)
    warnings: List[FrameValidationError] = field(default_factory=list)
    score: int = 0  # 0-100 quality score
    
    def add_error(self, code: str, message: str, field: str = None):
        self.errors.append(FrameValidationError(
            code=code, message=message, field=field, severity="error"
        ))
        self.valid = False
    
    def add_warning(self, code: str, message: str, field: str = None):
        self.warnings.append(FrameValidationError(
            code=code, message=message, field=field, severity="warning"
        ))


class FrameValidator:
    """
    Validates decision frames against DMG requirements.
    
    Checks:
    - F001: Question is non-empty
    - F002: At least 3 options present
    - F003: Options have distinct titles
    - F004: Context is provided
    - F005: Status quo option exists
    - F006: Options have rationale (pros/cons or description)
    """
    
    MIN_OPTIONS = 3
    
    def __init__(self, level: FrameValidationLevel = FrameValidationLevel.STANDARD):
        self.level = level
    
    def validate(self, frame: Any) -> FrameValidationResult:
        """
        Validate a frame or MEMO draft.
        
        Args:
            frame: Frame object or MEMO dict
            
        Returns:
            FrameValidationResult with errors, warnings, and quality score
        """
        result = FrameValidationResult(valid=True)
        
        # Convert to dict if needed
        if hasattr(frame, "to_memo"):
            memo = frame.to_memo()
        elif hasattr(frame, "question"):
            # Frame object
            memo = {
                "title": frame.question,
                "options": [{"id": o.id, "title": o.title} for o in frame.options],
                "context": frame.context.__dict__ if hasattr(frame.context, "__dict__") else {}
            }
        else:
            memo = frame
        
        # F001: Question/title present
        title = memo.get("title", "")
        if not title or len(title.strip()) < 5:
            result.add_error(
                "F001",
                "Frame requires a clear question (≥5 characters)",
                "title"
            )
        
        # F002: At least 3 options
        options = memo.get("options", [])
        if len(options) < self.MIN_OPTIONS:
            result.add_error(
                "F002", 
                f"Frame requires at least {self.MIN_OPTIONS} options. Found: {len(options)}",
                "options"
            )
        
        # F003: Options have distinct titles
        option_titles = [o.get("title", "") for o in options]
        if len(option_titles) != len(set(option_titles)):
            result.add_error(
                "F003",
                "Option titles must be distinct",
                "options"
            )
        
        # F004: Context provided (for STANDARD and above)
        if self.level in [FrameValidationLevel.STANDARD, FrameValidationLevel.STRICT]:
            context = memo.get("context", {})
            if not context or (
                not context.get("constraints") and 
                not context.get("assumptions") and
                not context.get("timeline")
            ):
                result.add_warning(
                    "F004",
                    "Frame should include context (constraints, assumptions, or timeline)",
                    "context"
                )
        
        # F005: Status quo option (for STRICT)
        if self.level == FrameValidationLevel.STRICT:
            has_status_quo = any(
                "status quo" in o.get("title", "").lower() or
                "do nothing" in o.get("title", "").lower() or
                o.get("id", "") == "status-quo"
                for o in options
            )
            if not has_status_quo:
                result.add_warning(
                    "F005",
                    "Frame should include a 'status quo' or 'do nothing' option",
                    "options"
                )
        
        # F006: Options have rationale (for STRICT)
        if self.level == FrameValidationLevel.STRICT:
            for i, opt in enumerate(options):
                has_rationale = (
                    opt.get("description") or 
                    opt.get("pros") or 
                    opt.get("cons") or
                    opt.get("rationale")
                )
                if not has_rationale:
                    result.add_warning(
                        "F006",
                        f"Option '{opt.get('title', i)}' should have description or pros/cons",
                        f"options[{i}]"
                    )
        
        # Calculate quality score
        result.score = self._calculate_score(memo, result)
        
        return result
    
    def _calculate_score(self, memo: Dict, result: FrameValidationResult) -> int:
        """Calculate frame quality score (0-100)."""
        score = 100
        
        # Deduct for errors
        score -= len(result.errors) * 25
        
        # Deduct for warnings
        score -= len(result.warnings) * 10
        
        # Bonus for good practices
        options = memo.get("options", [])
        
        # Bonus: More than minimum options
        if len(options) > self.MIN_OPTIONS:
            score = min(100, score + 5)
        
        # Bonus: All options have descriptions
        if all(o.get("description") for o in options):
            score = min(100, score + 10)
        
        # Bonus: Has owner
        if memo.get("owner"):
            score = min(100, score + 5)
        
        return max(0, score)


def validate_frame(
    frame: Any,
    level: str = "standard"
) -> FrameValidationResult:
    """
    Quick helper to validate a frame.
    
    Args:
        frame: Frame object or MEMO dict
        level: "minimal", "standard", or "strict"
        
    Returns:
        FrameValidationResult
    """
    level_enum = FrameValidationLevel(level)
    validator = FrameValidator(level=level_enum)
    return validator.validate(frame)
