# Série 3 · Physics in Action no Studio

Sete episódios, um por área principal da física, **gravados dentro do PINNeAPPle Studio**
(`pinneapple-engineering-api`): cada app é um serviço real, o botão que aparece no vídeo roda o
solver de verdade, e o campo em 3-D que gira na tela é o que a app serve depois que o job termina.
Nada aqui é gráfico de matplotlib.

Os vídeos estão em [`midia/`](midia/), as fichas (roteiro, número medido, limites e legendas PT/EN)
em [`episodios/`](episodios/).

## Os sete episódios

| # | área | app | o que aparece | vídeo |
|---|---|---|---|---|
| 01 | eletromagnetismo | `afpm_designer` | motor de fluxo axial, \|B\| em 3-D sobre 15.728 triângulos, cogging do estimate contra o 3-D | [6 s](midia/01-eletromagnetismo.mp4) |
| 02 | aerodinâmica externa | `ahmed_twin` | corpo de Ahmed em 3-D, Cp na superfície, sliders de inclinação/folga/velocidade | [7 s](midia/02-aerodinamica-externa.mp4) |
| 03 | aviação | `aero_optimizer` | aeronave em 3-D com Cp do OpenFOAM, 47,9 g CO₂/pkm certificável | [4,7 s](midia/03-aviacao.mp4) |
| 04 | térmico de trocador | `heatsink_sizer` | 38.301 candidatos → 414 → 24 verificados, campo em 3-D nas aletas | [6,2 s](midia/04-termico-trocador.mp4) |
| 05 | térmico de eletrônica | `pcb_hotspot` | placa com FPGA/DDR em 3-D, Tj por parte, margem e balanço de energia | [5 s](midia/05-termico-eletronica.mp4) |
| 06 | acústica | `soundshape_ai` | duto bass-reflex em 3-D, Helmholtz ao vivo, otimizador conferido na fórmula | [5 s](midia/06-acustica.mp4) |
| 07 | freio / mobilidade | `brakecool_ai` | rotor ventilado em 3-D, 112 → 65 °C, Monte Carlo de tolerância | [9 s](midia/07-freio.mp4) |

Cada episódio tem um `.jpg` de pôster com o mesmo nome.

## Como um episódio é gravado

O gravador é [`gravar.py`](gravar.py) — Playwright dirigindo a página, não captura de tela:

```bash
# 1. subir as apps (cada uma é um serviço FastAPI)
cd PINNeAPPle/apps/afpm_designer && PYTHONPATH=../..:../_shared \
  uvicorn afpm_designer.api:app --port 8191          # as portas estão em PORTAS, no gravar.py

# 2. gravar
python gravar.py brakecool      # brakecool | soundshape | heatsink | pcb | afpm
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

## Ambiente desta máquina

- As apps rodam nativas com `uvicorn` (sem build de Docker), que é mais rápido para gravar.
- O `afpm_designer` é o episódio caro: o job de verificação leva ~4,5 min por rodada.
- O `ahmed_twin` só sobe com a pasta `_runs/cfd` do estudo presente; o vídeo 02 veio da sessão em
  que esses dados estavam disponíveis (nesta cópia do repositório eles não estão).
- Nenhum episódio usa dado de cliente: os casos são de referência (corpo de Ahmed, motor de fluxo
  axial, placa com FPGA/DDR, dissipador extrudado, duto bass-reflex, rotor ventilado).
