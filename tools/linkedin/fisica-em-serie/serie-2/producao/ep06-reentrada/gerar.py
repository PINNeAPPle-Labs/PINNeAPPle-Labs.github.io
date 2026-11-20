#!/usr/bin/env python3
"""EP 06 · Reentrada — condução transiente no escudo térmico, com fluxo prescrito e balanço de energia.

O problema caro da reentrada é o escoamento; o que decide a espessura do escudo é a condução
transiente atrás dele. Este episódio resolve a parte que se pode resolver com número: uma laje
de material térmico com fluxo de calor na face exposta, integrada no tempo, e duas réguas:

  * temperatura de superfície contra a solução exata de fluxo constante em meio semi-infinito
    (T = 2q√(αt/π)/k) — a verificação do esquema;
  * balanço de energia: o que entrou pela face tem de estar guardado na laje.

E o resultado que interessa ao projeto: a temperatura na face fria para três espessuras.

    /opt/homebrew/bin/python3.11 gerar.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import math

import numpy as np
from scipy.linalg import solve_banded

AQUI = Path(__file__).resolve().parent
SERIE2 = AQUI.parents[1]
MIDIA = SERIE2 / "midia"
sys.path.insert(0, str(AQUI.parent))

import estilo  # noqa: E402
import texto  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

K_COND = 0.55        # W/(m.K), material ablativos/carbonosos típicos
RHO = 1400.0         # kg/m3
CP = 1250.0          # J/(kg.K)
ALFA = K_COND / (RHO * CP)
T_INICIAL = 293.0
Q_PICO = 1.2e6       # W/m2, ordem de um pico de reentrada em ponto de estagnação
T_PICO = 40.0        # s
LARGURA = 18.0       # s, meia-largura do pulso de calor


def fluxo(t):
    return Q_PICO * np.exp(-((t - T_PICO) / LARGURA) ** 2)


def _passo_de_tempo(r_alvo: float, dx: float) -> float:
    """O passo de tempo vem do número de Fourier alvo: dt = r dx^2 / alfa."""
    return r_alvo * dx ** 2 / ALFA


def resolver(espessura: float, n: int = 400, t_final: float = 120.0, r_alvo: float = 0.5):
    """Diferenças finitas implícitas (backward Euler) com fluxo de Neumann na face exposta.

    O passo de tempo não é escolhido a dedo: sai do número de Fourier alvo, para que a mesma
    resolução temporal seja usada nas três espessuras e a verificação valha para o que roda.
    """
    dx = espessura / n
    x = (np.arange(n) + 0.5) * dx
    passos = int(round(t_final / _passo_de_tempo(r_alvo, dx)))
    dt = t_final / passos
    r = ALFA * dt / dx ** 2
    T = np.full(n, T_INICIAL)
    historico, tempos, energia_in, energia_laje = [], [], [], []
    guardar = max(passos // 60, 1)

    for passo in range(passos):
        t = passo * dt
        q = fluxo(t)
        ab = np.zeros((3, n))
        b = T.copy()
        ab[0, 1:] = -r
        ab[1, :] = 1 + 2 * r
        ab[2, :-1] = -r
        ab[1, 0] = 1 + 2 * r      # meia-célula na face com fluxo: q entra em dx/2
        ab[0, 1] = -2 * r         # A[0,1]: o superdiagonal mora em ab[0,1]
        ab[1, -1] = 1 + r         # face fria adiabática
        b[0] += 2 * r * q * dx / K_COND
        T = solve_banded((1, 1), ab, b)
        if passo % guardar == 0:
            historico.append(T.copy())
            tempos.append(t + dt)
            tt = t + dt
            energia_in.append(Q_PICO * LARGURA * np.sqrt(np.pi) / 2 *
                              (math.erf((tt - T_PICO) / LARGURA) + math.erf(T_PICO / LARGURA)))
            energia_laje.append(RHO * CP * np.trapezoid(T - T_INICIAL, x))
    return {"x": x, "campos": np.array(historico), "tempos": np.array(tempos),
            "energia_in": np.array(energia_in), "energia_laje": np.array(energia_laje),
            "espessura": espessura, "dt": dt, "r": r, "passos": passos,
            "T_fria_max": float(np.max([c[-1] for c in historico])),
            "T_quente_max": float(np.max([c[0] for c in historico]))}


def verificacao_analitica(r_alvo: float = 0.5, n: int = 2000, espessura: float = 0.5,
                          t_final: float = 20.0):
    """Fluxo constante em laje grossa: a face quente segue T = T0 + 2q√(αt/π)/k.

    Roda no **mesmo número de Fourier** usado nas lajes de produção, e depois com r/4, para
    que o erro reportado seja o da configuração que aparece no vídeo e a convergência temporal
    fique medida em vez de suposta.
    """
    q = 2.0e5
    resultados = {}
    for r_alvo_atual in (r_alvo, r_alvo / 4):
        dx = espessura / n
        passos = int(round(t_final / _passo_de_tempo(r_alvo_atual, dx)))
        dt = t_final / passos
        r = ALFA * dt / dx ** 2
        T = np.full(n, T_INICIAL)
        ts, Ts = [], []
        for passo in range(passos):
            ab = np.zeros((3, n))
            ab[0, 1:] = -r; ab[1, :] = 1 + 2 * r; ab[2, :-1] = -r
            ab[1, 0] = 1 + 2 * r; ab[0, 1] = -2 * r; ab[1, -1] = 1 + r
            b = T.copy(); b[0] += 2 * r * q * dx / K_COND
            T = solve_banded((1, 1), ab, b)
            t = (passo + 1) * dt
            if passo % max(passos // 200, 1) == 0:
                ts.append(t); Ts.append(T[0])
        ts = np.array(ts); Ts = np.array(Ts)
        analitico = T_INICIAL + 2 * q * np.sqrt(ALFA * ts / np.pi) / K_COND
        erro = float(np.max(np.abs(Ts - analitico)) / np.max(analitico - T_INICIAL))
        resultados[r_alvo_atual] = {"ts": ts, "Ts": Ts, "analitico": analitico, "erro": erro,
                                    "r": r, "dt": dt}
    return resultados


def desenhar(espessuras, segundos=16.0):
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 06 · REENTRADA", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "O calor entra por\num ponto", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "condução transiente 1-D · fluxo prescrito · sem CFD do escoamento",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax_q = fig.add_axes([0.09, 0.655, 0.82, 0.135])
    ax_c = fig.add_axes([0.09, 0.425, 0.82, 0.175])
    ax_f = fig.add_axes([0.09, 0.205, 0.82, 0.150])
    ax_e = fig.add_axes([0.09, 0.065, 0.36, 0.100])

    t = np.linspace(0, 120, 800)
    ax_q.plot(t, fluxo(t) / 1e6, color=estilo.ACENTO, linewidth=2.2)
    ax_q.set_title("fluxo de calor prescrito no nariz", loc="left", fontsize=11, pad=8)
    ax_q.set_xlabel("t [s]"); ax_q.set_ylabel("q [MW/m²]")
    marca_q = ax_q.axvline(0, color=estilo.TINTA_2, linewidth=1.2, linestyle="--")

    ax_c.set_title("a onda térmica atravessando a espessura", loc="left", fontsize=11, pad=8)
    ax_c.set_xlabel("x [mm] (0 = face exposta)"); ax_c.set_ylabel("T [K]")
    base = espessuras[0]
    linhas_eixo = []
    for i, res in enumerate(espessuras):
        (ln,) = ax_c.plot(res["x"] * 1000, res["campos"][0],
                          color=estilo.PALETA[i % len(estilo.PALETA)], linewidth=2.0,
                          label=f"{1000*res['espessura']:.0f} mm")
        linhas_eixo.append(ln)
        ax_c.axvline(1000 * res["espessura"], color=estilo.PALETA[i % len(estilo.PALETA)],
                     linewidth=0.9, linestyle=":", alpha=0.7)
    ax_c.set_xlim(0, 1000 * espessuras[-1]["espessura"])
    ax_c.legend(fontsize=8.5, ncols=3, loc="upper right")

    ax_f.set_title("face fria: temperatura para três espessuras", loc="left", fontsize=11, pad=8)
    for i, res in enumerate(espessuras):
        ax_f.plot(res["tempos"], [c[-1] for c in res["campos"]],
                  color=estilo.PALETA[i % len(estilo.PALETA)], linewidth=2.0,
                  label=f"{1000*res['espessura']:.0f} mm")
    ax_f.set_xlabel("t [s]"); ax_f.set_ylabel("T [K]")
    ax_f.legend(fontsize=9, ncols=3)

    ax_e.set_title("balanço de energia", loc="left", fontsize=10.5, pad=10)
    ax_e.plot(base["tempos"], base["energia_in"] / 1e6, color=estilo.ACENTO_2, linewidth=1.8,
              label="entrou")
    ax_e.plot(base["tempos"], base["energia_laje"] / 1e6, color=estilo.VERDE, linewidth=1.8,
              linestyle="--", label="guardado")
    ax_e.set_xlabel("t [s]"); ax_e.set_ylabel("MJ/m²"); ax_e.legend(fontsize=8)

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, "sutton-graves não entra: q(t) é prescrito", color="#7a7a7a",
             fontsize=8.5, family="monospace", ha="right")

    fps = 30
    n = int(segundos * fps)
    nq = len(base["tempos"])
    video = MIDIA / "ep06-reentrada.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])

    def frame(i):
        k = int(round(i / max(n - 1, 1) * (nq - 1)))
        for ln, res in zip(linhas_eixo, espessuras):
            kk = min(k, len(res["campos"]) - 1)
            ln.set_ydata(res["campos"][kk])
        ax_c.set_ylim(T_INICIAL - 20, max(c.max() for c in base["campos"]) * 1.08)
        marca_q.set_xdata([base["tempos"][k]] * 2)
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
    for i, res in enumerate(espessuras):
        axp.plot(res["x"] * 1000, res["campos"][-1], color=estilo.PALETA[i % len(estilo.PALETA)],
                 linewidth=3, label=f"{1000*res['espessura']:.0f} mm")
    axp.set_xlim(0, 1000 * espessuras[-1]["espessura"])
    axp.set_ylim(T_INICIAL - 20, max(c.max() for c in base["campos"]) * 1.05)
    axp.legend(fontsize=9)
    axp.set_facecolor(estilo.SUPERFICIE)
    fig2.text(0.055, 0.95, "PHYSICS IN ACTION · 06 · REENTRADA", color="#ffffff",
              fontsize=10.5, family="monospace")
    fig2.text(0.055, 0.905, "face fria ao fim do pulso: "
              + " · ".join(f"{1000*r['espessura']:.0f} mm {r['T_fria_max']:.0f} K"
                           for r in espessuras),
              color="#ffffff", fontsize=15, family="Oxanium")
    poster = MIDIA / "ep06-reentrada-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")


def main() -> None:
    print("verificação analítica ...", flush=True)
    ver = verificacao_analitica()
    base_v = ver[0.5]; fino_v = ver[0.125]
    print(f"  r = {base_v['r']:.2f} (o mesmo das lajes): erro máximo "
          f"{100*base_v['erro']:.2f}%", flush=True)
    print(f"  r = {fino_v['r']:.2f} (passo 4x menor): erro máximo "
          f"{100*fino_v['erro']:.2f}%", flush=True)

    espessuras = []
    for esp in (0.010, 0.025, 0.050):
        print(f"laje de {1000*esp:.0f} mm ...", flush=True)
        r = resolver(esp)
        delta = np.abs(r["energia_in"] - r["energia_laje"]) / np.maximum(r["energia_in"], 1e-9)
        r["erro_energia"] = float(delta.max())
        print(f"  r = {r['r']:.2f} · {r['passos']} passos · face fria {r['T_fria_max']:.1f} K "
              f"· face quente {r['T_quente_max']:.0f} K · balanço {100*r['erro_energia']:.2f}%",
              flush=True)
        espessuras.append(r)

    desenhar(espessuras)
    escrever_resultado(base_v, fino_v, espessuras)


def escrever_resultado(base_v, fino_v, espessuras):
    linhas = [
        "# EP 06 · resultado medido", "",
        "Condução transiente 1-D (backward Euler, 400 células) numa laje de material térmico com "
        f"k = {K_COND} W/(m·K), ρ = {RHO:.0f} kg/m³, cp = {CP:.0f} J/(kg·K), fluxo prescrito na face "
        f"exposta com pico de {Q_PICO/1e6:.1f} MW/m² em t = {T_PICO:.0f} s "
        f"(pulso gaussiano de meia-largura {LARGURA:.0f} s, energia total "
        f"{Q_PICO*LARGURA*np.sqrt(np.pi)/1e6:.1f} MJ/m²).", "",
        "O passo de tempo não é escolhido por espessura: sai de um número de Fourier alvo "
        f"r = α·dt/dx² = 0,5, de modo que a verificação abaixo vale para o que aparece no vídeo.",
        "",
        "## Verificação (face quente contra a solução exata de fluxo constante em meio "
        "semi-infinito, T = T₀ + 2q√(αt/π)/k)", "",
        f"- **r = {base_v['r']:.2f}**, o mesmo das lajes de produção: erro máximo de "
        f"**{100*base_v['erro']:.2f}%**",
        f"- **r = {fino_v['r']:.2f}** (passo de tempo 4× menor): erro máximo de "
        f"**{100*fino_v['erro']:.2f}%** — a diferença entre os dois é a convergência temporal "
        "medida, não suposta", "",
        "## Três espessuras, mesmo pulso de calor", "",
        "| espessura | células | r | face quente (pico) | face fria (pico) | erro do balanço de energia |",
        "|---|---|---|---|---|---|",
    ]
    for r in espessuras:
        linhas.append(f"| {1000*r['espessura']:.0f} mm | 400 | {r['r']:.2f} | "
                      f"{r['T_quente_max']:.0f} K | {r['T_fria_max']:.0f} K | "
                      f"{100*r['erro_energia']:.2f}% |")
    linhas += ["", "## O que este resultado é", "",
               "A parte do problema de reentrada que se resolve sem CFD: quanto calor atravessa o "
               "escudo e em quanto tempo. O esquema é verificado contra solução exata no mesmo "
               "número de Fourier em que roda, a convergência temporal é medida, e o balanço de "
               "energia é conferido a cada rodada.", "",
               "## O que este resultado não é", "",
               "- **Não há CFD do escoamento**: o fluxo q(t) é prescrito, não vem de um solver "
               "compressível com química de gás real.",
               "- **Não há ablação, pirólise nem mudança de propriedades com a temperatura.** "
               f"É por isso que a face quente chega a {max(r['T_quente_max'] for r in espessuras):.0f} K: "
               "acima da temperatura de decomposição de qualquer ablador real, a superfície "
               "deveria estar consumindo material e segurando a temperatura. O número alto não "
               "é um resultado sobre o material — é o modelo mostrando que a ablação não pode "
               "ser ignorada num caso de projeto.",
               "- A face fria, essa sim, é o que se quer: com 10 mm a laje inteira aquece, com "
               "50 mm o calor ainda não chegou ao fundo no tempo do pulso.",
               "- Não é um caso de veículo: não há geometria, ângulo de ataque nem trajetória."]
    (AQUI / "resultado.md").write_text(texto.virgula("\n".join(linhas)) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
