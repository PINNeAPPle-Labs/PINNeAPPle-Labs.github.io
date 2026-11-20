"""Motor de indução acoplado a uma rede térmica: perdas elétricas viram calor, calor vira perda.

Duas metades, e o acoplamento entre elas é o episódio:

  * **elétrica**: circuito equivalente por fase do motor de indução (IEEE), com o ramo de
    magnetização. Do escorregamento saem torque, correntes e perdas (cobre do estator, cobre do
    rotor, ferro e mecânicas);
  * **térmica**: rede de três nós (enrolamento, ferro, carcaça) com capacidades e condutâncias
    declaradas, o último nó trocando calor com o ambiente por convecção.

O laço que fecha as duas: a resistência do cobre cresce com a temperatura,
``R(T) = R20 (1 + alfa (T - 20))``. Mais quente → mais perda → mais quente. É esse laço que
decide se um motor "de 7,5 kW" entrega 7,5 kW por uma hora ou por seis minutos.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------- máquina (por fase, ligação Y)

V_FASE = 230.0        # 400 V de linha em Y
POLOS = 4
F_REDE = 50.0
R_S20 = 0.85          # resistência do estator a 20 C [ohm]
R_R20 = 0.62          # resistência do rotor referida ao estator a 20 C [ohm]
X_S = 1.55
X_R = 1.55
X_M = 42.0
P_FERRO = 190.0       # perda no ferro, tomada constante e declarada [W]
P_MEC = 90.0          # perda mecânica [W]
ALFA_CU = 0.00393     # 1/K, coeficiente do cobre

N_S = 60.0 * F_REDE / (POLOS / 2)          # rpm síncrona
W_S = 2.0 * np.pi * N_S / 60.0             # rad/s mecânicos


def thevenin(t_estator=None):
    """Equivalente de Thévenin visto do rotor, com o ramo de magnetização."""
    r_s = R_S20 if t_estator is None else resistencia(R_S20, t_estator)
    z_s = r_s + 1j * X_S
    z_m = 1j * X_M
    v_th = V_FASE * z_m / (z_s + z_m)
    z_th = z_s * z_m / (z_s + z_m)
    return v_th, z_th


def resistencia(r20, temperatura):
    return r20 * (1.0 + ALFA_CU * (temperatura - 20.0))


def torque(s, t_estator=None, t_rotor=None):
    """Torque eletromagnético [N.m] para escorregamento s e temperaturas dos enrolamentos."""
    s = np.asarray(s, dtype=float)
    if np.any(s <= 0.0):
        s = np.maximum(s, 1e-12)
    v_th, z_th = thevenin(t_estator)
    r_r = R_R20 if t_rotor is None else resistencia(R_R20, t_rotor)
    r2 = r_r / s
    i2 = np.abs(v_th) / np.abs(z_th + r2 + 1j * X_R)
    p_ag = 3.0 * i2 ** 2 * r2
    return p_ag / W_S


def correntes(s, t_estator=None, t_rotor=None):
    """Corrente de estator e de rotor referida, em módulo."""
    r_s = R_S20 if t_estator is None else resistencia(R_S20, t_estator)
    r_r = R_R20 if t_rotor is None else resistencia(R_R20, t_rotor)
    z_m = 1j * X_M
    z_rotor = r_r / s + 1j * X_R
    z_par = z_m * z_rotor / (z_m + z_rotor)
    i1 = np.abs(V_FASE / (r_s + 1j * X_S + z_par))
    v_th, z_th = thevenin(t_estator)
    i2 = np.abs(v_th) / np.abs(z_th + r_r / s + 1j * X_R)
    return i1, i2


def perdas(s, t_estator=None, t_rotor=None):
    """Perdas em watts: cobre do estator, cobre do rotor, ferro e mecânicas."""
    i1, i2 = correntes(s, t_estator, t_rotor)
    r_s = R_S20 if t_estator is None else resistencia(R_S20, t_estator)
    r_r = R_R20 if t_rotor is None else resistencia(R_R20, t_rotor)
    return {"estator": float(3.0 * i1 ** 2 * r_s), "rotor": float(3.0 * i2 ** 2 * r_r),
            "ferro": P_FERRO, "mecanica": P_MEC}


def potencia_util(s, t_estator=None, t_rotor=None):
    return float(torque(s, t_estator, t_rotor) * W_S * (1.0 - s))


def escorregamento_de_carga(p_carga, t_estator=None, t_rotor=None):
    """Escorregamento que entrega a potência de eixo pedida (busca na faixa estável)."""
    from scipy.optimize import brentq
    alvo = lambda s: potencia_util(s, t_estator, t_rotor) - p_carga  # noqa: E731
    s_max = escorregamento_maximo(t_estator, t_rotor)
    if alvo(1e-4) >= 0:
        return 1e-4
    if alvo(s_max * 0.98) <= 0:
        raise ValueError("carga acima do torque máximo")
    return float(brentq(alvo, 1e-4, s_max * 0.98))


def escorregamento_maximo(t_estator=None, t_rotor=None):
    v_th, z_th = thevenin(t_estator)
    r_r = R_R20 if t_rotor is None else resistencia(R_R20, t_rotor)
    return float(r_r / np.hypot(np.real(z_th), np.imag(z_th) + X_R))


# ---------------------------------------------------------------- térmica

class RedeTermica:
    """Três nós: enrolamento (0), ferro (1), carcaça (2). Condutâncias e capacidades declaradas."""

    def __init__(self, c_enrol=3500.0, c_ferro=12000.0, c_carcaca=9000.0,
                 g_enrol_ferro=40.0, g_ferro_carcaca=60.0, g_carcaca_amb=25.0):
        self.c = np.array([c_enrol, c_ferro, c_carcaca])       # J/K
        self.g_ef = g_enrol_ferro
        self.g_fc = g_ferro_carcaca
        self.g_ca = g_carcaca_amb                              # W/K, é o resfriamento

    def derivada(self, t, temp, pot):
        """temp: [enrolamento, ferro, carcaça]; pot: [perda no enrol., perda no ferro]."""
        te, tf, tc = temp
        q_enrol, q_ferro = pot(t, temp) if callable(pot) else pot
        d_enrol = (q_enrol - self.g_ef * (te - tf)) / self.c[0]
        d_ferro = (q_ferro + self.g_ef * (te - tf) - self.g_fc * (tf - tc)) / self.c[1]
        d_carcaca = (self.g_fc * (tf - tc) - self.g_ca * (tc - 20.0)) / self.c[2]
        return [d_enrol, d_ferro, d_carcaca]

    def estavel(self, t_final=7200.0, dt=1.0, p_carga=7500.0, t_inicial=(20.0, 20.0, 20.0)):
        """Roda o acoplamento com **carga constante**.

        A carga é fixa, então o escorregamento não fica parado: ele é reencontrado a cada passo
        para a temperatura atual. Foi o erro da primeira versão deste modelo — com o
        escorregamento congelado, a potência entregue caía silenciosamente conforme o motor
        aquecia, e o laço térmico aparecia mais brando do que é.
        """
        tempos = np.arange(0.0, t_final + dt, dt)

        def campo(t, temp):
            try:
                s = escorregamento_de_carga(p_carga, temp[0], temp[1])
            except ValueError:                      # carga acima do torque máximo: o motor para
                s = escorregamento_maximo(temp[0], temp[1])
            perdas_ = perdas(s, t_estator=temp[0], t_rotor=temp[1])
            # do cobre do rotor, metade entra pelo enrolamento e metade pelo ferro
            return [perdas_["estator"] + 0.5 * perdas_["rotor"],
                    perdas_["ferro"] + 0.5 * perdas_["rotor"]]

        sol = solve_ivp(self.derivada, (0.0, t_final), list(t_inicial), t_eval=tempos,
                        args=(campo,), method="Radau", rtol=1e-8, atol=1e-8)
        return sol.t, sol.y

    def analitico_um_no(self, potencia, t_final=7200.0, dt=1.0, t_ambiente=20.0):
        """Rede reduzida a um nó: a solução é exponencial exata, e é a régua da rede de três nós."""
        c_total = float(self.c.sum())
        g_total = 1.0 / (1.0 / self.g_ef + 1.0 / self.g_fc + 1.0 / self.g_ca)
        tau = c_total / g_total
        d_inf = potencia / g_total
        t = np.arange(0.0, t_final + dt, dt)
        return t, t_ambiente + d_inf * (1.0 - np.exp(-t / tau)), tau, d_inf
