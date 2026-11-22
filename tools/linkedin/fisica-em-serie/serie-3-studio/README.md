# Série 3 · Physics in Action no Studio

Dez episódios, um por área principal da física, **gravados dentro do PINNeAPPle Studio**
(`pinneapple-engineering-api`): cada app é um serviço real, o botão que aparece no vídeo roda o
solver de verdade, e o campo em 3-D que gira na tela é o que a app serve depois que o job termina.
Nada aqui é gráfico de matplotlib.

Os vídeos estão em [`midia/`](midia/), as fichas (roteiro, número medido, limites e legendas PT/EN)
em [`episodios/`](episodios/).

## Os dez episódios

| # | área | app | o que aparece | vídeo |
|---|---|---|---|---|
| 01 | eletromagnetismo | `afpm_designer` | motor de fluxo axial, \|B\| em 3-D sobre 15.728 triângulos, cogging do estimate contra o 3-D | [5,7 s](midia/01-eletromagnetismo.mp4) |
| 02 | aerodinâmica externa | `ahmed_twin` | corpo de Ahmed em 3-D, Cp na superfície, sliders de inclinação/folga/velocidade | [7 s](midia/02-aerodinamica-externa.mp4) |
| 03 | aviação | `aero_optimizer` | aeronave em 3-D com Cp do OpenFOAM, 47,9 g CO₂/pkm certificável | [4,7 s](midia/03-aviacao.mp4) |
| 04 | térmico de trocador | `heatsink_sizer` | 38.301 candidatos → 414 → 24 verificados, campo em 3-D nas aletas | [6,2 s](midia/04-termico-trocador.mp4) |
| 05 | térmico de eletrônica | `pcb_hotspot` | placa com FPGA/DDR em 3-D, Tj por parte, margem e balanço de energia | [5 s](midia/05-termico-eletronica.mp4) |
| 06 | acústica | `soundshape_ai` | duto bass-reflex em 3-D, Helmholtz ao vivo, otimizador conferido na fórmula | [5 s](midia/06-acustica.mp4) |
| 07 | freio / mobilidade | `brakecool_ai` | rotor ventilado em 3-D, 112 → 65 °C, Monte Carlo de tolerância | [9 s](midia/07-freio.mp4) |
| 08 | mecânica dos sólidos | `ridetune_ai` | viga de suspensão em 3-D com tensão viva, 3022 → 2169 g e a sensibilidade que decide | [6,4 s](midia/08-mecanica-solidos.mp4) |
| 09 | astronomia | `observatory` | céu de São Paulo em 3-D (JPL DE421), Lua a 371.661 km, sistema solar com o tempo andando | [5,3 s](midia/09-astronomia.mp4) |
| 10 | óptica | `optics_lab` | imagem aérea de litografia em 3-D através do foco, CD/NILS/janela de processo, Abbe × Hopkins | [4 s](midia/10-optica.mp4) |

Cada episódio tem um `.jpg` de pôster com o mesmo nome.

## Como um episódio é gravado

O gravador é [`gravar.py`](gravar.py) — Playwright dirigindo a página, não captura de tela:

```bash
# 1. subir as apps (cada uma é um serviço FastAPI)
cd PINNeAPPle/apps/afpm_designer && PYTHONPATH=../..:../_shared \
  uvicorn afpm_designer.api:app --port 8191          # as portas estão em PORTAS, no gravar.py

# 2. gravar
python gravar.py brakecool      # brakecool | soundshape | heatsink | pcb | afpm | ridetune | observatory | optics
```

O que o gravador faz, por episódio:

1. abre a app, espera a página;
2. executa a interação real — preenche requisito, clica no botão que submete o job, espera a fila
   (`_esperar_texto` acompanha o painel de resultado em vez de dormir um tempo fixo);
3. arrasta o mouse sobre o canvas em arco (`Gravador.orbita`), capturando um quadro PNG por passo, e
   rola a página devagar quando o resultado está abaixo da dobra (`Gravador.rolar`);
4. codifica com ffmpeg em 1200 px de largura, 30 fps, `yuv420p`.

Os quadros ficam em `/tmp/grav_<episódio>/`; o corte (`clip`) é escolhido por episódio para deixar no
enquadramento o campo **e** o número que o campo produz.

## O que os números dizem (e o que não dizem)

Todos os episódios publicam o limite junto do número, e as fichas em `episodios/` repetem isso:

- **01** o estimate quasi-3-D **superestima o cogging em 12,8%** (8,604 contra 7,626 N·m) e o fluxo
  em 2,1% — e o app mostra o desvio na própria tela.
- **02** o twin foi treinado com **73 corridas OpenFOAM k-omega SST**; em 40° ele cai exatamente
  sobre um caso de treino (distância 0,00) e o CD 0,2987 é o CFD, não interpolação. Em 25°, CD
  0,2954, na faixa experimental clássica.
- **03** o Cp é de uma corrida guardada de OpenFOAM, não de um solver no navegador.
- **04** a triagem não é o resultado: os 24 projetos que sobram são recalculados pela física, com
  ±15% de pessimismo na convecção; erro da triagem contra a física, 0,30 °C na média.
- **05** o app avisa que FPGA, DDR1 e LDO passam nominalmente e **não passam com 20% menos
  refrigeração**.
- **06** o ar no duto não tem gradiente (modelo concentrado) e a fronteira de compromisso **colapsa**
  neste ponto de operação — as duas coisas estão escritas na ficha.
- **07** o veredito do Monte Carlo depende de um limite genérico de 500 °C; o número que importa é o
  espalhamento, ±0,2 °C.
- **08** o otimizador **não** acha o mínimo: o próprio README da app declara 0,73 kg no ótimo da
  fórmula fechada contra 2,17 kg entregues, porque a verificação checa segurança e não otimalidade.
  O que o vídeo entrega é a elasticidade: espessura 22,2 contra largura 11,1.
- **09** as posições são aparentes e topocêntricas, não astrométricas — e o próprio README da app
  reprova o propagador aprendido para muitos NEOs (1,2× melhor que Kepler contra um portão de 5×).
- **10** a imagem é escalar (sem polarização) e a lente é perfeita além do defoco; os três checagens
  na tela são as mesmas do teste da biblioteca. O mesmo clipe tem viés de 20,7 nm em ArF imersão e
  0,11 nm em EUV — os planos do desenho estão espaçados para a vista, não em escala.

## Ambiente desta máquina

- As apps rodam nativas com `uvicorn` (sem build de Docker), que é mais rápido para gravar.
- O `afpm_designer` é o episódio caro: o job de verificação leva ~4,5 min por rodada.
- O `optics_lab` é uma app **nova**, construída para esta série (está em `PINNeAPPle/apps/optics_lab`,
  sobre `pinneapple_physics.lithography`): sobe com `uvicorn optics_lab.api:app --port 8166`.
- O `observatory` precisa do kernel JPL DE421: `pip install skyfield-data` (ou `PINNEAPPLE_DE_KERNEL`
  apontando para um `.bsp`). Sem ele a app não sobe.
- O `ahmed_twin` só sobe com a pasta `_runs/cfd` do estudo presente. Esta cópia **foi refeita**: a
  campanha roda com o OpenFOAM **nativo arm64** (`brew install --cask gerlero/openfoam`), ~150× mais
  rápido que a imagem amd64 do Docker — uma corrida de 1.000 iterações passa de horas para minutos. A
  ressalva anterior deste README ("refazer exigiria dias") estava errada e fica corrigida aqui.
  A pasta `_runs/` continua fora do git (é dado, não código): quem clona precisa rodar a campanha.
- Nenhum episódio usa dado de cliente: os casos são de referência (corpo de Ahmed, motor de fluxo
  axial, placa com FPGA/DDR, dissipador extrudado, duto bass-reflex, rotor ventilado, viga de
  suspensão, céu de São Paulo).

## Versão 9:16 e proveniência

- `vertical.py` compõe a versão 1080×1920 de cada episódio em `midia-vertical/`: fundo da marca, o
  vídeo 16:9 inteiro em 1080 de largura, o gancho em cima e, no pé, o que o episódio **não** afirma.
  Não é recorte — recortar comeria justamente o número que dá sentido ao vídeo.
- `manifesto.py` escreve `midia/<episódio>.manifest.json` (schema `pinneapple.cinema.media/1`) com o
  SHA-256, a duração e o tamanho **medidos** de cada produto, mais o app, o commit do app e o número
  que a ficha publica. Com `--biblioteca` ele também escreve `apps/<app>/cinema.json` no checkout da
  biblioteca, que é o que faz a galeria do Studio entregar a mídia.
- `cinema.py` é o ponto de entrada único: `estado` mostra o que existe por episódio sem gerar nada,
  `vertical` / `tecnico` / `manifesto` rodam cada etapa e `tudo` encadeia as três na ordem.
- `tecnico.py` monta o **produto B**: 60 s em 16:9, em cinco blocos — título, a gravação com o número
  na faixa de baixo, como o número foi medido, a verificação que a página mostra, e o que o vídeo não
  afirma. Sai em `midia-tecnica/`.
- O portão de mídia reconstrói esses números (`node verify.js` no espelho do `take-a-piece`): clip
  trocado, manifesto velho, arquivo fora do manifesto ou episódio sem ressalva quebram a verificação.

Os três produtos de Cinema por episódio: `screen-16x9` (a gravação crua), `short-9x16` (4 a 9 s, com
gancho) e `technical-16x9` (60 s, cartelas cronometradas). O short ainda está abaixo dos 15–30 s que a
especificação pede: chegar lá exige capturar mais interação real (e, no `afpm_designer`, mais minutos de
job), não repetir quadro para encher duração.

