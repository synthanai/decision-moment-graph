"""
Unit tests for action_dispatcher module.
"""

import pytest
import json
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sdk" / "python"))

from action_dispatcher import (
    Action, ActionType, Observation,
    LoggingDispatcher, DryRunDispatcher, CompositeDispatcher,
    create_dispatcher
)


class TestAction:
    """Tests for Action dataclass."""
    
    def test_action_creation(self):
        action = Action(
            action_type=ActionType.LOG,
            payload={"decision": "Test"},
            target="test-target"
        )
        assert action.action_type == ActionType.LOG
        assert action.payload["decision"] == "Test"
        assert action.target == "test-target"
    
    def test_action_from_dmg(self):
        dmg = {
            "memo": {
                "memo_id": "test-123",
                "decision": "Proceed",
                "recommendation": "Go ahead",
                "ramp": {"level": 2}
            }
        }
        action = Action.from_dmg(dmg)
        assert action.payload["decision"] == "Proceed"
        assert action.payload["ramp_level"] == 2


class TestObservation:
    """Tests for Observation dataclass."""
    
    def test_observation_success(self):
        obs = Observation(
            summary="Test passed",
            success=True,
            metrics={"latency": 100}
        )
        assert obs.success
        assert obs.get_metric("latency") == 100
    
    def test_observation_validates(self):
        obs = Observation(summary="OK", success=True)
        assert obs.validates("any claim")
        
        obs_fail = Observation(summary="Failed", success=False)
        assert not obs_fail.validates("any claim")


class TestLoggingDispatcher:
    """Tests for LoggingDispatcher."""
    
    def test_can_execute_any(self):
        dispatcher = LoggingDispatcher()
        action = Action(action_type=ActionType.HTTP_POST, payload={})
        assert dispatcher.can_execute(action)
    
    def test_execute_logs_action(self):
        dispatcher = LoggingDispatcher()
        action = Action(
            action_type=ActionType.LOG,
            payload={"test": True}
        )
        result = dispatcher.execute(action)
        
        assert result.success
        assert len(dispatcher.executed_actions) == 1
    
    def test_execute_dmg_directly(self):
        dispatcher = LoggingDispatcher()
        dmg = {"memo": {"decision": "Test"}}
        result = dispatcher.execute(dmg)
        
        assert result.success
    
    def test_rollback(self):
        dispatcher = LoggingDispatcher()
        action = Action(action_type=ActionType.LOG, payload={})
        dispatcher.execute(action)
        
        assert dispatcher.rollback(action)
        assert len(dispatcher.executed_actions) == 0


class TestDryRunDispatcher:
    """Tests for DryRunDispatcher."""
    
    def test_always_succeeds_at_1_0(self):
        dispatcher = DryRunDispatcher(success_rate=1.0)
        action = Action(action_type=ActionType.HTTP_POST, payload={})
        
        for _ in range(10):
            result = dispatcher.execute(action)
            assert result.success
    
    def test_fails_at_0_0(self):
        dispatcher = DryRunDispatcher(success_rate=0.0)
        action = Action(action_type=ActionType.LOG, payload={})
        result = dispatcher.execute(action)
        
        assert not result.success
    
    def test_simulates_latency(self):
        dispatcher = DryRunDispatcher(latency_ms=50)
        action = Action(action_type=ActionType.LOG, payload={})
        
        start = datetime.now()
        dispatcher.execute(action)
        elapsed = (datetime.now() - start).total_seconds() * 1000
        
        assert elapsed >= 45  # Allow some margin


class TestCompositeDispatcher:
    """Tests for CompositeDispatcher."""
    
    def test_chains_dispatchers(self):
        d1 = DryRunDispatcher(success_rate=0.0)  # Always fails
        d2 = LoggingDispatcher()  # Falls back to this
        
        composite = CompositeDispatcher([d1, d2])
        action = Action(action_type=ActionType.LOG, payload={})
        result = composite.execute(action)
        
        assert result.success


class TestCreateDispatcher:
    """Tests for factory function."""
    
    def test_create_logging(self):
        dispatcher = create_dispatcher({"type": "logging"})
        assert isinstance(dispatcher, LoggingDispatcher)
    
    def test_create_dry_run(self):
        dispatcher = create_dispatcher({"type": "dry_run", "success_rate": 0.5})
        assert isinstance(dispatcher, DryRunDispatcher)
    
    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            create_dispatcher({"type": "invalid"})
