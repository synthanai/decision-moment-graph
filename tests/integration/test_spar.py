"""
Integration tests for SPAR → DMG adapter
"""

import pytest
import sys
from pathlib import Path


# Add sdk to path for imports
SDK_PATH = Path(__file__).parent.parent.parent / "sdk" / "python"
if str(SDK_PATH) not in sys.path:
    sys.path.insert(0, str(SDK_PATH))


class TestSPARAdapterImport:
    """Test SPAR adapter can be imported."""
    
    def test_import_spar_adapter(self):
        """Should be able to import SPARAdapter."""
        try:
            from spar_adapter import SPARAdapter
            assert SPARAdapter is not None
        except ImportError as e:
            pytest.skip(f"Could not import spar_adapter: {e}")
    
    def test_adapter_instantiation(self):
        """Should be able to create adapter instance."""
        try:
            from spar_adapter import SPARAdapter
            adapter = SPARAdapter()
            assert adapter is not None
        except ImportError:
            pytest.skip("spar_adapter not available")


class TestSPARConversion:
    """Test SPAR output to DMG conversion."""
    
    @pytest.fixture
    def sample_spar_output(self):
        """Sample SPAR output for testing."""
        return {
            "spar_id": "spar-test-001",
            "question": "Should we build or buy the analytics feature?",
            "context": "We have 3 engineers; $50k budget",
            "config": {
                "pattern": "dialectic",
                "depth": "clash",
                "style": "steelman"
            },
            "positions": [
                {
                    "agent": "north",
                    "role": "Champion",
                    "position": "Build in-house for full control",
                    "arguments": ["Full customization", "No vendor lock-in"],
                    "evidence": []
                },
                {
                    "agent": "east",
                    "role": "Challenger",
                    "position": "Buy vendor solution for speed",
                    "arguments": ["Faster time-to-value", "Lower risk"],
                    "evidence": [{"type": "case_study", "uri": "https://example.com"}]
                },
                {
                    "agent": "south",
                    "role": "Pragmatist",
                    "position": "Hybrid: buy core, customize edges",
                    "arguments": ["Best of both worlds"],
                    "evidence": []
                },
                {
                    "agent": "west",
                    "role": "Sage",
                    "position": "Defer decision until requirements clearer",
                    "arguments": ["Reduce waste", "More information needed"],
                    "evidence": []
                }
            ],
            "synthesis": {
                "recommendation": "Buy vendor solution with custom integration",
                "confidence": 0.75,
                "rationale": "Speed outweighs control given timeline",
                "key_tensions": ["Lock-in risk acknowledged"],
                "conditions_to_reverse": ["If integration exceeds 3 months"]
            },
            "probe": {
                "plurality": 9,
                "rigor": 8,
                "origin": 9,
                "basis": 8,
                "execution": 7
            },
            "transcript": [
                {"seq": 1, "ts": "2026-01-25T00:00:00Z", "agent": "north", "type": "position", "content": "Build in-house..."},
                {"seq": 2, "ts": "2026-01-25T00:01:00Z", "agent": "east", "type": "rebuttal", "content": "But buying gives us..."}
            ]
        }
    
    def test_convert_spar_to_dmg(self, sample_spar_output):
        """Convert SPAR output to DMG format."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            # Verify DMG structure
            assert "dmg_version" in dmg
            assert "memo" in dmg
            assert "moment" in dmg
            assert "objects" in dmg
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_memo_title_from_question(self, sample_spar_output):
        """MEMO title should come from SPAR question."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            assert dmg["memo"]["title"] == sample_spar_output["question"]
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_options_from_positions(self, sample_spar_output):
        """Options should be created from SPAR positions."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            options = dmg["memo"]["options"]
            positions = sample_spar_output["positions"]
            
            assert len(options) == len(positions)
            
            for option in options:
                assert "source" in option
                assert option["source"].startswith("spar:")
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_recommendation_from_synthesis(self, sample_spar_output):
        """Recommendation should come from SPAR synthesis."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            recommendation = dmg["memo"]["recommendation"]
            synthesis = sample_spar_output["synthesis"]["recommendation"]
            
            assert synthesis in recommendation
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_dissent_from_non_winning_positions(self, sample_spar_output):
        """DISSENT should be created from positions that weren't recommended."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            dissents = dmg["objects"]["dissents"]
            
            # Should have dissents from positions that weren't the recommendation
            assert len(dissents) > 0
            
            for dissent in dissents:
                assert "author" in dissent
                assert "claim" in dissent
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_trace_from_evidence(self, sample_spar_output):
        """TRACE should be created from SPAR evidence."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            traces = dmg["objects"]["traces"]
            
            # East agent had evidence, should create trace
            assert len(traces) > 0
            
            for trace in traces:
                assert "source" in trace
                assert "uri" in trace["source"]
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_moment_from_transcript(self, sample_spar_output):
        """MOMENT events should be created from SPAR transcript."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            events = dmg["moment"]["events"]
            
            # Should have multiple events
            assert len(events) > 1
            
            # Should include MEMO_CREATED
            event_types = [e["type"] for e in events]
            assert "MEMO_CREATED" in event_types
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_ramp_auto_suggestion(self, sample_spar_output):
        """RAMP should be auto-suggested from SPAR config."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            ramp = dmg["memo"]["ramp"]
            
            assert "level" in ramp
            assert 1 <= ramp["level"] <= 5
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_confidence_from_synthesis(self, sample_spar_output):
        """Expected outcomes should include SPAR confidence."""
        try:
            from spar_adapter import SPARAdapter
            
            adapter = SPARAdapter()
            dmg = adapter.convert(sample_spar_output)
            
            expected_outcomes = dmg["memo"]["expected_outcomes"]
            
            assert len(expected_outcomes) > 0
            
            # Should have confidence from synthesis
            confidences = [o.get("confidence") for o in expected_outcomes if o.get("confidence")]
            assert sample_spar_output["synthesis"]["confidence"] in confidences
        except ImportError:
            pytest.skip("spar_adapter not available")


class TestSPARModes:
    """Test different SPAR modes produce valid DMG."""
    
    @pytest.fixture
    def base_spar(self):
        """Base SPAR output for mode testing."""
        return {
            "spar_id": "spar-mode-test",
            "question": "Test question",
            "context": "",
            "positions": [
                {"agent": "north", "role": "Champion", "position": "Yes", "arguments": ["Reason 1"]},
                {"agent": "south", "role": "Challenger", "position": "No", "arguments": ["Reason 2"]}
            ],
            "synthesis": {
                "recommendation": "Yes",
                "confidence": 0.6,
                "rationale": "More pros",
                "key_tensions": [],
                "conditions_to_reverse": []
            },
            "probe": {"plurality": 7, "rigor": 7, "origin": 7, "basis": 7, "execution": 7}
        }
    
    def test_quick_mode(self, base_spar):
        """Quick mode (2 agents) produces valid DMG."""
        try:
            from spar_adapter import SPARAdapter
            
            base_spar["config"] = {"pattern": "binary", "depth": "duel"}
            
            adapter = SPARAdapter()
            dmg = adapter.convert(base_spar)
            
            # Quick mode should still produce valid DMG
            assert dmg["memo"]["title"] == base_spar["question"]
        except ImportError:
            pytest.skip("spar_adapter not available")
    
    def test_deep_mode(self, base_spar):
        """Deep mode (8 agents) produces valid DMG."""
        try:
            from spar_adapter import SPARAdapter
            
            # Add more positions for deep mode
            base_spar["positions"].extend([
                {"agent": "east", "role": "Skeptic", "position": "Maybe", "arguments": ["Need more data"]},
                {"agent": "west", "role": "Sage", "position": "Wait", "arguments": ["History shows"]},
            ])
            base_spar["config"] = {"pattern": "dialectic", "depth": "rumble"}
            
            adapter = SPARAdapter()
            dmg = adapter.convert(base_spar)
            
            assert len(dmg["memo"]["options"]) == 4
        except ImportError:
            pytest.skip("spar_adapter not available")
