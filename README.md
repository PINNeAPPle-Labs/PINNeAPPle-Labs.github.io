# pinneapple-labs-site

Landing site for **PINNeAPPle Labs** — open-source Physics AI with verification as part of the
product. Served at <https://pinneapple-labs.github.io/>.

Four pages, two languages, generated from one script.

## Build

```bash
python3 build.py
```

That writes:

| path | page |
|---|---|
| `index.html` | main page (pt-BR) |
| `en/index.html` | main page (English) |
| `casos-de-uso/index.html` · `en/casos-de-uso/` | every technical validation, with its external reference |
| `lib/index.html` · `en/lib/` | architecture, quickstart, open-source split |
| `historia/index.html` · `en/historia/` | why the project exists, and who builds it |

`build.py` also regenerates `sitemap.xml`. Commit the generated HTML along with the script —
GitHub Pages serves the files as they are, there is no build step on the server.

## What lives where

| file | what it is |
|---|---|
| `build.py` | the whole source: page text (pt/en), the shared shell, the nav, the footer, the floating WhatsApp button |
| `styles.css` | the design system: tokens, layout, components, the sticky button |
| `app.js` | nav toggle, copy-to-clipboard, code tabs, scroll reveal, section spy, lazy video playback |
| `fonts.css`, `fonts/` | self-hosted Archivo + JetBrains Mono (latin subset, OFL) |
| `img/` | product and capability stills; `img/results/` holds real result plots |
| `videos/` | hero clip plus two app recordings; all ship `preload="none"` and only load when visible |
| `Dockerfile` | nginx image serving the tree, for a self-hosted deploy |

## Editing

Edit `build.py`, then run it. Do not hand-edit the generated `index.html` files — the next
build overwrites them.

Two things sit at the top of `build.py` because they are used from every page:

* `WHATSAPP` — digits only; feeds the floating button, the hero CTA and the closing band;
* `NAV` / `PAGES` — a new page is one entry in each, plus a `page_*` builder.

The install command on the hero is a `<button class="install" data-copy="…">`; change
`data-copy` to change what gets copied.

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
written next to it. Do not add a metric without a source — and if a figure changes, change the
row it came from on the use-cases page rather than editing the prose.
