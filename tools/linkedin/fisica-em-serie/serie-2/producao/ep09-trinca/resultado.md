# EP 09 · resultado medido

Elasticidade 2-D em estado plano (Q4, espessura unitária), meia-placa de 200 mm de largura com trinca central de comprimento 2a, E = 210 GPa, ν = 0,3, tração de 100 MPa. Nós duplicados nas faces da trinca. K sai do J-integral pela definição (contorno fechado em volta da ponta), com J = K²/E em estado plano de tensão.

## Verificações

1. **patch test** (sem trinca, campo uniforme): σ_yy de 100,000 a 100,000 MPa contra 100 MPa aplicados, e **J = 4,6e-12** — zero a menos de erro de máquina. É a checagem que separa um integrador certo de um que só devolve números plausíveis.
2. **refino de malha** contra a fórmula fechada da secante, K = σ√(πa)·√(sec(πa/2W)):

| malha | h do elemento | K medido | secante | erro |
|---|---|---|---|---|
| 40×80 | 2,500 mm | 27,10 | 25,70 | +5,5% |
| 60×120 | 1,667 mm | 26,89 | 25,70 | +4,6% |
| 80×160 | 1,250 mm | 26,79 | 25,70 | +4,2% |
| 120×240 | 0,833 mm | 26,68 | 25,70 | +3,8% |

3. **caminho independente** — a taxa de liberação de energia por diferença finita da energia potencial, que não usa J em nenhum ponto: G = 3302 J/m² → K = **26,33 MPa√m**, contra **26,96** do J no contorno — 2,4% de diferença entre dois métodos que não compartilham código.
4. **independência de caminho**: k=4: 27,60 · k=8: 27,11 · k=12: 26,96 · k=16: 26,88 · k=20: 26,84 → variação de 2,8% entre o contorno mais próximo e o mais distante.

## O resultado

| a [mm] | K medido | secante | erro |
|---|---|---|---|
| 10 | 18,25 | 17,83 | +2,3% |
| 15 | 22,69 | 22,01 | +3,1% |
| 20 | 26,79 | 25,70 | +4,2% |
| 30 | 34,90 | 32,52 | +7,3% |
| 40 | 43,61 | 39,41 | +10,7% |

Com a malha mais fina o erro cai para **+3,8%** e continua descendo com h: a convergência é lenta porque o elemento Q4 **não representa a singularidade 1/√r** da ponta. Um elemento quarter-point ou um enriquecimento resolveria; não foi feito, e é a razão de este episódio ser implementação e não produção.

## O que este resultado é

Um FE próprio, com a verificação que importa: um caso com resposta exata (campo uniforme), uma fórmula fechada para a geometria real, e um segundo método independente para o mesmo número.

## O que este resultado não é

- **Não é um código de fratura de produção**: sem elemento singular, sem plasticidade, sem propagação.
- Estado plano de tensão, espessura unitária: nada de 3-D, nada de constraint de triaxialidade.
- Material linear elástico: nenhuma zona plástica, nenhum critério de falha aplicado — o número é K, não um veredito sobre o componente.
- A geometria é de placa com trinca central: não é o componente de ninguém.
