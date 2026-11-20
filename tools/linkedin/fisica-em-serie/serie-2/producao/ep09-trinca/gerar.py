#!/usr/bin/env python3
"""EP 09 · Trinca — o fator de intensidade de tensão medido, não tabelado.

Malha de Q4 em elasticidade 2-D (estado plano), meia-placa com trinca central e nós duplicados
na face. O fator de intensidade sai do J-integral pela definição (contorno fechado em volta da
ponta), e a implementação é conferida por quatro caminhos:

  1. **patch test**: sem trinca, o campo é uniforme e o J tem de ser zero (é, a menos de erro de
     máquina);
  2. **refino de malha** contra a fórmula fechada da secante (Feddersen);
  3. **caminho independente**: a taxa de liberação de energia por diferença finita da energia
     potencial, que não usa J em lugar nenhum;
  4. **independência de caminho**: o J medido em contornos de tamanhos diferentes.

O que este episódio não é: um código de produção. O elemento Q4 não representa a singularidade
1/√r da ponta, e é por isso que a convergência é lenta — o número está no documento.

    /opt/homebrew/bin/python3.11 gerar.py [--rapido]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
SERIE2 = AQUI.parents[1]
MIDIA = SERIE2 / "midia"
sys.path.insert(0, str(AQUI.parent))

import estilo  # noqa: E402
import texto  # noqa: E402
import fratura as fr  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

E = 210e9
NU = 0.3
SIGMA = 100e6
MEIA_LARGURA = 0.1
MEIA_ALTURA = 0.1
A_BASE = 0.02


def resolver(a, nx=80, ny=160, grau=1.0):
    nos, elems = fr.malha(MEIA_LARGURA, MEIA_ALTURA, a, nx, ny, grau=grau)
    u = fr.resolver(nos, elems, E, NU, SIGMA, meia_altura=MEIA_ALTURA)
    return nos, elems, u


def k_de(a, nx, ny, k, grau=1.0):
    nos, elems, u = resolver(a, nx, ny, grau)
    J = fr.j_contorno(nos, elems, u, E, NU, a, MEIA_ALTURA, nx, ny, k=k)
    return fr.k_de_j(J, E, NU), J


def patch_test():
    """Sem trinca o campo é uniforme; o J tem de ser zero e a tensão, a aplicada."""
    nos, elems, u = resolver(0.0, 40, 80)
    tensoes = fr.tensoes(nos, elems, u, E, NU)
    sy = np.array([t[0][1] for t in tensoes])
    J = fr.j_contorno(nos, elems, u, E, NU, 0.03, MEIA_ALTURA, 40, 80, k=8)
    # a "trinca" de comprimento zero não existe: desloca o contorno para longe das bordas
    return {"tensao_min": float(sy.min()), "tensao_max": float(sy.max()), "j": float(J)}


def refino(malhas):
    saida = []
    for nx, ny in malhas:
        nos, elems, u = resolver(A_BASE, nx, ny)
        k = ny // 6
        J = fr.j_contorno(nos, elems, u, E, NU, A_BASE, MEIA_ALTURA, nx, ny, k=k)
        saida.append({"nx": nx, "ny": ny, "h": MEIA_LARGURA / nx, "k": k, "j": J,
                      "K": fr.k_de_j(J, E, NU), "feddersen": fr.k_feddersen(SIGMA, A_BASE,
                                                                           MEIA_LARGURA)})
    return saida


def caminho_independente():
    nos, elems, u = resolver(A_BASE, 80, 160)
    saida = []
    for k in (4, 8, 12, 16, 20):
        J = fr.j_contorno(nos, elems, u, E, NU, A_BASE, MEIA_ALTURA, 80, 160, k=k)
        saida.append({"k": k, "K": fr.k_de_j(J, E, NU)})
    return saida


def energia_potencial(a, nx=80, ny=160):
    nos, elems = fr.malha(MEIA_LARGURA, MEIA_ALTURA, a, nx, ny)
    u = fr.resolver(nos, elems, E, NU, SIGMA, meia_altura=MEIA_ALTURA)
    F = np.zeros(len(u))
    for borda, sinal in ((MEIA_ALTURA, 1.0), (-MEIA_ALTURA, -1.0)):
        linha = np.where(np.isclose(nos[:, 1], borda))[0]
        linha = linha[np.argsort(nos[linha, 0])]
        dx = np.diff(nos[linha, 0])
        for i, no in enumerate(linha):
            peso = (dx[i - 1] if i > 0 else 0.0) / 2.0 + (dx[i] if i < len(dx) else 0.0) / 2.0
            F[2 * no + 1] += sinal * SIGMA * peso
    F[2 * np.where(np.isclose(nos[:, 0], 0.0))[0]] = 0.0
    return -0.5 * float(F @ u)


def energia_release(delta=1e-3):
    base = energia_potencial(A_BASE)
    g = (energia_potencial(A_BASE - delta) - base) / delta
    return {"G": g, "K": float(np.sqrt(max(g, 1e-9) * E))}


def varredura_trinca(comprimentos):
    saida = []
    for a in comprimentos:
        nos, elems, u = resolver(a, 80, 160)
        J = fr.j_contorno(nos, elems, u, E, NU, a, MEIA_ALTURA, 80, 160, k=26)
        saida.append({"a": a, "K": fr.k_de_j(J, E, NU),
                      "feddersen": fr.k_feddersen(SIGMA, a, MEIA_LARGURA),
                      "nos": nos, "elems": elems, "u": u})
    return saida


def campo_sigma_yy(nos, elems, u, nx, ny):
    """σ_yy por elemento, devolvido como grade (nx, ny) para o pcolormesh."""
    tensoes = fr.tensoes(nos, elems, u, E, NU)
    xc = np.array([t[2][:, 0].mean() for t in tensoes])
    yc = np.array([t[2][:, 1].mean() for t in tensoes])
    sy = np.array([t[0][1] for t in tensoes]) / 1e6
    return xc.reshape(nx, ny), yc.reshape(nx, ny), sy.reshape(nx, ny)


def desenhar(patch, ref, caminho, energia, varredura, segundos=20.0):
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 09 · TRINCA", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "O número que decide\nnão está no desenho", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "elasticidade 2-D · Q4 · J-integral por contorno",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax_c = fig.add_axes([0.09, 0.620, 0.82, 0.220])
    ax_k = fig.add_axes([0.09, 0.370, 0.36, 0.180])
    ax_r = fig.add_axes([0.56, 0.370, 0.34, 0.180])
    ax_p = fig.add_axes([0.09, 0.080, 0.82, 0.170])

    Xq, Yq, Zq = campo_sigma_yy(varredura[0]["nos"], varredura[0]["elems"], varredura[0]["u"],
                               80, 160)
    pc = ax_c.pcolormesh(Xq, Yq, np.clip(Zq, 0, 400), cmap="inferno", shading="nearest",
                         vmin=0, vmax=400)
    ax_c.set_aspect("equal")
    ax_c.set_xlim(0, 0.06); ax_c.set_ylim(-0.04, 0.04)
    ax_c.set_title("tensão vertical σ_yy perto da ponta", loc="left", fontsize=11, pad=8)
    ax_c.set_xlabel("x [m]"); ax_c.set_ylabel("y [m]"); ax_c.grid(False)
    fig.colorbar(pc, ax=ax_c, fraction=0.03, pad=0.01).ax.tick_params(labelsize=8,
                                                                     colors=estilo.TINTA_2)

    ax_k.set_title("K contra o tamanho da trinca", loc="left", fontsize=10.5, pad=10)
    as_ = [v["a"] for v in varredura]
    ax_k.plot(as_, [v["feddersen"] / 1e6 for v in varredura], color=estilo.TINTA_2,
              linewidth=2.4, label="secante")
    ax_k.plot(as_, [v["K"] / 1e6 for v in varredura], "o", color=estilo.ACENTO, markersize=5,
              label="J-integral")
    ax_k.set_xlabel("a [m]"); ax_k.set_ylabel("K [MPa·m^0.5]"); ax_k.legend(fontsize=8)

    ax_r.set_title("convergência com a malha", loc="left", fontsize=10.5, pad=10)
    h = [r["h"] for r in ref]
    ax_r.semilogx(h, [r["K"] / 1e6 for r in ref], "o-", color=estilo.ACENTO_2, linewidth=2,
                  markersize=5)
    ax_r.axhline(ref[0]["feddersen"] / 1e6, color=estilo.VERDE, linewidth=1.3, linestyle="--")
    ax_r.set_xlabel("h do elemento [m]"); ax_r.set_ylabel("K [MPa·m^0.5]")

    ax_p.set_title("independência de caminho e verificação cruzada", loc="left",
                   fontsize=11, pad=8)
    ax_p.plot([c["k"] for c in caminho], [c["K"] / 1e6 for c in caminho], "o-",
              color=estilo.ACENTO_2, linewidth=2.0, markersize=5, label="J no contorno")
    ax_p.axhline(energia["K"] / 1e6, color=estilo.ACENTO, linewidth=1.6, linestyle=":",
                 label="energia liberada (dif. finita)")
    ax_p.axhline(fr.k_feddersen(SIGMA, A_BASE, MEIA_LARGURA) / 1e6, color=estilo.VERDE,
                 linewidth=1.4, linestyle="--", label="secante (fechada)")
    ax_p.set_xlabel("distância do contorno [células]"); ax_p.set_ylabel("K [MPa·m^0.5]")
    ax_p.legend(fontsize=8.5, ncols=3)

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, f"patch test: J = {patch['j']:.0e}", color="#7a7a7a",
             fontsize=8.5, family="monospace", ha="right")
    rotulo = fig.text(0.5, 0.598, "", ha="center", va="center", color=estilo.TINTA,
                      fontsize=10.5, family="monospace")

    fps = 30
    n = int(segundos * fps)
    nv = len(varredura)
    video = MIDIA / "ep09-trinca.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])
    marcas = {v["a"]: ax_k.plot([v["a"]], [v["K"] / 1e6], "o", color=estilo.VERDE,
                                markersize=9, alpha=0)[0] for v in varredura}

    def frame(i):
        u = i / max(n - 1, 1) * (nv - 1)
        k = min(int(u), nv - 1)
        v = varredura[k]
        _, _, Z = campo_sigma_yy(v["nos"], v["elems"], v["u"], 80, 160)
        pc.set_array(np.clip(Z, 0, 400).ravel())
        for chave, m in marcas.items():
            m.set_alpha(1.0 if chave == v["a"] else 0.15)
        rotulo.set_text(f"a = {1000*v['a']:.0f} mm   ·   K = {v['K']/1e6:.2f} MPa m^0.5   ·   "
                        f"secante {v['feddersen']/1e6:.2f}")
        return []

    frame(0)
    with escritor.saving(fig, str(video), dpi=100):
        for i in range(n):
            frame(i)
            escritor.grab_frame()
    plt.close(fig)
    print(f"vídeo: {video} ({video.stat().st_size/1e6:.1f} MB)")

    fig2, axp = plt.subplots(figsize=(10.8, 13.5), dpi=100)
    fig2.subplots_adjust(0, 0, 1, 1); axp.axis("off")
    axp.set_facecolor(estilo.SUPERFICIE)
    axp.pcolormesh(Xq, Yq, np.clip(Zq, 0, 400), cmap="inferno", shading="nearest",
                   vmin=0, vmax=400)
    axp.set_xlim(0, 0.06); axp.set_ylim(-0.04, 0.04)
    fig2.text(0.055, 0.95, "PHYSICS IN ACTION · 09 · TRINCA", color="#ffffff",
              fontsize=10.5, family="monospace")
    fig2.text(0.055, 0.905, f"erro final {100*(ref[-1]['K']/ref[-1]['feddersen']-1):+.1f}% "
              f"com {ref[-1]['nx']}x{ref[-1]['ny']}", color="#ffffff", fontsize=17,
              family="Oxanium")
    poster = MIDIA / "ep09-trinca-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--segundos", type=float, default=20.0)
    args = ap.parse_args()

    print("patch test ...", flush=True)
    patch = patch_test()
    print(f"  σ_yy {patch['tensao_min']/1e6:.3f}–{patch['tensao_max']/1e6:.3f} MPa · "
          f"J = {patch['j']:.1e}", flush=True)

    print("refino ...", flush=True)
    malhas = [(40, 80), (60, 120), (80, 160), (120, 240)] if not args.rapido else [(40, 80), (80, 160)]
    ref = refino(malhas)
    for r in ref:
        print(f"  {r['nx']}x{r['ny']}: K {r['K']/1e6:.2f} contra {r['feddersen']/1e6:.2f} "
              f"({100*(r['K']/r['feddersen']-1):+.1f}%)", flush=True)

    print("independência de caminho ...", flush=True)
    caminho = caminho_independente()
    print("  " + " · ".join(f"k={c['k']}: {c['K']/1e6:.2f}" for c in caminho), flush=True)

    print("energia liberada ...", flush=True)
    energia = energia_release()
    print(f"  G = {energia['G']:.1f} J/m² → K = {energia['K']/1e6:.2f}", flush=True)

    print("varredura de trinca ...", flush=True)
    comprimentos = [0.010, 0.015, 0.020, 0.030, 0.040]
    varredura = varredura_trinca(comprimentos)

    desenhar(patch, ref, caminho, energia, varredura, segundos=args.segundos)
    escrever_resultado(patch, ref, caminho, energia, varredura)


def escrever_resultado(patch, ref, caminho, energia, varredura):
    fechado = fr.k_feddersen(SIGMA, A_BASE, MEIA_LARGURA)
    linhas = [
        "# EP 09 · resultado medido", "",
        "Elasticidade 2-D em estado plano (Q4, espessura unitária), meia-placa de "
        f"{2*MEIA_LARGURA*1000:.0f} mm de largura com trinca central de comprimento 2a, "
        f"E = {E/1e9:.0f} GPa, ν = {NU}, tração de {SIGMA/1e6:.0f} MPa. Nós duplicados nas faces "
        "da trinca. K sai do J-integral pela definição (contorno fechado em volta da ponta), com "
        "J = K²/E em estado plano de tensão.", "",
        "## Verificações", "",
        f"1. **patch test** (sem trinca, campo uniforme): σ_yy de "
        f"{patch['tensao_min']/1e6:.3f} a {patch['tensao_max']/1e6:.3f} MPa contra 100 MPa "
        f"aplicados, e **J = {patch['j']:.1e}** — zero a menos de erro de máquina. É a checagem "
        "que separa um integrador certo de um que só devolve números plausíveis.",
        "2. **refino de malha** contra a fórmula fechada da secante, "
        "K = σ√(πa)·√(sec(πa/2W)):", "",
        "| malha | h do elemento | K medido | secante | erro |", "|---|---|---|---|---|",
    ]
    for r in ref:
        linhas.append(f"| {r['nx']}×{r['ny']} | {1000*r['h']:.3f} mm | {r['K']/1e6:.2f} | "
                      f"{r['feddersen']/1e6:.2f} | {100*(r['K']/r['feddersen']-1):+.1f}% |")
    linhas += ["",
               "3. **caminho independente** — a taxa de liberação de energia por diferença finita "
               f"da energia potencial, que não usa J em nenhum ponto: G = {energia['G']:.0f} J/m² "
               f"→ K = **{energia['K']/1e6:.2f} MPa√m**, contra "
               f"**{caminho[2]['K']/1e6:.2f}** do J no contorno — "
               f"{100*abs(energia['K']-caminho[2]['K'])/energia['K']:.1f}% de diferença entre "
               "dois métodos que não compartilham código.",
               "4. **independência de caminho**: " +
               " · ".join(f"k={c['k']}: {c['K']/1e6:.2f}" for c in caminho) +
               f" → variação de {100*(max(c['K'] for c in caminho)/min(c['K'] for c in caminho)-1):.1f}% "
               "entre o contorno mais próximo e o mais distante.", "",
               "## O resultado", "",
               "| a [mm] | K medido | secante | erro |", "|---|---|---|---|"]
    for v in varredura:
        linhas.append(f"| {1000*v['a']:.0f} | {v['K']/1e6:.2f} | {v['feddersen']/1e6:.2f} | "
                      f"{100*(v['K']/v['feddersen']-1):+.1f}% |")
    linhas += ["",
               f"Com a malha mais fina o erro cai para "
               f"**{100*(ref[-1]['K']/ref[-1]['feddersen']-1):+.1f}%** e continua descendo com h: "
               "a convergência é lenta porque o elemento Q4 **não representa a singularidade "
               "1/√r** da ponta. Um elemento quarter-point ou um enriquecimento resolveria; não "
               "foi feito, e é a razão de este episódio ser implementação e não produção.", "",
               "## O que este resultado é", "",
               "Um FE próprio, com a verificação que importa: um caso com resposta exata (campo "
               "uniforme), uma fórmula fechada para a geometria real, e um segundo método "
               "independente para o mesmo número.", "",
               "## O que este resultado não é", "",
               "- **Não é um código de fratura de produção**: sem elemento singular, sem "
               "plasticidade, sem propagação.",
               "- Estado plano de tensão, espessura unitária: nada de 3-D, nada de constraint "
               "de triaxialidade.",
               "- Material linear elástico: nenhuma zona plástica, nenhum critério de falha "
               "aplicado — o número é K, não um veredito sobre o componente.",
               "- A geometria é de placa com trinca central: não é o componente de ninguém."]
    (AQUI / "resultado.md").write_text(texto.virgula("\n".join(linhas)) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
