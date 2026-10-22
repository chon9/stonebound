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

from .endgame import pass_is_equivalent, settled_for_friendly_pass

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


def backend_options():
    return {"cpu": (ROOT / "resources/cpu/katago.exe").is_file(),
            "gpu": Path(find_package_resource("katrain/KataGo/katago.exe")).is_file()}


class GameContext(KaTrainBase):
    def __init__(self, backend=None):
        if backend not in (None, 'cpu', 'gpu'):
            raise ValueError('Choose CPU or GPU.')
        self.backend = backend or ('cpu' if FROZEN else 'gpu')
        self._config = json.loads(Path(find_package_resource("katrain/config.json")).read_text(encoding="utf-8"))
        self._config["game"].update({"size": "9", "komi": 6.5, "handicap": 0, "rules": "chinese"})
        self._config["engine"].update({"max_visits": 64, "fast_visits": 16, "max_time": 1.5, "allow_recovery": False})
        # The portable build starts with generic CPU KataGo, requiring no GPU driver.
        # It uses the same upstream KaTrain model and calibrated AI strategy.
        cpu_engine = ROOT / "resources/cpu/katago.exe"
        if self.backend == 'cpu':
            self._config["engine"].update({"katago": str(cpu_engine), "max_visits": 16, "fast_visits": 8, "max_time": 2.0})
        config_path = INSTALL_DIR / "engine-config.json"
        if config_path.exists():
            settings = json.loads(config_path.read_text(encoding="utf-8"))
            self._config["engine"].update(settings)
        for env, field in (("KATAGO_EXECUTABLE", "katago"), ("KATAGO_MODEL", "model"), ("KATAGO_CONFIG", "config")):
            if os.environ.get(env):
                self._config["engine"][field] = os.environ[env]
        if backend:
            # An explicit in-game choice selects the bundled executable. Keep
            # model/search configuration, but never run an old custom command.
            executable = cpu_engine if backend == 'cpu' else Path(find_package_resource('katrain/KataGo/katago.exe'))
            if not executable.is_file():
                raise ValueError(f'The {backend.upper()} engine is not installed.')
            self._config['engine'].update(katago=str(executable), backend='local', altcommand='', remote_url='')
        elif config_path.exists() or os.environ.get('KATAGO_EXECUTABLE'):
            self.backend = 'custom'
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
    def __init__(self, backend=None):
        self.context = GameContext(backend)
        self.backend = self.context.backend
        self.engine = None
        self.status = "starting"
        self.error = None
        self.ready = threading.Event()
        self.init_lock = threading.Lock()
        self.closed = threading.Event()

    def initialize(self):
        with self.init_lock:
            if self.status == "ready":
                return
            self.status, self.error = "starting", None
            try:
                if self.closed.is_set():
                    raise RuntimeError('Engine startup cancelled.')
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
                    if self.closed.is_set():
                        raise RuntimeError('Engine startup cancelled.')
                    if not self.engine.check_alive(exception_if_dead=True):
                        raise RuntimeError('KataGo could not start. ' + ' '.join(self.context.errors[-3:]))
                    if time.monotonic() > deadline:
                        raise TimeoutError("KataGo startup took too long. Check the engine configuration and GPU drivers.")
                if error:
                    raise RuntimeError(error[0])
                if self.closed.is_set():
                    raise RuntimeError('Engine startup cancelled.')
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
        if not self.engine.check_alive(exception_if_dead=True):
            raise ValueError('KataGo stopped. Choose CPU or GPU again in Settings to restart it.')

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
            if not self.engine.check_alive(exception_if_dead=True):
                raise RuntimeError('KataGo stopped. Choose CPU or GPU again in Settings to restart it.')
            if time.monotonic() > deadline:
                raise TimeoutError("KataGo is taking longer than expected. You can retry this turn.")
            time.sleep(0.02)

    def play_rival(self, game, rival):
        node = game.current_node
        self.wait_analysis(node)
        candidates = node.candidate_moves
        if candidates:
            best = Move.from_gtp(candidates[0]['move'], player=node.next_player)
            # Rank calibration uses the raw policy; it must not override a
            # searched pass or prolong a settled game with harmless cleanup.
            searched_pass = best.is_pass
            friendly_pass = (not searched_pass and node.is_pass and node.parent
                             and settled_for_friendly_pass(game.board_size[0],
                                 [[*s.coords, s.player] for s in game.stones],
                                 node.ownership, node.score, node.next_player, best.coords)
                             and pass_is_equivalent(node.next_player,
                                 self._evaluate_after(node, Move(None, node.next_player)),
                                 self._evaluate_after(node, best)))
            if searched_pass or friendly_pass:
                move = Move(None, node.next_player)
                played = game.play(move, expected_node=node)
                if played:
                    played.ai_thoughts = ('KataGo searched pass.' if searched_pass else
                                         'KataGo friendly pass: settled borders and no meaningful gain from continuing.')
                return move, played
        settings = copy.deepcopy(self.context.config("ai")[AI_RANK])
        settings["kyu_rank"] = rival["kyu"]
        return generate_ai_move(game, AI_RANK, settings)

    def _evaluate_after(self, node, move):
        # Detached history: hypothetical continuations never touch the real board
        # or feed child evaluation results back into its coaching statistics.
        clone = GameNode(properties=copy.deepcopy(node.root.properties))
        for ancestor in node.nodes_from_root[1:]:
            clone = GameNode(parent=clone, properties=copy.deepcopy(ancestor.properties))
        clone = GameNode(parent=clone, move=move)
        finished, result, errors = threading.Event(), [], []

        def received(analysis, partial):
            if not partial:
                result.append(analysis)
                finished.set()

        self.engine.request_analysis(clone, received,
            error_callback=lambda r: (errors.append(str(r)), finished.set()),
            visits=max(16, min(64, self.context.config('engine/max_visits'))),
            extra_settings={'conservativePass': True, 'wideRootNoise': 0.0}, ownership=False)
        deadline = time.monotonic() + 45
        while not finished.wait(.02):
            if self.closed.is_set() or not self.engine.check_alive(exception_if_dead=True):
                raise RuntimeError('KataGo stopped during the endgame check. Retry this turn.')
            if time.monotonic() > deadline:
                raise TimeoutError('KataGo endgame check timed out. Retry this turn.')
        if errors:
            raise RuntimeError('KataGo endgame check failed: ' + errors[0])
        return result[0].get('rootInfo', {})

    def close(self):
        self.closed.set()
        if self.engine:
            self.engine.shutdown()
