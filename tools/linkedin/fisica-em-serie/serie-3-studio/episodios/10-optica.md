# EP S3-10 · Óptica — a imagem aérea de um clipe litográfico

**Área** óptica · **App** `optics_lab` (Optics Lab, construída nesta campanha) · **Duração** 4,0 s
· **Mídia** `midia/10-optica.mp4`

## O que o vídeo mostra

O Studio abrindo um sistema óptico de litografia — comprimento de onda, abertura numérica, coerência
parcial e forma da iluminação — e devolvendo a **imagem aérea** de um clipe (três linhas de 64 nm em
passo de 192 nm mais uma curva), calculada pela soma de Abbe sobre a pupila e a fonte declaradas.

O campo aparece em 3-D nos cinco planos de foco (−60, −30, 0, +30, +60 nm): a mesma imagem, vista a
cinco profundidades. O vídeo troca para **EUV** e volta para **ArF imersão**, e os números acompanham.

## O número que o episódio usa

| | ArF imersão | EUV |
|---|---|---|
| λ / NA / σ | 193 nm / 1,35 / 0,70 | 13,5 nm / 0,33 / 0,50 |
| CD impressa (máscara 64 nm) | **84,7 nm** (viés **+20,7 nm**) | **64,11 nm** (viés **+0,11 nm**) |
| NILS | **2,24** | **19,05** |
| meia-passo mínimo λ/(NA(1+σ)) | **84,1 nm** | **27,3 nm** |
| profundidade de foco / latitude | 60 nm / 0,20 | 120 nm / 0,20 |
| EPE mínima | 2,55 nm | 0,01 nm |
| tempo de cálculo | 0,53 s (121 pontos de fonte) | 1,09 s (69 pontos) |

O par é o argumento do episódio: o **mesmo clipe** está no limite em ArF imersão (k₁ = 0,67, viés de
20 nm, NILS 2,2 — apertado) e é trivial em EUV (viés de 0,1 nm, NILS 19). Não é uma opinião sobre
tecnologia: é a mesma máscara, dois sistemas ópticos, e a diferença aparece nas métricas.

## As três checagens na tela

| checagem | ArF | o que ela prova |
|---|---|---|
| ganho da máscara clara | **2,4·10⁻¹⁵** | máscara toda clara tem de imagear em exatamente 1,0 |
| modulação em 0,95× e 1,10× do limite | não modula / modula | a meia-ordem difratada entra ou não na pupila |
| Abbe × Hopkins (SOCS) | **8,7·10⁻¹⁵** | duas formulações independentes do mesmo cálculo concordam |

Mais a média da imagem contra a transmissão média da máscara (0,047). Todas PASS — e se uma falhar,
a tela mostra FALHA em vermelho, porque a checagem é a mesma que o teste da biblioteca faz.

## Roteiro

| tempo | imagem | texto na tela |
|---|---|---|
| 0–1,5 s | clipe imageado em 3-D, câmera inclinando | `193 nm · NA 1,35 · σ 0,70` |
| 1,5–2,7 s | troca para EUV, imagem mais definida | `64,11 nm · viés +0,11 nm · NILS 19,05` |
| 2,7–4 s | volta para ArF, caso apertado | `84,7 nm · viés +20,7 nm · NILS 2,24` |

## O que este episódio não afirma

- Que é imagem vetorial: o pupil é escalar, sem polarização — em NA alto isso importa e não está no
  modelo.
- Que a lente tem aberrações: além do defoco da lista, a lente é perfeita; sem flare, sem máscara 3-D.
- Que o resiste é modelado: `printed` é um limiar (opcionalmente difundido), sem química de resiste
  amplificado nem revelação.
- Que o clipe é um produto: são três linhas de 64 nm e uma curva num campo de 1024 nm.
- Que os planos do desenho estão em escala: eles estão espaçados em 0,35 µm para caber na vista; a
  faixa física é a lista de foco, −60 a +60 nm.

## Legenda (PT)

Litografia é óptica aplicada: uma máscara, uma pupila, e a pergunta de quanto do padrão sobrevive até
o wafer. Aqui o mesmo clipe — três linhas de 64 nm em passo de 192 nm — passa por dois sistemas. Em
ArF imersão (193 nm, NA 1,35) ele imprime com viés de 20,7 nm e NILS 2,24: está no limite. Em EUV
(13,5 nm, NA 0,33) o viés cai para 0,11 nm e o NILS sobe para 19.

A tela não pede confiança: mostra a máscara clara imageando em 2,4·10⁻¹⁵, a modulação virando
exatamente no limite λ/(NA(1+σ)), e a soma de Abbe batendo com os kernels de Hopkins em 8,7·10⁻¹⁵.

`#Óptica #Litografia #Semicondutores #Simulação #PhysicsAI #PINNeAPPle`

## Legenda (EN)

Lithography is applied optics: a mask, a pupil, and the question of how much of the pattern survives
to the wafer. Here the same clip — three 64 nm lines at 192 nm pitch — goes through two systems. In
ArF immersion (193 nm, NA 1.35) it prints with a 20.7 nm bias and NILS 2.24: at the limit. In EUV
(13.5 nm, NA 0.33) the bias drops to 0.11 nm and NILS rises to 19.

The screen does not ask for trust: it shows the clear mask imaging to 2.4·10⁻¹⁵, the modulation
turning exactly at λ/(NA(1+σ)), and the Abbe sum matching the Hopkins kernels to 8.7·10⁻¹⁵.

`#Optics #Lithography #Semiconductors #Simulation #PhysicsAI #PINNeAPPle`
