"""
Unit tests for circuit_breaker module.
"""

import pytest
import time

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sdk" / "python"))

from circuit_breaker import (
    CircuitBreaker, BreakerState, CircuitBreakerOpen,
    KillSwitch, KillSwitchActivated,
    RateLimiter, RateLimitExceeded
)


class TestCircuitBreaker:
    """Tests for CircuitBreaker."""
    
    def test_starts_closed(self):
        breaker = CircuitBreaker()
        assert breaker.state == BreakerState.CLOSED
    
    def test_allows_requests_when_closed(self):
        breaker = CircuitBreaker()
        assert breaker.allow_request()
    
    def test_opens_after_failures(self):
        breaker = CircuitBreaker(failure_threshold=3)
        
        for _ in range(3):
            breaker.record_failure()
        
        assert breaker.state == BreakerState.OPEN
        assert not breaker.allow_request()
    
    def test_records_success(self):
        breaker = CircuitBreaker()
        breaker.record_success()
        
        assert breaker.stats.successful_calls == 1
    
    def test_reset(self):
        breaker = CircuitBreaker(failure_threshold=2)
        breaker.record_failure()
        breaker.record_failure()
        
        assert breaker.state == BreakerState.OPEN
        
        breaker.reset()
        assert breaker.state == BreakerState.CLOSED
    
    def test_context_manager_success(self):
        breaker = CircuitBreaker()
        
        with breaker:
            pass  # Success
        
        assert breaker.stats.successful_calls == 1
    
    def test_context_manager_failure(self):
        breaker = CircuitBreaker()
        
        with pytest.raises(ValueError):
            with breaker:
                raise ValueError("Test error")
        
        assert breaker.stats.failed_calls == 1
    
    def test_context_manager_blocked(self):
        breaker = CircuitBreaker(failure_threshold=1)
        breaker.record_failure()
        
        with pytest.raises(CircuitBreakerOpen):
            with breaker:
                pass


class TestKillSwitch:
    """Tests for KillSwitch."""
    
    def setup_method(self):
        KillSwitch.reset_singleton()
    
    def test_singleton(self):
        s1 = KillSwitch()
        s2 = KillSwitch()
        assert s1 is s2
    
    def test_starts_active(self):
        switch = KillSwitch()
        assert switch.is_active
    
    def test_activate(self):
        switch = KillSwitch()
        switch.activate("Emergency")
        
        assert not switch.is_active
        assert switch.status["reason"] == "Emergency"
    
    def test_deactivate(self):
        switch = KillSwitch()
        switch.activate("Test")
        switch.deactivate("Resolved")
        
        assert switch.is_active
    
    def test_check_raises_when_activated(self):
        switch = KillSwitch()
        switch.activate("Test")
        
        with pytest.raises(KillSwitchActivated):
            switch.check()


class TestRateLimiter:
    """Tests for RateLimiter."""
    
    def test_allows_within_limit(self):
        limiter = RateLimiter(max_calls=10, window_seconds=60)
        
        for _ in range(10):
            assert limiter.allow()
    
    def test_blocks_over_limit(self):
        limiter = RateLimiter(max_calls=3, window_seconds=60)
        
        for _ in range(3):
            limiter.allow()
        
        assert not limiter.allow()
    
    def test_remaining(self):
        limiter = RateLimiter(max_calls=5, window_seconds=60)
        
        limiter.allow()
        limiter.allow()
        
        assert limiter.remaining() == 3
    
    def test_reset(self):
        limiter = RateLimiter(max_calls=2, window_seconds=60)
        
        limiter.allow()
        limiter.allow()
        assert not limiter.allow()
        
        limiter.reset()
        assert limiter.allow()
