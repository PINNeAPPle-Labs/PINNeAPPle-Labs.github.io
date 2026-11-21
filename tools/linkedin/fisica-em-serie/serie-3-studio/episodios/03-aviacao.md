# EP S3-03 · Aviação — o avião de 1.920 geometrias

**Área** aerodinâmica de aeronave · **App** `aero_optimizer` (Aircraft Design Optimizer)
· **Duração** 4,7 s · **Mídia** `midia/03-aviacao.mp4`

## O que o vídeo mostra

A aeronave em 3-D com o **Cp do OpenFOAM** na superfície — não um surrogate pintado: o campo vem
da corrida que a app submete e guarda. A câmera gira o modelo no modo *Surface Cp*, com a legenda
que separa sucção (azul) de estagnação (vermelho), e as outras vistas (Realistic, Streamlines,
Slices, Stall map) aparecem na barra superior.

## O número que o episódio usa

| grandeza | valor |
|---|---|
| geometrias avaliadas no estudo | **1.920** |
| tempo do estudo | **96 s** |
| projeto certificável escolhido | **47,9 g CO₂/pkm** |
| Mach de cruzeiro | 0,785 |
| Vref | 130 kt |
| envergadura | 35,8 m |
| alongamento | 10,2 |
| enflechamento | 29° |
| faixa de Cp na tela | −1,347 a 0,597 |

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–1,5 s | avião em 3-D, Cp do OpenFOAM | `1.920 geometrias · 96 s` |
| 1,5–4,7 s | câmera girando no modo Surface Cp | `47,9 g CO₂/pkm · Mach 0,785` |

## O que este episódio não afirma

- Que o campo de Cp é de um solver que roda dentro do navegador: é uma corrida guardada, e a app
  diz de onde vem.
- Que 1.920 geometrias é um espaço de projeto exaustivo: é um espaço paramétrico declarado, varrido
  com surrogate e verificado por CFD nos candidatos.
- Que 47,9 g CO₂/pkm é o que a aeronave vai emitir em serviço: é a métrica de projeto da app para
  um perfil de missão declarado.

## Legenda (PT)

Mil novecentas e vinte geometrias de asa avaliadas em 96 segundos, e um Cp de OpenFOAM na
superfície do projeto que sobrou. Não é um surrogate pintado de campo: é a corrida guardada,
servida em 3-D.

O número que fecha a escolha: 47,9 g de CO₂ por passageiro-quilômetro, com Mach 0,785, Vref 130 kt,
envergadura 35,8 m. O que o Studio mostra é a geometria que produz esse número, girando na tela.

`#Aviação #Aerodinâmica #OpenFOAM #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

One thousand nine hundred and twenty wing geometries in 96 seconds, and an OpenFOAM Cp on the
surface of the design that survived. Not a surrogate dressed up as a field: the stored run, served
in 3-D.

The number that closes the choice: 47.9 g CO₂ per passenger-kilometre, at Mach 0.785, Vref 130 kt,
35.8 m span. What the Studio shows is the geometry that produces it, turning on screen.

`#Aviation #Aerodynamics #OpenFOAM #Simulation #PhysicsAI #PINNeAPPle`
