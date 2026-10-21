"""Chinese area scoring, with KataGo ownership used to identify dead stones.

Unsettled groups should be played out before both players pass. Only strongly
opposed ownership (85%) removes a group; remaining groups count as alive.
"""


def area_score(size, stones, ownership=None, komi=6.5):
    board = {(x, y): color for x, y, color in stones}
    removed = []
    if ownership and len(ownership) == size * size:
        for (x, y), color in list(board.items()):
            value = ownership[(size - 1 - y) * size + x]
            if (color == "B" and value < -0.85) or (color == "W" and value > 0.85):
                removed.append((x, y, color))
                del board[(x, y)]
    scores = {"B": sum(c == "B" for c in board.values()), "W": sum(c == "W" for c in board.values()) + komi}
    visited = set(board)
    neutral = 0
    for x in range(size):
        for y in range(size):
            if (x, y) in visited:
                continue
            region, bordering, queue = [], set(), [(x, y)]
            visited.add((x, y))
            while queue:
                px, py = queue.pop()
                region.append((px, py))
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if not (0 <= nx < size and 0 <= ny < size):
                        continue
                    if (nx, ny) in board:
                        bordering.add(board[(nx, ny)])
                    elif (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            if len(bordering) == 1:
                scores[next(iter(bordering))] += len(region)
            else:
                neutral += len(region)
    diff = scores["B"] - scores["W"]
    return {"black": scores["B"], "white": scores["W"], "neutral": neutral, "dead": removed, "winner": "B" if diff > 0 else "W", "margin": abs(diff), "komi": komi}
