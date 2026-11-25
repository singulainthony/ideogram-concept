"""Prepare web images + asset data for the concept page.

Usage: python3 -I tools/prepare_assets.py <ideogram_download_dir>

Reads Ideogram's export (images + asset_data.csv) and writes:
  assets/img/<slug>.jpg        1600px long edge, for the lightbox
  assets/img/<slug>-sm.jpg     760px long edge, for the page
  assets/img/logo.png          logo cropped from the LinkedIn render
  assets/img/og.jpg            1200x630 social card
  data/assets.json             prompt + settings for every asset
"""
import csv
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1])
IMG = ROOT / "assets" / "img"
IMG.mkdir(parents=True, exist_ok=True)

# Order in the export -> slug, channel label, what it was for
META = {
    "0001": ("pinterest-tips", "Pinterest pin", "Evergreen tips content"),
    "0002": ("flatlay-monthly", "Local business post", "Monthly Tech Care plan"),
    "0003": ("facebook-cover", "Facebook page cover", "Brand promise"),
    "0004": ("linkedin-trust", "LinkedIn feed", "Social proof"),
    "0005": ("header-neighbourhood", "Social header", "Local identity"),
    "0006": ("holiday-gift", "Instagram post", "Seasonal gift offer"),
    "0007": ("curious-about-ai", "Landscape social", "AI lessons offer"),
    "0008": ("scam-alert-story", "Instagram / FB Story", "Scam-awareness PSA"),
    "0009": ("family-feed", "Instagram feed", "Hero brand image"),
}

LOGO_LOCK = (
    "Reproduce the North York Tech Help logo from the reference image exactly"
)


def save(im: Image.Image, path: Path, long_edge: int, quality: int) -> None:
    im = im.convert("RGB")
    im.thumbnail((long_edge, long_edge), Image.LANCZOS)
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


rows = list(csv.DictReader(open(SRC / "asset_data.csv", newline="", encoding="utf-8")))
out = []
for row in rows:
    key = row["filename"][:4]
    slug, channel, purpose = META[key]
    src = SRC / row["filename"]
    im = Image.open(src)
    w, h = im.size
    save(im, IMG / f"{slug}.jpg", 1600, 80)
    save(im, IMG / f"{slug}-sm.jpg", 760, 78)

    magic = json.loads(row["magic_prompt_output"])["instruction_caption"]
    out.append({
        "id": key,
        "slug": slug,
        "channel": channel,
        "purpose": purpose,
        "ratio": row["aspect_ratio"],
        "width": w,
        "height": h,
        "model": f"Ideogram {row['model']}",
        "rendering": row["rendering"],
        "magicPrompt": row["magic_prompt"],
        "seed": row["seed_number"],
        "prompt": row["prompt"],
        "logoLock": LOGO_LOCK in row["prompt"],
        "ideogramPlan": magic["high_level_instruction"],
        "keptTheSame": [c["desc"] for c in magic.get("content_that_stay_the_same", [])],
        "url": row["asset_url"],
    })

(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data" / "assets.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))

# Logo: the LinkedIn render has the cleanest logo on pure white (top-left).
li = Image.open(next(SRC.glob("0004_*.jpeg"))).convert("RGB")
logo = li.crop((70, 105, 450, 430))
logo.thumbnail((520, 520), Image.LANCZOS)
logo.save(IMG / "logo.png", optimize=True)

# OG card: paper background, headline on the left, three renders on the right.
from PIL import ImageDraw, ImageFont

FONTS = Path("/System/Library/Fonts/Supplemental")
og = Image.new("RGB", (1200, 630), (243, 239, 230))
d = ImageDraw.Draw(og)
serif = ImageFont.truetype(str(FONTS / "Georgia.ttf"), 68)
serif_i = ImageFont.truetype(str(FONTS / "Georgia Italic.ttf"), 68)
mono = ImageFont.truetype(str(FONTS / "Courier New Bold.ttf"), 20)
d.text((64, 70), "UNOFFICIAL CONCEPT", font=mono, fill=(185, 49, 15))
d.text((64, 140), "One logo in.", font=serif, fill=(22, 20, 15))
d.text((64, 222), "A whole", font=serif_i, fill=(185, 49, 15))
d.text((64, 304), "campaign out.", font=serif_i, fill=(185, 49, 15))
d.text((64, 520), "ANTHONY CARNEVALE", font=mono, fill=(22, 20, 15))
d.text((64, 550), "Made with Ideogram 4.0. Not affiliated.", font=mono, fill=(123, 116, 102))
x = 600
for p in ["family-feed", "scam-alert-story", "pinterest-tips"]:
    t = Image.open(IMG / f"{p}-sm.jpg")
    t.thumbnail((10_000, 470), Image.LANCZOS)
    og.paste(t, (x, 80))
    x += t.width + 18
og.save(IMG / "og.jpg", "JPEG", quality=86, optimize=True)

print(f"{len(out)} assets, logo-lock clause in {sum(a['logoLock'] for a in out)}/{len(out)} prompts")
print("ratios:", sorted({a['ratio'] for a in out}))
print("rendering:", [a["rendering"] for a in out])
words = [len(a["prompt"].split()) for a in out]
print("prompt words:", words, "avg", sum(words) // len(words))
