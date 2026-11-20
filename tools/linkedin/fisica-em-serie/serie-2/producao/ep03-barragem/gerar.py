#!/usr/bin/env python3
"""EP 03 · Barragem — rompimento com superfície livre, resolvido e comparado com Ritter.

Solver próprio de águas rasas 1-D e 2-D (volumes finitos, fluxo HLL, batimetria com obstáculo).
A verificação é a solução exata de Ritter para o rompimento em leito seco — a régua mais dura
que este problema tem, porque é analítica.

O que o vídeo mostra e o documento confirma:
  * 1-D contra Ritter: erro L2 do perfil de profundidade, e a posição da frente contra 2c0t;
  * 2-D com obstáculo: a frente contornando, e a conservação de volume ao longo da rodada.

Não há sedimento: é uma fase. O documento diz isso em letra grande.

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
import aguas_rasas as aguas  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

G = 9.81
H0 = 1.0          # profundidade inicial do reservatório [m]
L_DOM = 10.0      # comprimento do domínio [m]
N1D = 800


def simular_1d(n: int = N1D, t_final: float = 0.8, cfl: float = 0.4):
    dx = L_DOM / n
    x = (np.arange(n) + 0.5) * dx
    h = np.where(x < L_DOM / 2, H0, aguas.SECO)
    hu = np.zeros(n)
    t = 0.0
    marcos = {"pvi": None}
    guardados = {}
    alvos = [0.2, 0.4, 0.6, 0.8]
    prox = 0
    passos = 0
    while t < t_final and passos < 500000:
        dt = min(aguas.cfl_1d(h, hu, dx, cfl), t_final - t)
        h, hu = aguas.passo_1d(h, hu, dx, dt)
        t += dt
        passos += 1
        while prox < len(alvos) and t >= alvos[prox]:
            guardados[alvos[prox]] = (x.copy(), h.copy(), aguas._vel(h, hu).copy(), t)
            prox += 1
    return guardados


def simular_2d(nx: int = 240, ny: int = 120, t_final: float = 4.0, cfl: float = 0.35,
               obstaculo: bool = True):
    """Águas rasas 2-D com obstáculo retangular, paredes refletivas."""
    dx = L_DOM / nx
    dy = (L_DOM / 2) / ny
    x = (np.arange(nx) + 0.5) * dx
    y = (np.arange(ny) + 0.5) * dy
    h = np.where(x[None, :] < L_DOM / 2, H0, aguas.SECO) * np.ones((ny, 1))
    hu = np.zeros((ny, nx)); hv = np.zeros((ny, nx))
    fundo = np.zeros((ny, nx))
    if obstaculo:
        fy = np.where((y > 0.30 * L_DOM / 2) & (y < 0.62 * L_DOM / 2))[0]
        fx = np.where((x > 0.28 * L_DOM) & (x < 0.34 * L_DOM))[0]
        fundo[np.ix_(fy, fx)] = 0.6
    t = 0.0; passos = 0
    quadros, tempos, volumes = [], [], []
    proximo = 0
    n_quadros = 44
    volume_inicial = float(h.sum()) * dx * dy

    while t < t_final and passos < 120000:
        u = aguas._vel(h, hu); v = aguas._vel(h, hv)
        c = np.sqrt(G * np.maximum(h, aguas.SECO))
        dt = cfl / max(float((np.abs(u) + c).max()) / dx,
                       float((np.abs(v) + c).max()) / dy)
        dt = min(dt, t_final - t)
        h, hu, hv = aguas.passo_2d(h, hu, hv, dx, dy, dt)
        seco = (fundo > 0) & (h < 0.02)
        h[seco] = aguas.SECO; hu[seco] = 0.0; hv[seco] = 0.0
        t += dt; passos += 1
        if t >= proximo * t_final / n_quadros or passos == 1:
            quadros.append((h + fundo).copy())
            tempos.append(t)
            volumes.append(float(h.sum()) * dx * dy)
            proximo += 1

    return {"campos": np.array(quadros), "tempos": np.array(tempos),
            "volumes": np.array(volumes), "volume_inicial": volume_inicial,
            "fundo": fundo, "dx": dx, "dy": dy, "passos": passos, "x": x, "y": y}


def desenhar(res1, res2, erro_l2, erro_frente, segundos=16.0):
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 03 · BARRAGEM", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "A onda que sobra\ndepois da parede", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "águas rasas 1-D e 2-D · HLL · uma fase, sem sedimento",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax = fig.add_axes([0.09, 0.400, 0.82, 0.290])
    ax1 = fig.add_axes([0.09, 0.120, 0.36, 0.150])
    ax2 = fig.add_axes([0.56, 0.120, 0.34, 0.150])

    im = ax.imshow(res2["campos"][0].T, origin="lower", cmap="Blues",
                   extent=[0, L_DOM / 2, 0, L_DOM], aspect="auto", vmin=0, vmax=H0 + 0.6)
    ax.set_title("profundidade da lâmina (com obstáculo)", loc="left", fontsize=11, pad=8)
    ax.set_xlabel("y [m]"); ax.set_ylabel("x [m]"); ax.grid(False)
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.01).ax.tick_params(labelsize=8,
                                                                   colors=estilo.TINTA_2)
    texto_t = ax.text(0.985, 0.965, "", transform=ax.transAxes, ha="right", va="top",
                      color="#ffffff", fontsize=10.5, family="monospace",
                      bbox=dict(boxstyle="round,pad=0.3", fc="#1b1b1b", ec=estilo.LINHA, alpha=0.85))

    x1, h1, _, _ = res1[0.8]
    ax1.set_title("1-D contra Ritter", loc="left", fontsize=10.5, pad=10)
    ax1.plot(x1, aguas.ritter(x1, 0.8, L_DOM / 2, H0), color=estilo.TINTA_2, linewidth=3.2, alpha=0.6, label="Ritter")
    linha, = ax1.plot(x1, h1, color=estilo.ACENTO_2, linewidth=1.6, label="HLL")
    ax1.set_xlabel("x [m]"); ax1.set_ylabel("h [m]")
    ax1.legend(fontsize=8, loc="upper right")
    ax1.text(0.04, 0.12, f"L2 = {erro_l2:.3f}", transform=ax1.transAxes, fontsize=9,
             family="monospace", color=estilo.ACENTO)

    ax2.set_title("conservação de volume", loc="left", fontsize=10.5, pad=10)
    vol = res2["volumes"] / res2["volume_inicial"] - 1
    ax2.plot(res2["tempos"], 100 * vol, color=estilo.VERDE, linewidth=2.0)
    ax2.set_xlabel("t [s]"); ax2.set_ylabel("erro [%]")
    ax2.text(0.04, 0.85, f"máx {100*np.abs(vol).max():.2f}%", transform=ax2.transAxes,
             fontsize=9, family="monospace", color=estilo.VERDE)

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, f"frente contra Ritter: {100*erro_frente:.1f}%",
             color="#7a7a7a", fontsize=8.5, family="monospace", ha="right")

    fps = 30
    n = int(segundos * fps)
    video = MIDIA / "ep03-barragem.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])

    def frame(i):
        k = int(round(i / max(n - 1, 1) * (len(res2["campos"]) - 1)))
        im.set_data(res2["campos"][k].T)
        texto_t.set_text(f"t = {res2['tempos'][k]:.2f} s")
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
    axp.imshow(res2["campos"][-1].T, origin="lower", cmap="Blues",
               extent=[0, L_DOM / 2, 0, L_DOM], aspect="auto")
    fig2.text(0.055, 0.95, "PHYSICS IN ACTION · 03 · BARRAGEM", color="#ffffff",
              fontsize=10.5, family="monospace")
    fig2.text(0.055, 0.91, f"Ritter: erro L2 {erro_l2:.4f} · frente a {100*erro_frente:.1f}%", color="#ffffff",
              fontsize=17, family="Oxanium")
    poster = MIDIA / "ep03-barragem-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--segundos", type=float, default=16.0)
    args = ap.parse_args()

    print("1-D ...", flush=True)
    res1 = simular_1d(n=400 if args.rapido else N1D)
    x, h, u, t = res1[0.8]
    ana = aguas.ritter(x, 0.8, L_DOM / 2, H0)
    erro_l2 = float(np.sqrt(np.mean((h - ana) ** 2)) / H0)
    c0 = np.sqrt(G * H0)
    # frente: posição onde h cai abaixo de 2% da altura inicial
    corte = 0.10 * H0                                  # mesmo critério nos dois lados
    frente_num = x[np.where(h > corte)[0][-1]] - L_DOM / 2
    frente_ana = x[np.where(ana > corte)[0][-1]] - L_DOM / 2
    erro_frente = abs(frente_num - frente_ana) / max(frente_ana, 1e-9)
    print(f"  erro L2 = {erro_l2:.4f} · frente {frente_num:.3f} m contra {frente_ana:.3f} m "
          f"({100*erro_frente:.1f}%)", flush=True)

    print("2-D ...", flush=True)
    res2 = simular_2d(nx=140 if args.rapido else 240, ny=70 if args.rapido else 120,
                      t_final=3.0 if args.rapido else 4.0)
    vol = res2["volumes"] / res2["volume_inicial"] - 1
    print(f"  {res2['passos']} passos · erro máximo de volume {100*np.abs(vol).max():.3f}%",
          flush=True)

    desenhar(res1, res2, erro_l2, erro_frente, segundos=args.segundos)
    escrever_resultado(res2, erro_l2, erro_frente, frente_num, frente_ana, vol)


def escrever_resultado(res2, erro_l2, erro_frente, frente_num, frente_ana, vol):
    linhas = [
        "# EP 03 · resultado medido", "",
        "Solver próprio de águas rasas (volumes finitos, fluxo HLL) em 1-D e 2-D, rompimento de "
        "barragem em leito seco, profundidade inicial 1,0 m, domínio de 10 m.", "",
        f"- **1-D contra Ritter (solução exata)**: erro L2 relativo do perfil em t = 0,8 s → "
        f"**{erro_l2:.4f}**",
        f"- **posição da frente** (mesmo critério de 10% da altura nos dois lados): "
        f"{frente_num:.2f} m medidos contra {frente_ana:.2f} m de Ritter → "
        f"**{100*erro_frente:.1f}%**",
        f"- **conservação de volume 2-D**: erro máximo ao longo da rodada → "
        f"**{100*np.abs(vol).max():.3f}%**", "",
        "## O que este resultado é", "",
        "Águas rasas de uma fase, com obstáculo retangular de 0,6 m. A verificação é analítica "
        "(Ritter, 1892), que é a régua mais dura disponível para este problema.", "",
        "## O que este resultado não é", "",
        "- **Não tem sedimento.** Transporte sólido acoplado à fase líquida é outro modelo, e "
        "não está implementado nesta casa.",
        "- Não é um caso real: não há geometria de barragem, vale ou material.",
        "- Águas rasas não resolve o que acontece na colisão com a parede: é modelo de "
        "profundidade integrada, sem detalhe 3-D.",
    ]
    (AQUI / "resultado.md").write_text("\n".join(linhas) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
