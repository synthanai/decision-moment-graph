#!/usr/bin/env python3
"""
DMG Validator CLI

Validates DMG (Decision Moment Graph) files against the core schema
and governance rules.

Usage:
    python dmg_validate.py <file.dmg.json>
    python dmg_validate.py --batch <directory>
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Schema version
DMG_VERSION = "0.1"


class ValidationError:
    def __init__(self, code: str, message: str, path: str = ""):
        self.code = code
        self.message = message
        self.path = path

    def __str__(self):
        if self.path:
            return f"[{self.code}] {self.path}: {self.message}"
        return f"[{self.code}] {self.message}"


class DMGValidator:
    """Validates DMG files against spec and governance rules."""

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def validate(self, dmg: Dict[str, Any]) -> Tuple[bool, List[ValidationError], List[ValidationError]]:
        """Validate a DMG document. Returns (is_valid, errors, warnings)."""
        self.errors = []
        self.warnings = []

        # 1. Version check
        self._check_version(dmg)

        # 2. Required fields
        self._check_required_fields(dmg)

        # 3. MEMO validation
        if "memo" in dmg:
            self._validate_memo(dmg["memo"])

        # 4. MOMENT validation
        if "moment" in dmg:
            self._validate_moment(dmg["moment"])

        # 5. Governance rules (RAMP-based)
        if "memo" in dmg and "objects" in dmg:
            self._validate_governance_rules(dmg)

        # 6. Hash chain integrity
        if "moment" in dmg:
            self._validate_hash_chain(dmg["moment"])

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_version(self, dmg: Dict):
        if "dmg_version" not in dmg:
            self.errors.append(ValidationError("E001", "Missing dmg_version"))
        elif dmg["dmg_version"] != DMG_VERSION:
            self.warnings.append(ValidationError(
                "W001",
                f"Version mismatch: expected {DMG_VERSION}, got {dmg['dmg_version']}"
            ))

    def _check_required_fields(self, dmg: Dict):
        required = ["dmg_version", "memo", "moment"]
        for field in required:
            if field not in dmg:
                self.errors.append(ValidationError("E002", f"Missing required field: {field}"))

    def _validate_memo(self, memo: Dict):
        # Required MEMO fields
        required = ["memo_id", "title", "decision", "options", "recommendation", "ramp"]
        for field in required:
            if field not in memo:
                self.errors.append(ValidationError("E010", f"Missing required memo field: {field}", "memo"))

        # Options must have at least 3
        if "options" in memo:
            if len(memo["options"]) < 3:
                self.errors.append(ValidationError(
                    "E011",
                    f"MEMO must have at least 3 options, got {len(memo['options'])}",
                    "memo.options"
                ))

        # Decision must be meaningful
        if "decision" in memo:
            if len(memo["decision"]) < 10:
                self.errors.append(ValidationError(
                    "E012",
                    "Decision statement too short (min 10 chars)",
                    "memo.decision"
                ))

    def _validate_moment(self, moment: Dict):
        if "events" not in moment:
            self.errors.append(ValidationError("E020", "MOMENT missing events array", "moment"))
            return

        if len(moment["events"]) == 0:
            self.warnings.append(ValidationError("W020", "MOMENT has no events", "moment"))

        # Check event sequence
        for i, event in enumerate(moment["events"]):
            if "seq" not in event:
                self.errors.append(ValidationError("E021", f"Event {i} missing seq", f"moment.events[{i}]"))
            elif event["seq"] != i + 1:
                self.warnings.append(ValidationError(
                    "W021",
                    f"Event seq mismatch: expected {i+1}, got {event['seq']}",
                    f"moment.events[{i}]"
                ))

    def _validate_governance_rules(self, dmg: Dict):
        """Validate RAMP-based governance requirements."""
        memo = dmg["memo"]
        objects = dmg.get("objects", {})
        commit = objects.get("commit", {})

        ramp_level = memo.get("ramp", {}).get("level", 1)
        commit_state = commit.get("state", "Draft")

        # Rules only apply for Final/Approved states
        if commit_state not in ["Final", "Approved"]:
            return

        # Rule 1: Outcome check required for Final/Approved
        outcome = objects.get("outcome", {})
        if not outcome.get("next_check_date"):
            self.errors.append(ValidationError(
                "E100",
                "Final/Approved decisions require outcome.next_check_date",
                "objects.outcome.next_check_date"
            ))

        # RAMP >= 3 rules
        if ramp_level >= 3:
            # Rule 2: At least 1 DISSENT required
            dissents = objects.get("dissents", [])
            if len(dissents) < 1:
                self.errors.append(ValidationError(
                    "E101",
                    "RAMP >= 3 requires at least 1 DISSENT",
                    "objects.dissents"
                ))

            # Rule 3: Rollback owner required
            doors = memo.get("doors", {})
            own = doors.get("own", {})
            if not own.get("name"):
                self.errors.append(ValidationError(
                    "E102",
                    "RAMP >= 3 requires doors.own.name (rollback owner)",
                    "memo.doors.own.name"
                ))

            # Rule 4: At least 2 signals required
            signals = doors.get("signals", [])
            if len(signals) < 2:
                self.errors.append(ValidationError(
                    "E103",
                    f"RAMP >= 3 requires at least 2 signals, got {len(signals)}",
                    "memo.doors.signals"
                ))

            # Rule 5: At least 1 expected outcome required
            expected = memo.get("expected_outcomes", [])
            if len(expected) < 1:
                self.errors.append(ValidationError(
                    "E104",
                    "RAMP >= 3 requires at least 1 expected_outcome with confidence",
                    "memo.expected_outcomes"
                ))

    def _validate_hash_chain(self, moment: Dict):
        """Verify event hash chain integrity."""
        events = moment.get("events", [])
        if len(events) == 0:
            return

        prev_hash = ""
        for i, event in enumerate(events):
            if "hash" not in event:
                self.warnings.append(ValidationError(
                    "W030",
                    f"Event {i} missing hash",
                    f"moment.events[{i}]"
                ))
                continue

            if event.get("prev_hash", "") != prev_hash:
                self.warnings.append(ValidationError(
                    "W031",
                    f"Event {i} prev_hash mismatch",
                    f"moment.events[{i}]"
                ))

            prev_hash = event["hash"]


def validate_file(filepath: Path) -> bool:
    """Validate a single DMG file."""
    print(f"\n📋 Validating: {filepath.name}")
    print("-" * 50)

    try:
        with open(filepath, "r") as f:
            dmg = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False

    validator = DMGValidator()
    is_valid, errors, warnings = validator.validate(dmg)

    # Print warnings
    for w in warnings:
        print(f"⚠️  {w}")

    # Print errors
    for e in errors:
        print(f"❌ {e}")

    if is_valid:
        print(f"✅ VALID ({len(warnings)} warnings)")
    else:
        print(f"❌ INVALID ({len(errors)} errors, {len(warnings)} warnings)")

    return is_valid


def main():
    if len(sys.argv) < 2:
        print("Usage: python dmg_validate.py <file.dmg.json>")
        print("       python dmg_validate.py --batch <directory>")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("Error: --batch requires a directory path")
            sys.exit(1)
        directory = Path(sys.argv[2])
        files = list(directory.glob("*.dmg.json"))
        if not files:
            print(f"No *.dmg.json files found in {directory}")
            sys.exit(1)

        results = []
        for f in files:
            results.append((f.name, validate_file(f)))

        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        passed = sum(1 for _, v in results if v)
        failed = len(results) - passed
        for name, valid in results:
            status = "✅" if valid else "❌"
            print(f"  {status} {name}")
        print(f"\nTotal: {passed} passed, {failed} failed")
        sys.exit(0 if failed == 0 else 1)
    else:
        filepath = Path(sys.argv[1])
        is_valid = validate_file(filepath)
        sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
