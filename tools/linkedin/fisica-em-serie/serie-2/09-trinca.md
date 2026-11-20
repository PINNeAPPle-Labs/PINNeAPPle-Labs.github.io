# EP 09 · Uma trinca atravessando um componente

**Duração** 20 s · **Estado** produzido (implementação, não produção) — `midia/ep09-trinca.mp4` · **Base** `producao/fratura.py` (Q4 + J-integral), `producao/ep09-trinca/resultado.md`

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

## Resultado medido

Elasticidade 2-D em estado plano (Q4), placa de 200 mm com trinca central de 2a = 40 mm,
E = 210 GPa, ν = 0,3, tração de 100 MPa. Nós duplicados nas faces da trinca; K pelo J-integral
na definição, com J = K²/E.

| verificação | resultado |
|---|---|
| patch test (sem trinca, campo uniforme) | σ_yy de **100,000 a 100,000 MPa** e **J = 4,6e-12** — zero a menos de erro de máquina |
| refino de malha contra a secante de Feddersen | **+5,5% → +3,8%** de 40×80 a 120×240 |
| caminho independente (energia liberada por diferença finita) | K = **26,33** contra **26,96** do J no contorno → **2,3%** |
| independência de caminho | 27,60 → 26,84 conforme o contorno se afasta, **2,8%** de variação |

O erro de 3,8% contra a fórmula fechada **não** é ruído: ele cai monotonicamente com h, e cai
devagar porque o elemento Q4 não representa a singularidade 1/√r da ponta. Um elemento
quarter-point ou um enriquecimento resolveria — não foi feito, e é a razão de este episódio ser
implementação e não produção.

## O que ficou de fora, e por quê

- Sem elemento singular, sem plasticidade, sem propagação, sem histórico de carga.
- Estado plano de tensão, espessura unitária: nada de 3-D nem de triaxialidade.
- O número é K, não um veredito sobre componente nenhum.
- Não há cupom com curva da/dN: este episódio não fala de fadiga.

## O que o vídeo não deve afirmar

- Que é um código de fratura de produção: é implementação com verificação, e o erro de 3,8% está
  na tela, não escondido.
- Que o componente de alguém foi avaliado: a geometria é uma placa canônica.
- Que há critério de falha aplicado: o resultado é K, e comparar com tenacidade é outro passo.

## Legenda (PT)

Este é o único post da série que não vai ao ar até rodar.

Mecânica da fratura é o caso em que a imagem e o número estão mais distantes: um macro bonito de trinca não diz nada sobre a vida do componente, e a curva que diz — da/dN contra ΔK em log-log — não é bonita.

O plano está escrito, com as três coisas que faltam: elemento singular na ponta, critério de propagação e um cupom com curva publicada para comparar.

Enquanto não houver essas três, prefiro publicar a lista do que não temos a fingir que temos.


Medido: o J-integral reproduz a fórmula fechada da placa com trinca central com **+3,8%** de erro na malha mais fina, e converge devagar porque o elemento Q4 não carrega a singularidade 1/√r da ponta. Um segundo método, que não usa J em ponto nenhum, dá o mesmo número com 2,3% de diferença.

O patch test fecha em **4,6e-12** — zero a menos de erro de máquina. É implementação verificada, não código de produção, e o erro está na tela.

`#MecânicaDaFratura #Simulação #PhysicsAI #Fadiga #Materiais`

## Legenda (EN)

This is the one post in the series that does not go out until it runs.

Fracture mechanics is where image and number sit furthest apart: a beautiful macro of a crack says nothing about the life of the component, and the curve that does — da/dN against ΔK on a log-log plot — is not beautiful.

The plan is written, with the three missing pieces: singular element at the tip, a propagation criterion and a coupon with a published curve to compare against.

Until those three exist, I would rather publish the list of what we do not have than pretend we do.


Measured: the J-integral reproduces the closed-form centre-cracked plate to **+3.8%** on the finest mesh, and converges slowly because the Q4 element does not carry the 1/√r tip singularity. A second method, which uses no J anywhere, gives the same number within 2.3%.

The patch test closes at **4.6e-12** — zero to machine error. This is verified implementation, not production code, and the error is on screen.

`#FractureMechanics #Simulation #PhysicsAI #Fatigue #Materials`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-2/midia/ep09-trinca.mp4` | `producao/ep09-trinca/gerar.py` | **produzido** |
| `serie-2/midia/ep09-trinca-poster.jpg` | idem | **produzido** |
