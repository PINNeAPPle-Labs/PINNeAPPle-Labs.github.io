#!/usr/bin/env python3
"""Renderiza card.html num PNG pronto para o LinkedIn.

    python3 tools/linkedin/pre-acesso-2027/render.py

Sai `card.png` (1200x1200, PNG) e `card.jpg` (JPEG de 1200x1200, qualidade 92,
que é o que o LinkedIn recomprime melhor). O HTML é a fonte: mexa nele, rode de
novo. Depende de Chrome instalado e de `playwright` (o mesmo que os outros
scripts de `tools/`).
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PNG = HERE / "card.png"
JPG = HERE / "card.jpg"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=2)
        page.goto((HERE / "card.html").as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        page.locator("body").screenshot(path=str(PNG))
        browser.close()

    from PIL import Image

    im = Image.open(PNG).convert("RGB")
    im.resize((1200, 1200), Image.LANCZOS).save(JPG, quality=92, optimize=True)
    print(f"wrote {PNG.name} ({PNG.stat().st_size // 1024} KB) and {JPG.name} ({JPG.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
