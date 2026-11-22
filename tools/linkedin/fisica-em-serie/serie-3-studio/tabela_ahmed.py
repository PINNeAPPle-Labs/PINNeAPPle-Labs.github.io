#!/usr/bin/env python3
"""A tabela de validação do episódio 02, montada a partir dos resultados — nunca digitada à mão.

Lê ``_runs/cfd/results/*.json`` da campanha do corpo de Ahmed (OpenFOAM k-omega SST) e a referência
de Ahmed, Ram & Garon (1984), e imprime o Markdown que vai para a ficha e para o vídeo técnico. A
malha é escolhida pelo prefixo do id da corrida: ``val_*`` é a L1, ``valL2_*`` a L2.

    PINNEAPPLE_AHMED_RUNS=... python tabela_ahmed.py

O caminho padrão é o do checkout local; ``_runs/`` não é versionado (é dado, não código).
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

PADRAO = Path("/Users/yanbarros/Documents/GitHub/pinneapple-labs/PINNeAPPle/examples/end_to_end/"
              "ahmed_body/_runs/cfd/results")
# Ahmed, Ram & Garon (1984), SAE 840300: CD medido no túnel a 60 m/s, folga ao solo de 0,05 m.
AHMED_1984 = {0.0: 0.250, 12.5: 0.230, 25.0: 0.285, 30.0: 0.378, 35.0: 0.260, 40.0: 0.250}


def corridas(pasta: Path) -> list[dict]:
    out = []
    for p in sorted(glob.glob(str(pasta / "*.json"))):
        d = json.load(open(p))
        if d.get("ok") and d.get("outputs") and d.get("params", {}).get("speed") == 60.0:
            out.append(d)
    return out


def por_angulo(rs: list[dict], prefixo: str) -> dict[float, float]:
    """CD por ângulo de inclinação, na malha pedida (``val_`` = L1, ``valL2_`` = L2)."""
    m = {}
    for d in rs:
        rid = d["id"]
        if not rid.startswith(prefixo) or (prefixo == "val_" and rid.startswith("valL2")):
            continue
        m[round(float(d["params"]["slant_deg"]), 1)] = float(d["outputs"]["CD"])
    return m


def _celula(c: float | None, ref: float) -> tuple[str, str]:
    return (f"{c:.4f}", f"{100 * (c - ref) / ref:+.1f}%") if c else ("—", "—")


def tabela(l1: dict[float, float], l2: dict[float, float]) -> str:
    linhas = ["| inclinação | Ahmed 1984 | L1 (CD) | desvio | L2 (CD) | desvio |",
              "|---|---|---|---|---|---|"]
    for a in sorted(AHMED_1984):
        ref = AHMED_1984[a]
        (c1, d1), (c2, d2) = _celula(l1.get(a), ref), _celula(l2.get(a), ref)
        linhas.append(f"| {a:g}° | {ref:.3f} | {c1} | {d1} | {c2} | {d2} |")
    return "\n".join(linhas)


def main() -> None:
    pasta = Path(os.environ.get("PINNEAPPLE_AHMED_RUNS", PADRAO))
    rs = corridas(pasta)
    l1, l2 = por_angulo(rs, "val_"), por_angulo(rs, "valL2_")
    print(f"<!-- {len(rs)} corridas de validação (60 m/s) em {pasta}; L1: {len(l1)} ângulos, L2: {len(l2)} -->")
    print(tabela(l1, l2))


if __name__ == "__main__":
    main()
