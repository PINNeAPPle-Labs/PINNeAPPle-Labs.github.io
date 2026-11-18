#!/usr/bin/env python3
"""Builds the site's brand images from the logo originals, so no cut is made by hand.

    python3 tools/build_brand_assets.py

Sources, in ``assets/brand/source`` (the shipped logo files, 2000x2000):

    logo-horizontal.png     the lockup, transparent                          -> img/brand/logo-horizontal.png
    logo-vertical.png       the lockup, stacked, transparent                 -> img/brand/logo-vertical.png
    mark.png                the pineapple alone, transparent                 -> img/brand/mark.png
    *-on-dark.png           the same three, on the brand's own #212121 plate (unused by the
                            site, kept because that is how they were delivered)

Every output is cropped to the ink, so the file's box is the logo's box and the layout
does not carry empty margins the designer could not see. The favicons come from the mark,
on the brand background, because a transparent icon disappears on a dark tab bar.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "brand" / "source"
OUT = ROOT / "img" / "brand"

# The site background. The logo files ship on #212121; the site is #262626.
BRAND_BG = (38, 38, 38, 255)


def cropped(name: str) -> Image.Image:
    im = Image.open(SRC / name).convert("RGBA")
    box = im.getchannel("A").getbbox()
    if box is None:
        raise SystemExit(f"{name} is empty")
    return im.crop(box)


def save(im: Image.Image, path: Path, width: int) -> None:
    """Resize to the display width and quantise: the art is three flat colours plus
    antialiasing, so 96 colours are indistinguishable from truecolour and a quarter of
    the bytes."""
    height = round(im.height * width / im.width)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = im.resize((width, height), Image.LANCZOS).quantize(colors=96, method=Image.FASTOCTREE)
    out.save(path, optimize=True)
    print(f"{path.relative_to(ROOT)}  {width}x{height}  {path.stat().st_size // 1024} kB")


def icon(im: Image.Image, size: int, path: Path, pad: float = 0.14, bg=BRAND_BG) -> None:
    """The mark centred on a square plate, so it reads at 16 px."""
    inner = round(size * (1 - 2 * pad))
    scale = min(inner / im.width, inner / im.height)
    art = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    plate = Image.new("RGBA", (size, size), bg)
    plate.alpha_composite(art, ((size - art.width) // 2, (size - art.height) // 2))
    plate.save(path, optimize=True)
    print(f"{path.relative_to(ROOT)}  {size}x{size}  {path.stat().st_size // 1024} kB")


def main() -> None:
    horizontal = cropped("logo-horizontal.png")
    vertical = cropped("logo-vertical.png")
    mark = cropped("mark.png")

    save(horizontal, OUT / "logo-horizontal.png", 720)
    save(vertical, OUT / "logo-vertical.png", 400)
    save(mark, OUT / "mark.png", 200)

    icon(mark, 32, ROOT / "favicon-32.png", pad=0.10)
    icon(mark, 16, ROOT / "favicon-16.png", pad=0.06)
    icon(mark, 180, ROOT / "apple-touch-icon.png", pad=0.18)


if __name__ == "__main__":
    main()
