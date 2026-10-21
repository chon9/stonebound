"""Optional real-engine verification: win, buy, equip, unlock, and restart/resume.

Run from the project root with .venv/Scripts/python.exe tests/integration.py.
Uses an isolated save, no mocked AI or injected victories.
"""
import sys
import json
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stonebound.app import Stonebound
from stonebound.engine import ROOT


def settle(app):
    until = time.monotonic() + 60
    while app.state()["match"]["thinking"]:
        if time.monotonic() > until:
            raise TimeoutError("A real engine turn exceeded 60 seconds.")
        time.sleep(0.05)
    match = app.state()["match"]
    assert not match["error"], match["error"]
    return match


def main():
    temp_root = ROOT / ".runtime/test-temp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        save_path = Path(directory) / "save.json"
        app = Stonebound(save_path)
        try:
            app.initialize()
            assert app.bridge.status == "ready", app.bridge.error
            app.start("haru", 9)
            print("Playing a full game: KataGo hints as black versus KaTrain calibrated 15-kyu white.", flush=True)
            for turn in range(200):
                app.hint()
                assert len(app.match['sensei']['preview']['points']) == 81
                app.play(app.match["hint"]["point"])
                match = settle(app)
                if turn % 10 == 0:
                    print(f"Move {match['moveNumber']}: {len(match['stones'])} stones on the board", flush=True)
                if match["finished"]:
                    break
            assert match["finished"], "The game did not end within 400 moves."
            assert match['territory']['estimated'] is False
            assert match['territory']['points'] == match['result']['score']['territory']
            assert all(c in ('B', 'W', 'N') for x, y, c in match['territory']['points'])
            # Preserve the real finished game for the territory rendering check.
            final_fixture = ROOT / '.runtime/final-territory/save.json'
            final_fixture.parent.mkdir(parents=True, exist_ok=True)
            final_fixture.write_text(json.dumps(app.progress.snapshot()), encoding='utf-8')
            print(f"Real scored result: {match['result']}", flush=True)
            assert match["result"]["won"], "Strong black did not win; rerun to verify the reward route."
            assert app.progress.data["coins"] == 400
            assert app.progress.data["defeated"] == ["haru"]
            assert app.progress.data["wins"] == 1
            app.progress.buy("sakura")
            assert app.progress.data["coins"] == 100
            assert app.progress.data["equipped"]["board"] == "sakura"
            app.progress.equip("hinoki")
            app.progress.equip("sakura")
            # The newly unlocked rival is playable on a different board size.
            app.start("mei", 13)
            app.play([3, 3])
            expected = settle(app)
            app.bridge.close()
            restored = Stonebound(save_path)
            try:
                restored.initialize()
                actual = restored.state()
                assert restored.bridge.status == "ready", restored.bridge.error
                assert sorted(actual["match"]["stones"]) == sorted(expected["stones"])
                assert actual["match"]["moves"] == expected["moves"]
                assert actual["match"]["size"] == 13
                assert actual["profile"]["coins"] == 100
                assert actual["profile"]["equipped"]["board"] == "sakura"
                assert actual["profile"]["games"] == 1
                print("PASS: actual full-game scoring, first-win coins, rival unlock, purchase/equip, and server restart/resume.", flush=True)
            finally:
                restored.bridge.close()
        finally:
            app.bridge.close()


if __name__ == "__main__":
    main()
