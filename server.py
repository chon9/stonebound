"""Local-only HTTP interface. Run with .venv/Scripts/python.exe server.py."""
import argparse
import json
import mimetypes
import os
import re
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from stonebound.app import Stonebound
from stonebound.engine import ROOT, RUNTIME

WEB = ROOT / "web"


def make_handler(app):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            if args and str(args[0]).startswith("POST"):
                super().log_message(fmt, *args)

        def json(self, payload, status=200):
            data = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if not self._valid_host():
                return self.json({"error": "Invalid host."}, 403)
            path = urlparse(self.path).path
            if path == "/api/state":
                return self.json(app.state())
            if path.startswith("/api/"):
                return self.json({"error": "Unknown endpoint."}, 404)
            target = (WEB / ("index.html" if path == "/" else path.lstrip("/"))).resolve()
            if not target.is_relative_to(WEB) or not target.is_file():
                return self.send_error(404)
            data = target.read_bytes()
            total = len(data)
            start, end = 0, total - 1
            audio = target.suffix.lower() == '.mp3'
            byte_range = self.headers.get('Range') if audio else None
            if byte_range:
                match = re.fullmatch(r'bytes=(\d*)-(\d*)', byte_range)
                valid = bool(match and any(match.groups()))
                if valid:
                    first, last = match.groups()
                    if first:
                        start = int(first)
                        end = min(int(last), total-1) if last else total-1
                    else:
                        start = max(0, total-int(last))
                    valid = 0 <= start <= end < total
                if not valid:
                    self.send_response(416)
                    self.send_header('Content-Range', f'bytes */{total}')
                    self.send_header('Content-Length', '0')
                    self.end_headers()
                    return
                data = data[start:end+1]
            self.send_response(206 if byte_range else 200)
            self.send_header("Content-Type", mimetypes.guess_type(str(target))[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            if audio:
                self.send_header('Accept-Ranges', 'bytes')
            if byte_range:
                self.send_header('Content-Range', f'bytes {start}-{end}/{total}')
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                # Media players may stop a preload or skip a track mid-transfer.
                pass

        def _valid_host(self):
            return self.headers.get("Host", "").lower() in {f"localhost:{self.server.server_port}", f"127.0.0.1:{self.server.server_port}"}

        def do_POST(self):
            # Protect the local engine and save file from cross-origin browser requests.
            origin = self.headers.get("Origin")
            allowed_origins = {f"http://localhost:{self.server.server_port}", f"http://127.0.0.1:{self.server.server_port}"}
            if not self._valid_host() or (origin and origin not in allowed_origins) or self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                return self.json({"error": "Invalid local request."}, 403)
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 <= length <= 4096:
                    raise ValueError("Request is too large.")
                body = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(body, dict):
                    raise ValueError("Expected a JSON object.")
                path = urlparse(self.path).path
                actions = {
                    "/api/story/read": lambda: app.progress.read_story(body.get('page')),
                    "/api/sensei/read": lambda: app.progress.read_sensei(body.get('page')),
                    "/api/settings": lambda: app.settings(body),
                    "/api/match/start": lambda: app.start(body.get("opponent"), body.get("size", 9)),
                    "/api/match/play": lambda: app.play(body.get("point")),
                    "/api/match/pass": lambda: app.play(None),
                    "/api/match/undo": app.undo,
                    "/api/match/resign": app.resign,
                    "/api/match/abandon": app.abandon,
                    "/api/match/retry": app.retry,
                    "/api/match/hint": app.hint,
                    "/api/shop/buy": lambda: app.progress.buy(body.get("item")),
                    "/api/shop/equip": lambda: app.progress.equip(body.get("item")),
                }
                if path not in actions:
                    return self.json({"error": "Unknown endpoint."}, 404)
                with app.lock if path.startswith("/api/shop/") else _NoLock():
                    actions[path]()
                return self.json(app.state())
            except (ValueError, TypeError, KeyError) as exc:
                return self.json({"error": str(exc)}, 400)
            except Exception as exc:
                return self.json({"error": str(exc)}, 503)

    return Handler


class _NoLock:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def main():
    parser = argparse.ArgumentParser(description="Stonebound · A Go story powered by KaTrain")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="Open the game in your browser")
    args = parser.parse_args()
    app = Stonebound(RUNTIME / "save.json")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(app))
    threading.Thread(target=app.initialize, daemon=True).start()
    url = f"http://127.0.0.1:{args.port}"
    print(f"Stonebound is running at {url}\nKaTrain / KataGo is warming up. Ctrl+C to close.", flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        app.close()
        server.server_close()


if __name__ == "__main__":
    main()
