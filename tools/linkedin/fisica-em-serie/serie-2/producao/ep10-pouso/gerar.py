#!/usr/bin/env python3
"""EP 10 · Pouso de foguete com vento — controle em malha fechada, verificado sem vento.

Modelo de massa pontual em 2-D com empuxo vetorado, consumo de propelente, arrasto e rajada
lateral. O controlador é PD sobre posição e velocidade, com o empuxo saturado e o ângulo
limitado — o mesmo tipo de lei que voa num veículo real, sem otimização nenhuma.

A verificação do episódio não é "o vídeo ficou bonito":
  * sem vento, o veículo tem de pousar no alvo: erro de posição e velocidade de toque medidos;
  * com o controlador desligado, o mesmo caso tem de errar — senão o controlador não está
    fazendo nada e o número não significa nada;
  * varredura de vento de 0 a 20 m/s, com o erro de pouso em cada ponto.

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
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

G = 9.81
M0 = 2000.0          # kg na perna final
M_DRY = 1200.0
T_MAX = 2.2 * M0 * G # empuxo máximo (empuxo-peso 2,2)
ISP = 3000.0         # m/s de velocidade de exaustão efetiva
CD_A = 2.5           # Cd*A [m2]
RHO = 1.15
GIMBAL = np.radians(20.0)
X_ALVO, Z_ALVO = 0.0, 0.0
H0 = 800.0           # altitude inicial da perna final [m]
Z_TOQUE = 0.5        # altura do trem de pouso: abaixo disso, tocou [m]
V0 = -70.0           # velocidade vertical inicial [m/s]


def controlador(p, v, m, vento, kp=0.55, kd=1.9):
    """PD: devolve a aceleração **total** desejada (sem a gravidade, que o empuxo compensa)."""
    alvo = np.array([X_ALVO, Z_ALVO])
    return -kp * (p - alvo) - kd * v


def empuxo_de(a_total, m):
    """Converte aceleração total desejada em vetor de empuxo: só empurra para cima, dentro do gimbal."""
    forc = m * (a_total + np.array([0.0, G]))     # T = m (a - g)
    mag = float(np.linalg.norm(forc))
    if mag < 1e-9:
        return np.zeros(2), 0.0
    ang = float(np.arctan2(forc[0], forc[1]))     # ângulo fora da vertical
    ang = float(np.clip(ang, -GIMBAL, GIMBAL))
    mag = min(mag, T_MAX)
    if forc[1] < 0:                               # empuxo não puxa para baixo
        mag = 0.0
    return mag * np.array([np.sin(ang), np.cos(ang)]), mag


def simular(vento_ms: float = 0.0, com_controle: bool = True, t_max: float = 45.0, dt: float = 0.01,
            vento_rajada: bool = True):
    """Rajada lateral: seno com envelope, para o vento não ser uma constante entediante."""
    p = np.array([120.0, H0])           # começa deslocado do alvo, de propósito
    v = np.array([0.0, V0])
    m = M0
    t = 0.0
    hist = {k: [] for k in ("t", "x", "z", "vx", "vz", "T", "m", "vento")}
    pousou = False
    while t < t_max and p[1] > Z_TOQUE:
        if vento_rajada:
            envelope = min(1.0, t / 6.0)
            vento = vento_ms * envelope * (0.75 + 0.25 * np.sin(2 * np.pi * t / 9.0))
        else:
            vento = vento_ms
        if com_controle:
            empuxo, mag = empuxo_de(controlador(p, v, m, vento), m)
        else:
            empuxo, mag = np.zeros(2), 0.0       # sem controle: só gravidade e arrasto
        # arrasto relativo ao vento (o vento só age na horizontal)
        v_rel = np.array([v[0] - vento, v[1]])
        arrasto = -0.5 * RHO * CD_A * np.linalg.norm(v_rel) * v_rel
        acel = (empuxo + arrasto) / m + np.array([0.0, -G])
        v = v + acel * dt
        p = p + v * dt
        m = max(M_DRY, m - mag / ISP * dt)
        t += dt
        for chave, valor in (("t", t), ("x", p[0]), ("z", p[1]), ("vx", v[0]), ("vz", v[1]),
                             ("T", mag), ("m", m), ("vento", vento)):
            hist[chave].append(valor)
    pousou = p[1] <= Z_TOQUE
    return {k: np.asarray(v) for k, v in hist.items()} | {
        "erro_x": float(p[0] - X_ALVO) if pousou else float("nan"),
        "z_toque": float(p[1]),
        "vz_toque": float(v[1]) if pousou else float("nan"),
        "vx_toque": float(v[0]) if pousou else float("nan"),
        "pousou": pousou, "t": np.asarray(hist["t"]),
    }


def varredura(rapido: bool = False):
    ventos = [0, 4, 8, 12, 16, 20]
    if rapido:
        ventos = [0, 10, 20]
    bons, erros, toques = [], [], []
    for w in ventos:
        r = simular(w)
        bons.append(w); erros.append(r["erro_x"]); toques.append(r["vz_toque"])
        print(f"  vento {w:2d} m/s: erro x {r['erro_x']:+.2f} m · toque {r['vz_toque']:+.2f} m/s "
              f"· {'pousou' if r['pousou'] else 'NÃO pousou'}", flush=True)
    return np.array(bons), np.array(erros), np.array(toques)


def desenhar(sem_vento, sem_controle, ventos, erros, toques, segundos=20.0):
    h = sem_vento
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 10 · POUSO", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "O plano muda quando\no vento decide", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "massa pontual, empuxo vetorado, PD saturado · vento lateral com rajada",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax_v = fig.add_axes([0.09, 0.575, 0.82, 0.255])
    ax_s = fig.add_axes([0.09, 0.330, 0.36, 0.175])
    ax_w = fig.add_axes([0.56, 0.330, 0.34, 0.175])
    ax_e = fig.add_axes([0.09, 0.085, 0.82, 0.160])

    ax_v.set_xlim(-200, 320); ax_v.set_ylim(-20, H0 * 1.05)
    ax_v.set_title("vista lateral · trajetória do pouso", loc="left", fontsize=11, pad=8)
    ax_v.set_xlabel("x [m]"); ax_v.set_ylabel("z [m]"); ax_v.grid(True, alpha=0.25)
    ax_v.plot([X_ALVO, X_ALVO], [-20, 40], color=estilo.VERDE, linewidth=3, alpha=0.6)
    ax_v.text(X_ALVO + 8, 10, "alvo", color=estilo.VERDE, fontsize=9)
    (traj,) = ax_v.plot([], [], color=estilo.ACENTO_2, linewidth=1.6)
    (corpo,) = ax_v.plot([], [], "o", color=estilo.ACENTO, markersize=7)
    (traj_sc,) = ax_v.plot(sem_controle["x"], sem_controle["z"], color="#666666",
                           linewidth=1.0, linestyle="--", label="sem controle")
    ax_v.legend(loc="upper left", fontsize=9)

    ax_s.set_title("velocidade vertical", loc="left", fontsize=10.5, pad=10)
    linha_vz, = ax_s.plot([], [], color=estilo.ACENTO_2, linewidth=1.8)
    ax_s.set_xlabel("t [s]"); ax_s.set_ylabel("vz [m/s]")

    ax_w.set_title("empuxo e vento", loc="left", fontsize=10.5, pad=10)
    linha_T, = ax_w.plot([], [], color=estilo.ACENTO, linewidth=1.8, label="|T| [kN]")
    linha_w, = ax_w.plot([], [], color=estilo.VIOLETA, linewidth=1.4, label="vento [m/s]")
    ax_w.set_xlabel("t [s]"); ax_w.legend(fontsize=8)

    ax_e.set_title("erro de pouso contra intensidade do vento", loc="left", fontsize=10.5, pad=10)
    ax_e.plot(ventos, erros, "o-", color=estilo.ACENTO_2, linewidth=2)
    ax_e.axhline(0, color=estilo.LINHA, linewidth=0.8)
    ax_e.set_xlabel("vento [m/s]"); ax_e.set_ylabel("erro em x [m]")

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, "sem vento: erro e toque no documento", color="#7a7a7a",
             fontsize=8.5, family="monospace", ha="right")

    fps = 30
    n = int(segundos * fps)
    idx_max = len(h["t"])
    def frame(i):
        k = int((i / max(n - 1, 1)) ** 1.15 * (idx_max - 1)) + 1
        k = min(k, idx_max)
        traj.set_data(h["x"][:k], h["z"][:k])
        corpo.set_data([h["x"][k - 1]], [h["z"][k - 1]])
        t = h["t"][:k]
        linha_vz.set_data(t, h["vz"][:k])
        ax_s.set_xlim(0, max(h["t"][-1], 1))
        ax_s.set_ylim(min(h["vz"]) * 1.1, max(h["vz"]) * 1.1 + 1)
        linha_T.set_data(t, h["T"][:k] / 1000.0)
        linha_w.set_data(t, h["vento"][:k])
        ax_w.set_xlim(0, max(h["t"][-1], 1))
        ax_w.set_ylim(0, max(h["T"].max() / 1000.0, h["vento"].max() + 1) * 1.1)
        return []

    video = MIDIA / "ep10-pouso-foguete.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])
    frame(0)
    with escritor.saving(fig, str(video), dpi=100):
        for i in range(n):
            frame(i)
            escritor.grab_frame()
    plt.close(fig)
    print(f"vídeo: {video} ({video.stat().st_size/1e6:.1f} MB)")

    fig2, axp = plt.subplots(figsize=(10.8, 13.5), dpi=100)
    fig2.subplots_adjust(0, 0, 1, 1); axp.axis("off")
    axp.plot(h["x"], h["z"], color=estilo.ACENTO_2, linewidth=2)
    axp.set_xlim(-200, 320); axp.set_ylim(-20, H0 * 1.05); axp.set_facecolor(estilo.SUPERFICIE)
    fig2.text(0.055, 0.95, "PHYSICS IN ACTION · 10 · POUSO", color="#ffffff",
              fontsize=10.5, family="monospace")
    fig2.text(0.055, 0.90, "Vento lateral 0–20 m/s · controle PD saturado",
              color="#ffffff", fontsize=17, family="Oxanium")
    poster = MIDIA / "ep10-pouso-foguete-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--segundos", type=float, default=20.0)
    args = ap.parse_args()

    print("sem vento, com controle ...", flush=True)
    sem_vento = simular(0.0, True)
    print(f"  pousou={sem_vento['pousou']} erro x {sem_vento['erro_x']:+.3f} m "
          f"toque {sem_vento['vz_toque']:+.2f} m/s", flush=True)
    print("sem controle ...", flush=True)
    sem_controle = simular(0.0, False, t_max=25.0)
    print(f"  pousou={sem_controle['pousou']} vz final {sem_controle['vz'][-1]:+.1f} m/s",
          flush=True)
    print("varredura de vento ...", flush=True)
    ventos, erros, toques = varredura(args.rapido)

    desenhar(sem_vento, sem_controle, ventos, erros, toques, segundos=args.segundos)
    escrever_resultado(sem_vento, sem_controle, ventos, erros, toques)


def escrever_resultado(sem_vento, sem_controle, ventos, erros, toques):
    linhas = [
        "# EP 10 · resultado medido", "",
        "Massa pontual em 2-D, empuxo vetorado com gimbal de 20°, empuxo máximo de 2,2× o peso, "
        "Isp de 3.000 m/s, arrasto quadrático e vento lateral com rajada. Controlador PD "
        "saturado, sem otimização.", "",
        f"- **sem vento, com controle**: pousou em "
        f"{'sim' if sem_vento['pousou'] else 'não'}, erro lateral "
        f"**{sem_vento['erro_x']:+.3f} m**, velocidade de toque "
        f"**{sem_vento['vz_toque']:+.2f} m/s**",
        f"- **sem controle**: o mesmo caso termina a "
        f"{abs(sem_controle['vz'][-1]):.1f} m/s — o controlador é o que faz o pouso existir",
        "- **varredura de vento**:",
        "",
        "| vento [m/s] | erro lateral [m] | velocidade de toque [m/s] |",
        "|---|---|---|",
    ]
    for w, e, tq in zip(ventos, erros, toques):
        linhas.append(f"| {w} | {e:+.2f} | {tq:+.2f} |")
    linhas += ["", "## O que este resultado é", "",
               "Um laço de controle fechado com física de voo declarada, e uma verificação em "
               "dois lados: o caso sem vento tem de acertar o alvo, e o caso sem controle tem de "
               "errar. Sem os dois, o número do primeiro não significa nada.", "",
               "## O que este resultado não é", "",
               "- Não é um gêmeo do veículo: é massa pontual, sem atitude, sem inércia rotacional.",
               "- Não há voo nem ensaio: a comparação é entre o controlador e a ausência dele.",
               "- O vento é sintético, com envelope declarado; não é atmosfera medida."]
    (AQUI / "resultado.md").write_text("\n".join(linhas) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
