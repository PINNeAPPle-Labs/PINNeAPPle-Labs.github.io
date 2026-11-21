# EP S3-06 · Acústica — o duto bass-reflex

**Área** acústica · **App** `soundshape_ai` (SoundShape AI) · **Duração** 5,0 s
· **Mídia** `midia/06-acustica.mp4`

## O que o vídeo mostra

O duto de uma caixa bass-reflex em 3-D, com a malha de triângulos acompanhando os sliders: o raio
do duto sobe de 28 para 40 mm e o comprimento cai de 95 para 76 mm, com a frequência de Helmholtz
recalculada a cada passo (45,3 Hz → 72,1 Hz no manual) e a cor do duto trocando com ela.

Depois o botão **Optimize with AI** devolve o projeto para o alvo de 40 Hz, e a tela mostra a
verificação contra a fórmula fechada, com o veredito de cada checagem.

## O número que o episódio usa

| | raio | comprimento | volume do duto | frequência |
|---|---|---|---|---|
| ponto de partida | 25,0 mm | 100,0 mm | 196 cm³ | **45,31 Hz** |
| otimizado pelo surrogate | 22,82 mm | 113,17 mm | 185 cm³ | **40,00 Hz** (previsto) |
| conferido na fórmula fechada | — | — | — | **40,10 Hz** (alvo 40,0 · desvio **0,1%**) |

Fórmula: f = (c/2π)·√(A/(V·L_ef)), com L_ef = L + 0,85·r.

O app também declara o erro de validação do surrogate no servidor: **0,4%** contra a fórmula.

## O limite honesto deste episódio

O ar dentro do duto **não tem gradiente**: a cor é uniforme porque o modelo é concentrado
(Helmholtz), não um campo acústico 3-D. O app diz isso na própria tela. O 3-D aqui serve para ver a
geometria que está sendo dimensionada, não para ler um campo.

E a fronteira de compromisso (tamanho do duto contra precisão de sintonia) **colapsa** neste ponto
de operação: das oito varreduras de peso, sete devolvem o mesmo projeto (raio 11,73 mm, comprimento
20,00 mm — o piso da restrição) e a oitava deriva para 35,92 Hz com 10,2% de erro. Ou seja: com
20 L de caixa e alvo de 40 Hz, os dois objetivos apontam para o mesmo canto, e não há fronteira para
explorar. O gráfico aparece no vídeo; a leitura correta dele é essa, e não "há um compromisso".

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–1,2 s | duto em 3-D inclinando | `bass-reflex · Helmholtz` |
| 1,2–2,5 s | sliders de raio e comprimento, cor mudando | `45,3 Hz → 72,1 Hz` |
| 2,5–3,5 s | resultado do otimizador com as checagens | `40,1 Hz · alvo 40,0 · 0,1%` |
| 3,5–5 s | gráfico da fronteira | `fronteira degenerada` |

## O que este episódio não afirma

- Que há campo acústico resolvido: é modelo concentrado de Helmholtz; sem modos, sem difração, sem
  absorção.
- Que a fronteira mostrada é útil neste caso: ela colapsa, como escrito acima.
- Que o duto otimizado soa bem: frequência de sintonia não é resposta em frequência, e o episódio
  não mede nenhuma curva.

## Legenda (PT)

Um duto bass-reflex de 20 litros, afinado em 40 Hz. O otimizador parte de 45,3 Hz e chega a 40,1 —
0,1% do alvo — e a tela confere contra a fórmula fechada de Helmholtz, não contra o próprio modelo.

O limite está escrito no app: o ar dentro do duto não tem gradiente, porque o modelo é concentrado.
O 3-D mostra a geometria que está sendo dimensionada, não um campo. E a fronteira de compromisso
colapsa neste ponto: com 20 L e 40 Hz, os dois objetivos apontam para o mesmo canto.

`#Acústica #BassReflex #AltoFalantes #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

A 20-litre bass-reflex port tuned to 40 Hz. The optimiser starts at 45.3 Hz and lands on 40.1 —
0.1% off target — and the screen checks it against the closed-form Helmholtz formula, not against
its own model.

The limit is written in the app: the air inside the port has no gradient, because the model is
lumped. The 3-D shows the geometry being sized, not a field. And the trade-off frontier collapses at
this operating point: with 20 L and 40 Hz, both objectives point at the same corner.

`#Acoustics #BassReflex #Loudspeakers #Simulation #PhysicsAI #PINNeAPPle`
