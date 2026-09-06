#!/usr/bin/env python3
"""
Generates 12 high-fidelity synthesized transition sound effects (WAV) for AutoEditor.
All sounds are 44.1kHz, 16-bit PCM mono with zero external dependencies.
"""

import os
import wave
import struct
import math
import random

SAMPLE_RATE = 44100

def write_wav(path: str, samples: list, channels: int = 1):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, 'w') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        raw = bytearray()
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            val = int(clamped * 32767.0)
            raw.extend(struct.pack('<h', val))
        wav.writeframes(raw)

def gen_whoosh_fast():
    dur = 0.4
    n = int(SAMPLE_RATE * dur)
    samples = []
    random.seed(42)
    b0 = 0.0
    for i in range(n):
        t = i / n
        env = math.sin(math.pi * t) ** 2
        noise = random.uniform(-1, 1)
        b0 = 0.25 * noise + 0.75 * b0
        samples.append(b0 * env * 0.95)
    return samples

def gen_swoosh_smooth():
    dur = 0.65
    n = int(SAMPLE_RATE * dur)
    samples = []
    random.seed(101)
    b0 = b1 = 0.0
    for i in range(n):
        t = i / n
        env = math.sin(math.pi * t) ** 1.8
        freq = 200 + 1400 * (math.sin(math.pi * t) ** 1.5)
        noise = random.uniform(-1, 1)
        b0 = 0.15 * noise + 0.85 * b0
        b1 = 0.1 * b0 + 0.9 * b1
        sine = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE)) * 0.2
        val = (b1 * 0.8 + sine) * env * 0.9
        samples.append(val)
    return samples

def gen_camera_click():
    dur = 0.22
    n = int(SAMPLE_RATE * dur)
    samples = []
    random.seed(202)
    for i in range(n):
        t = i / SAMPLE_RATE
        val = 0.0
        if t < 0.03:
            env1 = math.exp(-t * 180)
            val += math.sin(2 * math.pi * 1800 * t) * env1 * 0.7
            val += random.uniform(-0.3, 0.3) * env1
        if t >= 0.07 and t < 0.18:
            t2 = t - 0.07
            env2 = math.exp(-t2 * 140)
            val += math.sin(2 * math.pi * 1200 * t2) * env2 * 0.85
            val += math.sin(2 * math.pi * 600 * t2) * env2 * 0.4
            val += random.uniform(-0.2, 0.2) * env2
        samples.append(val)
    return samples

def gen_bubble_pop():
    dur = 0.16
    n = int(SAMPLE_RATE * dur)
    samples = []
    phase = 0.0
    for i in range(n):
        t = i / n
        freq = 280 + 1600 * (t ** 2.2)
        env = (1.0 - t) * (math.sin(math.pi * min(1.0, t * 8)))
        phase += 2 * math.pi * freq / SAMPLE_RATE
        val = math.sin(phase) * env * 0.95
        samples.append(val)
    return samples

def gen_cinematic_boom():
    dur = 1.3
    n = int(SAMPLE_RATE * dur)
    samples = []
    phase = 0.0
    random.seed(303)
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 32 + 43 * math.exp(-t * 2.5)
        env = math.exp(-t * 2.2)
        phase += 2 * math.pi * freq / SAMPLE_RATE
        sub = math.sin(phase)
        sub = math.tanh(sub * 1.5) * 0.8
        if t < 0.05:
            impact_env = math.exp(-t * 80)
            sub += random.uniform(-0.4, 0.4) * impact_env
        samples.append(sub * env * 0.95)
    return samples

def gen_digital_glitch():
    dur = 0.32
    n = int(SAMPLE_RATE * dur)
    samples = []
    random.seed(404)
    step_freq = 400
    for i in range(n):
        t = i / SAMPLE_RATE
        if i % 400 == 0:
            step_freq = random.choice([600, 900, 1400, 1800, 2400, 800, 3200])
        env = math.sin(math.pi * (i / n))
        square = 1.0 if math.sin(2 * math.pi * step_freq * t) > 0 else -1.0
        val = square * env * 0.45 + random.uniform(-0.2, 0.2) * env
        samples.append(val)
    return samples

def gen_gentle_chime():
    dur = 0.9
    n = int(SAMPLE_RATE * dur)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 3.5)
        h1 = math.sin(2 * math.pi * 880 * t) * 0.5
        h2 = math.sin(2 * math.pi * 1760 * t) * 0.3
        h3 = math.sin(2 * math.pi * 2640 * t) * 0.15
        h4 = math.sin(2 * math.pi * 3520 * t) * 0.08
        val = (h1 + h2 + h3 + h4) * env
        samples.append(val)
    return samples

def gen_paper_turn():
    dur = 0.38
    n = int(SAMPLE_RATE * dur)
    samples = []
    random.seed(505)
    b0 = 0.0
    for i in range(n):
        t = i / n
        env = (math.sin(math.pi * t) ** 2) * (1 + 0.3 * math.sin(30 * math.pi * t))
        noise = random.uniform(-1, 1)
        b0 = 0.3 * noise + 0.7 * b0
        samples.append(b0 * env * 0.8)
    return samples

def gen_snappy_switch():
    dur = 0.12
    n = int(SAMPLE_RATE * dur)
    samples = []
    random.seed(606)
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 220)
        click = math.sin(2 * math.pi * 1450 * t) * env * 0.75 + random.uniform(-0.25, 0.25) * env
        samples.append(click)
    return samples

def gen_impact_punch():
    dur = 0.45
    n = int(SAMPLE_RATE * dur)
    samples = []
    phase = 0.0
    random.seed(707)
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 45 + 180 * math.exp(-t * 25)
        phase += 2 * math.pi * freq / SAMPLE_RATE
        env = math.exp(-t * 7.0)
        body = math.sin(phase) * env * 0.75
        attack = random.uniform(-0.4, 0.4) * math.exp(-t * 120) if t < 0.04 else 0.0
        samples.append((body + attack) * 0.95)
    return samples

def gen_cinematic_riser():
    dur = 0.95
    n = int(SAMPLE_RATE * dur)
    samples = []
    phase = 0.0
    for i in range(n):
        t = i / n
        freq = 110 * (4.5 ** t)
        phase += 2 * math.pi * freq / SAMPLE_RATE
        env = (t ** 1.8) * (1.0 + 0.15 * math.sin(20 * math.pi * t))
        val = math.sin(phase) * env * 0.8
        samples.append(val)
    return samples

def gen_short_woosh():
    dur = 0.25
    n = int(SAMPLE_RATE * dur)
    samples = []
    random.seed(808)
    b0 = 0.0
    for i in range(n):
        t = i / n
        env = math.sin(math.pi * t) ** 2.5
        freq = 400 + 2600 * math.sin(math.pi * t)
        noise = random.uniform(-1, 1)
        b0 = 0.25 * noise + 0.75 * b0
        samples.append(b0 * env * 0.9)
    return samples

SOUND_EFFECTS = {
    "whoosh_fast": {"name": "Fast Whip Whoosh", "generator": gen_whoosh_fast, "desc": "High energy whoosh for fast wipes and cuts", "category": "motion"},
    "swoosh_smooth": {"name": "Cinematic Swoosh", "generator": gen_swoosh_smooth, "desc": "Smooth air swoosh for slides and crossfades", "category": "motion"},
    "camera_click": {"name": "Camera Shutter & Click", "generator": gen_camera_click, "desc": "Snappy camera shutter for photo cuts and zooms", "category": "foley"},
    "bubble_pop": {"name": "Bubble Pop", "generator": gen_bubble_pop, "desc": "Playful pop for bouncy and viral short cuts", "category": "retro"},
    "cinematic_boom": {"name": "Cinematic Sub Boom", "generator": gen_cinematic_boom, "desc": "Deep impact hit for fade to black and dramatic cuts", "category": "impact"},
    "digital_glitch": {"name": "Digital Glitch", "generator": gen_digital_glitch, "desc": "Electronic riser for cyber and fast transitions", "category": "electronic"},
    "gentle_chime": {"name": "Gentle Bell Chime", "generator": gen_gentle_chime, "desc": "Sweet chime for elegant fades and corporate videos", "category": "ambient"},
    "paper_turn": {"name": "Paper Turn", "generator": gen_paper_turn, "desc": "Crisp paper flip for documentary and story cuts", "category": "foley"},
    "snappy_switch": {"name": "Tactile Click", "generator": gen_snappy_switch, "desc": "Sharp tactile click for instant cuts", "category": "foley"},
    "impact_punch": {"name": "Punch Impact", "generator": gen_impact_punch, "desc": "Solid modern punch impact", "category": "impact"},
    "cinematic_riser": {"name": "Tension Riser", "generator": gen_cinematic_riser, "desc": "Atmospheric upward swell riser", "category": "motion"},
    "short_woosh": {"name": "Snappy Micro-Woosh", "generator": gen_short_woosh, "desc": "Ultra-short woosh for fast cuts", "category": "motion"},
}

def generate_all(out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    metadata = {}
    for key, info in SOUND_EFFECTS.items():
        filename = f"{key}.wav"
        path = os.path.join(out_dir, filename)
        samples = info["generator"]()
        write_wav(path, samples)
        metadata[key] = {
            "id": key,
            "name": info["name"],
            "filename": filename,
            "url": f"/sfx/{filename}",
            "description": info["desc"],
            "category": info["category"]
        }
        print(f"Generated {filename} ({len(samples)} samples)")
    
    manifest_path = os.path.join(out_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        import json
        json.dump(metadata, f, indent=2)
    print(f"SFX manifest saved: {manifest_path}")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "out/sfx"
    generate_all(target)
