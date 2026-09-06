#!/usr/bin/env python3
"""
Test Suite for 0:05 vs 0-05 Timestamp Equivalence across AutoEditor
"""

import os
import sys
import json
import subprocess

PROJECT_DIR = r"d:\AutoEditor"

def run_tests():
    print("==================================================================")
    print(" VERIFYING 0:05 vs 0-05 TIMESTAMP EQUIVALENCE")
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

    js_chunk_path = os.path.join(PROJECT_DIR, "out", "_next", "static", "chunks", "app", "page-f2b7366e605a20db.js")

    # 1. Test Node execution of filename parser directly from bundle
    os.makedirs(os.path.join(PROJECT_DIR, "scratch"), exist_ok=True)
    node_script_file = os.path.join(PROJECT_DIR, "scratch", "eval_equiv.js")
    with open(node_script_file, "w", encoding="utf-8") as f:
        f.write("""
    const fs = require('fs');
    const content = fs.readFileSync('""" + js_chunk_path.replace("\\", "\\\\") + """', 'utf8');

    // Extract seconds function
    const secIdx = content.indexOf('seconds:function(e)');
    const endIdx = content.indexOf('(e.name)', secIdx);
    const fnStr = content.substring(secIdx + 'seconds:'.length, endIdx);
    const parseFn = eval('(' + fnStr + ')');

    // Extract function j
    const jIdx = content.indexOf('function j(e){');
    const jEnd = content.indexOf('}let y=e=>e&&e.box?1.5:1.16;', jIdx) + 1;
    const jStr = content.substring(jIdx, jEnd);
    const jFn = eval('(' + jStr + ')');

    const pairs = [
      ['0:05', '0-05', 5.0],
      ['0:05.png', '0-05.png', 5.0],
      ['0_05.png', '0-05.png', 5.0],
      ['0:00.png', '0-00.png', 0.0],
      ['0:28.png', '0-28.png', 28.0],
      ['0:05.5.mp4', '0-05.5.mp4', 5.5],
      ['1:02.mp4', '1-02.mp4', 62.0],
      ['1:05.png', '1-05.png', 65.0],
      ['scene 0:05.png', 'scene 0-05.png', 5.0],
      ['scene_0:05.png', 'scene_0-05.png', 5.0],
      ['scene-0:05.png', 'scene-0-05.png', 5.0],
      ['[0:05].png', '[0-05].png', 5.0],
      ['(0:05).png', '(0-05).png', 5.0],
      ['0:05 - intro.png', '0-05 - intro.png', 5.0],
      ['shot_1_0:05.png', 'shot_1_0-05.png', 5.0],
      ['0:05 scene.png', '0-05 scene.png', 5.0],
      ['0:05-video.mp4', '0-05-video.mp4', 5.0],
      ['0:05 to 0:10.mp4', '0-05 to 0-10.mp4', 5.0],
      ['0:05-0:10.mp4', '0-05-0-10.mp4', 5.0],
      ['0:05_0:10.mp4', '0-05_0-10.mp4', 5.0]
    ];

    const results = [];
    for (const [colon, hyphen, expected] of pairs) {
      const resColon = parseFn(colon);
      const resHyphen = parseFn(hyphen);
      const jColon = jFn(colon);
      const jHyphen = jFn(hyphen);
      results.push({
        colon,
        hyphen,
        expected,
        resColon,
        resHyphen,
        jColon,
        jHyphen,
        identical: resColon === resHyphen && resColon === expected
      });
    }

    console.log(JSON.stringify(results));
        """)

    res = subprocess.run(["node", node_script_file], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert_test("Evaluated equivalence pairs in Node", res.returncode == 0, res.stderr)

    if res.returncode == 0:
        data = json.loads(res.stdout.strip())
        for item in data:
            colon = item["colon"]
            hyphen = item["hyphen"]
            exp = item["expected"]
            c_val = item["resColon"]
            h_val = item["resHyphen"]
            assert_test(
                f"'{colon}' == '{hyphen}' == {exp}s",
                item["identical"],
                f"Colon: {c_val}, Hyphen: {h_val}"
            )
            # Also test jFn for pure timestamp tokens
            if colon in ["0:05", "1:02"]:
                assert_test(
                    f"j('{colon}') == j('{hyphen}') == {exp}s",
                    item["jColon"] == item["jHyphen"] == exp,
                    f"jColon: {item['jColon']}, jHyphen: {item['jHyphen']}"
                )

    print("==================================================================")
    print(f" EQUIVALENCE RESULTS: {passed} PASSED | {failed} FAILED")
    print("==================================================================")
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
