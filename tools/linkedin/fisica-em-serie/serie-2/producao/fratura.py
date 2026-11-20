"""Elasticidade 2-D (Q4, estado plano) com trinca central: J-integral por forma de domínio.

Modelo de **quarto de placa**: a placa tem meia-largura ``W`` e meia-altura ``H``, a trinca de
comprimento ``2a`` está centrada na origem sobre ``y = 0``, e as simetrias entram direto:

  * ``x = 0`` (plano que corta a trinca ao meio): ``ux = 0``;
  * ``y = 0`` para ``x > a`` (ligamento): ``uy = 0``;
  * ``y = 0`` para ``x < a`` (face da trinca): livre, sem nenhuma condição — é o que faz a
    trinca existir sem duplicar nós;
  * ``y = H``: tração uniforme ``sigma``.

O fator de intensidade de tensão sai do J-integral na forma de domínio equivalente,

    J = integral_A [ (sigma_ij du_i/dx1 - W delta_1j) dq/dxj ] dA,     W = 1/2 sigma:epsilon

com ``q`` valendo 1 perto da ponta e 0 longe dela. Em estado plano linear elástico ``J = K^2/E'``,
com ``E' = E`` (tensão plana) e ``E' = E/(1-nu^2)`` (deformação plana).
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def _eixo(lo, hi, n, anchor, grau):
    """Coordenadas de ``lo`` a ``hi``, mais densas perto de ``anchor`` (uma das pontas).

    A malha uniforme não resolve o campo singular da ponta da trinca: o J-integral fica preso em
    ~25% de erro por mais que se refine tudo por igual. O refino tem de ser **local**, e é o que
    esta função faz.
    """
    t = np.linspace(0.0, 1.0, n + 1)
    s = t ** grau if abs(anchor - hi) < abs(anchor - lo) else 1.0 - (1.0 - t) ** grau
    return lo + (hi - lo) * s


def malha(comprimento: float, meia_altura: float, a: float, nx: int, ny: int, grau=1.8):
    """Malha de Q4 em ``[0, comprimento] x [-meia_altura, meia_altura]`` com trinca em ``y = 0``.

    A trinca vai de ``x = 0`` a ``x = a``. Os nós dessa linha dentro da trinca são **duplicados**:
    os elementos acima usam a cópia de cima e os de baixo a de baixo, de modo que a face da trinca
    fica livre sem nenhuma condição especial. ``ny`` tem de ser par para a linha cair em nós.
    """
    if ny % 2:
        raise ValueError("ny tem de ser par para que a linha da trinca caia sobre nós")
    if a <= 0.0:                                   # sem trinca: malha uniforme e sem duplicação
        x = np.linspace(0.0, comprimento, nx + 1)
    else:
        ne, nd = nx // 2, nx - nx // 2
        x = np.concatenate([_eixo(0.0, a, ne, a, grau), _eixo(a, comprimento, nd, a, grau)[1:]])
    ne_y, nd_y = ny // 2, ny - ny // 2
    y = np.concatenate([_eixo(-meia_altura, 0.0, ne_y, 0.0, grau),
                        _eixo(0.0, meia_altura, nd_y, 0.0, grau)[1:]])
    X, Y = np.meshgrid(x, y, indexing="ij")
    base = np.column_stack([X.ravel(), Y.ravel()])
    idx = np.arange((nx + 1) * (ny + 1)).reshape(nx + 1, ny + 1)
    j0 = ny // 2
    dentro = (x < a - 1e-12) if a > 0.0 else np.zeros_like(x, dtype=bool)

    copia = np.full((nx + 1,), -1, dtype=int)
    extra = []
    proximo = idx.max() + 1
    for i in np.where(dentro)[0]:
        copia[i] = proximo
        extra.append(base[idx[i, j0]])
        proximo += 1
    nos = np.vstack([base] + [np.array(extra)]) if extra else base

    elems = np.empty((nx * ny, 4), dtype=int)
    for i in range(nx):
        for j in range(ny):
            e = i * ny + j
            conn = [idx[i, j], idx[i + 1, j], idx[i + 1, j + 1], idx[i, j + 1]]
            if j == j0 - 1:                       # elemento logo abaixo da linha da trinca
                conn = [copia[i] if (jj == j0 and copia[i] > 0) else c
                        for c, jj in zip(conn, (j, j, j + 1, j + 1))]
            elems[e] = conn
    return nos, elems


def _D(E: float, nu: float, plano: str):
    if plano == "tensao":
        c = E / (1.0 - nu ** 2)
        return c * np.array([[1.0, nu, 0.0], [nu, 1.0, 0.0], [0.0, 0.0, (1 - nu) / 2]])
    c = E / ((1.0 + nu) * (1.0 - 2.0 * nu))
    return c * np.array([[1 - nu, nu, 0.0], [nu, 1 - nu, 0.0], [0.0, 0.0, (1 - 2 * nu) / 2]])


G = 1.0 / np.sqrt(3.0)
PONTOS = [(-G, -G), (G, -G), (G, G), (-G, G)]


def _forma(xi, eta):
    N = 0.25 * np.array([(1 - xi) * (1 - eta), (1 + xi) * (1 - eta),
                         (1 + xi) * (1 + eta), (1 - xi) * (1 + eta)])
    dN = 0.25 * np.array([[-(1 - eta), -(1 - xi)], [(1 - eta), -(1 + xi)],
                          [(1 + eta), (1 + xi)], [-(1 + eta), (1 - xi)]])
    return N, dN


def matriz_local(coords, D):
    """Rigidez do elemento Q4 (espessura unitária)."""
    k = np.zeros((8, 8))
    for xi, eta in PONTOS:
        N, dN = _forma(xi, eta)
        J = coords.T @ dN
        det = np.linalg.det(J)
        dNx = dN @ np.linalg.inv(J)
        B = np.zeros((3, 8))
        B[0, 0::2] = dNx[:, 0]
        B[1, 1::2] = dNx[:, 1]
        B[2, 0::2] = dNx[:, 1]
        B[2, 1::2] = dNx[:, 0]
        k += B.T @ D @ B * det
    return k


def resolver(nos, elems, E, nu, sigma, plano="tensao", meia_altura=0.1, espessura=1.0):
    """Monta e resolve; tração uniforme em ``y = ±meia_altura``, simetria em ``x = 0``."""
    D = _D(E, nu, plano)
    n = len(nos)
    linhas, colunas, valores = [], [], []
    for conn in elems:
        ke = matriz_local(nos[conn], D) * espessura
        for i in range(4):
            for j in range(4):
                linhas += [2 * conn[i], 2 * conn[i] + 1, 2 * conn[i], 2 * conn[i] + 1]
                colunas += [2 * conn[j], 2 * conn[j] + 1, 2 * conn[j] + 1, 2 * conn[j]]
                valores += [ke[2*i, 2*j], ke[2*i+1, 2*j+1], ke[2*i, 2*j+1], ke[2*i+1, 2*j]]
    K = coo_matrix((valores, (linhas, colunas)), shape=(2 * n, 2 * n)).tocsr()

    F = np.zeros(2 * n)
    for borda, sinal in ((meia_altura, +1.0), (-meia_altura, -1.0)):
        linha = np.where(np.isclose(nos[:, 1], borda))[0]
        linha = linha[np.argsort(nos[linha, 0])]
        dx = np.diff(nos[linha, 0])
        for k, no in enumerate(linha):
            peso = (dx[k - 1] if k > 0 else 0.0) / 2.0 + (dx[k] if k < len(dx) else 0.0) / 2.0
            F[2 * no + 1] += sinal * sigma * peso * espessura

    fixos = list(2 * np.where(np.isclose(nos[:, 0], 0.0))[0])          # ux = 0 em x = 0
    canto = np.argmin(np.hypot(nos[:, 0], nos[:, 1] - meia_altura))
    fixos.append(2 * int(canto) + 1)                                    # tira a translação em y
    fixos = np.unique(np.array(fixos))

    livres = np.setdiff1d(np.arange(2 * n), fixos)
    u = np.zeros(2 * n)
    u[livres] = spsolve(K[livres][:, livres], F[livres])
    return u


def tensoes(nos, elems, u, E, nu, plano="tensao"):
    """Tensão e deformação médias por elemento (no centro)."""
    D = _D(E, nu, plano)
    saida = []
    for conn in elems:
        coords = nos[conn]
        N, dN = _forma(0.0, 0.0)
        J = coords.T @ dN
        dNx = dN @ np.linalg.inv(J)
        B = np.zeros((3, 8))
        B[0, 0::2] = dNx[:, 0]
        B[1, 1::2] = dNx[:, 1]
        B[2, 0::2] = dNx[:, 1]
        B[2, 1::2] = dNx[:, 0]
        ue = u[2 * conn[:, None] + np.array([0, 1])].ravel()
        eps = B @ ue
        saida.append((D @ eps, eps, coords, dNx, ue))
    return saida


def j_integral(nos, elems, u, E, nu, ponta, raio, plano="tensao", espessura=1.0):
    """J-integral por forma de domínio equivalente, com q em platô de raio ``raio``."""
    campos = tensoes(nos, elems, u, E, nu, plano)
    J = 0.0
    x_tip = np.asarray(ponta, float)
    for sig, eps, coords, dNx, ue in campos:
        centro = coords.mean(axis=0)
        if np.linalg.norm(centro - x_tip) > 2.2 * raio:
            continue
        # q nos nós do elemento: 1 dentro de raio, 0 fora de 1.6 raio, linear entre os dois
        q = np.ones(4)
        dq = np.zeros(4)
        for i, c in enumerate(coords):
            r = np.linalg.norm(c - x_tip)
            q[i] = 1.0 if r <= raio else (0.0 if r >= 1.6 * raio else (1.6 * raio - r) / (0.6 * raio))
        # gradiente de q pela própria interpolação bilinear
        dqdx = dNx[:, 0] @ q
        dqdy = dNx[:, 1] @ q
        # derivadas do deslocamento
        dux = np.zeros(2); duy = np.zeros(2)
        for i in range(4):
            dux += dNx[i, :] * ue[2 * i]
            duy += dNx[i, :] * ue[2 * i + 1]
        W = 0.5 * (sig[0] * eps[0] + sig[1] * eps[1] + sig[2] * eps[2])
        area = np.prod(np.ptp(coords, axis=0))
        termo_x = (sig[0] * dux[0] + sig[2] * duy[0] - W) * dqdx
        termo_y = (sig[2] * dux[1] + sig[1] * duy[1]) * dqdy
        J += (termo_x + termo_y) * area
    return float(J * espessura)


def k_de_j(J, E, nu, plano="tensao"):
    Ef = E if plano == "tensao" else E / (1.0 - nu ** 2)
    return float(np.sqrt(max(J, 0.0) * Ef))


def k_feddersen(sigma, a, meia_largura):
    """Trinca central em placa finita de meia-largura ``W``: K = sigma sqrt(pi a) sqrt(sec(pi a / 2W))."""
    return sigma * np.sqrt(np.pi * a) / np.sqrt(np.cos(np.pi * a / (2.0 * meia_largura)))


def _integrando(sig, eps, grad, n):
    """W n_x - (t . du/dx) numa face de normal n, com t = sigma . n."""
    W = 0.5 * (sig[0] * eps[0] + sig[1] * eps[1] + sig[2] * eps[2])
    tx = sig[0] * n[0] + sig[2] * n[1]
    ty = sig[2] * n[0] + sig[1] * n[1]
    return W * n[0] - (tx * grad[0] + ty * grad[1])


def j_contorno(nos, elems, u, E, nu, a, meia_altura, nx, ny, k=4, plano="tensao"):
    """J-integral pela definição: contorno retangular fechado em volta da ponta.

    O caminho sai da face superior da trinca, sobe, atravessa por cima da ponta, desce pelo lado
    do ligamento e volta pela face inferior. Os elementos usados são os vizinhos de cada trecho,
    e o normal aponta para fora da região que contém a ponta.
    """
    E_mod = E if plano == "tensao" else E / (1.0 - nu ** 2)
    D = _D(E, nu, plano)
    j0 = ny // 2
    i_t = int(np.argmin(np.abs(np.unique(np.round(nos[:, 0], 12)) - a)))
    xs = np.unique(np.round(nos[:, 0], 12))
    ys = np.unique(np.round(nos[:, 1], 12))
    i1, i2 = i_t - k, i_t + k
    j1, j2 = j0 - k, j0 + k
    x1, x2, y1, y2 = xs[i1], xs[i2], ys[j1], ys[j2]

    def tensao_elem(i, j):
        e = i * ny + j
        conn = elems[e]
        coords = nos[conn]
        N, dN = _forma(0.0, 0.0)
        Jinv = np.linalg.inv(coords.T @ dN)
        dNx = dN @ Jinv
        B = np.zeros((3, 8))
        B[0, 0::2] = dNx[:, 0]; B[1, 1::2] = dNx[:, 1]
        B[2, 0::2] = dNx[:, 1]; B[2, 1::2] = dNx[:, 0]
        ue = u[2 * conn[:, None] + np.array([0, 1])].ravel()
        eps = B @ ue
        return D @ eps, eps, np.array([dNx[:, 0] @ ue[0::2], dNx[:, 0] @ ue[1::2]])

    J = 0.0
    # trecho vertical esquerdo, de y=0 até y2 (elementos à direita: i = i1)
    for j in range(j0, j2):
        sig, eps, grad = tensao_elem(i1, j)
        J += _integrando(sig, eps, grad, (-1.0, 0.0)) * (ys[j + 1] - ys[j])
    # trecho superior, de x1 até x2 (elementos abaixo: j = j2-1)
    for i in range(i1, i2):
        sig, eps, grad = tensao_elem(i, j2 - 1)
        J += _integrando(sig, eps, grad, (0.0, 1.0)) * (xs[i + 1] - xs[i])
    # trecho vertical direito, de y2 até y1 (elementos à esquerda: i = i2-1)
    for j in range(j1 + 1, j2 + 1):
        sig, eps, grad = tensao_elem(i2 - 1, j - 1)
        J += _integrando(sig, eps, grad, (1.0, 0.0)) * (ys[j] - ys[j - 1])
    # trecho inferior, de x2 até x1 (elementos acima: j = j1)
    for i in range(i1, i2):
        sig, eps, grad = tensao_elem(i, j1)
        J += _integrando(sig, eps, grad, (0.0, -1.0)) * (xs[i + 1] - xs[i])
    # trecho vertical esquerdo inferior, de y1 até 0 (elementos à direita: i = i1)
    for j in range(j1, j0):
        sig, eps, grad = tensao_elem(i1, j)
        J += _integrando(sig, eps, grad, (-1.0, 0.0)) * (ys[j + 1] - ys[j])
    return float(J)
