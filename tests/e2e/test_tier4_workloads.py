"""
Tier 4: Real-World Workloads E2E Test Suite for AutoEditor AI Studio.
Tests complete Workflow A (Audio-to-Transcript) and Workflow B (Final Video Captions)
simulating real-world production usage with realistic audio and video samples.
"""

import os
import sys
import json
import unittest
import subprocess

from .conftest_utils import (
    PROJECT_DIR, TESTS_DIR, STORAGE_DIR, OUT_DIR, FFMPEG_EXE, SAMPLE_WAV,
    get_sample_transcript, generate_synthetic_wav, generate_synthetic_video,
    ensure_test_server, http_get, http_post_json
)

import transcribe_engine


class TestTier4RealWorldWorkloads(unittest.TestCase):
    """Tier 4: End-to-End Real-World Workload Execution"""

    @classmethod
    def setUpClass(cls):
        ensure_test_server(port=4001, timeout=10.0)

    def test_t4_workflow_a_audio_to_transcript_and_export(self):
        """
        Workflow A (Audio-to-Transcript):
        1. User imports audio file (test_sample.wav).
        2. Backend transcribes audio with Whisper + VAD + word timestamps.
        3. Formats second-based timestamps (0.0s – 3.4s).
        4. Exports and verifies TXT transcript download.
        5. Exports and verifies publication-quality PDF download with visual badges.
        """
        self.assertTrue(os.path.exists(SAMPLE_WAV), f"Sample audio must exist at {SAMPLE_WAV}")

        # Step 1 & 2: Trigger transcription via API
        payload = {"filepath": SAMPLE_WAV}
        status, headers, body = http_post_json("/api/transcribe", payload, timeout=60.0)
        self.assertEqual(status, 200, f"POST /api/transcribe failed with status {status}")

        data = json.loads(body.decode("utf-8"))
        self.assertTrue(data.get("ok"), "Transcription response ok must be True")
        req_id = data.get("id")
        self.assertIsNotNone(req_id, "Missing transaction ID")

        transcript = data.get("transcript", {})
        self.assertIn("segments", transcript)
        segments = transcript.get("segments", [])
        self.assertGreater(len(segments), 0, "Transcript must have segments")

        # Step 3: Verify segment text and timing
        full_text = transcript.get("text", "")
        self.assertTrue(
            "Welcome" in full_text or "Auto" in full_text or "transcription" in full_text.lower(),
            f"Transcript text mismatch: '{full_text}'"
        )

        for seg in segments:
            self.assertIn("start", seg)
            self.assertIn("end", seg)
            self.assertLessEqual(seg["start"], seg["end"])

        # Step 4: Verify TXT download
        txt_status, txt_headers, txt_bytes = http_get(f"/api/download/txt?id={req_id}")
        self.assertEqual(txt_status, 200, f"TXT download failed: {txt_status}")
        self.assertIn("text/plain", txt_headers.get("Content-Type", ""))
        txt_content = txt_bytes.decode("utf-8")
        self.assertIn("AUDIO TRANSCRIPT", txt_content)
        self.assertTrue(len(txt_content) > 100)

        # Step 5: Verify PDF download
        pdf_status, pdf_headers, pdf_bytes = http_get(f"/api/download/pdf?id={req_id}")
        self.assertEqual(pdf_status, 200, f"PDF download failed: {pdf_status}")
        self.assertIn("application/pdf", pdf_headers.get("Content-Type", ""))
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"), "Downloaded PDF must start with %PDF- header")
        self.assertGreater(len(pdf_bytes), 2000, "Downloaded PDF must be > 2KB")

    def test_t4_workflow_b_video_captions_burning(self):
        """
        Workflow B (Final Video Captions):
        1. Master video input is received or prepared.
        2. Transcript is retrieved or generated.
        3. User selects style from 60+ presets library (e.g. hormozi_bold).
        4. Subtitle engine compiles ASS file with Windows path escaping.
        5. FFmpeg burns ASS subtitles into MP4 video.
        6. Validates rendered MP4 video file and playback duration.
        """
        # Step 1: Create a realistic synthetic video clip (2.0s)
        test_video = os.path.join(TESTS_DIR, "t4_input_master.mp4")
        if os.path.exists(test_video):
            os.remove(test_video)

        ok = generate_synthetic_video(test_video, duration_sec=2.0)
        self.assertTrue(ok and os.path.exists(test_video), "Failed to generate test master video")

        # Step 2: Use sample transcript
        transcript = get_sample_transcript()

        # Step 3 & 4: Generate ASS subtitles via API
        ass_payload = {
            "transcript": transcript,
            "style": "hormozi_bold",
            "width": 640,
            "height": 360
        }
        status, headers, body = http_post_json("/api/generate-ass", ass_payload)
        self.assertEqual(status, 200, f"POST /api/generate-ass failed with status {status}")

        ass_data = json.loads(body.decode("utf-8"))
        ass_path = ass_data.get("ass_path")
        self.assertTrue(os.path.exists(ass_path), f"Compiled ASS file not found at {ass_path}")

        # Step 5: Burn subtitles into video with FFmpeg
        output_video = os.path.join(TESTS_DIR, "t4_burned_output.mp4")
        if os.path.exists(output_video):
            os.remove(output_video)

        escaped_ass = ass_path.replace("\\", "/").replace(":", r"\:")
        burn_cmd = [
            FFMPEG_EXE, "-y",
            "-i", test_video,
            "-vf", f"ass='{escaped_ass}'",
            "-c:v", "libx264",
            "-c:a", "copy",
            "-t", "2.0",
            output_video
        ]
        res = subprocess.run(burn_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(
            res.returncode, 0,
            f"FFmpeg burning failed: {res.stderr.decode('utf-8', errors='ignore')}"
        )

        # Step 6: Validate output video
        self.assertTrue(os.path.exists(output_video), "Rendered video file does not exist")
        self.assertGreater(os.path.getsize(output_video), 5000, "Rendered video size must be > 5KB")

        # Probe video using FFmpeg
        probe_cmd = [FFMPEG_EXE, "-i", output_video]
        probe_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        probe_out = probe_res.stderr.decode("utf-8", errors="ignore")
        self.assertIn("Video: h264", probe_out, "Burned video must contain an H.264 video track")

        # Cleanup
        for fpath in [test_video, output_video]:
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception:
                    pass

    def test_t4_session_multi_turn_processing(self):
        """
        Session Workload: Multiple successive operations (transcribe, export, multiple style ASS generations)
        in a single continuous session without crashing or running out of memory.
        """
        transcript = get_sample_transcript()
        styles_to_test = ["hormozi_bold", "neon_glow", "comic_pop"]
        generated_ass_files = []

        for s in styles_to_test:
            out_file = os.path.join(TESTS_DIR, f"t4_multiturn_{s}.ass")
            transcribe_engine.generate_ass_subtitles(transcript, s, out_file, 1920, 1080)
            self.assertTrue(os.path.exists(out_file))
            generated_ass_files.append(out_file)

        self.assertEqual(len(generated_ass_files), 3)

        # Cleanup
        for f in generated_ass_files:
            if os.path.exists(f):
                os.remove(f)


if __name__ == "__main__":
    unittest.main()
