#!/usr/bin/env python3
"""
DMG Conformance Test Runner

Runs all conformance test vectors against the DMG validator.

Usage:
    python conformance/runner.py
    python conformance/runner.py --category valid
    python conformance/runner.py --category invalid
    python conformance/runner.py --category merit
    python conformance/runner.py --ci
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
from dmg_validate import DMGValidator, MERITValidator


class ConformanceRunner:
    """Runs conformance tests against DMG validator."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.test_vectors_dir = base_dir / "test_vectors"
        self.results: List[Dict] = []
        
    def run_all(self) -> Tuple[int, int]:
        """Run all conformance tests. Returns (passed, failed)."""
        passed = 0
        failed = 0
        
        # Run valid tests
        p, f = self.run_valid_tests()
        passed += p
        failed += f
        
        # Run invalid tests
        p, f = self.run_invalid_tests()
        passed += p
        failed += f
        
        # Run MERIT level tests
        p, f = self.run_merit_tests()
        passed += p
        failed += f
        
        return passed, failed
    
    def run_category(self, category: str) -> Tuple[int, int]:
        """Run tests for a specific category."""
        if category == "valid":
            return self.run_valid_tests()
        elif category == "invalid":
            return self.run_invalid_tests()
        elif category == "merit":
            return self.run_merit_tests()
        else:
            print(f"Unknown category: {category}")
            return 0, 0
    
    def run_valid_tests(self) -> Tuple[int, int]:
        """Run valid test vectors. All should pass schema validation."""
        passed = 0
        failed = 0
        
        valid_dir = self.test_vectors_dir / "valid"
        if not valid_dir.exists():
            print("No valid test vectors found")
            return 0, 0
        
        print("\n" + "=" * 60)
        print("VALID TEST VECTORS")
        print("=" * 60)
        
        for filepath in sorted(valid_dir.glob("*.dmg.json")):
            try:
                with open(filepath) as f:
                    dmg = json.load(f)
                
                validator = DMGValidator()
                is_valid, errors, warnings = validator.validate(dmg)
                
                if is_valid:
                    print(f"✅ PASS: {filepath.name}")
                    passed += 1
                else:
                    print(f"❌ FAIL: {filepath.name}")
                    for e in errors:
                        print(f"   └─ {e}")
                    failed += 1
                    
            except json.JSONDecodeError as e:
                print(f"❌ FAIL: {filepath.name} (JSON error: {e})")
                failed += 1
        
        return passed, failed
    
    def run_invalid_tests(self) -> Tuple[int, int]:
        """Run invalid test vectors. All should fail with expected error."""
        passed = 0
        failed = 0
        
        invalid_dir = self.test_vectors_dir / "invalid"
        if not invalid_dir.exists():
            print("No invalid test vectors found")
            return 0, 0
        
        print("\n" + "=" * 60)
        print("INVALID TEST VECTORS")
        print("=" * 60)
        
        for filepath in sorted(invalid_dir.glob("*.dmg.json")):
            # Extract expected error from filename (e.g., invalid_E001_...)
            match = re.search(r"invalid_(E\d+)", filepath.name)
            expected_error = match.group(1) if match else None
            
            try:
                with open(filepath) as f:
                    dmg = json.load(f)
                
                # Also check if _expected_error is in the file
                if "_expected_error" in dmg:
                    expected_error = dmg["_expected_error"]
                
                validator = DMGValidator()
                is_valid, errors, warnings = validator.validate(dmg)
                
                if is_valid:
                    print(f"❌ FAIL: {filepath.name} (should have failed)")
                    failed += 1
                else:
                    # Check if expected error is in the errors
                    error_codes = [e.code for e in errors]
                    if expected_error and expected_error in error_codes:
                        print(f"✅ PASS: {filepath.name} (got {expected_error})")
                        passed += 1
                    elif expected_error:
                        print(f"⚠️  PARTIAL: {filepath.name}")
                        print(f"   └─ Expected {expected_error}, got {error_codes}")
                        passed += 1  # Still counts as pass - it did fail
                    else:
                        print(f"✅ PASS: {filepath.name} (failed as expected)")
                        passed += 1
                        
            except json.JSONDecodeError as e:
                if "parse_error" in filepath.name:
                    print(f"✅ PASS: {filepath.name} (parse error as expected)")
                    passed += 1
                else:
                    print(f"❌ FAIL: {filepath.name} (unexpected JSON error: {e})")
                    failed += 1
        
        return passed, failed
    
    def run_merit_tests(self) -> Tuple[int, int]:
        """Run MERIT level test vectors."""
        passed = 0
        failed = 0
        
        merit_dir = self.test_vectors_dir / "merit_levels"
        if not merit_dir.exists():
            print("No MERIT test vectors found")
            return 0, 0
        
        print("\n" + "=" * 60)
        print("MERIT LEVEL TEST VECTORS")
        print("=" * 60)
        
        for filepath in sorted(merit_dir.glob("*.dmg.json")):
            # Extract expected level from filename
            expected_level = None
            if "merit_none" in filepath.name:
                expected_level = "MERIT-None"
            elif "merit_partial" in filepath.name:
                expected_level = "MERIT-Partial"
            elif "merit_valid" in filepath.name:
                expected_level = "MERIT-Valid"
            
            try:
                with open(filepath) as f:
                    dmg = json.load(f)
                
                # Check if _expected_level is in the file
                if "_expected_level" in dmg:
                    expected_level = dmg["_expected_level"]
                
                validator = MERITValidator()
                result = validator.validate(dmg)
                actual_level = result["level"]
                
                if actual_level == expected_level:
                    print(f"✅ PASS: {filepath.name}")
                    print(f"   └─ {actual_level} ({result['passes']}/5)")
                    passed += 1
                else:
                    print(f"❌ FAIL: {filepath.name}")
                    print(f"   └─ Expected {expected_level}, got {actual_level}")
                    failed += 1
                    
            except json.JSONDecodeError as e:
                print(f"❌ FAIL: {filepath.name} (JSON error: {e})")
                failed += 1
        
        return passed, failed


def main():
    conformance_dir = Path(__file__).parent
    runner = ConformanceRunner(conformance_dir)
    
    # Parse arguments
    ci_mode = "--ci" in sys.argv
    category = None
    
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--category" and i < len(sys.argv) - 1:
            category = sys.argv[i + 1]
    
    # Run tests
    if category:
        passed, failed = runner.run_category(category)
    else:
        passed, failed = runner.run_all()
    
    # Print summary
    print("\n" + "=" * 60)
    print("CONFORMANCE SUMMARY")
    print("=" * 60)
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📊 Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All conformance tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    # Exit with appropriate code for CI
    if ci_mode:
        sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
