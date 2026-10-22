"""Conservative friendly passing for an analysis-engine client.

KataGo's GTP PlayUtils::maybeFriendlyPass checks settled borders and compares
playing on with passing. Analysis clients must perform this step themselves.
https://github.com/lightvector/KataGo/blob/v1.18.1/cpp/program/playutils.cpp
Our dead-chain detection deliberately uses the same stricter rule as our count.
"""
import math

from .scoring import area_score


def neighbors(point, size):
    x, y = point
    return [(nx, ny) for nx, ny in ((x-1,y), (x+1,y), (x,y-1), (x,y+1))
            if 0 <= nx < size and 0 <= ny < size]


def settled_for_friendly_pass(size, stones, ownership, score_lead, player, point):
    """Reject early passes, dame, uncertain groups and urgent local replies."""
    if (ownership is None or len(ownership) != size*size or score_lead is None
            or not math.isfinite(score_lead) or any(not math.isfinite(v) for v in ownership)
            or player not in ('B','W') or point is None):
        return False
    score = area_score(size, stones, ownership)
    # Dame are worth points under Chinese area scoring. Never skip them here.
    if score['neutral'] or abs(score['black']-score['white']-score_lead) > 1.0:
        return False
    dead = {tuple(s[:2]) for s in score['dead']}
    board = {(x,y):c for x,y,c in stones if (x,y) not in dead}
    area = {(x,y):c for x,y,c in score['territory']}
    area.update(board)
    for (x,y), color in area.items():
        value = ownership[(size-1-y)*size+x]
        # Both territory and remaining live stones must have confident ownership.
        if (color == 'B' and value < .75) or (color == 'W' and value > -.75):
            return False
    opponent = 'W' if player == 'B' else 'B'
    if any(board.get(p) == opponent for p in neighbors(point, size)):
        return False
    checked = set()
    for adjacent in neighbors(point, size):
        if board.get(adjacent) != player or adjacent in checked:
            continue
        queue, liberties = [adjacent], set()
        checked.add(adjacent)
        while queue:
            for p in neighbors(queue.pop(), size):
                if p not in board:
                    liberties.add(p)
                elif board[p] == player and p not in checked:
                    checked.add(p); queue.append(p)
        if len(liberties) <= 1:
            return False
    return True


def pass_is_equivalent(player, after_pass, after_move):
    """Scores and utility are BLACK-perspective, including on White's turn."""
    if player not in ('B', 'W'):
        return False
    sign = 1 if player == 'B' else -1
    for key, tolerance in (('utility', .1), ('scoreLead', .25), ('scoreSelfplay', .25)):
        p, m = after_pass.get(key), after_move.get(key)
        if (not isinstance(p, (int, float)) or not isinstance(m, (int, float))
                or not math.isfinite(p) or not math.isfinite(m)
                or sign*p < sign*m-tolerance):
            return False
    return True
