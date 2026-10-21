"""Bundle official Google Fonts for offline play; not required at runtime."""
import re
import urllib.request
from pathlib import Path

out = Path(__file__).resolve().parents[1] / "web/assets/fonts"
out.mkdir(parents=True, exist_ok=True)
for family, weights, folder in [("DM Sans", "400..700", "dmsans"), ("Manrope", "500..800", "manrope")]:
    url = f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}:wght@{weights}&display=swap"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Chrome/140.0.0.0 Safari/537.36"})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    latin = css.rsplit("/* latin */", 1)[-1]
    font_url = re.search(r"url\((https://[^)]+)\)", latin).group(1)
    data = urllib.request.urlopen(font_url, timeout=30).read()
    (out / f"{folder}.woff2").write_bytes(data)
    license_url = f"https://raw.githubusercontent.com/google/fonts/main/ofl/{folder}/OFL.txt"
    (out / f"{folder}-OFL.txt").write_bytes(urllib.request.urlopen(license_url, timeout=30).read())
    print(f"Bundled {family}: {len(data)} bytes")
