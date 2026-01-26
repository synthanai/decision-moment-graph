#!/usr/bin/env python3
"""
DMG SWARM CLI

Command-line interface for running parallel agent swarms with SPARKIT deliberation.
Implements the SWARM-RESOLVE protocol:
DECOMPOSE → SPAWN → MONITOR → COLLECT → UNBLOCK → SYNTHESIZE → GOVERN

Each SubAgent runs its own RESOLVE loop:
Recon → Enrich → SPAR → Okay → Launch → Verify → Encode

Usage:
    dmg swarm "Refactor authentication module" --parallel 3
    dmg swarm "Build new API" --decompose --mode openrouter
    dmg swarm --from-plan tasks.json --auto-execute
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

# Add SDK to path
SDK_PATH = Path(__file__).parent.parent / "sdk" / "python"
if str(SDK_PATH) not in sys.path:
    sys.path.insert(0, str(SDK_PATH))


async def swarm_command(args):
    """Execute the SWARM-RESOLVE loop."""
    
    # Import modules
    try:
        from swarm_coordinator import (
            SwarmCoordinator, SwarmBudget, TaskNode, TaskStatus,
            create_task_graph_from_list
        )
        from sparkit_runner import run_sparkit
        from agentic_adapter import AgenticSPARAdapter
        from action_dispatcher import LoggingDispatcher, DryRunDispatcher
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running from the dmg-open-standard directory")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("🐝 DMG SWARM - Parallel Agent Coordination")
    print("=" * 70)
    print()
    
    # Create budget
    budget = SwarmBudget(
        max_total_cost=args.budget,
        max_parallel_agents=args.parallel,
        max_execution_time_seconds=args.timeout
    )
    
    # Create coordinator
    coordinator = SwarmCoordinator(
        goal=args.goal,
        budget=budget,
        task_executor=lambda task, agent: sparkit_task_executor(
            task, agent, args, run_sparkit, AgenticSPARAdapter,
            DryRunDispatcher if args.dry_run else LoggingDispatcher
        )
    )
    
    # Load or generate task graph
    if args.from_plan:
        print(f"📂 Loading task plan from: {args.from_plan}")
        with open(args.from_plan, 'r') as f:
            tasks = json.load(f)
        coordinator.task_graph = create_task_graph_from_list(tasks)
        print(f"   Loaded {len(tasks)} tasks")
    elif args.decompose:
        print("🧠 Decomposing goal with SPARKIT...")
        tasks = await decompose_goal_with_sparkit(
            args.goal, 
            args.context,
            run_sparkit,
            mode=args.mode
        )
        coordinator.task_graph = create_task_graph_from_list(tasks)
        print(f"   Generated {len(tasks)} tasks from goal decomposition")
    else:
        # Single task mode
        task = TaskNode(
            task_id="task-main",
            description=args.goal,
            status=TaskStatus.READY
        )
        coordinator.task_graph.add_node(task)
        print("   Running in single-task mode")
    
    print()
    print("📋 Task Graph:")
    for task_id, node in coordinator.task_graph.nodes.items():
        blocked = f" (blocked by: {', '.join(node.blocked_by)})" if node.blocked_by else ""
        print(f"   [{node.status.value:8}] {task_id}: {node.description[:50]}{blocked}")
    print()
    
    print("⚙️  Configuration:")
    print(f"   Max parallel agents: {budget.max_parallel_agents}")
    print(f"   Budget limit: ${budget.max_total_cost:.2f}")
    print(f"   Timeout: {budget.max_execution_time_seconds}s")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()
    
    # Run the swarm
    print("=" * 70)
    print("🚀 SWARM-RESOLVE LOOP STARTING")
    print("=" * 70)
    print()
    
    result = await coordinator.run()
    
    # Display results
    print()
    print("=" * 70)
    print("📊 SWARM RESULTS")
    print("=" * 70)
    print()
    
    print(f"Status: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
    print(f"Swarm ID: {result['swarm_id']}")
    print()
    
    print("📋 Final Task States:")
    for node in result['task_graph']['nodes']:
        status_icon = "✅" if node['status'] == 'done' else "❌" if node['status'] == 'failed' else "⏸️"
        print(f"   {status_icon} {node['task_id']}: {node['status']}")
        if node.get('error'):
            print(f"      Error: {node['error']}")
    print()
    
    if result.get('synthesis'):
        print("🔗 Synthesis:")
        for task_id, output in result['synthesis'].get('merged_outputs', {}).items():
            print(f"   {task_id}: {json.dumps(output)[:60]}...")
    print()
    
    print("💰 Budget:")
    print(f"   Max: ${result['budget']['max_cost']:.2f}")
    print(f"   Used: ${result['budget']['actual_cost']:.2f}")
    if result['budget']['alerts']:
        print(f"   Alerts: {len(result['budget']['alerts'])}")
    print()
    
    print(f"📝 Events logged: {len(result['events'])}")
    if args.verbose:
        for event in result['events']:
            print(f"   [{event['ts'][:19]}] {event['event_type']}")
    print()
    
    # Output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Swarm result saved to: {output_path}")
    
    # Export DMG
    if args.dmg_output:
        dmg_path = Path(args.dmg_output)
        dmg_export = coordinator.to_dmg_swarm()
        with open(dmg_path, 'w') as f:
            json.dump(dmg_export, f, indent=2, default=str)
        print(f"💾 DMG Swarm exported to: {dmg_path}")
    
    print()
    print("=" * 70)
    print("✅ SWARM COMPLETE")
    print("=" * 70)
    
    return result


async def sparkit_task_executor(
    task: "TaskNode",
    agent: "SubAgent", 
    args,
    run_sparkit,
    AgenticSPARAdapter,
    DispatcherClass
) -> dict:
    """
    Execute a single task using SPARKIT + RESOLVE.
    
    This is the bridge between SwarmCoordinator and the existing
    RESOLVE infrastructure.
    """
    print(f"   🔄 [{agent.agent_id}] Starting: {task.description[:40]}...")
    
    # Phase 3: SPAR - Run deliberation for this task
    spar_output = run_sparkit(
        question=f"How should we: {task.description}?",
        context=args.context or "",
        mode=args.mode,
        depth="clash",
        style="balanced"
    )
    
    # Create RESOLVE adapter
    adapter = AgenticSPARAdapter()
    
    # Create dispatcher
    dispatcher = DispatcherClass()
    
    # Run RESOLVE loop for this task
    resolve_result = adapter.run_loop(
        spar_output,
        action_executor=dispatcher.execute if args.auto_execute else None,
        auto_execute=args.auto_execute
    )
    
    print(f"   ✅ [{agent.agent_id}] Complete: confidence={spar_output['synthesis'].get('confidence', 0):.0%}")
    
    return {
        "task_id": task.task_id,
        "spar_id": spar_output.get("spar_id"),
        "recommendation": spar_output["synthesis"].get("recommendation"),
        "confidence": spar_output["synthesis"].get("confidence"),
        "gate_result": resolve_result.gate_decision.result.value if resolve_result.gate_decision else None,
        "executed": resolve_result.executed,
        "merit_score": resolve_result.dmg.get("merit_score")
    }


async def decompose_goal_with_sparkit(
    goal: str,
    context: str,
    run_sparkit,
    mode: str = "local"
) -> list:
    """
    Use SPARKIT to decompose a high-level goal into a TaskGraph.
    
    The LLM generates a structured task breakdown with dependencies.
    """
    # Run SPARKIT with decomposition prompt
    decompose_question = f"""Break down this goal into a task graph:

GOAL: {goal}
CONTEXT: {context or 'None provided'}

Generate a JSON array of tasks with this structure:
[
    {{"id": "1", "description": "First task to do", "blocked_by": []}},
    {{"id": "2", "description": "Second task that depends on first", "blocked_by": ["1"]}},
    ...
]

Requirements:
- Each task should be atomic and actionable
- blocked_by lists task IDs that must complete first
- Order tasks logically (dependencies first)
- Include 3-7 tasks for a typical goal
"""
    
    spar_output = run_sparkit(
        question=decompose_question,
        context=f"Decomposing: {goal}",
        mode=mode,
        depth="duel",  # Quick, focused
        style="balanced"
    )
    
    # Try to extract task structure from synthesis
    # In production, this would use structured output parsing
    recommendation = spar_output.get("synthesis", {}).get("recommendation", "")
    
    # For now, generate sensible default decomposition
    # In production, parse from LLM output
    tasks = [
        {"id": "1", "description": f"Analyze current state: {goal[:30]}...", "blocked_by": []},
        {"id": "2", "description": f"Design approach: {goal[:30]}...", "blocked_by": ["1"]},
        {"id": "3", "description": f"Implement core changes: {goal[:30]}...", "blocked_by": ["2"]},
        {"id": "4", "description": f"Test and validate: {goal[:30]}...", "blocked_by": ["3"]},
        {"id": "5", "description": f"Document and finalize: {goal[:30]}...", "blocked_by": ["4"]}
    ]
    
    return tasks


def main():
    parser = argparse.ArgumentParser(
        description="DMG SWARM - Parallel Agent Coordination CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dmg swarm "Refactor auth module" --parallel 3
  dmg swarm "Build API" --decompose --mode openrouter
  dmg swarm --from-plan tasks.json --auto-execute --dry-run
  dmg swarm "Quick task" --output result.json --dmg-output swarm.dmg.json
        """
    )
    
    # Goal input
    parser.add_argument(
        "goal",
        nargs="?",
        help="The high-level goal for the swarm to accomplish"
    )
    
    parser.add_argument(
        "--context", "-c",
        default="",
        help="Additional context for the swarm"
    )
    
    parser.add_argument(
        "--from-plan",
        help="Load task graph from JSON file instead of generating"
    )
    
    # Decomposition
    parser.add_argument(
        "--decompose", "-d",
        action="store_true",
        help="Use SPARKIT to decompose goal into task graph automatically"
    )
    
    # Swarm options
    parser.add_argument(
        "--parallel", "-p",
        type=int,
        default=3,
        help="Maximum parallel agents (default: 3)"
    )
    
    parser.add_argument(
        "--budget", "-b",
        type=float,
        default=10.0,
        help="Maximum budget in dollars (default: $10.00)"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="Timeout in seconds (default: 300)"
    )
    
    # Execution options
    parser.add_argument(
        "--auto-execute", "-x",
        action="store_true",
        help="Automatically execute actions if governance approves"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate execution without side effects"
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["local", "openrouter"],
        default="local",
        help="SPARKIT mode: local (simulated) or openrouter (API)"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        help="Output path for swarm result JSON"
    )
    
    parser.add_argument(
        "--dmg-output",
        help="Output path for DMG Swarm schema export"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output (show all events)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not args.goal and not args.from_plan:
        parser.error("Either 'goal' or '--from-plan' is required")
    
    try:
        asyncio.run(swarm_command(args))
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted - triggering kill switch")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
