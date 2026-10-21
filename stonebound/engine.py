"""Headless adapter to KaTrain's actual Game, KataGoEngine and AI strategies.

No reimplementation or fallback bot: engine failures stay visible to the user.
The pinned upstream checkout is left unmodified.
"""
import copy
import json
import os
import sys
import threading
import time
from pathlib import Path

FROZEN = bool(getattr(sys, "frozen", False))
ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
INSTALL_DIR = Path(sys.executable).resolve().parent if FROZEN else ROOT
RUNTIME = Path(os.environ.get("STONEBOUND_DATA_DIR", str(INSTALL_DIR / ("data" if FROZEN else ".runtime")))).resolve()
RUNTIME.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_NO_CONSOLELOG", "1")
os.environ.setdefault("KIVY_NO_FILELOG", "1")
os.environ.setdefault("KIVY_LOG_MODE", "PYTHON")
os.environ.setdefault("KIVY_HOME", str(RUNTIME / "kivy"))
sys.path.insert(0, str(ROOT / "vendor" / "katrain"))

from katrain.core import engine as engine_module
from katrain.core.ai import generate_ai_move
from katrain.core.base_katrain import KaTrainBase, Player
from katrain.core.constants import AI_RANK, OUTPUT_ERROR, PLAYER_AI
from katrain.core.engine import KataGoEngine
from katrain.core.game import BaseGame, Game, IllegalMoveException, Move
from katrain.core.game_node import GameNode
from katrain.core.utils import find_package_resource

engine_module.DATA_FOLDER = str(RUNTIME / "katago")


class GameContext(KaTrainBase):
    def __init__(self):
        self._config = json.loads(Path(find_package_resource("katrain/config.json")).read_text(encoding="utf-8"))
        self._config["game"].update({"size": "9", "komi": 6.5, "handicap": 0, "rules": "chinese"})
        self._config["engine"].update({"max_visits": 64, "fast_visits": 16, "max_time": 1.5, "allow_recovery": False})
        # The portable build starts with generic CPU KataGo, requiring no GPU driver.
        # It uses the same upstream KaTrain model and calibrated AI strategy.
        cpu_engine = ROOT / "resources/cpu/katago.exe"
        if FROZEN and cpu_engine.exists():
            self._config["engine"].update({"katago": str(cpu_engine), "max_visits": 16, "fast_visits": 8, "max_time": 2.0})
        config_path = INSTALL_DIR / "engine-config.json"
        if config_path.exists():
            settings = json.loads(config_path.read_text(encoding="utf-8"))
            self._config["engine"].update(settings)
        for env, field in (("KATAGO_EXECUTABLE", "katago"), ("KATAGO_MODEL", "model"), ("KATAGO_CONFIG", "config")):
            if os.environ.get(env):
                self._config["engine"][field] = os.environ[env]
        # Keep all engine caches inside the project.
        self._config["engine"]["allow_recovery"] = False
        self.players_info = {"B": Player("B"), "W": Player("W", PLAYER_AI, AI_RANK)}
        self.game = None
        self.errors = []
        self.debug_level = -1

    def log(self, message, level=0):
        if level <= OUTPUT_ERROR:
            self.errors.append(str(message))
            self.errors = self.errors[-10:]
            print(f"[KaTrain] {message}", file=sys.stderr)

    def update_state(self, *args, **kwargs):
        pass


class KaTrainBridge:
    def __init__(self):
        self.context = GameContext()
        self.engine = None
        self.status = "starting"
        self.error = None
        self.ready = threading.Event()
        self.init_lock = threading.Lock()

    def initialize(self):
        with self.init_lock:
            if self.status == "ready":
                return
            self.status, self.error = "starting", None
            try:
                self.engine = KataGoEngine(self.context, copy.deepcopy(self.context.config("engine")))
                node = GameNode(properties={"SZ": 9, "KM": 6.5, "RU": "chinese"})
                finished = threading.Event()
                error = []

                def received(result, partial):
                    if not partial:
                        finished.set()

                self.engine.request_analysis(node, received, error_callback=lambda result: (error.append(str(result)), finished.set()), visits=2)
                deadline = time.monotonic() + 240
                while not finished.wait(0.2):
                    self.engine.check_alive(exception_if_dead=True)
                    if time.monotonic() > deadline:
                        raise TimeoutError("KataGo startup took too long. Check the engine configuration and GPU drivers.")
                if error:
                    raise RuntimeError(error[0])
                self.status = "ready"
                self.ready.set()
            except Exception as exc:
                self.error = str(exc)
                self.status = "error"
                if self.engine:
                    self.engine.shutdown()

    def require_ready(self):
        if self.status != "ready":
            raise ValueError(self.error or "KataGo is warming up. Your first game will be ready shortly.")
        self.engine.check_alive(exception_if_dead=True)

    def new_game(self, size, moves=None):
        self.require_ready()
        self.engine.on_new_game()
        game = Game(self.context, self.engine, game_properties={"SZ": size, "KM": 6.5, "RU": "chinese"})
        self.context.game = game
        for color, point in moves or []:
            game.play(Move.from_gtp(point, player=color), analyze=False)
        if moves:
            game.current_node.analyze(self.engine)
        return game

    def wait_analysis(self, node, timeout=45):
        deadline = time.monotonic() + timeout
        while not node.analysis_complete:
            self.engine.check_alive(exception_if_dead=True)
            if time.monotonic() > deadline:
                raise TimeoutError("KataGo is taking longer than expected. You can retry this turn.")
            time.sleep(0.02)

    def play_rival(self, game, rival):
        self.wait_analysis(game.current_node)
        settings = copy.deepcopy(self.context.config("ai")[AI_RANK])
        settings["kyu_rank"] = rival["kyu"]
        return generate_ai_move(game, AI_RANK, settings)

    def close(self):
        if self.engine:
            self.engine.shutdown()
