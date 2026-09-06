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
import json
import uuid
import shutil
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# Import transcription engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import transcribe_engine

PORT = 4001
STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

class AutoEditorHandler(BaseHTTPRequestHandler):
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
                "version": "2.0",
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
                    # Parse multipart boundary
                    boundary = content_type.split("boundary=")[-1].strip().encode()
                    body = self.rfile.read(content_len)
                    
                    parts = body.split(b"--" + boundary)
                    saved = False
                    for part in parts:
                        if b'filename="' in part:
                            header, data = part.split(b"\r\n\r\n", 1)
                            data = data.rstrip(b"\r\n")
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

        if path == "/api/generate-ass":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode("utf-8"))

                transcript = data.get("transcript")
                style_key = data.get("style", "hormozi_bold")
                width = data.get("width", 1920)
                height = data.get("height", 1080)

                if not transcript:
                    self.send_json_response(400, {"error": "Missing transcript object"})
                    return

                ass_id = str(uuid.uuid4())
                ass_path = os.path.join(STORAGE_DIR, f"{ass_id}.ass")
                transcribe_engine.generate_ass_subtitles(transcript, style_key, ass_path, width, height)

                with open(ass_path, "r", encoding="utf-8") as f:
                    ass_content = f.read()

                resp = {
                    "ok": True,
                    "style": style_key,
                    "ass_path": ass_path,
                    "ass_content": ass_content
                }

                self.send_json_response(200, resp)

            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        if path == "/api/burn-captions":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                data = json.loads(body.decode("utf-8"))

                video_path = data.get("video_path")
                ass_path = data.get("ass_path")
                output_path = data.get("output_path")
                fonts_dir = data.get("fonts_dir")

                if not video_path or not os.path.exists(video_path):
                    self.send_json_response(400, {"error": "Invalid or missing video_path"})
                    return
                if not ass_path or not os.path.exists(ass_path):
                    self.send_json_response(400, {"error": "Invalid or missing ass_path"})
                    return
                if not output_path:
                    output_path = os.path.join(STORAGE_DIR, f"burned_{uuid.uuid4().hex[:8]}.mp4")

                success = transcribe_engine.burn_captions_to_video(video_path, ass_path, output_path, fonts_dir=fonts_dir)
                if not success:
                    self.send_json_response(500, {"error": "FFmpeg caption burn failed"})
                    return

                resp = {
                    "ok": True,
                    "output_video": output_path,
                    "ass_path": ass_path
                }
                self.send_json_response(200, resp)
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
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
