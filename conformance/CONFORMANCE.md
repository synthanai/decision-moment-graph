# DMG Conformance Test Suite

This directory contains the official conformance test vectors for validating DMG implementations.

## Directory Structure

```
conformance/
├── test_vectors/
│   ├── valid/          # Files that MUST pass schema validation
│   ├── invalid/        # Files that MUST fail schema validation
│   └── merit_levels/   # Files testing MERIT compliance levels
├── runner.py           # Conformance test runner
└── CONFORMANCE.md      # This file
```

## Running Tests

```bash
# Run all conformance tests
python conformance/runner.py

# Run specific category
python conformance/runner.py --category valid
python conformance/runner.py --category invalid
python conformance/runner.py --category merit

# CI mode (exit code indicates pass/fail)
python conformance/runner.py --ci
```

## Test Vector Naming Convention

- `valid_*.dmg.json` — Must pass schema validation
- `invalid_*.dmg.json` — Must fail with specific error code
- `merit_none_*.dmg.json` — Must result in MERIT-None (0-2 principles)
- `merit_partial_*.dmg.json` — Must result in MERIT-Partial (3-4 principles)
- `merit_valid_*.dmg.json` — Must result in MERIT-Valid (5 principles)

## Expected Behaviors

### Valid Vectors
All files in `valid/` MUST:
- Pass JSON parsing
- Pass schema validation with 0 errors
- May have warnings

### Invalid Vectors
All files in `invalid/` MUST:
- Pass JSON parsing (or specify `_parse_error` in filename)
- Fail schema validation with the error code in the filename

### MERIT Level Vectors
Files in `merit_levels/` MUST:
- Pass schema validation
- Return the MERIT level indicated in the filename

## Adding New Test Vectors

1. Create a new `.dmg.json` file in the appropriate directory
2. Name it following the convention above
3. Run `python conformance/runner.py` to verify
