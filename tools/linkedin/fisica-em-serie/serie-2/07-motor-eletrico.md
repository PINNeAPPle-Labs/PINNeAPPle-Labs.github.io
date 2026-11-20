# EP 07 · O que acontece dentro de um motor elétrico

**Duração** 22 s · **Estado** produzido — `midia/ep07-motor.mp4` · **Base** `producao/motor.py` (circuito equivalente + rede térmica), `producao/ep07-motor/resultado.md`, `artigos/motor-prius-dois-solvers`

## O que o vídeo prova

Que a perda de um motor não é um número fixo: ela depende da temperatura, e a temperatura depende
da perda. Esse laço é o que decide se um motor "de 7,5 kW" entrega os 7,5 kW por uma hora ou por
seis minutos — e o vídeo mostra o laço fechado, com o ponto em que ele deixa de ter solução.

## Por que é o episódio comercial da série

Motor elétrico é o caso multifísico que a indústria compra: mobilidade, bombas, ventiladores,
compressores. E é o tipo de pergunta que chega como orçamento: *"meu motor está aquecendo, o
problema é o motor ou é a ventilação?"* — pergunta que só se responde com os dois modelos juntos.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–4 s | Curva torque × escorregamento em três temperaturas | `20 / 90 / 140 °C` | "A mesma máquina, três temperaturas. A curva de torque não é a mesma, porque a resistência do cobre não é a mesma." |
| 4–9 s | Barra de perdas: estator, rotor, ferro, mecânica | `1.055 W` | "No ponto nominal, mil e cinquenta e cinco watts viram calor. É esse número que o projeto térmico tem de dissipar." |
| 9–15 s | Temperatura do enrolamento subindo, ventilador degradado | `100% → 25%` | "Com o ventilador funcionando, o enrolamento estabiliza perto de noventa graus. Com um quarto do resfriamento, não estabiliza." |
| 15–19 s | A curva que não achata | `sem regime permanente` | "Abaixo de dez vírgula três watts por kelvin não existe equilíbrio: cada grau a mais aumenta a perda mais rápido do que aumenta a dissipação." |
| 19–22 s | Checagens: um nó, três nós, balanço de energia | `verificação` | "E a checagem que fecha: o balanço de energia tem de fechar e a rede tem de reproduzir o caso analítico. Fecha em zero vírgula zero por cento." |

## Resultado medido

Motor de indução de 4 polos, 400 V em Y, 50 Hz, circuito equivalente declarado, acoplado a uma
rede térmica de três nós (enrolamento, ferro, carcaça). Carga fixa de 7,5 kW no eixo; o
escorregamento é **reencontrado a cada passo** para a temperatura atual, porque com carga
constante ele não fica parado.

| régua | resultado |
|---|---|
| limite de um nó contra a exponencial exata | erro máximo **0,00 K** |
| rede de três nós contra a soma das resistências térmicas | 81,67 K medidos contra 81,67 K analíticos |
| balanço de energia na rodada de projeto | **0,00%** (4,74 kWh entraram, 0,31 ficaram, 4,43 saíram) |
| transiente contra a solução algébrica do regime | **0,00 K** de diferença |

| resfriamento | enrolamento em 4 h | limite de 155 °C (classe F) |
|---|---|---|
| 100% (40 W/K) | 91 °C | não atinge |
| 60% (24 W/K) | 120 °C | não atinge |
| 40% (16 W/K) | 167 °C | 112 min |
| 25% (10 W/K) | em fuga | 59 min |

**Resfriamento crítico: 10,3 W/K.** Abaixo disso a equação de equilíbrio não tem solução.

## O que o vídeo não deve afirmar

- Que é FEA eletromagnética: não há campo no entreferro, saturação nem harmônicos. As perdas no
  ferro entram como constante declarada.
- Que há ventilador modelado: o resfriamento é uma condutância global.
- Que a classe F é um modelo de vida útil: é um limite de temperatura.
- Que estes parâmetros são de um motor caracterizado nesta casa: são de um motor plausível.
- Que o campo magnético de um motor real não é medido aqui — ele é, em outro material
  (`artigos/motor-prius-dois-solvers`, 0,19% contra GetDP), e este episódio não repete aquilo.

## Legenda (PT)

Motor elétrico é onde a multifísica deixa de ser exercício e vira orçamento: perda vira calor, calor vira mais perda, e o cliente pergunta por que o motor queimou.

O laço é esse: a resistência do cobre cresce com a temperatura, a perda cresce com a resistência, e com carga fixa o escorregamento também sobe — porque o motor precisa entregar o mesmo torque.

Medido: com o ventilador funcionando, o enrolamento estabiliza em 91 °C. Com 40% do resfriamento, chega a 155 °C em 112 minutos. Com 25%, não estabiliza nunca: abaixo de 10,3 W/K a equação de equilíbrio simplesmente não tem solução.

O balanço de energia fecha em 0,00%, a rede térmica reproduz o caso analítico, e o transiente bate com a solução algébrica. Não há FEA eletromagnética aqui — e isso está escrito no documento.

Link do artigo no primeiro comentário.

`#MobilidadeElétrica #Simulação #PhysicsAI #TransferênciaDeCalor #Multifísica`

## Legenda (EN)

Electric motors are where multiphysics stops being an exercise and becomes a quote: loss becomes heat, heat becomes more loss, and the client asks why the motor burned.

The loop is this: copper resistance grows with temperature, loss grows with resistance, and at constant load the slip grows too — because the motor still has to deliver the same torque.

Measured: with the fan working, the winding settles at 91 °C. At 40% of the cooling it reaches 155 °C in 112 minutes. At 25% it never settles: below 10.3 W/K the equilibrium equation simply has no solution.

The energy balance closes to 0.00%, the thermal network reproduces the analytic case, and the transient matches the algebraic solution. There is no electromagnetic FEA here — and the document says so.

Link to the article in the first comment.

`#ElectricMobility #Simulation #PhysicsAI #HeatTransfer #Multiphysics`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-2/midia/ep07-motor.mp4` | `producao/ep07-motor/gerar.py` | **produzido** |
| `serie-2/midia/ep07-motor-poster.jpg` | idem | **produzido** |
| `serie-1/midia/em-motor-campo.webp` | `img/exp/motor-campo.webp` | existe (outro episódio, não entra) |
| `serie-1/midia/em-afpm.png` | Studio, máquina de fluxo axial | existe (não entra) |
