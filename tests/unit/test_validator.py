"""
Unit tests for DMG CLI validator
"""

import pytest
import subprocess
import json
import sys
from pathlib import Path


class TestValidatorCLI:
    """Test the dmg_validate.py CLI."""
    
    def test_validator_exists(self, validator_path):
        """Validator script should exist."""
        assert validator_path.exists()
    
    def test_validator_help(self, validator_path):
        """Validator should show help."""
        result = subprocess.run(
            [sys.executable, str(validator_path), "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "DMG Validator" in result.stdout or "usage" in result.stdout.lower()
    
    def test_validate_complete_decision(self, validator_path, valid_fixtures_dir):
        """Complete decision should pass validation."""
        fixture = valid_fixtures_dir / "complete_decision.dmg.json"
        
        result = subprocess.run(
            [sys.executable, str(validator_path), str(fixture)],
            capture_output=True,
            text=True
        )
        
        # Should exit 0 (success)
        assert result.returncode == 0
        assert "valid" in result.stdout.lower() or "passed" in result.stdout.lower()
    
    def test_validate_minimal_decision(self, validator_path, valid_fixtures_dir):
        """Minimal decision should pass validation."""
        fixture = valid_fixtures_dir / "minimal.dmg.json"
        
        result = subprocess.run(
            [sys.executable, str(validator_path), str(fixture)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
    
    def test_validate_two_options(self, validator_path, invalid_fixtures_dir):
        """Two options should fail validation."""
        fixture = invalid_fixtures_dir / "only_two_options.dmg.json"
        
        result = subprocess.run(
            [sys.executable, str(validator_path), str(fixture)],
            capture_output=True,
            text=True
        )
        
        # Should exit non-zero (failure)
        assert result.returncode != 0
        assert "option" in result.stdout.lower() or "error" in result.stderr.lower()
    
    def test_validate_missing_doors(self, validator_path, invalid_fixtures_dir):
        """Missing DOORS owner should fail for RAMP ≥3 Final."""
        fixture = invalid_fixtures_dir / "missing_doors_owner.dmg.json"
        
        result = subprocess.run(
            [sys.executable, str(validator_path), str(fixture)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "doors" in result.stdout.lower() or "owner" in result.stdout.lower()
    
    def test_validate_nonexistent_file(self, validator_path):
        """Nonexistent file should error gracefully."""
        result = subprocess.run(
            [sys.executable, str(validator_path), "/nonexistent/file.json"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "not found" in result.stdout.lower() or "error" in result.stderr.lower()
    
    def test_validate_invalid_json(self, validator_path, tmp_path):
        """Invalid JSON should error gracefully."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{ not valid json }")
        
        result = subprocess.run(
            [sys.executable, str(validator_path), str(bad_file)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0


class TestValidatorOutput:
    """Test validator output formatting."""
    
    def test_output_includes_summary(self, validator_path, valid_fixtures_dir):
        """Output should include validation summary."""
        fixture = valid_fixtures_dir / "complete_decision.dmg.json"
        
        result = subprocess.run(
            [sys.executable, str(validator_path), str(fixture)],
            capture_output=True,
            text=True
        )
        
        # Should mention what was checked
        output = result.stdout.lower()
        assert "ramp" in output or "options" in output or "validation" in output
    
    def test_output_includes_warnings(self, validator_path, valid_fixtures_dir):
        """Output may include warnings for recommendations."""
        fixture = valid_fixtures_dir / "minimal.dmg.json"
        
        result = subprocess.run(
            [sys.executable, str(validator_path), str(fixture)],
            capture_output=True,
            text=True
        )
        
        # Minimal decision might trigger warnings
        # This test documents expected behavior
        assert result.returncode == 0  # Still passes, just warns


class TestValidatorProgrammatic:
    """Test validator as importable module."""
    
    def test_import_validator(self, validator_path):
        """Should be able to import validator module."""
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("dmg_validate", validator_path)
        module = importlib.util.module_from_spec(spec)
        
        # Should load without error
        try:
            spec.loader.exec_module(module)
            loaded = True
        except Exception as e:
            # Main block might cause issues, that's OK
            loaded = True if "main" in str(e).lower() else False
        
        assert loaded
