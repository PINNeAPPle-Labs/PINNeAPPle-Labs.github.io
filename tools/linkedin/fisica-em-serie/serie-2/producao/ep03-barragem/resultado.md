# EP 03 · resultado medido

Solver próprio de águas rasas (volumes finitos, fluxo HLL) em 1-D e 2-D, rompimento de barragem em leito seco, profundidade inicial 1,0 m, domínio de 10 m.

- **1-D contra Ritter (solução exata)**: erro L2 relativo do perfil em t = 0,8 s → **0,0052**
- **posição da frente** (mesmo critério de 10% da altura nos dois lados): 2,66 m medidos contra 2,63 m de Ritter → **1,0%**
- **conservação de volume 2-D**: erro máximo ao longo da rodada → **0,000%**

## O que este resultado é

Águas rasas de uma fase, com obstáculo retangular de 0,6 m. A verificação é analítica (Ritter, 1892), que é a régua mais dura disponível para este problema.

## O que este resultado não é

- **Não tem sedimento.** Transporte sólido acoplado à fase líquida é outro modelo, e não está implementado nesta casa.
- Não é um caso real: não há geometria de barragem, vale ou material.
- Águas rasas não resolve o que acontece na colisão com a parede: é modelo de profundidade integrada, sem detalhe 3-D.
