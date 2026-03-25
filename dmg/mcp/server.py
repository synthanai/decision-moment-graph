
from mcp.server.fastmcp import FastMCP
import json
from pathlib import Path
from typing import Dict, Any, List
import sys
import os

# Create MCP Server
mcp = FastMCP("dmg")

# Import Validator from CLI
# Assuming running from repo root, so 'dmg' is importable
try:
    from dmg.cli.dmg_validate import DMGValidator, MERITValidator
except ImportError:
    # If path issue, add parent dir
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from dmg.cli.dmg_validate import DMGValidator, MERITValidator

def find_dmg_files(root_dir: str = ".") -> List[Path]:
    """Recursively find .dmg.json files"""
    return list(Path(root_dir).rglob("*.dmg.json"))

@mcp.resource("dmg://graph/summary")
def get_graph_summary() -> str:
    """Get high-level statistics of the decision graph"""
    files = find_dmg_files()
    
    stats = {
        "total_moments": len(files),
        "by_state": {},
        "merit_level": "Unknown" 
    }
    
    # Quick scan
    for f in files:
        try:
            with open(f) as fd:
                data = json.load(fd)
                state = data.get("objects", {}).get("commit", {}).get("state", "Unknown")
                stats["by_state"][state] = stats["by_state"].get(state, 0) + 1
        except:
            pass
            
    return json.dumps(stats, indent=2)

@mcp.resource("dmg://moment/{filename}")
def get_moment(filename: str) -> str:
    """Get details of a specific decision moment by filename"""
    # Security: prevent traversal
    if ".." in filename or "/" in filename:
        return json.dumps({"error": "Invalid filename"})
        
    # Search for file
    files = find_dmg_files()
    target = next((f for f in files if f.name == filename), None)
    
    if not target:
        return json.dumps({"error": "File not found"})
        
    with open(target) as f:
        return f.read()

@mcp.tool()
def validate_moment(file_path: str) -> str:
    """Validate a DMG file against Schema and MERIT principles"""
    path = Path(file_path)
    if not path.exists():
        return json.dumps({"error": f"File not found: {file_path}"})
        
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        return json.dumps({"error": f"Invalid JSON: {str(e)}"})
        
    # Run Schema Validation
    validator = DMGValidator()
    is_valid, errors, warnings = validator.validate(data)
    
    # Run MERIT Validation
    merit = MERITValidator()
    merit_res = merit.validate(data)
    
    report = {
        "file": str(path),
        "valid": is_valid,
        "errors": [str(e) for e in errors],
        "warnings": [str(w) for w in warnings],
        "merit": merit_res
    }
    
    return json.dumps(report, indent=2)

@mcp.tool()
def create_moment_scaffold(title: str, outcome_description: str) -> str:
    """Create a new Draft DMG Scaffold"""
    # Basic Template
    template = {
        "dmg_version": "0.1",
        "memo": {
            "memo_id": f"memo-{hash(title) % 10000}",
            "title": title,
            "decision": "Proposed decision goes here...",
            "options": [],
            "recommendation": "",
            "ramp": {"level": 1},
            "expected_outcomes": []
        },
        "moment": {
            "events": []
        },
        "objects": {
            "outcome": {
                "description": outcome_description,
                "checks": []
            },
            "commit": {"state": "Draft"}
        }
    }
    
    return json.dumps(template, indent=2)

if __name__ == "__main__":
    mcp.run()
