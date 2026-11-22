#!/usr/bin/env python3
"""O motor de Cinema em um comando: grava, recorta, monta o técnico e registra a proveniência.

Cada etapa já existia como script solto; este é o ponto de entrada que as encadeia na ordem certa e
recusa pular etapa. Não é gerador de vídeo: o quadro vem da app real (Playwright) e o resto é
composição determinística sobre o que a app mostrou.

    python cinema.py estado                 # o que existe por episódio, sem tocar em nada
    python cinema.py gravar ahmed           # re-grava um episódio (a app precisa estar de pé)
    python cinema.py vertical [episódio]    # 9:16 a partir de midia/
    python cinema.py tecnico [episódio]     # 16:9 de 60 s com as cartelas
    python cinema.py manifesto [--biblioteca]
    python cinema.py tudo                   # vertical + tecnico + manifesto, em todos
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MIDIA, VERTICAL, TECNICA = AQUI / "midia", AQUI / "midia-vertical", AQUI / "midia-tecnica"
EPISODIOS = [
    "01-eletromagnetismo", "02-aerodinamica-externa", "03-aviacao", "04-termico-trocador",
    "05-termico-eletronica", "06-acustica", "07-freio", "08-mecanica-solidos", "09-astronomia",
    "10-optica",
]


def _rodar(script: str, *args: str) -> int:
    cmd = [sys.executable, str(AQUI / script), *args]
    return subprocess.run(cmd, cwd=AQUI).returncode


def estado() -> int:
    """Uma linha por episódio: gravado, 9:16, técnico, manifesto. Nada é gerado."""
    print(f"{'episódio':<26} {'16:9':<6} {'9:16':<6} {'técnico':<8} manifesto")
    faltando = 0
    for ep in EPISODIOS:
        col = [("sim" if (MIDIA / f"{ep}.mp4").is_file() else "—"),
               ("sim" if (VERTICAL / f"{ep}.mp4").is_file() else "—"),
               ("sim" if (TECNICA / f"{ep}.mp4").is_file() else "—"),
               ("sim" if (MIDIA / f"{ep}.manifest.json").is_file() else "—")]
        faltando += sum(1 for c in col if c == "—")
        print(f"{ep:<26} {col[0]:<6} {col[1]:<6} {col[2]:<8} {col[3]}")
    print(f"\n{faltando} etapa(s) faltando")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    acao, *resto = sys.argv[1:]
    alvo = [a for a in resto if not a.startswith("--")]
    if acao == "estado":
        return estado()
    if acao == "gravar":
        if not alvo:
            print("qual episódio? (chaves em gravar.py: PORTAS)")
            return 1
        return _rodar("gravar.py", alvo[0])
    if acao == "vertical":
        return _rodar("vertical.py", *alvo)
    if acao == "tecnico":
        return _rodar("tecnico.py", *alvo)
    if acao == "manifesto":
        return _rodar("manifesto.py", *alvo, *[a for a in resto if a.startswith("--")])
    if acao == "tudo":
        for etapa in ("vertical.py", "tecnico.py"):
            if _rodar(etapa, *alvo):
                return 1
        return _rodar("manifesto.py", *alvo, *[a for a in resto if a.startswith("--")])
    print(f"ação desconhecida: {acao}. Use estado, gravar, vertical, tecnico, manifesto ou tudo.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
