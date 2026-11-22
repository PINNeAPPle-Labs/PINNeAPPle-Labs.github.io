#!/usr/bin/env python3
"""Versão 9:16 de cada episódio, com o gancho legível e a ressalva à vista.

O vídeo original é 16:9 e mostra a tela do Studio: recortar para 9:16 comeria justamente o número
que dá sentido ao episódio. Então a vertical não é recorte — é composição: fundo da marca, o vídeo
inteiro centralizado em 1080 px de largura, o gancho em cima, o número embaixo e, no pé, o que o
episódio **não** afirma.

    python vertical.py            # todos os episódios que tiverem mp4 em midia/
    python vertical.py 05         # só um

Saída em ``midia-vertical/<episódio>.mp4`` (1080x1920, 30 fps, yuv420p).
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
MIDIA = AQUI / "midia"
SAIDA = AQUI / "midia-vertical"

W, H = 1080, 1920
FUNDO = (38, 38, 38)            # #262626, a marca
TINTA = (245, 245, 245)
ACENTO = (0, 129, 190)          # #0081be
ACENTO_2 = (162, 58, 0)         # #a23a00
APAGADO = (150, 150, 150)
FRACO = (110, 110, 110)

VIDEO_Y, VIDEO_H = 505, 700     # a faixa onde o vídeo entra (escalado para 1080 de largura)

FONTE_NEGRITO = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONTE_NORMAL = "/System/Library/Fonts/Supplemental/Arial.ttf"


@dataclass(frozen=True)
class Cartela:
    gancho: str        # o que se lê no primeiro segundo
    numero: str        # a prova, logo abaixo do vídeo
    detalhe: str       # de onde o número vem
    ressalva: str      # o que o episódio não afirma
    app: str


TEXTOS = {
    "01-eletromagnetismo": Cartela(
        "Meu estimate erra o cogging\nem 12,8%. E a tela diz isso.",
        "8,604 contra 7,626 N·m  ·  +2,1% no fluxo",
        "motor de fluxo axial: estimativa quasi-3-D contra a mesma máquina na malha 3-D",
        "não é elemento finito 3-D completo, e os parâmetros são de um motor plausível",
        "afpm_designer"),
    "02-aerodinamica-externa": Cartela(
        "O gêmeo avisa quando\nestá interpolando.",
        "CD 0,2954  ·  distância ao caso de treino 0,03",
        "corpo de Ahmed: twin treinado com a campanha OpenFOAM k-omega SST do próprio estudo",
        "k-omega SST estacionário não reproduz o pico de arrasto logo abaixo de 30°",
        "ahmed_twin"),
    "03-aviacao": Cartela(
        "1.920 asas em 96 s.\nUma virou projeto.",
        "47,9 g CO₂/pkm  ·  Cp do OpenFOAM",
        "aeronave: projeto certificável escolhido sobre o espaço paramétrico varrido",
        "o Cp é de uma corrida guardada, não de um solver no navegador",
        "aero_optimizer"),
    "04-termico-trocador": Cartela(
        "38.301 dissipadores triados.\n24 passam pela física.",
        "62,1 °C  ·  0,371 K/W  ·  17,2 Pa",
        "dissipador extrudado: triagem pelo surrogate, número refeito pela física com +15% de pessimismo",
        "não é CFD: convecção por correlação, condução por volumes finitos nas aletas",
        "heatsink_sizer"),
    "05-termico-eletronica": Cartela(
        "Margem de 0,9 °C\nnão é margem.",
        "FPGA 99,1 °C  ·  limite 100 °C",
        "placa com FPGA/DDR: passa nominalmente, não passa com 20% menos refrigeração",
        "não é CFD do ar: convecção por correlação de placa plana com radiação",
        "pcb_hotspot"),
    "06-acustica": Cartela(
        "40,1 Hz contra 40,0 de alvo.\n0,1%.",
        "Helmholtz conferido na fórmula fechada",
        "duto bass-reflex: o otimizador propõe, a fórmula confere",
        "o ar no duto não tem gradiente: o modelo é concentrado, não um campo acústico",
        "soundshape_ai"),
    "07-freio": Cartela(
        "A tolerância move a temperatura\nem ± 0,2 °C. Menos que o modelo.",
        "65 °C no projeto otimizado  ·  200 amostras",
        "rotor ventilado: Monte Carlo de fabricação recalculado na fórmula, nunca no surrogate",
        "o limite de 500 °C é genérico; a convecção não entra no Monte Carlo",
        "brakecool_ai"),
    "08-mecanica-solidos": Cartela(
        "A espessura pesa\nexatamente o dobro da largura.",
        "elasticidade 22,2 × 11,1",
        "viga de suspensão: vida de fadiga por Basquin, seção reta, carga cíclica declarada",
        "não é FEA: é a fórmula fechada de viga engastada, sem concentração de tensão",
        "ridetune_ai"),
    "09-astronomia": Cartela(
        "O céu de agora:\ncalculado, não fotografado.",
        "Lua a 371.661 km  ·  JPL DE421",
        "céu de São Paulo em 3-D, posições topocêntricas com refração perto do horizonte",
        "posições aparentes, não astrométricas; a cor das estrelas vem do tipo espectral",
        "observatory"),
    "10-optica": Cartela(
        "O mesmo clipe:\nviés de 20,7 nm ou 0,11 nm.",
        "ArF imersão × EUV  ·  Abbe = Hopkins",
        "litografia: imagem aérea em cinco planos de foco, conferida na forma fechada",
        "imagem escalar sem polarização; a lente é perfeita além do defoco",
        "optics_lab"),
}


def _fonte(caminho: str, tamanho: int):
    try:
        return ImageFont.truetype(caminho, tamanho)
    except OSError:
        return ImageFont.load_default()


def moldura(c: Cartela) -> Image.Image:
    im = Image.new("RGB", (W, H), FUNDO)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=ACENTO)
    d.text((70, 92), "PINNeAPPle", font=_fonte(FONTE_NEGRITO, 44), fill=TINTA)
    d.text((70, 150), "PHYSICS IN ACTION", font=_fonte(FONTE_NORMAL, 26), fill=ACENTO)
    d.multiline_text((70, 268), c.gancho, font=_fonte(FONTE_NEGRITO, 60), fill=TINTA,
                     spacing=16, align="left")
    d.rectangle([0, VIDEO_Y - 3, W, VIDEO_Y + VIDEO_H + 3], fill=(20, 20, 20))

    y = VIDEO_Y + VIDEO_H + 62
    d.text((70, y), c.numero, font=_fonte(FONTE_NEGRITO, 40), fill=ACENTO_2)
    y += 86
    for linha in textwrap.wrap(c.detalhe, 56)[:2]:
        d.text((70, y), linha, font=_fonte(FONTE_NORMAL, 29), fill=APAGADO)
        y += 40
    y += 26
    d.text((70, y), "o que o vídeo não afirma", font=_fonte(FONTE_NORMAL, 24), fill=FRACO)
    y += 38
    for linha in textwrap.wrap(c.ressalva, 56)[:3]:
        d.text((70, y), linha, font=_fonte(FONTE_NORMAL, 28), fill=APAGADO)
        y += 38

    d.text((70, VIDEO_Y + VIDEO_H + 480), f"app: {c.app}", font=_fonte(FONTE_NORMAL, 28), fill=ACENTO)
    d.line([70, H - 150, W - 70, H - 150], fill=(70, 70, 70), width=2)
    d.text((70, H - 118), "PINNeAPPle Studio — todo número sai do solver",
           font=_fonte(FONTE_NORMAL, 26), fill=APAGADO)
    d.text((70, H - 74), "github.com/PINNeAPPle-Labs", font=_fonte(FONTE_NORMAL, 26), fill=ACENTO)
    return im


def vertical(ep: str) -> Path | None:
    src = MIDIA / f"{ep}.mp4"
    cartela = TEXTOS.get(ep)
    if not src.is_file() or cartela is None:
        return None
    SAIDA.mkdir(exist_ok=True)
    fundo = SAIDA / f"{ep}-fundo.png"
    moldura(cartela).save(fundo)
    destino = SAIDA / f"{ep}.mp4"
    filtro = f"[1:v]scale={W}:-2[vid];[0:v][vid]overlay=0:{VIDEO_Y}:shortest=1,format=yuv420p"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", str(fundo),
                    "-i", str(src), "-filter_complex", filtro, "-r", "30",
                    "-c:v", "libx264", "-crf", "20", "-movflags", "+faststart", str(destino)],
                   check=True)
    fundo.unlink(missing_ok=True)
    print(f"  {destino.name}: {destino.stat().st_size/1e6:.1f} MB")
    return destino


def main() -> None:
    alvo = sys.argv[1] if len(sys.argv) > 1 else ""
    feitos = sum(1 for f in sorted(MIDIA.glob("*.mp4"))
                 if (not alvo or f.stem.startswith(alvo)) and vertical(f.stem))
    print(f"{feitos} vídeos verticais em {SAIDA}")


if __name__ == "__main__":
    main()
