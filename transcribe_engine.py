#!/usr/bin/env python3
"""
AutoEditor Transcription & Caption Engine
Provides:
1. Local offline audio transcription with word- and sentence-level timestamps (faster-whisper).
2. Clean TXT export (with timestamps & pure reading format).
3. Publication-quality PDF export (with metadata, timestamps, structured tables via reportlab / fpdf2).
4. CapCut-style ASS (Advanced SubStation Alpha) subtitle generator with 8 distinct styles:
   - Hormozi Kinetic (Bold, uppercase, bright yellow active highlight, heavy stroke)
   - Bouncy Social / Shorts (Scale pop, lime green highlight)
   - Neon Cyber Glow (Cyan/Magenta futuristic glow)
   - Boxed Pill / Tag (Orange pill badge behind active word/line)
   - Minimalist Modern (Clean lower-third translucent bar)
   - Classic Broadcast (Crisp white with black outline)
   - Karaoke Golden Fill (Gradual gold fill)
   - Comic Pop (Playful font with heavy comic outline and pink shadow)
"""

import os
import sys
import json
import math
import subprocess
import argparse
import html
import threading
from datetime import datetime

# Global in-memory cache for loaded Whisper models
_MODEL_CACHE = {}
_MODEL_LOCK = threading.Lock()

def is_model_cached() -> bool:
    """Return True if any model has been loaded into memory."""
    return len(_MODEL_CACHE) > 0

def get_model(model_size: str = "small", device: str = "cpu", compute_type: str = "int8"):
    """
    Tiered Whisper model loader with in-memory caching and thread safety.
    Attempts to load requested model (e.g. 'small'), falls back automatically
    to 'base' if unavailable or offline.
    """
    key = (model_size, device, compute_type)
    with _MODEL_LOCK:
        if key in _MODEL_CACHE:
            return _MODEL_CACHE[key]

        from faster_whisper import WhisperModel

        model = None
        if model_size not in ("base", "tiny"):
            try:
                print(f"Loading faster-whisper model '{model_size}' on {device} ({compute_type})...", file=sys.stderr)
                model = WhisperModel(model_size, device=device, compute_type=compute_type, local_files_only=True)
                print(f"Successfully loaded '{model_size}' from local cache.", file=sys.stderr)
            except Exception as e:
                print(f"Model '{model_size}' unavailable locally ({e}). Falling back to 'base'...", file=sys.stderr)
                model = None

        if model is None:
            fallback_size = "base" if model_size != "tiny" else "tiny"
            fallback_key = (fallback_size, device, compute_type)
            if fallback_key in _MODEL_CACHE:
                model = _MODEL_CACHE[fallback_key]
            else:
                print(f"Loading faster-whisper model '{fallback_size}' on {device} ({compute_type})...", file=sys.stderr)
                try:
                    model = WhisperModel(fallback_size, device=device, compute_type=compute_type, local_files_only=True)
                except Exception:
                    model = WhisperModel(fallback_size, device=device, compute_type=compute_type)
                _MODEL_CACHE[fallback_key] = model

        _MODEL_CACHE[key] = model
        return model

def format_second_timestamp(start: float, end: float) -> str:
    """
    Strict R3 second-based formatting: f'{start:.1f}s – {end:.1f}s' (e.g. '0.0s – 3.4s').
    Uses en-dash (\u2013).
    """
    s = max(0.0, float(start))
    e = max(s, float(end))
    return f"{s:.1f}s \u2013 {e:.1f}s"

def format_timestamp(seconds: float, include_ms: bool = False) -> str:
    """
    Strict R3 second-based formatting: f'{seconds:.1f}s' (e.g. '0.0s', '3.4s').
    """
    total_sec = max(0.0, float(seconds))
    return f"{total_sec:.1f}s"

def format_ass_time(seconds: float) -> str:
    total_centis = int(round(max(0.0, float(seconds)) * 100))
    centis = total_centis % 100
    total_secs = total_centis // 100
    secs = total_secs % 60
    minutes = (total_secs // 60) % 60
    hours = total_secs // 3600
    return f"{hours:d}:{minutes:02d}:{secs:02d}.{centis:02d}"

def transcribe_audio(audio_path: str, model_size: str = "small", language: str = None) -> dict:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    device = "cpu"
    compute_type = "int8"
    model = get_model(model_size=model_size, device=device, compute_type=compute_type)

    print(f"Transcribing '{audio_path}' with word-level timestamps (beam_size=5, speech_pad_ms=400)...", file=sys.stderr)
    segments_gen, info = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True,
        language=language,
        vad_filter=True,
        vad_parameters=dict(
            min_silence_duration_ms=400,
            speech_pad_ms=400
        )
    )

    segments_list = []
    full_text_parts = []
    total_words = 0

    for seg in segments_gen:
        seg_words = []
        if seg.words:
            for w in seg.words:
                total_words += 1
                seg_words.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3)
                })

        clean_text = seg.text.strip()
        full_text_parts.append(clean_text)
        ts_str = format_second_timestamp(seg.start, seg.end)
        segments_list.append({
            "id": seg.id,
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "timestamp": ts_str,
            "text": clean_text,
            "words": seg_words
        })

    duration = info.duration if hasattr(info, "duration") and info.duration else (segments_list[-1]["end"] if segments_list else 0.0)

    result = {
        "audio_file": os.path.basename(audio_path),
        "duration": round(duration, 3),
        "language": info.language if hasattr(info, "language") else "en",
        "language_probability": round(info.language_probability, 3) if hasattr(info, "language_probability") else 1.0,
        "total_words": total_words,
        "created_at": datetime.now().isoformat(),
        "text": " ".join(full_text_parts),
        "segments": segments_list
    }

    return result

def export_to_txt(transcript_data: dict, output_txt_path: str):
    lines = []
    filename = transcript_data.get("audio_file", "Audio")
    duration = transcript_data.get("duration", 0.0)
    dur_str = f"{duration:.1f}s"
    total_words = transcript_data.get("total_words", 0)

    lines.append("=================================================================")
    lines.append(f" AUDIO TRANSCRIPT: {filename}")
    lines.append(f" Total Duration: {dur_str} | Total Words: {total_words}")
    lines.append(f" Timeline: 0.0s --> {dur_str}")
    lines.append(f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=================================================================")
    lines.append("")
    lines.append("--- [ TIMESTAMPS & DIALOGUE ] ---")
    lines.append("")

    for seg in transcript_data.get("segments", []):
        ts = format_second_timestamp(seg["start"], seg["end"])
        text = seg.get("text", "").strip()
        lines.append(f"[{ts}] Speaker: {text}")
        lines.append("")

    lines.append("=================================================================")
    lines.append("--- [ FULL TEXT SCRIPT ] ---")
    lines.append("=================================================================")
    lines.append("")
    lines.append(transcript_data.get("text", "").strip())
    lines.append("")

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"TXT exported to: {output_txt_path}", file=sys.stderr)

def export_to_pdf(transcript_data: dict, output_pdf_path: str):
    try:
        _export_pdf_reportlab(transcript_data, output_pdf_path)
    except Exception as e:
        print(f"ReportLab notice: {e}, falling back to fpdf2...", file=sys.stderr)
        _export_pdf_fpdf2(transcript_data, output_pdf_path)

def _export_pdf_reportlab(transcript_data: dict, output_pdf_path: str):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Flowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas

    class RoundedBadge(Flowable):
        """Visual rounded pill badge with #EEF2FF fill, #1E40AF bold text, and soft border."""
        def __init__(self, text, width=95, height=20, bg_color='#EEF2FF', text_color='#1E40AF', border_color='#C7D2FE'):
            super().__init__()
            self.text = text
            self.width = width
            self.height = height
            self.bg_color = colors.HexColor(bg_color)
            self.text_color = colors.HexColor(text_color)
            self.border_color = colors.HexColor(border_color)

        def wrap(self, availWidth, availHeight):
            return self.width, self.height

        def draw(self):
            self.canv.saveState()
            self.canv.setFillColor(self.bg_color)
            self.canv.setStrokeColor(self.border_color)
            self.canv.setLineWidth(0.75)
            self.canv.roundRect(0, 0, self.width, self.height, 4, stroke=1, fill=1)
            self.canv.setFont("Helvetica-Bold", 8.5)
            self.canv.setFillColor(self.text_color)
            self.canv.drawCentredString(self.width / 2.0, (self.height / 2.0) - 3, self.text)
            self.canv.restoreState()

    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_number(num_pages)
                canvas.Canvas.showPage(self)
            canvas.Canvas.save(self)

        def draw_page_number(self, page_count):
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#71717A"))
            self.setStrokeColor(colors.HexColor("#E4E4E7"))
            self.setLineWidth(0.5)
            self.line(40, 35, 572, 35)
            self.drawString(40, 24, "TryAIToday AutoEditor — Audio Transcript")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(572, 24, page_text)
            self.restoreState()

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748B')
    )
    text_style = ParagraphStyle(
        'DialogueText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B')
    )

    elements = []
    elements.append(Paragraph("Audio Transcript & Timestamps", title_style))
    elements.append(Spacer(1, 4))
    
    filename = transcript_data.get("audio_file", "Audio File")
    dur_str = f"{transcript_data.get('duration', 0.0):.1f}s"
    words = transcript_data.get("total_words", 0)
    lang = str(transcript_data.get("language", "en")).upper()
    now_str = datetime.now().strftime("%B %d, %Y - %H:%M")
    
    escaped_filename = html.escape(str(filename))
    meta_text = f"Source: <b>{escaped_filename}</b> &nbsp;|&nbsp; Duration: <b>{dur_str}</b> &nbsp;|&nbsp; Words: <b>{words}</b> &nbsp;|&nbsp; Language: <b>{lang}</b> &nbsp;|&nbsp; Generated: {now_str}"
    elements.append(Paragraph(meta_text, subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=12))

    table_data = [
        [
            Paragraph("<b>Timestamp</b>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#475569'))),
            Paragraph("<b>Transcribed Dialogue</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#475569')))
        ]
    ]

    segments = transcript_data.get("segments", [])
    for seg in segments:
        ts_str = format_second_timestamp(seg["start"], seg["end"])
        ts_badge = RoundedBadge(ts_str)
        
        dialogue = seg.get("text", "").strip()
        escaped_dialogue = html.escape(dialogue)
        text_cell = Paragraph(escaped_dialogue, text_style)
        table_data.append([ts_badge, text_cell])

    t = Table(table_data, colWidths=[110, 422])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#E2E8F0')),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
    ]))

    elements.append(t)
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"PDF exported via ReportLab: {output_pdf_path}", file=sys.stderr)

def _export_pdf_fpdf2(transcript_data: dict, output_pdf_path: str):
    from fpdf import FPDF

    class PDF(FPDF):
        def footer(self):
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            footer_text = f"Page {self.page_no()}/{{nb}} - TryAIToday AutoEditor"
            self.cell(0, 10, footer_text.encode("latin-1", "replace").decode("latin-1"), align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)

    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Audio Transcript & Timestamps", new_x="LMARGIN", new_y="NEXT")

    filename = transcript_data.get("audio_file", "Audio File")
    dur_str = f"{transcript_data.get('duration', 0.0):.1f}s"
    words = transcript_data.get("total_words", 0)
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)
    meta_line = f"File: {filename}  |  Duration: {dur_str}  |  Total Words: {words}"
    pdf.cell(0, 6, meta_line.encode("latin-1", "replace").decode("latin-1"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_draw_color(203, 213, 225)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    for seg in transcript_data.get("segments", []):
        ts_str = format_second_timestamp(seg["start"], seg["end"])
        ts_clean = ts_str.replace('\u2013', '-').replace('\u2014', '-')
        text = seg.get("text", "").strip()
        text_clean = text.encode("latin-1", "replace").decode("latin-1")

        pdf.set_font("helvetica", "B", 8)
        pdf.set_text_color(30, 64, 175)
        pdf.cell(45, 6, f"[{ts_clean}]", align="L")

        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(30, 41, 59)
        pdf.multi_cell(0, 6, text_clean)
        pdf.ln(2)

    pdf.output(output_pdf_path)
    print(f"PDF exported via fpdf2: {output_pdf_path}", file=sys.stderr)

def burn_captions_to_video(video_path: str, ass_path: str, output_path: str, fonts_dir: str = None) -> bool:
    """
    Burns ASS subtitles into a video using ffmpeg with Windows path escaping.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_exe = os.path.join(base_dir, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
    if fonts_dir and os.path.exists(fonts_dir):
        escaped_fonts = fonts_dir.replace("\\", "/").replace(":", "\\:")
        vf_filter = f"ass='{escaped_ass}':fontsdir='{escaped_fonts}'"
    else:
        vf_filter = f"ass='{escaped_ass}'"

    cmd = [
        ffmpeg_exe, "-y",
        "-i", video_path,
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-c:a", "copy",
        output_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode == 0 and os.path.exists(output_path)

def remove_vocal_from_video_or_audio(input_path: str, output_path: str, vocal_volume: float = 0.0) -> bool:
    """
    Suppresses or eliminates human vocal frequencies from video/audio
    while preserving high-frequency clicks, transients, foley, and background sound effects.
    vocal_volume: 0.0 = complete voice removal (max attenuation)
                  0.5 = 50% voice volume
                  1.0 = full voice (original)
    Supports both audio output (.wav, .mp3, .m4a) and video output (.mp4, .mov, .mkv, etc.).
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_exe = os.path.join(base_dir, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    v_vol = max(0.0, min(1.0, float(vocal_volume)))
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    ext = os.path.splitext(output_path)[1].lower()
    is_video_out = ext in [".mp4", ".mov", ".mkv", ".webm", ".avi"]

    if v_vol >= 0.98:
        # Pass through without vocal reduction
        if is_video_out:
            cmd = [ffmpeg_exe, "-y", "-i", input_path, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", output_path]
        elif ext == ".wav":
            cmd = [ffmpeg_exe, "-y", "-i", input_path, "-vn", "-c:a", "pcm_s16le", output_path]
        elif ext == ".mp3":
            cmd = [ffmpeg_exe, "-y", "-i", input_path, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", output_path]
        else:
            cmd = [ffmpeg_exe, "-y", "-i", input_path, "-vn", "-c:a", "aac", "-b:a", "192k", output_path]
    else:
        # Speech fundamentals (120Hz-400Hz) and formants (800Hz-3.5kHz) notch attenuation
        # Preserves crisp click transients (>4kHz) and sub frequencies
        att = int(round(-32.0 * (1.0 - v_vol)))
        af_filter = (
            f"equalizer=f=300:t=q:w=1.2:g={int(att*0.8)},"
            f"equalizer=f=1050:t=q:w=1.6:g={att},"
            f"equalizer=f=2200:t=q:w=1.6:g={int(att*0.9)},"
            f"equalizer=f=3300:t=q:w=1.4:g={int(att*0.7)}"
        )
        if is_video_out:
            cmd = [
                ffmpeg_exe, "-y",
                "-i", input_path,
                "-c:v", "copy",
                "-af", af_filter,
                "-c:a", "aac", "-b:a", "192k",
                output_path
            ]
        elif ext == ".wav":
            cmd = [
                ffmpeg_exe, "-y",
                "-i", input_path,
                "-vn",
                "-af", af_filter,
                "-c:a", "pcm_s16le",
                output_path
            ]
        elif ext == ".mp3":
            cmd = [
                ffmpeg_exe, "-y",
                "-i", input_path,
                "-vn",
                "-af", af_filter,
                "-c:a", "libmp3lame", "-b:a", "192k",
                output_path
            ]
        else:
            cmd = [
                ffmpeg_exe, "-y",
                "-i", input_path,
                "-vn",
                "-af", af_filter,
                "-c:a", "aac", "-b:a", "192k",
                output_path
            ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode == 0 and os.path.exists(output_path)

def mix_audio_with_sfx(main_audio: str, sfx_events: list, output_audio: str, sfx_volume: float = 0.5, voice_volume: float = 1.0) -> bool:
    """
    Mixes master voiceover audio with transition sound effects at specified timestamps.
    sfx_events: list of dicts: [{"file": path_to_wav, "timestamp": sec}]
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_exe = os.path.join(base_dir, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    os.makedirs(os.path.dirname(os.path.abspath(output_audio)), exist_ok=True)
    ext = os.path.splitext(output_audio)[1].lower()
    if ext == ".wav":
        codec_args = ["-c:a", "pcm_s16le"]
    elif ext == ".mp3":
        codec_args = ["-c:a", "libmp3lame", "-b:a", "192k"]
    else:
        codec_args = ["-c:a", "aac", "-b:a", "192k"]

    if not sfx_events:
        # Just adjust voice volume if needed
        cmd = [
            ffmpeg_exe, "-y", "-i", main_audio,
            "-af", f"volume={voice_volume:.3f}",
            *codec_args, output_audio
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0 and os.path.exists(output_audio)

    # Build multi-input filter_complex
    cmd = [ffmpeg_exe, "-y", "-i", main_audio]
    filter_parts = [f"[0:a]volume={voice_volume:.3f}[a0]"]
    mix_inputs = ["[a0]"]

    for idx, evt in enumerate(sfx_events, start=1):
        sfx_path = evt.get("file")
        ts_ms = int(round(max(0.0, float(evt.get("timestamp", 0.0))) * 1000.0))
        if sfx_path and os.path.exists(sfx_path):
            cmd.extend(["-i", sfx_path])
            filter_parts.append(f"[{idx}:a]volume={sfx_volume:.3f},adelay={ts_ms}|{ts_ms}[sfx{idx}]")
            mix_inputs.append(f"[sfx{idx}]")

    num_inputs = len(mix_inputs)
    if num_inputs == 1:
        cmd = [
            ffmpeg_exe, "-y", "-i", main_audio,
            "-af", f"volume={voice_volume:.3f}",
            *codec_args, output_audio
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0 and os.path.exists(output_audio)

    filter_parts.append(f"{''.join(mix_inputs)}amix=inputs={num_inputs}:normalize=0:dropout_transition=0[aout]")
    filter_str = ";".join(filter_parts)

    cmd.extend([
        "-filter_complex", filter_str,
        "-map", "[aout]",
        *codec_args,
        output_audio
    ])
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode == 0 and os.path.exists(output_audio)


CATEGORIES = {   'viral_shorts': 'Viral Shorts & TikTok',
    'hormozi': 'Hormozi & Viral Retention',
    'neon_glow': 'Neon Cyber Glow',
    'cinematic': 'Cinematic & Documentary',
    'boxed_pill': 'Boxed & Pill Badges',
    'headline': 'Bold Punchy & Headline',
    'comic_pop': 'Retro & Comic Pop',
    'broadcast': 'Clean Corporate & Broadcast'}

CAPTION_STYLES = {   'bouncy_shorts': {   'id': 'bouncy_shorts',
                         'name': 'Bouncy Social',
                         'category': 'viral_shorts',
                         'category_label': 'Viral Shorts',
                         'description': 'High engagement TikTok/Shorts style '
                                        'with active word scale pop and '
                                        'vibrant lime green highlight.',
                         'font': 'Arial Black',
                         'fallback_font': 'Arial',
                         'fontsize': 48,
                         'primary_color': '&H00FFFFFF',
                         'active_color': '&H0000FF00',
                         'outline_color': '&H00000000',
                         'back_color': '&H00000000',
                         'bold': 1,
                         'outline': 4.0,
                         'shadow': 2.0,
                         'alignment': 2,
                         'margin_v': 80,
                         'uppercase': True,
                         'animation_type': 'bounce_pop',
                         'preview_class': 'preview-bouncy',
                         'preview_html': 'BOUNCY <span '
                                         'class="act">SCALE</span> POP',
                         'css': {   'fontFamily': 'Arial Black, sans-serif',
                                    'color': '#ffffff',
                                    'activeColor': '#22c55e',
                                    'textTransform': 'uppercase',
                                    'textShadow': '-2px -2px 0 #000, 2px -2px '
                                                  '0 #000, -2px 2px 0 #000, '
                                                  '2px 2px 0 #000'}},
    'tiktok_pop': {   'id': 'tiktok_pop',
                      'name': 'TikTok Speed Pop',
                      'category': 'viral_shorts',
                      'category_label': 'Viral Shorts',
                      'description': 'Electric yellow scale pop with dark '
                                     'stroke for fast-paced viral videos.',
                      'font': 'Arial Black',
                      'fallback_font': 'Impact',
                      'fontsize': 50,
                      'primary_color': '&H00FFFFFF',
                      'active_color': '&H0000FFFF',
                      'outline_color': '&H00000000',
                      'back_color': '&H00000000',
                      'bold': 1,
                      'outline': 4.5,
                      'shadow': 2.0,
                      'alignment': 2,
                      'margin_v': 78,
                      'uppercase': True,
                      'animation_type': 'bounce_pop',
                      'preview_class': 'preview-tiktok-pop',
                      'preview_html': 'VIRAL <span class="act">SPEED</span> '
                                      'HOOK',
                      'css': {   'fontFamily': 'Arial Black, sans-serif',
                                 'color': '#ffffff',
                                 'activeColor': '#facc15',
                                 'textTransform': 'uppercase',
                                 'textShadow': '2px 2px 0 #000, -2px -2px 0 '
                                               '#000'}},
    'viral_green_hook': {   'id': 'viral_green_hook',
                            'name': 'Viral Green Hook',
                            'category': 'viral_shorts',
                            'category_label': 'Viral Shorts',
                            'description': 'High-contrast neon emerald '
                                           'highlight designed for maximum '
                                           'retention on first 3 seconds.',
                            'font': 'Impact',
                            'fallback_font': 'Arial Black',
                            'fontsize': 52,
                            'primary_color': '&H00FFFFFF',
                            'active_color': '&H0014FF39',
                            'outline_color': '&H00000000',
                            'back_color': '&H80000000',
                            'bold': 1,
                            'outline': 4.5,
                            'shadow': 2.5,
                            'alignment': 2,
                            'margin_v': 75,
                            'uppercase': True,
                            'animation_type': 'karaoke_highlight',
                            'preview_class': 'preview-viral-green',
                            'preview_html': 'STOP <span '
                                            'class="act">SCROLLING</span> NOW',
                            'css': {   'fontFamily': 'Impact, sans-serif',
                                       'color': '#ffffff',
                                       'activeColor': '#10b981',
                                       'textTransform': 'uppercase',
                                       'textShadow': '2px 2px 0 #000, -2px '
                                                     '-2px 0 #000'}},
    'snap_yellow': {   'id': 'snap_yellow',
                       'name': 'Snap Yellow Pulse',
                       'category': 'viral_shorts',
                       'category_label': 'Viral Shorts',
                       'description': 'Bright sunshine yellow with snap pulse '
                                      'animation for punchy storytelling.',
                       'font': 'Trebuchet MS',
                       'fallback_font': 'Arial Black',
                       'fontsize': 48,
                       'primary_color': '&H00FFFFFF',
                       'active_color': '&H0000E1FF',
                       'outline_color': '&H00000000',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 4.0,
                       'shadow': 2.0,
                       'alignment': 2,
                       'margin_v': 76,
                       'uppercase': True,
                       'animation_type': 'scale_pulse',
                       'preview_class': 'preview-snap-yellow',
                       'preview_html': 'SNAP <span class="act">PULSE</span> '
                                       'ACTION',
                       'css': {   'fontFamily': 'Trebuchet MS, sans-serif',
                                  'fontWeight': 'bold',
                                  'color': '#ffffff',
                                  'activeColor': '#f59e0b',
                                  'textTransform': 'uppercase',
                                  'textShadow': '2px 2px 0 #000'}},
    'speed_demon': {   'id': 'speed_demon',
                       'name': 'Speed Demon Coral',
                       'category': 'viral_shorts',
                       'category_label': 'Viral Shorts',
                       'description': 'Fiery coral orange pop for '
                                      'high-velocity talking head reels.',
                       'font': 'Arial Black',
                       'fallback_font': 'Impact',
                       'fontsize': 50,
                       'primary_color': '&H00F0F0F0',
                       'active_color': '&H003366FF',
                       'outline_color': '&H00000000',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 4.0,
                       'shadow': 2.0,
                       'alignment': 2,
                       'margin_v': 80,
                       'uppercase': True,
                       'animation_type': 'bounce_pop',
                       'preview_class': 'preview-speed-demon',
                       'preview_html': 'ULTRA <span class="act">FAST</span> '
                                       'PACED',
                       'css': {   'fontFamily': 'Arial Black, sans-serif',
                                  'color': '#f8fafc',
                                  'activeColor': '#ff6b4a',
                                  'textTransform': 'uppercase',
                                  'textShadow': '2px 2px 0 #000'}},
    'reel_zoomer': {   'id': 'reel_zoomer',
                       'name': 'Reel Zoomer Cyan',
                       'category': 'viral_shorts',
                       'category_label': 'Viral Shorts',
                       'description': 'Dynamic cyan active pop with subtle '
                                      'scale zoom for Reels and TikTok.',
                       'font': 'Impact',
                       'fallback_font': 'Arial Black',
                       'fontsize': 50,
                       'primary_color': '&H00FFFFFF',
                       'active_color': '&H00FFFF00',
                       'outline_color': '&H00000000',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 4.0,
                       'shadow': 2.0,
                       'alignment': 2,
                       'margin_v': 78,
                       'uppercase': True,
                       'animation_type': 'bounce_pop',
                       'preview_class': 'preview-reel-zoomer',
                       'preview_html': 'SMASH <span class="act">THAT</span> '
                                       'FOLLOW',
                       'css': {   'fontFamily': 'Impact, sans-serif',
                                  'color': '#ffffff',
                                  'activeColor': '#06b6d4',
                                  'textTransform': 'uppercase',
                                  'textShadow': '2px 2px 0 #000'}},
    'trendsetter_red': {   'id': 'trendsetter_red',
                           'name': 'Trendsetter Crimson',
                           'category': 'viral_shorts',
                           'category_label': 'Viral Shorts',
                           'description': 'Deep crimson pop highlight that '
                                          'commands immediate viewer focus.',
                           'font': 'Arial Black',
                           'fallback_font': 'Arial',
                           'fontsize': 48,
                           'primary_color': '&H00FFFFFF',
                           'active_color': '&H002A2AFF',
                           'outline_color': '&H00000000',
                           'back_color': '&H00000000',
                           'bold': 1,
                           'outline': 4.2,
                           'shadow': 2.2,
                           'alignment': 2,
                           'margin_v': 80,
                           'uppercase': True,
                           'animation_type': 'karaoke_highlight',
                           'preview_class': 'preview-trend-red',
                           'preview_html': 'SECRET <span '
                                           'class="act">HACK</span> REVEALED',
                           'css': {   'fontFamily': 'Arial Black, sans-serif',
                                      'color': '#ffffff',
                                      'activeColor': '#ef4444',
                                      'textTransform': 'uppercase',
                                      'textShadow': '2px 2px 0 #000'}},
    'karaoke_gold': {   'id': 'karaoke_gold',
                        'name': 'Karaoke Golden Fill',
                        'category': 'viral_shorts',
                        'category_label': 'Viral Shorts',
                        'description': 'Dim text fills with brilliant gold '
                                       'word-by-word as spoken.',
                        'font': 'Arial Black',
                        'fallback_font': 'Arial',
                        'fontsize': 46,
                        'primary_color': '&H88CCCCCC',
                        'active_color': '&H0000C8FF',
                        'outline_color': '&H00000000',
                        'back_color': '&H00000000',
                        'bold': 1,
                        'outline': 3.5,
                        'shadow': 2.0,
                        'alignment': 2,
                        'margin_v': 75,
                        'uppercase': False,
                        'animation_type': 'karaoke_highlight',
                        'preview_class': 'preview-gold',
                        'preview_html': 'Vibrant <span '
                                        'class="act">golden</span> speech',
                        'css': {   'fontFamily': 'Arial Black, sans-serif',
                                   'color': '#94a3b8',
                                   'activeColor': '#f59e0b',
                                   'textShadow': '2px 2px 0 #000'}},
    'hormozi_bold': {   'id': 'hormozi_bold',
                        'name': 'Hormozi Kinetic',
                        'category': 'hormozi',
                        'category_label': 'Hormozi',
                        'description': 'Bold all-caps with bright yellow '
                                       'active-word highlight and heavy black '
                                       'stroke. Viral shorts/reels style.',
                        'font': 'Impact',
                        'fallback_font': 'Arial Black',
                        'fontsize': 52,
                        'primary_color': '&H00FFFFFF',
                        'active_color': '&H0000FFFF',
                        'outline_color': '&H00000000',
                        'back_color': '&H80000000',
                        'bold': 1,
                        'outline': 4.5,
                        'shadow': 2.5,
                        'alignment': 2,
                        'margin_v': 75,
                        'uppercase': True,
                        'animation_type': 'karaoke_highlight',
                        'preview_class': 'preview-hormozi',
                        'preview_html': 'READY TO <span '
                                        'class="act">DOMINATE</span> SOCIAL',
                        'css': {   'fontFamily': 'Impact, sans-serif',
                                   'color': '#ffffff',
                                   'activeColor': '#ffe600',
                                   'textTransform': 'uppercase',
                                   'textShadow': '-2px -2px 0 #000, 2px -2px 0 '
                                                 '#000, -2px 2px 0 #000, 2px '
                                                 '2px 0 #000'}},
    'hormozi_lime': {   'id': 'hormozi_lime',
                        'name': 'Hormozi Lime Retention',
                        'category': 'hormozi',
                        'category_label': 'Hormozi',
                        'description': 'Signature Hormozi heavy typography '
                                       'with electric lime active highlight.',
                        'font': 'Impact',
                        'fallback_font': 'Arial Black',
                        'fontsize': 52,
                        'primary_color': '&H00FFFFFF',
                        'active_color': '&H0000FF00',
                        'outline_color': '&H00000000',
                        'back_color': '&H80000000',
                        'bold': 1,
                        'outline': 4.5,
                        'shadow': 2.5,
                        'alignment': 2,
                        'margin_v': 75,
                        'uppercase': True,
                        'animation_type': 'karaoke_highlight',
                        'preview_class': 'preview-hormozi-lime',
                        'preview_html': 'SCALE TO <span class="act">ONE '
                                        'MILLION</span> FAST',
                        'css': {   'fontFamily': 'Impact, sans-serif',
                                   'color': '#ffffff',
                                   'activeColor': '#22c55e',
                                   'textTransform': 'uppercase',
                                   'textShadow': '-2px -2px 0 #000, 2px -2px 0 '
                                                 '#000, -2px 2px 0 #000, 2px '
                                                 '2px 0 #000'}},
    'hormozi_gold': {   'id': 'hormozi_gold',
                        'name': 'Gold Beast Retention',
                        'category': 'hormozi',
                        'category_label': 'Hormozi',
                        'description': 'Massive Impact letters with luxury '
                                       'gold highlight for business & wealth '
                                       'content.',
                        'font': 'Impact',
                        'fallback_font': 'Arial Black',
                        'fontsize': 52,
                        'primary_color': '&H00FFFFFF',
                        'active_color': '&H0000D7FF',
                        'outline_color': '&H00000000',
                        'back_color': '&H80000000',
                        'bold': 1,
                        'outline': 4.8,
                        'shadow': 2.8,
                        'alignment': 2,
                        'margin_v': 75,
                        'uppercase': True,
                        'animation_type': 'karaoke_highlight',
                        'preview_class': 'preview-hormozi-gold',
                        'preview_html': 'THE 100M <span '
                                        'class="act">OFFER</span> PLAYBOOK',
                        'css': {   'fontFamily': 'Impact, sans-serif',
                                   'color': '#ffffff',
                                   'activeColor': '#f59e0b',
                                   'textTransform': 'uppercase',
                                   'textShadow': '-2px -2px 0 #000, 2px -2px 0 '
                                                 '#000, -2px 2px 0 #000, 2px '
                                                 '2px 0 #000'}},
    'hormozi_cyan': {   'id': 'hormozi_cyan',
                        'name': 'Cyan Striker Retention',
                        'category': 'hormozi',
                        'category_label': 'Hormozi',
                        'description': 'Vivid cyan active word on dark '
                                       'background with heavy black outline.',
                        'font': 'Impact',
                        'fallback_font': 'Arial Black',
                        'fontsize': 52,
                        'primary_color': '&H00FFFFFF',
                        'active_color': '&H00FFFF00',
                        'outline_color': '&H00000000',
                        'back_color': '&H80000000',
                        'bold': 1,
                        'outline': 4.5,
                        'shadow': 2.5,
                        'alignment': 2,
                        'margin_v': 75,
                        'uppercase': True,
                        'animation_type': 'karaoke_highlight',
                        'preview_class': 'preview-hormozi-cyan',
                        'preview_html': 'NEVER <span class="act">GIVE '
                                        'UP</span> ON IT',
                        'css': {   'fontFamily': 'Impact, sans-serif',
                                   'color': '#ffffff',
                                   'activeColor': '#06b6d4',
                                   'textTransform': 'uppercase',
                                   'textShadow': '-2px -2px 0 #000, 2px -2px 0 '
                                                 '#000, -2px 2px 0 #000, 2px '
                                                 '2px 0 #000'}},
    'hormozi_red': {   'id': 'hormozi_red',
                       'name': 'Millionaire Crimson',
                       'category': 'hormozi',
                       'category_label': 'Hormozi',
                       'description': 'Aggressive red active word pop for '
                                      'hard-hitting business statements.',
                       'font': 'Impact',
                       'fallback_font': 'Arial Black',
                       'fontsize': 52,
                       'primary_color': '&H00FFFFFF',
                       'active_color': '&H000000FF',
                       'outline_color': '&H00000000',
                       'back_color': '&H80000000',
                       'bold': 1,
                       'outline': 4.5,
                       'shadow': 2.5,
                       'alignment': 2,
                       'margin_v': 75,
                       'uppercase': True,
                       'animation_type': 'karaoke_highlight',
                       'preview_class': 'preview-hormozi-red',
                       'preview_html': 'THIS IS <span class="act">THE '
                                       'BIGGEST</span> MISTAKE',
                       'css': {   'fontFamily': 'Impact, sans-serif',
                                  'color': '#ffffff',
                                  'activeColor': '#ef4444',
                                  'textTransform': 'uppercase',
                                  'textShadow': '-2px -2px 0 #000, 2px -2px 0 '
                                                '#000, -2px 2px 0 #000, 2px '
                                                '2px 0 #000'}},
    'hormozi_white_black': {   'id': 'hormozi_white_black',
                               'name': 'Monochrome Heavy Punch',
                               'category': 'hormozi',
                               'category_label': 'Hormozi',
                               'description': 'Pure high-contrast black and '
                                              'white typography with extreme '
                                              'outline weight.',
                               'font': 'Impact',
                               'fallback_font': 'Arial Black',
                               'fontsize': 54,
                               'primary_color': '&H00FFFFFF',
                               'active_color': '&H00FFFFFF',
                               'outline_color': '&H00000000',
                               'back_color': '&H80000000',
                               'bold': 1,
                               'outline': 5.0,
                               'shadow': 3.0,
                               'alignment': 2,
                               'margin_v': 75,
                               'uppercase': True,
                               'animation_type': 'bounce_pop',
                               'preview_class': 'preview-monochrome-punch',
                               'preview_html': 'TOTAL <span '
                                               'class="act">CLARITY</span> '
                                               'WINS',
                               'css': {   'fontFamily': 'Impact, sans-serif',
                                          'color': '#ffffff',
                                          'activeColor': '#ffffff',
                                          'textTransform': 'uppercase',
                                          'textShadow': '-3px -3px 0 #000, 3px '
                                                        '-3px 0 #000, -3px 3px '
                                                        '0 #000, 3px 3px 0 '
                                                        '#000'}},
    'hormozi_orange': {   'id': 'hormozi_orange',
                          'name': 'Hyper Growth Orange',
                          'category': 'hormozi',
                          'category_label': 'Hormozi',
                          'description': 'Warm flame orange highlight for '
                                         'energy and high conversion.',
                          'font': 'Impact',
                          'fallback_font': 'Arial Black',
                          'fontsize': 52,
                          'primary_color': '&H00FFFFFF',
                          'active_color': '&H0000A5FF',
                          'outline_color': '&H00000000',
                          'back_color': '&H80000000',
                          'bold': 1,
                          'outline': 4.5,
                          'shadow': 2.5,
                          'alignment': 2,
                          'margin_v': 75,
                          'uppercase': True,
                          'animation_type': 'karaoke_highlight',
                          'preview_class': 'preview-hormozi-orange',
                          'preview_html': 'MAKE YOUR <span '
                                          'class="act">BUSINESS</span> SCALE',
                          'css': {   'fontFamily': 'Impact, sans-serif',
                                     'color': '#ffffff',
                                     'activeColor': '#f97316',
                                     'textTransform': 'uppercase',
                                     'textShadow': '-2px -2px 0 #000, 2px -2px '
                                                   '0 #000, -2px 2px 0 #000, '
                                                   '2px 2px 0 #000'}},
    'hormozi_electric': {   'id': 'hormozi_electric',
                            'name': 'Electric Titan Blue',
                            'category': 'hormozi',
                            'category_label': 'Hormozi',
                            'description': 'Bold sapphire blue active '
                                           'highlight with maximum presence.',
                            'font': 'Impact',
                            'fallback_font': 'Arial Black',
                            'fontsize': 52,
                            'primary_color': '&H00FFFFFF',
                            'active_color': '&H00FF9600',
                            'outline_color': '&H00000000',
                            'back_color': '&H80000000',
                            'bold': 1,
                            'outline': 4.5,
                            'shadow': 2.5,
                            'alignment': 2,
                            'margin_v': 75,
                            'uppercase': True,
                            'animation_type': 'bounce_pop',
                            'preview_class': 'preview-hormozi-electric',
                            'preview_html': 'BUILD AN <span '
                                            'class="act">EMPIRE</span> TODAY',
                            'css': {   'fontFamily': 'Impact, sans-serif',
                                       'color': '#ffffff',
                                       'activeColor': '#3b82f6',
                                       'textTransform': 'uppercase',
                                       'textShadow': '-2px -2px 0 #000, 2px '
                                                     '-2px 0 #000, -2px 2px 0 '
                                                     '#000, 2px 2px 0 #000'}},
    'neon_glow': {   'id': 'neon_glow',
                     'name': 'Neon Cyber Glow',
                     'category': 'neon_glow',
                     'category_label': 'Neon Cyber',
                     'description': 'Futuristic cyan & magenta glowing caption '
                                    'text. Ideal for tech, dark backgrounds, '
                                    'and gaming.',
                     'font': 'Trebuchet MS',
                     'fallback_font': 'Arial',
                     'fontsize': 46,
                     'primary_color': '&H00FFFFFF',
                     'active_color': '&H00FFFF00',
                     'outline_color': '&H00FF00FF',
                     'back_color': '&H00000000',
                     'bold': 1,
                     'outline': 3.0,
                     'shadow': 4.0,
                     'alignment': 2,
                     'margin_v': 70,
                     'uppercase': False,
                     'animation_type': 'glow_highlight',
                     'preview_class': 'preview-neon',
                     'preview_html': 'FUTURE <span class="act">CYBER</span> '
                                     'GLOW',
                     'css': {   'fontFamily': 'Trebuchet MS, sans-serif',
                                'fontWeight': 'bold',
                                'color': '#ffffff',
                                'activeColor': '#22d3ee',
                                'textShadow': '0 0 8px #06b6d4, 0 0 14px '
                                              '#a855f7'}},
    'neon_purple': {   'id': 'neon_purple',
                       'name': 'Electric Purple Glow',
                       'category': 'neon_glow',
                       'category_label': 'Neon Cyber',
                       'description': 'Deep electric violet glow for gaming, '
                                      'music, and nocturnal aesthetics.',
                       'font': 'Arial Black',
                       'fallback_font': 'Arial',
                       'fontsize': 46,
                       'primary_color': '&H00FFFFFF',
                       'active_color': '&H00FF32B4',
                       'outline_color': '&H00330033',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 3.2,
                       'shadow': 4.5,
                       'alignment': 2,
                       'margin_v': 72,
                       'uppercase': True,
                       'animation_type': 'glow_highlight',
                       'preview_class': 'preview-neon-purple',
                       'preview_html': 'DEEP <span class="act">VIOLET</span> '
                                       'PULSE',
                       'css': {   'fontFamily': 'Arial Black, sans-serif',
                                  'color': '#ffffff',
                                  'activeColor': '#c084fc',
                                  'textTransform': 'uppercase',
                                  'textShadow': '0 0 10px #a855f7, 0 0 20px '
                                                '#7e22ce'}},
    'neon_pink': {   'id': 'neon_pink',
                     'name': 'Hot Magenta Neon',
                     'category': 'neon_glow',
                     'category_label': 'Neon Cyber',
                     'description': 'High-intensity hot pink neon with soft '
                                    'magenta radiance.',
                     'font': 'Trebuchet MS',
                     'fallback_font': 'Arial',
                     'fontsize': 46,
                     'primary_color': '&H00FFFFFF',
                     'active_color': '&H00CC00FF',
                     'outline_color': '&H00000000',
                     'back_color': '&H00000000',
                     'bold': 1,
                     'outline': 3.0,
                     'shadow': 4.0,
                     'alignment': 2,
                     'margin_v': 70,
                     'uppercase': True,
                     'animation_type': 'glow_highlight',
                     'preview_class': 'preview-neon-pink',
                     'preview_html': 'HOT <span class="act">MAGENTA</span> '
                                     'NIGHTS',
                     'css': {   'fontFamily': 'Trebuchet MS, sans-serif',
                                'fontWeight': 'bold',
                                'color': '#ffffff',
                                'activeColor': '#f43f5e',
                                'textTransform': 'uppercase',
                                'textShadow': '0 0 10px #f43f5e, 0 0 20px '
                                              '#e11d48'}},
    'neon_acid': {   'id': 'neon_acid',
                     'name': 'Acid Matrix Green',
                     'category': 'neon_glow',
                     'category_label': 'Neon Cyber',
                     'description': 'Terminal matrix phosphor green glow for '
                                    'tech and coding tutorials.',
                     'font': 'Courier New',
                     'fallback_font': 'Arial',
                     'fontsize': 44,
                     'primary_color': '&H0000FF00',
                     'active_color': '&H00FFFFFF',
                     'outline_color': '&H00003300',
                     'back_color': '&H00000000',
                     'bold': 1,
                     'outline': 2.5,
                     'shadow': 4.0,
                     'alignment': 2,
                     'margin_v': 70,
                     'uppercase': False,
                     'animation_type': 'glow_highlight',
                     'preview_class': 'preview-neon-acid',
                     'preview_html': '$ <span '
                                     'class="act">ACCESS</span>_GRANTED',
                     'css': {   'fontFamily': 'Courier New, monospace',
                                'fontWeight': 'bold',
                                'color': '#22c55e',
                                'activeColor': '#ffffff',
                                'textShadow': '0 0 8px #22c55e, 0 0 16px '
                                              '#15803d'}},
    'neon_ice_blue': {   'id': 'neon_ice_blue',
                         'name': 'Ice Laser Blue',
                         'category': 'neon_glow',
                         'category_label': 'Neon Cyber',
                         'description': 'Crisp arctic ice laser glow for '
                                        'high-tech and sleek video aesthetics.',
                         'font': 'Segoe UI',
                         'fallback_font': 'Arial',
                         'fontsize': 45,
                         'primary_color': '&H00FFFFFF',
                         'active_color': '&H00FFFF00',
                         'outline_color': '&H00663300',
                         'back_color': '&H00000000',
                         'bold': 1,
                         'outline': 2.8,
                         'shadow': 4.0,
                         'alignment': 2,
                         'margin_v': 72,
                         'uppercase': False,
                         'animation_type': 'glow_highlight',
                         'preview_class': 'preview-ice-blue',
                         'preview_html': 'Glacial <span class="act">ice '
                                         'laser</span> precision',
                         'css': {   'fontFamily': 'Segoe UI, sans-serif',
                                    'fontWeight': 'bold',
                                    'color': '#ffffff',
                                    'activeColor': '#38bdf8',
                                    'textShadow': '0 0 10px #38bdf8, 0 0 20px '
                                                  '#0284c7'}},
    'neon_tokyo': {   'id': 'neon_tokyo',
                      'name': 'Tokyo Sunset Violet',
                      'category': 'neon_glow',
                      'category_label': 'Neon Cyber',
                      'description': 'Shinjuku neon nightlife aesthetic with '
                                     'dual violet and warm amber glow.',
                      'font': 'Trebuchet MS',
                      'fallback_font': 'Arial',
                      'fontsize': 46,
                      'primary_color': '&H00FFFFFF',
                      'active_color': '&H0000D7FF',
                      'outline_color': '&H00800080',
                      'back_color': '&H00000000',
                      'bold': 1,
                      'outline': 3.2,
                      'shadow': 4.0,
                      'alignment': 2,
                      'margin_v': 70,
                      'uppercase': True,
                      'animation_type': 'glow_highlight',
                      'preview_class': 'preview-neon-tokyo',
                      'preview_html': 'TOKYO <span class="act">MIDNIGHT</span> '
                                      'RUN',
                      'css': {   'fontFamily': 'Trebuchet MS, sans-serif',
                                 'fontWeight': 'bold',
                                 'color': '#ffffff',
                                 'activeColor': '#fbbf24',
                                 'textTransform': 'uppercase',
                                 'textShadow': '0 0 10px #c084fc, 0 0 20px '
                                               '#d946ef'}},
    'neon_toxic': {   'id': 'neon_toxic',
                      'name': 'Toxic Amber Glow',
                      'category': 'neon_glow',
                      'category_label': 'Neon Cyber',
                      'description': 'Radioactive neon yellow-amber glow for '
                                     'high-adrenaline clips.',
                      'font': 'Arial Black',
                      'fallback_font': 'Impact',
                      'fontsize': 48,
                      'primary_color': '&H00FFFFFF',
                      'active_color': '&H0000E6FF',
                      'outline_color': '&H00002233',
                      'back_color': '&H00000000',
                      'bold': 1,
                      'outline': 3.5,
                      'shadow': 4.2,
                      'alignment': 2,
                      'margin_v': 74,
                      'uppercase': True,
                      'animation_type': 'glow_highlight',
                      'preview_class': 'preview-toxic-amber',
                      'preview_html': 'DANGER <span class="act">TOXIC</span> '
                                      'ZONE',
                      'css': {   'fontFamily': 'Arial Black, sans-serif',
                                 'color': '#ffffff',
                                 'activeColor': '#facc15',
                                 'textTransform': 'uppercase',
                                 'textShadow': '0 0 10px #eab308, 0 0 22px '
                                               '#ca8a04'}},
    'neon_synthwave': {   'id': 'neon_synthwave',
                          'name': 'Synthwave Horizon',
                          'category': 'neon_glow',
                          'category_label': 'Neon Cyber',
                          'description': '80s retro outrun synthwave style '
                                         'with neon cyan and pink highlights.',
                          'font': 'Trebuchet MS',
                          'fallback_font': 'Arial',
                          'fontsize': 46,
                          'primary_color': '&H00FFFF00',
                          'active_color': '&H00FF00FF',
                          'outline_color': '&H00330033',
                          'back_color': '&H00000000',
                          'bold': 1,
                          'outline': 3.0,
                          'shadow': 4.0,
                          'alignment': 2,
                          'margin_v': 72,
                          'uppercase': True,
                          'animation_type': 'glow_highlight',
                          'preview_class': 'preview-synthwave',
                          'preview_html': 'OUTRUN <span class="act">THE '
                                          'SUN</span> 1984',
                          'css': {   'fontFamily': 'Trebuchet MS, sans-serif',
                                     'fontWeight': 'bold',
                                     'color': '#22d3ee',
                                     'activeColor': '#f43f5e',
                                     'textTransform': 'uppercase',
                                     'textShadow': '0 0 10px #f43f5e, 0 0 20px '
                                                   '#06b6d4'}},
    'minimalist_modern': {   'id': 'minimalist_modern',
                             'name': 'Minimalist Documentary',
                             'category': 'cinematic',
                             'category_label': 'Cinematic',
                             'description': 'Clean, elegant lower-third '
                                            'subtitle bar with soft '
                                            'translucent backing. YouTube '
                                            'essays and interviews.',
                             'font': 'Arial',
                             'fallback_font': 'Helvetica',
                             'fontsize': 38,
                             'primary_color': '&H00F1F5F9',
                             'active_color': '&H0038BDF8',
                             'outline_color': '&H000F172A',
                             'back_color': '&H88000000',
                             'bold': 0,
                             'outline': 1.5,
                             'shadow': 1.0,
                             'alignment': 2,
                             'margin_v': 60,
                             'uppercase': False,
                             'animation_type': 'clean_karaoke',
                             'preview_class': 'preview-minimal',
                             'preview_html': 'Clean <span '
                                             'class="act">documentary</span> '
                                             'essay',
                             'css': {   'fontFamily': 'Arial, sans-serif',
                                        'color': '#cbd5e1',
                                        'activeColor': '#38bdf8',
                                        'background': 'rgba(0, 0, 0, 0.7)',
                                        'padding': '4px 10px',
                                        'borderRadius': '4px'}},
    'film_slate': {   'id': 'film_slate',
                      'name': '35mm Film Slate',
                      'category': 'cinematic',
                      'category_label': 'Cinematic',
                      'description': 'Crisp white cinema lettering with subtle '
                                     'letter-spacing for feature films and '
                                     'trailers.',
                      'font': 'Arial',
                      'fallback_font': 'Helvetica',
                      'fontsize': 36,
                      'primary_color': '&H00F8FAFC',
                      'active_color': '&H00FFFFFF',
                      'outline_color': '&H00000000',
                      'back_color': '&H40000000',
                      'bold': 1,
                      'outline': 2.0,
                      'shadow': 1.5,
                      'alignment': 2,
                      'margin_v': 58,
                      'uppercase': False,
                      'animation_type': 'standard_phrase',
                      'preview_class': 'preview-film-slate',
                      'preview_html': 'The truth behind <span class="act">the '
                                      'story</span> unfolds',
                      'css': {   'fontFamily': 'Arial, sans-serif',
                                 'fontWeight': 'bold',
                                 'color': '#f8fafc',
                                 'activeColor': '#ffffff',
                                 'letterSpacing': '1px',
                                 'textShadow': '1px 1px 2px #000'}},
    'noir_editorial': {   'id': 'noir_editorial',
                          'name': 'Film Noir Monochrome',
                          'category': 'cinematic',
                          'category_label': 'Cinematic',
                          'description': 'High contrast black-and-white '
                                         'elegance for dramatic narratives and '
                                         'deep commentary.',
                          'font': 'Georgia',
                          'fallback_font': 'Times New Roman',
                          'fontsize': 38,
                          'primary_color': '&H00E2E8F0',
                          'active_color': '&H00FFFFFF',
                          'outline_color': '&H00000000',
                          'back_color': '&H90000000',
                          'bold': 0,
                          'outline': 1.8,
                          'shadow': 2.0,
                          'alignment': 2,
                          'margin_v': 62,
                          'uppercase': False,
                          'animation_type': 'clean_karaoke',
                          'preview_class': 'preview-noir',
                          'preview_html': 'Shadows in the <span '
                                          'class="act">dark alleyway</span>',
                          'css': {   'fontFamily': 'Georgia, serif',
                                     'fontStyle': 'italic',
                                     'color': '#e2e8f0',
                                     'activeColor': '#ffffff',
                                     'textShadow': '2px 2px 3px #000'}},
    'editorial_serif': {   'id': 'editorial_serif',
                           'name': 'Editorial Serif Elegance',
                           'category': 'cinematic',
                           'category_label': 'Cinematic',
                           'description': 'Refined classic serif typography '
                                          'for video essays and historical '
                                          'deep dives.',
                           'font': 'Georgia',
                           'fallback_font': 'Times New Roman',
                           'fontsize': 40,
                           'primary_color': '&H00F1F5F9',
                           'active_color': '&H0060A5FA',
                           'outline_color': '&H000F172A',
                           'back_color': '&H00000000',
                           'bold': 1,
                           'outline': 2.2,
                           'shadow': 1.8,
                           'alignment': 2,
                           'margin_v': 64,
                           'uppercase': False,
                           'animation_type': 'clean_karaoke',
                           'preview_class': 'preview-editorial-serif',
                           'preview_html': 'A timeless <span '
                                           'class="act">editorial</span> '
                                           'perspective',
                           'css': {   'fontFamily': 'Georgia, serif',
                                      'fontWeight': 'bold',
                                      'color': '#f1f5f9',
                                      'activeColor': '#60a5fa',
                                      'textShadow': '1px 1px 2px #0f172a'}},
    'masterclass_sub': {   'id': 'masterclass_sub',
                           'name': 'Masterclass Studio White',
                           'category': 'cinematic',
                           'category_label': 'Cinematic',
                           'description': 'Sleek, high-production corporate '
                                          'studio subtitles inspired by '
                                          'MasterClass videos.',
                           'font': 'Segoe UI',
                           'fallback_font': 'Arial',
                           'fontsize': 38,
                           'primary_color': '&H00FFFFFF',
                           'active_color': '&H00F8FAFC',
                           'outline_color': '&H001E293B',
                           'back_color': '&H70000000',
                           'bold': 1,
                           'outline': 2.0,
                           'shadow': 1.2,
                           'alignment': 2,
                           'margin_v': 60,
                           'uppercase': False,
                           'animation_type': 'clean_karaoke',
                           'preview_class': 'preview-masterclass',
                           'preview_html': 'Mastering the craft of <span '
                                           'class="act">filmmaking</span>',
                           'css': {   'fontFamily': 'Segoe UI, sans-serif',
                                      'fontWeight': '600',
                                      'color': '#ffffff',
                                      'activeColor': '#ffffff',
                                      'background': 'rgba(15, 23, 42, 0.75)',
                                      'padding': '4px 12px',
                                      'borderRadius': '4px'}},
    'cinematic_gold': {   'id': 'cinematic_gold',
                          'name': 'A24 Warm Amber',
                          'category': 'cinematic',
                          'category_label': 'Cinematic',
                          'description': 'Warm muted amber tone for indie '
                                         'films, atmospheric cinema, and moody '
                                         'vlogs.',
                          'font': 'Arial',
                          'fallback_font': 'Helvetica',
                          'fontsize': 38,
                          'primary_color': '&H00D0E0E8',
                          'active_color': '&H0020C0FF',
                          'outline_color': '&H00000000',
                          'back_color': '&H60000000',
                          'bold': 1,
                          'outline': 2.2,
                          'shadow': 1.5,
                          'alignment': 2,
                          'margin_v': 60,
                          'uppercase': False,
                          'animation_type': 'clean_karaoke',
                          'preview_class': 'preview-cinematic-gold',
                          'preview_html': 'A poetic vision of <span '
                                          'class="act">golden light</span>',
                          'css': {   'fontFamily': 'Arial, sans-serif',
                                     'fontWeight': '600',
                                     'color': '#e2e8f0',
                                     'activeColor': '#fbbf24',
                                     'textShadow': '1px 1px 3px #000'}},
    'horizon_bar': {   'id': 'horizon_bar',
                       'name': 'Horizon Translucent Plate',
                       'category': 'cinematic',
                       'category_label': 'Cinematic',
                       'description': 'Full-width soft frosted bottom banner '
                                      'for flawless reading over busy camera '
                                      'pans.',
                       'font': 'Arial',
                       'fallback_font': 'Helvetica',
                       'fontsize': 36,
                       'primary_color': '&H00FFFFFF',
                       'active_color': '&H0038BDF8',
                       'outline_color': '&H00000000',
                       'back_color': '&HAA101010',
                       'bold': 0,
                       'border_style': 3,
                       'outline': 2.0,
                       'shadow': 0.0,
                       'alignment': 2,
                       'margin_v': 55,
                       'uppercase': False,
                       'animation_type': 'clean_karaoke',
                       'preview_class': 'preview-horizon-bar',
                       'preview_html': 'Across the vast <span '
                                       'class="act">ocean horizon</span>',
                       'css': {   'fontFamily': 'Arial, sans-serif',
                                  'color': '#ffffff',
                                  'activeColor': '#38bdf8',
                                  'background': 'rgba(16, 16, 16, 0.8)',
                                  'padding': '5px 14px',
                                  'borderRadius': '2px'}},
    'nordic_frost': {   'id': 'nordic_frost',
                        'name': 'Nordic Frosted Minimal',
                        'category': 'cinematic',
                        'category_label': 'Cinematic',
                        'description': 'Cool slate grey inactive text with '
                                       'pure crisp white active reveal.',
                        'font': 'Segoe UI',
                        'fallback_font': 'Arial',
                        'fontsize': 38,
                        'primary_color': '&H0094A3B8',
                        'active_color': '&H00FFFFFF',
                        'outline_color': '&H000F172A',
                        'back_color': '&H00000000',
                        'bold': 1,
                        'outline': 2.0,
                        'shadow': 1.5,
                        'alignment': 2,
                        'margin_v': 62,
                        'uppercase': False,
                        'animation_type': 'clean_karaoke',
                        'preview_class': 'preview-nordic',
                        'preview_html': 'Quiet reflections in the <span '
                                        'class="act">winter stillness</span>',
                        'css': {   'fontFamily': 'Segoe UI, sans-serif',
                                   'fontWeight': 'bold',
                                   'color': '#94a3b8',
                                   'activeColor': '#ffffff',
                                   'textShadow': '1px 1px 2px #0f172a'}},
    'boxed_pill': {   'id': 'boxed_pill',
                      'name': 'Boxed Pill Tag',
                      'category': 'boxed_pill',
                      'category_label': 'Boxed & Pill',
                      'description': 'Clean rounded orange/dark badge behind '
                                     'active text. High contrast readability '
                                     'on any video background.',
                      'font': 'Segoe UI',
                      'fallback_font': 'Arial',
                      'fontsize': 42,
                      'primary_color': '&H00FFFFFF',
                      'active_color': '&H0000D7FF',
                      'outline_color': '&H00000000',
                      'back_color': '&HCC1E1E1E',
                      'bold': 1,
                      'border_style': 3,
                      'outline': 3.0,
                      'shadow': 0.0,
                      'alignment': 2,
                      'margin_v': 75,
                      'uppercase': False,
                      'animation_type': 'box_pill',
                      'preview_class': 'preview-boxed',
                      'preview_html': 'HIGH <span class="act">CONTRAST</span> '
                                      'READ',
                      'css': {   'fontFamily': 'Segoe UI, sans-serif',
                                 'fontWeight': 'bold',
                                 'color': '#ffffff',
                                 'activeColor': '#ffffff',
                                 'activeBg': '#ea580c'}},
    'dark_slate_pill': {   'id': 'dark_slate_pill',
                           'name': 'Dark Slate Rounded Pill',
                           'category': 'boxed_pill',
                           'category_label': 'Boxed & Pill',
                           'description': 'Modern rounded dark slate pill '
                                          'backing for clean UI aesthetics.',
                           'font': 'Arial',
                           'fallback_font': 'Segoe UI',
                           'fontsize': 40,
                           'primary_color': '&H00E2E8F0',
                           'active_color': '&H0038BDF8',
                           'outline_color': '&H00000000',
                           'back_color': '&HE01E293B',
                           'bold': 1,
                           'border_style': 3,
                           'outline': 3.0,
                           'shadow': 0.0,
                           'alignment': 2,
                           'margin_v': 72,
                           'uppercase': False,
                           'animation_type': 'box_pill',
                           'preview_class': 'preview-slate-pill',
                           'preview_html': 'MODERN <span '
                                           'class="act">SLATE</span> BADGE',
                           'css': {   'fontFamily': 'Arial, sans-serif',
                                      'fontWeight': 'bold',
                                      'color': '#e2e8f0',
                                      'activeColor': '#ffffff',
                                      'activeBg': '#0284c7'}},
    'red_alert_box': {   'id': 'red_alert_box',
                         'name': 'Red Alert Tag Pill',
                         'category': 'boxed_pill',
                         'category_label': 'Boxed & Pill',
                         'description': 'High-urgency red badge behind active '
                                        'words, perfect for shocking hooks and '
                                        'facts.',
                         'font': 'Impact',
                         'fallback_font': 'Arial Black',
                         'fontsize': 46,
                         'primary_color': '&H00FFFFFF',
                         'active_color': '&H000000FF',
                         'outline_color': '&H00000000',
                         'back_color': '&HCC111827',
                         'bold': 1,
                         'border_style': 3,
                         'outline': 3.2,
                         'shadow': 0.0,
                         'alignment': 2,
                         'margin_v': 75,
                         'uppercase': True,
                         'animation_type': 'box_pill',
                         'preview_class': 'preview-red-alert',
                         'preview_html': 'CRITICAL <span '
                                         'class="act">WARNING</span> NOW',
                         'css': {   'fontFamily': 'Impact, sans-serif',
                                    'color': '#ffffff',
                                    'activeColor': '#ffffff',
                                    'activeBg': '#dc2626',
                                    'textTransform': 'uppercase'}},
    'emerald_pill': {   'id': 'emerald_pill',
                        'name': 'Emerald Pill Badge',
                        'category': 'boxed_pill',
                        'category_label': 'Boxed & Pill',
                        'description': 'Vibrant emerald green active word '
                                       'badge for finance, eco, and success '
                                       'topics.',
                        'font': 'Segoe UI',
                        'fallback_font': 'Arial',
                        'fontsize': 42,
                        'primary_color': '&H00FFFFFF',
                        'active_color': '&H0014FF39',
                        'outline_color': '&H00000000',
                        'back_color': '&HCC0F172A',
                        'bold': 1,
                        'border_style': 3,
                        'outline': 3.0,
                        'shadow': 0.0,
                        'alignment': 2,
                        'margin_v': 74,
                        'uppercase': False,
                        'animation_type': 'box_pill',
                        'preview_class': 'preview-emerald-pill',
                        'preview_html': 'PROVEN <span '
                                        'class="act">GROWTH</span> FORMULA',
                        'css': {   'fontFamily': 'Segoe UI, sans-serif',
                                   'fontWeight': 'bold',
                                   'color': '#ffffff',
                                   'activeColor': '#ffffff',
                                   'activeBg': '#059669'}},
    'purple_glow_box': {   'id': 'purple_glow_box',
                           'name': 'Electric Violet Box',
                           'category': 'boxed_pill',
                           'category_label': 'Boxed & Pill',
                           'description': 'Violet pill badge with bright white '
                                          'active lettering for lifestyle and '
                                          'AI creators.',
                           'font': 'Trebuchet MS',
                           'fallback_font': 'Arial',
                           'fontsize': 44,
                           'primary_color': '&H00FFFFFF',
                           'active_color': '&H00FF32B4',
                           'outline_color': '&H00000000',
                           'back_color': '&HCC1E1B4B',
                           'bold': 1,
                           'border_style': 3,
                           'outline': 3.0,
                           'shadow': 0.0,
                           'alignment': 2,
                           'margin_v': 74,
                           'uppercase': True,
                           'animation_type': 'box_pill',
                           'preview_class': 'preview-violet-box',
                           'preview_html': 'NEXT GEN <span '
                                           'class="act">CREATIVE</span> AI',
                           'css': {   'fontFamily': 'Trebuchet MS, sans-serif',
                                      'fontWeight': 'bold',
                                      'color': '#ffffff',
                                      'activeColor': '#ffffff',
                                      'activeBg': '#7c3aed',
                                      'textTransform': 'uppercase'}},
    'sunset_pill': {   'id': 'sunset_pill',
                       'name': 'Sunset Gradient Pill',
                       'category': 'boxed_pill',
                       'category_label': 'Boxed & Pill',
                       'description': 'Warm coral-sunset boxed tag that pops '
                                      'softly on both bright and dark frames.',
                       'font': 'Arial',
                       'fallback_font': 'Segoe UI',
                       'fontsize': 42,
                       'primary_color': '&H00FFFFFF',
                       'active_color': '&H002080FF',
                       'outline_color': '&H00000000',
                       'back_color': '&HCC18181B',
                       'bold': 1,
                       'border_style': 3,
                       'outline': 3.0,
                       'shadow': 0.0,
                       'alignment': 2,
                       'margin_v': 72,
                       'uppercase': False,
                       'animation_type': 'box_pill',
                       'preview_class': 'preview-sunset-pill',
                       'preview_html': 'Golden hour <span '
                                       'class="act">sunset</span> vibes',
                       'css': {   'fontFamily': 'Arial, sans-serif',
                                  'fontWeight': 'bold',
                                  'color': '#ffffff',
                                  'activeColor': '#ffffff',
                                  'activeBg': '#f97316'}},
    'royal_blue_badge': {   'id': 'royal_blue_badge',
                            'name': 'Royal Blue Clean Badge',
                            'category': 'boxed_pill',
                            'category_label': 'Boxed & Pill',
                            'description': 'Deep corporate royal blue pill '
                                           'badge with white typography.',
                            'font': 'Segoe UI',
                            'fallback_font': 'Arial',
                            'fontsize': 40,
                            'primary_color': '&H00F8FAFC',
                            'active_color': '&H00FF8000',
                            'outline_color': '&H00000000',
                            'back_color': '&HCC0F172A',
                            'bold': 1,
                            'border_style': 3,
                            'outline': 2.8,
                            'shadow': 0.0,
                            'alignment': 2,
                            'margin_v': 70,
                            'uppercase': False,
                            'animation_type': 'box_pill',
                            'preview_class': 'preview-royal-blue',
                            'preview_html': 'Trusted by <span '
                                            'class="act">industry '
                                            'leaders</span>',
                            'css': {   'fontFamily': 'Segoe UI, sans-serif',
                                       'fontWeight': 'bold',
                                       'color': '#ffffff',
                                       'activeColor': '#ffffff',
                                       'activeBg': '#1d4ed8'}},
    'high_vis_amber': {   'id': 'high_vis_amber',
                          'name': 'High-Vis Amber Pill',
                          'category': 'boxed_pill',
                          'category_label': 'Boxed & Pill',
                          'description': 'High-visibility industrial black '
                                         'pill with pure vibrant amber active '
                                         'text.',
                          'font': 'Arial Black',
                          'fallback_font': 'Impact',
                          'fontsize': 44,
                          'primary_color': '&H00E2E8F0',
                          'active_color': '&H0000D7FF',
                          'outline_color': '&H00000000',
                          'back_color': '&HEE000000',
                          'bold': 1,
                          'border_style': 3,
                          'outline': 3.2,
                          'shadow': 0.0,
                          'alignment': 2,
                          'margin_v': 75,
                          'uppercase': True,
                          'animation_type': 'box_pill',
                          'preview_class': 'preview-vis-amber',
                          'preview_html': 'ATTENTION <span class="act">HIGH '
                                          'VALUE</span> STEP',
                          'css': {   'fontFamily': 'Arial Black, sans-serif',
                                     'color': '#ffffff',
                                     'activeColor': '#000000',
                                     'activeBg': '#fbbf24',
                                     'textTransform': 'uppercase'}},
    'headline_3d_punch': {   'id': 'headline_3d_punch',
                             'name': '3D Punch Out Headline',
                             'category': 'headline',
                             'category_label': 'Headline',
                             'description': 'Heavy 3D extruded drop shadow '
                                            'giving physical weight to every '
                                            'word.',
                             'font': 'Impact',
                             'fallback_font': 'Arial Black',
                             'fontsize': 54,
                             'primary_color': '&H00FFFFFF',
                             'active_color': '&H0000E6FF',
                             'outline_color': '&H00000000',
                             'back_color': '&H00000000',
                             'bold': 1,
                             'outline': 4.5,
                             'shadow': 4.5,
                             'alignment': 2,
                             'margin_v': 76,
                             'uppercase': True,
                             'animation_type': 'bounce_pop',
                             'preview_class': 'preview-3d-punch',
                             'preview_html': 'MASSIVE <span class="act">3D '
                                             'PUNCH</span> IMPACT',
                             'css': {   'fontFamily': 'Impact, sans-serif',
                                        'color': '#ffffff',
                                        'activeColor': '#facc15',
                                        'textTransform': 'uppercase',
                                        'textShadow': '3px 3px 0 #000, 6px 6px '
                                                      '0 rgba(0,0,0,0.6)'}},
    'headline_angled': {   'id': 'headline_angled',
                           'name': 'Angled Action Banner',
                           'category': 'headline',
                           'category_label': 'Headline',
                           'description': 'Slightly skewed high-velocity '
                                          'sports and action headline '
                                          'typography.',
                           'font': 'Arial Black',
                           'fallback_font': 'Impact',
                           'fontsize': 50,
                           'primary_color': '&H00FFFFFF',
                           'active_color': '&H0000FF00',
                           'outline_color': '&H00000000',
                           'back_color': '&H00000000',
                           'bold': 1,
                           'outline': 4.0,
                           'shadow': 3.0,
                           'alignment': 2,
                           'margin_v': 78,
                           'uppercase': True,
                           'animation_type': 'bounce_pop',
                           'preview_class': 'preview-angled',
                           'preview_html': 'EXPLOSIVE <span '
                                           'class="act">ACTION</span> SPEED',
                           'css': {   'fontFamily': 'Arial Black, sans-serif',
                                      'fontStyle': 'italic',
                                      'color': '#ffffff',
                                      'activeColor': '#22c55e',
                                      'textTransform': 'uppercase',
                                      'textShadow': '3px 3px 0 #000'}},
    'headline_big_impact': {   'id': 'headline_big_impact',
                               'name': 'Big Impact Heavyweight',
                               'category': 'headline',
                               'category_label': 'Headline',
                               'description': 'Ultra-thick, condensed '
                                              'heavyweight letters for '
                                              'dramatic YouTube titles.',
                               'font': 'Impact',
                               'fallback_font': 'Arial Black',
                               'fontsize': 56,
                               'primary_color': '&H00FFFFFF',
                               'active_color': '&H0000FFFF',
                               'outline_color': '&H00000000',
                               'back_color': '&H90000000',
                               'bold': 1,
                               'outline': 5.0,
                               'shadow': 3.0,
                               'alignment': 2,
                               'margin_v': 75,
                               'uppercase': True,
                               'animation_type': 'scale_pulse',
                               'preview_class': 'preview-big-impact',
                               'preview_html': 'THE BIGGEST <span '
                                               'class="act">SECRET</span> EVER',
                               'css': {   'fontFamily': 'Impact, sans-serif',
                                          'color': '#ffffff',
                                          'activeColor': '#facc15',
                                          'textTransform': 'uppercase',
                                          'textShadow': '-3px -3px 0 #000, 3px '
                                                        '-3px 0 #000, -3px 3px '
                                                        '0 #000, 3px 3px 0 '
                                                        '#000'}},
    'headline_blackout': {   'id': 'headline_blackout',
                             'name': 'Blackout Inverted Punch',
                             'category': 'headline',
                             'category_label': 'Headline',
                             'description': 'Inverted black typography with '
                                            'heavy yellow and white strokes.',
                             'font': 'Impact',
                             'fallback_font': 'Arial Black',
                             'fontsize': 52,
                             'primary_color': '&H00000000',
                             'active_color': '&H0000FFFF',
                             'outline_color': '&H00FFFFFF',
                             'back_color': '&H00000000',
                             'bold': 1,
                             'outline': 4.5,
                             'shadow': 3.0,
                             'alignment': 2,
                             'margin_v': 75,
                             'uppercase': True,
                             'animation_type': 'bounce_pop',
                             'preview_class': 'preview-blackout',
                             'preview_html': 'INVERTED <span '
                                             'class="act">BLACKOUT</span> '
                                             'PUNCH',
                             'css': {   'fontFamily': 'Impact, sans-serif',
                                        'color': '#000000',
                                        'activeColor': '#ffe600',
                                        'textTransform': 'uppercase',
                                        'textShadow': '-2px -2px 0 #fff, 2px '
                                                      '-2px 0 #fff, -2px 2px 0 '
                                                      '#fff, 2px 2px 0 #fff'}},
    'headline_thunder': {   'id': 'headline_thunder',
                            'name': 'Thunder Yellow Stroke',
                            'category': 'headline',
                            'category_label': 'Headline',
                            'description': 'High-voltage lightning yellow '
                                           'stroke with dark midnight blue '
                                           'body.',
                            'font': 'Arial Black',
                            'fallback_font': 'Impact',
                            'fontsize': 50,
                            'primary_color': '&H00201005',
                            'active_color': '&H0000E6FF',
                            'outline_color': '&H0000D7FF',
                            'back_color': '&H00000000',
                            'bold': 1,
                            'outline': 4.0,
                            'shadow': 3.0,
                            'alignment': 2,
                            'margin_v': 75,
                            'uppercase': True,
                            'animation_type': 'scale_pulse',
                            'preview_class': 'preview-thunder',
                            'preview_html': 'THUNDER <span '
                                            'class="act">STRIKE</span> POWER',
                            'css': {   'fontFamily': 'Arial Black, sans-serif',
                                       'color': '#0f172a',
                                       'activeColor': '#fbbf24',
                                       'textTransform': 'uppercase',
                                       'textShadow': '-2px -2px 0 #facc15, 2px '
                                                     '-2px 0 #facc15'}},
    'headline_heavy_metal': {   'id': 'headline_heavy_metal',
                                'name': 'Heavy Metal Chrome',
                                'category': 'headline',
                                'category_label': 'Headline',
                                'description': 'Chiseled metallic chrome with '
                                               'sharp black bevel shadow.',
                                'font': 'Impact',
                                'fallback_font': 'Arial Black',
                                'fontsize': 52,
                                'primary_color': '&H00E2E8F0',
                                'active_color': '&H00FFFFFF',
                                'outline_color': '&H00000000',
                                'back_color': '&H80000000',
                                'bold': 1,
                                'outline': 4.5,
                                'shadow': 3.5,
                                'alignment': 2,
                                'margin_v': 75,
                                'uppercase': True,
                                'animation_type': 'bounce_pop',
                                'preview_class': 'preview-heavy-metal',
                                'preview_html': 'RAW <span '
                                                'class="act">UNSTOPPABLE</span> '
                                                'FORCE',
                                'css': {   'fontFamily': 'Impact, sans-serif',
                                           'color': '#e2e8f0',
                                           'activeColor': '#ffffff',
                                           'textTransform': 'uppercase',
                                           'textShadow': '3px 3px 0 #000, 5px '
                                                         '5px 0 #475569'}},
    'headline_stencil': {   'id': 'headline_stencil',
                            'name': 'Military Bold Stencil',
                            'category': 'headline',
                            'category_label': 'Headline',
                            'description': 'Tactical military-grade stencil '
                                           'aesthetic for survival and outdoor '
                                           'content.',
                            'font': 'Arial Black',
                            'fallback_font': 'Trebuchet MS',
                            'fontsize': 48,
                            'primary_color': '&H00D9E2EC',
                            'active_color': '&H0010E030',
                            'outline_color': '&H000F1710',
                            'back_color': '&H00000000',
                            'bold': 1,
                            'outline': 3.8,
                            'shadow': 2.5,
                            'alignment': 2,
                            'margin_v': 75,
                            'uppercase': True,
                            'animation_type': 'karaoke_highlight',
                            'preview_class': 'preview-stencil',
                            'preview_html': 'TACTICAL <span '
                                            'class="act">SURVIVAL</span> GEAR',
                            'css': {   'fontFamily': 'Arial Black, sans-serif',
                                       'letterSpacing': '2px',
                                       'color': '#cbd5e1',
                                       'activeColor': '#4ade80',
                                       'textTransform': 'uppercase',
                                       'textShadow': '2px 2px 0 #0f172a'}},
    'headline_iron': {   'id': 'headline_iron',
                         'name': 'Iron Titan Display',
                         'category': 'headline',
                         'category_label': 'Headline',
                         'description': 'Solid, grounded heavy headline '
                                        'typography for motivational edits.',
                         'font': 'Impact',
                         'fallback_font': 'Arial Black',
                         'fontsize': 54,
                         'primary_color': '&H00FFFFFF',
                         'active_color': '&H0000A5FF',
                         'outline_color': '&H00000000',
                         'back_color': '&H00000000',
                         'bold': 1,
                         'outline': 4.5,
                         'shadow': 2.8,
                         'alignment': 2,
                         'margin_v': 75,
                         'uppercase': True,
                         'animation_type': 'scale_pulse',
                         'preview_class': 'preview-iron-titan',
                         'preview_html': 'FORGED IN <span '
                                         'class="act">IRON</span> DISCIPLINE',
                         'css': {   'fontFamily': 'Impact, sans-serif',
                                    'color': '#ffffff',
                                    'activeColor': '#f97316',
                                    'textTransform': 'uppercase',
                                    'textShadow': '-2px -2px 0 #000, 2px -2px '
                                                  '0 #000, -2px 2px 0 #000, '
                                                  '2px 2px 0 #000'}},
    'comic_pop': {   'id': 'comic_pop',
                     'name': 'Comic Pop Playful',
                     'category': 'comic_pop',
                     'category_label': 'Comic Pop',
                     'description': 'Playful, bold, high-contrast comic '
                                    'aesthetic with 3D shadow depth. Great for '
                                    'storytelling & kids content.',
                     'font': 'Trebuchet MS',
                     'fallback_font': 'Arial Black',
                     'fontsize': 48,
                     'primary_color': '&H0000FFFF',
                     'active_color': '&H00FF33FF',
                     'outline_color': '&H00000000',
                     'back_color': '&H00000000',
                     'bold': 1,
                     'outline': 5.0,
                     'shadow': 4.0,
                     'alignment': 2,
                     'margin_v': 75,
                     'uppercase': True,
                     'animation_type': 'bounce_pop',
                     'preview_class': 'preview-comic',
                     'preview_html': 'PLAYFUL <span class="act">COMIC</span> '
                                     'FUN',
                     'css': {   'fontFamily': 'Trebuchet MS, cursive',
                                'fontWeight': 'bold',
                                'color': '#facc15',
                                'activeColor': '#ec4899',
                                'textTransform': 'uppercase',
                                'textShadow': '2px 2px 0 #ec4899, 4px 4px 0 '
                                              '#000'}},
    'bubble_pink': {   'id': 'bubble_pink',
                       'name': 'Bubblegum Pink Pop',
                       'category': 'comic_pop',
                       'category_label': 'Comic Pop',
                       'description': 'Sweet bubblegum pink with cyan drop '
                                      'shadow for fun vlog edits.',
                       'font': 'Arial Black',
                       'fallback_font': 'Trebuchet MS',
                       'fontsize': 46,
                       'primary_color': '&H00FF80DF',
                       'active_color': '&H00FFFFFF',
                       'outline_color': '&H00000000',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 4.0,
                       'shadow': 3.5,
                       'alignment': 2,
                       'margin_v': 74,
                       'uppercase': True,
                       'animation_type': 'bounce_pop',
                       'preview_class': 'preview-bubble-pink',
                       'preview_html': 'SWEET <span '
                                       'class="act">BUBBLEGUM</span> POP',
                       'css': {   'fontFamily': 'Arial Black, sans-serif',
                                  'color': '#f472b6',
                                  'activeColor': '#ffffff',
                                  'textTransform': 'uppercase',
                                  'textShadow': '2px 2px 0 #06b6d4, 4px 4px 0 '
                                                '#000'}},
    'arcade_8bit': {   'id': 'arcade_8bit',
                       'name': 'Arcade Retro 8-Bit',
                       'category': 'comic_pop',
                       'category_label': 'Comic Pop',
                       'description': 'Pixel arcade gaming aesthetic with neon '
                                      'yellow and hot magenta colors.',
                       'font': 'Trebuchet MS',
                       'fallback_font': 'Courier New',
                       'fontsize': 44,
                       'primary_color': '&H0000FF00',
                       'active_color': '&H0000FFFF',
                       'outline_color': '&H00000000',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 4.0,
                       'shadow': 3.0,
                       'alignment': 2,
                       'margin_v': 70,
                       'uppercase': True,
                       'animation_type': 'bounce_pop',
                       'preview_class': 'preview-arcade-8bit',
                       'preview_html': 'PRESS <span class="act">START</span> '
                                       'TO PLAY',
                       'css': {   'fontFamily': 'Trebuchet MS, monospace',
                                  'fontWeight': 'bold',
                                  'color': '#4ade80',
                                  'activeColor': '#facc15',
                                  'textTransform': 'uppercase',
                                  'textShadow': '3px 3px 0 #000'}},
    'cartoon_blast': {   'id': 'cartoon_blast',
                         'name': 'Cartoon Dynamic Blast',
                         'category': 'comic_pop',
                         'category_label': 'Comic Pop',
                         'description': 'High-bounce comic lettering with '
                                        'energetic color pops.',
                         'font': 'Impact',
                         'fallback_font': 'Trebuchet MS',
                         'fontsize': 50,
                         'primary_color': '&H0000E6FF',
                         'active_color': '&H000000FF',
                         'outline_color': '&H00000000',
                         'back_color': '&H00000000',
                         'bold': 1,
                         'outline': 4.8,
                         'shadow': 3.5,
                         'alignment': 2,
                         'margin_v': 76,
                         'uppercase': True,
                         'animation_type': 'bounce_pop',
                         'preview_class': 'preview-cartoon-blast',
                         'preview_html': 'KA-BOOM <span '
                                         'class="act">EXPLOSION</span> NOW',
                         'css': {   'fontFamily': 'Impact, sans-serif',
                                    'color': '#facc15',
                                    'activeColor': '#ef4444',
                                    'textTransform': 'uppercase',
                                    'textShadow': '2px 2px 0 #ef4444, 4px 4px '
                                                  '0 #000'}},
    'pop_art_yellow': {   'id': 'pop_art_yellow',
                          'name': 'Pop Art Halftone Yellow',
                          'category': 'comic_pop',
                          'category_label': 'Comic Pop',
                          'description': 'Lichtenstein-inspired vintage pop '
                                         'art yellow with bold black outlines.',
                          'font': 'Arial Black',
                          'fallback_font': 'Trebuchet MS',
                          'fontsize': 48,
                          'primary_color': '&H00FFFFFF',
                          'active_color': '&H0000E1FF',
                          'outline_color': '&H00000000',
                          'back_color': '&H00000000',
                          'bold': 1,
                          'outline': 4.5,
                          'shadow': 3.2,
                          'alignment': 2,
                          'margin_v': 75,
                          'uppercase': True,
                          'animation_type': 'karaoke_highlight',
                          'preview_class': 'preview-pop-art',
                          'preview_html': 'VINTAGE <span class="act">POP '
                                          'ART</span> LOOK',
                          'css': {   'fontFamily': 'Arial Black, sans-serif',
                                     'color': '#ffffff',
                                     'activeColor': '#fbbf24',
                                     'textTransform': 'uppercase',
                                     'textShadow': '3px 3px 0 #000'}},
    'comic_kapow': {   'id': 'comic_kapow',
                       'name': 'Kapow Action Comic',
                       'category': 'comic_pop',
                       'category_label': 'Comic Pop',
                       'description': 'Superhero action scene font with bright '
                                      'cyan and fiery orange highlights.',
                       'font': 'Impact',
                       'fallback_font': 'Arial Black',
                       'fontsize': 52,
                       'primary_color': '&H00FFFF00',
                       'active_color': '&H000066FF',
                       'outline_color': '&H00000000',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 4.8,
                       'shadow': 3.8,
                       'alignment': 2,
                       'margin_v': 76,
                       'uppercase': True,
                       'animation_type': 'bounce_pop',
                       'preview_class': 'preview-comic-kapow',
                       'preview_html': 'KAPOW <span class="act">SUPER</span> '
                                       'PUNCH',
                       'css': {   'fontFamily': 'Impact, sans-serif',
                                  'color': '#06b6d4',
                                  'activeColor': '#f97316',
                                  'textTransform': 'uppercase',
                                  'textShadow': '2px 2px 0 #000, 4px 4px 0 '
                                                '#f97316'}},
    'kawaii_lilac': {   'id': 'kawaii_lilac',
                        'name': 'Kawaii Pastel Lilac',
                        'category': 'comic_pop',
                        'category_label': 'Comic Pop',
                        'description': 'Gentle pastel lilac and mint tones for '
                                       'cozy, cute, and aesthetic vlogs.',
                        'font': 'Trebuchet MS',
                        'fallback_font': 'Arial',
                        'fontsize': 44,
                        'primary_color': '&H00F0D0FF',
                        'active_color': '&H00C0FFB0',
                        'outline_color': '&H00331033',
                        'back_color': '&H00000000',
                        'bold': 1,
                        'outline': 3.0,
                        'shadow': 2.0,
                        'alignment': 2,
                        'margin_v': 72,
                        'uppercase': False,
                        'animation_type': 'bounce_pop',
                        'preview_class': 'preview-kawaii',
                        'preview_html': 'Super cute <span class="act">cozy '
                                        'vlog</span> vibes',
                        'css': {   'fontFamily': 'Trebuchet MS, sans-serif',
                                   'fontWeight': 'bold',
                                   'color': '#e9d5ff',
                                   'activeColor': '#86efac',
                                   'textShadow': '2px 2px 0 #581c87'}},
    'superhero_red': {   'id': 'superhero_red',
                         'name': 'Superhero Comic Punch',
                         'category': 'comic_pop',
                         'category_label': 'Comic Pop',
                         'description': 'Iconic comic book red letters with '
                                        'golden yellow active glow.',
                         'font': 'Impact',
                         'fallback_font': 'Arial Black',
                         'fontsize': 52,
                         'primary_color': '&H002020FF',
                         'active_color': '&H0000FFFF',
                         'outline_color': '&H00000000',
                         'back_color': '&H00000000',
                         'bold': 1,
                         'outline': 4.5,
                         'shadow': 3.5,
                         'alignment': 2,
                         'margin_v': 75,
                         'uppercase': True,
                         'animation_type': 'bounce_pop',
                         'preview_class': 'preview-superhero-red',
                         'preview_html': 'MIGHTY <span class="act">HERO</span> '
                                         'RISES',
                         'css': {   'fontFamily': 'Impact, sans-serif',
                                    'color': '#ef4444',
                                    'activeColor': '#facc15',
                                    'textTransform': 'uppercase',
                                    'textShadow': '2px 2px 0 #000, 4px 4px 0 '
                                                  '#facc15'}},
    'classic_broadcast': {   'id': 'classic_broadcast',
                             'name': 'Classic Broadcast',
                             'category': 'broadcast',
                             'category_label': 'Broadcast',
                             'description': 'Standard Netflix / TV crisp white '
                                            'typography with deep black shadow '
                                            'outline. 100% timeless.',
                             'font': 'Arial',
                             'fallback_font': 'Helvetica',
                             'fontsize': 40,
                             'primary_color': '&H00FFFFFF',
                             'active_color': '&H00FFFFFF',
                             'outline_color': '&H00000000',
                             'back_color': '&H00000000',
                             'bold': 1,
                             'outline': 3.0,
                             'shadow': 2.0,
                             'alignment': 2,
                             'margin_v': 65,
                             'uppercase': False,
                             'animation_type': 'standard_phrase',
                             'preview_class': 'preview-broadcast',
                             'preview_html': 'Standard broadcast clarity',
                             'css': {   'fontFamily': 'Arial, sans-serif',
                                        'fontWeight': 'bold',
                                        'color': '#ffffff',
                                        'activeColor': '#ffffff',
                                        'textShadow': '2px 2px 3px #000'}},
    'netflix_clean': {   'id': 'netflix_clean',
                         'name': 'Netflix Standard Subtitle',
                         'category': 'broadcast',
                         'category_label': 'Broadcast',
                         'description': 'Calibrated to Netflix technical '
                                        'subtitle delivery specs for '
                                        'international streaming.',
                         'font': 'Arial',
                         'fallback_font': 'Helvetica',
                         'fontsize': 38,
                         'primary_color': '&H00FFFFFF',
                         'active_color': '&H00F1F5F9',
                         'outline_color': '&H00000000',
                         'back_color': '&H80000000',
                         'bold': 0,
                         'outline': 2.0,
                         'shadow': 1.5,
                         'alignment': 2,
                         'margin_v': 60,
                         'uppercase': False,
                         'animation_type': 'standard_phrase',
                         'preview_class': 'preview-netflix',
                         'preview_html': 'Streaming clarity for all viewers '
                                         'worldwide.',
                         'css': {   'fontFamily': 'Arial, sans-serif',
                                    'color': '#ffffff',
                                    'activeColor': '#f8fafc',
                                    'textShadow': '1.5px 1.5px 2px #000'}},
    'youtube_standard': {   'id': 'youtube_standard',
                            'name': 'YouTube CC Crisp',
                            'category': 'broadcast',
                            'category_label': 'Broadcast',
                            'description': 'Standard YouTube closed-captioning '
                                           'typography with black backing '
                                           'strip.',
                            'font': 'Roboto',
                            'fallback_font': 'Arial',
                            'fontsize': 36,
                            'primary_color': '&H00FFFFFF',
                            'active_color': '&H00FFFFFF',
                            'outline_color': '&H00000000',
                            'back_color': '&HE0080808',
                            'bold': 0,
                            'border_style': 3,
                            'outline': 2.0,
                            'shadow': 0.0,
                            'alignment': 2,
                            'margin_v': 60,
                            'uppercase': False,
                            'animation_type': 'standard_phrase',
                            'preview_class': 'preview-youtube-cc',
                            'preview_html': 'Official YouTube closed caption '
                                            'format',
                            'css': {   'fontFamily': 'Arial, sans-serif',
                                       'color': '#ffffff',
                                       'activeColor': '#ffffff',
                                       'background': 'rgba(8, 8, 8, 0.85)',
                                       'padding': '4px 8px'}},
    'bbc_crisp': {   'id': 'bbc_crisp',
                     'name': 'BBC Editorial Subtitle',
                     'category': 'broadcast',
                     'category_label': 'Broadcast',
                     'description': 'High-legibility typography matching BBC '
                                    'news broadcast standard.',
                     'font': 'Arial',
                     'fallback_font': 'Helvetica',
                     'fontsize': 38,
                     'primary_color': '&H0000FFFF',
                     'active_color': '&H0000FFFF',
                     'outline_color': '&H00000000',
                     'back_color': '&H80000000',
                     'bold': 1,
                     'outline': 2.5,
                     'shadow': 1.5,
                     'alignment': 2,
                     'margin_v': 62,
                     'uppercase': False,
                     'animation_type': 'standard_phrase',
                     'preview_class': 'preview-bbc',
                     'preview_html': 'BBC News international broadcast format',
                     'css': {   'fontFamily': 'Arial, sans-serif',
                                'fontWeight': 'bold',
                                'color': '#facc15',
                                'activeColor': '#facc15',
                                'textShadow': '2px 2px 2px #000'}},
    'corporate_navy': {   'id': 'corporate_navy',
                          'name': 'Corporate Clean Navy',
                          'category': 'broadcast',
                          'category_label': 'Broadcast',
                          'description': 'Subtle deep navy and crisp white for '
                                         'enterprise and B2B SaaS '
                                         'presentations.',
                          'font': 'Segoe UI',
                          'fallback_font': 'Arial',
                          'fontsize': 38,
                          'primary_color': '&H00FFFFFF',
                          'active_color': '&H0060A5FA',
                          'outline_color': '&H000F172A',
                          'back_color': '&H00000000',
                          'bold': 1,
                          'outline': 2.2,
                          'shadow': 1.5,
                          'alignment': 2,
                          'margin_v': 65,
                          'uppercase': False,
                          'animation_type': 'clean_karaoke',
                          'preview_class': 'preview-corp-navy',
                          'preview_html': 'Enterprise <span '
                                          'class="act">quarterly review</span> '
                                          'metrics',
                          'css': {   'fontFamily': 'Segoe UI, sans-serif',
                                     'fontWeight': '600',
                                     'color': '#ffffff',
                                     'activeColor': '#60a5fa',
                                     'textShadow': '1px 1px 3px #0f172a'}},
    'ted_speaker': {   'id': 'ted_speaker',
                       'name': 'TED Stage Keynote',
                       'category': 'broadcast',
                       'category_label': 'Broadcast',
                       'description': 'Refined sans-serif subtitle for keynote '
                                      'speeches and TED-style ideas.',
                       'font': 'Helvetica',
                       'fallback_font': 'Arial',
                       'fontsize': 38,
                       'primary_color': '&H00F8FAFC',
                       'active_color': '&H000000FF',
                       'outline_color': '&H00000000',
                       'back_color': '&H00000000',
                       'bold': 1,
                       'outline': 2.2,
                       'shadow': 1.5,
                       'alignment': 2,
                       'margin_v': 62,
                       'uppercase': False,
                       'animation_type': 'clean_karaoke',
                       'preview_class': 'preview-ted',
                       'preview_html': 'Ideas worth <span '
                                       'class="act">spreading</span> worldwide',
                       'css': {   'fontFamily': 'Arial, sans-serif',
                                  'fontWeight': 'bold',
                                  'color': '#f8fafc',
                                  'activeColor': '#ef4444',
                                  'textShadow': '1px 1px 2px #000'}},
    'swiss_neutral': {   'id': 'swiss_neutral',
                         'name': 'Swiss Neutral Typography',
                         'category': 'broadcast',
                         'category_label': 'Broadcast',
                         'description': 'Understated Helvetica Swiss grid '
                                        'typography for architectural and '
                                        'design content.',
                         'font': 'Arial',
                         'fallback_font': 'Helvetica',
                         'fontsize': 36,
                         'primary_color': '&H00E2E8F0',
                         'active_color': '&H00FFFFFF',
                         'outline_color': '&H0018181B',
                         'back_color': '&H00000000',
                         'bold': 0,
                         'outline': 1.8,
                         'shadow': 1.0,
                         'alignment': 2,
                         'margin_v': 58,
                         'uppercase': False,
                         'animation_type': 'standard_phrase',
                         'preview_class': 'preview-swiss',
                         'preview_html': 'Functional and objective typographic '
                                         'form',
                         'css': {   'fontFamily': 'Arial, sans-serif',
                                    'color': '#e2e8f0',
                                    'activeColor': '#ffffff',
                                    'letterSpacing': '0.5px',
                                    'textShadow': '1px 1px 1px #18181b'}},
    'subtitle_pro': {   'id': 'subtitle_pro',
                        'name': 'Universal Subtitle Pro',
                        'category': 'broadcast',
                        'category_label': 'Broadcast',
                        'description': 'High-contrast accessibility-compliant '
                                       'subtitle for universal legibility.',
                        'font': 'Verdana',
                        'fallback_font': 'Arial',
                        'fontsize': 36,
                        'primary_color': '&H00FFFFFF',
                        'active_color': '&H00FFFFFF',
                        'outline_color': '&H00000000',
                        'back_color': '&HCC000000',
                        'bold': 1,
                        'outline': 3.0,
                        'shadow': 1.5,
                        'alignment': 2,
                        'margin_v': 62,
                        'uppercase': False,
                        'animation_type': 'standard_phrase',
                        'preview_class': 'preview-sub-pro',
                        'preview_html': 'Universal legibility across all '
                                        'displays',
                        'css': {   'fontFamily': 'Verdana, sans-serif',
                                   'fontWeight': 'bold',
                                   'color': '#ffffff',
                                   'activeColor': '#ffffff',
                                   'textShadow': '2px 2px 2px #000'}}}

def generate_ass_subtitles(transcript_data: dict, style_key: str, output_ass_path: str, video_width: int = 1920, video_height: int = 1080, pos_x: float = None, pos_y: float = None, font_scale: float = 1.0):
    style = CAPTION_STYLES.get(style_key, CAPTION_STYLES["hormozi_bold"])

    font = style.get("font", "Arial")
    fontsize = style.get("fontsize", 44)
    if font_scale and font_scale > 0 and font_scale != 1.0:
        fontsize = max(14, int(round(fontsize * float(font_scale))))

    primary_c = style.get("primary_color", "&H00FFFFFF")
    active_c = style.get("active_color", "&H0000FFFF")
    outline_c = style.get("outline_color", "&H00000000")
    back_c = style.get("back_color", "&H80000000")
    bold = style.get("bold", 1)
    outline = style.get("outline", 3.0)
    shadow = style.get("shadow", 2.0)
    alignment = style.get("alignment", 2)
    margin_v = style.get("margin_v", 70)
    border_style = style.get("border_style", 1)
    is_uppercase = style.get("uppercase", False)
    anim_type = style.get("animation_type", "karaoke_highlight")

    # Interactive monitor positioning support
    pos_tag = ""
    if pos_x is not None or pos_y is not None:
        px = int(round((pos_x if pos_x is not None else 0.5) * video_width))
        py = int(round((pos_y if pos_y is not None else 0.85) * video_height))
        pos_tag = f"{{\\an5\\pos({px},{py})}}"

    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {video_width}",
        f"PlayResY: {video_height}",
        "ScaledBorderAndShadow: yes",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{font},{fontsize},{primary_c},{active_c},{outline_c},{back_c},{bold},0,0,0,100,100,0,0,{border_style},{outline},{shadow},{alignment},40,40,{margin_v},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    if isinstance(transcript_data, list):
        segments = transcript_data
    elif isinstance(transcript_data, dict):
        segments = transcript_data.get("segments", transcript_data.get("cues", []))
    else:
        segments = []

    for seg in segments:
        words = seg.get("words")
        if words is None:
            txt = seg.get("text", "").strip()
            if not txt:
                continue
            seg_start = float(seg.get("start", 0.0))
            seg_end = float(seg.get("end", seg_start + 1.0))
            tokens = txt.split()
            if len(tokens) > 1 and seg_end > seg_start:
                step = (seg_end - seg_start) / len(tokens)
                words = [{"word": tok, "start": seg_start + idx * step, "end": seg_start + (idx + 1) * step} for idx, tok in enumerate(tokens)]
            else:
                words = []

        if not words:
            start_str = format_ass_time(seg.get("start", 0.0))
            end_str = format_ass_time(seg.get("end", 0.0))
            txt = seg.get("text", "").strip()
            if is_uppercase:
                txt = txt.upper()
            if pos_tag:
                txt = f"{pos_tag}{txt}"
            ass_lines.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{txt}")
            continue

        chunk_size = 4
        word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

        for chunk in word_chunks:
            chunk_start = chunk[0]["start"]
            chunk_end = chunk[-1]["end"]
            
            if chunk_end <= chunk_start:
                chunk_end = chunk_start + 0.5

            for i, target_word in enumerate(chunk):
                w_start = target_word["start"]
                w_end = target_word["end"]
                
                if w_end <= w_start:
                    w_end = w_start + 0.25

                start_str = format_ass_time(w_start)
                end_str = format_ass_time(w_end)

                line_parts = []
                for j, w in enumerate(chunk):
                    raw_word = w["word"]
                    if is_uppercase:
                        raw_word = raw_word.upper()

                    if j == i:
                        if anim_type == "bounce_pop":
                            line_parts.append(f"{{\\c{active_c}\\fscx115\\fscy115}}{raw_word}{{\\fscx100\\fscy100\\c{primary_c}}}")
                        elif anim_type == "scale_pulse":
                            line_parts.append(f"{{\\c{active_c}\\fscx120\\fscy120}}{raw_word}{{\\fscx100\\fscy100\\c{primary_c}}}")
                        elif anim_type in ["karaoke_highlight", "glow_highlight", "clean_karaoke"]:
                            line_parts.append(f"{{\\c{active_c}}}{raw_word}{{\\c{primary_c}}}")
                        elif anim_type == "box_pill":
                            line_parts.append(f"{{\\c{active_c}\\b1}}{raw_word}{{\\c{primary_c}}}")
                        else:
                            line_parts.append(raw_word)
                    else:
                        line_parts.append(raw_word)

                dialogue_text = " ".join(line_parts)
                if pos_tag:
                    dialogue_text = f"{pos_tag}{dialogue_text}"
                ass_lines.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{dialogue_text}")

    os.makedirs(os.path.dirname(os.path.abspath(output_ass_path)), exist_ok=True)
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))

    print(f"ASS subtitles generated ({style_key}): {output_ass_path}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="AutoEditor Transcription & Caption Generator Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    trans_p = subparsers.add_parser("transcribe", help="Transcribe audio file to JSON with timestamps")
    trans_p.add_argument("audio", help="Path to input audio file (WAV, MP3, etc.)")
    trans_p.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium"], help="Whisper model size")
    trans_p.add_argument("--language", default=None, help="Language code (e.g. en, ur, es)")
    trans_p.add_argument("--out-json", default=None, help="Output JSON path")
    trans_p.add_argument("--out-txt", default=None, help="Output TXT path")
    trans_p.add_argument("--out-pdf", default=None, help="Output PDF path")
    trans_p.add_argument("--style", default=None, choices=list(CAPTION_STYLES.keys()), help="Also generate ASS with this style")
    trans_p.add_argument("--out-ass", default=None, help="Output ASS subtitle path")

    pdf_p = subparsers.add_parser("export-pdf", help="Export existing transcript JSON to PDF")
    pdf_p.add_argument("json_file", help="Path to transcript JSON")
    pdf_p.add_argument("output_pdf", help="Path to output PDF")

    txt_p = subparsers.add_parser("export-txt", help="Export existing transcript JSON to TXT")
    txt_p.add_argument("json_file", help="Path to transcript JSON")
    txt_p.add_argument("output_txt", help="Path to output TXT")

    ass_p = subparsers.add_parser("generate-ass", help="Generate CapCut ASS subtitles from transcript JSON")
    ass_p.add_argument("json_file", help="Path to transcript JSON")
    ass_p.add_argument("style", choices=list(CAPTION_STYLES.keys()), help="Caption style name")
    ass_p.add_argument("output_ass", help="Path to output ASS file")
    ass_p.add_argument("--width", type=int, default=1920, help="Video width")
    ass_p.add_argument("--height", type=int, default=1080, help="Video height")

    subparsers.add_parser("list-styles", help="List all available CapCut caption styles")

    args = parser.parse_args()

    if args.command == "list-styles":
        print(json.dumps(CAPTION_STYLES, indent=2))
        return

    if args.command == "transcribe":
        result = transcribe_audio(args.audio, model_size=args.model, language=args.language)
        if args.out_json:
            with open(args.out_json, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"JSON saved: {args.out_json}", file=sys.stderr)
        else:
            print(json.dumps(result, ensure_ascii=False))

        if args.out_txt:
            export_to_txt(result, args.out_txt)
        if args.out_pdf:
            export_to_pdf(result, args.out_pdf)
        if args.style and args.out_ass:
            generate_ass_subtitles(result, args.style, args.out_ass)

    elif args.command == "export-pdf":
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        export_to_pdf(data, args.output_pdf)

    elif args.command == "export-txt":
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        export_to_txt(data, args.output_txt)

    elif args.command == "generate-ass":
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        generate_ass_subtitles(data, args.style, args.output_ass, args.width, args.height)

if __name__ == "__main__":
    main()
