import json
import tempfile
import unittest
from pathlib import Path

from stonebound.catalog import ITEMS, OPPONENTS, ITEM_BY_ID
from stonebound.campaign import CHAPTERS
from stonebound.progress import Progress
from stonebound.story import SCRIPT, story_snapshot


class CampaignTests(unittest.TestCase):
    def setUp(self):
        temp_root=Path(__file__).resolve().parents[1]/'.runtime/test-temp'
        temp_root.mkdir(parents=True,exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=temp_root)
        self.path = Path(self.tmp.name)/'save.json'
        self.p = Progress(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_complete_catalog_and_sequential_opponents(self):
        self.assertEqual(len(OPPONENTS), 24)
        self.assertEqual(len({r['id'] for r in OPPONENTS}), 24)
        self.assertEqual(len(ITEMS), 48)
        self.assertEqual(len({i['id'] for i in ITEMS}), 48)
        self.assertEqual(sum(i['type']=='board' for i in ITEMS), 24)
        self.assertEqual(sum(i['type']=='stones' for i in ITEMS), 24)
        self.assertEqual(sum(i['source']=='story' for i in ITEMS), 8)
        previous = None
        for i,r in enumerate(OPPONENTS):
            self.assertEqual(r['requires'],previous)
            self.assertEqual(r['chapter'],i//3+1)
            self.assertIn(r['id'],CHAPTERS[i//3]['rivals'])
            self.assertIn(r['portrait'],range(4))
            self.assertEqual(len(r['intro']),3)
            previous=r['id']
        self.assertEqual(OPPONENTS[0]['kyu'],15)
        self.assertEqual(OPPONENTS[-1]['kyu'],-3)

    def test_every_referenced_illustration_is_in_the_project(self):
        assets=Path(__file__).resolve().parents[1]/'web/assets'
        for n in range(1,9):
            self.assertEqual((assets/f'comics/chapter-{n:02d}.png').read_bytes()[:8],b'\x89PNG\r\n\x1a\n')
        for n in range(1,7):
            name='cast.png' if n==1 else f'cast-{n:02d}.png'
            self.assertEqual((assets/name).read_bytes()[:8],b'\x89PNG\r\n\x1a\n')

    def test_story_requires_whole_chapter_not_just_boss(self):
        s=story_snapshot(['ren','sora'])
        self.assertTrue(s['pages'][0]['unlocked'])
        self.assertTrue(all(not p['unlocked'] for p in s['pages'][1:]))
        self.assertTrue(all(not p['panels'] for p in s['pages'][1:]))
        self.assertEqual(len(SCRIPT),8)
        self.assertTrue(all(len(rows)==6 for rows in SCRIPT))
        for row in SCRIPT:
            for panel in row:
                self.assertTrue(all(panel))

    def test_read_gate_and_persisted_deduplication(self):
        with self.assertRaises(ValueError): self.p.read_story('ch02-open')
        with self.assertRaises(ValueError): self.p.read_story('not-a-page')
        self.p.read_story('ch01-open')
        self.p.read_story('ch01-open')
        self.assertEqual(Progress(self.path).data['story_seen'],['ch01-open'])
        self.assertEqual(self.p.data['coins'],150)

    def test_chapter_keepsake_granted_once_without_replacing_equipment(self):
        self.p.reward('haru',True,'B+1.5')
        self.p.reward('mei',True,'B+2.5')
        result=self.p.reward('ren',True,'B+1.5')
        self.assertEqual(result['items'],['river_map'])
        self.assertEqual(result['chapters'],[1])
        self.assertEqual(self.p.data['equipped']['board'],'hinoki')
        self.assertEqual(self.p.reward('ren',True,'B+1.5')['items'],[])
        self.assertEqual(Progress(self.path).data['owned'].count('river_map'),1)
        self.assertTrue(story_snapshot(self.p.data['defeated'])['pages'][2]['unlocked'])
        self.assertEqual(len(story_snapshot(self.p.data['defeated'])['pages'][1]['panels']),3)

    def test_legacy_save_migrates_without_early_final_gift(self):
        saved={'coins':999,'xp':700,'defeated':['haru','mei','ren','sora'],
               'owned':['hinoki','classic','sakura'],'equipped':{'board':'sakura','stones':'classic'}}
        self.path.write_text(json.dumps(saved),encoding='utf-8')
        restored=Progress(self.path)
        self.assertIn('river_map',restored.data['owned'])
        self.assertNotIn('homecoming',restored.data['owned'])
        self.assertEqual(restored.data['coins'],999)
        self.assertEqual(restored.data['equipped']['board'],'sakura')
        self.assertEqual(restored.data['story_seen'],[])
        self.assertFalse(story_snapshot(restored.data['defeated'])['pages'][-1]['unlocked'])

    def test_story_gifts_cannot_be_bought_even_with_enough_coins(self):
        self.p.data.update(coins=100000,defeated=[r['id'] for r in OPPONENTS])
        with self.assertRaises(ValueError): self.p.buy('homecoming')
        self.assertNotIn('homecoming',self.p.data['owned'])

    def test_full_journey_unlocks_all_panels_and_eight_gifts(self):
        for rival in OPPONENTS:
            self.p.reward(rival['id'],True,'B+0.5')
        s=story_snapshot(self.p.data['defeated'])
        self.assertEqual(len(s['pages']),16)
        self.assertTrue(all(p['unlocked'] for p in s['pages']))
        self.assertEqual(sum(len(p['panels']) for p in s['pages']),48)
        self.assertEqual(sum(ITEM_BY_ID[i]['source']=='story' for i in self.p.data['owned']),8)
        for page in s['pages']: self.p.read_story(page['id'])
        self.assertEqual(len(Progress(self.path).data['story_seen']),16)


if __name__=='__main__': unittest.main()
