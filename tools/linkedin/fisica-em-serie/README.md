# Duas séries de posts · The Physics Atlas + Physics in Action

Material completo de duas séries editoriais para o LinkedIn, construídas sobre o acervo real do
PINNeAPPle. Não é um plano a executar: o texto dos 20 posts está escrito, os carrosséis da Série 1
estão renderizados em PNG/JPG prontos para subir, e os roteiros da Série 2 dizem, caso por caso,
o que já pode ser filmado e o que precisa rodar antes.

| | Série 1 — **The Physics Atlas** | Série 2 — **Physics in Action** |
|---|---|---|
| formato | 10 carrosséis, 8 slides, 1080×1350 | 10 vídeos de 40–50 s |
| prova | amplitude: dez domínios, cada número com o limite ao lado | profundidade: um caso ambicioso por episódio |
| estado | **pronto** — PNG/JPG renderizados, PT e EN | **roteiro** — 3 parcialmente prontos, 7 a produzir |
| pasta | [`serie-1/`](serie-1/) | [`serie-2/`](serie-2/) |

## A regra que vale para tudo

Cada imagem e cada slide diz **o que ele é**, com uma etiqueta na própria arte:

| etiqueta | significa |
|---|---|
| `SOLVER` | resultado de um solver de referência desta casa |
| `SURROGATE` | previsão de modelo de IA, com o erro declarado |
| `EXPERIMENTO` | comparação com ensaio publicado, com o fator ao lado |
| `STUDIO` | captura do PINNeAPPle Studio |
| `CONCEITUAL` | ilustração; nenhum número é atribuído |

E o último slide de cada carrossel é sempre "o que este carrossel não está dizendo". Essa é a
marca: o resultado vem com o limite, e a lacuna é publicada em vez de escondida.

## Os dez domínios

| # | domínio | número que ancora o carrossel |
|---|---|---|
| 01 | CFD e aerodinâmica | −15,7% de arrasto em 20 rodadas; −13,9% na malha fina |
| 02 | Mecânica estrutural | 24,4% de erro no pico do crash; 135,9 mm de balanço |
| 03 | Calor | 1,7% de erro e **REJECT** no resíduo; 227.059× mais rápido |
| 04 | Eletromagnetismo | 0,19% entre dois solvers; ~13 N·m de desvio do paper |
| 05 | Multifásicos e partículas | 1,05–1,49× o ensaio de erosão de Vieira et al. |
| 06 | Multifísica | o que está acoplado, o que está em parte e o que não está |
| 07 | Acústica e vibrações | espectro, rajada e resposta — e a ausência do solver acústico |
| 08 | Materiais | identidades termodinâmicas abaixo de 0,0021% |
| 09 | Geofísica e energia | 0,42 de correlação do El Niño contra 0,33 do AR |
| 10 | Sistemas dinâmicos | 30,7 mm de afundamento contra 319 mm; τ 0,94 de alerta |

## Calendário

Duas publicações por semana, terça e quinta, 9h de Brasília. O intervalo entre elas é o que
permite responder comentário — e comentário respondido é o que faz o post seguinte render.

| semana | terça | quinta |
|---|---|---|
| 24/11 | 01 CFD | 02 Estrutural |
| 01/12 | 03 Calor | 04 Eletromagnetismo |
| 08/12 | 05 Partículas | 06 Multifísica |
| 15/12 | 07 Vibração | 08 Materiais |
| *recesso* | — | — |
| 05/01 | 09 Geofísica | 10 Dinâmica |

A Série 2 começa depois, um episódio por semana, às terças, a partir de 12/01/2027 — e na ordem
de prontidão, não na ordem de impacto: **01 CO₂ no subsolo → 02 colapso estrutural → 03 barragem
→ 04 turbulência na aeronave → 05 foguete supersônico → 06 reentrada → 07 motor elétrico → 08
metamaterial → 10 pouso → 09 trinca**. Os dois últimos fecham a série porque são os mais
distantes de rodar; o 09 é o único que não vai ao ar antes de ter número.

## Três formatos recorrentes

Servem para reaproveitar qualquer experimento, sem inventar caso novo:

1. **Physics vs AI** — solver de um lado, surrogate do outro, mapa de erro e métrica no meio.
   Já existe pronto para CFD (`aero-autonoma-trust`), crash (`crash-pico`) e calor
   (`fno-checagens`).
2. **Inside the Simulation** — um fenômeno explicado em 6 quadros: vórtice de ponta de asa,
   esmagamento axial, frente de onda.
3. **Can We Trust This Simulation?** — conservação, convergência, domínio de validade e o caso
   em que a checagem reprovou. O artigo `guardrail-veriphysics` é o molde.

## Como publicar um carrossel

1. Suba os 8 JPG de `serie-1/img/<slug>-pt-01.jpg` a `-08.jpg`, nesta ordem.
2. Cole a legenda de [`serie-1/legendas.md`](serie-1/legendas.md) no campo de texto.
3. O link do artigo vai no **primeiro comentário** — o LinkedIn reduz o alcance de post com link
   no corpo. A legenda já termina dizendo isso.
4. Se for publicar em inglês, use os arquivos `-en-*` com a legenda EN. São posts separados, não
   tradução no mesmo post.
5. Responda comentário técnico com número, não com "obrigado pelo comentário". É o que a série
   toda promete.

## Como mexer no material

O JSON é a fonte de verdade do carrossel; o PNG é derivado.

```bash
cd PINNeAPPle-Labs.github.io
/opt/homebrew/bin/python3.11 tools/linkedin/fisica-em-serie/serie-1/build.py --checar
/opt/homebrew/bin/python3.11 tools/linkedin/fisica-em-serie/serie-1/build.py            # tudo
/opt/homebrew/bin/python3.11 tools/linkedin/fisica-em-serie/serie-1/build.py --so 03-calor --langs pt
```

- `--checar` confere mídia ausente, campo vazio e número de slides fora da faixa.
- `--revisao` escreve `serie-1/revisao/<slug>.md`, a copy em texto para ler e corrigir.
- `--png` guarda também o master 2160×2700; por padrão só o JPG de 1080×1350 fica.
- Editar texto: `serie-1/carrosseis/<slug>.json`. O campo pode ser string ou `{pt, en}`.
- Trocar imagem: `serie-1/midia/`. Toda mídia é **cópia local** — nada quebra se o outro repo
  mudar de lugar.
- Mexer no desenho do slide: `serie-1/card.html` (fonte, cor, espaçamento). As cores são as da
  marca (`#262626`, `#0081be`, `#a23a00`, tintas `#e07a3c` e `#3fa9dc`).

## O que medir

Não medir curtida. Medir, por post:

- **comentário técnico** — pergunta sobre método, erro ou domínio de validade. É o único sinal
  que diz que a série atingiu engenheiro, e não só quem passa o dedo;
- **clique no artigo** (primeiro comentário) — diz qual domínio puxa tráfego para o site;
- **inscrição na lista de pré-acesso** com a origem marcada — o número que o comercial usa.

O que a série deve produzir, ao fim dos 20 posts: dez domínios testados para saber onde o
público responde, três formatos recorrentes prontos para repetir, e um conjunto de figuras
publicadas com etiqueta de origem — que é o ativo mais difícil de copiar.

## Arquivos

```
fisica-em-serie/
  README.md            este documento
  midia.md             inventário de mídia: o que existe, onde está e o que falta produzir
  serie-1/
    card.html          template do slide
    build.py           renderiza PNG/JPG e escreve a revisão em markdown
    carrosseis/*.json  os 10 carrosséis (fonte de verdade)
    legendas.md        as 20 legendas (PT/EN)
    midia/             cópias locais das imagens usadas
    img/               saída: <slug>-<lang>-NN.jpg
    revisao/           a copy em markdown, gerada
  serie-2/
    01..10-*.md        os 10 roteiros de vídeo
```
