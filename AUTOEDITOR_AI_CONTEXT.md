# TryAIToday AutoEditor (v2) — AI Assistant Context & System Primer

> **Hidayat / Note for AI Chatbots:**  
> Jab bhi user aap se kisi video project, script writing, storyboard planning, ya asset generation ke bare mein baat kare, aap ko is document ke mutabiq un ki video plan karni hai taake wo direct **AutoEditor** mein import ki ja sake.

---

## 1. Project Overview (Software Kya Hai?)

**TryAIToday AutoEditor (v2)** ek local automated video editing aur synchronization desktop tool hai.  
Yeh software timestamp ke mutabiq named images/videos aur ek master voiceover audio ko aapas mein sync kar ke final MP4 video generate karta hai.

### Key Characteristics:
- **100% Local & Private:** Rendering user ke apne computer par CPU ya GPU (NVIDIA NVENC, Intel QSV, AMD AMF) aur bundled `ffmpeg.exe` ke zariye hoti hai. Koi bhi media internet par upload nahi hota.
- **Frontend / UI:** Local web interface hai jo `http://localhost:4000` par browser mein khulta hai (`out/` folder static Next.js application).
- **Backend:** `AutoEditor.exe` (Bun/Node engine) jo local HTTP server aur rendering pipeline chalata hai.

---

## 2. Core Workflow (Yeh Kaise Kaam Karta Hai?)

1. **Master Voiceover:** User 1 audio file (`.mp3` ya `.wav`) import karta hai jo puri video ki total duration set karti hai.
2. **Storyboard Visuals (Images & Videos):** User images (`.png`, `.jpg`, `.webp`) ya video clips (`.mp4`) drop karta hai jinka naam unke appear hone ke second/time ke mutabiq rakha gaya ho.
3. **Timeline Build:** Software automatically har image/video ko audio ke sath sahi waqt par timeline par place kar deta hai.
4. **Customization:**
   - **Transitions:** Cut (None), Crossfade (`fade`), Fade to black (`fadeblack`), Wipe left (`wipeleft`), Wipe right.
   - **Camera Motions:** Zoom In (`zoomin`), Zoom Out (`zoomout`), Pan.
   - **Video Clip Controls:** Trim start/end, speed control, audio volume mixing under narration, fit/crop modes.
   - **Captions / Subtitles:** SRT/VTT file ya timestamped text script jise video par burn kiya jata hai using `caption.ttf`.
   - **Aspect Ratio & FPS:** 16:9 (Landscape YouTube), 9:16 (Shorts/Reels/TikTok), 1:1 (Square), 24/30/60 FPS.
5. **Render & Export:** User "Render" par click karta hai, local GPU/CPU se video render hoti hai aur automatically `<User Downloads>/AutoEditor/` folder mein MP4 save ho jati hai.

---

## 3. Strict Filename & Timestamp Rules (AI ke liye Zaroori Rules)

AutoEditor visual files ko unke filename se timeline par map karta hai:

### Supported Naming Formats:
- **`M-SS.ext` (Recommended):**  
  - `0-00.png` → Video ke bilkul shuru (0:00) par aayegi.
  - `0-04.png` → 4th second (0:04) par cut-in karegi.
  - `0-15.jpg` → 15th second (0:15) par aayegi.
  - `1-02.mp4` → 1 minute 2 second (62nd second) par video clip play hogi.
- **`M_SS.ext`:** Jaise `0_00.png`, `0_08.png`, `1_20.mp4`.
- **`HH-MM-SS.ext`:** Jaise `0-01-30.png` (1 min 30 sec).
- **Direct Seconds:** Jaise `5.png` (5s), `45.jpg` (45s), `105.png` (1m 05s).

> **Rule:** Jab tak agli image/video ka timestamp nahi aata, pichli image screen par rehti hai. Is liye timestamps ke darmiyan gap scene ki duration tay karta hai.

---

## 4. AI Chatbot Output Format (Standard Template for Planning)

Jab user kahe: *"Mujhe is topic par video banani hai"* ya *"Video plan karo"*, AI ko hamesha niche diye gaye format mein plan dena chahiye:

### A. Voiceover Script (Audio Narration)
Pure narration script ko natural reading pace (approx 2.5 words per second) ke sath likhein.

### B. Storyboard Table (AutoEditor Ready)
| Scene # | Timestamp | Filename | Voiceover Line (Narration) | Visual Prompt (Midjourney / Flux / Leonardo) | Motion / Transition |
|---------|-----------|----------|----------------------------|----------------------------------------------|---------------------|
| 1 | 0:00 | `0-00.png` | "In a world driven by AI..." | Cinematic shot of a futuristic glowing AI brain, 8k | Zoom In / Crossfade |
| 2 | 0:05 | `0-05.png` | "Everything is moving faster than ever." | Cyberpunk city with flying cars in rain, hyperrealistic | Pan / Fade to black |
| 3 | 0:12 | `0-12.mp4` | "Here is how you can stay ahead." | Short video clip of a person working on multi-monitors | Trim to 6s, Volume 20% |

### C. Captions File (SRT / VTT format)
User ko ready-to-use SRT text format dein taake wo ise upload kar sakein.

---

## 5. Directory Structure Reference

```text
d:\AutoEditor\
├── AutoEditor.exe       # Main executable (Starts local Bun/Node server on port 4000)
├── ffmpeg.exe           # Bundled video & audio encoder (with NVENC/QSV/AMF support)
├── caption.ttf          # Font used for burning subtitle text into the video
├── READ ME FIRST.txt    # Basic startup instructions
├── out/                 # Static web application served at http://localhost:4000
│   ├── index.html
│   └── _next/           # Next.js frontend assets & UI scripts
└── AUTOEDITOR_AI_CONTEXT.md  # This AI prompt context document
```

---

## 6. How to Run & Requirements

- **OS:** Windows 10/11 (64-bit).
- **Run:** Double-click `AutoEditor.exe` → Black console window opens → Browser opens `http://localhost:4000`. Keep black window open.
- **Hardware:** Auto-detects NVIDIA/Intel/AMD GPU for fast encoding; falls back to CPU if no GPU is available.
- **Outputs:** Saved automatically to `Downloads\AutoEditor\`.
