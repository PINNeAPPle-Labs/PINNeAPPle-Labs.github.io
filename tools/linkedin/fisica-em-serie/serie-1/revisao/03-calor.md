# 03 · Calor: campo certo e física violada são duas coisas

_The Physics Atlas · PINNeAPPle · carrossel 3 de 10_

## Slide 1 — capa
`The Physics Atlas · 03/10 · Calor`

**PT** — O campo está certo. E agora?
  Um dissipador, uma placa fria e um permutador em operação — cada um com o erro ao lado.
  `midia/term-twin.jpg`

**EN** — The field is right. Now what?
  A heat sink, a cold plate and an exchanger in operation — each with its error beside it.

## Slide 2 — dado
`Dimensionamento térmico`

**PT** — Sete geometrias de dissipador, um substituto
  227.059×
  mais rápido que o FEA 3-D, com 4,46% de erro médio e 7,35% no pior caso
  Sete geometrias resolvidas em FEniCS/dolfinx, malha em gmsh, e a comparação feita **em pontos que não estavam no treino**. A previsão é determinística: três rodadas, em dias diferentes, devolveram os mesmos números.
  artigos/substituto-termico
  `midia/term-heatsink.jpg`

**EN** — Seven heat-sink geometries, one surrogate
  227,059×
  faster than the 3-D FEA, at 4.46% mean error and 7.35% worst case
  Seven geometries solved in FEniCS/dolfinx, meshed in gmsh, compared **at points that were not in the training set**. The prediction is deterministic: three runs, on different days, returned the same numbers.
  artigos/substituto-termico

## Slide 3 — media
`O substituto acerta`

**PT** — 1,7% de erro em 50 layouts de placa fria
  FNO2d com 1,18 milhão de parâmetros, treinado em 133 s. Erro relativo L2 de **1,7%** fora do treino e o ponto quente errando no máximo **0,24 K**. E 1,5 vez mais rápido que o volumes finitos — não mil vezes.
  artigos/fno-placa-fria
  [SURROGATE]
  `midia/term-fno-campos.webp`

**EN** — 1.7% error across 50 cold-plate layouts
  An FNO2d with 1.18 million parameters, trained in 133 s. Relative L2 error of **1.7%** out of training, with the hotspot erring by at most **0.24 K**. And 1.5 times faster than finite volumes — not a thousand.
  artigos/fno-placa-fria

## Slide 4 — media
`E o cartão diz não`

**PT** — Resíduo de PDE: 0,164 contra o limite de 0,1
  Decisão: **REJECT**. Acertar o campo de referência e satisfazer a equação são duas coisas diferentes, e a segunda é a que decide se o resultado entra num projeto. Passaram a condição de contorno e a positividade — as duas mais fáceis.
  artigos/fno-placa-fria
  [SURROGATE]
  `midia/term-fno-checagens.webp`

**EN** — PDE residual: 0.164 against the 0.1 limit
  Decision: **REJECT**. Matching the reference field and satisfying the equation are two different things, and the second decides whether the result enters a design. The boundary condition and positivity checks passed — the two easy ones.
  artigos/fno-placa-fria

## Slide 5 — media
`Do solver para a planta`

**PT** — Um permutador que avisou 2,6 horas antes
  Gêmeo do HX-201 ajustado só com o histórico anterior à janela de validação, com uma sonda redundante fora do ajuste servindo de juiz: **0,216 °C** de erro e 95,5% de cobertura da banda.
  artigos/gemeo-hx201
  [SURROGATE]
  `midia/term-twin.jpg`

**EN** — An exchanger that warned 2.6 hours ahead
  The HX-201 twin was fitted only on history before the validation window, with a redundant probe kept out of the fit as judge: **0.216 °C** of error and 95.5% band coverage.
  artigos/gemeo-hx201

## Slide 6 — media
`No Studio`

**PT** — "Dissipador de aletas para 60 W"
  A frase entra em português comum; sai o valor, as verificações uma por uma com valor e limite, a versão do código e o hash de cada arquivo. Se o seu caso cai fora da faixa validada, a resposta é essa — e não um campo colorido.
  PINNeAPPle Studio · dimensionamento térmico
  [STUDIO]
  `midia/term-studio.jpg`

**EN** — "Fin heatsink for 60 W"
  The sentence goes in plain language; out comes the value, the checks one by one with value and limit, the code version and the hash of every file. If your case falls outside the validated range, that is the answer — not a colourful field.
  PINNeAPPle Studio · thermal sizing

## Slide 7 — media
`Onde o erro não é o critério`

**PT** — CO₂ perto do ponto crítico
  A rede direta é **16× mais precisa** e viola a identidade de c_v em **1.100%**. A rede de potencial erra mais e mantém as seis identidades abaixo de 0,0021%. Para alimentar um solver de CFD, quem serve é a segunda.
  artigos/co2-supercritico
  [SURROGATE]
  `midia/term-co2.webp`

**EN** — CO₂ near the critical point
  The direct network is **16× more accurate** and violates the c_v identity by **1,100%**. The potential network errs more and keeps all six identities below 0.0021%. To feed a CFD solver, the second one is the one that serves.
  artigos/co2-supercritico

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - O alvo do CO₂ é uma equação de estado (Span & Wagner), não um ensaio: mede-se fidelidade ao modelo de referência.
  - 4,46% é a média dentro da faixa treinada; fora dela, o erro não está medido. Determinismo não é acerto.
  - A antecedência de 2,6 h vem de uma extrapolação linear, com o erro reportado.

**EN** — What this carousel is not saying
  - The CO₂ target is an equation of state (Span & Wagner), not a test: what is measured is fidelity to the reference model.
  - 4.46% is the mean inside the trained range; outside it, the error is unmeasured. Determinism is not accuracy.
  - The 2.6 h lead comes from a linear extrapolation, with the error reported.
