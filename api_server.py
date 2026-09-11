#!/usr/bin/env python3
"""
AutoEditor AI Companion Server
Runs on port 4001 (or user-defined port).
Handles:
- POST /api/transcribe (Audio to word/sentence timestamps with Whisper)
- GET  /api/styles (List 8 CapCut-style caption presets with CSS & ASS parameters)
- POST /api/generate-ass (Generate styled ASS subtitles for video render)
- GET  /api/download/pdf (Download publication-quality PDF transcript)
- GET  /api/download/txt (Download clean TXT transcript)
"""

import os
import sys

# Ensure stdout and stderr are valid streams under pythonw (where they default to None)
if sys.stdout is None or not hasattr(sys.stdout, "write"):
    try:
        sys.stdout = open(os.devnull, "w", encoding="utf-8", errors="replace")
    except Exception:
        pass

if sys.stderr is None or not hasattr(sys.stderr, "write"):
    try:
        sys.stderr = open(os.devnull, "w", encoding="utf-8", errors="replace")
    except Exception:
        pass

import json
import uuid
import shutil
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# Import transcription engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import transcribe_engine
import openrouter_client
import style_distiller
import asset_hunter
import svg_synthesizer
import qa_gateway


PORT = 4001
STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

class AutoEditorHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Headless mode: suppress or write to devnull safely
        pass

    def send_json_response(self, status_code: int, data):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(payload)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Range, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/health":
            self.send_json_response(200, {
                "ok": True,
                "service": "AutoEditor AI Engine",
                "model_cached": transcribe_engine.is_model_cached(),
                "version": "3.0",
                "ai_director_ready": True,
                "pid": os.getpid()
            })
            return

        if path == "/api/categories":
            cats = [
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
            self.send_json_response(200, cats)
            return

        if path == "/api/styles":
            category_filter = query.get("category", [None])[0]
            styles = transcribe_engine.CAPTION_STYLES
            if category_filter and category_filter.lower() != "all":
                filtered = {k: v for k, v in styles.items() if v.get("category", "").lower() == category_filter.lower()}
                self.send_json_response(200, filtered)
            else:
                self.send_json_response(200, styles)
            return

        if path == "/api/download/pdf":
            file_id = query.get("id", [None])[0]
            if not file_id:
                self.send_json_response(400, {"error": "Missing id parameter"})
                return
            pdf_path = os.path.join(STORAGE_DIR, f"{file_id}.pdf")
            if not os.path.exists(pdf_path):
                self.send_json_response(404, {"error": "PDF transcript not found"})
                return

            file_size = os.path.getsize(pdf_path)
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'attachment; filename="transcript_{file_id[:8]}.pdf"')
            self.send_header("Content-Length", str(file_size))
            self.send_header("Connection", "close")
            self.end_headers()
            with open(pdf_path, "rb") as f:
                shutil.copyfileobj(f, self.wfile)
            return

        if path == "/api/download/txt":
            file_id = query.get("id", [None])[0]
            if not file_id:
                self.send_json_response(400, {"error": "Missing id parameter"})
                return
            txt_path = os.path.join(STORAGE_DIR, f"{file_id}.txt")
            if not os.path.exists(txt_path):
                self.send_json_response(404, {"error": "TXT transcript not found"})
                return

            file_size = os.path.getsize(txt_path)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="transcript_{file_id[:8]}.txt"')
            self.send_header("Content-Length", str(file_size))
            self.send_header("Connection", "close")
            self.end_headers()
            with open(txt_path, "rb") as f:
                shutil.copyfileobj(f, self.wfile)
            return

        if path == "/api/sfx":
            sfx_manifest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage", "sfx", "manifest.json")
            if not os.path.exists(sfx_manifest):
                sfx_manifest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "sfx", "manifest.json")
            if os.path.exists(sfx_manifest):
                with open(sfx_manifest, "r", encoding="utf-8") as f:
                    self.send_json_response(200, json.load(f))
            else:
                self.send_json_response(200, {})
            return

        if path.startswith("/sfx/"):
            filename = os.path.basename(path)
            sfx_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "sfx", filename)
            if not os.path.exists(sfx_file):
                sfx_file = os.path.join(STORAGE_DIR, "sfx", filename)
            if os.path.exists(sfx_file):
                size = os.path.getsize(sfx_file)
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(size))
                self.send_header("Connection", "close")
                self.end_headers()
                with open(sfx_file, "rb") as f:
                    shutil.copyfileobj(f, self.wfile)
                return
            self.send_json_response(404, {"error": "SFX not found"})
            return

        if path == "/api/download/audio":
            file_id = query.get("id", [None])[0]
            if not file_id:
                self.send_json_response(400, {"error": "Missing id parameter"})
                return
            audio_path = os.path.join(STORAGE_DIR, f"{file_id}.wav")
            if not os.path.exists(audio_path):
                audio_path = os.path.join(STORAGE_DIR, f"{file_id}.mp3")
            if not os.path.exists(audio_path):
                self.send_json_response(404, {"error": "Audio not found"})
                return
            size = os.path.getsize(audio_path)
            self.send_response(200)
            self.send_header("Content-Type", "audio/wav")
            self.send_header("Content-Length", str(size))
            self.send_header("Connection", "close")
            self.end_headers()
            with open(audio_path, "rb") as f:
                shutil.copyfileobj(f, self.wfile)
            return

        if path == "/api/download/video":
            file_id = query.get("id", [None])[0]
            if not file_id:
                self.send_json_response(400, {"error": "Missing id parameter"})
                return
            video_path = os.path.join(STORAGE_DIR, f"{file_id}.mp4")
            if not os.path.exists(video_path):
                self.send_json_response(404, {"error": "Video not found"})
                return
            size = os.path.getsize(video_path)
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(size))
            self.send_header("Connection", "close")
            self.end_headers()
            with open(video_path, "rb") as f:
                shutil.copyfileobj(f, self.wfile)
            return

        if path == "/api/openrouter/models":
            try:
                client = openrouter_client.OpenRouterClient()
                models = client.fetch_models() if hasattr(client, 'fetch_models') else []
                is_conf = client.is_configured() if hasattr(client, 'is_configured') else False
                self.send_json_response(200, {"models": models, "configured": is_conf})
            except Exception as e:
                self.send_json_response(200, {"models": [], "configured": False, "error": str(e)})
            return

        if path == "/api/openrouter/config":
            try:
                config = openrouter_client.OpenRouterClient().load_config()
                if "api_key" in config and config["api_key"]:
                    config["api_key"] = "***" + config["api_key"][-4:]
                self.send_json_response(200, config)
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/profiles":
            try:
                profiles = style_distiller.list_profiles()
                self.send_json_response(200, profiles)
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path.startswith("/api/profiles/"):
            try:
                profile_name = path.split("/")[-1]
                profile = style_distiller.load_profile(profile_name)
                if profile:
                    self.send_json_response(200, profile)
                else:
                    self.send_json_response(404, {"error": "Profile not found"})
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/assets/manifest":
            try:
                manifest_path = os.path.join(STORAGE_DIR, "LICENSE_MANIFEST.json")
                if os.path.exists(manifest_path):
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    self.send_json_response(200, manifest)
                else:
                    self.send_json_response(200, {})
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        self.send_json_response(404, {"error": "Not Found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/transcribe":
            try:
                content_type = self.headers.get("Content-Type", "")
                content_len = int(self.headers.get("Content-Length", 0))

                req_id = str(uuid.uuid4())
                upload_audio_path = os.path.join(STORAGE_DIR, f"audio_{req_id}.wav")

                # Handle multipart or raw body or JSON with filepath
                if "multipart/form-data" in content_type:
                    # Parse multipart boundary safely
                    boundary_str = content_type.split("boundary=")[-1].split(";")[0].strip().strip('"').strip("'")
                    boundary = boundary_str.encode("utf-8")
                    body = self.rfile.read(content_len)
                    
                    parts = body.split(b"--" + boundary)
                    saved = False
                    for part in parts:
                        if b'filename="' in part:
                            header, data = part.split(b"\r\n\r\n", 1)
                            if data.endswith(b"\r\n"):
                                data = data[:-2]
                            elif data.endswith(b"--\r\n"):
                                data = data[:-4]
                            elif data.endswith(b"--"):
                                data = data[:-2]
                            with open(upload_audio_path, "wb") as f:
                                f.write(data)
                            saved = True
                            break
                    if not saved:
                        self.send_json_response(400, {"error": "No audio file part in multipart body"})
                        return
                elif "application/json" in content_type:
                    body = self.rfile.read(content_len)
                    data = json.loads(body.decode("utf-8"))
                    audio_source = data.get("filepath")
                    if not audio_source or not os.path.exists(audio_source):
                        self.send_json_response(400, {"error": "Invalid or missing filepath"})
                        return
                    upload_audio_path = audio_source
                else:
                    # Raw binary audio
                    body = self.rfile.read(content_len)
                    with open(upload_audio_path, "wb") as f:
                        f.write(body)

                # Transcribe with faster-whisper (tiered: small -> base with beam_size=5, speech_pad_ms=400)
                print(f"[{req_id}] Transcribing audio...", file=sys.stderr)
                transcript = transcribe_engine.transcribe_audio(upload_audio_path, model_size="small")

                # Generate TXT & PDF
                txt_path = os.path.join(STORAGE_DIR, f"{req_id}.txt")
                pdf_path = os.path.join(STORAGE_DIR, f"{req_id}.pdf")
                json_path = os.path.join(STORAGE_DIR, f"{req_id}.json")

                transcribe_engine.export_to_txt(transcript, txt_path)
                transcribe_engine.export_to_pdf(transcript, pdf_path)
                
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(transcript, f, indent=2, ensure_ascii=False)

                resp = {
                    "ok": True,
                    "id": req_id,
                    "transcript": transcript,
                    "text_path": txt_path,
                    "pdf_path": pdf_path,
                    "downloads": {
                        "txt": f"http://localhost:{PORT}/api/download/txt?id={req_id}",
                        "pdf": f"http://localhost:{PORT}/api/download/pdf?id={req_id}"
                    },
                    "styles": transcribe_engine.CAPTION_STYLES
                }

                self.send_json_response(200, resp)

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/vocal-remove":
            try:
                content_type = self.headers.get("Content-Type", "")
                content_len = int(self.headers.get("Content-Length", 0))
                req_id = str(uuid.uuid4())
                upload_path = os.path.join(STORAGE_DIR, f"vocal_in_{req_id}.wav")
                vocal_vol = 0.0

                if "multipart/form-data" in content_type:
                    boundary_str = content_type.split("boundary=")[-1].split(";")[0].strip().strip('"').strip("'")
                    boundary = boundary_str.encode("utf-8")
                    body = self.rfile.read(content_len)
                    parts = body.split(b"--" + boundary)
                    for part in parts:
                        if b'name="vocal_volume"' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            try:
                                vocal_vol = float(data.strip().decode())
                            except Exception:
                                pass
                        if b'filename="' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            if data.endswith(b"\r\n"):
                                data = data[:-2]
                            elif data.endswith(b"--\r\n"):
                                data = data[:-4]
                            elif data.endswith(b"--"):
                                data = data[:-2]
                            with open(upload_path, "wb") as f:
                                f.write(data)
                elif "application/json" in content_type:
                    body = self.rfile.read(content_len)
                    data = json.loads(body.decode("utf-8"))
                    upload_path = data.get("filepath", "")
                    vocal_vol = float(data.get("vocal_volume", 0.0))
                else:
                    body = self.rfile.read(content_len)
                    with open(upload_path, "wb") as f:
                        f.write(body)

                if not os.path.exists(upload_path):
                    self.send_json_response(400, {"error": "No input file found"})
                    return

                out_path = os.path.join(STORAGE_DIR, f"{req_id}.wav")
                ok = transcribe_engine.remove_vocal_from_video_or_audio(upload_path, out_path, vocal_volume=vocal_vol)
                if not ok or not os.path.exists(out_path):
                    self.send_json_response(500, {"error": "Vocal removal processing failed"})
                    return

                self.send_json_response(200, {
                    "ok": True,
                    "id": req_id,
                    "audio_url": f"http://localhost:{PORT}/api/download/audio?id={req_id}",
                    "audio_path": out_path,
                    "vocal_volume": vocal_vol
                })
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/generate-ass":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode("utf-8"))

                transcript = data.get("transcript")
                style_key = data.get("style", "hormozi_bold")
                width = data.get("width", 1920)
                height = data.get("height", 1080)
                pos_x = data.get("pos_x")
                pos_y = data.get("pos_y")
                font_scale = data.get("font_scale", 1.0)

                if not transcript:
                    self.send_json_response(400, {"error": "Missing transcript object"})
                    return

                ass_id = str(uuid.uuid4())
                ass_path = os.path.join(STORAGE_DIR, f"{ass_id}.ass")
                transcribe_engine.generate_ass_subtitles(
                    transcript, style_key, ass_path, width, height,
                    pos_x=pos_x, pos_y=pos_y, font_scale=font_scale
                )

                with open(ass_path, "r", encoding="utf-8") as f:
                    ass_content = f.read()

                resp = {
                    "ok": True,
                    "style": style_key,
                    "ass_path": ass_path,
                    "ass_content": ass_content,
                    "pos_x": pos_x,
                    "pos_y": pos_y,
                    "font_scale": font_scale
                }

                self.send_json_response(200, resp)

            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/mix-audio":
            try:
                content_type = self.headers.get("Content-Type", "")
                content_len = int(self.headers.get("Content-Length", 0))
                req_id = str(uuid.uuid4())
                upload_audio_path = os.path.join(STORAGE_DIR, f"mix_in_{req_id}.wav")
                voice_vol = 1.0
                sfx_vol = 0.5
                sfx_events = []

                if "multipart/form-data" in content_type:
                    boundary_str = content_type.split("boundary=")[-1].split(";")[0].strip().strip('"').strip("'")
                    boundary = boundary_str.encode("utf-8")
                    body = self.rfile.read(content_len)
                    parts = body.split(b"--" + boundary)
                    for part in parts:
                        if b'name="voice_volume"' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            try: voice_vol = float(data.strip().decode())
                            except Exception: pass
                        elif b'name="sfx_volume"' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            try: sfx_vol = float(data.strip().decode())
                            except Exception: pass
                        elif b'name="sfx_events"' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            try: sfx_events = json.loads(data.strip().decode())
                            except Exception: pass
                        elif b'filename="' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            if data.endswith(b"\r\n"): data = data[:-2]
                            elif data.endswith(b"--\r\n"): data = data[:-4]
                            elif data.endswith(b"--"): data = data[:-2]
                            with open(upload_audio_path, "wb") as f:
                                f.write(data)
                elif "application/json" in content_type:
                    body = self.rfile.read(content_len)
                    data = json.loads(body.decode("utf-8"))
                    upload_audio_path = data.get("filepath", "")
                    voice_vol = float(data.get("voice_volume", 1.0))
                    sfx_vol = float(data.get("sfx_volume", 0.5))
                    sfx_events = data.get("sfx_events", [])
                else:
                    body = self.rfile.read(content_len)
                    with open(upload_audio_path, "wb") as f:
                        f.write(body)

                if not os.path.exists(upload_audio_path):
                    self.send_json_response(400, {"error": "Missing input audio file"})
                    return

                # Resolve SFX files if relative/named
                sfx_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "sfx")
                resolved_events = []
                for ev in sfx_events:
                    f_name = ev.get("file", "")
                    if not os.path.isabs(f_name):
                        if not f_name.endswith(".wav"):
                            f_name = f_name + ".wav"
                        cand = os.path.join(sfx_dir, os.path.basename(f_name))
                        if os.path.exists(cand):
                            f_name = cand
                    resolved_events.append({"file": f_name, "timestamp": float(ev.get("timestamp", 0))})

                out_audio_path = os.path.join(STORAGE_DIR, f"{req_id}.wav")
                ok = transcribe_engine.mix_audio_with_sfx(
                    upload_audio_path, resolved_events, out_audio_path,
                    sfx_volume=sfx_vol, voice_volume=voice_vol
                )
                if not ok or not os.path.exists(out_audio_path):
                    self.send_json_response(500, {"error": "Audio mixing failed"})
                    return

                self.send_json_response(200, {
                    "ok": True,
                    "id": req_id,
                    "audio_path": out_audio_path,
                    "audio_url": f"http://localhost:{PORT}/api/download/audio?id={req_id}"
                })
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/burn-captions":
            try:
                content_type = self.headers.get("Content-Type", "")
                content_len = int(self.headers.get("Content-Length", 0))
                req_id = str(uuid.uuid4())
                video_path = os.path.join(STORAGE_DIR, f"burn_in_{req_id}.mp4")
                ass_path = os.path.join(STORAGE_DIR, f"burn_sub_{req_id}.ass")
                output_path = os.path.join(STORAGE_DIR, f"{req_id}.mp4")
                fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "fonts")
                if not os.path.exists(fonts_dir):
                    fonts_dir = os.path.dirname(os.path.abspath(__file__))

                if "multipart/form-data" in content_type:
                    boundary_str = content_type.split("boundary=")[-1].split(";")[0].strip().strip('"').strip("'")
                    boundary = boundary_str.encode("utf-8")
                    body = self.rfile.read(content_len)
                    parts = body.split(b"--" + boundary)
                    for part in parts:
                        if b'name="ass_content"' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            if data.endswith(b"\r\n"): data = data[:-2]
                            elif data.endswith(b"--\r\n"): data = data[:-4]
                            elif data.endswith(b"--"): data = data[:-2]
                            with open(ass_path, "wb") as f: f.write(data)
                        elif b'filename="' in part and (b'.mp4' in part or b'video' in part):
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            if data.endswith(b"\r\n"): data = data[:-2]
                            elif data.endswith(b"--\r\n"): data = data[:-4]
                            elif data.endswith(b"--"): data = data[:-2]
                            with open(video_path, "wb") as f: f.write(data)
                        elif b'filename="' in part and b'.ass' in part:
                            hdr, data = part.split(b"\r\n\r\n", 1)
                            if data.endswith(b"\r\n"): data = data[:-2]
                            elif data.endswith(b"--\r\n"): data = data[:-4]
                            elif data.endswith(b"--"): data = data[:-2]
                            with open(ass_path, "wb") as f: f.write(data)
                elif "application/json" in content_type:
                    body = self.rfile.read(content_len)
                    data = json.loads(body.decode("utf-8"))
                    video_path = data.get("video_path", video_path)
                    custom_ass = data.get("ass_path")
                    if custom_ass and os.path.exists(custom_ass):
                        ass_path = custom_ass
                    elif data.get("ass_content"):
                        with open(ass_path, "w", encoding="utf-8") as f:
                            f.write(data["ass_content"])
                    elif data.get("transcript"):
                        transcribe_engine.generate_ass_subtitles(
                            data["transcript"],
                            data.get("style", "hormozi_bold"),
                            ass_path,
                            data.get("width", 1920),
                            data.get("height", 1080),
                            pos_x=data.get("pos_x"),
                            pos_y=data.get("pos_y"),
                            font_scale=data.get("font_scale", 1.0)
                        )
                    if data.get("output_path"):
                        output_path = data.get("output_path")
                    if data.get("fonts_dir"):
                        fonts_dir = data.get("fonts_dir")

                if not os.path.exists(video_path):
                    self.send_json_response(400, {"error": "Invalid or missing video input"})
                    return
                if not os.path.exists(ass_path):
                    self.send_json_response(400, {"error": "Invalid or missing ass subtitles"})
                    return

                success = transcribe_engine.burn_captions_to_video(video_path, ass_path, output_path, fonts_dir=fonts_dir)
                if not success or not os.path.exists(output_path):
                    self.send_json_response(500, {"error": "FFmpeg caption burn failed"})
                    return

                resp = {
                    "ok": True,
                    "id": req_id,
                    "output_video": output_path,
                    "video_url": f"http://localhost:{PORT}/api/download/video?id={req_id}",
                    "ass_path": ass_path
                }
                self.send_json_response(200, resp)
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/openrouter/config":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode("utf-8"))
                openrouter_client.OpenRouterClient().save_config(data)
                self.send_json_response(200, {"ok": True})
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/assets/search":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode("utf-8"))
                query_str = data.get("query")
                hunter = asset_hunter.AssetHunter()
                results = hunter.search_openverse(query_str, media_type=data.get("media_type"), license_filter=data.get("license_filter"))
                self.send_json_response(200, results)
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/assets/generate-svg":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode("utf-8"))
                svg_content = svg_synthesizer.generate_svg_from_concept(
                    data.get("concept"),
                    color=data.get("color"),
                    style=data.get("style"),
                    width=data.get("width"),
                    height=data.get("height")
                )
                png_path = svg_synthesizer.rasterize_svg_to_png(svg_content)
                self.send_json_response(200, {"png_path": png_path})
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/qa/validate":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode("utf-8"))
                gateway = qa_gateway.QAGateway()
                report = gateway.run_full_qa(
                    data.get("timeline"),
                    word_grid=data.get("word_grid"),
                    audio_path=data.get("audio_path"),
                    assets=data.get("assets"),
                    subtitle_color=data.get("subtitle_color"),
                    video_width=data.get("video_width"),
                    video_height=data.get("video_height")
                )
                self.send_json_response(200, report.to_dict() if hasattr(report, 'to_dict') else report)
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/ai-director":
            try:
                content_type = self.headers.get("Content-Type", "")
                content_len = int(self.headers.get("Content-Length", 0))
                
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                mode_query = query_params.get("mode", [None])[0]
                
                if "multipart/form-data" in content_type:
                    self.send_json_response(400, {"error": "Use JSON body with audio_path for ai-director"})
                    return
                else:
                    body = self.rfile.read(content_len)
                    data = json.loads(body.decode("utf-8"))
                
                audio_path = data.get("audio_path")
                style_profile_name = data.get("style_profile")
                user_prompt = data.get("user_prompt")
                mode = data.get("mode", mode_query or "high")
                api_key = data.get("api_key")
                
                if not audio_path or not os.path.exists(audio_path):
                    self.send_json_response(400, {"error": "Valid audio_path required"})
                    return
                
                model_size = "base.en" if mode == "presentation" else "small"
                transcript = transcribe_engine.transcribe_audio(audio_path, model_size=model_size)
                
                chunks = transcribe_engine.semantic_chunk_text(transcript)
                
                if mode != "presentation":
                    hunter = asset_hunter.AssetHunter()
                    entities = hunter.extract_visual_entities(chunks)
                else:
                    entities = []
                
                profile = style_distiller.load_profile(style_profile_name) if hasattr(style_distiller, "load_profile") else None
                if not profile and hasattr(style_distiller, "get_factory_profile"):
                    profile = style_distiller.get_factory_profile(style_profile_name)
                    
                client = openrouter_client.OpenRouterClient()
                if api_key:
                    client.api_key = api_key
                else:
                    client.load_config()
                
                edit_plan = None
                try:
                    import time
                    start_time = time.time()
                    edit_plan = client.generate_edit_plan(chunks, profile, user_prompt)
                    if mode == "presentation" and (time.time() - start_time) > 4:
                        raise Exception("Timeout")
                except Exception as e:
                    if mode == "presentation":
                        with open(os.path.join(STORAGE_DIR, "fallback_templates", "default_edit.json"), "r", encoding="utf-8") as f:
                            edit_plan = json.load(f)
                    else:
                        raise e
                        
                if not edit_plan:
                    with open(os.path.join(STORAGE_DIR, "fallback_templates", "default_edit.json"), "r", encoding="utf-8") as f:
                        edit_plan = json.load(f)
                
                snapped_cuts = transcribe_engine.align_cuts_to_phonemes(edit_plan, transcript)
                
                sfx_events = transcribe_engine.apply_smart_sfx_pairing(snapped_cuts, profile)
                
                gateway = qa_gateway.QAGateway()
                qa_report = gateway.run_full_qa(snapped_cuts, word_grid=transcript, subtitle_color='#FFFFFF')
                
                self.send_json_response(200, {
                    "transcript": transcript,
                    "edit_plan": snapped_cuts,
                    "qa_report": qa_report.to_dict() if hasattr(qa_report, 'to_dict') else qa_report,
                    "sfx_events": sfx_events,
                    "assets": entities,
                    "cost_estimate": 0.0
                })
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                try:
                    with open(os.path.join(STORAGE_DIR, "fallback_templates", "default_edit.json"), "r", encoding="utf-8") as f:
                        fallback_plan = json.load(f)
                    self.send_json_response(200, {
                        "error_handled": str(e),
                        "edit_plan": fallback_plan
                    })
                except Exception as ex:
                    self.send_json_response(500, {"error": str(e), "fallback_error": str(ex)})
            return

        self.send_json_response(404, {"error": "Not Found"})

class AutoEditorServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def run(port=PORT, host="0.0.0.0"):
    server_address = (host, port)
    httpd = AutoEditorServer(server_address, AutoEditorHandler)
    pid = os.getpid()
    pid_path = os.path.join(STORAGE_DIR, "api_server.pid")
    try:
        with open(pid_path, "w", encoding="utf-8") as f:
            f.write(str(pid))
    except Exception:
        pass

    print(f"AutoEditor AI Server (PID {pid}) running on http://{host}:{port}", file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            if os.path.exists(pid_path):
                os.remove(pid_path)
        except Exception:
            pass
        httpd.server_close()

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    h = sys.argv[2] if len(sys.argv) > 2 else "0.0.0.0"
    run(p, h)
