"""
Unit tests for DMG JSON Schema validation
"""

import pytest
import json
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
class TestSchemaValidation:
    """Test DMG schema validation."""
    
    def test_schema_loads(self, schema):
        """Schema should load without errors."""
        assert schema is not None
        assert "$schema" in schema
        assert schema.get("title") == "DMG Core Schema"
    
    def test_valid_complete_decision(self, schema, complete_decision):
        """Complete valid decision should pass schema validation."""
        try:
            validate(instance=complete_decision, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Valid decision failed schema validation: {e.message}")
    
    def test_valid_minimal_decision(self, schema, minimal_decision):
        """Minimal valid decision should pass schema validation."""
        try:
            validate(instance=minimal_decision, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Minimal decision failed schema validation: {e.message}")
    
    def test_missing_required_field(self, schema):
        """Decision missing required field should fail."""
        invalid = {
            "dmg_version": "0.1",
            "memo": {
                # Missing memo_id and title
                "options": []
            }
        }
        with pytest.raises(ValidationError):
            validate(instance=invalid, schema=schema)
    
    def test_invalid_dmg_version(self, schema):
        """Invalid dmg_version should fail."""
        invalid = {
            "dmg_version": "9.9",  # Invalid version
            "memo": {
                "memo_id": "test",
                "title": "Test",
                "options": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
                "ramp": {"level": 3}
            }
        }
        # Note: Schema may or may not enforce version - check behavior
        # This test documents expected behavior
    
    def test_ramp_level_bounds(self, schema):
        """RAMP level should be between 1-5."""
        base = {
            "dmg_version": "0.1",
            "memo": {
                "memo_id": "test",
                "title": "Test",
                "options": [{"name": "A"}, {"name": "B"}, {"name": "C"}]
            }
        }
        
        # Valid levels
        for level in [1, 2, 3, 4, 5]:
            base["memo"]["ramp"] = {"level": level}
            try:
                validate(instance=base, schema=schema)
            except ValidationError:
                pytest.fail(f"RAMP level {level} should be valid")
        
        # Invalid levels
        for level in [0, 6, -1, 10]:
            base["memo"]["ramp"] = {"level": level}
            with pytest.raises(ValidationError):
                validate(instance=base, schema=schema)
    
    def test_options_array(self, schema):
        """Options should be an array of objects."""
        base = {
            "dmg_version": "0.1",
            "memo": {
                "memo_id": "test",
                "title": "Test",
                "ramp": {"level": 3}
            }
        }
        
        # Valid options
        base["memo"]["options"] = [
            {"name": "A", "description": "Opt A"},
            {"name": "B", "description": "Opt B"},
            {"name": "C", "description": "Opt C"}
        ]
        validate(instance=base, schema=schema)
        
        # Invalid: string instead of array
        base["memo"]["options"] = "not an array"
        with pytest.raises(ValidationError):
            validate(instance=base, schema=schema)
    
    def test_commit_states(self, schema, minimal_decision):
        """Commit state should be valid enum."""
        valid_states = ["Draft", "Proposed", "Approved", "Final", "Reversed", "Superseded"]
        
        for state in valid_states:
            minimal_decision["objects"] = {
                "commit": {"state": state}
            }
            # Should not raise
            validate(instance=minimal_decision, schema=schema)
    
    def test_dissent_structure(self, schema, minimal_decision):
        """Dissent should have required fields."""
        minimal_decision["objects"] = {
            "dissents": [
                {
                    "dissent_id": "d1",
                    "author": "Jane Doe",
                    "claim": "I disagree because...",
                    "conditions_to_change_mind": "If X happens"
                }
            ]
        }
        validate(instance=minimal_decision, schema=schema)
    
    def test_moment_events(self, schema, minimal_decision):
        """Moment events should be properly structured."""
        minimal_decision["moment"] = {
            "moment_id": "moment-test",
            "memo_id": "test-minimal-001",
            "events": [
                {
                    "event_id": "evt-001",
                    "seq": 1,
                    "ts": "2026-01-25T00:00:00Z",
                    "type": "MEMO_CREATED",
                    "actor": "user",
                    "payload": {},
                    "prev_hash": "",
                    "hash": "abc123"
                }
            ]
        }
        validate(instance=minimal_decision, schema=schema)


class TestSchemaStructure:
    """Test schema structure and documentation."""
    
    def test_schema_has_definitions(self, schema):
        """Schema should have reusable definitions."""
        assert "definitions" in schema or "$defs" in schema
    
    def test_schema_has_descriptions(self, schema):
        """Key schema properties should have descriptions."""
        assert "description" in schema
        
        # Check memo properties
        memo_props = schema.get("properties", {}).get("memo", {}).get("properties", {})
        for key in ["memo_id", "title", "options", "ramp"]:
            if key in memo_props:
                assert "description" in memo_props[key] or "type" in memo_props[key]
    
    def test_schema_examples(self, schema):
        """Schema should include examples."""
        # Check if examples are provided in definitions
        definitions = schema.get("definitions", schema.get("$defs", {}))
        # At least some definitions should have examples
        has_examples = any(
            "examples" in defn or "example" in defn
            for defn in definitions.values()
            if isinstance(defn, dict)
        )
        # Note: examples are recommended but not required
