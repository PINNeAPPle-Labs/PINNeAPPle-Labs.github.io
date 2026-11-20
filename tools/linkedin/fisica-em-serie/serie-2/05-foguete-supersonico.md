# EP 05 · A IA consegue prever o escoamento supersônico de um foguete?

**Duração** 45 s · **Estado** a produzir — o solver compressível precisa rodar primeiro · **Base** `examples/rocket_launch`, `examples/flight_dynamics`, `cfd_valvula_globo` (transônico)

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

## O que precisa rodar antes de publicar

- Caso supersônico axisimétrico ou 3-D com `rhoCentralFoam` (ou equivalente), convergido, com a posição do choque comparada a uma correlação publicada (cone em escoamento supersônico é o caso barato).
- Coeficientes de arrasto medidos e comparados com correlação, não estimados.
- Um substituto treinado sobre uma faixa de Mach declarada, com validação fora da faixa mostrada.
- Se não der tempo: o episódio pode virar "o que a plataforma faz em transônico" usando a válvula globo, que já existe — mas aí o título muda.

## O que o vídeo não deve afirmar

- Que prevê o escoamento de um foguete real: é geometria simplificada.
- Que o substituto substitui o solver: substitui dentro da faixa, e a faixa está no gráfico.
- Que há validação experimental: não há ensaio de túnel nesta casa.

## Legenda (PT)

Ondas de choque são o teste mais duro que um pipeline de CFD pode enfrentar: o campo tem descontinuidade, o solver precisa de fluxo com correção de choque, e a malha decide metade do resultado.

Este episódio existe para responder uma pergunta com número: um substituto treinado num campo supersônico acerta o quê, e até onde?

A resposta que planejamos mostrar não é "acerta tudo". É o mapa de erro e a fronteira da faixa de Mach em que ele foi treinado — porque fora dela o modelo não vale, e quem usa precisa saber antes.

Ainda não rodamos o caso supersônico. Este roteiro é o plano, com o que falta escrito nele. Quando rodar, sai o vídeo com o número dentro.

`#CFD #PhysicsAI #Simulação #Aeroespacial #Supersônico`

## Legenda (EN)

Shock waves are the hardest test a CFD pipeline can face: the field has discontinuities, the solver needs shock-capturing flux, and the mesh decides half the result.

This episode exists to answer one question with a number: a surrogate trained on a supersonic field gets what right, and how far?

The answer we plan to show is not "it gets everything right". It is the error map and the boundary of the Mach range it was trained in — because outside that range the model does not hold, and whoever uses it needs to know first.

We have not run the supersonic case yet. This script is the plan, with what is missing written into it. When it runs, the video comes out with the number inside.

`#CFD #PhysicsAI #Simulation #Aerospace #Supersonic`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/din-rocket.png` | `rocket_launch/ascent_profile.png` | existe (perfil de subida) |
| `img/exp/aero-autonoma-trust.webp` | triagem com incerteza | existe (análogo metodológico) |
| campo de Mach 3-D | a rodar | **a produzir** |
| mapa de erro do substituto | a rodar | **a produzir** |
