# EP S3-08 · Mecânica dos sólidos — o braço de suspensão

**Área** mecânica dos sólidos / fadiga · **App** `ridetune_ai` (RideTune AI) · **Duração** 6,4 s
· **Mídia** `midia/08-mecanica-solidos.mp4`

## O que o vídeo mostra

Um braço de suspensão modelado como viga engastada, em 3-D, com a **tensão de flexão viva ao longo do
comprimento**: o topo da cor é o engaste, o verde claro é a ponta livre, e a seta verde é a força
aplicada. Os sliders mexem na seção transversal (largura e espessura) e a cor da viga muda junto,
porque a tensão muda junto.

Depois o **Optimize with AI** devolve o projeto mais leve que ainda cumpre a vida de fadiga, e o
**Run sensitivity analysis** responde à pergunta que decide o projeto: qual das duas variáveis manda.

## O número que o episódio usa

Carga cíclica de 1200 N, alvo de 10⁶ ciclos, aço mola (σ_f' = 1200 MPa, b = −0,09), braço de 0,35 m.

| ponto | seção | tensão de flexão | vida | massa |
|---|---|---|---|---|
| projeto de partida | 50,0 × 22,0 mm | 104,1 MPa | 3,12·10¹¹ | 3022 g |
| exploração manual (fim) | 32,0 × 14,0 mm | **401,8 MPa** | **9,52·10⁴** | 1231 g — mais leve, e **falha** |
| otimizado e re-verificado | 45,5 × 17,5 mm | 185,0 MPa | 5,58·10⁸ | **2169 g** (28% mais leve) |

`σ = 6FL/(wt²)`, e a vida vem de Basquin. O surrogado previu 185,0 MPa contra 184,0 MPa da fórmula
fechada (0,5%), e a vida de 5,58·10⁸ ciclos é 558× o alvo de 10⁶.

A análise de sensibilidade é a parte que um engenheiro leva para a reunião: as elasticidades saem
**11,11 para a largura e 22,22 para a espessura** — a vida é exatamente **2,00× mais sensível à
espessura** que à largura neste ponto (e o número −2/b = 22,2 é o que a teoria manda). Ou seja: a
largura é inútil para ganhar vida; a espessura é o único botão.

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–1,5 s | viga em 3-D girando, campo de tensão | `1200 N · 10⁶ ciclos` |
| 1,5–3 s | sliders descendo, viga ficando vermelha | `104,1 → 401,8 MPa` |
| 3–4,5 s | otimizador e verificação | `3022 g → 2169 g · 28% mais leve` |
| 4,5–6,4 s | elasticidades | `espessura 22,22 · largura 11,11` |

## O que este episódio não afirma

- Que é FEA: a tensão é a fórmula fechada de viga engastada com seção reta, sem concentração de
  tensão, sem contato, sem 3-D. O campo em 3-D é a distribuição ao longo do comprimento, não uma
  solução de elementos finitos.
- Que o projeto do otimizador é o mais leve possível: **não é**. O próprio README da app declara que
  o Adam para dentro da região viável e que o mínimo da fórmula fechada é ~0,73 kg contra os 2,17 kg
  entregues — a verificação checa segurança, não otimalidade.
- Que a vida de 5,58·10⁸ ciclos é vida real: Basquin extrapola, não há limite de fadiga, e não há
  ensaio de bancada nem dado de estrada.
- Que a exploração manual terminou num projeto bom: ela terminou em 401,8 MPa, acima do admissível —
  é o vídeo mostrando o que acontece quando se aperta o slider sem olhar o número.

## Legenda (PT)

Um braço de suspensão, 1200 N cíclicos, alvo de um milhão de ciclos. A viga em 3-D mostra a tensão
de flexão ao longo do comprimento: vermelho no engaste, verde na ponta.

O que acontece quando você aperta o slider: a seção cai para 32 por 14 mm e a tensão sobe para
401,8 MPa — acima do admissível, vida de 9,5·10⁴ ciclos, 1231 g. Mais leve, e reprova. O otimizador então devolve 45,5 por
17,5 mm: 2169 g, 28% mais leve, 185 MPa e 558 vezes a vida pedida.

E a análise de sensibilidade fecha a conta: elasticidade 22,2 na espessura contra 11,1 na largura. A
vida é exatamente duas vezes mais sensível à espessura. A largura era o botão errado.

`#MecânicaDosSólidos #Fadiga #Suspensão #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

A suspension arm, 1200 N cyclic, a one-million-cycle target. The 3-D beam shows bending stress along
its length: red at the fixed end, green at the tip.

What happens when you push the slider: the section drops to 32 by 14 mm and stress climbs to
401.8 MPa — above the allowable, life down to 9.5·10⁴ cycles. It fails. The optimiser then returns
45.5 by 17.5 mm: 2169 g, 28% lighter, 185 MPa, 558 times the life asked for.

And the sensitivity analysis closes it: elasticity 22.2 on thickness against 11.1 on width. Life is
exactly twice as sensitive to thickness. Width was the wrong button.

`#SolidMechanics #Fatigue #Suspension #Simulation #PhysicsAI #PINNeAPPle`
