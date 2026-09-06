#!/usr/bin/env python3
"""
AutoEditor Persistent Windows Background Service Manager
Monitors, auto-starts, and auto-recovers the AutoEditor AI Engine (api_server.py).
Runs headlessly via pythonw.exe using CREATE_NO_WINDOW | DETACHED_PROCESS.
"""

import os
import sys
import time
import json
import signal
import urllib.request
import subprocess
from datetime import datetime

# Ensure stdout and stderr are valid streams under pythonw (where they default to None)
if sys.stdout is None or not hasattr(sys.stdout, "write"):
    try:
        sys.stdout = open(os.devnull, "w", encoding="utf-8", errors="replace")
    except Exception:
        pass

if sys.stderr is None or not hasattr(sys.stderr, "write"):
    try:
        sys.stderr = open(os.devnull, "w", encoding="utf-8", errors="replace")
    except Exception:
        pass

# Configure UTF-8 encoding for Windows console to handle status emojis
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

SUPERVISOR_PID_FILE = os.path.join(STORAGE_DIR, "service_manager.pid")
API_PID_FILE = os.path.join(STORAGE_DIR, "api_server.pid")
LOG_FILE = os.path.join(STORAGE_DIR, "service_manager.log")

PORT = 4001
HEALTH_URL = f"http://127.0.0.1:{PORT}/api/health"

PYTHON_EXE = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
PYTHONW_EXE = os.path.join(BASE_DIR, ".venv", "Scripts", "pythonw.exe")
if not os.path.exists(PYTHONW_EXE):
    PYTHONW_EXE = PYTHON_EXE
if not os.path.exists(PYTHON_EXE):
    PYTHON_EXE = sys.executable

CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def check_health(timeout: float = 1.0) -> dict:
    try:
        req = urllib.request.Request(HEALTH_URL, headers={"Connection": "close"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            if res.status == 200:
                data = json.loads(res.read().decode("utf-8"))
                if data.get("ok") is True:
                    return data
    except Exception:
        pass
    return None

def is_pid_alive(pid: int) -> bool:
    if not pid or pid <= 0:
        return False
    try:
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if h:
            exit_code = ctypes.c_ulong()
            ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(exit_code))
            ctypes.windll.kernel32.CloseHandle(h)
            return exit_code.value == 259  # STILL_ACTIVE
        return False
    except Exception:
        pass
    try:
        res = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, creationflags=CREATE_NO_WINDOW
        )
        for line in res.stdout.strip().splitlines():
            if f'"{pid}"' in line:
                return True
        return False
    except Exception:
        return False

def get_startupinfo():
    if sys.platform == "win32":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        return si
    return None

def is_autoeditor_running() -> bool:
    try:
        # 1. First probe port 4000 directly (instant and reliable)
        req = urllib.request.Request("http://127.0.0.1:4000", headers={"Connection": "close"})
        with urllib.request.urlopen(req, timeout=0.6) as res:
            if res.status in (200, 301, 302, 404):
                return True
    except Exception:
        pass

    try:
        res = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq AutoEditor.exe", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, creationflags=CREATE_NO_WINDOW
        )
        for line in res.stdout.strip().splitlines():
            if "AutoEditor.exe" in line:
                return True
        return False
    except Exception:
        return True

def kill_pid(pid: int):
    if not pid or pid <= 0:
        return
    try:
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            capture_output=True, creationflags=CREATE_NO_WINDOW
        )
    except Exception:
        pass


def free_port(port: int = PORT):
    try:
        sup_pid = read_pid(SUPERVISOR_PID_FILE)
        my_pid = os.getpid()
        res = subprocess.run(
            f"netstat -ano -p tcp | findstr :{port}",
            shell=True, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW
        )
        killed_any = False
        for line in res.stdout.strip().splitlines():
            if "LISTENING" in line:
                parts = line.strip().split()
                pid = int(parts[-1])
                if pid > 0 and pid != my_pid and pid != sup_pid:
                    log(f"Freeing port {port}: terminating process {pid}")
                    kill_pid(pid)
                    killed_any = True
        if killed_any:
            time.sleep(0.2)
    except Exception:
        pass

def read_pid(path: str) -> int:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return int(f.read().strip())
    except Exception:
        pass
    return None

def write_pid(path: str, pid: int):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(pid))
    except Exception:
        pass

def remove_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def spawn_api_server() -> int:
    free_port(PORT)
    api_script = os.path.join(BASE_DIR, "api_server.py")
    cmd = [PYTHONW_EXE, api_script, str(PORT)]
    cmd_str = ' '.join(cmd)
    log(f"Spawning API server headlessly: {cmd_str}")
    api_log_path = os.path.join(STORAGE_DIR, "api_server.log")
    try:
        api_log_file = open(api_log_path, "a", encoding="utf-8")
    except Exception:
        api_log_file = subprocess.DEVNULL
    proc = subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        startupinfo=get_startupinfo(),
        creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
        stdout=api_log_file,
        stderr=api_log_file
    )
    write_pid(API_PID_FILE, proc.pid)
    log(f"API server spawned headlessly with PID: {proc.pid}")
    return proc.pid

def run_supervisor():
    my_pid = os.getpid()
    write_pid(SUPERVISOR_PID_FILE, my_pid)
    log(f"Supervisor started (PID: {my_pid})")

    def handle_exit(signum, frame):
        log(f"Supervisor received signal {signum}, shutting down...")
        api_pid = read_pid(API_PID_FILE)
        if api_pid and is_pid_alive(api_pid):
            kill_pid(api_pid)
        free_port(PORT)
        remove_file(SUPERVISOR_PID_FILE)
        remove_file(API_PID_FILE)
        sys.exit(0)

    try:
        signal.signal(signal.SIGTERM, handle_exit)
        signal.signal(signal.SIGINT, handle_exit)
    except Exception:
        pass

    # Initial check & spawn
    if not check_health(timeout=1.5):
        log("Initial health check failed. Spawning api_server...")
        spawn_api_server()
        # Wait up to 5 seconds
        for _ in range(10):
            time.sleep(0.5)
            h = check_health(timeout=1.0)
            if h:
                active_p = h.get("pid")
                if active_p:
                    write_pid(API_PID_FILE, active_p)
                log("API server healthy on initial spawn.")
                break

    autoeditor_seen = False
    consecutive_ae_missing = 0

    try:
        while True:
            time.sleep(1.0)
            
            # Auto-shutdown watchdog: if AutoEditor was running and is now stopped, terminate cleanly
            ae_alive = is_autoeditor_running()
            if ae_alive:
                autoeditor_seen = True
                consecutive_ae_missing = 0
            else:
                consecutive_ae_missing += 1

            # Auto-shutdown watchdog: only terminate if AutoEditor was running and has been confirmed absent for at least 60s
            if autoeditor_seen and consecutive_ae_missing >= 60:
                log("AutoEditor.exe and port 4000 have stopped for 60s. Automatically shutting down AI Engine...")
                handle_exit(0, None)
                break

            api_pid = read_pid(API_PID_FILE)
            pid_alive = is_pid_alive(api_pid) if api_pid else False

            if not pid_alive:
                # Fast path: process is dead or missing.
                # Check if a healthy API server is already running (PID drift/sync) before recovering
                health = check_health(timeout=0.15)
                if health is not None:
                    active_pid = health.get("pid")
                    if active_pid:
                        log(f"Watchdog PID sync: updating PID file from {api_pid} to {active_pid}")
                        write_pid(API_PID_FILE, active_pid)
                        continue

                log(f"Watchdog fast-path alert: api_pid={api_pid} is dead. Triggering immediate auto-recovery...")
                free_port(PORT)
                new_pid = spawn_api_server()

                # Verify recovered within 5 seconds
                recovered = False
                for _ in range(10):
                    time.sleep(0.3)
                    h = check_health(timeout=0.5)
                    if h:
                        active_p = h.get("pid")
                        if active_p:
                            write_pid(API_PID_FILE, active_p)
                        recovered = True
                        break

                if recovered:
                    log(f"Auto-recovery successful! API server running on PID {new_pid}.")
                else:
                    log(f"Auto-recovery warning: Health check still pending for PID {new_pid}.")
                continue

            # api_pid is alive: check server responsiveness
            health = check_health(timeout=1.0)
            if health is not None:
                # Server is healthy. Prevent desynchronization false kills
                active_pid = health.get("pid")
                if active_pid and active_pid != api_pid:
                    log(f"Watchdog PID sync: updating PID file from {api_pid} to {active_pid}")
                    write_pid(API_PID_FILE, active_pid)
                continue

            # Process is alive according to tasklist, but health check timed out.
            # May be busy processing heavy audio transcription or model loading.
            log(f"Watchdog alert: PID {api_pid} alive but health check timed out. Re-probing...")
            healthy = False
            for retry in range(4):
                time.sleep(1.5)
                re_health = check_health(timeout=1.5)
                if re_health is not None:
                    active_pid = re_health.get("pid")
                    if active_pid and active_pid != api_pid:
                        log(f"Watchdog PID sync: updating PID file from {api_pid} to {active_pid}")
                        write_pid(API_PID_FILE, active_pid)
                    healthy = True
                    break
                if not is_pid_alive(api_pid):
                    break
            if healthy:
                continue

            if not is_pid_alive(api_pid):
                continue  # Loop will immediately trigger fast-path recovery

            log(f"API server PID {api_pid} confirmed unresponsive after retries. Triggering auto-recovery...")
            kill_pid(api_pid)
            free_port(PORT)
            new_pid = spawn_api_server()

            recovered = False
            for _ in range(10):
                time.sleep(0.3)
                h = check_health(timeout=0.5)
                if h:
                    active_p = h.get("pid")
                    if active_p:
                        write_pid(API_PID_FILE, active_p)
                    recovered = True
                    break

            if recovered:
                log(f"Auto-recovery successful! API server running on PID {new_pid}.")
            else:
                log(f"Auto-recovery warning: Health check still pending for PID {new_pid}.")

    except KeyboardInterrupt:
        handle_exit(0, None)
    except Exception as e:
        import traceback
        log(f"Supervisor unhandled exception: {e}\n{traceback.format_exc()}")
    finally:
        remove_file(SUPERVISOR_PID_FILE)
        log("Supervisor exited.")

def start_command():
    sup_pid = read_pid(SUPERVISOR_PID_FILE)
    if sup_pid and is_pid_alive(sup_pid):
        health = check_health(timeout=1.0)
        if health:
            api_p = health.get('pid')
            print(f"🟢 AutoEditor AI Engine background service already running (Supervisor PID: {sup_pid}, API PID: {api_p}).")
            return 0

    print("Starting AutoEditor AI Engine persistent background service...")
    manager_script = os.path.abspath(__file__)
    cmd = [PYTHONW_EXE, manager_script, "run-supervisor"]
    
    try:
        sup_log_file = open(LOG_FILE, "a", encoding="utf-8")
    except Exception:
        sup_log_file = subprocess.DEVNULL
    proc = subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        startupinfo=get_startupinfo(),
        creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
        stdout=sup_log_file,
        stderr=sup_log_file
    )

    print(f"Launched background supervisor (PID: {proc.pid}). Waiting for AI Engine to become ready...")
    for _ in range(16):
        time.sleep(0.5)
        health = check_health(timeout=1.0)
        if health:
            api_p = health.get('pid')
            if api_p:
                write_pid(API_PID_FILE, api_p)
            print(f"🟢 AI Engine Ready! Listening on {HEALTH_URL} (API PID: {api_p})")
            return 0

    print("⚠️ Service started, but health response took longer than 6s. Check storage/service_manager.log.")
    return 1

def stop_command():
    print("Stopping AutoEditor AI Engine background service...")
    sup_pid = read_pid(SUPERVISOR_PID_FILE)
    if sup_pid and is_pid_alive(sup_pid):
        print(f"Terminating supervisor process (PID: {sup_pid})...")
        kill_pid(sup_pid)
    remove_file(SUPERVISOR_PID_FILE)

    api_pid = read_pid(API_PID_FILE)
    if api_pid and is_pid_alive(api_pid):
        print(f"Terminating API server process (PID: {api_pid})...")
        kill_pid(api_pid)
    remove_file(API_PID_FILE)

    free_port(PORT)
    print("🛑 AutoEditor AI Engine service stopped.")
    return 0

def status_command():
    sup_pid = read_pid(SUPERVISOR_PID_FILE)
    sup_alive = is_pid_alive(sup_pid) if sup_pid else False
    api_pid = read_pid(API_PID_FILE)
    api_alive = is_pid_alive(api_pid) if api_pid else False
    health = check_health(timeout=2.0)

    sup_status = 'Active' if sup_alive else 'Stopped'
    api_status = 'Active' if api_alive else 'Stopped'
    port_status = '🟢 Healthy (200 OK)' if health else '🔴 Offline / Unreachable'

    print("=======================================================")
    print(" AutoEditor AI Engine Background Service Status")
    print("=======================================================")
    print(f" Supervisor PID : {sup_pid} ({sup_status})")
    print(f" API Server PID : {api_pid} ({api_status})")
    print(f" Port {PORT} Status: {port_status}")
    if health:
        mc = 'Yes' if health.get('model_cached') else 'No'
        print(f" Model Cached   : {mc}")
        print(f" Service Name   : {health.get('service')}")
        print(f" Version        : {health.get('version')}")
    print("=======================================================")
    return 0 if health else 1

def restart_command():
    print("Restarting AutoEditor AI Engine background service...")
    stop_command()
    time.sleep(1.0)
    return start_command()

def main():
    if len(sys.argv) < 2:
        print("Usage: python service_manager.py [start|stop|restart|status]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "start":
        sys.exit(start_command())
    elif cmd == "stop":
        sys.exit(stop_command())
    elif cmd == "restart":
        sys.exit(restart_command())
    elif cmd == "status":
        sys.exit(status_command())
    elif cmd == "run-supervisor":
        run_supervisor()
    else:
        print(f"Unknown command: {cmd}")
        print("Available commands: start, stop, restart, status")
        sys.exit(1)

if __name__ == "__main__":
    main()
