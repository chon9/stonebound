import copy
import math
import secrets
import threading
import time

from .catalog import ITEMS, OPPONENTS, OPPONENT_BY_ID
from .engine import BaseGame, IllegalMoveException, KaTrainBridge, Move
from .progress import Progress
from .scoring import area_score
from .story import story_snapshot
from .music import TRACKS, TRACK_IDS
from .sensei import advice, ownership_preview, review_move, story_snapshot as spirit_story


class Stonebound:
    def __init__(self, save_path):
        self.lock = threading.RLock()
        self.progress = Progress(save_path)
        self.bridge = KaTrainBridge()
        self.game = None
        self.match = None
        self.initialized = threading.Event()

    def initialize(self):
        self.bridge.initialize()
        if self.bridge.status == "ready":
            try:
                with self.lock:
                    saved = self.progress.data.get("match")
                    if saved:
                        self.game = self.bridge.new_game(saved["size"], saved["moves"])
                        self.match = {**saved, "thinking": False, "error": None, "hint": None, "sensei": None}
                        # Older completed saves had a score but no territory map.
                        score = (self.match.get('result') or {}).get('score')
                        if score and 'territory' not in score:
                            dead = {tuple(s[:2]) for s in score.get('dead', [])}
                            live = [[*s.coords, s.player] for s in self.game.stones if s.coords not in dead]
                            score['territory'] = area_score(saved['size'], live)['territory']
                        if score:
                            self.match['territory'] = {'estimated': False, 'points': score['territory'], 'dead': score['dead']}
                        if not self.match.get("finished") and self.game.current_node.next_player == "W":
                            self._start_turn()
            except Exception as exc:
                self.bridge.status, self.bridge.error = "error", f"Could not restore your saved match: {exc}"
        self.initialized.set()

    def _persist_match(self):
        if self.game and self.match:
            self.match["moves"] = [[node.move.player, node.move.gtp()] for node in self.game.current_node.nodes_from_root if node.move]
            self.progress.data["match"] = {k: copy.deepcopy(v) for k, v in self.match.items() if k not in ("thinking", "hint", "error", "sensei")}
        else:
            self.progress.data["match"] = None
        self.progress.save()

    def state(self):
        with self.lock:
            profile = self.progress.snapshot()
            profile.pop("match", None)
            match = None
            if self.match and self.game:
                match = copy.deepcopy(self.match)
                match.update({
                    "stones": [[*s.coords, s.player] for s in self.game.stones],
                    "next": self.game.current_node.next_player,
                    "last": ([*self.game.current_node.move.coords, self.game.current_node.move.player] if self.game.current_node.move and not self.game.current_node.move.is_pass else None),
                    "captures": {"B": self.game.prisoner_count["W"], "W": self.game.prisoner_count["B"]},
                    "moveNumber": self.game.current_node.depth,
                    "lastPass": bool(self.game.current_node.is_pass and self.game.current_node.parent),
                })
            return {"profile": profile, "match": match, "opponents": OPPONENTS, "items": ITEMS,
                    "music": TRACKS,
                    "story": story_snapshot(profile['defeated'], profile['story_seen']),
                    "sensei": spirit_story(profile['defeated'], profile['sensei_seen']),
                    "engine": {"status": self.bridge.status, "error": self.bridge.error, "name": "KaTrain · KataGo", "strategy": "KaTrain calibrated rank"}}

    def start(self, opponent_id, size):
        with self.lock:
            self.bridge.require_ready()
            if self.match and not self.match.get("finished"):
                raise ValueError("You have a game in progress. Resume it or leave it first.")
            rival = OPPONENT_BY_ID.get(opponent_id)
            if not rival:
                raise ValueError("Choose a rival from the city.")
            if rival["requires"] and rival["requires"] not in self.progress.data["defeated"] and opponent_id not in self.progress.data['defeated']:
                raise ValueError("Meet the previous rival on your journey first.")
            if type(size) is not int or size not in (9, 13, 19):
                raise ValueError("Choose a 9×9, 13×13, or 19×19 board.")
            self.game = self.bridge.new_game(size)
            self.match = {"id": secrets.token_hex(8), "opponent": opponent_id, "size": size, "moves": [],
                          "thinking": False, "finished": False, "error": None, "hint": None, "result": None,
                          "sensei": None, "review": None, "territory": None}
            self._persist_match()

    def settings(self, values):
        with self.lock:
            updates = {}
            if "language" in values:
                if values["language"] not in ("en", "zh-CN"):
                    raise ValueError("Choose English or Simplified Chinese.")
                updates["language"] = values["language"]
            if "sound" in values:
                if type(values["sound"]) is not bool:
                    raise ValueError("Sound must be on or off.")
                updates["sound"] = values["sound"]
            if "music" in values:
                if type(values["music"]) is not bool:
                    raise ValueError("Music must be on or off.")
                updates["music"] = values["music"]
            if "music_volume" in values:
                volume = values["music_volume"]
                if type(volume) not in (int, float) or not math.isfinite(volume) or not 0 <= volume <= 1:
                    raise ValueError("Music volume must be between 0 and 100 percent.")
                updates["music_volume"] = volume
            if "music_track" in values:
                track = values["music_track"]
                if not isinstance(track, str) or track not in TRACK_IDS:
                    raise ValueError("Choose a track from the soundtrack.")
                updates["music_track"] = track
            self.progress.data.update(updates)
            self.progress.save()

    def _require_game(self, player_turn=True):
        if not self.game or not self.match or self.match.get("finished"):
            raise ValueError("Start a new game in the city.")
        if self.match["thinking"]:
            raise ValueError("Your rival is thinking. Give them a moment.")
        if player_turn and self.game.current_node.next_player != "B":
            raise ValueError("Retry your rival's turn before playing.")

    def play(self, point):
        # Finish the BEFORE evaluation without holding the app lock. Capture it
        # before child analysis can update the parent's candidate statistics.
        with self.lock:
            self._require_game()
            game, node = self.game, self.game.current_node
        self.bridge.wait_analysis(node)
        with self.lock:
            self._require_game()
            if self.game is not game or self.game.current_node is not node:
                raise ValueError('The board changed. Choose your move again.')
            if point is not None and (not isinstance(point, list) or len(point) != 2 or any(type(v) is not int for v in point) or any(v < 0 or v >= self.match["size"] for v in point)):
                raise ValueError("Choose an intersection on the board.")
            move = Move(coords=tuple(point) if point is not None else None, player="B")
            before = (node.score, node.candidate_moves[0]['move']) if node.candidate_moves else None
            try:
                self.game.play(move)
            except IllegalMoveException as exc:
                raise ValueError("That point is occupied, repeats a ko, or leaves your stones with no liberties.") from exc
            self.match["hint"] = None
            self.match['sensei'] = self.match['review'] = self.match['territory'] = None
            self.match["error"] = None
            self._persist_match()
            self._start_turn(before)

    def _start_turn(self, before=None):
        self.match["thinking"] = True
        token = self.match["id"]
        game = self.game
        rival = OPPONENT_BY_ID[self.match["opponent"]]

        def work():
            try:
                node = game.current_node
                review = None
                if before and node.move and node.move.player == 'B':
                    self.bridge.wait_analysis(node)
                    review = review_move(before[0], node.score, node.move.gtp(), before[1], node.depth)
                if not (node.is_pass and node.parent and node.parent.is_pass):
                    _, played = self.bridge.play_rival(game, rival)
                    if played is None:
                        raise RuntimeError("The engine discarded the turn. Please retry.")
                node = game.current_node
                finished = node.is_pass and node.parent and node.parent.is_pass
                if finished:
                    self.bridge.wait_analysis(node)
                with self.lock:
                    if not self.match or self.match["id"] != token:
                        return
                    self.match["thinking"] = False
                    if review:
                        self.match['review'] = review
                    if finished:
                        score = area_score(self.match["size"], [[*s.coords, s.player] for s in game.stones], node.ownership)
                        label = f"{score['winner']}+{score['margin']:g}"
                        self._finish(score["winner"] == "B", label, score)
                    self._persist_match()
            except Exception as exc:
                with self.lock:
                    if self.match and self.match["id"] == token:
                        self.match["thinking"] = False
                        self.match["error"] = f"KataGo couldn't complete this turn: {exc}"
                        self._persist_match()

        threading.Thread(target=work, daemon=True).start()

    def _finish(self, won, result, score=None):
        if self.match["finished"]:
            return
        # Commit the result, the final board and the reward in one atomic save.
        reward = self.progress.reward(self.match["opponent"], won, result, commit=False)
        self.match.update({"finished": True, "thinking": False, "result": {"won": won, "label": result, "score": score, **reward}})
        self.match['hint'] = self.match['sensei'] = None
        if score:
            self.match['territory'] = {'estimated': False, 'points': score['territory'], 'dead': score['dead']}

    def undo(self):
        with self.lock:
            self._require_game(player_turn=False)
            if not self.game.current_node.depth:
                raise ValueError("Place your first stone to begin.")
            # Return to the position before the player's last turn, including after an engine error.
            n = 2 if self.game.current_node.next_player == "B" else 1
            BaseGame.undo(self.game, n_times=n)
            self.match["error"] = self.match["hint"] = None
            self.match['sensei'] = self.match['review'] = self.match['territory'] = None
            self.game.current_node.analyze(self.bridge.engine)
            self._persist_match()

    def resign(self):
        with self.lock:
            self._require_game(player_turn=False)
            game, node = self.game, self.game.current_node
        self.bridge.wait_analysis(node)
        preview = ownership_preview(game.board_size[0], node.ownership, node.score)
        with self.lock:
            self._require_game(player_turn=False)
            if self.game is not game or game.current_node is not node:
                raise ValueError('The board changed. Try again.')
            self._finish(False, "W+R")
            self.match['territory'] = preview
            self._persist_match()

    def abandon(self):
        with self.lock:
            if self.match and self.match["thinking"]:
                raise ValueError("Wait for your rival to finish thinking before leaving.")
            self.bridge.engine.on_new_game() if self.bridge.engine else None
            self.game = self.match = None
            self._persist_match()

    def retry(self):
        with self.lock:
            self._require_game(player_turn=False)
            if self.game.current_node.next_player != "W" and not (self.game.current_node.is_pass and self.game.current_node.parent and self.game.current_node.parent.is_pass):
                raise ValueError("It's your turn to play.")
            self.bridge.require_ready()
            if not self.game.current_node.analysis_complete:
                self.game.current_node.analyze(self.bridge.engine)
            self.match["error"] = None
            self._start_turn()

    def hint(self):
        with self.lock:
            self._require_game()
            game, token, node = self.game, self.match["id"], self.game.current_node
        self.bridge.wait_analysis(node)
        teaching = advice(node, game.board_size[0], [[*s.coords, s.player] for s in game.stones], Move)
        with self.lock:
            if self.game is game and self.match and self.match["id"] == token and self.game.current_node is node and not self.match['finished'] and not self.match['thinking']:
                self.match["hint"] = {"point": teaching['point'], "gtp": teaching['gtp']}
                self.match['sensei'] = teaching
            else:
                raise ValueError('The board changed. Ask the master again.')
