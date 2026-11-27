# Série 3 · Physics in Action no Studio

Episódios **gravados dentro do PINNeAPPle Studio** (`pinneapple-engineering-api`), com as apps
reais rodando, não com gráficos de matplotlib. A diferença em relação à Série 2 é o que a tela
mostra: casos industriais, campo em 3-D e o número saindo do próprio app enquanto a câmera roda.

## Como um episódio é gravado

1. **Subir a app do domínio** (cada uma é um serviço FastAPI):

   ```bash
   # sem Docker, com as dependências do app instaladas
   cd PINNeAPPle/apps/<app> && PYTHONPATH=../..:../_shared \
     uvicorn <app>.api:app --port <porta>

   # ou pela imagem (Docker Desktop precisa estar de pé)
   cd PINNeAPPle && docker build -f apps/<app>/Dockerfile -t <app> . \
     && docker run -p <porta>:<porta> <app>
   ```

2. **Dirigir a página com Playwright**: preencher o formulário, clicar no botão que roda o
   solver, esperar o job terminar (a maioria é fila, com progresso), orbitar o campo 3-D com o
   mouse e capturar quadro a quadro.
3. **Codificar** com ffmpeg e guardar em `midia/`.

O job é sempre um job de verdade: `POST /api/<job>` devolve um id, o app reporta `progress` e o
campo em 3-D só existe depois que o solver termina.

## O que já está validado

| app | domínio | o que aparece | estado |
|---|---|---|---|
| `ahmed_twin` | aerodinâmica externa | Ahmed body em 3-D, Cp na superfície, CD/CL com faixa de 90% | **gravado** (`piloto-ahmed-3d.mp4`) |
| `afpm_designer` | eletromagnetismo | motor de fluxo axial, \|B\| em 3-D, cogging, Estimate × 3-D | **validado** (`prova-afpm-3d-*.png`) |
| `pcb_hotspot` | térmico de eletrônica | placa com FPGA/DDR/LDO, Tj, margem por componente | **validado** (`prova-pcb-hotspot.png`), mapa 2-D |
| `heatsink_sizer` | térmico de trocador | dimensionamento de dissipador com banda de convecção | roda |
| `soundshape_ai` | acústica | — | roda |

O `afpm_designer` mede o que o episódio precisa: o estimate quasi-3-D **superestima** o cogging
em 12,8% (8,604 contra 7,626 N·m) e o fluxo em 2,1% — e o app diz isso na própria tela.

## O que falta

- Gravar os episódios restantes no formato acima (cada um tem um custo de solver: o 3-D do motor
  leva ~4,5 min por rodada).
- `aero_optimizer` (A320) e `brakecool_ai` (disco de freio) precisam da imagem Docker e, no caso
  do avião, de OpenFOAM para a checagem.
- Nenhum episódio usa dado de cliente: os casos são benchmarks industriais públicos (Ahmed body,
  motor de fluxo axial, placa com FPGA/DDR).

## Ambiente desta máquina

- Docker Desktop: daemon de pé, 10 CPUs, 7,75 GB — a imagem `afpm-designer` foi construída com
  sucesso (contexto de 6 GB, ~2 min de build).
- As apps também rodam nativas com `uvicorn`, que é mais rápido para gravar (sem build).
