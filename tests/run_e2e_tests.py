#!/usr/bin/env python3
"""
Unified Opaque-Box E2E Test Runner for AutoEditor AI Studio.
Discovers and executes tests across Tiers 1-4, manages test server lifecycle,
outputs formatted human-readable summaries and machine-readable JSON reports,
and returns exit code 0 on complete pass.

Usage:
    python tests/run_e2e_tests.py [--tier {1,2,3,4,all}] [-v] [--json-out PATH] [-k FILTER]
"""

import os
import sys
import time
import json
import unittest
import argparse

# Set up project path
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Ensure console supports utf-8 safely on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from tests.e2e.conftest_utils import ensure_test_server, stop_test_server, probe_http_health


class StructuredTestResult(unittest.TestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=1):
        super().__init__(stream, descriptions, verbosity)
        self.verbosity = verbosity
        self.records = []
        self._start_times = {}

    def startTest(self, test):
        super().startTest(test)
        self._start_times[test.id()] = time.time()
        if self.verbosity > 1:
            print(f"  RUNNING: {test.id()} ... ", end="", flush=True)

    def addSuccess(self, test):
        super().addSuccess(test)
        elapsed = time.time() - self._start_times.get(test.id(), time.time())
        self.records.append({
            "id": test.id(),
            "name": test._testMethodName,
            "class": test.__class__.__name__,
            "status": "PASS",
            "duration": round(elapsed, 4),
            "error": None
        })
        if self.verbosity > 1:
            print(f"PASS ({elapsed:.2f}s)")
        elif self.verbosity == 1:
            print(".", end="", flush=True)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        elapsed = time.time() - self._start_times.get(test.id(), time.time())
        err_msg = self._exc_info_to_string(err, test)
        self.records.append({
            "id": test.id(),
            "name": test._testMethodName,
            "class": test.__class__.__name__,
            "status": "FAIL",
            "duration": round(elapsed, 4),
            "error": err_msg
        })
        if self.verbosity > 1:
            print(f"FAIL ({elapsed:.2f}s)")
        elif self.verbosity == 1:
            print("F", end="", flush=True)

    def addError(self, test, err):
        super().addError(test, err)
        elapsed = time.time() - self._start_times.get(test.id(), time.time())
        err_msg = self._exc_info_to_string(err, test)
        self.records.append({
            "id": test.id(),
            "name": test._testMethodName,
            "class": test.__class__.__name__,
            "status": "ERROR",
            "duration": round(elapsed, 4),
            "error": err_msg
        })
        if self.verbosity > 1:
            print(f"ERROR ({elapsed:.2f}s)")
        elif self.verbosity == 1:
            print("E", end="", flush=True)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        elapsed = time.time() - self._start_times.get(test.id(), time.time())
        self.records.append({
            "id": test.id(),
            "name": test._testMethodName,
            "class": test.__class__.__name__,
            "status": "SKIP",
            "duration": round(elapsed, 4),
            "error": reason
        })
        if self.verbosity > 1:
            print(f"SKIP ({reason})")
        elif self.verbosity == 1:
            print("S", end="", flush=True)


def parse_args():
    parser = argparse.ArgumentParser(description="AutoEditor AI Studio E2E Test Runner")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all",
                        help="Select test tier to execute (default: all)")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Enable verbose test output")
    parser.add_argument("--json-out", type=str, default=None,
                        help="Filepath to write structured JSON test results")
    parser.add_argument("-k", "--filter", type=str, default=None,
                        help="Filter test cases by pattern in test name")
    return parser.parse_args()


def load_suite(tier="all", pattern=None):
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    tier_modules = {
        "1": "tests.e2e.test_tier1_features",
        "2": "tests.e2e.test_tier2_boundaries",
        "3": "tests.e2e.test_tier3_combinations",
        "4": "tests.e2e.test_tier4_workloads"
    }

    selected = [tier_modules[tier]] if tier in tier_modules else list(tier_modules.values())

    for mod_name in selected:
        try:
            mod_suite = loader.loadTestsFromName(mod_name)
            if pattern:
                filtered = unittest.TestSuite()
                for test in mod_suite:
                    if hasattr(test, "_testMethodName") and pattern.lower() in test._testMethodName.lower():
                        filtered.addTest(test)
                    elif hasattr(test, "__iter__"):
                        for subtest in test:
                            if pattern.lower() in subtest._testMethodName.lower():
                                filtered.addTest(subtest)
                suite.addTest(filtered)
            else:
                suite.addTest(mod_suite)
        except Exception as e:
            print(f"Warning: Failed to load module {mod_name}: {e}", file=sys.stderr)

    return suite


def main():
    args = parse_args()
    verbosity = 2 if args.verbose else 1

    print("=" * 72)
    print(" AutoEditor AI Studio — Opaque-Box E2E Test Runner")
    print(f" Tier Selection : Tier {args.tier.upper()}")
    print(f" Working Dir    : {PROJECT_DIR}")
    print(f" Verbosity      : {verbosity}")
    if args.filter:
        print(f" Filter Pattern : {args.filter}")
    print("=" * 72)

    # Ensure background test server is available for API tests
    print("\n[INIT] Checking backend AI engine status on port 4001...")
    server_proc = ensure_test_server(port=4001, timeout=12.0)
    if probe_http_health(port=4001, timeout=2.0):
        print("[INIT] [ONLINE] AI Companion Server is ONLINE and ready on port 4001.")
    else:
        print("[INIT] [OFFLINE] AI Companion Server not responding on port 4001. Proceeding with offline tests.")

    # Load test suite
    suite = load_suite(tier=args.tier, pattern=args.filter)
    total_tests = suite.countTestCases()
    print(f"\n[EXEC] Loaded {total_tests} test cases. Commencing execution...\n")

    start_time = time.time()
    result = StructuredTestResult(verbosity=verbosity)
    try:
        suite.run(result)
    finally:
        # If we spawned the server specifically for this run, shut it down
        stop_test_server()

    elapsed = time.time() - start_time
    if verbosity == 1:
        print()

    # Tally results
    passed_count = len([r for r in result.records if r["status"] == "PASS"])
    failed_count = len(result.failures)
    error_count = len(result.errors)
    skipped_count = len(result.skipped)

    print("\n" + "=" * 72)
    print(" TEST EXECUTION SUMMARY")
    print("=" * 72)
    print(f" Total Tests Run : {result.testsRun}")
    print(f" Passed          : {passed_count}")
    print(f" Failed          : {failed_count}")
    print(f" Errors          : {error_count}")
    print(f" Skipped         : {skipped_count}")
    print(f" Total Time      : {elapsed:.2f}s")
    print("=" * 72)

    if failed_count > 0 or error_count > 0:
        print("\nFAILURE / ERROR DETAILS:")
        for r in result.records:
            if r["status"] in ("FAIL", "ERROR"):
                print(f"\n--- [{r['status']}] {r['id']} ---")
                if r["error"]:
                    print(r["error"])

    # Write JSON report if requested
    if args.json_out:
        out_path = os.path.abspath(args.json_out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        report_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tier": args.tier,
            "total": result.testsRun,
            "passed": passed_count,
            "failed": failed_count,
            "errors": error_count,
            "skipped": skipped_count,
            "duration": round(elapsed, 4),
            "records": result.records
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        print(f"\n[REPORT] Saved structured JSON report to: {out_path}")

    if failed_count == 0 and error_count == 0:
        print("\n[SUCCESS] ALL E2E TESTS PASSED SUCCESSFULLY!")
        return 0
    else:
        print(f"\n[FAILED] {failed_count + error_count} TEST(S) ENCOUNTERED ISSUES.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
