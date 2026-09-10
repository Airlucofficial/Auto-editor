# TryAIToday AutoEditor (v2) & AI Caption Studio — Master Project Documentation

> **Master Reference Manual & Architecture Specification**  
> **Target Audience:** Developers, AI Coding Assistants, and System Integrators.  
> *Note for AI Chatbots & New Sessions:* This document contains the single-source-of-truth description of AutoEditor's architecture, full feature inventory, command-line operations, REST API contracts, UI workflows, and historical evolution. You do **not** need to parse the entire codebase to understand AutoEditor's capabilities; everything is specified in full detail below.

---

## Table of Contents
1. [Executive Summary & Purpose](#1-executive-summary--purpose)
2. [System Architecture & Runtime Model](#2-system-architecture--runtime-model)
3. [Complete History & Evolution of AutoEditor](#3-complete-history--evolution-of-autoeditor)
4. [How to Run AutoEditor (Every Mode & CLI Command)](#4-how-to-run-autoeditor-every-mode--cli-command)
5. [Core Storyboard & Media Synchronization Engine](#5-core-storyboard--media-synchronization-engine)
6. [Intelligent Video Auto-Speed Engine](#6-intelligent-video-auto-speed-engine)
7. [Aspect Ratios & 9:16 Vertical Editing Mode](#7-aspect-ratios--916-vertical-editing-mode)
8. [CapCut-Style Multi-Track Timeline & Toolbar](#8-capcut-style-multi-track-timeline--toolbar)
9. [Professional Playhead Scrubber & Dual-Track Scrubbing](#9-professional-playhead-scrubber--dual-track-scrubbing)
10. [Local Whisper AI Transcription & VAD Engine](#10-local-whisper-ai-transcription--vad-engine)
11. [Strict Second Timestamps (`0.0s – 3.4s`) & Document Exports (TXT / PDF)](#11-strict-second-timestamps-00s--34s--document-exports-txt--pdf)
12. [64 CapCut-Style Caption Presets Catalog (8 Categories)](#12-64-capcut-style-caption-presets-catalog-8-categories)
13. [On-Monitor Draggable & Resizable Caption Bounding Box](#13-on-monitor-draggable--resizable-caption-bounding-box)
14. [Master Voiceover Volume (0%–200%) & In-Editor Audio Playback](#14-master-voiceover-volume-0200--in-editor-audio-playback)
15. [Studio History Engine (Undo, Redo, Reset to Default)](#15-studio-history-engine-undo-redo-reset-to-default)
16. [AI Voice Removal & Speech Suppression (Preserving Foley & Clicks)](#16-ai-voice-removal--speech-suppression-preserving-foley--clicks)
17. [12 High-Fidelity Synthesized Transition Sound Effects (SFX)](#17-12-high-fidelity-synthesized-transition-sound-effects-sfx)
18. [Customizable Workspace Layout, Splitters & Window Modes](#18-customizable-workspace-layout-splitters--window-modes)
19. [FFmpeg Subtitle Burning & Video Export Pipeline](#19-ffmpeg-subtitle-burning--video-export-pipeline)
20. [Persistent Windows Background Watchdog (`service_manager.py`)](#20-persistent-windows-background-watchdog-service_managerpy)
21. [Complete REST API Reference (Port 4001)](#21-complete-rest-api-reference-port-4001)
22. [Repository Layout & File Index](#22-repository-layout--file-index)
23. [Test Suite Architecture & Verification (111 Tests)](#23-test-suite-architecture--verification-111-tests)
24. [AI Chatbot Video Planning Guide & Output Templates](#24-ai-chatbot-video-planning-guide--output-templates)

---

## 1. Executive Summary & Purpose

**TryAIToday AutoEditor (v2)** is a local, private, desktop video editing and automated content creation studio. It bridges the gap between raw AI-generated assets (narration audio, Midjourney/Flux/Leonardo images, video clips) and polished, publish-ready MP4 videos formatted for YouTube, TikTok, Instagram Reels, and Shorts.

### What Kind of Software Is It? (Tool / Software / Web-Based App Classification)
If asked *"Is this a tool, software, or a web-based app?"*, the official classification is:
**Local Desktop Software (with a Local Web-Based Interface)**.

* **One-Sentence Definition:** It is a local, offline desktop video editing software that opens and runs in your browser via a local server on your own PC (`http://localhost:4000`).
* **Technical Definition:** It is a **hybrid desktop application** comprising a compiled desktop backend (`AutoEditor.exe`), a bundled local media pipeline (`ffmpeg.exe`), and an offline Python AI engine (`faster-whisper`), with a modern Next.js single-page application served locally.
* **Why It Is NOT a Cloud "Web App":**
  - **Zero Cloud Uploads:** No video, image, audio, or transcript data ever leaves your computer or gets uploaded to the internet.
  - **100% Offline & Private:** AI transcription, video rendering, and subtitle burning run exclusively on your machine's CPU and GPU.
  - **Native Desktop Integration:** It operates via native Windows executables and background services, using the browser window purely as a graphical user interface (GUI) and visual monitor.

### Primary Missions
1. **Automated Storyboard Synchronization:** Eliminates manual timeline dragging by automatically aligning images and video clips to master narration based entirely on timestamps embedded in filenames (e.g. `0-00.png`, `0-04.5.mp4`).
2. **Local AI Speech-to-Text Transcription:** Transcribes voiceovers using offline Whisper AI (`faster-whisper`), outputting word-by-word timestamps, interval formats (`0.0s – 3.4s`), and downloadable TXT and visual badge PDF documents.
3. **CapCut-Style Kinetic Caption Studio:** Equips creators with 64 curated subtitle presets across 8 categories, live on-canvas word-by-word animation preview, on-monitor interactive repositioning/resizing, and final FFmpeg ASS subtitle burning.
4. **Intelligent Clip Automation:** Automatically speeds up long videos to fit short voiceover slots, attenuates speech frequencies from background clips while preserving clicks and foley, and injects 12 synthesized transition sound effects with smart auto-selection.
5. **100% Offline & Private:** Zero media or audio is ever uploaded to the cloud. All Whisper transcription, canvas rendering, and FFmpeg encoding run on the user's local CPU and GPU.

---

## 2. System Architecture & Runtime Model

AutoEditor operates as a hybrid, multi-process desktop system composed of three main layers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          USER WEB BROWSER                              │
│                http://localhost:4000  (Next.js Single-Page App)         │
│  - Multi-Track Timeline          - Live Canvas Preview (tu callback)  │
│  - 64-Preset Caption Studio      - Draggable Monitor Bounding Box     │
│  - Splitter & Layout Manager     - In-Editor Audio Playback Engine    │
└───────────────────▲────────────────────────────────┬───────────────────┘
                    │                                │
      HTTP (Port 4000)                               │ REST API (Port 4001)
                    │                                │
┌───────────────────┴──────────┐   ┌─────────────────▼───────────────────┐
│       AutoEditor.exe         │   │            api_server.py            │
│   (Bun / Node Desktop Server)│   │       (Python 3.10+ Multi-Thread)   │
│ - Serves out/ static SPA     │   │ - Faster-Whisper Transcription Engine│
│ - Manages render jobs        │   │ - 64 CapCut Presets & ASS Compiler  │
│ - Dispatches ffmpeg encoding │   │ - TXT & ReportLab PDF Generator     │
│ - Tracks audio duration      │   │ - Audio Pre-Mixer & Vocal Suppressor│
└──────────────────────────────┘   └─────────────────▲───────────────────┘
                                                     │
                                           Monitored & Recovered
                                                     │
                                   ┌─────────────────┴───────────────────┐
                                   │         service_manager.py          │
                                   │   (Headless pythonw Watchdog)       │
                                   │ - Probes /api/health every 1.0s     │
                                   │ - Auto-starts api_server.py         │
                                   │ - Fast-path crash recovery (<1.5s)  │
                                   │ - Auto-shuts down when app closes   │
                                   └─────────────────────────────────────┘
```

### Process Roles
1. **Frontend / Desktop Server (`AutoEditor.exe` on port 4000):** Native Bun/Node binary serving static assets from `out/`. Handles timeline data management, render job queuing, local downloads, and canvas synchronization.
2. **AI Companion Server (`api_server.py` on port 4001):** High-concurrency Python HTTP service exposing REST endpoints for AI speech transcription, ASS subtitle compilation, audio pre-mixing, vocal removal, and PDF generation.
3. **Persistent Watchdog Service (`service_manager.py`):** Headless Windows daemon launched via `pythonw.exe` (`CREATE_NO_WINDOW | DETACHED_PROCESS`). It monitors the AI engine, auto-recovers crashes within 1.5 seconds, frees occupied ports, and shuts down automatically when `AutoEditor.exe` terminates.
4. **Encoding Engine (`ffmpeg.exe`):** Bundled FFmpeg build supporting `libass`, custom fonts (`caption.ttf`), and hardware-accelerated encoders (NVIDIA NVENC `h264_nvenc`, Intel QSV `h264_qsv`, AMD AMF `h264_amf`, and CPU fallback `libx264`).

---

## 3. Complete History & Evolution of AutoEditor

AutoEditor underwent a structured engineering evolution documented through its git version history:

| Commit | Date | Title / Scope | Key Breakthroughs & Additions |
|---|---|---|---|
| **b3e19f1** | 2026-09-05 | *Initial commit: AutoEditor project files and web UI* | Foundation commit containing `AutoEditor.exe`, bundled `ffmpeg.exe`, `caption.ttf`, Next.js frontend chunks (`out/`), static styles, and the basic image-to-voiceover timeline synchronization engine. |
| **54d056d** | 2026-09-06 | *feat(ai): add in-editor auto-captions, 64 CapCut presets, clean navbar, and Whisper AI transcription suite* | Major architectural upgrade adding `faster-whisper` integration, `api_server.py`, `service_manager.py`, 64 CapCut-style presets catalog across 8 categories, ASS compilation, second-based timestamp formatter (`0.0s – 3.4s`), ReportLab PDF generator with visual badges, and 4-tier E2E testing framework. |
| **2990fba** | 2026-09-06 | *fix(service): headless background AI service with pythonw, auto-shutdown on app exit, and 1-click stop script* | Eliminated unwanted console command prompt windows by migrating the service manager to `pythonw.exe` (`CREATE_NO_WINDOW`). Added auto-shutdown watchdog when `AutoEditor.exe` closes for 60s, and introduced `Stop-AutoEditor.bat`. |
| **ddc566a** | 2026-09-06 | *fix: auto captions button click responsiveness, persistent AI watchdog stability, and robust voiceover sync* | Fixed event delegation and button click responsiveness for the navbar auto-captions trigger. Hardened watchdog PID drift synchronization to prevent false restarts. Perfected voiceover audio reference attachment. |
| **47223a0** | 2026-09-06 | *feat: intelligent video speed fit to timestamp duration and flexible decimal timestamp parser* | Implemented dynamic video speed fitting. If an uploaded video clip is longer than its timeline slot, AutoEditor calculates `speed = src_duration / slot_duration` and applies FFmpeg `setpts`/`tpad` filters. Added `⚡ Auto-Speed` badges and flexible decimal timestamp parsing (`5.5.mp4`, `0-05.5.mp4`, `5.5-10.mp4`). |
| **f9f13a7** | 2026-09-06 | *fix: resolve timeline build freezing/lag and add intelligent 0:05 vs 0-05 timestamp equivalence* | Resolved timeline freezing during build by optimizing slot calculations. Made colon (`0:05`) and hyphen (`0-05`) timestamps 100% equivalent across all naming styles (`[0:05]`, `(0:05)`, `scene 0:05.png`, `0:05 to 0:10.mp4`). |
| **2391f57** | 2026-09-07 | *feat: implement 64 caption styles drawer, monitor placement/resizing, full view, voice volume, undo/redo, vocal suppression, and smart transition SFX* | Massive 7-feature capability overhaul:<br>1. On-monitor draggable & resizable caption box with 8 handles.<br>2. 64-style drawer & monitor quick bar.<br>3. Expand preview and full view modes.<br>4. Master voiceover volume control (0% to 200% via Web Audio gain).<br>5. Studio History (Undo, Redo, Reset to Default with 50-state stack).<br>6. AI Voice Removal notch filter attenuating vocal formants while preserving foley/clicks.<br>7. 12 synthesized 44.1kHz transition sound effects with smart auto-selection. |
| **121844b** | 2026-09-07 | *fix(client): resolve ReferenceError: eL is not defined causing Next.js client-side exception* | Fixed scope integrity in patched Next.js production bundle `page-f2b7366e605a20db.js` by ensuring `let eL` declaration is properly preserved. |
| **966b82a** | 2026-09-07 | *fix(patch): make patch_page.py idempotent and restore missing assertion in test_new_features* | Made `patch_page.py` completely idempotent so repeated executions verify existing AST structures without double-patching or syntax corruption. |
| **e407b7b** | 2026-09-08 | *feat(ui/audio): add 9:16 vertical video editing mode and full in-editor audio playback* | Added dedicated 9:16 vertical video editing mode (1080×1920) for TikTok/Reels/Shorts, top bar aspect ratio toggles (`📱 9:16 Vertical` ↔ `🖥️ 16:9 Landscape`), silent audio clock generator (`createSilentAudioUrl`), unmuted video playback, and global AudioContext unlock handlers on space/arrow keys. |

---

## 4. How to Run AutoEditor (Every Mode & CLI Command)

### Method 1: The 1-Click AI Launcher (Recommended)
Double-click `Start-AutoEditor-AI.bat` in the project root:
```bat
:: What Start-AutoEditor-AI.bat executes:
.venv\Scripts\python.exe service_manager.py start
set RENDER_ZOOM_SS=1
AutoEditor.exe
:: On exit, automatically runs:
.venv\Scripts\python.exe service_manager.py stop
```
- Starts the headless AI companion watchdog in the background.
- Launches `AutoEditor.exe` on port 4000.
- Automatically stops all background Python processes when the console window is closed.

### Method 2: The 1-Click Stop Utility
Double-click `Stop-AutoEditor.bat` to terminate all running instances of `AutoEditor.exe`, `api_server.py`, and `service_manager.py`:
```powershell
.\Stop-AutoEditor.bat
```

### Method 3: Manual Terminal Execution (Developer Mode)

#### Step 1: Start the AI Companion Watchdog
```powershell
# In PowerShell / Command Prompt:
.\.venv\Scripts\python.exe service_manager.py start
```
*Verify status:*
```powershell
.\.venv\Scripts\python.exe service_manager.py status
```
*Expected output:*
```text
=======================================================
 AutoEditor AI Engine Background Service Status
=======================================================
 Supervisor PID : 12344 (Active)
 API Server PID : 15820 (Active)
 Port 4001 Status: 🟢 Healthy (200 OK)
 Model Cached   : Yes
 Service Name   : AutoEditor AI Engine
 Version        : 2.0
=======================================================
```

#### Step 2: Start the Desktop Server
```powershell
$env:RENDER_ZOOM_SS = "1"
.\AutoEditor.exe
```
Open `http://localhost:4000` in Google Chrome, Microsoft Edge, or any modern browser.

### Method 4: Direct CLI Operations

#### Audio Transcription to JSON, TXT, PDF, and ASS:
```powershell
.\.venv\Scripts\python.exe transcribe_engine.py transcribe "path\to\audio.wav" `
    --model base `
    --out-json "storage\transcript.json" `
    --out-txt "storage\transcript.txt" `
    --out-pdf "storage\transcript.pdf" `
    --style hormozi_bold `
    --out-ass "storage\subtitles.ass"
```

#### Generate ASS Subtitles from existing Transcript JSON:
```powershell
.\.venv\Scripts\python.exe transcribe_engine.py generate-ass `
    "storage\transcript.json" `
    "neon_glow" `
    "storage\output.ass" `
    --width 1920 `
    --height 1080
```

#### Export Transcript JSON to Publication-Quality PDF:
```powershell
.\.venv\Scripts\python.exe transcribe_engine.py export-pdf `
    "storage\transcript.json" `
    "storage\published_transcript.pdf"
```

#### List All 64 Available Caption Styles:
```powershell
.\.venv\Scripts\python.exe transcribe_engine.py list-styles
```

---

## 5. Core Storyboard & Media Synchronization Engine

AutoEditor builds complete timelines automatically by mapping visual assets to narration timestamps encoded in filenames:

### Supported Filename Syntax
1. **Minute-Second (`M-SS` or `M:SS`):**
   - `0-00.png` or `0:00.png` → Starts at `0.0s`.
   - `0-04.png` or `0:04.png` → Appears at `4.0s`.
   - `1-02.mp4` or `1:02.mp4` → Appears at `62.0s` (1 minute 2 seconds).
2. **Decimal Timestamps (`M-SS.S` or `SS.S`):**
   - `0-05.5.mp4` or `0:05.5.mp4` → Starts at `5.5s`.
   - `5.5.mp4` → Starts at `5.5s`.
   - `12.3.png` → Starts at `12.3s`.
3. **Explicit Range Syntax:**
   - `5.5-10.mp4` → Starts at `5.5s` and transitions at `10.0s`.
   - `0-05.5_0-10.mp4` → Starts at `5.5s` and transitions at `10.0s`.
   - `5.5 to 0.10.mp4` → Starts at `5.5s` and transitions at `10.0s`.
4. **Descriptive Prefixes and Suffixes:**
   - `scene_0:05.png`, `0:05 - intro.png`, `shot_1_0-05.png`, `[0:05].png`, `(0:05).png` all parse cleanly to `5.0s`.
5. **Strict Colon-Hyphen Equivalence:**
   `0:05` and `0-05` parse to the exact same millisecond timestamp across all file extensions (`.png`, `.jpg`, `.webp`, `.mp4`).

### Timeline Placement Rules
- The **Master Voiceover** (`.mp3` or `.wav`) dictates the total duration of the project timeline.
- An image or video clip stays active on screen until the next clip's timestamp arrives. The interval between timestamps determines scene duration.
- Gaps before the first timestamp (e.g. if the first file is `0-03.png`) are automatically filled with a starting hold frame or black gap.

---

## 6. Intelligent Video Auto-Speed Engine

When a creator imports a video clip that is longer than the timestamp duration allotted to it, AutoEditor dynamically calculates an acceleration factor so the entire clip fits perfectly into the scene without cutting off prematurely.

### Mathematical Formulation
$$\text{Speed Multiplier} = \frac{\text{Source Clip Duration}}{\text{Target Timeline Slot Duration}}$$

*Example:* A 15.0-second video clip (`my_clip.mp4`) placed in a slot from `5.0s` to `10.0s` (5.0s slot):
$$\text{Speed} = \frac{15.0}{5.0} = 3.0\times$$

### System Features
- **In-Editor Speed Badge:** Automatically mounts a `⚡ 3.0×` pill on the video clip card in the timeline lane.
- **Header Indicator:** Displays `⚡ Auto-Speed: Active` in the top bar.
- **FFmpeg Acceleration Filter:** During rendering, AutoEditor translates the speed ratio into an exact PTS (Presentation Time Stamp) filter:
  ```text
  -vf "setpts=(PTS-STARTPTS)/3.0000,tpad=stop_mode=clone:stop_duration=5.000,trim=duration=5.000,setpts=PTS-STARTPTS,fps=30"
  ```
- **Metadata Pre-Caching:** Video metadata (`onloadedmetadata`) is cached in `window._videoDurationCache` upon file selection, enabling instantaneous badge rendering.

---

## 7. Aspect Ratios & 9:16 Vertical Editing Mode

AutoEditor supports both widescreen horizontal and mobile vertical production environments:

| Mode | Aspect Ratio | Render Resolution | Target Platform |
|---|:---:|:---:|---|
| **Widescreen Landscape** | `16:9` | $1920 \times 1080$ | YouTube Main, Vimeo, Desktop, TV |
| **Vertical Video Mode** | `9:16` | $1080 \times 1920$ | YouTube Shorts, TikTok, Instagram Reels |
| **Square** | `1:1` | $1080 \times 1080$ | Instagram Feeds, LinkedIn |
| **Auto** | Native | Preserves first image dimensions | Custom aspect ratios |

### 9:16 Vertical Mode Capabilities
- **1-Click Header Toggle (`btn-aspect-toggle`):** Instantly toggles between `📱 9:16 Vertical` and `🖥️ 16:9 Landscape`.
- **Transport Bar Aspect Pill (`btn-ratio-pill`):** Quick ratio switch accessible right beside playback controls.
- **CSS Layout Transformation:** Injects `.cap-vertical-mode` onto the editor canvas and viewport, properly constraining preview proportions and framing vertical subtitles.
- **Dynamic Project Info Badge:** Updates header pill to `📱 AutoEditor Pro · 9:16 1080×1920 (Vertical)`.

---

## 8. CapCut-Style Multi-Track Timeline & Toolbar

The timeline interface is modeled after professional NLEs (Non-Linear Editors) like CapCut Desktop:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 00:00:04:12  |  ✂️ Split  🗑️ Delete  ↶ Undo  ↷ Redo  🧲 Snap   [Zoom: − [──●──] + ↔ Fit]│
├──────────────┬─────────────────────────────────────────────────────────────────────────┤
│ 💬 Subtitles │ [0.0s - 3.4s: Welcome to AutoEditor]  [3.4s - 6.8s: Every style works]  │
├──────────────┼─────────────────────────────────────────────────────────────────────────┤
│ 🎬 Video     │ [0-00.png]              [0-05.5.mp4 ⚡ 2.4×]      [0-12.jpg]            │
├──────────────┼─────────────────────────────────────────────────────────────────────────┤
│ 🎵 Audio     │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ Master Voiceover Audio (Waveform) ▓▓▓▓▓▓▓▓▓▓▓▓▓ │
├──────────────┼─────────────────────────────────────────────────────────────────────────┤
│ 🔔 SFX       │             [🔔 whoosh_fast]                   [🔔 cinematic_boom]     │
└──────────────┴─────────────────────────────────────────────────────────────────────────┘
```

### Timeline Lanes & Track Gutters
1. **Subtitles Track (`tl__tag--subtitles`):** Displays subtitle cue pills synchronized with audio. Clicking any subtitle cue jumps playback directly to that segment. Includes visibility toggle (`👁️`) and track lock (`🔒`).
2. **Video Track (`tl__tag--video`):** Contains visual storyboard clips, transition diamonds, motion tags, and auto-speed badges.
3. **Master Audio Track (`tl__tag--audio`):** Waveform representation of the voiceover narration. Includes mute toggle (`🔊`/`🔇`) and track lock.
4. **Transition SFX Track (`tl__tag--sfx`):** Displays sound effect markers at transition cut points. Clicking any marker previews the sound effect.

### Toolbar Actions
- **Timecode Display (`#cap-tl-timecode-display`):** Real-time SMPTE timecode format `HH:MM:SS:FF` (hours, minutes, seconds, frames at 30fps).
- **Split Tool (`#cap-tl-btn-split`):** Splits clip at the current playhead position.
- **Delete Tool (`#cap-tl-btn-delete`):** Removes selected clip or transition.
- **Undo / Redo (`#cap-tl-btn-undo`, `#cap-tl-btn-redo`):** Step backward or forward through editing history.
- **Magnetic Snapping (`#cap-tl-btn-snap`):** Toggles magnetic playhead snapping to cut boundaries (threshold: 0.18s).
- **Zoom Controls:** Slider from $0.5\times$ to $3.0\times$, Zoom In (`+`), Zoom Out (`−`), and Fit to Window (`↔ Fit`).

---

## 9. Professional Playhead Scrubber & Dual-Track Scrubbing

AutoEditor features a low-latency playhead scrubber with bi-directional audio/visual synchronization:

- **Grip Pointer Capture (`setPointerCapture`):** Enables fluid playhead dragging without losing mouse focus during rapid movements.
- **Dual-Track Scrubbing:** Users can click and scrub directly on the top **Time Ruler** (`.tl__ruler`) OR anywhere inside the **Captions Track Lane** (`#cap-tl-captions-lane`).
- **Canvas Redraw Bridge:** Invokes `window._TRIGGER_CANVAS_DRAW()` on every scrub tick, rendering real-time video frames and active subtitle animations without timeline lag.
- **Audio Seek Synchronization:** Automatically seeks `_VOICEOVER_AUDIO_EL.currentTime` in real time during scrubbing.

---

## 10. Local Whisper AI Transcription & VAD Engine

Speech-to-text transcription is powered by `faster-whisper` (a CTranslate2 reimplementation of OpenAI's Whisper model), running completely offline:

### Technical Specifications
- **Model Hierarchy:** Defaults to `small` (high accuracy), falling back automatically to `base` or `tiny` if offline or resource-constrained.
- **In-Memory Model Caching (`_MODEL_CACHE`):** Preserves loaded model weights in memory across HTTP requests, eliminating 15–25 second model loading delays on subsequent calls.
- **Beam Search:** Configured with `beam_size=5` for superior vocabulary recognition and reduced hallucination.
- **Speech Padding:** $400\text{ms}$ pre- and post-speech padding prevents cutoffs on word start and end syllables.
- **Voice Activity Detection (VAD):** Integrated Silero VAD with `min_silence_duration_ms=400` ensures natural phrase boundaries.
- **Word-Level Timing Alignment:** Generates exact start and end timestamps for every single spoken word.

---

## 11. Strict Second Timestamps (`0.0s – 3.4s`) & Document Exports (TXT / PDF)

AutoEditor standardizes all segment timestamps to a clean second-based interval format:
$$\text{Format:} \quad \mathbf{f"\{start:.1f\}s \text{ – } \{end:.1f\}s"} \quad (\text{e.g. } \mathbf{"0.0s \text{ – } 3.4s"})$$

### 1. Plain Text Export (`.txt`)
- Formatted with visual headers, total duration, word count, and bracketed intervals:
  ```text
  =================================================================
   AUDIO TRANSCRIPT: voiceover.wav
   Total Duration: 45.2s | Total Words: 118
   Timeline: 0.0s --> 45.2s
   Generated: 2026-09-08 14:30:00
  =================================================================

  --- [ TIMESTAMPS & DIALOGUE ] ---

  [0.0s – 3.4s] Speaker: Welcome to AutoEditor video studio.
  [3.4s – 7.1s] Speaker: Creating professional videos with AI captions.

  =================================================================
  --- [ FULL TEXT SCRIPT ] ---
  =================================================================
  Welcome to AutoEditor video studio. Creating professional videos...
  ```

### 2. Publication-Quality PDF Export (`.pdf`)
- Built using Python's **ReportLab** library (with automatic fallback to `fpdf2`).
- Renders custom flowable `RoundedBadge` elements:
  - **Fill Color:** `#EEF2FF` (Soft indigo/slate)
  - **Text Color:** `#1E40AF` (Deep sapphire bold)
  - **Border:** `#C7D2FE` ($0.75\text{pt}$ border width with $4\text{px}$ corner radius)
- Features structured tabular layouts, document metadata headers, horizontal rules, and dynamic running footers with two-pass canvas pagination (`Page X of Y`).

---

## 12. 64 CapCut-Style Caption Presets Catalog (8 Categories)

AutoEditor includes an exhaustive library of 64 curated subtitle presets divided evenly across 8 aesthetic categories (8 presets per category). Every style includes matching ASS subtitle styles, CSS live preview properties, and canvas render rules:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        64 PRESET STYLES CATALOG                        │
├──────────────────────┬─────────────────────────────────────────────────┤
│ Category             │ Included Style Presets                          │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 1. Viral Shorts      │ bouncy_shorts, tiktok_pop, viral_green_hook,    │
│    & TikTok          │ snap_yellow, speed_demon, reel_zoomer,          │
│                      │ trendsetter_red, karaoke_gold                   │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 2. Hormozi & Viral   │ hormozi_bold, hormozi_lime, hormozi_gold,       │
│    Retention         │ hormozi_cyan, hormozi_red, hormozi_white_black, │
│                      │ hormozi_orange, hormozi_electric                │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 3. Neon Cyber Glow   │ neon_glow, neon_purple, neon_pink, neon_acid,   │
│                      │ neon_ice_blue, neon_tokyo, neon_toxic,          │
│                      │ neon_synthwave                                  │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 4. Cinematic &       │ minimalist_modern, film_slate, noir_editorial,  │
│    Documentary       │ editorial_serif, masterclass_sub, cinematic_gold│
│                      │ horizon_bar, nordic_frost                       │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 5. Boxed & Pill      │ boxed_pill, dark_slate_pill, red_alert_box,     │
│    Badges            │ emerald_pill, purple_glow_box, sunset_pill,     │
│                      │ royal_blue_badge, high_vis_amber                │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 6. Bold Punchy &     │ headline_3d_punch, headline_angled,             │
│    Headline          │ headline_big_impact, headline_blackout,         │
│                      │ headline_thunder, headline_heavy_metal,         │
│                      │ headline_stencil, headline_iron                 │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 7. Retro & Comic Pop │ comic_pop, bubble_pink, arcade_8bit,            │
│                      │ cartoon_blast, pop_art_yellow, comic_kapow,     │
│                      │ kawaii_lilac, superhero_red                     │
├──────────────────────┼─────────────────────────────────────────────────┤
│ 8. Clean Corporate   │ classic_broadcast, netflix_clean,               │
│    & Broadcast       │ youtube_standard, bbc_crisp, corporate_navy,    │
│                      │ ted_speaker, swiss_neutral, subtitle_pro        │
└──────────────────────┴─────────────────────────────────────────────────┘
```

### Supported Animation Types
- `bounce_pop`: Dynamic scale pop ($\times 1.15$) on the active spoken word.
- `scale_pulse`: Heavy scale enlargement ($\times 1.20$) for punchy retention words.
- `karaoke_highlight`: Instant color fill transformation when word is spoken.
- `glow_highlight`: High-contrast neon luminescence effect on active token.
- `box_pill`: Contrasting solid badge pill plate behind the active word.
- `clean_karaoke`: Smooth color transition for corporate and documentary content.
- `standard_phrase`: Clean static phrase display for broadcast accessibility.

---

## 13. On-Monitor Draggable & Resizable Caption Bounding Box

Creators can visually position and scale subtitles directly on the video monitor window before rendering:

### Mechanics & Controls
- **Overlay Container (`#cap-monitor-box`):** A high-visibility bounding box rendered directly over the video canvas with coordinates badge:
  `Caption · X: 50% · Y: 85% · Size: 100%`.
- **8 Cardinal & Diagonal Handles:**
  - `nw`, `ne`, `sw`, `se`: Corner resizing.
  - `n`, `s`: Vertical scale adjustment.
  - `w`, `e`: Horizontal scale adjustment.
- **Drag Repositioning:** Clicking anywhere inside the box allows free 2D repositioning across the video canvas (constrained between $5\%$ and $95\%$).
- **Normalized Coordinate System:** Stored in `window._CAPTION_POS`:
  ```javascript
  window._CAPTION_POS = { x: 0.50, y: 0.85, scale: 1.00 };
  ```
- **Bidirectional Synchronization:** Moving the box updates the sidebar range sliders (`cap-pos-x-range`, `cap-pos-y-range`, `cap-scale-range`) in real time, and vice versa.
- **ASS Subtitle Injection:** Injected directly into compiled ASS dialogue headers using the alignment tag `\an5` and calculated absolute pixel positions:
  $$\text{Pixel } X = \text{round}(x \times \text{width}), \quad \text{Pixel } Y = \text{round}(y \times \text{height})$$
  $$\text{Dialogue Tag:} \quad \mathbf{\{\backslash\text{an5}\backslash\text{pos}(960, 918)\}}$$

---

## 14. Master Voiceover Volume (0%–200%) & In-Editor Audio Playback

### Master Voice Volume Slider
- **Range:** $0\%$ (muted) to $200\%$ ($2.0\times$ volume boost).
- **Web Audio API Integration:** For volumes exceeding $100\%$ ($>1.0$), AutoEditor instantiates a Web Audio `AudioContext` and connects a `GainNode` to amplify the audio signal past standard HTML5 limits without distortion.
- **Pre-Mix Rendering:** Passed to the backend during video export; FFmpeg adjusts audio levels via `-af "volume=1.500"`.

### In-Editor Audio Playback Engine
- **Silent Clock Generator (`createSilentAudioUrl`):** If a user creates a project with images only (no voiceover), AutoEditor synthesizes a valid in-memory 44.1kHz PCM WAV blob of silence. This acts as a clock, ensuring the playhead moves, video clips play, and animations execute seamlessly.
- **Unmuted Video Clip Playback:** Video elements appended to the DOM (`v_<id>`) have `muted = false` and synchronize playback with the master playhead.
- **Autoplay Policy Handlers:** Global click and keydown listeners automatically resume suspended `AudioContext` instances on spacebar or arrow key press.

---

## 15. Studio History Engine (Undo, Redo, Reset to Default)

AutoEditor maintains an autonomous history manager (`StudioHistory`) with a 50-state rollback stack:

```javascript
StudioHistory.capture() => {
  style: "hormozi_bold",
  pos: { x: 0.5, y: 0.85, scale: 1.2 },
  voiceVol: 1.25,
  sfxEnabled: true,
  sfxVol: 0.6,
  sfxId: "whoosh_fast",
  clipVoiceSettings: { ... }
}
```

### Actions & Shortcuts
- **Step Back (Undo):** `Ctrl+Z` or `#btn-step-back`.
- **Step Forward (Redo):** `Ctrl+Y`, `Ctrl+Shift+Z` or `#btn-step-forward`.
- **Reset to Default (`#btn-reset-default`):** Instantly restores caption style to `classic`, coordinates to center-bottom ($X=50\%, Y=85\%, \text{Scale}=1.0$), voice volume to $100\%$, and turns off optional SFX with confirmation prompt.

---

## 16. AI Voice Removal & Speech Suppression (Preserving Foley & Clicks)

When video clips contain unwanted talking or dialogue that clashes with the master voiceover, creators can activate **AI Voice Removal**:

### How It Works
- Rather than muting the clip entirely (which kills all background atmosphere), AutoEditor uses a multi-stage acoustic notch filter designed around human speech formants:
  - **Fundamental Notch:** $300\text{Hz}$ ($Q=1.2$, gain up to $-26\text{dB}$)
  - **First Formant (F1) Notch:** $1050\text{Hz}$ ($Q=1.6$, gain up to $-32\text{dB}$)
  - **Second Formant (F2) Notch:** $2200\text{Hz}$ ($Q=1.6$, gain up to $-29\text{dB}$)
  - **Third Formant (F3) Notch:** $3300\text{Hz}$ ($Q=1.4$, gain up to $-22\text{dB}$)
- **Preserves Transients:** Frequencies above $4.0\text{kHz}$ (mouse clicks, paper turns, footsteps, camera shutters, high impacts) and sub-bass frequencies below $120\text{Hz}$ remain crisp and intact.
- **In-Browser Preview:** Implemented via Web Audio `BiquadFilterNode` cascade.
- **Backend Video & Audio Processing:** Endpoint `POST /api/vocal-remove` outputs processed audio (`.wav`) or re-encoded video (`.mp4`) with suppressed vocals.

---

## 17. 12 High-Fidelity Synthesized Transition Sound Effects (SFX)

AutoEditor includes 12 procedural sound effects synthesized directly using mathematical waveform functions (sine sweeps, white noise filtering, exponential decay envelopes) at $44.1\text{kHz}$, 16-bit mono PCM with zero external audio assets required:

| SFX Key | Sound Name | Audio Character | Best Suited For |
|---|---|---|---|
| `whoosh_fast` | Fast Whip Whoosh | Bandpass filtered noise sweep ($0.4\text{s}$) | Fast whip wipes, snap cuts |
| `swoosh_smooth` | Cinematic Swoosh | Dual low-pass resonance swoosh ($0.65\text{s}$) | Slides, smooth crossfades |
| `camera_click` | Camera Shutter & Click | Dual transient click + mechanical spring ($0.22\text{s}$) | Photo cuts, hard cuts |
| `bubble_pop` | Bubble Pop | Pitch-swept sine ($280\text{Hz} \to 1880\text{Hz}$, $0.16\text{s}$) | Viral shorts, playful pops |
| `cinematic_boom` | Cinematic Sub Boom | Low sub-bass drop ($65\text{Hz} \to 24\text{Hz}$, $1.3\text{s}$) | Fade to black, dramatic cuts |
| `digital_glitch` | Digital Glitch | FM synth square modulation ($0.32\text{s}$) | Cyber cuts, neon transitions |
| `gentle_chime` | Gentle Bell Chime | Harmonic overtone bell decay ($0.9\text{s}$) | Elegant fades, corporate |
| `paper_turn` | Paper Turn | Organic filtered foley flutter ($0.38\text{s}$) | Documentary, book flips |
| `snappy_switch` | Tactile Click | High-frequency mechanical tap ($0.12\text{s}$) | Instant cuts, UI highlights |
| `impact_punch` | Punch Impact | Sub kick with mid transient ($0.45\text{s}$) | Dynamic action, fast beats |
| `cinematic_riser` | Tension Riser | Exponential upward pitch swell ($0.95\text{s}$) | Build-ups, tension cuts |
| `short_woosh` | Snappy Micro-Woosh | Ultra-fast air puff ($0.25\text{s}$) | Rapid micro-cuts |

### Smart Auto-Selection Algorithm
When `window._SELECTED_SFX = "auto"`, AutoEditor inspects the transition type of each timeline cut and assigns sound effects automatically:
- `wipeleft` / `wiperight` $\to$ `whoosh_fast`
- `slideup` $\to$ `swoosh_smooth`
- `fadeblack` $\to$ `cinematic_boom`
- `fade` $\to$ `gentle_chime`
- `circlecrop` $\to$ `bubble_pop`
- `cut` / `none` $\to$ `camera_click`

### Multi-Input Audio Mixing
During final export, `POST /api/mix-audio` compiles an FFmpeg `filter_complex` graph using `adelay` and `amix` to position each transition SFX at its exact millisecond timestamp underneath the master voiceover.

---

## 18. Customizable Workspace Layout, Splitters & Window Modes

The editor features a flexible workspace configuration system with persistent settings stored in `localStorage`:

### 1. Interactive Drag-Splitters
- **Horizontal Splitter (`#editor-splitter-h`):** Resizes the right inspector sidebar between $220\text{px}$ and $650\text{px}$. Includes a 1-click collapse button (`◀` / `▶`).
- **Vertical Splitter (`#editor-splitter-v`):** Adjusts the proportion between the video preview monitor and the timeline between $30\%$ and $82\%$.

### 2. Expand Preview Mode (`btn-expand-preview-main`)
- Maximizes the video monitor to dominate the window while keeping the multi-track timeline docked below for editing.
- Shortcut: `Esc` or `Ctrl+Enter` to toggle.

### 3. Workspace Presets Bar (`#cap-workspace-bar`)
- **🎬 Large Preview:** $74\%$ monitor height, collapsed sidebar panels.
- **⚡ Timeline:** $44\%$ monitor height, expanded multi-track view.
- **🎨 Captions:** Focus on caption styles drawer and positioning controls.
- **🚀 Export:** Focus on export quality, bitrate, and audio mixing.
- **⚙️ Default:** Balanced $58\%$ preview with full inspector sidebar.

### 4. Layout Lock & Panel Customization
- **Lock Layout (`#btn-toggle-lock-layout`):** Freezes all splitters to prevent accidental resizing during editing sessions.
- **Panels Menu (`#cap-layout-dropdown`):** Allows creators to toggle individual panel visibility (Preview Window, Multi-Track Timeline, Export Panel, Transitions Panel, Voice Volume Controls, Auto-Speed Badge).

---

## 19. FFmpeg Subtitle Burning & Video Export Pipeline

The rendering pipeline converts the timeline into an encoded MP4 video file:

```
[Storyboard Images & Videos] ──┐
[Master Voiceover Audio]     ──┼─► [AutoEditor.exe Render Engine]
[Transition Sound Effects]   ──┘                │
                                       Produces base MP4
                                                │
                                                ▼
[Transcript JSON] ───────────────► [api_server.py ASS Compiler]
                                                │
                                       Produces styled .ass
                                                │
                                                ▼
                                   [FFmpeg Subtitle Burner]
                                   -vf "ass='...':fontsdir='...'"
                                                │
                                                ▼
                                    [Final Master Video.mp4]
                               (Saved to Downloads\AutoEditor\)
```

### Windows Path Escaping Standard
To prevent FFmpeg filtergraph syntax errors on Windows, all drive letters and paths are sanitized:
```python
escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
escaped_fonts = fonts_dir.replace("\\", "/").replace(":", "\\:")
vf_filter = f"ass='{escaped_ass}':fontsdir='{escaped_fonts}'"
```

### Automatic File Destination
Rendered videos download automatically in the user's browser and are saved locally to:
```text
C:\Users\<User>\Downloads\AutoEditor\<project_name>.mp4
```

---

## 20. Persistent Windows Background Watchdog (`service_manager.py`)

The companion AI server is supervised by an autonomous background daemon:

### Core Supervisor Architecture
- **Headless Execution:** Runs using `pythonw.exe` with process flags `CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`. No black console windows appear on screen.
- **Port Conflict Resolution (`free_port`):** Checks TCP port 4001 via `netstat`; if another process is occupying the port, it kills the blocking PID before launching.
- **Fast-Path Recovery (<1.5s):** Probes `GET /api/health` every 1.0 second. If `api_server.py` crashes or is killed, the supervisor respawns it immediately.
- **PID Synchronization:** Monitors `api_server.pid` and updates process IDs to prevent false crash detections.
- **Auto-Shutdown Watchdog:** Probes `http://localhost:4000` and scans for `AutoEditor.exe`. When the user closes AutoEditor, the supervisor waits for 60 consecutive seconds of inactivity, terminates the AI server, removes PID files, and exits cleanly.

---

## 21. Complete REST API Reference (Port 4001)

All endpoints accept and return JSON (unless handling binary audio/video downloads). CORS is enabled (`Access-Control-Allow-Origin: *`).

### `GET /api/health`
Checks server health, Whisper model cache state, and process ID.
- **Response (200 OK):**
  ```json
  {
    "ok": true,
    "service": "AutoEditor AI Engine",
    "model_cached": true,
    "version": "2.0",
    "pid": 15820
  }
  ```

### `GET /api/categories`
Returns the 8 style preset categories.
- **Response (200 OK):**
  ```json
  [
    {"id": "all", "name": "All Styles (64)"},
    {"id": "viral_shorts", "name": "Viral Shorts & TikTok"},
    {"id": "hormozi", "name": "Hormozi & Viral Retention"},
    {"id": "neon_glow", "name": "Neon Cyber Glow"},
    {"id": "cinematic", "name": "Cinematic & Documentary"},
    {"id": "boxed_pill", "name": "Boxed & Pill Badges"},
    {"id": "headline", "name": "Bold Punchy & Headline"},
    {"id": "comic_pop", "name": "Retro & Comic Pop"},
    {"id": "broadcast", "name": "Clean Corporate & Broadcast"}
  ]
  ```

### `GET /api/styles?category=<id>`
Returns styles metadata, fonts, colors, and CSS definitions. Omit query to return all 64 presets.

### `GET /api/sfx`
Returns the 12 transition sound effects catalog.

### `GET /sfx/<filename>`
Streams the raw 44.1kHz WAV sound effect file.

### `POST /api/transcribe`
Transcribes audio with word-level timestamps using Faster-Whisper.
- **Supported Formats:** `multipart/form-data` with `audio` file, raw binary body, or JSON `{"filepath": "..."}`.
- **Response (200 OK):**
  ```json
  {
    "ok": true,
    "id": "b3e19f12-...",
    "transcript": {
      "audio_file": "voiceover.wav",
      "duration": 4.5,
      "total_words": 8,
      "segments": [
        {
          "id": 0,
          "start": 0.0,
          "end": 2.4,
          "timestamp": "0.0s – 2.4s",
          "text": "Welcome to AutoEditor captions.",
          "words": [
            {"word": "Welcome", "start": 0.0, "end": 0.5},
            {"word": "to", "start": 0.5, "end": 0.8},
            {"word": "AutoEditor", "start": 0.8, "end": 1.7},
            {"word": "captions.", "start": 1.7, "end": 2.4}
          ]
        }
      ]
    },
    "text_path": "storage/b3e19f12.txt",
    "pdf_path": "storage/b3e19f12.pdf",
    "downloads": {
      "txt": "http://localhost:4001/api/download/txt?id=b3e19f12",
      "pdf": "http://localhost:4001/api/download/pdf?id=b3e19f12"
    }
  }
  ```

### `POST /api/generate-ass`
Compiles an ASS subtitle file from transcript data with custom styling and coordinates.
- **Payload:**
  ```json
  {
    "transcript": { ... },
    "style": "hormozi_bold",
    "width": 1920,
    "height": 1080,
    "pos_x": 0.50,
    "pos_y": 0.85,
    "font_scale": 1.2
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "ok": true,
    "style": "hormozi_bold",
    "ass_path": "storage/uuid.ass",
    "ass_content": "[Script Info]\n...",
    "pos_x": 0.5,
    "pos_y": 0.85,
    "font_scale": 1.2
  }
  ```

### `POST /api/mix-audio`
Pre-mixes voiceover audio with transition sound effects at specified millisecond timestamps.
- **Payload:** JSON or multipart with `audio` file, `voice_volume` (0.0–2.0), `sfx_volume` (0.0–1.0), and `sfx_events`:
  ```json
  [
    {"file": "whoosh_fast.wav", "timestamp": 4.5},
    {"file": "cinematic_boom.wav", "timestamp": 12.0}
  ]
  ```

### `POST /api/vocal-remove`
Suppresses speech frequencies from video or audio files while preserving transients.
- **Payload:** File upload or JSON with `filepath` and `vocal_volume` (0.0 to 1.0).

### `POST /api/burn-captions`
Burns compiled ASS subtitles into an MP4 video using FFmpeg.
- **Payload:** Multipart or JSON with `video_path`, `ass_path`, and `output_path`.

### `GET /api/download/txt?id=<id>` & `GET /api/download/pdf?id=<id>`
Downloads generated TXT or publication-quality PDF transcript files with `Content-Disposition: attachment`.

---

## 22. Repository Layout & File Index

```text
d:\AutoEditor\
├── AutoEditor.exe                  # Main Bun/Node application server (port 4000)
├── ffmpeg.exe                      # Bundled FFmpeg encoder with libass & GPU support
├── caption.ttf                     # Primary subtitle font asset
├── Start-AutoEditor-AI.bat         # 1-Click launcher (Starts watchdog & opens app)
├── Stop-AutoEditor.bat             # 1-Click shutdown utility (Kills all processes)
├── READ ME FIRST.txt               # Quick-start documentation for end users
├── PROJECT.md                      # Milestone 1 & 2 design notes
├── AUTOEDITOR_AI_CONTEXT.md        # Prompt guidelines for external AI chatbots
├── AUTOEDITOR_PROJECT_DOCUMENT.md  # THIS MASTER SPECIFICATION FILE
│
├── api_server.py                   # Multi-threaded HTTP server (port 4001)
├── transcribe_engine.py            # Faster-Whisper, ASS compiler, PDF/TXT exporter
├── service_manager.py              # Windows persistent background service supervisor
├── patch_page.py                   # AST patching utility for React client bundle
├── append_css.py                   # CSS build generator for AutoEditor styles
├── generate_sfx.py                 # Algorithmic generator for the 12 transition SFX
│
├── out/                            # Static SPA assets served at http://localhost:4000
│   ├── index.html                  # Main application HTML entry point
│   ├── auto_captions.js            # Frontend studio controller, playhead, layout manager
│   ├── auto_captions.css           # Caption studio modal, monitor box, and layout styles
│   ├── fonts/caption.ttf           # Web font asset
│   ├── sfx/                        # 12 synthesized WAV transition sound effects
│   │   ├── manifest.json           # SFX library catalog and metadata
│   │   ├── whoosh_fast.wav         # Fast Whip Whoosh
│   │   ├── cinematic_boom.wav      # Cinematic Sub Boom
│   │   └── ... (10 more WAVs)
│   └── _next/                      # React / Next.js chunk bundles
│       └── static/chunks/app/page-f2b7366e605a20db.js  # Main editor React chunk
│
├── storage/                        # Persistent working directory for transcripts & renders
│   ├── service_manager.pid         # PID of running supervisor
│   ├── api_server.pid              # PID of running AI engine
│   └── service_manager.log         # Supervisor operation logs
│
└── tests/                          # 111 Automated Test Suites
    ├── run_e2e_tests.py            # CLI test runner
    ├── e2e_results.json            # Machine-readable test execution report
    ├── test_new_features.py        # Verification of the 7 major studio features
    ├── test_vertical_and_audio.py  # Verification of 9:16 vertical mode & audio
    ├── test_colon_hyphen_equivalence.py # Verification of 0:05 vs 0-05 timestamps
    ├── test_intelligent_video_speed.py  # Verification of video auto-speed fitting
    └── e2e/                        # 4-Tier E2E opaque-box test suite
        ├── test_tier1_features.py     # Tier 1: Core Feature Coverage (35 tests)
        ├── test_tier2_boundaries.py   # Tier 2: Boundary & Corner Cases (35 tests)
        ├── test_tier3_combinations.py # Tier 3: Pairwise Combinations (5 tests)
        └── test_tier4_workloads.py    # Tier 4: Real-World Scenarios (3 tests)
```

---

## 23. Test Suite Architecture & Verification (111 Tests)

AutoEditor includes an extensive testing framework ensuring zero regressions across all features:

### Test Execution Summary
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```
*Current Suite Status:* **111 Tests Ran · 100% Passed · 0 Errors · 0 Failures**

| Test Module | Coverage Scope | Tests | Result |
|---|---|:---:|:---:|
| `tests/e2e/test_tier1_features.py` | Core feature contracts (M1 watchdog, Whisper, ASS, PDF badges) | 35 | 🟢 PASS |
| `tests/e2e/test_tier2_boundaries.py` | Edge cases (Unicode, zero audio, long strings, rapid segments) | 35 | 🟢 PASS |
| `tests/e2e/test_tier3_combinations.py` | Cross-feature interactions (all 64 styles $\times$ ASS compilation) | 5 | 🟢 PASS |
| `tests/e2e/test_tier4_workloads.py` | Real-world workflows (Workflow A: Transcribe/Export, B: Burn) | 3 | 🟢 PASS |
| `tests/test_new_features.py` | 7 Core studio features (drawer, monitor box, vocal cut, SFX) | 18 | 🟢 PASS |
| `tests/test_vertical_and_audio.py` | 9:16 vertical mode, AudioContext resume, silent audio generator | 8 | 🟢 PASS |
| `tests/test_colon_hyphen_equivalence.py` | Parser equivalence for `0:05` vs `0-05` across filename patterns | 4 | 🟢 PASS |
| `tests/test_intelligent_video_speed.py` | Mathematical speed ratios, speed badges, and FFmpeg PTS filters | 3 | 🟢 PASS |
| **Total** | **All AutoEditor Subsystems Verified** | **111** | **🟢 100% PASS** |

---

## 24. AI Chatbot Video Planning Guide & Output Templates

When an external user asks an AI assistant: *"Plan a video on topic X for AutoEditor"*, the AI must structure the response according to the following 3-part blueprint so that assets can be directly dragged and dropped into AutoEditor:

### 1. Narration Script (Audio Voiceover)
Write the master voiceover script at an average speaking rate of **2.5 words per second**. Note the estimated total audio duration.

### 2. AutoEditor Storyboard Table
Map every visual scene to strict timestamp filenames. Ensure filenames use either `M-SS.ext` or `M:SS.ext`:

| Scene # | Timestamp | Recommended Filename | Voiceover Line (Narration) | Visual Prompt (Midjourney / Flux / Leonardo) | Transition / Motion |
|:---:|:---:|:---|---|---|---|
| 1 | `0:00` | `0-00.png` | "In a world driven by AI..." | Cinematic close-up shot of a glowing cybernetic brain, volumetric lighting, 8k | Crossfade / Zoom In |
| 2 | `0:05` | `0-05.png` | "Everything is moving faster than ever." | Futuristic cyberpunk metropolis with flying transit cars in rain, photorealistic | Wipe Left / Pan |
| 3 | `0:11.5`| `0-11.5.mp4` | "Here is how you can stay ahead." | Video clip of creative editor working at multi-monitor workstation, cinematic | Auto-Speed Fit / None |
| 4 | `0:18` | `0-18.png` | "Start building today." | Clean minimalist studio desk with sleek laptop displaying creative timeline | Fade to Black / Zoom Out |

### 3. Storyboard Rules for AI
1. **First Asset Rule:** Scene 1 must always start at `0-00.png` or `0-00.mp4` to prevent initial black frames.
2. **Gap Rule:** The interval between consecutive scene timestamps determines scene duration. (e.g. `0-00` to `0-05` = 5.0 seconds).
3. **Decimal Timestamps:** Decimal timestamps (`0-04.5.png`, `5.5.mp4`) are fully supported for fast-paced pacing.
4. **Auto-Speed for Videos:** Mention if a video clip will be automatically accelerated to fit a tight slot.
5. **Captions Style Recommendation:** Suggest one of the 64 presets (e.g. `hormozi_bold` for business/growth, `bouncy_shorts` for TikTok/Shorts, `neon_glow` for tech/cyberpunk, `minimalist_modern` for documentaries).

---
*(End of Master Document — TryAIToday AutoEditor v2)*
