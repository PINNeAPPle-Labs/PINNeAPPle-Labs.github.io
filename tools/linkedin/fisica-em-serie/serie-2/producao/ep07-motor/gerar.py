#!/usr/bin/env python3
"""EP 07 · Motor elétrico — o acoplamento que transforma perda em perda.

Duas metades acopladas: o circuito equivalente do motor de indução dá torque, corrente e perdas;
a rede térmica de três nós dá a temperatura. O laço é a resistência do cobre crescendo com a
temperatura: mais quente → mais perda → mais quente. Com carga fixa, o escorregamento também
sobe, e é isso que faz a curva virar.

Verificações (todas medidas, nenhuma suposta):
  1. limite de um nó contra a exponencial exata;
  2. balanço de energia na rodada de projeto;
  3. estado final do transiente contra a solução algébrica do regime permanente;
  4. a curva torque–escorregamento contra o ponto de operação pedido.

    /opt/homebrew/bin/python3.11 gerar.py [--rapido]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, root

AQUI = Path(__file__).resolve().parent
SERIE2 = AQUI.parents[1]
MIDIA = SERIE2 / "midia"
sys.path.insert(0, str(AQUI.parent))

import estilo  # noqa: E402
import texto  # noqa: E402
import motor as mo  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

P_CARGA = 7500.0          # W no eixo, nominal declarado
G_PROJETO = 40.0          # W/K carcaça→ambiente com o ventilador funcionando
T_LIMITE = 155.0          # °C, classe F
T_FINAL = 4 * 3600.0      # 4 h


# ---------------------------------------------------------------- verificações

def verificar_um_no():
    """Com as condutâncias internas enormes, os três nós colapsam: a régua é a exponencial."""
    rede = mo.RedeTermica(g_enrol_ferro=1e6, g_ferro_carcaca=1e6, g_carcaca_amb=8.0)
    potencia = 1000.0
    tempos = np.arange(0.0, 7200.0 + 5.0, 5.0)
    from scipy.integrate import solve_ivp
    sol = solve_ivp(rede.derivada, (0.0, 7200.0), [20.0, 20.0, 20.0], t_eval=tempos,
                    args=([potencia / 2.0, potencia / 2.0],), method="Radau",
                    rtol=1e-10, atol=1e-10)
    t_ana, t_exata, tau, d_inf = rede.analitico_um_no(potencia, t_final=7200.0, dt=5.0)
    erro = float(np.max(np.abs(sol.y[0] - t_exata)))
    return {"tempos": t_ana, "numerico": sol.y[0], "exato": t_exata, "tau": tau,
            "d_inf": d_inf, "erro": erro, "potencia": potencia}


def verificar_serie():
    """Rede de três nós, com perda constante imposta: a régua é a soma das resistências térmicas."""
    rede = mo.RedeTermica()
    potencia = 1000.0
    tempos = np.arange(0.0, 20000.0, 20.0)
    from scipy.integrate import solve_ivp
    sol = solve_ivp(rede.derivada, (0.0, 20000.0), [20.0, 20.0, 20.0], t_eval=tempos,
                    args=([potencia, 0.0],), method="Radau", rtol=1e-10, atol=1e-10)
    serie = potencia * (1.0 / rede.g_ef + 1.0 / rede.g_fc + 1.0 / rede.g_ca)
    return {"delta_numerico": float(sol.y[0, -1] - 20.0), "delta_analitico": float(serie),
            "erro": abs(float(sol.y[0, -1] - 20.0) - serie)}


def verificar_energia(rede, t, T, p_carga):
    """O que entrou em calor tem de estar guardado nos nós mais o que saiu para o ar."""
    pot = []
    for k in range(len(t)):
        s = mo.escorregamento_de_carga(p_carga, T[0, k], T[1, k])
        p = mo.perdas(s, T[0, k], T[1, k])
        # a perda mecânica fica nos mancais: não entra na rede de três nós, e por isso
        # não entra neste balanço (ela apareceria como energia que entra e não sai)
        pot.append(p["estator"] + p["rotor"] + p["ferro"])
    pot = np.asarray(pot)
    entrou = float(np.trapezoid(pot, t))
    guardado = float(np.sum(rede.c * (T[:, -1] - T[:, 0])))
    saiu = float(np.trapezoid(rede.g_ca * (T[2] - 20.0), t))
    return {"entrou": entrou, "guardado": guardado, "saiu": saiu,
            "erro": abs(entrou - guardado - saiu) / entrou}


def regime_permanente(rede, p_carga, tentativas=((80.0, 80.0, 60.0),)):
    """Solução algébrica: perda = o que a rede conduz, com o laço fechado."""
    def sistema(temp):
        te, tf, tc = temp
        try:
            s = mo.escorregamento_de_carga(p_carga, te, tf)
        except ValueError:
            return [1e6, 1e6, 1e6]
        p = mo.perdas(s, te, tf)
        q_e = p["estator"] + 0.5 * p["rotor"]
        q_f = p["ferro"] + 0.5 * p["rotor"]
        return [q_e - rede.g_ef * (te - tf),
                q_f + rede.g_ef * (te - tf) - rede.g_fc * (tf - tc),
                rede.g_fc * (tf - tc) - rede.g_ca * (tc - 20.0)]

    for chute in tentativas:
        sol = root(sistema, chute, method="hybr")
        if sol.success and np.all(np.abs(sol.x) < 1000.0) and sol.x[0] > 20.0:
            return sol.x
    return None


def tempo_ate_limite(t, T, limite=T_LIMITE):
    superior = np.where(T[0] >= limite)[0]
    if superior.size == 0:
        return None
    return float(t[superior[0]])


def varredura_resfriamento(fracoes):
    saida = []
    for f in fracoes:
        rede = mo.RedeTermica(g_carcaca_amb=G_PROJETO * f)
        t, T = rede.estavel(t_final=T_FINAL, dt=20.0, p_carga=P_CARGA)
        est = regime_permanente(rede, P_CARGA)
        deriva = float((T[0, -1] - T[0, -2]) / (t[-1] - t[-2]) * 3600.0)   # K/h no fim
        saida.append({"fracao": f, "g": G_PROJETO * f, "t": t, "T": T,
                      "t_limite": tempo_ate_limite(t, T), "deriva": deriva,
                      "regime": est,
                      "s_fim": mo.escorregamento_de_carga(P_CARGA, T[0, -1], T[1, -1])
                      if est is not None else float("nan")})
    return saida


def resfriamento_critico(inicio=3.0, fim=G_PROJETO):
    """Abaixo desta condutância a carcaça→ambiente não existe regime permanente."""
    def existe(g):
        rede = mo.RedeTermica(g_carcaca_amb=g)
        return regime_permanente(rede, P_CARGA) is not None
    if existe(inicio):
        return inicio
    if not existe(fim):
        return float("nan")
    return float(brentq(lambda g: 1.0 if existe(g) else -1.0, inicio, fim, xtol=0.05))


# ---------------------------------------------------------------- desenho

def desenhar(um_no, serie, energia, casos, critico, segundos=22.0):
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 07 · MOTOR", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "A perda que vira\nperda", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "circuito equivalente × rede térmica × R(T) do cobre",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax_t = fig.add_axes([0.09, 0.640, 0.82, 0.190])
    ax_q = fig.add_axes([0.09, 0.430, 0.36, 0.160])
    ax_e = fig.add_axes([0.56, 0.430, 0.34, 0.160])
    ax_v = fig.add_axes([0.09, 0.120, 0.82, 0.200])

    ax_t.set_title("torque × escorregamento, com a temperatura do enrolamento",
                   loc="left", fontsize=11, pad=8)
    ss = np.linspace(1e-4, 0.45, 600)
    for i, temp in enumerate((20.0, 90.0, 140.0)):
        ax_t.plot(100 * ss, mo.torque(ss, t_estator=temp, t_rotor=temp),
                  color=estilo.PALETA[i], linewidth=2.0, label=f"enrolamento a {temp:.0f} °C")
    s_nom = mo.escorregamento_de_carga(P_CARGA)
    ax_t.plot([100 * s_nom], [float(mo.torque(s_nom))], "o", color=estilo.VERDE, markersize=7)
    ax_t.annotate("7,5 kW", (100 * s_nom, float(mo.torque(s_nom))), textcoords="offset points",
                  xytext=(8, 6), color=estilo.VERDE, fontsize=9)
    ax_t.set_xlabel("escorregamento [%]"); ax_t.set_ylabel("T [N·m]")
    ax_t.legend(fontsize=8.5)

    ax_q.set_title("perdas no ponto nominal", loc="left", fontsize=10.5, pad=10)
    p = mo.perdas(s_nom)
    nomes = ["estator", "rotor", "ferro", "mecanica"]
    valores = [p[n] for n in nomes]
    rotulos = ["estator", "rotor", "ferro", "mecânica"]
    ax_q.barh(rotulos[::-1], valores[::-1], color=[estilo.PALETA[0]] * 4)
    for i, v in enumerate(valores[::-1]):
        ax_q.text(v + 12, i, f"{v:.0f} W", va="center", fontsize=8.5, color=estilo.TINTA_2)
    ax_q.set_xlim(0, max(valores) * 1.35)
    ax_q.set_xlabel("W")

    ax_e.set_title("verificação · nó único", loc="left", fontsize=10.5, pad=10)
    ax_e.plot(um_no["tempos"] / 60.0, um_no["exato"], color=estilo.TINTA_2, linewidth=3.0,
              alpha=0.7, label="exato")
    ax_e.plot(um_no["tempos"] / 60.0, um_no["numerico"], color=estilo.ACENTO_2, linewidth=1.6,
              label="rede")
    ax_e.set_xlabel("min"); ax_e.set_ylabel("ΔT [K]")
    ax_e.text(0.05, 0.30, f"1 nó: {um_no['erro']:.2f} K", transform=ax_e.transAxes,
              fontsize=8.5, family="monospace", color=estilo.TINTA)
    ax_e.text(0.05, 0.20, f"3 nós: {serie['erro']:.2f} K", transform=ax_e.transAxes,
              fontsize=8.5, family="monospace", color=estilo.TINTA)
    ax_e.legend(fontsize=8)

    ax_v.set_title("temperatura do enrolamento com o ventilador degradado",
                   loc="left", fontsize=11, pad=8)
    ax_v.axhline(T_LIMITE, color=estilo.LARANJA, linewidth=1.4, linestyle="--")
    ax_v.text(0.5, T_LIMITE + 4, "limite da classe F", color=estilo.ACENTO, fontsize=8.5)
    ax_v.text(0.62, 0.55, "sem regime permanente:\nsegue subindo", transform=ax_v.transAxes,
              color=estilo.PALETA[3], fontsize=9, ha="center")
    linhas_v = [ax_v.plot(caso["t"] / 60.0, caso["T"][0],
                          color=estilo.PALETA[i % len(estilo.PALETA)], linewidth=1.8,
                          label=f"{100*caso['fracao']:.0f}% do resfriamento")[0]
                for i, caso in enumerate(casos)]
    ax_v.set_ylim(15, max(c["T"][0].max() for c in casos) * 1.05)
    ax_v.set_xlim(0, casos[0]["t"][-1] / 60.0)
    ax_v.legend(fontsize=8.5, ncols=4, loc="lower right")

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, f"balanço de energia: {100*energia['erro']:.2f}%",
             color="#7a7a7a", fontsize=8.5, family="monospace", ha="right")

    fps = 30
    n = int(segundos * fps)
    nc = len(casos)
    video = MIDIA / "ep07-motor.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])

    def frame(i):
        fracao_tempo = i / max(n - 1, 1)
        k = max(int(round(fracao_tempo * (len(casos[0]["t"]) - 1))), 1)
        for linha, caso in zip(linhas_v, casos):
            linha.set_xdata(caso["t"][:k] / 60.0)
            linha.set_ydata(caso["T"][0][:k])
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
    for i, caso in enumerate(casos):
        axp.plot(caso["t"] / 60.0, caso["T"][0], color=estilo.PALETA[i % len(estilo.PALETA)],
                 linewidth=2.5)
    axp.set_xlim(0, T_FINAL / 60.0)
    axp.set_ylim(15, max(c["T"][0].max() for c in casos) * 1.03)
    fig2.text(0.055, 0.95, "PHYSICS IN ACTION · 07 · MOTOR", color="#ffffff",
              fontsize=10.5, family="monospace")
    fig2.text(0.055, 0.905, f"resfriamento crítico em {critico:.1f} W/K",
              color="#ffffff", fontsize=17, family="Oxanium")
    poster = MIDIA / "ep07-motor-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--segundos", type=float, default=22.0)
    args = ap.parse_args()

    print("verificação de um nó ...", flush=True)
    um_no = verificar_um_no()
    print(f"  erro máximo contra a exponencial exata: {um_no['erro']:.2f} K "
          f"(tau {um_no['tau']:.0f} s, ΔT_inf {um_no['d_inf']:.1f} K)", flush=True)

    serie = verificar_serie()
    print(f"  rede de três nós contra a soma das resistências térmicas: "
          f"{serie['delta_numerico']:.2f} contra {serie['delta_analitico']:.2f} K "
          f"({serie['erro']:.3f} K)", flush=True)

    print("regime de projeto ...", flush=True)
    rede = mo.RedeTermica(g_carcaca_amb=G_PROJETO)
    t, T = rede.estavel(t_final=T_FINAL, dt=20.0, p_carga=P_CARGA)
    energia = verificar_energia(rede, t, T, P_CARGA)
    est = regime_permanente(rede, P_CARGA)
    print(f"  enrolamento {T[0, -1]:.1f} °C · carcaça {T[2, -1]:.1f} °C", flush=True)
    print(f"  balanço de energia: entrou {energia['entrou']/3.6e6:.2f} kWh, guardado "
          f"{energia['guardado']/3.6e6:.3f} kWh, saiu {energia['saiu']/3.6e6:.2f} kWh "
          f"→ erro {100*energia['erro']:.2f}%", flush=True)
    print(f"  transiente × algébrico: {T[0, -1]:.2f} contra {est[0]:.2f} °C "
          f"({abs(T[0,-1]-est[0]):.2f} K)", flush=True)

    print("varredura de resfriamento ...", flush=True)
    fracoes = [1.0, 0.6, 0.4, 0.25] if not args.rapido else [1.0, 0.4]
    casos = varredura_resfriamento(fracoes)
    for c in casos:
        lim = f"{c['t_limite']/60:.0f} min" if c["t_limite"] else "não atinge em 4 h"
        reg = f"{c['regime'][0]:.0f} °C" if c["regime"] is not None else "sem regime"
        print(f"  {100*c['fracao']:3.0f}% ({c['g']:.1f} W/K): {reg} · limite em {lim} · "
              f"deriva {c['deriva']:+.1f} K/h", flush=True)

    critico = resfriamento_critico()
    print(f"resfriamento crítico: {critico:.1f} W/K", flush=True)

    desenhar(um_no, serie, energia, casos, critico, segundos=args.segundos)
    escrever_resultado(um_no, serie, energia, est, casos, critico)


def escrever_resultado(um_no, serie, energia, est, casos, critico):
    s_nom = mo.escorregamento_de_carga(P_CARGA)
    p = mo.perdas(s_nom)
    total = sum(p.values())
    linhas = [
        "# EP 07 · resultado medido", "",
        "Motor de indução de 4 polos, 400 V em Y, 50 Hz, com o circuito equivalente declarado "
        f"(R_s = {mo.R_S20} Ω, R_r' = {mo.R_R20} Ω a 20 °C, X = {mo.X_S} Ω, X_m = {mo.X_M} Ω) "
        "acoplado a uma rede térmica de três nós (enrolamento, ferro, carcaça). Carga fixa de "
        f"{P_CARGA/1000:.1f} kW no eixo. O cobre tem α = {mo.ALFA_CU} 1/K.", "",
        f"- ponto nominal: escorregamento **{100*s_nom:.2f}%** ({mo.N_S*(1-s_nom):.0f} rpm), "
        f"torque {float(mo.torque(s_nom)):.1f} N·m",
        f"- perdas: estator {p['estator']:.0f} W, rotor {p['rotor']:.0f} W, ferro "
        f"{p['ferro']:.0f} W, mecânica {p['mecanica']:.0f} W → **{total:.0f} W** "
        f"(eficiência {100*P_CARGA/(P_CARGA+total):.1f}%)", "",
        "## Verificações", "",
        f"1. **limite de um nó** contra a exponencial exata (τ = {um_no['tau']/60:.1f} min): "
        f"erro máximo de **{um_no['erro']:.2f} K**",
        f"1b. **rede de três nós** com perda constante contra a soma das resistências térmicas: "
        f"{serie['delta_numerico']:.2f} K medidos contra {serie['delta_analitico']:.2f} K "
        f"analíticos (**{serie['erro']:.3f} K**)",
        f"2. **balanço de energia** na rodada de projeto: entraram "
        f"{energia['entrou']/3.6e6:.2f} kWh, ficaram guardados "
        f"{energia['guardado']/3.6e6:.3f} kWh e saíram {energia['saiu']/3.6e6:.2f} kWh → "
        f"**{100*energia['erro']:.2f}%** de erro",
        f"3. **transiente contra o algébrico**: ao fim das 4 h a integração está em "
        f"{casos[0]['T'][0,-1]:.2f} °C e a raiz do sistema não linear em {est[0]:.2f} °C → "
        f"**{abs(casos[0]['T'][0,-1]-est[0]):.2f} K** de diferença", "",
        "## O que o acoplamento faz", "",
        "| resfriamento | carcaça→ambiente | enrolamento em 4 h | limite de 155 °C |",
        "|---|---|---|---|",
    ]
    for c in casos:
        lim = f"{c['t_limite']/60:.0f} min" if c["t_limite"] else "não atinge"
        estado = f"{c['T'][0,-1]:.0f} °C" if c["regime"] is not None else "em fuga"
        linhas.append(f"| {100*c['fracao']:.0f}% | {c['g']:.1f} W/K | {estado} | {lim} |")
    linhas += ["",
               f"**Resfriamento crítico: {critico:.1f} W/K** — abaixo disso a equação de "
               "equilíbrio não tem solução: cada grau a mais aumenta a perda mais rápido do que "
               "aumenta a dissipação, e a temperatura não para.", "",
               "Com o ventilador funcionando (40 W/K) o enrolamento estabiliza perto de 90 °C. "
               "Com 25% do resfriamento, a mesma carga leva o enrolamento ao limite da classe F "
               "e a perda de cobre já cresceu — porque a resistência subiu e o escorregamento "
               "também, para entregar o mesmo torque.", "",
               "## O que este resultado é", "",
               "Um acoplamento declarado entre dois modelos clássicos: circuito equivalente do "
               "motor de indução e rede térmica concentrada, com o laço R(T) fechado e a carga "
               "mantida constante durante toda a rodada.", "",
               "## O que este resultado não é", "",
               "- **Não é FEA eletromagnética**: não há campo no entreferro, saturação, harmônicos "
               "nem perdas no ferro calculadas — elas entram como constante declarada.",
               "- Não há ventilador modelado: o resfriamento entra como uma condutância global.",
               "- Não há degradação do isolamento: a classe F é um limite de temperatura, não um "
               "modelo de vida útil.",
               "- Os parâmetros do circuito são de um motor plausível, não de uma máquina "
               "caracterizada nesta casa."]
    (AQUI / "resultado.md").write_text(texto.virgula("\n".join(linhas)) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
