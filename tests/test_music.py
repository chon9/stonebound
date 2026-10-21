import hashlib
import unittest
from pathlib import Path

from stonebound.music import MUSIC, TRACKS


class MusicAssetsTests(unittest.TestCase):
    def test_cc0_playlist_is_complete_and_matches_recorded_hashes(self):
        root=Path(__file__).resolve().parents[1]/'web'
        self.assertEqual(len(TRACKS),4)
        self.assertEqual(len({t['id'] for t in TRACKS}),4)
        self.assertGreater(sum(t['duration'] for t in TRACKS),540)
        self.assertIn('Cynic Project',MUSIC['credit'])
        for track in TRACKS:
            with self.subTest(track=track['id']):
                self.assertEqual(track['license'],'CC0-1.0')
                self.assertEqual(track['license_url'],'https://creativecommons.org/publicdomain/zero/1.0/')
                self.assertTrue(track['source'].startswith('https://opengameart.org/content/'))
                file=(root/track['file'].lstrip('/')).resolve()
                self.assertTrue(file.is_relative_to(root))
                self.assertEqual(file.stat().st_size,track['bytes'])
                self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(),track['sha256'])


if __name__=='__main__': unittest.main()
