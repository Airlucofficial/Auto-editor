# Project: AutoEditor Speech Transcription & Caption Studio

## Architecture
AutoEditor is a desktop application combining a compiled native Express frontend server (`AutoEditor.exe` on port 4000) serving static assets from `out/`, with a persistent local Python AI engine on port 4001 (`api_server.py`) monitored by a headless Windows service manager (`service_manager.py`).

### Data Flow
1. **Audio Import & Transcription (Workflow A)**:
   - User imports audio/video via web UI (`out/auto_captions.js`).
   - UI sends audio to `api_server.py` (`POST /api/transcribe`).
   - `transcribe_engine.py` runs `faster-whisper` (small/base with beam size 5, speech padding 400ms, VAD filter) with in-memory model caching (`_MODEL_CACHE`).
   - Transcription engine generates segments with exact word timings and second-based timestamps (`0.0s – 3.4s`).
   - Results are stored in `storage/<id>.json`, `storage/<id>.txt`, and `storage/<id>.pdf`.
   - UI renders transcript segments with `0.0s – 3.4s` badges; user can 1-click download TXT or PDF with visual pill badges.
2. **Preset Browsing & Video Caption Burning (Workflow B)**:
   - UI loads 64 curated CapCut-style presets across 8 categories from `GET /api/styles`.
   - User filters presets using category pills (`All (64)`, `Viral Shorts`, `Hormozi`, etc.) and search bar.
   - User watches real-time word-by-word active animation preview synchronized with audio.
   - User selects preset and requests video burning (`POST /api/burn-captions` or client burn trigger).
   - Backend compiles ASS subtitle file with Windows-safe path escaping (`ass='D\:/...':fontsdir='...'`) and runs `ffmpeg.exe` to produce captioned MP4 video.
3. **Background Persistence**:
   - `service_manager.py` runs via `pythonw.exe` with `CREATE_NO_WINDOW | DETACHED_PROCESS`.
   - Probes `GET /api/health` every 3 seconds; auto-restarts `api_server.py` if process exits or becomes unresponsive.
   - UI polls `/api/health` and mounts real-time `🟢 AI Engine Ready` badge in `.bar__actions`.

## Code Layout & Write Boundaries
- `api_server.py`: HTTP API routes, ThreadingHTTPServer, `/api/health`, `/api/styles`, `/api/transcribe`, `/api/generate-ass`, `/api/burn-captions`, `/api/download/*`.
- `transcribe_engine.py`: Faster-Whisper transcription, in-memory model cache, VAD, word timing alignment, second-based timestamp formatter (`0.0s – 3.4s`), TXT export, ReportLab PDF export with visual pill badges, 64 CapCut-style presets catalog across 8 categories, ASS compilation.
- `service_manager.py`: Windows persistent background supervisor, process monitoring, auto-start, auto-recovery.
- `Start-AutoEditor-AI.bat`: Launch script orchestrating service manager and application.
- `out/auto_captions.js`: Web UI client logic, `🟢 AI Engine Ready` top bar badge, category filter pills, search input, live word-by-word animation preview, two-track workflows.
- `out/auto_captions.css`: Caption studio modal styling, category pills, search bar, visual badges, preview style classes.
- `tests/`: Automated test suite, E2E opaque-box test runner, fixtures, and verification scripts.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Persistent Windows Background Service | Headless watchdog running via pythonw.exe with CREATE_NO_WINDOW, auto-recovering api_server | M1 | ORIGINAL_REQUEST R1 |
| 2 | Threading HTTP Server & Health Check | ThreadingHTTPServer on port 4001 with explicit Content-Length & Connection: close; fast /api/health | M1 | ORIGINAL_REQUEST R1 |
| 3 | Auto-Start Integration | Windows batch and auto-start capability ensuring AI engine stays running | M1 | ORIGINAL_REQUEST R1 |
| 4 | UI Real-Time Ready Indicator | Main top bar (.bar__actions) mounts real-time `🟢 AI Engine Ready` status badge polling health | M2 | ORIGINAL_REQUEST Acceptance Criteria |
| 5 | High-Accuracy Whisper Engine | Whisper small/base with beam search 5 and speech padding (400ms) | M1 | ORIGINAL_REQUEST R2 |
| 6 | Advanced VAD Filtering | Voice Activity Detection ensuring natural sentence boundaries without awkward cutoffs | M1 | ORIGINAL_REQUEST R2 |
| 7 | Word-Level Timing Alignment | Accurate word-by-word timestamps preserved in segments and output data | M1 | ORIGINAL_REQUEST R2 |
| 8 | In-Memory Model Caching | _MODEL_CACHE preventing ~20s reload latency across transcription calls | M1 | Survey 1 Finding |
| 9 | Second-Based Timestamp Format | Strict `0.0s – 3.4s` (`X.Xs – Y.Ys`) formatting helper | M1 | ORIGINAL_REQUEST R3 |
| 10 | TXT Export with Second Timestamps | Downloadable .txt files using `[0.0s – 3.4s]` format | M1 | ORIGINAL_REQUEST R3 |
| 11 | PDF Export with Visual Badges | Downloadable .pdf with visual rounded pill badges (`#EEF2FF` fill, `#1E40AF` text) | M1 | ORIGINAL_REQUEST R3 |
| 12 | UI Second-Based Segment Badges | Web UI transcript segment cards displaying formatted second badges `0.0s – 3.4s` | M2 | ORIGINAL_REQUEST R3 |
| 13 | 64 Presets Across 8 Categories | 64 distinct CapCut-style presets (8 per category) covering typography, colors, borders, shadows | M2 | ORIGINAL_REQUEST R4 |
| 14 | Interactive Category Filter Pills | Filter pills (`All (64)`, `Viral Shorts`, `Hormozi`, etc.) in Caption Studio UI | M2 | ORIGINAL_REQUEST R4 |
| 15 | Real-Time Search Bar | Search input filtering presets by name, category, and tags in real time | M2 | ORIGINAL_REQUEST R4 |
| 16 | Real-Time Word-by-Word Live Preview | Interactive player animating active word highlights in real time | M2 | ORIGINAL_REQUEST R4 |
| 17 | Robust ASS Subtitle Compilation | Clean ASS v4.00+ compilation with scale pops, pill boxes, and character sanitization | M2 | ORIGINAL_REQUEST R4 |
| 18 | FFmpeg Subtitle Burning Pipeline | Hardened Windows path escaping (`ass='D\:/...':fontsdir='...'`) burning ASS to MP4 | M2 | ORIGINAL_REQUEST R4 |
| 19 | Workflow A (Audio-to-Transcript) | Audio import -> High-accuracy transcription -> Second timestamps -> 1-click TXT/PDF download | M3 | ORIGINAL_REQUEST R5 |
| 20 | Workflow B (Final Video Captions) | Video -> Extract audio / transcribe -> Select preset with live preview -> Burn via FFmpeg | M3 | ORIGINAL_REQUEST R5 |
| 21 | Opaque-Box E2E Test Suite | Automated test suite verifying timestamps, all 64 presets, FFmpeg video burning, server health | E2E / M3 | ORIGINAL_REQUEST Acceptance Criteria |
| 22 | Adversarial Hardening | Stress testing edge cases (special chars, long audio, unicode, fast speech) | M3 | Orchestration Plan |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Suite Track | Design and implement opaque-box test runner, fixtures, and assertions (Tiers 1-4) producing TEST_READY.md | none | IN_PROGRESS |
| M1 | Backend AI Engine & Persistent Windows Service | service_manager.py, ThreadingHTTPServer, Whisper model caching, VAD, speech padding, word alignment, 0.0s – 3.4s timestamps (JSON/TXT/PDF) | none | IN_PROGRESS |
| M2 | Caption Studio, 64 Presets & FFmpeg Subtitle Pipeline | 64 presets across 8 categories, ASS compilation, FFmpeg burning, UI category pills, search bar, live preview, `🟢 AI Engine Ready` badge | M1 | PLANNED |
| M3 | Two-Track Workflows, E2E Pass & Adversarial Hardening | End-to-end integration of Workflow A and Workflow B, 100% E2E test suite pass, Tier 5 adversarial stress testing | M1, M2, E2E | PLANNED |

## Interface Contracts

### HTTP API Endpoints (`api_server.py:4001`)
- `GET /api/health` -> `{"ok": true, "service": "AutoEditor AI Engine", "model_cached": bool, "version": "2.0"}`
- `GET /api/styles` -> `{"styles": [ { "id": str, "name": str, "category": str, "font": str, "fontsize": int, "primary_color": str, "secondary_color": str, "outline_color": str, "outline": int, "shadow": int, "preview_class": str, "desc": str, ... } ]}`
- `POST /api/transcribe` -> multipart/form-data with file or JSON with path:
  Response: `{"id": str, "segments": [{"id": int, "start": float, "end": float, "text": str, "timestamp": "0.0s – 3.4s", "words": [{"word": str, "start": float, "end": float}]}], "text_path": str, "pdf_path": str}`
- `POST /api/generate-ass` -> JSON `{"segments": [...], "style": str}`:
  Response: `{"ok": true, "ass_path": str, "ass_content": str}`
- `POST /api/burn-captions` -> JSON `{"video_path": str, "ass_path": str, "output_path": str}`:
  Response: `{"ok": true, "output_video": str, "duration": float}`
- `GET /api/download/txt?id=<id>` -> file download with `Content-Disposition`
- `GET /api/download/pdf?id=<id>` -> file download with `Content-Disposition`

### Timestamp Formatting Standard
- Function: `format_second_timestamp(start: float, end: float) -> str`
- Format: `f"{start:.1f}s – {end:.1f}s"` (e.g. `"0.0s – 3.4s"`)
- TXT format: `[0.0s – 3.4s] Speaker: transcribed text...`
- PDF format: Table cell with rounded pill badge containing `"0.0s – 3.4s"`
- UI format: `<span class="cap-ts-badge">0.0s – 3.4s</span>`

### FFmpeg Filter Escaping Standard
- Windows path escaping: replace `\` with `/`, escape `:` as `\:`, wrap in single quotes:
  `filter_str = f"ass='{escaped_ass_path}':fontsdir='{escaped_font_dir}'"`
- Example: `-vf "ass='d\:/AutoEditor/storage/sub.ass':fontsdir='d\:/AutoEditor'"`
