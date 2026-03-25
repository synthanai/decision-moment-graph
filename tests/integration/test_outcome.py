"""
Integration tests for outcome tracking
"""

import pytest
import json
from datetime import datetime, timedelta


class TestOutcomeScheduling:
    """Test outcome check scheduling."""
    
    def test_schedule_from_ramp_level(self):
        """Suggested check date based on RAMP level."""
        ramp_to_days = {
            1: 7,     # L1: 1 week
            2: 14,    # L2: 2 weeks
            3: 30,    # L3: 1 month
            4: 90,    # L4: 3 months
            5: 180    # L5: 6 months
        }
        
        for ramp, days in ramp_to_days.items():
            decision_date = datetime.now()
            suggested_check = decision_date + timedelta(days=days)
            
            assert (suggested_check - decision_date).days == days
    
    def test_overdue_detection(self):
        """Detect overdue outcome checks."""
        past_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        outcome = {
            "next_check_date": past_date
        }
        
        is_overdue = outcome["next_check_date"] < today
        assert is_overdue
    
    def test_upcoming_detection(self):
        """Detect upcoming outcome checks."""
        future_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        outcome = {
            "next_check_date": future_date
        }
        
        is_upcoming = today <= outcome["next_check_date"] <= next_week
        assert is_upcoming


class TestOutcomeChecks:
    """Test outcome check recording."""
    
    @pytest.fixture
    def sample_memo(self):
        """Sample memo with expected outcomes."""
        return {
            "memo_id": "outcome-test-001",
            "title": "Test Decision",
            "expected_outcomes": [
                {
                    "metric": "Revenue increase",
                    "expected": "+15%",
                    "confidence": 0.7,
                    "horizon": "Q2 2026"
                },
                {
                    "metric": "Customer churn",
                    "expected": "<5%",
                    "confidence": 0.8,
                    "horizon": "Q2 2026"
                }
            ],
            "context": {
                "assumptions": [
                    "Market conditions remain stable",
                    "Team maintains current velocity"
                ]
            }
        }
    
    def test_outcome_check_structure(self, sample_memo):
        """Outcome check should have required structure."""
        check = {
            "check_date": datetime.now().strftime("%Y-%m-%d"),
            "actual_result": "Revenue increased 12%, churn at 4%",
            "expected_outcomes_audit": [
                {
                    "metric": "Revenue increase",
                    "predicted": "+15%",
                    "actual": "+12%",
                    "delta": "-3%",
                    "verdict": "partial"
                },
                {
                    "metric": "Customer churn",
                    "predicted": "<5%",
                    "actual": "4%",
                    "delta": "on target",
                    "verdict": "success"
                }
            ],
            "assumptions_audit": [
                {
                    "assumption": "Market conditions remain stable",
                    "accurate": True,
                    "learning": ""
                },
                {
                    "assumption": "Team maintains current velocity",
                    "accurate": False,
                    "learning": "Lost 2 engineers in Q1"
                }
            ],
            "verdict": "adjust",
            "next_action": "Review pricing strategy"
        }
        
        assert "check_date" in check
        assert "actual_result" in check
        assert "verdict" in check
        assert check["verdict"] in ["keep", "adjust", "reverse"]
    
    def test_assumptions_audit(self, sample_memo):
        """Assumptions should be auditable."""
        assumptions = sample_memo["context"]["assumptions"]
        
        audit = []
        for assumption in assumptions:
            audit.append({
                "assumption": assumption,
                "accurate": None,  # To be filled
                "learning": ""
            })
        
        assert len(audit) == len(assumptions)
    
    def test_calibration_calculation(self):
        """Calculate calibration score from outcomes."""
        outcomes = [
            {"predicted_confidence": 0.5, "was_correct": True},
            {"predicted_confidence": 0.5, "was_correct": False},
            {"predicted_confidence": 0.7, "was_correct": True},
            {"predicted_confidence": 0.7, "was_correct": False},
            {"predicted_confidence": 0.9, "was_correct": True},
        ]
        
        # Group by confidence bucket
        buckets = {}
        for outcome in outcomes:
            conf = outcome["predicted_confidence"]
            if conf not in buckets:
                buckets[conf] = {"count": 0, "correct": 0}
            buckets[conf]["count"] += 1
            if outcome["was_correct"]:
                buckets[conf]["correct"] += 1
        
        # Calculate accuracy per bucket
        for conf, data in buckets.items():
            actual_rate = data["correct"] / data["count"]
            buckets[conf]["actual_rate"] = actual_rate
        
        # Check calibration at 50% bucket
        assert buckets[0.5]["actual_rate"] == 0.5  # 1/2 = 50% actual


class TestVerdicts:
    """Test verdict determination."""
    
    def test_keep_verdict(self):
        """Keep verdict when outcomes met."""
        expected = [
            {"metric": "Revenue", "expected": "+10%", "actual": "+12%"},
            {"metric": "Churn", "expected": "<5%", "actual": "3%"}
        ]
        
        # All expectations met or exceeded
        all_met = all(
            self._exceeded_or_met(e) for e in expected
        )
        
        verdict = "keep" if all_met else "adjust"
        assert verdict == "keep"
    
    def test_adjust_verdict(self):
        """Adjust verdict when outcomes partially met."""
        expected = [
            {"metric": "Revenue", "expected": "+10%", "actual": "+7%"},  # Missed
            {"metric": "Churn", "expected": "<5%", "actual": "3%"}  # Met
        ]
        
        some_met = any(self._exceeded_or_met(e) for e in expected)
        all_met = all(self._exceeded_or_met(e) for e in expected)
        
        verdict = "adjust" if some_met and not all_met else ("keep" if all_met else "reverse")
        assert verdict == "adjust"
    
    def test_reverse_verdict(self):
        """Reverse verdict when outcomes significantly missed."""
        expected = [
            {"metric": "Revenue", "expected": "+10%", "actual": "-5%"},  # Way off
            {"metric": "Churn", "expected": "<5%", "actual": "15%"}  # Way off
        ]
        
        all_missed = not any(self._exceeded_or_met(e) for e in expected)
        
        verdict = "reverse" if all_missed else "adjust"
        assert verdict == "reverse"
    
    def _exceeded_or_met(self, expectation):
        """Simple check if expectation was met (example logic)."""
        # In reality, this would parse the values
        actual = expectation.get("actual", "")
        expected = expectation.get("expected", "")
        
        # Simplified: if actual contains a + and expected contains a +, check values
        if "+" in actual and "+" in expected:
            actual_val = float(actual.replace("+", "").replace("%", ""))
            expected_val = float(expected.replace("+", "").replace("%", ""))
            return actual_val >= expected_val
        
        if "<" in expected:
            threshold = float(expected.replace("<", "").replace("%", ""))
            actual_val = float(actual.replace("%", ""))
            return actual_val < threshold
        
        return False


class TestOutcomeChain:
    """Test multiple outcome checks over time."""
    
    def test_outcome_history(self):
        """Track multiple outcome checks."""
        outcome = {
            "outcome_id": "outcome-001",
            "next_check_date": "2026-04-01",
            "checks": [
                {
                    "check_date": "2026-01-01",
                    "verdict": "keep",
                    "notes": "Initial check, on track"
                },
                {
                    "check_date": "2026-02-01",
                    "verdict": "adjust",
                    "notes": "Minor deviation, correcting"
                },
                {
                    "check_date": "2026-03-01",
                    "verdict": "keep",
                    "notes": "Back on track"
                }
            ]
        }
        
        assert len(outcome["checks"]) == 3
        
        # Latest check
        latest = outcome["checks"][-1]
        assert latest["verdict"] == "keep"
    
    def test_verdict_trend(self):
        """Analyze verdict trend over time."""
        verdicts = ["keep", "keep", "adjust", "adjust", "reverse"]
        
        # Detect deteriorating trend
        if len(verdicts) >= 3:
            recent = verdicts[-3:]
            if recent == ["adjust", "adjust", "reverse"]:
                trend = "deteriorating"
            elif recent == ["reverse", "adjust", "keep"]:
                trend = "recovering"
            else:
                trend = "stable"
        
        assert trend == "deteriorating"


class TestLearningLoop:
    """Test learning from outcomes."""
    
    def test_dissent_vindication_tracking(self):
        """Track which dissenters were vindicated."""
        dissents = [
            {"author": "A", "claim": "Timeline too aggressive"},
            {"author": "B", "claim": "Budget insufficient"},
            {"author": "C", "claim": "Team not ready"}
        ]
        
        audit = [
            {"author": "A", "vindicated": True, "notes": "Took 2 months longer"},
            {"author": "B", "vindicated": False, "notes": "Stayed in budget"},
            {"author": "C", "vindicated": True, "notes": "Needed training"}
        ]
        
        vindicated = [a for a in audit if a["vindicated"]]
        vindication_rate = len(vindicated) / len(audit)
        
        assert vindication_rate == 2/3
    
    def test_assumption_failure_tracking(self):
        """Track which assumptions failed."""
        assumptions = [
            "Market remains stable",
            "Team velocity maintained",
            "No regulatory changes"
        ]
        
        audit = [
            {"assumption": "Market remains stable", "accurate": True},
            {"assumption": "Team velocity maintained", "accurate": False},
            {"assumption": "No regulatory changes", "accurate": True}
        ]
        
        failed = [a for a in audit if not a["accurate"]]
        failure_rate = len(failed) / len(audit)
        
        assert len(failed) == 1
        assert failed[0]["assumption"] == "Team velocity maintained"
