# 08 · Do átomo ao componente: três escalas de material

_The Physics Atlas · PINNeAPPle · carrossel 8 de 10_

## Slide 1 — capa
`The Physics Atlas · 08/10 · Materiais`

**PT** — Do átomo ao componente.
  Três escalas resolvidas por métodos diferentes — e uma quarta que ainda não está implementada.
  `midia/mat-md.jpg`

**EN** — From the atom to the component.
  Three scales solved by different methods — and a fourth that is not implemented yet.

## Slide 2 — media
`Escala atômica`

**PT** — Dinâmica molecular: o material como ele é
  Átomos, potencial de interação e trajetória. Nesta escala não se fala em tensão nem em módulo: mede-se o que as partículas fazem, e é disso que as propriedades do contínuo precisam nascer.
  PINNeAPPle · examples/molecular
  [SOLVER]
  `midia/mat-md.jpg`

**EN** — Molecular dynamics: the material as it is
  Atoms, interaction potential and trajectory. At this scale one does not speak of stress or modulus: what is measured is what the particles do, and that is where continuum properties have to come from.
  PINNeAPPle · examples/molecular

## Slide 3 — media
`O que sai da escala atômica`

**PT** — Difusão, energia e estrutura
  Temperatura, energia e deslocamento quadrático médio ao longo da trajetória. São estas as quantidades que viram coeficiente de difusão e, depois, propriedade de entrada de um modelo de contínuo.
  [SOLVER]
  `midia/mat-md-dash.png`

**EN** — Diffusion, energy and structure
  Temperature, energy and mean squared displacement along the trajectory. These are the quantities that become a diffusion coefficient and, later, an input property for a continuum model.

## Slide 4 — media
`Plasticidade`

**PT** — O esmagamento, resolvido com plasticidade J2
  Contato penalizado, plasticidade J2, 2.783 nós e 1.480 hexaedros. O cupom roda num laptop — e é essa a escala em que o comportamento do material pode ser conferido sem uma campanha de ensaios.
  [SOLVER]
  `midia/est-crash-superficie.webp`

**EN** — Crush, solved with J2 plasticity
  Penalty contact, J2 plasticity, 2,783 nodes and 1,480 hexahedra. The coupon runs on a laptop — and that is the scale at which material behaviour can be checked without a test campaign.

## Slide 5 — media
`Desgaste`

**PT** — Material saindo da peça, medido
  O desgaste é a interface entre o material e o escoamento: a partícula que risca a parede é o mesmo fenômeno da curva de 90°, visto pela parede. A taxa fica dentro do fator 2 do ensaio publicado.
  artigos/erosao-curva-90
  [EXPERIMENTO]
  `midia/mp-wear.jpg`

**EN** — Material leaving the part, measured
  Wear is the interface between material and flow: the particle scoring the wall is the same phenomenon as the 90° bend, seen from the wall. The rate lands inside the factor-2 band of the published experiment.
  artigos/erosao-curva-90

## Slide 6 — media
`Propriedade termodinâmica`

**PT** — O material que obedece às próprias identidades
  A rede que aprende a energia de Helmholtz e tira cada propriedade por derivada mantém as seis identidades termodinâmicas abaixo de 0,0021%. A que acerta cada número isolado viola a de c_v em 1.100%.
  artigos/co2-supercritico
  [SURROGATE]
  `midia/mat-co2-erros.webp`

**EN** — The material that obeys its own identities
  The network that learns the Helmholtz energy and takes every property as a derivative keeps all six thermodynamic identities below 0.0021%. The one that gets each number on its own violates the c_v identity by 1,100%.
  artigos/co2-supercritico

## Slide 7 — texto
`O que falta`

**PT** — Trinca, fadiga e microestrutura: ainda não
  - **Mecânica da fratura** — não implementada. Sem isso, não há propagação de trinca medida, só ilustração.
  - **Fadiga** — não implementada. Depende de histórico de carregamento e de curva S-N, e nenhuma das duas está no repositório com resultado.
  - **Microestrutura** — existe na escala atômica (MD), não no contínuo: crescimento de grão e solidificação não estão resolvidos.

**EN** — Crack, fatigue and microstructure: not yet
  - **Fracture mechanics** — not implemented. Without it there is no measured crack growth, only illustration.
  - **Fatigue** — not implemented. It needs a load history and an S-N curve, and neither is in the repository with a result.
  - **Microstructure** — exists at the atomic scale (MD), not in the continuum: grain growth and solidification are not solved.

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - Não há ensaio de tração nem de dureza nesta casa: o material entra por propriedade declarada, não por caracterização própria.
  - A ponte entre MD e contínuo é um projeto em aberto, não um pipeline pronto.
  - Nada aqui substitui um laudo de material.

**EN** — What this carousel is not saying
  - There is no tensile or hardness test in this house: the material enters as a declared property, not as our own characterisation.
  - The bridge between MD and continuum is an open project, not a finished pipeline.
  - Nothing here replaces a material report.
