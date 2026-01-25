#!/usr/bin/env python3
"""
End-to-End RESOLVE Loop Example

Demonstrates the full agentic loop:
Recon → Enrich → SPAR → Okay → Launch → Verify → Encode

This example simulates two decision cycles to show how
memory enrichment improves subsequent decisions.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add SDK to path
SDK_PATH = Path(__file__).parent.parent / "sdk" / "python"
sys.path.insert(0, str(SDK_PATH))

from agentic_adapter import AgenticSPARAdapter, Observation
from action_dispatcher import LoggingDispatcher, DryRunDispatcher
from semantic_memory import SemanticMemoryStore


def run_complete_resolve_cycle():
    """
    Run two complete RESOLVE cycles demonstrating memory enrichment.
    """
    print("=" * 70)
    print("🔄 RESOLVE LOOP: End-to-End Example")
    print("=" * 70)
    print()
    
    # Initialize components
    memory = SemanticMemoryStore()
    adapter = AgenticSPARAdapter(memory_store=memory)
    dispatcher = DryRunDispatcher(success_rate=0.8, latency_ms=50)
    
    # =========================================================================
    # CYCLE 1: First Decision (No Prior Context)
    # =========================================================================
    
    print("┌" + "─" * 68 + "┐")
    print("│ CYCLE 1: API Migration Decision                                    │")
    print("└" + "─" * 68 + "┘")
    print()
    
    spar_output_1 = {
        "spar_id": "spar-cycle-001",
        "question": "Should we migrate the legacy API to GraphQL?",
        "context": "Current REST API is 4 years old; 50+ endpoints; team of 6",
        "positions": [
            {
                "agent": "north",
                "role": "Champion",
                "position": "Full migration to GraphQL",
                "arguments": ["Better DX", "Reduced over-fetching", "Type safety"]
            },
            {
                "agent": "east",
                "role": "Challenger",
                "position": "Keep REST, add GraphQL layer",
                "arguments": ["Lower risk", "Gradual adoption", "Preserve existing clients"]
            },
            {
                "agent": "south",
                "role": "Pragmatist",
                "position": "Migrate high-traffic endpoints first",
                "arguments": ["Quick wins", "Learn as we go", "Validate assumptions"]
            },
            {
                "agent": "west",
                "role": "Sage",
                "position": "Wait for more data on usage patterns",
                "arguments": ["Measure first", "Avoid premature optimization"]
            }
        ],
        "synthesis": {
            "recommendation": "Migrate top 5 endpoints to GraphQL as pilot",
            "confidence": 0.68,
            "rationale": "Validates approach with minimal risk",
            "key_tensions": ["Speed vs thoroughness", "New tech learning curve"],
            "conditions_to_reverse": ["If pilot takes > 3 weeks", "If performance degrades > 10%"]
        },
        "transcript": [],
        "config": {"pattern": "dialectic", "depth": "clash"}
    }
    
    print("📍 R - RECON: Defining decision scope")
    print(f"   Question: {spar_output_1['question']}")
    print()
    
    print("📍 E - ENRICH: Checking memory for prior decisions")
    result_1 = adapter.run_loop(
        spar_output_1,
        action_executor=dispatcher.execute,
        auto_execute=False  # Don't execute yet
    )
    print(f"   Prior lessons available: {len(result_1.lessons_applied)}")
    print()
    
    print("📍 S - SPAR: Deliberation complete")
    print(f"   Recommendation: {spar_output_1['synthesis']['recommendation']}")
    print(f"   Confidence: {spar_output_1['synthesis']['confidence']:.0%}")
    print()
    
    print("📍 O - OKAY: Governance gate check")
    print(f"   Result: {result_1.gate_decision.result.value.upper()}")
    print(f"   Reason: {result_1.gate_decision.reason}")
    print()
    
    # Simulate adding DOORS for execution
    print("   📝 Adding required DOORS information...")
    result_1.dmg["objects"]["doors"] = {
        "declare": "We will migrate top 5 endpoints to GraphQL",
        "observe": ["Response latency", "Error rate", "Developer satisfaction"],
        "own": {"name": "API Team Lead", "role": "Tech Lead"},
        "ready": "Rollback: revert to REST endpoints within 1 hour",
        "signals": [
            {"metric": "latency", "threshold": ">200ms", "action": "Investigate"},
            {"metric": "errors", "threshold": ">1%", "action": "Rollback"}
        ]
    }
    
    # Re-run with DOORS
    result_1 = adapter.run_loop(
        spar_output_1,
        action_executor=dispatcher.execute,
        auto_execute=True
    )
    
    print("📍 L - LAUNCH: Executing decision")
    print(f"   Executed: {result_1.executed}")
    if result_1.observation:
        print(f"   Observation: {result_1.observation.summary}")
    print()
    
    print("📍 V - VERIFY: Reality check")
    # Simulate actual outcome observation
    actual_outcome = Observation(
        summary="Pilot completed in 4 weeks (over estimate), performance improved 15%",
        success=True,
        metrics={
            "duration_weeks": 4,
            "latency_improvement": "15%",
            "team_satisfaction": 8
        }
    )
    
    # Record the outcome
    result_1.dmg = adapter.record_outcome(result_1.dmg, actual_outcome)
    
    # Simulate a lesson learned from inaccurate assumption
    result_1.dmg["objects"]["outcome"]["checks"][0]["assumptions_audit"] = [
        {
            "assumption": "Pilot takes 3 weeks",
            "accurate": False,
            "learning": "GraphQL migrations take 30% longer than estimated"
        }
    ]
    
    print(f"   Actual: {actual_outcome.summary}")
    print()
    
    print("📍 E - ENCODE: Storing to memory")
    memory.add(result_1.dmg)
    print(f"   MERIT Score: {result_1.dmg.get('merit_score', 'N/A')}/5")
    print(f"   Memory size: {len(memory)} decision(s)")
    print()
    
    # =========================================================================
    # CYCLE 2: Similar Decision WITH Prior Context
    # =========================================================================
    
    print()
    print("┌" + "─" * 68 + "┐")
    print("│ CYCLE 2: Database Migration Decision (With Memory)                 │")
    print("└" + "─" * 68 + "┘")
    print()
    
    spar_output_2 = {
        "spar_id": "spar-cycle-002",
        "question": "Should we migrate the database from PostgreSQL to MongoDB?",
        "context": "PostgreSQL is 5 years old; complex joins; team considering document model",
        "positions": [
            {
                "agent": "north",
                "role": "Champion",
                "position": "Full migration to MongoDB",
                "arguments": ["Better for document data", "Horizontal scaling"]
            },
            {
                "agent": "east",
                "role": "Challenger",
                "position": "Keep PostgreSQL, add caching layer",
                "arguments": ["Proven reliability", "Team expertise", "ACID compliance"]
            },
            {
                "agent": "south",
                "role": "Pragmatist",
                "position": "Migrate specific collections first",
                "arguments": ["Test compatibility", "Gradual learning"]
            }
        ],
        "synthesis": {
            "recommendation": "Migrate user preferences to MongoDB as pilot",
            "confidence": 0.65,
            "rationale": "Low-risk data, validates approach",
            "key_tensions": ["Data integrity vs flexibility"],
            "conditions_to_reverse": ["If data consistency issues arise"]
        },
        "config": {"pattern": "dialectic", "depth": "clash"}
    }
    
    print("📍 R - RECON: Defining decision scope")
    print(f"   Question: {spar_output_2['question']}")
    print()
    
    print("📍 E - ENRICH: Checking memory for prior decisions")
    result_2 = adapter.run_loop(
        spar_output_2,
        action_executor=None,
        auto_execute=False
    )
    
    print(f"   ✨ Prior lessons found: {len(result_2.lessons_applied)}")
    for lesson in result_2.lessons_applied:
        print(f"      → {lesson}")
    print()
    print(f"   Context enriched: {'Prior Lessons' in result_2.enriched_context}")
    print()
    
    print("📍 S - SPAR: Deliberation complete")
    print(f"   Recommendation: {spar_output_2['synthesis']['recommendation']}")
    print(f"   Confidence: {spar_output_2['synthesis']['confidence']:.0%}")
    print()
    
    print("📍 O - OKAY: Governance gate check")
    print(f"   Result: {result_2.gate_decision.result.value.upper()}")
    print()
    
    # =========================================================================
    # Summary
    # =========================================================================
    
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print()
    print("Cycle 1 (No prior context):")
    print("  • Made decision from scratch")
    print("  • Learned: 'GraphQL migrations take 30% longer than estimated'")
    print()
    print("Cycle 2 (With memory enrichment):")
    print("  • Retrieved lesson from Cycle 1")
    print("  • Context automatically enhanced with prior learning")
    print("  • Better informed decision")
    print()
    print("Memory Stats:", memory.stats())
    print()
    print("🎯 The RESOLVE loop closes: decisions inform future decisions.")
    print("=" * 70)


if __name__ == "__main__":
    run_complete_resolve_cycle()
