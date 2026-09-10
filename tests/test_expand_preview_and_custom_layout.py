#!/usr/bin/env python3
import os
import subprocess
import unittest

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class TestExpandPreviewAndCustomLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css_path = os.path.join(PROJECT_DIR, 'out', 'auto_captions.css')
        cls.js_path = os.path.join(PROJECT_DIR, 'out', 'auto_captions.js')
        cls.page_chunk_path = os.path.join(PROJECT_DIR, 'out', '_next', 'static', 'chunks', 'app', 'page-f2b7366e605a20db.js')
        
        with open(cls.css_path, 'r', encoding='utf-8') as f:
            cls.css = f.read()
        with open(cls.js_path, 'r', encoding='utf-8') as f:
            cls.js = f.read()
        with open(cls.page_chunk_path, 'r', encoding='utf-8') as f:
            cls.page = f.read()

    def test_expand_preview_css(self):
        self.assertIn('.editor.editor--expand-preview', self.css)
        self.assertIn('.btn-expand-preview', self.css)
        self.assertIn('.cap-expanded-preview-banner', self.css)

    def test_expand_preview_js(self):
        self.assertIn('function toggleExpandPreview()', self.js)
        self.assertIn('function injectExpandPreviewButton()', self.js)
        self.assertIn('btn-expand-preview-main', self.js)
        self.assertIn('cap-expanded-preview-banner', self.js)

    def test_playhead_react_hooks(self):
        self.assertIn('window._SEEK_TO', self.page)
        self.assertIn('window._GET_CURRENT_TIME', self.page)
        self.assertIn('window._TIMELINE_TOTAL_DURATION', self.page)

    def test_playhead_controller_js(self):
        self.assertIn('function initTimelinePlayheadController()', self.js)
        self.assertIn('setPointerCapture', self.js)
        self.assertIn('tl__playhead-grip', self.js)

    def test_playhead_css_pointer_events(self):
        self.assertIn('.tl__playhead', self.css)
        self.assertIn('.tl__playhead-grip', self.css)

    def test_splitters_css_and_js(self):
        self.assertIn('.editor-splitter--h', self.css)
        self.assertIn('.editor-splitter--v', self.css)
        self.assertIn('function injectLayoutSplitters()', self.js)

    def test_workspace_presets_and_menu(self):
        self.assertIn('function injectWorkspacePresets()', self.js)
        self.assertIn('function applyWorkspacePreset', self.js)
        self.assertIn('preview_focus', self.js)
        self.assertIn('btn-toggle-lock-layout', self.js)

    def test_syntax_integrity(self):
        r1 = subprocess.run(['node', '-c', self.js_path], capture_output=True)
        self.assertEqual(r1.returncode, 0)
        r2 = subprocess.run(['node', '-c', self.page_chunk_path], capture_output=True)
        self.assertEqual(r2.returncode, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
