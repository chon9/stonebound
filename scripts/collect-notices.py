"""Preserve distribution notices for embedded Python/runtime dependencies."""
import importlib.metadata
import shutil
import sys
import urllib.request
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resources/licenses"
OUT.mkdir(parents=True, exist_ok=True)
for name in ['kivy','pysgf','pywebview','pythonnet','clr-loader','cffi','pycparser','bottle',
             'proxy-tools','typing-extensions','requests','certifi','chardet','charset-normalizer',
             'idna','urllib3','pywin32','pyinstaller','setuptools']:
    dist = importlib.metadata.distribution(name)
    for file in dist.files or []:
        if any(part.upper().startswith(('LICENSE', 'LICENCE', 'COPYING', 'NOTICE')) for part in file.parts):
            source = Path(dist.locate_file(file))
            if source.is_file():
                target = OUT / name / file.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
python_license = Path(sys.base_prefix) / "LICENSE.txt"
if python_license.exists():
    shutil.copyfile(python_license, OUT / "PYTHON-LICENSE.txt")
shutil.copyfile(ROOT / "vendor/katrain/LICENSE", OUT / "KATRAIN-LICENSE.txt")
kata = OUT / "KataGo"
kata.mkdir(parents=True, exist_ok=True)
tree_cache = ROOT / ".runtime/downloads/katago-source-tree.json"
if not tree_cache.exists():
    req = urllib.request.Request('https://api.github.com/repos/lightvector/KataGo/git/trees/v1.18.1?recursive=1', headers={'User-Agent':'Stonebound-build'})
    tree_cache.write_bytes(urllib.request.urlopen(req, timeout=60).read())
tree = json.loads(tree_cache.read_text(encoding='utf-8'))['tree']
paths = ['LICENSE', 'CONTRIBUTORS', 'cpp/core/sha2.cpp']
paths += [f['path'] for f in tree if f['type']=='blob' and f['path'].startswith('cpp/external/') and Path(f['path']).name.upper().startswith(('LICENSE','LICENCE','COPYING','NOTICE'))]
for relative in paths:
    target = kata / relative
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        url = f'https://raw.githubusercontent.com/lightvector/KataGo/v1.18.1/{relative}'
        target.write_bytes(urllib.request.urlopen(url, timeout=30).read())
print(f'Preserved dependency notices and {len(paths)} KataGo license/source notices in {OUT}')
