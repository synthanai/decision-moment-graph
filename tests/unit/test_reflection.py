"""
Unit tests for reflection module.
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sdk" / "python"))

from reflection import (
    ReflectionLoop, ReflectionResult, ReflectionVerdict,
    ConfidenceCalibration
)


class TestReflectionLoop:
    """Tests for ReflectionLoop."""
    
    def test_continue_on_no_outcome(self):
        reflector = ReflectionLoop()
        dmg = {"objects": {"outcome": {}}}
        
        result = reflector.evaluate(dmg)
        assert result.verdict == ReflectionVerdict.CONTINUE
        assert not result.should_respar
    
    def test_respar_on_reverse(self):
        reflector = ReflectionLoop()
        dmg = {
            "objects": {
                "outcome": {
                    "checks": [{"verdict": "reverse"}]
                }
            }
        }
        
        result = reflector.evaluate(dmg)
        assert result.verdict == ReflectionVerdict.RESPAR
        assert result.should_respar
    
    def test_respar_on_multiple_assumption_failures(self):
        reflector = ReflectionLoop()
        dmg = {
            "objects": {
                "outcome": {
                    "checks": [{
                        "verdict": "adjust",
                        "assumptions_audit": [
                            {"assumption": "A1", "accurate": False, "learning": "L1"},
                            {"assumption": "A2", "accurate": False, "learning": "L2"}
                        ]
                    }]
                }
            }
        }
        
        result = reflector.evaluate(dmg)
        assert len(result.suggestions) > 0
    
    def test_respar_on_vindicated_dissents(self):
        reflector = ReflectionLoop()
        dmg = {
            "objects": {
                "outcome": {
                    "checks": [{
                        "verdict": "adjust",
                        "dissent_audit": [
                            {"dissent_id": "d1", "vindicated": True},
                            {"dissent_id": "d2", "vindicated": True}
                        ]
                    }]
                }
            }
        }
        
        result = reflector.evaluate(dmg)
        assert "vindicated" in result.reason.lower()


class TestReflectionResult:
    """Tests for ReflectionResult factory methods."""
    
    def test_continue_decision(self):
        result = ReflectionResult.continue_decision("All good")
        assert result.verdict == ReflectionVerdict.CONTINUE
        assert not result.should_respar
        assert result.confidence == 0.9
    
    def test_suggest_respar(self):
        result = ReflectionResult.suggest_respar(
            "Issues found",
            ["Fix A", "Fix B"]
        )
        assert result.verdict == ReflectionVerdict.RESPAR
        assert result.should_respar
        assert len(result.suggestions) == 2


class TestConfidenceCalibration:
    """Tests for ConfidenceCalibration."""
    
    def test_record_and_adjust(self):
        cal = ConfidenceCalibration()
        
        # Record some predictions
        for _ in range(5):
            cal.record(predicted=0.8, actual_success=True)
        for _ in range(5):
            cal.record(predicted=0.8, actual_success=False)
        
        # Should have some adjustment
        adjusted = cal.adjust(0.8)
        assert 0.1 <= adjusted <= 0.95
    
    def test_no_adjustment_with_few_records(self):
        cal = ConfidenceCalibration()
        cal.record(predicted=0.7, actual_success=True)
        
        # Not enough data, should return raw
        assert cal.adjust(0.8) == 0.8
    
    def test_accuracy_score(self):
        cal = ConfidenceCalibration()
        
        # Perfect predictions
        cal.record(predicted=1.0, actual_success=True)
        cal.record(predicted=0.0, actual_success=False)
        
        score = cal.accuracy_score()
        assert score == 1.0
    
    def test_stats(self):
        cal = ConfidenceCalibration()
        cal.record(predicted=0.7, actual_success=True)
        
        stats = cal.stats()
        assert stats["records"] == 1
        assert stats["avg_predicted"] == 0.7
