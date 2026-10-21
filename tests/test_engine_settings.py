import os
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from stonebound.app import Stonebound
from stonebound.engine import ROOT, BaseGame, GameContext, GameNode, KaTrainBridge, Move
from stonebound.progress import Progress


class EngineSettingsTests(unittest.TestCase):
    def setUp(self):
        folder = ROOT / '.runtime/test-temp'; folder.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=folder)
        self.app = Stonebound.__new__(Stonebound)
        self.app.lock = threading.RLock()
        self.app.progress = Progress(Path(self.tmp.name) / 'save.json')
        self.app.progress.data.update(coins=925, xp=123, ai_backend='cpu')
        self.app.engine_switching = False
        self.app.engine_target = self.app.engine_switch_error = None
        self.app.bridge = SimpleNamespace(backend='cpu', status='ready', close=Mock())
        self.app.game = self.make_game(19, [['B', 'D4'], ['W', 'Q16']])
        self.app.match = {'id':'switch-test','opponent':'haru','size':19,'thinking':False,'finished':False,
                          'hint':{'gtp':'C3'},'sensei':{'gtp':'C3'},'error':None,'result':None}
        self.app._persist_match()
        self.release, self.entered, self.closed = threading.Event(), threading.Event(), threading.Event()

    def tearDown(self):
        self.release.set()
        deadline = time.monotonic() + 2
        while self.app.engine_switching and time.monotonic() < deadline:
            time.sleep(.01)
        with self.app.lock: self.tmp.cleanup()

    @staticmethod
    def make_game(size, moves):
        game = BaseGame(GameContext(), move_tree=GameNode(properties={'SZ':size,'KM':6.5,'RU':'chinese'}))
        for color, gtp in moves: game.play(Move.from_gtp(gtp, player=color))
        return game

    def candidate(self, mode='gpu', fails=False):
        result = SimpleNamespace(backend=mode, status='starting', error=None, new_game=self.make_game, close=self.closed.set)
        def initialize():
            self.entered.set()
            if not self.release.wait(2): raise TimeoutError('Test gate timed out')
            result.status = 'error' if fails else 'ready'
            result.error = 'No compatible OpenCL device' if fails else None
        result.initialize = initialize
        return result

    def settle(self):
        deadline = time.monotonic() + 2
        while self.app.engine_switching and time.monotonic() < deadline: time.sleep(.01)
        self.assertFalse(self.app.engine_switching)

    def test_invalid_backend_is_atomic_with_other_settings(self):
        for value in ('cuda', '', None, [], 1, True):
            before = self.app.progress.snapshot()
            with self.assertRaises(ValueError): self.app.settings({'language':'zh-CN','ai_backend':value})
            self.assertEqual(before, self.app.progress.snapshot())

    def test_switch_preserves_board_rewards_and_saves_choice_only_on_success(self):
        previous = self.app.bridge
        before = self.app.progress.snapshot()['match']
        with patch('stonebound.app.KaTrainBridge', return_value=self.candidate()):
            self.app.settings({'ai_backend':'gpu'})
            self.assertTrue(self.entered.wait(.5))
            self.assertTrue(self.app.engine_switching)
            self.assertEqual(self.app.progress.data['ai_backend'], 'cpu')
            self.assertFalse(previous.close.called)
            for operation in (lambda:self.app.play([2,2]), self.app.abandon, lambda:self.app.start('haru',9)):
                with self.assertRaisesRegex(ValueError, 'switching'): operation()
            with self.assertRaises(ValueError): self.app.settings({'ai_backend':'cpu'})
            self.release.set(); self.settle()
        restored = Progress(self.app.progress.path)
        self.assertEqual(restored.data['ai_backend'], 'gpu')
        self.assertEqual(restored.data['match']['moves'], before['moves'])
        self.assertEqual(restored.data['coins'], 925)
        self.assertEqual(restored.data['xp'], 123)
        self.assertIsNone(self.app.match['hint'])
        self.assertEqual(self.app.game.current_node.depth, 2)

    def test_failed_gpu_keeps_working_engine_and_exact_board(self):
        previous, board, saved = self.app.bridge, self.app.game, self.app.progress.snapshot()
        with patch('stonebound.app.KaTrainBridge', return_value=self.candidate(fails=True)):
            self.app.settings({'ai_backend':'gpu'}); self.assertTrue(self.entered.wait(.5))
            self.release.set(); self.settle(); self.assertTrue(self.closed.wait(.5))
        self.assertIs(self.app.bridge, previous)
        self.assertIs(self.app.game, board)
        self.assertEqual(self.app.progress.snapshot(), saved)
        self.assertFalse(previous.close.called)
        self.assertIn('GPU could not start', self.app.engine_switch_error)

    def test_failed_save_rolls_back_engine_and_progress(self):
        previous, board, saved = self.app.bridge, self.app.game, self.app.progress.snapshot()
        with patch('stonebound.app.KaTrainBridge', return_value=self.candidate()):
            self.app.settings({'ai_backend':'gpu'}); self.assertTrue(self.entered.wait(.5))
            with patch.object(self.app.progress, 'save', side_effect=OSError('Disk full')):
                self.release.set(); self.settle(); self.assertTrue(self.closed.wait(.5))
        self.assertIs(self.app.bridge, previous)
        self.assertIs(self.app.game, board)
        self.assertEqual(self.app.progress.snapshot(), saved)
        self.assertFalse(previous.close.called)

    def test_cpu_recovers_saved_game_after_startup_failure(self):
        self.app.bridge.status = 'error'
        self.app.game = self.app.match = None
        with patch('stonebound.app.KaTrainBridge', return_value=self.candidate('cpu')):
            self.app.settings({'ai_backend':'cpu'}); self.assertTrue(self.entered.wait(.5))
            self.release.set(); self.settle()
        self.assertEqual(self.app.match['id'], 'switch-test')
        self.assertEqual(self.app.game.current_node.depth, 2)
        self.assertEqual(self.app.progress.data['coins'], 925)

    def test_reselecting_stopped_backend_restarts_it(self):
        self.app.bridge.require_ready = Mock(side_effect=ValueError('KataGo stopped'))
        with patch('stonebound.app.KaTrainBridge', return_value=self.candidate('cpu')):
            self.app.settings({'ai_backend':'cpu'}); self.assertTrue(self.entered.wait(.5))
            self.release.set(); self.settle()
        self.assertEqual(self.app.bridge.backend, 'cpu')
        self.assertEqual(self.app.game.current_node.depth, 2)

    def test_closing_during_switch_closes_both_engines_without_committing_choice(self):
        previous = self.app.bridge
        with patch('stonebound.app.KaTrainBridge', return_value=self.candidate()):
            self.app.settings({'ai_backend':'gpu'}); self.assertTrue(self.entered.wait(.5))
            self.app.close()
            self.assertTrue(self.closed.is_set())
            previous.close.assert_called_once()
            self.release.set(); self.settle()
        self.assertIs(self.app.bridge, previous)
        self.assertEqual(self.app.progress.data['ai_backend'], 'cpu')

    def test_closed_bridge_does_not_launch_a_new_process(self):
        bridge = KaTrainBridge('gpu')
        bridge.close()
        with patch('stonebound.engine.KataGoEngine') as start:
            bridge.initialize()
        start.assert_not_called()
        self.assertEqual(bridge.status, 'error')

    def test_switch_is_rejected_during_a_rival_turn(self):
        self.app.match['thinking'] = True
        before = self.app.progress.snapshot()
        with self.assertRaisesRegex(ValueError, 'finish thinking'):
            self.app.settings({'language':'zh-CN','ai_backend':'gpu'})
        self.assertEqual(before, self.app.progress.snapshot())

    def test_explicit_mode_overrides_custom_executable(self):
        with patch.dict(os.environ, {'KATAGO_EXECUTABLE':'old-custom-engine.exe'}):
            cpu, gpu = GameContext('cpu'), GameContext('gpu')
        self.assertEqual(Path(cpu.config('engine/katago')), ROOT/'resources/cpu/katago.exe')
        self.assertNotEqual(cpu.config('engine/katago'), gpu.config('engine/katago'))
        self.assertEqual(gpu.config('engine/backend'), 'local')
        self.assertEqual(gpu.config('engine/altcommand'), '')

    def test_dead_engine_is_reported_without_waiting_for_timeout(self):
        bridge = KaTrainBridge('gpu')
        engine = Mock(); engine.check_alive.return_value = False
        start = time.monotonic()
        with patch('stonebound.engine.KataGoEngine', return_value=engine): bridge.initialize()
        self.assertLess(time.monotonic()-start, 1)
        self.assertEqual(bridge.status, 'error')
        engine.shutdown.assert_called()
        with self.assertRaisesRegex(RuntimeError, 'KataGo stopped'):
            bridge.wait_analysis(SimpleNamespace(analysis_complete=False))
