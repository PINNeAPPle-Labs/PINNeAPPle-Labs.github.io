# 04 · Dois solvers concordam, e os dois discordam do artigo

_The Physics Atlas · PINNeAPPle · carrossel 4 de 10_

## Slide 1 — capa
`The Physics Atlas · 04/10 · Eletromagnetismo`

**PT** — Quando dois códigos concordam.
  O motor do Prius resolvido pela FEM da casa e por um solver independente, em 12 posições de rotor.
  `midia/em-motor-campo.webp`

**EN** — When two codes agree.
  The Prius motor solved by our own FEM and by an independent solver, at 12 rotor positions.

## Slide 2 — media
`O caso`

**PT** — |B| e linhas de fluxo no quarto de máquina
  Geometria do motor do Prius 2010, um dos benchmarks abertos mais usados em máquinas elétricas. Magnetostática 2-D, rotor na posição de máximo torque por ampère, 250 A.
  artigos/motor-prius-dois-solvers
  [SOLVER]
  `midia/em-motor-campo.webp`

**EN** — |B| and flux lines in the quarter machine
  The geometry of the 2010 Prius motor, one of the most used open benchmarks in electrical machines. 2-D magnetostatics, rotor at the maximum-torque-per-ampere position, 250 A.
  artigos/motor-prius-dois-solvers

## Slide 3 — dado
`A concordância`

**PT** — Duas implementações, mesmas 12 posições
  0,19%
  de diferença máxima de torque contra o GetDP, com RMS de 0,81 N·m
  A força contra-eletromotriz a 1000 rpm bate em 87,60 V contra 87,64 V no fundamental. Onde os dois mais se afastam é o ripple de cogging: 1,35 contra 1,05 N·m.
  artigos/motor-prius-dois-solvers
  `midia/em-motor-getdp.webp`

**EN** — Two implementations, the same 12 positions
  0.19%
  maximum torque difference against GetDP, with an RMS of 0.81 N·m
  Back-EMF at 1000 rpm matches at 87.60 V against 87.64 V in the fundamental. Where they differ most is cogging ripple: 1.35 against 1.05 N·m.
  artigos/motor-prius-dois-solvers

## Slide 4 — texto
`Contra o artigo publicado`

**PT** — Aqui o resultado incomoda — e é isso que ele serve para dizer
  - Contra a curva do artigo, o RMS é de **13,3 N·m** na FEM da casa e **12,9 N·m** no GetDP.
  - Os dois se afastam do paper pela mesma ordem — e não um do outro.
  - Conclusão: o desvio é do **modelo** (geometria, materiais, hipótese 2-D), não da implementação. Um número que concorda com o paper esconde onde olhar; dois que concordam entre si apontam.

**EN** — Here the result is uncomfortable — and that is what it is for
  - Against the paper's curve, the RMS is **13.3 N·m** for our FEM and **12.9 N·m** for GetDP.
  - Both drift from the paper by the same order — not from each other.
  - Conclusion: the deviation belongs to the **model** (geometry, materials, the 2-D assumption), not the implementation. A number that agrees with the paper hides where to look; two that agree with each other point at it.

## Slide 5 — media
`Além da máquina`

**PT** — Seis problemas com solução exata
  Capacitor de placas paralelas, Poisson com carga, dipolo, fio infinito, onda plana e o modo TM de uma cavidade — cada um resolvido por PINN **com a solução analítica ao lado**. É a forma mais barata de descobrir se o método está implementado certo antes de aplicá-lo a algo sem resposta conhecida.
  PINNeAPPle · examples/electrodynamics
  [SOLVER]
  `midia/em-prius-demag.png`

**EN** — Six problems with an exact solution
  Parallel-plate capacitor, Poisson with charge, dipole, infinite wire, plane wave and the TM mode of a cavity — each solved by a PINN **with the analytical solution beside it**. It is the cheapest way to find out whether the method is implemented correctly before applying it to something without a known answer.
  PINNeAPPle · examples/electrodynamics

## Slide 6 — media
`No Studio`

**PT** — Máquina de fluxo axial, do formulário ao campo
  Estimativa, campo em vista 3-D e verificação na mesma tela: o mesmo critério de sempre, aplicado a uma máquina que não é a do benchmark.
  PINNeAPPle Studio · afpm designer
  [STUDIO]
  `midia/em-afpm.png`

**EN** — Axial-flux machine, from form to field
  Estimate, field in 3-D view and verification on the same screen: the same criterion as always, applied to a machine that is not the benchmark's.
  PINNeAPPle Studio · AFPM designer

## Slide 7 — texto
`O limite desta área`

**PT** — O que é 2-D e o que fica de fora
  - Efeitos de ponta, skew e perdas **não entram** nesta comparação.
  - Concordância entre dois solvers mede consistência numérica — não acerto contra ensaio.
  - A área de antenas existe no repositório (padrões, guias, Vivaldi), mas ainda não tem carrossel com resultado medido: preferimos não publicar o que não medimos.

**EN** — What is 2-D, and what stays out
  - End effects, skew and losses are **not** in this comparison.
  - Agreement between two solvers measures numerical consistency — not accuracy against a test.
  - The antenna area exists in the repository (patterns, guides, Vivaldi), but it has no carousel with a measured result yet: we would rather not publish what we have not measured.

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - Não há ensaio de bancada nesta comparação: dois códigos concordando não é a mesma coisa que dois códigos certos.
  - O desvio de ~13 N·m contra o paper é do modelo — e o modelo é uma hipótese que alguém escolheu.
  - Magnetostática não é motor completo: falta térmico, perdas e a parte estrutural.

**EN** — What this carousel is not saying
  - There is no bench test in this comparison: two codes agreeing is not the same as two codes being right.
  - The ~13 N·m drift against the paper belongs to the model — and the model is a hypothesis someone chose.
  - Magnetostatics is not a complete motor: thermal, losses and the structural side are missing.
