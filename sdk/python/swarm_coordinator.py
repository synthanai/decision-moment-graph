#!/usr/bin/env python3
"""
DMG Swarm Coordinator

Implements the SWARM-RESOLVE protocol for parallel agent coordination:
DECOMPOSE → SPAWN → MONITOR → COLLECT → UNBLOCK → SYNTHESIZE → GOVERN

This module wraps the existing RESOLVE loop, enabling parallel sub-agent
execution with TaskGraph dependency enforcement.

Usage:
    from sdk.python.swarm_coordinator import SwarmCoordinator
    
    coordinator = SwarmCoordinator(goal="Refactor auth module")
    result = await coordinator.run()
"""

import logging
import json
import time
import asyncio
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import uuid
from dataclasses import dataclass, field
from enum import Enum

# Use agentic-kit primitives
from agentic_kit.memory import SemanticMemoryStore
from agentic_kit.dispatchers import (
    CompositeDispatcher, 
    LoggingDispatcher, 
    DryRunDispatcher, 
    create_dispatcher,
    Action,
    ActionType
)
from agentic_kit.circuit_breaker import CircuitBreaker, CircuitBreakerOpen
from agentic_kit.reflection import ReflectionLoop, ReflectionResult


# ============================================================================
# Enums
# ============================================================================

class TaskStatus(Enum):
    BLOCKED = "blocked"
    READY = "ready"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


class SubAgentStatus(Enum):
    SPAWNED = "spawned"
    WORKING = "working"
    DONE = "done"
    FAILED = "failed"
    TERMINATED = "terminated"


class SwarmStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    TERMINATED = "terminated"


class EdgeType(Enum):
    BLOCKS = "blocks"      # Hard dependency
    INFORMS = "informs"    # Soft (output shared but not required)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class TaskNode:
    """Single unit of work in the task graph."""
    task_id: str
    description: str
    status: TaskStatus = TaskStatus.BLOCKED
    blocked_by: list[str] = field(default_factory=list)
    agent_id: Optional[str] = None
    dmg_moment_id: Optional[str] = None
    output: Any = None
    error: Optional[str] = None
    priority: int = 3
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class TaskEdge:
    """Dependency relationship between tasks."""
    from_task: str
    to_task: str
    edge_type: EdgeType = EdgeType.BLOCKS


@dataclass
class TaskGraph:
    """Directed acyclic graph of work items."""
    nodes: dict[str, TaskNode] = field(default_factory=dict)
    edges: list[TaskEdge] = field(default_factory=list)
    
    def add_node(self, node: TaskNode) -> None:
        self.nodes[node.task_id] = node
    
    def add_edge(self, from_task: str, to_task: str, edge_type: EdgeType = EdgeType.BLOCKS) -> None:
        self.edges.append(TaskEdge(from_task, to_task, edge_type))
        if edge_type == EdgeType.BLOCKS:
            self.nodes[to_task].blocked_by.append(from_task)
            self.nodes[to_task].status = TaskStatus.BLOCKED
    
    def get_ready_tasks(self) -> list[TaskNode]:
        """Return tasks that have no unfinished blockers."""
        ready = []
        for node in self.nodes.values():
            if node.status in (TaskStatus.DONE, TaskStatus.FAILED, TaskStatus.SKIPPED, TaskStatus.RUNNING):
                continue
            blockers_done = all(
                self.nodes[b].status == TaskStatus.DONE 
                for b in node.blocked_by
            )
            if blockers_done:
                node.status = TaskStatus.READY
                ready.append(node)
        return ready
    
    def is_complete(self) -> bool:
        """Check if all tasks are done, failed, or skipped."""
        return all(
            n.status in (TaskStatus.DONE, TaskStatus.FAILED, TaskStatus.SKIPPED)
            for n in self.nodes.values()
        )
    
    def to_dict(self) -> dict:
        """Serialize for DMG storage."""
        return {
            "nodes": [
                {
                    "task_id": n.task_id,
                    "description": n.description,
                    "status": n.status.value,
                    "blocked_by": n.blocked_by,
                    "agent_id": n.agent_id,
                    "dmg_moment_id": n.dmg_moment_id,
                    "output": n.output,
                    "error": n.error,
                    "priority": n.priority,
                    "started_at": n.started_at.isoformat() if n.started_at else None,
                    "completed_at": n.completed_at.isoformat() if n.completed_at else None
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {"from_task": e.from_task, "to_task": e.to_task, "type": e.edge_type.value}
                for e in self.edges
            ]
        }


@dataclass
class SubAgent:
    """Isolated execution context for parallel work."""
    agent_id: str
    task_id: str
    depth: int = 0
    status: SubAgentStatus = SubAgentStatus.SPAWNED
    parent_agent_id: Optional[str] = None
    permissions: list[str] = field(default_factory=lambda: ["read_memory", "execute_action"])
    model_tier: str = "comprehensive"
    context_summary: Optional[str] = None
    spawned_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class SwarmBudget:
    """Resource constraints (INV-SWARM-02)."""
    max_total_cost: float = 10.0
    max_parallel_agents: int = 5
    max_execution_time_seconds: int = 300
    max_depth: int = 3  # INV-SWARM-01
    current_cost: float = 0.0
    alerts: list[dict] = field(default_factory=list)
    
    def check_budget(self) -> tuple[bool, Optional[str]]:
        """Check if budget constraints are violated."""
        if self.current_cost >= self.max_total_cost:
            return False, f"Budget exceeded: ${self.current_cost:.2f} >= ${self.max_total_cost:.2f}"
        return True, None
    
    def add_cost(self, cost: float) -> None:
        self.current_cost += cost
        # Check alert thresholds
        for threshold in [50, 75, 90]:
            pct = (self.current_cost / self.max_total_cost) * 100
            if pct >= threshold and not any(a.get("threshold_percent") == threshold for a in self.alerts):
                self.alerts.append({
                    "threshold_percent": threshold,
                    "triggered": True,
                    "triggered_at": datetime.now().isoformat()
                })


# ============================================================================
# Swarm Coordinator
# ============================================================================

class SwarmCoordinator:
    """
    Orchestrates SWARM-RESOLVE protocol.
    
    Wraps the existing RESOLVE loop for parallel sub-agent execution.
    """
    
    # Invariants (INV-SWARM-*)
    MAX_DEPTH = 3           # INV-SWARM-01
    KILL_SWITCH_TIMEOUT = 5 # INV-SWARM-04: terminate all within 5s
    
    def __init__(
        self,
        goal: str,
        parent_moment_id: Optional[str] = None,
        budget: Optional[SwarmBudget] = None,
        task_executor: Optional[Callable] = None
    ):
        self.swarm_id = f"swarm-{uuid.uuid4().hex[:12]}"
        self.goal = goal
        self.parent_moment_id = parent_moment_id
        self.budget = budget or SwarmBudget()
        self.task_executor = task_executor or self._default_executor
        
        self.task_graph = TaskGraph()
        self.sub_agents: dict[str, SubAgent] = {}
        self.status = SwarmStatus.PENDING
        self.events: list[dict] = []
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        
        self._kill_switch_triggered = False
        self._active_tasks: set[str] = set()
    
    # -------------------------------------------------------------------------
    # SWARM-RESOLVE Protocol
    # -------------------------------------------------------------------------
    
    async def run(self) -> dict:
        """Execute full SWARM-RESOLVE loop."""
        try:
            self.status = SwarmStatus.RUNNING
            self._log_event("SWARM_SPAWNED", payload={"goal": self.goal})
            
            # Phase 1: DECOMPOSE
            await self._decompose()
            
            # Phase 2-5: SPAWN → MONITOR → COLLECT → UNBLOCK (loop)
            while not self.task_graph.is_complete():
                # Check kill switch
                if self._kill_switch_triggered:
                    await self._terminate_all()
                    return self._build_result(success=False, reason="Kill switch triggered")
                
                # Check budget
                ok, reason = self.budget.check_budget()
                if not ok:
                    self._log_event("BUDGET_ALERT", payload={"reason": reason})
                    await self._terminate_all()
                    return self._build_result(success=False, reason=reason)
                
                # Get ready tasks
                ready_tasks = self.task_graph.get_ready_tasks()
                if not ready_tasks:
                    # All tasks blocked or running - wait
                    await asyncio.sleep(0.1)
                    continue
                
                # Limit parallel agents
                available_slots = self.budget.max_parallel_agents - len(self._active_tasks)
                tasks_to_run = ready_tasks[:available_slots]
                
                # SPAWN: Create sub-agents for ready tasks
                spawn_tasks = [self._spawn_and_run(task) for task in tasks_to_run]
                await asyncio.gather(*spawn_tasks, return_exceptions=True)
            
            # Phase 6: SYNTHESIZE
            synthesis = await self._synthesize()
            
            # Phase 7: GOVERN
            governed_result = await self._govern(synthesis)
            
            self.status = SwarmStatus.COMPLETE
            self.completed_at = datetime.now()
            self._log_event("SWARM_COMPLETED")
            
            return self._build_result(success=True, synthesis=governed_result)
            
        except Exception as e:
            self.status = SwarmStatus.FAILED
            self._log_event("SWARM_TERMINATED", payload={"error": str(e)})
            return self._build_result(success=False, reason=str(e))
    
    async def _decompose(self) -> None:
        """Phase 1: Break goal into TaskGraph."""
        # Default: single task (override in subclass for real decomposition)
        task = TaskNode(
            task_id=f"task-{uuid.uuid4().hex[:8]}",
            description=self.goal,
            status=TaskStatus.READY
        )
        self.task_graph.add_node(task)
        self._log_event("SWARM_DECOMPOSED", payload={"task_count": len(self.task_graph.nodes)})
    
    async def _spawn_and_run(self, task: TaskNode) -> None:
        """Spawn a SubAgent and run the task."""
        # Mark as running
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        self._active_tasks.add(task.task_id)
        
        # Create SubAgent
        agent = SubAgent(
            agent_id=f"agent-{uuid.uuid4().hex[:8]}",
            task_id=task.task_id,
            depth=0  # Coordinator spawns at depth 0
        )
        task.agent_id = agent.agent_id
        self.sub_agents[agent.agent_id] = agent
        self._log_event("SUBAGENT_SPAWNED", task_id=task.task_id, agent_id=agent.agent_id)
        
        try:
            # Execute task (this would call RESOLVE loop)
            agent.status = SubAgentStatus.WORKING
            result = await self.task_executor(task, agent)
            
            # Collect result
            task.output = result
            task.status = TaskStatus.DONE
            task.completed_at = datetime.now()
            agent.status = SubAgentStatus.DONE
            agent.completed_at = datetime.now()
            
            self._log_event("TASK_COMPLETED", task_id=task.task_id, agent_id=agent.agent_id)
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            agent.status = SubAgentStatus.FAILED
            
            self._log_event("TASK_FAILED", task_id=task.task_id, payload={"error": str(e)})
        
        finally:
            self._active_tasks.discard(task.task_id)
    
    async def _synthesize(self) -> dict:
        """Phase 6: Merge outputs from completed tasks."""
        outputs = {
            task_id: node.output 
            for task_id, node in self.task_graph.nodes.items()
            if node.status == TaskStatus.DONE
        }
        self._log_event("SWARM_SYNTHESIZED", payload={"output_count": len(outputs)})
        return {"merged_outputs": outputs}
    
    async def _govern(self, synthesis: dict) -> dict:
        """Phase 7: Apply RAMP checks to final synthesis."""
        # INV-SWARM-07: RAMP 4+ decisions escalate to coordinator
        # Default: pass through (override for real governance)
        return synthesis
    
    # -------------------------------------------------------------------------
    # Kill Switch (INV-SWARM-04)
    # -------------------------------------------------------------------------
    
    def trigger_kill_switch(self) -> None:
        """Emergency stop for all sub-agents."""
        self._kill_switch_triggered = True
    
    async def _terminate_all(self) -> None:
        """Terminate all active sub-agents within 5 seconds."""
        self._log_event("SWARM_TERMINATED", payload={"reason": "kill_switch"})
        self.status = SwarmStatus.TERMINATED
        
        # Mark all running tasks as failed
        for task in self.task_graph.nodes.values():
            if task.status == TaskStatus.RUNNING:
                task.status = TaskStatus.FAILED
                task.error = "Terminated by kill switch"
        
        # Mark all agents as terminated
        for agent in self.sub_agents.values():
            if agent.status in (SubAgentStatus.SPAWNED, SubAgentStatus.WORKING):
                agent.status = SubAgentStatus.TERMINATED
    
    # -------------------------------------------------------------------------
    # Default Executor (stub)
    # -------------------------------------------------------------------------
    
    async def _default_executor(self, task: TaskNode, agent: SubAgent) -> dict:
        """
        Default task executor (stub).
        
        In production, this would:
        1. Run RESOLVE loop for this task
        2. Create DMG MOMENT
        3. Return structured result
        """
        # Simulate work
        await asyncio.sleep(0.1)
        return {"status": "completed", "task": task.description}
    
    # -------------------------------------------------------------------------
    # Event Logging (INV-SWARM-05)
    # -------------------------------------------------------------------------
    
    def _log_event(
        self,
        event_type: str,
        task_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        payload: Optional[dict] = None
    ) -> None:
        """Log event for audit trail."""
        event = {
            "event_type": event_type,
            "ts": datetime.now().isoformat(),
            "swarm_id": self.swarm_id,
        }
        if task_id:
            event["task_id"] = task_id
        if agent_id:
            event["agent_id"] = agent_id
        if payload:
            event["payload"] = payload
        self.events.append(event)
    
    # -------------------------------------------------------------------------
    # Serialization
    # -------------------------------------------------------------------------
    
    def _build_result(
        self,
        success: bool,
        synthesis: Optional[dict] = None,
        reason: Optional[str] = None
    ) -> dict:
        """Build final result object."""
        return {
            "swarm_id": self.swarm_id,
            "success": success,
            "status": self.status.value,
            "goal": self.goal,
            "task_graph": self.task_graph.to_dict(),
            "synthesis": synthesis,
            "error": reason,
            "budget": {
                "max_cost": self.budget.max_total_cost,
                "actual_cost": self.budget.current_cost,
                "alerts": self.budget.alerts
            },
            "events": self.events,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def to_dmg_swarm(self) -> dict:
        """Export as DMG Swarm schema-compliant object."""
        return {
            "swarm_id": self.swarm_id,
            "parent_moment_id": self.parent_moment_id,
            "root_goal": self.goal,
            "task_graph": self.task_graph.to_dict(),
            "sub_agents": [
                {
                    "agent_id": a.agent_id,
                    "task_id": a.task_id,
                    "depth": a.depth,
                    "status": a.status.value,
                    "parent_agent_id": a.parent_agent_id,
                    "permissions": a.permissions,
                    "spawned_at": a.spawned_at.isoformat(),
                    "completed_at": a.completed_at.isoformat() if a.completed_at else None
                }
                for a in self.sub_agents.values()
            ],
            "status": self.status.value,
            "budget": {
                "max_total_cost": self.budget.max_total_cost,
                "max_parallel_agents": self.budget.max_parallel_agents,
                "max_execution_time_seconds": self.budget.max_execution_time_seconds,
                "current_cost": self.budget.current_cost,
                "alerts": self.budget.alerts
            },
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


# ============================================================================
# Convenience Functions
# ============================================================================

def create_task_graph_from_list(tasks: list[dict]) -> TaskGraph:
    """
    Create TaskGraph from a simple list of task definitions.
    
    Example:
        tasks = [
            {"id": "1", "description": "Setup auth", "blocked_by": []},
            {"id": "2", "description": "Implement JWT", "blocked_by": ["1"]},
            {"id": "3", "description": "Add tests", "blocked_by": ["2"]}
        ]
    """
    graph = TaskGraph()
    
    # First pass: create all nodes
    for t in tasks:
        node = TaskNode(
            task_id=t["id"],
            description=t["description"],
            status=TaskStatus.READY if not t.get("blocked_by") else TaskStatus.BLOCKED,
            blocked_by=t.get("blocked_by", []),
            priority=t.get("priority", 3)
        )
        graph.add_node(node)
    
    # Second pass: create edges
    for t in tasks:
        for blocker in t.get("blocked_by", []):
            graph.edges.append(TaskEdge(blocker, t["id"], EdgeType.BLOCKS))
    
    return graph


# ============================================================================
# CLI Entry Point
# ============================================================================

async def main():
    """Example usage."""
    # Create a simple swarm
    coordinator = SwarmCoordinator(
        goal="Refactor authentication module",
        budget=SwarmBudget(max_total_cost=5.0, max_parallel_agents=3)
    )
    
    # Override with a real task graph
    coordinator.task_graph = create_task_graph_from_list([
        {"id": "1", "description": "Analyze current auth implementation"},
        {"id": "2", "description": "Design new JWT structure", "blocked_by": ["1"]},
        {"id": "3", "description": "Implement token service", "blocked_by": ["2"]},
        {"id": "4", "description": "Add refresh token logic", "blocked_by": ["2"]},
        {"id": "5", "description": "Write integration tests", "blocked_by": ["3", "4"]}
    ])
    
    # Run the swarm
    result = await coordinator.run()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
