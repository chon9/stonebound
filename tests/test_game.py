import json
import tempfile
import threading
import unittest
from pathlib import Path

from stonebound.engine import ROOT, BaseGame, GameContext, GameNode, IllegalMoveException, Move
from stonebound.progress import Progress
from stonebound.scoring import area_score
from stonebound.app import Stonebound


class KaTrainRulesTests(unittest.TestCase):
    def game(self, black=(), white=()):
        root = GameNode(properties={"SZ": 5, "KM": 6.5, "RU": "chinese"})
        if black:
            root.set_property("AB", [Move(p).sgf((5, 5)) for p in black])
        if white:
            root.set_property("AW", [Move(p).sgf((5, 5)) for p in white])
        return BaseGame(GameContext(), move_tree=root)

    def test_capture_removes_opponent_and_counts_prisoner(self):
        game = self.game(black=[(0, 1), (1, 0), (2, 1)], white=[(1, 1)])
        game.play(Move((1, 2), "B"))
        self.assertNotIn(Move((1, 1), "W"), game.stones)
        self.assertEqual(game.prisoner_count["W"], 1)

    def test_suicide_rolls_back_board(self):
        game = self.game(white=[(0, 1), (1, 0), (2, 1), (1, 2)])
        before = list(game.stones)
        with self.assertRaises(IllegalMoveException):
            game.play(Move((1, 1), "B"))
        self.assertEqual(set(game.stones), set(before))
        self.assertEqual(game.current_node.depth, 0)

    def test_immediate_ko_recapture_is_rejected(self):
        game = self.game(black=[(0, 1), (1, 0), (2, 1)], white=[(1, 1), (0, 2), (2, 2), (1, 3)])
        game.play(Move((1, 2), "B"))
        with self.assertRaises(IllegalMoveException):
            game.play(Move((1, 1), "W"))
        self.assertIn(Move((1, 2), "B"), game.stones)

    def test_undo_restores_captured_stones(self):
        game = self.game(black=[(0, 1), (1, 0), (2, 1)], white=[(1, 1)])
        game.play(Move((1, 2), "B"))
        game.undo()
        self.assertIn(Move((1, 1), "W"), game.stones)
        self.assertEqual(game.prisoner_count["W"], 0)


class ProgressTests(unittest.TestCase):
    def setUp(self):
        temp_root = ROOT / ".runtime/test-temp"
        temp_root.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=temp_root)
        self.progress = Progress(Path(self.tmp.name) / "save.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_shop_rejects_locked_and_unaffordable_items(self):
        with self.assertRaises(ValueError):
            self.progress.buy("sakura")
        self.progress.reward("haru", True, "B+5.5")
        self.progress.buy("sakura")
        self.assertEqual(self.progress.data["coins"], 100)
        self.assertEqual(self.progress.data["equipped"]["board"], "sakura")
        with self.assertRaises(ValueError):
            self.progress.buy("jade")
        with self.assertRaises(ValueError):
            self.progress.buy("sakura")

    def test_repeat_win_rewards_and_reload(self):
        first = self.progress.reward("haru", True, "B+2.5")
        repeat = self.progress.reward("haru", True, "B+1.5")
        loss = self.progress.reward("haru", False, "W+R")
        restored = Progress(self.progress.path)
        self.assertEqual(first["coins"], 250)
        self.assertEqual(repeat["coins"], 80)
        self.assertEqual(loss["coins"], 0)
        self.assertEqual(restored.data["coins"], 480)
        self.assertEqual(restored.data["defeated"], ["haru"])
        self.assertEqual(restored.data["wins"], 2)
        self.assertEqual(restored.data["games"], 3)

    def test_equip_requires_ownership(self):
        with self.assertRaises(ValueError):
            self.progress.equip("midnight")
        self.progress.equip("hinoki")
        self.assertEqual(self.progress.data["equipped"]["board"], "hinoki")

    def test_corrupt_save_is_not_silently_overwritten(self):
        self.progress.path.write_text("broken", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            Progress(self.progress.path)
        self.assertEqual(self.progress.path.read_text(), "broken")

    def test_language_and_sound_survive_reload(self):
        app = Stonebound.__new__(Stonebound)
        app.lock, app.progress = threading.RLock(), self.progress
        app.settings({"language": "zh-CN", "sound": False})
        restored = Progress(self.progress.path)
        self.assertEqual(restored.data["language"], "zh-CN")
        self.assertFalse(restored.data["sound"])
        self.assertEqual(restored.data["coins"], 150)

    def test_invalid_settings_do_not_partially_change_preferences(self):
        app = Stonebound.__new__(Stonebound)
        app.lock, app.progress = threading.RLock(), self.progress
        with self.assertRaises(ValueError):
            app.settings({"language": "zh-CN", "sound": "off"})
        self.assertEqual(self.progress.data["language"], "en")
        self.assertTrue(self.progress.data["sound"])

    def test_existing_save_gets_preference_defaults(self):
        old = {"coins": 925, "defeated": ["haru"], "xp": 100}
        self.progress.path.write_text(json.dumps(old), encoding="utf-8")
        restored = Progress(self.progress.path)
        self.assertEqual(restored.data["coins"], 925)
        self.assertEqual(restored.data["language"], "en")
        self.assertTrue(restored.data["sound"])
        self.assertTrue(restored.data['music'])
        self.assertEqual(restored.data['music_volume'],.22)
        self.assertEqual(restored.data['music_track'],'vaporware')

    def test_music_preferences_survive_reload_independently_of_stone_sounds(self):
        app = Stonebound.__new__(Stonebound)
        app.lock, app.progress = threading.RLock(), self.progress
        app.settings({'sound':False,'music':True,'music_volume':.37,'music_track':'another-august'})
        restored=Progress(self.progress.path)
        self.assertFalse(restored.data['sound'])
        self.assertTrue(restored.data['music'])
        self.assertEqual(restored.data['music_volume'],.37)
        self.assertEqual(restored.data['music_track'],'another-august')
        app.settings({'music':False})
        self.assertFalse(Progress(self.progress.path).data['music'])
        self.assertEqual(self.progress.data['coins'],150)

    def test_invalid_music_preferences_are_rejected_atomically(self):
        app = Stonebound.__new__(Stonebound)
        app.lock, app.progress = threading.RLock(), self.progress
        invalid=[{'music':1},{'music':'on'},{'music_volume':True},{'music_volume':-.01},
                 {'music_volume':1.01},{'music_volume':float('nan')},{'music_volume':float('inf')},
                 {'music_volume':'0.5'},{'music_track':'https://example.com/music.mp3'},
                 {'music_track':[]},{'music_track':None}]
        for values in invalid:
            with self.subTest(values=values):
                before=self.progress.snapshot()
                with self.assertRaises(ValueError): app.settings({'language':'zh-CN',**values})
                self.assertEqual(self.progress.snapshot(),before)

    def test_zero_and_full_music_volume_are_valid(self):
        app = Stonebound.__new__(Stonebound)
        app.lock, app.progress = threading.RLock(), self.progress
        for volume in (0,1):
            app.settings({'music_volume':volume})
            self.assertEqual(Progress(self.progress.path).data['music_volume'],volume)


class ScoringTests(unittest.TestCase):
    def test_area_and_neutral_points(self):
        # Two full columns enclose one territory column each; middle column is neutral.
        stones = [(1, y, "B") for y in range(5)] + [(3, y, "W") for y in range(5)]
        score = area_score(5, stones)
        self.assertEqual(score["black"], 10)
        self.assertEqual(score["white"], 16.5)
        self.assertEqual(score["neutral"], 5)
        self.assertEqual(score["winner"], "W")

    def test_ownership_coordinates_remove_dead_stones(self):
        ownership = [1.0] * 25
        score = area_score(5, [(0, 0, "W"), (2, 2, "B")], ownership)
        self.assertEqual(score["dead"], [(0, 0, "W")])
        self.assertEqual(score["black"], 25)
        self.assertEqual(score["white"], 6.5)

    def test_uncertain_groups_remain_alive(self):
        score = area_score(5, [(1, 1, "W"), (2, 2, "B")], [0.5] * 25)
        self.assertEqual(score["dead"], [])
        self.assertEqual(score["neutral"], 23)


if __name__ == "__main__":
    unittest.main()
