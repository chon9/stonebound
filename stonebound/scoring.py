"""Chinese area scoring, with KataGo ownership used to identify dead stones.

Unsettled groups should be played out before both players pass. Only strongly
opposed ownership (85%) removes a group; remaining groups count as alive.
"""


def area_score(size, stones, ownership=None, komi=6.5):
    board = {(x, y): color for x, y, color in stones}
    removed = []
    if ownership and len(ownership) == size * size:
        checked = set()
        for point, color in list(board.items()):
            if point in checked:
                continue
            group, queue = [], [point]
            checked.add(point)
            while queue:
                x, y = queue.pop()
                group.append((x, y))
                for neighbor in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                    if neighbor not in checked and board.get(neighbor) == color:
                        checked.add(neighbor)
                        queue.append(neighbor)
            # A connected chain cannot be partly dead. Any uncertain stone keeps
            # the whole chain alive until the players resolve it on the board.
            values = [ownership[(size - 1 - y) * size + x] for x, y in group]
            if all(v < -.85 if color == 'B' else v > .85 for v in values):
                for x, y in group:
                    removed.append((x, y, color))
                    del board[(x, y)]
    scores = {"B": sum(c == "B" for c in board.values()), "W": sum(c == "W" for c in board.values()) + komi}
    visited = set(board)
    neutral = 0
    territory = []
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
                owner = next(iter(bordering))
                scores[owner] += len(region)
            else:
                owner = 'N'
                neutral += len(region)
            territory.extend([px, py, owner] for px, py in region)
    diff = scores["B"] - scores["W"]
    return {"black": scores["B"], "white": scores["W"], "neutral": neutral, "dead": removed, "winner": "B" if diff > 0 else "W", "margin": abs(diff), "komi": komi, "territory": territory}
