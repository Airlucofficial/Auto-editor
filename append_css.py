#!/usr/bin/env python3
"""Appends enhanced studio CSS to out/auto_captions.css"""

css = """
/* ==========================================================================
   ENHANCED AUTOEDITOR STUDIO CONTROLS:
   1. 64 Caption Styles Expandable Drawer & Arrow Toggle
   2. On-Monitor Draggable & Resizable Caption Box
   3. Full View / Fullscreen Monitor
   4. Master Voiceover Volume Control
   5. Step Undo/Redo & Reset to Default
   6. Video Clip AI Voice Removal (Keep SFX & Clicks)
   7. Transition Sound Effects & Smart Auto-Selection
   ========================================================================== */

/* 1. Caption Presets Header with Arrow Toggle */
.cap-editor-presets-head {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-bottom: 8px !important;
  padding-bottom: 4px !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
}

.cap-editor-presets-title {
  font-size: 13px !important;
  font-weight: 700 !important;
  color: #e2e8f0 !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.cap-expand-arrow-btn {
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  background: rgba(168, 85, 247, 0.15) !important;
  border: 1px solid rgba(168, 85, 247, 0.35) !important;
  color: #c084fc !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  padding: 3px 9px !important;
  border-radius: 6px !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
}
.cap-expand-arrow-btn:hover {
  background: rgba(168, 85, 247, 0.28) !important;
  color: #ffffff !important;
  border-color: #a855f7 !important;
}
.cap-expand-arrow-btn .cap-arrow-icon {
  display: inline-block !important;
  transition: transform 0.2s ease !important;
  font-size: 10px !important;
}
.cap-expand-arrow-btn.is-expanded .cap-arrow-icon {
  transform: rotate(180deg) !important;
}

/* Collapsible 64 Styles Drawer */
.cap-presets-drawer {
  display: none;
  background: #0f131a !important;
  border: 1px solid #232936 !important;
  border-radius: 10px !important;
  padding: 10px !important;
  margin-top: 8px !important;
  margin-bottom: 12px !important;
  max-height: 420px !important;
  overflow-y: auto !important;
}
.cap-presets-drawer.is-open {
  display: block !important;
  animation: capDrawerSlide 0.2s ease-out !important;
}

@keyframes capDrawerSlide {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

.cap-drawer-search {
  width: 100% !important;
  background: #191f2c !important;
  border: 1px solid #2d3546 !important;
  border-radius: 6px !important;
  padding: 6px 10px !important;
  font-size: 12px !important;
  color: #ffffff !important;
  margin-bottom: 8px !important;
  box-sizing: border-box !important;
}
.cap-drawer-search:focus {
  outline: none !important;
  border-color: #a855f7 !important;
  box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2) !important;
}

.cap-drawer-categories {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 4px !important;
  margin-bottom: 10px !important;
}

.cap-drawer-pill {
  background: #1e2430 !important;
  border: 1px solid #2d3546 !important;
  color: #94a3b8 !important;
  font-size: 11px !important;
  padding: 3px 8px !important;
  border-radius: 4px !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
}
.cap-drawer-pill:hover {
  color: #f1f5f9 !important;
  background: #2a3346 !important;
}
.cap-drawer-pill.active {
  background: #a855f7 !important;
  border-color: #a855f7 !important;
  color: #ffffff !important;
  font-weight: 600 !important;
}

.cap-drawer-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)) !important;
  gap: 6px !important;
}

.cap-drawer-card {
  background: #171c26 !important;
  border: 1px solid #283042 !important;
  border-radius: 6px !important;
  padding: 6px 8px !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  text-align: center !important;
  user-select: none !important;
}
.cap-drawer-card:hover {
  border-color: #818cf8 !important;
  background: #1f2737 !important;
  transform: translateY(-1px) !important;
}
.cap-drawer-card.selected {
  border-color: #a855f7 !important;
  background: rgba(168, 85, 247, 0.18) !important;
  box-shadow: 0 0 0 1px #a855f7 !important;
}

.cap-drawer-card-name {
  font-size: 11.5px !important;
  font-weight: 700 !important;
  color: #e2e8f0 !important;
  margin-bottom: 3px !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}
.cap-drawer-card-cat {
  font-size: 9.5px !important;
  color: #818cf8 !important;
  text-transform: uppercase !important;
}

/* Active style indicator in sidebar */
.cap-active-indicator {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  background: rgba(168, 85, 247, 0.12) !important;
  border: 1px solid rgba(168, 85, 247, 0.3) !important;
  border-radius: 6px !important;
  padding: 6px 10px !important;
  margin-bottom: 8px !important;
}
.cap-active-label {
  font-size: 11px !important;
  color: #94a3b8 !important;
}
.cap-active-value {
  font-size: 12px !important;
  font-weight: 700 !important;
  color: #e9d5ff !important;
}

/* 2. Interactive On-Monitor Draggable & Resizable Caption Box */
.cap-monitor-overlay {
  position: absolute !important;
  inset: 0 !important;
  pointer-events: none !important;
  z-index: 50 !important;
  overflow: hidden !important;
}

.cap-monitor-box {
  position: absolute !important;
  pointer-events: auto !important;
  box-sizing: border-box !important;
  border: 2px dashed #a855f7 !important;
  border-radius: 6px !important;
  cursor: move !important;
  background: rgba(168, 85, 247, 0.08) !important;
  box-shadow: 0 0 16px rgba(168, 85, 247, 0.35) !important;
  transition: border-color 0.15s ease, background 0.15s ease !important;
  user-select: none !important;
  touch-action: none !important;
}
.cap-monitor-box:hover {
  border-color: #c084fc !important;
  background: rgba(168, 85, 247, 0.14) !important;
}
.cap-monitor-box.is-dragging {
  border-color: #38bdf8 !important;
  background: rgba(56, 189, 248, 0.15) !important;
  box-shadow: 0 0 20px rgba(56, 189, 248, 0.45) !important;
}

.cap-monitor-badge {
  position: absolute !important;
  bottom: calc(100% + 5px) !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  background: #0f131a !important;
  border: 1px solid #a855f7 !important;
  color: #f1f5f9 !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  padding: 2px 7px !important;
  border-radius: 4px !important;
  white-space: nowrap !important;
  pointer-events: none !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.6) !important;
}

/* 8-point resize handles */
.cap-handle {
  position: absolute !important;
  width: 10px !important;
  height: 10px !important;
  background: #ffffff !important;
  border: 2px solid #a855f7 !important;
  border-radius: 50% !important;
  box-sizing: border-box !important;
  pointer-events: auto !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.5) !important;
  transition: transform 0.1s ease !important;
}
.cap-handle:hover {
  transform: scale(1.35) !important;
  background: #a855f7 !important;
  border-color: #ffffff !important;
}

.cap-handle-nw { top: -5px !important; left: -5px !important; cursor: nwse-resize !important; }
.cap-handle-ne { top: -5px !important; right: -5px !important; cursor: nesw-resize !important; }
.cap-handle-sw { bottom: -5px !important; left: -5px !important; cursor: nesw-resize !important; }
.cap-handle-se { bottom: -5px !important; right: -5px !important; cursor: nwse-resize !important; }
.cap-handle-n  { top: -5px !important; left: calc(50% - 5px) !important; cursor: ns-resize !important; }
.cap-handle-s  { bottom: -5px !important; left: calc(50% - 5px) !important; cursor: ns-resize !important; }
.cap-handle-w  { left: -5px !important; top: calc(50% - 5px) !important; cursor: ew-resize !important; }
.cap-handle-e  { right: -5px !important; top: calc(50% - 5px) !important; cursor: ew-resize !important; }

/* Position Fine-Tune in Sidebar */
.cap-pos-row {
  display: grid !important;
  grid-template-columns: 1fr 1fr 1fr !important;
  gap: 4px !important;
  margin-top: 6px !important;
  margin-bottom: 8px !important;
}
.cap-pos-preset-btn {
  background: #1a202c !important;
  border: 1px solid #2d3748 !important;
  color: #cbd5e1 !important;
  font-size: 11px !important;
  padding: 4px 6px !important;
  border-radius: 4px !important;
  cursor: pointer !important;
  text-align: center !important;
}
.cap-pos-preset-btn:hover {
  background: #2d3748 !important;
  color: #ffffff !important;
}
.cap-pos-preset-btn.is-active {
  background: #a855f7 !important;
  border-color: #a855f7 !important;
  color: #ffffff !important;
  font-weight: 700 !important;
}

/* 3. Full View / Fullscreen Monitor */
.btn-fullview {
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: #e2e8f0 !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  padding: 4px 10px !important;
  border-radius: 6px !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  margin-left: 6px !important;
}
.btn-fullview:hover {
  background: rgba(255, 255, 255, 0.18) !important;
  color: #ffffff !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
}

.viewer--fullview {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 999999 !important;
  background: #000000 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 0 !important;
  margin: 0 !important;
}
.viewer--fullview .viewer__frame {
  flex: 1 1 auto !important;
  width: 100% !important;
  height: calc(100vh - 60px) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #000000 !important;
}
.viewer--fullview .viewer__canvas {
  max-width: 100% !important;
  max-height: 100% !important;
  object-fit: contain !important;
}
.viewer--fullview .transport {
  width: 100% !important;
  max-width: 1200px !important;
  background: rgba(15, 19, 26, 0.95) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
  padding: 10px 20px !important;
  box-sizing: border-box !important;
}

.btn-exit-fullview {
  position: fixed !important;
  top: 16px !important;
  right: 20px !important;
  z-index: 1000000 !important;
  background: rgba(0, 0, 0, 0.75) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #ffffff !important;
  padding: 6px 14px !important;
  border-radius: 9999px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6) !important;
}
.btn-exit-fullview:hover {
  background: #ef4444 !important;
  border-color: #ef4444 !important;
}

/* 4. Master Voiceover Volume Control */
.cap-voice-vol-wrap {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  padding: 3px 8px !important;
  border-radius: 6px !important;
  margin-left: 6px !important;
}
.cap-voice-vol-label {
  font-size: 11px !important;
  color: #94a3b8 !important;
  display: flex !important;
  align-items: center !important;
  gap: 3px !important;
}
.cap-voice-vol-slider {
  width: 65px !important;
  height: 4px !important;
  cursor: pointer !important;
  accent-color: #a855f7 !important;
}
.cap-voice-vol-val {
  font-size: 11px !important;
  font-weight: 700 !important;
  color: #f1f5f9 !important;
  min-width: 32px !important;
  text-align: right !important;
}

/* 5. Undo, Redo & Reset to Default */
.cap-history-actions {
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
}
.cap-reset-btn {
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  background: rgba(239, 68, 68, 0.12) !important;
  border: 1px solid rgba(239, 68, 68, 0.3) !important;
  color: #f87171 !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  padding: 3px 8px !important;
  border-radius: 5px !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  margin-left: 4px !important;
}
.cap-reset-btn:hover {
  background: rgba(239, 68, 68, 0.25) !important;
  color: #ffffff !important;
  border-color: #ef4444 !important;
}

/* 6. Video Clip AI Voice Removal */
.clip-voice-remover-card {
  background: rgba(99, 102, 241, 0.08) !important;
  border: 1px solid rgba(99, 102, 241, 0.25) !important;
  border-radius: 8px !important;
  padding: 10px !important;
  margin-top: 10px !important;
  margin-bottom: 8px !important;
}
.clip-voice-remover-head {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-bottom: 6px !important;
}
.clip-voice-remover-title {
  font-size: 12px !important;
  font-weight: 700 !important;
  color: #c7d2fe !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
}
.clip-voice-remover-hint {
  font-size: 10.5px !important;
  color: #94a3b8 !important;
  line-height: 1.3 !important;
  margin-top: 4px !important;
}
.clip-voice-remover-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  background: rgba(16, 185, 129, 0.15) !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
  color: #34d399 !important;
  font-size: 10.5px !important;
  font-weight: 600 !important;
  padding: 2px 7px !important;
  border-radius: 4px !important;
  margin-top: 6px !important;
}

/* 7. Transition Sound Effects */
.cap-sfx-section {
  background: #11151e !important;
  border: 1px solid #1f2737 !important;
  border-radius: 8px !important;
  padding: 10px !important;
  margin-top: 12px !important;
}
.cap-sfx-head {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-bottom: 8px !important;
}
.cap-sfx-title {
  font-size: 12.5px !important;
  font-weight: 700 !important;
  color: #f1f5f9 !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}
.cap-sfx-optin {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  color: #cbd5e1 !important;
  cursor: pointer !important;
}
.cap-sfx-optin input[type="checkbox"] {
  width: 15px !important;
  height: 15px !important;
  accent-color: #a855f7 !important;
  cursor: pointer !important;
}

.cap-sfx-body {
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding-top: 8px !important;
  margin-top: 6px !important;
}
.cap-sfx-smart-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  background: rgba(56, 189, 248, 0.12) !important;
  border: 1px solid rgba(56, 189, 248, 0.3) !important;
  color: #38bdf8 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  padding: 3px 8px !important;
  border-radius: 4px !important;
  margin-bottom: 8px !important;
}
.cap-sfx-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)) !important;
  gap: 4px !important;
  max-height: 160px !important;
  overflow-y: auto !important;
  margin-top: 6px !important;
  padding-right: 2px !important;
}
.cap-sfx-chip {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  background: #171c26 !important;
  border: 1px solid #283042 !important;
  border-radius: 5px !important;
  padding: 4px 6px !important;
  font-size: 10.5px !important;
  color: #cbd5e1 !important;
  cursor: pointer !important;
  transition: all 0.12s ease !important;
}
.cap-sfx-chip:hover {
  background: #1f2737 !important;
  border-color: #818cf8 !important;
}
.cap-sfx-chip.is-active {
  background: rgba(168, 85, 247, 0.22) !important;
  border-color: #a855f7 !important;
  color: #ffffff !important;
  font-weight: 700 !important;
}
.cap-sfx-play-btn {
  background: transparent !important;
  border: none !important;
  color: #a855f7 !important;
  font-size: 10px !important;
  cursor: pointer !important;
  padding: 2px !important;
  border-radius: 3px !important;
}
.cap-sfx-play-btn:hover {
  color: #ffffff !important;
  background: #a855f7 !important;
}
"""

with open("out/auto_captions.css", "a", encoding="utf-8") as f:
    f.write(css)

print("Appended enhanced CSS successfully!")
