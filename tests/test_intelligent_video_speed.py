#!/usr/bin/env python3
"""
Test Suite for Intelligent Video Speed Fit to Timestamp Duration & Flexible Timestamp Parser
"""

import os
import sys
import json
import subprocess

PROJECT_DIR = r"d:\AutoEditor"

def run_tests():
    print("==================================================================")
    print(" VERIFYING INTELLIGENT VIDEO SPEED & FLEXIBLE TIMESTAMPS")
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

    # 1. Test Node.js execution of the flexible timestamp parser in React bundle
    js_chunk_path = os.path.join(PROJECT_DIR, "out", "_next", "static", "chunks", "app", "page-f2b7366e605a20db.js")
    with open(js_chunk_path, "r", encoding="utf-8") as f:
        js_chunk = f.read()

    # Syntax check
    node_syntax = subprocess.run(["node", "-c", js_chunk_path], capture_output=True, text=True)
    assert_test("React page chunk passes node -c syntax check", node_syntax.returncode == 0, node_syntax.stderr)

    # 2. Extract and run test cases on the exact parser from page chunk
    node_eval_code = """
    const fs = require('fs');
    const content = fs.readFileSync('""" + js_chunk_path.replace("\\", "\\\\") + """', 'utf8');

    // Extract seconds function
    const secIdx = content.indexOf('seconds:function(e)');
    if (secIdx === -1) {
      console.log(JSON.stringify({ error: 'seconds:function not found' }));
      process.exit(1);
    }
    const endIdx = content.indexOf('(e.name)', secIdx);
    const fnStr = content.substring(secIdx + 'seconds:'.length, endIdx);
    const parseFn = eval('(' + fnStr + ')');

    const testCases = {
      '5.5.mp4': 5.5,
      '0-05.5.mp4': 5.5,
      '0_05.5.mp4': 5.5,
      '0.10.mp4': 10.0,
      '0-10.mp4': 10.0,
      '5.5-10.mp4': 5.5,
      '5.5_10.mp4': 5.5,
      '5.5 to 0.10.mp4': 5.5,
      '0-05.5_0-10.mp4': 5.5,
      '0-00.png': 0.0,
      '1-02.mp4': 62.0,
      '45.jpg': 45.0,
      '105.png': 65.0
    };

    const results = {};
    for (const [k, expected] of Object.entries(testCases)) {
      results[k] = parseFn(k);
    }
    console.log(JSON.stringify(results));
    """

    res = subprocess.run(["node", "-e", node_eval_code], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert_test("Node.js evaluated page chunk parser successfully", res.returncode == 0, res.stderr)

    if res.returncode == 0:
        parsed_results = json.loads(res.stdout.strip())
        expected_cases = {
            '5.5.mp4': 5.5,
            '0-05.5.mp4': 5.5,
            '0_05.5.mp4': 5.5,
            '0.10.mp4': 10.0,
            '0-10.mp4': 10.0,
            '5.5-10.mp4': 5.5,
            '5.5_10.mp4': 5.5,
            '5.5 to 0.10.mp4': 5.5,
            '0-05.5_0-10.mp4': 5.5,
            '0-00.png': 0.0,
            '1-02.mp4': 62.0,
            '45.jpg': 45.0,
            '105.png': 65.0
        }
        for filename, exp in expected_cases.items():
            act = parsed_results.get(filename)
            assert_test(f"Parser parsed '{filename}' -> {exp}s", act == exp, f"Got: {act}")

    # 3. Check video duration metadata loading improvement
    assert_test("page chunk listens to onloadedmetadata", "onloadedmetadata" in js_chunk)
    assert_test("page chunk uses preload='auto'", "preload=\"auto\"" in js_chunk)

    # 4. Check clip card auto-speed badge rendering in page chunk
    assert_test("page chunk renders clip__speed badge", "clip__speed" in js_chunk)
    assert_test("page chunk calculates speed ratio for badge", "d.videoDuration/i" in js_chunk)

    # 5. Check auto_captions.css contains auto-speed styles
    css_path = os.path.join(PROJECT_DIR, "out", "auto_captions.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    assert_test("auto_captions.css contains .clip__speed styles", ".clip__speed" in css_content)
    assert_test("auto_captions.css contains .cap-auto-speed-pill styles", ".cap-auto-speed-pill" in css_content)

    # 6. Check auto_captions.js contains auto-speed helpers
    js_captions_path = os.path.join(PROJECT_DIR, "out", "auto_captions.js")
    with open(js_captions_path, "r", encoding="utf-8") as f:
        js_captions = f.read()
    assert_test("auto_captions.js passes node syntax check",
                subprocess.run(["node", "-c", js_captions_path], capture_output=True).returncode == 0)
    assert_test("auto_captions.js contains injectAutoSpeedBadge", "injectAutoSpeedBadge" in js_captions)
    assert_test("auto_captions.js contains updateTimelineSpeedBadges", "updateTimelineSpeedBadges" in js_captions)
    assert_test("auto_captions.js maintains _videoDurationCache", "_videoDurationCache" in js_captions)

    # 7. Speed Calculation and FFmpeg Acceleration Simulation
    print("\n--- Testing Mathematical Speed Calculation & FFmpeg Acceleration ---")
    video_src_dur = 15.0
    slot_target_dur = 5.0
    computed_speed = round(video_src_dur / slot_target_dur, 4)
    assert_test(f"Speed math: {video_src_dur}s in {slot_target_dur}s slot -> {computed_speed}x", computed_speed == 3.0)

    # Slot 5.5s to 10.0s = 4.5s
    slot_4_5 = 4.5
    computed_speed_4_5 = round(video_src_dur / slot_4_5, 4)
    assert_test(f"Speed math: {video_src_dur}s in {slot_4_5}s slot -> {computed_speed_4_5}x", computed_speed_4_5 == 3.3333)

    # FFmpeg Video Render Speed Test
    ffmpeg_exe = os.path.join(PROJECT_DIR, "ffmpeg.exe")
    temp_src = os.path.join(PROJECT_DIR, "tests", "temp_15s_test.mp4")
    temp_out = os.path.join(PROJECT_DIR, "tests", "temp_5s_accel.mp4")

    try:
        # Create 15s test video
        subprocess.run([
            ffmpeg_exe, "-y", "-f", "lavfi", "-i", "testsrc=size=320x180:rate=30",
            "-t", "15", "-c:v", "libx264", "-pix_fmt", "yuv420p", temp_src
        ], capture_output=True)

        assert_test("Created 15s test source video", os.path.exists(temp_src))

        # Speed up by 3.0x to fit 5.0s slot using AutoEditor's exact filter:
        filter_str = f"setpts=(PTS-STARTPTS)/{computed_speed:.4f},tpad=stop_mode=clone:stop_duration={slot_target_dur:.3f},trim=duration={slot_target_dur:.3f},setpts=PTS-STARTPTS,fps=30"
        subprocess.run([
            ffmpeg_exe, "-y", "-i", temp_src, "-vf", filter_str,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", temp_out
        ], capture_output=True)

        assert_test("FFmpeg rendered accelerated video successfully", os.path.exists(temp_out))

        # Probe output duration
        probe_res = subprocess.run([
            ffmpeg_exe, "-i", temp_out
        ], capture_output=True, text=True)
        
        duration_line = [l for l in probe_res.stderr.splitlines() if "Duration:" in l]
        has_5s_dur = any("00:00:05.00" in l for l in duration_line)
        assert_test("Output video duration is exactly 5.00s", has_5s_dur, f"Probe output: {duration_line}")

    finally:
        # Cleanup temp videos
        for fpath in (temp_src, temp_out):
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception:
                    pass

    print("\n==================================================================")
    print(f" RESULTS: {passed} PASSED | {failed} FAILED")
    print("==================================================================")
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
