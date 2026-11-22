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
| **visualização** (campos, escalas) | **falta** |
| **cinema** (short, técnico, carrossel) | **falta** |
| **integração com a Engineering API** | **falta** |
| **proveniência** (commit, corrida, hash) | **parcial** — o `id` e os `files` dão o rastro; não há hash nem commit |

Proposta: acrescentar três chaves opcionais (`visualization`, `cinema`, `provenance`) ao mesmo schema, com bump
para `pinneapple.experiment/2`. **Não** criar um segundo formato: o portão de CI já valida este, e 174 exemplos
já o preenchem.

## 2. Catálogo de demonstrações (§8, §17)

| pedido | estado | evidência |
|---|---|---|
| listar demonstrações | **existe** | `GET /v1/studio/gallery` → 173 entradas |
| filtrar por domínio | **parcial** | filtro por `kind`/`state`/`q`; `domain` está no payload mas não é filtro |
| buscar aplicação de engenharia | **existe** | `q` sobre título, descrição e chave |
| metadados científicos | **existe** | `measured`, `flows`, `pt`, `blocked_by` |
| datasets / modelos / validação por demo | **parcial** | via `/v1/studio/tools/{id}` e os campos da entrada |
| mídia | **falta** | entrada tem `thumbs` (WebP), não tem vídeo |
| iniciar execução pelo id | **falta** | proposto `POST /v1/studio/gallery/{id}/runs` |
| acompanhar execução | **existe** | jobs do `appkit` (progresso) |
| `/demos` como rota nova | **não se aplica** | duplicaria a galeria |

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
| **A · short** (15–30 s, 9:16) | **parcial** — existe o vídeo 16:9 de 4–9 s | recorte 9:16 e gancho legível nos primeiros 3 s |
| **B · técnico** (60–120 s, 16:9) | **falta** — a ficha tem o roteiro, não a narração | locução ou cartelas cronometradas |
| **C · executável** | **parcial** | roda pelo `uvicorn`; falta o registro e o botão na API |

## 5. Geração de mídia

| pedido | estado |
|---|---|
| "integrar Fable para imagem/vídeo" | **não se aplica** — Fable é o modelo de linguagem desta sessão, não um serviço de mídia |
| render determinístico a partir do dado | **existe** — Playwright + ffmpeg (`gravar.py`), campo vindo do solver |
| carrossel | **parcial** — a Série 1 tem carrosséis em `serie-1/`; não saem do mesmo pipeline |
| thumbnail | **existe** — pôster por episódio (`-poster.jpg`) |
| manifesto de proveniência por mídia | **falta** |

## 6. Prioridade recomendada

1. `media` + `provenance` no `experiment.json` e na entrada de galeria (destrava §15 e §8 de uma vez).
2. `POST /v1/studio/gallery/{id}/runs` para os dez apps que já têm adapter.
3. Recorte 9:16 com gancho nos dez vídeos existentes (produto A completo).
4. Manifesto por episódio e verificação de mídia no gate.
5. Só então: novos experimentos. Dez áreas já cobertas é material suficiente para um trimestre.
