#!/usr/bin/env python3
"""Draw a random zen ink-wash (水墨画) painting for a haiku post.

Usage:
  python3 tools/make_zen.py --season autumn --seed 42 --out /tmp/zen.png
  python3 tools/make_zen.py --season winter --random --out /tmp/zen.png
  python3 tools/make_zen.py --random --out /tmp/zen.png --webp static/flora/2026-11-23.webp

Writes a cropped PNG (about 400x600, portrait orientation for the blog).
Use --webp to also write a 400x600 WebP ready for static/flora/.

Needs: Python 3, numpy, Pillow. No GPU, no LaTeX, no AI model.

Scene vocabulary by season:
  spring  — gentle hills, light mist, birds returning, sparse blossoms
  summer  — layered mountains, vermilion sun, dense foliage, hazy
  autumn  — lone peak, dry texture strokes, bare pine, traveller, pagoda
  winter  — stark peak, heavy mist, bare branches, deep empty space

Based on cloveric/claude-drawing-skill inkpaint module (MIT).
"""
import argparse
import os
import random
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from inkpaint_engine import Painting, spline, curve, fbm1d


# ---------------------------------------------------------------- scene composers

def scene_spring(p, rng):
    """Gentle hills with mist, birds returning — fresh and open."""
    W, H = p.W, p.H
    p.paper()

    # distant hills, very faint
    far = p.ridge(int(H * 0.42), peaks=[
        (W * 0.25, H * 0.08, W * 0.22),
        (W * 0.70, H * 0.06, W * 0.18),
    ], rough=14)
    p.wash(far, dens=0.10, decay=H * 0.18, mist_y=H * 0.65)

    # mid hills
    mid = p.ridge(int(H * 0.52), peaks=[
        (W * 0.45, H * 0.10, W * 0.20),
        (W * 0.80, H * 0.07, W * 0.15),
    ], rough=18)
    p.wash(mid, dens=0.18, decay=H * 0.15)

    # soft mist band
    p.mist(H * 0.48, h=H * 0.07, strength=0.5)

    # a few birds returning
    n_birds = rng.integers(3, 6)
    bx = rng.uniform(W * 0.15, W * 0.55)
    by = rng.uniform(H * 0.12, H * 0.25)
    birds = []
    for i in range(n_birds):
        birds.append((
            bx + rng.uniform(-W * 0.06, W * 0.06),
            by + rng.uniform(-H * 0.03, H * 0.03),
            rng.uniform(0.6, 1.1)
        ))
    p.birds(birds)

    # a small foreground accent — moss dots on a low ridge
    fore = p.ridge(int(H * 0.82), peaks=[
        (W * 0.60, H * 0.04, W * 0.15),
    ], rough=10)
    p.wash(fore, dens=0.30, decay=H * 0.10, occlude=True)
    p.moss(fore, int(W * 0.45), int(W * 0.75), n=30)


def scene_summer(p, rng):
    """Layered mountains, vermilion sun, dense and hazy."""
    W, H = p.W, p.H
    p.paper()

    # vermilion sun
    sx = rng.uniform(W * 0.15, W * 0.40)
    sy = rng.uniform(H * 0.10, H * 0.20)
    p.sun(sx, sy, r=min(W, H) * 0.045)

    # three layers of mountains, far to near
    far = p.ridge(int(H * 0.35), peaks=[
        (W * 0.20, H * 0.10, W * 0.25),
        (W * 0.65, H * 0.12, W * 0.20),
        (W * 0.90, H * 0.07, W * 0.15),
    ], rough=20)
    p.wash(far, dens=0.12, decay=H * 0.20, mist_y=H * 0.55)

    mid = p.ridge(int(H * 0.48), peaks=[
        (W * 0.40, H * 0.14, W * 0.22),
        (W * 0.75, H * 0.10, W * 0.18),
    ], rough=24)
    p.wash(mid, dens=0.22, decay=H * 0.16, mist_y=H * 0.62)
    p.cun(mid, int(W * 0.25), int(W * 0.60), n=50, shadow_x=W * 0.35)

    near = p.ridge(int(H * 0.70), peaks=[
        (W * 0.55, H * 0.12, W * 0.20),
    ], rough=20)
    p.wash(near, dens=0.32, decay=H * 0.14)
    p.cun(near, int(W * 0.38), int(W * 0.72), n=70, shadow_x=W * 0.50)
    p.moss(near, int(W * 0.40), int(W * 0.70), n=40)

    # haze between layers
    p.mist(H * 0.42, h=H * 0.06, strength=0.55)
    p.mist(H * 0.60, h=H * 0.05, strength=0.4)

    # a couple of birds high up
    birds = [(rng.uniform(W * 0.55, W * 0.75), rng.uniform(H * 0.08, H * 0.18), s)
             for s in [rng.uniform(0.7, 1.0) for _ in range(2)]]
    p.birds(birds)


def scene_autumn(p, rng):
    """Lone peak, dry texture, pine or pagoda, traveller — solitary mood."""
    W, H = p.W, p.H
    p.paper()

    # a single dominant peak
    px = rng.uniform(W * 0.30, W * 0.55)
    peak = p.peak(px, H * 0.10, height=H * 0.50,
                  left_w=W * 0.22, right_w=W * 0.28, power=1.2,
                  shoulders=[(px - W * 0.18, H * 0.06, W * 0.10)],
                  rough=22)
    p.wash(peak, dens=0.28, decay=H * 0.18, tex=90)
    p.cun(peak, int(px - W * 0.22), int(px + W * 0.25), n=120, shadow_x=px - W * 0.05)
    p.moss(peak, int(px - W * 0.15), int(px + W * 0.15), n=50)
    p.ridge_line(peak, int(px - W * 0.20), int(px + W * 0.22))

    # distant faint ridge
    far = p.ridge(int(H * 0.45), peaks=[
        (W * 0.80, H * 0.06, W * 0.18),
    ], rough=12)
    p.wash(far, dens=0.10, decay=H * 0.15, mist_y=H * 0.55)

    # mist around the base
    p.mist(H * 0.55, h=H * 0.08, strength=0.6)

    # choose accent: pine, pagoda, or traveller
    accent = rng.choice(['pine', 'pagoda', 'traveller'])
    if accent == 'pine':
        root_x = rng.uniform(W * 0.65, W * 0.80)
        p.pine(
            root=(root_x, H * 0.78),
            top=(root_x - W * 0.02, H * 0.50),
            bend=W * 0.04,
            branches=[
                ((root_x - W * 0.01, H * 0.62), (root_x - W * 0.08, H * 0.56), -W * 0.015),
                ((root_x + W * 0.01, H * 0.55), (root_x + W * 0.07, H * 0.50), W * 0.01),
            ],
            trunk_w=max(8, int(W * 0.018)),
        )
    elif accent == 'pagoda':
        pg_x = rng.uniform(W * 0.70, W * 0.82)
        pg_y = peak[int(np.clip(pg_x, 0, W - 1))] + 8
        if pg_y < H * 0.75:
            p.pagoda(pg_x, pg_y)
    else:
        tv_x = rng.uniform(W * 0.68, W * 0.82)
        tv_y = H * 0.80
        p.traveller(tv_x, tv_y)

    # a bird or two
    if rng.random() > 0.4:
        p.birds([(rng.uniform(W * 0.60, W * 0.85), rng.uniform(H * 0.15, H * 0.30), rng.uniform(0.7, 1.0))])


def scene_winter(p, rng):
    """Stark peak, heavy mist, deep empty space — the most minimal."""
    W, H = p.W, p.H
    p.paper()

    # a stark, tall peak — high and narrow
    px = rng.uniform(W * 0.25, W * 0.45)
    peak = p.peak(px, H * 0.05, height=H * 0.55,
                  left_w=W * 0.15, right_w=W * 0.18, power=1.3,
                  rough=28)
    p.wash(peak, dens=0.22, decay=H * 0.14, tex=80, mist_y=H * 0.50, mist_h=H * 0.12)
    p.cun(peak, int(px - W * 0.15), int(px + W * 0.18), n=80, shadow_x=px - W * 0.05)

    # heavy mist swallows the base
    p.mist(H * 0.48, h=H * 0.10, strength=0.8)
    p.mist(H * 0.60, h=H * 0.07, strength=0.5)

    # a faint secondary ridge barely visible through mist
    if rng.random() > 0.3:
        far = p.ridge(int(H * 0.50), peaks=[
            (W * 0.75, H * 0.05, W * 0.15),
        ], rough=10)
        p.wash(far, dens=0.08, decay=H * 0.12)

    # minimal foreground: a rock or nothing
    if rng.random() > 0.5:
        rock_ridge = p.ridge(int(H * 0.85), peaks=[
            (W * 0.70, H * 0.04, W * 0.08),
        ], rough=8)
        p.rock(rock_ridge, dens=0.5, texture=20)

    # lone bird — or none at all
    if rng.random() > 0.5:
        p.birds([(rng.uniform(W * 0.55, W * 0.80), rng.uniform(H * 0.20, H * 0.35), rng.uniform(0.8, 1.1))])


SCENES = {
    'spring': scene_spring,
    'summer': scene_summer,
    'autumn': scene_autumn,
    'winter': scene_winter,
}


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="Draw a random zen ink-wash painting for a haiku post.")
    ap.add_argument("--season", choices=SCENES,
                    help="season mood (default: pick by month or random)")
    ap.add_argument("--seed", type=int,
                    help="random seed for reproducibility")
    ap.add_argument("--random", action="store_true",
                    help="random seed and season")
    ap.add_argument("--out", required=True,
                    help="output PNG path")
    ap.add_argument("--webp",
                    help="also write a 400x600 WebP (e.g. static/flora/2026-11-23.webp)")
    ap.add_argument("--width", type=int, default=540,
                    help="canvas width in px (default 540, portrait)")
    ap.add_argument("--height", type=int, default=810,
                    help="canvas height in px (default 810, portrait)")
    a = ap.parse_args()

    seed = a.seed if a.seed is not None else random.randint(1, 9999)

    if a.season:
        season = a.season
    elif a.random:
        season = random.choice(list(SCENES))
    else:
        # pick by current month
        import datetime
        m = datetime.date.today().month
        season = {12: 'winter', 1: 'winter', 2: 'winter',
                  3: 'spring', 4: 'spring', 5: 'spring',
                  6: 'summer', 7: 'summer', 8: 'summer',
                  9: 'autumn', 10: 'autumn', 11: 'autumn'}[m]

    rng = np.random.default_rng(seed)
    p = Painting(a.width, a.height, seed=seed)
    SCENES[season](p, rng)

    from PIL import Image
    img = p.composite()
    img.save(a.out)

    if a.webp:
        th = img.copy()
        th.thumbnail((400, 600), Image.LANCZOS)
        th.save(a.webp, "WEBP", quality=82, method=6)

    print(f"seed={seed} season={season} size={img.size} -> {a.out}")


if __name__ == "__main__":
    main()
