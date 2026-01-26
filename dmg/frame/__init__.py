"""
FRAME-KIT: Decision Framing Module

The first phase of the DMG Lifecycle: structure the question and options.

Usage:
    from dmg.frame import FrameBuilder, FrameValidator
    
    builder = FrameBuilder()
    frame = builder.from_question(
        question="Should we migrate to microservices?",
        context="5-year monolith, team of 8"
    )
    
    # Validates MEMO structure
    validator = FrameValidator()
    result = validator.validate(frame)
"""

from .builder import FrameBuilder
from .validator import FrameValidator, FrameValidationResult
from .templates import FRAME_TEMPLATES

__all__ = [
    "FrameBuilder",
    "FrameValidator", 
    "FrameValidationResult",
    "FRAME_TEMPLATES"
]
