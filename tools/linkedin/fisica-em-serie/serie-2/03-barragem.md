# EP 03 · A barragem, e o que a simulação realmente entrega

**Duração** 40 s · **Estado** a produzir — as duas metades existem separadas · **Base** `examples/free_surface` (superfície livre) + `examples/geomechanics` (coluna granular)

## O que o vídeo prova

Que a frente de onda, o run-up e o alcance final são medidos, e que a versão com sedimento é um problema de duas fases que esta casa **ainda não resolve** — dito no vídeo, não na legenda.

## Por que este episódio é o mais arriscado da série

É o que mais se parece com um vídeo de divulgação e o que menos tem de resultado. A regra que salva o episódio: mostrar os dois casos que existem, nomear o que falta, e não colar um render de água onde deveria estar um solver.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Coluna granular desabando, lateral removida | `colapso granular` | "Uma coluna de material, a parede que sai, e um resultado que qualquer laboratório de geotecnia reproduz." |
| 5–12 s | Mesma sequência em câmera lenta, com o ângulo de repouso anotado | `ângulo de repouso` | "O que se mede aqui não é a poeira: é o ângulo final, o alcance e o tempo até parar." |
| 12–20 s | Corte para superfície livre: onda correndo o declive | `run-up` | "A outra metade é a água: frente de onda, run-up e a lâmina que sobra depois que ela passa." |
| 20–28 s | Os dois painéis lado a lado, mesma escala de tempo | `mesmo tempo, dois modelos` | "Dois modelos, dois métodos, nenhum deles resolvendo água e sedimento juntos. É aqui que a maioria dos vídeos de barragem engana." |
| 28–36 s | Caixa de texto sobre a cena: "ainda não" | `acoplamento bifásico: a implementar` | "O que falta é exatamente isso: transporte de sedimento acoplado à fase líquida, com conservação de massa medida nos dois lados." |
| 36–40 s | Assinatura + link | — | "Quando rodar, este vídeo é refeito com o número dentro." |

## O que precisa rodar antes de publicar

- Caso de **dam break** com superfície livre e obstáculo, com altura de onda comparada a um benchmark experimental (Martin & Moyce é o clássico e é barato).
- Se o episódio for vender sedimento: acoplamento bifásico (ou Euler-Euler / MP-PIC), que hoje não está implementado.
- Conservação de massa nos dois lados, plotada.

## O que o vídeo não deve afirmar

- Que simula uma barragem real: o caso é idealizado.
- Que o sedimento está resolvido. Não está.
- Que o resultado foi validado contra o rompimento de uma barragem real.

## Legenda (PT)

Todo vídeo de ruptura de barragem parece o mesmo: água marrom, câmera lenta, muito drama. A pergunta que interessa a quem projeta é outra — a altura de onda bate com o ensaio?

Este episódio mostra o que temos de verdade: colapso granular com ângulo de repouso medido e superfície livre com frente de onda e run-up. Dois modelos, dois métodos.

E mostra o que ainda não temos: transporte de sedimento acoplado à fase líquida. Quando rodar, o vídeo é refeito com o número dentro.

Publicar a lacuna é a parte barata. Esconder custa caro depois.

Link no primeiro comentário.

`#CFD #Simulação #PhysicsAI #Hidráulica #SuperfícieLivre`

## Legenda (EN)

Every dam-break video looks the same: brown water, slow motion, a lot of drama. The question that matters to whoever designs is different — does the wave height match the experiment?

This episode shows what we genuinely have: granular collapse with a measured angle of repose, and free-surface flow with a wave front and run-up. Two models, two methods.

And it shows what we do not have yet: sediment transport coupled to the liquid phase. When it runs, the video is remade with the number inside.

Publishing the gap is the cheap part. Hiding it gets expensive later.

Link in the first comment.

`#CFD #Simulation #PhysicsAI #Hydraulics #FreeSurface`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/mf-coluna.png` | `geomechanics/column_collapse.png` | existe |
| `serie-1/midia/mf-free-surface.png` | `free_surface/runner_slope.png` | existe |
| animação de dam break com obstáculo | a rodar | **a produzir** |
| comparação com Martin & Moyce | a plotar | **a produzir** |
