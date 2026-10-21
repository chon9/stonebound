"""Fetch the official generic x64 KataGo CPU build for portable releases."""
import hashlib
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://github.com/lightvector/KataGo/releases/download/v1.18.1/katago-v1.18.1-eigen-windows-x64.zip"
SHA256 = "074485cf150c38aa3bb14ac9f54f2952ffefbceb44673709bbb8a83650bf95d6"
archive = ROOT / ".runtime/downloads/katago-v1.18.1-eigen-windows-x64.zip"
archive.parent.mkdir(parents=True, exist_ok=True)
if not archive.exists():
    print("Downloading official KataGo CPU engine…", flush=True)
    request = urllib.request.Request(URL, headers={"User-Agent": "Stonebound-build"})
    archive.write_bytes(urllib.request.urlopen(request, timeout=90).read())
if hashlib.sha256(archive.read_bytes()).hexdigest() != SHA256:
    raise RuntimeError("KataGo archive checksum does not match the official release.")
destination = ROOT / "resources/cpu"
destination.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(archive) as zipped:
    for member in zipped.infolist():
        if member.is_dir():
            continue
        target = (destination / member.filename).resolve()
        if not target.is_relative_to(destination.resolve()):
            raise RuntimeError("Unsafe archive path.")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(zipped.read(member))
(destination / "SOURCE.txt").write_text(f"KataGo v1.18.1 · Eigen generic x64 CPU build\n{URL}\nSHA256 {SHA256}\n", encoding="utf-8")
print(f"Verified CPU engine extracted to {destination}")
