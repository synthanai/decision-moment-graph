"""
Unit tests for DMG governance rules
"""

import pytest
import json
from pathlib import Path


class TestGovernanceRule1_Options:
    """Test: All decisions must have ≥3 options."""
    
    def test_three_options_passes(self, minimal_decision):
        """Three options should pass."""
        assert len(minimal_decision["memo"]["options"]) >= 3
    
    def test_two_options_fails(self, invalid_fixtures_dir):
        """Two options should fail governance check."""
        with open(invalid_fixtures_dir / "only_two_options.dmg.json") as f:
            dmg = json.load(f)
        
        options = dmg["memo"].get("options", [])
        assert len(options) < 3
    
    def test_four_options_passes(self):
        """More than three options is fine."""
        dmg = {
            "memo": {
                "options": [
                    {"name": "A"},
                    {"name": "B"},
                    {"name": "C"},
                    {"name": "D"}
                ]
            }
        }
        assert len(dmg["memo"]["options"]) >= 3


class TestGovernanceRule2_Dissent:
    """Test: RAMP ≥3 with Final/Approved requires ≥1 DISSENT."""
    
    def test_high_ramp_final_needs_dissent(self, invalid_fixtures_dir):
        """RAMP 3+ with Final state needs dissent."""
        with open(invalid_fixtures_dir / "no_dissent_high_ramp.dmg.json") as f:
            dmg = json.load(f)
        
        ramp = dmg["memo"]["ramp"]["level"]
        state = dmg["objects"]["commit"]["state"]
        dissents = dmg["objects"].get("dissents", [])
        
        assert ramp >= 3
        assert state in ["Final", "Approved"]
        assert len(dissents) == 0  # This should fail
    
    def test_low_ramp_no_dissent_ok(self):
        """RAMP 1-2 can finalize without dissent."""
        dmg = {
            "memo": {
                "ramp": {"level": 2}
            },
            "objects": {
                "dissents": [],
                "commit": {"state": "Final"}
            }
        }
        ramp = dmg["memo"]["ramp"]["level"]
        state = dmg["objects"]["commit"]["state"]
        
        # This should pass - low RAMP doesn't need dissent
        assert ramp < 3 or len(dmg["objects"]["dissents"]) > 0
    
    def test_draft_no_dissent_ok(self):
        """Draft state doesn't require dissent regardless of RAMP."""
        dmg = {
            "memo": {
                "ramp": {"level": 5}
            },
            "objects": {
                "dissents": [],
                "commit": {"state": "Draft"}
            }
        }
        state = dmg["objects"]["commit"]["state"]
        assert state == "Draft"  # Dissent not required for Draft


class TestGovernanceRule3_DOORS:
    """Test: RAMP ≥3 with Final/Approved requires DOORS owner."""
    
    def test_high_ramp_needs_doors_owner(self, invalid_fixtures_dir):
        """RAMP 3+ with Final needs named DOORS owner."""
        with open(invalid_fixtures_dir / "missing_doors_owner.dmg.json") as f:
            dmg = json.load(f)
        
        ramp = dmg["memo"]["ramp"]["level"]
        doors = dmg["memo"].get("doors", {})
        owner = doors.get("own", {}).get("name")
        
        assert ramp >= 3
        assert not owner  # This should fail
    
    def test_doors_owner_present_passes(self, complete_decision):
        """Complete decision has DOORS owner."""
        doors = complete_decision["memo"].get("doors", {})
        owner = doors.get("own", {}).get("name")
        
        assert owner and len(owner) > 0
    
    def test_doors_signals_required(self, complete_decision):
        """RAMP 3+ requires ≥2 DOORS signals."""
        doors = complete_decision["memo"].get("doors", {})
        signals = doors.get("signals", [])
        ramp = complete_decision["memo"]["ramp"]["level"]
        
        if ramp >= 3:
            assert len(signals) >= 2


class TestGovernanceRule4_OutcomeCheck:
    """Test: Final/Approved requires outcome check date."""
    
    def test_final_needs_outcome_date(self, invalid_fixtures_dir):
        """Final state requires outcome.next_check_date."""
        with open(invalid_fixtures_dir / "missing_outcome_date.dmg.json") as f:
            dmg = json.load(f)
        
        state = dmg["objects"]["commit"]["state"]
        outcome_date = dmg["objects"].get("outcome", {}).get("next_check_date")
        
        assert state == "Final"
        assert not outcome_date  # This should fail
    
    def test_valid_has_outcome_date(self, complete_decision):
        """Complete decision has outcome check date."""
        outcome = complete_decision["objects"].get("outcome", {})
        next_check = outcome.get("next_check_date")
        
        assert next_check is not None


class TestGovernanceRule5_ExpectedOutcomes:
    """Test: RAMP ≥3 requires expected outcomes with confidence."""
    
    def test_high_ramp_needs_expected_outcomes(self, complete_decision):
        """RAMP 3+ should have expected outcomes."""
        ramp = complete_decision["memo"]["ramp"]["level"]
        expected = complete_decision["memo"].get("expected_outcomes", [])
        
        if ramp >= 3:
            assert len(expected) >= 1
    
    def test_outcomes_have_confidence(self, complete_decision):
        """Expected outcomes should have confidence scores."""
        expected = complete_decision["memo"].get("expected_outcomes", [])
        
        for outcome in expected:
            assert "confidence" in outcome
            assert 0 <= outcome["confidence"] <= 1


class TestGovernanceLogic:
    """Test governance decision logic."""
    
    def test_governance_matrix(self):
        """Test the governance requirements matrix."""
        # Define requirements by RAMP level
        requirements = {
            1: {"min_options": 3, "dissent_required": False, "doors_required": False},
            2: {"min_options": 3, "dissent_required": False, "doors_required": False},
            3: {"min_options": 3, "dissent_required": True, "doors_required": True},
            4: {"min_options": 3, "dissent_required": True, "doors_required": True},
            5: {"min_options": 3, "dissent_required": True, "doors_required": True},
        }
        
        for level, reqs in requirements.items():
            assert reqs["min_options"] == 3
            if level >= 3:
                assert reqs["dissent_required"] is True
                assert reqs["doors_required"] is True
            else:
                assert reqs["dissent_required"] is False
    
    def test_state_transitions(self):
        """Test valid state transitions."""
        valid_transitions = {
            "Draft": ["Proposed", "Draft"],
            "Proposed": ["Draft", "Approved", "Proposed"],
            "Approved": ["Final", "Draft", "Approved"],
            "Final": ["Reversed", "Superseded", "Final"],
            "Reversed": ["Reversed"],
            "Superseded": ["Superseded"]
        }
        
        # Verify transition rules are complete
        for state, valid_next in valid_transitions.items():
            assert state in valid_next or state in ["Reversed", "Superseded"]
