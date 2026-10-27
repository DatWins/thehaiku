---
title: Comments & Social
subtitle: Comment systems, social sharing, GitHub buttons, and footer icons
comments: false
---

Beautiful Hugo supports five comment systems, social sharing buttons, GitHub repository buttons, and 42 social icon links in the footer, plus custom icons of your own.

## Comment Systems

All comment systems are enabled per-page with `comments: true` in front matter. Only one comment system can be active at a time.

### Disqus

The classic comment system, integrated via Hugo's built-in Disqus support:

```toml
[Services]
  [Services.Disqus]
    Shortname = "your-disqus-shortname"

[Params]
  delayDisqus = true
```

`delayDisqus = true` defers loading until the user clicks a "Show comments" button, improving page load performance.

### Giscus

Giscus uses GitHub Discussions as a comment backend. It's privacy-friendly and requires no external service:

```toml
[Params.giscus]
  repo = "owner/repo"
  repoId = "R_kgDO..."
  category = "Announcements"
  categoryId = "DIC_kwDO..."
  mapping = "pathname"
  strict = "0"
  reactionsEnabled = "1"
  emitMetadata = "0"
  inputPosition = "top"
  theme = "preferred_color_scheme"
  lang = "en"
  lazyLoading = true
```

Get your configuration values from [giscus.app](https://giscus.app).

### Utterances

Utterances uses GitHub Issues as a comment backend — a lighter alternative to Giscus:

```toml
[Params.utterances]
  repo = "owner/repo"
  issueTerm = "pathname"
  theme = "preferred-color-scheme"
  label = "comment"
```

Get your configuration from [utteranc.es](https://utteranc.es).

### Cusdis

Cusdis is a lightweight, privacy-friendly comment system:

```toml
[Params]
  cusdisID = "your-app-id"
```

Get your App ID from [cusdis.com](https://cusdis.com).

### Staticman

Staticman adds comments as static data files via Git pull requests, with optional reCAPTCHA spam protection:

```toml
[Params.staticman]
  api = "https://your-staticman-instance.herokuapp.com/v3/entry/github/owner/repo/main/comments"

  [Params.staticman.recaptcha]
    sitekey = "your-site-key"
    secret = "your-secret"
```

## Social Share Buttons

Enable social sharing buttons on posts with `socialShare = true`. The buttons appear at the bottom of each post:

```toml
[Params]
  socialShare = true
```

The following platforms are supported:

| Platform | Icon |
|----------|------|
| Twitter / X | X logo |
| Facebook | Facebook logo |
| Reddit | Reddit logo |
| LinkedIn | LinkedIn logo |
| StumbleUpon | StumbleUpon logo |
| Pinterest | Pinterest logo |
| Email | Envelope icon |

Override per page:

```yaml
---
title: My Post
socialShare: false
---
```

## GitHub Buttons

Show GitHub repository buttons (star, watch, fork, follow) on any page using front matter:

```yaml
---
title: My Project
ghRepo: "halogenica/beautifulhugo"
ghBadge: ["star", "watch", "fork"]
ghCount: true
---
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `ghRepo` | string | — | GitHub repo in `owner/repo` format (per-page front matter only) |
| `ghBadge` | list | — | Which buttons to show: `star`, `watch`, `fork`, `follow`. Can be set per-page or site-wide via `Params.ghBadge` |
| `ghCount` | bool | `true` | Show count numbers on buttons. Can be set per-page or site-wide via `Params.ghCount` |

The buttons are loaded from [ghbtns.com](https://ghbtns.com) via lightweight iframes.

You can also set `ghBadge` and `ghCount` site-wide so they apply to every page that has a `ghRepo`:

```toml
[Params]
  ghBadge = ["star", "fork"]
  ghCount = true
```

## Footer Social Icons

Add social links under `[Params.author]` and they appear as icons in the footer. Beautiful Hugo supports 42 platforms:

| Key | Platform | URL Pattern |
|-----|----------|-------------|
| `email` | Email | `mailto:%s` |
| `facebook` | Facebook | `https://www.facebook.com/%s` |
| `github` | GitHub | `https://github.com/%s` |
| `gitlab` | GitLab | `https://gitlab.com/%s` |
| `git` | Git (custom URL) | `%s` (use full URL) |
| `bitbucket` | Bitbucket | `https://bitbucket.org/%s` |
| `twitter` | Twitter / X | `https://twitter.com/%s` |
| `slack` | Slack | `https://%s.slack.com/` |
| `reddit` | Reddit | `https://reddit.com/u/%s` |
| `linkedin` | LinkedIn | `https://linkedin.com/%s` |
| `xing` | Xing | `https://www.xing.com/profile/%s` |
| `stackoverflow` | Stack Overflow | `https://stackoverflow.com/%s` |
| `snapchat` | Snapchat | `https://www.snapchat.com/add/%s` |
| `instagram` | Instagram | `https://www.instagram.com/%s` |
| `youtube` | YouTube | `https://www.youtube.com/%s` |
| `soundcloud` | SoundCloud | `https://soundcloud.com/%s` |
| `spotify` | Spotify | `https://open.spotify.com/user/%s` |
| `bandcamp` | Bandcamp | `https://%s.bandcamp.com/` |
| `itchio` | itch.io | `https://itch.io/profile/%s` |
| `keybase` | Keybase | `https://keybase.io/%s` |
| `vk` | VK | `https://vk.com/%s` |
| `paypal` | PayPal | `https://paypal.me/%s` |
| `telegram` | Telegram | `https://telegram.me/%s` |
| `500px` | 500px | `https://500px.com/%s` |
| `codepen` | CodePen | `https://codepen.io/%s` |
| `kaggle` | Kaggle | `https://www.kaggle.com/%s` |
| `mastodon` | Mastodon | `https://%s` (use full URL; `rel="me"` for verification) |
| `weibo` | Weibo | `https://weibo.com/%s` |
| `medium` | Medium | `https://medium.com/@%s` |
| `discord` | Discord | `https://discord.gg/%s` |
| `strava` | Strava | `https://www.strava.com/athletes/%s` |
| `steam` | Steam | `https://steamcommunity.com/id/%s` |
| `quora` | Quora | `https://www.quora.com/profile/%s` |
| `amazonwishlist` | Amazon Wishlist | `https://amzn.com/w/%s` |
| `slideshare` | SlideShare | `https://www.slideshare.net/%s` |
| `angellist` | AngelList | `https://www.angel.co/p/%s` |
| `about` | Custom link | `%s` (use full URL) |
| `lastfm` | Last.fm | `https://www.last.fm/user/%s` |
| `bluesky` | Bluesky | `https://bsky.app/profile/%s` |
| `orcid` | ORCID | `https://orcid.org/%s` |
| `googlescholar` | Google Scholar | `https://scholar.google.com/citations?user=%s` |
| `goodreads` | Goodreads | `https://goodreads.com/%s` |

If a value starts with `http://` or `https://`, it is used directly as the URL. Otherwise, it is interpolated into the default URL pattern.

For **LinkedIn**, the value should include the path prefix (e.g. `in/username` for a personal profile or `company/username` for a company page). If you provide a bare username with no `/`, the theme automatically prepends `in/` for backward compatibility.

```toml
[Params.author]
  name = "Some Person"
  github = "username"
  linkedin = "in/username"
  mastodon = "https://mastodon.social/@username"
```

### Custom Icons

Platforms that are not in the table go under `[[Params.author.custom]]`. Each
entry carries its own link, label and icon class, and appears after the
built-in icons:

```toml
[[Params.author.custom]]
  href = "https://social.example/@username"
  title = "GoToSocial"
  icon = "ds-gotosocial"
  rel = "me"          # optional; "me" enables Fediverse link verification
```

`icon` is a CSS class. Any Font Awesome free class works with no further
setup. To use a different icon font, load its stylesheet from your own
`layouts/_partials/head_custom.html`.

#### Example: Fediverse icons

[Decentralized Social Icons](https://icons.wedistribute.org/) covers about 90
Fediverse platforms and protocols that Font Awesome does not, such as
GoToSocial, Friendica, Pixelfed, PeerTube and Lemmy. The theme does not ship
the font, because most sites do not need it, but a site can add it in three
steps.

1. Copy `DSoci.css`, `DSoci.woff2` and `DSoci.woff` from the
   [icon set](https://codeberg.org/WeDistribute/preview-decentralized-social-icons)
   into your site at `static/dsoci/`. Keep the `LICENSES` directory and the
   `.license` files with them: the set is [REUSE](https://reuse.software/)
   compliant, and each logo has its own copyright holder.

2. Load the stylesheet from `layouts/_partials/head_custom.html`:

   ```go-html-template
   <link rel="stylesheet" href="{{ "dsoci/DSoci.css" | relURL }}">
   ```

3. Add one entry per account. The class is `ds-` plus the project name:

   ```toml
   [[Params.author.custom]]
     href = "https://social.example/@username"
     title = "GoToSocial"
     icon = "ds-gotosocial"
     rel = "me"

   [[Params.author.custom]]
     href = "https://pixelfed.example/username"
     title = "Pixelfed"
     icon = "ds-pixelfed"
     rel = "me"
   ```

The icon font sets its own `font-size`. If a glyph looks too large or too
small next to the built-in icons, correct it in your own CSS:

```css
.footer-links [class^="ds-"] { font-size: 0.9em; }
```
