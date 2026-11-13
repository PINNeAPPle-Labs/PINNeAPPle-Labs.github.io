#!/usr/bin/env python3
"""Renderiza card.html nos PNGs prontos para o LinkedIn, em pt e em en.

    python3 tools/linkedin/pre-acesso-2027/render.py

Sai `card.png` + `card.jpg` (português) e `card-en.png` + `card-en.jpg`
(inglês), todos 1200x1200. O JPEG de 1200 px é o que se sobe no LinkedIn; o
PNG é o master em 2x. O HTML é a fonte: mexa nele, rode de novo. Depende de
Chrome instalado e de `playwright` (o mesmo dos outros scripts de `tools/`).
"""

from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
LANGS = {"pt": "card", "en": "card-en"}


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=2)
        for lang, stem in LANGS.items():
            page.goto((HERE / "card.html").as_uri() + f"?lang={lang}", wait_until="load")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            png = HERE / f"{stem}.png"
            page.locator("body").screenshot(path=str(png))
            jpg = HERE / f"{stem}.jpg"
            Image.open(png).convert("RGB").resize((1200, 1200), Image.LANCZOS).save(
                jpg, quality=92, optimize=True
            )
            print(f"{lang}: {png.name} ({png.stat().st_size // 1024} KB), "
                  f"{jpg.name} ({jpg.stat().st_size // 1024} KB)")
        browser.close()


if __name__ == "__main__":
    main()
