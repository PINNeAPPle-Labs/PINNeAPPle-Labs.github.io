"""Cartões de texto para os vídeos que são montagem (não simulação ao vivo).

Um cartão é um PNG 1080x1350 com a mesma moldura dos slides do carrossel: faixa azul no topo,
kicker em monoespaçado, título em Oxanium, corpo em Archivo e o rodapé da marca. Serve para
abrir e fechar um episódio, ou para apresentar números entre dois trechos de vídeo.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

import estilo


def cartao(destino: Path, kicker: str, titulo: str, corpo: list[str] | None = None,
           numero: str | None = None, numero_nota: str | None = None,
           rodape: str = "PINNeAPPle") -> Path:
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.962, kicker.upper(), color=estilo.ACENTO_2, fontsize=11,
             family="monospace", va="top")

    y = 0.905
    fig.text(0.055, y, titulo, color=estilo.TINTA, fontsize=30, family="Oxanium",
             va="top", linespacing=1.12)

    if numero:
        fig.text(0.055, 0.700, numero, color=estilo.ACENTO, fontsize=62, family="Oxanium",
                 va="top")
    if numero_nota:
        fig.text(0.055, 0.625, numero_nota, color=estilo.TINTA, fontsize=17, va="top",
                 wrap=True, linespacing=1.35)

    if corpo:
        altura = 0.50 if numero else 0.62
        for i, linha in enumerate(corpo):
            yy = altura - i * 0.082
            fig.patches.append(plt.Rectangle((0.055, yy + 0.012), 0.014, 0.014,
                                             transform=fig.transFigure,
                                             facecolor=estilo.LARANJA, edgecolor="none"))
            fig.text(0.085, yy + 0.019, linha, color="#dcdcdc", fontsize=16.5, va="center",
                     wrap=True)

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.text(0.055, 0.028, rodape, color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, "Physics in Action", color="#7a7a7a", fontsize=8.5,
             family="monospace", ha="right")
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig)
    return destino
