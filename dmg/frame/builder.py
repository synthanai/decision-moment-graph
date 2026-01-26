"""
FRAME Builder

Structures a decision question into a well-formed MEMO draft.
Ensures ≥3 options, clear context, and proper RAMP suggestion.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib


@dataclass
class FrameOption:
    """A single option in a decision frame."""
    id: str
    title: str
    description: str = ""
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    

@dataclass
class FrameContext:
    """Context for a decision frame."""
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    stakeholders: List[str] = field(default_factory=list)
    timeline: Optional[str] = None
    budget: Optional[str] = None


@dataclass
class Frame:
    """A structured decision frame (MEMO draft)."""
    question: str
    options: List[FrameOption]
    context: FrameContext
    recommendation: Optional[str] = None
    owner: Optional[str] = None
    
    # Metadata
    frame_id: str = ""
    created_at: str = ""
    
    def __post_init__(self):
        if not self.frame_id:
            self.frame_id = f"frame-{int(datetime.now().timestamp())}"
        if not self.created_at:
            self.created_at = datetime.now().isoformat() + "Z"
    
    def to_memo(self) -> Dict[str, Any]:
        """Convert frame to MEMO format."""
        return {
            "memo_id": self.frame_id.replace("frame-", "memo-"),
            "title": self.question,
            "decision": self.recommendation or "",
            "context": {
                "constraints": self.context.constraints,
                "assumptions": self.context.assumptions,
                "stakeholders": self.context.stakeholders,
                "timeline": self.context.timeline,
                "budget": self.context.budget
            },
            "options": [
                {
                    "id": opt.id,
                    "title": opt.title,
                    "description": opt.description,
                    "pros": opt.pros,
                    "cons": opt.cons
                }
                for opt in self.options
            ],
            "recommendation": self.recommendation,
            "owner": self.owner,
            "version": 1,
            "created_at": self.created_at,
            "updated_at": self.created_at
        }


class FrameBuilder:
    """
    Builder for creating well-structured decision frames.
    
    Ensures:
    - ≥3 options (including status quo)
    - Clear question formulation
    - Context extraction
    - RAMP level suggestion
    """
    
    MIN_OPTIONS = 3
    
    def __init__(self):
        self._question = ""
        self._options: List[FrameOption] = []
        self._context = FrameContext()
        self._recommendation = None
        self._owner = None
    
    def from_question(
        self, 
        question: str, 
        context: str = ""
    ) -> "FrameBuilder":
        """Start a frame from a question string."""
        self._question = question
        
        # Parse context string into structured context
        if context:
            # Split on common delimiters
            parts = [p.strip() for p in context.replace(";", ",").split(",")]
            self._context.constraints = parts
        
        # Add default "do nothing" option
        self._options = [
            FrameOption(
                id="status-quo",
                title="Do nothing / Status quo",
                description="Maintain current approach"
            )
        ]
        
        return self
    
    def add_option(
        self,
        title: str,
        description: str = "",
        pros: List[str] = None,
        cons: List[str] = None
    ) -> "FrameBuilder":
        """Add an option to the frame."""
        option_id = f"opt-{len(self._options) + 1}"
        self._options.append(FrameOption(
            id=option_id,
            title=title,
            description=description,
            pros=pros or [],
            cons=cons or []
        ))
        return self
    
    def set_context(
        self,
        constraints: List[str] = None,
        assumptions: List[str] = None,
        stakeholders: List[str] = None,
        timeline: str = None,
        budget: str = None
    ) -> "FrameBuilder":
        """Set structured context."""
        if constraints:
            self._context.constraints = constraints
        if assumptions:
            self._context.assumptions = assumptions
        if stakeholders:
            self._context.stakeholders = stakeholders
        if timeline:
            self._context.timeline = timeline
        if budget:
            self._context.budget = budget
        return self
    
    def set_recommendation(self, recommendation: str) -> "FrameBuilder":
        """Set initial recommendation (optional)."""
        self._recommendation = recommendation
        return self
    
    def set_owner(self, owner: str) -> "FrameBuilder":
        """Set decision owner."""
        self._owner = owner
        return self
    
    def build(self) -> Frame:
        """Build the frame, validating constraints."""
        if len(self._options) < self.MIN_OPTIONS:
            raise ValueError(
                f"Frame requires at least {self.MIN_OPTIONS} options. "
                f"Current: {len(self._options)}. "
                f"Hint: Add more alternatives with add_option()."
            )
        
        if not self._question:
            raise ValueError("Frame requires a question. Use from_question().")
        
        return Frame(
            question=self._question,
            options=self._options,
            context=self._context,
            recommendation=self._recommendation,
            owner=self._owner
        )
    
    def suggest_ramp_level(self) -> int:
        """Suggest a RAMP level based on frame characteristics."""
        level = 3  # Default
        
        # Adjust based on timeline
        if self._context.timeline:
            timeline = self._context.timeline.lower()
            if "urgent" in timeline or "immediate" in timeline:
                level = max(1, level - 1)
            elif "year" in timeline or "long" in timeline:
                level = min(5, level + 1)
        
        # Adjust based on budget
        if self._context.budget:
            # Simple heuristic: higher budget = higher RAMP
            budget = self._context.budget.lower()
            if "million" in budget or "m" in budget:
                level = min(5, level + 1)
        
        # Adjust based on stakeholder count
        if len(self._context.stakeholders) > 5:
            level = min(5, level + 1)
        
        return level


def frame_question(
    question: str,
    context: str = "",
    options: List[str] = None
) -> Frame:
    """
    Quick helper to frame a question.
    
    Args:
        question: The decision question
        context: Context string
        options: List of option titles (auto-generates if <3)
        
    Returns:
        A Frame ready for SPAR deliberation
    """
    builder = FrameBuilder().from_question(question, context)
    
    if options:
        for opt in options:
            builder.add_option(title=opt)
    
    # Ensure minimum options
    while len(builder._options) < FrameBuilder.MIN_OPTIONS:
        builder.add_option(
            title=f"Alternative {len(builder._options)}",
            description="(To be defined)"
        )
    
    return builder.build()
