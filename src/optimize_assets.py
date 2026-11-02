"""Downloads the site's photos and fonts once and stores fast, self-hosted copies in docs/assets/.

Photos become WebP files at several widths (docs/assets/img/<name>-<width>.webp) so every
screen gets a right-sized image from the same domain as the page. Fonts are the Latin
subsets only. Re-run when you add a photo to PHOTOS:
    python3 src/optimize_assets.py && python3 src/build.py
"""
import json
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "src" / ".photo-cache"            # full-size originals, not committed
IMG_OUT = ROOT / "docs" / "assets" / "img"
FONT_OUT = ROOT / "docs" / "assets" / "fonts"
MANIFEST = ROOT / "src" / "photos.json"

WIDTHS = (480, 800, 1200, 1600)
QUALITY = 70

# Unsplash photo id → file name used on the site.
PHOTOS = {
    "1571260899304-425eee4c7efc": "classroom",
    "1627556704302-624286467c65": "graduation-cap",
    "1507842217343-583bb7270b66": "library-shelves",
    "1488190211105-8b0e65b80b4e": "desk-notes",
    "1606761568499-6d2451b23c66": "lecture-hall",
    "1531482615713-2afd69097998": "team-laptops",
    "1456513080510-7bf3a84b82f8": "library-books",
    "1455390582262-044cdead277a": "pen-writing",
    "1551288049-bebda4e38f71": "data-charts",
    "1515378791036-0648a3ef77b2": "laptop-research",
    "1524178232363-1fb2b075b655": "presentation",
    "1521737604893-d14cc237f11d": "group-discussion",
    "1513258496099-48168024aec0": "online-study",
    "1517842645767-c639042777db": "notebook-pen",
}

FONTS = {
    "archivo-latin.woff2": "https://fonts.gstatic.com/s/archivo/v25/k3kPo8UDI-1M0wlSV9XAw6lQkqWY8Q82sLydOxKsv4Rn.woff2",
    "hind-400-latin.woff2": "https://fonts.gstatic.com/s/hind/v18/5aU69_a8oxmIdGl4BDGwgDI.woff2",
    "hind-600-latin.woff2": "https://fonts.gstatic.com/s/hind/v18/5aU19_a8oxmIfLZcERySjRhc9V0.woff2",
    "hind-700-latin.woff2": "https://fonts.gstatic.com/s/hind/v18/5aU19_a8oxmIfNJdERySjRhc9V0.woff2",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ArtSpark asset build)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    for d in (CACHE, IMG_OUT, FONT_OUT):
        d.mkdir(parents=True, exist_ok=True)

    manifest = {}
    total = 0
    for pid, name in PHOTOS.items():
        src = CACHE / f"{name}.jpg"
        if not src.exists():
            src.write_bytes(fetch(f"https://images.unsplash.com/photo-{pid}?auto=format&fit=max&w=2000&q=85&fm=jpg"))
        im = Image.open(src).convert("RGB")
        widths = []
        for w in WIDTHS:
            if w > im.width:
                continue
            h = round(im.height * w / im.width)
            out = IMG_OUT / f"{name}-{w}.webp"
            im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=6)
            total += out.stat().st_size
            widths.append(w)
        manifest[pid] = {"name": name, "widths": widths, "ratio": [im.width, im.height]}
        print(f"{name:18} {im.width}x{im.height} -> {widths}")

    for fname, url in FONTS.items():
        out = FONT_OUT / fname
        if not out.exists():
            out.write_bytes(fetch(url))
        total += out.stat().st_size

    MANIFEST.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"done — {total / 1024:.0f} KB of images and fonts in docs/assets")


if __name__ == "__main__":
    main()
