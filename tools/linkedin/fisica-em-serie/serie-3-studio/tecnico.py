#!/usr/bin/env python3
"""Produto B: o vídeo técnico de 16:9, 60 s, com as cartelas cronometradas.

O short de 9:16 serve para parar o dedo; este serve para quem quer saber como o número foi medido. São
cinco blocos: título, a gravação da app (com o número embaixo), como o número foi medido, a verificação
que aparece na tela e, por último, o que o vídeo **não** afirma — nessa ordem, porque é a ordem em que a
confiança se constrói, não a ordem em que o marketing gostaria.

    python tecnico.py            # todos os episódios
    python tecnico.py 05         # só um

Saída em ``midia-tecnica/<episódio>.mp4`` (1920x1080, 30 fps, yuv420p).
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from vertical import APAGADO, ACENTO, ACENTO_2, FONTE_NEGRITO, FONTE_NORMAL, FRACO, FUNDO, TEXTOS, TINTA

AQUI = Path(__file__).resolve().parent
MIDIA = AQUI / "midia"
SAIDA = AQUI / "midia-tecnica"

W, H = 1920, 1080
MARGEM = 130

# A linha de verificação de cada episódio sai da seção "O número que o episódio usa" da ficha
# (`episodios/<episódio>.md`): é o que a tela mostra ao lado do número, não uma promessa.
VERIFICACAO = {
    "01-eletromagnetismo": "estimate quasi-3-D contra a mesma máquina na malha 3-D: 8,604 contra 7,626 N·m",
    "02-aerodinamica-externa": "o CD vem com a distância ao caso de treino: perto de um ponto medido, e a tela diz quando não é",
    "03-aviacao": "o Cp é de uma corrida OpenFOAM guardada; 1.920 asas varridas em 96 s até o projeto certificável",
    "04-termico-trocador": "38.301 candidatos triados pelo surrogate e 24 reavaliados pela física, com +15% de pessimismo",
    "05-termico-eletronica": "balanço de energia e margem por componente: a FPGA fica a 0,9 °C do limite",
    "06-acustica": "Helmholtz conferido na fórmula fechada: 40,10 Hz contra alvo de 40,0 (0,1%)",
    "07-freio": "projeto re-verificado na fórmula, nunca no surrogate; o Monte Carlo move a temperatura em ±0,2 °C",
    "08-mecanica-solidos": "projeto re-verificado contra a fórmula da viga: 3022 g → 2169 g com vida de fadiga declarada",
    "09-astronomia": "posições topocêntricas contra JPL DE421, com refração perto do horizonte",
    "10-optica": "Abbe e Hopkins concordam a 8,7·10⁻¹⁵; viés de 20,7 nm em ArF imersão e 0,11 nm em EUV",
}

SEG_TITULO, SEG_VIDEO, SEG_METODO, SEG_CHECAGEM, SEG_LIMITE = 6, 22, 11, 11, 10


def _fonte(caminho: str, tamanho: int):
    try:
        return ImageFont.truetype(caminho, tamanho)
    except OSError:
        return ImageFont.load_default()


def _base() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (W, H), FUNDO)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 16], fill=ACENTO)
    d.text((MARGEM, 74), "PINNeAPPle", font=_fonte(FONTE_NEGRITO, 40), fill=TINTA)
    d.text((MARGEM, 126), "PHYSICS IN ACTION", font=_fonte(FONTE_NORMAL, 24), fill=ACENTO)
    return im, d


def _rodape(d: ImageDraw.ImageDraw, texto: str) -> None:
    d.line([MARGEM, H - 120, W - MARGEM, H - 120], fill=(70, 70, 70), width=2)
    d.text((MARGEM, H - 92), texto, font=_fonte(FONTE_NORMAL, 24), fill=FRACO)


def _cartao(rotulo: str, titulo: str, corpo: list[str], cor_titulo=TINTA, rodape: str = "") -> Image.Image:
    im, d = _base()
    d.text((MARGEM, 250), rotulo.upper(), font=_fonte(FONTE_NORMAL, 26), fill=ACENTO)
    d.multiline_text((MARGEM, 300), titulo, font=_fonte(FONTE_NEGRITO, 68), fill=cor_titulo, spacing=18)
    y = 300 + 100 * (titulo.count("\n") + 1) + 40
    for linha in corpo:
        d.text((MARGEM, y), linha, font=_fonte(FONTE_NORMAL, 34), fill=APAGADO)
        y += 52
    if rodape:
        _rodape(d, rodape)
    return im


def cartoes(ep: str) -> dict[str, Image.Image]:
    c = TEXTOS[ep]
    titulo = (AQUI / "episodios" / f"{ep}.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
    pe = f"{c.numero}  ·  app: {c.app}"
    numero, _, resto = titulo.partition(" · ")          # "EP S3-05" e o título do episódio
    numero = numero.replace("EP ", "")
    return {
        "titulo": _cartao("episódio " + numero, "\n".join(textwrap.wrap(resto, 34)[:2]),
                                        [f"app do Studio: {c.app}", "gravado dentro do PINNeAPPle Studio, com job de verdade"],
                          rodape=f"{c.numero}  ·  app: {c.app}"),
        "metodo": _cartao("como o número foi medido", "o número não é estimativa de tela",
                          textwrap.wrap(c.detalhe, 78)[:3], rodape=pe),
        "checagem": _cartao("verificação na tela", "o que a própria página confere",
                            textwrap.wrap(VERIFICACAO[ep], 78)[:3], rodape=pe),
        "limite": _cartao("o que este vídeo não afirma", "o limite vem junto com o número",
                          textwrap.wrap(c.ressalva, 78)[:3], cor_titulo=ACENTO_2, rodape=pe),
        "numero": _legenda_numero(c),
    }


def _legenda_numero(c) -> Image.Image:
    """Faixa inferior para o bloco de gravação: o número por cima do vídeo, sobre fundo opaco."""
    faixa = Image.new("RGB", (W, 150), FUNDO)
    d = ImageDraw.Draw(faixa)
    d.rectangle([0, 0, W, 6], fill=ACENTO)
    d.text((MARGEM, 40), c.numero, font=_fonte(FONTE_NEGRITO, 44), fill=ACENTO_2)
    d.text((MARGEM, 100), f"app: {c.app}", font=_fonte(FONTE_NORMAL, 24), fill=ACENTO)
    return faixa


def _png(im: Image.Image, destino: Path) -> Path:
    im.save(destino)
    return destino


def _imagem_para_video(png: Path, destino: Path, segundos: int) -> None:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", str(png),
                    "-t", str(segundos), "-r", "30", "-c:v", "libx264", "-crf", "22",
                    "-pix_fmt", "yuv420p", str(destino)], check=True)


def _bloco_gravacao(ep: str, legenda: Path, destino: Path) -> None:
    """A gravação 16:9 inteira acima da faixa do número — nada do que a tela mostra fica cortado."""
    altura = H - 150
    # setsar=1 nos dois lados: sem isso o auto_scale do overlay ajusta a faixa ao SAR do vídeo e o quadro
    # sai com 1081 linhas, que o x264 recusa (o PNG é quadrado, o vídeo gravado não declara SAR 1).
    filtro = (f"[0:v]scale={W}:{altura}:force_original_aspect_ratio=decrease:force_divisible_by=2,"
              f"pad={W}:{altura}:(ow-iw)/2:(oh-ih)/2:color=0x262626,"
              f"pad={W}:{H}:0:0:color=0x262626,setsar=1[bg];"
              f"[1:v]setsar=1[faixa];[bg][faixa]overlay=0:{altura}")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-stream_loop", "-1", "-i", str(MIDIA / f"{ep}.mp4"),
                    "-loop", "1", "-i", str(legenda), "-filter_complex", filtro,
                    "-t", str(SEG_VIDEO), "-r", "30", "-c:v", "libx264", "-crf", "22",
                    "-pix_fmt", "yuv420p", str(destino)], check=True)


def tecnico(ep: str) -> Path | None:
    if not (MIDIA / f"{ep}.mp4").is_file() or ep not in TEXTOS:
        return None
    SAIDA.mkdir(exist_ok=True)
    tmp = SAIDA / f"_{ep}"
    tmp.mkdir(exist_ok=True)
    c = cartoes(ep)
    partes = []
    for nome, segundos in (("titulo", SEG_TITULO), ("metodo", SEG_METODO),
                           ("checagem", SEG_CHECAGEM), ("limite", SEG_LIMITE)):
        p = tmp / f"{nome}.mp4"
        _imagem_para_video(_png(c[nome], tmp / f"{nome}.png"), p, segundos)
        partes.append(p)
        if nome == "titulo":                       # a gravação entra logo depois do título
            pv = tmp / "video.mp4"
            _bloco_gravacao(ep, _png(c["numero"], tmp / "numero.png"), pv)
            partes.append(pv)
    lista = tmp / "lista.txt"
    lista.write_text("".join(f"file '{p}'\n" for p in partes), encoding="utf-8")
    destino = SAIDA / f"{ep}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", "-movflags", "+faststart", str(destino)], check=True)
    for p in tmp.glob("*"):
        p.unlink()
    tmp.rmdir()
    print(f"  {destino.name}: {destino.stat().st_size/1e6:.1f} MB")
    return destino


def main() -> None:
    alvo = sys.argv[1] if len(sys.argv) > 1 else ""
    feitos = sum(1 for f in sorted(MIDIA.glob("*.mp4"))
                 if (not alvo or f.stem.startswith(alvo)) and tecnico(f.stem))
    print(f"{feitos} vídeos técnicos em {SAIDA}")


if __name__ == "__main__":
    main()
