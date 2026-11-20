# EP 04 · Quando a turbulência sacode a aeronave

**Duração** 22 s · **Estado** **produzido** — `midia/ep04-turbulencia.mp4` · **Base** `examples/flight_dynamics` (`07_same_gust.py`)

## O que o vídeo prova

Que a mesma rajada dá respostas diferentes, medidas, e que as fórmulas fechadas de engenharia
servem para umas aeronaves e não para outras — com o número de cada caso na tela.

## Resultado medido (rodado em 2026-11-20)

Rajada 1-cosine de 7,62 m/s (25 ft/s), 2H = 100 m, a 3.000 m, comando fixo, cada aeronave na
sua velocidade de encontro. Quatro aeronaves do catálogo, 660 quadros a 30 fps.

| aeronave | V [m/s] | pico Δn_z | quase-estacionário | Pratt | erro do quase | erro do Pratt |
|---|---|---|---|---|---|---|
| Avião leve | 55 | **+0,625** | 1,463 | 1,014 | **+134%** | +62% |
| Turboélice regional | 120 | **+0,571** | 0,644 | 0,523 | +13% | −8% |
| A320 | 128 | **+0,357** | 0,396 | 0,321 | +11% | −10% |
| Planador motorizado | 40 | **+0,939** | 1,883 | 1,297 | **+100%** | +38% |

As três rotas — solver dinâmico, fórmula quase-estacionária e fórmula de Pratt — concordam
dentro de 13% nas duas aeronaves pesadas. Nas duas leves elas **não** concordam, e o
quase-estacionário chega a +134%: é o limite da fórmula, que ignora o atraso da sustentação e a
dinâmica de corpo curto. O vídeo publica as duas leituras juntas, porque é isso que decide qual
método usar em cada caso.

## Por que entrou cedo na série

É o episódio com a maior razão resultado/esforço: a simulação já existia no repositório, e o
que faltava era o vídeo. Rodou em 85 s, e reproduz exatamente os números de
`examples/flight_dynamics/results/same_gust.json`.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Câmera dentro da cabine: a fuselagem vibrando, janela com nuvem | — | "Isto é o que o passageiro sente. O que o engenheiro precisa saber é outra coisa." |
| 5–12 s | Três séries de rajada correndo, uma por vez, com legenda de intensidade | `leve · moderada · severa` | "A entrada do problema é uma série de rajadas gerada com espectro de von Kármán. Escolher a intensidade é escolher o que a estrutura vai enfrentar." |
| 12–20 s | PSD aparecendo: curva log-log, faixas marcadas | `densidade espectral` | "O espectro diz onde a energia está. Sem ele, comparar duas aeronaves é comparar desenhos." |
| 20–28 s | Resposta no tempo: deslocamento e aceleração, com a frequência própria marcada | `f_n` | "E a resposta mostra onde a estrutura encontra a excitação: se a frequência própria cai dentro da faixa de energia, o número muda de ordem." |
| 28–36 s | Quatro aeronaves, mesma rajada, respostas diferentes | `mesma rajada, quatro geometrias` | "A mesma rajada, quatro geometrias, quatro respostas. É isto que a análise entrega antes do voo, em vez de depois." |
| 36–40 s | Tela do Studio e assinatura | `PINNeAPPle Studio` | "E o resultado sai com o modelo de turbulência declarado ao lado, porque é ele que define o que o número significa." |

## O que precisa rodar antes de publicar

- Rodar as quatro geometrias e plotar as respostas no mesmo eixo (as figuras existentes são por condição, não por aeronave lado a lado).
- Declarar na tela a intensidade e a escala de comprimento usadas em cada curva — sem isso o vídeo vira decoração.
- Se entrar comparação com dado de voo, citar a fonte; hoje o que existe é turbulência sintética.

## O que o vídeo não deve afirmar

- Que é atmosfera real medida em voo: é espectro sintético, declarado.
- Que há ruído radiado calculado: não há solver acústico.
- Que a resposta é certificável: não é um carregamento de projeto, é um estudo de sensibilidade.

## Legenda (PT)

Turbulência não é adjetivo. É uma escolha de modelo, e ela muda o número.

Este vídeo mostra o caminho completo: a série de rajadas gerada com espectro de von Kármán, a densidade espectral de potência que diz onde a energia está, e a resposta da estrutura — a mesma rajada aplicada a quatro geometrias, com quatro respostas diferentes.

O detalhe que faz a diferença: a frequência própria marcada no gráfico. Se ela cai dentro da faixa onde a excitação tem energia, a resposta deixa de ser proporcional.

Turbulência sintética, com intensidade e escala declaradas na tela. Não é voo, e o vídeo diz isso.

Link no primeiro comentário.

`#Aeroelasticidade #Simulação #PhysicsAI #DinâmicaEstrutural #Aeronáutica`

## Legenda (EN)

Turbulence is not an adjective. It is a modelling choice, and it changes the number.

This video shows the full path: the gust series generated with a von Kármán spectrum, the power spectral density that says where the energy is, and the structural response — the same gust applied to four geometries, with four different answers.

The detail that matters: the natural frequency marked on the plot. If it falls inside the band where the excitation carries energy, the response stops being proportional.

Synthetic turbulence, with intensity and scale declared on screen. It is not a flight test, and the video says so.

Link in the first comment.

`#Aeroelasticity #Simulation #PhysicsAI #StructuralDynamics #Aerospace`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/vib-traces.png` | `flight_dynamics/turbulence_traces.png` | existe |
| `serie-1/midia/vib-psd.png` | `flight_dynamics/turbulence_psd.png` | existe |
| `serie-1/midia/vib-gust.png` | `flight_dynamics/gust_sensitivity.png` | existe |
| viewer A320 em voo | `flight_dynamics/viewer_a320_takeoff.png` | existe (estático) |
| animação das quatro respostas | a plotar | **a produzir** |
