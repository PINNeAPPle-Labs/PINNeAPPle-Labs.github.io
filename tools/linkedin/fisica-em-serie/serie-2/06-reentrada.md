# EP 06 · A IA consegue prever o aquecimento extremo na reentrada?

**Duração** 45 s · **Estado** a produzir — a condução transiente roda, o acoplamento não · **Base** `digital-twins/atmospheric-reentry` (conceito, implementação pendente), `artigos/fno-placa-fria`, cadeia do módulo `capsule-aeroheating`

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

## O que precisa rodar antes de publicar

- Caso de condução transiente 1-D e 2-D no escudo, com fluxo prescrito e balanço de energia medido.
- Uma curva `q(t)` de origem declarada: correlação de engenharia (tipo Sutton-Graves) **ou** um substituto treinado — e o erro de cada uma na superfície.
- Comparação com uma solução de referência (analítica para o caso 1-D com fluxo degrau; solver para o 2-D).
- Se entrar CFD do campo externo, é outro projeto: declare que não entra.

## O que o vídeo não deve afirmar

- Que há CFD de reentrada resolvido aqui: hoje o gêmeo é conceito, com hipóteses a documentar.
- Que o material do escudo foi caracterizado nesta casa: propriedades entram declaradas.
- Que o resultado é certificável para voo.

## Legenda (PT)

Reentrada é o caso em que a imagem e o resultado se separam com mais facilidade. Um render de cápsula atravessando a atmosfera custa uma tarde e não prova nada.

O que prova alguma coisa é o gráfico: o fluxo de calor no ponto de estagnação ao longo do tempo, a condução transiente dentro do escudo e a temperatura que chega à interface com a estrutura — para três espessuras.

Se o fluxo vier de um modelo substituto em vez do escoamento resolvido, o erro dele entra como condição de contorno. É esse erro que precisa estar medido.

Ainda é roteiro. O que temos hoje é a condução transiente e o critério de verificação; o que falta está escrito no documento.

`#Aeroespacial #Simulação #PhysicsAI #TransferênciaDeCalor #Reentrada`

## Legenda (EN)

Reentry is the case where image and result separate most easily. A render of a capsule crossing the atmosphere costs an afternoon and proves nothing.

What proves something is the plot: the heat flux at the stagnation point over time, the transient conduction inside the shield and the temperature that reaches the interface with the structure — for three thicknesses.

If the flux comes from a surrogate instead of a resolved flow, its error enters as a boundary condition. That error is what needs to be measured.

It is still a script. What we have today is transient conduction and the verification criterion; what is missing is written into the document.

`#Aerospace #Simulation #PhysicsAI #HeatTransfer #Reentry`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/term-fno-campos.webp` | campo térmico (análogo) | existe |
| `digital-twins/atmospheric-reentry` | página do catálogo, marcada como conceito | existe |
| corte do escudo com isotermas | a rodar | **a produzir** |
| curva `q(t)` e temperatura na interface | a rodar | **a produzir** |
