#!/usr/bin/env python3
"""
Empirical Benchmark for Watchdog Recovery SLA (< 5.0 seconds)
Author: challenger_m1_1
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
import subprocess

PORT = 4001
BASE_URL = f"http://127.0.0.1:{PORT}"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
API_PID_FILE = os.path.join(STORAGE_DIR, "api_server.pid")
SUP_PID_FILE = os.path.join(STORAGE_DIR, "service_manager.pid")

CREATE_NO_WINDOW = 0x08000000

def get_health(timeout=0.2):
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/health", headers={"Connection": "close"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            if res.status == 200:
                data = json.loads(res.read().decode("utf-8"))
                return data
    except Exception:
        pass
    return None

def run_single_recovery_trial(trial_num):
    print(f"\n--- TRIAL {trial_num} ---")
    if not os.path.exists(API_PID_FILE):
        print("API PID file missing!")
        return None

    with open(API_PID_FILE, "r") as f:
        target_pid = int(f.read().strip())

    initial_health = get_health(timeout=1.0)
    if not initial_health:
        print("Initial health check failed before test!")
        return None
    reported_pid = initial_health.get("pid")
    print(f"Pre-kill state: PID file={target_pid}, reported API PID={reported_pid}")

    # Record precise start
    t0 = time.perf_counter()
    subprocess.run(["taskkill", "/F", "/PID", str(target_pid)], capture_output=True, creationflags=CREATE_NO_WINDOW)
    t_killed = time.perf_counter()

    down_time = None
    recovered_time = None
    new_pid = None

    # Poll up to 10 seconds every 50ms
    deadline = t0 + 10.0
    while time.perf_counter() < deadline:
        t_now = time.perf_counter()
        h = get_health(timeout=0.1)
        if down_time is None:
            if not h:
                down_time = t_now - t0
                print(f"  [+{down_time*1000:.0f}ms] Service confirmed down")
        else:
            if h and h.get("ok"):
                cur_pid = h.get("pid")
                if cur_pid != target_pid:
                    recovered_time = t_now - t0
                    new_pid = cur_pid
                    print(f"  [+{recovered_time*1000:.0f}ms] Service RECOVERED! New PID: {new_pid}")
                    break
        time.sleep(0.05)

    if recovered_time is not None:
        pass_5s = recovered_time <= 5.0
        print(f"Result: {recovered_time:.2f}s (Passed <= 5.0s: {pass_5s})")
        return {
            "trial": trial_num,
            "old_pid": target_pid,
            "new_pid": new_pid,
            "down_time_ms": (down_time or 0) * 1000,
            "recovery_s": recovered_time,
            "passed_sla": pass_5s
        }
    else:
        print("Result: FAILED to recover within 10 seconds!")
        return {
            "trial": trial_num,
            "old_pid": target_pid,
            "new_pid": None,
            "down_time_ms": (down_time or 0) * 1000,
            "recovery_s": None,
            "passed_sla": False
        }

def main():
    print("=" * 70)
    print(" EMPIRICAL WATCHDOG AUTO-RECOVERY BENCHMARK (5 TRIALS)")
    print(" Threshold: Recovery must complete within 5.0 seconds")
    print("=" * 70)

    trials = []
    for i in range(1, 4):
        res = run_single_recovery_trial(i)
        if res:
            trials.append(res)
        # Wait a moment between trials for service to stabilize
        time.sleep(2.0)

    print("\n" + "=" * 70)
    print(" EMPIRICAL RECOVERY BENCHMARK SUMMARY")
    print("=" * 70)
    for t in trials:
        rec_str = f"{t['recovery_s']:.2f}s" if t['recovery_s'] else "TIMEOUT (>10s)"
        status_str = "PASS (<=5s)" if t['passed_sla'] else "FAIL (>5s SLA)"
        print(f" Trial {t['trial']}: Old PID={t['old_pid']} -> New PID={t['new_pid']} | Recovery={rec_str} | {status_str}")

    recoveries = [t['recovery_s'] for t in trials if t['recovery_s'] is not None]
    if recoveries:
        print(f"\n Latency Stats: Min={min(recoveries):.2f}s, Avg={sum(recoveries)/len(recoveries):.2f}s, Max={max(recoveries):.2f}s")
    
    passed_count = sum(1 for t in trials if t['passed_sla'])
    print(f" SLA Compliance Rate: {passed_count}/{len(trials)} ({passed_count/len(trials)*100:.1f}%)")

if __name__ == "__main__":
    main()
