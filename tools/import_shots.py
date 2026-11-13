#!/usr/bin/env python3
"""Copies the Engineering app screenshots into the site, ready to serve.

    python3 tools/import_shots.py [--source <checkout>]

Source of truth is the application repository, so the site never shows a screen it
cannot reproduce:

    ../pinneapple-engineering-api/docs/screenshots/studio/*.png

What it does and why
--------------------
* resizes to 1366 px wide (the captures are already that width, retina ones are not),
* crops the long full-page captures to the region that says something on a landing page,
* writes WebP at quality 84 — a PNG of the job report is 300 KB, the WebP is 63 KB,
* also writes `studio-home.jpg`, because link previews (Open Graph) want JPEG.

Run it again whenever the app's screenshots change; commit the output with the HTML.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT.parent / "pinneapple-engineering-api" / "docs" / "screenshots"

# (source file, output name, crop box or None, width)
JOBS = [
    ("studio/desktop-light-01-home.png", "studio-home.webp", None, 1366),
    ("studio/desktop-light-02-explore.png", "studio-explore.webp", None, 1366),
    ("studio/desktop-light-09-coverage.png", "studio-coverage.webp", None, 1366),
    # The report capture is a 2108 px tall PT|EN pair; the top holds the chart, the
    # checks and the evidence status, which is the part the site talks about.
    ("studio/i18n-pt-en-job-report.png", "studio-report.webp", (0, 0, 1386, 1150), 1386),
]

OG = ("studio/desktop-light-01-home.png", "studio-home.jpg", 1200)


def resize(im: Image.Image, width: int) -> Image.Image:
    if im.width <= width:
        return im
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = ap.parse_args()

    out_dir = ROOT / "img" / "eng"
    out_dir.mkdir(parents=True, exist_ok=True)

    for rel, name, crop, width in JOBS:
        src = args.source / rel
        im = Image.open(src).convert("RGB")
        if crop:
            im = im.crop(crop)
        im = resize(im, width)
        im.save(out_dir / name, "WEBP", quality=84, method=6)
        print(f"{name:24} {im.width}x{im.height}  {(out_dir / name).stat().st_size // 1024} KB")

    rel, name, width = OG
    im = resize(Image.open(args.source / rel).convert("RGB"), width)
    im.save(out_dir / name, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"{name:24} {im.width}x{im.height}  {(out_dir / name).stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
