"""
SPAR → DMG Adapter

Converts SPAR debate outputs into DMG-compliant decision artifacts.

Usage:
    from dmg.adapters import SPARAdapter
    
    adapter = SPARAdapter()
    dmg = adapter.convert(spar_output)
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib


class SPARAdapter:
    """Converts SPAR debate outputs to DMG format."""
    
    DMG_VERSION = "0.2"
    
    def __init__(self):
        pass
    
    def convert(self, spar_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a SPAR output to a DMG object.
        
        Args:
            spar_output: The JSON output from a SPAR session
            
        Returns:
            A DMG-compliant dictionary
        """
        spar_id = spar_output.get('spar_id', self._generate_id())
        memo_id = f"dmg-from-{spar_id}"
        
        # Build MEMO
        memo = self._build_memo(spar_output, memo_id)
        
        # Build MOMENT (provenance)
        moment = self._build_moment(spar_output, memo_id)
        
        # Build objects (DISSENT, TRACE, COMMIT, OUTCOME)
        objects = self._build_objects(spar_output, memo_id)
        
        return {
            "dmg_version": self.DMG_VERSION,
            "memo": memo,
            "moment": moment,
            "objects": objects
        }
    
    def _build_memo(self, spar: Dict, memo_id: str) -> Dict:
        """Build MEMO from SPAR output."""
        synthesis = spar.get('synthesis', {})
        
        # Map positions to options
        options = []
        for pos in spar.get('positions', []):
            options.append({
                "name": pos.get('position', f"Option {pos.get('agent', '')}"),
                "description": pos.get('position', ''),
                "pros": pos.get('arguments', []),
                "cons": [],
                "source": f"spar:{pos.get('agent', 'unknown')}"
            })
        
        # Parse context into constraints
        context_str = spar.get('context', '')
        constraints = [c.strip() for c in context_str.split(';') if c.strip()]
        
        # Build recommendation with rationale
        recommendation = synthesis.get('recommendation', '')
        rationale = synthesis.get('rationale', '')
        if rationale:
            recommendation = f"{recommendation}. {rationale}"
        
        # Suggest RAMP level
        ramp_level = self._suggest_ramp(spar)
        
        return {
            "memo_id": memo_id,
            "title": spar.get('question', 'Untitled Decision'),
            "arena_id": spar.get('arena_id', 'spar-generated'),
            "decision": synthesis.get('recommendation', ''),
            "context": {
                "constraints": constraints,
                "assumptions": []
            },
            "options": options,
            "recommendation": recommendation,
            "ramp": {
                "level": ramp_level,
                "justification": "Auto-assigned from SPAR; review recommended"
            },
            "expected_outcomes": [
                {
                    "metric": "Decision confidence",
                    "expected": "Successful outcome",
                    "confidence": synthesis.get('confidence', 0.5),
                    "notes": "From SPAR synthesis"
                }
            ],
            "version": 1,
            "created_at": datetime.now().isoformat() + "Z",
            "updated_at": datetime.now().isoformat() + "Z"
        }
    
    def _build_moment(self, spar: Dict, memo_id: str) -> Dict:
        """Build MOMENT provenance from SPAR transcript."""
        moment_id = f"moment-{memo_id}"
        events = []
        
        # Initial creation event
        events.append(self._create_event(
            seq=1,
            event_type="MEMO_CREATED",
            actor="spar-adapter",
            payload={
                "source": "spar",
                "spar_id": spar.get('spar_id', 'unknown')
            },
            prev_hash=""
        ))
        
        # Add transcript events
        transcript = spar.get('transcript', [])
        for i, turn in enumerate(transcript):
            events.append(self._create_event(
                seq=i + 2,
                event_type="BLOCK_ADDED",
                actor=f"spar:{turn.get('agent', 'unknown')}",
                payload={
                    "type": turn.get('type', 'statement'),
                    "content": turn.get('content', '')[:200]  # Truncate
                },
                prev_hash=events[-1]['hash'] if events else ""
            ))
        
        return {
            "moment_id": moment_id,
            "memo_id": memo_id,
            "events": events
        }
    
    def _build_objects(self, spar: Dict, memo_id: str) -> Dict:
        """Build DISSENT, TRACE, COMMIT, OUTCOME objects."""
        synthesis = spar.get('synthesis', {})
        
        # Build DIS SENT from non-winning positions
        dissents = []
        recommendation = synthesis.get('recommendation', '').lower()
        
        for pos in spar.get('positions', []):
            # If position wasn't the recommendation, it's a dissent
            if pos.get('position', '').lower() not in recommendation:
                dissent = {
                    "dissent_id": f"dissent-{pos.get('agent', 'unknown')}",
                    "author": f"spar:{pos.get('agent', 'unknown')}",
                    "claim": pos.get('position', ''),
                    "evidence": pos.get('arguments', []),
                    "conditions_to_change_mind": ""
                }
                
                # Try to extract conditions from synthesis
                conditions = synthesis.get('conditions_to_reverse', [])
                if conditions:
                    dissent["conditions_to_change_mind"] = conditions[0]
                
                dissents.append(dissent)
        
        # Build TRACE from evidence
        traces = []
        for pos in spar.get('positions', []):
            for i, ev in enumerate(pos.get('evidence', [])):
                if isinstance(ev, dict) and ev.get('uri'):
                    traces.append({
                        "trace_id": f"trace-{pos.get('agent', 'unknown')}-{i}",
                        "claim": pos.get('position', ''),
                        "source": {
                            "type": ev.get('type', 'unknown'),
                            "uri": ev.get('uri', ''),
                            "retrieved_at": datetime.now().isoformat() + "Z"
                        },
                        "strength": "medium"
                    })
        
        return {
            "dissents": dissents,
            "traces": traces,
            "commit": {
                "state": "Proposed"
            },
            "outcome": {
                "outcome_id": f"outcome-{memo_id}",
                "next_check_date": None,
                "checks": []
            }
        }
    
    def _suggest_ramp(self, spar: Dict) -> int:
        """Suggest a RAMP level based on SPAR config."""
        config = spar.get('config', {})
        synthesis = spar.get('synthesis', {})
        
        # Start with L3 as default
        level = 3
        
        # Horizon adjustments
        horizon = config.get('horizon', 'cycle')
        if horizon == 'now':
            level = max(1, level - 1)
        elif horizon == 'legacy':
            level = min(5, level + 1)
        
        # Confidence adjustments
        confidence = synthesis.get('confidence', 0.5)
        if confidence < 0.5:
            level = min(5, level + 1)
        
        # Tension count
        tensions = synthesis.get('key_tensions', [])
        if len(tensions) > 3:
            level = min(5, level + 1)
        
        return level
    
    def _create_event(
        self,
        seq: int,
        event_type: str,
        actor: str,
        payload: Dict,
        prev_hash: str
    ) -> Dict:
        """Create a MOMENT event with hash chain."""
        ts = datetime.now().isoformat() + "Z"
        event_id = f"evt-{seq:03d}-{self._generate_id()[:8]}"
        
        # Create hash
        hash_input = f"{seq}{event_type}{json.dumps(payload, sort_keys=True)}{prev_hash}"
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:12]
        
        return {
            "event_id": event_id,
            "seq": seq,
            "ts": ts,
            "type": event_type,
            "actor": actor,
            "payload": payload,
            "prev_hash": prev_hash,
            "hash": hash_value
        }
    
    def _generate_id(self) -> str:
        """Generate a unique ID."""
        import time
        import random
        return f"{int(time.time())}-{random.randint(1000, 9999)}"


def convert_spar_file(input_path: str, output_path: str) -> None:
    """CLI helper to convert a SPAR JSON file to DMG."""
    with open(input_path, 'r') as f:
        spar_output = json.load(f)
    
    adapter = SPARAdapter()
    dmg = adapter.convert(spar_output)
    
    with open(output_path, 'w') as f:
        json.dump(dmg, f, indent=2)
    
    print(f"✅ Converted {input_path} → {output_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python spar_adapter.py <input.spar.json> <output.dmg.json>")
        sys.exit(1)
    
    convert_spar_file(sys.argv[1], sys.argv[2])
