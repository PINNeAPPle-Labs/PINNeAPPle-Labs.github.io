# EP 02 · O que acontece quando uma estrutura chega ao limite

**Duração** 45 s · **Estado** parcial — a estática roda, a progressão não · **Base** `artigos/construcoes-de-bloco`, prefixo CalculiX, `digital-twins/bridge-structural-health`

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

## O que precisa rodar antes de publicar

- Um caso de **falha progressiva** (não-linear, com flambagem) — hoje a plataforma tem estática rígida e FEA linear. Ou o vídeo assume que é estática, ou roda o não-linear.
- Replay de corpo rígido em vídeo, com as juntas intactas e o passo de integração declarado.
- A animação da busca geração a geração já existe (`videos/blocos-evolucao.mp4`): serve como abertura ou como bônus.

## O que o vídeo não deve afirmar

- Que prevê colapso de ponte real: o modelo é de encaixe, com atrito assumido em 0,4 e compressão ilimitada.
- Que a discordância entre os dois simuladores foi resolvida: ela está publicada em 90/100/75%.
- Certificação de segurança estrutural.

## Legenda (PT)

Uma construção de brinquedo é o melhor banco de testes de engenharia que existe: a peça, a junta e a falha cabem numa conta de estática.

O vídeo mostra o balanço de 135,9 mm com 8 peças, a ponte de 3 peças carregando 1,46 vez o pedido e a torre de 153,6 mm — cada um com a junta crítica identificada e a tração no pino ao lado do desenho.

E mostra o que quase ninguém publica: onde os dois simuladores discordam. No limite exato da pilha harmônica, a forma fechada diz que fica de pé e o corpo rígido derruba. É essa discordância que decide se você confia no número.

Link do artigo no primeiro comentário.

`#EngenhariaEstrutural #Simulação #PhysicsAI #ElementosFinitos #Falha`

## Legenda (EN)

A toy build is the best engineering test bench there is: the part, the joint and the failure all fit into a statics calculation.

The video shows the 135.9 mm overhang with 8 parts, the 3-part bridge carrying 1.46 times the load asked for and the 153.6 mm tower — each with its critical joint and the stud tension beside the drawing.

And it shows what almost nobody publishes: where the two simulators disagree. At the exact harmonic-stack limit the closed form says it stands and the rigid-body simulator drops it. That disagreement is what decides whether you trust the number.

Article link in the first comment.

`#StructuralEngineering #Simulation #PhysicsAI #FiniteElement #Failure`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/est-blocos.webp` | `img/exp/blocos-balanco.webp` | existe |
| `videos/blocos-evolucao.mp4` | site | existe |
| render do balanço em vídeo | a produzir | **a produzir** |
| replay de corpo rígido | a produzir | **a produzir** |
