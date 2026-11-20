# EP 08 · Dá para tornar um objeto invisível ao radar?

**Duração** 45 s · **Estado** a produzir — o método existe, o caso não · **Base** `examples/electrodynamics` (seis problemas com solução exata), `pinneapple_simulation/electromagnetics/antenna`

## O que o vídeo prova

Que espalhamento eletromagnético é um número — seção reta de espalhamento — e que reduzi-lo com uma camada de metamaterial é um problema de otimização com faixa de frequência declarada, não um efeito especial.

## O que precisa existir antes da primeira câmera

Hoje a plataforma resolve eletrostática, onda plana e modo de cavidade com solução exata. Um cilindro em onda plana com camada de metamaterial é um caso novo: precisa de formulação de espalhamento 2-D, condição de fronteira absorvente e um número comparável (SBC — seção reta de espalhamento bistática).

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Onda plana chegando num cilindro; padrão de espalhamento acendendo atrás | `onda plana` | "Um objeto não some. Ele espalha. A pergunta é quanto, em que direção e em que frequência." |
| 5–13 s | Campo espalhado do cilindro nu, com a cor indicando amplitude | `SBC` | "A métrica tem nome: seção reta de espalhamento. É ela que se mede e é ela que se reduz." |
| 13–22 s | O mesmo cilindro com a camada, campo reorganizado | `metamaterial` | "A camada não absorve tudo: ela reorganiza o campo em volta para que a onda siga como se o objeto não estivesse ali — dentro de uma faixa." |
| 22–31 s | Gráfico: SBC contra frequência, duas curvas (nu e com camada) | `redução × faixa` | "A curva é o resultado honesto: redução grande numa faixa estreita, e nada fora dela. Invisibilidade de ampla é ficção." |
| 31–39 s | Varredura de parâmetros: espessura e permissividade | `ε_r · espessura` | "Espessura e permissividade definem onde a redução acontece. Otimizar é escolher a faixa antes de escolher a camada." |
| 39–45 s | Checagens: reciprocidade, energia, convergência de malha | `verificação` | "E as checagens que separam um campo bonito de um resultado: reciprocidade, balanço de energia e convergência com a malha." |

## O que precisa rodar antes de publicar

- Formulação 2-D de espalhamento com fronteira absorvente, verificada contra a série de Mie para o cilindro nu (é a solução exata do problema, e existe para qualquer frequência).
- Camada de metamaterial com parâmetros efetivos declarados, faixa de redução medida e a curva SBC(ω) plotada.
- Convergência de malha mostrada — em problema de onda, malha grossa inventa resultado.
- Se a camada for otimizada: declarar o orçamento e o espaço de busca.

## O que o vídeo não deve afirmar

- Que há um dispositivo fabricado: é simulação.
- Que a invisibilidade é ampla: é uma faixa de frequência, com a curva na tela.
- Que o resultado se aplica a um alvo real: cilindro canônico, 2-D.

## Legenda (PT)

"Invisibilidade" vende, e por isso é o tema em que é mais fácil mentir. O que existe de verdade é uma curva: seção reta de espalhamento contra frequência, com e sem a camada.

O plano do episódio é esse. Cilindro canônico em onda plana, verificado contra a solução de Mie — que é exata e está disponível. Depois a mesma geometria com a camada de metamaterial, e a curva de redução com a faixa onde ela vale.

Fora da faixa, a camada não faz nada. É isso que a curva mostra e o render esconde.

Ainda não rodamos o caso de espalhamento. O método está no repositório, com seis problemas de eletromagnetismo conferidos contra solução analítica — o teste mais barato que existe antes de tentar o caro.

`#Eletromagnetismo #Metamateriais #Simulação #PhysicsAI #Fotônica`

## Legenda (EN)

"Invisibility" sells, which is why it is the easiest topic to lie about. What genuinely exists is a curve: scattering cross section against frequency, with and without the layer.

That is the plan for the episode. A canonical cylinder in a plane wave, verified against the Mie solution — which is exact and available. Then the same geometry with the metamaterial layer, and the reduction curve with the band where it holds.

Outside that band the layer does nothing. That is what the curve shows and the render hides.

We have not run the scattering case yet. The method is in the repository, with six electromagnetics problems checked against analytical solutions — the cheapest test there is before attempting the expensive one.

`#Electromagnetics #Metamaterials #Simulation #PhysicsAI #Photonics`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/em-prius-demag.png` | campo EM (análogo) | existe |
| `serie-1/midia/em-afpm.png` | Studio EM | existe |
| padrão de espalhamento do cilindro | a rodar | **a produzir** |
| curva SBC(ω) | a rodar | **a produzir** |
