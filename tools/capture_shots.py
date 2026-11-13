#!/usr/bin/env python3
"""Captures the Studio app screenshots the site shows, in dark mode.

    python3 tools/capture_shots.py [--url http://127.0.0.1:8010/] [--key-file /tmp/pea_key.txt]

The app must be running. Writes `img/eng/*.webp` plus `img/eng/studio-home.jpg`
(the Open Graph image, which has to be JPEG).

Why capture instead of importing the PNGs from `pinneapple-engineering-api/docs/screenshots`:
those are in the light theme, and a light capture in a dark page reads as a hole punched
through the layout. The app has a dark theme, so the honest fix is to photograph the app
the way the page shows it, not to tint the picture.

Viewport shots (1366x900), never full-page: a full-page capture scrolls the content and
leaves the sticky nav printed in the middle of the image, which looks like a rendering bug.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "img" / "eng"
W, H = 1366, 900
HOME_H = 916  # home content ends here; taller would only add empty space
QUERY = "dissipador de calor com aletas"
PRESET = 'a[href*="#/tool/preset%3Aplate_fin_heatsink_forced"]'


def save(page, name: str, webp: bool = True) -> None:
    tmp = OUT / f".{name}.png"
    page.screenshot(path=str(tmp))
    im = Image.open(tmp).convert("RGB")
    if webp:
        im.save(OUT / name, "WEBP", quality=84, method=6)
    tmp.unlink()
    print(f"{name:24} {im.width}x{im.height}  {(OUT / name).stat().st_size // 1024} KB")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8010/")
    ap.add_argument("--key-file", type=Path, default=Path("/tmp/pea_key.txt"))
    args = ap.parse_args()

    key = re.search(r"pea_[A-Za-z0-9]+", args.key_file.read_text()).group(0)
    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        ctx = browser.new_context(
            viewport={"width": W, "height": HOME_H},
            device_scale_factor=1,
        )
        page = ctx.new_page()
        page.goto(args.url, wait_until="networkidle")
        page.select_option("#theme", "dark")
        page.wait_for_timeout(700)
        if page.locator("#keybtn").is_visible():
            page.click("#keybtn")
            page.fill("#keyin", key)
            page.click("#keysave")
            page.wait_for_timeout(400)

        # 1. the home screen
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(500)
        save(page, "studio-home.webp")
        im = Image.open(OUT / "studio-home.webp").convert("RGB")
        im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS).save(
            OUT / "studio-home.jpg", "JPEG", quality=86, optimize=True, progressive=True
        )
        print(f"{'studio-home.jpg':24} {im.width}x{im.height}  "
              f"{(OUT / 'studio-home.jpg').stat().st_size // 1024} KB")

        # every shot below is a viewport of 1366x900
        page.set_viewport_size({"width": W, "height": H})

        # 2. the search results
        page.fill("#hq", QUERY)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
        save(page, "studio-explore.webp")

        # 3. a job: the tool, the run, and the checks coming back
        page.click(PRESET)
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.click("button:has-text('Rodar')")
        for _ in range(120):
            page.wait_for_timeout(500)
            if "Verificações" in page.evaluate("document.body.innerText"):
                break
        page.wait_for_timeout(1200)
        # frame the run from the button down: the job, the verdict and the checks are
        # what the page claims, so they all have to be in the picture
        page.evaluate("""() => {
            const run = [...document.querySelectorAll('button')]
                .find(b => b.innerText.trim() === 'Rodar');
            if (run) {
                run.scrollIntoView({block: 'start'});
                window.scrollBy(0, -140);
            }
        }""")
        page.wait_for_timeout(800)
        save(page, "studio-report.webp")

        # 4. coverage
        page.click('a[href="#/cobertura"]')
        page.wait_for_timeout(2500)
        save(page, "studio-coverage.webp")

        ctx.close()
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
