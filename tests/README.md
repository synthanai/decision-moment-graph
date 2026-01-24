# DMG Test Suite

Comprehensive test coverage for the Decision Moment Graph standard.

## Test Categories

```
tests/
├── fixtures/           # Test data files
│   ├── valid/          # Valid DMG files
│   └── invalid/        # Invalid DMG files for error testing
├── unit/               # Unit tests
│   ├── test_schema.py  # JSON Schema validation
│   ├── test_validator.py # CLI validator tests
│   └── test_governance.py # Governance rules
├── integration/        # Integration tests
│   ├── test_workflow.py # Full workflow
│   ├── test_spar.py    # SPAR integration
│   └── test_outcome.py # Outcome tracking
└── conftest.py         # Shared fixtures
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=cli --cov-report=html
```

## Test Coverage Targets

| Component | Target | Current |
|-----------|--------|---------|
| Schema validation | 95% | - |
| Governance rules | 100% | - |
| CLI validator | 90% | - |
| SPAR adapter | 85% | - |
| State machine | 100% | - |
