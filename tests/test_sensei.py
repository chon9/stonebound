import json
import tempfile
import unittest
import threading
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path

from stonebound.engine import ROOT
from stonebound.catalog import OPPONENTS
from stonebound.progress import Progress
from stonebound.scoring import area_score
from stonebound.sensei import ownership_preview, review_move, story_snapshot
from stonebound.app import Stonebound


class SenseiTests(unittest.TestCase):
    def test_delayed_hint_cannot_attach_to_a_changed_board(self):
        app = Stonebound.__new__(Stonebound)
        node = SimpleNamespace(next_player='B')
        app.lock = threading.RLock()
        app.game = SimpleNamespace(current_node=node, board_size=(9, 9), stones=[])
        app.match = {'id': 'test', 'finished': False, 'thinking': False, 'hint': None, 'sensei': None}
        app.bridge = SimpleNamespace(wait_analysis=lambda _: setattr(app.game, 'current_node', SimpleNamespace(next_player='B')))
        with patch('stonebound.app.advice', return_value={'point': [2, 2], 'gtp': 'C3'}):
            with self.assertRaisesRegex(ValueError, 'board changed'): app.hint()
        self.assertIsNone(app.match['hint'])
        self.assertIsNone(app.match['sensei'])
    def test_black_loss_measured_before_white_reply(self):
        review = review_move(4.5, -4, 'A1', 'D4', 13)
        self.assertEqual(review['loss'], 8.5)
        self.assertEqual(review['severity'], 'blunder')
        self.assertIn('缓急', review['quote'])
        self.assertEqual(review['moveNumber'], 13)
        self.assertEqual(review_move(-8, -1, 'D3', 'D4', 1)['loss'], 0)
        self.assertEqual(review_move(1, -3, 'D3', 'D4', 1)['severity'], 'mistake')

    def test_never_scold_recommended_move_due_to_search_noise(self):
        self.assertEqual(review_move(10, -10, 'D4', 'D4', 1)['severity'], 'calm')
        self.assertEqual(review_move(10, -10, 'pass', 'PASS', 1)['loss'], 0)
        self.assertIsNone(review_move(None, 1, 'A1', 'D4', 1))
        self.assertIsNone(review_move(1, float('nan'), 'A1', 'D4', 1))

    def test_ownership_black_perspective_and_bottom_left_coordinates(self):
        ownership = [0.] * 81
        ownership[0] = 1  # top left A9
        ownership[-1] = -1  # bottom right J1
        ownership[72] = .64  # A1 is uncertain, not Black
        points = {(x, y): c for x, y, c in ownership_preview(9, ownership, 3)['points']}
        self.assertEqual(points[(0, 8)], 'B')
        self.assertEqual(points[(8, 0)], 'W')
        self.assertEqual(points[(0, 0)], 'N')
        self.assertEqual(len(points), 81)
        for bad in (None, [], [1] * 80, [float('nan')] * 81):
            with self.assertRaises(ValueError): ownership_preview(9, bad)

    def test_final_map_matches_count_including_dame_and_dead_stones(self):
        stones = [(1, y, 'B') for y in range(5)] + [(3, y, 'W') for y in range(5)]
        score = area_score(5, stones)
        points = score['territory']
        self.assertEqual(len(points), 15)
        self.assertEqual(sum(c == 'B' for x, y, c in points) + 5, score['black'])
        self.assertEqual(sum(c == 'W' for x, y, c in points) + 5 + 6.5, score['white'])
        self.assertEqual(sum(c == 'N' for x, y, c in points), score['neutral'])
        score = area_score(5, [(0, 0, 'W'), (2, 2, 'B')], [1.] * 25)
        self.assertIn([0, 0, 'B'], score['territory'])
        self.assertEqual(len(score['territory']) + 1, score['black'])

    def test_connected_group_is_never_partly_removed(self):
        ownership = [1.] * 25
        ownership[(5-1-1)*5+1] = .5
        score = area_score(5, [(0, 1, 'W'), (1, 1, 'W'), (3, 3, 'B')], ownership)
        self.assertEqual(score['dead'], [])

    def test_story_gates_and_read_state_do_not_grant_rewards(self):
        root = ROOT / '.runtime/test-temp'; root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as d:
            p = Progress(Path(d) / 'save.json')
            p.read_sensei('spirit-awakening'); p.read_sensei('spirit-awakening')
            restored = Progress(p.path)
            self.assertEqual(restored.data['sensei_seen'], ['spirit-awakening'])
            self.assertEqual(restored.data['coins'], 150)
            self.assertEqual(restored.data['xp'], 0)
            for id in ('spirit-homecoming', 'bad', None):
                with self.assertRaises(ValueError): p.read_sensei(id)
            initial = story_snapshot([], [])
            self.assertEqual(sum(c['unlocked'] for c in initial['reflections']), 1)
            chapter2 = story_snapshot([r['id'] for r in OPPONENTS if r['chapter'] == 1], [])
            self.assertTrue(chapter2['reflections'][1]['unlocked'])
            final = story_snapshot([r['id'] for r in OPPONENTS], [])
            self.assertTrue(final['pages'][1]['unlocked'])
            self.assertEqual(len(final['reflections']), 8)
            self.assertEqual(sum(len(p['panels']) for p in final['pages']), 6)

    def test_legacy_profile_keeps_progress_with_new_story_default(self):
        root = ROOT / '.runtime/test-temp'; root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as d:
            path = Path(d) / 'save.json'
            path.write_text(json.dumps({'coins': 925, 'xp': 123}), encoding='utf-8')
            restored = Progress(path)
            self.assertEqual(restored.data['sensei_seen'], [])
            self.assertEqual(restored.data['coins'], 925)
