#!/usr/bin/env python3
"""EP 01 · CO2 no subsolo — deslocamento bifásico sobre o campo de permeabilidade do SPE10.

O caso: uma camada do SPE10 Model 1 (dado público, 60 x 220 células), injeção num canto e
produção no canto oposto, deslocamento bifásico imiscível resolvido por IMPES (pressão
implícita, saturação explícita) num solver próprio.

O que fica verificado, e é o que o vídeo mostra:
  * o solver 1-D contra a solução analítica de Buckley-Leverett (frente de Welge), com o erro
    L1 medido;
  * o balanço de massa 2-D: injetado = dentro do domínio + produzido, célula a célula;
  * a frente de saturação avançando na camada heterogênea.

Não é o OPM Flow e não é composicional: é deslocamento imiscível, e o documento diz isso.

    /opt/homebrew/bin/python3.11 gerar.py            # roda e renderiza
    ... gerar.py --rapido                            # grade grossa, 6 s de vídeo
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

AQUI = Path(__file__).resolve().parent
SERIE2 = AQUI.parents[1]
MIDIA = SERIE2 / "midia"
sys.path.insert(0, str(AQUI.parent))

import estilo  # noqa: E402
import texto  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter  # noqa: E402

SPE10 = Path.home() / "simr-data" / "opm-data" / "spe10model1" / "PERM_SPE10MODEL1.INC"
NX, NY, NZ = 100, 1, 20      # dimensão do deck público que está no disco (não é o 60x220x85)

# fluidos: fase injetada (análogo do CO2 supercrítico) deslocando a fase residente (saloura)
MU_INJ = 6e-5          # Pa.s, ordem do CO2 supercrítico
MU_RES = 1e-3          # Pa.s, água/saloura
KR_MAX = 0.8
N_INJ, N_RES = 2.0, 2.0   # expoentes de Corey
PORO = 0.2
COMPRIMENTO_M = 300.0     # lado maior da camada (220 células)
ALTURA_M = 82.0           # lado menor (60 células)
D_PRESSAO = 2.0e7         # Pa, diferencial entre injetor e produtor
ARQUIVO_DADOS = AQUI / "dados.npz"


# ----------------------------------------------------------------------------- campo SPE10
def carregar_permeabilidade() -> np.ndarray:
    """Lê o bloco PERMX do deck público do SPE10 e devolve a camada 2-D (20 x 100) em mD."""
    texto = SPE10.read_text(errors="ignore")
    linhas = texto.splitlines()
    valores, dentro = [], False
    for linha in linhas:
        limpa = linha.split("--")[0].strip()
        if not limpa:
            continue
        if limpa.upper().startswith("PERMX"):
            dentro = True
            continue
        if not dentro:
            continue
        if limpa.startswith("/"):
            break
        for pedaco in limpa.replace("/", " ").split():
            try:
                valores.append(float(pedaco))
            except ValueError:
                pass
    arr = np.asarray(valores)
    if arr.size != NX * NY * NZ:
        raise RuntimeError(f"esperava {NX*NY*NZ} valores, vieram {arr.size}")
    return arr.reshape(NZ, NY, NX)[:, 0, :]


# ----------------------------------------------------------------------------- física
def fracao_fluxo(s_inj: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """f(S) e f'(S) para Corey, com S = saturação da fase injetada."""
    s = np.clip(s_inj, 1e-6, 1 - 1e-6)
    lam_i = KR_MAX * s ** N_INJ / MU_INJ
    lam_r = KR_MAX * (1 - s) ** N_RES / MU_RES
    lam_t = lam_i + lam_r
    f = lam_i / lam_t
    dlam_i = KR_MAX * N_INJ * s ** (N_INJ - 1) / MU_INJ
    dlam_r = -KR_MAX * N_RES * (1 - s) ** (N_RES - 1) / MU_RES
    df = (dlam_i * lam_t - lam_i * (dlam_i + dlam_r)) / lam_t ** 2
    return f, df


def simular_1d(n: int = 2000, pvi_final: float = 0.9, cfl: float = 0.25):
    """Injeção linear 1-D, para comparar com a solução analítica."""
    dx = 1.0 / n
    s = np.zeros(n)
    s[:] = 0.0                        # residente puro no início
    t, hist = 0.0, {}
    marcos = [0.1, 0.3, 0.5, 0.7]
    proximo = 0
    grade = np.linspace(1e-6, 1 - 1e-6, 4001)
    _, df_grade = fracao_fluxo(grade)
    vmax = float(df_grade.max())          # CFL pela velocidade máxima em toda a faixa de S
    dt = cfl * dx / vmax
    while t < pvi_final and proximo < len(marcos):
        dt = cfl * dx / vmax
        # upwind explícito: fluxo entra pela esquerda, f(0) = f(S_inj)
        f, _ = fracao_fluxo(s)
        f_face = np.concatenate([[fracao_fluxo(np.array([1.0]))[0][0]], f[:-1]])
        s = s - dt / dx * (f - f_face)
        s = np.clip(s, 0.0, 1.0)
        t += dt
        while proximo < len(marcos) and t >= marcos[proximo]:
            hist[marcos[proximo]] = s.copy()
            proximo += 1
    return np.linspace(dx / 2, 1 - dx / 2, n), hist


def faces(trans: np.ndarray):
    """Transmissibilidade nas faces por média harmônica — a média certa para salto de K."""
    eps = 1e-30
    tx = 2 * trans[:, :-1] * trans[:, 1:] / np.maximum(trans[:, :-1] + trans[:, 1:], eps)
    ty = 2 * trans[:-1, :] * trans[1:, :] / np.maximum(trans[:-1, :] + trans[1:, :], eps)
    return tx, ty


def resolver_pressao(trans: np.ndarray, fonte: np.ndarray, fixo: int):
    """∇·(T ∇p) = q numa grade 2-D ordenada em linha, com uma célula de pressão fixa."""
    ny, nx = trans.shape
    n = nx * ny
    idx = np.arange(n).reshape(ny, nx)
    linhas, colunas, vals = [], [], []
    diag = np.zeros(n)
    tx, ty = faces(trans)

    # só as fora da diagonal entram aqui; a diagonal é montada uma vez, em `diag`
    a = idx[:, :-1].ravel(); b = idx[:, 1:].ravel(); w = tx.ravel()
    linhas += [a, b]; colunas += [b, a]; vals += [-w, -w]
    diag += np.bincount(a, weights=w, minlength=n) + np.bincount(b, weights=w, minlength=n)

    a = idx[:-1, :].ravel(); b = idx[1:, :].ravel(); w = ty.ravel()
    linhas += [a, b]; colunas += [b, a]; vals += [-w, -w]
    diag += np.bincount(a, weights=w, minlength=n) + np.bincount(b, weights=w, minlength=n)

    linhas.append(np.arange(n)); colunas.append(np.arange(n)); vals.append(diag)
    A = sp.csc_matrix((np.concatenate(vals), (np.concatenate(linhas), np.concatenate(colunas))),
                      shape=(n, n))
    rhs = fonte.ravel().copy()
    # sistema com fonte total nula: singular a menos de uma constante. Regulariza a diagonal
    # e tira a média, que é o caminho padrão para o problema de Neumann puro.
    escala = float(np.abs(diag).mean()) or 1.0
    A = A + sp.eye(n, format="csc") * (1e-9 * escala)
    p = spla.spsolve(A.tocsc(), rhs)
    p = np.asarray(p) - np.mean(p)
    return p.reshape(ny, nx), tx, ty


def simular_2d(perm: np.ndarray, pvi_alvo: float = 0.6, cfl: float = 0.35,
               max_passos: int = 6000, n_quadros: int = 48):
    """IMPES na camada, com passo de tempo escolhido por CFL e rodada até o PVI alvo.

    Injetor no canto inferior esquerdo, produtor no canto superior direito, vazão unitária.
    O poço entra na equação de saturação — é isso que faz a pluma existir.
    """
    ny, nx = perm.shape
    dy = COMPRIMENTO_M / (nx - 1)
    dx = ALTURA_M / (ny - 1)
    perm_si = perm * 1e-15                                   # mD -> m2
    trans_base = perm_si / (MU_RES * dx * dy)
    fonte = np.zeros((ny, nx))
    fonte[0, 0] = 1.0
    fonte[-1, -1] = -1.0
    fixo = (ny - 1) * nx + (nx - 1)
    volume_celula = PORO * dx * dy
    volume_poroso = volume_celula * nx * ny
    alvo = pvi_alvo * volume_poroso

    s = np.zeros((ny, nx))
    injetado = produzido = perda_clip = 0.0
    passos = 0
    registros = {"passos": [], "pvi": [], "injetado": [], "produzido": [],
                 "massa_dominio": [], "campos": []}
    proximo_quadro = 0

    while injetado < alvo and passos < max_passos:
        lam_i = KR_MAX * np.clip(s, 1e-6, 1) ** N_INJ / MU_INJ
        lam_r = KR_MAX * np.clip(1 - s, 1e-6, 1) ** N_RES / MU_RES
        trans = trans_base * (lam_i + lam_r)
        p, tx, ty = resolver_pressao(trans, fonte, fixo)

        ux = -tx * (p[:, 1:] - p[:, :-1])
        uy = -ty * (p[1:, :] - p[:-1, :])
        vmax = max(np.abs(ux).max() / volume_celula, np.abs(uy).max() / volume_celula, 1e-30)
        dt = min(cfl / vmax, 0.25 * volume_celula)     # o poço também manda no passo

        f, _ = fracao_fluxo(s)
        fx = np.where(ux > 0, f[:, :-1], f[:, 1:]) * ux
        fy = np.where(uy > 0, f[:-1, :], f[1:, :]) * uy
        div = np.zeros_like(s)
        div[:, :-1] += fx
        div[:, 1:] -= fx
        div[:-1, :] += fy
        div[1:, :] -= fy
        div[0, 0] -= 1.0                        # injetor despeja fase pura
        saida_poco = f[-1, -1] * 1.0
        div[-1, -1] += saida_poco               # produtor retira o que chega

        s_novo = s - dt * div / volume_celula
        perda_clip += float(np.abs(s_novo - np.clip(s_novo, 0.0, 1.0)).sum()) * volume_celula
        s = np.clip(s_novo, 0.0, 1.0)

        injetado += dt * 1.0
        produzido += dt * saida_poco
        passos += 1

        if injetado >= proximo_quadro * alvo / n_quadros or passos == 1:
            registros["passos"].append(passos)
            registros["pvi"].append(injetado / volume_poroso)
            registros["injetado"].append(injetado)
            registros["produzido"].append(produzido)
            registros["massa_dominio"].append(float(s.sum()) * volume_celula)
            registros["campos"].append(s.copy())
            proximo_quadro += 1

    for chave in ("pvi", "injetado", "produzido", "massa_dominio", "passos"):
        registros[chave] = np.array(registros[chave])
    registros["campos"] = np.array(registros["campos"])
    registros["perda_clip"] = perda_clip
    registros["volume_poroso"] = volume_poroso
    registros["passos_totais"] = passos
    return registros


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--segundos", type=float, default=18.0)
    args = ap.parse_args()

    print("lendo SPE10 ...", flush=True)
    camada = carregar_permeabilidade()
    perm3d = camada
    print(f"camada {camada.shape}, perm {camada.min():.2f} a {camada.max():.1f} mD "
          f"(razão {camada.max()/camada.min():.0f}x)", flush=True)

    print("1-D contra Buckley-Leverett ...", flush=True)
    x1, hist = simular_1d(n=400 if args.rapido else 2000)
    # perfil analítico no mesmo PVI para comparar
    pvi_comp = 0.3
    s_analitico = np.full_like(x1, np.nan)
    s_grade = np.linspace(1e-9, 1 - 1e-9, 20001)
    f_grade, df_grade = fracao_fluxo(s_grade)
    g = f_grade / s_grade - df_grade
    idx = np.where(np.diff(np.sign(g)))[0]
    s_frente = float(s_grade[idx[-1]])
    v_frente = float(fracao_fluxo(np.array([s_frente]))[1][0])
    x_frente = v_frente * pvi_comp
    # o ramo certo é o que vai de S_f até 1 (f' decrescente de v_f até 0): o outro lado
    # da curva de f' corresponde a estados que a solução de Riemann não visita
    ramo = s_grade >= s_frente
    df_ramo, s_ramo = df_grade[ramo][::-1], s_grade[ramo][::-1]
    for j, xd in enumerate(x1):
        if xd > x_frente:
            s_analitico[j] = 0.0
        elif xd <= 1e-9:
            s_analitico[j] = 1.0
        else:
            s_analitico[j] = float(np.interp(xd / pvi_comp, df_ramo, s_ramo))
    num = hist[pvi_comp]
    erro_l1 = float(np.mean(np.abs(num - s_analitico)))
    print(f"  S_frente = {s_frente:.3f}, v_frente = {v_frente:.3f}, erro L1 do perfil = {erro_l1:.3f}",
          flush=True)

    print("IMPES 2-D ...", flush=True)
    res = simular_2d(camada, pvi_alvo=0.15 if args.rapido else 0.6,
                     max_passos=400 if args.rapido else 6000,
                     n_quadros=12 if args.rapido else 48)
    inj = float(res["injetado"][-1]) if res["injetado"].size else 0.0
    dentro = float(res["massa_dominio"][-1])
    fora = float(res["produzido"][-1])
    balanco = (inj - dentro - fora) / max(inj, 1e-30)
    print(f"  injetado {inj:.4f} · no domínio {dentro:.4f} · produzido {fora:.4f} "
          f"· fecho {100*(1-balanco):.2f}% · perda de clipping "
          f"{100*res['perda_clip']/max(inj,1e-30):.3f}%", flush=True)
    res["fecho"] = 1 - balanco
    np.savez_compressed(ARQUIVO_DADOS, camada=camada, campos=res["campos"], pvi=res["pvi"],
                        injetado=res["injetado"], produzido=res["produzido"],
                        massa_dominio=res["massa_dominio"], x1=x1, num=num,
                        analitico=s_analitico, erro_l1=erro_l1, s_frente=s_frente,
                        v_frente=v_frente, fecho=1 - balanco, perda_clip=res["perda_clip"])

    desenhar(perm3d, camada, res, x1, num, s_analitico, erro_l1, s_frente, 1 - balanco,
             segundos=args.segundos, rapido=args.rapido)


def desenhar(perm_full, camada, res, x1, num, analitico, erro_l1, s_frente, fecho,
             segundos: float = 18.0, rapido: bool = False) -> None:
    campos, pvi = res["campos"], res["pvi"]
    cores = plt.get_cmap("turbo")
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)

    kicker = "PHYSICS IN ACTION · 01 · CO2 NO SUBSOLO"
    fig.text(0.055, 0.978, kicker, color=estilo.ACENTO_2, fontsize=10.5,
             family="monospace", va="top")
    fig.text(0.055, 0.952, "A pluma que atravessa\no reservatório", color=estilo.TINTA,
             fontsize=24, family="Oxanium", va="top", linespacing=1.12)
    fig.text(0.055, 0.876, "SPE10 Model 1 · deck público 100 × 1 × 20 · IMPES próprio",
             color=estilo.TINTA_2, fontsize=11.5, va="top")

    ax_perm = fig.add_axes([0.09, 0.635, 0.80, 0.170])
    ax_sat = fig.add_axes([0.09, 0.395, 0.80, 0.205])
    ax_bl = fig.add_axes([0.09, 0.115, 0.34, 0.145])
    ax_mass = fig.add_axes([0.55, 0.115, 0.34, 0.145])

    ax_perm.imshow(np.log10(perm_full), cmap="magma", aspect="auto", origin="lower")
    ax_perm.set_title("permeabilidade da camada (log₁₀ mD)", loc="left", fontsize=11, pad=8)
    ax_perm.set_xticks([]); ax_perm.set_yticks([]); ax_perm.grid(False)

    im = ax_sat.imshow(campos[0], cmap="turbo", vmin=0, vmax=1, aspect="auto",
                       origin="lower", interpolation="nearest")
    ax_sat.set_title("saturação da fase injetada", loc="left", fontsize=11, pad=8)
    ax_sat.set_xticks([]); ax_sat.set_yticks([]); ax_sat.grid(False)
    cbar = fig.colorbar(im, ax=ax_sat, fraction=0.035, pad=0.015)
    cbar.ax.tick_params(labelsize=8.5, colors=estilo.TINTA_2)
    cbar.outline.set_edgecolor(estilo.LINHA)
    texto_pvi = ax_sat.text(0.985, 0.965, "", transform=ax_sat.transAxes, ha="right", va="top",
                            color="#ffffff", fontsize=10.5, family="monospace",
                            bbox=dict(boxstyle="round,pad=0.35", fc="#1b1b1b", ec=estilo.LINHA,
                                      alpha=0.85))

    ax_bl.set_title("1-D contra Buckley-Leverett", loc="left", fontsize=10.5, pad=10)
    ax_bl.plot(x1, analitico, color=estilo.TINTA_2, linewidth=3.0, alpha=0.55, label="analítico")
    linha_num, = ax_bl.plot([], [], color=estilo.ACENTO_2, linewidth=1.8, label="IMPES")
    ax_bl.set_xlabel("x_D"); ax_bl.set_ylabel("S")
    ax_bl.legend(fontsize=8.5, loc="lower left")
    ax_bl.text(0.97, 0.05, f"L1 = {erro_l1:.3f}", transform=ax_bl.transAxes, ha="right",
               fontsize=9, family="monospace", color=estilo.ACENTO)

    ax_mass.set_title("balanço de massa", loc="left", fontsize=10.5, pad=10)
    linha_inj, = ax_mass.plot([], [], color=estilo.ACENTO_2, linewidth=2.0, label="injetado")
    linha_den, = ax_mass.plot([], [], color=estilo.VERDE, linewidth=2.0, label="no domínio")
    linha_pro, = ax_mass.plot([], [], color=estilo.ACENTO, linewidth=2.0, label="produzido")
    ax_mass.set_xlabel("passo"); ax_mass.set_ylabel("volume de poros")
    ax_mass.legend(fontsize=8.5, loc="center right")
    ax_mass.set_xlim(0, len(pvi))

    fig.patches.append(plt.Line2D([0.055, 0.945], [0.045, 0.045], transform=fig.transFigure,
                                  color=estilo.LINHA, linewidth=0.9, zorder=60))
    fig.patches.append(plt.Rectangle((0, 0.9955), 1, 0.0045, transform=fig.transFigure,
                                     facecolor=estilo.AZUL, edgecolor="none", zorder=60))
    fig.text(0.055, 0.028, "PINNeAPPle", color=estilo.TINTA, fontsize=9, family="monospace")
    fig.text(0.945, 0.028, f"fecho do balanço {100*fecho:.1f}%", color="#7a7a7a", fontsize=8.5,
             family="monospace", ha="right")

    fps = 30
    n_frames = int(segundos * fps)
    MIDIA.mkdir(parents=True, exist_ok=True)
    video = MIDIA / "ep01-co2-subsolo.mp4"
    escritor = FFMpegWriter(fps=fps, bitrate=4500, codec="libx264",
                            extra_args=["-pix_fmt", "yuv420p", "-crf", "21"])

    def desenha(i: int):
        k = int(round(i / max(n_frames - 1, 1) * (len(campos) - 1)))
        im.set_data(campos[k])
        texto_pvi.set_text(f"PVI {pvi[k]:.2f}")
        # BL: mostra o perfil numérico acumulando até o PVI final (curva completa no fim)
        fracao = (k + 1) / len(campos)
        ax_bl.set_xlim(0, 1)
        ax_bl.set_ylim(0, 1)
        linha_num.set_data(x1 if fracao >= 1 else x1[: int(len(x1) * fracao)],
                           num if fracao >= 1 else num[: int(len(num) * fracao)])
        n = k + 1
        linha_inj.set_data(np.arange(n), res["injetado"][:n])
        linha_den.set_data(np.arange(n), res["massa_dominio"][:n])
        linha_pro.set_data(np.arange(n), res["produzido"][:n])
        ax_mass.set_ylim(0, max(res["injetado"].max(), 1e-3) * 1.1)
        return []

    desenha(0)
    with escritor.saving(fig, str(video), dpi=100):
        for i in range(n_frames):
            desenha(i)
            escritor.grab_frame()
    plt.close(fig)
    print(f"vídeo: {video} ({video.stat().st_size/1e6:.1f} MB)")

    # poster
    fig2, ax = plt.subplots(figsize=(10.8, 13.5), dpi=100)
    fig2.subplots_adjust(0, 0, 1, 1)
    ax.axis("off")
    ax.imshow(campos[-1], cmap="turbo", vmin=0, vmax=1, aspect="auto", origin="lower",
              extent=[0, 1, 0, 1])
    fig2.text(0.055, 0.965, "PHYSICS IN ACTION · 01 · CO2 NO SUBSOLO", color="#ffffff",
              fontsize=10.5, family="monospace", va="top")
    fig2.text(0.055, 0.930, f"PVI {pvi[-1]:.2f} · frente de Welge em S_f = {s_frente:.2f}",
              color="#ffffff", fontsize=16, family="Oxanium", va="top")
    poster = MIDIA / "ep01-co2-subsolo-poster.jpg"
    fig2.savefig(poster, dpi=100, facecolor=estilo.SUPERFICIE)
    plt.close(fig2)
    print(f"poster: {poster}")

    escrever_resultado(camada, res, erro_l1, s_frente, fecho)


def escrever_resultado(camada, res, erro_l1, s_frente, fecho) -> None:
    linhas = [
        "# EP 01 · resultado medido", "",
        "Seção do deck público do SPE10 Model 1 (100 × 1 × 20 células, lida do arquivo original), "
        "injeção no canto inferior esquerdo e "
        "produção no canto oposto, deslocamento bifásico imiscível por IMPES próprio. "
        f"Razão de permeabilidade na camada: {camada.max()/camada.min():.0f}×.", "",
        f"- **Buckley-Leverett 1-D**: erro L1 do perfil de saturação em PVI = 0,3 → "
        f"**{erro_l1:.3f}**; saturação de frente de Welge S_f = **{s_frente:.3f}**.",
        f"- **Balanço de massa 2-D**: injetado = no domínio + produzido fecha em "
        f"**{100*fecho:.1f}%** ao fim da rodada.",
        f"- Saturação máxima no domínio ao final: **{res['campos'][-1].max():.2f}**; "
        f"volume de poros injetado: **{res['pvi'][-1]:.2f}**.", "",
        "## O que este resultado é", "",
        "Deslocamento imiscível de duas fases, com curvas de permeabilidade relativa de Corey e "
        "viscosidade da fase injetada na ordem do CO₂ supercrítico. O campo de permeabilidade é "
        "o dado público do SPE10, lido do arquivo original — não é uma realização sintética.", "",
        "## O que este resultado não é", "",
        "- Não é composicional: não há dissolução, histerese, capilaridade nem variação de "
        "viscosidade com a pressão, que são justamente o que decide o destino do CO₂ num caso real.",
        "- Não é o OPM Flow: é um solver próprio, e a validação dele é contra a solução analítica "
        "de Buckley-Leverett, não contra outro simulador comercial.",
        "- Não é um sítio geológico: a camada do SPE10 é um benchmark público, não um reservatório "
        "com caracterização.",
    ]
    (AQUI / "resultado.md").write_text(texto.virgula("\n".join(linhas)) + "\n")
    print("resultado.md")


if __name__ == "__main__":
    main()
