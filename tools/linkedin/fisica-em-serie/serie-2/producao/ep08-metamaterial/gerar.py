#!/usr/bin/env python3
"""EP 08 · Metamaterial — o manto que cancela um harmônico e paga a conta nos outros.

Espalhamento 2-D por um cilindro condutor com uma casca dielétrica concêntrica, resolvido pela
série exata de Bessel/Hankel (ver `mie2d.py`). O episódio não é "fizemos um manto": é medir o
que uma casca isotrópica consegue e não consegue.

  * **verificação cruzada**: a série multicamada contra a série de cilindro único que já existe
    no repositório (`em.waves.cylinder_scattering_tm`) — tem de coincidir a menos de erro de
    máquina;
  * **verificação da largura de espalhamento**: contra a integração direta do campo distante;
  * **resultado**: quanto a casca cancela no harmônico para o qual foi projetada, quanto ela
    cobra nos outros, e a largura de banda em que isso vale.

    /opt/homebrew/bin/python3.11 gerar.py [--rapido]
"""

from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
SERIE2 = AQUI.parents[1]
MIDIA = SERIE2 / "midia"
sys.path.insert(0, str(AQUI.parent))

# a série de referência mora no pacote da casa
sys.path.insert(0, str(AQUI.parents[6] / "PINNeAPPle"))

import estilo  # noqa: E402
import texto  # noqa: E402
import mie2d  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

warnings.filterwarnings("ignore")

K0 = 2.0 * np.pi            # lambda = 1
A_NUCLEO = 0.25
RAZAO = 1.8                 # raio externo / raio do núcleo
B_CASCA = RAZAO * A_NUCLEO
PERDA = -0.03               # parte imaginária da permissividade da casca (declarada)


def coeficientes(k0, raios, eps):
    m = len(raios) + 1
    return {n: abs(mie2d.harmonico(n, k0, raios, eps, [1.0] * m,
                                   pec=(eps[0] is None))[1]) for n in range(0, 5)}


def melhor_casca(k0=K0, nucleo=None, razao=RAZAO, faixa=(-3.0, 4.0), n=240):
    a = A_NUCLEO
    b = razao * a
    larguras = []
    valores = np.linspace(faixa[0], faixa[1], n)
    for er in valores:
        larguras.append(mie2d.largura_espalhamento(k0, [a, b], [nucleo, complex(er, PERDA)]))
    larguras = np.array(larguras)
    i = int(np.argmin(larguras))
    return valores, larguras, valores[i], larguras[i]


def verificar_contra_biblioteca():
    """A série multicamada com uma camada só tem de reproduzir a série da casa."""
    from pinneapple_simulation.electromagnetics.waves import cylinder_scattering_tm
    X, Y = np.meshgrid(np.linspace(-1.5, 1.5, 121), np.linspace(-1.5, 1.5, 121))
    casos, erros = [], []
    for nome, eps in (("dielétrico ε = 4", 4.0), ("dielétrico ε = 12", 12.0),
                      ("metálico ε = −20 + 2j", complex(-20, 2)), ("condutor", None)):
        ref = cylinder_scattering_tm(X, Y, K0, A_NUCLEO, eps)
        meu = mie2d.campo(X, Y, K0, [A_NUCLEO], [eps])
        erros.append(float(np.max(np.abs(meu - ref)) / np.max(np.abs(ref))))
        casos.append(nome)
    return casos, erros


def verificar_largura():
    """A largura de espalhamento contra a integração direta do campo distante."""
    from pinneapple_simulation.electromagnetics.waves import cylinder_scattering_tm
    R = 60.0
    phi = np.linspace(0.0, 2.0 * np.pi, 1440, endpoint=False)
    x, y = R * np.cos(phi), R * np.sin(phi)
    saida = []
    for eps in (None, 4.0):
        campo = cylinder_scattering_tm(x, y, K0, A_NUCLEO, eps, total=False)
        numerica = float(np.trapezoid(np.abs(campo) ** 2, phi) * R)
        serie = mie2d.largura_espalhamento(K0, [A_NUCLEO], [eps])
        saida.append({"eps": eps, "numerica": numerica, "serie": serie,
                      "erro": abs(numerica - serie) / serie})
    return saida


def banda(k0_design, eps_casca, limite_db=1.0):
    """Faixa de k0a em que a casca ainda reduz pelo menos `limite_db`."""
    kas = np.linspace(0.6 * k0_design * A_NUCLEO, 1.6 * k0_design * A_NUCLEO, 200)
    reducao = []
    for ka in kas:
        k0 = ka / A_NUCLEO
        nu = mie2d.largura_espalhamento(k0, [A_NUCLEO], [None])
        co = mie2d.largura_espalhamento(k0, [A_NUCLEO, B_CASCA], [None, eps_casca])
        reducao.append(10.0 * np.log10(nu / co))
    reducao = np.array(reducao)
    dentro = kas[reducao >= limite_db]
    if dentro.size == 0:
        return {"kas": kas, "reducao": reducao, "largura_relativa": 0.0, "faixa": (np.nan, np.nan)}
    return {"kas": kas, "reducao": reducao,
            "largura_relativa": float(dentro.max() - dentro.min()),
            "faixa": (float(dentro.min()), float(dentro.max()))}


def campo_mapa(k0, eps_casca, n=181, extensao=2.0):
    x = np.linspace(-extensao, extensao, n)
    X, Y = np.meshgrid(x, x)
    raios = [A_NUCLEO] if eps_casca is None else [A_NUCLEO, B_CASCA]
    eps = [None] if eps_casca is None else [None, eps_casca]
    return X, Y, mie2d.campo(X, Y, k0, raios, eps)


def desenhar(ver_lib, ver_larg, valores, larguras, eps_otimo, harmonico_nu, harmonico_co,
             banda_res, segundos=20.0):
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 08 · METAMATERIAL", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "Cancelar um harmônico\nnão é ficar invisível", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "série exata de Bessel/Hankel · casca isotrópica · TM",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax_m = fig.add_axes([0.30, 0.545, 0.40, 0.280])
    ax_h = fig.add_axes([0.09, 0.320, 0.36, 0.150])
    ax_b = fig.add_axes([0.56, 0.320, 0.34, 0.150])
    ax_d = fig.add_axes([0.09, 0.075, 0.82, 0.170])

    x = np.linspace(-2.0, 2.0, 181)
    X, Y = np.meshgrid(x, x)
    _, _, Z0 = campo_mapa(K0, None, n=181)
    im = ax_m.imshow(np.abs(Z0), origin="lower", extent=[-2, 2, -2, 2], cmap="RdBu_r",
                     vmin=0, vmax=np.abs(Z0).max())
    circulo = plt.Circle((0, 0), A_NUCLEO, fill=False, color="#111111", linewidth=1.2)
    ax_m.add_artist(circulo)
    casca = plt.Circle((0, 0), B_CASCA, fill=False, color="#ffffff", linewidth=1.0,
                       linestyle="--")
    ax_m.add_artist(casca)
    ax_m.set_title("|Ez| total · onda vindo da esquerda", loc="left", fontsize=11, pad=8)
    ax_m.set_xticks([]); ax_m.set_yticks([]); ax_m.grid(False); ax_m.set_aspect("equal")
    fig.colorbar(im, ax=ax_m, fraction=0.03, pad=0.01).ax.tick_params(labelsize=8,
                                                                     colors=estilo.TINTA_2)

    ns = np.arange(0, 4)
    ax_h.set_title("variação por harmônico", loc="left", fontsize=10.5, pad=10)
    db = [20 * np.log10(harmonico_co[n] / harmonico_nu[n]) for n in ns]
    cores = [estilo.VERDE if v < 0 else estilo.ACENTO for v in db]
    ax_h.bar([f"n={n}" for n in ns], db, color=cores)
    ax_h.axhline(0, color=estilo.LINHA, linewidth=0.9)
    for i, v in enumerate(db):
        ax_h.text(i, v + (0.7 if v >= 0 else -1.9), f"{v:+.1f}", ha="center", fontsize=8.5,
                  color=estilo.TINTA_2, va="bottom" if v >= 0 else "top")
    ax_h.set_ylabel("dB"); ax_h.set_ylim(min(db) - 3.0, max(db) + 3.0)

    ax_b.set_title("largura de espalhamento", loc="left", fontsize=10.5, pad=10)
    ax_b.plot(banda_res["kas"], banda_res["reducao"], color=estilo.ACENTO_2, linewidth=2.0)
    ax_b.axhline(0, color=estilo.LINHA, linewidth=0.9)
    ax_b.axvline(K0 * A_NUCLEO, color=estilo.VERDE, linewidth=1.2, linestyle="--")
    ax_b.set_xlabel("k0·a"); ax_b.set_ylabel("redução [dB]")

    ax_d.set_title("projeto da casca: largura de espalhamento contra a permissividade",
                   loc="left", fontsize=11, pad=8)
    ax_d.plot(valores, larguras, color=estilo.ACENTO_2, linewidth=2.0)
    nu = mie2d.largura_espalhamento(K0, [A_NUCLEO], [None])
    ax_d.axhline(nu, color=estilo.TINTA_2, linewidth=1.0, linestyle=":",
                 label="núcleo nu")
    ax_d.plot([eps_otimo], [larguras.min()], "o", color=estilo.ACENTO, markersize=7)
    ax_d.annotate(f"ε = {eps_otimo:.2f}", (eps_otimo, larguras.min()),
                  textcoords="offset points", xytext=(10, -14), color=estilo.ACENTO, fontsize=9)
    ax_d.set_xlabel("permissividade da casca")
    ax_d.set_ylabel("largura / comprimento de onda")
    ax_d.legend(fontsize=8.5)
    marcador = ax_d.axvline(valores[0], color=estilo.VERDE, linewidth=1.0, alpha=0.6)

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, f"série × casa: erro {ver_lib:.0e}",
             color="#7a7a7a", fontsize=8.5, family="monospace", ha="right")
    rotulo = fig.text(0.5, 0.508, "", ha="center", va="center", color=estilo.TINTA,
                      fontsize=10.5, family="monospace")

    fps = 30
    n_frames = int(segundos * fps)
    video = MIDIA / "ep08-metamaterial.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])

    # os campos são pré-calculados num conjunto menor de pontos e reaproveitados nos quadros:
    # recalcular a série a cada quadro custaria minutos por um ganho visual nulo
    passo = np.linspace(0, len(valores) - 1, 44).astype(int)
    cache = {int(k): np.abs(campo_mapa(K0, complex(valores[k], PERDA), n=181)[2])
             for k in passo}
    chaves = np.array(sorted(cache))
    indices = np.linspace(0, len(chaves) - 1, n_frames).astype(int)
    vmax = np.abs(Z0).max()

    def frame(i):
        k = int(chaves[indices[i]])
        er = valores[k]
        im.set_data(cache[k])
        marcador.set_xdata([er, er])
        rotulo.set_text(f"casca eps = {er:+.2f}   ·   largura {larguras[k]:.3f} lambda   ·   "
                        f"{10*np.log10(nu/larguras[k]):+.1f} dB")
        return []

    frame(0)
    with escritor.saving(fig, str(video), dpi=100):
        for i in range(n_frames):
            frame(i)
            escritor.grab_frame()
    plt.close(fig)
    print(f"vídeo: {video} ({video.stat().st_size/1e6:.1f} MB)")

    fig2, axp = plt.subplots(figsize=(10.8, 13.5), dpi=100)
    fig2.subplots_adjust(0, 0, 1, 1); axp.axis("off")
    axp.set_facecolor(estilo.SUPERFICIE)
    axp.imshow(np.abs(Z0), origin="lower", extent=[-2, 2, -2, 2], cmap="RdBu_r", vmin=0,
               vmax=vmax)
    fig2.text(0.055, 0.95, "PHYSICS IN ACTION · 08 · METAMATERIAL", color="#ffffff",
              fontsize=10.5, family="monospace")
    fig2.text(0.055, 0.905, f"dipolo {db[1]:+.1f} dB · total "
              f"{10*np.log10(nu/larguras.min()):+.1f} dB",
              color="#ffffff", fontsize=17, family="Oxanium")
    poster = MIDIA / "ep08-metamaterial-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--segundos", type=float, default=20.0)
    args = ap.parse_args()

    print("verificação cruzada com a série da casa ...", flush=True)
    casos, erros = verificar_contra_biblioteca()
    for c, e in zip(casos, erros):
        print(f"  {c}: {e:.1e}", flush=True)

    print("verificação da largura de espalhamento ...", flush=True)
    ver_larg = verificar_largura()
    for v in ver_larg:
        print(f"  eps={v['eps']}: numérica {v['numerica']:.5f} λ · série {v['serie']:.5f} λ "
              f"({100*v['erro']:.2f}%)", flush=True)

    print("projeto da casca ...", flush=True)
    valores, larguras, eps_otimo, melhor = melhor_casca()
    print(f"  eps ótimo {eps_otimo:+.2f} → {melhor:.4f} λ "
          f"(núcleo nu {mie2d.largura_espalhamento(K0, [A_NUCLEO], [None]):.4f} λ)", flush=True)

    harmonico_nu = coeficientes(K0, [A_NUCLEO], [None])
    harmonico_co = coeficientes(K0, [A_NUCLEO, B_CASCA], [None, complex(eps_otimo, PERDA)])
    for n in range(4):
        print(f"  n={n}: {20*np.log10(harmonico_co[n]/harmonico_nu[n]):+.1f} dB", flush=True)

    banda_res = banda(K0, complex(eps_otimo, PERDA))
    print(f"  banda acima de 1 dB: k0a {banda_res['faixa'][0]:.2f}–{banda_res['faixa'][1]:.2f}",
          flush=True)

    desenhar(max(erros), ver_larg, valores, larguras, eps_otimo,
             harmonico_nu, harmonico_co, banda_res, segundos=args.segundos)
    escrever_resultado(erros, casos, ver_larg, valores, larguras, eps_otimo, harmonico_nu,
                       harmonico_co, banda_res)


def escrever_resultado(erros, casos, ver_larg, valores, larguras, eps_otimo, harmonico_nu,
                       harmonico_co, banda_res):
    nu = mie2d.largura_espalhamento(K0, [A_NUCLEO], [None])
    melhor = float(larguras.min())
    db = {n: 20 * np.log10(harmonico_co[n] / harmonico_nu[n]) for n in range(4)}
    linhas = [
        "# EP 08 · resultado medido", "",
        "Espalhamento 2-D por um cilindro condutor de raio a com casca dielétrica concêntrica de "
        f"raio {RAZAO}·a, polarização TM, incidência normal. Solução pela série exata de "
        "Bessel/Hankel multicamada (`producao/mie2d.py`), com k0·a = "
        f"{K0*A_NUCLEO:.3f} no ponto de projeto.", "",
        "## Verificações", "",
        "1. **contra a série de cilindro único que já existe no repositório** "
        "(`em.waves.cylinder_scattering_tm`), no mesmo grid de campo:", "",
        "| caso | erro relativo máximo |", "|---|---|",
    ]
    for c, e in zip(casos, erros):
        linhas.append(f"| {c} | {e:.1e} |")
    linhas += ["",
               "2. **largura de espalhamento** contra a integração direta do campo distante a "
               "60 λ:", "",
               "| caso | integração | série | erro |", "|---|---|---|---|"]
    for v in ver_larg:
        nome = "condutor" if v["eps"] is None else f"ε = {v['eps']}"
        linhas.append(f"| {nome} | {v['numerica']:.5f} λ | {v['serie']:.5f} λ | "
                      f"{100*v['erro']:.2f}% |")
    linhas += ["", "## O resultado", "",
               f"O núcleo nu espalha **{nu:.4f} λ**. Uma casca isotrópica, otimizada em "
               f"permissividade, leva isso a **{melhor:.4f} λ** — ganho de "
               f"**{10*np.log10(nu/melhor):.1f} dB**, com ε = {eps_otimo:+.2f} e "
               f"b/a = {RAZAO}.", "",
               "O que a casca faz de fato aparece quando se olha harmônico por harmônico:", "",
               "| harmônico | núcleo nu | com casca | variação |", "|---|---|---|---|"]
    for n in range(4):
        linhas.append(f"| n = {n} | {harmonico_nu[n]:.4f} | {harmonico_co[n]:.4f} | "
                      f"{db[n]:+.1f} dB |")
    linhas += ["",
               f"A casca **cancela o dipolo** ({db[1]:+.1f} dB) — que é o termo para o qual ela "
               f"foi projetada — e **cobra a conta nos outros**: o harmônico 3 sobe "
               f"{db[3]:+.1f} dB. O total melhora só {10*np.log10(nu/melhor):.1f} dB porque a "
               "largura de espalhamento soma todos eles.", "",
               f"A banda em que a redução passa de 1 dB vai de k0·a = "
               f"{banda_res['faixa'][0]:.2f} a {banda_res['faixa'][1]:.2f} — estreita, como "
               "toda ressonância de cancelamento.", "",
               "## O que este resultado é", "",
               "Uma medida exata de até onde vai uma casca **isotrópica**: ela ajusta um harmônico "
               "por vez, e o que se ganha num se perde em outro. Um manto de transformação óptica "
               "não é isotrópico — ele precisa de μ_r ≠ μ_θ — e por isso este modelo, com camadas "
               "isotrópicas, não o representa.", "",
               "## O que este resultado não é", "",
               "- **Não é um manto de invisibilidade**: é uma casca homogênea otimizada.",
               "- Não há dispersão de material: ε é constante dentro da banda varrida, o que "
               "nenhum metamaterial real faz.",
               "- Não há estrutura subcomprimento de onda: a casca é homogeneizada por hipótese.",
               "- Não é 3-D: cilindro infinito, incidência normal, uma polarização."]
    (AQUI / "resultado.md").write_text(texto.virgula("\n".join(linhas)) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
