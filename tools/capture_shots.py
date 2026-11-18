#!/usr/bin/env python3
"""Captures the Studio app screenshots the site shows, in dark mode.

    python3 tools/capture_shots.py [--url http://127.0.0.1:8010/] [--key-file /tmp/pea_key.txt] [--lang pt|en]

The app must be running. Writes `img/eng/*.webp` plus `img/eng/studio-home.jpg`
(the Open Graph image, which has to be JPEG). With `--lang en` every file gets an
`-en` suffix and the UI is switched to English, which is what the English card of
the LinkedIn post uses; the site itself shows the Portuguese captures.

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
RUN_LABEL = {"pt": "Rodar", "en": "Run"}


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
    ap.add_argument("--lang", choices=["pt", "en"], default="pt",
                    help="en writes every file with an -en suffix, in an English UI")
    args = ap.parse_args()

    sfx = "" if args.lang == "pt" else "-en"
    run_label = RUN_LABEL[args.lang]
    key = re.search(r"pea_[A-Za-z0-9_-]+", args.key_file.read_text()).group(0)  # keys may carry a hyphen
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
        page.select_option("#lang", args.lang)
        page.wait_for_timeout(700)
        if page.locator("#keybtn").is_visible():
            page.click("#keybtn")
            page.fill("#keyin", key)
            page.click("#keysave")
            page.wait_for_timeout(400)

        # 1. the home screen
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(500)
        save(page, f"studio-home{sfx}.webp")
        im = Image.open(OUT / f"studio-home{sfx}.webp").convert("RGB")
        im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS).save(
            OUT / f"studio-home{sfx}.jpg", "JPEG", quality=86, optimize=True, progressive=True
        )
        print(f"{f'studio-home{sfx}.jpg':24} {im.width}x{im.height}  "
              f"{(OUT / f'studio-home{sfx}.jpg').stat().st_size // 1024} KB")

        # every shot below is a viewport of 1366x900
        page.set_viewport_size({"width": W, "height": H})

        # 2. the search results
        page.fill("#hq", QUERY)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
        save(page, f"studio-explore{sfx}.webp")

        # 3. a job: the tool, the run, and the checks coming back
        page.click(PRESET)
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.click(f"button:has-text('{run_label}')")
        for _ in range(120):
            page.wait_for_timeout(500)
            if "Verifica" in page.evaluate("document.body.innerText") or \
               "Checks" in page.evaluate("document.body.innerText"):
                break
        page.wait_for_timeout(1200)
        # frame the run from the button down: the job, the verdict and the checks are
        # what the page claims, so they all have to be in the picture
        page.evaluate("""(label) => {
            const run = [...document.querySelectorAll('button')]
                .find(b => b.innerText.trim() === label);
            if (run) {
                run.scrollIntoView({block: 'start'});
                window.scrollBy(0, -140);
            }
        }""", run_label)
        page.wait_for_timeout(800)
        save(page, f"studio-report{sfx}.webp")

        # 4. coverage
        page.click('a[href="#/cobertura"]')
        page.wait_for_timeout(2500)
        save(page, f"studio-coverage{sfx}.webp")

        ctx.close()
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
