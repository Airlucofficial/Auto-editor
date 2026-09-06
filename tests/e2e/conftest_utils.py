"""
Shared test utilities, fixtures, and synthetic media generators for AutoEditor E2E tests.
"""

import os
import sys
import json
import time
import wave
import struct
import math
import shutil
import urllib.request
import urllib.error
import subprocess

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TESTS_DIR = os.path.join(PROJECT_DIR, "tests")
E2E_DIR = os.path.join(TESTS_DIR, "e2e")
STORAGE_DIR = os.path.join(PROJECT_DIR, "storage")
OUT_DIR = os.path.join(PROJECT_DIR, "out")
FFMPEG_EXE = os.path.join(PROJECT_DIR, "ffmpeg.exe")
SAMPLE_WAV = os.path.join(PROJECT_DIR, "test_sample.wav")
SAMPLE_TRANSCRIPT_JSON = os.path.join(PROJECT_DIR, "test_transcript.json")

# Ensure PROJECT_DIR is in sys.path
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

_SPAWNED_SERVER_PROC = None

def get_sample_transcript() -> dict:
    """Returns a valid, realistic transcript dictionary matching PROJECT.md contracts."""
    if os.path.exists(SAMPLE_TRANSCRIPT_JSON):
        with open(SAMPLE_TRANSCRIPT_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "audio_file": "test_sample.wav",
        "duration": 7.68,
        "language": "en",
        "total_words": 16,
        "text": "Welcome to Auto Editor. This is a high quality automated transcription test with timestamps.",
        "segments": [
            {
                "id": 1,
                "start": 0.0,
                "end": 2.24,
                "text": "Welcome to Auto Editor.",
                "words": [
                    {"word": "Welcome", "start": 0.0, "end": 0.52},
                    {"word": "to", "start": 0.52, "end": 0.78},
                    {"word": "Auto", "start": 0.78, "end": 1.54},
                    {"word": "Editor.", "start": 1.54, "end": 2.24}
                ]
            },
            {
                "id": 2,
                "start": 3.2,
                "end": 6.58,
                "text": "This is a high quality automated transcription test with timestamps.",
                "words": [
                    {"word": "This", "start": 3.2, "end": 3.38},
                    {"word": "is", "start": 3.38, "end": 3.60},
                    {"word": "a", "start": 3.60, "end": 3.72},
                    {"word": "high", "start": 3.72, "end": 3.86},
                    {"word": "quality", "start": 3.86, "end": 4.26},
                    {"word": "automated", "start": 4.26, "end": 4.78},
                    {"word": "transcription", "start": 4.78, "end": 5.42},
                    {"word": "test", "start": 5.42, "end": 5.90},
                    {"word": "with", "start": 5.90, "end": 6.14},
                    {"word": "timestamps.", "start": 6.14, "end": 6.58}
                ]
            }
        ]
    }

def generate_synthetic_wav(output_path: str, duration_sec: float = 1.0, freq: float = 440.0, is_silence: bool = False):
    """Generates a standard PCM WAV audio file using standard library."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    sample_rate = 16000
    num_samples = int(sample_rate * duration_sec)
    
    with wave.open(output_path, "w") as wav_file:
        wav_file.setnchannels(1)       # Mono
        wav_file.setsampwidth(2)      # 16-bit
        wav_file.setframerate(sample_rate)
        
        frames = bytearray()
        for i in range(num_samples):
            if is_silence:
                sample_val = 0
            else:
                t = float(i) / sample_rate
                sample_val = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * freq * t))
            frames.extend(struct.pack("<h", sample_val))
        
        wav_file.writeframes(frames)

def generate_synthetic_video(output_path: str, duration_sec: float = 2.0) -> bool:
    """Generates a synthetic MP4 video using ffmpeg.exe if available."""
    if not os.path.exists(FFMPEG_EXE):
        return False
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "lavfi", "-i", f"color=c=navy:s=320x240:d={duration_sec}",
        "-f", "lavfi", "-i", f"sine=f=440:d={duration_sec}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode == 0 and os.path.exists(output_path)

def probe_http_health(port: int = 4001, timeout: float = 1.0) -> bool:
    """Checks if http://127.0.0.1:{port}/api/health returns 200 OK."""
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/health")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("ok") is True
    except Exception:
        return False
    return False

def ensure_test_server(port: int = 4001, timeout: float = 10.0):
    """
    Ensures that api_server.py is running. If not running, launches it as a background process.
    """
    global _SPAWNED_SERVER_PROC
    if probe_http_health(port=port, timeout=1.0):
        return None

    api_server_py = os.path.join(PROJECT_DIR, "api_server.py")
    python_exe = sys.executable
    _SPAWNED_SERVER_PROC = subprocess.Popen(
        [python_exe, api_server_py, str(port)],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    deadline = time.time() + timeout
    while time.time() < deadline:
        if probe_http_health(port=port, timeout=0.5):
            return _SPAWNED_SERVER_PROC
        time.sleep(0.5)

    return _SPAWNED_SERVER_PROC

def stop_test_server():
    """Stops the test server process if it was spawned by this test session."""
    global _SPAWNED_SERVER_PROC
    if _SPAWNED_SERVER_PROC:
        try:
            _SPAWNED_SERVER_PROC.terminate()
            _SPAWNED_SERVER_PROC.wait(timeout=3)
        except Exception:
            try:
                _SPAWNED_SERVER_PROC.kill()
            except Exception:
                pass
        _SPAWNED_SERVER_PROC = None

def http_get(path: str, port: int = 4001, timeout: float = 5.0) -> tuple:
    """Executes a GET request returning (status, headers_dict, body_bytes)."""
    url = f"http://127.0.0.1:{port}{path}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            headers = dict(resp.getheaders())
            body = resp.read()
            return resp.status, headers, body
    except urllib.error.HTTPError as e:
        headers = dict(e.headers)
        body = e.read()
        return e.code, headers, body
    except urllib.error.URLError as e:
        return 0, {}, str(e).encode("utf-8")

def http_post_json(path: str, payload: dict, port: int = 4001, timeout: float = 15.0) -> tuple:
    """Executes a POST request with JSON payload returning (status, headers_dict, body_bytes)."""
    url = f"http://127.0.0.1:{port}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            headers = dict(resp.getheaders())
            body = resp.read()
            return resp.status, headers, body
    except urllib.error.HTTPError as e:
        headers = dict(e.headers)
        body = e.read()
        return e.code, headers, body
    except urllib.error.URLError as e:
        return 0, {}, str(e).encode("utf-8")
