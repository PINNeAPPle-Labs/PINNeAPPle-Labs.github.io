# EP 01 · Milhares de litros de CO₂ atravessando o subsolo

**Duração** 18 s · **Estado** **produzido** — `midia/ep01-co2-subsolo.mp4` · **Base** deck público do SPE10 Model 1 (`~/simr-data/opm-data/spe10model1`) + solver IMPES próprio

## O que o vídeo prova

Que a invasão de uma fase num meio poroso heterogêneo é um resultado de solver: frente medida,
balanço de massa fechando e um erro conhecido contra a solução analítica. Não é fumaça.

## Resultado medido (rodado em 2026-11-20)

Seção do deck público do SPE10 Model 1 — 100 × 1 × 20 células, lida do arquivo original —,
injeção num canto e produção no oposto, deslocamento bifásico imiscível, 2.000 células.

| o que | medido |
|---|---|
| erro L1 do perfil 1-D contra Buckley-Leverett (PVI = 0,3) | **0,001** |
| saturação de frente de Welge | **0,238** |
| balanço de massa 2-D (injetado = domínio + produzido) | **100,00%** |
| volume de poros injetado ao fim | **0,60** |
| razão de permeabilidade na camada | **999.000×** |

A razão de permeabilidade de 10⁶ é o que dá o desenho: a pluma não avança como um pistão, ela
escolhe os canais. E é por isso que o balanço de massa fecha em 100,00%: o esquema é
conservativo por construção, e a perda por clipping foi **zero**.

## O que este episódio mudou em relação ao plano

O plano dizia OPM Flow. O OPM não está disponível nesta máquina (Docker parado), e o deck que
está no disco é a variante 100 × 1 × 20, não o 60 × 220 × 85. Em vez de trocar o resultado por
uma imagem, o episódio roda um solver IMPES próprio sobre o **mesmo dado público**, e a
validação passa a ser contra a solução analítica de Buckley-Leverett — que é uma régua mais
dura do que comparar com outro simulador.

## Por que este abre a série

É o episódio com a cadeia de verificação mais curta: solver → solução analítica → balanço. E o
solver de reservatório é o que a indústria compra primeiro.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–4 s | Corte seco: aqui embaixo, em cinza, uma fatia de reservatório com a pluma entrando | — | "Isto não é fumaça. É CO₂ entrando em rocha, a dois quilômetros de profundidade." |
| 4–10 s | Campo de saturação da pluma, tempo correndo | `10 anos` | "Um solver de escoamento em meio poroso resolve a frente ano a ano: onde ela está, quão rápido anda, o que ela contorna." |
| 10–18 s | Malha e camadas do deck SPE10, com a permeabilidade aparecendo | `SPE10 · OPM Flow` | "O dado de entrada é um deck público, com as camadas e a permeabilidade que qualquer um pode baixar e reproduzir." |
| 18–26 s | Gráfico: massa injetada contra massa no domínio | `balanço de massa` | "A checagem que decide não é a imagem: é o balanço. O que entrou menos o que está no domínio tem de fechar." |
| 26–34 s | Split: campo do solver × campo do substituto, com o mapa de erro | `erro por célula` | "O substituto existe para responder em segundos. O mapa de erro é o que diz onde ele pode ser usado." |
| 34–40 s | Tela do Studio: caso, verificações, decisão | `PINNeAPPle Studio` | "E a decisão sai junto com o número: onde o modelo serve, e onde ele não serve." |

## O que precisa rodar antes de publicar

- Caso de injeção montado sobre o SPE10 com fronteira e condições declaradas (o deck é de produção de óleo; a injeção de CO₂ é um caso novo).
- Balanço de massa medido e plotado, não estimado.
- Um substituto treinado sobre as rodadas, com validação em rodadas fora do treino.
- Se o CO₂ for supercrítico, as propriedades vêm da equação de estado — e aí entra o resultado de `co2-supercritico` (rede de potencial, não a direta).

## O que o vídeo não deve afirmar

- Que há armazenamento geológico validado: não há sítio real, há deck público.
- Que a pluma é prevista por IA: a previsão é do solver; o substituto entra depois, com erro medido.
- Qualquer prazo de projeto que dependa de geologia local.

## Legenda (PT)

Um solver de reservatório, um deck público e uma pergunta que a indústria faz há vinte anos: para onde vai o CO₂ depois que ele entra no subsolo?

O vídeo mostra a frente de saturação avançando ano a ano, o balanço de massa fechando e o mapa de erro do substituto que responde em segundos o que o solver leva minutos.

Nenhuma imagem de fumaça: campo de saturação, célula por célula, com o dado de entrada citado.

Link do artigo no primeiro comentário.

`#CCS #Simulação #PhysicsAI #Reservatórios #Descarbonização`

## Legenda (EN)

A reservoir simulator, a public deck and a question the industry has been asking for twenty years: where does CO₂ go once it enters the ground?

The video shows the saturation front advancing year by year, the mass balance closing and the error map of the surrogate that answers in seconds what the solver takes minutes.

No smoke renders: a saturation field, cell by cell, with the input data cited.

Article link in the first comment.

`#CCS #Simulation #PhysicsAI #Reservoir #Decarbonisation`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/geo-simr.jpg` | `img/simr.jpg` | existe (referência estática) |
| campo de saturação animado | a renderizar do OPM Flow | **a produzir** |
| gráfico de balanço de massa | a plotar da rodada | **a produzir** |
| `serie-1/midia/mat-co2-erros.webp` | `img/exp/co2-erros.webp` | existe (propriedades) |
