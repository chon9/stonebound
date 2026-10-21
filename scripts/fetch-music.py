"""Download original CC0 recordings; retain license, source and file hashes."""
import concurrent.futures
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web/assets/music'
TRACKS = [
    ('vaporware', 'Vaporware', '云间琴声', '003_Vaporware_2.mp3', 'calm-piano-1-vaporware'),
    ('another-august', 'Another August', '又一个八月', '013_Another_August_0.mp3', 'another-august'),
    ('synthwave-4k', 'Synthwave 4k', '静谧涟漪', '001_Synthwave_4k_0.mp3', 'calm-ambient-1-synthwave-4k'),
    ('happy-lullaby', 'Happy Lullaby', '晚风摇篮曲', 'song17.mp3', 'happy-lullaby-song17'),
]


def fetch(track):
    id, title, zh, remote, page = track
    url = 'https://opengameart.org/sites/default/files/' + remote
    path = OUT / (id + '.mp3')
    if not path.exists():
        request = urllib.request.Request(url, headers={'User-Agent': 'Stonebound-music/0.3.1'})
        with urllib.request.urlopen(request, timeout=90) as response:
            data = response.read()
        if len(data) < 100000 or data[:20].lower().startswith(b'<!doctype'):
            raise RuntimeError(f'Invalid music download: {id}')
        path.write_bytes(data)
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name',
        '-of', 'json', str(path)], text=True))
    if not any(s['codec_name'] == 'mp3' for s in probe['streams']):
        raise RuntimeError(f'Not an MP3 recording: {id}')
    return {'id': id, 'title': title, 'title_zh': zh, 'artist': 'The Cynic Project',
            'file': '/assets/music/' + path.name, 'license': 'CC0-1.0',
            'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
            'source': 'https://opengameart.org/content/' + page, 'download_url': url,
            'duration': round(float(probe['format']['duration']), 2),
            'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        tracks = list(pool.map(fetch, TRACKS))
    manifest = {'playlist': 'Quiet moves', 'license_checked': '2026-10-21',
                'credit': 'The Cynic Project / cynicmusic.com / pixelsphere.org',
                'tracks': tracks}
    (OUT/'playlist.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(f"Bundled {len(tracks)} original CC0 tracks, {sum(t['duration'] for t in tracks)/60:.1f} minutes.")
    for t in tracks:
        print(t['title'], t['duration'], t['sha256'])


if __name__ == '__main__':
    main()
