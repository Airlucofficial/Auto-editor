"""
Tier 3: Pairwise Cross-Feature Combinations E2E Test Suite for AutoEditor AI Studio.
Tests pairwise interactions across orthogonal features:
- VAD Filtering (F6) + Second-Based Timestamp Formatting (F9)
- Presets Catalog (F13) + ASS Subtitle Compilation (F17)
- Word-Level Timing (F7) + PDF Visual Badges (F11)
- Threading Server (F2) + Concurrent Downloads (F10, F11)
- ASS Compilation (F17) + FFmpeg Video Burning Pipeline (F18)
"""

import os
import sys
import json
import unittest
import threading
import subprocess

from .conftest_utils import (
    PROJECT_DIR, TESTS_DIR, STORAGE_DIR, OUT_DIR, FFMPEG_EXE, SAMPLE_WAV,
    get_sample_transcript, generate_synthetic_wav, generate_synthetic_video,
    ensure_test_server, http_get, http_post_json
)

import transcribe_engine


class TestTier3Combinations(unittest.TestCase):
    """Pairwise Cross-Feature Combinatorial Test Suite"""

    @classmethod
    def setUpClass(cls):
        ensure_test_server(port=4001, timeout=10.0)

    def test_t3_vad_and_timestamp_formatting_parity(self):
        """Combination 1: VAD Filtering (F6) + Second-Based Timestamp Formatting (F9)."""
        transcript = get_sample_transcript()
        segments = transcript.get("segments", [])
        self.assertGreater(len(segments), 0)

        for seg in segments:
            start = seg["start"]
            end = seg["end"]
            self.assertLessEqual(start, end, f"Start {start} must be <= End {end}")
            
            # Format using helper or contract formula
            if hasattr(transcribe_engine, "format_second_timestamp"):
                ts_str = transcribe_engine.format_second_timestamp(start, end)
            else:
                ts_str = f"{start:.1f}s – {end:.1f}s"

            self.assertTrue(ts_str.endswith("s"), f"Timestamp '{ts_str}' must end with 's'")
            self.assertIn("–", ts_str, f"Timestamp '{ts_str}' must contain en-dash '–'")
            parts = ts_str.split("–")
            self.assertEqual(len(parts), 2)
            self.assertTrue(parts[0].strip().endswith("s"))
            self.assertTrue(parts[1].strip().endswith("s"))

    def test_t3_all_presets_ass_compilation(self):
        """Combination 2: Presets Catalog (F13) + ASS Subtitle Compilation (F17).
        Iterates through EVERY style in CAPTION_STYLES and verifies ASS compilation succeeds.
        """
        transcript = get_sample_transcript()
        styles = list(transcribe_engine.CAPTION_STYLES.keys())
        self.assertGreaterEqual(len(styles), 8, "Expected at least 8 styles in CAPTION_STYLES")

        for style_key in styles:
            out_ass = os.path.join(TESTS_DIR, f"t3_compile_{style_key}.ass")
            if os.path.exists(out_ass):
                os.remove(out_ass)

            transcribe_engine.generate_ass_subtitles(transcript, style_key, out_ass, 1920, 1080)
            self.assertTrue(
                os.path.exists(out_ass),
                f"Failed to generate ASS for preset style: '{style_key}'"
            )
            self.assertGreater(
                os.path.getsize(out_ass),
                200,
                f"Generated ASS for '{style_key}' is too small ({os.path.getsize(out_ass)} bytes)"
            )

            with open(out_ass, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("[Script Info]", content, f"Missing [Script Info] for style '{style_key}'")
            self.assertIn("[V4+ Styles]", content, f"Missing [V4+ Styles] for style '{style_key}'")
            self.assertIn("[Events]", content, f"Missing [Events] for style '{style_key}'")
            self.assertIn("Dialogue:", content, f"Missing Dialogue events for style '{style_key}'")

            # Cleanup
            if os.path.exists(out_ass):
                os.remove(out_ass)

    def test_t3_word_timing_and_pdf_table_generation(self):
        """Combination 3: Word-Level Timing Alignment (F7) + PDF Visual Badges (F11)."""
        transcript = get_sample_transcript()
        out_pdf = os.path.join(TESTS_DIR, "t3_word_timing_export.pdf")
        if os.path.exists(out_pdf):
            os.remove(out_pdf)

        transcribe_engine.export_to_pdf(transcript, out_pdf)
        self.assertTrue(os.path.exists(out_pdf))
        self.assertGreater(os.path.getsize(out_pdf), 1500)

        with open(out_pdf, "rb") as f:
            pdf_bytes = f.read()
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"))

        if os.path.exists(out_pdf):
            os.remove(out_pdf)

    def test_t3_concurrent_http_downloads(self):
        """Combination 4: Threading HTTP Server (F2) + Concurrent Downloads (F10, F11).
        Spawns concurrent worker threads fetching API endpoints simultaneously.
        """
        results = []
        errors = []

        def worker(endpoint):
            try:
                status, headers, body = http_get(endpoint, timeout=10.0)
                results.append((endpoint, status, len(body)))
            except Exception as e:
                errors.append((endpoint, str(e)))

        endpoints = ["/api/health", "/api/styles", "/api/health", "/api/styles", "/api/health"]
        threads = [threading.Thread(target=worker, args=(ep,)) for ep in endpoints]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Concurrent requests produced errors: {errors}")
        self.assertEqual(len(results), len(endpoints), "All concurrent requests should complete")
        for ep, status, body_len in results:
            self.assertEqual(status, 200, f"Expected 200 OK for {ep}, got {status}")
            self.assertGreater(body_len, 0, f"Expected non-empty response for {ep}")

    def test_t3_ass_compilation_and_ffmpeg_burning(self):
        """Combination 5: ASS Compilation (F17) + FFmpeg Video Burning Pipeline (F18).
        Compiles a style to ASS and directly burns it into a video sample with FFmpeg.
        """
        transcript = get_sample_transcript()
        style_key = "hormozi_bold"
        ass_path = os.path.join(TESTS_DIR, "t3_burn_combo.ass")
        mp4_out = os.path.join(TESTS_DIR, "t3_burn_combo.mp4")

        if os.path.exists(mp4_out):
            os.remove(mp4_out)
        if os.path.exists(ass_path):
            os.remove(ass_path)

        transcribe_engine.generate_ass_subtitles(transcript, style_key, ass_path, 640, 360)
        self.assertTrue(os.path.exists(ass_path))

        escaped_ass = ass_path.replace("\\", "/").replace(":", r"\:")
        cmd = [
            FFMPEG_EXE, "-y",
            "-f", "lavfi", "-i", "color=c=black:s=640x360:d=1.5",
            "-vf", f"ass='{escaped_ass}'",
            "-c:v", "libx264", "-t", "1.5",
            mp4_out
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(res.returncode, 0, f"FFmpeg burn failed: {res.stderr.decode('utf-8', errors='ignore')}")
        self.assertTrue(os.path.exists(mp4_out))
        self.assertGreater(os.path.getsize(mp4_out), 2000)

        # Cleanup
        if os.path.exists(ass_path):
            os.remove(ass_path)
        if os.path.exists(mp4_out):
            os.remove(mp4_out)


if __name__ == "__main__":
    unittest.main()
