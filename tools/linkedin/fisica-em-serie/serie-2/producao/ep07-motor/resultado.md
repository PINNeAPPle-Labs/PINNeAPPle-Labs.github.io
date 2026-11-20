# EP 07 · resultado medido

Motor de indução de 4 polos, 400 V em Y, 50 Hz, com o circuito equivalente declarado (R_s = 0,85 Ω, R_r' = 0,62 Ω a 20 °C, X = 1,55 Ω, X_m = 42,0 Ω) acoplado a uma rede térmica de três nós (enrolamento, ferro, carcaça). Carga fixa de 7,5 kW no eixo. O cobre tem α = 0,00393 1/K.

- ponto nominal: escorregamento **3,70%** (1445 rpm), torque 49,6 N·m
- perdas: estator 487 W, rotor 288 W, ferro 190 W, mecânica 90 W → **1055 W** (eficiência 87,7%)

## Verificações

1. **limite de um nó** contra a exponencial exata (τ = 51,0 min): erro máximo de **0,00 K**
1b. **rede de três nós** com perda constante contra a soma das resistências térmicas: 81,67 K medidos contra 81,67 K analíticos (**0,000 K**)
2. **balanço de energia** na rodada de projeto: entraram 4,74 kWh, ficaram guardados 0,311 kWh e saíram 4,43 kWh → **0,00%** de erro
3. **transiente contra o algébrico**: ao fim das 4 h a integração está em 90,80 °C e a raiz do sistema não linear em 90,80 °C → **0,00 K** de diferença

## O que o acoplamento faz

| resfriamento | carcaça→ambiente | enrolamento em 4 h | limite de 155 °C |
|---|---|---|---|
| 100% | 40,0 W/K | 91 °C | não atinge |
| 60% | 24,0 W/K | 120 °C | não atinge |
| 40% | 16,0 W/K | 166 °C | 112 min |
| 25% | 10,0 W/K | em fuga | 59 min |

**Resfriamento crítico: 10,3 W/K** — abaixo disso a equação de equilíbrio não tem solução: cada grau a mais aumenta a perda mais rápido do que aumenta a dissipação, e a temperatura não para.

Com o ventilador funcionando (40 W/K) o enrolamento estabiliza perto de 90 °C. Com 25% do resfriamento, a mesma carga leva o enrolamento ao limite da classe F e a perda de cobre já cresceu — porque a resistência subiu e o escorregamento também, para entregar o mesmo torque.

## O que este resultado é

Um acoplamento declarado entre dois modelos clássicos: circuito equivalente do motor de indução e rede térmica concentrada, com o laço R(T) fechado e a carga mantida constante durante toda a rodada.

## O que este resultado não é

- **Não é FEA eletromagnética**: não há campo no entreferro, saturação, harmônicos nem perdas no ferro calculadas — elas entram como constante declarada.
- Não há ventilador modelado: o resfriamento entra como uma condutância global.
- Não há degradação do isolamento: a classe F é um limite de temperatura, não um modelo de vida útil.
- Os parâmetros do circuito são de um motor plausível, não de uma máquina caracterizada nesta casa.
