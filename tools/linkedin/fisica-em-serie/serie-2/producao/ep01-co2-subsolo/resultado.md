# EP 01 · resultado medido

Seção do deck público do SPE10 Model 1 (100 × 1 × 20 células, lida do arquivo original), injeção no canto inferior esquerdo e produção no canto oposto, deslocamento bifásico imiscível por IMPES próprio. Razão de permeabilidade na camada: 998915×.

- **Buckley-Leverett 1-D**: erro L1 do perfil de saturação em PVI = 0,3 → **0,001**; saturação de frente de Welge S_f = **0,238**.
- **Balanço de massa 2-D**: injetado = no domínio + produzido fecha em **100,0%** ao fim da rodada.
- Saturação máxima no domínio ao final: **0,99**; volume de poros injetado: **0,60**.

## O que este resultado é

Deslocamento imiscível de duas fases, com curvas de permeabilidade relativa de Corey e viscosidade da fase injetada na ordem do CO₂ supercrítico. O campo de permeabilidade é o dado público do SPE10, lido do arquivo original — não é uma realização sintética.

## O que este resultado não é

- Não é composicional: não há dissolução, histerese, capilaridade nem variação de viscosidade com a pressão, que são justamente o que decide o destino do CO₂ num caso real.
- Não é o OPM Flow: é um solver próprio, e a validação dele é contra a solução analítica de Buckley-Leverett, não contra outro simulador comercial.
- Não é um sítio geológico: a camada do SPE10 é um benchmark público, não um reservatório com caracterização.
