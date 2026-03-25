"""
FRAME Templates

Pre-built templates for common decision patterns.
Use these to quickly frame standard decision types.
"""

from typing import Dict, List, Any


# Standard decision frame templates
FRAME_TEMPLATES: Dict[str, Dict[str, Any]] = {
    
    "build_vs_buy": {
        "name": "Build vs Buy",
        "description": "Deciding between building in-house or purchasing a solution",
        "question_template": "Should we build {feature} in-house or buy an existing solution?",
        "default_options": [
            {"id": "build", "title": "Build in-house", "description": "Develop the solution internally"},
            {"id": "buy", "title": "Buy/license", "description": "Purchase or license an existing solution"},
            {"id": "hybrid", "title": "Hybrid approach", "description": "Buy core, build integrations"},
            {"id": "status-quo", "title": "Status quo", "description": "Continue without this capability"}
        ],
        "typical_constraints": [
            "Engineering capacity",
            "Budget constraints", 
            "Time to market",
            "Long-term ownership costs"
        ]
    },
    
    "technology_migration": {
        "name": "Technology Migration",
        "description": "Migrating from one technology stack to another",
        "question_template": "Should we migrate from {current} to {proposed}?",
        "default_options": [
            {"id": "full-migration", "title": "Full migration", "description": "Complete replacement"},
            {"id": "incremental", "title": "Incremental migration", "description": "Phased approach"},
            {"id": "parallel", "title": "Run in parallel", "description": "Maintain both temporarily"},
            {"id": "status-quo", "title": "Stay on current stack", "description": "No migration"}
        ],
        "typical_constraints": [
            "Downtime tolerance",
            "Team expertise",
            "Vendor support timeline",
            "Integration dependencies"
        ]
    },
    
    "resource_allocation": {
        "name": "Resource Allocation",
        "description": "Deciding how to allocate limited resources",
        "question_template": "How should we allocate {resource} across {options}?",
        "default_options": [
            {"id": "option-a", "title": "Focus on A", "description": "Prioritize first option"},
            {"id": "option-b", "title": "Focus on B", "description": "Prioritize second option"},
            {"id": "split", "title": "Split allocation", "description": "Divide resources"},
            {"id": "defer", "title": "Defer decision", "description": "Wait for more information"}
        ],
        "typical_constraints": [
            "Total budget",
            "Timeline",
            "Strategic priorities",
            "Risk tolerance"
        ]
    },
    
    "process_change": {
        "name": "Process Change",
        "description": "Changing an organizational process or workflow",
        "question_template": "Should we change our {process} process?",
        "default_options": [
            {"id": "full-change", "title": "Full process change", "description": "Replace current process"},
            {"id": "incremental", "title": "Incremental improvement", "description": "Evolve gradually"},
            {"id": "pilot", "title": "Pilot program", "description": "Test with subset"},
            {"id": "status-quo", "title": "Keep current process", "description": "No change"}
        ],
        "typical_constraints": [
            "Team capacity for change",
            "Training requirements",
            "Compliance considerations",
            "Stakeholder buy-in"
        ]
    },
    
    "vendor_selection": {
        "name": "Vendor Selection",
        "description": "Selecting between multiple vendors or partners",
        "question_template": "Which vendor should we select for {need}?",
        "default_options": [
            {"id": "vendor-a", "title": "Vendor A", "description": "First vendor option"},
            {"id": "vendor-b", "title": "Vendor B", "description": "Second vendor option"},
            {"id": "vendor-c", "title": "Vendor C", "description": "Third vendor option"},
            {"id": "none", "title": "No vendor / in-house", "description": "Handle internally"}
        ],
        "typical_constraints": [
            "Budget",
            "Feature requirements",
            "Integration needs",
            "Long-term support"
        ]
    },
    
    "go_no_go": {
        "name": "Go / No-Go",
        "description": "Binary decision with mitigation options",
        "question_template": "Should we proceed with {initiative}?",
        "default_options": [
            {"id": "go", "title": "Go - proceed as planned", "description": "Execute the initiative"},
            {"id": "go-modified", "title": "Go with modifications", "description": "Proceed with adjustments"},
            {"id": "delay", "title": "Delay", "description": "Postpone for more information"},
            {"id": "no-go", "title": "No-go", "description": "Do not proceed"}
        ],
        "typical_constraints": [
            "Risk assessment",
            "Resource readiness",
            "Market timing",
            "Stakeholder alignment"
        ]
    }
}


def get_template(template_name: str) -> Dict[str, Any]:
    """
    Get a frame template by name.
    
    Args:
        template_name: One of the template names (e.g., "build_vs_buy")
        
    Returns:
        Template dict with options and constraints
        
    Raises:
        KeyError if template not found
    """
    if template_name not in FRAME_TEMPLATES:
        available = ", ".join(FRAME_TEMPLATES.keys())
        raise KeyError(f"Template '{template_name}' not found. Available: {available}")
    return FRAME_TEMPLATES[template_name]


def list_templates() -> List[str]:
    """List all available template names."""
    return list(FRAME_TEMPLATES.keys())


def apply_template(
    template_name: str,
    **substitutions
) -> Dict[str, Any]:
    """
    Apply a template with variable substitutions.
    
    Args:
        template_name: Template to use
        **substitutions: Variables to substitute in the template
        
    Returns:
        Frame dict ready for FrameBuilder
        
    Example:
        frame = apply_template(
            "build_vs_buy",
            feature="customer analytics"
        )
    """
    template = get_template(template_name)
    
    # Substitute in question
    question = template["question_template"].format(**substitutions)
    
    return {
        "question": question,
        "options": template["default_options"].copy(),
        "constraints": template["typical_constraints"].copy()
    }
