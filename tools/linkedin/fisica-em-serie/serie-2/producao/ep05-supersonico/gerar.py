#!/usr/bin/env python3
"""EP 05 · Foguete supersônico — o choque que decide a geometria.

Sem OpenFOAM e sem CFD 3-D: Euler quasi-1D no bocal (volumes finitos, HLLC, primeira ordem),
verificado contra três soluções analíticas que existem para este problema:

  1. distribuição de Mach no escoamento isentrópico → relação área–Mach;
  2. vazão em massa com garganta sônica → fórmula da vazão crítica;
  3. posição do choque normal parado no divergente → Rankine–Hugoniot casado com o isentrópico
     dos dois lados (e a queda de pressão de estagnação como segunda régua no mesmo ponto).

E o resultado de engenharia: o coeficiente de empuxo em função da razão de pressões, com o pico
na expansão ideal e a perda dos dois lados — superexpandido (choque dentro do bocal) e
subexpandido (energia saindo sem virar empuxo).

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
import euler_bocal as eb  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

P0 = 1.0e6           # pressão de estagnação na câmara [Pa]
T0 = 300.0           # temperatura de estagnação [K]
A_T = np.pi * 0.05 ** 2
RAZAO_ENTRADA = 3.0
RAZAO_SAIDA = 2.5
X_T = 0.35
COMPRIMENTO = 1.0

GEOM = dict(a_t=A_T, a_in=RAZAO_ENTRADA * A_T, a_exit=RAZAO_SAIDA * A_T, x_t=X_T,
            comprimento=COMPRIMENTO)


def mach_isentropico_saida():
    return eb.mach_de_area(RAZAO_SAIDA)


def pressao_saida_isentropica():
    m = mach_isentropico_saida()
    return P0 * (1.0 + 0.5 * (eb.GAMMA - 1.0) * m * m) ** (-eb.GAMMA / (eb.GAMMA - 1.0))


def rodar_caso(p_back, n=600, passos=150000):
    b = eb.Bocal(n=n, p0=P0, t0=T0, p_back=p_back, **GEOM)
    it, desvio = b.rodar(passos=passos, tol=1e-10)
    return b, it, desvio


def verificar_isentropico(n=600):
    """Saída supersônica: o campo inteiro tem de seguir a relação área–Mach."""
    p_back = 0.2 * pressao_saida_isentropica()
    b, it, _ = rodar_caso(p_back, n=n)
    # ramo divergente, longe da garganta (onde a curvatura da parede quebra a hipótese 1-D)
    sel = b.x > X_T + 0.08
    a_rel = eb.area(b.x[sel], **GEOM) / A_T
    m_ana = np.array([eb.mach_de_area(r) for r in a_rel])
    erro = float(np.max(np.abs(b.mach[sel] - m_ana) / m_ana))
    m_saida = float(b.mach[-1])
    erro_saida = abs(m_saida - mach_isentropico_saida()) / mach_isentropico_saida()
    vazao_med = b.vazao()
    vazao_ana = eb.vazao_critica(P0, T0, A_T)
    vazao_x = b.rho * b.u * b.a_c
    deriva = float(np.max(np.abs(vazao_x - vazao_med)) / vazao_med)
    return {"bocal": b, "iter": it, "erro_perfil": erro, "m_saida": m_saida,
            "erro_saida": erro_saida, "vazao": vazao_med, "vazao_ana": vazao_ana,
            "erro_vazao": abs(vazao_med - vazao_ana) / vazao_ana, "deriva_vazao": deriva,
            "m_ana": m_ana, "sel": sel, "p_back": p_back}


def varredura_choque(p_backs):
    """Choque no divergente: posição medida contra a curva analítica."""
    saida = []
    for pb in p_backs:
        alvo = eb.brentq(lambda x: eb.contrapressao_do_choque(x, p0=P0, **GEOM) - pb,
                         X_T + 0.015, COMPRIMENTO - 0.002)
        b, it, _ = rodar_caso(pb)
        xs, queda = b.posicao_choque()
        m1 = eb.mach_de_area(float(eb.area(xs, **GEOM)) / A_T)
        _, _, queda_ana = eb.choque_normal(m1)
        saida.append({"p_back": pb, "x_analitico": float(alvo), "x_medido": xs,
                      "erro": abs(xs - alvo) / alvo, "queda_medida": queda,
                      "queda_analitica": float(queda_ana), "m_saida": float(b.mach[-1]),
                      "iter": it, "bocal": b})
    return saida


def varredura_empuxo(razoes):
    """Coeficiente de empuxo contra a razão de pressões. p_a é a contrapressão do ambiente."""
    saida = []
    for razao in razoes:
        p_amb = P0 / razao
        b, it, _ = rodar_caso(p_amb)
        m_e = float(b.mach[-1])
        a_e = float(b.a_c[-1])
        empuxo = b.vazao() * b.u[-1] + (b.p[-1] - p_amb) * a_e
        saida.append({"npr": razao, "p_amb": p_amb, "cf": empuxo / (P0 * A_T),
                      "p_saida": float(b.p[-1]), "m_saida": m_e, "iter": it})
    return saida


def cf_expansao_ideal():
    """C_F com expansão perfeita: p_saída = p_ambiente, todo o momentum vira empuxo."""
    m = mach_isentropico_saida()
    t_e = T0 / (1.0 + 0.5 * (eb.GAMMA - 1.0) * m * m)
    p_e = P0 * (t_e / T0) ** (eb.GAMMA / (eb.GAMMA - 1.0))
    u_e = m * np.sqrt(eb.GAMMA * eb.RGAS * t_e)
    return eb.vazao_critica(P0, T0, A_T) * u_e / (P0 * A_T)


def desenhar(iso, choques, empuxo, segundos=22.0):
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.text(0.055, 0.978, "PHYSICS IN ACTION · 05 · SUPERSÔNICO", color=estilo.ACENTO_2,
             fontsize=10.5, family="monospace", va="top")
    fig.text(0.055, 0.952, "A contrapressão\ndecide onde o choque para", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "Euler quasi-1D · HLLC · bocal convergente-divergente · gás ideal",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax_p = fig.add_axes([0.09, 0.640, 0.82, 0.190])
    ax_m = fig.add_axes([0.09, 0.405, 0.82, 0.185])
    ax_s = fig.add_axes([0.09, 0.120, 0.36, 0.165])
    ax_c = fig.add_axes([0.56, 0.120, 0.36, 0.165])

    # contorno do bocal, desenhado como área em torno do eixo
    xg = np.linspace(0, COMPRIMENTO, 400)
    ag = eb.area(xg, **GEOM)
    escala = 0.42 / ag.max()

    ax_p.set_title("pressão ao longo do bocal", loc="left", fontsize=11, pad=8)
    ax_p.fill_between(xg, escala * ag, -escala * ag, color="#333333", zorder=0)
    ax_p.set_xlabel("x [m] (garganta em 0,35)"); ax_p.set_ylabel("p / p0")
    linhas_p = []
    for i, caso in enumerate(choques):
        b = caso["bocal"]
        (ln,) = ax_p.plot(b.x, b.p / P0, color=estilo.PALETA[i % len(estilo.PALETA)],
                          linewidth=2.0, label=f"p_a = {caso['p_back']/1e5:.1f} bar", zorder=3)
        linhas_p.append(ln)
    ax_p.legend(fontsize=8.5, ncols=2, loc="lower left")
    ax_p.set_ylim(-0.55, 1.08)

    ax_m.set_title("número de Mach · onde ele cruza 1 é a garganta", loc="left",
                   fontsize=11, pad=8)
    ax_m.axhline(1.0, color=estilo.TINTA_2, linewidth=1.0, linestyle="--")
    ax_m.set_xlabel("x [m]"); ax_m.set_ylabel("M")
    linhas_m = []
    for i, caso in enumerate(choques):
        b = caso["bocal"]
        (ln,) = ax_m.plot(b.x, b.mach, color=estilo.PALETA[i % len(estilo.PALETA)],
                          linewidth=2.0, zorder=3)
        linhas_m.append(ln)
    ax_m.set_ylim(0, mach_isentropico_saida() * 1.15)

    ax_s.set_title("posição do choque", loc="left", fontsize=10.5, pad=10)
    # só existe choque dentro do bocal entre a contrapressão da saída e a que o leva à garganta
    p_min = eb.contrapressao_do_choque(COMPRIMENTO - 0.002, p0=P0, **GEOM)
    p_max = eb.contrapressao_do_choque(X_T + 0.015, p0=P0, **GEOM)
    pbs = np.linspace(p_min * 1.02, p_max * 0.995, 60)
    xs_ana = [eb.brentq(lambda x: eb.contrapressao_do_choque(x, p0=P0, **GEOM) - pb,
                        X_T + 0.015, COMPRIMENTO - 0.002) for pb in pbs]
    ax_s.plot(np.array(pbs) / 1e5, xs_ana, color=estilo.TINTA_2, linewidth=2.0,
              label="analítico")
    ax_s.set_xlim(p_min / 1e5 * 0.97, p_max / 1e5 * 1.02)
    ax_s.plot([c["p_back"] / 1e5 for c in choques], [c["x_medido"] for c in choques], "o",
              color=estilo.ACENTO, markersize=6, label="medido")
    ax_s.set_xlabel("p_a [bar]"); ax_s.set_ylabel("x do choque [m]")
    ax_s.legend(fontsize=8)

    ax_c.set_title("coeficiente de empuxo · bocal fixo", loc="left", fontsize=10.5, pad=10)
    ax_c.plot([e["npr"] for e in empuxo], [e["cf"] for e in empuxo], "o-",
              color=estilo.ACENTO_2, linewidth=2, markersize=5)
    ax_c.axvline(P0 / pressao_saida_isentropica(), color=estilo.VERDE, linewidth=1.2,
                 linestyle="--")
    ax_c.text(P0 / pressao_saida_isentropica() * 1.06, 0.90, "projeto\n(p_saída = p_a)",
              color=estilo.VERDE, fontsize=8.5, va="top")
    ax_c.set_xscale("log")
    ax_c.set_xlabel("p0 / p_a"); ax_c.set_ylabel("C_F")

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028,
             f"choque contra analítico: erro máx {100*max(c['erro'] for c in choques):.1f}%",
             color="#7a7a7a", fontsize=8.5, family="monospace", ha="right")
    rotulo = fig.text(0.5, 0.352, "", ha="center", va="center", color=estilo.TINTA,
                      fontsize=10.5, family="monospace")

    fps = 30
    n = int(segundos * fps)
    nq = len(choques)
    video = MIDIA / "ep05-supersonico.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])

    def frame(i):
        u = i / max(n - 1, 1) * (nq - 1)
        k = min(int(u), nq - 2)
        f = u - k
        b0, b1 = choques[k]["bocal"], choques[k + 1]["bocal"]
        pressao = (1 - f) * (b0.p / P0) + f * (b1.p / P0)
        mach = (1 - f) * b0.mach + f * b1.mach
        for j, (lp, lm) in enumerate(zip(linhas_p, linhas_m)):
            peso = (1 - f) if j == k else (f if j == k + 1 else 0.0)
            lp.set_alpha(0.25 + 0.75 * peso)
            lm.set_alpha(0.25 + 0.75 * peso)
        linhas_p[k].set_ydata(pressao)
        linhas_m[k].set_ydata(mach)
        pc = (1 - f) * choques[k]["p_back"] + f * choques[k + 1]["p_back"]
        rotulo.set_text(f"contrapressão {pc/1e5:.2f} bar   ·   choque em "
                        f"{(1-f)*choques[k]['x_medido'] + f*choques[k+1]['x_medido']:.3f} m"
                        f"\n(transição interpolada entre regimes estacionários)")
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
    base = choques[-1]["bocal"]
    axp.plot(base.x, base.p / P0, color=estilo.ACENTO_2, linewidth=3)
    axp.set_xlim(0, COMPRIMENTO); axp.set_ylim(-0.05, 1.02)
    fig2.text(0.055, 0.95, "PHYSICS IN ACTION · 05 · SUPERSÔNICO", color="#ffffff",
              fontsize=10.5, family="monospace")
    fig2.text(0.055, 0.905, "C_F máx "
              f"{max(e['cf'] for e in empuxo):.3f} · choque a "
              f"{max(c['erro'] for c in choques)*100:.1f}% do analítico",
              color="#ffffff", fontsize=16, family="Oxanium")
    poster = MIDIA / "ep05-supersonico-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--segundos", type=float, default=22.0)
    args = ap.parse_args()

    print("isentrópico ...", flush=True)
    iso = verificar_isentropico(n=400 if args.rapido else 600)
    print(f"  M saída {iso['m_saida']:.3f} contra {mach_isentropico_saida():.3f} "
          f"({100*iso['erro_saida']:.2f}%)", flush=True)
    print(f"  perfil M(x): erro máximo {100*iso['erro_perfil']:.2f}%", flush=True)
    print(f"  vazão {iso['vazao']:.3f} contra {iso['vazao_ana']:.3f} kg/s "
          f"({100*iso['erro_vazao']:.2f}%) · deriva ao longo do bocal "
          f"{100*iso['deriva_vazao']:.2f}%", flush=True)

    print("choques ...", flush=True)
    pbs = [4.9e5, 6.5e5, 8.1e5, 9.2e5] if not args.rapido else [6.5e5, 8.1e5]
    choques = varredura_choque(pbs)
    for c in choques:
        print(f"  p_a {c['p_back']/1e5:.2f} bar: choque {c['x_medido']:.3f} contra "
              f"{c['x_analitico']:.3f} ({100*c['erro']:.1f}%) · queda de p0 "
              f"{c['queda_medida']:.3f} contra {c['queda_analitica']:.3f}", flush=True)

    print("empuxo ...", flush=True)
    razoes = ([8, 15.6, 30] if args.rapido
              else [3, 5, 8, 12, 15.6, 20, 30, 60, 120])
    empuxo = varredura_empuxo(razoes)
    for e in empuxo:
        print(f"  p0/p_a {e['npr']:6.1f}: C_F {e['cf']:.3f}", flush=True)

    desenhar(iso, choques, empuxo, segundos=args.segundos)
    escrever_resultado(iso, choques, empuxo)


def escrever_resultado(iso, choques, empuxo):
    melhor = max(empuxo, key=lambda e: e["cf"])
    pior = min(empuxo, key=lambda e: e["cf"])
    npr_projeto = P0 / pressao_saida_isentropica()
    medido_no_projeto = min(empuxo, key=lambda e: abs(e["npr"] - npr_projeto))
    pior = dict(pior, x_fim=0.0)
    for c in choques:
        if abs(c["p_back"] - pior["p_amb"]) <= 0.15 * pior["p_amb"]:
            pior = dict(pior, x_fim=c["x_medido"])
    if not pior["x_fim"]:
        try:
            pior["x_fim"] = float(eb.brentq(
                lambda x: eb.contrapressao_do_choque(x, p0=P0, **GEOM) - pior["p_amb"],
                X_T + 0.015, COMPRIMENTO - 0.002))
        except ValueError:
            pior["x_fim"] = 0.0
    linhas = [
        "# EP 05 · resultado medido", "",
        "Euler quasi-1D em um bocal convergente-divergente (volumes finitos, fluxo HLLC, "
        "primeira ordem), 600 células, gás ideal com γ = 1,4. Câmara com p0 = 1,0 MPa e "
        "T0 = 300 K, garganta de 50 mm de raio, razão de áreas de 2,5 na saída.", "",
        "## As três réguas analíticas", "",
        f"- **relação área–Mach** no divergente: erro máximo de **{100*iso['erro_perfil']:.2f}%** "
        f"no perfil de Mach; Mach de saída {iso['m_saida']:.3f} contra "
        f"{mach_isentropico_saida():.3f} do analítico ({100*iso['erro_saida']:.2f}%)",
        f"- **vazão crítica**: {iso['vazao']:.2f} kg/s medidos contra "
        f"{iso['vazao_ana']:.2f} kg/s analíticos (**{100*iso['erro_vazao']:.2f}%**); a vazão se "
        f"mantém ao longo do bocal com deriva de {100*iso['deriva_vazao']:.2f}%",
        "- **posição do choque** e **queda de pressão de estagnação** no mesmo ponto:", "",
        "| p_a [bar] | x do choque medido | analítico | erro | p0₂/p0₁ medido | analítico |",
        "|---|---|---|---|---|---|",
    ]
    for c in choques:
        linhas.append(f"| {c['p_back']/1e5:.2f} | {c['x_medido']:.3f} m | "
                      f"{c['x_analitico']:.3f} m | {100*c['erro']:.1f}% | "
                      f"{c['queda_medida']:.3f} | {c['queda_analitica']:.3f} |")
    linhas += ["", "## O resultado de engenharia", "",
               "O coeficiente de empuxo de um bocal **fixo** não tem pico no ponto de projeto: ele "
               "cresce com a razão de pressões e satura perto do vácuo, porque com p_a menor "
               "sobra pressão na saída que vira empuxo. O que o projeto decide é onde a curva "
               "começa a custar caro.", "",
               f"- **ponto de projeto** (p_a = p_saída isentrópica = "
               f"{pressao_saida_isentropica()/1e5:.2f} bar, p0/p_a = "
               f"{P0/pressao_saida_isentropica():.1f}): C_F = **{medido_no_projeto['cf']:.3f}** "
               f"medido contra **{cf_expansao_ideal():.3f}** da expansão ideal → "
               f"{100*abs(medido_no_projeto['cf']-cf_expansao_ideal())/cf_expansao_ideal():.2f}%",
               f"- **superexpandido** (p0/p_a = {pior['npr']:.0f}): o C_F cai para "
               f"**{pior['cf']:.3f}**, "
               f"{100*(1-pior['cf']/medido_no_projeto['cf']):.0f}% abaixo do projeto" +
               (f", com o choque parado em {pior['x_fim']:.3f} m dentro do divergente"
                if pior['x_fim'] else
                ". Nesse ponto a contrapressão está abaixo da faixa em que o choque cabe dentro "
                "do bocal — e este modelo, que não resolve o jato, deixa de dizer qualquer coisa "
                "sobre onde o escoamento se ajusta"),
               f"- **subexpandido** (p0/p_a = {melhor['npr']:.0f}): C_F = "
               f"**{melhor['cf']:.3f}**, mas o gás sai a "
               f"{melhor['p_saida']/1e5:.2f} bar sem virar velocidade — é pressão que um bocal "
               f"maior converteria, e o preço é área e massa.", "",
               "A curva é o que escolhe a geometria: a razão de áreas 2,5 fica bem dimensionada "
               "para uma faixa estreita de contrapressão, e fora dela ou sobra pressão na saída "
               "ou o choque entra no bocal.", "",
               "## O que este resultado é", "",
               "Um solver de Euler quasi-1D com três verificações analíticas independentes no "
               "mesmo escoamento: perfil isentrópico, vazão crítica e choque normal. O choque "
               "é resolvido por captura (HLLC), não imposto como descontinuidade.", "",
               "## O que este resultado não é", "",
               "- **Não é CFD 3-D**: é quasi-1D, sem camada limite, sem separação, sem "
               "curvatura de parede. Perto da garganta a hipótese 1-D é a mais frágil, e por "
               "isso a comparação do perfil começa 8 cm depois dela.",
               "- Não há química de combustão: γ e R são constantes, declarados.",
               "- Não há onda de expansão fora do bocal: o que sai do bocal não é resolvido, "
               "então o regime subexpandido aparece só como perda, não como pluma.",
               "- Primeira ordem: o choque aparece espalhado por algumas células, e a posição "
               "é lida no mínimo da pressão de estagnação."]
    (AQUI / "resultado.md").write_text(texto.virgula("\n".join(linhas)) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
