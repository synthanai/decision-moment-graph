"""
Shared pytest fixtures for DMG test suite
"""

import pytest
import json
import os
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return the path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_fixtures_dir(fixtures_dir):
    """Return the path to valid test fixtures."""
    return fixtures_dir / "valid"


@pytest.fixture
def invalid_fixtures_dir(fixtures_dir):
    """Return the path to invalid test fixtures."""
    return fixtures_dir / "invalid"


@pytest.fixture
def complete_decision(valid_fixtures_dir):
    """Load the complete valid decision fixture."""
    with open(valid_fixtures_dir / "complete_decision.dmg.json") as f:
        return json.load(f)


@pytest.fixture
def minimal_decision(valid_fixtures_dir):
    """Load the minimal valid decision fixture."""
    with open(valid_fixtures_dir / "minimal.dmg.json") as f:
        return json.load(f)


@pytest.fixture
def schema_path():
    """Return the path to the DMG schema."""
    return Path(__file__).parent.parent / "schema" / "dmg-core-v0.1.schema.json"


@pytest.fixture
def schema(schema_path):
    """Load the DMG JSON schema."""
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def validator_path():
    """Return the path to the validator CLI."""
    return Path(__file__).parent.parent / "cli" / "dmg_validate.py"


# Helper functions

def load_fixture(fixtures_dir: Path, name: str) -> dict:
    """Load a fixture by name."""
    path = fixtures_dir / f"{name}.dmg.json"
    with open(path) as f:
        return json.load(f)


def get_all_valid_fixtures(valid_fixtures_dir: Path) -> list:
    """Get all valid fixture file paths."""
    return list(valid_fixtures_dir.glob("*.dmg.json"))


def get_all_invalid_fixtures(invalid_fixtures_dir: Path) -> list:
    """Get all invalid fixture file paths."""
    return list(invalid_fixtures_dir.glob("*.dmg.json"))
