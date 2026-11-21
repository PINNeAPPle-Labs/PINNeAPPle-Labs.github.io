# EP S3-01 · Eletromagnetismo — o motor de fluxo axial

**Área** eletromagnetismo · **App** `afpm_designer` (Axial-Flux Motor Designer) · **Duração** 6 s
· **Mídia** `midia/01-eletromagnetismo.mp4`

## O que o vídeo mostra

A tela do Studio rodando o projeto de um motor de fluxo axial: o formulário com os parâmetros do
estator e do rotor, o botão **Estimate (quasi-3D)**, o job rodando de verdade (fila, progresso) e,
quando ele termina, o campo |B| em 3-D sobre a malha de 15.728 triângulos, girando com o mouse.
O mapa vai de 0,02 T a 2,27 T na superfície (máximo de 2,38 T no nó, no entreferro).

## O número que o episódio usa

O app entrega dois números para a mesma máquina e **mostra a diferença entre eles**, que é o que
torna o episódio honesto:

| grandeza | estimate quasi-3-D | verificação 3-D | desvio |
|---|---|---|---|
| torque de cogging | 8,604 N·m | 7,626 N·m | **+12,8%** |
| fluxo no entreferro | — | — | **+2,1%** |

O estimate é rápido e serve para varrer projeto; a verificação 3-D é que vale para fechar número.
O vídeo mostra os dois na mesma sessão, com o desvio escrito na própria tela.

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–1,5 s | formulário do motor | `AFPM · estimate quasi-3D` |
| 1,5–3 s | job rodando | `job de verdade` |
| 3–6 s | campo \|B\| em 3-D girando | `máx 2,38 T · cogging +12,8% sobre o 3-D` |

## O que este episódio não afirma

- Que é FEA de elemento finito em 3-D completo: o estimate é quasi-3-D e a verificação é a malha
  que a app constrói, não um solver de campo aberto.
- Que o desvio de cogging é aceitável para qualquer aplicação: 12,8% é grande para quem especifica
  cogging, e o app diz isso em vez de esconder.
- Que os parâmetros são de um motor caracterizado nesta casa: são de um motor plausível.

## Legenda (PT)

Um motor de fluxo axial, projetado na tela. O estimate quasi-3-D leva segundos; o campo em 3-D
leva minutos. E os dois discordam — no cogging, 8,604 contra 7,626 N·m, 12,8% de diferença.

O app mostra o desvio em vez de escondê-lo. É essa a diferença entre um surrogate que serve para
varrer projeto e um número que serve para fechar especificação.

`#Eletromagnetismo #MotoresElétricos #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

An axial-flux motor, designed on screen. The quasi-3-D estimate takes seconds; the 3-D field takes
minutes. And the two disagree — on cogging torque, 8.604 against 7.626 N·m, a 12.8% gap.

The app shows the gap instead of hiding it. That is the difference between a surrogate that is good
for sweeping a design space and a number that is good for signing a spec.

`#Electromagnetics #ElectricMotors #Simulation #PhysicsAI #PINNeAPPle`
