# Handoff: "the haiku" blog

Read this first if you are an agent (or a person) picking up work on this
site. It records how the site looks the way it does and how to add a
flower-and-bird picture to a new post. Everything here was built with the
owner (GitHub: DatWins) in Claude sessions on 30 Oct to 1 Nov 2026.

The owner is not a programmer. Do the work, check it, push it, and explain
the result in plain words. They review on a Windows PC and an Android phone.

## The site

- Repo: `DatWins/thehaiku`, branch `main`.
- Live: https://datwins.github.io/thehaiku/ (note the `/thehaiku/` subpath).
- Hugo 0.168.0 extended, theme Beautiful Hugo as a git submodule in
  `themes/beautifulhugo` (never edit the theme; override in `layouts/` and CSS).
- Deploy: `.github/workflows/hugo.yml` builds and publishes to GitHub Pages
  on every push to `main` (about a minute). Pages source is "GitHub Actions".
  Netlify was removed on purpose; don't bring it back.
- Posts: `content/posts/YYYY-MM-DD.md`. Title is the date, `categories` is
  the season (spring / summer / autumn / winter), `tags` is the form
  (haiku / tanka / haibun). New posts start from `content/posts/_template.md`.

## The look (all in `static/css/haiku.css` unless noted)

- Linen paper background `static/textures/linen.webp` on `html` and `body`
  (with `!important`, because the theme sets a white body).
- All image URLs in the CSS are relative to the CSS file (`../flora/...`,
  `../birds/...`, `../textures/...`). Root paths like `/textures/x.webp`
  break because the site lives under `/thehaiku/`. This was the cause of
  an early "background doesn't change" bug.
- Header (home title): a watercolour wreath frame drawn with tikz-flora,
  `static/flora/header-frame-wide.webp` (screens 768 px and up) and
  `header-frame-tall.webp` (phones), set as the background of
  `.intro-header .page-heading` with padding so the title sits inside. On
  phones the title is smaller (1.55rem) so it fits the tall frame.
- A chickadee landing on the frame's top-left red flower:
  `static/birds/chickadee-landing.webp`, drawn as
  `.intro-header .page-heading::before`, positioned in percentages of the
  framed box so it stays on that flower at every width. The owner loved
  this ("the bird is spot on"); don't move it without being asked.
- Navbar name "the haiku" is big and bold; the home title is smaller
  Cormorant Garamond italic; the small date line over each poem
  (`.post-preview h2.post-title`) is bold and dark.
- Footer: transparent (shows the linen); the copyright line was removed by
  `layouts/_partials/footer.html` (a copy of the theme's footer). The
  theme-credit line stays.
- Each post's picture: front matter `image: "/flora/<file>.webp"`.
  The front page shows it beside the poem (above it on phones) in full
  colour (the theme's grey filter and square crop are overridden), and
  `layouts/_partials/before_content.html` shows it above the poem on the
  post's own page.

## Picture for each post: a flower spray with its own chickadee

Current posts:

| Post | Picture | Bird |
|---|---|---|
| 2026-10-26 "empty notebook" | `static/flora/2026-10-26-first.webp` | 1-flight, flipped, hovering at the red flower |
| 2026-10-25 "morning commute" | `static/flora/2026-10-25.webp` | 5-sing-open, flipped, on its twig by the green flower |
| 2026-10-20 "rain on the window" | `static/flora/2026-10-20.webp` | 8-flyaway, leaving the top of the spray |

Plain sprays without birds, for reuse: `static/flora/flora-spring.webp`,
`flora-summer`, `flora-autumn`, `flora-autumn2`, `flora-autumn3`,
`flora-winter`.

### Adding one to a new post

1. Needs `lualatex`, `pdftocairo`, `git`, Python with Pillow. Run from the
   repo root.
2. Draw the flower (random seed, colours for the post's season):

   ```bash
   python3 tools/make_flower.py --season autumn --random --out /tmp/flower.png
   ```

   It prints the seed; keep it if the owner likes the drawing.
3. Put a chickadee on it, using a pose not used by the posts next to it:

   ```bash
   python3 tools/add_bird.py /tmp/flower.png --pose 1-flight --flip \
     --at 320 90 --width 240 \
     --out static/flora/2026-11-02.webp --preview /tmp/check.jpg
   ```

   Open `/tmp/check.jpg` and adjust `--at X Y` (where the feet go, in
   flower pixels) and `--width` until the bird truly lands on a petal or
   its twig meets a stem. Look at it every time; numbers alone are not
   enough. Poses: `1-flight`, `2-landing` (both have their branch erased),
   `8-flyaway` (no branch), and `3-perched`, `4-tilt`, `5-sing-open`,
   `6-sing-closed`, `7-preen` (they keep their twig; place the twig so it
   joins the plant). `--flip` turns the bird to face left.
4. In the post's front matter set `image: "/flora/2026-11-02.webp"`.
5. Check before pushing: download Hugo 0.168.0 extended from GitHub
   releases, build with `--baseURL http://localhost:8137/thehaiku/`, serve
   the output inside a `thehaiku/` folder, and screenshot with Playwright at
   1440 px and 390 px. Offline, Bootstrap and Google Fonts don't load, so
   the menu and fonts look plain; judge only the pictures.
6. Commit and push to `main`; tell the owner to refresh (Ctrl+F5).

### Season colours used by `make_flower.py`

- spring: violet hero and blooms, green leaves
- summer: teal and blue
- autumn: warm red / gold / earth (three variants, picked by `--random`)
- winter: blue-grey with teal leaves

### Header frame (if it ever needs redrawing)

tikz-flora `layout=surround`, seed 19, `density=0.6`, every ornament weight
0, `palette={hero=warm,blooms=violet,leaves=green,leaflets=earth,stems=earth,sprays=gold}`,
`mix={umbel=0}`, rendered at 110 dpi with `-transp`:
- wide: paper 28 x 12 cm, margin 3 cm
- tall: paper 12 x 18 cm, margin 2.6 cm

Use the same patched build folder that `make_flower.py` sets up.
If the frame changes, re-check the landing bird's position over the red
flower (its `left`/`top` in `haiku.css`).

## Where the art comes from

- Flowers and frames: tikz-flora, MIT, https://github.com/wn-mitch/tikz-flora
  (written with Claude Code by its author). `make_flower.py` switches off three
  of its page decorations in a local copy (a long tendril into the text area,
  a dotted gold chain, sparkles) because they look wrong on the blog.
- Chickadees: the Chickadee project's illustrations (Apache-2.0,
  github.com/sahilmahendrakar/chickadee), copied into `tools/birds/` with its
  licence. Credit both in commit messages.
- Claude cannot paint new illustrations; it can only draw with tikz-flora
  and reuse these birds. The owner is also looking for public-domain art
  (e.g. Hokusai prints on Wikimedia Commons) and has Pixabay photos in mind,
  but photos don't match the drawn style.

## Known small things

- `readme.md` still says "Claude Skills" at the top (copied from another
  blog); it could be renamed to "the haiku".
- `static/img/fuji.svg` and `static/poetry-template.html` are no longer used.
- A Claude skill called **haiku-flower-drawing** was written for adding a
  flower to a post; this file is the fuller, current version of that recipe,
  including the birds.
