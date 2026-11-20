# EP 06 · resultado medido

Condução transiente 1-D (backward Euler, 400 células) numa laje de material térmico com k = 0,55 W/(m·K), ρ = 1400 kg/m³, cp = 1250 J/(kg·K), fluxo prescrito na face exposta com pico de 1,2 MW/m² em t = 40 s (pulso gaussiano de meia-largura 18 s, energia total 38,3 MJ/m²).

O passo de tempo não é escolhido por espessura: sai de um número de Fourier alvo r = α·dt/dx² = 0,5, de modo que a verificação abaixo vale para o que aparece no vídeo.

## Verificação (face quente contra a solução exata de fluxo constante em meio semi-infinito, T = T₀ + 2q√(αt/π)/k)

- **r = 0,50**, o mesmo das lajes de produção: erro máximo de **1,95%**
- **r = 0,12** (passo de tempo 4× menor): erro máximo de **1,72%** — a diferença entre os dois é a convergência temporal medida, não suposta

## Três espessuras, mesmo pulso de calor

| espessura | células | r | face quente (pico) | face fria (pico) | erro do balanço de energia |
|---|---|---|---|---|---|
| 10 mm | 400 | 0,50 | 6592 K | 2088 K | 0,10% |
| 25 mm | 400 | 0,50 | 6592 K | 305 K | 0,08% |
| 50 mm | 400 | 0,50 | 6592 K | 293 K | 0,31% |

## O que este resultado é

A parte do problema de reentrada que se resolve sem CFD: quanto calor atravessa o escudo e em quanto tempo. O esquema é verificado contra solução exata no mesmo número de Fourier em que roda, a convergência temporal é medida, e o balanço de energia é conferido a cada rodada.

## O que este resultado não é

- **Não há CFD do escoamento**: o fluxo q(t) é prescrito, não vem de um solver compressível com química de gás real.
- **Não há ablação, pirólise nem mudança de propriedades com a temperatura.** É por isso que a face quente chega a 6592 K: acima da temperatura de decomposição de qualquer ablador real, a superfície deveria estar consumindo material e segurando a temperatura. O número alto não é um resultado sobre o material — é o modelo mostrando que a ablação não pode ser ignorada num caso de projeto.
- A face fria, essa sim, é o que se quer: com 10 mm a laje inteira aquece, com 50 mm o calor ainda não chegou ao fundo no tempo do pulso.
- Não é um caso de veículo: não há geometria, ângulo de ataque nem trajetória.
