# 05 · Milhares de partículas: onde a mistura não é a fase

_The Physics Atlas · PINNeAPPle · carrossel 5 de 10_

## Slide 1 — capa
`The Physics Atlas · 05/10 · Partículas`

**PT** — Milhares de partículas. Física simples. Contas honestas.
  O que é multifásico de verdade nesta plataforma, e o que é transporte — a diferença importa.
  `midia/mf-stirred.jpg`

**EN** — Thousands of particles. Simple physics. Honest accounting.
  What is genuinely multiphase on this platform, and what is transport — the difference matters.

## Slide 2 — media
`Discreto, partícula por partícula`

**PT** — Tanque agitado: cada partícula é resolvida
  DEM puro: colisão, atrito e contato resolvidos para cada partícula. É o caso em que a física discreta aparece inteira — e o custo cresce com o número de partículas, não com o refinamento da malha.
  PINNeAPPle · examples/granular_dem
  [SOLVER]
  `midia/mf-stirred.jpg`

**EN** — Stirred tank: every particle is solved
  Pure DEM: collision, friction and contact solved for every particle. It is the case where discrete physics shows itself whole — and the cost grows with the particle count, not the mesh refinement.
  PINNeAPPle · examples/granular_dem

## Slide 3 — media
`Colapso granular`

**PT** — Uma coluna que desaba
  O experimento clássico de coluna granular: solta-se a lateral, a coluna desaba e o raio final depende do aspecto inicial. É o análogo granular do que se vê num vídeo de barragem — e é **granular**, não água.
  PINNeAPPle · examples/geomechanics
  [SOLVER]
  `midia/mf-coluna.png`

**EN** — A column that comes down
  The classic granular-column experiment: release the side, the column collapses and the final run-out depends on the initial aspect ratio. It is the granular analogue of what a dam video shows — and it is **granular**, not water.
  PINNeAPPle · examples/geomechanics

## Slide 4 — media
`Mistura não é fase`

**PT** — Kenics: linhas de corrente
  O misturador estático Kenics mostra transporte e mistura de concentração num escoamento único. É um resultado de **advecção e mistura**, não de duas fases — e chamar de multifásico seria inflar o que está medido.
  PINNeAPPle · flow_studio
  [SOLVER]
  `midia/mf-kenics-linhas.jpg`

**EN** — Kenics: streamlines
  The Kenics static mixer shows transport and concentration mixing in a single-phase flow. It is a result of **advection and mixing**, not of two phases — and calling it multiphase would inflate what is measured.
  PINNeAPPle · flow_studio

## Slide 5 — media
`O que a mistura faz`

**PT** — Estriações de concentração
  As faixas são a assinatura do misturador: cada elemento divide e gira o escoamento, e o que entra separado sai estratificado em escalas cada vez menores.
  [SOLVER]
  `midia/mf-kenics-faixas.png`

**EN** — Concentration striations
  The striations are the mixer's signature: each element splits and twists the flow, and what enters separate leaves stratified at ever smaller scales.

## Slide 6 — media
`Acoplamento de verdade`

**PT** — Fluido + partícula + parede
  Aqui as três coisas interagem: o escoamento carrega a areia, a areia bate na parede, a parede perde material. O resultado ficou entre **1,05 e 1,49 vez** o ensaio de Vieira et al. (2016).
  artigos/erosao-curva-90
  [EXPERIMENTO]
  `midia/cfd-erosao.jpg`

**EN** — Fluid + particle + wall
  Here all three interact: the flow carries the sand, the sand hits the wall, the wall loses material. The result landed between **1.05 and 1.49 times** the Vieira et al. (2016) experiment.
  artigos/erosao-curva-90

## Slide 7 — media
`Superfície livre`

**PT** — A onda que corre sobre o declive
  Escoamento com superfície livre: a frente de onda, o run-up e a lâmina que sobra depois que ela passa. É a base do que um caso de barragem exigiria — com uma parede a menos.
  PINNeAPPle · examples/free_surface
  [SOLVER]
  `midia/mf-free-surface.png`

**EN** — The wave that runs up the slope
  Free-surface flow: the wave front, the run-up and the film that stays after it passes. It is the basis a dam case would need — with one wall fewer.
  PINNeAPPle · examples/free_surface

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - Tanque DEM é partícula; Kenics é mistura de uma fase; erosão é fluido-partícula-parede. Três coisas, três nomes.
  - Não há resultado bifásico gás-líquido medido nesta casa — e não vamos chamar o Kenics de bifásico para fechar a lista.
  - Erosão é fator 2 de tolerância, não precisão de 1%.

**EN** — What this carousel is not saying
  - The DEM tank is particles; Kenics is single-phase mixing; erosion is fluid-particle-wall. Three things, three names.
  - There is no measured gas-liquid two-phase result here — and we will not call Kenics two-phase to round out the list.
  - Erosion carries a factor-2 tolerance, not 1% precision.
