---
title: Shortcodes
subtitle: Built-in shortcodes with live examples
comments: false
---

Beautiful Hugo ships with several shortcodes for common patterns like collapsible sections, multi-column layouts, tabbed content, image galleries, videos, and diagrams.

## callout

The `callout` shortcode renders a Bootstrap alert-based callout box. It supports multiple paragraphs and an optional title. Nine styles are available, matching Bootstrap 5's alert classes: `primary`, `secondary`, `info` (default), `warning`, `danger`, `success`, `light`, `dark`, and `note` (a custom grey style).

| Parameter | Position | Required | Description |
|-----------|----------|----------|-------------|
| type | 1 | no | Callout style: `primary`, `secondary`, `info` (default), `warning`, `danger`, `success`, `light`, `dark`, `note` |
| title | 2 | no | Optional heading text (supports Markdown) |
| (inner) | — | yes | The body content (supports Markdown, multiple paragraphs) |

**Live examples:**

{{< callout info "Information" >}}
This is an **info** callout — the default style. Use it for helpful tips or informational asides.

You can include multiple paragraphs, **formatted text**, and even code: `console.log("hello")`.
{{< /callout >}}

{{< callout primary "Primary" >}}
This is a **primary** callout. Use it for key points or branded highlights.
{{< /callout >}}

{{< callout secondary "Secondary" >}}
This is a **secondary** callout. Use it for less prominent asides.
{{< /callout >}}

{{< callout warning "Caution" >}}
This is a **warning** callout. Use it to flag potential issues or important caveats.
{{< /callout >}}

{{< callout danger "Critical" >}}
This is a **danger** callout. Use it for critical errors or destructive actions.
{{< /callout >}}

{{< callout success "All good" >}}
This is a **success** callout. Use it for confirmation messages or completed actions.
{{< /callout >}}

{{< callout light "Light" >}}
This is a **light** callout. Use it for subtle, low-emphasis notes. It adapts its palette in dark mode.
{{< /callout >}}

{{< callout dark "Dark" >}}
This is a **dark** callout. Use it for high-contrast, bold asides. It adapts its palette in dark mode.
{{< /callout >}}

{{< callout note >}}
This is a **note** callout — a neutral grey style for side remarks that don't fit the other categories.
{{< /callout >}}

**Source:**

```markdown
{{</* callout info "Information" */>}}
This is an **info** callout — the default style.

You can include multiple paragraphs.
{{</* /callout */>}}

{{</* callout primary "Primary" */>}}
This is a **primary** callout.
{{</* /callout */>}}

{{</* callout secondary "Secondary" */>}}
This is a **secondary** callout.
{{</* /callout */>}}

{{</* callout warning "Caution" */>}}
This is a **warning** callout.
{{</* /callout */>}}

{{</* callout danger "Critical" */>}}
This is a **danger** callout.
{{</* /callout */>}}

{{</* callout success "All good" */>}}
This is a **success** callout.
{{</* /callout */>}}

{{</* callout light "Light" */>}}
This is a **light** callout.
{{</* /callout */>}}

{{</* callout dark "Dark" */>}}
This is a **dark** callout.
{{</* /callout */>}}

{{</* callout note */>}}
This is a **note** callout (no title).
{{</* /callout */>}}
```

The `type` parameter defaults to `info`, so `{{</* callout */>}}` is equivalent to `{{</* callout info */>}}`. The title parameter is optional — omit it for a title-less callout.

## details

The `details` shortcode renders a collapsible `<details>` element. The first positional parameter is the summary text; the inner content is the body.

| Parameter | Position | Required | Description |
|-----------|----------|----------|-------------|
| summary | 1 | yes | The clickable summary label (supports Markdown) |
| (inner) | — | yes | The expandable body content (supports Markdown) |

**Live example:**

{{< details "Click to expand this section" >}}
This content is hidden by default. You can use **Markdown** here, and even code:

```python
def hello():
    print("Hello from inside a details block!")
```
{{< /details >}}

**Source:**

```markdown
{{</* details "Click to expand this section" */>}}
This content is hidden by default. You can use **Markdown** here.
{{</* /details */>}}
```

## columns / column

The `columns` and `column` shortcodes create a two-column layout using the `splitbox` CSS class. `columns` is a paired shortcode; `column` marks the boundary between the left and right column.

| Shortcode | Purpose |
|-----------|---------|
| `{{</* columns */>}}` | Opens the two-column wrapper and starts the left column |
| `{{</* column */>}}` | Closes the left column and starts the right column |
| `{{</* /columns */>}}` | Closes the right column and the wrapper |

For historical reasons, you can also use
`{{</* columns /*/>}} ... {{</* endcolumns */>}}`
(note the required self-closing tag) as a backward compatibility shim.
{{< callout warning "Backward compatibility" >}}
The `columns`/`endcolumns` self-closing syntax is deprecated and may be removed in a future release.
{{< /callout >}}

**Live example:**

{{< columns >}}
Left column content. This is great for side-by-side comparisons, like showing a configuration option next to its effect.

- Bullet points work
- **Bold text** works
- [Links](/) work

{{< column >}}
Right column content. Each column takes roughly 48% of the available width.

```toml
[Params]
  colorScheme = "auto"
```
{{< /columns >}}

**Source:**

```markdown
{{</* columns */>}}
Left column content here.
{{</* column */>}}
Right column content here.
{{</* /columns */>}}
```

## tabs / tab

The `tabs` and `tab` shortcodes render a Bootstrap 5 tabbed interface. Tabs with the same `groupId` across different blocks will switch in sync.

| Shortcode | Parameter | Required | Description |
|-----------|-----------|----------|-------------|
| `tabs` | `groupId` | no | Group identifier for tab synchronization |
| `tab` | name (positional) | yes | Display label for the tab button |

**Live example — three tabs:**

{{< tabs groupId="config-format" >}}
{{< tab "TOML" >}}
```toml
[Params]
  subtitle = "My Site"
  colorScheme = "auto"
```
{{< /tab >}}
{{< tab "YAML" >}}
```yaml
Params:
  subtitle: "My Site"
  colorScheme: "auto"
```
{{< /tab >}}
{{< tab "JSON" >}}
```json
{
  "Params": {
    "subtitle": "My Site",
    "colorScheme": "auto"
  }
}
```
{{< /tab >}}
{{< /tabs >}}

**Synchronized tabs** — click a tab below and watch the one above switch too:

{{< tabs groupId="config-format" >}}
{{< tab "TOML" >}}
TOML is the default format for Hugo config files.
{{< /tab >}}
{{< tab "YAML" >}}
YAML is also supported by Hugo.
{{< /tab >}}
{{< tab "JSON" >}}
JSON works too, though it's less common for config.
{{< /tab >}}
{{< /tabs >}}

**Source:**

```markdown
{{</* tabs groupId="config-format" */>}}
{{</* tab "TOML" */>}}
  ... content ...
{{</* /tab */>}}
{{</* tab "YAML" */>}}
  ... content ...
{{</* /tab */>}}
{{</* tab "JSON" */>}}
  ... content ...
{{</* /tab */>}}
{{</* /tabs */>}}
```

To synchronize tabs across multiple blocks, give them the same `groupId`:

```markdown
{{</* tabs groupId="config-format" */>}}
{{</* tab "TOML" */>}} ... {{</* /tab */>}}
{{</* tab "YAML" */>}} ... {{</* /tab */>}}
{{</* /tabs */>}}

{{</* tabs groupId="config-format" */>}}
{{</* tab "TOML" */>}} ... {{</* /tab */>}}
{{</* tab "YAML" */>}} ... {{</* /tab */>}}
{{</* /tabs */>}}
```

## beautifulfigure

The `beautifulfigure` shortcode renders a PhotoSwipe-enhanced figure with lightbox support, captions, attribution, and effects. See [Figures & Galleries](../figures-and-galleries/#beautifulfigure) for the full parameter reference and live examples.

## figure

The `figure` shortcode is a router. By default it delegates to `beautifulfigure` (PhotoSwipe-enhanced). When `disableFigureOverride = true` is set in your config, it uses Hugo's standard `<figure>` shortcode instead.

See [Figures & Galleries](../figures-and-galleries/) for details on the routing behavior and the `disableFigureOverride` flag.

## gallery

The `gallery` shortcode renders an image gallery grid with PhotoSwipe support. It supports manual mode (place `beautifulfigure` shortcodes inside) and directory mode (auto-populate from a directory). See [Figures & Galleries](../figures-and-galleries/#gallery) for the full parameter reference and live examples.

## video

The `video` shortcode embeds a self-hosted video file in a `<figure>` that scales with the page width, with an optional caption. It uses the browser's native player. For YouTube and Vimeo, use Hugo's built-in `youtube` and `vimeo` shortcodes.

Paths resolve like `beautifulfigure`: page bundle resources and files under `assets/` are published by Hugo, paths that start with `/` are served from `static/`, and remote URLs pass through. A `poster` image from a page bundle or `assets/` is resized to at most 1280 pixels wide.

**Live example:**

{{< video src="/video/sample.mp4" poster="/video/sample-poster.jpg" width="480px" caption="A generated colour gradient, 8 seconds long and silent" attr="ffmpeg gradients" attrlink="https://ffmpeg.org/" >}}

**Source:**

```markdown
{{</* video src="/video/sample.mp4" poster="/video/sample-poster.jpg" width="480px" caption="A generated colour gradient, 8 seconds long and silent" attr="ffmpeg gradients" attrlink="https://ffmpeg.org/" */>}}
```

A muted, looping clip that starts on its own works as an animated image replacement:

```markdown
{{</* video src="demo.webm" autoplay=true loop=true controls=false */>}}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `src` (or first positional) | string | — | Video file. Required |
| `type` | string | from extension | MIME type of the source, e.g. `video/webm` |
| `poster` | string | — | Image shown before playback |
| `width` | string | — | CSS `max-width` of the figure, e.g. `480px` or `50%` |
| `caption` | string | — | Caption text (supports Markdown) |
| `title` | string | — | Heading above the caption |
| `attr`, `attrlink` | string | — | Attribution text and optional link |
| `alt` | string | — | Accessible name for the video element |
| `controls` | bool | `true` | Show the browser's playback controls |
| `autoplay` | bool | `false` | Start playback automatically. Implies `muted`, which browsers require for autoplay |
| `loop` | bool | `false` | Restart the video when it ends |
| `muted` | bool | `false` | Start with the sound off |
| `playsinline` | bool | `true` | Play in the page on mobile. Set to `false` to let iOS open the full-screen player |
| `preload` | string | browser default | `none`, `metadata`, or `auto` |
| `track` | string | — | WebVTT captions file, shown by default |
| `trackLang` | string | — | Language code of the captions file |
| `class` | string | — | Extra CSS classes on the figure |

When the browser cannot play the file, a download link is shown in its place. The link text comes from the `videoUnsupported` i18n key.

## icon

The `icon` shortcode renders a Font Awesome icon inline, so markdown content can use the icons the theme already loads. Give it the class list of the icon. Hugo does not allow positional and named arguments together, so use `class="..."` as soon as you add another argument. Add `label` when the icon carries meaning of its own; without it the icon is hidden from screen readers.

**Live example:**

Download the {{< icon "fas fa-file-pdf" >}} PDF guide, or read it on {{< icon class="fab fa-github" label="GitHub" >}}.

**Source:**

```markdown
Download the {{</* icon "fas fa-file-pdf" */>}} PDF guide, or read it on {{</* icon class="fab fa-github" label="GitHub" */>}}.
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `class` (or first positional) | string | — | Font Awesome class list, e.g. `fas fa-file-pdf` |
| `label` | string | — | Accessible name. Omit it for a decorative icon |
| `style` | string | — | Inline CSS, e.g. `color: green` |

## mermaid

The `mermaid` shortcode renders Mermaid diagrams (flowcharts, sequence diagrams, Gantt charts, etc.) with automatic light/dark mode handling via dual-rendering. It accepts an optional `align` parameter (`center`, `left`, or `right`).

A ` ```mermaid ` fenced code block gives the same result through a codeblock render hook, and is the recommended form. The shortcode stays available.

See [Math & Diagrams](../math-and-diagrams/) for live examples and source code.

## no-ai-summary

The `no-ai-summary` shortcode wraps content in a `<div data-nosnippet>` element, telling search engines not to use that content for AI-generated summaries or snippets.

**Live example:**

{{< no-ai-summary >}}
This text is wrapped in `data-nosnippet` and should not appear in search engine AI summaries.
{{< /no-ai-summary >}}

**Source:**

```markdown
{{</* no-ai-summary */>}}
This text is wrapped in `data-nosnippet` and should not appear in search engine AI summaries.
{{</* /no-ai-summary */>}}
```

See [SEO & i18n](../seo-and-i18n/) for the full robot meta tags and AI summary limit configuration.

## publications

The `publications` shortcode lists every `type: publication` page on the site, grouped by year, with the same markup as a publication section list. Use it to place the list on a regular page, such as a research group page.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `section` | all | Only list pages from this content section |
| `links` | `true` | Set to `false` to hide the DOI, PDF, and other links |

**Live example:**

{{< publications links=false >}}

**Source:**

```markdown
{{</* publications links=false */>}}
```

See [Configuration — Publication Pages](../configuration/#publication-pages) for the page type itself.

## include-code

The `include-code` shortcode reads a source file from disk and renders it with syntax highlighting. It supports auto-detection of the language from the file extension, line numbers, and line highlighting (Chroma only).

See [Code Blocks — Including External Files](../code-blocks/#including-external-files) for the full parameter reference and live examples.
