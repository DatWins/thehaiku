---
title: Bundled big image
subtitle: A header image that lives next to the post
date: 2026-05-12
tags: ["example"]
thumbnail: forest.jpg
bigimg:
  - src: forest.jpg
    desc: "A page resource"
---

This post is a [page bundle](https://gohugo.io/content-management/page-bundles/). The `bigimg` entry `forest.jpg` is resolved as a page resource, so the image can live in the same directory as `index.md`.

Images in a bundle are also processed by Hugo. The `thumbnail` above is cropped to a square for the post list, the header image is capped at `bigimgWidth`, and the figure and gallery below get resized variants with a `srcset`:

{{< beautifulfigure src="forest.jpg" caption="A page-resource figure with automatic sizes" width="50%" class="center" >}}

{{< gallery dir="photos" caption-effect="fade" />}}

Plain Markdown images get the same treatment. This one is a page resource, so it has a `srcset`:

![A page-resource Markdown image](forest.jpg "Forest")

A `width` attribute on the next line sets the display size and caps the generated variants:

![A 300 pixel Markdown image](forest.jpg)
{width=300}

This one is under `static/`, so it is served unchanged:

![A static Markdown image](/img/global-ike.png)
