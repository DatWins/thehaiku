#!/usr/bin/env python3
"""Put a chickadee onto a flower spray and save the post's picture.

Usage:
  python3 tools/add_bird.py FLOWER.png --pose 1-flight --at 322 96 --width 240 --flip \
      --out static/flora/2026-10-26-first.webp --preview /tmp/check.jpg

--at X Y   where the bird's feet (or body, for flyaway) go, in FLOWER.png pixels
           (FLOWER.png is the full-size output of make_flower.py, about 460x670).
           Aim at the top edge of a petal for a landing/hovering bird, or a
           stem/leaf edge for a perched bird on its twig.
--width    bird width in px (about 230-320 looks right on a 460 px spray).
--flip     mirror the bird so it faces left (toward a flower on its left).
--pad L T R B  extra transparent room around the spray if the bird sticks out.
Always open --preview and adjust --at/--width until the bird really sits on
the flower, the way a person would place it.

Bird art: the Chickadee project (Apache-2.0), tools/birds/.
"""
import argparse, os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
# Anchor = feet (or body) position in the original 1122x1402 pose image;
# erase = (x, y): clear everything right of x and below y (removes the drawn branch).
POSES = {
    "1-flight":      {"anchor": (457, 657), "erase": (520, 800)},
    "2-landing":     {"anchor": (560, 830), "erase": (500, 835)},
    "3-perched":     {"anchor": (600, 1050), "erase": None},   # keeps its twig
    "4-tilt":        {"anchor": (600, 1050), "erase": None},   # keeps its twig
    "5-sing-open":   {"anchor": (623, 985), "erase": None},    # keeps its twig
    "6-sing-closed": {"anchor": (623, 985), "erase": None},    # keeps its twig
    "7-preen":       {"anchor": (623, 985), "erase": None},    # keeps its twig
    "8-flyaway":     {"anchor": (582, 540), "erase": None},    # no branch
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("flower")
    ap.add_argument("--pose", choices=POSES, required=True)
    ap.add_argument("--at", type=int, nargs=2, required=True)
    ap.add_argument("--width", type=int, default=240)
    ap.add_argument("--flip", action="store_true")
    ap.add_argument("--pad", type=int, nargs=4, default=(0, 110, 90, 0))
    ap.add_argument("--out", required=True)
    ap.add_argument("--preview")
    a = ap.parse_args()
    p = POSES[a.pose]
    fl = Image.open(a.flower).convert("RGBA"); fl = fl.crop(fl.getbbox())
    l, t, r, b = a.pad
    can = Image.new("RGBA", (fl.width + l + r, fl.height + t + b)); can.alpha_composite(fl, (l, t))
    bd = Image.open(os.path.join(HERE, "birds", a.pose + ".webp")).convert("RGBA")
    if p["erase"]:
        x0, y0 = p["erase"]; px = bd.load()
        for y in range(y0, bd.height):
            for x in range(x0, bd.width): px[x, y] = (0, 0, 0, 0)
    ax, ay = p["anchor"]
    if a.flip:
        bd = ImageOps.mirror(bd); ax = bd.width - ax
    s = a.width / bd.width
    bd = bd.resize((a.width, round(bd.height * s)), Image.LANCZOS)
    x = l + a.at[0] - round(ax * s); y = t + a.at[1] - round(ay * s)
    can.paste(bd, (x, y), bd) if (x < 0 or y < 0) else can.alpha_composite(bd, (x, y))
    can = can.crop(can.getbbox())
    if a.preview:
        bg = Image.new("RGBA", can.size, (239, 233, 220, 255)); bg.alpha_composite(can)
        bg.convert("RGB").save(a.preview, quality=85)
    th = can.copy(); th.thumbnail((400, 600), Image.LANCZOS)
    th.save(a.out, "WEBP", quality=82, method=6)
    print(f"{a.pose} at {a.at} width {a.width} -> {a.out}")

if __name__ == "__main__":
    main()
