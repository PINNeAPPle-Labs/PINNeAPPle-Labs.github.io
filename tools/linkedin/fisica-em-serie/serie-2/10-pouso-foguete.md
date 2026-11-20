# EP 10 · Pousar um foguete quando o vento decide

**Duração** 45 s · **Estado** parcial — física e controle existem separados · **Base** `examples/rocket_launch`, `examples/flight_dynamics`, `examples/control`, `examples/mujoco`, `digital-twins/reusable-rocket`

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

## O que precisa rodar antes de publicar

- Modelo de dinâmica de voo com o corredor de pouso definido e um controlador fechando a malha em perturbação de vento.
- Um caso de referência verificável: sem vento, o pouso tem de cair onde a trajetória nominal diz — se não cair, o controlador está errado, não o mundo.
- Curva de sensibilidade ao vento, com o limite de validade marcado.
- Se entrar RL: declarar semente, orçamento de treino e o gap sim-to-real (que não existe aqui).

## O que o vídeo não deve afirmar

- Que é um gêmeo do veículo real: é modelo de teste.
- Que houve voo: não houve.
- Que o controlador é ótimo: é um controlador que fecha o corredor sob perturbação declarada.

## Legenda (PT)

É o fecho natural da série, e por um motivo: pousar é o caso em que a física e o controle precisam concordar.

O vídeo mostra a trajetória nominal, a rajada que empurra o estado para fora do corredor, o controlador devolvendo e o custo em combustível. E mostra a curva que interessa a quem projeta: até que intensidade de vento o pouso continua dentro do corredor.

Física e controle existem separados nesta plataforma. Juntar as duas em malha fechada, com o caso sem vento servindo de verificação, é o que falta.

É a mesma lógica do rover que aprendeu o solo pelas próprias rodas: o plano muda quando o mundo ensina.

`#Controle #Simulação #PhysicsAI #Aeroespacial #Foguetes`

## Legenda (EN)

It is the natural closing of the series, for one reason: landing is the case where physics and control have to agree.

The video shows the nominal trajectory, the gust that pushes the state out of the corridor, the controller bringing it back and the fuel cost. And it shows the curve that matters to whoever designs: up to what wind intensity the landing stays inside the corridor.

Physics and control exist separately on this platform. Closing the loop between them, with the no-wind case as verification, is what is missing.

It is the same logic as the rover that learned the soil from its own wheels: the plan changes when the world teaches.

`#Control #Simulation #PhysicsAI #Aerospace #Rockets`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/din-rocket.png` | perfil de subida | existe |
| `serie-1/midia/din-viper.png` | render de veículo | existe (análogo) |
| descida com grade de vento | a produzir | **a produzir** |
| curva de sensibilidade ao vento | a produzir | **a produzir** |
