# EP S3-04 · Térmico de trocador — o dissipador aletado

**Área** transferência de calor / projeto térmico · **App** `heatsink_sizer` (HeatSink Sizer)
· **Duração** 6,2 s · **Mídia** `midia/04-termico-trocador.mp4`

## O que o vídeo mostra

O caminho completo de um projeto térmico dentro do Studio: os requisitos entram (100 W, limite de
70 °C, ar a 2 m/s em duto, envelope 100×100×50 mm, alumínio extrudado), o botão **Find designs**
roda a triagem e devolve a tabela de projetos verificados, e o **Details** abre o campo de
temperatura em 3-D sobre o empilhamento de aletas — girando, com as vistas topo/lateral e a leitura
de ponto no volume.

## O número que o episódio usa

| etapa | número |
|---|---|
| candidatos amostrados | 40.000 |
| candidatos triados | **38.301** |
| passaram a triagem (limite superior conformal 95%) | **414** |
| verificados pela física (FVM + correlações) | **24** |
| tempo | **1,6 s** |

Projeto recomendado (92 × 44 × 5,5 mm de base, 31 aletas de 1,1 × 38 mm, alumínio 6063-T5):

| grandeza | valor |
|---|---|
| ponto quente na fonte | **62,1 °C** (banda pessimista 59,2–65,9) |
| margem até 70 °C | **4,1 °C** |
| resistência térmica | **0,371 K/W** |
| queda de pressão | **17,2 Pa** (25,2 m³/h) |
| massa | **214 g** |
| eficiência de aleta | **85%** (h = 43,1 W/m²K, passo 1,93 mm) |
| erro da triagem contra a física | média 0,30 °C, máxima 0,85 °C |

O ponto importante: a triagem **não é** o resultado. Todo projeto que aparece na tabela foi
recalculado pelo motor de física, com a correlação de convecção e a condução 3-D por volumes
finitos — e a faixa de ±15% na convecção entra como caso pessimista, não como nota de rodapé.

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–2 s | formulário de requisitos preenchido | `100 W · 70 °C · 2 m/s · 100×100×50` |
| 2–3,5 s | tabela de projetos + contadores da busca | `38.301 → 414 → 24` |
| 3,5–6,2 s | campo de temperatura em 3-D nas aletas | `62,1 °C · 0,371 K/W · 17,2 Pa` |

## O que este episódio não afirma

- Que é CFD: a convecção vem de correlação (Teertstra 2000 no duto, Bar-Cohen & Rohsenow 1984 em
  convecção natural) e a condução é volumes finitos nas aletas; aletas e escoamento não são
  resolvidos como campo.
- Que a peça pode ser fabricada como está: as dimensões são arredondadas para valores de extrusão,
  mas ferramental, tolerância e fornecedor não entram no cálculo.
- Que 62,1 °C é a temperatura que o componente vai medir: é a estimativa com a interface térmica
  declarada (10 K·mm²/W); a montagem real é a maior fonte de erro.

## Legenda (PT)

Trinta e oito mil projetos de dissipador triados em menos de dois segundos por um surrogate. Sobram
414. A física recalcula 24. E o que a tela mostra é o campo de temperatura em 3-D nas aletas do
projeto que sobrou: 62,1 °C de ponto quente, 0,371 K/W, 17,2 Pa de perda, 214 g.

O ponto é esse: a triagem é barata e por isso pode varrer tudo; o número que vai para a especificação
é recalculado com a correlação de convecção e a condução nas aletas, com ±15% de pessimismo na
convecção. Erro da triagem contra a física: 0,30 °C na média.

`#TransferênciaDeCalor #Dissipador #Eletrônica #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

Thirty-eight thousand heat-sink designs screened in under two seconds by a surrogate. 414 survive.
Physics recomputes 24. And what the screen shows is the 3-D temperature field on the fins of the
design that survived: 62.1 °C hotspot, 0.371 K/W, 17.2 Pa of pressure drop, 214 g.

That is the point: screening is cheap, so it can sweep everything; the number that goes into a spec
is recomputed with the convection correlation and fin conduction, with a ±15% pessimistic band on
convection. Screening error against physics: 0.30 °C on average.

`#HeatTransfer #HeatSink #Electronics #Simulation #PhysicsAI #PINNeAPPle`
