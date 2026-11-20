"""Euler quasi-1D (bocal de área variável): volumes finitos, fluxo HLLC, primeira ordem.

O bocal é a geometria que decide o foguete: garganta sônica, divergente que converte pressão em
velocidade, e — quando a contrapressão sobe — um choque normal parado dentro do divergente. As
três coisas que este módulo resolve têm solução analítica, e é contra elas que o episódio se
verifica:

  * distribuição de Mach no escoamento isentrópico → relação área–Mach;
  * vazão em massa com garganta sônica → fórmula da vazão crítica;
  * posição do choque → choque normal (Rankine–Hugoniot) casado com o isentrópico dos dois lados.

Equações conservativas com área:

    d(A U)/dt + d(A F)/dx = S,     U = [rho, rho u, E],  F = [rho u, rho u^2 + p, u (E + p)]
    S = [0, p dA/dx, 0]

Tratamento de fronteira: células fantasma, entrada subsônica com p0 e T0 impostos, saída
supersônica por extrapolação e saída subsônica com contrapressão.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

GAMMA = 1.4
RGAS = 287.0
CP = GAMMA * RGAS / (GAMMA - 1.0)


# ---------------------------------------------------------------- geometria

def area(x, a_t=1.0, a_in=3.0, a_exit=2.5, x_t=0.35, comprimento=1.0):
    """Bocal convergente-divergente: garganta em x_t, entrada e saída com áreas declaradas."""
    x = np.asarray(x, dtype=float)
    a = np.empty_like(x)
    conv = x <= x_t
    a[conv] = a_t + (a_in - a_t) * ((x_t - x[conv]) / x_t) ** 2
    div = ~conv
    a[div] = a_t + (a_exit - a_t) * ((x[div] - x_t) / (comprimento - x_t)) ** 2
    return a


# ---------------------------------------------------------------- analítico

def area_mach(m, gamma=GAMMA):
    """A/A* para um Mach m."""
    return (1.0 / m) * ((2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * m * m)) ** (
        (gamma + 1.0) / (2.0 * (gamma - 1.0)))


def mach_de_area(razao, supersônico=True, gamma=GAMMA):
    """Inverte a relação área–Mach no ramo pedido."""
    alvo = lambda m: area_mach(m, gamma) - razao  # noqa: E731
    limite = 1.0 - 1e-9 if not supersônico else 1.0 + 1e-9
    if supersônico:
        return brentq(alvo, limite, 60.0)
    return brentq(alvo, 1e-6, limite)


def vazao_critica(p0, t0, a_estrela, gamma=GAMMA, rgas=RGAS):
    """Vazão em massa com garganta sônica."""
    return (a_estrela * p0 / np.sqrt(t0) * np.sqrt(gamma / rgas) *
            (2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (2.0 * (gamma - 1.0))))


def choque_normal(m1, gamma=GAMMA):
    """Razões de Rankine–Hugoniot para o choque normal."""
    m2 = np.sqrt((1.0 + 0.5 * (gamma - 1.0) * m1 ** 2) / (gamma * m1 ** 2 - 0.5 * (gamma - 1.0)))
    p2_p1 = 1.0 + 2.0 * gamma / (gamma + 1.0) * (m1 ** 2 - 1.0)
    p02_p01 = ((gamma + 1.0) * m1 ** 2 / ((gamma - 1.0) * m1 ** 2 + 2.0)) ** (
        gamma / (gamma - 1.0)) * ((gamma + 1.0) / (2.0 * gamma * m1 ** 2 - (gamma - 1.0))) ** (
        1.0 / (gamma - 1.0))
    return m2, p2_p1, p02_p01


def saida_por_choque(x_choque, p0=1.0e6, a_t=1.0, a_in=3.0, a_exit=2.5, x_t=0.35,
                     comprimento=1.0, gamma=GAMMA):
    """Para um choque parado em x_choque: (M_e, p_e/p0) do escoamento a jusante."""
    a_s = float(area(x_choque, a_t, a_in, a_exit, x_t, comprimento))
    m1 = mach_de_area(a_s / a_t, True, gamma)
    m2, _, p02_p01 = choque_normal(m1, gamma)
    # a jusante o A* é outro: escala pela garganta equivalente daquele escoamento
    a_estrela_2 = a_s / area_mach(m2, gamma)
    m_e = mach_de_area(a_exit / a_estrela_2, False, gamma)
    p_e_p02 = (1.0 + 0.5 * (gamma - 1.0) * m_e ** 2) ** (-gamma / (gamma - 1.0))
    return m_e, p_e_p02 * p02_p01


def contrapressao_do_choque(x_choque, p0=1.0e6, **kw):
    """Contrapressão (absoluta) que mantém o choque exatamente em x_choque."""
    _, pe_sobre_p0 = saida_por_choque(x_choque, p0=p0, **kw)
    return pe_sobre_p0 * p0


# ---------------------------------------------------------------- fluxo HLLC

def _onda(u, a):
    return u - a, u + a


def _hllc(rl, ul, pl, rr, ur, pr, gamma=GAMMA):
    """Fluxo HLLC com estimativa de Davis para as ondas externas e contacto de Rankine–Hugoniot.

    A seleção de região é a parte que não perdoa: F_L só vale onde S_L >= 0, F*_L entre S_L e
    S_M, F*_R entre S_M e S_R, e F_R acima de S_R. Trocar isso por um `where` mais curto foi o
    que fez a primeira versão deste solucionador divergir.
    """
    al = np.sqrt(gamma * pl / rl)
    ar = np.sqrt(gamma * pr / rr)
    el = pl / (gamma - 1.0) + 0.5 * rl * ul * ul
    er = pr / (gamma - 1.0) + 0.5 * rr * ur * ur

    sl = np.minimum(ul - al, ur - ar)
    sr = np.maximum(ul + al, ur + ar)
    den = np.where(np.abs(rl * (sl - ul) - rr * (sr - ur)) < 1e-12, 1e-12,
                   rl * (sl - ul) - rr * (sr - ur))
    sm = (pr - pl + rl * ul * (sl - ul) - rr * ur * (sr - ur)) / den

    flh, flm, fle = rl * ul, rl * ul * ul + pl, ul * (el + pl)
    frh, frm, fre = rr * ur, rr * ur * ur + pr, ur * (er + pr)

    def estrela(r, u, p, e, s):
        # s - u é **negativo** do lado esquerdo: um máximo com zero aqui estraga o estado
        # estrela (foi exatamente esse o erro que fez o tubo de choque explodir na primeira vez)
        den = r * (s - u)
        den = np.where(np.abs(den) < 1e-30, 1e-30, den)
        fator = r * (s - u) / np.where(np.abs(s - sm) < 1e-12, 1e-12, s - sm)
        rho_est = fator
        mom_est = fator * sm
        ene_est = fator * (e / r + (sm - u) * (sm + p / den))
        return rho_est, mom_est, ene_est

    rl_est, ml_est, el_est = estrela(rl, ul, pl, el, sl)
    rr_est, mr_est, er_est = estrela(rr, ur, pr, er, sr)

    fstar_l = (flh + sl * (rl_est - rl), flm + sl * (ml_est - rl * ul),
               fle + sl * (el_est - el))
    fstar_r = (frh + sr * (rr_est - rr), frm + sr * (mr_est - rr * ur),
               fre + sr * (er_est - er))

    def escolhe(fl, fsl, fsr, fr):
        return np.where(sl >= 0, fl,
                        np.where(sm >= 0, fsl, np.where(sr > 0, fsr, fr)))

    fh = escolhe(flh, fstar_l[0], fstar_r[0], frh)
    fm = escolhe(flm, fstar_l[1], fstar_r[1], frm)
    fe = escolhe(fle, fstar_l[2], fstar_r[2], fre)
    return fh, fm, fe, sm, sl, sr


# ---------------------------------------------------------------- solver

class Bocal:
    """Estado primitivo por célula, com área nas faces e fonte de variação de área."""

    def __init__(self, n=1200, p0=1.0e6, t0=300.0, a_t=1.0, a_in=3.0, a_exit=2.5,
                 x_t=0.35, comprimento=1.0, p_back=None):
        self.n = n
        self.p0, self.t0 = p0, t0
        self.comprimento = comprimento
        self.a_t, self.a_in, self.a_exit, self.x_t = a_t, a_in, a_exit, x_t
        self.dx = comprimento / n
        self.x = (np.arange(n) + 0.5) * self.dx
        self.a_c = area(self.x, a_t, a_in, a_exit, x_t, comprimento)
        self.a_f = area(np.arange(n + 1) * self.dx, a_t, a_in, a_exit, x_t, comprimento)
        self.p_back = p_back

        # começo de baixo para cima: escoamento quase parado, com pressão de estagnação
        self.rho = np.full(n, p0 / (RGAS * t0))
        self.u = np.full(n, 1.0)
        self.p = np.full(n, p0)

    # -- utilidades
    @property
    def a_som(self):
        return np.sqrt(GAMMA * self.p / self.rho)

    @property
    def mach(self):
        return np.abs(self.u) / self.a_som

    def conservadas(self, rho=None, u=None, p=None):
        rho = self.rho if rho is None else rho
        u = self.u if u is None else u
        p = self.p if p is None else p
        e = p / (GAMMA - 1.0) + 0.5 * rho * u * u
        return rho, rho * u, e

    def _fantasmas(self):
        """Duas células fantasma de cada lado: entrada com estagnação, saída conforme o regime."""
        rho, u, p = self.rho, self.u, self.p
        # esquerda: entrada subsônica, p0 e T0 impostos, velocidade vinda do interior
        u_in = u[0]
        t_in = self.t0 - 0.5 * u_in ** 2 / CP
        p_in = self.p0 * (t_in / self.t0) ** (GAMMA / (GAMMA - 1.0))
        rho_in = p_in / (RGAS * t_in)
        # direita: extrapola se a saída é supersônica; impõe contrapressão se subsônica —
        # e também quando a pressão interna caiu abaixo da contrapressão, porque nesse caso
        # o escoamento não pode ser supersônico (senão o bocal ficaria travado na solução
        # isentrópica qualquer que fosse a contrapressão: é histerese de condição de contorno)
        if self.p_back is None or (self.mach[-1] >= 1.0 and self.p[-1] >= self.p_back):
            rho_o, u_o, p_o = rho[-1], u[-1], p[-1]
        else:
            rho_o, u_o, p_o = rho[-1], u[-1], self.p_back
        return (np.concatenate([np.full(2, rho_in), rho, np.full(2, rho_o)]),
                np.concatenate([np.full(2, u_in), u, np.full(2, u_o)]),
                np.concatenate([np.full(2, p_in), p, np.full(2, p_o)]))

    def _taxa(self):
        rho, u, p = self._fantasmas()
        fh, fm, fe, _, _, _ = _hllc(rho[:-1], u[:-1], p[:-1], rho[1:], u[1:], p[1:])
        # as faces físicas são as de índice 1..n+1 no arranjo com fantasma
        fh = fh[1:self.n + 2] * self.a_f
        fm = fm[1:self.n + 2] * self.a_f
        fe = fe[1:self.n + 2] * self.a_f
        dh = -(fh[1:] - fh[:-1]) / self.dx
        dm = -(fm[1:] - fm[:-1]) / self.dx + self.p * (self.a_f[1:] - self.a_f[:-1]) / self.dx
        de = -(fe[1:] - fe[:-1]) / self.dx
        return dh / self.a_c, dm / self.a_c, de / self.a_c

    def _aplicar(self, drho, dmu, de, dt):
        rho, mu, e = self.conservadas()
        rho = rho + dt * drho
        mu = mu + dt * dmu
        e = e + dt * de
        self.rho = rho
        self.u = mu / rho
        self.p = (e - 0.5 * rho * self.u ** 2) * (GAMMA - 1.0)
        self.p = np.maximum(self.p, 1e-6 * self.p0)

    def passo(self, cfl=0.45):
        dt = cfl * self.dx / float(np.max(np.abs(self.u) + self.a_som))
        d1 = self._taxa()
        r0, m0, e0 = self.conservadas()
        self._aplicar(*d1, dt)
        d2 = self._taxa()
        self.rho, self.u, self.p = r0, m0 / r0, (e0 - 0.5 * r0 * (m0 / r0) ** 2) * (GAMMA - 1.0)
        self.p = np.maximum(self.p, 1e-6 * self.p0)
        self._aplicar(*d2, dt)
        return dt

    def vazao(self):
        k = int(np.argmin(self.a_c))
        return float(self.rho[k] * self.u[k] * self.a_c[k])

    def estagnacao(self):
        """Pressão de estagnação local, para achar o choque pela queda de p0."""
        m = self.mach
        return self.p * (1.0 + 0.5 * (GAMMA - 1.0) * m ** 2) ** (GAMMA / (GAMMA - 1.0))

    def rodar(self, passos=200000, tol=2e-9, cfl=0.45, cada=200):
        anterior = None
        for i in range(passos):
            self.passo(cfl)
            if i % cada == 0:
                atual = self.rho * self.u * self.a_c
                if anterior is not None:
                    escala = float(np.max(np.abs(atual)))
                    desvio = float(np.max(np.abs(atual - anterior))) / max(escala, 1e-30)
                    if desvio < tol and i > 2000:
                        return i, desvio
                anterior = atual
        return passos, float("nan")

    def posicao_choque(self, margem=0.06):
        """Onde a pressão de estagnação cai, e a queda entre os dois patamares.

        Ler a queda no próprio mínimo do choque mede o valor dentro da transição espalhada, não
        o estado a jusante: um esquema de primeira ordem suaviza o choque em algumas células e
        o mínimo fica no meio do degrau. Por isso a queda é medida entre patamares, longe da
        transição.
        """
        p0 = self.estagnacao()
        divergente = self.x > self.x_t
        i = int(np.argmin(np.where(divergente, p0, np.inf)))
        x_s = float(self.x[i])
        # a margem encolhe quando o choque chega perto de uma das pontas: com o choque colado
        # na saída não há 6 cm de patamar a jusante, e usar a margem fixa devolveria o valor
        # dentro da transição em vez do estado de jusante
        margem = max(min(margem, 0.35 * (x_s - self.x_t), 0.35 * (self.comprimento - x_s)),
                     3.0 * self.dx)
        jusante = self.x > x_s + margem
        montante = (self.x > self.x_t + margem) & (self.x < x_s - margem)
        if jusante.sum() < 5 or montante.sum() < 5:
            return x_s, float(p0[i] / p0[0])
        return x_s, float(np.mean(p0[jusante]) / np.mean(p0[montante]))
