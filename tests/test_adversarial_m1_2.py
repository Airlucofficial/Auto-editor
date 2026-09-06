#!/usr/bin/env python3
"""
Adversarial Stress Test Suite for Milestone 1 (challenger_m1_2)
Focus Areas:
1. format_second_timestamp boundary conditions and mathematical invariants
2. transcribe_audio word alignment, monotonicity, and caching latency speedup
3. TXT export output parsing and strict regex compliance
4. PDF export binary %PDF structure and ReportLab badge table cells
"""

import os
import sys
import re
import json
import time
import math
import zlib
import base64
import random
from datetime import datetime

# Configure UTF-8 for Windows console
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Setup project path
PROJECT_DIR = r"d:\AutoEditor"
sys.path.insert(0, PROJECT_DIR)

import transcribe_engine

# Output directory for test artifacts
STORAGE_DIR = os.path.join(PROJECT_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

class EmpiricalReport:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def record(self, test_id: str, name: str, passed: bool, details: str = "", metrics: dict = None):
        if passed:
            self.passed += 1
            status = "PASS"
        else:
            self.failed += 1
            status = "FAIL"
        
        entry = {
            "id": test_id,
            "name": name,
            "status": status,
            "details": details,
            "metrics": metrics or {}
        }
        self.results.append(entry)
        symbol = "✓" if passed else "✗"
        print(f"  [{symbol}] {test_id}: {name} - {status}")
        if details:
            print(f"      {details}")
        if metrics:
            print(f"      Metrics: {metrics}")

report = EmpiricalReport()

# =====================================================================
# SUITE 1: format_second_timestamp BOUNDARY CONDITIONS & INVARIANTS
# =====================================================================
def run_suite_1():
    print("\n" + "=" * 70)
    print(" SUITE 1: format_second_timestamp BOUNDARY CONDITIONS & INVARIANTS")
    print("=" * 70)

    # 1.1 Mandatory Boundary Inputs from Dispatch
    # Boundaries: 0.000, 0.049, 0.050, 0.099, 3.35, 59.99, 3600.5
    cases = [
        (0.000, 0.049, "0.0s \u2013 0.0s"),
        (0.049, 0.050, "0.0s \u2013 0.1s"),
        (0.050, 0.099, "0.1s \u2013 0.1s"),
        (0.099, 3.350, "0.1s \u2013 3.4s"),
        (3.350, 59.990, "3.4s \u2013 60.0s"),
        (59.990, 3600.500, "60.0s \u2013 3600.5s"),
    ]

    for start, end, expected in cases:
        out = transcribe_engine.format_second_timestamp(start, end)
        ok = (out == expected)
        # Check that separator is strictly en-dash (\u2013, ord 8211)
        sep_ok = "\u2013" in out and "-" not in out.replace("\u2013", "")
        report.record(
            f"T1.1_BOUNDARY_({start},{end})",
            f"format_second_timestamp({start}, {end})",
            ok and sep_ok,
            f"Got: '{out}', Expected: '{expected}', EnDashCodepoint: {ord(out.split()[1]) == 8211}"
        )

    # 1.2 Individual boundary point behavior
    individual_points = [
        (0.000, "0.0s"),
        (0.049, "0.0s"),
        (0.050, "0.1s"),
        (0.099, "0.1s"),
        (3.350, "3.4s"),
        (59.990, "60.0s"),
        (3600.500, "3600.5s"),
    ]
    for pt, expected_fmt in individual_points:
        out = transcribe_engine.format_second_timestamp(pt, pt)
        expected = f"{expected_fmt} \u2013 {expected_fmt}"
        report.record(
            f"T1.2_POINT_{pt}",
            f"format_second_timestamp({pt}, {pt}) == '{expected}'",
            out == expected,
            f"Got: '{out}'"
        )

    # 1.3 Negative inputs (Clamping invariant)
    neg_out1 = transcribe_engine.format_second_timestamp(-5.0, 3.0)
    report.record(
        "T1.3_NEGATIVE_START",
        "Clamps negative start to 0.0s",
        neg_out1 == "0.0s \u2013 3.0s",
        f"Got: '{neg_out1}'"
    )

    neg_out2 = transcribe_engine.format_second_timestamp(-10.5, -2.1)
    report.record(
        "T1.3_NEGATIVE_BOTH",
        "Clamps both negative inputs to 0.0s – 0.0s",
        neg_out2 == "0.0s \u2013 0.0s",
        f"Got: '{neg_out2}'"
    )

    # 1.4 Inverted timestamps (start > end protection)
    inv_out = transcribe_engine.format_second_timestamp(15.4, 4.2)
    report.record(
        "T1.4_INVERTED_TIMESTAMPS",
        "Prevents start > end by clamping end to max(start, end)",
        inv_out == "15.4s \u2013 15.4s",
        f"Got: '{inv_out}'"
    )

    # 1.5 Very large timestamps (Hour+ scale)
    large_out = transcribe_engine.format_second_timestamp(86400.0, 86405.5)
    report.record(
        "T1.5_LARGE_TIMESTAMP",
        "Correctly formats large timestamps > 24h",
        large_out == "86400.0s \u2013 86405.5s",
        f"Got: '{large_out}'"
    )

    # 1.6 Fuzz testing with 1,000 random float pairs
    fuzz_passed = True
    fuzz_errors = []
    regex_pattern = re.compile(r"^\d+\.\d+s \u2013 \d+\.\d+s$")

    random.seed(42)
    for _ in range(1000):
        s = random.uniform(-100.0, 10000.0)
        e = random.uniform(-100.0, 10000.0)
        res = transcribe_engine.format_second_timestamp(s, e)
        
        if not regex_pattern.match(res):
            fuzz_passed = False
            fuzz_errors.append(f"Regex fail: ({s}, {e}) -> {res}")
            break
        
        # Parse output floats back and assert mathematical invariant
        parts = res.replace("s", "").split(" \u2013 ")
        parsed_s = float(parts[0])
        parsed_e = float(parts[1])
        if parsed_s < 0.0 or parsed_e < parsed_s:
            fuzz_passed = False
            fuzz_errors.append(f"Invariant fail: parsed ({parsed_s}, {parsed_e}) from ({s}, {e})")
            break

    report.record(
        "T1.6_FUZZ_1000_PAIRS",
        "1,000 random float pairs satisfy regex and monotonicity invariants",
        fuzz_passed,
        f"Errors: {fuzz_errors[:3]}" if fuzz_errors else "All 1,000 satisfied invariants"
    )


# =====================================================================
# SUITE 2: transcribe_audio WORD ALIGNMENT & CACHING LATENCY SPEEDUP
# =====================================================================
def run_suite_2():
    print("\n" + "=" * 70)
    print(" SUITE 2: transcribe_audio WORD ALIGNMENT & CACHING LATENCY SPEEDUP")
    print("=" * 70)

    sample_wav = os.path.join(PROJECT_DIR, "test_sample.wav")
    if not os.path.exists(sample_wav):
        report.record("T2.0_WAV_EXISTS", "Sample WAV file exists", False, f"Missing: {sample_wav}")
        return None

    report.record("T2.0_WAV_EXISTS", "Sample WAV file exists", True, f"Found: {sample_wav}")

    # 2.1 Model Loader Caching Speedup (get_model)
    # Clear cache first to measure pure cold vs warm
    transcribe_engine._MODEL_CACHE.clear()

    t0 = time.perf_counter()
    model_cold = transcribe_engine.get_model("base")
    t_cold_model = time.perf_counter() - t0

    t0 = time.perf_counter()
    model_warm = transcribe_engine.get_model("base")
    t_warm_model = time.perf_counter() - t0

    speedup_model = t_cold_model / max(t_warm_model, 1e-6)
    report.record(
        "T2.1_MODEL_CACHE_SPEEDUP",
        "get_model in-memory caching latency speedup",
        t_warm_model < 0.01 and speedup_model > 50,
        f"Cold: {t_cold_model*1000:.2f}ms, Warm: {t_warm_model*1000:.4f}ms, Speedup: {speedup_model:.1f}x",
        {"cold_ms": round(t_cold_model*1000, 2), "warm_ms": round(t_warm_model*1000, 4), "speedup": round(speedup_model, 1)}
    )

    # 2.2 Cold vs Warm Full Transcription (transcribe_audio)
    # Clear cache again for fair cold transcription benchmark
    transcribe_engine._MODEL_CACHE.clear()

    print("  [..] Executing Cold Transcription (Invocation 1)...")
    t0 = time.perf_counter()
    transcript_cold = transcribe_engine.transcribe_audio(sample_wav, model_size="base")
    t_cold_trans = time.perf_counter() - t0

    print("  [..] Executing Warm Transcription (Invocation 2)...")
    t0 = time.perf_counter()
    transcript_warm = transcribe_engine.transcribe_audio(sample_wav, model_size="base")
    t_warm_trans = time.perf_counter() - t0

    speedup_trans = t_cold_trans / max(t_warm_trans, 1e-6)
    report.record(
        "T2.2_TRANSCRIPTION_SPEEDUP",
        "transcribe_audio cold vs warm latency reduction",
        t_warm_trans <= t_cold_trans,
        f"Cold: {t_cold_trans:.2f}s, Warm: {t_warm_trans:.2f}s, Speedup: {speedup_trans:.2f}x",
        {"cold_s": round(t_cold_trans, 2), "warm_s": round(t_warm_trans, 2), "speedup": round(speedup_trans, 2)}
    )

    # 2.3 Transcript Data Integrity
    has_text = len(transcript_warm.get("text", "").strip()) > 0
    has_segments = len(transcript_warm.get("segments", [])) > 0
    total_words = transcript_warm.get("total_words", 0)
    duration = transcript_warm.get("duration", 0.0)

    report.record(
        "T2.3_TRANSCRIPT_INTEGRITY",
        "Transcript has non-empty text, segments, duration, and word count",
        has_text and has_segments and total_words > 0 and duration > 0.0,
        f"Segments: {len(transcript_warm.get('segments', []))}, Total Words: {total_words}, Duration: {duration}s"
    )

    # 2.4 Word Alignment & Monotonicity Verification
    words_passed = True
    word_errors = []
    accumulated_words = 0

    prev_seg_end = 0.0
    for s_idx, seg in enumerate(transcript_warm.get("segments", [])):
        seg_start = seg.get("start", 0.0)
        seg_end = seg.get("end", 0.0)

        # Monotonicity of segments
        if seg_start < prev_seg_end - 0.5: # allow small overlap
            word_errors.append(f"Segment {s_idx} start {seg_start} before prev end {prev_seg_end}")
        prev_seg_end = seg_end

        if seg_end < seg_start:
            word_errors.append(f"Segment {s_idx} end {seg_end} < start {seg_start}")

        words = seg.get("words", [])
        if not words:
            word_errors.append(f"Segment {s_idx} has empty words array")

        prev_word_start = 0.0
        for w_idx, w in enumerate(words):
            accumulated_words += 1
            w_text = w.get("word", "")
            w_start = w.get("start", 0.0)
            w_end = w.get("end", 0.0)
            w_prob = w.get("probability", 0.0)

            # Assert non-empty text
            if not w_text or not w_text.strip():
                word_errors.append(f"Seg {s_idx} Word {w_idx} text is empty")

            # Assert word start <= end
            if w_end < w_start:
                word_errors.append(f"Seg {s_idx} Word '{w_text}' end ({w_end}) < start ({w_start})")

            # Assert word start sequence monotonicity
            if w_start < prev_word_start:
                word_errors.append(f"Seg {s_idx} Word '{w_text}' start {w_start} < prev word start {prev_word_start}")
            prev_word_start = w_start

            # Assert probability bounded [0, 1]
            if not (0.0 <= w_prob <= 1.0):
                word_errors.append(f"Seg {s_idx} Word '{w_text}' probability {w_prob} out of bounds")

    report.record(
        "T2.4_WORD_ALIGNMENT_MONOTONICITY",
        "Every word has valid timings, non-empty text, start<=end, and sequence monotonicity",
        len(word_errors) == 0 and accumulated_words == total_words,
        f"Validated {accumulated_words} words. Errors: {word_errors[:3]}",
        {"words_checked": accumulated_words, "error_count": len(word_errors)}
    )

    # 2.5 Tiered Loader Fallback Safety (Request 'small' with incomplete cache)
    transcribe_engine._MODEL_CACHE.clear()
    t0 = time.perf_counter()
    model_fallback = transcribe_engine.get_model("small")
    t_fallback = time.perf_counter() - t0

    report.record(
        "T2.5_TIERED_LOADER_FALLBACK",
        "Tiered loader safely falls back to 'base' when 'small' is incomplete without crash",
        model_fallback is not None and ("small", "cpu", "int8") in transcribe_engine._MODEL_CACHE,
        f"Fallback resolved in {t_fallback*1000:.2f}ms, model active: {model_fallback is not None}"
    )

    return transcript_warm


# =====================================================================
# SUITE 3: TXT EXPORT STRICT REGEX ASSERTIONS & PARSING
# =====================================================================
def run_suite_3(transcript):
    print("\n" + "=" * 70)
    print(" SUITE 3: TXT EXPORT STRICT REGEX ASSERTIONS & PARSING")
    print("=" * 70)

    if not transcript:
        report.record("T3.0_SKIP", "Skipping TXT suite due to missing transcript", False)
        return

    txt_path = os.path.join(STORAGE_DIR, "adversarial_test.txt")
    transcribe_engine.export_to_txt(transcript, txt_path)

    report.record("T3.1_TXT_EXISTS", "TXT export file successfully created", os.path.exists(txt_path))

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Regex required by Dispatch: strictly assert all timestamps match regex ^\[\d+\.\d+s – \d+\.\d+s\]
    # Note: \u2013 is unicode en-dash
    regex_dispatch = re.compile(r"^\[\d+\.\d+s \u2013 \d+\.\d+s\]")
    regex_dialogue = re.compile(r"^\[(\d+\.\d+)s \u2013 (\d+\.\d+)s\] Speaker:\s*(.+)$")

    timestamp_lines = []
    dialogue_matches = 0
    dialogue_errors = []

    for idx, line in enumerate(lines):
        trimmed = line.strip()
        if trimmed.startswith("["):
            timestamp_lines.append((idx, trimmed))
            if regex_dispatch.match(trimmed):
                match = regex_dialogue.match(trimmed)
                if match:
                    dialogue_matches += 1
                    s_str, e_str, text = match.groups()
                    s_val = float(s_str)
                    e_val = float(e_str)
                    if s_val > e_val:
                        dialogue_errors.append(f"Line {idx}: start {s_val} > end {e_val}")
                    if not text.strip():
                        dialogue_errors.append(f"Line {idx}: empty dialogue text")
                else:
                    dialogue_errors.append(f"Line {idx}: matched timestamp regex but not full dialogue format: '{trimmed}'")
            else:
                dialogue_errors.append(f"Line {idx}: timestamp line failed regex ^\\[\\d+\\.\\d+s \u2013 \\d+\\.\\d+s\\]: '{trimmed}'")

    num_segments = len(transcript.get("segments", []))
    report.record(
        "T3.2_TXT_TIMESTAMP_REGEX",
        "Strictly assert 100% of dialogue timestamps match regex ^\\[\\d+\\.\\d+s \u2013 \\d+\\.\\d+s\\]",
        len(dialogue_errors) == 0 and dialogue_matches == num_segments,
        f"Matched: {dialogue_matches}/{num_segments} segments. Errors: {dialogue_errors}",
        {"dialogue_matches": dialogue_matches, "expected_segments": num_segments}
    )

    # 3.3 Verify NO legacy formatting appears anywhere in the TXT
    raw_content = "".join(lines)
    has_legacy_ms = bool(re.search(r"\[\d{2}:\d{2}\.\d{3}", raw_content))
    has_legacy_arrow = bool(re.search(r"-->\s*\d{2}:\d{2}", raw_content))
    report.record(
        "T3.3_NO_LEGACY_TIMESTAMPS",
        "TXT contains no legacy MM:SS.mmm or arrow timestamps in dialogue lines",
        not has_legacy_ms and not has_legacy_arrow,
        f"Legacy MS matches: {has_legacy_ms}, Legacy arrow matches: {has_legacy_arrow}"
    )

    # 3.4 Verify Header & Full Script Integrity
    has_header = "AUDIO TRANSCRIPT:" in raw_content
    has_duration = "Total Duration:" in raw_content
    has_timeline = "Timeline: 0.0s -->" in raw_content
    has_script = "--- [ FULL TEXT SCRIPT ] ---" in raw_content

    report.record(
        "T3.4_HEADER_AND_SCRIPT_SECTIONS",
        "TXT contains required header metadata and full text script sections",
        has_header and has_duration and has_timeline and has_script,
        f"Header: {has_header}, Duration: {has_duration}, Timeline: {has_timeline}, Script: {has_script}"
    )

    # 3.5 Adversarial Synthetic TXT (100 synthetic segments with boundary timestamps)
    synthetic_transcript = {
        "audio_file": "adversarial_synth.wav",
        "duration": 3600.5,
        "total_words": 100,
        "language": "en",
        "text": "Adversarial synthetic script test with 100 boundary segments.",
        "segments": [
            {
                "id": i,
                "start": round(i * 36.005, 3),
                "end": round((i + 1) * 36.005, 3),
                "timestamp": transcribe_engine.format_second_timestamp(i * 36.005, (i + 1) * 36.005),
                "text": f"Boundary dialogue segment index {i} with special chars: <test> & 'quotes'."
            }
            for i in range(100)
        ]
    }
    synth_txt_path = os.path.join(STORAGE_DIR, "adversarial_synth.txt")
    transcribe_engine.export_to_txt(synthetic_transcript, synth_txt_path)

    with open(synth_txt_path, "r", encoding="utf-8") as f:
        synth_lines = f.readlines()

    synth_matches = sum(1 for line in synth_lines if regex_dialogue.match(line.strip()))
    report.record(
        "T3.5_SYNTHETIC_100_SEGMENTS",
        "100 synthetic boundary segments exported to TXT with 100% regex compliance",
        synth_matches == 100,
        f"Matched {synth_matches}/100 dialogue lines in synthetic export",
        {"matched": synth_matches, "expected": 100}
    )


# =====================================================================
# SUITE 4: PDF EXPORT BINARY STRUCTURE & REPORTLAB BADGES
# =====================================================================
def run_suite_4(transcript):
    print("\n" + "=" * 70)
    print(" SUITE 4: PDF EXPORT BINARY STRUCTURE & REPORTLAB BADGES")
    print("=" * 70)

    if not transcript:
        report.record("T4.0_SKIP", "Skipping PDF suite due to missing transcript", False)
        return

    pdf_path = os.path.join(STORAGE_DIR, "adversarial_test.pdf")
    transcribe_engine.export_to_pdf(transcript, pdf_path)

    report.record("T4.1_PDF_EXISTS", "PDF export file successfully created", os.path.exists(pdf_path))

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # 4.2 Binary %PDF Header & %%EOF Trailer Assertions
    starts_pdf = pdf_bytes.startswith(b"%PDF-1.")
    ends_eof = b"%%EOF" in pdf_bytes
    has_size = len(pdf_bytes) > 1000

    report.record(
        "T4.2_PDF_BINARY_STRUCTURE",
        "PDF file satisfies binary %PDF-1.x magic header, %%EOF trailer, and non-trivial size",
        starts_pdf and ends_eof and has_size,
        f"Header: {pdf_bytes[:8]}, Has %%EOF: {ends_eof}, FileSize: {len(pdf_bytes)} bytes"
    )

    # 4.3 ReportLab Generator Verification
    is_reportlab = b"ReportLab Generated PDF document" in pdf_bytes
    report.record(
        "T4.3_REPORTLAB_PRODUCER",
        "PDF confirmed produced by ReportLab document template engine",
        is_reportlab,
        "Found ReportLab header comment in binary document stream"
    )

    # 4.4 Stream Decompression & RoundedBadge Operator Inspection
    # Decompress ASCII85 + FlateDecode streams
    decompressed_streams = []
    for m in re.finditer(rb"stream[\r\n]+(.*?)endstream", pdf_bytes, re.DOTALL):
        raw_stream = m.group(1).strip()
        data = raw_stream
        if raw_stream.endswith(b"~>"):
            try:
                data = base64.a85decode(raw_stream, adobe=True)
            except Exception:
                pass
        try:
            decomp = zlib.decompress(data)
            decompressed_streams.append(decomp.decode("latin1", errors="replace"))
        except Exception:
            decompressed_streams.append(data.decode("latin1", errors="replace"))

    full_pdf_text = " ".join(decompressed_streams)

    # Inspect ReportLab RoundedBadge Operators:
    # 1. Fill color #EEF2FF: .933333 .94902 1 rg
    has_bg_color = ".933333 .94902 1 rg" in full_pdf_text
    # 2. Stroke color #C7D2FE: .780392 .823529 .996078 RG
    has_stroke_color = ".780392 .823529 .996078 RG" in full_pdf_text
    # 3. Text color #1E40AF: .117647 .25098 .686275 rg
    has_text_color = ".117647 .25098 .686275 rg" in full_pdf_text
    # 4. Bold font: /F2 or Helvetica-Bold in font dictionaries
    has_bold_font = b"/BaseFont /Helvetica-Bold" in pdf_bytes
    # 5. Timestamp text drawn with en-dash (\226 in WinAnsi)
    has_badge_timestamp = ("\\226" in full_pdf_text or "\u2013" in full_pdf_text) and "0.0s" in full_pdf_text

    report.record(
        "T4.4_REPORTLAB_ROUNDED_BADGE",
        "RoundedBadge Flowable verified: #EEF2FF fill, #C7D2FE border, #1E40AF text, bold font, en-dash text",
        has_bg_color and has_stroke_color and has_text_color and has_bold_font and has_badge_timestamp,
        f"FillColor: {has_bg_color}, StrokeColor: {has_stroke_color}, TextColor: {has_text_color}, BoldFont: {has_bold_font}, BadgeText: {has_badge_timestamp}"
    )

    # 4.5 NumberedCanvas Pagination and Footer Assertions
    has_footer_title = "TryAIToday AutoEditor" in full_pdf_text
    has_page_num = "Page 1 of 1" in full_pdf_text or "Page 1 of" in full_pdf_text
    report.record(
        "T4.5_NUMBERED_CANVAS_FOOTER",
        "NumberedCanvas two-pass total page count and footer branding verified",
        has_footer_title and has_page_num,
        f"Branding: {has_footer_title}, Pagination: {has_page_num}"
    )

    # 4.6 Multi-Page Pagination Stress Test (60 segments)
    multi_page_transcript = {
        "audio_file": "multipage_stress.wav",
        "duration": 600.0,
        "total_words": 600,
        "language": "en",
        "text": "Multi-page document stress test with 60 dialogue segments.",
        "segments": [
            {
                "id": i,
                "start": round(i * 10.0, 3),
                "end": round((i + 1) * 10.0, 3),
                "timestamp": transcribe_engine.format_second_timestamp(i * 10.0, (i + 1) * 10.0),
                "text": f"This is segment number {i} with sufficient text content to cause line wrapping and multi-page layout."
            }
            for i in range(60)
        ]
    }
    multi_pdf_path = os.path.join(STORAGE_DIR, "adversarial_multipage.pdf")
    transcribe_engine.export_to_pdf(multi_page_transcript, multi_pdf_path)

    with open(multi_pdf_path, "rb") as f:
        multi_bytes = f.read()

    # Count pages in PDF (Count /Type /Page occurrences)
    page_count = len(re.findall(rb"/Type\s*/Page\b", multi_bytes)) - len(re.findall(rb"/Type\s*/Pages\b", multi_bytes))
    report.record(
        "T4.6_MULTIPLE_PAGE_LAYOUT",
        "60-segment transcript paginates cleanly into multiple pages with persistent badges",
        page_count >= 2 and os.path.getsize(multi_pdf_path) > 3000,
        f"Generated {page_count} pages, size: {os.path.getsize(multi_pdf_path)} bytes",
        {"pages": page_count}
    )

    # 4.7 XML & HTML Character Sanitization in ReportLab Paragraph
    xml_transcript = {
        "audio_file": "xml_escape_test.wav",
        "duration": 15.0,
        "total_words": 15,
        "language": "en",
        "text": "Dialogue with characters: Tom & Jerry, 5 < 10, 10 > 5, and 'quotes'.",
        "segments": [
            {
                "id": 0,
                "start": 0.0,
                "end": 5.0,
                "timestamp": "0.0s \u2013 5.0s",
                "text": "Testing unescaped ampersand: Tom & Jerry and angle brackets: a < b and c > d."
            }
        ]
    }
    xml_pdf_path = os.path.join(STORAGE_DIR, "adversarial_xml.pdf")
    xml_export_ok = True
    try:
        transcribe_engine.export_to_pdf(xml_transcript, xml_pdf_path)
    except Exception as e:
        xml_export_ok = False
        print(f"      XML export error: {e}")

    report.record(
        "T4.7_XML_CHARACTER_RESILIENCE",
        "ReportLab exports text containing &, <, > without crashing",
        xml_export_ok and os.path.exists(xml_pdf_path),
        f"File created: {os.path.exists(xml_pdf_path)}"
    )


# =====================================================================
# MAIN RUNNER
# =====================================================================
def main():
    print("=" * 70)
    print(" EMPIRICAL ADVERSARIAL CHALLENGER SUITE (M1.2)")
    print(f" Time: {datetime.now().isoformat()}")
    print("=" * 70)

    run_suite_1()
    transcript = run_suite_2()
    run_suite_3(transcript)
    run_suite_4(transcript)

    print("\n" + "=" * 70)
    print(f" FINAL RESULTS: {report.passed} PASSED, {report.failed} FAILED")
    print("=" * 70)

    # Save empirical results to JSON for handoff referencing
    results_json = os.path.join(STORAGE_DIR, "challenger_m1_2_results.json")
    with open(results_json, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "passed": report.passed,
            "failed": report.failed,
            "results": report.results
        }, f, indent=2)
    print(f"Empirical data written to: {results_json}")

    return 0 if report.failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
