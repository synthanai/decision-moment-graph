#!/usr/bin/env python3
"""
DMG Lifecycle CLI

Command-line interface for running the DMG Lifecycle:
FRAME → TRACE → SPAR → RAMP → COMMIT → OUTCOME

Usage:
    dmg lifecycle "Should we migrate to microservices?" --context "5-year monolith"
    dmg lifecycle "Question" --auto-execute --dispatcher logging
    dmg lifecycle "Question" --dry-run
    dmg lifecycle --from-spar output.spar.json
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add SDK to path
SDK_PATH = Path(__file__).parent.parent / "sdk" / "python"
if str(SDK_PATH) not in sys.path:
    sys.path.insert(0, str(SDK_PATH))


def lifecycle_command(args):
    """Execute the DMG Lifecycle: FRAME → TRACE → SPAR → RAMP → COMMIT → OUTCOME."""
    
    # Import adapters
    try:
        from agentic_adapter import AgenticSPARAdapter, Observation
        from action_dispatcher import (
            LoggingDispatcher, DryRunDispatcher, HttpDispatcher,
            create_dispatcher
        )
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running from the dmg-open-standard directory")
        sys.exit(1)
    
    # Initialize adapter
    adapter = AgenticSPARAdapter()
    
    # Load SPAR output
    if args.from_spar:
        print(f"📂 Loading SPAR from: {args.from_spar}")
        with open(args.from_spar, 'r') as f:
            spar_output = json.load(f)
    else:
        # Generate simulated SPAR output for the question
        spar_output = generate_spar_output(args.question, args.context)
    
    print()
    print("=" * 60)
    print("🔄 DMG LIFECYCLE")
    print("   FRAME → TRACE → SPAR → RAMP → COMMIT → OUTCOME")
    print("=" * 60)
    print()
    
    # Phase 1: FRAME
    print("📍 Phase 1: FRAME — Structure question & options")
    print(f"   Question: {spar_output.get('question', 'N/A')}")
    print(f"   Context: {spar_output.get('context', 'N/A')[:80]}...")
    print()
    
    # Phase 2: TRACE
    print("📍 Phase 2: TRACE — Retrieve prior decisions & evidence")
    
    # Phase 3: SPAR
    print("📍 Phase 3: SPAR — Run structured deliberation")
    synthesis = spar_output.get('synthesis', {})
    print(f"   Recommendation: {synthesis.get('recommendation', 'N/A')}")
    print(f"   Confidence: {synthesis.get('confidence', 0):.0%}")
    print()
    
    # Create dispatcher
    if args.dry_run:
        dispatcher = DryRunDispatcher(success_rate=args.success_rate)
        print("   Dispatcher: DRY RUN MODE")
    elif args.dispatcher == "http" and args.target_url:
        dispatcher = HttpDispatcher(base_url=args.target_url)
        print(f"   Dispatcher: HTTP → {args.target_url}")
    else:
        dispatcher = LoggingDispatcher(log_file=args.log_file)
        print(f"   Dispatcher: Logging" + (f" → {args.log_file}" if args.log_file else ""))
    print()
    
    # Run the loop
    result = adapter.run_loop(
        spar_output,
        action_executor=dispatcher.execute if args.auto_execute else None,
        auto_execute=args.auto_execute
    )
    
    # Phase 4: RAMP
    print("📍 Phase 4: RAMP — Governance gate (RAMP/DOORS)")
    gate = result.gate_decision
    if gate.result.value == "approved":
        print(f"   ✅ APPROVED: {gate.reason}")
    elif gate.result.value == "escalate_human":
        print(f"   ⚠️  ESCALATE: {gate.reason}")
    else:
        print(f"   🚫 BLOCKED: {gate.reason}")
    
    if gate.required_actions:
        print("   Required Actions:")
        for action in gate.required_actions:
            print(f"      • {action}")
    print()
    
    # Phase 5: COMMIT
    print("📍 Phase 5: COMMIT — Finalize & execute")
    if result.executed:
        print(f"   ✅ Executed: {result.observation.summary}")
        print(f"   Duration: {result.observation.duration_ms}ms")
    else:
        print(f"   ⏸️  Not executed (auto_execute={args.auto_execute})")
    print()
    
    # Phase 6: OUTCOME
    print("📍 Phase 6: OUTCOME — Verify predictions vs reality")
    if result.observation:
        print(f"   Success: {result.observation.success}")
        print(f"   Metrics: {result.observation.metrics}")
    else:
        print("   (Awaiting execution)")
    print()
    
    # MERIT Check
    print("📊 MERIT Score")
    dmg = result.dmg
    merit_score = dmg.get("merit_score", "N/A")
    print(f"   Score: {merit_score}/5")
    print(f"   DMG Version: {dmg.get('dmg_version', '0.1')}")
    
    # Lessons applied
    if result.lessons_applied:
        print(f"   Lessons Applied: {len(result.lessons_applied)}")
        for lesson in result.lessons_applied[:3]:
            print(f"      • {lesson[:60]}...")
    print()
    
    # Output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(dmg, f, indent=2)
        print(f"💾 DMG saved to: {output_path}")
    
    print("=" * 60)
    print("✅ LIFECYCLE COMPLETE")
    print("=" * 60)
    
    return result


def generate_spar_output(question: str, context: str = "") -> dict:
    """
    Generate a simulated SPAR output for testing.
    
    In production, this would come from run_spar.py or a real SPAR session.
    """
    return {
        "spar_id": f"spar-{int(datetime.now().timestamp())}",
        "question": question,
        "context": context or "No additional context provided",
        "config": {
            "pattern": "dialectic",
            "depth": "clash",
            "style": "balanced"
        },
        "positions": [
            {
                "agent": "north",
                "role": "Champion",
                "position": f"Yes, we should proceed with this decision",
                "arguments": ["Aligns with strategic goals", "Manageable risk profile"]
            },
            {
                "agent": "east",
                "role": "Challenger",
                "position": "We should reconsider the timeline",
                "arguments": ["Resource constraints", "Market uncertainty"]
            },
            {
                "agent": "south",
                "role": "Pragmatist",
                "position": "Phased approach recommended",
                "arguments": ["Reduces risk", "Allows learning"]
            },
            {
                "agent": "west",
                "role": "Sage",
                "position": "Historical patterns suggest caution",
                "arguments": ["Similar initiatives have failed", "Need more data"]
            }
        ],
        "synthesis": {
            "recommendation": "Proceed with phased implementation",
            "confidence": 0.72,
            "rationale": "Balances speed with risk management",
            "key_tensions": ["Timeline vs thoroughness", "Investment vs uncertainty"],
            "conditions_to_reverse": ["If Phase 1 results are below 50% of target"]
        },
        "transcript": [],
        "probe": {
            "plurality": 8,
            "rigor": 7,
            "origin": 8,
            "basis": 7,
            "execution": 8
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="DMG Lifecycle CLI - FRAME → TRACE → SPAR → RAMP → COMMIT → OUTCOME",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dmg lifecycle "Should we migrate to microservices?"
  dmg lifecycle "Question" --context "We have 5 engineers, $50k budget"
  dmg lifecycle "Question" --auto-execute --dry-run
  dmg lifecycle --from-spar session.spar.json --output decision.dmg.json
        """
    )
    
    # Question input
    parser.add_argument(
        "question",
        nargs="?",
        help="The decision question to process through the DMG Lifecycle"
    )
    
    parser.add_argument(
        "--context", "-c",
        default="",
        help="Additional context for the decision"
    )
    
    parser.add_argument(
        "--from-spar",
        help="Load SPAR output from JSON file instead of generating"
    )
    
    # Execution options
    parser.add_argument(
        "--auto-execute", "-x",
        action="store_true",
        help="Automatically execute if governance approves"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate execution without side effects"
    )
    
    parser.add_argument(
        "--success-rate",
        type=float,
        default=1.0,
        help="Success rate for dry-run simulation (0.0-1.0)"
    )
    
    # Dispatcher options
    parser.add_argument(
        "--dispatcher", "-d",
        choices=["logging", "http", "dry_run"],
        default="logging",
        help="Action dispatcher type"
    )
    
    parser.add_argument(
        "--target-url",
        help="Target URL for HTTP dispatcher"
    )
    
    parser.add_argument(
        "--log-file",
        help="Log file for logging dispatcher"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        help="Output path for DMG JSON file"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not args.question and not args.from_spar:
        parser.error("Either 'question' or '--from-spar' is required")
    
    try:
        lifecycle_command(args)
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
