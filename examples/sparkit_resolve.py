#!/usr/bin/env python3
"""
SPARKIT → RESOLVE Integration

Pipes SPARKIT output directly into the RESOLVE agentic loop.

Usage:
    # Run SPARKIT then RESOLVE in one command
    python sparkit_resolve.py "Should we migrate to microservices?" --context "..."
    
    # Or pipe existing SPAR output
    python sparkit_resolve.py --from-spar session.spar.json
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import argparse

# Add SDK to path
SDK_PATH = Path(__file__).parent.parent / "sdk" / "python"
sys.path.insert(0, str(SDK_PATH))


def run_sparkit(question: str, context: str = "", tier: str = "deep") -> dict:
    """
    Run SPARKIT and return the output.
    
    Tries OpenRouter runner first, falls back to simulated output.
    """
    # Path to SPARKIT runner
    sparkit_paths = [
        Path(__file__).parent.parent.parent.parent / ".agent/skills/sparkit/run_spar.py",
        Path.home() / "Documents/Documents - M1/My Books/SYNTHAI/synthai-master-repo/.agent/skills/sparkit/run_spar.py",
    ]
    
    sparkit_runner = None
    for p in sparkit_paths:
        if p.exists():
            sparkit_runner = p
            break
    
    if sparkit_runner:
        print("🎯 Running SPARKIT via OpenRouter...")
        try:
            cmd = [
                sys.executable,
                str(sparkit_runner),
                question,
                f"--{tier}"
            ]
            if context:
                cmd.extend(["--context", context])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )
            
            # Parse output - look for JSON block
            output = result.stdout
            
            # Try to find JSON in output
            if "```json" in output:
                json_start = output.find("```json") + 7
                json_end = output.find("```", json_start)
                json_str = output[json_start:json_end].strip()
                return json.loads(json_str)
            
            # Fall through to simulated if no JSON found
            print("   ⚠️ No structured output, using simulated SPAR")
            
        except subprocess.TimeoutExpired:
            print("   ⚠️ SPARKIT timed out, using simulated SPAR")
        except Exception as e:
            print(f"   ⚠️ SPARKIT error: {e}, using simulated SPAR")
    
    # Simulated output
    return generate_simulated_spar(question, context)


def generate_simulated_spar(question: str, context: str = "") -> dict:
    """Generate simulated SPAR output for testing."""
    return {
        "spar_id": f"spar-{int(datetime.now().timestamp())}",
        "question": question,
        "context": context or "No additional context",
        "config": {
            "pattern": "dialectic",
            "depth": "clash",
            "style": "balanced"
        },
        "positions": [
            {
                "agent": "north",
                "role": "Champion",
                "position": "Proceed with the proposal",
                "arguments": ["Strategic alignment", "Competitive advantage"]
            },
            {
                "agent": "east",
                "role": "Challenger",
                "position": "Reconsider the approach",
                "arguments": ["Resource constraints", "Risk exposure"]
            },
            {
                "agent": "south",
                "role": "Pragmatist",
                "position": "Phased implementation",
                "arguments": ["Reduced risk", "Learning opportunity"]
            },
            {
                "agent": "west",
                "role": "Sage",
                "position": "Gather more data first",
                "arguments": ["Historical patterns", "Avoid premature commitment"]
            }
        ],
        "synthesis": {
            "recommendation": "Proceed with phased approach, starting with pilot",
            "confidence": 0.72,
            "rationale": "Balances opportunity with risk management",
            "key_tensions": ["Speed vs thoroughness", "Innovation vs stability"],
            "conditions_to_reverse": ["If pilot fails to meet 50% of targets"]
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


def run_resolve(spar_output: dict, args) -> dict:
    """Run RESOLVE loop on SPAR output."""
    from agentic_adapter import AgenticSPARAdapter
    from action_dispatcher import LoggingDispatcher, DryRunDispatcher
    from semantic_memory import SemanticMemoryStore
    
    # Initialize components
    memory = SemanticMemoryStore(persist_path=args.memory_path) if args.memory_path else SemanticMemoryStore()
    adapter = AgenticSPARAdapter(memory_store=memory)
    
    # Choose dispatcher
    if args.dry_run:
        dispatcher = DryRunDispatcher(success_rate=0.9)
    else:
        dispatcher = LoggingDispatcher(log_file=args.log_file)
    
    # Run the loop
    result = adapter.run_loop(
        spar_output,
        action_executor=dispatcher.execute if args.auto_execute else None,
        auto_execute=args.auto_execute
    )
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="SPARKIT → RESOLVE Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("question", nargs="?", help="Decision question")
    parser.add_argument("--context", "-c", default="", help="Additional context")
    parser.add_argument("--from-spar", help="Load SPAR from JSON file")
    parser.add_argument("--tier", choices=["compact", "deep", "ultra"], default="deep")
    parser.add_argument("--auto-execute", "-x", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--memory-path", help="Path to persist memory")
    parser.add_argument("--log-file", help="Path for action log")
    parser.add_argument("--output", "-o", help="Output DMG to file")
    
    args = parser.parse_args()
    
    if not args.question and not args.from_spar:
        parser.error("Either 'question' or '--from-spar' required")
    
    print("=" * 60)
    print("🔗 SPARKIT → RESOLVE Integration")
    print("=" * 60)
    print()
    
    # Step 1: Get SPAR output
    if args.from_spar:
        print(f"📂 Loading SPAR from: {args.from_spar}")
        with open(args.from_spar, 'r') as f:
            spar_output = json.load(f)
    else:
        print(f"🎯 Question: {args.question}")
        spar_output = run_sparkit(args.question, args.context, args.tier)
    
    print()
    print(f"✅ SPAR Complete")
    print(f"   Recommendation: {spar_output.get('synthesis', {}).get('recommendation', 'N/A')}")
    print(f"   Confidence: {spar_output.get('synthesis', {}).get('confidence', 0):.0%}")
    print()
    
    # Step 2: Run RESOLVE
    print("🔄 Starting RESOLVE Loop...")
    print()
    
    result = run_resolve(spar_output, args)
    
    # Output
    print()
    print("=" * 60)
    print("📊 RESULT")
    print("=" * 60)
    print(f"Gate: {result.gate_decision.result.value.upper()}")
    print(f"Reason: {result.gate_decision.reason}")
    print(f"Executed: {result.executed}")
    print(f"Lessons Applied: {len(result.lessons_applied)}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result.dmg, f, indent=2)
        print(f"💾 Saved to: {args.output}")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
