"""
Reflection Loop Extension

Adds post-VERIFY self-critique capability:
"Given this outcome, should we re-SPAR?"

Usage:
    from reflection import ReflectionLoop
    
    reflector = ReflectionLoop(adapter)
    should_respar, reason = reflector.evaluate(dmg, observation)
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple, List, Optional
from enum import Enum


class ReflectionVerdict(Enum):
    """Result of reflection evaluation."""
    CONTINUE = "continue"       # Decision is working, proceed
    ADJUST = "adjust"          # Minor tweaks needed, no re-SPAR
    RESPAR = "respar"          # Significant issues, re-deliberate
    ESCALATE = "escalate"      # Human review needed


@dataclass
class ReflectionResult:
    """Result of reflection evaluation."""
    verdict: ReflectionVerdict
    confidence: float
    reason: str
    suggestions: List[str]
    should_respar: bool
    
    @classmethod
    def continue_decision(cls, reason: str = "Decision performing as expected"):
        return cls(
            verdict=ReflectionVerdict.CONTINUE,
            confidence=0.9,
            reason=reason,
            suggestions=[],
            should_respar=False
        )
    
    @classmethod
    def suggest_respar(cls, reason: str, suggestions: List[str] = None):
        return cls(
            verdict=ReflectionVerdict.RESPAR,
            confidence=0.7,
            reason=reason,
            suggestions=suggestions or ["Re-run SPAR with updated context"],
            should_respar=True
        )


class ReflectionLoop:
    """
    Post-VERIFY reflection module.
    
    Evaluates whether a decision needs re-deliberation based on:
    - Outcome vs expectations
    - Vindicated dissents
    - Changed assumptions
    - Environmental changes
    """
    
    # Thresholds for triggering re-SPAR
    CONFIDENCE_DROP_THRESHOLD = 0.3   # If confidence drops >30%
    DISSENT_VINDICATION_THRESHOLD = 2  # If 2+ dissents vindicated
    ASSUMPTION_FAILURE_THRESHOLD = 2   # If 2+ assumptions wrong
    
    def __init__(self, adapter=None):
        self.adapter = adapter
    
    def evaluate(
        self,
        dmg: Dict[str, Any],
        observation: Optional[Dict[str, Any]] = None
    ) -> ReflectionResult:
        """
        Evaluate whether decision needs re-deliberation.
        
        Args:
            dmg: The DMG with outcome data
            observation: Optional latest observation
            
        Returns:
            ReflectionResult with verdict and suggestions
        """
        issues = []
        suggestions = []
        
        # Check outcome data
        objects = dmg.get("objects", {})
        outcome = objects.get("outcome", {})
        checks = outcome.get("checks", [])
        
        if not checks:
            return ReflectionResult.continue_decision("No outcome data yet")
        
        latest_check = checks[-1]
        
        # 1. Check verdict
        verdict = latest_check.get("verdict", "keep")
        if verdict == "reverse":
            return ReflectionResult.suggest_respar(
                "Decision was reversed - fundamental re-thinking needed",
                ["Re-SPAR with outcome learnings", "Consider alternative approaches"]
            )
        
        # 2. Check assumption failures
        assumption_failures = [
            a for a in latest_check.get("assumptions_audit", [])
            if not a.get("accurate", True)
        ]
        
        if len(assumption_failures) >= self.ASSUMPTION_FAILURE_THRESHOLD:
            issues.append(f"{len(assumption_failures)} assumptions proved incorrect")
            suggestions.extend([
                a.get("learning", "Review assumption")
                for a in assumption_failures
            ])
        
        # 3. Check vindicated dissents
        vindicated = [
            d for d in latest_check.get("dissent_audit", [])
            if d.get("vindicated", False)
        ]
        
        if len(vindicated) >= self.DISSENT_VINDICATION_THRESHOLD:
            issues.append(f"{len(vindicated)} dissents were vindicated")
            suggestions.append("Consider dissenting positions in re-deliberation")
        
        # 4. Check confidence calibration
        memo = dmg.get("memo", {})
        expected_outcomes = memo.get("expected_outcomes", [])
        outcome_audits = latest_check.get("expected_outcomes_audit", [])
        
        if expected_outcomes and outcome_audits:
            original_confidence = expected_outcomes[0].get("confidence", 0.7)
            
            # Calculate effective confidence based on actuals
            hits = sum(1 for a in outcome_audits if a.get("delta", "N/A") == "0")
            effective_confidence = hits / len(outcome_audits) if outcome_audits else 0
            
            drop = original_confidence - effective_confidence
            if drop > self.CONFIDENCE_DROP_THRESHOLD:
                issues.append(f"Confidence dropped {drop:.0%}")
                suggestions.append("Recalibrate expectations in new SPAR")
        
        # 5. Environmental changes (from observation)
        if observation:
            if observation.get("environment_changed", False):
                issues.append("Environment has significantly changed")
                suggestions.append("Re-SPAR with updated context")
        
        # Determine overall verdict
        if len(issues) >= 2:
            return ReflectionResult(
                verdict=ReflectionVerdict.RESPAR,
                confidence=0.75,
                reason="; ".join(issues),
                suggestions=suggestions[:5],  # Limit suggestions
                should_respar=True
            )
        elif len(issues) == 1:
            return ReflectionResult(
                verdict=ReflectionVerdict.ADJUST,
                confidence=0.8,
                reason=issues[0],
                suggestions=suggestions[:3],
                should_respar=False
            )
        else:
            return ReflectionResult.continue_decision()
    
    def auto_respar(
        self,
        dmg: Dict[str, Any],
        original_spar: Dict[str, Any],
        max_iterations: int = 3
    ) -> Tuple[Dict[str, Any], int]:
        """
        Automatically re-SPAR if needed, up to max_iterations.
        
        Returns:
            Tuple of (final DMG, number of iterations)
        """
        if not self.adapter:
            raise ValueError("Adapter required for auto_respar")
        
        current_dmg = dmg
        iterations = 0
        
        while iterations < max_iterations:
            result = self.evaluate(current_dmg)
            
            if not result.should_respar:
                break
            
            # Enhance context with learnings
            enhanced_context = original_spar.get("context", "")
            enhanced_context += f"\n\nPrior attempt learnings:\n"
            for suggestion in result.suggestions:
                enhanced_context += f"- {suggestion}\n"
            
            # Run new SPAR
            enhanced_spar = {**original_spar, "context": enhanced_context}
            loop_result = self.adapter.run_loop(enhanced_spar, auto_execute=False)
            
            current_dmg = loop_result.dmg
            iterations += 1
        
        return current_dmg, iterations


# Confidence Calibration Tracker
class ConfidenceCalibration:
    """
    Track prediction accuracy over time to calibrate confidence.
    
    Usage:
        calibrator = ConfidenceCalibration()
        calibrator.record(predicted=0.8, actual_success=True)
        calibrator.record(predicted=0.7, actual_success=False)
        
        # Get calibrated confidence
        adjusted = calibrator.adjust(raw_confidence=0.8)
    """
    
    def __init__(self):
        self.records: List[Dict] = []
    
    def record(self, predicted: float, actual_success: bool):
        """Record a prediction and its outcome."""
        self.records.append({
            "predicted": predicted,
            "actual": 1.0 if actual_success else 0.0
        })
    
    def adjust(self, raw_confidence: float) -> float:
        """
        Adjust confidence based on historical accuracy.
        
        If we've been overconfident, this reduces the confidence.
        If we've been underconfident, this increases it.
        """
        if len(self.records) < 5:
            return raw_confidence  # Not enough data
        
        # Calculate bias: average(predicted) - average(actual)
        avg_predicted = sum(r["predicted"] for r in self.records) / len(self.records)
        avg_actual = sum(r["actual"] for r in self.records) / len(self.records)
        
        bias = avg_predicted - avg_actual
        
        # Adjust by removing bias
        adjusted = raw_confidence - bias
        
        # Clamp to [0.1, 0.95]
        return max(0.1, min(0.95, adjusted))
    
    def accuracy_score(self) -> float:
        """Calculate Brier score (lower is better)."""
        if not self.records:
            return 0.0
        
        mse = sum(
            (r["predicted"] - r["actual"]) ** 2
            for r in self.records
        ) / len(self.records)
        
        return 1.0 - mse  # Convert to accuracy (higher is better)
    
    def stats(self) -> Dict[str, Any]:
        """Return calibration statistics."""
        if not self.records:
            return {"records": 0}
        
        return {
            "records": len(self.records),
            "avg_predicted": sum(r["predicted"] for r in self.records) / len(self.records),
            "avg_actual": sum(r["actual"] for r in self.records) / len(self.records),
            "accuracy_score": self.accuracy_score()
        }


if __name__ == "__main__":
    # Demo
    sample_dmg = {
        "memo": {
            "expected_outcomes": [{"confidence": 0.8}]
        },
        "objects": {
            "outcome": {
                "checks": [
                    {
                        "verdict": "adjust",
                        "assumptions_audit": [
                            {"assumption": "A1", "accurate": False, "learning": "L1"},
                            {"assumption": "A2", "accurate": False, "learning": "L2"}
                        ],
                        "dissent_audit": [
                            {"dissent_id": "d1", "vindicated": True}
                        ],
                        "expected_outcomes_audit": []
                    }
                ]
            }
        }
    }
    
    reflector = ReflectionLoop()
    result = reflector.evaluate(sample_dmg)
    
    print(f"Verdict: {result.verdict.value}")
    print(f"Should re-SPAR: {result.should_respar}")
    print(f"Reason: {result.reason}")
    print(f"Suggestions: {result.suggestions}")
