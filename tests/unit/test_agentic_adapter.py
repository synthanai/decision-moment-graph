"""
Unit tests for AgenticSPARAdapter

Tests the closed-loop agentic capabilities:
- Context enrichment from memory
- Governance gate validation
- Outcome recording
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add sdk to path for imports
SDK_PATH = Path(__file__).parent.parent.parent / "sdk" / "python"
if str(SDK_PATH) not in sys.path:
    sys.path.insert(0, str(SDK_PATH))


class TestAgenticAdapterImport:
    """Test agentic adapter can be imported."""
    
    def test_import_agentic_adapter(self):
        """Should be able to import AgenticSPARAdapter."""
        try:
            from agentic_adapter import AgenticSPARAdapter
            assert AgenticSPARAdapter is not None
        except ImportError as e:
            pytest.skip(f"Could not import agentic_adapter: {e}")
    
    def test_adapter_instantiation(self):
        """Should be able to create adapter instance."""
        try:
            from agentic_adapter import AgenticSPARAdapter
            adapter = AgenticSPARAdapter()
            assert adapter is not None
        except ImportError:
            pytest.skip("agentic_adapter not available")
    
    def test_inherits_from_spar_adapter(self):
        """AgenticSPARAdapter should extend SPARAdapter."""
        try:
            from agentic_adapter import AgenticSPARAdapter
            from spar_adapter import SPARAdapter
            
            adapter = AgenticSPARAdapter()
            assert isinstance(adapter, SPARAdapter)
        except ImportError:
            pytest.skip("adapters not available")


class TestContextEnrichment:
    """Test context enrichment from memory."""
    
    @pytest.fixture
    def adapter_with_memory(self):
        """Create adapter with pre-populated memory store."""
        try:
            from agentic_adapter import AgenticSPARAdapter, SimpleMemoryStore
            
            store = SimpleMemoryStore()
            
            # Add a prior decision with lessons
            prior_dmg = {
                "memo": {"memo_id": "prior-001", "title": "API migration decision"},
                "objects": {
                    "outcome": {
                        "checks": [
                            {
                                "check_date": "2026-01-01",
                                "assumptions_audit": [
                                    {
                                        "assumption": "Migration takes 2 weeks",
                                        "accurate": False,
                                        "learning": "Add 100% buffer for migrations"
                                    }
                                ],
                                "dissent_audit": [
                                    {
                                        "dissent_id": "d-001",
                                        "vindicated": True,
                                        "note": "Complexity was underestimated"
                                    }
                                ]
                            }
                        ]
                    }
                },
                "merit_score": 4
            }
            store.store(prior_dmg)
            
            return AgenticSPARAdapter(memory_store=store)
        except ImportError:
            pytest.skip("agentic_adapter not available")
    
    def test_enrich_context_returns_tuple(self, adapter_with_memory):
        """enrich_context should return (context, lessons) tuple."""
        enriched, lessons = adapter_with_memory.enrich_context(
            question="Should we migrate to new API?",
            original_context="Current API is v1"
        )
        
        assert isinstance(enriched, str)
        assert isinstance(lessons, list)
    
    def test_enrich_context_includes_lessons(self, adapter_with_memory):
        """Enriched context should include lessons from prior decisions."""
        enriched, lessons = adapter_with_memory.enrich_context(
            question="Should we migrate to new API?",
            original_context="Current API is v1"
        )
        
        # Should have extracted lessons
        assert len(lessons) > 0
        assert "Add 100% buffer for migrations" in lessons
    
    def test_enrich_context_preserves_original(self, adapter_with_memory):
        """Original context should be preserved in enriched version."""
        original = "Current API is v1"
        enriched, _ = adapter_with_memory.enrich_context(
            question="Should we migrate?",
            original_context=original
        )
        
        assert original in enriched
    
    def test_enrich_context_handles_empty_memory(self):
        """Should handle empty memory store gracefully."""
        try:
            from agentic_adapter import AgenticSPARAdapter, SimpleMemoryStore
            
            adapter = AgenticSPARAdapter(memory_store=SimpleMemoryStore())
            original = "Some context"
            
            enriched, lessons = adapter.enrich_context("Any question?", original)
            
            assert enriched == original
            assert lessons == []
        except ImportError:
            pytest.skip("agentic_adapter not available")


class TestGovernanceGates:
    """Test governance gate validation."""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance."""
        try:
            from agentic_adapter import AgenticSPARAdapter
            return AgenticSPARAdapter()
        except ImportError:
            pytest.skip("agentic_adapter not available")
    
    @pytest.fixture
    def low_ramp_dmg(self):
        """DMG with RAMP level 1 (auto-approvable)."""
        return {
            "memo": {
                "ramp": {"level": 1},
                "expected_outcomes": [{"confidence": 0.8}]
            },
            "objects": {
                "doors": {"ready": "Can revert config change"},
                "dissents": []
            }
        }
    
    @pytest.fixture
    def high_ramp_dmg(self):
        """DMG with RAMP level 4 (requires human review)."""
        return {
            "memo": {
                "ramp": {"level": 4},
                "expected_outcomes": [{"confidence": 0.8}]
            },
            "objects": {
                "doors": {
                    "own": {"name": "Tech Lead"},
                    "ready": "Rollback plan documented",
                    "signals": [
                        {"metric": "latency", "threshold": ">500ms"},
                        {"metric": "errors", "threshold": ">1%"}
                    ]
                },
                "dissents": []
            }
        }
    
    def test_low_ramp_approved(self, adapter, low_ramp_dmg):
        """RAMP 1-2 with rollback plan should be approved."""
        from agentic_adapter import GateResult
        
        decision = adapter.check_governance(low_ramp_dmg)
        assert decision.result == GateResult.APPROVED
    
    def test_high_ramp_escalates(self, adapter, high_ramp_dmg):
        """RAMP 3+ should escalate to human."""
        from agentic_adapter import GateResult
        
        decision = adapter.check_governance(high_ramp_dmg)
        assert decision.result == GateResult.ESCALATE_HUMAN
    
    def test_unresolved_dissent_escalates(self, adapter, high_ramp_dmg):
        """Unresolved dissents at high RAMP should escalate."""
        from agentic_adapter import GateResult
        
        # Add unresolved dissent
        high_ramp_dmg["objects"]["dissents"] = [
            {"dissent_id": "d-001", "author": "engineer", "claim": "Risk underestimated"}
        ]
        
        decision = adapter.check_governance(high_ramp_dmg)
        assert decision.result == GateResult.ESCALATE_HUMAN
        assert "unresolved dissent" in decision.reason.lower()
    
    def test_missing_doors_owner_blocks(self, adapter):
        """Missing DOORS owner at RAMP 3+ should block."""
        from agentic_adapter import GateResult
        
        dmg = {
            "memo": {
                "ramp": {"level": 3},
                "expected_outcomes": [{"confidence": 0.9}]
            },
            "objects": {
                "doors": {
                    "ready": "Some plan",
                    "signals": [{"metric": "m1"}, {"metric": "m2"}]
                    # Missing "own"
                },
                "dissents": []
            }
        }
        
        decision = adapter.check_governance(dmg)
        assert decision.result == GateResult.BLOCKED
        assert "DOORS owner" in str(decision.required_actions)
    
    def test_low_confidence_escalates(self, adapter):
        """Low confidence should escalate."""
        from agentic_adapter import GateResult
        
        dmg = {
            "memo": {
                "ramp": {"level": 2},
                "expected_outcomes": [{"confidence": 0.4}]  # Below 0.6 threshold
            },
            "objects": {
                "doors": {"ready": "Some plan"},
                "dissents": []
            }
        }
        
        decision = adapter.check_governance(dmg)
        assert decision.result == GateResult.ESCALATE_HUMAN
        assert "confidence" in decision.reason.lower()
    
    def test_ramp_5_always_escalates(self, adapter):
        """RAMP 5 should always escalate regardless of other factors."""
        from agentic_adapter import GateResult
        
        dmg = {
            "memo": {
                "ramp": {"level": 5},
                "expected_outcomes": [{"confidence": 0.99}]
            },
            "objects": {
                "doors": {
                    "own": {"name": "CEO"},
                    "ready": "Complete plan",
                    "signals": [{"m": 1}, {"m": 2}, {"m": 3}]
                },
                "dissents": []
            }
        }
        
        decision = adapter.check_governance(dmg)
        assert decision.result == GateResult.ESCALATE_HUMAN
        assert "RAMP 5" in decision.reason


class TestOutcomeRecording:
    """Test outcome recording for feedback loop."""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance."""
        try:
            from agentic_adapter import AgenticSPARAdapter
            return AgenticSPARAdapter()
        except ImportError:
            pytest.skip("agentic_adapter not available")
    
    @pytest.fixture
    def sample_dmg(self):
        """Sample DMG for outcome recording."""
        return {
            "memo": {
                "memo_id": "memo-001",
                "context": {"assumptions": ["Integration takes 2 weeks"]},
                "expected_outcomes": [
                    {"metric": "completion_time", "expected": "2 weeks", "confidence": 0.7}
                ]
            },
            "moment": {
                "events": [
                    {"event_id": "e-001", "type": "MEMO_CREATED", "hash": "abc123", "prev_hash": ""}
                ]
            },
            "objects": {
                "dissents": [
                    {"dissent_id": "d-001", "claim": "Timeline is optimistic"}
                ],
                "outcome": {"outcome_id": "out-001", "checks": []}
            }
        }
    
    @pytest.fixture
    def success_observation(self):
        """Successful observation."""
        try:
            from agentic_adapter import Observation
            return Observation(
                summary="Integration completed in 2.5 weeks",
                metrics={"completion_time": "2.5 weeks"},
                success=True
            )
        except ImportError:
            pytest.skip("agentic_adapter not available")
    
    def test_record_outcome_adds_check(self, adapter, sample_dmg, success_observation):
        """Recording outcome should add a check to outcome.checks."""
        updated = adapter.record_outcome(sample_dmg, success_observation)
        
        checks = updated["objects"]["outcome"]["checks"]
        assert len(checks) == 1
    
    def test_record_outcome_includes_actual_result(self, adapter, sample_dmg, success_observation):
        """Check should include actual result from observation."""
        updated = adapter.record_outcome(sample_dmg, success_observation)
        
        check = updated["objects"]["outcome"]["checks"][0]
        assert check["actual_result"] == success_observation.summary
    
    def test_record_outcome_audits_expectations(self, adapter, sample_dmg, success_observation):
        """Check should audit expected outcomes."""
        updated = adapter.record_outcome(sample_dmg, success_observation)
        
        check = updated["objects"]["outcome"]["checks"][0]
        audit = check["expected_outcomes_audit"]
        
        assert len(audit) == 1
        assert audit[0]["metric"] == "completion_time"
        assert audit[0]["predicted"] == "2 weeks"
        assert audit[0]["actual"] == "2.5 weeks"
    
    def test_record_outcome_audits_dissents(self, adapter, sample_dmg, success_observation):
        """Check should audit dissents."""
        updated = adapter.record_outcome(sample_dmg, success_observation)
        
        check = updated["objects"]["outcome"]["checks"][0]
        audit = check["dissent_audit"]
        
        assert len(audit) == 1
        assert audit[0]["dissent_id"] == "d-001"
    
    def test_record_outcome_adds_moment_event(self, adapter, sample_dmg, success_observation):
        """Recording should add OUTCOME_RECORDED event to moment."""
        updated = adapter.record_outcome(sample_dmg, success_observation)
        
        events = updated["moment"]["events"]
        assert len(events) == 2  # Original + new
        assert events[-1]["type"] == "OUTCOME_RECORDED"
    
    def test_record_outcome_sets_next_check_date(self, adapter, sample_dmg, success_observation):
        """Recording should set next check date."""
        updated = adapter.record_outcome(sample_dmg, success_observation)
        
        next_check = updated["objects"]["outcome"]["next_check_date"]
        assert next_check is not None
    
    def test_record_outcome_calculates_merit_score(self, adapter, sample_dmg, success_observation):
        """Recording should calculate MERIT score."""
        updated = adapter.record_outcome(sample_dmg, success_observation)
        
        assert "merit_score" in updated
        assert 0 <= updated["merit_score"] <= 5


class TestFullLoop:
    """Test full agentic loop execution."""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance."""
        try:
            from agentic_adapter import AgenticSPARAdapter
            return AgenticSPARAdapter()
        except ImportError:
            pytest.skip("agentic_adapter not available")
    
    @pytest.fixture
    def sample_spar_output(self):
        """Sample SPAR output for loop testing."""
        return {
            "spar_id": "spar-loop-001",
            "question": "Should we implement feature X?",
            "context": "Budget: $10k; Timeline: 2 weeks",
            "positions": [
                {"agent": "north", "position": "Yes", "arguments": ["ROI positive"]},
                {"agent": "south", "position": "No", "arguments": ["Resource constrained"]}
            ],
            "synthesis": {
                "recommendation": "Implement MVP first",
                "confidence": 0.7,
                "rationale": "Test assumptions with minimal investment",
                "key_tensions": ["Resource vs opportunity"],
                "conditions_to_reverse": []
            },
            "config": {"pattern": "dialectic"}
        }
    
    def test_run_loop_returns_result(self, adapter, sample_spar_output):
        """run_loop should return LoopResult."""
        from agentic_adapter import LoopResult
        
        result = adapter.run_loop(sample_spar_output)
        
        assert isinstance(result, LoopResult)
        assert result.dmg is not None
        assert result.gate_decision is not None
    
    def test_run_loop_creates_dmg(self, adapter, sample_spar_output):
        """Loop should create valid DMG from SPAR output."""
        result = adapter.run_loop(sample_spar_output)
        
        assert "dmg_version" in result.dmg
        assert "memo" in result.dmg
        assert "moment" in result.dmg
    
    def test_run_loop_without_executor_not_executed(self, adapter, sample_spar_output):
        """Without executor, executed should be False."""
        result = adapter.run_loop(sample_spar_output, auto_execute=True)
        
        # No executor provided, should not execute
        assert result.executed is False
    
    def test_run_loop_with_executor(self, adapter, sample_spar_output):
        """With executor and auto_execute, should execute if approved."""
        from agentic_adapter import Observation
        
        def mock_executor(dmg):
            return Observation(summary="Action executed successfully")
        
        # Use low RAMP to get approval
        sample_spar_output["config"]["horizon"] = "now"  # Lower RAMP
        
        result = adapter.run_loop(
            sample_spar_output,
            action_executor=mock_executor,
            auto_execute=True
        )
        
        # Execution depends on gate decision
        if result.gate_decision.result.value == "approved":
            assert result.executed is True
            assert result.observation is not None
