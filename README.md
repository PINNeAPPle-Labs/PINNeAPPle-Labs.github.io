# pinneapple-labs-site

Landing site for **PINNeAPPle Labs**, open-source Physics AI with verification as part of the
product. Served at <https://pinneapple-labs.github.io/>.

A commercial home, the product page for **PINNeAPPle Engineering** (with a "coming soon" badge),
an articles section with one post per experiment, and the library page, in two languages,
generated from one script.

## Build

```bash
python3 build.py
```

That writes:

| path | page |
|---|---|
| `index.html` | home (pt-BR) |
| `en/index.html` | home (English) |
| `engineering/index.html` · `en/engineering/` | PINNeAPPle Engineering, the product, coming soon |
| `artigos/index.html` · `en/artigos/` | article index, newest first |
| `artigos/<slug>/index.html` · `en/artigos/<slug>/` | one post per experiment, from the `POSTS` list |
| `lib/index.html` · `en/lib/` | architecture, quickstart, open-source split |
| `casos-de-uso/`, `historia/` (+ `en/`) | redirect stubs to `/artigos/` and `/#historia`; the old URLs keep working |

`build.py` also regenerates `sitemap.xml`. Commit the generated HTML along with the script:
GitHub Pages serves the files as they are, there is no build step on the server.

## What lives where

| file | what it is |
|---|---|
| `build.py` | the whole source: page text (pt/en), the shared shell, the nav, the footer, the floating WhatsApp button |
| `styles.css` | the design system: tokens, layout, components, the sticky button |
| `app.js` | nav toggle, copy-to-clipboard, code tabs, scroll reveal, section spy, lazy video playback |
| `fonts.css`, `fonts/` | self-hosted Archivo + JetBrains Mono (latin subset, OFL) |
| `img/` | product and capability stills; `img/results/` holds real result plots |
| `videos/` | hero clip, two base-app recordings and the two Studio tours (`studio-pt.mp4`, `studio-en.mp4`); all ship `preload="none"` and only load when visible |
| `tools/` | `import_shots.py` (screenshots from the app repo) and `record_studio.py` (the Studio tours) |
| `Dockerfile` | nginx image serving the tree, for a self-hosted deploy |

## Editing

Edit `build.py`, then run it. Do not hand-edit the generated `index.html` files: the next
build overwrites them.

Two things sit at the top of `build.py` because they are used from every page:

* `WHATSAPP`: digits only; feeds the floating button, the hero CTA and the closing band;
* `NAV` / `PAGES`: a new page is one entry in each, plus a `page_*` builder;
* `POSTS`: the articles. One dict per post (slug, date, tag, figures and the body blocks in both
  languages) is enough: the index card, the post page, the sitemap entry and the home teaser are
  all generated from it.

A post body is a list of blocks: `("h2", text)`, `("p", text)`, `("fig", (src, alt, caption))`,
`("video", (src, poster, caption))`, rendered by `render_block()`. Long UI screenshots go through
`shot()`, which wraps them in a browser frame.

The install command on the library page is a `<button class="install" data-copy="…">`; change
`data-copy` to change what gets copied.

Screenshots of the Engineering app live in `img/eng/`, generated from
`pinneapple-engineering-api/docs/screenshots/` (resized, cropped and converted to WebP, the
sources are 1366 px wide and some are several thousand pixels tall). `img/eng/studio-home.jpg`
exists only as the Open Graph image, because link previews want JPEG.

The two Studio tours in `videos/` come from `tools/record_studio.py`: it drives the running
app with Playwright (search → tool → run → checks → report → coverage), burns in the captions
in the page itself, then cuts the solver wait out and encodes the MP4. Keeping the script in
the repo is the point, a screen the site shows is a screen the application renders, and it
can be recorded again.

## Deploying

GitHub Pages serves `main` at the root. `.nojekyll` is present so nothing gets filtered.

Self-hosted:

```bash
docker build -t pinneapple-labs-site .
docker run --rm -p 8080:80 pinneapple-labs-site
```

## Content rule

Every number on the site is traceable to a run in the PINNeAPPle repository or to a published
reference (Vieira et al. 2016, Ghia et al., Bekker–Wong). When a claim has a limit, the limit is
written next to it, and the articles carry a "what was not proven" block. Do not add a metric
without a source, and if a figure changes, change the experiment it came from rather than
editing the prose.
