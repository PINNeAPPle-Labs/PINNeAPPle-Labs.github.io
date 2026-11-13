#!/usr/bin/env python3
"""Copies experiment figures from the library checkout into the site, ready to serve.

    python3 tools/import_figures.py [--source ../PINNeAPPle/examples]

Each article shows figures produced by the example itself, so the source of truth is
`<examples>/<example>/figures/*.png` (or `_out/figures` for the autolab runs), never a
redrawn chart. What this does:

* the card thumbnail is cropped to 16:10 and written at 1200x750: the article grid
  assumes that aspect and `object-fit: cover` would cut a chart's axis labels,
* body figures keep their native aspect (a chart is read, not cropped), capped at
  1400 px wide, and go out as WebP at quality 88,
* nothing is retouched, recoloured or re-plotted here. If a figure is wrong, it is
  wrong in the example too, and that is the point.

Run it again whenever an example re-runs and its figures change.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "img" / "exp"
THUMB = (1200, 750)          # 16:10, what `.post-card .thumb` expects
BODY_W = 1400

# (example, source figure, output name). A name ending in `-thumb` becomes the
# 16:10 card crop; everything else keeps its aspect ratio.
FIGS = [
    # aerodinâmica autônoma
    ("autolab_aero/_out/figures/pareto.png", "aero-autonoma-thumb"),
    ("autolab_aero/_out/figures/pareto.png", "aero-autonoma-pareto"),
    ("autolab_aero/_out/figures/trust_abc.png", "aero-autonoma-trust"),
    ("autolab_aero/_out/figures/best_wake_vorticity.png", "aero-autonoma-wake"),
    # futebol
    ("sports/figures/ball_flights_3d.png", "futebol-thumb"),
    ("sports/figures/ball_holdout_landing.png", "futebol-pouso"),
    ("sports/figures/ball_flights_3d.png", "futebol-voo"),
    ("sports/figures/pc_reliability.png", "futebol-controle"),
    # ferramentas de dinâmica
    ("dynamics_toolkit/figures/early_warning.png", "dinamica-thumb"),
    ("dynamics_toolkit/figures/first_passage.png", "dinamica-passagem"),
    ("dynamics_toolkit/figures/koopman.png", "dinamica-koopman"),
    ("dynamics_toolkit/figures/early_warning.png", "dinamica-alerta"),
    # Unity / OpenUSD
    ("unity/media/05_blender_still.png", "unity-thumb"),
    ("unity/media/05_blender_still.png", "unity-espuleta"),
    # placa fria com FNO
    ("fno_coldplate/results/fields.png", "fno-campos"),
    ("fno_coldplate/results/checks.png", "fno-checagens"),
    # El Niño
    ("enso_forecasting/figures/plumes.png", "nino-plumas"),
    ("enso_forecasting/figures/skill_vs_lead.png", "nino-habilidade"),
    ("enso_forecasting/figures/spring_barrier.png", "nino-barreira"),
    # rover lunar
    ("autolab_rover/results/traverse.png", "rover-rotas"),
    ("autolab_rover/results/site_map.png", "rover-mapa"),
    ("autolab_rover/results/soil_learning.png", "rover-solo"),
    # construções de bloco
    ("bricks/_out/best_cantilever_cycles.png", "blocos-thumb"),
    ("bricks/_out/best_cantilever_cycles.png", "blocos-balanco"),
    ("bricks/_out/comparison.png", "blocos-comparacao"),
    # eletromagnetismo aplicado
    ("electrodynamics/results/10_pmsm_field.png", "motor-campo"),
    ("electrodynamics/results/14_prius_getdp_crosscheck.png", "motor-getdp"),
    # CO2 supercrítico
    ("potential_co2/figures/identities_all_properties.png", "co2-identidades"),
    ("potential_co2/figures/errors_all_properties.png", "co2-erros"),
    ("potential_co2/figures/isotherms_all_properties.png", "co2-isotermas"),
]


def crop_16_10(im: Image.Image) -> Image.Image:
    target = THUMB[0] / THUMB[1]
    w, h = im.size
    if w / h > target:            # too wide, trim the sides
        nw = round(h * target)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w / target)        # too tall, trim top and bottom
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path,
                    default=ROOT.parent / "PINNeAPPle" / "examples")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    for rel, name in FIGS:
        src = args.source / rel
        if not src.exists():
            print(f"missing: {src}")
            continue
        im = Image.open(src).convert("RGB")
        if name.endswith("-thumb"):
            im = crop_16_10(im).resize(THUMB, Image.LANCZOS)
        elif im.width > BODY_W:
            im = im.resize((BODY_W, round(im.height * BODY_W / im.width)), Image.LANCZOS)
        dest = OUT / f"{name}.webp"
        im.save(dest, "WEBP", quality=88, method=6)
        print(f"{dest.name:28} {im.width}x{im.height}  {dest.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
