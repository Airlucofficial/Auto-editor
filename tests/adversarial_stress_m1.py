#!/usr/bin/env python3
"""
Adversarial Stress Test Suite for Milestone 1 (Server Concurrency, HTTP Resilience, Watchdog Recovery)
Author: challenger_m1_1
"""

import os
import sys
import time
import json
import socket
import urllib.request
import urllib.error
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

PORT = 4001
BASE_URL = f"http://127.0.0.1:{PORT}"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
API_PID_FILE = os.path.join(STORAGE_DIR, "api_server.pid")
SUP_PID_FILE = os.path.join(STORAGE_DIR, "service_manager.pid")

CREATE_NO_WINDOW = 0x08000000

def log_section(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def http_get(url, timeout=3.0):
    start = time.perf_counter()
    req = urllib.request.Request(url, headers={"Connection": "close"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            body = res.read()
            latency = (time.perf_counter() - start) * 1000.0
            return {
                "status": res.status,
                "body": body,
                "latency_ms": latency,
                "error": None
            }
    except urllib.error.HTTPError as e:
        latency = (time.perf_counter() - start) * 1000.0
        return {
            "status": e.code,
            "body": e.read(),
            "latency_ms": latency,
            "error": f"HTTPError: {e.code}"
        }
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000.0
        return {
            "status": None,
            "body": None,
            "latency_ms": latency,
            "error": str(e)
        }

def http_custom(method, path, body_bytes=None, headers=None, timeout=3.0):
    start = time.perf_counter()
    url = f"{BASE_URL}{path}"
    h = {"Connection": "close"}
    if headers:
        h.update(headers)
    
    req = urllib.request.Request(url, data=body_bytes, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            resp_body = res.read()
            latency = (time.perf_counter() - start) * 1000.0
            return {
                "status": res.status,
                "body": resp_body,
                "latency_ms": latency,
                "error": None
            }
    except urllib.error.HTTPError as e:
        latency = (time.perf_counter() - start) * 1000.0
        return {
            "status": e.code,
            "body": e.read(),
            "latency_ms": latency,
            "error": f"HTTPError {e.code}"
        }
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000.0
        return {
            "status": None,
            "body": None,
            "latency_ms": latency,
            "error": str(e)
        }

def raw_socket_request(raw_bytes, timeout=3.0):
    """Sends raw bytes over a TCP socket to test malformed/partial protocols."""
    start = time.perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(("127.0.0.1", PORT))
        s.sendall(raw_bytes)
        resp = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
            except socket.timeout:
                break
        latency = (time.perf_counter() - start) * 1000.0
        return {"response": resp, "latency_ms": latency, "error": None}
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000.0
        return {"response": None, "latency_ms": latency, "error": str(e)}
    finally:
        try:
            s.close()
        except Exception:
            pass

# -------------------------------------------------------------
# TEST 1: Concurrency Benchmarks
# -------------------------------------------------------------
def test_concurrency():
    log_section("TEST SUITE 1: Rapid HTTP Concurrency (25 & 50 requests)")

    for n_req in [25, 50]:
        print(f"\n--> Running {n_req} concurrent requests to GET /api/health...")
        results = []
        wall_start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=n_req) as executor:
            futures = [executor.submit(http_get, f"{BASE_URL}/api/health") for _ in range(n_req)]
            for f in as_completed(futures):
                results.append(f.result())
        wall_duration = (time.perf_counter() - wall_start) * 1000.0

        statuses = [r["status"] for r in results]
        errors = [r["error"] for r in results if r["error"] is not None]
        latencies = sorted([r["latency_ms"] for r in results])
        p50 = latencies[len(latencies) // 2]
        p95 = latencies[int(len(latencies) * 0.95)]
        avg = sum(latencies) / len(latencies)

        print(f"    Completed: {len(results)}/{n_req} in {wall_duration:.1f}ms")
        print(f"    Status Codes: 200 OK: {statuses.count(200)}, Others: {len(statuses) - statuses.count(200)}")
        print(f"    Errors/Timeouts: {len(errors)}")
        print(f"    Latency Stats (ms): Min={min(latencies):.2f}, Avg={avg:.2f}, Median={p50:.2f}, P95={p95:.2f}, Max={max(latencies):.2f}")

        assert statuses.count(200) == n_req, f"Expected {n_req} 200 OK responses, got {statuses.count(200)}"
        assert len(errors) == 0, f"Expected 0 connection errors, got {len(errors)}: {errors}"
        print(f"    [PASS] Concurrency {n_req} requests succeeded with 0 dropped connections.")

    # Mixed concurrent endpoints
    print("\n--> Running 30 mixed concurrent requests (/api/health, /api/styles, /api/download/txt?id=missing)...")
    endpoints = [
        f"{BASE_URL}/api/health",
        f"{BASE_URL}/api/styles",
        f"{BASE_URL}/api/styles?category=viral+shorts",
        f"{BASE_URL}/api/download/txt?id=missing_id_probe",
        f"{BASE_URL}/api/download/pdf?id=missing_id_probe"
    ] * 6  # 30 requests total

    results = []
    wall_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(http_get, ep) for ep in endpoints]
        for f in as_completed(futures):
            results.append(f.result())
    wall_duration = (time.perf_counter() - wall_start) * 1000.0

    errors = [r["error"] for r in results if r["status"] not in (200, 404)]
    print(f"    Completed: {len(results)}/30 mixed requests in {wall_duration:.1f}ms")
    print(f"    Status breakdown: 200 OK: {sum(1 for r in results if r['status']==200)}, 404: {sum(1 for r in results if r['status']==404)}, Unexpected: {len(errors)}")
    assert len(errors) == 0, f"Unexpected errors in mixed concurrency: {errors}"
    print("    [PASS] Mixed concurrency succeeded with 0 connection timeouts.")

# -------------------------------------------------------------
# TEST 2: Malformed Requests, Verbs & Boundary Handling
# -------------------------------------------------------------
def test_malformed_requests():
    log_section("TEST SUITE 2: Malformed Requests, Unsupported Verbs & Edge Cases")

    test_cases = [
        ("OPTIONS on /api/health", "OPTIONS", "/api/health", None, None, 200),
        ("GET with query params on /api/health", "GET", "/api/health?foo=bar&baz=123", None, None, 200),
        ("POST to GET-only endpoint /api/styles", "POST", "/api/styles", b'{"dummy":1}', {"Content-Type": "application/json"}, 404),
        ("DELETE verb on /api/health", "DELETE", "/api/health", None, None, 501),  # BaseHTTPRequestHandler default 501 or 404
        ("PUT verb on /api/styles", "PUT", "/api/styles", b'{"test":1}', {"Content-Type": "application/json"}, 501),
        ("PATCH verb on /api/transcribe", "PATCH", "/api/transcribe", b'{}', {"Content-Type": "application/json"}, 501),
        ("POST /api/generate-ass with malformed non-JSON body", "POST", "/api/generate-ass", b'{bad-json: broken', {"Content-Type": "application/json"}, 500),
        ("POST /api/generate-ass with missing transcript field", "POST", "/api/generate-ass", b'{"style": "hormozi_bold"}', {"Content-Type": "application/json"}, 400),
        ("POST /api/burn-captions with missing files", "POST", "/api/burn-captions", b'{"video_path":"nonexistent.mp4","ass_path":"nonexistent.ass"}', {"Content-Type": "application/json"}, 400),
        ("POST /api/burn-captions with malformed JSON", "POST", "/api/burn-captions", b'not json at all', {"Content-Type": "application/json"}, 500),
        ("POST /api/transcribe with missing audio part in multipart", "POST", "/api/transcribe", b'--boundary\r\nContent-Disposition: form-data; name="field"\r\n\r\nval\r\n--boundary--', {"Content-Type": "multipart/form-data; boundary=boundary"}, 400),
        ("POST /api/transcribe with missing filepath in JSON", "POST", "/api/transcribe", b'{"filepath":"storage/nonexistent_dummy_xyz.wav"}', {"Content-Type": "application/json"}, 400),
        ("GET /api/download/pdf without id parameter", "GET", "/api/download/pdf", None, None, 400),
        ("GET /api/download/txt without id parameter", "GET", "/api/download/txt", None, None, 400),
        ("GET /api/download/pdf with path traversal id", "GET", "/api/download/pdf?id=../../../../boot.ini", None, None, 404),
        ("GET nonexistent route /api/nonexistent_endpoint", "GET", "/api/nonexistent_endpoint", None, None, 404),
    ]

    for name, method, path, body, headers, expected_code in test_cases:
        res = http_custom(method, path, body_bytes=body, headers=headers)
        status = res["status"]
        if expected_code == 501:
            passed = status in (501, 404, 405)
        else:
            passed = status == expected_code
        status_msg = f"status={status} (expected {expected_code})"
        print(f"    [{'PASS' if passed else 'FAIL'}] {name}: {status_msg}, latency={res['latency_ms']:.1f}ms")
        assert passed, f"Test '{name}' failed: got status {status}, expected {expected_code}"

    # Raw socket edge cases: truncated HTTP request
    print("\n--> Testing raw socket malformed byte stream (truncated request)...")
    res_sock = raw_socket_request(b"GET /api/hea")
    print(f"    Socket closed/timeout cleanly, latency={res_sock['latency_ms']:.1f}ms")

    # Verify server is still alive and responsive after adversarial onslaught
    health = http_get(f"{BASE_URL}/api/health")
    assert health["status"] == 200, f"Server crashed or unresponsive after malformed requests! Health: {health}"
    print("    [PASS] Server remains 100% healthy and responsive after malformed requests.")

# -------------------------------------------------------------
# TEST 3: Process Kill & Watchdog Auto-Restart Latency
# -------------------------------------------------------------
def test_watchdog_auto_recovery():
    log_section("TEST SUITE 3: Forceful Process Kill & Watchdog Auto-Recovery (< 5.0s)")

    # Read current supervisor and API PID
    if not os.path.exists(SUP_PID_FILE) or not os.path.exists(API_PID_FILE):
        raise RuntimeError("PID files missing. Is service_manager running?")

    with open(SUP_PID_FILE, "r") as f:
        sup_pid = int(f.read().strip())
    with open(API_PID_FILE, "r") as f:
        old_api_pid = int(f.read().strip())

    print(f"    Supervisor PID : {sup_pid}")
    print(f"    Target API PID : {old_api_pid}")

    # Confirm initial health
    initial_health = http_get(f"{BASE_URL}/api/health", timeout=1.0)
    assert initial_health["status"] == 200, "Server is not healthy before kill test"
    print(f"    Pre-kill Health: 200 OK (PID reported by API: {json.loads(initial_health['body']).get('pid')})")

    # Force kill api_server.py
    print(f"\n--> Forcefully executing taskkill /F /PID {old_api_pid}...")
    kill_start = time.perf_counter()
    subprocess.run(["taskkill", "/F", "/PID", str(old_api_pid)], capture_output=True, creationflags=CREATE_NO_WINDOW)

    down_confirmed = False
    recovered = False
    new_api_pid = None
    recovery_latency = 0.0

    # Poll every 100ms for up to 6.0 seconds
    while (time.perf_counter() - kill_start) < 6.0:
        elapsed = time.perf_counter() - kill_start
        probe = http_get(f"{BASE_URL}/api/health", timeout=0.2)
        if not down_confirmed:
            if probe["status"] != 200:
                down_confirmed = True
                print(f"    [+{elapsed*1000:.0f}ms] Confirmed API server DOWN (error: {probe['error']})")
        else:
            if probe["status"] == 200:
                try:
                    data = json.loads(probe["body"])
                    reported_pid = data.get("pid")
                    if reported_pid and reported_pid != old_api_pid:
                        recovered = True
                        new_api_pid = reported_pid
                        recovery_latency = elapsed
                        print(f"    [+{elapsed*1000:.0f}ms] Confirmed API server RECOVERED! New PID: {new_api_pid}")
                        break
                except Exception:
                    pass
        time.sleep(0.1)

    print(f"\n--> Empirical Recovery Benchmark Results:")
    print(f"    Recovery Time       : {recovery_latency:.3f} seconds")
    print(f"    Requirement Limit   : <= 5.000 seconds")
    print(f"    Old PID             : {old_api_pid}")
    print(f"    New Active PID      : {new_api_pid}")
    print(f"    Down Confirmed      : {down_confirmed}")
    print(f"    Recovery Succeeded  : {recovered}")

    assert down_confirmed, "Failed to confirm API server down after kill"
    assert recovered, "Watchdog failed to recover API server within 6 seconds"
    assert recovery_latency <= 5.0, f"Recovery latency {recovery_latency:.2f}s exceeded 5.0s threshold!"
    assert new_api_pid != old_api_pid, f"PID did not change after recovery: {new_api_pid}"

    # Verify post-recovery server operations
    post_styles = http_get(f"{BASE_URL}/api/styles", timeout=1.0)
    assert post_styles["status"] == 200, "GET /api/styles failed on recovered server"
    print("    [PASS] Watchdog auto-recovery verified within strict 5-second boundary.")

def main():
    print("=" * 70)
    print(" ADVERSARIAL EMPIRICAL STRESS TEST SUITE — MILESTONE 1")
    print(" AutoEditor AI Engine & Persistent Windows Watchdog")
    print("=" * 70)

    try:
        test_concurrency()
        test_malformed_requests()
        test_watchdog_auto_recovery()

        print("\n" + "=" * 70)
        print(" ALL EMPIRICAL STRESS TESTS PASSED WITH 100% SUCCESS!")
        print("=" * 70)
        return 0
    except AssertionError as e:
        print("\n" + "!" * 70)
        print(f" STRESS TEST ASSERTION FAILED: {e}")
        print("!" * 70)
        return 1
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\n" + "!" * 70)
        print(f" STRESS TEST UNEXPECTED ERROR: {e}")
        print("!" * 70)
        return 2

if __name__ == "__main__":
    sys.exit(main())
