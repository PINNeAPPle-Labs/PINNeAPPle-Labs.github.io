# EP 09 · Uma trinca atravessando um componente

**Duração** 40 s · **Estado** a produzir — e o mais distante de todos · **Base** mecânica da fratura (não implementada), `artigos/pico-de-crash-com-surrogate` (plasticidade), `examples/molecular`

## O que o vídeo prova

Que a propagação de trinca é um problema com um número — fator de intensidade de tensão, taxa de crescimento por ciclo — e que sem esse número o vídeo não deve existir.

## Por que este episódio é o último da fila

É o mais bonito de imaginar e o que a plataforma está mais longe de fazer. Mecânica da fratura exige elemento singular na ponta, critério de propagação e, para fadiga, curva S-N ou da/dN com histórico de carregamento. Nada disso está implementado. O roteiro existe para não se perder a ideia — e para deixar claro o que falta.

## Roteiro (só depois de rodar)

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Macro de uma trinca num cupom, luz rasante | — | "Toda peça tem uma trinca. A pergunta não é se ela existe: é quanto tempo ela leva." |
| 5–13 s | Campo de tensão na ponta da trinca, com ampliação | `K_I` | "Na ponta da trinca a tensão não tem valor finito — tem um fator. É ele que compara com a tenacidade do material." |
| 13–22 s | Propagação ciclo a ciclo, com a frente avançando | `da/dN` | "Com o histórico de carregamento, a frente avança por ciclo. A curva de crescimento é o resultado, não o desenho." |
| 22–31 s | Gráfico da/dN contra ΔK, em log-log, com a reta de Paris | `Paris` | "Em log-log, três regimes: abaixo do limiar não cresce, no meio cresce em lei de potência, acima instabiliza." |
| 31–38 s | Comparação com um resultado publicado de cupom | `validação` | "Sem comparação com cupom publicado, isto é ilustração. Com ela, é cálculo." |
| 38–40 s | Assinatura | — | "É por isso que este episódio é o último da fila." |

## O que precisa rodar antes de publicar

- Formulação com singularidade na ponta (quarter-point elements ou J-integral), verificada contra uma solução conhecida (placa com trinca central tem solução fechada).
- Critério de propagação e integração do histórico de carga.
- Um cupom com curva da/dN publicada para comparar — sem isso, não publica.

## O que o vídeo não deve afirmar

- Nada. Enquanto não rodar, este episódio não vai ao ar; o roteiro fica no repositório como projeto.

## Legenda (PT)

Este é o único post da série que não vai ao ar até rodar.

Mecânica da fratura é o caso em que a imagem e o número estão mais distantes: um macro bonito de trinca não diz nada sobre a vida do componente, e a curva que diz — da/dN contra ΔK em log-log — não é bonita.

O plano está escrito, com as três coisas que faltam: elemento singular na ponta, critério de propagação e um cupom com curva publicada para comparar.

Enquanto não houver essas três, prefiro publicar a lista do que não temos a fingir que temos.

`#MecânicaDaFratura #Simulação #PhysicsAI #Fadiga #Materiais`

## Legenda (EN)

This is the one post in the series that does not go out until it runs.

Fracture mechanics is where image and number sit furthest apart: a beautiful macro of a crack says nothing about the life of the component, and the curve that does — da/dN against ΔK on a log-log plot — is not beautiful.

The plan is written, with the three missing pieces: singular element at the tip, a propagation criterion and a coupon with a published curve to compare against.

Until those three exist, I would rather publish the list of what we do not have than pretend we do.

`#FractureMechanics #Simulation #PhysicsAI #Fatigue #Materials`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/mat-md.jpg` | MD (escala atômica) | existe |
| `serie-1/midia/mp-wear.jpg` | desgaste | existe |
| campo na ponta da trinca | a implementar | **a produzir** |
| curva da/dN | a implementar | **a produzir** |
