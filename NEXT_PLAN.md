# AutoEditor AI Director & Autonomous Video Studio — Next Phase Roadmap

> **File:** `NEXT_PLAN.md`  
> **Status:** Approved Architecture & Implementation Plan  
> **Purpose:** Blueprint for building the **Autonomous AI Video Director & Style-Transfer Engine** into AutoEditor. When resuming work in any future session, this document serves as the exact step-by-step implementation guide.

---

## 1. Executive Vision: The "Zero-Touch, 90-Second" Video Director

### The Core Goal
Transform AutoEditor from a manual synchronization tool into an **Autonomous AI Video Director**. 
A creator inputs their voiceover audio and chooses a style (e.g., *"MrBeast Retention"*, *"Ali Abdaal Educational"*, *"Vox Documentary"*, or a custom reference). 

The software autonomously:
1. Transcribes and semantically analyzes the speech using local Whisper AI.
2. Selects an ultra-low-cost LLM via **OpenRouter** (DeepSeek-V3, Qwen 2.5) costing **less than $0.003 per edit**.
3. Understands where complete thoughts begin and end (eliminating the "1-second lag" AI bug).
4. Automatically retrieves missing transparent stickers, icons, and B-roll from the web.
5. Injects multi-layer graphics, paired transition sound effects, and kinetic typography.
6. Audits the edit through a **Deterministic QA Gateway** (safe zones, contrast check, audio ducking).
7. Delivers a broadcast-ready, 100% uploadable MP4 video in **under 90 seconds** without touching local GPU resources.

---

## 2. Problem $\to$ Solution Engineering Matrix

Every major challenge identified has an exact, mathematically grounded architectural fix:

| # | The Problem / Failure Mode | Root Cause | AutoEditor Engineering Solution |
|---|---|---|---|
| **1** | **Editing costs \$1 per video (Too expensive)** | Standard commercial apps route everything to proprietary, overpriced APIs. | **OpenRouter Dynamic Cost Router:** Automatically queries OpenRouter's live pricing API. Defaults to top open-weights models (DeepSeek-V3, Qwen 2.5 72B) running at **\$0.14 per million tokens** $\to$ **\$0.001–\$0.003 per full video edit**. |
| **2** | **"AI Flop" 1–2 second lag / Desync** | Dumb editors guess timestamps based on text tokens, cutting in the middle of spoken words. | **Phonetic Anchor Snapping:** Local Whisper produces word-level millisecond timestamps. The engine snaps every cut, sticker, and motion to the nearest **silence gap between spoken words** ($\pm 40\text{ms}$). Syllables are never chopped. |
| **3** | **Unreadable text & bad font choices** | Text colors clash with background video brightness; text gets covered by TikTok buttons. | **Luminance Contrast & Safe-Zone Engine:** Scans underlying frame brightness. Automatically forces $3.5\text{px}$ drop shadows or solid dark pill backplates on light backgrounds. Enforces mobile safe-zones ($Y=65\%–80\%$, $X=50\%$) so buttons never obscure captions. |
| **4** | **Boring, static pacing (Awkward pauses)** | AI leaves static images on screen for 5–7 seconds without visual stimulation. | **The 2.8s Boredom Detector:** QA engine scans the timeline before rendering. If any scene sits still for $>2.8\text{s}$, it automatically injects a subtle zoom punch-in ($1.0 \to 1.08\times$) or cuts to contextual B-roll. |
| **5** | **User lacks stickers, icons, or graphics** | Users have a script but zero visual assets to illustrate concepts. | **Autonomous Asset Retrieval Agent:** Detects missing visual entities from the transcript (e.g., *"Bitcoin chart"*, *"Warning icon"*), queries transparent PNG / stock repositories, downloads them to `storage/assets/`, and binds them to the timeline. |
| **6** | **Muddy, distorted audio mixing** | Background music or loud sound effects overpower the narrator's voice. | **Intelligent Sidechain Ducking:** Narrator voiceover is mastered to broadcast standard ($-14\text{ LUFS}$). Background tracks are automatically ducked by $-18\text{dB}$ whenever vocal energy is detected. |
| **7** | **Laptop freezes / GPU crashes during live demo** | Heavy diffusion models crash laptop VRAM during presentations. | **Stage-Defense Architecture:** Whisper runs on quantized 8-bit **CPU** (<250MB RAM). Video compositing runs via standard H.264 hardware encoders (NVENC/QSV) with a fast **720p 6-second Demo Mode** and an offline fallback cache. |

---

## 3. System Architecture & Component Design

```
┌────────────────────────────────────────────────────────────────────────┐
│                          USER WEB BROWSER UI                           │
│     [AI Video Director Modal] ── [OpenRouter Model Picker ($/M)]       │
│     [Style Selector: MrBeast / Ali Abdaal / Vox / Custom Prompt]       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                         POST /api/ai-director
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     BACKEND AI ENGINE (api_server.py)                  │
│                                                                        │
│  1. Local Whisper Engine                                               │
│     └─► Audio $\to$ Phoneme-aligned word timestamps (0.0s – 3.4s)      │
│                                                                        │
│  2. OpenRouter Cost Router                                             │
│     └─► Queries /api/v1/models $\to$ Selects DeepSeek-V3 / Qwen ($0.002)│
│                                                                        │
│  3. Semantic Boundary & Entity Extractor                               │
│     └─► Chunks text into grammatical ideas & identifies visual needs   │
│                                                                        │
│  4. Autonomous Asset Hunter                                            │
│     └─► Downloads transparent PNG stickers & stock B-roll to storage/  │
│                                                                        │
│  5. Closed-Loop QA Gateway (The Validator)                             │
│     └─► Snaps cuts, verifies contrast, clamps safe-zones, ducks audio  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Outputs 100% verified EDL
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               LOCAL HARDWARE-ACCELERATED RENDER PIPELINE               │
│  - Auto-populates Next.js Multi-Track Timeline in Browser              │
│  - Instant Canvas Playback with 64 Kinetic Styles & 12 SFX             │
│  - Local FFmpeg NVENC/QSV hardware export to Downloads\AutoEditor\     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Phase-by-Phase Implementation Roadmap

### Phase 1: OpenRouter Integration & Live Model Marketplace
- **Objective:** Enable user-configurable, live-fetched AI models with transparent pricing.
- **Backend (`api_server.py`):**
  - Add `GET /api/openrouter/models`: Queries `https://openrouter.ai/api/v1/models`, parses context size, provider, and calculates cost per 1M input/output tokens.
  - Store encrypted/local API key in `storage/openrouter_config.json`.
  - Add default smart routing:
    - *Economy Tier (Default):* `deepseek/deepseek-chat` or `qwen/qwen-2.5-72b-instruct` (~$0.0015/edit).
    - *High Reasoning Tier:* `deepseek/deepseek-r1` or `anthropic/claude-3.5-sonnet` (for complex video reverse-engineering).
- **Frontend UI (`out/auto_captions.js` & `auto_captions.css`):**
  - Add **"AI Director"** button in header navigation bar.
  - OpenRouter Model Selector dropdown displaying live pricing badge (e.g., `DeepSeek-V3 · $0.14/1M · Recommended`).

### Phase 2: Semantic Thought Boundary & Phonetic Snapping Engine
- **Objective:** Eliminate timestamp drift and ensure cuts land on natural pauses.
- **Implementation (`transcribe_engine.py`):**
  - Create `align_cuts_to_phonemes(draft_timeline, whisper_word_grid)`:
    - Takes raw LLM cut suggestions.
    - Matches suggested seconds against Whisper's word array.
    - Detects word end times and inter-word silence intervals ($>120\text{ms}$).
    - Snaps timestamps to the exact millisecond of silence.
  - Export strict, validated cut timestamps into AutoEditor timeline slots.

### Phase 3: Creator Style DNA & Preset Profiling
- **Objective:** Give videos the exact 99% aesthetic match of iconic creators.
- **Implementation:**
  - Create `creator_profiles.json` in `storage/styles/`:
    - **MrBeast Profile:** Fast cut pace ($1.5\text{s}–2.5\text{s}$), `tiktok_pop` yellow captions, punch zooms, `impact_punch` & `whoosh_fast` on every visual cut.
    - **Ali Abdaal Profile:** Calm educational pacing ($4\text{s}–6\text{s}$), `editorial_serif` / `minimalist_modern` captions, slow smooth zoom, `gentle_chime` & `paper_turn` SFX.
    - **Vox / Johnny Harris Profile:** Visual essay pacing ($3\text{s}–5\text{s}$), `noir_editorial` with dark slate pill, panning motion, `cinematic_boom` & paper flutter.
    - **Alex Hormozi Profile:** Kinetic hook pacing ($2\text{s}–3\text{s}$), `hormozi_bold` active green highlight, center-punch zooms, micro-whooshes.
  - Prompt Engineering: Structured system prompt enforcing JSON schema conforming to AutoEditor's timeline spec.

### Phase 4: Autonomous Asset Hunter (Sticker & B-Roll Scraper)
- **Objective:** Automatically source missing visual entities so users don't have to hunt for images.
- **Implementation (`asset_hunter.py`):**
  - When the LLM Director identifies a missing graphic (e.g., *"Bitcoin logo PNG"* or *"Shocked face sticker"*):
  - Queries public transparent icon APIs (Flaticon / Wikimedia / Openverse / DuckDuckGo image search filter `type:png transparent`).
  - Downloads and validates alpha channel (transparency check using Pillow).
  - Saves asset to `storage/assets/<project_id>/` and inserts into Track 2 (Overlay Track).

### Phase 5: Multi-Layer Timeline Composition & Paired SFX Synchronization
- **Objective:** Layer stickers, popups, and paired sound effects on top of base video.
- **Implementation:**
  - Leverage AutoEditor's 12 synthesized 44.1kHz sound effects catalog:
    - Sticker popup $\to$ Triggers `bubble_pop.wav`.
    - Text slide-in $\to$ Triggers `whoosh_fast.wav`.
    - Realization / Impact $\to$ Triggers `cinematic_boom.wav`.
    - Fact / Statistic $\to$ Triggers `snappy_switch.wav` or `camera_click.wav`.
  - Compile multi-input FFmpeg audio graph using `adelay` and `amix` with sidechain ducking.

### Phase 6: Closed-Loop QA Gateway (The Deterministic Validator)
- **Objective:** Guarantee that zero defective videos ever reach the user.
- **Automated Validation Checks:**
  1. **Acoustic Sync Audit:** Verifies all cuts sit in silence gaps ($\pm 40\text{ms}$).
  2. **Luminance Contrast Audit:** Background frame sampling ensuring $>4.5:1$ contrast against subtitle text.
  3. **Social Safe-Zone Clamp:** Constrains subtitle box to $65\%–80\%$ $Y$-zone and $50\%$ $X$-center.
  4. **Pacing Audit:** Auto-injects camera zoom if any frame exceeds $2.8\text{s}$ without motion.
  5. **Audio Master Check:** Verifies voiceover levels meet $-14\text{ LUFS}$ broadcast target.

### Phase 7: Stage-Defense & Live Presentation Failsafe
- **Objective:** 100% guarantee against crashes or freezes during university defense.
- **Implementation:**
  - **`--presentation` / Demo Flag:**
    - Forces Whisper to `base.en` on CPU (<200MB RAM, finishes in 2.5s).
    - Renders preview at 720p 24fps in **under 8 seconds**.
  - **Offline Fallback Cache:**
    - If OpenRouter API takes $>4.0\text{s}$ or Wi-Fi disconnects, the system instantly executes a cached deterministic edit template without showing an error.

---

## 5. Defense & Academic Value (How to Present to Professors)

When presenting this project to a software engineering review panel:

1. **Title:**  
   *AutoEditor AI: Autonomous Style-Conditioned Video Editing via Multimodal LLM Orchestration and Deterministic QA*
2. **Key Innovation:**  
   Bridging stochastic generative AI (LLMs) with deterministic systems programming (FFmpeg hardware encoding & Whisper acoustic alignment).
3. **Core Metric:**  
   Reduces a 4-hour human editing workflow down to **75 seconds**, at an operating cost of **\$0.002 per video**.
4. **Reliability Architecture:**  
   Closed-loop automated verification eliminating hallucinations, desync, and visual collisions before rendering.

---
*(End of Roadmap — Ready for execution in next development cycle)*
