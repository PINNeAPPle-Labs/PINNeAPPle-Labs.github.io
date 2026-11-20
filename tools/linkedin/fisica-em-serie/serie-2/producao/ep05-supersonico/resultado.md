# EP 05 · resultado medido

Euler quasi-1D em um bocal convergente-divergente (volumes finitos, fluxo HLLC, primeira ordem), 600 células, gás ideal com γ = 1,4. Câmara com p0 = 1,0 MPa e T0 = 300 K, garganta de 50 mm de raio, razão de áreas de 2,5 na saída.

## As três réguas analíticas

- **relação área–Mach** no divergente: erro máximo de **0,13%** no perfil de Mach; Mach de saída 2,440 contra 2,443 do analítico (0,11%)
- **vazão crítica**: 18,29 kg/s medidos contra 18,33 kg/s analíticos (**0,18%**); a vazão se mantém ao longo do bocal com deriva de 0,16%
- **posição do choque** e **queda de pressão de estagnação** no mesmo ponto:

| p_a [bar] | x do choque medido | analítico | erro | p0₂/p0₁ medido | analítico |
|---|---|---|---|---|---|
| 4,90 | 0,948 m | 0,947 m | 0,0% | 0,567 | 0,567 |
| 6,50 | 0,801 m | 0,802 m | 0,2% | 0,708 | 0,710 |
| 8,10 | 0,656 m | 0,658 m | 0,3% | 0,857 | 0,858 |
| 9,20 | 0,523 m | 0,525 m | 0,5% | 0,961 | 0,962 |

## O resultado de engenharia

O coeficiente de empuxo de um bocal **fixo** não tem pico no ponto de projeto: ele cresce com a razão de pressões e satura perto do vácuo, porque com p_a menor sobra pressão na saída que vira empuxo. O que o projeto decide é onde a curva começa a custar caro.

- **ponto de projeto** (p_a = p_saída isentrópica = 0,64 bar, p0/p_a = 15,6): C_F = **1,333** medido contra **1,336** da expansão ideal → 0,25%
- **superexpandido** (p0/p_a = 3): o C_F cai para **0,661**, 50% abaixo do projeto. Nesse ponto a contrapressão está abaixo da faixa em que o choque cabe dentro do bocal — e este modelo, que não resolve o jato, deixa de dizer qualquer coisa sobre onde o escoamento se ajusta
- **subexpandido** (p0/p_a = 120): C_F = **1,472**, mas o gás sai a 0,64 bar sem virar velocidade — é pressão que um bocal maior converteria, e o preço é área e massa.

A curva é o que escolhe a geometria: a razão de áreas 2,5 fica bem dimensionada para uma faixa estreita de contrapressão, e fora dela ou sobra pressão na saída ou o choque entra no bocal.

## O que este resultado é

Um solver de Euler quasi-1D com três verificações analíticas independentes no mesmo escoamento: perfil isentrópico, vazão crítica e choque normal. O choque é resolvido por captura (HLLC), não imposto como descontinuidade.

## O que este resultado não é

- **Não é CFD 3-D**: é quasi-1D, sem camada limite, sem separação, sem curvatura de parede. Perto da garganta a hipótese 1-D é a mais frágil, e por isso a comparação do perfil começa 8 cm depois dela.
- Não há química de combustão: γ e R são constantes, declarados.
- Não há onda de expansão fora do bocal: o que sai do bocal não é resolvido, então o regime subexpandido aparece só como perda, não como pluma.
- Primeira ordem: o choque aparece espalhado por algumas células, e a posição é lida no mínimo da pressão de estagnação.
