# EP S3-07 · Freio — o rotor ventilado

**Área** térmica de máquina / mobilidade · **App** `brakecool_ai` (BrakeCool AI) · **Duração** 9,0 s
· **Mídia** `midia/07-freio.mp4`

## O que o vídeo mostra

Um disco de freio ventilado em 3-D, com o campo de temperatura nos dutos entre as aletas, girando
com o mouse. O cenário é frenagem sustentada (serra, não uma freada única): 800 W contínuos,
resfriamento de estrada.

O botão **Optimize with AI** roda o surrogate e o projeto é **re-verificado** pela fórmula; depois a
potência sobe para 1.600 W (o campo esquenta na tela) e o **Run Monte Carlo (N=200)** responde a
outra pergunta: quanto a tolerância de fabricação move a temperatura.

## O número que o episódio usa

| | aletas | folga | espessura | temperatura |
|---|---|---|---|---|
| projeto de referência | 36 | 8,0 mm | 4,00 mm | **112 °C** |
| otimizado (surrogate) | 79 | 15,9 mm | 3,60 mm | **65 °C** — a fórmula dá 65 °C (0,7% da subida) |

Redução de **47 °C** com a mesma potência de frenagem. A verificação cobre concordância
surrogate × fórmula, limites geométricos e de fabricação, limite térmico e balanço de energia — todos
PASS, com *trust score* 100 e cobertura de 50%.

Com a potência em 1.600 W, o mesmo projeto vai a **105,1 °C**. O Monte Carlo (200 amostras, ruído
uniforme em espessura ±0,05 mm e folga ±0,10 mm, contagem de aletas fixa, cada amostra recalculada
na fórmula fechada — nunca no surrogate):

| grandeza | valor |
|---|---|
| média | **105 °C** |
| desvio-padrão | **±0,2 °C** |
| p95 (pior caso realista) | **105 °C** |
| amostras abaixo da linha de segurança | **100%** |
| veredito | **ROBUST** |

O limite usado pelo app é 500 °C — genérico para ferro fundido, e é o número que ele tem. O que
importa aqui não é o veredito: é o **espalhamento**, ±0,2 °C. Tolerância de fabricação de décimos de
milímetro move a temperatura menos que o erro do próprio modelo, e é isso que muda a conversa com o
fornecedor.

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–2 s | rotor em 3-D, campo nos dutos | `800 W · estrada · 112 °C` |
| 2–4 s | otimizador + re-verificação | `36 → 79 aletas · 112 → 65 °C` |
| 4–6 s | potência 1.600 W, campo mais quente | `1.600 W · 105 °C` |
| 6–9 s | Monte Carlo N=200 e o histograma | `±0,2 °C · 100% abaixo do limite` |

## O que este episódio não afirma

- Que é CFD do ar em volta do disco: o campo é o perfil 1-D ao longo de cada aleta (base quente perto
  do cubo, borda fria) mais a condução pela espessura; o escoamento não é resolvido.
- Que 500 °C é o limite do disco real: é o limite declarado pelo app; um ferro fundido de freio tem
  limites metalúrgicos bem abaixo disso e o episódio não os avalia.
- Que a tolerância de fabricação é a única incerteza: a convecção é o termo dominante e ela não entra
  no Monte Carlo.
- Que 65 °C é a temperatura que o disco vai medir em serra: é a estimativa para o cenário declarado.

## Legenda (PT)

Frenagem sustentada é o caso que quebra disco de freio: 800 W contínuos, não uma freada. O projeto
de referência estabiliza em 112 °C. O otimizador acha 79 aletas e derruba para 65 — e o app
re-verifica na fórmula em vez de acreditar no surrogate.

Depois a pergunta que o fornecedor faz: quanto a tolerância de fabricação mexe nisso? Duzentas
amostras com ±0,05 mm na espessura e ±0,10 mm na folga dão ±0,2 °C. Menos que o erro do próprio
modelo. Isso é uma resposta, e não é a que a planilha costuma dar.

`#Freios #Mobilidade #Térmica #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

Sustained braking is what kills a brake rotor: 800 W continuous, not one hard stop. The reference
design settles at 112 °C. The optimiser finds 79 vanes and brings it to 65 — and the app re-verifies
against the formula instead of trusting the surrogate.

Then the supplier's question: how much does manufacturing tolerance move this? Two hundred samples
with ±0.05 mm on thickness and ±0.10 mm on gap give ±0.2 °C. Less than the model's own error. That
is an answer, and it is not the one a spreadsheet usually gives.

`#Brakes #Mobility #Thermal #Simulation #PhysicsAI #PINNeAPPle`
