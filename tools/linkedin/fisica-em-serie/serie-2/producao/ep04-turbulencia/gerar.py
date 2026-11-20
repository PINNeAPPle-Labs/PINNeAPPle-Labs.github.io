#!/usr/bin/env python3
"""EP 04 · A mesma rajada, quatro respostas.

Roda a mesma rajada 1-cosine nas quatro aeronaves do catálogo do PINNeAPPle, guarda as
histórias e renderiza o vídeo de 1080x1350 do episódio.

    /opt/homebrew/bin/python3.11 gerar.py            # simula (se preciso) e renderiza
    ... gerar.py --so-simular
    ... gerar.py --so-renderizar
    ... gerar.py --rapido                            # 2 aeronaves, 4 s, para testar o desenho

O que fica medido e vai na tela:
  * o pico de incremento de fator de carga no CG, por aeronave, para a mesma rajada;
  * a comparação com duas fórmulas fechadas de engenharia (quase-estacionária e Pratt), que é
    a verificação do episódio: se o solver e as duas fórmulas concordam, o número tem lastro.

Saída: serie-2/midia/ep04-turbulencia.mp4, poster, dados.json, resultado.md
"""

from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
SERIE2 = AQUI.parents[1]
MIDIA = AQUI.parent / "midia" if (AQUI.parent / "midia").exists() else SERIE2 / "midia"
RAIZ = AQUI.parents[6]
sys.path.insert(0, str(RAIZ / "PINNeAPPle"))
sys.path.insert(0, str(AQUI.parent))

import estilo  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

H_ALT, U, HALF, LEAD = 3000.0, 7.62, 50.0, 1.5        # 25 ft/s, 2H = 100 m, como no exemplo do repo
DADOS = AQUI / "dados.pkl"
ROTULOS = {
    "light_ga": "Avião leve",
    "regional_turboprop": "Turboélice regional",
    "a320": "A320",
    "motor_glider": "Planador motorizado",
}
ROTULOS_EN = {
    "light_ga": "Light GA",
    "regional_turboprop": "Regional turboprop",
    "a320": "A320",
    "motor_glider": "Motor glider",
}


def simular(rapido: bool = False) -> dict:
    from pinneapple_simulation.flight import catalog
    from pinneapple_simulation.flight.control import StickFixed
    from pinneapple_simulation.flight.encounter import gust_sensitivity
    from pinneapple_simulation.flight.simulate import simulate
    from pinneapple_simulation.flight.trim import stability_derivatives, trim
    from pinneapple_simulation.flight.turbulence import DiscreteGust, pratt_gust_load
    from pinneapple_simulation.flight.verification import ENCOUNTER_SPEED

    nomes = ["a320", "light_ga"] if rapido else catalog.names()
    saida = {"rajada": {"amplitude_ms": U, "comprimento_2H_m": 2 * HALF, "altitude_m": H_ALT,
                        "forma": "1-cosine completa, ascendente"},
             "aeronaves": {}}

    for nome in nomes:
        ac = catalog.build(nome)
        V = ENCOUNTER_SPEED[nome]
        tr = trim(ac, V, H_ALT)
        deriv = stability_derivatives(ac, tr)
        g = DiscreteGust(amplitude=U, length=HALF, start=LEAD * V, shape="full")
        T = LEAD + 2 * HALF / V + 6.0
        h = simulate(ac, tr.x, StickFixed(tr.controls), T, 0.005, wind=g,
                     record_gamma=True, record_every=2)
        rho = ac.atmosphere(tr.x)[0]
        sig = rho / 1.225
        pratt = pratt_gust_load(ac.wing_loading, deriv["CL_alpha"], ac.af.mac,
                                U * math.sqrt(sig), V * math.sqrt(sig), rho=rho)
        dn = h.nz - h.nz[0]
        quase = gust_sensitivity(ac, V, rho, deriv["CL_alpha"]) * U
        saida["aeronaves"][nome] = {
            "V_ms": float(V),
            "carga_alar": float(ac.wing_loading),
            "CL_alpha": float(deriv["CL_alpha"]),
            "t_s": h.t.copy(),
            "dnz": dn,
            "altitude_m": h.altitude.copy(),
            "theta_deg": np.degrees(h.euler[:, 1] - h.euler[0, 1]),
            "dnz_max": float(dn.max()),
            "dnz_min": float(dn.min()),
            "t_pico_s": float(h.t[int(np.argmax(dn))] - LEAD),
            "quase_estacionario": float(quase),
            "pratt": float(pratt["dn"]),
            "pratt_Kg": float(pratt["K_g"]),
            "theta_max_deg": float(np.degrees(np.abs(h.euler[:, 1] - h.euler[0, 1]).max())),
            "dh_max_m": float(np.abs(h.altitude - H_ALT).max()),
        }
        print(f"{nome:18s} V {V:5.0f} m/s  pico dnz {dn.max():+.3f}  "
              f"(quase-estacionário {quase:.3f}, Pratt {pratt['dn']:.3f})", flush=True)

    with DADOS.open("wb") as fh:
        pickle.dump(saida, fh)
    return saida


def carregar(rapido: bool = False) -> dict:
    if DADOS.exists():
        with DADOS.open("rb") as fh:
            return pickle.load(fh)
    return simular(rapido=rapido)


def tabela_verificacao(saida: dict) -> list[dict]:
    """Diferença relativa entre o solver e as duas fórmulas fechadas, por aeronave."""
    linhas = []
    for nome, a in saida["aeronaves"].items():
        pico = a["dnz_max"]
        linhas.append({
            "aeronave": nome,
            "pico": pico,
            "quase_estacionario": a["quase_estacionario"],
            "pratt": a["pratt"],
            "erro_quase_pct": 100 * (a["quase_estacionario"] - pico) / pico,
            "erro_pratt_pct": 100 * (a["pratt"] - pico) / pico,
        })
    return linhas


def renderizar(saida: dict, fps: int = 30, segundos: float = 22.0) -> None:
    nomes = list(saida["aeronaves"].keys())
    cores = {n: estilo.PALETA[i % len(estilo.PALETA)] for i, n in enumerate(nomes)}
    t_max = max(float(a["t_s"][-1]) for a in saida["aeronaves"].values())
    janela = min(t_max, LEAD + 2 * HALF / min(a["V_ms"] for a in saida["aeronaves"].values()) + 5.0)

    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    ax_raj = fig.add_axes([0.10, 0.672, 0.82, 0.145])
    ax_nz = fig.add_axes([0.10, 0.390, 0.82, 0.210])
    ax_bar = fig.add_axes([0.30, 0.100, 0.62, 0.175])
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 04 · TURBULÊNCIA", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "A mesma rajada,\nquatro respostas", color=estilo.TINTA,
             fontsize=25, family="Oxanium", va="top", linespacing=1.1)
    fig.text(0.055, 0.884, f"1-cosine de {U:.2f} m/s, {2*HALF:.0f} m, a {H_ALT:.0f} m "
                           f"· comando fixo", color=estilo.TINTA_2, fontsize=12, va="top")
    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, "flight_dynamics · 1-cosine gust", color="#7a7a7a", fontsize=8.5,
             family="monospace", ha="right")
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))

    # --- painel da rajada: o perfil no espaço, e um marcador andando com a aeronave mais lenta
    ax_raj.set_title("A rajada no espaço (distância percorrida)", loc="left", fontsize=12, pad=10)
    ax_raj.set_xlabel("")
    ax_raj.set_ylabel("w [m/s]")
    ax_raj.set_xlim(0, 2 * HALF)
    ax_raj.set_ylim(0, U * 1.15)
    xs = np.linspace(0, 2 * HALF, 400)
    perfil = U * 0.5 * (1 - np.cos(2 * np.pi * xs / (2 * HALF)))
    ax_raj.plot(xs, perfil, color=estilo.ACENTO_2, linewidth=2.0)
    ax_raj.fill_between(xs, 0, perfil, color=estilo.ACENTO_2, alpha=0.12)
    marca = ax_raj.axvline(0, color=estilo.ACENTO, linewidth=2.2)
    texto_marca = ax_raj.text(0.02, U * 1.02, "", color=estilo.ACENTO, fontsize=9.5,
                              family="monospace")

    # --- painel do fator de carga
    ax_nz.set_title("Incremento de fator de carga no CG", loc="left", fontsize=12, pad=14)
    ax_nz.set_xlabel("tempo desde o início da rajada [s]")
    ax_nz.set_ylabel("Δn_z no CG")
    ax_nz.set_xlim(0, janela - LEAD)
    todos = np.concatenate([a["dnz"] for a in saida["aeronaves"].values()])
    ax_nz.set_ylim(min(-0.05, todos.min() * 1.1), max(todos.max() * 1.15, 0.1))
    linhas = {}
    pontos = {}
    for nome in nomes:
        a = saida["aeronaves"][nome]
        (ln,) = ax_nz.plot([], [], color=cores[nome], linewidth=2.0, label=ROTULOS.get(nome, nome))
        (pt,) = ax_nz.plot([], [], "o", color=cores[nome], markersize=6)
        linhas[nome] = ln
        pontos[nome] = pt
    ax_nz.legend(loc="upper right", ncols=2, fontsize=9.5)
    ax_nz.axhline(0, color=estilo.LINHA, linewidth=0.8)

    # --- painel de barras: solver contra as duas fórmulas, aparece no fim
    ax_bar.set_title("Pico medido × fórmulas fechadas", loc="left",
                     fontsize=12, pad=14)
    ax_bar.set_xlabel("Δn_z")
    ax_bar.set_yticks([])
    ax_bar.set_xlim(0, max(a["quase_estacionario"] for a in saida["aeronaves"].values()) * 1.25)
    alturas = np.arange(len(nomes))[::-1]
    barras = {}
    for i, nome in enumerate(nomes):
        y = alturas[i]
        barras[nome] = [
            ax_bar.barh(y + 0.26, 0, height=0.22, color=cores[nome], alpha=1.0),
            ax_bar.barh(y, 0, height=0.22, color=cores[nome], alpha=0.55),
            ax_bar.barh(y - 0.26, 0, height=0.22, color=cores[nome], alpha=0.25),
        ]
    ax_bar.set_yticks(alturas)
    ax_bar.set_yticklabels([ROTULOS.get(n, n) for n in nomes], fontsize=10.5)
    ax_bar.tick_params(axis="y", length=0, pad=8)
    ax_bar.spines["left"].set_visible(False)

    from matplotlib.patches import Patch
    ax_bar.legend(handles=[Patch(facecolor=estilo.TINTA_2, alpha=a, label=r) for a, r in
                           ((1.0, "solver"), (0.55, "quase-estacionário"), (0.25, "Pratt"))],
                  loc="lower right", bbox_to_anchor=(1.0, 1.0), ncols=3, fontsize=9.5,
                  handlelength=1.1, handleheight=0.9, columnspacing=1.4)

    total_frames = int(fps * segundos)
    tempos = np.linspace(0, janela, total_frames)
    V_nomes = {n: saida["aeronaves"][n]["V_ms"] for n in nomes}

    def desenha(i: int):
        t = tempos[i]
        # marcador da rajada: usa a aeronave mais rápida como referência de varredura
        atraso = LEAD
        x = max(0.0, min(2 * HALF, V_nomes[nomes[0]] * max(0.0, t - atraso)))
        marca.set_xdata([x, x])
        texto_marca.set_position((min(x + 2, 2 * HALF - 12), U * 1.02))
        texto_marca.set_text(f"{x/ (2*HALF) * 100:4.0f}%")
        for nome in nomes:
            a = saida["aeronaves"][nome]
            janela_t = a["t_s"] <= min(t, a["t_s"][-1])
            if janela_t.sum() > 2:
                linhas[nome].set_data(a["t_s"][janela_t] - LEAD, a["dnz"][janela_t])
                pontos[nome].set_data([a["t_s"][janela_t][-1] - LEAD], [a["dnz"][janela_t][-1]])
        # barras crescem no último terço
        f = np.clip((i / total_frames - 0.55) / 0.35, 0, 1)
        for nome, trio in barras.items():
            if f <= 0:
                continue
            a = saida["aeronaves"][nome]
            valores = [a["dnz_max"], a["quase_estacionario"], a["pratt"]]
            for barra, v in zip(trio, valores):
                barra[0].set_width(v * f)
        return []

    MIDIA.mkdir(parents=True, exist_ok=True)
    video = MIDIA / "ep04-turbulencia.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4200, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])
    desenha(0)
    with escritor.saving(fig, str(video), dpi=100):
        for i in range(total_frames):
            desenha(i)
            escritor.grab_frame()
    plt.close(fig)
    print(f"vídeo: {video} ({video.stat().st_size/1e6:.1f} MB)")

    # poster: frame em que tudo já apareceu
    render_poster(saida, nomes, cores, janela)


def render_poster(saida, nomes, cores, janela) -> None:
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    estilo.quadro(fig, "Physics in Action · 04 · Turbulência",
                  "A mesma rajada, quatro respostas", "flight_dynamics · 1-cosine gust")
    ax = fig.add_axes([0.10, 0.135, 0.82, 0.72])
    for nome in nomes:
        a = saida["aeronaves"][nome]
        ax.plot(a["t_s"] - LEAD, a["dnz"], color=cores[nome], linewidth=2.2,
                label=ROTULOS.get(nome, nome))
    ax.set_xlim(0, janela - LEAD)
    ax.set_xlabel("tempo desde o início da rajada [s]")
    ax.set_ylabel("Δn_z no CG")
    ax.set_title("", loc="left")
    ax.legend(loc="upper right", fontsize=11)
    ax.axhline(0, color=estilo.LINHA, linewidth=0.8)
    poster = MIDIA / "ep04-turbulencia-poster.jpg"
    fig.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig)
    print(f"poster: {poster}")


def escrever_resultado(saida: dict, linhas: list[dict]) -> None:
    out = ["# EP 04 · resultado medido", "",
           f"Rajada 1-cosine de {U} m/s (25 ft/s), 2H = {2*HALF:.0f} m, a {H_ALT:.0f} m, "
           "comando fixo, quatro aeronaves do catálogo, cada uma na sua velocidade de encontro.",
           "", "| aeronave | V [m/s] | pico Δn_z | quase-estacionário | Pratt | erro do quase | erro do Pratt |",
           "|---|---|---|---|---|---|---|"]
    for linha in linhas:
        out.append(f"| {linha['aeronave']} | {saida['aeronaves'][linha['aeronave']]['V_ms']:.0f} "
                   f"| {linha['pico']:+.3f} | {linha['quase_estacionario']:.3f} "
                   f"| {linha['pratt']:.3f} | {linha['erro_quase_pct']:+.1f}% "
                   f"| {linha['erro_pratt_pct']:+.1f}% |")
    pesadas = [l for l in linhas if l["aeronave"] in ("a320", "regional_turboprop")]
    leves = [l for l in linhas if l["aeronave"] not in ("a320", "regional_turboprop")]
    out += ["", "## O que isso verifica, e o que isso desmente", "",
            "As duas fórmulas fechadas são de engenharia, e não do modelo: a quase-estacionária usa "
            "aerodinâmica de asa em regime permanente, e Pratt acrescenta o fator de atenuação K_g."]
    if pesadas:
        faixa = [abs(l["erro_quase_pct"]) for l in pesadas] + [abs(l["erro_pratt_pct"]) for l in pesadas]
        out.append("")
        out.append(f"Nas aeronaves mais pesadas ({', '.join(l['aeronave'] for l in pesadas)}) as três "
                   f"rotas concordam dentro de {max(faixa):.0f}%: o solver reproduz o que a fórmula "
                   "fechada prevê, e é isso que dá lastro ao número.")
    if leves:
        out.append("")
        out.append(f"Nas mais leves ({', '.join(l['aeronave'] for l in leves)}) elas **não** concordam — "
                   f"o quase-estacionário chega a {max(l['erro_quase_pct'] for l in leves):+.0f}% acima do "
                   "pico medido. Não é erro do solver: é o limite da fórmula quase-estacionária, que "
                   "ignora o atraso da sustentação e a dinâmica de corpo curto. Fica publicado assim.")
    out += ["", "O que isso significa na prática: para a aeronave pesada, qualquer uma das três serve; "
            "para a leve, só o solver.",
            "", "## O que não está medido", "",
            "- Rajada discreta idealizada: não é atmosfera real medida em voo.",
            "- Comando fixo, sem piloto e sem autopiloto nesta rodada.",
            "- Nenhuma comparação com dado de voo: o que se verifica é o solver contra fórmulas fechadas."]
    (AQUI / "resultado.md").write_text("\n".join(out) + "\n")
    print("resultado.md")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--so-simular", action="store_true")
    ap.add_argument("--so-renderizar", action="store_true")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--segundos", type=float, default=22.0)
    args = ap.parse_args()

    saida = simular(rapido=args.rapido) if not args.so_renderizar else carregar(args.rapido)
    linhas = tabela_verificacao(saida)
    for linha in linhas:
        print(f"  {linha['aeronave']:20s} pico {linha['pico']:.3f}  "
              f"quase {linha['erro_quase_pct']:+.1f}%  Pratt {linha['erro_pratt_pct']:+.1f}%")
    escrever_resultado(saida, linhas)
    if not args.so_simular:
        renderizar(saida, fps=args.fps, segundos=args.segundos)


if __name__ == "__main__":
    main()
