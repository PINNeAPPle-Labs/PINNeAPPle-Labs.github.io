# pinneapple-labs-site

Landing site for **PINNeAPPle Labs**, open-source Physics AI with verification as part of the
product. Served at <https://pinneapple-labs.github.io/>.

A single home page that carries the commercial pitch and, in the middle of it, the
**PINNeAPPle Studio** product story (with a "coming soon" badge), an articles section with one
post per experiment, and the library page, in two languages, generated from one script.

## Build

```bash
python3 build.py
```

That writes:

| path | page |
|---|---|
| `index.html` | home (pt-BR): the whole story, product sections included, from `#apresentacao` to `#historia` |
| `en/index.html` | home (English) |
| `artigos/index.html` · `en/artigos/` | article index, newest first |
| `artigos/<slug>/index.html` · `en/artigos/<slug>/` | one post per experiment, from the `POSTS` list |
| `lib/index.html` · `en/lib/` | architecture, quickstart, open-source split |
| `studio/`, `engineering/`, `casos-de-uso/`, `historia/` (+ `en/`) | redirect stubs, in that order, to `/#produto`, `/#produto`, `/artigos/` and `/#historia`; the old URLs keep working |

There is one page plus the article index and the lib page: the old product page was merged
into the home, so the product is a section (`#produto`) of it, not a tab of its own.

`build.py` also regenerates `sitemap.xml`. Commit the generated HTML along with the script:
GitHub Pages serves the files as they are, there is no build step on the server.

## What lives where

| file | what it is |
|---|---|
| `build.py` | the whole source: page text (pt/en), the shared shell, the nav, the footer, the floating WhatsApp button |
| `styles.css` | the design system: tokens, layout, components, the sticky button |
| `app.js` | nav toggle, copy-to-clipboard, code tabs, scroll reveal, section spy, lazy video playback |
| `fonts.css`, `fonts/` | self-hosted Archivo + JetBrains Mono (latin subset, OFL) |
| `img/` | product and capability stills; `img/results/` holds real result plots; `img/exp/` holds the figures each article shows, straight from the example that produced them |
| `videos/` | hero clip, two base-app recordings, the two Studio tours (`studio-pt.mp4`, `studio-en.mp4`) and the `reel-*.mp4` clips the product section scrolls through; all ship `preload="none"` and only load and play when visible |
| `tools/` | `import_shots.py` (screenshots from the app repo), `capture_shots.py` (captures them from the running app), `record_studio.py` (the Studio tours) and `import_figures.py` (article figures out of `../PINNeAPPle/examples`) |
| `Dockerfile` | nginx image serving the tree, for a self-hosted deploy |

## Editing

Edit `build.py`, then run it. Do not hand-edit the generated `index.html` files: the next
build overwrites them.

Two things sit at the top of `build.py` because they are used from every page:

* `WHATSAPP`: digits only; feeds the floating button, the hero CTA and the closing band;
* `NAV` / `PAGES`: a new page is one entry in each, plus a `page_*` builder. `produto_sections()`
  is the exception: it has no `PAGES` entry, because it is rendered inside the home;
* `POSTS`: the articles. One dict per post (slug, date, tag, figures and the body blocks in both
  languages) is enough: the index card, the post page, the sitemap entry and the home teaser are
  all generated from it.

A post body is a list of blocks: `("h2", text)`, `("p", text)`, `("fig", (src, alt, caption))`,
`("video", (src, poster, caption))`, rendered by `render_block()`. Long UI screenshots go through
`shot()`, which wraps them in a browser frame.

The talk on the home page is a `button.yt` with a `data-id`: `app.js` swaps it for a
`youtube-nocookie` iframe on click, so nothing is requested from YouTube until someone asks for it.
The poster is local (`img/simr.jpg`), so the section renders without the network too.

The `reel-*.mp4` clips in the product section come straight from the examples (`dashboard_replay.mp4`
cropped to the dashboard, `evolution_cantilever.mp4`, `traverse.mp4`, `04_surrogate_turntable.mp4`,
`enso_1997_98_slab.mp4`); the list lives in `REEL` in `build.py`.

The install command on the library page is a `<button class="install" data-copy="…">`; change
`data-copy` to change what gets copied.

Article figures are not redrawn or recoloured: `tools/import_figures.py` copies the PNG the
run wrote, converts it to WebP and, for the card thumbnail only, either crops it to 16:10 or
leaves it whole on a plate (`chart=True` in the post dict when the source is a matplotlib
chart, whose axes the crop would cut).

Screenshots of the Studio app live in `img/eng/`, generated from
`pinneapple-engineering-api/docs/screenshots/` (resized, cropped and converted to WebP, the
sources are 1366 px wide and some are several thousand pixels tall). `img/eng/studio-home.jpg`
exists only as the Open Graph image, because link previews want JPEG.

The two Studio tours in `videos/` come from `tools/record_studio.py`: it drives the running
app with Playwright (search → tool → run → checks → report → coverage), burns in the captions
in the page itself, then cuts the solver wait out and encodes the MP4. Keeping the script in
the repo is the point, a screen the site shows is a screen the application renders, and it
can be recorded again.

## Pré-acesso (Google Forms)

A chamada de pré-acesso ao Studio é um link do Google Forms por idioma:

```python
# build.py, no topo
PREACCESS_FORM = {
    "pt": "https://forms.gle/xxxxxxxx",
    "en": "https://forms.gle/yyyyyyyy",
}
```

Os dois formulários saem prontos de `tools/create_prerelease_forms.gs`, um script de Google
Apps Script: abra <https://script.google.com>, cole o arquivo, rode
`criarFormulariosDePreAcesso` e leia os links no registro de execução. Ele cria os formulários
(3 perguntas obrigatórias e 1 opcional, e-mail vindo da conta Google), liga cada um a uma
planilha de respostas e imprime o link curto de cada idioma.

Enquanto um idioma não tiver link, **nada é renderizado nele**: nem o item de menu, nem a
faixa `#pre-acesso` que aparece na home (hoje a única página que a tem, no fim do produto).
É de propósito, um botão que leva a lugar nenhum é pior que botão nenhum.

O formulário é externo, então o site continua estático: nenhum backend, nenhum cookie,
nada carregado do Google antes de a pessoa clicar.

Formulário recomendado (curto, seis perguntas, todas com motivo):

| pergunta | tipo | obrigatória | por quê |
|---|---|---|---|
| Nome | resposta curta | sim | saber com quem falar |
| E-mail | resposta curta, validação de e-mail | sim | é por aqui que o convite sai |
| Empresa | resposta curta | sim | separa profissional de curioso |
| Área de atuação | múltipla escolha | sim | prioriza quem tem dor parecida |
| Que problema você quer resolver primeiro? | parágrafo | não | a resposta mais valiosa do formulário |
| Time de engenharia | múltipla escolha (1–5, 6–20, 21+) | não | dimensiona o plano |

Ajustes no Google Forms: coletar e-mail automaticamente, mensagem de confirmação dizendo
que o convite sai em 2027 por ordem de inscrição, notificação por e-mail a cada resposta e
respostas ligadas a uma planilha. Para saber se o clique veio do site em português ou em
inglês, use o preenchimento prévio (`?usp=pp_url&entry.XXXXXX=pt`) na constante — dois links,
um por idioma, ou um campo oculto.

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
