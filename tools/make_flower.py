#!/usr/bin/env python3
"""Draw a watercolour flower spray with tikz-flora (MIT) for a haiku post.

Usage:
  python3 tools/make_flower.py --season autumn --seed 1234 --out /tmp/flower.png
  python3 tools/make_flower.py --season autumn --random --out /tmp/flower.png

Writes a transparent, cropped PNG at full size (about 460x670 px). Then
either shrink it straight into static/flora/ with --webp, or add a bird
with tools/add_bird.py.

Needs: lualatex, pdftocairo, git, Python Pillow. See HANDOFF.md.
"""
import argparse, os, random, shutil, subprocess, sys, tempfile
from PIL import Image

PALETTES = {
    "spring": [("hero=violet,blooms=violet,leaves=green,stems=earth,sprays=violet", "lily=0")],
    "summer": [("hero=teal,blooms=blue,leaves=green,stems=earth,sprays=teal", "")],
    "autumn": [("hero=warm,blooms=warm,leaves=earth,stems=earth,sprays=gold", "umbel=0"),
               ("hero=gold,blooms=warm,leaves=earth,stems=earth,sprays=gold", "umbel=0"),
               ("hero=earth,blooms=warm,leaves=green,stems=earth,sprays=warm", "gyps=0")],
    "winter": [("hero=blue-grey,blooms=blue-grey,leaves=teal,stems=earth,sprays=blue-grey", "gyps=2")],
}
NO_ORNAMENTS = ",".join(k + "=0" for k in (
    "night sun moon constellation planet armillary scrolled strapwork compass rosette "
    "sunburst quatrefoil knot medallion zodiac_pendant gilt_cross gilt_rosette gilt_dotted "
    "gilt_lozenge gilt_star gilt_crescent gilt_trefoil sun_crest compass_rose armillary_crest "
    "zodiac wreath swash fleuron_rule headpiece cul_de_lampe hedera garland bracket fan corner_leaf").split())

# Three package features that look wrong on the blog; switched off in a local copy.
PATCHES = [
    ('local excursion = not spec.frame_only and Layout.excursion(rng:fork("excursion"), spec, root)',
     'local excursion = nil -- blog: no tendril into the text block'),
    ('for k, rn in ipairs(runs) do', 'for k, rn in ipairs({}) do -- blog: no gilt chain'),
    ('local sparkles = Fill.sparkles(rng:fork("sparkles"), g, 40, spec.ornaments)',
     'local sparkles = {} -- blog: no sparkles'),
]

def setup(work):
    repo = os.path.join(work, "tikz-flora")
    if not os.path.isdir(repo):
        subprocess.run(["git", "clone", "-q", "--depth", "1",
                        "https://github.com/wn-mitch/tikz-flora", repo], check=True)
    build = os.path.join(work, "build")
    if not os.path.isdir(build):
        os.makedirs(build)
        shutil.copy(os.path.join(repo, "tex", "tikzflora.sty"), build)
        shutil.copy(os.path.join(repo, "tex", "tikzflora-boot.lua"), build)
        shutil.copytree(os.path.join(repo, "lua"), os.path.join(build, "lua"))
        p = os.path.join(build, "lua", "flora", "compose.lua")
        s = open(p).read()
        for old, new in PATCHES:
            if s.count(old) != 1:
                sys.exit(f"compose.lua changed upstream; patch by hand: {old[:50]}...")
            s = s.replace(old, new)
        open(p, "w").write(s)
    return build

def render(build, name, body, papers):
    tex = os.path.join(build, name + ".tex")
    open(tex, "w").write(papers + body)
    for _ in range(2):
        subprocess.run(["lualatex", "-interaction=nonstopmode", name + ".tex"], cwd=build,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["pdftocairo", "-png", "-r", "150", "-transp", "-singlefile",
                    name + ".pdf", name], cwd=build, check=True)
    im = Image.open(os.path.join(build, name + ".png")).convert("RGBA")
    return im.crop(im.getbbox())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", choices=PALETTES, default="autumn")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--random", action="store_true", help="random seed and palette variant")
    ap.add_argument("--out", required=True, help="output PNG (full size, transparent)")
    ap.add_argument("--webp", help="also write a 400x600 WebP here (e.g. static/flora/2026-11-02.webp)")
    ap.add_argument("--work", default=os.path.join(tempfile.gettempdir(), "haiku-flora"))
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else random.randint(1, 9999)
    pal, mix = random.choice(PALETTES[a.season]) if a.random else PALETTES[a.season][0]
    build = setup(a.work)
    head = ("\\documentclass{article}\n"
            "\\usepackage[paperwidth=9cm,paperheight=13cm,left=7.5cm,right=0.5cm,top=0.5cm,bottom=0.5cm]{geometry}\n"
            "\\usepackage{tikzflora}\n\\pagestyle{empty}\n")
    body = (f"\\florasetup{{seed={seed}, layout=left, density=0.7, ornaments={{{NO_ORNAMENTS}}},\n"
            f"  palette={{{pal}}}, mix={{{mix}}}}}\n\\begin{{document}}\n\\mbox{{}}\n\\end{{document}}\n")
    im = render(build, f"flower{seed}", body, head)
    im.save(a.out)
    if a.webp:
        th = im.copy(); th.thumbnail((400, 600), Image.LANCZOS)
        th.save(a.webp, "WEBP", quality=82, method=6)
    print(f"seed={seed} season={a.season} size={im.size} -> {a.out}")

if __name__ == "__main__":
    main()
