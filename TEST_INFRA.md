# Test Infrastructure & Specification Architecture — AutoEditor AI Studio

## 1. Overview & System Under Test (SUT)

AutoEditor AI Studio is a high-accuracy speech transcription and CapCut-style caption studio running on Windows desktop. The system under test consists of five primary components:
1. **Persistent Windows Background Service (`service_manager.py`)**: Headless watchdog daemon operating via `pythonw.exe` (`CREATE_NO_WINDOW | DETACHED_PROCESS`), supervising the local AI engine with automatic crash recovery.
2. **AI Companion HTTP Server (`api_server.py:4001`)**: Multi-threaded HTTP server exposing RESTful endpoints for health probing, style cataloging, faster-whisper transcription, ASS subtitle compilation, video subtitle burning, and transcript file downloads.
3. **Core Transcription & Caption Engine (`transcribe_engine.py`)**: High-accuracy `faster-whisper` integration (small/base models, beam search 5, speech padding 400ms, VAD filtering, word alignment), in-memory model cache, second-based timestamp formatter (`0.0s – 3.4s`), TXT/PDF export generators with visual pill badges, and 64 curated CapCut-style presets across 8 categories.
4. **Desktop Video Subtitle Pipeline (`ffmpeg.exe`)**: Local FFmpeg executable with `libass` support, executing subtitle burning with Windows-safe path escaping.
5. **Static Web UI Client (`out/index.html`, `out/auto_captions.js`, `out/auto_captions.css`)**: Frontend interface displaying real-time `🟢 AI Engine Ready` status, category filter pills, instant search bar, interactive preview player with word-by-word active animation, and one-click downloads.

This test infrastructure document formalizes the opaque-box, specification-driven testing strategy verifying all 22 features defined in `PROJECT.md` across four comprehensive tiers.

---

## 2. Testing Methodologies

### 2.1 Category-Partition Method
Functional inputs, environments, and response partitions are categorized into discrete equivalence classes to ensure exhaustive coverage without redundant duplication:

| Functional Domain | Input Parameters / Environment | Partitions & Equivalence Classes |
|-------------------|--------------------------------|----------------------------------|
| **HTTP API Requests** | `Content-Type`, `Method`, `Path`, `Payload` | - Valid multipart/form-data with binary WAV/MP3<br>- Valid JSON with `filepath`<br>- Raw binary audio body<br>- Empty body / missing headers<br>- Malformed JSON syntax<br>- Unknown URL paths (404)<br>- Unsupported HTTP methods (405/501) |
| **Audio Ingestion** | File format, sample rate, channels, duration | - 16kHz/22.05kHz/44.1kHz/48kHz WAV<br>- Mono vs Stereo<br>- Standard speech (2s – 60s)<br>- Very short speech (<0.5s)<br>- Pure silence (VAD active test)<br>- High noise / fast speech |
| **Timestamps** | `start: float`, `end: float` | - Zero start (`0.0s`)<br>- Sub-second duration (`0.0s – 0.4s`)<br>- Multi-second duration (`3.4s – 7.8s`)<br>- Minute-scale boundary (`59.9s – 61.2s`)<br>- Hour-scale boundary (`3599.5s – 3602.1s`) |
| **Caption Presets** | Preset ID, Category, Typography, FX | - 8 Categories: Viral Shorts, Hormozi, Neon Cyber Glow, Cinematic, Boxed & Pill, Bold Punchy, Retro Comic, Clean Corporate<br>- 64 distinct presets (8 per category)<br>- Active color highlights, stroke outlines, drop shadows, scale pops, pill backplates |
| **ASS Subtitle Compilation** | Styles, Events, Dialogue strings | - Standard alphanumeric text<br>- Special punctuation and symbols (`&`, `<`, `>`, `"`, `'`)<br>- ASS control characters (`{`, `}`, `\`, `\N`)<br>- Non-ASCII & Unicode (accents, emojis, CJK)<br>- Zero-length / whitespace-only words |
| **FFmpeg Subtitle Burning** | Video input, ASS subtitle path, output path | - Local absolute Windows paths (`D:\AutoEditor\...`)<br>- Spaces in paths<br>- Windows drive letter escaping (`d\:/...`)<br>- Valid font directory resolution (`caption.ttf`) |

### 2.2 Boundary Value Analysis (BVA)
Boundary Value Analysis focuses on values at, immediately below, and immediately above operational and structural boundaries:
- **Audio Durations**: $0.000\text{s}$ (zero length), $0.100\text{s}$ (minimum audio slice), $0.400\text{s}$ (VAD silence threshold boundary), $3600.0\text{s}$ (hour boundary formatting).
- **Text & Word Lengths**: Empty string `""`, single character `"A"`, whitespace `"   "`, multiline text `"\n\r"`, long uninterrupted token (100+ chars).
- **Preset Catalog Indices**: Index 0, 7, 8, 15, 63, 64 (catalog boundary, ensuring exactly 64 curated styles across 8 categories with 8 styles per category).
- **HTTP Payload Sizes**: 0 bytes, 1 byte, standard payload (50KB – 2MB), oversized request limits.
- **Timestamp Formatter**: `0.001 -> 0.0s`, `0.050 -> 0.1s`, `0.099 -> 0.1s`, `3.35 -> 3.4s`, matching strict `f"{start:.1f}s – {end:.1f}s"`.

### 2.3 Pairwise Combinatorial Testing
Pairwise combinatorial testing verifies that multi-feature interactions function correctly across orthogonal dimensions:
- **Pairwise Combination 1**: `VAD Filtering (F6)` $\times$ `Second-Based Timestamp Formatting (F9)`: Verifies that segments split naturally by VAD boundaries format cleanly into `X.Xs – Y.Ys` without zero-length or inverted time intervals.
- **Pairwise Combination 2**: `64 Caption Presets (F13)` $\times$ `ASS Subtitle Compilation (F17)`: Verifies that every single one of the 64 presets compiles to syntactically valid ASS v4.00+ script headers, styles, and dialogue events.
- **Pairwise Combination 3**: `Transcription Alignment (F7)` $\times$ `PDF Visual Badge Generation (F11)`: Verifies that word-aligned segments render into ReportLab flowable tables with rounded `#EEF2FF` pill badges.
- **Pairwise Combination 4**: `Threading HTTP Server (F2)` $\times$ `TXT/PDF File Downloads (F10, F11)`: Verifies concurrent download requests with proper `Content-Length`, `Content-Disposition`, and non-blocking socket handling.
- **Pairwise Combination 5**: `ASS Compilation (F17)` $\times$ `FFmpeg Subtitle Burning (F18)`: Verifies that compiled styles with Windows drive letter escaping burn into MP4 video with FFmpeg without filter graph parsing errors.

### 2.4 Real-World Workloads
Real-world workloads evaluate the full system under realistic end-user operational workflows:
- **Workflow A (Audio-to-Transcript)**: User imports an audio recording (`test_sample.wav`) -> Server transcribes with Faster-Whisper + VAD -> Generates word-aligned segments with `0.0s – 3.4s` timestamps -> Generates downloadable TXT and visual-badge PDF -> User downloads both files -> Validates text fidelity, timestamp formatting, and PDF structural integrity.
- **Workflow B (Final Video Captions)**: User submits a master video -> Extracts audio / transcribes -> Selects CapCut preset from catalog -> Compiles styled ASS subtitle file -> Invokes FFmpeg burn pipeline -> Produces captioned MP4 video -> Probes output video stream duration, resolution, and valid H.264 video track.

---

## 3. Four-Tier Test Suite Architecture

The executable test suite is located in `d:\AutoEditor\tests\e2e\` and is structured into four distinct tiers:

```
d:\AutoEditor\tests\
├── e2e\
│   ├── __init__.py
│   ├── conftest_utils.py          # Shared fixtures, mock servers, audio/video generators
│   ├── test_tier1_features.py     # Tier 1: Feature Coverage (>=5 tests per feature area)
│   ├── test_tier2_boundaries.py   # Tier 2: Boundary Value Analysis & Edge Cases
│   ├── test_tier3_combinations.py # Tier 3: Pairwise Cross-Feature Combinations
│   └── test_tier4_workloads.py    # Tier 4: Real-World Workload Scenarios (Workflow A & B)
└── run_e2e_tests.py               # Unified CLI Test Runner with JSON reporting & exit codes
```

### 3.1 Tier 1: Feature Coverage
Validates the primary happy path and core specification contract for each of the 22 features defined in `PROJECT.md § Feature Inventory`.
- **Area 1: Service Persistence & Server Infrastructure** (Features 1, 2, 3)
  - `test_f1_service_manager_structure`: Verifies `service_manager.py` watchdog logic and process supervision.
  - `test_f2_health_endpoint_response`: Verifies `GET /api/health` returns HTTP 200, `{"ok": true, ...}`.
  - `test_f2_http_server_threading_headers`: Verifies HTTP server handles Connection and Content-Length headers correctly.
  - `test_f3_batch_launcher_script`: Verifies `Start-AutoEditor-AI.bat` contains headless launch configuration.
  - `test_f1_service_auto_restart_contract`: Verifies auto-recovery mechanism on engine process termination.
- **Area 2: Transcription Engine, VAD, Alignment & Caching** (Features 5, 6, 7, 8)
  - `test_f5_whisper_engine_parameters`: Verifies `beam_size=5` and speech padding configuration.
  - `test_f6_vad_filter_enabled`: Verifies VAD filtering parameter structure (`min_silence_duration_ms=400`).
  - `test_f7_word_level_timing_alignment`: Verifies word-level start/end timestamps are present and monotonic.
  - `test_f8_model_cache_persistence`: Verifies `_MODEL_CACHE` preserves loaded model instances across calls.
  - `test_f5_transcribe_audio_execution`: Verifies end-to-end audio transcription of reference WAV file.
- **Area 3: Second-Based Timestamps & Document Exports** (Features 9, 10, 11)
  - `test_f9_format_second_timestamp_contract`: Verifies `format_second_timestamp(start, end)` produces strict `0.0s – 3.4s`.
  - `test_f10_txt_export_format`: Verifies exported TXT uses `[0.0s – 3.4s]` format markers.
  - `test_f11_pdf_export_structure`: Verifies PDF export generates valid binary PDF with visual table badges.
  - `test_f11_pdf_badge_styling_contract`: Verifies PDF badge color specifications (`#EEF2FF` fill, `#1E40AF` text).
  - `test_f9_transcript_segments_timestamp_field`: Verifies JSON output contains formatted `timestamp` string in every segment.
- **Area 4: Web UI Components & Contract Conformance** (Features 4, 12, 14, 15, 16)
  - `test_f4_ui_ready_indicator_badge`: Verifies `out/auto_captions.js` contains `🟢 AI Engine Ready` badge logic.
  - `test_f12_ui_second_based_badge_rendering`: Verifies frontend renders segment timestamp badges with class `cap-ts-badge`.
  - `test_f14_ui_category_filter_pills`: Verifies UI contains 8 category filter pills including `All`.
  - `test_f15_ui_realtime_search_bar`: Verifies UI search bar filtering logic by preset name, category, and tags.
  - `test_f16_ui_word_by_word_live_preview`: Verifies interactive player word highlight animation frames.
- **Area 5: 64 Caption Presets Catalog & ASS Compilation** (Features 13, 17)
  - `test_f13_presets_count_and_categories`: Verifies preset catalog contains 64 presets across 8 categories (8 per category).
  - `test_f13_preset_schema_completeness`: Verifies required preset fields (`id`, `name`, `category`, `font`, `fontsize`, `primary_color`, `outline_color`).
  - `test_f17_ass_compilation_script_info`: Verifies compiled ASS contains standard `[Script Info]`, `[V4+ Styles]`, and `[Events]`.
  - `test_f17_ass_dialogue_timing_format`: Verifies ASS dialogue timestamps adhere to `H:MM:SS.cc` centisecond format.
  - `test_f17_ass_style_definitions`: Verifies ASS styles match preset typography, colors, and margins.
- **Area 6: FFmpeg Subtitle Burning Pipeline** (Feature 18)
  - `test_f18_ffmpeg_binary_availability`: Verifies `ffmpeg.exe` exists, is executable, and supports `libass`.
  - `test_f18_windows_path_escaping`: Verifies path escaping standard: `ass='D\:/...':fontsdir='...'`.
  - `test_f18_font_asset_resolution`: Verifies `caption.ttf` exists and is accessible.
  - `test_f18_ffmpeg_burn_command_construction`: Verifies parameter generation for subtitle filter graph.
  - `test_f18_ffmpeg_video_burn_execution`: Verifies FFmpeg generates valid playable MP4 with burned subtitles.
- **Area 7: End-to-End Workflows & Adversarial Hardening** (Features 19, 20, 21, 22)
  - `test_f19_workflow_a_endpoint_flow`: Verifies `/api/transcribe` -> `/api/download/txt` -> `/api/download/pdf`.
  - `test_f20_workflow_b_endpoint_flow`: Verifies `/api/styles` -> `/api/generate-ass` -> `/api/burn-captions`.
  - `test_f21_opaque_box_test_suite_readiness`: Verifies all test modules load and execute autonomously.
  - `test_f22_adversarial_special_characters`: Verifies handling of quotes, angle brackets, and ampersands.
  - `test_f22_adversarial_unicode_and_emojis`: Verifies handling of international unicode and emoji symbols.

### 3.2 Tier 2: Boundary & Corner Cases
Evaluates robustness at extreme parameter values, malformed data, and edge conditions (>=5 tests per feature area):
- Empty audio file / 0-byte upload handling.
- Silence-only audio (VAD non-speech handling).
- Audio with single short syllable (<0.2s).
- Long multi-minute audio simulation.
- Timestamp boundaries: exact `0.0s`, negative clamp protection, large duration boundaries.
- Text boundaries: empty transcript segments, whitespace-only strings, extremely long uninterrupted strings.
- ASS subtitle boundaries: special ASS tag syntax inside dialogue (`{`, `}`, `\N`, `\h`), backslash escapes.
- Preset catalog boundaries: invalid / non-existent style ID fallback to default (`hormozi_bold`).
- HTTP API boundaries: missing multipart boundary, invalid JSON payload, missing `id` query parameter on download endpoints.
- Path boundaries: non-existent filepaths, paths with spaces, unicode paths.

### 3.3 Tier 3: Cross-Feature Combinations
Evaluates pairwise cross-feature interactions:
- **Pair 1**: `VAD Filtering (F6)` + `Timestamp Formatting (F9)`: Segment boundaries match VAD intervals and format to `0.0s – X.Xs`.
- **Pair 2**: `64 Presets Catalog (F13)` + `ASS Subtitle Compilation (F17)`: Exhaustive iteration verifying every single preset compiles valid ASS.
- **Pair 3**: `Word-Level Timing (F7)` + `PDF Visual Badges (F11)`: Word timing aggregation into segment badges rendered in ReportLab table cells.
- **Pair 4**: `Threading Server (F2)` + `Concurrent File Downloads (F10, F11)`: Multi-threaded simultaneous downloads of TXT and PDF.
- **Pair 5**: `ASS Compilation (F17)` + `FFmpeg Subtitle Burning (F18)`: ASS output fed directly to FFmpeg filter graph.
- **Pair 6**: `Batch Script (F3)` + `Service Manager (F1)` + `Health Check (F2)`: Verifying daemon invocation and port 4001 readiness probe.

### 3.4 Tier 4: Real-World Workloads
Executes full multi-step realistic workflows end-to-end:
- **Workload A (Audio-to-Transcript Pipeline)**:
  1. Ingest realistic 7.68s speech audio (`test_sample.wav`).
  2. Perform Faster-Whisper transcription.
  3. Validate transcript structure: text contains `"Auto Editor"` / `"transcription"`, duration > 7s, segments with `0.0s – 3.4s` timestamps.
  4. Generate and download clean TXT file; assert header, word count, and `[X.Xs – Y.Ys]` timestamps.
  5. Generate and download publication PDF; assert binary `%PDF` header, non-zero size (>2000 bytes), and valid page stream.
- **Workload B (Final Video Captions Pipeline)**:
  1. Generate synthetic reference MP4 video with audio track using FFmpeg.
  2. Transcribe audio to word-level segments.
  3. Select style preset from catalog (e.g. `hormozi_bold`).
  4. Compile styled ASS subtitle file with Windows drive letter escaping (`ass='D\:/...'`).
  5. Burn subtitles into target MP4 video using `ffmpeg.exe`.
  6. Probe output video using FFmpeg/ffprobe; verify exit code 0, non-empty file, and valid duration.

---

## 4. Feature Coverage Traceability Matrix

| Feature ID | Feature Name | Tier 1 Test Class / Method | Tier 2 Test Method | Tier 3 Test Method | Tier 4 Test Method |
|:---|:---|:---|:---|:---|:---|
| **F1** | Persistent Windows Service | `TestTier1ServiceInfrastructure.test_f1_service_manager_structure` | `test_t2_service_manager_missing_target` | `test_t3_service_and_health_probe` | `test_t4_workflow_a_resilience` |
| **F2** | Threading Server & Health | `TestTier1ServiceInfrastructure.test_f2_health_endpoint_response` | `test_t2_api_malformed_requests` | `test_t3_concurrent_downloads` | `test_t4_workflow_a_e2e` |
| **F3** | Auto-Start Integration | `TestTier1ServiceInfrastructure.test_f3_batch_launcher_script` | `test_t2_batch_script_missing_env` | `test_t3_batch_and_service_manager` | `test_t4_workflow_a_e2e` |
| **F4** | UI Real-Time Ready Indicator | `TestTier1WebUIComponents.test_f4_ui_ready_indicator_badge` | `test_t2_ui_badge_server_offline_state` | `test_t3_ui_and_health_polling` | `test_t4_workflow_a_e2e` |
| **F5** | High-Accuracy Whisper Engine | `TestTier1TranscriptionEngine.test_f5_whisper_engine_parameters` | `test_t2_audio_zero_length` | `test_t3_whisper_and_txt_export` | `test_t4_workflow_a_e2e` |
| **F6** | Advanced VAD Filtering | `TestTier1TranscriptionEngine.test_f6_vad_filter_enabled` | `test_t2_audio_pure_silence` | `test_t3_vad_and_timestamp_format` | `test_t4_workflow_a_e2e` |
| **F7** | Word-Level Timing Alignment | `TestTier1TranscriptionEngine.test_f7_word_level_timing_alignment` | `test_t2_single_word_audio` | `test_t3_word_timing_and_pdf_badge`| `test_t4_workflow_a_e2e` |
| **F8** | In-Memory Model Caching | `TestTier1TranscriptionEngine.test_f8_model_cache_persistence` | `test_t2_model_cache_invalidation` | `test_t3_cache_and_repeated_calls`| `test_t4_workflow_a_e2e` |
| **F9** | Second-Based Timestamp Format| `TestTier1TimestampsAndExports.test_f9_format_second_timestamp_contract` | `test_t2_timestamp_extreme_values` | `test_t3_timestamp_and_all_exports` | `test_t4_workflow_a_e2e` |
| **F10**| TXT Export with Second Timestamps| `TestTier1TimestampsAndExports.test_f10_txt_export_format` | `test_t2_txt_export_empty_segments` | `test_t3_txt_and_pdf_parity` | `test_t4_workflow_a_e2e` |
| **F11**| PDF Export with Visual Badges | `TestTier1TimestampsAndExports.test_f11_pdf_export_structure` | `test_t2_pdf_export_unicode_text` | `test_t3_pdf_and_word_alignment` | `test_t4_workflow_a_e2e` |
| **F12**| UI Second-Based Segment Badges| `TestTier1WebUIComponents.test_f12_ui_second_based_badge_rendering` | `test_t2_ui_badge_empty_segments` | `test_t3_ui_and_transcript_render` | `test_t4_workflow_a_e2e` |
| **F13**| 64 Presets Across 8 Categories| `TestTier1PresetsAndASS.test_f13_presets_count_and_categories` | `test_t2_preset_unknown_fallback` | `test_t3_all_64_presets_ass_compile` | `test_t4_workflow_b_e2e` |
| **F14**| Interactive Category Filter Pills| `TestTier1WebUIComponents.test_f14_ui_category_filter_pills` | `test_t2_ui_pill_click_filtering` | `test_t3_ui_pill_and_preset_count` | `test_t4_workflow_b_e2e` |
| **F15**| Real-Time Search Bar | `TestTier1WebUIComponents.test_f15_ui_realtime_search_bar` | `test_t2_ui_search_special_chars` | `test_t3_ui_search_and_pill_filter` | `test_t4_workflow_b_e2e` |
| **F16**| Word-by-Word Live Preview | `TestTier1WebUIComponents.test_f16_ui_word_by_word_live_preview` | `test_t2_ui_preview_missing_words` | `test_t3_ui_preview_and_ass_parity` | `test_t4_workflow_b_e2e` |
| **F17**| Robust ASS Subtitle Compilation| `TestTier1PresetsAndASS.test_f17_ass_compilation_script_info` | `test_t2_ass_special_chars_escaping` | `test_t3_ass_and_ffmpeg_burning` | `test_t4_workflow_b_e2e` |
| **F18**| FFmpeg Subtitle Burning | `TestTier1FFmpegPipeline.test_f18_ffmpeg_binary_availability` | `test_t2_ffmpeg_missing_video_file` | `test_t3_ffmpeg_and_ass_escaping` | `test_t4_workflow_b_e2e` |
| **F19**| Workflow A (Audio-to-Transcript)| `TestTier1Workflows.test_f19_workflow_a_endpoint_flow` | `test_t2_workflow_a_corrupt_audio` | `test_t3_workflow_a_full_cycle` | `test_t4_workflow_a_e2e` |
| **F20**| Workflow B (Final Video Captions)| `TestTier1Workflows.test_f20_workflow_b_endpoint_flow` | `test_t2_workflow_b_missing_ass` | `test_t3_workflow_b_full_cycle` | `test_t4_workflow_b_e2e` |
| **F21**| Opaque-Box E2E Test Suite | `TestTier1Workflows.test_f21_opaque_box_test_suite_readiness` | `test_t2_test_runner_cli_args` | `test_t3_test_runner_json_output` | `test_t4_suite_meta_verification` |
| **F22**| Adversarial Hardening | `TestTier1Workflows.test_f22_adversarial_special_characters` | `test_t2_adversarial_malformed_input`| `test_t3_adversarial_stress` | `test_t4_adversarial_workload` |

---

## 5. Test Runner Execution & Validation Protocol

The test suite is driven by `tests/run_e2e_tests.py` using Python's standard `unittest` engine.

### CLI Usage:
```powershell
# Run entire test suite across all 4 tiers
.venv\Scripts\python.exe tests/run_e2e_tests.py

# Run specific tier
.venv\Scripts\python.exe tests/run_e2e_tests.py --tier 1
.venv\Scripts\python.exe tests/run_e2e_tests.py --tier 2
.venv\Scripts\python.exe tests/run_e2e_tests.py --tier 3
.venv\Scripts\python.exe tests/run_e2e_tests.py --tier 4

# Run with verbose output
.venv\Scripts\python.exe tests/run_e2e_tests.py -v

# Run with JSON results export
.venv\Scripts\python.exe tests/run_e2e_tests.py --json-out tests/e2e_results.json
```

### Exit Codes:
- `0`: All executed tests passed.
- `1`: One or more tests failed or encountered errors.
- `2`: Configuration or runtime environment error.
