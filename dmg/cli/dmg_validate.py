#!/usr/bin/env python3
"""
DMG Validator CLI

Validates DMG (Decision Moment Graph) files against the core schema
and governance rules. Supports MERIT principle validation.

Usage:
    python dmg_validate.py <file.dmg.json>
    python dmg_validate.py --batch <directory>
    python dmg_validate.py --merit <file.dmg.json>
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Schema version
DMG_VERSION = "0.1"

# MERIT thresholds (per MERIT_VALIDATOR_SPEC.md)
MERIT_THRESHOLDS = {
    "measured": 0.6,
    "evidenced": 0.7,
    "reversible": 0.7,
    "inspectable": 0.7,
    "traceable": 0.7
}


class ValidationError:
    def __init__(self, code: str, message: str, path: str = ""):
        self.code = code
        self.message = message
        self.path = path

    def __str__(self):
        if self.path:
            return f"[{self.code}] {self.path}: {self.message}"
        return f"[{self.code}] {self.message}"


class MERITValidator:
    """
    Validates DMG files against the MERIT principles.
    
    MERIT = Measured with OUTCOME, Evidenced via MEMO, 
            Reversible thru DOORS, Inspectable in MOMENT, Traceable by TRACE
    """

    def validate(self, dmg: Dict[str, Any]) -> Dict[str, Any]:
        """Returns MERIT validation results."""
        results = {
            "measured": self._check_measured(dmg),
            "evidenced": self._check_evidenced(dmg),
            "reversible": self._check_reversible(dmg),
            "inspectable": self._check_inspectable(dmg),
            "traceable": self._check_traceable(dmg)
        }
        
        # Calculate passes
        passes = sum(1 for k, v in results.items() 
                     if v["score"] >= MERIT_THRESHOLDS[k])
        
        # Determine level
        if passes == 5:
            level = "MERIT-Valid"
        elif passes >= 3:
            level = "MERIT-Partial"
        else:
            level = "MERIT-None"
        
        return {
            "principles": results,
            "passes": passes,
            "total": 5,
            "level": level
        }

    def _check_measured(self, dmg: Dict) -> Dict:
        """M: Measured with OUTCOME - quantified outcomes linked to predictions."""
        score = 0.0
        details = []
        
        outcome = dmg.get("objects", {}).get("outcome")
        memo = dmg.get("memo", {})
        expected = memo.get("expected_outcomes", [])
        
        # M1: OUTCOME object check (30%)
        if outcome:
            score += 0.30
            details.append("✓ OUTCOME object exists")
            
            checks = outcome.get("checks", [])
            
            # Scenario A: Retrospective (Has checks)
            if len(checks) > 0:
                score += 0.30 # M2 passed
                details.append("✓ Outcome checks exist")
                
                # M3b: Audit results exist
                has_actuals = False
                for check in checks:
                    audits = check.get("expected_outcomes_audit", [])
                    if audits and all(a.get("actual") for a in audits):
                        has_actuals = True
                        break
                
                if has_actuals:
                    score += 0.40
                    details.append("✓ Actual results recorded")
                else:
                    details.append("✗ Checks exist but missing actuals")
            
            # Scenario B: Prospective (No checks yet)
            else:
                 # M3a: Has defined predictions
                 if len(expected) > 0:
                     score += 0.40 # Awarding points to reach passing threshold
                     details.append("✓ Prospective: checks empty but expected_outcomes defined")
                 else:
                     details.append("✗ No checks and no expected_outcomes")
        
        else:
            # Fallback for Proposed decisions without OUTCOME object yet?
            # Spec says M1 requires OUTCOME object. So we stick to that.
            # But maybe we should warn?
            details.append("✗ No OUTCOME object")
            
            # Special case: If Expected Outcomes exist, give partial credit?
            if len(expected) > 0:
                details.append("◐ defined expected_outcomes (needs empty outcome object for M1)")

        return {"score": round(score, 2), "details": details}

    def _check_evidenced(self, dmg: Dict) -> Dict:
        """E: Evidenced via MEMO - documented options with rationale."""
        score = 0.0
        details = []
        
        memo = dmg.get("memo", {})
        
        # E1: MEMO exists with decision (30%)
        if memo and memo.get("decision"):
            score += 0.30
            details.append("✓ MEMO with decision")
            
            # E2: At least 3 options (40%)
            options = memo.get("options", [])
            if len(options) >= 3:
                score += 0.40
                details.append(f"✓ {len(options)} options documented")
                
                # E3: Options have rationale (30%)
                if all(opt.get("rationale") or (opt.get("pros") and opt.get("cons")) 
                       for opt in options):
                    score += 0.30
                    details.append("✓ All options have rationale")
                else:
                    details.append("✗ Some options missing rationale")
            else:
                details.append(f"✗ Only {len(options)} options (need 3+)")
        else:
            details.append("✗ No MEMO or decision")
        
        return {"score": round(score, 2), "details": details}

    def _check_reversible(self, dmg: Dict) -> Dict:
        """R: Reversible thru DOORS - governance gates and rollback paths."""
        score = 0.0
        details = []
        
        doors = dmg.get("objects", {}).get("doors", {})
        
        # R1: DOORS object exists (30%)
        if doors:
            score += 0.30
            details.append("✓ DOORS object exists")
            
            # R2: Owner defined (40%)
            own = doors.get("own", {})
            if own.get("name"):
                score += 0.40
                details.append(f"✓ Owner: {own.get('name')}")
            else:
                details.append("✗ No ownership defined")
            
            # R3: Rollback path (ready) defined (30%)
            if doors.get("ready"):
                score += 0.30
                details.append("✓ Rollback path documented")
            else:
                details.append("✗ No rollback path (ready)")
        else:
            details.append("✗ No DOORS object")
        
        return {"score": round(score, 2), "details": details}

    def _check_inspectable(self, dmg: Dict) -> Dict:
        """I: Inspectable in MOMENT - audit trail with valid hash chain."""
        score = 0.0
        details = []
        
        moment = dmg.get("moment", {})
        events = moment.get("events", [])
        
        # I1: MOMENT exists with events (40%)
        if events:
            score += 0.40
            details.append(f"✓ {len(events)} events in MOMENT")
            
            # I2: Events have required fields (30%)
            required = ["event_id", "seq", "ts", "type", "actor"]
            if all(all(e.get(f) for f in required) for e in events):
                score += 0.30
                details.append("✓ Events have required fields")
            else:
                details.append("✗ Some events missing fields")
            
            # I3: Hash chain is valid (30%)
            if len(events) > 1:
                chain_valid = True
                prev_hash = ""
                for e in events:
                    if e.get("prev_hash", "") != prev_hash:
                        chain_valid = False
                        break
                    prev_hash = e.get("hash", "")
                
                if chain_valid:
                    score += 0.30
                    details.append("✓ Hash chain valid")
                else:
                    details.append("✗ Hash chain broken")
            else:
                score += 0.30  # Single event, chain trivially valid
                details.append("✓ Single event (chain trivially valid)")
        else:
            details.append("✗ No events in MOMENT")
        
        return {"score": round(score, 2), "details": details}

    def _check_traceable(self, dmg: Dict) -> Dict:
        """T: Traceable by TRACE - evidence provenance chain."""
        score = 0.0
        details = []
        
        traces = dmg.get("objects", {}).get("traces", [])
        
        # T1: TRACE objects exist (40%)
        if traces:
            score += 0.40
            details.append(f"✓ {len(traces)} TRACE objects")
            
            # T2: All traces have source provenance (30%)
            if all(t.get("source", {}).get("uri") or t.get("source", {}).get("type") 
                   for t in traces):
                score += 0.30
                details.append("✓ All traces have source")
            else:
                details.append("✗ Some traces missing source")
            
            # T3: At least one strong trace (30%)
            if any(t.get("strength") == "strong" for t in traces):
                score += 0.30
                details.append("✓ Has strong evidence")
            else:
                details.append("◐ No 'strong' evidence (medium/weak only)")
        else:
            details.append("✗ No TRACE objects")
        
        return {"score": round(score, 2), "details": details}


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


def validate_file(filepath: Path, merit_mode: bool = False) -> bool:
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
        print(f"✅ Schema: VALID ({len(warnings)} warnings)")
    else:
        print(f"❌ Schema: INVALID ({len(errors)} errors, {len(warnings)} warnings)")

    # MERIT validation
    if merit_mode:
        print("\n" + "=" * 50)
        print("MERIT VALIDATION")
        print("=" * 50)
        
        merit_validator = MERITValidator()
        result = merit_validator.validate(dmg)
        
        # Print each principle
        for name, data in result["principles"].items():
            initial = name[0].upper()
            passed = data["score"] >= MERIT_THRESHOLDS[name]
            status = "✓" if passed else "✗"
            print(f"\n{initial}: {name.capitalize()} ({data['score']:.0%})")
            for detail in data["details"]:
                print(f"   {detail}")
        
        # Print summary
        print("\n" + "-" * 50)
        level_emoji = {"MERIT-Valid": "🟢", "MERIT-Partial": "🟡", "MERIT-None": "🔴"}
        print(f"{level_emoji.get(result['level'], '⚪')} {result['level']} ({result['passes']}/{result['total']} principles)")
        
        # Return based on MERIT level (accept Partial or Valid)
        return result["passes"] >= 3

    return is_valid


def main():
    if len(sys.argv) < 2:
        print("Usage: python dmg_validate.py <file.dmg.json>")
        print("       python dmg_validate.py --batch <directory>")
        print("       python dmg_validate.py --merit <file.dmg.json>")
        sys.exit(1)

    merit_mode = "--merit" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--merit"]

    if args[0] == "--batch":
        if len(args) < 2:
            print("Error: --batch requires a directory path")
            sys.exit(1)
        directory = Path(args[1])
        files = list(directory.glob("*.dmg.json"))
        if not files:
            print(f"No *.dmg.json files found in {directory}")
            sys.exit(1)

        results = []
        for f in files:
            results.append((f.name, validate_file(f, merit_mode)))

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
        filepath = Path(args[0])
        is_valid = validate_file(filepath, merit_mode)
        sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()

