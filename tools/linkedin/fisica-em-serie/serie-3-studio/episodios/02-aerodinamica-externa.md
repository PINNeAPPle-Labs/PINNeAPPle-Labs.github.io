# EP S3-02 · Aerodinâmica externa — o corpo de Ahmed

**Área** aerodinâmica externa · **App** `ahmed_twin` (Ahmed Twin) · **Duração** 7 s
· **Mídia** `midia/02-aerodinamica-externa.mp4`

## O que o vídeo mostra

O corpo de Ahmed — a geometria que a literatura usa para saber se um modelo de CFD presta — em 3-D,
com o Cp na superfície, e os três sliders que mudam o escoamento de verdade: inclinação da traseira,
folga ao solo e velocidade. A câmera gira o corpo enquanto os sliders se movem.

O twin é um surrogate treinado com uma campanha de **73 corridas OpenFOAM k-omega SST** do próprio
estudo (modelos escolhidos: `mg_ensemble` para CD, `gp_cl` para CL, `pod_cp` para o Cp). A tela
mostra, a cada movimento, a distância até o caso de treino mais próximo e o limite da região de
confiança (0,25).

## O número que o episódio usa

| ponto | inclinação | folga | velocidade | CD | CL | distância ao treino |
|---|---|---|---|---|---|---|
| abertura | 25,0° | 0,050 m | 60,0 m/s | **0,2954** ± 0,0075 | **0,2802** ± 0,1417 | 0,03 (dentro do limite 0,25) |
| final | 40,0° | 0,050 m | 60,0 m/s | **0,2987** ± 0,0081 | **0,0893** ± 0,1470 | **0,00** — é um caso de treino |

(incertezas a 90%, como o app escreve na tela)

O valor em 25° (0,2954) fica na faixa experimental clássica do corpo de Ahmed, 0,285–0,295. Em 40°
o twin está **em cima** de uma corrida de treino: ali o número não é interpolação, é o CFD. E o CL
desaba de 0,2802 para 0,0893 quando a traseira passa de 25° para 40° — é a mudança de regime que
o corpo de Ahmed foi desenhado para mostrar.

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–1 s | corpo em 3-D, Cp na superfície | `Ahmed body · Cp` |
| 1–5 s | sliders: 25° → 40°, corpo girando | `25° → 40° · 60 m/s` |
| 5–7 s | CD e CL atualizando, incerteza a 90% | `CD 0,2987 ± 0,0081 (90%)` |

## O que este episódio não afirma

- Que é CFD ao vivo: o número é do surrogate. O botão **Run a verifying CFD job here**, que roda
  OpenFOAM no mesmo caso, está na tela — mas o vídeo não espera a corrida.
- Que a incerteza a 90% é uma faixa de confiança do modelo: é o erro empírico do surrogate contra
  as corridas que o treinaram, e a app escreve isso na tela.
- Que o resultado vale para outro veículo: o twin interpola dentro do espaço varrido do estudo, e a
  distância ao caso de treino é mostrada justamente para isso.

## Legenda (PT)

O corpo de Ahmed existe por um motivo: é a geometria onde todo mundo já mediu, e por isso serve
para saber se um modelo presta. Aqui ele está em 3-D, com Cp na superfície e os sliders que mudam
o escoamento — inclinação da traseira de 25° para 40°, folga ao solo, 60 m/s.

Em 25° o CD sai 0,2954, na faixa experimental clássica. Em 40° o twin cai exatamente sobre uma das
73 corridas de treino, e a tela avisa: distância 0,00. Ali o número deixa de ser interpolação.

`#Aerodinâmica #CFD #GêmeoDigital #OpenFOAM #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

The Ahmed body exists for one reason: it is the geometry everyone has measured, so it tells you
whether a model is worth anything. Here it is in 3-D, with surface Cp and the sliders that change
the flow — rear slant from 25° to 40°, ground clearance, 60 m/s.

At 25° the CD comes out 0.2954, inside the classic experimental band. At 40° the twin lands exactly
on one of its 73 training runs, and the screen says so: distance 0.00. There the number stops being
an interpolation.

`#Aerodynamics #CFD #DigitalTwin #OpenFOAM #Simulation #PhysicsAI #PINNeAPPle`
