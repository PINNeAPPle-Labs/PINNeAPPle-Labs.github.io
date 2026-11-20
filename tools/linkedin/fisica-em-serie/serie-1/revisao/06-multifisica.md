# 06 · Uma simulação não basta: quando a física interage com a física

_The Physics Atlas · PINNeAPPle · carrossel 6 de 10_

## Slide 1 — capa
`The Physics Atlas · 06/10 · Multifísica`

**PT** — Uma simulação não basta.
  O que a plataforma acopla hoje, o que acopla em parte e o que ainda não acopla — com o nome certo em cada caso.
  `midia/mp-stress.jpg`

**EN** — One simulation is not enough.
  What the platform couples today, what it couples in part and what it does not couple yet — each called by its right name.

## Slide 2 — texto
`Cinco acoplamentos`

**PT** — O que a engenharia cobra de uma plataforma multifísica
  A lista vale mais com a terceira coluna do que sem ela.
  - **Fluido + partícula + parede** — erosão, desgaste, ciclones. _Implementado e comparado com ensaio._
  - **Condução + convecção (CHT)** — dissipadores, placas frias, trocadores. _Implementado, com resíduo medido._
  - **Temperatura + tensão** — gradiente térmico, tensão residual. _Parcial: campos resolvidos em separado._
  - **Eletromagnético + térmico + estrutural** — motores, transformadores. _Parcial: só a parte magnética está medida._
  - **Fluido + estrutura (FSI)** — asa flexível, válvula, flutter. _Ainda não._

**EN** — What engineering asks of a multiphysics platform
  The list is worth more with that third column than without it.
  - **Fluid + particle + wall** — erosion, wear, cyclones. _Implemented and compared against an experiment._
  - **Conduction + convection (CHT)** — heat sinks, cold plates, exchangers. _Implemented, with a measured residual._
  - **Temperature + stress** — thermal gradients, residual stress. _Partial: fields solved separately._
  - **Electromagnetic + thermal + structural** — motors, transformers. _Partial: only the magnetic side is measured._
  - **Fluid + structure (FSI)** — flexible wing, valve, flutter. _Not yet._

## Slide 3 — media
`CHT`

**PT** — Condução no sólido, convecção no fluido, um campo só
  O substituto da placa fria acerta 1,7% do campo de referência — e é reprovado no resíduo. Num caso acoplado isso pesa mais, não menos: o erro de um lado vira condição de contorno do outro.
  artigos/fno-placa-fria
  [SURROGATE]
  `midia/term-fno-campos.webp`

**EN** — Conduction in the solid, convection in the fluid, one field
  The cold-plate surrogate matches the reference field to 1.7% — and is rejected on the residual. In a coupled case that weighs more, not less: the error on one side becomes the boundary condition on the other.
  artigos/fno-placa-fria

## Slide 4 — media
`Fluido + partícula + parede`

**PT** — O acoplamento que já passou por um ensaio
  O escoamento move a partícula, a partícula risca a parede, a parede muda — e a taxa de erosão fica entre **1,05 e 1,49 vez** o medido por Vieira et al. (2016). Acoplamento fraco, em sequência, com o resultado conferido fora de casa.
  [EXPERIMENTO]
  `midia/cfd-erosao.jpg`

**EN** — The coupling that already met an experiment
  The flow moves the particle, the particle scores the wall, the wall changes — and the erosion rate lands between **1.05 and 1.49 times** what Vieira et al. (2016) measured. Weak coupling, in sequence, with the result checked outside the house.

## Slide 5 — media
`Temperatura + tensão`

**PT** — O campo de tensão em 3-D, validado contra FEM
  É a metade estrutural do acoplamento termomecânico, resolvida e validada. A outra metade — passar o campo de temperatura como carregamento térmico e comparar com um caso de referência — é o próximo passo, e ainda não tem número publicado.
  PINNeAPPle · apps/d24-validate
  [SOLVER]
  `midia/mp-stress.jpg`

**EN** — The 3-D stress field, validated against FEM
  This is the structural half of the thermomechanical coupling, solved and validated. The other half — feeding the temperature field in as a thermal load and comparing against a reference case — is the next step, and it has no published number yet.
  PINNeAPPle · apps/d24-validate

## Slide 6 — media
`Processo, não componente`

**PT** — Uma panela de aço, do ciclo ao substituto
  O caso em que o acoplamento é o próprio problema: o térmico do processo define o que acontece com o material, e o substituto existe para responder em segundos o que o modelo leva horas.
  PINNeAPPle · examples/modelica
  [SURROGATE]
  `midia/mp-ladle.png`

**EN** — A steel ladle, from cycle to surrogate
  The case where the coupling is the problem itself: the process thermal history defines what happens to the material, and the surrogate exists to answer in seconds what the model takes hours to run.
  PINNeAPPle · examples/modelica

## Slide 7 — texto
`Forte e fraco`

**PT** — A diferença que separa um resultado de uma promessa
  - **Fraco** — um solver termina, o campo vai para o outro, o segundo resolve. É o que a plataforma faz hoje, e é o que a erosão e o CHT usam.
  - **Forte** — os dois resolvem juntos, a cada passo, com malha móvel. Não está implementado, e é o que FSI exige.
  - Transferir campo entre malhas diferentes é onde o erro entra calado: cada interpolação conserva ou não conserva, e isso precisa ser medido, não assumido.

**EN** — The difference that separates a result from a promise
  - **Weak** — one solver finishes, the field goes to the other, the second solves. That is what the platform does today, and what erosion and CHT use.
  - **Strong** — both solve together, every step, with a moving mesh. It is not implemented, and it is what FSI requires.
  - Transferring a field between different meshes is where error slips in quietly: each interpolation either conserves or does not, and that has to be measured, not assumed.

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - Motor elétrico multifísico completo (EM + calor + estrutura) é um projeto, não um resultado.
  - Flutter, asa flexível e válvula com malha móvel: não implementados.
  - Os casos desta série que ainda não rodaram estão marcados como _a produzir_ — e continuarão marcados até rodarem.

**EN** — What this carousel is not saying
  - A complete multiphysics electric motor (EM + heat + structure) is a project, not a result.
  - Flutter, flexible wings and valves with a moving mesh: not implemented.
  - The cases in this series that have not run yet are marked _to be produced_ — and will stay marked until they run.
