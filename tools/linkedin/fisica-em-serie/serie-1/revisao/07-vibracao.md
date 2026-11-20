# 07 · Vibração: o que a plataforma mede, e o que ela ainda não mede

_The Physics Atlas · PINNeAPPle · carrossel 7 de 10_

## Slide 1 — capa
`The Physics Atlas · 07/10 · Vibração`

**PT** — A estrutura responde. A pergunta é a quanto.
  Excitação, espectro e resposta — e uma área que ainda não está pronta, dita com essas palavras.
  `midia/vib-cantilever.jpg`

**EN** — The structure responds. The question is by how much.
  Excitation, spectrum and response — and one area that is not ready yet, said in those words.

## Slide 2 — texto
`A posição honesta`

**PT** — Não há solver acústico nesta plataforma. Ainda.
  - O que **existe e está medido**: resposta dinâmica, excitação turbulenta, espectro, sensibilidade a rajada e modos.
  - O que **não existe**: propagação acústica, ruído radiado, transmissão por parede e metamaterial acústico.
  - Publicar a segunda lista é o que dá crédito à primeira — e é a regra da casa desde o primeiro artigo.

**EN** — There is no acoustic solver on this platform. Yet.
  - What **exists and is measured**: dynamic response, turbulent excitation, spectra, gust sensitivity and modes.
  - What **does not exist**: acoustic propagation, radiated noise, wall transmission and acoustic metamaterials.
  - Publishing the second list is what gives the first one credit — and it has been the house rule since the first article.

## Slide 3 — media
`A excitação`

**PT** — Turbulência atmosférica como entrada
  Séries de rajada geradas com o espectro de von Kármán para três intensidades. A estrutura não escolhe o que a excita: quem escolhe é o modelo de turbulência, e ele precisa estar declarado.
  PINNeAPPle · examples/flight_dynamics
  [SOLVER]
  `midia/vib-traces.png`

**EN** — Atmospheric turbulence as input
  Gust series generated with the von Kármán spectrum at three intensities. The structure does not choose what excites it: the turbulence model does, and it has to be declared.
  PINNeAPPle · examples/flight_dynamics

## Slide 4 — media
`O espectro`

**PT** — Onde a energia está, e onde a estrutura sofre
  A densidade espectral de potência é o que liga a excitação à resposta: sem ela, comparar duas aeronaves é comparar desenhos. Com ela, é comparar amplitudes em cada faixa.
  [SOLVER]
  `midia/vib-psd.png`

**EN** — Where the energy is, and where the structure suffers
  The power spectral density is what links excitation to response: without it, comparing two aircraft is comparing drawings. With it, it is comparing amplitudes in each band.

## Slide 5 — media
`A resposta`

**PT** — Sensibilidade a rajada, por aeronave
  A mesma rajada, aplicada a geometrias diferentes, dá respostas diferentes — e é isso que a análise serve para dizer antes do voo, em vez de depois.
  [SOLVER]
  `midia/vib-gust.png`

**EN** — Gust sensitivity, per aircraft
  The same gust, applied to different geometries, gives different responses — and that is what the analysis is for: saying it before the flight, instead of after.

## Slide 6 — media
`O modo`

**PT** — von Mises numa viga em balanço
  Forma modal e tensão no mesmo lugar. A frequência própria é o que decide se a excitação de um lado do espectro vai encontrar a estrutura do outro.
  CalculiX · viga em balanço
  [SOLVER]
  `midia/vib-cantilever.jpg`

**EN** — von Mises on a cantilever beam
  Mode shape and stress in the same place. The natural frequency is what decides whether the excitation on one side of the spectrum meets the structure on the other.
  CalculiX · cantilever beam

## Slide 7 — media
`O mínimo denominador`

**PT** — Do pêndulo ao amortecimento
  Todo método de dinâmica se confere primeiro onde a resposta é conhecida: oscilador, amortecimento, ressonância. Foi assim que as cinco ferramentas do kit foram auditadas.
  artigos/ferramentas-de-dinamica
  [SOLVER]
  `midia/vib-pendulo.png`

**EN** — From pendulum to damping
  Every dynamics method is checked first where the answer is known: oscillator, damping, resonance. That is how the five tools in the kit were audited.
  artigos/ferramentas-de-dinamica

## Slide 8 — fecho
`Antes de fechar`

**PT** — O que este carrossel não está dizendo
  - Não há resultado de ruído radiado nem de transmissão acústica publicado — porque não foi medido.
  - A turbulência aqui é sintética, com espectro declarado: não é atmosfera real medida em voo.
  - Quando a área acústica rodar, ela entra neste carrossel com número e limite, como as outras.

**EN** — What this carousel is not saying
  - There is no published radiated-noise or acoustic-transmission result — because it has not been measured.
  - The turbulence here is synthetic, with a declared spectrum: it is not real atmosphere measured in flight.
  - When the acoustic area runs, it enters this carousel with a number and a limit, like the others.
