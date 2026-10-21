"""Portable Windows entry point: bundled server, KaTrain, KataGo and native WebView2."""
import argparse
import ctypes
import hashlib
import json
import os
import sys
import threading
import time
import traceback
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Stonebound · 棋缘物语")
    parser.add_argument("--data-dir", help="Optional save directory; defaults to data beside the EXE")
    parser.add_argument("--serve", action="store_true", help="Run the bundled backend without a desktop window")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--self-test", metavar="REPORT", help="Verify the bundled engine with a real AI move")
    parser.add_argument("--window-test", metavar="REPORT", help="Verify the native window without displaying it")
    args = parser.parse_args()
    if args.data_dir:
        os.environ["STONEBOUND_DATA_DIR"] = str(Path(args.data_dir).resolve())
    if getattr(sys, "frozen", False) and not args.serve:
        early_data = Path(os.environ.get("STONEBOUND_DATA_DIR", str(Path(sys.executable).resolve().parent / "data")))
        early_data.mkdir(parents=True, exist_ok=True)
        sys.stdout = sys.stderr = (early_data / "desktop.log").open("a", encoding="utf-8", buffering=1)
    from stonebound.engine import FROZEN, RUNTIME
    RUNTIME.mkdir(parents=True, exist_ok=True)

    # Prevent two desktop copies from writing the same portable save.
    mutex = None
    if sys.platform == "win32":
        name = "Local\\Stonebound-" + hashlib.sha256(str(RUNTIME).encode()).hexdigest()[:24]
        ctypes.windll.kernel32.CreateMutexW.restype = ctypes.c_void_p
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, name)
        if not mutex or ctypes.windll.kernel32.GetLastError() == 183:
            raise RuntimeError("Stonebound is already running with this save. / 此存档已在另一窗口中运行。")

    from stonebound.app import Stonebound
    from server import ThreadingHTTPServer, make_handler
    app = Stonebound(RUNTIME / "save.json")
    server = None
    try:
        if args.self_test:
            app.initialize()
            if app.bridge.status != "ready":
                raise RuntimeError(app.bridge.error)
            if app.match and not app.match["finished"]:
                raise RuntimeError("Use an empty --data-dir for self-test; existing game preserved.")
            app.start("haru", 9)
            app.play([2, 2])
            deadline = time.monotonic() + 120
            while app.state()["match"]["thinking"]:
                if time.monotonic() > deadline:
                    raise TimeoutError("The bundled AI did not reply in time.")
                time.sleep(0.1)
            state = app.state()
            if state["match"]["error"] or state["match"]["moveNumber"] != 2:
                raise RuntimeError(state["match"]["error"] or "The AI turn did not complete.")
            app.hint()
            coaching = app.state()['match']['sensei']
            if not coaching or len(coaching['preview']['points']) != 81 or not app.match.get('review'):
                raise RuntimeError('The bundled mentor did not return KataGo advice and a territory map.')
            app.settings({"language": "zh-CN"})
            report = {"ok": True, "frozen": FROZEN, "engine": app.bridge.context.config("engine/katago"),
                      "model": app.bridge.context.config("engine/model"), "moves": state["match"]["moves"],
                      "stones": state["match"]["stones"], "language": app.progress.data["language"],
                      "music_tracks":len(state['music']),
                      "sensei": {"best_move": coaching['gtp'], "ownership_points":len(coaching['preview']['points']),
                                 "review":app.match['review']['severity'], "spirit_manga_pages":len(state['sensei']['pages'])},
                      "campaign": {"opponents":len(state['opponents']), "items":len(state['items']),
                                   "chapters":len(state['story']['chapters']), "manga_pages":len(state['story']['pages'])}}
            Path(args.self_test).resolve().write_text(json.dumps(report, indent=2), encoding="utf-8")
            return

        server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(app))
        server.daemon_threads = True
        threading.Thread(target=app.initialize, daemon=True).start()
        if args.serve:
            print(f"Stonebound http://127.0.0.1:{server.server_port}", flush=True)
            server.serve_forever()
            return
        threading.Thread(target=server.serve_forever, daemon=True).start()
        import webview

        class DesktopAPI:
            def fullscreen(self):
                window.toggle_fullscreen()

        window = webview.create_window("Stonebound · 棋缘物语", f"http://127.0.0.1:{server.server_port}",
                                      width=1366, height=900, min_size=(800, 640), background_color="#10292a",
                                      js_api=DesktopAPI(), hidden=bool(args.window_test))

        def test_window():
            deadline = time.monotonic() + 45
            last_error = None
            try:
                while time.monotonic() < deadline:
                    try:
                        ready = window.evaluate_js("!!document.querySelector('.begin-btn')")
                        if ready:
                            title = window.evaluate_js("document.title")
                            chapters = window.evaluate_js("document.querySelectorAll('[data-chapter]').length")
                            window.evaluate_js("document.querySelector('.spirit-invitation').click(); window.__spiritImage = new Image(); window.__spiritImage.src = '/assets/comics/sensei.png'; true")
                            while time.monotonic() < deadline and not window.evaluate_js("window.__spiritImage.naturalWidth > 0"):
                                time.sleep(.1)
                            spirit_width = window.evaluate_js("window.__spiritImage.naturalWidth")
                            spirit_panels = window.evaluate_js("document.querySelectorAll('.spirit-comic .comic-panel').length")
                            if spirit_width != 1536 or spirit_panels != 3:
                                raise RuntimeError('The native ghost manga did not load.')
                            window.evaluate_js("document.querySelector('[data-action=\"close-modal\"]').click(); true")
                            window.evaluate_js("document.querySelector('.manga-invitation').click(); window.__comicImage = new Image(); window.__comicImage.src = '/assets/comics/chapter-01.png'; true")
                            while time.monotonic() < deadline and not window.evaluate_js("window.__comicImage.naturalWidth > 0"):
                                time.sleep(.1)
                            image_width = window.evaluate_js("window.__comicImage.naturalWidth")
                            panels = window.evaluate_js("document.querySelectorAll('.comic-panel').length")
                            if image_width == 0 or panels != 3:
                                raise RuntimeError('Native manga reader did not load its illustrations.')
                            # Hidden WebView2 windows defer media preloading. Decode a
                            # bundled recording directly; trusted-gesture playback is
                            # verified separately by the real browser interaction suite.
                            window.evaluate_js("""
                                window.__musicDecode = {};
                                fetch(document.querySelector('#bgm-audio').src)
                                  .then(response => response.arrayBuffer())
                                  .then(data => {
                                    const context = new AudioContext();
                                    return context.decodeAudioData(data)
                                      .then(buffer => {window.__musicDecode.duration = buffer.duration;})
                                      .finally(() => context.close());
                                  })
                                  .catch(error => {window.__musicDecode.error = String(error);});
                                true
                            """)
                            while time.monotonic() < deadline and not window.evaluate_js("!!(window.__musicDecode.duration || window.__musicDecode.error)"):
                                time.sleep(.1)
                            music_duration = window.evaluate_js("window.__musicDecode.duration || 0")
                            if not music_duration or music_duration < 30:
                                detail = window.evaluate_js("window.__musicDecode.error || 'timeout'")
                                raise RuntimeError(f'Native soundtrack decoder could not load the bundled music: {detail}')
                            Path(args.window_test).resolve().write_text(json.dumps({"ok": True, "native_window": True, "title": title,
                                "chapter_buttons":chapters, "comic_panels":panels, "comic_image_width":image_width,
                                "spirit_panels":spirit_panels, "spirit_image_width":spirit_width,
                                "music_tracks":len(app.state()['music']), "decoded_music_duration":music_duration}), encoding="utf-8")
                            return
                    except Exception as error:
                        last_error = str(error)
                    time.sleep(0.2)
                diagnostics = window.evaluate_js("JSON.stringify({lobby:!!document.querySelector('.begin-btn'),audio:document.querySelector('#bgm-audio')&&{src:document.querySelector('#bgm-audio').currentSrc,ready:document.querySelector('#bgm-audio').readyState,error:document.querySelector('#bgm-audio').error?.code},text:document.body.innerText.slice(0,160)})")
                raise TimeoutError(f"Native window verification timed out: {last_error}; {diagnostics}")
            except Exception as error:
                Path(args.window_test).resolve().write_text(json.dumps({"ok": False, "error": str(error)}), encoding="utf-8")
            finally:
                window.destroy()

        webview.start(test_window if args.window_test else None, gui="edgechromium", debug=False,
                      private_mode=False, storage_path=str(RUNTIME / "webview"))
        if args.window_test:
            result = json.loads(Path(args.window_test).resolve().read_text(encoding='utf-8'))
            if not result.get('ok'):
                raise RuntimeError(result.get('error', 'Native window verification failed.'))
    finally:
        app.close()
        if server:
            # serve_forever runs in a separate thread in the windowed version.
            if not args.serve:
                server.shutdown()
            server.server_close()
        if mutex:
            ctypes.windll.kernel32.CloseHandle(ctypes.c_void_p(mutex))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        message = traceback.format_exc()
        for flag in ("--self-test", "--window-test"):
            if flag in sys.argv:
                report_path = Path(sys.argv[sys.argv.index(flag) + 1]).resolve()
                report_path.write_text(json.dumps({"ok": False, "error": message}), encoding="utf-8")
        if sys.stderr:
            print(message, file=sys.stderr)
        if sys.platform == "win32" and not any(a in sys.argv for a in ("--serve", "--self-test", "--window-test")):
            ctypes.windll.user32.MessageBoxW(None,
                "Stonebound could not start. Check data/desktop.log. Windows 10/11 with Microsoft Edge WebView2 is required.\n"
                "游戏未能启动，请查看data/desktop.log。需要Windows 10/11及Microsoft Edge WebView2。\n\n" + message[-1400:],
                "Stonebound · 棋缘物语", 0x10)
        sys.exit(1)
