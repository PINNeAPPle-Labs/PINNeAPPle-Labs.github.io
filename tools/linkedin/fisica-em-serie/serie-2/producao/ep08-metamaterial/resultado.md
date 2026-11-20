# EP 08 · resultado medido

Espalhamento 2-D por um cilindro condutor de raio a com casca dielétrica concêntrica de raio 1,8·a, polarização TM, incidência normal. Solução pela série exata de Bessel/Hankel multicamada (`producao/mie2d.py`), com k0·a = 1,571 no ponto de projeto.

## Verificações

1. **contra a série de cilindro único que já existe no repositório** (`em.waves.cylinder_scattering_tm`), no mesmo grid de campo:

| caso | erro relativo máximo |
|---|---|
| dielétrico ε = 4 | 4,8e-16 |
| dielétrico ε = 12 | 6,7e-16 |
| metálico ε = −20 + 2j | 6,9e-16 |
| condutor | 2,4e-14 |

2. **largura de espalhamento** contra a integração direta do campo distante a 60 λ:

| caso | integração | série | erro |
|---|---|---|---|
| condutor | 1,35591 λ | 1,35838 λ | 0,18% |
| ε = 4,0 | 1,98730 λ | 1,99177 λ | 0,22% |

## O resultado

O núcleo nu espalha **1,3584 λ**. Uma casca isotrópica, otimizada em permissividade, leva isso a **0,8593 λ** — ganho de **2,0 dB**, com ε = +2,07 e b/a = 1,8.

O que a casca faz de fato aparece quando se olha harmônico por harmônico:

| harmônico | núcleo nu | com casca | variação |
|---|---|---|---|
| n = 0 | 0,7549 | 0,9784 | +2,3 dB |
| n = 1 | 0,8399 | 0,3423 | -7,8 dB |
| n = 2 | 0,2740 | 0,2411 | -1,1 dB |
| n = 3 | 0,0370 | 0,1434 | +11,8 dB |

A casca **cancela o dipolo** (-7,8 dB) — que é o termo para o qual ela foi projetada — e **cobra a conta nos outros**: o harmônico 3 sobe +11,8 dB. O total melhora só 2,0 dB porque a largura de espalhamento soma todos eles.

A banda em que a redução passa de 1 dB vai de k0·a = 1,05 a 1,84 — estreita, como toda ressonância de cancelamento.

## O que este resultado é

Uma medida exata de até onde vai uma casca **isotrópica**: ela ajusta um harmônico por vez, e o que se ganha num se perde em outro. Um manto de transformação óptica não é isotrópico — ele precisa de μ_r ≠ μ_θ — e por isso este modelo, com camadas isotrópicas, não o representa.

## O que este resultado não é

- **Não é um manto de invisibilidade**: é uma casca homogênea otimizada.
- Não há dispersão de material: ε é constante dentro da banda varrida, o que nenhum metamaterial real faz.
- Não há estrutura subcomprimento de onda: a casca é homogeneizada por hipótese.
- Não é 3-D: cilindro infinito, incidência normal, uma polarização.
