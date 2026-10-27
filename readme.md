# Claude Skills
My notes and skills built with Claude. Hugo site using the Beautiful Hugo theme, hosted on Netlify.

- Hugo: v0.168.0 (extended)
- Theme: Beautiful Hugo (latest, Bootstrap 5), in `themes/beautifulhugo`
- Settings: `hugo.toml`

## Add a note
1. Copy `content/posts/_template.md` to a new file in `content/posts/`.
2. Fill in the title, date, tags and categories, and set `draft: false`.
3. Commit and push. Netlify rebuilds the site.

## Preview on Windows
Install Hugo once (in PowerShell):
```
winget install Hugo.Hugo.Extended
```
Then, inside this folder:
```
hugo server
```
Open http://localhost:1313 in your browser.

## Updating later
- Hugo on Netlify: change `HUGO_VERSION` in `netlify.toml`.
- Theme: `git submodule update --remote themes/beautifulhugo`
