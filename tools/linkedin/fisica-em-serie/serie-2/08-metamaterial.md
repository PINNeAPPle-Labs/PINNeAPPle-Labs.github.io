# EP 08 · Dá para tornar um objeto invisível ao radar?

**Duração** 20 s · **Estado** produzido — `midia/ep08-metamaterial.mp4` · **Base** `producao/mie2d.py` (série multicamada), `producao/ep08-metamaterial/resultado.md`, `pinneapple_simulation/electromagnetics/waves.py` (série de referência)

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

## Resultado medido

Série exata de Bessel/Hankel para cilindros concêntricos (`mie2d.py`), cilindro condutor de raio
a com casca dielétrica de raio 1,8·a, polarização TM, k0·a = 1,571 no ponto de projeto.

Verificações: a série multicamada, reduzida a uma camada, reproduz a série de cilindro único que
já existe na casa em **4,8e-16 a 2,4e-14** (erro de máquina) em quatro casos — dielétrico ε = 4,
ε = 12, metálico ε = −20 + 2j e condutor. E a largura de espalhamento confere com a integração
direta do campo distante a 60 λ dentro de **0,2%**.

O resultado:

| | núcleo nu | com casca | variação |
|---|---|---|---|
| largura total | 1,3584 λ | **0,8593 λ** | **2,0 dB** |
| harmônico n = 0 | 0,7550 | 0,9770 | +2,3 dB |
| harmônico n = 1 (dipolo) | 0,8399 | 0,3595 | **−7,8 dB** |
| harmônico n = 2 | 0,2740 | 0,2231 | −1,1 dB |
| harmônico n = 3 | 0,0370 | 0,1364 | **+11,8 dB** |

A casca cancela o dipolo, que é o termo para o qual ela foi projetada, e **cobra a conta nos
outros**: o harmônico 3 sobe 11,8 dB. O total melhora 2 dB porque a largura soma todos eles. A
banda em que a redução passa de 1 dB vai de k0·a = 1,05 a 1,84 — estreita, como toda ressonância
de cancelamento.

## O que ficou de fora, e por quê

- **Não é um manto de invisibilidade**: é uma casca homogênea otimizada, e o resultado mostra o
  limite dela.
- Não há manto de transformação óptica: ele precisa de μ_r ≠ μ_θ, e este modelo tem camadas
  isotrópicas. Um manto assim não é representável aqui.
- Não há dispersão de material nem estrutura subcomprimento de onda: ε constante na banda.
- Não é 3-D: cilindro infinito, incidência normal, uma polarização.

## O que o vídeo não deve afirmar

- Que há um dispositivo fabricado: é simulação exata de um cilindro ideal.
- Que há invisibilidade: o total melhora 2 dB — o vídeo mostra a conta harmônico por harmônico
  justamente para não vender o contrário.
- Que o resultado se aplica a um alvo real: cilindro canônico, 2-D, uma polarização.
- Que o solver é numérico: é série exata, e é por isso que a verificação é de erro de máquina —
  não há malha para convergir.

## Legenda (PT)

"Invisibilidade" vende, e por isso é o tema em que é mais fácil mentir. O que existe de verdade é uma curva: seção reta de espalhamento contra frequência, com e sem a camada.

O plano do episódio é esse. Cilindro canônico em onda plana, verificado contra a solução de Mie — que é exata e está disponível. Depois a mesma geometria com a camada de metamaterial, e a curva de redução com a faixa onde ela vale.

Fora da faixa, a camada não faz nada. É isso que a curva mostra e o render esconde.

Ainda não rodamos o caso de espalhamento. O método está no repositório, com seis problemas de eletromagnetismo conferidos contra solução analítica — o teste mais barato que existe antes de tentar o caro.


Medido, harmônico por harmônico: a casca cancela o dipolo em **−7,8 dB** — o termo para o qual ela foi projetada — e **cobra a conta nos outros**, com o harmônico 3 subindo 11,8 dB. A largura total de espalhamento melhora **2,0 dB**, e só numa faixa estreita de k0·a.

É o resultado que importa: cancelar um termo não é ficar invisível. A série é exata e foi conferida contra a implementação independente que já existe na casa, com erro de máquina.

`#Eletromagnetismo #Metamateriais #Simulação #PhysicsAI #Fotônica`

## Legenda (EN)

"Invisibility" sells, which is why it is the easiest topic to lie about. What genuinely exists is a curve: scattering cross section against frequency, with and without the layer.

That is the plan for the episode. A canonical cylinder in a plane wave, verified against the Mie solution — which is exact and available. Then the same geometry with the metamaterial layer, and the reduction curve with the band where it holds.

Outside that band the layer does nothing. That is what the curve shows and the render hides.

We have not run the scattering case yet. The method is in the repository, with six electromagnetics problems checked against analytical solutions — the cheapest test there is before attempting the expensive one.


Measured, harmonic by harmonic: the shell cancels the dipole by **−7.8 dB** — the term it was designed for — and **charges the bill to the others**, with harmonic 3 rising by 11.8 dB. The total scattering width improves by **2.0 dB**, and only over a narrow band of k0·a.

That is the point: cancelling one term is not becoming invisible. The series is exact and was checked against the house's independent implementation, to machine error.

`#Electromagnetics #Metamaterials #Simulation #PhysicsAI #Photonics`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-2/midia/ep08-metamaterial.mp4` | `producao/ep08-metamaterial/gerar.py` | **produzido** |
| `serie-2/midia/ep08-metamaterial-poster.jpg` | idem | **produzido** |
