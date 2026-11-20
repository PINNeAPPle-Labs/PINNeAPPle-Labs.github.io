# EP 07 · O que acontece dentro de um motor elétrico

**Duração** 50 s · **Estado** parcial — magnética medida, térmica separada, acoplamento a produzir · **Base** `artigos/motor-prius-dois-solvers`, `examples/motor_magnetics`, `apps/afpm-designer-*`

## O que o vídeo prova

Que o campo magnético do motor é medido contra um solver independente (0,19% de diferença de torque) e que o acoplamento com o calor é o próximo passo — não um resultado atual.

## Por que é o episódio comercial da série

Motor elétrico é o caso multifísico que a indústria compra: mobilidade elétrica, bombas, ventiladores, compressores. É também o que exige três campos ao mesmo tempo, e é aí que a honestidade sobre o estágio atual pesa mais.

## Roteiro

| tempo | imagem | texto na tela | narração (PT) |
|---|---|---|---|
| 0–5 s | Corte do motor girando, campo |B| pulsando com o rotor | `250 A` | "Três campos vivem dentro deste motor. Hoje a plataforma resolve um deles com número, e é por ele que começamos." |
| 5–13 s | Campo |B| e linhas de fluxo, rotor parado em 12 posições | `12 posições` | "Doze posições de rotor, duas implementações independentes. A diferença máxima de torque é de um vírgula zero nove newton-metro." |
| 13–21 s | Gráfico: torque nas 12 posições, duas curvas e a diferença embaixo | `0,19%` | "Zero vírgula dezenove por cento no pico. Duas malhas diferentes, dois códigos diferentes, o mesmo número." |
| 21–29 s | Mesmo gráfico com a curva do artigo publicado sobreposta | `13 N·m de desvio` | "Contra o artigo publicado, os dois se afastam pela mesma quantia. Isso muda a pergunta: o problema não é o código, é o modelo." |
| 29–38 s | Campo térmico no mesmo estator, resolvido em separado | `térmico: separado` | "O calor existe, resolvido à parte. O que ainda não existe é o acoplamento: perda magnética virando fonte de calor, e a temperatura voltando para o material do ímã." |
| 38–46 s | Diagrama do acoplamento, com a parte que falta hachurada | `perdas → calor → ímã` | "Enquanto essa seta não estiver implementada e medida, o vídeo diz o que é: dois resultados, não um." |
| 46–50 s | Assinatura | — | "Quando fechar, este episódio é refeito com os três campos na mesma imagem." |

## O que precisa rodar antes de publicar

- O ciclo magnético pode ir ao ar **hoje**: 0,19% contra GetDP, 12 posições, é resultado medido.
- Para o acoplamento: mapa de perdas (ferro e cobre) como fonte térmica, solver térmico no mesmo domínio, e a realimentação da temperatura na curva B-H do ímã — com um caso de referência para comparar.
- Verificar que a malha magnética e a térmica compartilham a interface corretamente, e medir o que a interpolação perde.

## O que o vídeo não deve afirmar

- Que é um gêmeo multifísico do motor: são dois campos, resolvidos em separado.
- Que o desvio de 13 N·m contra o paper foi explicado: ele aponta a hipótese, não a corrige.
- Que efeitos 3-D (ponta, skew e perdas) estão no modelo: são magnetostática 2-D.

## Legenda (PT)

Motor elétrico é onde a multifísica deixa de ser exercício e vira requisito: perda magnética vira calor, calor muda a curva do ímã, e o ímã muda o torque.

O que temos hoje, com número: o campo do motor do Prius resolvido por duas implementações independentes, com 0,19% de diferença de torque em 12 posições de rotor. E um desvio de ~13 N·m contra o artigo publicado que aparece igual nos dois — o que aponta para o modelo, não para o código.

O que ainda não temos: a seta que fecha o ciclo, do mapa de perdas até a temperatura realimentando o material.

O vídeo mostra as duas coisas, com a segunda marcada a hachura. Enquanto não fechar, é dois resultados, não um.

`#MobilidadeElétrica #Simulação #PhysicsAI #Eletromagnetismo #Multifísica`

## Legenda (EN)

Electric motors are where multiphysics stops being an exercise and becomes a requirement: magnetic loss becomes heat, heat shifts the magnet's curve, and the magnet shifts the torque.

What we have today, with a number: the Prius motor field solved by two independent implementations, with 0.19% torque difference across 12 rotor positions. And a ~13 N·m drift against the published paper that shows up equally in both — which points at the model, not the code.

What we do not have yet: the arrow that closes the loop, from the loss map to temperature feeding back into the material.

The video shows both, with the second one hatched out. Until it closes, it is two results, not one.

`#ElectricMobility #Simulation #PhysicsAI #Electromagnetics #Multiphysics`

## Mídia

| arquivo | origem | estado |
|---|---|---|
| `serie-1/midia/em-motor-campo.webp` | `img/exp/motor-campo.webp` | existe |
| `serie-1/midia/em-motor-getdp.webp` | `img/exp/motor-getdp.webp` | existe |
| `serie-1/midia/em-afpm.png` | Studio, máquina de fluxo axial | existe |
| campo térmico no estator | a rodar | **a produzir** |
| mapa de perdas | a rodar | **a produzir** |
