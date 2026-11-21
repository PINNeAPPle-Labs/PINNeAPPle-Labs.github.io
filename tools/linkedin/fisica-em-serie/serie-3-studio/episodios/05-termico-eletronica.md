# EP S3-05 · Térmico de eletrônica — a placa com FPGA e DDR

**Área** transferência de calor em eletrônica · **App** `pcb_hotspot` (PCB Hotspot)
· **Duração** 5,0 s · **Mídia** `midia/05-termico-eletronica.mp4`

## O que o vídeo mostra

Uma placa de 160 × 100 mm com 6 camadas de cobre e 1,6 mm de espessura, com seis componentes
dissipando 13,80 W no total, em convecção natural vertical, ambiente de 35 °C. O botão **Run full
analysis** roda o caso e a tela devolve: temperatura de junção por componente, margem até Tj,max,
onde o calor vai e o campo de temperatura da placa em 3-D, com os componentes coloridos pela
temperatura de cápsula e a leitura de ponto no volume.

## O número que o episódio usa

| parte | potência | Tj | banda com ±20% de refrigeração | margem | estado |
|---|---|---|---|---|---|
| FPGA (BGA 35×35) | 8,00 W | **99,1 °C** | 92,8–108,4 | **0,9 °C** | marginal |
| LDO (SOIC-8) | 0,60 W | **121,8 °C** | 116,2–130,1 | 3,2 °C | marginal |
| DDR1 (BGA 17×17) | 1,20 W | 86,5 °C | 80,7–95,1 | 8,5 °C | marginal |
| DDR2 (BGA 17×17) | 1,20 W | 86,3 °C | 80,5–94,9 | 8,7 °C | ok |
| VRM (QFN-32) | 1,80 W | 108,3 °C | 102,2–117,5 | 16,7 °C | ok |
| PHY (QFN-64) | 1,00 W | 80,0 °C | 74,8–88,0 | 45,0 °C | ok |

O aviso que o app dá no topo é o resultado comercial do episódio: **"FPGA, DDR1 e LDO passam
nominalmente, mas não com 20% menos refrigeração — adicione margem."** Um projeto que passa no
papel e falha no campo, dito antes de acontecer.

Onde o calor vai: 5,76 W pelo topo da placa (42%), 6,59 W pelo fundo (48%), 1,45 W pelos topos dos
componentes (11%) — 13,80 W fechando.

As duas checagens que a própria tela mostra:

| checagem | valor |
|---|---|
| balanço de energia (calor ao ar + chassi contra potência total − 1) | **1,2·10⁻¹³** |
| convergência de malha (variação da junção quente entre malha grossa e fina) | **0,8%** |

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–1,5 s | tabela de componentes e o aviso | `13,80 W em 6 partes` |
| 1,5–3,5 s | campo de temperatura da placa em 3-D girando | `FPGA Tj 99,1 °C · margem 0,9 °C` |
| 3,5–5 s | divisão do calor e checagens | `energia 1,2e-13 · malha 0,8%` |

## O que este episódio não afirma

- Que é CFD do ar em volta da placa: a convecção é correlação de placa plana com radiação, e o
  coeficiente de superfície aparece no relatório (12,6 W/m²K). Não há escoamento resolvido.
- Que a junção é medida: Tj vem de resistência térmica de junção a cápsula e da condução nas
  camadas de cobre; a calibração contra medição existe em outra aba, com dados do usuário.
- Que 0,9 °C de margem é aceitável: é justamente o que o app sinaliza como marginal.
- Que a placa é de um cliente: é um caso de referência com FPGA/DDR/LDO.

## Legenda (PT)

Treze vírgula oito watts em seis partes de uma placa de 160 por 100 milímetros. A junção mais quente
é o FPGA: 99,1 °C com limite de 100. Margem de 0,9 grau.

O app não diz "passou". Diz que passa nominalmente e **não passa com 20% menos refrigeração** —
que é a pergunta que aparece depois, no campo. O campo de temperatura da placa gira na tela, e o
balanço de energia fecha em 1,2·10⁻¹³.

`#Eletrônica #Térmica #PCB #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

Thirteen point eight watts across six parts of a 160 by 100 millimetre board. The hottest junction
is the FPGA: 99.1 °C against a 100 °C limit. A 0.9 degree margin.

The app does not say "it passes". It says it passes nominally and does **not** pass with 20% weaker
cooling — which is the question that shows up later, in the field. The board's temperature field
turns on screen, and the energy balance closes to 1.2·10⁻¹³.

`#Electronics #Thermal #PCB #Simulation #PhysicsAI #PINNeAPPle`
