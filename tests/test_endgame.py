import copy
import threading
import unittest
from unittest.mock import Mock, patch

from stonebound.endgame import pass_is_equivalent, settled_for_friendly_pass
from stonebound.engine import BaseGame, GameContext, GameNode, KaTrainBridge, Move


class FriendlyPassTests(unittest.TestCase):
    def settled(self, **changes):
        stones = [(2,y,'B') for y in range(9)] + [(3,y,'W') for y in range(9)]
        ownership = [1. if x < 3 else -1. for y in range(9) for x in range(9)]
        values = dict(size=9, stones=stones, ownership=ownership, score_lead=-33.5, player='W', point=(6,4))
        values.update(changes)
        return settled_for_friendly_pass(**values)

    def test_closed_borders_and_confident_ownership_allow_check(self):
        self.assertTrue(self.settled())

    def test_opening_or_unclaimed_dame_prevent_friendly_pass(self):
        stones = [(2,y,'B') for y in range(9)] + [(4,y,'W') for y in range(9)]
        ownership = [1. if x < 3 else 0. if x == 3 else -1. for y in range(9) for x in range(9)]
        self.assertFalse(self.settled(stones=stones, ownership=ownership, score_lead=-24.5))
        self.assertFalse(self.settled(stones=[(2,2,'B'),(6,6,'W')]))

    def test_uncertain_group_or_score_disagreement_prevent_finish(self):
        ownership = [1. if x < 3 else -1. for y in range(9) for x in range(9)]
        ownership[(8-4)*9+3] = -.5
        self.assertFalse(self.settled(ownership=ownership))
        self.assertFalse(self.settled(score_lead=-30))

    def test_point_next_to_live_opponent_is_not_ignored(self):
        self.assertFalse(self.settled(point=(1,4)))

    def test_missing_or_nonfinite_analysis_cannot_end_game(self):
        for ownership in (None, [], [float('nan')]*81):
            self.assertFalse(self.settled(ownership=ownership))
        self.assertFalse(self.settled(score_lead=float('inf')))

    def test_equivalence_uses_black_perspective_for_white(self):
        move = dict(utility=-1.2, scoreLead=-77., scoreSelfplay=-77.)
        self.assertTrue(pass_is_equivalent('W', dict(utility=-1.19, scoreLead=-76.9, scoreSelfplay=-76.9), move))
        self.assertFalse(pass_is_equivalent('W', dict(utility=-1.19, scoreLead=-76., scoreSelfplay=-77.), move))
        self.assertFalse(pass_is_equivalent('W', dict(utility=-1.19, scoreLead=-77., scoreSelfplay=-76.), move))
        self.assertFalse(pass_is_equivalent('W', dict(utility=-.9, scoreLead=-77., scoreSelfplay=-77.), move))

    def test_black_and_missing_fields(self):
        move = dict(utility=1.2, scoreLead=77., scoreSelfplay=77.)
        self.assertTrue(pass_is_equivalent('B', dict(utility=1.19, scoreLead=76.9, scoreSelfplay=76.9), move))
        self.assertFalse(pass_is_equivalent('B', dict(utility=1.19, scoreLead=76., scoreSelfplay=77.), move))
        self.assertFalse(pass_is_equivalent('W', {}, move))
        self.assertFalse(pass_is_equivalent('W', dict(utility=float('nan'), scoreLead=77., scoreSelfplay=77.), move))


class BridgeEndgameTests(unittest.TestCase):
    def setUp(self):
        self.game = BaseGame(GameContext(), move_tree=GameNode(properties={'SZ':9,'KM':6.5,'RU':'chinese'}))
        self.game.play(Move(None,'B'))
        self.node = self.game.current_node
        self.node.analysis['root'] = {'scoreLead':-6.5,'winrate':.5,'visits':64}
        self.node.analysis['completed'] = True
        self.bridge = KaTrainBridge.__new__(KaTrainBridge)
        self.bridge.context = GameContext()
        self.bridge.closed = threading.Event()
        self.bridge.wait_analysis = Mock()

    def candidate(self, gtp):
        self.node.analysis['moves'] = {gtp:dict(move=gtp,order=0,scoreLead=-6.5,winrate=.5)}

    def test_searched_pass_overrides_rank_policy(self):
        self.candidate('pass')
        with patch('stonebound.engine.generate_ai_move') as weakened:
            move, played = self.bridge.play_rival(self.game, {'kyu':15})
        self.assertTrue(move.is_pass)
        self.assertIs(played, self.game.current_node)
        self.assertTrue(played.parent.is_pass)
        weakened.assert_not_called()

    def test_early_pass_does_not_skip_normal_rank_strategy(self):
        self.candidate('C3')
        with patch('stonebound.engine.generate_ai_move', return_value=('rank-move','node')) as weakened:
            result = self.bridge.play_rival(self.game, {'kyu':15})
        self.assertEqual(result, ('rank-move','node'))
        weakened.assert_called_once()

    def test_friendly_pass_needs_comparison_and_completed_borders(self):
        self.candidate('C3')
        values = dict(utility=-1., scoreLead=-6.5, scoreSelfplay=-6.5)
        self.bridge._evaluate_after = Mock(return_value=values)
        with patch('stonebound.engine.settled_for_friendly_pass', return_value=True):
            move, _ = self.bridge.play_rival(self.game, {'kyu':15})
        self.assertTrue(move.is_pass)
        self.assertEqual(self.bridge._evaluate_after.call_count, 2)

    def test_meaningful_gain_prevents_friendly_pass(self):
        self.candidate('C3')
        self.bridge._evaluate_after = Mock(side_effect=[dict(utility=-1.,scoreLead=-6.5,scoreSelfplay=-6.5),
                                                       dict(utility=-1.,scoreLead=-7.5,scoreSelfplay=-7.5)])
        with patch('stonebound.engine.settled_for_friendly_pass', return_value=True), \
             patch('stonebound.engine.generate_ai_move', return_value=('rank-move','node')):
            self.assertEqual(self.bridge.play_rival(self.game, {'kyu':15}), ('rank-move','node'))

    def test_hypothetical_queries_do_not_change_board_tree_or_coaching(self):
        self.candidate('C3')
        before = copy.deepcopy(self.node.analysis)
        nodes = list(self.node.nodes_from_root)
        def request(clone, callback, **kwargs):
            self.assertIsNot(clone.parent, self.node)
            self.assertEqual(clone.moves[0].gtp(), 'C3')
            self.assertTrue(kwargs['extra_settings']['conservativePass'])
            callback({'rootInfo':{'scoreLead':-6.5}}, False)
        self.bridge.engine = Mock(request_analysis=request)
        self.assertEqual(self.bridge._evaluate_after(self.node, Move.from_gtp('C3','W')), {'scoreLead':-6.5})
        self.assertIs(self.game.current_node, self.node)
        self.assertEqual(self.node.analysis, before)
        self.assertEqual(self.node.nodes_from_root, nodes)
        self.assertEqual(self.node.children, [])
        self.assertEqual(self.game.stones, [])
