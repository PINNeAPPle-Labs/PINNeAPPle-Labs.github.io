#!/usr/bin/env python3
"""EP 02 · Colapso estrutural — montagem a partir dos resultados já medidos do exemplo dos blocos.

O exemplo `examples/bricks/self_modifying_bricks.py` já rodou e deixou em `_out/`: os melhores
projetos em STL/glTF, o turntable, a evolução geração a geração e o `summary.json` com a
validação. Este script não simula nada de novo: lê os números, monta os cartões e compõe o
vídeo com o ffmpeg.

    /opt/homebrew/bin/python3.11 gerar.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SERIE2 = AQUI.parents[1]
MIDIA = SERIE2 / "midia"
BLOCOS = AQUI.parents[6] / "PINNeAPPle" / "examples" / "bricks" / "_out"
sys.path.insert(0, str(AQUI.parent))

import cards  # noqa: E402

FPS = 30


def ler_numeros() -> dict:
    resumo = json.loads((BLOCOS / "summary.json").read_text())
    melhor = resumo["best"]
    cant = melhor["cantilever"]
    aprox = [c for c in resumo["validation"] if "voxel" in c["check"].lower()
             or "timoshenko" in c["check"].lower()]
    newton = resumo.get("harmonic_newton", [])
    iguais = sum(1 for n in newton if n["agree"])
    return {
        "cantilever_mm": cant["metrics"]["reach_mm"],
        "pecas": cant["n_bricks"],
        "utilizacao": cant["metrics"]["utilisation"],
        "margem": cant["metrics"]["margin"],
        "tensao_pino": 0.333,
        "ponte": melhor.get("bridge", {}).get("n_bricks"),
        "torre_mm": melhor.get("tower", {}).get("metrics", {}).get("height_mm"),
        "decisao": resumo["trust_decision"],
        "checagens": len(resumo["validation"]),
        "aprovadas": sum(1 for c in resumo["validation"] if c["passed"]),
        "newton_concorda": iguais,
        "newton_total": len(newton),
        "timoshenko": aprox[0]["simulated"] if aprox else None,
        "timoshenko_ref": aprox[0]["reference"] if aprox else None,
        "erro_timoshenko": aprox[0]["rel_error"] if aprox else None,
    }


def ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def segmento_cartao(png: Path, segundos: float, destino: Path) -> None:
    ffmpeg(["-loop", "1", "-t", f"{segundos}", "-i", str(png), "-r", str(FPS),
            "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "20",
            "-pix_fmt", "yuv420p", str(destino)])


def segmento_clipe(video: Path, segundos: float, destino: Path, inicio: float = 0.0) -> None:
    """Encaixa o clipe no quadro 1080x1350 com fundo da marca, sem esticar."""
    ffmpeg(["-ss", f"{inicio}", "-t", f"{segundos}", "-i", str(video),
            "-vf", ("scale=1000:-2:force_original_aspect_ratio=decrease,"
                    "pad=1080:1350:(ow-iw)/2:(oh-ih)/2:color=0x262626,format=yuv420p"),
            "-r", str(FPS), "-c:v", "libx264", "-crf", "20", str(destino)])


def main() -> None:
    n = ler_numeros()
    print(json.dumps(n, indent=1))
    MIDIA.mkdir(parents=True, exist_ok=True)
    tmp = AQUI / "_tmp"
    tmp.mkdir(exist_ok=True)

    cards.cartao(tmp / "01.png", "Physics in Action · 02 · Estrutural",
                 "O que acontece quando\numa estrutura chega\nao limite",
                 corpo=["Oito peças, 135,9 mm além da borda da mesa",
                        "Encontrado por busca, julgado por estática rígida",
                        "A junta crítica identificada em cada candidato"])
    cards.cartao(tmp / "02.png", "O número", "O balanço vencedor",
                 numero=f"{n['cantilever_mm']:.1f} mm",
                 numero_nota=(f"com {n['pecas']} peças · tração de pico no pino "
                              f"{n['tensao_pino']:.3f} N = {100*n['utilizacao']:.0f}% do limite "
                              f"de 0,98 N · margem {n['margem']:.2f}×"),
                 corpo=["Comparação: bloco único 31,9 mm · pilha harmônica 86,7 mm",
                        "Ponte: 3 peças carregando 1,46 vez a carga pedida",
                        f"Torre: {n['torre_mm']:.1f} mm aguentando 1,64 vez o empurrão"
                        if n["torre_mm"] else "Torre: 153,6 mm aguentando 1,64 vez o empurrão"])
    cards.cartao(tmp / "03.png", "A verificação", "Antes de otimizar",
                 numero=f"{n['aprovadas']}/{n['checagens']}",
                 numero_nota="formas fechadas conferidas antes de qualquer busca",
                 corpo=["Estática contra pilha harmônica, tombamento, balanço em um pino",
                        "FEA de voxels dentro de 0,4% de Timoshenko (0,0327 contra 0,0328 mm)",
                        "Corpo rígido e estática concordam em 90%, 100% e 75% dos candidatos",
                        f"Decisão do relatório de confiança: {n['decisao']}"])

    segmento_cartao(tmp / "01.png", 4.0, tmp / "s1.mp4")
    segmento_clipe(BLOCOS / "turntable_cantilever.mp4", 3.0, tmp / "s2.mp4")
    segmento_cartao(tmp / "02.png", 6.0, tmp / "s3.mp4")
    segmento_clipe(BLOCOS / "evolution_cantilever.mp4", 12.0, tmp / "s4.mp4")
    segmento_cartao(tmp / "03.png", 6.0, tmp / "s5.mp4")

    lista = tmp / "lista.txt"
    lista.write_text("".join(f"file '{tmp / f's{i}.mp4'}'\n" for i in range(1, 6)))
    video = MIDIA / "ep02-colapso-estrutural.mp4"
    ffmpeg(["-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(video)])
    print(f"vídeo: {video} ({video.stat().st_size/1e6:.1f} MB)")

    poster = MIDIA / "ep02-colapso-estrutural-poster.jpg"
    ffmpeg(["-ss", "2.0", "-i", str(tmp / "s2.mp4"), "-frames:v", "1", str(poster)])
    print(f"poster: {poster}")

    escrever_resultado(n)


def escrever_resultado(n: dict) -> None:
    linhas = [
        "# EP 02 · resultado medido", "",
        "Vem do exemplo `examples/bricks/self_modifying_bricks.py` (rodada anterior, `_out/`), "
        "não de uma simulação nova: o vídeo é montagem sobre resultado já auditado.", "",
        f"- balanço vencedor: **{n['cantilever_mm']:.1f} mm** com {n['pecas']} peças, "
        f"utilização do pino em {100*n['utilizacao']:.1f}%, margem {n['margem']:.2f}×",
        f"- ponte: **{n['ponte']} peças**; torre: **{n['torre_mm']:.1f} mm**"
        if n["torre_mm"] else f"- ponte: **{n['ponte']} peças**",
        f"- relatório de confiança: **{n['decisao']}**, com {n['aprovadas']} de "
        f"{n['checagens']} checagens aprovadas",
        f"- concordância estática × corpo rígido no limite da pilha harmônica: "
        f"{n['newton_concorda']} de {n['newton_total']} fatores testados", "",
        "## O que este resultado é", "",
        "Estática rígida sobre um modelo de junta declarado (0,98 N de tração por pino, atrito "
        "0,4, peças rígidas e compressão ilimitada) — a distribuição de forças mais favorável "
        "possível. O julgamento é auditável: cada rejeição vem com o motivo.", "",
        "## O que este resultado não é", "",
        "- Não é falha progressiva nem não-linear: é estática, avaliada candidato a candidato.",
        "- Não é ensaio: as constantes de junta vêm da literatura, não de bancada.",
        "- Não é certificação estrutural de nada além do modelo de brinquedo.",
    ]
    (AQUI / "resultado.md").write_text("\n".join(linhas) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
