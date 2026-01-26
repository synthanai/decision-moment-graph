"""
Unit tests for audit_export module.
"""

import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sdk" / "python"))

from audit_export import AuditExporter


@pytest.fixture
def sample_dmg():
    return {
        "dmg_version": "0.1",
        "memo": {
            "memo_id": "test-001",
            "title": "API Migration Decision",
            "decision": "Proceed with GraphQL",
            "recommendation": "Migrate top 5 endpoints",
            "ramp": {"level": 3},
            "options": [
                {"name": "Full Migration", "description": "All at once"}
            ]
        },
        "objects": {
            "doors": {
                "own": {"name": "Tech Lead"},
                "ready": "Rollback in 1 hour"
            },
            "dissents": [
                {"author": "SRE", "claim": "Risk concern", "resolution": None}
            ],
            "outcome": {
                "checks": [{"verdict": "keep", "actual_result": "Success"}]
            },
            "traces": [{"source": "RFC-123"}]
        },
        "moment": {
            "events": [
                {"seq": 1, "type": "MEMO_CREATED", "actor": "system", "ts": "2026-01-01"}
            ]
        }
    }


class TestAuditExporter:
    """Tests for AuditExporter."""
    
    def test_to_html(self, sample_dmg):
        exporter = AuditExporter()
        html = exporter.to_html(sample_dmg)
        
        assert "<!DOCTYPE html>" in html
        assert "API Migration Decision" in html
        assert "MERIT Score" in html
    
    def test_to_markdown(self, sample_dmg):
        exporter = AuditExporter()
        md = exporter.to_markdown(sample_dmg)
        
        assert "# Decision Audit" in md
        assert "API Migration Decision" in md
        assert "MERIT Compliance" in md
        assert "Reversibility" in md
    
    def test_to_json(self, sample_dmg):
        import json
        exporter = AuditExporter()
        json_str = exporter.to_json(sample_dmg)
        
        data = json.loads(json_str)
        assert data["memo_id"] == "test-001"
        assert "merit_score" in data
        assert "merit_compliance" in data
    
    def test_to_file_html(self, sample_dmg):
        exporter = AuditExporter()
        
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            path = exporter.to_file(sample_dmg, f.name)
        
        try:
            content = Path(path).read_text()
            assert "<!DOCTYPE html>" in content
        finally:
            Path(path).unlink(missing_ok=True)
    
    def test_to_file_md(self, sample_dmg):
        exporter = AuditExporter()
        
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            path = exporter.to_file(sample_dmg, f.name)
        
        try:
            content = Path(path).read_text()
            assert "# Decision Audit" in content
        finally:
            Path(path).unlink(missing_ok=True)
    
    def test_merit_calculation(self, sample_dmg):
        exporter = AuditExporter()
        json_str = exporter.to_json(sample_dmg)
        
        import json
        data = json.loads(json_str)
        
        # Should have MERIT compliance details
        assert "Measured" in data["merit_compliance"]
        assert "Evidenced" in data["merit_compliance"]
        assert "Reversible" in data["merit_compliance"]
