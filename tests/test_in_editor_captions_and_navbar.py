#!/usr/bin/env python3
"""
Test Suite for In-Editor Auto-Captions and Navbar Icon Removal
"""
import os
import sys
import subprocess

PROJECT_DIR = r"d:\AutoEditor"

def run_tests():
    print("==================================================================")
    print(" VERIFYING IN-EDITOR CAPTIONS & NAVBAR CLEANUP")
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

    # 1. Check out/index.html for complete absence of Discord and Extension links
    index_html_path = os.path.join(PROJECT_DIR, "out", "index.html")
    with open(index_html_path, "r", encoding="utf-8") as f:
        index_html = f.read()
    assert_test("out/index.html does not contain dc-link", "dc-link" not in index_html)
    assert_test("out/index.html does not contain ext-link", "ext-link" not in index_html)
    assert_test("out/index.html does not contain discord.gg", "discord.gg" not in index_html)
    assert_test("out/index.html does not contain chromewebstore", "chromewebstore" not in index_html)
    assert_test("out/index.html includes auto_captions.css", "auto_captions.css" in index_html)
    assert_test("out/index.html includes auto_captions.js", "auto_captions.js" in index_html)

    # 2. Check page-f2b7366e605a20db.js React chunk
    chunk_path = os.path.join(PROJECT_DIR, "out", "_next", "static", "chunks", "app", "page-f2b7366e605a20db.js")
    with open(chunk_path, "r", encoding="utf-8") as f:
        chunk_content = f.read()
    assert_test("React page chunk does not contain dc-link", "dc-link" not in chunk_content)
    assert_test("React page chunk does not contain ext-link", "ext-link" not in chunk_content)
    assert_test("React page chunk does not contain discord.gg", "discord.gg" not in chunk_content)

    # 3. Check CSS hiding rules
    css_path = os.path.join(PROJECT_DIR, "out", "auto_captions.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    assert_test("CSS hides dc-link and ext-link with display: none !important",
                ".dc-link, .ext-link" in css_content and "display: none !important" in css_content)
    assert_test("CSS contains in-editor generate button styles", ".cap-ai-generate-btn" in css_content)
    assert_test("CSS contains in-editor presets styles", ".cap-editor-presets-section" in css_content)

    # 4. Check auto_captions.js for in-editor features
    js_path = os.path.join(PROJECT_DIR, "out", "auto_captions.js")
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()
    assert_test("auto_captions.js contains removeUnwantedLinks", "removeUnwantedLinks" in js_content)
    assert_test("auto_captions.js contains handleInEditorGenerateCaptions", "handleInEditorGenerateCaptions" in js_content)
    assert_test("auto_captions.js contains injectCaptionsIntoEditor", "injectCaptionsIntoEditor" in js_content)
    assert_test("auto_captions.js contains segmentsToSRT", "segmentsToSRT" in js_content)
    assert_test("auto_captions.js contains getVoiceoverAudio", "getVoiceoverAudio" in js_content)
    assert_test("auto_captions.js contains FEATURED_EDITOR_PRESETS", "FEATURED_EDITOR_PRESETS" in js_content)
    assert_test("auto_captions.js contains all 64 presets", js_content.count('"id": "') >= 64)

    # 5. Check JS syntax with node -c
    node_res_js = subprocess.run(["node", "-c", js_path], capture_output=True, text=True)
    assert_test("auto_captions.js passes node syntax check", node_res_js.returncode == 0, node_res_js.stderr)

    node_res_chunk = subprocess.run(["node", "-c", chunk_path], capture_output=True, text=True)
    assert_test("React page chunk passes node syntax check", node_res_chunk.returncode == 0, node_res_chunk.stderr)

    print("\n==================================================================")
    print(f" RESULTS: {passed} PASSED | {failed} FAILED")
    print("==================================================================")
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
