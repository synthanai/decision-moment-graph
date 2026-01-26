"""
Agentic SPAR Adapter

Extends SPARAdapter with closed-loop agentic capabilities:
- Memory retrieval for context enrichment
- Governance gate validation
- Outcome recording for feedback loops

Usage:
    from agentic_adapter import AgenticSPARAdapter
    
    adapter = AgenticSPARAdapter()
    result = adapter.run_loop(
        question="Should we migrate to microservices?",
        context="Current monolith is 5 years old",
        memory_store=my_memory_store
    )
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Protocol, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib

# Import base adapter
try:
    from spar_adapter import SPARAdapter
except ImportError:
    # Fallback for standalone testing
    class SPARAdapter:
        DMG_VERSION = "0.1"
        def convert(self, spar_output):
            return {"dmg_version": self.DMG_VERSION, "memo": {}, "moment": {}, "objects": {}}


class GateResult(Enum):
    """Result of governance gate check."""
    APPROVED = "approved"
    ESCALATE_HUMAN = "escalate_human"
    BLOCKED = "blocked"


@dataclass
class GateDecision:
    """Detailed governance gate decision."""
    result: GateResult
    reason: str
    required_actions: List[str] = field(default_factory=list)
    
    @classmethod
    def approved(cls, reason: str = "All gates passed"):
        return cls(result=GateResult.APPROVED, reason=reason)
    
    @classmethod
    def escalate(cls, reason: str, actions: List[str] = None):
        return cls(result=GateResult.ESCALATE_HUMAN, reason=reason, required_actions=actions or [])
    
    @classmethod
    def blocked(cls, reason: str, actions: List[str] = None):
        return cls(result=GateResult.BLOCKED, reason=reason, required_actions=actions or [])


@dataclass
class Observation:
    """Observation from environment after action execution."""
    summary: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat() + "Z")
    success: bool = True
    
    def get_metric(self, name: str) -> Any:
        """Get a specific metric value."""
        return self.metrics.get(name)
    
    def validates(self, claim: str) -> bool:
        """Check if observation validates a claim (simplified)."""
        # In real implementation, this would use semantic matching
        return self.success


@dataclass
class LoopResult:
    """Result of a complete agentic loop iteration."""
    dmg: Dict[str, Any]
    gate_decision: GateDecision
    executed: bool
    observation: Optional[Observation] = None
    enriched_context: str = ""
    lessons_applied: List[str] = field(default_factory=list)


# Use agentic-kit
from agentic_kit.memory import SemanticMemoryStore, SimpleMemoryStore

class AgenticSPARAdapter(SPARAdapter):
    """
    Agentic extension of SPARAdapter with feedback loops and governance.
    
    Adds three core capabilities:
    1. Context enrichment from prior decisions
    2. Governance gate validation before action
    3. Outcome recording for closed-loop learning
    """
    
    # Governance configuration
    RAMP_AUTO_APPROVE_THRESHOLD = 2
    CONFIDENCE_ESCALATION_THRESHOLD = 0.6
    MAX_UNRESOLVED_DISSENTS_FOR_AUTO = 0
    
    def __init__(self, memory_store: Optional[SemanticMemoryStore] = None):
        super().__init__()
        self.memory_store = memory_store or SimpleMemoryStore()
    
    def run_loop(
        self,
        spar_output: Dict[str, Any],
        action_executor: Optional[Callable] = None,
        auto_execute: bool = False
    ) -> LoopResult:
        """
        Execute full agentic SPAR loop.
        
        Args:
            spar_output: Output from SPAR deliberation session
            action_executor: Optional callable to execute the decision
            auto_execute: Whether to auto-execute approved decisions
            
        Returns:
            LoopResult with DMG, gate decision, and optional observation
        """
        # Step 1: Enrich context from memory
        original_context = spar_output.get("context", "")
        enriched_context, lessons = self.enrich_context(
            spar_output.get("question", ""),
            original_context
        )
        
        # Update SPAR output with enriched context
        spar_output_enriched = {**spar_output, "context": enriched_context}
        
        # Step 2: Convert SPAR to DMG
        dmg = self.convert(spar_output_enriched)
        
        # Add lessons as context note
        if lessons:
            if "context" not in dmg["memo"]:
                dmg["memo"]["context"] = {}
            dmg["memo"]["context"]["prior_lessons"] = lessons
        
        # Step 3: Check governance gates
        gate_decision = self.check_governance(dmg)
        
        # Step 4: Execute if approved and executor provided
        observation = None
        executed = False
        
        if gate_decision.result == GateResult.APPROVED:
            if auto_execute and action_executor:
                try:
                    observation = action_executor(dmg)
                    executed = True
                    
                    # Step 5: Record outcome
                    dmg = self.record_outcome(dmg, observation)
                    
                    # Step 6: Store in memory for future enrichment
                    self.memory_store.add(dmg)
                except Exception as e:
                    observation = Observation(
                        summary=f"Execution failed: {str(e)}",
                        success=False
                    )
                    dmg = self.record_outcome(dmg, observation)
        
        return LoopResult(
            dmg=dmg,
            gate_decision=gate_decision,
            executed=executed,
            observation=observation,
            enriched_context=enriched_context,
            lessons_applied=lessons
        )
    
    def enrich_context(
        self,
        question: str,
        original_context: str
    ) -> tuple[str, List[str]]:
        """
        Retrieve relevant prior decisions for context enrichment.
        
        Args:
            question: The decision question
            original_context: Original context from SPAR
            
        Returns:
            Tuple of (enriched context string, list of lessons applied)
        """
        lessons = []
        
        # Query similar decisions
        similar = self.memory_store.query(
            query=question,
            limit=5,
            min_score=0.0, # Merit filtering logic needs custom filter if strict
            filter_fn=lambda x: x.data.get("merit_score", 0) >= 3
        )
        
        if not similar:
            return original_context, lessons
        
        # Extract lessons from outcome checks
        for dmg in similar:
            outcome = dmg.get("objects", {}).get("outcome", {})
            checks = outcome.get("checks", [])
            
            for check in checks:
                # Extract from assumptions that were wrong
                for assumption_audit in check.get("assumptions_audit", []):
                    if not assumption_audit.get("accurate", True):
                        learning = assumption_audit.get("learning", "")
                        if learning:
                            lessons.append(learning)
                
                # Extract from vindicated dissents
                for dissent_audit in check.get("dissent_audit", []):
                    if dissent_audit.get("vindicated", False):
                        note = dissent_audit.get("note", "")
                        if note:
                            lessons.append(f"Prior dissent validated: {note}")
        
        # Build enriched context
        if lessons:
            lessons_text = "\n".join(f"- {l}" for l in lessons[:5])  # Limit to 5
            enriched = f"{original_context}\n\n**Prior Lessons:**\n{lessons_text}"
            return enriched, lessons
        
        return original_context, lessons
    
    def check_governance(self, dmg: Dict[str, Any]) -> GateDecision:
        """
        Validate decision against RAMP-based governance gates.
        
        Args:
            dmg: The DMG object to validate
            
        Returns:
            GateDecision with result, reason, and required actions
        """
        memo = dmg.get("memo", {})
        objects = dmg.get("objects", {})
        
        ramp = memo.get("ramp", {})
        ramp_level = ramp.get("level", 3)
        
        # Gate 1: Check RAMP level for auto-approve
        if ramp_level <= self.RAMP_AUTO_APPROVE_THRESHOLD:
            # Check DOORS for reversibility
            doors = objects.get("doors", {})
            if doors.get("ready"):
                return GateDecision.approved(
                    f"RAMP {ramp_level} with rollback plan allows auto-approval"
                )
        
        # Gate 2: Check for unresolved dissents at high RAMP
        dissents = objects.get("dissents", [])
        unresolved = [d for d in dissents if not d.get("resolution")]
        
        if ramp_level >= 4 and unresolved:
            return GateDecision.escalate(
                f"RAMP {ramp_level} with {len(unresolved)} unresolved dissent(s) requires human review",
                [f"Resolve dissent from {d.get('author', 'unknown')}" for d in unresolved]
            )
        
        # Gate 3: Check DOORS completeness for RAMP 3+
        if ramp_level >= 3:
            doors = objects.get("doors", {})
            missing = []
            
            own = doors.get("own", {})
            if not own.get("name"):
                missing.append("DOORS owner (doors.own.name)")
            
            if not doors.get("ready"):
                missing.append("Rollback plan (doors.ready)")
            
            signals = doors.get("signals", [])
            if len(signals) < 2:
                missing.append("At least 2 reversal signals (doors.signals)")
            
            if missing:
                return GateDecision.blocked(
                    f"RAMP {ramp_level} requires complete DOORS checklist",
                    missing
                )
        
        # Gate 4: Check confidence threshold
        expected_outcomes = memo.get("expected_outcomes", [])
        if expected_outcomes:
            confidence = expected_outcomes[0].get("confidence", 1.0)
            if confidence < self.CONFIDENCE_ESCALATION_THRESHOLD:
                return GateDecision.escalate(
                    f"Confidence {confidence:.0%} below threshold requires human confirmation",
                    ["Review synthesis and consider additional deliberation"]
                )
        
        # Gate 5: Always escalate RAMP 5
        if ramp_level >= 5:
            return GateDecision.escalate(
                "RAMP 5 (irreversible) always requires human approval",
                ["Executive review required", "Document in decision register"]
            )
        
        # All gates passed
        if ramp_level >= 3:
            return GateDecision.escalate(
                f"RAMP {ramp_level} requires human confirmation before execution"
            )
        
        return GateDecision.approved("All governance gates passed")
    
    def record_outcome(
        self,
        dmg: Dict[str, Any],
        observation: Observation
    ) -> Dict[str, Any]:
        """
        Close the loop by recording actual outcome.
        
        Args:
            dmg: The DMG object to update
            observation: Observation from action execution
            
        Returns:
            Updated DMG with outcome recorded
        """
        memo = dmg.get("memo", {})
        objects = dmg.get("objects", {})
        
        # Build expected outcomes audit
        expected_outcomes = memo.get("expected_outcomes", [])
        expected_outcomes_audit = []
        
        for exp in expected_outcomes:
            metric = exp.get("metric", "unknown")
            predicted = exp.get("expected", "N/A")
            confidence = exp.get("confidence", 0.5)
            actual = observation.get_metric(metric) or "Not measured"
            
            expected_outcomes_audit.append({
                "metric": metric,
                "predicted": str(predicted),
                "confidence": confidence,
                "actual": str(actual),
                "delta": self._calculate_delta(predicted, actual)
            })
        
        # Build dissent audit
        dissents = objects.get("dissents", [])
        dissent_audit = []
        
        for dissent in dissents:
            dissent_audit.append({
                "dissent_id": dissent.get("dissent_id", "unknown"),
                "vindicated": observation.validates(dissent.get("claim", "")),
                "note": f"Observation: {observation.summary[:100]}"
            })
        
        # Build assumptions audit from context
        context = memo.get("context", {})
        assumptions = context.get("assumptions", [])
        assumptions_audit = [
            {
                "assumption": a,
                "accurate": observation.success,  # Simplified
                "learning": "" if observation.success else f"Assumption may need revision: {a}"
            }
            for a in assumptions
        ]
        
        # Determine verdict
        verdict = self._determine_verdict(observation, expected_outcomes_audit)
        
        # Build outcome check
        check = {
            "check_date": observation.timestamp,
            "actual_result": observation.summary,
            "assumptions_audit": assumptions_audit,
            "dissent_audit": dissent_audit,
            "expected_outcomes_audit": expected_outcomes_audit,
            "verdict": verdict,
            "next_action": self._suggest_next_action(verdict, observation)
        }
        
        # Update outcome object
        if "outcome" not in objects:
            objects["outcome"] = {
                "outcome_id": f"outcome-{dmg.get('memo', {}).get('memo_id', 'unknown')}",
                "next_check_date": None,
                "checks": []
            }
        
        objects["outcome"]["checks"].append(check)
        
        # Set next check date (30 days by default)
        next_check = datetime.now() + timedelta(days=30)
        objects["outcome"]["next_check_date"] = next_check.strftime("%Y-%m-%d")
        
        # Add MOMENT event
        dmg = self._add_outcome_event(dmg, check)
        
        # Calculate MERIT score
        dmg["merit_score"] = self._calculate_merit_score(dmg)
        
        return dmg
    
    def _calculate_delta(self, predicted: Any, actual: Any) -> str:
        """Calculate delta between predicted and actual values."""
        try:
            if isinstance(predicted, (int, float)) and isinstance(actual, (int, float)):
                delta = actual - predicted
                return f"{delta:+.2f}" if isinstance(delta, float) else f"{delta:+d}"
        except (TypeError, ValueError):
            pass
        return "N/A"
    
    def _determine_verdict(
        self,
        observation: Observation,
        expected_outcomes_audit: List[Dict]
    ) -> str:
        """Determine verdict based on observation and expected outcomes."""
        if not observation.success:
            return "reverse"
        
        # Check if significant deltas exist
        significant_misses = 0
        for audit in expected_outcomes_audit:
            delta = audit.get("delta", "N/A")
            if delta != "N/A" and delta != "0":
                try:
                    delta_val = float(delta.replace("+", ""))
                    if abs(delta_val) > 0.2:  # 20% threshold
                        significant_misses += 1
                except ValueError:
                    pass
        
        if significant_misses > len(expected_outcomes_audit) / 2:
            return "adjust"
        
        return "keep"
    
    def _suggest_next_action(self, verdict: str, observation: Observation) -> str:
        """Suggest next action based on verdict."""
        if verdict == "reverse":
            return "Execute rollback plan per DOORS.ready"
        elif verdict == "adjust":
            return "Review assumptions and consider mid-course correction"
        else:
            return "Continue monitoring per DOORS.signals"
    
    def _add_outcome_event(self, dmg: Dict[str, Any], check: Dict) -> Dict[str, Any]:
        """Add OUTCOME_RECORDED event to MOMENT."""
        moment = dmg.get("moment", {})
        events = moment.get("events", [])
        
        seq = len(events) + 1
        prev_hash = events[-1]["hash"] if events else ""
        
        event = {
            "event_id": f"evt-{seq:03d}-outcome",
            "seq": seq,
            "ts": check["check_date"],
            "type": "OUTCOME_RECORDED",
            "actor": "agentic-adapter",
            "payload": {
                "verdict": check["verdict"],
                "actual_result": check["actual_result"][:200]
            },
            "prev_hash": prev_hash,
            "hash": self._compute_hash(seq, "OUTCOME_RECORDED", check, prev_hash)
        }
        
        events.append(event)
        moment["events"] = events
        dmg["moment"] = moment
        
        return dmg
    
    def _compute_hash(self, seq: int, event_type: str, payload: Dict, prev_hash: str) -> str:
        """Compute event hash for integrity chain."""
        hash_input = f"{seq}{event_type}{json.dumps(payload, sort_keys=True)}{prev_hash}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:12]
    
    def _calculate_merit_score(self, dmg: Dict[str, Any]) -> int:
        """Calculate MERIT score (0-5)."""
        score = 0
        objects = dmg.get("objects", {})
        memo = dmg.get("memo", {})
        moment = dmg.get("moment", {})
        
        # M: Measured - has outcome checks
        if objects.get("outcome", {}).get("checks"):
            score += 1
        
        # E: Evidenced - has traces
        if objects.get("traces"):
            score += 1
        
        # R: Reversible - has DOORS owner and ready plan
        doors = objects.get("doors", {})
        if doors.get("own", {}).get("name") and doors.get("ready"):
            score += 1
        
        # I: Inspectable - has events with valid chain
        events = moment.get("events", [])
        if events and events[0].get("type") == "MEMO_CREATED":
            score += 1
        
        # T: Traceable - has complete event chain
        if events and all(e.get("prev_hash") is not None for e in events[1:]):
            score += 1
        
        return score


# CLI helper for testing
def demo_loop():
    """Demonstrate agentic loop with sample SPAR output."""
    
    sample_spar = {
        "spar_id": "spar-demo-001",
        "question": "Should we migrate to microservices?",
        "context": "Current monolith is 5 years old; team of 8",
        "positions": [
            {"agent": "north", "role": "Champion", "position": "Yes, for scalability"},
            {"agent": "east", "role": "Challenger", "position": "No, complexity risk"},
            {"agent": "south", "role": "Pragmatist", "position": "Incremental approach"},
        ],
        "synthesis": {
            "recommendation": "Incremental migration starting with auth service",
            "confidence": 0.72,
            "rationale": "Balances speed with risk management",
            "key_tensions": ["Complexity vs scalability"],
            "conditions_to_reverse": ["If migration takes >6 months"]
        },
        "transcript": [],
        "config": {"pattern": "dialectic", "depth": "clash"}
    }
    
    adapter = AgenticSPARAdapter()
    result = adapter.run_loop(sample_spar, auto_execute=False)
    
    print("=" * 60)
    print("AGENTIC SPAR LOOP RESULT")
    print("=" * 60)
    print(f"Gate Decision: {result.gate_decision.result.value}")
    print(f"Reason: {result.gate_decision.reason}")
    if result.gate_decision.required_actions:
        print("Required Actions:")
        for action in result.gate_decision.required_actions:
            print(f"  - {action}")
    print(f"Executed: {result.executed}")
    print(f"Lessons Applied: {result.lessons_applied}")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    demo_loop()
