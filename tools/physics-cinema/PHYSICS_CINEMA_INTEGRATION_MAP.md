# Physics Cinema — mapa de integração entre os dois repositórios

Como as peças se ligam hoje (medido) e como se ligam na primeira fatia vertical (proposto, com o ponto de
extensão nomeado). Regra que vale em todas as linhas: **a biblioteca não depende da API**, e a API não reimplementa
física.

## 1. O caminho que já existe

```text
PINNeAPPle (biblioteca)
  pinneapple_physics / _simulation / _design        ← física e solvers
  pinneapple_tools.visualization.studio             ← Scene + field_view → glTF (_F0…)
        │
        ├─► apps/<app>/  (67 apps FastAPI, cada uma importa a biblioteca)
        │        │  appkit.install(): login, CSP, /vendor, /shared
        │        └─► página + fieldview3d.js → canvas 3-D no navegador
        │
        └─► pinneapple_studio (catálogo: ferramentas, galeria, cobertura)
                 │
                 └─► engineering-api: app/studio/build.py
                          lê o checkout → data/studio.sqlite (tabelas gallery, tools, modules, packages)
                          servido em /v1/studio/gallery, /tools, /coverage, /thumbs/{sha}
```

O contrato real entre os dois é **um banco SQLite construído a partir do checkout** — não um import Python. É
por isso que a API roda sem a biblioteca e sem o peso dela.

## 2. O caminho que falta (e onde ele encaixa)

```text
    id de galeria  ─────────────────────────────────────────────┐
    (ex.: example:autolab_aero)                                 │
                                                                ▼
                                          POST /v1/studio/gallery/{id}/runs      ← NOVO
                                                                │
                                          appkit job (fila + progresso)          ← JÁ EXISTE
                                                                │
                                          adapter do app que serve aquele id     ← JÁ EXISTE (app/<app>/api.py)
                                                                │
                                          execução na biblioteca                 ← JÁ EXISTE
                                                                │
                                          artefato: glTF + métricas + manifesto  ← glTF existe; manifesto NÃO
                                                                │
                                          GET .../runs/{run_id}                  ← NOVO (leitura)
```

O ponto de extensão é `app/studio/routes.py` (ao lado de `gallery`), e o adapter já existe em cada app. Não há
necessidade de rota `/demos`: a galeria **é** o catálogo, e o id dela já nomeia o app que executa.

## 3. Onde entra a mídia

Hoje a entrada de galeria carrega `thumbs` (WebP por SHA). O que falta:

| peça | onde entra | por quê |
|---|---|---|
| `media` na entrada de galeria | `pinneapple_studio` (biblioteca) → tabela `gallery` (API) | o vídeo é do experimento, não de um diretório de marketing |
| manifesto de proveniência | arquivo ao lado do vídeo (`<episódio>.manifest.json`) | commit, corrida, campo, colormap, duração, hash |
| validação de mídia | `verify.js` do `take-a-piece` estendido | tamanho, duração, proporção, legenda legível |

Enquanto isso não sobe, a mídia fica nos dois repositórios de conteúdo (site e `take-a-piece`) e a galeria
continua só com a imagem — que é honesto: o vídeo é consequência, não substituto do dado.

## 4. Primeira fatia vertical escolhida

**Ahmed body** — porque é a única em que as quatro etapas já são reais ao mesmo tempo:

| etapa | estado | evidência |
|---|---|---|
| experimento na biblioteca | **feito** | `examples/end_to_end/ahmed_body/01_cfd_campaign.py`, 57→64 corridas OpenFOAM |
| saída científica verificada | **feito** | `_runs/cfd/results/*.json`, validação contra Ahmed 1984 |
| app do Studio | **feito** | `apps/ahmed_twin`, twin com distância ao caso de treino |
| vídeo | **a regravar** | `gravar.py ahmed`, driver commitado (`7a0a309`) |
| showcase reproduzível | **feito** | comando da campanha + ficha do episódio |
| registro na galeria | **parcial** | `app:ahmed_twin` na galeria; sem mídia e sem execução pelo id |

O que falta para fechar a fatia: manifesto de proveniência do episódio 02 e o vídeo com a campanha completa.

## 5. Convenções respeitadas

- `app/studio/` continua lendo **só** o SQLite; nenhuma importação da biblioteca em tempo de request.
- Nenhuma física nova em `apps/`: o `optics_lab` provou o caminho (a física ficou em
  `pinneapple_physics.lithography`, a app só compõe) e o portão `check_app_helpers.py` reprova o contrário.
- A API não ganha rota que execute código arbitrário: o id de galeria resolve para um adapter **conhecido**.
