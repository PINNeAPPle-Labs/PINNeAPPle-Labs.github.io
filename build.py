#!/usr/bin/env python3
"""Builds the PINNeAPPle Labs site: four pages, two languages.

    python3 build.py

Output
------
    index.html               main page (pt-BR)         en/index.html
    casos-de-uso/index.html  the evidence page         en/casos-de-uso/index.html
    lib/index.html           the library page          en/lib/index.html
    historia/index.html      the project page          en/historia/index.html

One place holds the shared shell (head, nav, footer, the sticky WhatsApp button) so the
pages cannot drift apart. Text lives next to the markup it belongs to, per language.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Configuration — change here, not in the pages
# ---------------------------------------------------------------------------

SITE = "https://pinneapple-labs.github.io"
WHATSAPP = "5584991287602"          # digits only, used by the floating button
EMAIL = "yanbarrosyan@gmail.com"
GITHUB = "https://github.com/PINNeAPPle-Labs/PINNeAPPle"
PYPI = "https://pypi.org/project/pinneapple/"
DOCS = "https://pinneapple-labs.github.io/PINNeAPPle/"
CHANGELOG = f"{GITHUB}/blob/main/CHANGELOG.md"

LANGUAGES = {
    "pt": {"code": "pt-BR", "dir": "", "label": "PT", "other": "en", "other_label": "EN"},
    "en": {"code": "en", "dir": "en", "label": "EN", "other": "pt", "other_label": "PT"},
}

# Slug of each page, identical in both languages (only the /en/ prefix changes).
PAGES = {
    "home": "",
    "casos": "casos-de-uso",
    "lib": "lib",
    "historia": "historia",
}


def url(lang: str, page: str) -> str:
    d = LANGUAGES[lang]["dir"]
    slug = PAGES[page]
    parts = [p for p in (d, slug) if p]
    return "/".join(parts) + ("/" if parts else "")


def up(lang: str, page: str) -> str:
    """Relative prefix to reach the site root from a page."""
    depth = len([p for p in (LANGUAGES[lang]["dir"], PAGES[page]) if p])
    return "../" * depth


# ---------------------------------------------------------------------------
# Shared shell
# ---------------------------------------------------------------------------

NAV = {
    "pt": [("home", "Produtos"), ("casos", "Casos de uso"), ("lib", "A lib"), ("historia", "História")],
    "en": [("home", "Products"), ("casos", "Use cases"), ("lib", "The library"), ("historia", "Story")],
}

STRINGS = {
    "pt": {
        "skip": "Pular para o conteúdo",
        "wa": "Falar com um engenheiro",
        "wa_msg": "Olá! Vim pelo site da PINNeAPPle Labs e tenho um problema de engenharia para discutir.",
        "cta_title": "Tem uma simulação lenta, cara ou difícil de verificar?",
        "cta_lead": "Mande o caso. Respondemos com um escopo fechado e uma métrica de sucesso mensurável — ou dizemos que o método clássico resolve melhor.",
        "cta_primary": "Falar com um engenheiro",
        "docs_nav": "Docs",
        "cta_short": "Falar com um engenheiro",
        "cta_secondary": "Começar pelo código",
        "foot_tag": "Physics AI de código aberto, com verificação como parte do produto. Modelos que mostram a conta.",
        "foot_platform": "Plataforma",
        "foot_code": "Código",
        "foot_contact": "Contato",
        "foot_law": "LAIS &amp; YAN LTDA · CNPJ 62.766.371/0001-36 · Entrega industrial com a Domus.",
        "foot_rights": "Apache-2.0 no código, verificação por padrão.",
        "lbl_products": "Produtos",
        "lbl_cases": "Casos de uso",
        "lbl_lib": "A lib",
        "lbl_story": "História",
    },
    "en": {
        "skip": "Skip to content",
        "wa": "Talk to an engineer",
        "wa_msg": "Hello! I found PINNeAPPle Labs through the site and have an engineering problem to discuss.",
        "cta_title": "Got a simulation that is slow, expensive or hard to verify?",
        "cta_lead": "Send it over. We come back with a closed scope and a measurable success criterion — or we tell you the classical method does it better.",
        "cta_primary": "Talk to an engineer",
        "docs_nav": "Docs",
        "cta_short": "Talk to an engineer",
        "cta_secondary": "Start from the code",
        "foot_tag": "Open-source Physics AI, with verification as part of the product. Models that show their work.",
        "foot_platform": "Platform",
        "foot_code": "Code",
        "foot_contact": "Contact",
        "foot_law": "LAIS &amp; YAN LTDA · CNPJ 62.766.371/0001-36 · Industrial delivery with Domus.",
        "foot_rights": "Apache-2.0 in the code, verification by default.",
        "lbl_products": "Products",
        "lbl_cases": "Use cases",
        "lbl_lib": "The library",
        "lbl_story": "Story",
    },
}

TITLES = {
    "home": {
        "pt": "PINNeAPPle Labs — Physics AI de código aberto, com verificação",
        "en": "PINNeAPPle Labs — Open-source Physics AI, with verification",
    },
    "casos": {
        "pt": "Casos de uso — PINNeAPPle Labs",
        "en": "Use cases — PINNeAPPle Labs",
    },
    "lib": {
        "pt": "A biblioteca PINNeAPPle — PINNeAPPle Labs",
        "en": "The PINNeAPPle library — PINNeAPPle Labs",
    },
    "historia": {
        "pt": "História do projeto — PINNeAPPle Labs",
        "en": "Project story — PINNeAPPle Labs",
    },
}

DESCRIPTIONS = {
    "home": {
        "pt": "CFD, modelos substitutos, verificação e gêmeos digitais sobre uma base aberta. Números medidos, visualizações reais, e o erro declarado em cada entrega.",
        "en": "CFD, surrogate models, verification and digital twins on an open base. Measured numbers, real visualisations, and the error stated on every delivery.",
    },
    "casos": {
        "pt": "As validações técnicas da PINNeAPPle, com o número medido e a referência externa de cada uma — inclusive onde ainda não chegamos.",
        "en": "PINNeAPPle's technical validations, each with its measured number and external reference — including where we have not got there yet.",
    },
    "lib": {
        "pt": "Arquitetura, quickstart e o split honesto do código aberto da plataforma PINNeAPPle: 31 módulos, 248 exemplos, Apache-2.0.",
        "en": "Architecture, quickstart and the honest open-source split of the PINNeAPPle platform: 31 modules, 248 examples, Apache-2.0.",
    },
    "historia": {
        "pt": "Por que a PINNeAPPle existe, como ela é construída e por quem — uma regra: se não tem número medido, não vai para a tela.",
        "en": "Why PINNeAPPle exists, how it is built and by whom — one rule: if it has no measured number, it does not go on screen.",
    },
}


def head(lang: str, page: str, root: str) -> str:
    L = LANGUAGES[lang]
    alt_pt = f"{SITE}/{url('pt', page)}"
    alt_en = f"{SITE}/{url('en', page)}"
    return f"""<!doctype html>
<html lang="{L['code']}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{TITLES[page][lang]}</title>
<meta name="description" content="{DESCRIPTIONS[page][lang]}" />
<meta name="theme-color" content="#070a10" />
<link rel="canonical" href="{SITE}/{url(lang, page)}" />
<link rel="alternate" hreflang="pt-BR" href="{alt_pt}" />
<link rel="alternate" hreflang="en" href="{alt_en}" />
<link rel="alternate" hreflang="x-default" href="{alt_pt}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{TITLES[page][lang]}" />
<meta property="og:description" content="{DESCRIPTIONS[page][lang]}" />
<meta property="og:image" content="{root}img/portfolio/13-aircraft-render-pressure.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml" />
<link rel="stylesheet" href="{root}fonts.css" />
<link rel="stylesheet" href="{root}styles.css" />
</head>
<body>
<a class="skip-link" href="#main">{STRINGS[lang]['skip']}</a>
"""


LOGO = """<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <path d="M16 2.6c1.35 2.1 1.95 4.4 1.8 6.7" stroke="#3dd6c4" stroke-width="1.9" stroke-linecap="round"/>
        <path d="M15.3 3.4c-2.6 1-4.4 2.9-5.4 5.3" stroke="#3dd6c4" stroke-width="1.9" stroke-linecap="round"/>
        <path d="M16.7 3.4c2.6 1 4.4 2.9 5.4 5.3" stroke="#3dd6c4" stroke-width="1.9" stroke-linecap="round"/>
        <ellipse cx="16" cy="20.1" rx="7.7" ry="9.2" fill="#f0b32e" fill-opacity=".18" stroke="#f0b32e" stroke-width="1.9"/>
        <path d="M12.4 12.6 19.6 27.6M19.6 12.6 12.4 27.6M8.9 17.6h14.2M10.6 22.6h10.8" stroke="#f0b32e" stroke-width="1.15" stroke-opacity=".7"/>
      </svg>"""

WA_ICON = """<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm5.8 14.06c-.24.68-1.4 1.3-1.93 1.35-.53.05-1.02.24-3.44-.72-2.9-1.15-4.72-4.15-4.86-4.34-.14-.19-1.15-1.53-1.15-2.92s.73-2.07 1-2.35c.26-.29.58-.36.77-.36l.55.01c.18 0 .42-.07.65.5.24.58.81 2 .88 2.14.07.14.12.31.02.5-.1.19-.15.31-.29.48l-.44.51c-.15.15-.3.31-.13.6.17.29.75 1.24 1.62 2.01 1.11.99 2.05 1.3 2.34 1.44.29.15.46.12.63-.07.17-.19.72-.84.91-1.13.19-.29.38-.24.64-.15.26.1 1.66.78 1.95.93.29.14.48.22.55.34.07.13.07.75-.17 1.43Z"/></svg>"""


def header(lang: str, page: str, root: str) -> str:
    L = LANGUAGES[lang]
    links = "\n".join(
        f'      <a href="{root}{url(lang, key) or ""}"'
        f'{" aria-current=\"page\"" if key == page else ""}>{label}</a>'
        for key, label in NAV[lang]
    )
    # The documentation lives outside this repo, on the platform's own site.
    links += (f'\n      <a href="{DOCS}" target="_blank" rel="noopener">'
              f'{STRINGS[lang]["docs_nav"]} ↗</a>')
    return f"""<header class="site">
  <div class="bar">
    <a class="brand" href="{root}{url(lang, 'home') or ''}">
      {LOGO}
      <span>PINNeAPPle<span class="labs"> Labs</span></span>
    </a>

    <nav class="main" id="primary-nav" aria-label="{STRINGS[lang]['foot_platform']}">
{links}
    </nav>

    <div class="bar-cta">
      <a class="chip" href="{root}{url(_other(lang), page)}" hreflang="{LANGUAGES[_other(lang)]['code']}">{L['other_label']}</a>
      <a class="btn btn-primary btn-sm" href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
    </div>

    <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 5h14M2 9h14M2 13h14"/></svg>
    </button>
  </div>
</header>
"""


def _other(lang: str) -> str:
    return "en" if lang == "pt" else "pt"


def footer(lang: str, page: str, root: str) -> str:
    S = STRINGS[lang]
    o = _other(lang)
    return f"""
<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="{root}{url(lang, 'home') or ''}">
          {LOGO}
          <span>PINNeAPPle<span class="labs"> Labs</span></span>
        </a>
        <p>{S['foot_tag']}</p>
      </div>
      <div>
        <h4>{S['foot_platform']}</h4>
        <ul>
          <li><a href="{root}{url(lang, 'home') or ''}">{S['lbl_products']}</a></li>
          <li><a href="{root}{url(lang, 'casos')}">{S['lbl_cases']}</a></li>
          <li><a href="{root}{url(lang, 'lib')}">{S['lbl_lib']}</a></li>
          <li><a href="{root}{url(lang, 'historia')}">{S['lbl_story']}</a></li>
        </ul>
      </div>
      <div>
        <h4>{S['foot_code']}</h4>
        <ul>
          <li><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></li>
          <li><a href="{PYPI}" target="_blank" rel="noopener">PyPI</a></li>
          <li><a href="{DOCS}" target="_blank" rel="noopener">Docs</a></li>
          <li><a href="{CHANGELOG}" target="_blank" rel="noopener">Changelog</a></li>
        </ul>
      </div>
      <div>
        <h4>{S['foot_contact']}</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{S['wa']}</a></li>
          <li><a href="{root}{url(o, page)}" hreflang="{LANGUAGES[o]['code']}">{LANGUAGES[o]['label']}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base">
      <span>© <span id="yr">2026</span> PINNeAPPle Labs · {S['foot_rights']}</span>
      <span>{S['foot_law']}</span>
    </div>
  </div>
</footer>

<a class="fab" href="https://wa.me/{WHATSAPP}?text={_q(S['wa_msg'])}" target="_blank" rel="noopener" aria-label="{S['wa']}">
  {WA_ICON}<span>{S['wa']}</span>
</a>

<script src="{root}app.js" defer></script>
<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def _q(text: str) -> str:
    import urllib.parse
    return urllib.parse.quote(text)


def wa_button(lang: str, cls: str = "btn btn-primary", label: str | None = None) -> str:
    """The primary call to action, in one place so the wording cannot drift."""
    S = STRINGS[lang]
    text = label or S["cta_primary"]
    return (f'<a class="{cls}" href="https://wa.me/{WHATSAPP}?text={_q(S["wa_msg"])}" '
            f'target="_blank" rel="noopener">{text}</a>')


def cta_band(lang: str, root: str) -> str:
    S = STRINGS[lang]
    return f"""  <section class="cta-band">
    <div class="wrap cta-inner">
      <div>
        <p class="eyebrow">{'Traga o seu caso' if lang == 'pt' else 'Bring your case'}</p>
        <h2>{S['cta_title']}</h2>
        <p class="lead" style="max-width:52ch">{S['cta_lead']}</p>
      </div>
      <div class="cta-actions">
        {wa_button(lang)}
        <a class="btn btn-ghost" href="{GITHUB}" target="_blank" rel="noopener">{S['cta_secondary']}</a>
      </div>
    </div>
  </section>
"""


# ---------------------------------------------------------------------------
# Page: home
# ---------------------------------------------------------------------------

PRODUCTS = {
    "pt": [
        dict(
            tag="Produto 01 · CFD",
            name="PINNeAPPle CFD",
            lead="O fluxo CFD completo, de E1 a E11: você descreve o problema, o pipeline monta geometria e malha, roda o OpenFOAM, gera o dataset, treina o substituto e fecha com o mapa de provas.",
            bullets=[
                "<b>Erosão em curva de 90°:</b> entre 1,05× e 1,49× do ensaio publicado, dentro do fator 2 que a indústria aceita.",
                "<b>Substituto 1,0% de erro</b> na perda de carga em pontos nunca vistos.",
                "<b>32 simulações</b> da geometria ao modelo treinado em 23 minutos.",
            ],
            metric="1,05–1,49×",
            metric_label="do ensaio aberto, dentro do fator 2",
            video="videos/hero-aero.mp4", poster="videos/hero-aero.jpg",
            caption="Pressão na pele (Cp) em OpenFOAM 3D, do projeto ao campo",
            cases="ver os casos de CFD",
        ),
        dict(
            tag="Produto 02 · Substitutos",
            name="Surrogate Studio",
            lead="Transforma as simulações que a sua equipe já rodou num modelo que responde em microssegundos — conferido contra o solver a cada entrega, nunca contra ele mesmo.",
            bullets=[
                "<b>~200.000× mais rápido</b> que a simulação 3D real, em sete geometrias de dissipador.",
                "<b>4,46% de erro médio</b> e 7,35% no pior caso contra FEniCS/dolfinx.",
                "<b>Previsão determinística:</b> os mesmos números em três rodadas, em dias diferentes.",
            ],
            metric="~200.000×",
            metric_label="mais rápido, com 4,46% de erro",
            video="videos/app1.mp4", poster="videos/app1.jpg",
            caption="O app de dimensionamento térmico, rodando",
            cases="ver os casos de substitutos",
        ),
        dict(
            tag="Produto 03 · Verificação",
            name="VeriPhysics",
            lead="O portão entre o resultado e a decisão: recebe um modelo, um caso CFD ou um deck FEA e devolve uma nota por checagem — resíduo, convergência, calibração, cobertura — com o número e a fonte.",
            bullets=[
                "<b>Pegou o que a loss escondeu</b> num modelo de cliente: resíduo centenas de vezes acima do limiar.",
                "<b>Viga sem apoios:</b> “Job finished” com 1,8e11 mm de deslocamento; o preflight marca FAIL antes da execução.",
                "<b>Malha:</b> métricas idênticas ao checkMesh do OpenFOAM.",
            ],
            metric="11 checagens",
            metric_label="nenhuma nota fabricada, nunca",
            video="videos/app8.mp4", poster="videos/app8.jpg",
            caption="O preflight de simulação apontando o que vai falhar",
            cases="ver os casos de verificação",
        ),
        dict(
            tag="Produto 04 · Gêmeo digital",
            name="PINNeAPPle Twin",
            lead="Um modelo validado trabalhando ao lado do dado real — e a camada que decide se ele pode entrar em operação. Contrato assinado, preflight, backtest contra sonda redundante e evidência arquivada.",
            bullets=[
                "<b>0,216 °C de erro</b> no caso HX-201, com incrustação estimada a 0,001651 contra 0,001637 verdadeiro.",
                "<b>95,5% de cobertura</b> da banda na janela de validação, calibrada nas horas anteriores.",
                "<b>Alarme 2,6 h antes</b> do cruzamento medido, com o erro da previsão declarado.",
            ],
            metric="2,6 h",
            metric_label="de antecedência, com erro de previsão declarado",
            image="img/twin.jpg", img_alt="Ativo industrial em 3D com painel de leitura ao vivo",
            caption="O ativo em 3D com a leitura viva ao lado",
            cases="ver os casos de gêmeo digital",
        ),
    ],
    "en": [
        dict(
            tag="Product 01 · CFD",
            name="PINNeAPPle CFD",
            lead="The full CFD workflow, E1 to E11: you describe the problem, the pipeline builds geometry and mesh, runs OpenFOAM, generates the dataset, trains the surrogate and closes with the evidence map.",
            bullets=[
                "<b>Erosion in a 90° bend:</b> between 1.05× and 1.49× the published experiment, inside the factor-2 band industry accepts.",
                "<b>Surrogate at 1.0% error</b> on pressure drop at points it never saw.",
                "<b>32 simulations</b> from geometry to trained model in 23 minutes.",
            ],
            metric="1.05–1.49×",
            metric_label="of the open experiment, inside factor 2",
            video="videos/hero-aero.mp4", poster="videos/hero-aero.jpg",
            caption="Skin pressure (Cp) in 3D OpenFOAM, from design to field",
            cases="see the CFD cases",
        ),
        dict(
            tag="Product 02 · Surrogates",
            name="Surrogate Studio",
            lead="Turns the simulations your team already ran into a model that answers in microseconds — checked against the solver on every delivery, never against itself.",
            bullets=[
                "<b>~200,000× faster</b> than the real 3D simulation, across seven heat-sink geometries.",
                "<b>4.46% mean error</b> and 7.35% worst case against FEniCS/dolfinx.",
                "<b>Deterministic prediction:</b> the same numbers on three runs, on different days.",
            ],
            metric="~200,000×",
            metric_label="faster, at 4.46% error",
            video="videos/app1.mp4", poster="videos/app1.jpg",
            caption="The thermal sizing app, running",
            cases="see the surrogate cases",
        ),
        dict(
            tag="Product 03 · Verification",
            name="VeriPhysics",
            lead="The gate between the result and the decision: it takes a model, a CFD case or an FEA deck and returns one score per check — residual, convergence, calibration, coverage — with the number and its source.",
            bullets=[
                "<b>Caught what the loss hid</b> on a client model: residual hundreds of times over the threshold.",
                "<b>Unsupported beam:</b> “Job finished” with 1.8e11 mm of displacement; preflight flags FAIL before the run.",
                "<b>Mesh:</b> metrics identical to OpenFOAM's checkMesh.",
            ],
            metric="11 checks",
            metric_label="no fabricated score, ever",
            video="videos/app8.mp4", poster="videos/app8.jpg",
            caption="The simulation preflight pointing at what will fail",
            cases="see the verification cases",
        ),
        dict(
            tag="Product 04 · Digital twin",
            name="PINNeAPPle Twin",
            lead="A validated model working next to operational data — and the layer that decides whether it may go on line. Signed contract, preflight, backtest against a redundant probe, and filed evidence.",
            bullets=[
                "<b>0.216 °C error</b> on HX-201, with fouling estimated at 0.001651 against a true 0.001637.",
                "<b>95.5% band coverage</b> on the validation window, calibrated on the hours before it.",
                "<b>An alarm 2.6 h before</b> the measured crossing, with the forecast error stated.",
            ],
            metric="2.6 h",
            metric_label="of warning, with the forecast error stated",
            image="img/twin.jpg", img_alt="Industrial asset in 3D with a live reading panel",
            caption="The asset in 3D beside the live reading",
            cases="see the digital twin cases",
        ),
    ],
}

HOME = {
    "pt": dict(
        eyebrow="Physics AI de código aberto · Apache-2.0",
        h1="A simulação não fecha o prazo. A gente faz ela fechar.",
        lead="Transformamos o seu caso de engenharia num modelo que responde em segundos e é <b>conferido contra o solver, o ensaio ou a norma</b> — com o erro medido na tela. CFD, substitutos, verificação e gêmeos digitais.",
        install="pip install pinneapple",
        docs="Ler a documentação →",
        chips=["PyPI 0.7.0", "31 módulos", "63 aplicações", "248 exemplos"],
        stats=[
            ("~200.000×", "mais rápido que a simulação 3D real, num substituto térmico", "4,46% de erro vs. FEniCS"),
            ("1,05–1,49×", "erosão simulada vs. ensaio aberto, dentro do fator 2", "Vieira et al. 2016"),
            ("−18,2%", "de arrasto num aerofólio, com a sustentação mantida", "0,04% de variação"),
            ("2,6 h", "de antecedência no alarme do gêmeo, com erro declarado", "HX-201, incrustação"),
        ],
        products_h="Quatro produtos, todos com número medido.",
        products_p="Cada um existe em código, roda hoje e mostra o próprio erro. Abra os casos de uso para ver a referência externa de cada número.",
        existing_h="O que já existe hoje",
        existing="Não é um anúncio de roadmap. Está no repositório e no PyPI:",
        existing_items=[
            ("31", "módulos publicados, do PDE ao serving"),
            ("63", "aplicações construídas sobre a base"),
            ("248", "exemplos executáveis com saída conferida"),
            ("15", "padrões da indústria: AAS, DTDL, NGSI-LD, Ditto, OPC UA…"),
        ],
        feat_h="Três provas, com imagem.",
        feat_p="Resultados que saíram de uma execução, não de uma estimativa.",
        dest_h="Para onde ir agora",
        dest_p="A tela principal mostra o que fazemos. O resto está a um clique:",
        dests=[
            ("casos", "Casos de uso", "Todas as validações técnicas, com o número medido, a referência externa e o limite declarado de cada uma."),
            ("lib", "Detalhes da lib", "Arquitetura em camadas, quickstart, benchmarks públicos e o split honesto do código aberto."),
            ("historia", "História do projeto", "Por que a PINNeAPPle existe, a regra que ela segue e quem constrói."),
        ],
        cases_btn="Ver todos os casos de uso",
        feat_captions=["Pressão na pele, OpenFOAM 3D", "1.920 projetos e a frente de Pareto", "Vorticidade de um par de Lamb-Oseen"],
    ),
    "en": dict(
        eyebrow="Open-source Physics AI · Apache-2.0",
        h1="Your simulation misses the deadline. We make it hit.",
        lead="We turn your engineering case into a model that answers in seconds and is <b>checked against the solver, the experiment or the standard</b> — with the measured error on screen. CFD, surrogates, verification and digital twins.",
        install="pip install pinneapple",
        docs="Read the docs →",
        chips=["PyPI 0.7.0", "31 modules", "63 applications", "248 examples"],
        stats=[
            ("~200,000×", "faster than the real 3D simulation, on a thermal surrogate", "4.46% error vs. FEniCS"),
            ("1.05–1.49×", "simulated vs. open erosion experiment, inside factor 2", "Vieira et al. 2016"),
            ("−18.2%", "profile drag on an airfoil, with lift held", "0.04% variation"),
            ("2.6 h", "of twin alarm lead, with the error stated", "HX-201, fouling"),
        ],
        products_h="Four products, every one with a measured number.",
        products_p="Each exists in code, runs today, and shows its own error. Open the use cases for the external reference behind every figure.",
        existing_h="What already exists today",
        existing="This is not a roadmap announcement. It is in the repository and on PyPI:",
        existing_items=[
            ("31", "published modules, from the PDE to serving"),
            ("63", "applications built on the base"),
            ("248", "runnable examples with checked output"),
            ("15", "industry standards: AAS, DTDL, NGSI-LD, Ditto, OPC UA…"),
        ],
        feat_h="Three proofs, with a picture.",
        feat_p="Results that came out of a run, not out of an estimate.",
        dest_h="Where to go next",
        dest_p="The main page shows what we do. The rest is one click away:",
        dests=[
            ("casos", "Use cases", "Every technical validation, with its measured number, external reference and stated limit."),
            ("lib", "The library", "Layered architecture, quickstart, public benchmarks and the honest open-source split."),
            ("historia", "Project story", "Why PINNeAPPle exists, the rule it follows and who builds it."),
        ],
        cases_btn="See all use cases",
        feat_captions=["Skin pressure, 3D OpenFOAM", "1,920 designs and the Pareto front", "Vorticity of a Lamb-Oseen pair"],
    ),
}


def page_home(lang: str) -> str:
    root = up(lang, "home")
    S = STRINGS[lang]
    C = HOME[lang]
    parts = [head(lang, "home", root), header(lang, "home", root), '<main id="main">']

    chips = "".join(f'<span class="chip">{c}</span>' for c in C["chips"])
    parts.append(f"""
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">{C['eyebrow']}</p>
        <h1>{C['h1']}</h1>
        <p class="lead">{C['lead']}</p>
        <div class="hero-actions">
          {wa_button(lang)}
          <button class="install" data-copy="{C['install']}" aria-label="{C['install']}">
            <span class="prompt" aria-hidden="true">$</span>
            <span class="cmd">{C['install']}</span>
            <span class="copy-ico" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 3.5v-1a1 1 0 0 0-1-1h-7a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h1"/></svg></span>
          </button>
          <a class="btn btn-ghost" href="{DOCS}" target="_blank" rel="noopener">{C['docs']}</a>
        </div>
        <div class="hero-meta">{chips}</div>
      </div>
      <figure class="hero-media">
        <video src="{root}videos/hero-aero.mp4" poster="{root}videos/hero-aero.jpg" muted loop playsinline preload="metadata" data-autoplay
               aria-label="{C['feat_captions'][0]}"></video>
        <figcaption><span><b>1.920 projetos</b> de avião, 3 objetivos, CFD 3D</span><span>OpenFOAM</span></figcaption>
      </figure>
    </div>
  </section>
""")

    stats = "".join(
        f'    <div class="stat-cell" role="listitem"><div class="n{" cyan" if i % 2 else ""}">{n}</div>'
        f'<div class="l">{l}</div><div class="s">{s}</div></div>\n'
        for i, (n, l, s) in enumerate(C["stats"])
    )
    parts.append(f'  <div class="stats" role="list">\n{stats}  </div>\n')

    # products
    parts.append(f"""
  <section id="produtos">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{S['lbl_products']}</p><h2>{C['products_h']}</h2></div>
        <p>{C['products_p']}</p>
      </div>
""")
    for i, p in enumerate(PRODUCTS[lang]):
        flip = " flip" if i % 2 else ""
        bullets = "".join(f"<li>{b}</li>" for b in p["bullets"])
        if p.get("video"):
            media = (f'<video src="{root}{p["video"]}" poster="{root}{p["poster"]}" muted loop playsinline '
                     f'preload="none" data-autoplay aria-label="{p["caption"]}"></video>')
        else:
            media = f'<img src="{root}{p["image"]}" alt="{p["img_alt"]}" loading="lazy" decoding="async" />'
        parts.append(f"""
      <div class="split-block{flip} reveal product-block">
        <div>
          <p class="eyebrow dim">{p['tag']}</p>
          <h3 class="product-name">{p['name']}</h3>
          <p style="color:var(--text-dim)">{p['lead']}</p>
          <ul class="checks">{bullets}</ul>
          <div class="product-proof"><b>{p['metric']}</b><span>{p['metric_label']}</span></div>
          <p class="product-actions">
            <a class="btn btn-ghost btn-sm" href="{root}{url(lang, 'casos')}#{_anchor(p['name'])}">{p['cases']} →</a>
          </p>
        </div>
        <figure class="media product-media">
          {media}
          <figcaption>{p['caption']}</figcaption>
        </figure>
      </div>
""")
    parts.append(f"""      <p class="section-cta reveal">{wa_button(lang)}<a class="btn btn-ghost" href="{root}{url(lang, 'casos')}">{C['cases_btn']} →</a></p>
    </div>
  </section>
""")

    # what exists today
    items = "".join(
        f'<div class="exist-cell"><b>{n}</b><span>{l}</span></div>' for n, l in C["existing_items"]
    )
    parts.append(f"""
  <section id="hoje" class="alt tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{_k(lang, 'hoje')}</p><h2>{C['existing_h']}</h2></div>
        <p>{C['existing']}</p>
      </div>
      <div class="exist-grid reveal">{items}</div>
      <p class="section-cta reveal">{wa_button(lang, "btn btn-ghost")}</p>
    </div>
  </section>
""")

    # feature imagery
    caps = C["feat_captions"]
    parts.append(f"""
  <section id="provas">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{_k(lang, 'provas')}</p><h2>{C['feat_h']}</h2></div>
        <p>{C['feat_p']}</p>
      </div>
      <div class="gallery reveal">
        <figure class="gitem g-w4">
          <img src="{root}img/portfolio/13-aircraft-render-pressure.jpg" alt="{caps[0]}" loading="lazy" decoding="async" />
          <figcaption><b>{caps[0]}</b>1.920 projetos, −13% CO₂/pax-km</figcaption>
        </figure>
        <figure class="gitem g-w4">
          <img src="{root}img/portfolio/aero_pareto.jpg" alt="{caps[1]}" loading="lazy" decoding="async" />
          <figcaption><b>{caps[1]}</b>menos CO₂, cruzeiro mais rápido, aproximação mais lenta</figcaption>
        </figure>
        <figure class="gitem contain g-w4">
          <img src="{root}img/results/field_vortex_pair.png" alt="{caps[2]}" loading="lazy" decoding="async" />
          <figcaption><b>{caps[2]}</b>t = 0,01 · 0,30 · 0,80 · 2,00</figcaption>
        </figure>
      </div>
      <p style="margin-top:1.6rem"><a class="btn btn-primary" href="{root}{url(lang, 'casos')}">{C['cases_btn']} →</a></p>
    </div>
  </section>
""")

    # destinations
    dests = "".join(
        f'<a class="dest" href="{root}{url(lang, key)}"><h3>{title}</h3><p>{desc}</p><span class="go">→</span></a>'
        for key, title, desc in C["dests"]
    )
    parts.append(f"""
  <section id="destinos" class="alt-deep">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{_k(lang, 'depois')}</p><h2>{C['dest_h']}</h2></div>
        <p>{C['dest_p']}</p>
      </div>
      <div class="dest-grid reveal">{dests}</div>
    </div>
  </section>
""")

    parts.append(cta_band(lang, root))
    parts.append("</main>")
    parts.append(footer(lang, "home", root))
    return "".join(parts)


KICKERS = {
    "pt": {
        "hoje": "Hoje", "provas": "Provas", "depois": "Continue",
        "prova": "Prova", "imagens": "Imagens", "plus": "E mais",
        "arquitetura": "Arquitetura", "comecar": "Começar",
        "porque": "Por quê", "como": "Como", "equipe": "Equipe", "aberto": "Código aberto",
    },
    "en": {
        "hoje": "Today", "provas": "Proof", "depois": "Next",
        "prova": "Evidence", "imagens": "Figures", "plus": "And more",
        "arquitetura": "Architecture", "comecar": "Get started",
        "porque": "Why", "como": "How", "equipe": "Team", "aberto": "Open source",
    },
}


def _k(lang: str, key: str) -> str:
    """A short section kicker, distinct from the heading below it."""
    return KICKERS[lang][key]


def _anchor(name: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")


# ---------------------------------------------------------------------------
# Page: use cases
# ---------------------------------------------------------------------------

ROWS = {
    "pt": [
        ("Substituto térmico", "7 geometrias de dissipador", "~200.000× · 4,46%", "FEniCS/dolfinx 3D + gmsh; pior caso 7,35%", "surrogate-studio"),
        ("Erosão em curva de 90°", "OpenFOAM + substituto", "1,05–1,49× · 1,0%", "Vieira et al. 2016, ensaio aberto; critério de fator 2", "pinneapple-cfd"),
        ("Otimização de aerofólio", "substituto com reverificação", "−18,2%", "Arrasto de perfil; sustentação-alvo mantida em 0,04%", ""),
        ("Aerodinâmica veicular", "10 rodadas de simpleFoam", "0,05% · 1,3%", "Campo de velocidade e coeficientes vs. OpenFOAM; Cd a 0,17%", ""),
        ("PINN vs. volumes finitos", "comparação campo a campo", "0,39%", "Solver de volumes finitos independente; máximo 0,67 °C", ""),
        ("Cavidade com tampa móvel", "refinamento de malha", "0,19%", "Ghia et al.; partindo de 1,26%", ""),
        ("Inversão de h com PINN", "placa 2D e bloco 3D", "14,8 ± 0,3", "Valor verdadeiro 15; ponto quente 79,2 °C vs. 79,1 °C", ""),
        ("Térmica de PCB", "8 famílias de encapsulamento", "dentro de 8%", "θJA publicado, do SOIC-8 a um BGA de 35 mm", ""),
        ("Mobilidade de rover", "modelo publicado corrigido", "0,7–3,8%", "Bekker–Wong; erro de tração 45× menor que o original", ""),
        ("Monte Carlo de disco de freio", "tolerância de fabricação", "1,9 °C", "Nominal 495,9 °C; percentil 95 em 498,1 °C, limite 500 °C", ""),
        ("Gêmeo HX-201", "permutador com incrustação", "0,216 °C · 95,5%", "Sonda redundante fora do filtro; verdadeiro 0,001637 m²K/W", "pinneapple-twin"),
        ("Confiança física", "modelo de cliente, confidencial", "resíduo >100×", "Guardrail do VeriPhysics sobre um modelo já treinado", "veriphysics"),
    ],
    "en": [
        ("Thermal surrogate", "7 heat-sink geometries", "~200,000× · 4.46%", "3D FEniCS/dolfinx + gmsh; worst case 7.35%", "surrogate-studio"),
        ("Erosion in a 90° bend", "OpenFOAM + surrogate", "1.05–1.49× · 1.0%", "Vieira et al. 2016, open experiment; factor-2 criterion", "pinneapple-cfd"),
        ("Airfoil optimization", "surrogate-guided, re-verified", "−18.2%", "Profile drag; target lift held to 0.04%", ""),
        ("Vehicle aerodynamics", "10 simpleFoam runs", "0.05% · 1.3%", "Velocity field and coefficients vs. OpenFOAM; Cd at 0.17%", ""),
        ("PINN vs. finite volumes", "field-by-field comparison", "0.39%", "Independent finite-volume solver; max 0.67 °C", ""),
        ("Lid-driven cavity", "mesh refinement", "0.19%", "Ghia et al.; starting from 1.26%", ""),
        ("Inverse h with a PINN", "2D plate and 3D block", "14.8 ± 0.3", "True value 15; hot spot 79.2 °C vs. 79.1 °C", ""),
        ("PCB thermodynamics", "8 package families", "within 8%", "Published θJA, from SOIC-8 to a 35 mm BGA", ""),
        ("Rover mobility", "published model, corrected", "0.7–3.8%", "Bekker–Wong; traction error 45× lower than the original", ""),
        ("Brake-disc Monte Carlo", "manufacturing tolerance", "1.9 °C", "Nominal 495.9 °C; 95th percentile at 498.1 °C, limit 500 °C", ""),
        ("HX-201 twin", "fouled exchanger", "0.216 °C · 95.5%", "Redundant probe kept out of the filter; true 0.001637 m²K/W", "pinneapple-twin"),
        ("Physics confidence", "client model, confidential", "residual >100×", "VeriPhysics guardrail over an already-trained model", "veriphysics"),
    ],
}

CASES = {
    "pt": dict(
        eyebrow="Casos de uso",
        h1="O que já medimos, contra o quê, e onde ainda não chegamos.",
        lead="Toda linha abaixo tem uma referência externa ao treino: um ensaio publicado, um solver de volumes ou elementos finitos, ou uma linha de base da indústria. Onde existe limite, ele está declarado ao lado do número.",
        table_h="Validações técnicas",
        gallery_h="As imagens por trás dos números",
        apps_h="Construído sobre a mesma base",
        apps_p="A plataforma tem 63 aplicações. Estas são as que sustentam os quatro produtos acima.",
        apps_btn="Ver o acervo no GitHub",
        limits_h="Onde ainda não chegamos",
        limits="Erosão depende do fator 2, não de precisão de 1%. Resíduos estáveis não provam que arrasto estabilizou. E numa das análises de custo, um método numérico clássico era mais rápido e mais exato que a própria rede — a recomendação foi o método clássico. A banda do gêmeo é de estado, calibrada numa janela separada, e o lead vem de extrapolação linear cujo erro é reportado.",
    ),
    "en": dict(
        eyebrow="Use cases",
        h1="What we have measured, against what, and where we are not there yet.",
        lead="Every row below has a reference external to training: a published experiment, a finite-volume or finite-element solver, or an industry baseline. Where there is a limit, it is stated beside the number.",
        table_h="Technical validations",
        gallery_h="The pictures behind the numbers",
        apps_h="Built on the same base",
        apps_p="The platform holds 63 applications. These are the ones behind the four products above.",
        apps_btn="Browse the set on GitHub",
        limits_h="Where we are not there yet",
        limits="Erosion relies on a factor-2 band, not 1% precision. Flat residuals do not prove drag has settled. And in one cost analysis a classical numerical method was faster and more accurate than the network itself — the recommendation was the classical method. The twin's band is a state band calibrated on a separate window, and its lead comes from a linear extrapolation whose error is reported.",
    ),
}

APPS_SAMPLE = {
    "pt": [
        ("HeatSink Sizer", "Dissipadores em segundos, conferidos contra correlações publicadas.", "0–5% vs. literatura"),
        ("PCB Hotspot", "Temperatura de junção de cada componente em cerca de um segundo.", "θJA dentro de 8%"),
        ("Simulation Preflight", "PASS, WARNING ou FAIL antes de rodar, com arquivo e linha.", "falha pega antes da execução"),
        ("Mesh Quality", "OpenFOAM, Gmsh, VTK, Abaqus, STL: métricas, heatmap, piores elementos.", "idêntico ao checkMesh"),
        ("Inverse Heat Lab", "O coeficiente h a partir de alguns termopares, com PINN.", "h = 14,8 ± 0,3"),
        ("Aircraft Design Optimizer", "NSGA-II sobre a asa, conferido em OpenFOAM 3D.", "−13% CO₂/pax-km"),
        ("Surrogate Studio", "Resultados de simulação viram um modelo rápido com validade imposta.", "endpoint versionado"),
        ("Twin Runtime", "Modelo validado ao lado do dado real, com EnKF e revalidação.", "MQTT · REST · OPC UA"),
        ("Evidence Report", "Experimentos viram evidência reproduzível com SHA-256 de tudo.", "só passa o que rodou"),
    ],
    "en": [
        ("HeatSink Sizer", "Heat sinks in seconds, checked against published correlations.", "0–5% vs. literature"),
        ("PCB Hotspot", "Junction temperature of every part in about a second.", "θJA within 8%"),
        ("Simulation Preflight", "PASS, WARNING or FAIL before the run, with file and line.", "caught before the run"),
        ("Mesh Quality", "OpenFOAM, Gmsh, VTK, Abaqus, STL: metrics, heatmap, worst elements.", "identical to checkMesh"),
        ("Inverse Heat Lab", "The h coefficient from a few thermocouples, with a PINN.", "h = 14.8 ± 0.3"),
        ("Aircraft Design Optimizer", "NSGA-II over the wing, checked in 3D OpenFOAM.", "−13% CO₂/pax-km"),
        ("Surrogate Studio", "Simulation results become a fast model with enforced validity.", "versioned endpoint"),
        ("Twin Runtime", "A validated model beside operational data, with EnKF and revalidation.", "MQTT · REST · OPC UA"),
        ("Evidence Report", "Experiments become reproducible evidence with SHA-256 on everything.", "only what ran passes"),
    ],
}

FEATURES = {
    "pt": [
        ("Aircraft Design Optimizer", "portfolio/13-aircraft-render-pressure.jpg", "Pressão na pele (Cp), 1.920 projetos voados, −13% de CO₂/pax-km"),
        ("Três objetivos que brigam", "portfolio/aero_pareto.jpg", "Menos CO₂, cruzeiro mais rápido, aproximação mais lenta"),
        ("Erosão numa curva de 90°", "erosao.jpg", "CFD contra ensaio aberto: 1,05–1,49×, dentro do fator 2"),
        ("Substituto vs. FEA 3D", "surrogate_speed_rerun.jpg", "4,46% de erro médio, ~200.000× mais rápido"),
        ("Relatório de verificação", "verificacao.jpg", "Uma nota de 0 a 1 por checagem, e o que não rodou aparece como tal"),
        ("Par de vórtices de Lamb-Oseen", "results/field_vortex_pair.png", "Vorticidade em t = 0,01 · 0,30 · 0,80 · 2,00"),
        ("Benchmark de arquiteturas", "results/bench_pareto.png", "Tempo de treino vs. erro de teste, VPINN × PINN × PIELM"),
        ("Verdadeiro vs. previsto", "results/bench_true_vs_pred.png", "Três modelos, mesma condição de contorno"),
        ("Escoamento ao redor de um cilindro", "results/field_flow_cylinder.png", "Campo gerado pelo solver de referência"),
        ("Chassi, tensão de von Mises", "results/chassis_von_mises.png", "Campo de elementos finitos com colocação PINN"),
    ],
    "en": [
        ("Aircraft Design Optimizer", "portfolio/13-aircraft-render-pressure.jpg", "Skin pressure (Cp), 1,920 designs flown, −13% CO₂/pax-km"),
        ("Three objectives that fight", "portfolio/aero_pareto.jpg", "Less CO₂, faster cruise, slower approach"),
        ("Erosion in a 90° bend", "erosao.jpg", "CFD against an open experiment: 1.05–1.49×, inside factor 2"),
        ("Surrogate vs. 3D FEA", "surrogate_speed_rerun.jpg", "4.46% mean error, ~200,000× faster"),
        ("Verification report", "verificacao.jpg", "A score from 0 to 1 per check, and an unrun check says so"),
        ("Lamb-Oseen vortex pair", "results/field_vortex_pair.png", "Vorticity at t = 0.01 · 0.30 · 0.80 · 2.00"),
        ("Architecture benchmark", "results/bench_pareto.png", "Training time vs. test error, VPINN × PINN × PIELM"),
        ("True vs. predicted", "results/bench_true_vs_pred.png", "Three models, same boundary condition"),
        ("Flow around a cylinder", "results/field_flow_cylinder.png", "Field produced by the reference solver"),
        ("Chassis, von Mises stress", "results/chassis_von_mises.png", "Finite-element field with PINN collocation"),
    ],
}


def page_casos(lang: str) -> str:
    root = up(lang, "casos")
    C = CASES[lang]
    rows = "".join(
        f'      <tr{" id=\"" + anchor + "\"" if anchor else ""}>'
        f'<td class="name">{a}<small>{b}</small></td><td class="metric">{c}</td>'
        f'<td>{d}</td><td><span class="badge ok">{"validado" if lang == "pt" else "validated"}</span></td></tr>\n'
        for a, b, c, d, anchor in ROWS[lang]
    )
    apps = "".join(
        f'<article class="card"><h3>{a}</h3><p>{b}</p><div class="foot"><b>{c}</b></div></article>'
        for a, b, c in APPS_SAMPLE[lang]
    )
    gal = ""
    for i, (title, fname, cap) in enumerate(FEATURES[lang]):
        width = "g-w6" if i < 2 else "g-w4"
        contain = " contain" if fname.startswith("results/") else ""
        gal += (f'<figure class="gitem{contain} {width}"><img src="{root}img/{fname}" alt="{title}" '
                f'loading="lazy" decoding="async" /><figcaption><b>{title}</b>{cap}</figcaption></figure>\n')

    return "".join([
        head(lang, "casos", root), header(lang, "casos", root),
        f"""<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow">{C['eyebrow']}</p>
      <h1>{C['h1']}</h1>
      <p class="lead" style="max-width:68ch">{C['lead']}</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{_k(lang, 'prova')}</p><h2>{C['table_h']}</h2></div>
      <div class="table-wrap reveal">
        <table class="data">
          <thead><tr><th scope="col">{'Caso' if lang == 'pt' else 'Case'}</th><th scope="col">{'Métrica' if lang == 'pt' else 'Metric'}</th><th scope="col">{'Referência' if lang == 'pt' else 'Reference'}</th><th scope="col">Status</th></tr></thead>
          <tbody>
{rows}          </tbody>
        </table>
      </div>
      <p class="section-cta reveal">{wa_button(lang)}{'<a class="btn btn-ghost" href="' + DOCS + '" target="_blank" rel="noopener">Documentação ↗</a>' if lang == 'pt' else '<a class="btn btn-ghost" href="' + DOCS + '" target="_blank" rel="noopener">Documentation ↗</a>'}</p>
    </div>
  </section>

  <section class="alt">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{_k(lang, 'imagens')}</p><h2>{C['gallery_h']}</h2></div>
      <div class="gallery reveal">
{gal}      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{_k(lang, 'plus')}</p><h2>{C['apps_h']}</h2></div>
        <p>{C['apps_p']}</p>
      </div>
      <div class="grid-3 reveal">{apps}</div>
      <p style="margin-top:1.6rem"><a class="btn btn-ghost" href="{GITHUB}/tree/main/apps" target="_blank" rel="noopener">{C['apps_btn']} →</a></p>
      <div class="note reveal"><span><b>{C['limits_h']}:</b> {C['limits']}</span></div>
    </div>
  </section>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, "casos", root),
    ])


# ---------------------------------------------------------------------------
# Page: library
# ---------------------------------------------------------------------------

LAYERS = [
    ("Aplicação", "APPS &amp; SERVING", ["pinneapple_app", "pinneapple_lab", "pinneapple_hub", "pinneapple_orchestration", "pinneapple_llm", "REST / FastAPI"]),
    ("Modelos", "NEURAL", ["pinneapple_neural", "pinneapple_models", "PINN", "FNO", "DeepONet", "GNN", "LSTM", "VPINN"]),
    ("Física &amp; solvers", "PHYSICS", ["pinneapple_physics", "pinneapple_solvers", "pinneapple_simulation", "pinneapple_pdb", "OpenFOAM", "FEniCS/dolfinx", "CalculiX"]),
    ("Análise", "ANALYSIS &amp; UQ", ["pinneapple_analysis", "pinneapple_veriphysics", "pinneapple_decision", "pinneapple_adaptation", "UQ", "EnKF", "Monte Carlo"]),
    ("Dados &amp; geometria", "DATA", ["pinneapple_data", "pinneapple_design", "pinneapple_catalog", "pinneapple_pdb", "pinneapple_twin3d", "pinneapple_blender"]),
    ("Núcleo", "CORE", ["pinneapple_core", "pinneapple_problemdesign", "pinneapple_registry", "pinneapple_tools", "pinneapple_security", "pinneapple_systems"]),
]

LAYERS_EN = [
    ("Application", "APPS &amp; SERVING", LAYERS[0][2]),
    ("Models", "NEURAL", LAYERS[1][2]),
    ("Physics &amp; solvers", "PHYSICS", LAYERS[2][2]),
    ("Analysis", "ANALYSIS &amp; UQ", LAYERS[3][2]),
    ("Data &amp; geometry", "DATA", LAYERS[4][2]),
    ("Core", "CORE", LAYERS[5][2]),
]

LIB = {
    "pt": dict(
        eyebrow="A biblioteca",
        h1="Um pipeline, do PDE escrito à predição servida.",
        lead="Cada camada é um pacote Python independente no PyPI — dá para usar só a parte que você precisa. Nenhuma camada esconde a de baixo: você vê a malha, o resíduo, a arquitetura e o erro.",
        stack_h="Arquitetura em camadas",
        start_h="A equação entra como texto",
        start_p="Instalação com um comando, sem build. O mesmo pacote roda o problema, o treino, a comparação com o solver e o relatório.",
        gains_h="O que você ganha no primeiro dia",
        gains=[
            "<b>Um ambiente reproduzível</b> — 248 exemplos com saída versionada, para comparar com o seu resultado.",
            "<b>Benchmarks públicos</b> — SSQN Helmholtz, LBM vortex shedding, espaço de projeto LPM, latência e I/O.",
            "<b>Interoperabilidade real</b> — OpenFOAM, CalculiX, FEniCS/dolfinx, Gmsh, VTK, STL, USD e glTF na mesma sessão.",
            "<b>Padrões da indústria</b> — AAS, DTDL, NGSI-LD, Eclipse Ditto e OPC UA para o que a planta já consome.",
        ],
        oss_h="A base é pública. A verificação também.",
        oss_p="Apache-2.0, no PyPI, com releases versionadas. O que é aberto está aberto de verdade — e o que é produto está dito como produto.",
        honest="Os quatro repositórios acima são genuinamente abertos. Os produtos são entregues como engenharia, não como release de código aberto.",
        repos=[
            ("PINNeAPPle-Labs/PINNeAPPle", "O núcleo: PINN, FNO, DeepONet, GNN, solvers, geometria, UQ, gêmeos digitais e serving REST.", "★ 104 · forks 28 · Apache-2.0 · PyPI 0.7.0"),
            ("PINNeAPPle-Labs/pinnfactory", "Framework leve e independente para PINNs a partir de PDEs em SymPy, com autodiferenciação em PyTorch.", "★ 72 · Apache-2.0 · standalone"),
            ("PINNeAPPle-Labs/PINNeAPPle-Benchmark", "Benchmarks públicos e reprodutíveis: SSQN Helmholtz, LBM vortex shedding, LPM, latência, shard balance.", "reprodutível · gráficos versionados"),
            ("PINNeAPPle-Labs/pinnaitor", "Framework agêntico de uso geral (ELM AI Agentic Framework), em estágio anterior — dito com clareza.", "★ 22 · MIT · estágio inicial"),
        ],
    ),
    "en": dict(
        eyebrow="The library",
        h1="One pipeline, from the written PDE to the served prediction.",
        lead="Every layer is an independent Python package on PyPI — use only the part you need. No layer hides the one below it: you see the mesh, the residual, the architecture and the error.",
        stack_h="Layered architecture",
        start_h="The equation goes in as text",
        start_p="One-command install, no build. The same package runs the problem, the training, the comparison against the solver and the report.",
        gains_h="What you get on day one",
        gains=[
            "<b>A reproducible environment</b> — 248 examples with versioned output, to compare against your own result.",
            "<b>Public benchmarks</b> — SSQN Helmholtz, LBM vortex shedding, LPM design space, latency and I/O.",
            "<b>Real interoperability</b> — OpenFOAM, CalculiX, FEniCS/dolfinx, Gmsh, VTK, STL, USD and glTF in one session.",
            "<b>Industry standards</b> — AAS, DTDL, NGSI-LD, Eclipse Ditto and OPC UA for what the plant already consumes.",
        ],
        oss_h="The base is public. So is verification.",
        oss_p="Apache-2.0, on PyPI, with versioned releases. What is open is genuinely open — and what is a product is called a product.",
        honest="The four repositories above are genuinely open source. The products are delivered as engineering, not as an open-source release.",
        repos=[
            ("PINNeAPPle-Labs/PINNeAPPle", "The core: PINN, FNO, DeepONet, GNN, solvers, geometry, UQ, digital twins and REST serving.", "★ 104 · 28 forks · Apache-2.0 · PyPI 0.7.0"),
            ("PINNeAPPle-Labs/pinnfactory", "A lightweight, standalone framework for PINNs from PDEs in SymPy, with PyTorch autodiff.", "★ 72 · Apache-2.0 · standalone"),
            ("PINNeAPPle-Labs/PINNeAPPle-Benchmark", "Public, reproducible benchmarks: SSQN Helmholtz, LBM vortex shedding, LPM, latency, shard balance.", "reproducible · versioned plots"),
            ("PINNeAPPle-Labs/pinnaitor", "A general-purpose agentic framework (ELM AI Agentic Framework), at an earlier stage — said plainly.", "★ 22 · MIT · early stage"),
        ],
    ),
}

CODE = """<pre class="code"><span class="c"># o coeficiente h que ninguém mede, a partir de alguns termopares</span>
<span class="k">from</span> pinneapple_physics <span class="k">import</span> HeatConduction1D
<span class="k">from</span> pinneapple_neural <span class="k">import</span> PINNTrainer

problem = HeatConduction1D(conductivity=<span class="n">50.0</span>, length=<span class="n">0.30</span>, learn_h=<span class="k">True</span>)
model = PINNTrainer(problem, layers=[<span class="n">3</span>, <span class="n">64</span>, <span class="n">64</span>, <span class="n">1</span>])
report = model.fit(thermocouples=medicoes, epochs=<span class="n">5000</span>)

<span class="f">print</span>(report.h, report.h_std)         <span class="c"># 14.8 0.3  (verdadeiro: 15)</span>
report.verify_against(<span class="s">"finite-volume"</span>)  <span class="c"># erro por campo, mapa de erro</span></pre>"""

CODE_EN = CODE.replace("o coeficiente h que ninguém mede, a partir de alguns termopares",
                       "the h nobody measures, from a handful of thermocouples") \
               .replace("verdadeiro: 15", "true value: 15") \
               .replace("erro por campo, mapa de erro", "per-field error, error map") \
               .replace("medicoes", "readings")


def page_lib(lang: str) -> str:
    root = up(lang, "lib")
    C = LIB[lang]
    layers = LAYERS if lang == "pt" else LAYERS_EN
    stack = "".join(
        f'<div class="layer"><div class="lname">{name}<small>{sub}</small></div>'
        f'<div class="lmods">{"".join(f"<span>{m}</span>" for m in mods)}</div></div>\n'
        for name, sub, mods in layers
    )
    gains = "".join(f"<li>{g}</li>" for g in C["gains"])
    repos = "".join(
        f'''<article class="repo">
          <div><h3><svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8a8 8 0 0 0 5.47 7.59c.4.07.55-.17.55-.38v-1.34c-2.23.48-2.7-1.07-2.7-1.07-.36-.93-.89-1.18-.89-1.18-.73-.5.05-.49.05-.49.81.06 1.23.83 1.23.83.72 1.23 1.88.87 2.34.67.07-.52.28-.88.51-1.08-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.6 7.6 0 0 1 4 0c1.53-1.03 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.28.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48v2.19c0 .21.15.46.55.38A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>{name}</h3>
            <p>{desc}</p><div class="rmeta"><span>{meta}</span></div></div>
          <div class="rlinks"><a class="btn btn-ghost btn-sm" href="https://github.com/{name}" target="_blank" rel="noopener">GitHub</a></div>
        </article>'''
        for name, desc, meta in C["repos"]
    )

    return "".join([
        head(lang, "lib", root), header(lang, "lib", root),
        f"""<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow">{C['eyebrow']}</p>
      <h1>{C['h1']}</h1>
      <p class="lead" style="max-width:68ch">{C['lead']}</p>
      <div class="hero-meta">
        <span class="chip"><span class="dot"></span>PyPI 0.7.0</span>
        <span class="chip">Python ≥ 3.10</span>
        <span class="chip">31 módulos</span>
        <span class="chip">248 exemplos</span>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{_k(lang, 'arquitetura')}</p><h2>{C['stack_h']}</h2></div>
      <div class="stack reveal">
{stack}      </div>
      <div class="note reveal"><span><b>{'Por que isso importa' if lang == 'pt' else 'Why this matters'}:</b> {'a mesma biblioteca que treina a rede é a que roda o solver de referência. Comparar o modelo com ele mesmo é o erro mais comum em Physics AI — aqui a referência é sempre externa ao treino.' if lang == 'pt' else 'the same library that trains the network also runs the reference solver. Comparing a model against itself is the most common mistake in Physics AI — here the reference is always external to training.'}</span></div>
    </div>
  </section>

  <section class="alt">
    <div class="wrap split-block reveal">
      <div class="code-card">
        <div class="code-head"><span class="fname">inverse_heat.py</span></div>
        {CODE if lang == 'pt' else CODE_EN}
      </div>
      <div>
        <p class="eyebrow">{_k(lang, 'comecar')}</p>
        <h2 style="font-size:clamp(1.5rem,2.8vw,2rem);margin-bottom:1rem">{C['start_h']}</h2>
        <p style="color:var(--text-dim)">{C['start_p']}</p>
        <h3 style="margin:1.8rem 0 .8rem">{C['gains_h']}</h3>
        <ul class="checks">{gains}</ul>
        <p class="section-cta" style="margin-top:1.6rem">{wa_button(lang)}<a class="btn btn-ghost" href="{DOCS}" target="_blank" rel="noopener">{'Abrir a documentação' if lang == 'pt' else 'Open the docs'} ↗</a></p>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{_k(lang, 'aberto')}</p><h2>{C['oss_h']}</h2></div>
        <p>{C['oss_p']}</p>
      </div>
      <div class="grid-2 reveal">{repos}</div>
      <div class="note reveal"><span><b>{'A separação honesta' if lang == 'pt' else 'The honest split'}:</b> {C['honest']}</span></div>
    </div>
  </section>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, "lib", root),
    ])


# ---------------------------------------------------------------------------
# Page: story
# ---------------------------------------------------------------------------

STORY = {
    "pt": dict(
        eyebrow="História",
        h1="A PINNeAPPle existe porque a conta tinha que aparecer.",
        lead="Modelos de IA para engenharia são fáceis de vender e difíceis de acreditar. A PINNeAPPle começou como uma biblioteca pessoal para não ter de confiar: cada resultado carrega a referência contra a qual foi conferido.",
        why_h="Por que padrão de verificação, e não só modelo",
        why=[
            ("O problema", "Uma PINN pode acertar o alvo e violar a equação no caminho. A loss de treino parece saudável e o resíduo da física está centenas de vezes acima do limiar — foi exatamente o que encontramos num modelo já treinado de um cliente real."),
            ("A regra", "Se não tem número medido contra uma referência externa ao treino, não vai para a tela. Isso vale para um README, para um slide e para a landing page."),
            ("O custo", "Dizer \"não\" é parte do produto. Num caso de mobilidade de rover, o método numérico clássico era mais rápido e mais exato que a rede — a recomendação foi o método clássico."),
        ],
        how_h="Como é construída",
        how=[
            ("Código aberto primeiro", "31 módulos no PyPI, Apache-2.0, 248 exemplos com saída conferida. A base é pública porque uma ferramenta de verificação que ninguém pode auditar não verifica nada."),
            ("Benchmarks públicos", "SSQN Helmholtz, LBM vortex shedding, espaço de projeto LPM, latência e I/O. Nada de benchmark interno apresentado como prova."),
            ("63 aplicações", "Cada uma com README, números e limites declarados. Servem de ponto de partida para um produto seu ou de prova de que a base aguenta o caso real."),
        ],
        who_h="Quem constrói",
        who="Física, engenharia industrial e software no mesmo time. A regra é a mesma de antes: se não tem número medido, não vai para a tela.",
        person_name="Yan Barros",
        person_role="criador do PINNeAPPle",
        person_bio="Físico de formação, une física, IA e engenharia para levar modelos científicos a aplicações reais. Criou o PINNeAPPle e atua com IA aplicada a problemas de engenharia e indústria no Brasil. Tem experiência em clima, agronegócio e astrofísica solar.",
        stats_h="Em números",
        stats=[("104", "estrelas no GitHub"), ("63", "aplicações construídas"), ("31", "módulos publicados"), ("248", "exemplos executáveis")],
    ),
    "en": dict(
        eyebrow="Story",
        h1="PINNeAPPle exists because the working had to be visible.",
        lead="AI models for engineering are easy to sell and hard to believe. PINNeAPPle started as a personal library so its author would not have to take anything on trust: every result carries the reference it was checked against.",
        why_h="Why verification first, and not just a model",
        why=[
            ("The problem", "A PINN can hit its target while violating the equation along the way. The training loss looks healthy and the physics residual sits hundreds of times over the threshold — which is exactly what we found in an already-trained model from a real client."),
            ("The rule", "If it has no number measured against a reference external to training, it does not go on screen. That holds for a README, for a slide and for this landing page."),
            ("The cost", "Saying \"no\" is part of the product. In one rover-mobility case the classical numerical method was faster and more accurate than the network — the recommendation was the classical method."),
        ],
        how_h="How it is built",
        how=[
            ("Open source first", "31 modules on PyPI, Apache-2.0, 248 examples with checked output. The base is public because a verification tool nobody can audit verifies nothing."),
            ("Public benchmarks", "SSQN Helmholtz, LBM vortex shedding, LPM design space, latency and I/O. No internal benchmark presented as proof."),
            ("63 applications", "Each with a README, numbers and stated limits. They are a starting point for your own product, or proof that the base holds up on the real case."),
        ],
        who_h="Who builds it",
        who="Physics, industrial engineering and software on the same team. The rule is the same as before: if it has no measured number, it does not go on screen.",
        person_name="Yan Barros",
        person_role="creator of PINNeAPPle",
        person_bio="A physicist by training, he combines physics, AI and engineering to take scientific models into real applications. He created PINNeAPPle and works on AI applied to real engineering and industrial problems in Brazil. His background includes climate, agribusiness and solar astrophysics.",
        stats_h="In numbers",
        stats=[("104", "GitHub stars"), ("63", "applications built"), ("31", "published modules"), ("248", "runnable examples")],
    ),
}


def page_historia(lang: str) -> str:
    root = up(lang, "historia")
    C = STORY[lang]
    why = "".join(f'<div class="story-row"><span class="k">{k}</span><p>{v}</p></div>' for k, v in C["why"])
    how = "".join(f'<div class="story-row"><span class="k">{k}</span><p>{v}</p></div>' for k, v in C["how"])
    stats = "".join(f'<div class="exist-cell"><b>{n}</b><span>{l}</span></div>' for n, l in C["stats"])

    return "".join([
        head(lang, "historia", root), header(lang, "historia", root),
        f"""<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow">{C['eyebrow']}</p>
      <h1>{C['h1']}</h1>
      <p class="lead" style="max-width:68ch">{C['lead']}</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{_k(lang, 'porque')}</p><h2>{C['why_h']}</h2></div>
      <div class="story reveal">{why}</div>
    </div>
  </section>

  <section class="alt">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{_k(lang, 'como')}</p><h2>{C['how_h']}</h2></div>
      <div class="story reveal">{how}</div>
      <div class="exist-grid reveal" style="margin-top:2.5rem">{stats}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{_k(lang, 'equipe')}</p><h2>{C['who_h']}</h2><p>{C['who']}</p></div>
      <div class="card" style="padding:1.8rem;max-width:44rem">
        <div class="person">
          <img src="{root}img/team/yan-barros.jpg" alt="{C['person_name']}" loading="lazy" decoding="async" />
          <div>
            <strong>{C['person_name']}</strong>
            <span class="role">{C['person_role']}</span>
            <p>{C['person_bio']}</p>
            <a href="https://www.linkedin.com/in/yan-barros-yan" target="_blank" rel="noopener">LinkedIn →</a>
          </div>
        </div>
      </div>
    </div>
  </section>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, "historia", root),
    ])


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

BUILDERS = {"home": page_home, "casos": page_casos, "lib": page_lib, "historia": page_historia}


def build() -> list[str]:
    written = []
    for page, builder in BUILDERS.items():
        for lang in LANGUAGES:
            rel = url(lang, page)
            out = ROOT / rel / "index.html" if rel else ROOT / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(builder(lang), encoding="utf-8")
            written.append(str(out.relative_to(ROOT)))
    return written


def write_sitemap() -> str:
    """Every page in every language, with the hreflang alternates search engines use."""
    entries = []
    for page in PAGES:
        for lang in LANGUAGES:
            alternates = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{LANGUAGES[o]["code"]}" href="{SITE}/{url(o, page)}"/>'
                for o in LANGUAGES
            )
            priority = "1.0" if page == "home" else "0.8"
            entries.append(
                f"  <url>\n    <loc>{SITE}/{url(lang, page)}</loc>\n{alternates}\n"
                f"    <priority>{priority}</priority>\n  </url>"
            )
    body = "\n".join(entries)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{body}\n</urlset>\n"
    )
    out = ROOT / "sitemap.xml"
    out.write_text(xml, encoding="utf-8")
    return str(out.relative_to(ROOT))


def main() -> int:
    for path in build():
        print("wrote", path)
    print("wrote", write_sitemap())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
