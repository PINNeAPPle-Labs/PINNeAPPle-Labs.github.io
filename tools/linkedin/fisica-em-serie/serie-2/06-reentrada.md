# EP 06 · A IA consegue prever o aquecimento extremo na reentrada?

**Duração** 45 s · **Estado** produzido — vídeo em `midia/ep06-reentrada.mp4` · **Base** `producao/ep06-reentrada/gerar.py`, `resultado.md`, `digital-twins/atmospheric-reentry` (conceito), `artigos/fno-placa-fria`, módulo `capsule-aeroheating`

## O que o vídeo prova

Que o aquecimento de um escudo térmico é um problema de condução transiente com condição de contorno de fluxo — e que a parte cara (o fluxo aerodinâmico) pode ser substituída por um modelo, desde que o erro dele esteja medido na superfície.

## A armadilha deste episódio

É o mais bonito da série e o mais fácil de falsificar: um render de cápsula entrando na atmosfera é gratuito e não prova nada. A regra: nenhuma imagem de reentrada sem um gráfico de temperatura ao lado.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Cápsula, com o ponto de estagnação marcado | `ponto de estagnação` | "Toda a energia de uma reentrada entra por um ponto. O resto do escudo existe para espalhar o que aquele ponto recebe." |
| 5–13 s | Perfil de fluxo de calor no tempo (curva subindo e caindo) | `q(t)` | "O fluxo não é constante: ele sobe na entrada, tem pico e cai. A forma dessa curva define o projeto do escudo." |
| 13–22 s | Corte do escudo: calor entrando, isotermas avançando | `condução transiente` | "Do lado de dentro, é condução transiente. O que se mede é quanto calor chega à interface com a estrutura, e em quanto tempo." |
| 22–31 s | Split: fluxo do modelo aerodinâmico × fluxo imposto pela correlação | `erro na superfície` | "Se o fluxo vier de um substituto, o erro dele entra como condição de contorno — e é isso que precisa estar medido, não a beleza do campo." |
| 31–39 s | Gráfico: temperatura na interface para três espessuras | `3 espessuras` | "Três espessuras, três respostas. O gráfico é a decisão de projeto; o render é o slide." |
| 39–45 s | Checagens: balanço de energia, positividade, convergência | `verificação` | "E a checagem que fecha: o balanço de energia tem de fechar. Se não fecha, não importa quão convincente esteja a imagem." |

## Resultado medido

Solver próprio de condução transiente 1-D (backward Euler, 400 células, malha uniforme), laje
de material térmico com k = 0,55 W/(m·K), ρ = 1.400 kg/m³, cp = 1.250 J/(kg·K). Fluxo prescrito
na face exposta: pulso gaussiano com pico de **1,2 MW/m² em t = 40 s**, meia-largura de 18 s,
energia total **38,3 MJ/m²**. Face fria adiabática. O passo de tempo sai de um número de Fourier
alvo (r = α·dt/dx² = 0,5), não é escolhido por espessura.

| régua | resultado |
|---|---|
| face quente contra a solução exata de fluxo constante em meio semi-infinito (r = 0,5, o mesmo que roda) | erro máximo **1,95 %** |
| a mesma, com passo de tempo 4× menor (r = 0,125) | erro máximo **1,72 %** — convergência temporal medida |
| balanço de energia (o que entrou pela face × o que está guardado na laje) | **0,08 % a 0,31 %** nas três espessuras |

| espessura | face quente (pico) | face fria (pico) |
|---|---|---|
| 10 mm | 6.592 K | **2.088 K** |
| 25 mm | 6.592 K | **305 K** |
| 50 mm | 6.592 K | **293 K** |

A face quente idêntica nas três espessuras é o resultado da onda não perceber a espessura no
tempo do pico — é a assinatura do regime semi-infinito, e ela serve de conferência.

E o número que precisa ser dito em voz alta: **6.592 K** é a temperatura de superfície que o
modelo devolve, e nenhum material real chega lá — acima da temperatura de decomposição, um
ablador estaria consumindo massa e segurando a superfície. Esse valor não é um resultado sobre
o material; é o modelo mostrando que **a ablação não pode ser ignorada** num caso de projeto.
O número de projeto é a face fria, e ela separa as três espessuras.

## O que ficou de fora, e por quê

- Não há CFD do escoamento: o fluxo q(t) é prescrito, não vem de um solver compressível com
  química de gás real. Sutton-Graves não entra.
- Não há ablação, pirólise nem variação de propriedades com a temperatura.
- Não há caso 2-D: a espessura é a variável que decide, e ela existe em 1-D.
- Não é um caso de veículo: sem geometria, ângulo de ataque ou trajetória.

## O que o vídeo não deve afirmar

- Que há CFD de reentrada resolvido aqui: hoje o gêmeo é conceito, com hipóteses a documentar.
- Que o material do escudo foi caracterizado nesta casa: propriedades entram declaradas.
- Que o resultado é certificável para voo.

## Legenda (PT)

Reentrada é o caso em que a imagem e o resultado se separam com mais facilidade. Um render de cápsula atravessando a atmosfera custa uma tarde e não prova nada.

O que prova alguma coisa é o gráfico: o fluxo de calor no ponto de estagnação ao longo do tempo, a condução transiente dentro do escudo e a temperatura que chega à interface com a estrutura — para três espessuras.

Se o fluxo vier de um modelo substituto em vez do escoamento resolvido, o erro dele entra como condição de contorno. É esse erro que precisa estar medido.

Os números, medidos: o esquema bate **1,95 %** contra a solução exata de fluxo constante, o balanço de energia fecha em **0,31 %**, e a face fria vai de **2.088 K com 10 mm** a **293 K com 50 mm** no mesmo pulso de 38 MJ/m².

E um número que vale mais que os outros: o modelo sem ablação põe a superfície a **6.592 K**. Nenhum material chega lá — é o cálculo dizendo que a ablação não é um detalhe a ignorar.

`#Aeroespacial #Simulação #PhysicsAI #TransferênciaDeCalor #Reentrada`

## Legenda (EN)

Reentry is the case where image and result separate most easily. A render of a capsule crossing the atmosphere costs an afternoon and proves nothing.

What proves something is the plot: the heat flux at the stagnation point over time, the transient conduction inside the shield and the temperature that reaches the interface with the structure — for three thicknesses.

If the flux comes from a surrogate instead of a resolved flow, its error enters as a boundary condition. That error is what needs to be measured.

The numbers, measured: the scheme matches the exact constant-flux solution to **1,95 %**, the energy balance closes to **0,31 %**, and the cold face goes from **2.088 K at 10 mm** to **293 K at 50 mm** under the same 38 MJ/m² pulse.

And one number worth more than the others: the model without ablation puts the surface at **6.592 K**. No material gets there — that is the calculation saying ablation is not a detail to skip.

`#Aerospace #Simulation #PhysicsAI #HeatTransfer #Reentry`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/term-fno-campos.webp` | campo térmico (análogo) | existe |
| `digital-twins/atmospheric-reentry` | página do catálogo, marcada como conceito | existe |
| `serie-2/midia/ep06-reentrada.mp4` | produzido por `producao/ep06-reentrada/gerar.py` | **produzido** |
| `serie-2/midia/ep06-reentrada-poster.jpg` | idem | **produzido** |
