"""Persistent, server-owned progression. Rewards never come from client scores."""
import copy
import json
import os
import threading
from pathlib import Path

from .catalog import ITEM_BY_ID, OPPONENT_BY_ID
from .story import completed_chapters, story_snapshot


def new_profile():
    return {
        "name": "Traveler", "coins": 150, "xp": 0, "wins": 0, "games": 0,
        "defeated": [], "owned": ["hinoki", "classic"],
        "equipped": {"board": "hinoki", "stones": "classic"},
        "journal": [], "match": None, "language": "en", "sound": True, "story_seen": [],
    }


class Progress:
    def __init__(self, path):
        self.path = Path(path)
        self.lock = threading.RLock()
        self.data = new_profile()
        if self.path.exists():
            # Fail loudly on corrupted saves instead of overwriting player progress.
            saved = json.loads(self.path.read_text(encoding="utf-8"))
            self.data.update(saved)
            if self._grant_keepsakes():
                self.save()

    def _grant_keepsakes(self):
        completed = completed_chapters(self.data['defeated'])
        gifts = [i['id'] for i in ITEM_BY_ID.values() if i.get('source') == 'story'
                 and OPPONENT_BY_ID[i['gift_from']]['chapter'] in completed and i['id'] not in self.data['owned']]
        self.data['owned'].extend(gifts)
        return gifts

    def read_story(self, page_id):
        with self.lock:
            page = next((p for p in story_snapshot(self.data['defeated'])['pages'] if p['id'] == page_id), None)
            if not page or not page['unlocked']:
                raise ValueError('Complete the previous chapter to read this story.')
            if page_id not in self.data['story_seen']:
                self.data['story_seen'].append(page_id)
                self.save()

    def save(self):
        with self.lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
            os.replace(tmp, self.path)

    def snapshot(self):
        with self.lock:
            return copy.deepcopy(self.data)

    def buy(self, item_id):
        with self.lock:
            item = ITEM_BY_ID.get(item_id)
            if not item:
                raise ValueError("This item is not in the shop.")
            if item.get('source') == 'story':
                raise ValueError('Complete the chapter to earn this keepsake.')
            if item_id in self.data["owned"]:
                raise ValueError("You already own this item.")
            if len(self.data["defeated"]) < item["wins"]:
                raise ValueError(f"Befriend {item['wins']} rivals by winning to unlock this item.")
            if self.data["coins"] < item["price"]:
                raise ValueError("You'll need a few more coins. Win a match to earn them.")
            self.data["coins"] -= item["price"]
            self.data["owned"].append(item_id)
            self.data["equipped"][item["type"]] = item_id
            self.save()

    def equip(self, item_id):
        with self.lock:
            if item_id not in self.data["owned"] or item_id not in ITEM_BY_ID:
                raise ValueError("Visit the shop to unlock this item first.")
            self.data["equipped"][ITEM_BY_ID[item_id]["type"]] = item_id
            self.save()

    def reward(self, opponent_id, won, result, commit=True):
        with self.lock:
            rival = OPPONENT_BY_ID[opponent_id]
            before = completed_chapters(self.data['defeated'])
            first = won and opponent_id not in self.data["defeated"]
            coins = (rival["reward"] if first else 80) if won else 0
            xp = rival["xp"] if won else 25
            self.data["games"] += 1
            self.data["wins"] += int(won)
            self.data["coins"] += coins
            self.data["xp"] += xp
            if first:
                self.data["defeated"].append(opponent_id)
            gifts = self._grant_keepsakes()
            chapters = [c for c in completed_chapters(self.data['defeated']) if c not in before]
            self.data["journal"].append({"opponent": opponent_id, "won": won, "result": result, "coins": coins, "xp": xp, "first": first})
            if commit:
                self.save()
            return {"coins": coins, "xp": xp, "first": first, "items": gifts, "chapters": chapters}
