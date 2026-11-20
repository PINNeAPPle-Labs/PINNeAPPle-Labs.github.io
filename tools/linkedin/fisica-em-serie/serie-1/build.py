#!/usr/bin/env python3
"""Renderiza os carrosséis da Série 1 (The Physics Atlas) a partir de carrosseis.json.

    /opt/homebrew/bin/python3.11 tools/linkedin/fisica-em-serie/serie-1/build.py
    ... build.py --so 01-cfd            # um carrossel só
    ... build.py --langs pt             # só português
    ... build.py --revisao              # não renderiza, só escreve revisao/*.md
    ... build.py --checar               # só confere mídia e campos obrigatórios

Sai, para cada carrossel e idioma:

    img/<slug>-<lang>-NN.png    master 2160x2700
    img/<slug>-<lang>-NN.jpg    o que se sobe no LinkedIn (1080x1350, q92)
    revisao/<slug>.md           a copy em texto, para ler e corrigir

O JSON é a fonte de verdade do carrossel; `legendas.md` guarda o texto do post.
Depende de `playwright` (usado pelos outros scripts de `tools/`) e de Chrome.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAR_DIR = HERE / "carrosseis"
IMG_DIR = HERE / "img"
REV_DIR = HERE / "revisao"
LANGS = ("pt", "en")
SERIE = {"pt": "The Physics Atlas · PINNeAPPle", "en": "The Physics Atlas · PINNeAPPle"}
RODAPE = {"pt": "pinneapple-labs.github.io", "en": "pinneapple-labs.github.io"}


def plain(text) -> str:
    """Troca o markup do slide por markdown, para a revisão ficar legível."""
    if not isinstance(text, str):
        return text
    text = text.replace("<b>", "**").replace("</b>", "**")
    text = text.replace("<i>", "_").replace("</i>", "_")
    return re.sub(r"<[^>]+>", "", text)


def loc(value, lang: str):
    """Resolve um campo que pode ser um texto único ou {pt, en}."""
    if isinstance(value, dict) and "pt" in value and "en" in value:
        return value[lang]
    return value


def load() -> dict:
    """Um JSON por carrossel em carrosseis/, ordenados pelo campo `ordem`."""
    cars = []
    for path in sorted(CAR_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as fh:
            cars.append(json.load(fh))
    cars.sort(key=lambda c: c["ordem"])
    return {"serie": SERIE, "rodape": RODAPE, "carrosseis": cars}


def media_path(rel: str) -> Path:
    return (HERE / rel).resolve()


def check(data: dict) -> list[str]:
    """Confere o que quebraria o render: mídia ausente, campo faltando, slide demais."""
    problems: list[str] = []
    seen = set()
    for car in data["carrosseis"]:
        slug = car["slug"]
        if slug in seen:
            problems.append(f"{slug}: slug repetido")
        seen.add(slug)
        slides = car["slides"]
        n = len(slides)
        if not 6 <= n <= 10:
            problems.append(f"{slug}: {n} slides (o alvo é 8, o limite é 10)")
        if slides[0].get("tipo") != "capa":
            problems.append(f"{slug}: o primeiro slide não é capa")
        if slides[-1].get("tipo") != "fecho":
            problems.append(f"{slug}: o último slide não é fecho")
        for i, s in enumerate(slides, 1):
            for lang in LANGS:
                for field in ("title", "kicker"):
                    if not loc(s.get(field), lang):
                        problems.append(f"{slug} slide {i}: falta {field} ({lang})")
                if s.get("tipo") not in ("capa", "fecho") \
                        and not loc(s.get("nota"), lang) and not loc(s.get("bullets"), lang) \
                        and not loc(s.get("num"), lang):
                    problems.append(f"{slug} slide {i}: slide sem corpo ({lang})")
            img = s.get("image")
            if img and not media_path(img).exists():
                problems.append(f"{slug} slide {i}: mídia ausente -> {img}")
    return problems


def write_revision(data: dict) -> None:
    REV_DIR.mkdir(exist_ok=True)
    for car in data["carrosseis"]:
        out = [f"# {car['ordem']:02d} · {loc(car['titulo'], 'pt')}", ""]
        out.append(f"_{loc(data['serie'], 'pt')} · carrossel {car['ordem']} de {car['total']}_")
        out.append("")
        for i, s in enumerate(car["slides"], 1):
            out.append(f"## Slide {i} — {s.get('tipo')}")
            if s.get("kicker"):
                out.append(f"`{loc(s['kicker'],'pt')}`")
            out.append("")
            out.append(f"**PT** — {plain(loc(s.get('title'),'pt'))}")
            for f in ("sub", "num", "numlabel", "nota", "fonte"):
                if s.get(f):
                    out.append(f"  {plain(loc(s[f],'pt'))}")
            for b in loc(s.get("bullets"), "pt") or []:
                out.append(f"  - {plain(b)}")
            if s.get("chip"):
                out.append(f"  [{s['chip']}]")
            if s.get("image"):
                out.append(f"  `{s['image']}`")
            out.append("")
            out.append(f"**EN** — {plain(loc(s.get('title'),'en'))}")
            for f in ("sub", "num", "numlabel", "nota", "fonte"):
                if s.get(f):
                    out.append(f"  {plain(loc(s[f],'en'))}")
            for b in loc(s.get("bullets"), "en") or []:
                out.append(f"  - {plain(b)}")
            out.append("")
        (REV_DIR / f"{car['slug']}.md").write_text("\n".join(out), encoding="utf-8")
        print(f"revisao/{car['slug']}.md")


def render(data: dict, slugs: list[str], langs: tuple[str, ...], keep_png: bool = False) -> None:
    from PIL import Image
    from playwright.sync_api import sync_playwright

    IMG_DIR.mkdir(exist_ok=True)
    feitos = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1080, "height": 1350},
                                device_scale_factor=2)
        page.goto((HERE / "card.html").as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready")
        for car in data["carrosseis"]:
            if slugs and car["slug"] not in slugs:
                continue
            total = len(car["slides"])
            for lang in langs:
                for i, s in enumerate(car["slides"], 1):
                    dado = {k: loc(v, lang) for k, v in s.items()}
                    dado["n"] = i
                    dado["total"] = total
                    dado["rodape_esq"] = data.get("rodape", {}).get(lang, "")
                    if dado.get("image"):
                        caminho = media_path(dado["image"])
                        dado["image"] = caminho.as_uri()
                        if dado.get("ajuste") == "contain":
                            # A faixa acompanha a proporção da figura: sem tarja preta
                            # sobrando no slide e sem cortar eixo nem legenda.
                            w, h = Image.open(caminho).size
                            dado["altura"] = max(260, min(900, int(920 * h / w)))
                    page.evaluate("d => window.renderSlide(d)", dado)
                    png = IMG_DIR / f"{car['slug']}-{lang}-{i:02d}.png"
                    page.locator("#slide").screenshot(path=str(png))
                    Image.open(png).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(
                        png.with_suffix(".jpg"), quality=92, optimize=True,
                        progressive=True)
                    if not keep_png:
                        png.unlink()
                    feitos += 1
                print(f"{car['slug']} [{lang}] {total} slides")
        browser.close()
    print(f"{feitos} slides renderizados em {IMG_DIR.relative_to(HERE.parent.parent.parent.parent)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--so", nargs="*", default=[], help="slugs a renderizar")
    ap.add_argument("--langs", default="pt,en")
    ap.add_argument("--revisao", action="store_true", help="só escreve a revisão em markdown")
    ap.add_argument("--checar", action="store_true", help="só confere o JSON e a mídia")
    ap.add_argument("--png", action="store_true", help="guarda também o master 2160x2700")
    args = ap.parse_args()

    data = load()
    problems = check(data)
    if problems:
        print("\n".join("  ! " + p for p in problems))
        if args.checar:
            return 1
    elif args.checar:
        print(f"ok: {len(data['carrosseis'])} carrosséis, mídia presente")
        return 0

    write_revision(data)
    if not args.revisao:
        langs = tuple(x.strip() for x in args.langs.split(",") if x.strip())
        render(data, args.so, langs, keep_png=args.png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
