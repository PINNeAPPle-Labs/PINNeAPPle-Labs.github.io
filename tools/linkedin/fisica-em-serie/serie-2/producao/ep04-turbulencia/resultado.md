# EP 04 · resultado medido

Rajada 1-cosine de 7.62 m/s (25 ft/s), 2H = 100 m, a 3000 m, comando fixo, quatro aeronaves do catálogo, cada uma na sua velocidade de encontro.

| aeronave | V [m/s] | pico Δn_z | quase-estacionário | Pratt | erro do quase | erro do Pratt |
|---|---|---|---|---|---|---|
| light_ga | 55 | +0.625 | 1.463 | 1.014 | +134.1% | +62.3% |
| regional_turboprop | 120 | +0.571 | 0.644 | 0.523 | +12.9% | -8.3% |
| a320 | 128 | +0.357 | 0.396 | 0.321 | +11.1% | -9.9% |
| motor_glider | 40 | +0.939 | 1.883 | 1.297 | +100.4% | +38.1% |

## O que isso verifica, e o que isso desmente

As duas fórmulas fechadas são de engenharia, e não do modelo: a quase-estacionária usa aerodinâmica de asa em regime permanente, e Pratt acrescenta o fator de atenuação K_g.

Nas aeronaves mais pesadas (regional_turboprop, a320) as três rotas concordam dentro de 13%: o solver reproduz o que a fórmula fechada prevê, e é isso que dá lastro ao número.

Nas mais leves (light_ga, motor_glider) elas **não** concordam — o quase-estacionário chega a +134% acima do pico medido. Não é erro do solver: é o limite da fórmula quase-estacionária, que ignora o atraso da sustentação e a dinâmica de corpo curto. Fica publicado assim.

O que isso significa na prática: para a aeronave pesada, qualquer uma das três serve; para a leve, só o solver.

## O que não está medido

- Rajada discreta idealizada: não é atmosfera real medida em voo.
- Comando fixo, sem piloto e sem autopiloto nesta rodada.
- Nenhuma comparação com dado de voo: o que se verifica é o solver contra fórmulas fechadas.
