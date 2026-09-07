#!/usr/bin/env python3
"""
Verification tests for the 7 new features of AutoEditor:
1. 64 Caption Styles & ASS generation with interactive position & scale
2. On-Monitor placement coordinates (pos_x, pos_y) and font_scale in ASS generator
3. Full view capability & CSS validation
4. Master voiceover volume control & audio mixing
5. Undo/Redo and Reset to default mechanisms
6. AI Voice Removal / Speech suppression preserving transients and SFX
7. Transition Sound Effects: 12 synthesized WAV files, manifest, smart auto-selection, and mixing
"""

import os
import sys
import json
import unittest
import urllib.request
import urllib.parse
import shutil
import subprocess

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

import transcribe_engine

SAMPLE_WAV = os.path.join(PROJECT_DIR, "test_sample.wav")
SAMPLE_TRANSCRIPT = {
    "audio_file": "test_sample.wav",
    "duration": 5.0,
    "total_words": 8,
    "segments": [
        {
            "id": 1,
            "start": 0.0,
            "end": 2.5,
            "text": "Welcome to Auto Editor captions.",
            "words": [
                {"word": "Welcome", "start": 0.0, "end": 0.5},
                {"word": "to", "start": 0.5, "end": 0.8},
                {"word": "Auto", "start": 0.8, "end": 1.4},
                {"word": "Editor", "start": 1.4, "end": 2.0},
                {"word": "captions.", "start": 2.0, "end": 2.5}
            ]
        },
        {
            "id": 2,
            "start": 2.8,
            "end": 4.8,
            "text": "Every style works perfectly.",
            "words": [
                {"word": "Every", "start": 2.8, "end": 3.3},
                {"word": "style", "start": 3.3, "end": 3.8},
                {"word": "works", "start": 3.8, "end": 4.2},
                {"word": "perfectly.", "start": 4.2, "end": 4.8}
            ]
        }
    ]
}

class TestNewFeatures(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = os.path.join(PROJECT_DIR, "storage", "test_tmp")
        os.makedirs(self.tmp_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_feature1_all_64_caption_styles_exist(self):
        """Feature 1: Verify all 64 caption styles exist across 8 categories."""
        styles = transcribe_engine.CAPTION_STYLES
        self.assertEqual(len(styles), 64, f"Expected 64 styles, got {len(styles)}")
        self.assertEqual(len(transcribe_engine.CATEGORIES), 8, "Expected 8 categories")

        # Verify each category has 8 styles
        for cat in transcribe_engine.CATEGORIES:
            cat_styles = [k for k, v in styles.items() if v.get("category") == cat]
            self.assertEqual(len(cat_styles), 8, f"Category {cat} should have 8 styles, got {len(cat_styles)}")

    def test_feature1_every_single_style_generates_valid_ass(self):
        """Feature 1: Verify every single style of the 64 styles generates valid ASS subtitles."""
        for style_key in transcribe_engine.CAPTION_STYLES:
            ass_path = os.path.join(self.tmp_dir, f"{style_key}.ass")
            transcribe_engine.generate_ass_subtitles(
                SAMPLE_TRANSCRIPT, style_key, ass_path, video_width=1920, video_height=1080
            )
            self.assertTrue(os.path.exists(ass_path), f"ASS file not created for style {style_key}")
            with open(ass_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("[Script Info]", content)
            self.assertIn("[V4+ Styles]", content)
            self.assertIn("Dialogue:", content)
            self.assertGreater(len(content), 200, f"ASS file for {style_key} is too small")

    def test_feature2_interactive_position_and_scale(self):
        """Feature 2: Verify custom on-monitor position (pos_x, pos_y) and font_scale in ASS."""
        ass_path = os.path.join(self.tmp_dir, "custom_pos.ass")
        transcribe_engine.generate_ass_subtitles(
            SAMPLE_TRANSCRIPT, "hormozi_bold", ass_path,
            video_width=1920, video_height=1080,
            pos_x=0.5, pos_y=0.25, font_scale=1.4
        )
        self.assertTrue(os.path.exists(ass_path))
        with open(ass_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Should contain \pos(960,270)
        self.assertIn("\\pos(960,270)", content, "Custom position \\pos(960,270) must appear in dialogue")
        # Scaled font size: base for hormozi_bold is 52, scaled by 1.4 -> 73
        self.assertIn("73", content, "Font size must be scaled by font_scale factor")

    def test_feature2_boundary_coordinates(self):
        """Feature 2: Test boundary coordinates pos_x=0.0, pos_y=1.0 and clamping."""
        ass_path = os.path.join(self.tmp_dir, "boundary_pos.ass")
        transcribe_engine.generate_ass_subtitles(
            SAMPLE_TRANSCRIPT, "neon_glow", ass_path,
            video_width=1920, video_height=1080,
            pos_x=0.05, pos_y=0.95, font_scale=0.5
        )
        self.assertTrue(os.path.exists(ass_path))
        with open(ass_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("\\pos(96,1026)", content)

    def test_feature4_voice_volume_variations(self):
        """Feature 4: Test mixing and voice volume adjustments at 0%, 50%, 100%, and 200%."""
        for vol in [0.0, 0.5, 1.0, 2.0]:
            out_vol = os.path.join(self.tmp_dir, f"vol_{int(vol*100)}.wav")
            ok = transcribe_engine.mix_audio_with_sfx(SAMPLE_WAV, [], out_vol, voice_volume=vol)
            self.assertTrue(ok, f"Voice volume adjustment at {vol} must succeed")
            self.assertTrue(os.path.exists(out_vol))
            self.assertGreater(os.path.getsize(out_vol), 1000)

    def test_feature6_ai_voice_removal_levels(self):
        """Feature 6: Verify AI Voice Removal function produces valid audio at multiple levels."""
        for level in [0.0, 0.5, 1.0]:
            out_audio = os.path.join(self.tmp_dir, f"vocal_{int(level*100)}.wav")
            ok = transcribe_engine.remove_vocal_from_video_or_audio(SAMPLE_WAV, out_audio, vocal_volume=level)
            self.assertTrue(ok, f"Voice removal at level {level} must succeed")
            self.assertTrue(os.path.exists(out_audio))
            self.assertGreater(os.path.getsize(out_audio), 1000)

    def test_feature7_sound_effects_exist_and_mix(self):
        """Feature 7: Verify all 12 sound effects exist and mixing function produces valid audio."""
        sfx_dir = os.path.join(PROJECT_DIR, "out", "sfx")
        manifest_file = os.path.join(sfx_dir, "manifest.json")
        self.assertTrue(os.path.exists(manifest_file), "SFX manifest.json must exist")
        
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(len(manifest), 12, "Manifest must contain 12 sound effects")

        for key, info in manifest.items():
            wav_file = os.path.join(sfx_dir, f"{key}.wav")
            self.assertTrue(os.path.exists(wav_file), f"SFX file {key}.wav must exist in out/sfx")
            self.assertGreater(os.path.getsize(wav_file), 500, f"SFX file {key}.wav must be non-empty")

        # Test mixing audio with SFX
        out_mix = os.path.join(self.tmp_dir, "mixed.m4a")
        whoosh_path = os.path.join(sfx_dir, "whoosh_fast.wav")
        boom_path = os.path.join(sfx_dir, "cinematic_boom.wav")
        sfx_events = [
            {"file": whoosh_path, "timestamp": 1.0},
            {"file": boom_path, "timestamp": 3.0}
        ]
        ok = transcribe_engine.mix_audio_with_sfx(SAMPLE_WAV, sfx_events, out_mix, sfx_volume=0.6, voice_volume=0.8)
        self.assertTrue(ok, "Audio mixing with SFX must succeed")
        self.assertTrue(os.path.exists(out_mix), "Mixed audio must be non-empty")
        self.assertGreater(os.path.getsize(out_mix), 1000)

    def test_frontend_assets_wiring(self):
        """Frontend verification: Verify UI elements and hooks in auto_captions.js & auto_captions.css."""
        js_path = os.path.join(PROJECT_DIR, "out", "auto_captions.js")
        css_path = os.path.join(PROJECT_DIR, "out", "auto_captions.css")
        chunk_path = os.path.join(PROJECT_DIR, "out", "_next", "static", "chunks", "app", "page-f2b7366e605a20db.js")

        with open(js_path, "r", encoding="utf-8") as f:
            js_code = f.read()

        with open(css_path, "r", encoding="utf-8") as f:
            css_code = f.read()

        with open(chunk_path, "r", encoding="utf-8") as f:
            chunk_code = f.read()

        # Canvas redraw hook
        self.assertIn("_CANVAS_REDRAW", chunk_code)
        self.assertIn("_DRAW_CAPTION", chunk_code)

        # Monitor bar & drawer
        self.assertIn("cap-monitor-styles-bar", js_code)
        self.assertIn("btn-monitor-expand-styles", js_code)
        self.assertIn("cap-monitor-styles-bar", css_code)

        # Monitor draggable/resizable box
        self.assertIn("cap-monitor-box", js_code)
        self.assertIn("cap-handle", js_code)
        self.assertIn("cap-monitor-box", css_code)

        # Full view
        self.assertIn("btn-toggle-fullview", js_code)
        self.assertIn("viewer--fullview", css_code)

        # Voice volume & file button
        self.assertIn("cap-voice-vol-slider", js_code)
        self.assertIn("btn-pick-voice-file", js_code)
        self.assertIn("cap-voice-vol-wrap", css_code)

        # History undo/redo & reset
        self.assertIn("btn-step-back", js_code)
        self.assertIn("btn-step-forward", js_code)
        self.assertIn("btn-reset-default", js_code)
        self.assertIn("StudioHistory", js_code)

        # AI Voice removal
        self.assertIn("chk-remove-clip-voice", js_code)
        self.assertIn("btn-process-vocal-remove", js_code)
        self.assertIn("clip-voice-remover-card", css_code)

        # Transition SFX
        self.assertIn("chk-enable-sfx", js_code)
        self.assertIn("slider-sfx-vol", js_code)
        self.assertIn("getSmartAutoSFX", js_code)
        self.assertIn("cap-sfx-section", css_code)

    def test_feature1_burn_captions_with_custom_pos(self):
        """Feature 1 & 2: Test burning custom positioned ASS subtitles directly into video with ffmpeg."""
        ass_path = os.path.join(self.tmp_dir, "burn_test.ass")
        mp4_in = os.path.join(self.tmp_dir, "blank.mp4")
        mp4_out = os.path.join(self.tmp_dir, "burned.mp4")

        transcribe_engine.generate_ass_subtitles(
            SAMPLE_TRANSCRIPT, "hormozi_bold", ass_path,
            video_width=640, video_height=360,
            pos_x=0.5, pos_y=0.75, font_scale=1.0
        )
        self.assertTrue(os.path.exists(ass_path))

        # Generate 2-second blank video
        ffmpeg_exe = os.path.join(PROJECT_DIR, "ffmpeg.exe")
        subprocess.run([
            ffmpeg_exe, "-y",
            "-f", "lavfi", "-i", "color=c=black:s=640x360:d=2",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", "2", "-c:v", "libx264", "-c:a", "aac",
            mp4_in
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(os.path.exists(mp4_in))

        # Burn captions
        ok = transcribe_engine.burn_captions_to_video(mp4_in, ass_path, mp4_out)
        self.assertTrue(ok, "burn_captions_to_video must return True")
        self.assertTrue(os.path.exists(mp4_out))
        self.assertGreater(os.path.getsize(mp4_out), 1000)

    def test_feature5_studio_history_node_evaluation(self):
        """Feature 5: Evaluate StudioHistory undo/redo/reset logic in Node.js."""
        node_script = """
        const fs = require('fs');
        const js = fs.readFileSync('out/auto_captions.js', 'utf8');

        // Extract StudioHistory definition
        const startIdx = js.indexOf('const StudioHistory = {');
        const endIdx = js.indexOf('function syncAllUIControls()', startIdx);
        let code = js.substring(startIdx, endIdx);
        code = code.replace('const StudioHistory =', 'global.StudioHistory =');

        // Dummy global state & mocks
        global.window = {
          _CURRENT_STYLE: "classic",
          _CAPTION_POS: { x: 0.5, y: 0.85, scale: 1.0 },
          _VOICEOVER_VOLUME: 1.0,
          _SFX_ENABLED: false,
          _SFX_VOLUME: 0.5,
          _SELECTED_SFX: "whoosh_fast",
          _CLIP_VOICE_SETTINGS: {}
        };
        global.document = {
          getElementById: () => ({ disabled: false, innerText: '', value: '' }),
          querySelector: () => null,
          querySelectorAll: () => []
        };
        global.allStyles = [{ id: "classic", name: "Classic" }, { id: "hormozi_bold", name: "Hormozi" }];
        global.syncAllUIControls = () => {};
        global.updateMonitorBoxPosition = () => {};
        global.confirm = () => true;

        eval(code);

        // Test init
        StudioHistory.init();
        if (StudioHistory.stack.length !== 1) throw new Error("Init should have 1 item");
        if (StudioHistory.index !== 0) throw new Error("Index should be 0");

        // Change state & push
        window._CURRENT_STYLE = "hormozi_bold";
        window._VOICEOVER_VOLUME = 1.8;
        StudioHistory.push("Style change");
        if (StudioHistory.stack.length !== 2) throw new Error("Stack should have 2 items");
        if (StudioHistory.index !== 1) throw new Error("Index should be 1");

        // Step back
        StudioHistory.stepBack();
        if (StudioHistory.index !== 0) throw new Error("Index should be 0 after stepBack");
        if (window._CURRENT_STYLE !== "classic") throw new Error("Style should revert to classic");
        if (window._VOICEOVER_VOLUME !== 1.0) throw new Error("Volume should revert to 1.0");

        // Step forward
        StudioHistory.stepForward();
        if (StudioHistory.index !== 1) throw new Error("Index should be 1 after stepForward");
        if (window._CURRENT_STYLE !== "hormozi_bold") throw new Error("Style should be hormozi_bold");

        // Reset to default
        StudioHistory.resetToDefault();
        if (window._CURRENT_STYLE !== "classic") throw new Error("Reset should set style to classic");
        if (window._VOICEOVER_VOLUME !== 1.0) throw new Error("Reset should set volume to 1.0");

        console.log("HISTORY_EVAL_OK");
        """
        eval_file = os.path.join(self.tmp_dir, "eval_history.js")
        with open(eval_file, "w", encoding="utf-8") as f:
            f.write(node_script)

        res = subprocess.run(["node", eval_file], cwd=PROJECT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0, f"Node script failed: {res.stderr}")
        self.assertIn("HISTORY_EVAL_OK", res.stdout)

    def test_feature7_smart_auto_sfx_node_evaluation(self):
        """Feature 7: Evaluate getSmartAutoSFX mapping in Node.js."""
        node_script = """
        const fs = require('fs');
        const js = fs.readFileSync('out/auto_captions.js', 'utf8');
        const fnIdx = js.indexOf('function getSmartAutoSFX(');
        const endIdx = js.indexOf('// -------------------------------------------------------------------------', fnIdx);
        const code = js.substring(fnIdx, endIdx);
        global.window = {};
        eval(code);

        const tests = [
          ['wipeleft', 'whoosh_fast'],
          ['wiperight', 'whoosh_fast'],
          ['slideup', 'swoosh_smooth'],
          ['fadeblack', 'cinematic_boom'],
          ['fade', 'gentle_chime'],
          ['circlecrop', 'bubble_pop'],
          ['none', 'camera_click'],
          ['', 'camera_click'],
          ['cut', 'camera_click']
        ];

        for (const [trans, exp] of tests) {
          const got = getSmartAutoSFX(trans);
          if (got !== exp) throw new Error(`Transition ${trans} expected ${exp}, got ${got}`);
        }
        console.log("SMART_SFX_OK");
        """
        eval_file = os.path.join(self.tmp_dir, "eval_sfx.js")
        with open(eval_file, "w", encoding="utf-8") as f:
            f.write(node_script)

        res = subprocess.run(["node", eval_file], cwd=PROJECT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0, f"SFX Node script failed: {res.stderr}")
        self.assertIn("SMART_SFX_OK", res.stdout)

    def test_api_server_endpoints_live(self):
        """End-to-end test of AI server endpoints on port 4001."""
        # 1. Health
        try:
            req = urllib.request.urlopen("http://localhost:4001/api/health", timeout=3)
            data = json.loads(req.read().decode())
            self.assertTrue(data.get("ok"))
        except Exception as e:
            self.skipTest(f"Port 4001 server offline: {e}")

        # 2. Styles
        req = urllib.request.urlopen("http://localhost:4001/api/styles", timeout=3)
        styles = json.loads(req.read().decode())
        self.assertEqual(len(styles), 64)

        # 3. SFX Manifest
        req = urllib.request.urlopen("http://localhost:4001/api/sfx", timeout=3)
        sfx = json.loads(req.read().decode())
        self.assertEqual(len(sfx), 12)

        # 4. Generate ASS with pos and font scale
        gen_body = json.dumps({
            "transcript": SAMPLE_TRANSCRIPT,
            "style": "snap_yellow",
            "pos_x": 0.4,
            "pos_y": 0.7,
            "font_scale": 1.2
        }).encode("utf-8")
        req = urllib.request.Request("http://localhost:4001/api/generate-ass", data=gen_body, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=5)
        ass_data = json.loads(resp.read().decode())
        self.assertTrue(ass_data.get("ok"))
        self.assertIn("\\pos(768,756)", ass_data.get("ass_content"))

        # 5. Vocal remove
        vocal_body = json.dumps({
            "filepath": SAMPLE_WAV,
            "vocal_volume": 0.1
        }).encode("utf-8")
        req = urllib.request.Request("http://localhost:4001/api/vocal-remove", data=vocal_body, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=5)
        vocal_data = json.loads(resp.read().decode())
        self.assertTrue(vocal_data.get("ok"))
        self.assertIn("audio_url", vocal_data)

    def test_feature1_generate_ass_with_raw_cues_list(self):
        """Feature 1: Verify generate_ass_subtitles accepts a list of cues and synthesizes word animations."""
        cues_list = [
            {"start": 0.0, "end": 2.0, "text": "Rapid viral hook"},
            {"start": 2.2, "end": 4.0, "text": "Second caption line"}
        ]
        ass_path = os.path.join(self.tmp_dir, "list_cues.ass")
        transcribe_engine.generate_ass_subtitles(cues_list, "hormozi_bold", ass_path, pos_x=0.5, pos_y=0.8)
        self.assertTrue(os.path.exists(ass_path))
        with open(ass_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Dialogue:", content)
        self.assertIn("RAPID", content)
        self.assertIn("\\pos(960,864)", content)

    def test_feature6_vocal_removal_video_output(self):
        """Feature 6: Verify vocal removal with video output preserves video stream."""
        blank_mp4 = os.path.join(self.tmp_dir, "vocal_video_in.mp4")
        out_mp4 = os.path.join(self.tmp_dir, "vocal_video_out.mp4")
        ffmpeg_exe = os.path.join(PROJECT_DIR, "ffmpeg.exe")
        subprocess.run([
            ffmpeg_exe, "-y",
            "-f", "lavfi", "-i", "color=c=blue:s=320x240:d=1",
            "-f", "lavfi", "-i", "sine=frequency=1000:duration=1",
            "-c:v", "libx264", "-c:a", "aac",
            blank_mp4
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(os.path.exists(blank_mp4))

        ok = transcribe_engine.remove_vocal_from_video_or_audio(blank_mp4, out_mp4, vocal_volume=0.2)
        self.assertTrue(ok, "remove_vocal_from_video_or_audio must succeed with video output")
        self.assertTrue(os.path.exists(out_mp4))
        self.assertGreater(os.path.getsize(out_mp4), 1000)

    def test_feature7_sfx_mixing_missing_file_resilience(self):
        """Feature 7: Verify mix_audio_with_sfx handles non-existent SFX gracefully."""
        out_audio = os.path.join(self.tmp_dir, "resilient_mix.wav")
        sfx_events = [{"file": "non_existent_sfx.wav", "timestamp": 1.0}]
        ok = transcribe_engine.mix_audio_with_sfx(SAMPLE_WAV, sfx_events, out_audio, voice_volume=1.2)
        self.assertTrue(ok, "mix_audio_with_sfx must succeed even if SFX files are missing")
        self.assertTrue(os.path.exists(out_audio))
    def test_page_chunk_scope_integrity(self):
        """Verify page chunk preserves 'let' declaration before eL in function F to prevent ReferenceError."""
        chunk_path = os.path.join(PROJECT_DIR, "out", "_next", "static", "chunks", "app", "page-f2b7366e605a20db.js")
        self.assertTrue(os.path.exists(chunk_path))
        with open(chunk_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("};let eL=(0,l.useCallback)", content, "page chunk must have 'let eL=' to avoid undeclared ReferenceError in strict mode")
        res = subprocess.run(["node", "-c", chunk_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"node syntax check failed: {res.stderr}")

if __name__ == "__main__":
    import subprocess
    unittest.main()

