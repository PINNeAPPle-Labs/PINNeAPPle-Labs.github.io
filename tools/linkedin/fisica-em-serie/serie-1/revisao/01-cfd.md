# 01 · Do carro de corrida à asa otimizada: o que a plataforma resolve em CFD

_The Physics Atlas · PINNeAPPle · carrossel 1 de 10_

## Slide 1 — capa
`The Physics Atlas · 01/10 · CFD`

**PT** — Do carro de corrida à asa otimizada.
  Sete resultados de CFD, cada um com o número e o limite ao lado.
  `midia/cfd-f1-beauty.jpg`

**EN** — From the race car to the optimised wing.
  Seven CFD results, each with its number and its limit beside it.

## Slide 2 — media
`O ponto de partida`

**PT** — Antes do carro, o corpo de Ahmed
  O caso de referência que todo solver de CFD precisa reproduzir antes de encarar uma geometria de verdade: linhas de corrente em 3-D, malha própria, sem ajuste para ficar bonito.
  OpenFOAM · corpo de Ahmed
  [SOLVER]
  `midia/cfd-ahmed-streamlines.jpg`

**EN** — Before the car, the Ahmed body
  The reference case every CFD solver has to reproduce before facing a real geometry: 3-D streamlines, our own mesh, no tuning to look good.
  OpenFOAM · Ahmed body

## Slide 3 — media
`De onde vem o arrasto`

**PT** — Vorticidade na esteira
  Vórtices de ponta de asa e o rastro das rodas. É isto que o arrasto medido está enxergando — e é por isto que mudar a asa muda o número.
  OpenFOAM 3-D · carro de corrida paramétrico
  [SOLVER]
  `midia/cfd-f1-wake.jpg`

**EN** — Vorticity in the wake
  Wing-tip vortices and the wheel wake. This is what the measured drag is looking at — and why changing the wing changes the number.
  3-D OpenFOAM · parametric race car

## Slide 4 — dado
`Otimização com orçamento`

**PT** — 20 simulações, 3,3 horas, um número
  −15,7%
  de arrasto — com o downforce acima do piso de 7 kN
  Vinte rodadas de OpenFOAM 3-D, cada uma escolhida por um critério de incerteza registrado. O mesmo desenho, na malha fina, dá **−13,9%**: é esse o número honesto, porque a malha da campanha subestima o downforce em 8,4%.
  artigos/aerodinamica-autonoma
  `midia/cfd-aero-pareto.webp`

**EN** — 20 simulations, 3.3 hours, one number
  −15.7%
  of drag — with downforce above the 7 kN floor
  Twenty 3-D OpenFOAM runs, each chosen by a recorded uncertainty criterion. The same design on the fine mesh gives **−13.9%**: that is the honest number, because the campaign mesh under-predicts downforce by 8.4%.
  artigos/aerodinamica-autonoma

## Slide 5 — media
`A outra ponta`

**PT** — 1.920 asas, e o resultado não é uma asa
  Pressão na pele em OpenFOAM 3-D, um dos 1.920 projetos avaliados. A saída é um mapa de trocas: **−13% de CO₂ por passageiro-quilômetro**, com a sustentação-alvo mantida dentro de 0,04%. Quem escolhe o ponto do mapa é a engenharia.
  artigos/asa-1920-projetos
  [SOLVER]
  `midia/cfd-asa-pressure.jpg`

**EN** — 1,920 wings, and the answer is not a wing
  Skin pressure in 3-D OpenFOAM, one of the 1,920 designs evaluated. The output is a trade-off map: **−13% CO₂ per passenger-kilometre**, with target lift held to within 0.04%. Engineering picks the point on the map.
  artigos/asa-1920-projetos

## Slide 6 — texto
`Como a plataforma trabalha`

**PT** — Quatro etapas, e uma delas é recusar
  É o passo 3 que muda a economia: o candidato fora do domínio é recusado _antes_ de gastar solver.
  - **Geometria e caso** — paramétrico, com a faixa de validade declarada antes de rodar.
  - **Solver de referência** — OpenFOAM, a resposta que continua sendo a régua.
  - **Substituto com incerteza** — e um veredito por candidato: favorável, incerto ou fora de domínio.
  - **Verificação** — conservação, malha e convergência conferidas uma a uma, com valor e limite.

**EN** — Four steps, and one of them is refusing
  Step 3 is what changes the economics: a candidate out of domain is refused _before_ any solver time is spent.
  - **Geometry and case** — parametric, with its validity range declared before the run.
  - **Reference solver** — OpenFOAM, still the yardstick.
  - **Surrogate with uncertainty** — and a verdict per candidate: favourable, uncertain or out of domain.
  - **Verification** — conservation, mesh and convergence checked one by one, with value and limit.

## Slide 7 — media
`O mesmo pipeline, com partículas`

**PT** — Erosão numa curva de 90°
  Ar com areia a 15 m/s. O resultado ficou entre **1,05 e 1,49 vez** a taxa medida no ensaio aberto de Vieira et al. (2016) — dentro do fator 2 que a indústria aceita, e dito assim em voz alta.
  artigos/erosao-curva-90
  [EXPERIMENTO]
  `midia/cfd-erosao.jpg`

**EN** — Erosion in a 90° bend
  Sand-laden air at 15 m/s. The result landed between **1.05 and 1.49 times** the rate measured in the open experiment by Vieira et al. (2016) — inside the factor-2 band industry accepts, and said out loud.
  artigos/erosao-curva-90

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - Não há túnel de vento nesta comparação: o ganho é medido contra o próprio baseline, no mesmo solver.
  - O substituto erra 2,4% no arrasto e 10,2% no downforce em validação cruzada — e fora da faixa geométrica validada não vale.
  - Erosão é fator 2, não precisão de 1%: o fenômeno não entrega isso.

**EN** — What this carousel is not saying
  - There is no wind tunnel in this comparison: the gain is measured against its own baseline, in the same solver.
  - The surrogate errs 2.4% in drag and 10.2% in downforce under cross-validation — and outside the validated geometry range it does not hold.
  - Erosion is factor 2, not 1% precision: the phenomenon does not deliver that.
