# Physics Cinema — auditoria dos dois repositórios

Medições de **2026-11-21**, feitas nesta máquina: contagem de arquivos, rotas lidas do código e do servidor
rodando, e uma gravação real de cada app citada. Onde o número veio de execução, está dito; onde veio de
leitura de código, também.

| repositório | clone | estado auditado |
|---|---|---|
| `PINNeAPPle` | `~/Documents/GitHub/pinneapple-labs/PINNeAPPle` | `feat/launch-ascent` (2 à frente, 31 atrás) + worktree limpo `wt-optics-lab` |
| `pinneapple-engineering-api` | `~/Documents/GitHub/pinneapple-labs/pinneapple-engineering-api` | `feat/pipeline-advisor-api`, mais 3 worktrees |

## 1. PINNeAPPle (motor científico)

### O que existe e roda

| ativo | medida | estado |
|---|---|---|
| pacotes `pinneapple*` | 18 (physics, neural, simulation, analysis, design, tools, catalog, lab, flow, reason, …) | funcional |
| `examples/` | **113 pastas**, **174 `experiment.json`** | manifeto válido por portão de CI |
| `apps/` | **67 apps** de Studio, cada uma um serviço FastAPI | roda nativo e em imagem |
| campos em 3-D | `pinneapple_tools.visualization.studio` (`Scene`, `field_view`) → glTF com atributos `_F0…` | funcional, usado por 20+ apps |
| gates | `check_app_helpers.py`, `check_experiment_manifests.py`, `pinneapple check`, ruff | rodam local (CI do GitHub morto por billing) |

### O que é experimental e diz isso

- `pinneapple_autolab` (o estudo do Ahmed, o DOE, o twin) emite `ExperimentalWarning` e declara API instável.
- `pinneapple_catalog` mantém o status por método; **"testado" não é "validado"** — o catálogo é a autoridade.

### O que **não** existe

- Nenhum pacote de produção de mídia: nada de render de vídeo, carrossel ou thumbnail na biblioteca. A mídia
  desta campanha vive fora dela (ver §3).
- Nenhum contrato único de "experimento de demonstração": `experiment.json` cobre ciência, não mídia.

## 2. pinneapple-engineering-api (orquestração)

### O que existe e roda

| rota | o que entrega | medida |
|---|---|---|
| `GET /v1/studio/gallery` | catálogo de demonstrações, com filtro por `kind` (`example`/`reproduction`/`app`), `state` e busca `q` | **173 entradas** (65 apps + 108 exemplos) medidas no servidor de 2026-11-21 |
| `GET /v1/studio/gallery/{id}` | entrada completa (descrição PT/EN, domínio, `measured`, `flows`, `thumbs`) | — |
| `GET /v1/studio/coverage`, `/tree`, `/tools/{id}`, `/glossary`, `/summary` | cobertura, árvore de pacotes, cartão por ferramenta | 217 ferramentas com razão registrada em `pinneapple_studio/tool_reasons.json` |
| `GET /v1/studio/thumbs/{sha}` | preview WebP por SHA da figura | cacheado por um ano |
| jobs | `POST` + polling de progresso (`appkit`) | usado pelas apps |

**Conclusão que muda o plano:** o catálogo de demonstrações do §8 da especificação **já existe**; é
`/v1/studio/gallery`, alimentado por `pinneapple_studio` a partir do checkout da biblioteca (`app/studio/build.py` →
`data/studio.sqlite`). Criar `/demos` seria duplicar. O que falta nele é **mídia**: a entrada de galeria tem
`thumbs` (imagem) e não tem vídeo.

### O que não existe

- Campo de mídia (vídeo, carrossel, post) no registro da galeria.
- Proveniência de mídia: qual commit, qual corrida, qual campo gerou aquele vídeo.
- Nenhuma rota que aceite "rodar esta demonstração" a partir de um id de galeria.

## 3. Onde a mídia está hoje (fora dos dois repositórios)

| lugar | conteúdo | commit |
|---|---|---|
| `PINNeAPPle-Labs.github.io` → `tools/linkedin/fisica-em-serie/serie-3-studio/` | **10 episódios** gravados no Studio (mp4 + pôster + ficha), `gravar.py` | `7a0a309` |
| `take-a-piece` → `physics-in-action/` | a mesma série, espelho para material comercial | `c7f9bfd` |

Os dez episódios são, na prática, o primeiro lote de Cinema já produzido: cada um sai de um app real, com job
de verdade e campo em 3-D. O que lhes falta para virar "experimento executável" é o que este documento propõe.

## 4. Sobre "Fable"

A especificação pede para investigar "o modelo ou serviço Fable" e integrá-lo como gerador de mídia
(imagem, vídeo, image-to-video). **Essa premissa está errada e não vou implementá-la como se fosse verdade.**

- **Fable 5.1 é o modelo de linguagem em que este trabalho roda** — não é um serviço de geração de imagem ou
  vídeo, e não há SDK, API, CLI ou MCP de mídia chamado "Fable" nesta máquina (`which fable` → não encontrado;
  nenhum servidor MCP configurado).
- Portanto **não existe** etapa "Fable" no pipeline de mídia. O que existe é: Playwright dirigindo a app real,
  capturando quadros, e ffmpeg codificando — determinístico, e o vídeo mostra exatamente o que o solver produziu.
- Se a intenção era "usar um modelo generativo para compor cenas", isso exigiria um serviço externo pago, com
  chave e custo, e **não pode** tocar nos campos físicos. Decisão sua, e a especificação já proíbe fabricar
  resultado — o que eu assino embaixo.

## 5. O que está bloqueado

| item | bloqueio | o que dá para fazer |
|---|---|---|
| CI dos dois repositórios | Actions morto por billing (desde 2026-11-05) | gate local: ruff + pytest + `check_app_helpers` + `node verify.js` |
| imagem Docker do engineering-api | não rebuildada desde #292; chave Anthropic 401; Docker travado por memória | rodar as rotas por `uvicorn` nativo sobre o venv |
| "rodar a demonstração pela API" | nenhuma rota aceita id de galeria → job | proposta no mapa de integração: `POST /v1/studio/gallery/{id}/runs` reusando `appkit` |
