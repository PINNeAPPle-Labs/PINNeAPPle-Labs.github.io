# Legendas · Série 1 — The Physics Atlas

Texto do post que acompanha cada carrossel. Um bloco por publicação, em português e em
inglês. O carrossel tem 8 imagens (ver `carrosseis/`); a legenda é o que vai no campo de
texto do LinkedIn.

Regras que valem para todas:

- O link vai no **primeiro comentário**, não na legenda — o LinkedIn reduz o alcance de post
  com link no corpo. A legenda diz "link no comentário".
- Nenhuma afirmação sem o número que a sustenta. Se um caso ainda não rodou, a legenda diz.
- Uma pergunta no fim, sempre sobre o problema do leitor, nunca sobre o produto.
- Hashtags: 4 a 6, sempre as mesmas três primeiras (`#CFD #Simulação #PhysicsAI`), o resto
  varia com a área.

---

## 01 · CFD

**PT**

Um carro de corrida paramétrico, três objetivos brigando entre si e um orçamento de 20
rodadas de CFD. A plataforma escolheu onde gastar cada uma e chegou a −15,7% de arrasto com
o downforce acima do piso. O mesmo desenho, na malha fina, dá −13,9%.

É esse segundo número que interessa. Sem ele, o primeiro é marketing.

O carrossel mostra sete resultados de CFD — corpo de Ahmed, esteira de F1, otimização de
asa com 1.920 geometrias, erosão em curva de 90° — cada um com o número e o limite do lado:
o que é solver de referência, o que é previsão de IA e o que é comparação com ensaio
publicado.

A parte incômoda está no último slide, e é a razão de publicar: qual é o erro do substituto,
onde ele extrapola e o que não foi medido.

Se o seu caso de CFD trava na mesma pergunta — qual é o próximo caso que vale simular? —
vale a leitura. Link do artigo no primeiro comentário.

`#CFD #Simulação #PhysicsAI #Aerodinâmica #OpenFOAM`

**EN**

A parametric race car, three objectives fighting each other and a budget of 20 CFD runs. The
platform chose where to spend each one and landed at −15.7% drag with downforce above the
floor. The same design on the fine mesh gives −13.9%.

That second number is the one that matters. Without it, the first is marketing.

The carousel shows seven CFD results — Ahmed body, F1 wake, wing optimisation across 1,920
geometries, erosion in a 90° bend — each with its number and its limit beside it: what is a
reference solver, what is an AI prediction and what is a comparison against a published
experiment.

The uncomfortable part is on the last slide, and it is the reason to publish: the surrogate's
error, where it extrapolates, and what was not measured.

If your CFD case is stuck on the same question — which case is worth simulating next? — it is
worth a read. Article link in the first comment.

`#CFD #Simulation #PhysicsAI #Aerodynamics #OpenFOAM`

---

## 02 · Estrutural

**PT**

Um para-choque contra poste rígido, 200 projetos resolvidos pelo solver explícito, e um
substituto que lê as sete variáveis de projeto. Nos 30 projetos mantidos fora do treino, o
deslocamento de pico sai com 24,4% de erro médio.

O mesmo modelo, sem o vetor de projeto, vai a 41,7%. Não é um modelo pior: é um modelo sem a
informação — ele converge para o campo médio porque nada no que recebe diz qual projeto está
sendo pedido.

Isso, e a construção de blocos que chega a 135,9 mm de balanço com 8 peças, estão no
carrossel junto com a parte que quase ninguém posta: o erro é viés de 2,7 mm, e a checagem
que julga cada candidato foi conferida contra nove formas fechadas antes de otimizar
qualquer coisa.

Estrutural é a área em que a física é mais fácil de auditar. Publicar a auditoria é o que
separa um resultado de um desenho.

Link do artigo no primeiro comentário.

`#Simulação #PhysicsAI #ElementosFinitos #Estrutural #CalculiX`

**EN**

A bumper beam against a rigid pole, 200 designs solved by the explicit solver, and a
surrogate that reads the seven design variables. On the 30 designs held out of training the
peak displacement comes out with 24.4% mean error.

The same model without the design vector goes to 41.7%. It is not a worse model: it is a
model without the information — it converges to the mean field because nothing it receives
says which design is being asked about.

That, plus the brick build that reaches 135.9 mm of overhang with 8 parts, is in the carousel
together with the part almost nobody posts: the error is a 2.7 mm bias, and the check that
judges every candidate was verified against nine closed forms before optimising anything.

Structures is the area where physics is easiest to audit. Publishing the audit is what
separates a result from a drawing.

Article link in the first comment.

`#Simulation #PhysicsAI #FiniteElement #Structural #CalculiX`

---

## 03 · Calor

**PT**

Um FNO com 1,7% de erro contra a solução de volumes finitos em 50 layouts de placa fria. E o
cartão de confiança dizendo **não**: resíduo de PDE em 0,164 contra o limite de 0,1.

Acertar o campo de referência e satisfazer a equação são duas coisas diferentes, e a segunda
é a que decide se o resultado entra num projeto.

O carrossel mostra os dois lados da transferência de calor nesta plataforma: o substituto de
dissipador que responde 227 mil vezes mais rápido com 4,46% de erro médio, o gêmeo de
permutador que avisou 2,6 horas antes com 0,216 °C de erro contra uma sonda redundante, e o
caso do CO₂ perto do ponto crítico, onde a rede mais precisa era a que quebrava a
termodinâmica em 1.100%.

Calor é fácil de desenhar e difícil de defender. Os números acima são o que temos para
defender.

Link do artigo no primeiro comentário.

`#CFD #Simulação #PhysicsAI #TransferênciaDeCalor #GêmeoDigital`

**EN**

An FNO with 1.7% error against the finite-volume solution across 50 cold-plate layouts. And
the trust card saying **no**: PDE residual at 0.164 against a 0.1 limit.

Matching the reference field and satisfying the equation are two different things, and the
second one decides whether the result enters a design.

The carousel shows both sides of heat transfer on this platform: the heat-sink surrogate that
answers 227,000 times faster at 4.46% mean error, the exchanger twin that warned 2.6 hours
ahead with 0.216 °C of error against a redundant probe, and the CO₂ case near the critical
point, where the most accurate network was the one breaking thermodynamics by 1,100%.

Heat is easy to draw and hard to defend. The numbers above are what we have to defend it
with.

Article link in the first comment.

`#CFD #Simulation #PhysicsAI #HeatTransfer #DigitalTwin`

---

## 04 · Eletromagnetismo

**PT**

Dois códigos escritos por gente diferente, com malhas diferentes, chegam ao mesmo torque: a
diferença máxima é de 1,09 N·m, ou 0,19%, em 12 posições de rotor.

E os dois se afastam do artigo publicado pela mesma quantia — 13,3 e 12,9 N·m de RMS.

É esse o resultado que vale postar. Quando dois números concordam entre si e discordam do
paper, o problema deixou de ser o código e passou a ser o modelo: geometria, materiais,
hipótese 2-D. Um número que concorda com o paper esconde onde olhar.

O carrossel traz o motor do Prius, os seis problemas de eletromagnetismo com solução exata
que rodam antes da máquina, e a parte que a área ainda não tem.

Link do artigo no primeiro comentário.

`#Eletromagnetismo #Simulação #PhysicsAI #ElementosFinitos #MáquinasElétricas`

**EN**

Two codes written by different people, on different meshes, arrive at the same torque: the
maximum difference is 1.09 N·m, or 0.19%, across 12 rotor positions.

And both drift from the published paper by the same amount — 13.3 and 12.9 N·m RMS.

That is the result worth posting. When two numbers agree with each other and disagree with
the paper, the problem stops being the code and becomes the model: geometry, materials, the
2-D assumption. A number that agrees with the paper hides where to look.

The carousel brings the Prius motor, the six electromagnetics problems with exact solutions
that run before the machine, and the part this area still does not have.

Article link in the first comment.

`#Electromagnetics #Simulation #PhysicsAI #FiniteElement #ElectricMachines`

---

## 05 · Partículas

**PT**

Três coisas que costumam ser chamadas de multifásico e não são a mesma coisa:

- tanque agitado com DEM é **partícula**, resolvida uma a uma;
- misturador Kenics é **mistura de uma fase**, transporte e concentração;
- erosão em curva de 90° é **fluido + partícula + parede**, e é o único dos três que passou
  por um ensaio publicado — dentro do fator 2, de 1,05 a 1,49 vez.

A distinção parece preciosismo até o dia em que alguém precisa decidir se contrata uma
simulação de leito fluidizado com base num vídeo bonito de partículas caindo.

O carrossel mostra o que roda, o que é análogo (colapso granular no lugar de barragem) e o
que ainda não existe nesta casa.

Link do artigo no primeiro comentário.

`#CFD #Simulação #PhysicsAI #Multifásico #DEM`

**EN**

Three things that usually get called multiphase and are not the same thing:

- a stirred tank with DEM is **particles**, resolved one by one;
- a Kenics mixer is **single-phase mixing**, transport and concentration;
- erosion in a 90° bend is **fluid + particle + wall**, and it is the only one of the three
  that met a published experiment — inside the factor-2 band, from 1.05 to 1.49 times.

The distinction sounds pedantic until the day someone has to decide whether to buy a
fluidised-bed simulation based on a nice video of falling particles.

The carousel shows what runs, what is an analogue (granular collapse instead of a dam) and
what does not exist here yet.

Article link in the first comment.

`#CFD #Simulation #PhysicsAI #Multiphase #DEM`

---

## 06 · Multifísica

**PT**

Toda plataforma de simulação diz que faz multifísica. A pergunta útil é outra: qual
acoplamento está implementado, qual está implementado em parte e qual não está.

Nesta casa, hoje:

- fluido + partícula + parede: implementado e comparado com ensaio (1,05–1,49×);
- condução + convecção: implementado, com resíduo medido e um caso reprovado;
- temperatura + tensão: parcial, os campos rodam em separado;
- eletromagnético + térmico + estrutural: parcial, só a parte magnética está medida;
- fluido + estrutura, com malha móvel: ainda não.

O carrossel explica a diferença entre acoplamento fraco e forte e por que a transferência de
campo entre malhas diferentes é onde o erro entra calado.

Prefiro uma lista com a terceira coluna a uma apresentação sem ela.

Link do artigo no primeiro comentário.

`#Simulação #PhysicsAI #Multifísica #CHT #FSI`

**EN**

Every simulation platform says it does multiphysics. The useful question is different: which
coupling is implemented, which is partly implemented and which is not.

In this house, today:

- fluid + particle + wall: implemented and compared against an experiment (1.05–1.49×);
- conduction + convection: implemented, with a measured residual and one rejected case;
- temperature + stress: partial, the fields run separately;
- electromagnetic + thermal + structural: partial, only the magnetic side is measured;
- fluid + structure, with a moving mesh: not yet.

The carousel explains the difference between weak and strong coupling and why transferring a
field between different meshes is where error slips in quietly.

I would rather have a list with that third column than a deck without it.

Article link in the first comment.

`#Simulation #PhysicsAI #Multiphysics #CHT #FSI`

---

## 07 · Vibração

**PT**

Não temos solver acústico. Ainda.

O que existe e está medido: excitação turbulenta com espectro declarado, densidade espectral
de potência, sensibilidade a rajada por aeronave, resposta modal e tensão no mesmo lugar.

O que não existe: propagação acústica, ruído radiado, transmissão por parede e metamaterial
acústico.

Publiquei o carrossel assim mesmo, com a segunda lista no segundo slide, porque a alternativa
— vender "acústica e vibrações" como se fossem a mesma coisa — estragaria o crédito da
primeira lista.

Quando a área acústica rodar, ela entra com número e limite, como as outras.

Link do artigo no primeiro comentário.

`#Simulação #PhysicsAI #Vibração #Acústica #DinâmicaEstrutural`

**EN**

We do not have an acoustic solver. Yet.

What exists and is measured: turbulent excitation with a declared spectrum, power spectral
density, gust sensitivity per aircraft, mode shape and stress in the same place.

What does not exist: acoustic propagation, radiated noise, wall transmission and acoustic
metamaterials.

I published the carousel anyway, with that second list on slide two, because the alternative
— selling "acoustics and vibration" as if they were the same thing — would spend the credit
of the first list.

When the acoustic area runs, it enters with a number and a limit, like the others.

Article link in the first comment.

`#Simulation #PhysicsAI #Vibration #Acoustics #StructuralDynamics`

---

## 08 · Materiais

**PT**

Três escalas, três métodos, três tipos de erro.

Na atômica, dinâmica molecular: o que se mede é o que as partículas fazem, e é disso que as
propriedades do contínuo precisam nascer. Na do componente, plasticidade J2 e contato
penalizado num cupom de 2.783 nós que roda num laptop. Na da propriedade, a rede que aprende
a energia de Helmholtz e mantém as seis identidades termodinâmicas abaixo de 0,0021% — contra
1.100% de violação na rede que só acerta cada número isolado.

E a quarta escala, que é a que costuma aparecer em post: trinca, fadiga e microestrutura.
Não estão implementadas. Sem elas não há propagação de trinca medida — há ilustração.

Link do artigo no primeiro comentário.

`#Materiais #Simulação #PhysicsAI #DinâmicaMolecular #MecânicaDosMateriais`

**EN**

Three scales, three methods, three kinds of error.

At the atomic scale, molecular dynamics: what gets measured is what the particles do, and
that is where continuum properties have to come from. At the component scale, J2 plasticity
and penalty contact on a 2,783-node coupon that runs on a laptop. At the property scale, the
network that learns the Helmholtz energy and keeps all six thermodynamic identities below
0.0021% — against a 1,100% violation in the network that only gets each number on its own.

And the fourth scale, the one that usually shows up in posts: crack, fatigue and
microstructure. They are not implemented. Without them there is no measured crack growth —
there is illustration.

Article link in the first comment.

`#Materials #Simulation #PhysicsAI #MolecularDynamics #SolidMechanics`

---

## 09 · Geofísica

**PT**

Reservatório e clima têm o mesmo problema de método: não existe solução analítica para
comparar. A régua passa a ser o dado observado, com janela fixa e significância declarada.

Foi isso que fizemos com o El Niño: 28 modelos de cinco famílias, os mesmos dados (OISST
v2.1), a mesma janela e o mesmo teste com correção de Holm. A 24 meses ganha um oscilador
físico de 15 parâmetros, com 0,42 de correlação de anomalia contra 0,33 do AR. As PINNs
construídas sobre o próprio oscilador ficam em −0,69 onde ele fica em 0,80.

O ranking inteiro foi publicado, incluindo as posições incômodas. É o que permite escolher
com orçamento em vez de entusiasmo.

Link do artigo no primeiro comentário.

`#Clima #Simulação #PhysicsAI #Reservatórios #Geofísica`

**EN**

Reservoir and climate share the same methodological problem: there is no analytical solution
to compare against. The yardstick becomes observed data, with a fixed window and declared
significance.

That is what we did with El Niño: 28 models from five families, the same data (OISST v2.1),
the same window and the same test with Holm correction. At 24 months a 15-parameter physical
oscillator wins, with 0.42 anomaly correlation against 0.33 for AR. The PINNs built on top of
that oscillator sit at −0.69 where it sits at 0.80.

The whole ranking is published, uncomfortable positions included. It is what lets the choice
be made with a budget instead of with enthusiasm.

Article link in the first comment.

`#Climate #Simulation #PhysicsAI #Reservoir #Geophysics`

---

## 10 · Dinâmica

**PT**

O rover travou a um terço do caminho: 42% de escorregamento e 319 mm de afundamento. O plano
direto tinha 12,9 m.

Ele mediu o escorregamento, refez o modelo do solo com um filtro de Kalman iterado,
replanejou — e chegou com 30,7 mm de afundamento. A rota nova tinha 2,2 vezes a distância e
gastou 3% menos energia. Em solo fofo o custo não é o quilômetro: é a patinagem.

O carrossel fecha a série com o que a dinâmica tem de melhor: um caso em que o caminho
ensina, o plano muda, e o relatório diz o que foi aprendido e com que erro.

Dez áreas, dez carrosséis, um critério: cada número com o limite ao lado.

Link do artigo no primeiro comentário.

`#Simulação #PhysicsAI #Dinâmica #Controle #Robótica`

**EN**

The rover stalled a third of the way in: 42% slip and 319 mm of sinkage. The direct plan was
12.9 m.

It measured the slip, rebuilt the soil model with an iterated Kalman filter, replanned — and
arrived with 30.7 mm of sinkage. The new route was 2.2 times the distance and used 3% less
energy. In soft soil the cost is not the kilometre: it is the wheel spin.

The carousel closes the series with the best dynamics has to offer: a case where the way
teaches, the plan changes, and the report states what was learned and with what error.

Ten areas, ten carousels, one criterion: every number with its limit beside it.

Article link in the first comment.

`#Simulation #PhysicsAI #Dynamics #Control #Robotics`
