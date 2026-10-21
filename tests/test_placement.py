"""Placement must not wait for slow coaching; rules remain server-authoritative."""
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace

from stonebound.app import Stonebound
from stonebound.engine import ROOT, BaseGame, GameContext, GameNode, Move
from stonebound.progress import Progress


class PlacementTests(unittest.TestCase):
    def setUp(self):
        folder = ROOT / '.runtime/test-temp'
        folder.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=folder)
        self.gate, self.waiting, self.done = threading.Event(), threading.Event(), threading.Event()
        self.app = Stonebound.__new__(Stonebound)
        self.app.lock = threading.RLock()
        self.app.engine_switching = False
        self.app.engine_target = self.app.engine_switch_error = None
        self.app.progress = Progress(Path(self.tmp.name) / 'save.json')
        self.root = GameNode(properties={'SZ': 19, 'KM': 6.5, 'RU': 'chinese'})
        self.app.game = BaseGame(GameContext(), move_tree=self.root)
        self.app.match = {'id': 'slow-analysis', 'opponent': 'haru', 'size': 19, 'thinking': False,
                          'finished': False, 'hint': None, 'sensei': None, 'review': None, 'territory': None, 'error': None}

        def wait(node):
            if node is self.root:
                self.waiting.set()
                if not self.gate.wait(3):
                    raise TimeoutError('The placement request blocked on analysis.')
            self.analyzed(node, 0 if node is self.root else -8)

        def rival(game, _):
            node = game.play(Move((15, 15), 'W'))
            self.analyzed(node, 100)  # Must not contaminate the player's review.
            self.done.set()
            return node.move, node

        self.app.bridge = SimpleNamespace(wait_analysis=wait, play_rival=rival, status='ready', error=None, backend='cpu')

    def tearDown(self):
        self.gate.set()
        if self.waiting.is_set():
            self.done.wait(2)
            deadline = time.monotonic() + 2
            while self.app.match['thinking'] and time.monotonic() < deadline:
                time.sleep(.01)
        with self.app.lock:
            self.tmp.cleanup()

    @staticmethod
    def analyzed(node, score):
        node.analysis['root'] = {'scoreLead': score, 'winrate': .5, 'visits': 16}
        node.analysis['moves'] = {'Q16': {'move': 'Q16', 'order': 0, 'scoreLead': score, 'winrate': .5}}
        node.analysis['completed'] = True

    def test_19x19_move_is_committed_while_analysis_is_still_blocked(self):
        start = time.perf_counter()
        self.app.play([3, 3])
        self.assertLess(time.perf_counter() - start, .5)
        self.assertTrue(self.waiting.wait(.5))
        self.assertFalse(self.gate.is_set())
        match = self.app.state()['match']
        self.assertEqual(match['stones'], [[3, 3, 'B']])
        self.assertTrue(match['thinking'])
        self.assertEqual(match['next'], 'W')
        saved = json.loads(self.app.progress.path.read_text(encoding='utf-8'))
        self.assertEqual(saved['match']['moves'], [['B', 'D4']])
        with self.assertRaisesRegex(ValueError, 'thinking'):
            self.app.play([4, 4])
        self.gate.set()
        deadline = time.monotonic() + 2
        while self.app.match['thinking'] and time.monotonic() < deadline:
            time.sleep(.01)
        self.assertIsNone(self.app.match['error'])
        self.assertEqual(self.app.match['review']['loss'], 8)
        self.assertEqual(self.app.match['review']['best'], 'Q16')
        self.assertEqual(self.app.state()['match']['moveNumber'], 2)

    def test_invalid_point_is_rejected_without_waiting_for_analysis(self):
        with self.assertRaises(ValueError):
            self.app.play([-1, 0])
        self.assertFalse(self.waiting.is_set())
        self.assertEqual(self.app.game.current_node.depth, 0)

    def test_occupied_point_is_rejected_without_waiting_for_analysis(self):
        self.app.game.play(Move((3, 3), 'B'))
        self.app.game.play(Move((15, 15), 'W'))
        with self.assertRaisesRegex(ValueError, 'occupied'):
            self.app.play([3, 3])
        self.assertFalse(self.waiting.is_set())
        self.assertEqual(self.app.game.current_node.depth, 2)
