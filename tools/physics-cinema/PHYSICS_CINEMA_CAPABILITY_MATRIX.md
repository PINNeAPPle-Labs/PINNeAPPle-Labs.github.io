# Physics Cinema — matriz de capacidade

O que a especificação pede × o que existe, medido em 2026-11-21. Legenda: **existe** · **parcial** · **falta** ·
**não se aplica** (premissa errada).

## 1. Contrato compartilhado de experimento (§6)

O contrato **já existe**: `experiment.json`, schema `pinneapple.experiment/1`, presente em **174** pastas de
`examples/`, validado por `scripts/check_experiment_manifests.py`.

| campo pedido pela especificação | onde está hoje |
|---|---|
| id, título, descrição, domínio | `id`, `title`, `description`, `domain` — em 174/174 |
| equações, método numérico | `methods` |
| módulos da biblioteca | `modules` |
| geometria, materiais, condições de contorno, parâmetros | `params` |
| solver, dataset, modelo, treino, inferência | `scripts` + `params` (o script carrega a configuração) |
| metodologia de validação, métricas, benchmark | `checks` + `metrics` (com `unit` e `how`) |
| arquivos gerados | `files`, `links` |
| **visualização** (campos, escalas) | **parcial** — o glTF e o `fieldview3d` existem, mas o manifesto não diz qual campo é | 
| **cinema** (short, técnico, carrossel) | **feito** — chave `cinema` opcional no `experiment.json` e `apps/<app>/cinema.json` (PR #2272) |
| **integração com a Engineering API** | **feito** — a entrada de galeria leva `cinema` (PR #753) |
| **proveniência** (commit, corrida, hash) | **feito** — `provenance` já existia; `cinema` traz SHA-256, duração e tamanho medidos |

A proposta de bump para `pinneapple.experiment/2` deste documento **não é necessária**: as três chaves são
aditivas, o validador aceita chave nova e o `Manifest` a preserva. Bumpar invalidaria os 174 manifestos existentes
para não ganhar nada.

## 2. Catálogo de demonstrações (§8, §17)

| pedido | estado | evidência |
|---|---|---|
| listar demonstrações | **existe** | `GET /v1/studio/gallery` → 173 entradas |
| filtrar por domínio | **parcial** | filtro por `kind`/`state`/`q`; `domain` está no payload mas não é filtro |
| buscar aplicação de engenharia | **existe** | `q` sobre título, descrição e chave |
| metadados científicos | **existe** | `measured`, `flows`, `pt`, `blocked_by` |
| datasets / modelos / validação por demo | **parcial** | via `/v1/studio/tools/{id}` e os campos da entrada |
| mídia | **feito** | `cinema` na entrada: 16:9 e 9:16, com SHA-256 e duração; a lista de `/v1/studio/gallery` também passou a entregar |
| iniciar execução pelo id | **existe** | `POST /v1/jobs` com `capability_id` `example.<entry id>` — medido no código, não na especificação |
| acompanhar execução | **existe** | jobs do `appkit` (progresso) |
| `/demos` como rota nova | **não se aplica** | duplicaria a galeria |
| rodar uma **app** pelo id | **não se aplica** | app é serviço FastAPI, não job em sandbox; a capability responde 501 com o comando de subir |

## 3. Os dez episódios já produzidos, por área

Cada linha é um app real, com job de verdade e campo em 3-D no vídeo.

| área | app | campo mostrado | verificação na tela |
|---|---|---|---|
| eletromagnetismo | `afpm_designer` | \|B\| em 3-D | estimate × 3-D: cogging +12,8% |
| aerodinâmica externa | `ahmed_twin` | Cp, CD com faixa de 90% | distância ao caso de treino |
| aviação | `aero_optimizer` | Cp do OpenFOAM | corrida guardada, 47,9 g CO₂/pkm |
| térmico de trocador | `heatsink_sizer` | T nas aletas | 24 de 38.301 verificados pela física |
| térmico de eletrônica | `pcb_hotspot` | T na placa | margem 0,9 °C e aviso de 20% menos refrigeração |
| acústica | `soundshape_ai` | geometria + Helmholtz | 40,1 Hz contra 40,0 de alvo |
| freio | `brakecool_ai` | T nos dutos | 65 °C; Monte Carlo ±0,2 °C |
| sólidos | `ridetune_ai` | σ ao longo da viga | elasticidade 22,2 × 11,1 |
| astronomia | `observatory` | céu em 3-D | JPL DE421, Lua a 371.661 km |
| óptica | `optics_lab` | imagem aérea no foco | Abbe × Hopkins 8,7·10⁻¹⁵ |

## 4. Os produtos A/B/C da especificação (§11), por episódio

| produto | estado | o que falta |
|---|---|---|
| **A · short** (15–30 s, 9:16) | **parcial** — os dez episódios têm versão 9:16 (1080x1920, 30 fps) com gancho e ressalva na cartela | a duração medida é de 4 a 9 s, não os 15–30 s pedidos: chegar lá exige capturar mais interação real, não repetir quadro |
| **B · técnico** (60–120 s, 16:9) | **falta** — a ficha tem o roteiro, não a narração | locução ou cartelas cronometradas |
| **C · executável** | **parcial** | roda pelo `uvicorn`; o registro na galeria agora existe (com mídia); falta a fatia de mídia no site público |

## 5. Geração de mídia

| pedido | estado |
|---|---|
| "integrar Fable para imagem/vídeo" | **não se aplica** — Fable é o modelo de linguagem desta sessão, não um serviço de mídia |
| render determinístico a partir do dado | **existe** — Playwright + ffmpeg (`gravar.py`), campo vindo do solver |
| carrossel | **parcial** — a Série 1 tem carrosséis em `serie-1/`; não saem do mesmo pipeline |
| thumbnail | **existe** — pôster por episódio (`-poster.jpg`) |
| manifesto de proveniência por mídia | **feito** — `midia/<episódio>.manifest.json` (`manifesto.py`), com hash, duração e o número da ficha |

## 6. Prioridade recomendada

1. ~~`media` + `provenance` no experimento e na galeria~~ — **feito** (PRs #2272 e #753).
2. ~~Rota para executar pelo id~~ — **não é preciso**: `POST /v1/jobs` já aceita `example.<entry id>`.
3. ~~Recorte 9:16 com gancho nos dez vídeos~~ — **feito** (`midia-vertical/`, 10 arquivos).
4. Manifesto por episódio no portão de mídia do site — **feito**; falta estender o `verify.js` do `take-a-piece`.
5. O que sobra de verdade: short de 15 a 30 s com interação real, produto B (60–120 s) e a página pública que serve
   os vídeos a partir da galeria.
