# EP 02 · O que acontece quando uma estrutura chega ao limite

**Duração** 45 s · **Estado** produzido — `midia/ep02-colapso-estrutural.mp4` · **Base** `examples/bricks/_out` (rodada auditada), `producao/ep02-colapso/resultado.md`, `artigos/construcoes-de-bloco`, `digital-twins/bridge-structural-health`

## O que o vídeo prova

Que a falha de uma estrutura de encaixe é previsível por estática rígida: qual junta abre, quanto ela carrega e por que a construção cai — com a conta ao lado do desenho.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Balanço de 8 peças passando da borda da mesa, renderizado | `135,9 mm` | "Oito peças, cento e trinta e cinco milímetros além da borda. Isto não foi desenhado: foi encontrado por busca." |
| 5–12 s | Câmera orbita o balanço; pino mais carregado acende em vermelho | `0,333 N · 34% do limite` | "Cada junta carrega o que a estática manda. O pino mais solicitado trabalha a 34% do limite de tração." |
| 12–20 s | Corte para ponte de 3 peças sobre o vão, carga aplicada | `1,462 N no meio do vão` | "Na ponte, três peças carregam uma vez e meia a carga pedida. A pergunta não é se fica de pé: é qual junta abre primeiro." |
| 20–28 s | Torre recebendo empurrão no topo; deformada com escala | `153,6 mm · 16 peças` | "A torre aguenta 1,64 vez o empurrão — e quando não aguenta, o relatório diz onde." |
| 28–36 s | Simulador de corpo rígido derrubando o candidato no limite exato | `90% · 100% · 75%` | "Estática e corpo rígido concordam em noventa, cem e setenta e cinco por cento dos candidatos. A discordância é o que ensina: no limite exato, o equilíbrio é neutro e a simulação decide por vocês." |
| 36–45 s | Relatório de confiança: nota 1,00, cobertura 1,00 | `9 formas fechadas` | "Antes de otimizar qualquer coisa, o modelo foi conferido contra nove formas fechadas. Foi por isso que ele pôde julgar." |

## Resultado medido

O episódio é montagem sobre um resultado que já existe e já foi auditado (`examples/bricks`,
rodada anterior). Nada foi simulado de novo para ele, e isso está dito no vídeo.

- balanço vencedor: **135,9 mm** com 8 peças, utilização do pino em **33,9%**, margem **2,95×**
- ponte: **3 peças**; torre: **153,6 mm**
- relatório de confiança: **APPROVED**, 9 de 9 checagens aprovadas
- concordância estática × corpo rígido no limite da pilha harmônica: **7 de 8** fatores testados

## O que ficou de fora, e por quê

- **Não há falha progressiva nem não-linear**: a plataforma tem estática rígida e FEA linear. O
  vídeo assume, em texto, que é estática avaliada candidato a candidato.
- Não há ensaio: as constantes de junta vêm da literatura, não de bancada.
- A animação da busca geração a geração existe (`videos/blocos-evolucao.mp4`) e entra como
  abertura, declarada como tal.

## O que o vídeo não deve afirmar

- Que prevê colapso de ponte real: o modelo é de encaixe, com atrito assumido em 0,4 e compressão ilimitada.
- Que a discordância entre os dois simuladores foi resolvida: ela está publicada em 90/100/75%.
- Certificação de segurança estrutural.

## Legenda (PT)

Uma construção de brinquedo é o melhor banco de testes de engenharia que existe: a peça, a junta e a falha cabem numa conta de estática.

O vídeo mostra o balanço de 135,9 mm com 8 peças, a ponte de 3 peças carregando 1,46 vez o pedido e a torre de 153,6 mm — cada um com a junta crítica identificada e a tração no pino ao lado do desenho.

E mostra o que quase ninguém publica: onde os dois simuladores discordam. No limite exato da pilha harmônica, a forma fechada diz que fica de pé e o corpo rígido derruba. É essa discordância que decide se você confia no número.

Link do artigo no primeiro comentário.


Medido: o balanço de melhor pontuação tem **135,9 mm** com 8 peças, utiliza o pino em 33,9% e sai com margem de 2,95×. A ponte tem 3 peças; a torre, 153,6 mm. O relatório de confiança fecha em **APPROVED**, 9 de 9 checagens.

É estática rígida sobre um modelo de junta declarado — a distribuição de forças mais favorável possível. Não é falha progressiva, não é ensaio, e o vídeo diz isso.

`#EngenhariaEstrutural #Simulação #PhysicsAI #ElementosFinitos #Falha`

## Legenda (EN)

A toy build is the best engineering test bench there is: the part, the joint and the failure all fit into a statics calculation.

The video shows the 135.9 mm overhang with 8 parts, the 3-part bridge carrying 1.46 times the load asked for and the 153.6 mm tower — each with its critical joint and the stud tension beside the drawing.

And it shows what almost nobody publishes: where the two simulators disagree. At the exact harmonic-stack limit the closed form says it stands and the rigid-body simulator drops it. That disagreement is what decides whether you trust the number.

Article link in the first comment.


Measured: the best-scoring balancer is **135.9 mm** tall with 8 pieces, loads the pin to 33.9% and comes out with a 2.95× margin. The bridge needs 3 pieces; the tower is 153.6 mm. The confidence report is **APPROVED**, 9 of 9 checks.

It is rigid statics over a declared joint model — the most favourable force distribution possible. Not progressive failure, not a test, and the video says so.

`#StructuralEngineering #Simulation #PhysicsAI #FiniteElement #Failure`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-2/midia/ep02-colapso-estrutural.mp4` | montagem sobre `examples/bricks/_out` | **produzido** |
| `serie-2/midia/ep02-colapso-estrutural-poster.jpg` | idem | **produzido** |
| `serie-1/midia/est-blocos.webp` | `img/exp/blocos-balanco.webp` | existe |
| `videos/blocos-evolucao.mp4` | site | existe |
