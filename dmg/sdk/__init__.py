"""
DMG SDK - Python SDK for Decision Memory Graph

RESOLVE Loop Components:
- AgenticSPARAdapter: Core agentic adapter with feedback loops
- SPARAdapter: SPAR → DMG converter
- ActionDispatcher: Action execution backends
- SemanticMemoryStore: Embedding-based memory
- ReflectionLoop: Post-VERIFY self-critique
- AuditExporter: Compliance report generation
- CircuitBreaker: Safety mechanisms
"""

__version__ = "0.1.0"

# Conditional imports - works both as package and standalone
try:
    # Try relative imports first (when installed as package)
    from .agentic_adapter import (
        AgenticSPARAdapter,
        GateResult,
        GateDecision,
        Observation,
        LoopResult,
    )
    from .spar_adapter import SPARAdapter
    from .action_dispatcher import (
        ActionDispatcher,
        Action,
        ActionType,
        LoggingDispatcher,
        HttpDispatcher,
        DryRunDispatcher,
        CompositeDispatcher,
        create_dispatcher,
    )
    from .semantic_memory import (
        SemanticMemoryStore,
        SimpleMemoryStore,
    )
    from .reflection import (
        ReflectionLoop,
        ReflectionResult,
        ReflectionVerdict,
        ConfidenceCalibration,
    )
    from .audit_export import AuditExporter
    from .circuit_breaker import (
        CircuitBreaker,
        CircuitBreakerOpen,
        KillSwitch,
        KillSwitchActivated,
        RateLimiter,
        RateLimitExceeded,
        safe_resolve,
    )
except ImportError:
    # Fall back to absolute imports (when running standalone)
    from agentic_adapter import (
        AgenticSPARAdapter,
        GateResult,
        GateDecision,
        Observation,
        LoopResult,
    )
    from spar_adapter import SPARAdapter
    from action_dispatcher import (
        ActionDispatcher,
        Action,
        ActionType,
        LoggingDispatcher,
        HttpDispatcher,
        DryRunDispatcher,
        CompositeDispatcher,
        create_dispatcher,
    )
    from semantic_memory import (
        SemanticMemoryStore,
        SimpleMemoryStore,
    )
    from reflection import (
        ReflectionLoop,
        ReflectionResult,
        ReflectionVerdict,
        ConfidenceCalibration,
    )
    from audit_export import AuditExporter
    from circuit_breaker import (
        CircuitBreaker,
        CircuitBreakerOpen,
        KillSwitch,
        KillSwitchActivated,
        RateLimiter,
        RateLimitExceeded,
        safe_resolve,
    )

__all__ = [
    # Core adapter
    "AgenticSPARAdapter",
    "SPARAdapter",
    "GateResult",
    "GateDecision",
    "Observation",
    "LoopResult",
    # Dispatchers
    "ActionDispatcher",
    "Action",
    "ActionType",
    "LoggingDispatcher",
    "HttpDispatcher",
    "DryRunDispatcher",
    "CompositeDispatcher",
    "create_dispatcher",
    # Memory
    "SemanticMemoryStore",
    "SimpleMemoryStore",
    # Reflection
    "ReflectionLoop",
    "ReflectionResult",
    "ReflectionVerdict",
    "ConfidenceCalibration",
    # Audit
    "AuditExporter",
    # Safety
    "CircuitBreaker",
    "CircuitBreakerOpen",
    "KillSwitch",
    "KillSwitchActivated",
    "RateLimiter",
    "RateLimitExceeded",
    "safe_resolve",
    # Version
    "__version__",
]
