#!/usr/bin/env python3
"""
Embedded SPARKIT Runner

Lightweight SPARKIT runner for the RESOLVE loop.
Can run locally (simulated) or via OpenRouter API.

Usage:
    from sparkit_runner import run_sparkit
    
    result = run_sparkit(
        question="Should we migrate?",
        context="5-year monolith",
        mode="local"  # or "openrouter"
    )
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class SPARPosition:
    """A position from a SPAR agent."""
    agent: str
    role: str
    position: str
    arguments: List[str] = field(default_factory=list)
    rebuttals: List[str] = field(default_factory=list)


@dataclass
class SPARSynthesis:
    """SPAR synthesis output."""
    recommendation: str
    confidence: float
    rationale: str
    key_tensions: List[str]
    conditions_to_reverse: List[str]


@dataclass
class SPARResult:
    """Complete SPAR session result."""
    spar_id: str
    question: str
    context: str
    positions: List[SPARPosition]
    synthesis: SPARSynthesis
    probe_scores: Dict[str, int]
    config: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "spar_id": self.spar_id,
            "question": self.question,
            "context": self.context,
            "positions": [
                {
                    "agent": p.agent,
                    "role": p.role,
                    "position": p.position,
                    "arguments": p.arguments,
                    "rebuttals": p.rebuttals
                }
                for p in self.positions
            ],
            "synthesis": {
                "recommendation": self.synthesis.recommendation,
                "confidence": self.synthesis.confidence,
                "rationale": self.synthesis.rationale,
                "key_tensions": self.synthesis.key_tensions,
                "conditions_to_reverse": self.synthesis.conditions_to_reverse
            },
            "probe": self.probe_scores,
            "config": self.config,
            "transcript": []
        }


# NEWS Compass Templates
NEWS_TEMPLATES = {
    "north": {
        "role": "Champion",
        "stance": "advocates for",
        "focus": "opportunities and benefits"
    },
    "east": {
        "role": "Challenger", 
        "stance": "challenges",
        "focus": "risks and obstacles"
    },
    "south": {
        "role": "Pragmatist",
        "stance": "seeks practical middle ground on",
        "focus": "feasibility and implementation"
    },
    "west": {
        "role": "Sage",
        "stance": "provides historical perspective on",
        "focus": "patterns and precedents"
    }
}


def run_sparkit(
    question: str,
    context: str = "",
    mode: str = "local",
    depth: str = "clash",  # duel, clash, rumble
    style: str = "balanced",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run SPARKIT deliberation.
    
    Args:
        question: The decision question
        context: Additional context
        mode: "local" (simulated) or "openrouter" (API)
        depth: "duel" (2), "clash" (4), "rumble" (8) agents
        style: balanced, adversarial, steelman, consensus, premortem
        api_key: OpenRouter API key (required for openrouter mode)
    
    Returns:
        SPAR output dictionary ready for AgenticSPARAdapter
    """
    if mode == "openrouter":
        return _run_openrouter(question, context, depth, style, api_key)
    else:
        return _run_local(question, context, depth, style)


def _run_local(
    question: str,
    context: str,
    depth: str,
    style: str
) -> Dict[str, Any]:
    """Run local simulated SPARKIT session."""
    
    # Determine agent count
    agent_count = {"duel": 2, "clash": 4, "rumble": 8}.get(depth, 4)
    
    # Generate positions
    positions = []
    agents = ["north", "east", "south", "west", "ne", "se", "sw", "nw"][:agent_count]
    
    for agent in agents:
        template = NEWS_TEMPLATES.get(agent, NEWS_TEMPLATES["north"])
        positions.append(SPARPosition(
            agent=agent,
            role=template["role"],
            position=f"{template['role']} {template['stance']} this decision",
            arguments=[
                f"Focus on {template['focus']}",
                "Evidence supports this position",
                "Consider the strategic implications"
            ]
        ))
    
    # Generate synthesis
    synthesis = SPARSynthesis(
        recommendation=_generate_recommendation(question, style),
        confidence=_calculate_confidence(style),
        rationale="Balancing multiple perspectives and trade-offs",
        key_tensions=["Speed vs. thoroughness", "Innovation vs. stability"],
        conditions_to_reverse=["If initial metrics fall below 50% of target"]
    )
    
    # Calculate PROBE scores
    probe = {
        "plurality": min(10, agent_count + 5),
        "rigor": 7,
        "origin": 8,
        "basis": 7,
        "execution": 8
    }
    
    result = SPARResult(
        spar_id=f"spar-{int(datetime.now().timestamp())}",
        question=question,
        context=context or "No additional context provided",
        positions=positions,
        synthesis=synthesis,
        probe_scores=probe,
        config={
            "pattern": "dialectic",
            "depth": depth,
            "style": style,
            "mode": "local"
        }
    )
    
    return result.to_dict()


def _run_openrouter(
    question: str,
    context: str,
    depth: str,
    style: str,
    api_key: Optional[str]
) -> Dict[str, Any]:
    """Run SPARKIT via OpenRouter API."""
    
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("⚠️ No OpenRouter API key, falling back to local mode")
        return _run_local(question, context, depth, style)
    
    try:
        import requests
    except ImportError:
        print("⚠️ requests not installed, falling back to local mode")
        return _run_local(question, context, depth, style)
    
    # Build prompt
    prompt = f"""You are running a SPARKIT deliberation session.

Question: {question}
Context: {context}
Depth: {depth}
Style: {style}

Generate a structured multi-agent debate with:
1. Positions from each agent (NEWS compass)
2. Synthesis with recommendation and confidence
3. Key tensions and conditions to reverse

Output as JSON matching this schema:
{{
    "positions": [
        {{"agent": "north", "role": "Champion", "position": "...", "arguments": [...]}}
    ],
    "synthesis": {{
        "recommendation": "...",
        "confidence": 0.0-1.0,
        "rationale": "...",
        "key_tensions": [...],
        "conditions_to_reverse": [...]
    }}
}}"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-r1:free",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000
            },
            timeout=120
        )
        
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            # Extract JSON from response
            return _parse_openrouter_response(content, question, context, depth, style)
        else:
            print(f"⚠️ OpenRouter returned {response.status_code}, falling back to local")
            return _run_local(question, context, depth, style)
            
    except Exception as e:
        print(f"⚠️ OpenRouter error: {e}, falling back to local")
        return _run_local(question, context, depth, style)


def _parse_openrouter_response(
    content: str,
    question: str,
    context: str,
    depth: str,
    style: str
) -> Dict[str, Any]:
    """Parse OpenRouter response into SPAR format."""
    try:
        # Try to find JSON in the response
        import re
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            parsed = json.loads(json_match.group())
            
            return {
                "spar_id": f"spar-or-{int(datetime.now().timestamp())}",
                "question": question,
                "context": context,
                "positions": parsed.get("positions", []),
                "synthesis": parsed.get("synthesis", {}),
                "probe": {"plurality": 8, "rigor": 8, "origin": 8, "basis": 8, "execution": 8},
                "config": {"pattern": "dialectic", "depth": depth, "style": style, "mode": "openrouter"},
                "transcript": []
            }
    except json.JSONDecodeError:
        pass
    
    # Fallback to local if parsing fails
    return _run_local(question, context, depth, style)


def _generate_recommendation(question: str, style: str) -> str:
    """Generate recommendation based on style."""
    if style == "consensus":
        return "Proceed with phased approach, building team alignment at each stage"
    elif style == "adversarial":
        return "Proceed only after addressing identified risks"
    elif style == "premortem":
        return "Mitigate failure modes before proceeding"
    else:
        return "Proceed with phased implementation, monitoring key metrics"


def _calculate_confidence(style: str) -> float:
    """Calculate confidence based on style."""
    return {
        "consensus": 0.82,
        "adversarial": 0.65,
        "premortem": 0.68,
        "steelman": 0.75,
        "balanced": 0.72
    }.get(style, 0.72)


if __name__ == "__main__":
    import sys
    
    question = sys.argv[1] if len(sys.argv) > 1 else "Should we proceed with this decision?"
    context = ""
    mode = "local"
    
    for i, arg in enumerate(sys.argv):
        if arg == "--context" and i + 1 < len(sys.argv):
            context = sys.argv[i + 1]
        if arg == "--openrouter":
            mode = "openrouter"
    
    result = run_sparkit(question, context, mode)
    print(json.dumps(result, indent=2))
