# 09 · Debaixo do chão e acima do clima: escalas que não cabem numa bancada

_The Physics Atlas · PINNeAPPle · carrossel 9 de 10_

## Slide 1 — capa
`The Physics Atlas · 09/10 · Geofísica`

**PT** — O reservatório não cabe numa bancada.
  Reservatório, aquífero, clima e solo: as escalas em que a validação tem de ser feita contra dado, não contra intuição.
  `midia/geo-simr.jpg`

**EN** — The reservoir does not fit on a bench.
  Reservoir, aquifer, climate and soil: the scales where validation has to be against data, not against intuition.

## Slide 2 — media
`Escala de campo`

**PT** — Reservatório: Darcy em quilômetros
  Escoamento em meio poroso resolvido com um solver de reservatório aberto (OPM Flow), sobre os decks públicos do SPE10. É o caso em que a permissão de publicação passa por citar o dado de entrada, não por desenhar um campo.
  PINNeAPPle-SimR · OPM Flow · SPE10
  [SOLVER]
  `midia/geo-simr.jpg`

**EN** — Reservoir: Darcy across kilometres
  Porous-media flow solved with an open reservoir simulator (OPM Flow), on the public SPE10 decks. It is the case where the licence to publish runs through citing the input data, not through drawing a field.
  PINNeAPPle-SimR · OPM Flow · SPE10

## Slide 3 — media
`Escala de poro`

**PT** — O que o Darcy não vê
  Lattice-Boltzmann em torno de esferas: a permeabilidade não é um parâmetro do problema, é o resultado dele. É assim que uma propriedade de entrada de reservatório pode ser conferida em vez de assumida.
  [SOLVER]
  `midia/geo-lbm.png`

**EN** — What Darcy does not see
  Lattice-Boltzmann around spheres: permeability is not a parameter of the problem, it is its result. That is how a reservoir input property can be checked instead of assumed.

## Slide 4 — dado
`Clima como problema de comparação`

**PT** — 28 modelos, uma régua só
  0,42
  de correlação de anomalia a 24 meses — contra 0,33 do AR e 0 da climatologia
  Cinco famílias, os mesmos dados (OISST v2.1), a mesma janela e a mesma regra de significância. Ganha um oscilador físico de 15 parâmetros. As PINNs construídas sobre ele ficam em **−0,69** onde ele fica em 0,80.
  artigos/el-nino-28-modelos
  `midia/geo-nino.webp`

**EN** — 28 models, one yardstick
  0.42
  anomaly correlation at 24 months — against 0.33 for AR and 0 for climatology
  Five families, the same data (OISST v2.1), the same window and the same significance rule. A 15-parameter physical oscillator wins. The PINNs built on top of it sit at **−0.69** where it sits at 0.80.
  artigos/el-nino-28-modelos

## Slide 5 — media
`Campo atmosférico`

**PT** — Ondas de calor como campo previsto
  Altura geopotencial em 500 hPa num evento de calor extremo. A pergunta não é se o campo é plausível, é contra qual análise ele foi comparado e com que habilidade — a mesma régua do ranking do El Niño.
  PINNeAPPle · examples/weather_forecasting
  [SURROGATE]
  `midia/geo-heatdome.png`

**EN** — Heat waves as a forecast field
  500 hPa geopotential height during an extreme heat event. The question is not whether the field is plausible, but what analysis it was compared against and with what skill — the same yardstick as the El Niño ranking.
  PINNeAPPle · examples/weather_forecasting

## Slide 6 — media
`Solo e geotecnia`

**PT** — Quando o material é o próprio risco
  O mesmo DEM do carrossel de partículas, aqui como problema geotécnico: colapso, ângulo de repouso e alcance final. É o tipo de caso em que a simulação serve para delimitar cenário, não para prever o evento.
  [SOLVER]
  `midia/mf-coluna.png`

**EN** — When the material is the risk itself
  The same DEM as in the particles carousel, here as a geotechnical problem: collapse, angle of repose and final run-out. It is the kind of case where simulation bounds a scenario instead of predicting the event.

## Slide 7 — texto
`A regra desta área`

**PT** — Onde não existe verdade, existe protocolo
  - Reservatório e clima não têm solução analítica: a régua passa a ser o dado observado, a janela fixa e a significância declarada.
  - O solver se confere antes contra o que tem resposta: a onda de Kelvin viaja a **2,689 m/s** contra 2,7 m/s da teoria.
  - Modelo que perde é publicado perdendo: é o que permite escolher com orçamento em vez de entusiasmo.

**EN** — Where there is no truth, there is protocol
  - Reservoir and climate have no analytical solution: the yardstick becomes observed data, a fixed window and declared significance.
  - The solver is checked first against what has an answer: the Kelvin wave travels at **2.689 m/s** against 2.7 m/s from theory.
  - A model that loses is published losing: that is what lets the choice be made with a budget instead of with enthusiasm.

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - A avaliação do El Niño é retrospectiva, com splits fixos: não é previsão operacional.
  - Não há resultado de migração de CO₂ em reservatório real medido aqui — há o caso, o solver e o caminho para medi-lo.
  - Geomecânica é modelo constitutivo escolhido; solo real tem variabilidade que nenhum modelo de 15 parâmetros carrega.

**EN** — What this carousel is not saying
  - The El Niño evaluation is retrospective, with fixed splits: it is not an operational forecast.
  - There is no measured CO₂ migration result in a real reservoir here — there is the case, the solver and the path to measuring it.
  - Geomechanics is a chosen constitutive model; real soil carries variability no 15-parameter model holds.
