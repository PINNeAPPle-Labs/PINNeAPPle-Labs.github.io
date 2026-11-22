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

## 2. O caminho de execução: existe, e é mais curto do que a especificação supunha

Correção da própria auditoria, medida no código depois de escrevê-la: **"rodar esta demonstração pelo id" já
existe**, só não está na rota que a especificação imaginou. O caminho real é:

```text
    id de galeria  ─────────────────────────────────────────────┐
    (ex.: example:fins)                                         │  capability_id = "example." + id
                                                                ▼
                                          POST /v1/jobs                        ← JÁ EXISTE
                                                                │
                                          app/studio/capabilities.py:get()     ← JÁ EXISTE
                                                                │
                                          forma do exemplo (quick, flow)       ← JÁ EXISTE
                                                                │
                                          appkit job (fila + progresso)        ← JÁ EXISTE
                                                                │
                                          GET /v1/jobs/{id} e /result          ← JÁ EXISTE
```

`tests/test_studio_api.py::test_form_checks` já exercita a montagem da capability (`example.example:fins` é
executável, `example.example:cfd_car` pede OpenFOAM, `example.app:hub` responde "é uma app"). O prefixo dobra
(`example.` + id `example:fins`), o que é feio mas não é um buraco funcional.

O que **não** existe, e não deve existir desse jeito: rodar uma **app** pelo id de galeria. Uma app do Studio é um
serviço FastAPI com página, não um job em sandbox; a entrada de galeria já entrega o comando de subir (`start`) e a
capability responde `501` dizendo exatamente isso. Criar `POST /v1/studio/gallery/{id}/runs` seria uma segunda
porta para o que `/v1/jobs` faz, e para apps prometeria o que o desenho não faz.

## 3. Onde entra a mídia

Hoje a entrada de galeria carrega `thumbs` (WebP por SHA). O que falta, e o que já foi feito:

| peça | onde entra | estado |
|---|---|---|
| `cinema` na entrada de galeria | `pinneapple_studio.gallery` → tabela `gallery` (API) | **feito** — PR #2272 (biblioteca) e #753 (API) |
| `cinema.json` por app | `apps/<app>/cinema.json` | **feito** — dez apps, com SHA-256 e duração medidos |
| manifesto de proveniência | ao lado do vídeo (`midia/<episódio>.manifest.json`) | **feito** — `manifesto.py`, schema `pinneapple.cinema.media/1` |
| validação de mídia no portão | `check_cinema` no portão de manifestos; com `PINNEAPPLE_CINEMA_ROOT` confere o hash | **feito** |

O bloco `cinema` é **aditivo**: o schema do `experiment.json` continua `pinneapple.experiment/1`. A proposta
anterior deste documento era subir para `/2`; não é preciso. O validador aceita chave nova, o `Manifest` a preserva
na ida e volta, e os 174 manifestos já escritos seguem válidos — bumpar o schema invalidaria todos para ganhar nada.

## 4. Primeira fatia vertical escolhida

**Ahmed body** — porque é a única em que as quatro etapas já são reais ao mesmo tempo:

| etapa | estado | evidência |
|---|---|---|
| experimento na biblioteca | **feito** | `examples/end_to_end/ahmed_body/01_cfd_campaign.py`, 57→64 corridas OpenFOAM |
| saída científica verificada | **feito** | `_runs/cfd/results/*.json`, validação contra Ahmed 1984 |
| app do Studio | **feito** | `apps/ahmed_twin`, twin com distância ao caso de treino |
| vídeo | **a regravar** | `gravar.py ahmed`, driver commitado (`7a0a309`); sai com a campanha completa |
| showcase reproduzível | **feito** | comando da campanha + ficha do episódio |
| registro na galeria | **feito** | `app:ahmed_twin` com o bloco `cinema` (16:9 e 9:16, hashes medidos) |
| manifesto de proveniência | **feito** | `midia/02-aerodinamica-externa.manifest.json` |

O que falta para fechar a fatia é só o vídeo com a campanha completa (as últimas corridas da malha L2 e as de CAD
estão rodando) e a ficha reescrita com os números finais.

## 5. Convenções respeitadas

- `app/studio/` continua lendo **só** o SQLite; nenhuma importação da biblioteca em tempo de request.
- Nenhuma física nova em `apps/`: o `optics_lab` provou o caminho (a física ficou em
  `pinneapple_physics.lithography`, a app só compõe) e o portão `check_app_helpers.py` reprova o contrário.
- A API não ganha rota que execute código arbitrário: o id de galeria resolve para um adapter **conhecido**.
