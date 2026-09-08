#!/usr/bin/env python3
import os
import subprocess
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT_DIR, 'out')
JS_PATH = os.path.join(OUT_DIR, 'auto_captions.js')
CSS_PATH = os.path.join(OUT_DIR, 'auto_captions.css')
PAGE_CHUNK_PATH = os.path.join(OUT_DIR, '_next', 'static', 'chunks', 'app', 'page-f2b7366e605a20db.js')

class TestVerticalAndAudioFeatures(unittest.TestCase):

    def test_page_chunk_syntax(self):
        res = subprocess.run(['node', '-c', PAGE_CHUNK_PATH], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f'Page chunk syntax error: {res.stderr}')

    def test_auto_captions_js_syntax(self):
        res = subprocess.run(['node', '-c', JS_PATH], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f'auto_captions.js syntax error: {res.stderr}')

    def test_aspect_ratio_hooks_in_page_chunk(self):
        with open(PAGE_CHUNK_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('window._SET_ASPECT', content)
        self.assertIn('window._ASPECT', content)
        self.assertIn('window._TIMELINE_DURATION', content)

    def test_voiceover_audio_ref_in_page_chunk(self):
        with open(PAGE_CHUNK_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('window._VOICEOVER_AUDIO_EL', content)

    def test_video_elements_unmuted_in_page_chunk(self):
        with open(PAGE_CHUNK_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('n.muted=!1', content)
        self.assertIn('document.body.appendChild(n)', content)

    def test_aspect_controls_in_auto_captions_js(self):
        with open(JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('setProjectAspect', content)
        self.assertIn('applyAspectUI', content)
        self.assertIn('injectAspectControls', content)
        self.assertIn('btn-aspect-toggle', content)
        self.assertIn('btn-ratio-pill', content)
        self.assertIn('cap-vertical-mode', content)

    def test_audio_playback_functions_in_auto_captions_js(self):
        with open(JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('createSilentAudioUrl', content)
        self.assertIn('ensureEditorAudioReady', content)
        self.assertIn('setMasterVoiceVolume', content)
        self.assertIn('window._VOICEOVER_AUDIO_EL', content)

    def test_css_vertical_mode_and_aspect_styles(self):
        with open(CSS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('.cap-aspect-toggle-btn', content)
        self.assertIn('.cap-ratio-pill', content)
        self.assertIn('.editor.cap-vertical-mode', content)
        self.assertIn('aspect-ratio: 9/16', content)
        self.assertIn('9:16 Vertical', content)

    def test_node_silent_audio_generator(self):
        node_script = """
const sampleRate = 8000;
const numSamples = Math.ceil(sampleRate * 2);
const buffer = new ArrayBuffer(44 + numSamples * 2);
const view = new DataView(buffer);
view.setUint32(0, 0x52494646, false);
view.setUint32(4, 36 + numSamples * 2, true);
view.setUint32(8, 0x57415645, false);
view.setUint32(12, 0x666d7420, false);
view.setUint16(16, 16, true);
view.setUint16(20, 1, true);
view.setUint16(22, 1, true);
view.setUint32(24, sampleRate, true);
view.setUint32(28, sampleRate * 2, true);
view.setUint16(32, 2, true);
view.setUint16(34, 16, true);
view.setUint32(36, 0x64617461, false);
view.setUint32(40, numSamples * 2, true);
const buf = Buffer.from(buffer);
console.log(buf.length);
console.log(buf.toString('ascii', 0, 4));
console.log(buf.toString('ascii', 8, 12));
"""
        res = subprocess.run(['node', '-e', node_script], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        lines = res.stdout.strip().split('\n')
        self.assertEqual(int(lines[0]), 44 + 32000)
        self.assertEqual(lines[1], 'RIFF')
        self.assertEqual(lines[2], 'WAVE')

if __name__ == '__main__':
    unittest.main()
