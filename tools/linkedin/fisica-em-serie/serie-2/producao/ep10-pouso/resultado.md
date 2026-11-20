# EP 10 · resultado medido

Massa pontual em 2-D, empuxo vetorado com gimbal de 20°, empuxo máximo de 2,2× o peso, Isp de 3.000 m/s, arrasto quadrático e vento lateral com rajada. Controlador PD saturado, sem otimização.

- **sem vento, com controle**: pousou em sim, erro lateral **+0.470 m**, velocidade de toque **-0.18 m/s**
- **sem controle**: o mesmo caso termina a 104.3 m/s — o controlador é o que faz o pouso existir
- **varredura de vento**:

| vento [m/s] | erro lateral [m] | velocidade de toque [m/s] |
|---|---|---|
| 0 | +0.47 | -0.18 |
| 4 | +0.52 | -0.18 |
| 8 | +0.59 | -0.18 |
| 12 | +0.70 | -0.18 |
| 16 | +0.86 | -0.18 |
| 20 | +1.04 | -0.18 |

## O que este resultado é

Um laço de controle fechado com física de voo declarada, e uma verificação em dois lados: o caso sem vento tem de acertar o alvo, e o caso sem controle tem de errar. Sem os dois, o número do primeiro não significa nada.

## O que este resultado não é

- Não é um gêmeo do veículo: é massa pontual, sem atitude, sem inércia rotacional.
- Não há voo nem ensaio: a comparação é entre o controlador e a ausência dele.
- O vento é sintético, com envelope declarado; não é atmosfera medida.
