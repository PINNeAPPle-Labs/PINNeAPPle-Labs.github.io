# 02 · Da tensão à falha: o que a plataforma mede em estrutural

_The Physics Atlas · PINNeAPPle · carrossel 2 de 10_

## Slide 1 — capa
`The Physics Atlas · 02/10 · Estrutural`

**PT** — Da tensão à falha.
  Quatro medições estruturais, cada uma contra uma referência que não é o modelo.
  `midia/est-bracket-render.jpg`

**EN** — From stress to failure.
  Four structural measurements, each against a reference that is not the model.

## Slide 2 — media
`O caso de base`

**PT** — O suporte em L, em CalculiX
  Malha própria, material próprio, campo resolvido. Antes de qualquer alegação sobre um componente real, o caso de base precisa fechar — e ele fecha.
  CalculiX · exemplo de prepomax
  [SOLVER]
  `midia/est-bracket-fea.png`

**EN** — The L-bracket, in CalculiX
  Our own mesh, our own material, the field solved. Before any claim about a real component, the baseline case has to close — and it does.
  CalculiX · prepomax example

## Slide 3 — dado
`O substituto, num crash`

**PT** — O pico de deslocamento, num projeto novo
  24,4%
  de erro médio no pico, nos 30 projetos mantidos fora do treino
  O mesmo modelo, sem o vetor das sete variáveis de projeto, vai a **41,7%**: ele converge para o campo médio porque nada no que recebe diz qual projeto está sendo pedido. Solver: 3,7 min por projeto. Substituto: 197 ms.
  artigos/pico-de-crash-com-surrogate
  `midia/est-crash-pico.webp`

**EN** — Peak displacement, on a design never seen
  24.4%
  mean error on the peak, across the 30 designs held out of training
  The same model, without the vector of seven design variables, goes to **41.7%**: it converges to the mean field because nothing it receives says which design is being asked about. Solver: 3.7 min per design. Surrogate: 197 ms.
  artigos/pico-de-crash-com-surrogate

## Slide 4 — media
`Onde o substituto erra`

**PT** — A referência e a previsão, na mesma escala
  A referência concentra o esmagamento no centro da viga; o substituto espalha uma faixa pela face do para-choque e perde o pico. O erro não é ruído: é viés de 2,7 mm, e está declarado.
  artigos/pico-de-crash-com-surrogate
  [SURROGATE]
  `midia/est-crash-superficie.webp`

**EN** — Reference and prediction, same scale
  The reference concentrates the crush at the centre of the beam; the surrogate spreads a band across the bumper face and misses the peak. The error is not noise: it is a 2.7 mm bias, and it is declared.
  artigos/pico-de-crash-com-surrogate

## Slide 5 — dado
`Busca com física no laço`

**PT** — Até onde uma construção de bloco vai
  135,9 mm
  de balanço com 8 peças — a pilha harmônica clássica chega a 86,7 mm, um bloco só a 31,9 mm
  A tração de pico no pino mais carregado ficou em 0,333 N, 34% do limite de 0,98 N. Cada candidato é julgado por estática rígida antes de virar resultado.
  artigos/construcoes-de-bloco
  `midia/est-blocos.webp`

**EN** — How far a brick build reaches
  135.9 mm
  of overhang with 8 parts — the classic harmonic stack reaches 86.7 mm, a single brick 31.9 mm
  Peak tension on the most loaded stud was 0.333 N, 34% of the 0.98 N limit. Every candidate is judged by rigid statics before it becomes a result.
  artigos/construcoes-de-bloco

## Slide 6 — texto
`Antes de otimizar`

**PT** — A física do modelo foi conferida contra nove formas fechadas
  - Pilha harmônica, tombamento de um bloco, balanço em um pino, empurrão em torre, reações de apoio.
  - Uma viga resolvida por FEA de voxels ficou a **0,4% de Timoshenko** (0,0327 contra 0,0328 mm).
  - Estática e simulador de corpo rígido concordam em **90%, 100% e 75%** dos candidatos — e a discordância está publicada, não escondida.

**EN** — The model's physics was checked against nine closed forms
  - Harmonic stack, tipping of one brick, one-stud overhang, tower push, support reactions.
  - A beam solved by voxel FEA landed within **0.4% of Timoshenko** (0.0327 against 0.0328 mm).
  - Statics and the rigid-body simulator agree on **90%, 100% and 75%** of the candidates — and the disagreement is published, not hidden.

## Slide 7 — media
`Num componente real`

**PT** — von Mises no chassi
  O mesmo pipeline de malha, solver e pós-processamento que fecha nos casos de base é o que roda aqui. O que muda é a geometria, não o critério.
  [SOLVER]
  `midia/est-chassis.png`

**EN** — von Mises on the chassis
  The same mesh, solver and post-processing pipeline that closes on the baseline cases is the one running here. What changes is the geometry, not the criterion.

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - O crash é um cupom de componente, não um veículo: viga DP1000 em duas crash boxes DP600, malha fixa.
  - O erro é contra o próprio solver, não contra ensaio — e a espessura entra pela tensão de escoamento, o que subestima flexão.
  - Otimização de blocos não prova fabricabilidade: prova que a estática que julgou o candidato foi conferida antes.

**EN** — What this carousel is not saying
  - The crash is a component coupon, not a vehicle: a DP1000 beam on two DP600 crash boxes, fixed mesh.
  - The error is against the solver itself, not against a test — and thickness enters through flow stress, which under-represents bending.
  - Block optimisation does not prove manufacturability: it proves the statics that judged the candidate was checked first.
