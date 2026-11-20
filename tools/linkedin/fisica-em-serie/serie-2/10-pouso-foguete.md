# EP 10 · Pousar um foguete quando o vento decide

**Duração** 20 s · **Estado** produzido — `midia/ep10-pouso-foguete.mp4` · **Base** `producao/ep10-pouso/gerar.py`, `producao/ep10-pouso/resultado.md`

## O que o vídeo prova

Que o pouso é um problema de controle com perturbação declarada, e que a diferença entre um plano e um bom plano aparece quando o vento muda — do mesmo jeito que o rover aprendeu o solo pelas rodas.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Foguete descendo, grade de vento visível à direita | `perturbação` | "A descida é a parte fácil. O problema é o vento que ninguém combinou." |
| 5–13 s | Perfil de subida e descida, com o corredor de pouso | `perfil` | "A trajetória nominal é uma curva. O controle existe para chegar nela quando o mundo não colabora." |
| 13–22 s | Rajada entrando; o vetor de estado saindo do corredor e voltando | `λ` | "Cada rajada empurra o estado para fora do corredor. O controlador devolve, e o gráfico mostra quanto tempo isso leva." |
| 22–31 s | Comparação: controle ligado × desligado | `com × sem` | "Sem controle, o desvio cresce até o pouso ser outro ponto. Com controle, o desvio é limitado — e o custo é combustível." |
| 31–39 s | Gráfico de sensibilidade à intensidade da rajada | `sensibilidade` | "A curva de sensibilidade é o resultado: até que intensidade o pouso continua dentro do corredor." |
| 39–45 s | Tela do Studio com as checagens | `verificação` | "E as checagens de sempre: conservação, convergência, e o limite de validade declarado." |

## Resultado medido

Massa pontual em 2-D, empuxo vetorado com gimbal de 20°, empuxo máximo de 2,2× o peso, Isp de
3000 m/s, arrasto quadrático e vento lateral com rajada. Controlador PD saturado, sem otimização.

- **sem vento, com controle**: pousou, erro lateral **+0,47 m**, velocidade de toque
  **−0,18 m/s**
- **sem controle**: o mesmo caso termina a **104,3 m/s** — é o controlador que faz o pouso existir
- **varredura de vento**, erro lateral de **+0,47 m** na calmaria a **+1,04 m** com 20 m/s, com a
  velocidade de toque praticamente constante em −0,18 m/s:

| vento [m/s] | erro lateral [m] | velocidade de toque [m/s] |
|---|---|---|
| 0 | +0,47 | −0,18 |
| 4 | +0,52 | −0,18 |
| 8 | +0,59 | −0,18 |
| 12 | +0,70 | −0,18 |
| 16 | +0,86 | −0,18 |
| 20 | +1,04 | −0,18 |

A verificação tem dois lados, e o segundo é o que costuma faltar: o caso sem vento tem de acertar
o alvo **e** o caso sem controle tem de errar. Sem os dois, o número do primeiro não significa
nada.

## O que ficou de fora, e por quê

- É massa pontual: sem atitude, sem inércia rotacional, sem dinâmica de propelente real.
- Não houve voo nem ensaio: a comparação é entre o controlador e a ausência dele.
- O vento é sintético, com envelope declarado; não é atmosfera medida.
- Não há RL: a lei é PD, e o orçamento de treino não existe porque não há treino.

## O que o vídeo não deve afirmar

- Que é um gêmeo do veículo real: é modelo de teste.
- Que houve voo: não houve.
- Que o controlador é ótimo: é um controlador que fecha o corredor sob perturbação declarada.

## Legenda (PT)

É o fecho natural da série, e por um motivo: pousar é o caso em que a física e o controle precisam concordar.

O vídeo mostra a trajetória nominal, a rajada que empurra o estado para fora do corredor, o controlador devolvendo e o custo em combustível. E mostra a curva que interessa a quem projeta: até que intensidade de vento o pouso continua dentro do corredor.

Física e controle existem separados nesta plataforma. Juntar as duas em malha fechada, com o caso sem vento servindo de verificação, é o que falta.

É a mesma lógica do rover que aprendeu o solo pelas próprias rodas: o plano muda quando o mundo ensina.


Medido: sem vento e com controle, o pouso cai a **0,47 m** do alvo com **−0,18 m/s** de toque. Sem controle, o mesmo caso termina a **104,3 m/s** — é o controlador que faz o pouso existir, e é essa a verificação que costuma faltar.

Com 20 m/s de vento lateral o erro vai a 1,04 m. É massa pontual, sem atitude, e não houve voo.

`#Controle #Simulação #PhysicsAI #Aeroespacial #Foguetes`

## Legenda (EN)

It is the natural closing of the series, for one reason: landing is the case where physics and control have to agree.

The video shows the nominal trajectory, the gust that pushes the state out of the corridor, the controller bringing it back and the fuel cost. And it shows the curve that matters to whoever designs: up to what wind intensity the landing stays inside the corridor.

Physics and control exist separately on this platform. Closing the loop between them, with the no-wind case as verification, is what is missing.

It is the same logic as the rover that learned the soil from its own wheels: the plan changes when the world teaches.


Measured: no wind and with control, the landing comes down **0.47 m** from the target at **−0.18 m/s**. Without control, the same case ends at **104.3 m/s** — the controller is what makes the landing exist, and that is the check that is usually missing.

With 20 m/s of crosswind the error grows to 1.04 m. It is a point mass, no attitude, and there was no flight.

`#Control #Simulation #PhysicsAI #Aerospace #Rockets`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-2/midia/ep10-pouso-foguete.mp4` | `producao/ep10-pouso/gerar.py` | **produzido** |
| `serie-2/midia/ep10-pouso-foguete-poster.jpg` | idem | **produzido** |
| `serie-1/midia/din-rocket.png` | perfil de subida | existe (não entra) |
