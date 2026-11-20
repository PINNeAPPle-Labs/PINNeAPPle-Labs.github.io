"""Estilo das figuras e dos vídeos das duas séries.

Cores, fontes e geometria do slide iguais às do carrossel (`serie-1/card.html`), para o vídeo e
o carrossel parecerem a mesma casa. As fontes são convertidas de woff2 (o que o site usa) para
ttf no primeiro uso, porque o matplotlib não lê woff2.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

HERE = Path(__file__).resolve().parent
FONTES_SITE = HERE.parents[4] / "fonts"           # PINNeAPPle-Labs.github.io/fonts
FONTES_TTF = HERE / "fontes"

SUPERFICIE = "#262626"
SUPERFICIE_2 = "#2f2f2f"
LINHA = "#3e3e3e"
TINTA = "#f1f1f1"
TINTA_2 = "#b6b6b6"
AZUL = "#0081be"
LARANJA = "#a23a00"
ACENTO = "#e07a3c"        # tinta clara do laranja, legível sobre #262626
ACENTO_2 = "#3fa9dc"      # tinta clara do azul
VERDE = "#8ed08e"
VIOLETA = "#b48ce0"

PALETA = [ACENTO_2, ACENTO, VERDE, VIOLETA, "#d9c26a", "#d97fa8"]

ARQUIVOS = {
    "oxanium": "oxanium-latin.woff2",
    "archivo": "k3kPo8UDI-1M0wlSV9XAw6lQkqWY8Q82sLydOxKsv4Rn.woff2",
    "mono": "tDbv2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8yKwBNntkaToggR7BYRbKPxDcwgknk-4.woff2",
}

# (chave do woff2, peso da instância, família, estilo, nome do ttf)
INSTANCIAS = [
    ("oxanium", 700, "Oxanium", "Bold", "oxanium-bold.ttf"),
    ("archivo", 400, "Archivo", "Regular", "archivo-regular.ttf"),
    ("archivo", 600, "Archivo", "SemiBold", "archivo-semibold.ttf"),
    ("mono", 400, "JetBrains Mono", "Regular", "mono-regular.ttf"),
]


def _instanciar(origem: Path, peso: int, familia: str, estilo: str, destino: Path) -> None:
    """Abre o woff2 (variável), fixa o peso e renomeia, para o matplotlib achar por família."""
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    fonte = TTFont(origem)
    fonte.flavor = None
    if "fvar" in fonte:
        eixos = {eixo.axisTag: eixo.defaultValue for eixo in fonte["fvar"].axes}
        eixos["wght"] = peso
        fonte = instancer.instantiateVariableFont(fonte, eixos, updateFontNames=False)
    for registro in list(fonte["name"].names):
        if registro.nameID == 1:
            registro.string = familia
        elif registro.nameID == 2:
            registro.string = estilo
        elif registro.nameID == 4:
            registro.string = f"{familia} {estilo}"
        elif registro.nameID == 6:
            registro.string = f"{familia.replace(' ', '')}-{estilo}"
    if "OS/2" in fonte:
        fonte["OS/2"].usWeightClass = peso
    destino.parent.mkdir(parents=True, exist_ok=True)
    fonte.save(destino)


def _prepara_fontes() -> None:
    """woff2 -> ttf instanciado, uma vez, e registra no matplotlib."""
    FONTES_TTF.mkdir(exist_ok=True)
    for chave, peso, familia, estilo_nome, ttf in INSTANCIAS:
        destino = FONTES_TTF / ttf
        if not destino.exists():
            _instanciar(FONTES_SITE / ARQUIVOS[chave], peso, familia, estilo_nome, destino)
        font_manager.fontManager.addfont(str(destino))

    plt.rcParams.update({
        "font.family": ["Archivo", "DejaVu Sans"],
        "font.monospace": ["JetBrains Mono", "DejaVu Sans Mono"],
        "font.size": 11,
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "savefig.facecolor": SUPERFICIE,
        "text.color": TINTA,
        "axes.labelcolor": TINTA_2,
        "axes.edgecolor": LINHA,
        "xtick.color": TINTA_2,
        "ytick.color": TINTA_2,
        "axes.titlecolor": TINTA,
        "grid.color": "#3a3a3a",
        "grid.linewidth": 0.8,
        "axes.grid": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.labelcolor": TINTA_2,
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.dpi": 110,
    })


_prepara_fontes()


def quadro(fig, kicker: str, titulo: str, rodape: str = "", n: int = 0, total: int = 0):
    """Moldura do vídeo: faixa azul no topo, kicker, título e rodapé da marca."""
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=AZUL, edgecolor="none", zorder=50))
    fig.text(0.055, 0.965, kicker.upper(), color=ACENTO_2, fontsize=10.5,
             family="monospace", ha="left", va="top")
    fig.text(0.055, 0.935, titulo, color=TINTA, fontsize=17, ha="left", va="top")
    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=LINHA, linewidth=0.9, zorder=50))
    fig.text(0.055, 0.028, "PINNeAPPle", color=TINTA, fontsize=9, family="monospace", va="bottom")
    fig.text(0.5, 0.028, rodape, color="#7a7a7a", fontsize=8.5, family="monospace",
             va="bottom", ha="center")
    if n and total:
        fig.text(0.945, 0.028, f"{n} / {total}", color="#7a7a7a", fontsize=8.5,
                 family="monospace", va="bottom", ha="right")


def painel(ax, titulo: str, ylabel: str = "", xlabel: str = ""):
    """Um painel de gráfico com o mesmo cabeçalho de todos os episódios."""
    ax.set_title(titulo, loc="left", fontsize=12.5, color=TINTA, pad=8)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_axisbelow(True)
    return ax
