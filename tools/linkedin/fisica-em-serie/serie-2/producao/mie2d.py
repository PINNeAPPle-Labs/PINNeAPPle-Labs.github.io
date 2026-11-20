"""Espalhamento 2-D por cilindros concêntricos, polarização TM (E ao longo de z).

Série exata de Bessel/Hankel para camadas isotrópicas concêntricas. Para cada harmônico ``n``:

   * região j (interior, ``r_{j-1} < r < r_j``):  ``Ez = A_j J_n(k_j r) + B_j Y_n(k_j r)``,
     com ``B_0 = 0`` por regularidade na origem (ou ``A_0 = B_0 = 0`` se o núcleo é PEC);
   * meio externo:  ``Ez = (-j)^n J_n(k0 r) + C_n H_n^(2)(k0 r)``.

As incógnitas são ``A_0`` (se o núcleo não for PEC), ``(A_j, B_j)`` para ``j = 1..L-1`` e ``C_n``.
Em cada interface impõe-se continuidade de ``Ez`` e de ``(1/mu) dEz/dr``; num núcleo PEC só a
primeira vale, porque não há campo dentro.

Convenção igual à do módulo `em.waves` desta casa — incidente ``exp(-j k0 x)``, dependência
``exp(+j omega t)``, Hankel de segunda espécie — para que a comparação com
``cylinder_scattering_tm`` seja direta e sirva de verificação cruzada.
"""

from __future__ import annotations

import numpy as np
from scipy.special import hankel2, jv, yv


def _inc(n: int) -> complex:
    return (1j) ** (-n)


def _d_j(n, x):
    return (jv(n - 1, x) - jv(n + 1, x)) / 2.0


def _d_y(n, x):
    return (yv(n - 1, x) - yv(n + 1, x)) / 2.0


def _d_h(n, x):
    return (hankel2(n - 1, x) - hankel2(n + 1, x)) / 2.0


def harmonico(n: int, k0: float, raios, eps, mu, pec: bool = False):
    """Resolve o harmônico n e devolve (coeficientes por camada, C_n)."""
    camadas = len(raios)
    k = [k0 * np.sqrt((1.0 if eps[j] is None else eps[j]) * mu[j])
         for j in range(camadas)] + [k0]

    idx = {}
    p = 0
    if not pec:
        idx[("A", 0)] = p
        p += 1
    for j in range(1, camadas):
        idx[("A", j)] = p
        idx[("B", j)] = p + 1
        p += 2
    idx["C"] = p
    m = p + 1

    mat = np.zeros((m, m), dtype=complex)
    rhs = np.zeros(m, dtype=complex)
    linha = 0

    def esquerda(j, r, sinal=+1.0):
        """Preenche as colunas da região j (lado esquerdo da interface)."""
        if pec and j == 0:
            return False
        if j == 0:
            mat[linha, idx[("A", 0)]] += sinal * jv(n, k[0] * r)
        else:
            mat[linha, idx[("A", j)]] += sinal * jv(n, k[j] * r)
            mat[linha, idx[("B", j)]] += sinal * yv(n, k[j] * r)
        return True

    def direita(j, r):
        """Preenche as colunas da região j+1 (lado direito) e devolve os RHS da incidência."""
        if j + 1 == camadas:                       # meio externo
            r_inc = _inc(n) * jv(n, k0 * r)
            mat[linha, idx["C"]] = -hankel2(n, k0 * r)
            rhs[linha] += r_inc
            return
        mat[linha, idx[("A", j + 1)]] = -jv(n, k[j + 1] * r)
        mat[linha, idx[("B", j + 1)]] = -yv(n, k[j + 1] * r)

    for j in range(camadas):
        r = raios[j]
        # --- continuidade de Ez
        esquerda(j, r)
        direita(j, r)
        linha += 1

        if pec and j == 0:
            continue

        # --- continuidade de (1/mu) dEz/dr
        if j == 0:
            mat[linha, idx[("A", 0)]] = _d_j(n, k[0] * r) * k[0] / mu[0]
        else:
            mat[linha, idx[("A", j)]] = _d_j(n, k[j] * r) * k[j] / mu[j]
            mat[linha, idx[("B", j)]] = _d_y(n, k[j] * r) * k[j] / mu[j]
        if j + 1 == camadas:
            mat[linha, idx["C"]] = -_d_h(n, k0 * r) * k0 / mu[camadas]
            rhs[linha] = _inc(n) * _d_j(n, k0 * r) * k0 / mu[camadas]
        else:
            mat[linha, idx[("A", j + 1)]] = -_d_j(n, k[j + 1] * r) * k[j + 1] / mu[j + 1]
            mat[linha, idx[("B", j + 1)]] = -_d_y(n, k[j + 1] * r) * k[j + 1] / mu[j + 1]
        linha += 1

    sol = np.linalg.solve(mat, rhs)
    coef = []
    for j in range(camadas):
        if pec and j == 0:
            coef.append((0.0, 0.0))
        elif j == 0:
            coef.append((sol[idx[("A", 0)]], 0.0))
        else:
            coef.append((sol[idx[("A", j)]], sol[idx[("B", j)]]))
    return coef, sol[idx["C"]]


def ordem_maxima(k0, raios, eps):
    valor = np.max([1.0 if e is None else np.abs(e) for e in eps])
    return int(np.ceil(k0 * max(raios) * np.sqrt(valor) + 12))


def largura_espalhamento(k0, raios, eps, mu=None, n_max=None):
    """Largura de espalhamento 2-D (unidade de comprimento)."""
    mu = [1.0] * (len(raios) + 1) if mu is None else list(mu)
    n_max = ordem_maxima(k0, raios, eps) if n_max is None else n_max
    C = [harmonico(n, k0, raios, eps, mu, pec=(eps[0] is None))[1]
         for n in range(-n_max, n_max + 1)]
    return float(4.0 / k0 * np.sum(np.abs(C) ** 2))


def campo(x, y, k0, raios, eps, mu=None, n_max=None):
    """Campo Ez total nos pontos (x, y)."""
    mu = [1.0] * (len(raios) + 1) if mu is None else list(mu)
    pec = eps[0] is None
    n_max = ordem_maxima(k0, raios, eps) if n_max is None else n_max
    x, y = np.asarray(x, float), np.asarray(y, float)
    rho, phi = np.hypot(x, y), np.arctan2(y, x)
    rho = np.maximum(rho, 1e-300)
    regiao = np.digitize(rho, raios)
    # dentro do espalhador o campo já é o total (série de J/Y da camada): a incidente só entra
    # onde a região é o meio externo
    total = np.where(regiao == len(raios), np.exp(-1j * k0 * x), 0.0).astype(complex)
    camadas = len(raios)
    for n in range(-n_max, n_max + 1):
        coef, C = harmonico(n, k0, raios, eps, mu, pec)
        e = C * hankel2(n, k0 * rho)
        for j in range(camadas):
            sel = regiao == j
            if not np.any(sel):
                continue
            kj = k0 * np.sqrt((1.0 if pec and j == 0 else eps[j]) * mu[j])
            a, b = coef[j]
            rsel = rho[sel]
            valor = a * jv(n, kj * rsel)
            if b != 0.0:                            # Y_n diverge na origem: só entra se valer
                valor = valor + b * yv(n, kj * rsel)
            e[sel] = valor
        total += e * np.exp(1j * n * phi)
    return total
