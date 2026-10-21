"""Metadata shared by settings validation and the offline soundtrack player."""
import json
import sys
from pathlib import Path

ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[1]))
MUSIC = json.loads((ROOT/'web/assets/music/playlist.json').read_text(encoding='utf-8'))
TRACKS = MUSIC['tracks']
TRACK_IDS = {t['id'] for t in TRACKS}
