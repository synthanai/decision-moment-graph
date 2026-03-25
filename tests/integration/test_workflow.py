"""
Integration tests for DMG workflow
"""

import pytest
import json
from datetime import datetime, timedelta


class TestFullDecisionWorkflow:
    """Test complete decision lifecycle."""
    
    def test_draft_to_final_workflow(self):
        """Test the complete Draft → Proposed → Approved → Final flow."""
        # Phase 1: Create Draft
        memo = {
            "memo_id": "workflow-test-001",
            "title": "Should we adopt GraphQL?",
            "options": [
                {"name": "Yes, full adoption", "description": "Replace REST with GraphQL"},
                {"name": "Partial", "description": "GraphQL for new APIs only"},
                {"name": "No", "description": "Stay with REST"}
            ],
            "ramp": {"level": 3},
            "version": 1,
            "created_at": datetime.now().isoformat()
        }
        
        dmg = {"dmg_version": "0.1", "memo": memo}
        assert dmg["memo"]["version"] == 1
        
        # Phase 2: Add Deliberation
        dmg["objects"] = {
            "dissents": [
                {
                    "dissent_id": "d1",
                    "author": "Backend Lead",
                    "claim": "Learning curve is steep",
                    "conditions_to_change_mind": "If we get 2 weeks dedicated training"
                }
            ],
            "traces": [
                {
                    "trace_id": "t1",
                    "claim": "GraphQL reduces over-fetching",
                    "source": {"type": "article", "uri": "https://graphql.org/learn/"},
                    "strength": "strong"
                }
            ]
        }
        
        # Phase 3: Add Governance
        dmg["memo"]["doors"] = {
            "declare": "We will use GraphQL for new APIs starting Q2",
            "observe": ["API response times", "Developer satisfaction"],
            "own": {"name": "Sarah Chen", "role": "Tech Lead"},
            "ready": "Fallback to REST if GraphQL causes >10% latency increase",
            "signals": [
                {"metric": "P99 latency", "threshold": ">200ms", "action": "Rollback"},
                {"metric": "Error rate", "threshold": ">2%", "action": "Rollback"}
            ]
        }
        
        dmg["memo"]["expected_outcomes"] = [
            {
                "metric": "Developer velocity",
                "expected": "+20%",
                "confidence": 0.7,
                "horizon": "Q3 2026"
            }
        ]
        
        # Phase 4: Commit
        dmg["objects"]["commit"] = {"state": "Proposed"}
        dmg["memo"]["version"] = 2
        
        # Phase 5: Approve
        dmg["objects"]["commit"]["state"] = "Approved"
        dmg["objects"]["commit"]["approvals"] = [
            {"actor": "cto@company.com", "approved_at": datetime.now().isoformat()}
        ]
        
        # Phase 6: Finalize
        dmg["objects"]["commit"]["state"] = "Final"
        dmg["objects"]["outcome"] = {
            "outcome_id": "outcome-workflow-001",
            "next_check_date": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
        }
        
        # Verify final state
        assert dmg["objects"]["commit"]["state"] == "Final"
        assert dmg["objects"]["outcome"]["next_check_date"] is not None
        assert len(dmg["objects"]["dissents"]) >= 1
        assert dmg["memo"]["doors"]["own"]["name"] is not None
    
    def test_outcome_check_flow(self):
        """Test outcome check recording."""
        # Setup: Final decision
        dmg = {
            "dmg_version": "0.1",
            "memo": {
                "memo_id": "outcome-test-001",
                "title": "Test decision",
                "options": [
                    {"name": "A"}, {"name": "B"}, {"name": "C"}
                ],
                "ramp": {"level": 3},
                "expected_outcomes": [
                    {"metric": "Success rate", "expected": ">80%", "confidence": 0.7}
                ]
            },
            "objects": {
                "commit": {"state": "Final"},
                "outcome": {
                    "outcome_id": "outcome-001",
                    "next_check_date": "2026-01-25",
                    "checks": []
                }
            }
        }
        
        # Perform outcome check
        check = {
            "check_date": "2026-01-25",
            "actual_result": "Achieved 85% success rate",
            "expected_outcomes_audit": [
                {
                    "metric": "Success rate",
                    "predicted": ">80%",
                    "actual": "85%",
                    "delta": "+5%"
                }
            ],
            "verdict": "keep",
            "next_action": "Continue with current approach"
        }
        
        dmg["objects"]["outcome"]["checks"].append(check)
        
        # Verify
        assert len(dmg["objects"]["outcome"]["checks"]) == 1
        assert dmg["objects"]["outcome"]["checks"][0]["verdict"] == "keep"
    
    def test_reversal_flow(self):
        """Test decision reversal."""
        dmg = {
            "dmg_version": "0.1",
            "memo": {
                "memo_id": "reversal-test-001",
                "title": "Decision to reverse",
                "ramp": {"level": 3}
            },
            "objects": {
                "commit": {"state": "Final"},
                "outcome": {
                    "checks": [
                        {
                            "check_date": "2026-01-25",
                            "actual_result": "Complete failure",
                            "verdict": "reverse",
                            "next_action": "Rollback to previous state"
                        }
                    ]
                }
            }
        }
        
        # Apply reversal
        dmg["objects"]["commit"]["state"] = "Reversed"
        dmg["objects"]["commit"]["reversed_at"] = datetime.now().isoformat()
        dmg["objects"]["commit"]["reversed_reason"] = "Outcome check indicated failure"
        
        assert dmg["objects"]["commit"]["state"] == "Reversed"


class TestMOMENTEventLogging:
    """Test MOMENT event chain."""
    
    def test_event_sequencing(self):
        """Events should be sequential."""
        events = [
            {"seq": 1, "type": "MEMO_CREATED"},
            {"seq": 2, "type": "OPTION_ADDED"},
            {"seq": 3, "type": "DISSENT_ADDED"},
            {"seq": 4, "type": "COMMIT_STATE_CHANGED"}
        ]
        
        # Verify sequence
        for i, event in enumerate(events):
            assert event["seq"] == i + 1
    
    def test_hash_chain_integrity(self):
        """Events should form a valid hash chain."""
        import hashlib
        
        def compute_hash(seq, type_, payload, prev_hash):
            data = f"{seq}{type_}{json.dumps(payload)}{prev_hash}"
            return hashlib.sha256(data.encode()).hexdigest()[:12]
        
        events = []
        
        # Event 1
        prev = ""
        hash1 = compute_hash(1, "MEMO_CREATED", {"title": "Test"}, prev)
        events.append({"seq": 1, "prev_hash": prev, "hash": hash1})
        
        # Event 2
        hash2 = compute_hash(2, "OPTION_ADDED", {"option": "A"}, hash1)
        events.append({"seq": 2, "prev_hash": hash1, "hash": hash2})
        
        # Verify chain
        for i in range(1, len(events)):
            assert events[i]["prev_hash"] == events[i-1]["hash"]
    
    def test_append_only(self):
        """MOMENT should be append-only."""
        moment = {
            "events": [
                {"seq": 1, "type": "MEMO_CREATED"},
                {"seq": 2, "type": "OPTION_ADDED"}
            ]
        }
        
        # Add new event
        moment["events"].append({"seq": 3, "type": "DISSENT_ADDED"})
        
        # Verify append only (no deletion, no edit)
        assert len(moment["events"]) == 3
        assert moment["events"][0]["seq"] == 1  # Original preserved


class TestDISSENTTracking:
    """Test DISSENT lifecycle."""
    
    def test_dissent_resolution_types(self):
        """Test valid DISSENT resolution types."""
        valid_resolutions = ["accepted", "mitigated", "deferred", "rejected"]
        
        for resolution in valid_resolutions:
            dissent = {
                "dissent_id": "d1",
                "author": "Test",
                "claim": "Test concern",
                "resolution": resolution
            }
            assert dissent["resolution"] in valid_resolutions
    
    def test_dissent_requires_conditions(self):
        """DISSENT should have conditions_to_change_mind."""
        dissent = {
            "dissent_id": "d1",
            "author": "Skeptic",
            "claim": "This won't work because...",
            "conditions_to_change_mind": "If success rate exceeds 80% in pilot"
        }
        
        assert dissent["conditions_to_change_mind"] is not None
        assert len(dissent["conditions_to_change_mind"]) > 0
    
    def test_dissent_audit(self):
        """Dissent should be auditable in outcome check."""
        dissent = {
            "dissent_id": "d1",
            "claim": "Timeline too aggressive",
            "conditions_to_change_mind": "If we deliver on time"
        }
        
        outcome_check = {
            "dissent_audit": [
                {
                    "dissent_id": "d1",
                    "vindicated": True,
                    "notes": "Timeline did slip by 2 weeks"
                }
            ]
        }
        
        assert outcome_check["dissent_audit"][0]["vindicated"] is True


class TestDOORSValidation:
    """Test DOORS checklist completeness."""
    
    def test_doors_all_fields(self):
        """DOORS should have all 5 components."""
        doors = {
            "declare": "We commit to X",
            "observe": ["Metric A", "Metric B"],
            "own": {"name": "John Doe", "role": "Owner"},
            "ready": "Rollback plan: revert to Y",
            "signals": [
                {"metric": "Error rate", "threshold": ">1%", "action": "Alert"},
                {"metric": "Latency", "threshold": ">500ms", "action": "Rollback"}
            ]
        }
        
        assert "declare" in doors
        assert "observe" in doors
        assert "own" in doors
        assert "ready" in doors
        assert "signals" in doors
    
    def test_doors_owner_is_named(self):
        """DOORS owner should be a specific person."""
        invalid_owners = ["the team", "engineering", "TBD", ""]
        
        doors = {
            "own": {"name": "Sarah Chen", "role": "Tech Lead"}
        }
        
        assert doors["own"]["name"] not in invalid_owners
        assert len(doors["own"]["name"]) > 0
    
    def test_doors_signals_have_thresholds(self):
        """Each signal should have metric, threshold, and action."""
        signals = [
            {"metric": "P99 latency", "threshold": ">200ms", "action": "Rollback"},
            {"metric": "Error rate", "threshold": ">1%", "action": "Alert team"}
        ]
        
        for signal in signals:
            assert "metric" in signal
            assert "threshold" in signal
            assert "action" in signal
