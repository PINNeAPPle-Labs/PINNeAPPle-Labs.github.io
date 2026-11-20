# EP 05 · A IA consegue prever o escoamento supersônico de um foguete?

**Duração** 45 s · **Estado** produzido — `midia/ep05-supersonico.mp4` · **Base** `producao/euler_bocal.py` (Euler quasi-1D, HLLC), `producao/ep05-supersonico/resultado.md`

## O que o vídeo prova

Que ondas de choque são um campo resolvido, com posição de choque e coeficientes medidos — e que um substituto treinado nesse campo tem domínio de validade, que o vídeo mostra em vez de esconder.

## O que precisa existir antes da primeira câmera

Este é o episódio em que a resposta honesta hoje é **não**: a plataforma tem CFD compressível em casos transônicos (a válvula globo) e tem um caso de lançamento, mas não tem um foguete supersônico resolvido com choque medido. O vídeo só existe depois disso.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Foguete em corte, Mach 2, choque colado ao bico | `Mach 2` | "A onda de choque não é um desenho. Ela tem posição, tem ângulo e tem consequência no empuxo." |
| 5–13 s | Campo de Mach com a malha aparecendo e sumindo | `rhoCentralFoam` | "Um solver compressível resolve o campo em 3-D. A malha aparece aqui de propósito: é ela que decide se o choque é nítido ou borrado." |
| 13–21 s | Corte para pressão e temperatura na parede | `Cp · T_wall` | "Pressão e temperatura na parede são o que a estrutura vai sentir — e é aí que o CFD deixa de ser imagem e vira carregamento." |
| 21–30 s | Split: campo do solver × campo do substituto, depois mapa de erro | `erro relativo L2` | "O substituto aprende este campo e responde em milissegundos. O mapa de erro diz onde ele pode ser chamado." |
| 30–38 s | Gráfico: erro contra Mach, com a faixa de treino sombreada | `fora da faixa: não vale` | "Fora da faixa de Mach em que foi treinado, o substituto não vale — e o gráfico mostra a fronteira, em vez de deixar o usuário descobrir." |
| 38–45 s | Comparação de tempo: solver × substituto | `min × ms` | "O ganho não é estético: é o que permite varrer vinte geometrias antes de escolher qual rodar de verdade." |

## Resultado medido

Euler quasi-1D em um bocal convergente-divergente (600 células, HLLC, primeira ordem), gás
ideal com γ = 1,4, câmara a 1,0 MPa e 300 K, garganta de 50 mm de raio, razão de áreas 2,5.

| régua analítica | resultado |
|---|---|
| relação área–Mach no divergente | erro máximo **0,13%** no perfil de Mach; M de saída 2,440 contra 2,443 (**0,11%**) |
| vazão crítica com garganta sônica | 18,29 kg/s medidos contra 18,33 kg/s (**0,18%**), com deriva de 0,16% ao longo do bocal |
| posição do choque | 0,948 / 0,801 / 0,656 / 0,523 m medidos contra 0,947 / 0,802 / 0,658 / 0,525 m (**até 0,5%**) |
| queda de pressão de estagnação no mesmo ponto | até **0,3%** do valor de Rankine–Hugoniot |

E o número de engenharia: no ponto de projeto (p_saída = p_ambiente, p0/p_a = 15,6) o C_F medido
é **1,333** contra **1,336** da expansão ideal (**0,25%**). Fora dele, com p0/p_a = 3, o C_F cai
para **0,661** — o choque entrou no divergente e cobrou a conta.

## O que ficou de fora, e por quê

- **Não é CFD 3-D**: quasi-1D, sem camada limite, sem separação, sem curvatura de parede.
- Não há química de combustão: γ e R constantes, declarados.
- Não há expansão fora do bocal: o regime subexpandido aparece como perda, não como pluma.
- Não há substituto treinado: todas as réguas são analíticas, e é por isso que o erro é pequeno
  e verificável.

## O que o vídeo não deve afirmar

- Que prevê o escoamento de um foguete real: é geometria simplificada.
- Que o substituto substitui o solver: substitui dentro da faixa, e a faixa está no gráfico.
- Que há validação experimental: não há ensaio de túnel nesta casa.

## Legenda (PT)

Ondas de choque são o teste mais duro que um pipeline de CFD pode enfrentar: o campo tem descontinuidade, o solver precisa de fluxo com correção de choque, e a malha decide metade do resultado.

Este episódio existe para responder uma pergunta com número: um substituto treinado num campo supersônico acerta o quê, e até onde?

A resposta que planejamos mostrar não é "acerta tudo". É o mapa de erro e a fronteira da faixa de Mach em que ele foi treinado — porque fora dela o modelo não vale, e quem usa precisa saber antes.

Ainda não rodamos o caso supersônico. Este roteiro é o plano, com o que falta escrito nele. Quando rodar, sai o vídeo com o número dentro.


Medido contra três réguas analíticas no mesmo escoamento: perfil área–Mach com **0,13%** de erro, vazão crítica com **0,18%** e posição do choque com **até 0,5%** — junto com a queda de pressão de estagnação, que bate em 0,3%.

E o número de engenharia: no ponto de projeto o C_F medido é **1,333** contra **1,336** da expansão ideal. Com p0/p_a = 3, ele cai para 0,661 — o choque entrou no divergente.

É quasi-1D. Não há camada limite, separação nem química de combustão, e o episódio não finge que há.

`#CFD #PhysicsAI #Simulação #Aeroespacial #Supersônico`

## Legenda (EN)

Shock waves are the hardest test a CFD pipeline can face: the field has discontinuities, the solver needs shock-capturing flux, and the mesh decides half the result.

This episode exists to answer one question with a number: a surrogate trained on a supersonic field gets what right, and how far?

The answer we plan to show is not "it gets everything right". It is the error map and the boundary of the Mach range it was trained in — because outside that range the model does not hold, and whoever uses it needs to know first.

We have not run the supersonic case yet. This script is the plan, with what is missing written into it. When it runs, the video comes out with the number inside.


Measured against three analytic rulers in the same flow: area–Mach profile to **0.13%**, choked mass flow to **0.18%**, and shock position to **within 0.5%** — together with the stagnation-pressure drop, matching to 0.3%.

And the engineering number: at the design point the measured C_F is **1.333** against **1.336** for ideal expansion. At p0/p_a = 3 it drops to 0.661 — the shock moved into the diverging section.

It is quasi-1-D. No boundary layer, no separation, no combustion chemistry, and the episode does not pretend otherwise.

`#CFD #PhysicsAI #Simulation #Aerospace #Supersonic`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-2/midia/ep05-supersonico.mp4` | `producao/ep05-supersonico/gerar.py` | **produzido** |
| `serie-2/midia/ep05-supersonico-poster.jpg` | idem | **produzido** |
