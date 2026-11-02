"""Builds every logo, icon and share image the site uses from src/logo-source.png.

The source logo is gold (#cc9933) and grey (#4d4d4d) artwork with a white
tagline on pure black. Each variant here either crops it on black (for dark
surfaces) or un-mixes the black into transparency (for the light page).

Run:  python3 src/make_assets.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "logo-source.png"
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

GOLD = (204, 153, 51)
GREY = (77, 77, 77)
INK = (17, 17, 17)

TAGLINE_TOP = 803          # rows below this are the white tagline
WORDMARK_BOX = (270, 440, 1424, 806)
FULL_BOX = (186, 432, 1428, 872)

src = Image.open(SRC).convert("RGB")


def save_png(img, name):
    img.save(OUT / name, optimize=True)


def on_black(box, width):
    img = src.crop(box)
    h = round(img.height * width / img.width)
    return img.resize((width, h), Image.LANCZOS)


def transparent(box, tagline_color=INK, keep_tagline=True):
    """Un-mix the black background: every pixel is colour * alpha over black."""
    img = src.crop(box)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    px, po = img.load(), out.load()
    top = box[1]
    for y in range(img.height):
        tagline_row = top + y >= TAGLINE_TOP
        for x in range(img.width):
            r, g, b = px[x, y]
            if max(r, g, b) < 6:
                continue
            gold = b < r * 0.6
            if tagline_row and not gold:
                if not keep_tagline:
                    continue
                a = min(255, max(r, g, b))
                po[x, y] = (*tagline_color, a)
            elif gold:
                a = min(255, round(r / GOLD[0] * 255))
                po[x, y] = (*GOLD, a)
            else:                                  # grey cap
                a = min(255, round(max(r, g, b) / GREY[0] * 255))
                po[x, y] = (*GREY, a)
    return out


def fit(img, width):
    h = round(img.height * width / img.width)
    return img.resize((width, h), Image.LANCZOS)


# — logos —
save_png(on_black(FULL_BOX, 900), "artspark-logo-dark.png")              # footer / dark bands
save_png(fit(transparent(WORDMARK_BOX), 520), "artspark-wordmark.png")  # nav on the light page
save_png(fit(transparent(FULL_BOX), 900), "artspark-logo-light.png")    # light surfaces, tagline in ink
save_png(fit(transparent(FULL_BOX, tagline_color=(255, 255, 255)), 900), "artspark-logo-white.png")  # any dark surface

# — square mark: the gold "A" under the grey cap, lifted from the logo —
mark = Image.new("RGBA", (1000, 1000), (0, 0, 0, 255))
a_glyph = transparent((280, 572, 448, 750), keep_tagline=False)
a_glyph = a_glyph.resize((round(a_glyph.width * 3.7), round(a_glyph.height * 3.7)), Image.LANCZOS)
mark.alpha_composite(a_glyph, ((1000 - a_glyph.width) // 2 - 40, 1000 - a_glyph.height - 110))

# The cap goes on as opaque artwork with a black keyline round it, the way the
# brim sits over the "k" in the logo; the "k" itself is blacked out first.
cap_box = (1090, 444, 1416, 806)
cap_rgb = src.crop(cap_box)
cap_alpha = transparent(cap_box, keep_tagline=False)
cp, ca = cap_rgb.load(), cap_alpha.load()
for y in range(cap_rgb.height):
    for x in range(cap_rgb.width):
        sx, sy = cap_box[0] + x, cap_box[1] + y
        r, g, b = cp[x, y]
        if b < r * 0.6 and not (sx > 1262 and (sy < 690 or sx > 1279)):
            cp[x, y] = (0, 0, 0)
            ca[x, y] = (0, 0, 0, 0)
mask = cap_alpha.getchannel("A").point(lambda v: 255 if v > 10 else 0).filter(ImageFilter.MaxFilter(9))
scale = 1.6
size = (round(cap_rgb.width * scale), round(cap_rgb.height * scale))
cap_rgb, mask = cap_rgb.resize(size, Image.LANCZOS), mask.resize(size, Image.LANCZOS)
cap_layer = Image.new("RGBA", size)
cap_layer.paste(cap_rgb.convert("RGBA"), (0, 0), mask)
mark.alpha_composite(cap_layer, (1000 - size[0] - 70, 60))

for size, name in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"),
                   (48, "favicon-48.png"), (32, "favicon-32.png")]:
    save_png(mark.resize((size, size), Image.LANCZOS).convert("RGB"), name)
mark.resize((48, 48), Image.LANCZOS).convert("RGB").save(
    ROOT / "docs" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# — 1200×630 share card for Open Graph / Twitter / WhatsApp previews —
og = Image.new("RGB", (1200, 630), (0, 0, 0))
logo = on_black(FULL_BOX, 880)
og.paste(logo, ((1200 - logo.width) // 2, 150))
d = ImageDraw.Draw(og)
d.rectangle((0, 0, 1200, 8), fill=GOLD)
d.rectangle((0, 622, 1200, 630), fill=GOLD)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
except OSError:
    font = ImageFont.load_default()
line = "ASSIGNMENTS  ·  THESIS  ·  RESEARCH  ·  PRESENTATIONS  ·  EDITING"
w = d.textlength(line, font=font)
d.text(((1200 - w) / 2, 520), line, fill=(200, 200, 200), font=font)
og.save(OUT / "artspark-og.jpg", quality=88, optimize=True, progressive=True)

print("assets written to", OUT)
