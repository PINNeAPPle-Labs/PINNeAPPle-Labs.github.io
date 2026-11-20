"""Águas rasas 1-D e 2-D: volumes finitos, fluxo HLL, paredes por células fantasma.

A parede é o detalhe que costuma passar batido: numa condição de contorno refletiva o fluxo de
massa é nulo, mas o de quantidade de movimento **não** — a parede exerce pressão. Tratar a face
de contorno como fluxo zero cria uma força espúria na primeira e na última célula (foi
exatamente o que a primeira versão deste solucionador fazia). Aqui a borda entra por célula
fantasma espelhada, e o fluxo na face da parede sai com a pressão certa.
"""

from __future__ import annotations

import numpy as np

G = 9.81
SECO = 1e-4


def _hll(hL, uL, hR, uR):
    cL = np.sqrt(G * np.maximum(hL, 0.0))
    cR = np.sqrt(G * np.maximum(hR, 0.0))
    FLh = hL * uL
    FLm = hL * uL * uL + 0.5 * G * hL * hL
    FRh = hR * uR
    FRm = hR * uR * uR + 0.5 * G * hR * hR
    sL = np.minimum(np.minimum(uL - cL, uR - cR), 0.0)
    sR = np.maximum(np.maximum(uL + cL, uR + cR), 0.0)
    den = np.where(np.abs(sR - sL) < 1e-12, 1e-12, sR - sL)
    fh = (sR * FLh - sL * FRh + sL * sR * (hR - hL)) / den
    fm = (sR * FLm - sL * FRm + sL * sR * (hR * uR - hL * uL)) / den
    return fh, fm


def _vel(h, m):
    return np.where(h > SECO, m / np.maximum(h, 1e-12), 0.0)


def passo_1d(h: np.ndarray, hu: np.ndarray, dx: float, dt: float):
    hp = np.concatenate([[h[0]], h, [h[-1]]])          # fantasma espelhada: h igual, u trocado
    mp = np.concatenate([[-hu[0]], hu, [-hu[-1]]])
    up = _vel(hp, mp)
    fh, fm = _hll(hp[:-1], up[:-1], hp[1:], up[1:])
    h = h - dt / dx * (fh[1:] - fh[:-1])
    hu = hu - dt / dx * (fm[1:] - fm[:-1])
    h = np.maximum(h, SECO)
    hu = np.where(h > 2 * SECO, hu, 0.0)
    return h, hu


def passo_2d(h, hu, hv, dx, dy, dt):
    # --- direção x
    hp = np.concatenate([h[:, :1], h, h[:, -1:]], axis=1)
    mp = np.concatenate([-hu[:, :1], hu, -hu[:, -1:]], axis=1)
    vp = np.concatenate([hv[:, :1], hv, hv[:, -1:]], axis=1)
    up = _vel(hp, mp)
    fh, fm = _hll(hp[:, :-1], up[:, :-1], hp[:, 1:], up[:, 1:])
    fv = np.where(fh > 0, vp[:, :-1] * up[:, :-1], vp[:, 1:] * up[:, 1:])
    h = h - dt / dx * (fh[:, 1:] - fh[:, :-1])
    hu = hu - dt / dx * (fm[:, 1:] - fm[:, :-1])
    hv = hv - dt / dx * (fv[:, 1:] - fv[:, :-1])

    # --- direção y
    hp = np.concatenate([h[:1, :], h, h[-1:, :]], axis=0)
    mp = np.concatenate([-hv[:1, :], hv, -hv[-1:, :]], axis=0)
    up2 = _vel(hp, mp)
    up_x = np.concatenate([hu[:1, :], hu, hu[-1:, :]], axis=0)
    gh, gm = _hll(hp[:-1, :], up2[:-1, :], hp[1:, :], up2[1:, :])
    gu = np.where(gh > 0, up_x[:-1, :] * up2[:-1, :], up_x[1:, :] * up2[1:, :])
    h = h - dt / dy * (gh[1:, :] - gh[:-1, :])
    hv = hv - dt / dy * (gm[1:, :] - gm[:-1, :])
    hu = hu - dt / dy * (gu[1:, :] - gu[:-1, :])

    h = np.maximum(h, SECO)
    seco = h <= 2 * SECO
    hu = np.where(seco, 0.0, hu)
    hv = np.where(seco, 0.0, hv)
    return h, hu, hv


def cfl_1d(h, hu, dx, cfl):
    u = _vel(h, hu)
    return cfl * dx / float(np.max(np.abs(u) + np.sqrt(G * np.maximum(h, SECO))))


def ritter(x, t, x0, h0):
    """Solução exata do rompimento em leito seco."""
    c0 = np.sqrt(G * h0)
    xi = (x - x0) / t
    h = np.zeros_like(x)
    dentro = (xi > -c0) & (xi < 2 * c0)
    c = (2 * c0 - xi) / 3
    h[dentro] = c[dentro] ** 2 / G
    h[xi <= -c0] = h0
    return h
