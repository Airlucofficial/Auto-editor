#!/usr/bin/env python3
"""
Comprehensive Test Suite for AutoEditor Transcription & CapCut Caption Generator
"""

import os
import sys
import json
import urllib.request
import subprocess

PROJECT_DIR = r"d:\AutoEditor"
sys.path.insert(0, PROJECT_DIR)

import transcribe_engine

def run_tests():
    print("==================================================================")
    print(" STARTING COMPREHENSIVE AUTOEDITOR AI TEST SUITE")
    print("==================================================================")
    
    passed = 0
    failed = 0

    def assert_test(name, condition, details=""):
        nonlocal passed, failed
        if condition:
            print(f" [PASS] {name}")
            passed += 1
        else:
            print(f" [FAIL] {name}: {details}")
            failed += 1

    # TEST 1: Audio file existence
    sample_wav = os.path.join(PROJECT_DIR, "test_sample.wav")
    assert_test("Test sample audio file exists", os.path.exists(sample_wav), f"Path: {sample_wav}")

    # TEST 2: Transcription Engine Execution & Timestamps
    print("\n--- Testing Whisper Transcription ---")
    transcript = transcribe_engine.transcribe_audio(sample_wav, model_size="tiny")
    assert_test("Transcription returned dictionary", isinstance(transcript, dict))
    assert_test("Transcript has text", len(transcript.get("text", "")) > 0, transcript.get("text"))
    assert_test("Transcript has segments", len(transcript.get("segments", [])) > 0)
    
    first_seg = transcript.get("segments", [])[0]
    assert_test("Segment has timestamps", "start" in first_seg and "end" in first_seg)
    assert_test("Segment has word-level timestamps", len(first_seg.get("words", [])) > 0)

    # TEST 3: TXT Export
    print("\n--- Testing TXT Export ---")
    txt_out = os.path.join(PROJECT_DIR, "tests", "test_out.txt")
    transcribe_engine.export_to_txt(transcript, txt_out)
    assert_test("TXT file created", os.path.exists(txt_out))
    with open(txt_out, "r", encoding="utf-8") as f:
        txt_content = f.read()
    assert_test("TXT contains timestamp markers", "-->" in txt_content)
    assert_test("TXT contains dialogue", "Welcome" in txt_content or "Auto" in txt_content or "try" in txt_content.lower())

    # TEST 4: PDF Export
    print("\n--- Testing PDF Export ---")
    pdf_out = os.path.join(PROJECT_DIR, "tests", "test_out.pdf")
    transcribe_engine.export_to_pdf(transcript, pdf_out)
    assert_test("PDF file created", os.path.exists(pdf_out))
    assert_test("PDF file has non-zero size", os.path.getsize(pdf_out) > 1000)

    # TEST 5: All 8 CapCut Styles ASS Generation
    print("\n--- Testing CapCut Styles ASS Generation ---")
    styles = list(transcribe_engine.CAPTION_STYLES.keys())
    assert_test("Found at least 8 distinct styles", len(styles) >= 8, f"Total: {len(styles)}")

    for s in styles:
        ass_path = os.path.join(PROJECT_DIR, "tests", f"test_{s}.ass")
        transcribe_engine.generate_ass_subtitles(transcript, s, ass_path, 1920, 1080)
        assert_test(f"Style ASS generated: {s}", os.path.exists(ass_path) and os.path.getsize(ass_path) > 200)

    # TEST 6: FFmpeg Subtitle Burn-In
    print("\n--- Testing FFmpeg ASS Burn-In ---")
    ffmpeg_exe = os.path.join(PROJECT_DIR, "ffmpeg.exe")
    mp4_out = os.path.join(PROJECT_DIR, "tests", "test_burned.mp4")
    
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "lavfi", "-i", "color=c=black:s=640x360:d=3",
        "-i", sample_wav,
        "-vf", "ass=tests/test_hormozi_bold.ass",
        "-c:v", "libx264", "-t", "3",
        mp4_out
    ]
    res = subprocess.run(cmd, cwd=PROJECT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert_test("FFmpeg rendered burned video successfully", res.returncode == 0 and os.path.exists(mp4_out))

    # TEST 7: AI Server Endpoints
    print("\n--- Testing AI Companion Server API ---")
    try:
        req = urllib.request.urlopen("http://localhost:4001/api/health", timeout=5)
        health_data = json.loads(req.read().decode())
        assert_test("GET /api/health returned ok", health_data.get("ok") is True)
    except Exception as e:
        assert_test("GET /api/health accessible", False, str(e))

    try:
        req = urllib.request.urlopen("http://localhost:4001/api/styles", timeout=5)
        styles_data = json.loads(req.read().decode())
        assert_test("GET /api/styles returned 8 styles", len(styles_data) >= 8)
    except Exception as e:
        assert_test("GET /api/styles accessible", False, str(e))

    # TEST 8: Frontend Assets Verification
    print("\n--- Testing Frontend Assets ---")
    html_file = os.path.join(PROJECT_DIR, "out", "index.html")
    css_file = os.path.join(PROJECT_DIR, "out", "auto_captions.css")
    js_file = os.path.join(PROJECT_DIR, "out", "auto_captions.js")

    assert_test("out/index.html exists", os.path.exists(html_file))
    assert_test("out/auto_captions.css exists", os.path.exists(css_file))
    assert_test("out/auto_captions.js exists", os.path.exists(js_file))

    with open(html_file, "r", encoding="utf-8") as f:
        html_data = f.read()
    assert_test("index.html references auto_captions.css", "auto_captions.css" in html_data)
    assert_test("index.html references auto_captions.js", "auto_captions.js" in html_data)

    print("\n==================================================================")
    print(f" TEST RESULTS SUMMARY: {passed} PASSED, {failed} FAILED")
    print("==================================================================")

    if failed == 0:
        print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print(f"\n{failed} TEST(S) FAILED.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
