#!/usr/bin/env python3
"""Builds the PINNeAPPle Labs site: a commercial home, the product page, the
articles (one post per experiment) and the library page, in two languages.

    python3 build.py

Output
------
    index.html                        home (pt-BR)          en/index.html
    studio/index.html                 the product           en/studio/index.html
    artigos/index.html                article index         en/artigos/index.html
    artigos/<slug>/index.html         one per post          en/artigos/<slug>/index.html
    lib/index.html                    the library           en/lib/index.html
    engineering/index.html            redirect to /studio/ (and the /en/ twin)
    casos-de-uso/index.html           redirect to /artigos/ (and the /en/ twin)
    historia/index.html               redirect to /#historia (and the /en/ twin)

One place holds the shared shell (head, nav, footer, the sticky WhatsApp button) so the
pages cannot drift apart. Text lives next to the markup it belongs to, per language.
"""
from __future__ import annotations

import shutil
import urllib.parse
from pathlib import Path

import casos_sucesso as CS

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Configuration, change here, not in the pages
# ---------------------------------------------------------------------------

SITE = "https://pinneapple-labs.github.io"
WHATSAPP = "5584991287602"          # digits only, used by the floating button
EMAIL = "yanbarrosyan@gmail.com"
GITHUB = "https://github.com/PINNeAPPle-Labs/PINNeAPPle"
PYPI = "https://pypi.org/project/pinneapple/"
DOCS = "https://pinneapple-labs.github.io/PINNeAPPle/"
CHANGELOG = f"{GITHUB}/blob/main/CHANGELOG.md"
# Early-access sign-up, one Google Form per language (they are created by
# `tools/create_prerelease_forms.gs`, which prints the forms.gle link for each).
# While a language has no link, that language renders no button at all, because a
# call to action that leads nowhere is worse than no call to action.
PREACCESS_FORM = {
    "pt": "https://forms.gle/FQT8ekYrHBaKizQo8",
    "en": "https://forms.gle/3F3n132d35N1hWyd6",
}

# The offer, in one place: the deadline band and the floor price are the only
# numbers a visitor needs before asking for a quote. Change them here.
OFERTA = {
    "pt": {
        "prazo": "4 a 10 semanas",
        "linha": ("Estudos ficam entre 4 e 10 semanas, conforme o escopo. O orçamento é fechado a partir da "
                  "geometria, do fluido e da pergunta — antes de qualquer conta."),
        "eyebrow": "Prazo e preço",
        "h": "Escopo, prazo e orçamento antes de qualquer conta",
    },
    "en": {
        "prazo": "4 to 10 weeks",
        "linha": ("Studies run 4 to 10 weeks, depending on the scope. The quote is closed from the geometry, "
                  "the fluid and the question — before any of the work."),
        "eyebrow": "Deadline and price",
        "h": "Scope, deadline and quote before any of the work",
    },
}

# The public example reports, one per case, built by `tools/build_relatorios.py`.
# Each segment page links its own; the home offer links the first one.
REPORT_FILES = {
    "estudo-erosao-curva-90": {
        "pt": "relatorios/estudo-erosao-curva-90-pt.pdf",
        "en": "relatorios/estudo-erosao-curva-90-en.pdf",
    },
    "gemeo-hx201": {
        "pt": "relatorios/gemeo-hx201-pt.pdf",
        "en": "relatorios/gemeo-hx201-en.pdf",
    },
    "valvula-globo": {
        "pt": "relatorios/valvula-globo-pt.pdf",
        "en": "relatorios/valvula-globo-en.pdf",
    },
    "aero-ahmed-body": {
        "pt": "relatorios/aero-ahmed-body-pt.pdf",
        "en": "relatorios/aero-ahmed-body-en.pdf",
    },
    "motor-spm": {
        "pt": "relatorios/motor-spm-pt.pdf",
        "en": "relatorios/motor-spm-en.pdf",
    },
    "topologia-estrutural": {
        "pt": "relatorios/topologia-estrutural-pt.pdf",
        "en": "relatorios/topologia-estrutural-en.pdf",
    },
    "el-nino-modelos": {
        "pt": "relatorios/el-nino-modelos-pt.pdf",
        "en": "relatorios/el-nino-modelos-en.pdf",
    },
}
REPORT_LABEL = {
    "pt": "Relatório de exemplo (PDF)",
    "en": "Example report (PDF)",
}

# The report library, grouped by area: the page at /relatorios/ lists every one.
# Items are `(slug, title, one line of what the report proves)`.
REPORTS_INDEX = {
    "pt": {
        "eyebrow": "Relatórios de exemplo",
        "h1": "Sete relatórios,<br />sete áreas de engenharia",
        "lead": ("Cada relatório abaixo é um estudo real de um caso do repositório, em português e em inglês. "
                 "Todos seguem a mesma estrutura: o que foi pedido, o método, a verificação contra ensaio ou "
                 "contra uma segunda rota de cálculo, e a página do que <b>não</b> ficou provado."),
        "note": ("São exemplos públicos, e três deles usam dados de demonstração (máquina, estrutura e clima). "
                 "O que se copia deles é a estrutura de verificação, não o número."),
        "area_lbl": "Área",
        "areas": [
            ("Óleo, gás e tubulação",
             "Escoamento com partículas e com gás compressível: os dois casos em que o número precisa vir com a incerteza.",
             [("estudo-erosao-curva-90", "Erosão em curva de 90°",
               "Areia em curva de tubulação contra o ensaio de Vieira et al. (2016): taxa de erosão e onde o modelo deixa de valer."),
              ("valvula-globo", "Válvula globo em gás compressível",
               "Vazão e queda de pressão em regime bloqueado, com a malha como causa declarada do que não convergiu.")]),
            ("Térmico e troca de calor",
             "Um trocador com histórico: o que o modelo acerta e o que só o dado de campo mostra.",
             [("gemeo-hx201", "Gêmeo digital de um trocador HX-201",
               "Coeficientes, incrustação e o desvio entre o previsto e o medido em cada campanha de limpeza.")]),
            ("Aerodinâmica",
             "Corpo de Ahmed, ponta a ponta: malha, validação, substituto e o erro que é do modelo.",
             [("aero-ahmed-body", "Corpo de Ahmed: arrasto e malha",
               "Quatro malhas com GCI, validação em seis ângulos de rampa e o ponto em que refinar piora o resultado.")]),
            ("Mecânica estrutural",
             "Otimização topológica medida no que importa: gradiente checado, volume respeitado e cinza contado.",
             [("topologia-estrutural", "Projeção, gradiente e o cinza",
               "MBB e cantilever em quatro execuções: 18,6% de compliance com projeção, ao custo de 3,6× iterações.")]),
            ("Eletromagnetismo",
             "Torque calculado por duas rotas independentes — e o que a discordância entre elas denuncia.",
             [("motor-spm", "Máquina síncrona de ímãs",
               "Maxwell contra coenergia a 0,087% no projeto, cogging, FCEM, perdas e a topologia do rotor com saturação.")]),
            ("Clima e geociências",
             "Trinta configurações sob um protocolo só, com teste de significância e o resultado ruim publicado.",
             [("el-nino-modelos", "El Niño em 30 configurações",
               "ACC 0,95 em h = 1, três configurações significativas em h = 6 e um PINN com ACC −0,69 em h = 3.")]),
        ],
        "how_eyebrow": "Estrutura",
        "how_h": "O que todo relatório tem",
        "how": [
            "O escopo fechado no começo: geometria, fluido, condição de contorno e a pergunta.",
            "A verificação explícita: ensaio de referência, segunda rota de cálculo ou checagem de gradiente.",
            "O número com a incerteza ao lado — nunca o número sozinho.",
            "Uma página de limites dizendo o que o estudo não resolve.",
            "A proveniência: o arquivo do repositório de onde cada número saiu.",
        ],
        "cta_h": "Quer um relatório assim para o seu caso?",
    },
    "en": {
        "eyebrow": "Example reports",
        "h1": "Seven reports,<br />seven engineering areas",
        "lead": ("Every report below is a real study of a case in the repository, in Portuguese and in English. "
                 "They all follow the same structure: what was asked, the method, the check against an experiment "
                 "or a second computation route, and the page of what was <b>not</b> proven."),
        "note": ("These are public examples, and three of them use demonstration data (machine, structure and climate). "
                 "What to copy from them is the verification structure, not the number."),
        "area_lbl": "Area",
        "areas": [
            ("Oil, gas and piping",
             "Particle-laden and compressible flow: the two cases where the number has to come with its uncertainty.",
             [("estudo-erosao-curva-90", "Erosion in a 90° bend",
               "Sand in a pipe bend against the Vieira et al. (2016) experiment: erosion rate and where the model stops holding."),
              ("valvula-globo", "Globe valve in compressible gas",
               "Flow rate and pressure drop in the choked regime, with the mesh named as the cause of what did not converge.")]),
            ("Thermal and heat transfer",
             "An exchanger with a history: what the model gets right and what only field data shows.",
             [("gemeo-hx201", "Digital twin of an HX-201 exchanger",
               "Coefficients, fouling and the gap between predicted and measured across cleaning campaigns.")]),
            ("Aerodynamics",
             "Ahmed body, end to end: mesh, validation, surrogate and the error that belongs to the model.",
             [("aero-ahmed-body", "Ahmed body: drag and mesh",
               "Four meshes with GCI, validation at six slant angles and the point where refining makes it worse.")]),
            ("Structural mechanics",
             "Topology optimization measured on what matters: gradient checked, volume respected, grey counted.",
             [("topologia-estrutural", "Projection, gradient and the grey",
               "MBB and cantilever in four runs: 18.6% of compliance with projection, at 3.6× the iterations.")]),
            ("Electromagnetics",
             "Torque computed by two independent routes — and what their disagreement exposes.",
             [("motor-spm", "Surface-PM machine",
               "Maxwell against co-energy to 0.087% at the design point, cogging, back-EMF, losses and rotor topology with saturation.")]),
            ("Climate and geosciences",
             "Thirty configurations under one protocol, with a significance test and the bad result published.",
             [("el-nino-modelos", "El Niño in 30 configurations",
               "ACC 0.95 at h = 1, three significant configurations at h = 6 and a PINN at ACC −0.69 at h = 3.")]),
        ],
        "how_eyebrow": "Structure",
        "how_h": "What every report has",
        "how": [
            "The scope closed at the start: geometry, fluid, boundary condition and the question.",
            "The explicit check: a reference experiment, a second computation route or a gradient check.",
            "The number with its uncertainty beside it — never the number alone.",
            "A limits page saying what the study does not solve.",
            "Provenance: the repository file each number came from.",
        ],
        "cta_h": "Want a report like this for your case?",
    },
}

LANGUAGES = {
    "pt": {"code": "pt-BR", "dir": "", "label": "PT", "other": "en", "other_label": "EN"},
    "en": {"code": "en", "dir": "en", "label": "EN", "other": "pt", "other_label": "PT"},
}

# ---------------------------------------------------------------------------
# Articles, one post per experiment. Newest first.
#
# Every number here is one already published on this site, with the reference it
# was measured against. Nothing is rounded up to look better than the run.
# ---------------------------------------------------------------------------

POSTS = [
    dict(
        slug="pico-de-crash-com-surrogate",
        iso="2026-11-14",
        mins=6,
        thumb="img/exp/crash-thumb.webp",
        chart=True,
        tag={"pt": "Crash automotivo", "en": "Automotive crash"},
        date={"pt": "14 de novembro de 2026", "en": "14 November 2026"},
        title={
            "pt": "O surrogate acerta o deslocamento de pico de um projeto que nunca viu",
            "en": "The surrogate gets the peak displacement of a design it has never seen",
        },
        lead={
            "pt": "Um para-choque contra poste rígido, 200 projetos resolvidos pelo solver explícito do PINNeAPPle e um "
                  "Transolver que lê as sete variáveis de projeto. Nos 30 projetos mantidos fora do treino, o "
                  "deslocamento de pico sai com 24,4% de erro médio — e o mesmo modelo sem o vetor de projeto "
                  "vai a 41,7%.",
            "en": "A bumper beam against a rigid pole, 200 designs solved by PINNeAPPle's own explicit crash solver and "
                  "a Transolver that reads the seven design variables. On the 30 designs held out of training the peak "
                  "displacement comes out with 24.4% mean error — and the same model without the design vector "
                  "goes to 41.7%.",
        },
        metric={
            "pt": ("24,4%", "de erro médio no deslocamento de pico dos 30 projetos mantidos fora do treino"),
            "en": ("24.4%", "mean error on the peak displacement of the 30 designs held out of training"),
        },
        limits={
            "pt": "É um cupom de componente — viga de para-choque DP1000 em duas crash boxes DP600 —, não um veículo "
                  "inteiro. Os rótulos vêm do solver de crash explícito desta biblioteca, não do OpenRadioss, e a "
                  "espessura age sobre a tensão de escoamento e a densidade de uma malha fixa, o que representa bem o "
                  "esmagamento axial e subestima a rigidez de flexão. O pico é medido nos 900 nós retidos de 2.783, os "
                  "mesmos para todos os modelos, e o erro é contra o solver, não contra um ensaio. A campanha é a "
                  "de 6 de novembro de 2026, no tempo final dela (0,8 ms) e cortada nos nove primeiros quadros: o "
                  "pipeline da época escrevia 9 ou 10 quadros para o mesmo evento, e o exemplo reconstrói o vetor de "
                  "projeto a partir do metadado de cada projeto em vez de re-simular.",
            "en": "This is a component coupon — a DP1000 bumper beam on two DP600 crash boxes —, not a full vehicle. The "
                  "labels come from this library's explicit crash solver, not from OpenRadioss, and thickness acts on "
                  "the flow stress and the density of a fixed mesh, which holds for axial crush and under-represents "
                  "bending stiffness. The peak is measured on the 900 retained nodes out of 2.783, the same for every "
                  "model, and the error is against the solver, not against a test. The campaign is the one of 6 "
                  "November 2026, kept at its own end time (0.8 ms) and trimmed to its first nine frames: the "
                  "pipeline of the time wrote 9 or 10 frames for the same event, and the example rebuilds the "
                  "design vector from each design's metadata instead of re-simulating.",
        },
        body={
            "pt": [
                ("p", "Um operador neural pode prever o deslocamento de pico de um crash sem rodar o crash. O exercício "
                      "que motivou este texto fez exatamente isso com dados de OpenRadioss e um Graph Neural Operator do "
                      "PhysicsNeMo, e acertou 3,5% num projeto held-out. A pergunta aqui é a mesma; o que muda é de onde "
                      "vêm os dados — do solver de crash explícito da própria biblioteca, num cupom que roda num laptop."),
                ("h2", "O caso"),
                ("p", "Uma viga de para-choque DP1000 apoiada em duas crash boxes DP600, lançada contra um poste rígido: "
                      "é a metade de componente de um programa de crash. Sete variáveis de projeto — velocidade de "
                      "impacto (50 a 64 km/h), as duas espessuras de parede, os dois limites de escoamento, o raio do "
                      "poste e o seu deslocamento lateral. A malha é fixa, com <b>2.783 nós e 1.480 elementos "
                      "hexaédricos</b>, e 200 projetos foram resolvidos pelo solver explícito (plasticidade J2, "
                      "contato penalizado), 0,8 ms de evento em nove quadros cada."),
                ("h2", "O que a rede vê"),
                ("p", "Por nó: as três coordenadas, o rótulo de parte (a viga e as duas caixas) e a espessura. Por "
                      "quadro: o tempo. Por projeto: as sete variáveis, mapeadas para [0, 1] dentro da própria faixa e "
                      "repetidas em todos os nós. Essa última parte é o que torna o modelo paramétrico. Como a malha "
                      "não muda entre projetos — é isso que permite comparar nó a nó —, a geometria sozinha não "
                      "distingue um projeto do outro: sem o vetor de projeto, a rede vê 200 vezes o mesmo conjunto de "
                      "pontos."),
                ("h2", "Os números"),
                ("p", "O erro relativo L2 do campo de deslocamento, médio sobre os 30 projetos fora do treino, fica em "
                      "<b>0,28</b> (intervalo de confiança de 95%: 0,27 a 0,29). O deslocamento de pico — o menor "
                      "deslocamento na direção do impacto, sobre todos os nós e quadros — sai com <b>24,4%</b> de "
                      "erro médio, mediana de 24,5% e pior caso de 30,0%. No projeto pole0185, a referência "
                      "dá -11,15 mm e o surrogate, -8,40 mm. O erro não é ruído: é viés. A nuvem de pontos "
                      "fica acima da diagonal em todos os 30 projetos — o modelo acerta qual projeto esmaga mais e "
                      "quanto, mas subestima a magnitude do pico em cerca de 2,7 mm, que é o que se espera de um "
                      "regressor que suaviza."),
                ("fig", ("img/exp/crash-pico.webp", "Deslocamento de pico previsto contra o de referência, por projeto fora do treino",
                         "Cada ponto é um projeto mantido fora do treino; a cor é o erro relativo do pico e a linha "
                         "tracejada é a predição perfeita. A nuvem fica acima da diagonal: o surrogate acerta a ordem "
                         "dos projetos e subestima a magnitude do pico em 2,7 mm.")),
                ("h2", "Sem o vetor de projeto não há resposta"),
                ("p", "O mesmo Transolver, com o mesmo orçamento de treino, o mesmo split e o mesmo conjunto de nós, mas "
                      "sem as sete variáveis, fica em <b>41,7%</b> de erro médio no pico (erro de campo "
                      "0,76 contra 0,28). Não é um modelo pior: é um modelo sem a informação. Ele converge "
                      "para o campo médio dos projetos de treino, porque nada no que recebe diz qual projeto está sendo "
                      "pedido — e é essa a diferença entre interpolar a base e responder por um projeto novo."),
                ("h2", "Quanto custa"),
                ("p", "O solver leva cerca de <b>3,7 minutos</b> por projeto (medido: 223 s para 1.519 passos em 1 ms de "
                      "evento, um processo). O surrogate tem 0,64 milhão de parâmetros e infere um projeto inteiro "
                      "em <b>197 ms</b>, medido no mesmo benchmark. Não é 'mil vezes mais rápido numa GPU': é o que "
                      "permite varrer o espaço de projeto antes de escolher quais simulações pagar."),
                ("fig", ("img/exp/crash-superficie.webp", "Superfície deformada: referência e surrogate",
                         "O mesmo projeto desenhado como superfície, não como nuvem de pontos: à esquerda a referência "
                         "do solver, à direita a predição do surrogate, deformados 2× e na mesma escala de cor. A "
                         "referência concentra o esmagamento no centro da viga; o surrogate espalha uma faixa pela "
                         "face do para-choque e perde o pico.")),
                ("h2", "O que não está medido"),
                ("p", "O cupom é de componente e a malha é grosseira para um crash real; a espessura entra pela tensão de "
                      "escoamento numa malha fixa, o que subestima flexão; o erro é contra o próprio solver, não contra "
                      "ensaio; e o pico é lido nos 900 nós retidos, os mesmos para todos os modelos — o que não muda o "
                      "ranking, mas muda o número. Nada aqui é certificação: é o protocolo, com os limites ao lado."),
                ("h2", "Por que publicar"),
                ("p", "Porque o resultado útil não é o número do surrogate, é o que ele permite decidir: com o vetor de "
                      "projeto dentro do modelo, um projeto novo custa 197 ms em vez de minutos de solver, e o erro "
                      "vem com intervalo. O resto — inclusive o run sem as variáveis, que vai a 41,7% — está no "
                      "repositório, no mesmo exemplo que gerou as figuras."),
            ],
            "en": [
                ("p", "A neural operator can predict the peak displacement of a crash without running the crash. The "
                      "exercise that prompted this text did exactly that on OpenRadioss data with a PhysicsNeMo Graph "
                      "Neural Operator, and landed 3.5% on a held-out design. The question here is the same; what "
                      "changes is where the data comes from — this library's own explicit crash solver, on a coupon "
                      "that runs on a laptop."),
                ("h2", "The case"),
                ("p", "A DP1000 bumper beam held by two DP600 crash boxes, driven into a rigid pole: the component-scale "
                      "half of a crash programme. Seven design variables — impact velocity (50 to 64 km/h), the two wall "
                      "thicknesses, the two flow stresses, the pole radius and its lateral offset. The mesh is fixed, "
                      "<b>2.783 nodes and 1.480 hexahedral elements</b>, and 200 designs were solved by the explicit "
                      "solver (J2 plasticity, penalty contact), 0.8 ms of the event in nine frames each."),
                ("h2", "What the network sees"),
                ("p", "Per node: the three coordinates, the part label (the beam and the two boxes) and the thickness. "
                      "Per frame: the time. Per design: the seven variables, mapped to [0, 1] inside their own range "
                      "and repeated on every node. That last part is what makes the model parametric. Since the mesh "
                      "does not change between designs — which is what allows node-by-node comparison —, the geometry "
                      "alone does not tell one design from another: without the design vector the network sees the same "
                      "set of points 200 times."),
                ("h2", "The numbers"),
                ("p", "The relative L2 error of the displacement field, averaged over the 30 designs held out of "
                      "training, is <b>0.28</b> (95% confidence interval: 0.27 to 0.29). The peak displacement — the "
                      "smallest displacement along the impact direction, over every node and frame — comes out with "
                      "<b>24.4%</b> mean error, a median of 24.5% and a worst case of 30.0%. On design "
                      "pole0185 the reference is -11.15 mm and the surrogate -8.40 mm. The error is not noise, it "
                      "is bias: the cloud of points sits above the diagonal on all 30 designs — the model gets which "
                      "design crushes more, and by how much, but under-predicts the magnitude of the peak by about "
                      "2.7 mm, which is what a smoothing regressor does."),
                ("fig", ("img/exp/crash-pico.webp", "Predicted against reference peak displacement, per held-out design",
                         "Each point is a design held out of training; the colour is the relative error of the peak and "
                         "the dashed line is a perfect prediction. The cloud sits above the diagonal: the surrogate "
                         "gets the order of the designs right and under-predicts the magnitude by 2.7 mm.")),
                ("h2", "Without the design vector there is no answer"),
                ("p", "The same Transolver, with the same training budget, the same split and the same node set, but "
                      "without the seven variables, sits at <b>41.7%</b> mean error on the peak (field error "
                      "0.76 against 0.28). It is not a worse model: it is a model without the information. "
                      "It converges to the mean field of the training designs, because nothing it receives says which "
                      "design is being asked about — and that is the difference between interpolating the corpus and "
                      "answering for a new design."),
                ("h2", "What it costs"),
                ("p", "The solver takes about <b>3.7 minutes</b> per design (measured: 223 s for 1.519 steps over 1 ms of "
                      "the event, one process). The surrogate has 0.64 million parameters and infers a whole design "
                      "in <b>197 ms</b>, measured in the same benchmark. It is not 'a thousand times faster on a "
                      "GPU': it is what lets a design space be swept before choosing which simulations to pay for."),
                ("fig", ("img/exp/crash-superficie.webp", "The deformed surface: reference and surrogate",
                         "The same design drawn as a surface, not as a point cloud: on the left the solver's reference, "
                         "on the right the surrogate's prediction, deformed 2× and on the same colour scale. The "
                         "reference concentrates the crush at the centre of the beam; the surrogate spreads a band "
                         "across the bumper face and misses the peak.")),
                ("h2", "What is not measured"),
                ("p", "The coupon is component scale and the mesh is coarse for a real crash; thickness enters through "
                      "the flow stress on a fixed mesh, which under-represents bending; the error is against the solver "
                      "itself, not against a test; and the peak is read on the 900 retained nodes, the same for every "
                      "model — which does not change the ranking, but does change the number. Nothing here is "
                      "certification: it is the protocol, with its limits next to it."),
                ("h2", "Why publish it"),
                ("p", "Because the useful result is not the surrogate's number, it is what it lets you decide: with the "
                      "design vector inside the model a new design costs 197 ms instead of minutes of solver, and "
                      "the error comes with an interval. The rest — including the run without the variables, which goes "
                      "to 41.7% — is in the repository, in the same example that produced the figures."),
            ],
        },
    ),
    dict(
        slug="fno-placa-fria",
        iso="2026-11-13",
        mins=5,
        thumb="img/exp/fno-checagens.webp",
        chart=True,
        tag={"pt": "Transferência de calor", "en": "Heat transfer"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "O FNO acerta o campo e é reprovado na física",
            "en": "The FNO gets the field right and fails the physics",
        },
        lead={
            "pt": "Uma placa fria com 50 layouts, um FNO de 1,18 milhão de parâmetros treinado em 133 s e 1,7% de erro contra a solução de volumes finitos. E o cartão de confiança dizendo não.",
            "en": "A cold plate with 50 layouts, an FNO with 1.18 million parameters trained in 133 s and 1.7% error against the finite-volume solution. And the trust card saying no.",
        },
        metric={
            "pt": ("0,164", "de resíduo de PDE contra o limite de 0,1, com o erro de referência em 1,7%"),
            "en": ("0.164", "PDE residual against a 0.1 limit, with the reference error at 1.7%"),
        },
        limits={
            "pt": "A rede é avaliada em 50 layouts mantidos fora do treino, mas 4 deles têm coeficiente fora do envelope de treino, e o cartão registra isso. O alvo é a solução de volumes finitos do próprio exemplo, não um ensaio: o que está medido é fidelidade ao solver e consistência com a equação, não acerto contra bancada.",
            "en": "The network is evaluated on 50 layouts held out of training, but 4 of them carry a coefficient outside the training envelope, and the card records it. The target is the example's own finite-volume solution, not a test: what is measured is fidelity to the solver and consistency with the equation, not accuracy against a bench.",
        },
        body={
            "pt": [
                ("p", "Trocar o solver por uma rede neural é fácil de demonstrar e difícil de defender: o campo parece certo, e ninguém sabe dizer se está. O experimento monta o caso em que essa pergunta pode ser respondida com número: a placa fria do exemplo da NVIDIA Omniverse, com o FNO da própria biblioteca no lugar do FNO do PhysicsNeMo."),
                ("h2", "O experimento"),
                ("p", "50 layouts de placa, com a fonte e a geometria variando, resolvidos por volumes finitos para gerar referência. O FNO2d tem 1,18 milhão de parâmetros, largura 32, 12 modos e 4 camadas, e treina em 133 s (2.700 passos) até a perda final de 0,0063."),
                ("h2", "Os números"),
                ("p", "Erro relativo L2 de <b>1,7%</b> nos 50 layouts mantidos fora do treino, com o ponto quente errando no máximo <b>0,24 K</b>. A inferência leva 1,59 ms por layout, contra 2,39 ms do solver de volumes finitos, ou seja, 1,5 vez mais rápida, e não mil vezes."),
                ("fig", ("img/exp/fno-campos.webp", "Campo de temperatura previsto e de referência em quatro layouts", "Quatro layouts: previsto, referência e a diferença. A olho nu o campo está certo, e é exatamente por isso que a checagem precisa ser numérica.")),
                ("h2", "O cartão diz não"),
                ("p", "A decisão saiu <b>REJECT</b>. O resíduo de PDE, com o limitante de energia certificado, ficou em <b>0,164</b> contra o limite de 0,1, e o limitante de erro L2 em 0,247 contra 0,05. O balanço de fluxo na fronteira deu 5,4% contra 2% de tolerância. Passaram a condição de contorno (1,6% contra 2%) e a positividade (0,16% contra 1%), que são as duas mais fáceis."),
                ("p", "O erro de referência, 2,5%, passou com folga. É essa a lição: acertar o campo de referência e satisfazer a equação são duas coisas diferentes, e a segunda é a que decide se o resultado pode entrar num projeto."),
                ("fig", ("img/exp/fno-checagens.webp", "As sete checagens do cartão de confiança", "As sete checagens, com valor, limite e veredito. Duas passam com folga, três reprovam, e a de aplicabilidade sinaliza 4 dos 50 layouts fora do envelope de treino.")),
                ("h2", "Como ler o resultado"),
                ("p", "O FNO é um substituto rápido e fiel ao solver que o gerou, e isso já vale para exploração de projeto. O que ele não é, neste treino, é uma solução da equação: 2.700 passos não bastaram para fechar o resíduo. Publicar as duas leituras juntas é o que permite usar o modelo onde ele serve e não usá-lo onde não serve."),
            ],
            "en": [
                ("p", "Replacing a solver with a neural network is easy to demonstrate and hard to defend: the field looks right, and nobody can say whether it is. The experiment builds the case where that question has a numeric answer: the cold plate from the NVIDIA Omniverse example, with the library's own FNO in place of PhysicsNeMo's."),
                ("h2", "The experiment"),
                ("p", "50 plate layouts, with source and geometry varying, solved by finite volumes to produce the reference. The FNO2d has 1.18 million parameters, width 32, 12 modes and 4 layers, and trains in 133 s (2,700 steps) to a final loss of 0.0063."),
                ("h2", "The numbers"),
                ("p", "Relative L2 error of <b>1.7%</b> across the 50 layouts held out of training, with the hotspot erring by at most <b>0.24 K</b>. Inference takes 1.59 ms per layout against 2.39 ms for the finite-volume solver, so 1.5 times faster, not a thousand."),
                ("fig", ("img/exp/fno-campos.webp", "Predicted and reference temperature fields in four layouts", "Four layouts: prediction, reference and the difference. By eye the field is right, which is exactly why the check has to be numeric.")),
                ("h2", "The card says no"),
                ("p", "The decision came out <b>REJECT</b>. The PDE residual, with the certified energy bound, landed at <b>0.164</b> against a limit of 0.1, and the L2 error bound at 0.247 against 0.05. Boundary flux balance gave 5.4% against a 2% tolerance. The boundary condition (1.6% against 2%) and positivity (0.16% against 1%) passed, and those are the two easy ones."),
                ("p", "The reference error, 2.5%, passed with room to spare. That is the lesson: matching the reference field and satisfying the equation are two different things, and the second one decides whether the result can enter a design."),
                ("fig", ("img/exp/fno-checagens.webp", "The seven checks on the trust card", "The seven checks, with value, limit and verdict. Two pass comfortably, three fail, and the applicability one flags 4 of the 50 layouts outside the training envelope.")),
                ("h2", "How to read the result"),
                ("p", "The FNO is a fast surrogate that is faithful to the solver that produced it, and that already earns its place in design exploration. What it is not, at this training budget, is a solution of the equation: 2,700 steps were not enough to close the residual. Publishing both readings together is what lets the model be used where it serves and left out where it does not."),
            ],
        },
    ),
    dict(
        slug="gemeo-no-unity",
        iso="2026-11-13",
        mins=6,
        thumb="img/exp/unity-thumb.webp",
        tag={"pt": "Gêmeo digital", "en": "Digital twin"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "O mesmo campo, do solver ao motor de jogo",
            "en": "The same field, from the solver to the game engine",
        },
        lead={
            "pt": "Três caminhos entre o PINNeAPPle e o Unity: o gêmeo exportado como projeto, uma cena do Unity virando camada OpenUSD com física, e uma ponte HTTP que responde em 23 ms enquanto o jogo roda.",
            "en": "Three paths between PINNeAPPle and Unity: the twin exported as a project folder, a Unity scene turned into an OpenUSD layer with physics, and an HTTP bridge that answers in 23 ms while the game runs.",
        },
        metric={
            "pt": ("23,1 ms", "de ida e volta na ponte, mediana de 5 chamadas"),
            "en": ("23.1 ms", "round trip on the bridge, median of 5 calls"),
        },
        limits={
            "pt": "A ponte roda em rede local e com um job pequeno por chamada (41 vértices em 6 passos): não é medida para malha grande nem para latência de internet. No teste 02 a cena do Unity foi emulada, não aberta no editor, e o que se verifica é o formato e a física resultante, não o comportamento do editor.",
            "en": "The bridge runs on a local network with a small job per call (41 vertices across 6 steps): it is not a measurement for a large mesh, nor for internet latency. In test 02 the Unity scene was emulated, not opened in the editor, and what is verified is the format and the resulting physics, not the editor's behaviour.",
        },
        body={
            "pt": [
                ("p", "Um gêmeo digital morre no mesmo lugar em quase todo projeto: o resultado bonito não chega ao ambiente onde alguém vai usar. O experimento ataca isso em três frentes, e cada uma termina num arquivo que outro programa consegue abrir."),
                ("h2", "Os três caminhos"),
                ("p", "<b>1. Exportar.</b> O gêmeo de engenharia vira pasta de projeto Unity, com o campo colorido por vértice ao longo do tempo, sensores e legenda. A checagem é de ida: 10 checagens passam e o verificador que relê a pasta devolve zero problemas, com a camada de dados em C# relendo 1.148 vértices."),
                ("p", "<b>2. Ler de volta.</b> Uma cena escrita no Unity é lida, recebe física checada (10 checagens, todas passando) e sai como camada OpenUSD de 34 kB, com 3 atributos amostrados no tempo e o esquema UsdPhysics."),
                ("p", "<b>3. Conversar.</b> Uma ponte HTTP que o runtime chama durante o jogo: POST de um caso, resposta com o campo, as checagens e a decisão."),
                ("fig", ("img/exp/unity-espuleta.webp", "Carretel com o campo de temperatura, renderizado no Blender", "O carretel com o campo de temperatura, renderizado a partir do mesmo dado que a ponte serve: 30 °C na base, 180 °C na ponta aquecida.")),
                ("h2", "Os números"),
                ("p", "A ponte faz a ida e volta de um job em <b>23,1 ms</b> (mediana de cinco chamadas), devolvendo o campo e as checagens. No teste de recusa, um desenho com 300 MPa de pico contra o escoamento de 250 MPa é rejeitado dentro da própria ponte, e o gêmeo salvo por ela volta com zero problemas. O substituto do campo fecha em <b>0,167%</b> de L2 relativo, com resíduo da equação do calor em 0,031 contra a tolerância de 0,05."),
                ("p", "E o detalhe que interessa: a primeira tentativa de treino, com 0,248% de L2, foi <b>reprovada</b> pela checagem de resíduo, e o treino foi refeito. É o mesmo critério do resto do produto, aplicado onde ninguém espera, que é dentro de um motor de jogo."),
                ("video", ("videos/unity-turntable.mp4", "videos/unity-turntable.jpg", "O substituto girando em 360 graus, com o campo avaliado na hora em cada quadro")),
                ("video", ("videos/unity-ponte.mp4", "videos/unity-ponte.jpg", "Temperatura na ponte do suporte ao longo do tempo, do job ao clipe")),
                ("h2", "Por que a ponte é o ponto"),
                ("p", "Exportar é uma foto. A ponte é o que faz o gêmeo continuar valendo quando o caso muda: o runtime pergunta, recebe o campo junto com as checagens, e a decisão viaja com o número em vez de ficar no relatório de quem rodou."),
                ("h2", "O que não foi provado"),
                ("p", "Latência em rede real, malha grande e sessão longa de jogo não estão medidos aqui, e o artigo não estima. O que está medido é o formato fechando, a física sobrevivendo à ida e volta e a checagem rodando dentro do laço."),
            ],
            "en": [
                ("p", "A digital twin usually dies in the same place: the beautiful result never reaches the environment where somebody will use it. The experiment attacks that on three fronts, and each one ends in a file another program can open."),
                ("h2", "The three paths"),
                ("p", "<b>1. Export.</b> The engineering twin becomes a Unity project folder, with the field coloured per vertex over time, sensors and a legend. The check is on the way out: 10 checks pass, the verifier that re-reads the folder reports zero problems, and the C# data layer re-reads 1,148 vertices."),
                ("p", "<b>2. Read back.</b> A scene authored in Unity is read, receives checked physics (10 checks, all passing) and leaves as a 34 kB OpenUSD layer with 3 time-sampled attributes and the UsdPhysics schema."),
                ("p", "<b>3. Talk.</b> An HTTP bridge the runtime calls while the game runs: POST a case, get back the field, the checks and the decision."),
                ("fig", ("img/exp/unity-espuleta.webp", "Spool with the temperature field, rendered in Blender", "The spool with its temperature field, rendered from the same data the bridge serves: 30 °C at the base, 180 °C at the heated tip.")),
                ("h2", "The numbers"),
                ("p", "The bridge makes the round trip for one job in <b>23.1 ms</b> (median of five calls), returning the field and the checks. In the refusal test, a design peaking at 300 MPa against a 250 MPa yield is rejected inside the bridge itself, and the twin it saves comes back with zero problems. The field surrogate closes at <b>0.167%</b> relative L2, with a heat-equation residual of 0.031 against a 0.05 tolerance."),
                ("p", "And the detail that matters: the first training attempt, at 0.248% L2, was <b>rejected</b> by the residual check, and the training was redone. It is the same criterion as the rest of the product, applied where nobody expects it, which is inside a game engine."),
                ("video", ("videos/unity-turntable.mp4", "videos/unity-turntable.jpg", "The surrogate turning through 360 degrees, with the field evaluated live on every frame")),
                ("video", ("videos/unity-ponte.mp4", "videos/unity-ponte.jpg", "Temperature on the bracket bridge over time, from the job to the clip")),
                ("h2", "Why the bridge is the point"),
                ("p", "Exporting is a photograph. The bridge is what keeps the twin valid when the case changes: the runtime asks, receives the field together with the checks, and the decision travels with the number instead of staying in the report of whoever ran it."),
                ("h2", "What was not proven"),
                ("p", "Latency on a real network, a large mesh and a long play session are not measured here, and the article does not estimate them. What is measured is the format closing the loop, the physics surviving the round trip, and the check running inside the loop."),
            ],
        },
    ),
    dict(
        slug="ferramentas-de-dinamica",
        iso="2026-11-13",
        mins=6,
        thumb="img/exp/dinamica-thumb.webp",
        chart=True,
        tag={"pt": "Sistemas dinâmicos", "en": "Dynamical systems"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "Cinco ferramentas, cinco referências independentes",
            "en": "Five tools, five independent references",
        },
        lead={
            "pt": "Primeira passagem, espectro de Koopman, sensores escolhidos por informação de Fisher, análise dimensional e indicadores de alerta. Cada um conferido contra uma resposta que não veio do modelo.",
            "en": "First passage, the Koopman spectrum, sensors chosen by Fisher information, dimensional analysis and early-warning indicators. Each one checked against an answer that did not come from the model.",
        },
        metric={
            "pt": ("5,6×10⁻⁴", "de erro máximo na primeira passagem da PINN, contra 4,4×10⁻³ do Monte Carlo"),
            "en": ("5.6×10⁻⁴", "maximum first-passage error from the PINN, against 4.4×10⁻³ for Monte Carlo"),
        },
        limits={
            "pt": "Cada ferramenta é conferida no problema em que a resposta exata existe: equação do calor 1D, oscilador com dois modos, sela. É isso que limita a conclusão, e o experimento não afirma acerto fora desses casos, só que o método está implementado certo e mede o que promete.",
            "en": "Each tool is checked on the problem where the exact answer exists: the 1D heat equation, a two-mode oscillator, a saddle-node. That is what bounds the conclusion, and the experiment claims nothing outside those cases except that the method is implemented correctly and measures what it promises.",
        },
        body={
            "pt": [
                ("p", "Ferramenta de análise é fácil de vender e difícil de auditar: o gráfico fica bonito e ninguém pergunta contra o que ele foi conferido. O experimento pega cinco ferramentas do kit e coloca cada uma contra uma referência que não é o próprio modelo."),
                ("h2", "Primeira passagem: PINN contra Monte Carlo contra a exata"),
                ("p", "Na equação do calor 1D, a PINN resolve a primeira passagem com erro máximo de <b>5,6×10⁻⁴</b> contra a solução analítica. O Monte Carlo, com 20 mil caminhos Euler-Maruyama, fica em 4,4×10⁻³, oito vezes pior. O tempo médio restrito até 2,0 fecha em 0,87247 na PINN, contra 0,872465 exato e 0,87515 ± 4,7×10⁻³ no Monte Carlo. A PINN leva 104 s de solver; o Monte Carlo, o tempo dos 20 mil caminhos."),
                ("fig", ("img/exp/dinamica-passagem.webp", "Sobrevivência da primeira passagem, PINN e Monte Carlo", "Sobrevivência da primeira passagem: a PINN por cima da curva exata, e a banda do Monte Carlo em volta dela.")),
                ("h2", "Koopman: as taxas de decaimento saem do espectro"),
                ("p", "Rodando DMD de posto 3 nos retratos da PINN, as taxas de decaimento dos três modos saem com erro relativo de 0,6%, 0,5% e 1,0% contra os autovalores exatos −D(kπ)². O controle com os mesmos retratos gerados pela solução exata dá erro zero, como tem que dar, e o resíduo do ResDMD nos três autopares fica em 9,7×10⁻⁴."),
                ("p", "O detalhe honesto: o posto escolhido pelo critério de Gavish-Donoho nos retratos da PINN é 22, e não 3. Ou seja, o espectro é recuperável desde que o analista saiba quantos modos existem, e é isso que o artigo reporta em vez de esconder."),
                ("fig", ("img/exp/dinamica-koopman.webp", "Autovalores recuperados por DMD a partir dos retratos da PINN", "Autovalores recuperados por DMD a partir dos retratos da PINN, contra os exatos. O que está em jogo não é a curva, é o número.")),
                ("h2", "Onde medir importa 45%"),
                ("p", "Escolhendo quando medir por informação de Fisher, os quatro tempos ótimos são 0, 0, 2,025 e 2,025, em 401 pontos da grade. O desvio-padrão do difusor que sai do limitante de Cramér-Rao é 0,00102, e o empírico de 500 ajustes é 0,00102. Amostrando de forma uniforme, os mesmos dois números vão para 0,00149 e 0,00146: <b>45% pior</b> pelo mesmo número de medidas."),
                ("h2", "Análise dimensional e alerta precoce"),
                ("p", "Com seis grandezas e posto 3, Buckingham pi reduz o problema a três grupos, e o colapso das curvas vai de 1,68 de dispersão relativa para <b>8×10⁻⁵</b>, com p=0,002 num controle de permutação (999 reatribuições). Nos indicadores de alerta precoce, a variância e a autocorrelação de janela móvel sobem antes da sela (tau de Kendall 0,94 e 0,91, p de 0,005 e 0,01) e não sobem no controle estável (tau −0,22, p=0,55)."),
                ("p", "E o caso que separa os dois indicadores: um sistema estável com ruído crescendo levanta a variância (0,97, p=0,005) sem levantar a autocorrelação (0,38, p=0,27). Um indicador sozinho teria dado alarme falso, e é por isso que o kit mede os dois."),
                ("fig", ("img/exp/dinamica-alerta.webp", "Variância e autocorrelação de janela móvel, sela e controle", "Variância e autocorrelação de janela móvel: a sela e o controle estável em cima, e o caso de ruído crescente embaixo, onde só um dos dois indicadores dispara.")),
                ("h2", "O que isso vale"),
                ("p", "Cinco ferramentas que medem o que prometem, cada uma com a referência ao lado e o erro declarado. É menos vistoso que uma arquitetura nova, e é o que permite usar qualquer uma delas numa decisão."),
            ],
            "en": [
                ("p", "Analysis tooling is easy to sell and hard to audit: the plot looks good and nobody asks what it was checked against. The experiment takes five tools from the kit and puts each one against a reference that is not the model itself."),
                ("h2", "First passage: PINN against Monte Carlo against the exact answer"),
                ("p", "On the 1D heat equation, the PINN solves first passage with a maximum error of <b>5.6×10⁻⁴</b> against the analytical solution. Monte Carlo, with 20 thousand Euler-Maruyama paths, lands at 4.4×10⁻³, eight times worse. The restricted mean time up to 2.0 closes at 0.87247 for the PINN, against an exact 0.872465 and 0.87515 ± 4.7×10⁻³ for Monte Carlo. The PINN takes 104 s of solver time; Monte Carlo takes the time of the 20 thousand paths."),
                ("fig", ("img/exp/dinamica-passagem.webp", "First-passage survival, PINN and Monte Carlo", "First-passage survival: the PINN on top of the exact curve, with the Monte Carlo band around it.")),
                ("h2", "Koopman: decay rates out of the spectrum"),
                ("p", "Running a rank-3 DMD on the PINN snapshots, the three mode decay rates come out with relative errors of 0.6%, 0.5% and 1.0% against the exact −D(kπ)² eigenvalues. The control, using snapshots generated from the exact solution, gives zero error, as it must, and the ResDMD residual on the three eigenpairs sits at 9.7×10⁻⁴."),
                ("p", "The honest detail: the rank chosen by the Gavish-Donoho criterion on the PINN snapshots is 22, not 3. So the spectrum is recoverable as long as the analyst knows how many modes exist, and that is what the article reports instead of hiding."),
                ("fig", ("img/exp/dinamica-koopman.webp", "Eigenvalues recovered by DMD from the PINN snapshots", "Eigenvalues recovered by DMD from the PINN snapshots, against the exact ones. What is at stake is not the curve, it is the number.")),
                ("h2", "Where you measure is worth 45%"),
                ("p", "Choosing when to measure by Fisher information, the four optimal times are 0, 0, 2.025 and 2.025 over a 401-point grid. The diffuser standard deviation from the Cramér-Rao bound is 0.00102, and the empirical value from 500 fits is 0.00102. Sampling uniformly moves the same two numbers to 0.00149 and 0.00146: <b>45% worse</b> for the same number of measurements."),
                ("h2", "Dimensional analysis and early warning"),
                ("p", "With six quantities and rank 3, Buckingham pi reduces the problem to three groups, and the collapse of the curves goes from 1.68 of relative spread to <b>8×10⁻⁵</b>, with p=0.002 in a permutation control (999 reassignments). On early-warning indicators, rolling variance and autocorrelation rise before the saddle-node (Kendall tau 0.94 and 0.91, p of 0.005 and 0.01) and do not rise in the stable control (tau −0.22, p=0.55)."),
                ("p", "And the case that separates the two indicators: a stable system with growing noise lifts the variance (0.97, p=0.005) without lifting the autocorrelation (0.38, p=0.27). One indicator alone would have raised a false alarm, which is why the kit measures both."),
                ("fig", ("img/exp/dinamica-alerta.webp", "Rolling variance and autocorrelation, saddle-node and control", "Rolling variance and autocorrelation: the saddle-node and the stable control on top, and the growing-noise case below, where only one of the two indicators fires.")),
                ("h2", "What it is worth"),
                ("p", "Five tools that measure what they promise, each with its reference beside it and its error stated. It is less glamorous than a new architecture, and it is what lets any of them be used in a decision."),
            ],
        },
    ),
    dict(
        slug="el-nino-28-modelos",
        iso="2026-11-13",
        mins=7,
        thumb="img/exp/nino-barreira.webp",
        chart=True,
        tag={"pt": "Clima", "en": "Climate"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "28 modelos para o El Niño, um protocolo, e o que perdeu",
            "en": "28 El Niño models, one protocol, and what lost",
        },
        lead={
            "pt": "Cinco famílias de modelo, do AR à PINN, com os mesmos dados, a mesma janela e a mesma régua de significância. A 24 meses de antecedência ganha um oscilador de poucos parâmetros, e duas redes grandes não superam a persistência.",
            "en": "Five model families, from AR to PINN, on the same data, the same window and the same significance rule. At a 24-month lead a small oscillator wins, and two large networks do not beat persistence.",
        },
        metric={
            "pt": ("0,42", "de correlação de anomalia a 24 meses com o oscilador recarregado sazonal, contra 0,33 do AR e 0 da climatologia"),
            "en": ("0.42", "anomaly correlation at 24 months for the seasonal recharge oscillator, against 0.33 for AR and 0 for climatology"),
        },
        limits={
            "pt": "A avaliação é retrospectiva, em OISST v2.1 com splits fixos, e não é uma previsão operacional. A régua é a correlação de anomalia e a habilidade de RMSE contra persistência e climatologia, com significância controlada por Holm; nos horizontes em que nenhum modelo bate o melhor baseline, o artigo diz que não bateu.",
            "en": "The evaluation is retrospective, on OISST v2.1 with fixed splits, and it is not an operational forecast. The yardstick is anomaly correlation and RMSE skill against persistence and climatology, with Holm-controlled significance; at the horizons where no model beats the best baseline, the article says so.",
        },
        body={
            "pt": [
                ("p", "Previsão climática tem um problema de comparação: cada trabalho usa uma métrica, uma janela e uma linha de base. O experimento iguala tudo isso, coloca 28 modelos de cinco famílias na mesma régua e publica o ranking inteiro, inclusive as posições incômodas."),
                ("h2", "O protocolo"),
                ("p", "Os dados são OISST v2.1, com as fontes guardadas com o SHA-256 de cada arquivo, mais as sondagens de termoclina e o estresse do ERA5. Todo modelo é avaliado na mesma janela de validação, com correlação de anomalia, habilidade de RMSE contra persistência e contra climatologia, e teste de significância com correção de Holm. Os modelos probabilísticos levam também CRPS, cobertura de 95% e desvio do PIT."),
                ("h2", "O resultado que importa"),
                ("p", "A 24 meses, o <b>oscilador recarregado sazonal</b>, um modelo físico de 15 parâmetros, chega a <b>0,42</b> de correlação de anomalia, contra 0,33 do AR e 0,34 do oscilador recarregado simples. A 6 meses, ele fica em 0,63 contra 0,43 do AR. A climatologia, por definição, fica em zero."),
                ("p", "Só dois modelos bateram o melhor baseline de cada horizonte com significância estatística, e só no começo: a CNN, com 561 mil parâmetros, no horizonte 1, e o ensemble híbrido nos horizontes 1, 2 e 3. Fora dessa faixa, a diferença some dentro do ruído."),
                ("fig", ("img/exp/nino-habilidade.webp", "Habilidade de cada modelo por horizonte de previsão", "Habilidade por horizonte para as cinco famílias. É no cruzamento das curvas, e não no topo da tabela, que a escolha de método se decide.")),
                ("h2", "O que perdeu, e está publicado"),
                ("p", "As PINNs não saíram melhor por serem PINNs. A PINN construída em cima do próprio oscilador recarregado (6 parâmetros, 91 s de ajuste) tem correlação de <b>−0,69</b> no horizonte 3, enquanto o oscilador do qual ela herda a física, com os mesmos 6 parâmetros, fica em 0,80. A versão com fechamento aprendido também colapsa: −0,71 no mesmo horizonte."),
                ("p", "A perda com resíduo físico (0,51 no horizonte 6) e a PINN de extrapolação (0,54) ficam no meio da tabela, à frente da persistência e atrás do oscilador físico. É o tipo de resultado que só aparece quando a comparação é feita na mesma régua."),
                ("fig", ("img/exp/nino-barreira.webp", "A barreira de previsibilidade da primavera", "A barreira de previsibilidade da primavera: a habilidade cai quando a previsão atravessa a estação, e é ali que a diferença entre os modelos se abre.")),
                ("h2", "A física antes do modelo"),
                ("p", "Antes de comparar modelos, o solver foi comparado com a solução analítica: a onda de Kelvin viaja a <b>2,689 m/s</b> contra 2,7 m/s da teoria, a resposta estacionária de Gill converge para a solução analítica com erro L2 de 1,5×10⁻³ em 72 pontos de longitude e 5×10⁻⁵ em 576, e o período do oscilador recarregado bate com a teoria em todas as cinco resoluções testadas."),
                ("h2", "Como ler o ranking"),
                ("p", "O ranking não elege o modelo mais moderno. Ele mostra onde a física barata ganha, onde a rede grande só empata e onde o método caro piora o resultado, que é o que permite escolher com orçamento e não com entusiasmo."),
            ],
            "en": [
                ("p", "Climate prediction has a comparison problem: every paper uses a metric, a window and a baseline of its own. The experiment levels all of that, puts 28 models from five families on the same yardstick and publishes the whole ranking, uncomfortable positions included."),
                ("h2", "The protocol"),
                ("p", "The data is OISST v2.1, with every source file kept under its SHA-256, plus thermocline casts and ERA5 stress. Every model is scored on the same validation window, with anomaly correlation, RMSE skill against persistence and against climatology, and a significance test with Holm correction. Probabilistic models also carry CRPS, 95% coverage and PIT deviation."),
                ("h2", "The result that matters"),
                ("p", "At 24 months, the <b>seasonal recharge oscillator</b>, a physical model with 15 parameters, reaches <b>0.42</b> anomaly correlation, against 0.33 for AR and 0.34 for the plain recharge oscillator. At 6 months it sits at 0.63 against 0.43 for AR. Climatology, by definition, sits at zero."),
                ("p", "Only two models beat the best baseline at each horizon with statistical significance, and only early: the CNN, with 561 thousand parameters, at lead 1, and the hybrid ensemble at leads 1, 2 and 3. Beyond that band, the difference disappears into the noise."),
                ("fig", ("img/exp/nino-habilidade.webp", "Skill of each model by forecast horizon", "Skill by horizon for the five families. It is where the curves cross, not the top of the table, that decides the method.")),
                ("h2", "What lost, and is published"),
                ("p", "The PINNs did not come out better for being PINNs. The PINN built on top of the recharge oscillator itself (6 parameters, 91 s to fit) scores <b>−0.69</b> correlation at lead 3, while the oscillator it inherits its physics from, with the same 6 parameters, sits at 0.80. The version with a learned closure collapses too: −0.71 at the same lead."),
                ("p", "The physics-loss model (0.51 at lead 6) and the extrapolation PINN (0.54) land mid-table, ahead of persistence and behind the physical oscillator. That is the kind of result that only shows up when the comparison is made on the same yardstick."),
                ("fig", ("img/exp/nino-barreira.webp", "The spring predictability barrier", "The spring predictability barrier: skill drops when the forecast crosses the season, and that is where the gap between models opens.")),
                ("h2", "Physics before the model"),
                ("p", "Before comparing models, the solver was compared with the analytical solution: the Kelvin wave travels at <b>2.689 m/s</b> against 2.7 m/s from theory, the steady Gill response converges to the analytical solution with an L2 error of 1.5×10⁻³ at 72 longitude points and 5×10⁻⁵ at 576, and the recharge-oscillator period matches theory at all five resolutions tested."),
                ("h2", "How to read the ranking"),
                ("p", "The ranking does not crown the most modern model. It shows where cheap physics wins, where a large network only draws, and where the expensive method makes things worse, which is what lets the choice be made with a budget instead of with enthusiasm."),
            ],
        },
    ),
    dict(
        slug="rover-aprende-solo",
        iso="2026-11-13",
        mins=6,
        thumb="img/exp/rover-rotas.webp",
        chart=True,
        tag={"pt": "Robótica", "en": "Robotics"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "O rover que aprendeu o solo pelas próprias rodas",
            "en": "The rover that learned the soil from its own wheels",
        },
        lead={
            "pt": "Uma missão em linguagem comum, uma rota no mapa orbital e um travamento na areia. O rover mediu o escorregamento, refez o modelo do solo, replanejou e chegou, com metade do escorregamento e um décimo do afundamento.",
            "en": "A mission in plain language, a route from the orbital map and a stall in the sand. The rover measured the slip, rebuilt the soil model, replanned and arrived, with half the slip and a tenth of the sinkage.",
        },
        metric={
            "pt": ("30,7 mm", "de afundamento máximo na rota replanejada, contra 319 mm na rota direta"),
            "en": ("30.7 mm", "maximum sinkage on the replanned route, against 319 mm on the direct one"),
        },
        limits={
            "pt": "O sítio é sintético, então o solo verdadeiro é conhecido: a comparação é honesta, mas não é campo. O rover é um modelo de veículo de teste, e o aprendizado supõe que o modelo de rodas (k_phi, n0, n1) cobre o terreno encontrado. Fora do sítio simulado, o artigo não afirma nada.",
            "en": "The site is synthetic, so the true soil is known: the comparison is honest, but it is not field data. The rover is a test-vehicle model, and the learning assumes the wheel model (k_phi, n0, n1) covers the terrain it meets. Outside the simulated site, the article claims nothing.",
        },
        body={
            "pt": [
                ("p", "A missão, escrita em linguagem comum, pede uma travessia até um ponto de coleta. O plano direto, traçado no mapa orbital, tem 12,9 m. Ele trava a um terço do caminho, com 42% de escorregamento e 319 mm de afundamento: areia, não solo compacto."),
                ("h2", "O ciclo"),
                ("p", "A plataforma roda a missão no multibody, vê a roda patinar, trata o que encontrou como regolito, aprende os parâmetros do solo a partir do próprio escorregamento com um filtro de Kalman iterado, refaz o mapa de risco e replaneja. Nada disso é informado por fora: o único sinal novo é o que aconteceu com as rodas."),
                ("fig", ("img/exp/rover-mapa.webp", "Solo verdadeiro, risco do mapa orbital e risco depois de aprender", "Três painéis: o solo verdadeiro, que o planejador não vê; o risco que o mapa orbital sugeria; e o risco depois de aprender o solo. A rota direta travou no ponto vermelho, a replanejada chegou.")),
                ("h2", "Os números"),
                ("p", "Rota A, direta: 12,93 m, 2.958 J, escorregamento máximo de 0,42, afundamento máximo de <b>319 mm</b>, e a crença aprendida dizendo que 100% da rota estava acima do limite de escorregamento. Rota B, replanejada: 28,56 m, 2.869 J, escorregamento de 0,21, afundamento de <b>30,7 mm</b> e risco zero."),
                ("p", "A rota mais longa gastou 3% menos energia. Percorreu 2,2 vezes a distância, com metade do escorregamento e um décimo do afundamento, o que é o ponto: em solo fofo, quilômetro não é o custo, patinagem é."),
                ("fig", ("img/exp/rover-rotas.webp", "Escorregamento, afundamento, energia e elevação nas duas rotas", "Escorregamento, afundamento, energia acumulada e elevação ao longo das duas rotas. A vermelha sobe o afundamento e para; a verde mantém o escorregamento abaixo do limite de missão durante toda a travessia.")),
                ("h2", "O que foi aprendido, e com que erro"),
                ("p", "Contra o solo verdadeiro do sítio sintético, a crença final ficou em 0,072 de erro em log₁₀ k_phi (1,14 desvio-padrão da posterior), 0,057 em n0 (1,02 desvio-padrão) e 0,0145 em n1 (0,29 desvio-padrão). O erro é pequeno e, mais importante, compatível com a incerteza que o próprio filtro declara."),
                ("fig", ("img/exp/rover-solo.webp", "Aprendizado do solo ao longo da travessia", "O aprendizado ao longo da travessia: a posterior estreita, o valor verdadeiro fica dentro da banda e o planejador passa a usar o que aprendeu.")),
                ("video", ("videos/rover-traverse.mp4", "videos/rover-traverse.jpg", "A travessia no simulador multibody, com a roda da frente afundando na areia antes do replanejamento")),
                ("h2", "Por que isso é o produto"),
                ("p", "A diferença entre um plano e um bom plano é o que se aprende no caminho. Aqui o caminho ensina, o plano muda, e o relatório diz o que foi aprendido e com que erro, que é o que permite a um engenheiro aceitar ou recusar a decisão."),
            ],
            "en": [
                ("p", "The mission, written in plain language, asks for a traverse to a sampling point. The direct plan, drawn from the orbital map, is 12.9 m long. It stalls a third of the way in, with 42% slip and 319 mm of sinkage: sand, not compact soil."),
                ("h2", "The loop"),
                ("p", "The platform runs the mission in the multibody simulator, sees the wheel spin, treats what it found as regolith, learns the soil parameters from the slip itself with an iterated Kalman filter, rebuilds the risk map and replans. None of that is handed in from outside: the only new signal is what happened at the wheels."),
                ("fig", ("img/exp/rover-mapa.webp", "True soil, risk from the orbital map, and risk after learning the soil", "Three panels: the true soil, which the planner cannot see; the risk the orbital map suggested; and the risk after learning the soil. The direct route stalled at the red mark, the replanned one arrived.")),
                ("h2", "The numbers"),
                ("p", "Route A, direct: 12.93 m, 2,958 J, maximum slip 0.42, maximum sinkage <b>319 mm</b>, and the learned belief saying 100% of the route sat above the slip limit. Route B, replanned: 28.56 m, 2,869 J, slip 0.21, sinkage <b>30.7 mm</b> and zero risk."),
                ("p", "The longer route used 3% less energy. It covered 2.2 times the distance, with half the slip and a tenth of the sinkage, which is the point: in soft soil the cost is not the kilometre, it is the wheel spin."),
                ("fig", ("img/exp/rover-rotas.webp", "Slip, sinkage, energy and elevation on both routes", "Slip, sinkage, accumulated energy and elevation along both routes. The red one climbs in sinkage and stops; the green one keeps slip below the mission limit for the whole traverse.")),
                ("h2", "What was learned, and with what error"),
                ("p", "Against the true soil of the synthetic site, the final belief landed at 0.072 error in log₁₀ k_phi (1.14 posterior standard deviations), 0.057 in n0 (1.02) and 0.0145 in n1 (0.29). The error is small and, more importantly, consistent with the uncertainty the filter itself declares."),
                ("fig", ("img/exp/rover-solo.webp", "Soil learning along the traverse", "Learning along the traverse: the posterior narrows, the true value stays inside the band, and the planner starts to use what it learned.")),
                ("video", ("videos/rover-traverse.mp4", "videos/rover-traverse.jpg", "The traverse in the multibody simulator, with the front wheel sinking into the sand before the replan")),
                ("h2", "Why this is the product"),
                ("p", "The difference between a plan and a good plan is what gets learned on the way. Here the way teaches, the plan changes, and the report states what was learned and with what error, which is what lets an engineer accept or refuse the decision."),
            ],
        },
    ),
    dict(
        slug="construcoes-de-bloco",
        iso="2026-11-13",
        mins=7,
        thumb="img/exp/blocos-thumb.webp",
        tag={"pt": "Estrutural", "en": "Structural"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "Três construções de bloco, com a física como juiz",
            "en": "Three brick builds, with physics as the judge",
        },
        lead={
            "pt": "Um balanço de 135,9 mm, uma ponte de 3 peças e uma torre de 153,6 mm, todos encontrados por busca automática. E a checagem que decide se dá para confiar: estática contra formas fechadas e contra um simulador de corpo rígido.",
            "en": "A 135.9 mm overhang, a bridge of 3 parts and a 153.6 mm tower, all found by automated search. And the check that decides whether to trust them: statics against closed forms and against a rigid-body simulator.",
        },
        metric={
            "pt": ("135,9 mm", "de balanço com 8 peças, contra 86,7 mm da pilha harmônica e 31,9 mm de um bloco só"),
            "en": ("135.9 mm", "of overhang with 8 parts, against 86.7 mm for the harmonic stack and 31.9 mm for one brick"),
        },
        limits={
            "pt": "O modelo de junta é a parte frágil: 0,98 N de tração por pino (valor da literatura), atrito 0,4 assumido, peças rígidas e compressão ilimitada, o que dá a distribuição de forças mais favorável possível. A estática e o simulador de corpo rígido concordam em 90%, 100% e 75% dos candidatos nos três objetivos, e é essa discordância que o artigo mostra em vez de esconder.",
            "en": "The joint model is the fragile part: 0.98 N of pull-out per stud (from the literature), friction 0.4 assumed, rigid parts and unlimited compression, which gives the most favourable force distribution possible. Statics and the rigid-body simulator agree on 90%, 100% and 75% of the candidates across the three goals, and that disagreement is what the article shows instead of hiding.",
        },
        body={
            "pt": [
                ("p", "Construção de encaixe é um problema de engenharia com uma vantagem rara: a peça, a junta e a falha cabem numa conta de estática. O experimento usa isso para fechar o ciclo inteiro: construir, julgar, explicar por que caiu, construir de novo."),
                ("h2", "Os três objetivos"),
                ("p", "O maior balanço além da borda da mesa com 8 peças; uma ponte sobre 96 mm de vão que carregue 1 N com o menor número de peças; a torre mais alta que aguente um empurrão no topo. Em cada candidato, a estática rígida decide se fica de pé e, quando não fica, diz qual junta abriu ou onde o resultante saiu do apoio."),
                ("h2", "Os números"),
                ("p", "Balanço: <b>135,9 mm</b> com 8 peças, com a tração de pico num pino em 0,333 N, 34% do limite de 0,98 N. Para comparar, um bloco só alcança 31,9 mm, a pilha harmônica clássica chega a 86,7 mm, e o limite do centro de massa é 255,2 mm."),
                ("p", "Ponte: <b>3 peças</b> carregando 1,462 N no meio do vão, 1,46 vez a carga pedida. Torre: <b>153,6 mm</b> com 16 peças, aguentando 16,4 mN no topo, 1,64 vez o empurrão."),
                ("fig", ("img/exp/blocos-balanco.webp", "O balanço vencedor, renderizado", "O balanço vencedor, renderizado: 8 peças, 135,9 mm além da borda da mesa, com o pino mais carregado em 34% do limite de tração.")),
                ("h2", "A checagem que decide"),
                ("p", "Antes de otimizar qualquer coisa, a física do modelo foi conferida contra nove formas fechadas: pilha harmônica, limite de tombamento de um bloco, balanço em um pino, empurrão em torre, reações de apoio e uma viga resolvida por FEA de voxels contra Timoshenko. Passaram as nove, com o FEA dentro de 0,4% de Timoshenko (0,0327 mm contra 0,0328 mm), e o relatório de confiança saiu aprovado, nota 1,00 com cobertura 1,00."),
                ("fig", ("img/exp/blocos-comparacao.webp", "As duas estratégias de busca nos três objetivos", "As duas estratégias de busca nos três objetivos, com o mesmo orçamento de 400 avaliações de física por execução e cinco sementes.")),
                ("h2", "Onde os dois simuladores discordam"),
                ("p", "Cada candidato foi reproduzido num simulador de corpo rígido, com as juntas intactas. A concordância foi de 90% no balanço, 100% na ponte e 75% na torre. As discordâncias ensinam: no limite exato da pilha harmônica, o equilíbrio é neutro, a forma fechada diz que fica de pé e o simulador derruba, com o bloco do topo caindo 108,8 mm; a 0,99 do limite ele fica, a 1,01 cai."),
                ("p", "O outro desvio é do solver, não do modelo: sob o empurrão sustentado de 10 mN na melhor torre, o atrito do integrador escorrega 0,23 mm com passo de 1 ms e 0,03 mm com passo de 0,25 ms. O escorregamento encolhe junto com o passo, então é artefato numérico, e está reportado como tal."),
                ("video", ("videos/blocos-evolucao.mp4", "videos/blocos-evolucao.jpg", "Uma execução da busca, geração a geração: cada candidato é montado, julgado e colorido pela tração no pino, de azul (folgado) a vermelho (no limite)")),
                ("h2", "Busca: substituto contra evolução"),
                ("p", "Com 400 avaliações de física por execução e cinco sementes, a busca guiada por substituto não bateu a evolução simples em nenhum dos três objetivos: no balanço, mediana de 103,9 mm contra 111,9 mm; na ponte, 8 peças contra 5, e só 3 das 5 sementes chegaram a um resultado viável; na torre, 115,2 mm contra 118,4 mm. O melhor resultado absoluto da torre, 153,6 mm, veio do substituto, o que não compensa a mediana pior."),
                ("h2", "Por que isso vale como produto"),
                ("p", "O ciclo é o de qualquer projeto: gerar, julgar com física, explicar a falha, refinar. A diferença é que o julgamento é auditável, cada rejeição vem com o motivo e cada número vem junto do modelo de junta que o produziu."),
            ],
            "en": [
                ("p", "Interlocking construction is an engineering problem with a rare advantage: the part, the joint and the failure all fit into a statics calculation. The experiment uses that to close the whole loop: build, judge, explain why it fell, build again."),
                ("h2", "The three goals"),
                ("p", "The longest overhang past the table edge with 8 parts; a bridge over a 96 mm gap carrying 1 N with the fewest parts; the tallest tower that survives a push at the top. For every candidate, rigid statics decides whether it stands and, when it does not, says which joint opened or where the resultant left its support."),
                ("h2", "The numbers"),
                ("p", "Overhang: <b>135.9 mm</b> with 8 parts, peak stud tension at 0.333 N, 34% of the 0.98 N limit. For comparison, a single brick reaches 31.9 mm, the classic harmonic stack 86.7 mm, and the centre-of-mass bound is 255.2 mm."),
                ("p", "Bridge: <b>3 parts</b> carrying 1.462 N at mid-span, 1.46 times the load asked for. Tower: <b>153.6 mm</b> with 16 parts, holding 16.4 mN at the top, 1.64 times the push."),
                ("fig", ("img/exp/blocos-balanco.webp", "The winning overhang, rendered", "The winning overhang, rendered: 8 parts, 135.9 mm past the table edge, with the most loaded stud at 34% of its pull-out limit.")),
                ("h2", "The check that decides"),
                ("p", "Before optimizing anything, the model's own physics was checked against nine closed forms: the harmonic stack, the tipping limit of one brick, the one-stud overhang, the tower push, the support reactions and a plate beam solved by voxel FEA against Timoshenko. All nine passed, with the FEA within 0.4% of Timoshenko (0.0327 mm against 0.0328 mm), and the trust report came out approved, score 1.00, coverage 1.00."),
                ("fig", ("img/exp/blocos-comparacao.webp", "The two search strategies across the three goals", "The two search strategies across the three goals, at the same budget of 400 physics evaluations per run and five seeds.")),
                ("h2", "Where the two simulators disagree"),
                ("p", "Every candidate was replayed in a rigid-body simulator, with the joints intact. Agreement was 90% on the overhang, 100% on the bridge and 75% on the tower. The disagreements teach something: at exactly the harmonic-stack limit the equilibrium is neutral, the closed form says it stands and the simulator drops it, with the top brick falling 108.8 mm; at 0.99 of the limit it stands, at 1.01 it falls."),
                ("p", "The other deviation belongs to the solver, not the model: under the sustained 10 mN push on the best tower, friction in the integrator creeps 0.23 mm at a 1 ms step and 0.03 mm at 0.25 ms. The creep shrinks with the step, so it is a numerical artefact, and it is reported as one."),
                ("video", ("videos/blocos-evolucao.mp4", "videos/blocos-evolucao.jpg", "One search run, generation by generation: every candidate is built, judged and coloured by stud tension, from blue (slack) to red (at the limit)")),
                ("h2", "Search: surrogate against evolution"),
                ("p", "With 400 physics evaluations per run and five seeds, the surrogate-guided search did not beat plain evolution on any of the three goals: on the overhang, a median of 103.9 mm against 111.9 mm; on the bridge, 8 parts against 5, and only 3 of the 5 seeds found a feasible build; on the tower, 115.2 mm against 118.4 mm. The best single result on the tower, 153.6 mm, came from the surrogate, which does not make up for the worse median."),
                ("h2", "Why this counts as a product"),
                ("p", "The loop is the one every project has: generate, judge with physics, explain the failure, refine. The difference is that the judgement is auditable, every rejection comes with its reason, and every number comes with the joint model that produced it."),
            ],
        },
    ),
    dict(
        slug="motor-prius-dois-solvers",
        iso="2026-11-13",
        mins=6,
        thumb="img/exp/motor-campo.webp",
        chart=True,
        tag={"pt": "Eletromagnetismo", "en": "Electromagnetics"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "Dois solvers concordam em 0,19%, e os dois discordam do artigo",
            "en": "Two solvers agree to 0.19%, and both disagree with the paper",
        },
        lead={
            "pt": "O motor do Prius resolvido pela FEM da casa e pelo GetDP, um código independente, em 12 posições de rotor. Os dois chegam ao mesmo torque. Contra o benchmark publicado, os dois se afastam a mesma distância.",
            "en": "The Prius motor solved by our own FEM and by GetDP, an independent code, at 12 rotor positions. Both arrive at the same torque. Against the published benchmark, both drift the same distance.",
        },
        metric={
            "pt": ("0,19%", "de diferença máxima de torque contra o GetDP, em 12 posições de rotor"),
            "en": ("0.19%", "maximum torque difference against GetDP, over 12 rotor positions"),
        },
        limits={
            "pt": "É magnetostática 2D: efeitos de ponta, skew e perdas não entram nesta comparação. A concordância entre os dois solvers mede consistência numérica, não acerto contra ensaio, e o desvio de cerca de 13 N·m contra o benchmark publicado aparece igual nos dois, o que aponta para diferença de modelo (geometria, materiais, hipótese 2D), não para erro de implementação.",
            "en": "This is 2D magnetostatics: end effects, skew and losses are not in this comparison. Agreement between the two solvers measures numerical consistency, not accuracy against a test, and the roughly 13 N·m deviation from the published benchmark shows up equally in both, which points to a difference of model (geometry, materials, the 2D assumption), not to an implementation error.",
        },
        body={
            "pt": [
                ("p", "Quando dois códigos escritos por gente diferente, com malhas diferentes, chegam ao mesmo torque, o resultado ganhou alguma credibilidade. Quando os dois se afastam do número publicado pela mesma quantia, a pergunta muda de lugar: o problema deixou de ser o código e passou a ser o modelo."),
                ("h2", "O caso"),
                ("p", "A geometria é a do motor do Prius 2010, um dos benchmarks abertos mais usados em máquinas elétricas. A FEM da casa resolve o campo em 2D; o GetDP, um solver de elementos finitos independente, resolve o mesmo problema na mesma geometria. São 12 posições de rotor e 960 pontos no entreferro."),
                ("fig", ("img/exp/motor-campo.webp", "Campo |B| e linhas de fluxo no quarto de máquina do motor do Prius", "O campo |B| e as linhas de fluxo no quarto de máquina, com o rotor na posição de máximo torque por ampère (250 A).")),
                ("h2", "Os números"),
                ("p", "Diferença máxima de torque entre os dois: <b>1,09 N·m</b>, ou <b>0,19%</b> no pico, com RMS de 0,81 N·m. A força contra-eletromotriz a 1000 rpm bate em 87,60 V contra 87,64 V no fundamental, e a distorção harmônica fica em 9,35% contra 9,04%. O ripple de cogging é onde os dois mais se afastam: 1,35 N·m contra 1,05 N·m."),
                ("fig", ("img/exp/motor-getdp.webp", "Torque nas 12 posições de rotor, os dois solvers e a diferença", "Torque nas 12 posições de rotor nas duas implementações, com a diferença embaixo. Onde a curva é mais inclinada, a diferença relativa é maior.")),
                ("h2", "Contra o benchmark publicado"),
                ("p", "Aqui o resultado incomoda. Contra a curva do artigo, o RMS é de 13,3 N·m na FEM da casa e 12,9 N·m no GetDP. Os dois se afastam do paper pela mesma ordem, e não um do outro: o desvio é do modelo, não da implementação, e é isso que autoriza discutir hipótese em vez de procurar bug."),
                ("h2", "O que mais roda nesse exemplo"),
                ("p", "Além da máquina, o exemplo cobre seis problemas com solução exata resolvidos por PINN: capacitor de placas paralelas, Poisson com carga, dipolo, fio infinito, onda plana e o modo TM de uma cavidade. Cada um tem a solução analítica ao lado da rede, que é a forma mais barata de descobrir se o método está implementado certo antes de aplicá-lo a algo sem resposta conhecida."),
                ("h2", "Por que publicar o desvio"),
                ("p", "Um número que concorda com o paper esconde qual parte do modelo está errada. Dois números que concordam entre si e discordam do paper dizem exatamente onde ir olhar."),
            ],
            "en": [
                ("p", "When two codes written by different people, on different meshes, arrive at the same torque, the result has earned some credibility. When both drift from the published number by the same amount, the question moves: the problem is no longer the code, it is the model."),
                ("h2", "The case"),
                ("p", "The geometry is the 2010 Prius motor, one of the most used open benchmarks in electrical machines. Our FEM solves the field in 2D; GetDP, an independent finite-element solver, solves the same problem on the same geometry. That is 12 rotor positions and 960 points along the air gap."),
                ("fig", ("img/exp/motor-campo.webp", "|B| field and flux lines in the quarter machine of the Prius motor", "The |B| field and the flux lines in the quarter machine, with the rotor at the maximum-torque-per-ampere position (250 A).")),
                ("h2", "The numbers"),
                ("p", "Maximum torque difference between the two: <b>1.09 N·m</b>, or <b>0.19%</b> at the peak, with an RMS of 0.81 N·m. Back-EMF at 1000 rpm matches at 87.60 V against 87.64 V in the fundamental, and total harmonic distortion sits at 9.35% against 9.04%. Cogging ripple is where they differ most: 1.35 N·m against 1.05 N·m."),
                ("fig", ("img/exp/motor-getdp.webp", "Torque across the 12 rotor positions, both solvers and the difference", "Torque across the 12 rotor positions in both implementations, with the difference below. Where the curve is steepest, the relative difference is largest.")),
                ("h2", "Against the published benchmark"),
                ("p", "Here the result is uncomfortable. Against the paper's curve, the RMS is 13.3 N·m for our FEM and 12.9 N·m for GetDP. Both drift from the paper by the same order, not from each other: the deviation belongs to the model, not the implementation, and that is what lets the discussion be about assumptions instead of a bug hunt."),
                ("h2", "What else runs in this example"),
                ("p", "Beyond the machine, the example covers six problems with exact solutions solved by a PINN: parallel-plate capacitor, Poisson with charge, dipole, infinite wire, plane wave and the TM mode of a cavity. Each one carries the analytical solution next to the network, which is the cheapest way to find out whether the method is implemented correctly before applying it to something without a known answer."),
                ("h2", "Why publish the deviation"),
                ("p", "A number that agrees with the paper hides which part of the model is wrong. Two numbers that agree with each other and disagree with the paper say exactly where to look."),
            ],
        },
    ),
    dict(
        slug="aerodinamica-autonoma",
        iso="2026-11-13",
        mins=7,
        thumb="img/exp/aero-autonoma-wake.webp",
        tag={"pt": "Automação", "en": "Automation"},
        date={"pt": "13 de novembro de 2026", "en": "13 November 2026"},
        title={
            "pt": "20 simulações, 3,3 horas, 15,7% menos arrasto",
            "en": "20 simulations, 3.3 hours, 15.7% less drag",
        },
        lead={
            "pt": "Um carro de corrida paramétrico, três objetivos declarados e um orçamento de 20 rodadas de CFD. A plataforma escolheu onde gastar cada uma, e o ganho foi conferido de novo na malha fina.",
            "en": "A parametric racing car, three stated objectives and a budget of 20 CFD runs. The platform chose where to spend each one, and the gain was checked again on the fine mesh.",
        },
        metric={
            "pt": ("−15,7% arrasto", "com o downforce acima do piso de 7 kN; −13,9% na malha fina"),
            "en": ("−15.7% drag", "with downforce above the 7 kN floor; −13.9% on the fine mesh"),
        },
        limits={
            "pt": "Não há ensaio nem túnel de vento nesta comparação: o ganho é medido contra o próprio baseline, no mesmo solver. A malha da campanha subestima o downforce em 8,4% frente à malha fina, e o substituto erra 2,4% no arrasto e 10,2% no downforce em validação cruzada. Fora da faixa geométrica validada, a previsão não vale.",
            "en": "There is no test and no wind tunnel in this comparison: the gain is measured against its own baseline, in the same solver. The campaign mesh under-predicts downforce by 8.4% against the fine mesh, and the surrogate errs 2.4% in drag and 10.2% in downforce under cross-validation. Outside the validated geometry range, the prediction does not hold.",
        },
        body={
            "pt": [
                ("p", "Otimizar com CFD é fácil de descrever e caro de fazer: cada avaliação custa horas de solver. O problema deixa de ser o algoritmo e passa a ser a pergunta que quase ninguém gasta tempo respondendo: <b>qual é o próximo caso que vale simular?</b>"),
                ("h2", "O que a plataforma fez sozinha"),
                ("p", "O caso é um carro de corrida paramétrico, com asas, altura de solo e ângulo de difusor, a 70 m/s. A missão recebeu três objetivos ao mesmo tempo: baixar o arrasto, manter o downforce acima de 7 kN e manter o balanço aerodinâmico dianteiro dentro da faixa. O orçamento: 20 rodadas de OpenFOAM 3D."),
                ("p", "A cada rodada o substituto é retreinado, o NSGA-II propõe os candidatos, e cada candidato recebe um veredito antes de gastar solver: favorável, incerto ou fora de domínio. Só o que vale a pena vira caso novo, e o critério é a própria incerteza do modelo."),
                ("fig", ("img/exp/aero-autonoma-trust.webp", "Os três vereditos de triagem, A incerto, B favorável, C fora de domínio", "Os três vereditos. A: o intervalo de 95% é maior que a tolerância, então o modelo não decide. B: dentro do domínio validado, com a incerteza na tolerância. C: extrapolação, com o ângulo de difusor acima do que foi simulado. O diamante é o CFD que veio depois, para conferir.")),
                ("h2", "O número"),
                ("p", "<b>−15,7% de arrasto</b> contra o baseline, com o downforce acima do piso de 7 kN e o balanço dentro da faixa, em 20 rodadas que somaram <b>3,3 horas</b> de solver (quatro núcleos) e nenhuma falha."),
                ("p", "O mesmo desenho, rodado na malha fina, dá <b>−13,9%</b>. É esse o número honesto: a malha usada na campanha subestima o downforce em 8,4% e, com ele, exagera um pouco o ganho."),
                ("fig", ("img/exp/aero-autonoma-pareto.webp", "Candidatos do substituto, frente de Pareto e os casos que foram ao CFD", "Cada × é um candidato do substituto; os anéis são a frente de Pareto; as estrelas são o baseline e o melhor desenho simulado. A linha tracejada é o piso de downforce, e é ela que transforma o problema em negociação em vez de minimização.")),
                ("h2", "Por que isso importa mais que o número"),
                ("p", "Um ganho de 15,7% depende de quantas simulações você pode pagar, e o custo aqui está medido: 20 avaliações, três horas e meia, cada uma escolhida por uma razão registrada. Um engenheiro com o mesmo orçamento chegaria longe; a diferença é que aqui o relatório diz onde o substituto estava extrapolando e por que aquela rodada foi comprada."),
                ("fig", ("img/exp/aero-autonoma-wake.webp", "Vorticidade no plano de esteira do desenho recomendado", "Vorticidade no plano de esteira do desenho recomendado: os vórtices de ponta de asa e o rastro das rodas, o que o arrasto medido está enxergando.")),
            ],
            "en": [
                ("p", "Optimizing with CFD is easy to describe and expensive to do: every evaluation costs hours of solver time. The problem stops being the algorithm and becomes the question almost nobody spends time answering: <b>which case is worth simulating next?</b>"),
                ("h2", "What the platform did on its own"),
                ("p", "The case is a parametric racing car, with wings, ride height and diffuser angle, at 70 m/s. The mission took three objectives at once: lower drag, keep downforce above 7 kN, keep the front aero balance inside its band. The budget: 20 runs of 3D OpenFOAM."),
                ("p", "Every round the surrogate is retrained, NSGA-II proposes the candidates, and each candidate gets a verdict before any solver time is spent: favourable, uncertain or out of domain. Only what is worth it becomes a new case, and the criterion is the model's own uncertainty."),
                ("fig", ("img/exp/aero-autonoma-trust.webp", "The three triage verdicts, A uncertain, B favourable, C out of domain", "The three verdicts. A: the 95% interval is wider than the tolerance, so the model cannot decide. B: inside the validated domain, with the uncertainty within tolerance. C: extrapolation, with diffuser angle above what was simulated. The diamond is the CFD that came afterwards, to check.")),
                ("h2", "The number"),
                ("p", "<b>−15.7% drag</b> against the baseline, with downforce above the 7 kN floor and the balance inside its band, over 20 runs summing <b>3.3 hours</b> of solver time (four cores) and no failures."),
                ("p", "The same design, run on the fine mesh, gives <b>−13.9%</b>. That is the honest number: the campaign mesh under-predicts downforce by 8.4% and, with it, flatters the gain a little."),
                ("fig", ("img/exp/aero-autonoma-pareto.webp", "Surrogate candidates, the Pareto front and the cases that went to CFD", "Every × is a surrogate candidate; the rings are the Pareto front; the stars are the baseline and the best simulated design. The dashed line is the downforce floor, and it is what turns the problem into a negotiation instead of a minimisation.")),
                ("h2", "Why this matters more than the number"),
                ("p", "A 15.7% gain depends on how many simulations you can pay for, and the cost here is measured: 20 evaluations, three and a half hours, each chosen for a recorded reason. An engineer with the same budget would get far; the difference is that here the report states where the surrogate was extrapolating and why that run was bought."),
                ("fig", ("img/exp/aero-autonoma-wake.webp", "Vorticity in the wake plane of the recommended design", "Vorticity in the wake plane of the recommended design: the wing-tip vortices and the wheel wake, what the measured drag is looking at.")),
            ],
        },
    ),
    dict(
        slug="futebol-fisica",
        iso="2026-11-12",
        mins=7,
        thumb="img/exp/futebol-thumb.webp",
        chart=True,
        tag={"pt": "Esporte", "en": "Sport"},
        date={"pt": "12 de novembro de 2026", "en": "12 November 2026"},
        title={
            "pt": "Onde a física ajuda no futebol, e onde ela não ajudou",
            "en": "Where physics helps in football, and where it did not",
        },
        lead={
            "pt": "Quatro perguntas com os mesmos dados públicos e a mesma regra: um modelo só com o dado contra outro que também conhece a física. Em três frentes a física ganha, na quarta não ganha nada, e o resultado negativo está publicado do mesmo jeito.",
            "en": "Four questions on the same public data and the same rule: a data-only model against one that also knows the physics. Physics wins in three of them, gains nothing in the fourth, and the negative result is published all the same.",
        },
        metric={
            "pt": ("2,44 m", "de erro no pouso da bola, contra 7,51 m do ajuste polinomial"),
            "en": ("2.44 m", "of landing error, against 7.51 m for the polynomial fit"),
        },
        limits={
            "pt": "Os dados são públicos e amostrais: três jogos de rastreamento (SkillCorner) e dois de eventos (Metrica), com um jogo para ajustar e outro para testar. O ajuste de gravidade livre devolve 6,1 m/s² como mediana, o que mede o viés do dado de transmissão, não a física da bola. No xG a física não melhorou o modelo, e isso está no texto.",
            "en": "The data is public and small: three tracking matches (SkillCorner) and two event matches (Metrica), one match to fit and another to test. The free-gravity fit returns 6.1 m/s² as a median, which measures the broadcast data's bias, not the ball's physics. On expected goals physics did not improve the model, and that is stated in the text.",
        },
        body={
            "pt": [
                ("p", "Dado de rastreamento e de eventos é barato e abundante, e a tentação é jogar tudo num modelo. A pergunta deste experimento é mais estreita e mais útil: quando a física entra, ela <b>paga</b>? Em quatro frentes, a resposta não foi a mesma."),
                ("h2", "A bola: arrasto, Magnus e uma gravidade que não é 9,81"),
                ("p", "Em voos altos de dados públicos de rastreamento, o ajuste que deixa a gravidade livre devolve <b>6,09 m/s²</b> como mediana. A bola não ficou mais leve: o dado de transmissão tem viés, e o ajuste o expõe em vez de escondê-lo. Em chutes simulados com 0,2 m de ruído, o mesmo ajuste recupera o coeficiente de arrasto com erro de 0,024."),
                ("p", "Na prática, prever onde a bola pousa olhando só a primeira metade do voo: o ajuste polinomial erra 7,51 m; arrasto mais Magnus erra 3,37 m; o modelo híbrido, 2,55 m; o modelo aprendido, <b>2,44 m</b>. Todos avaliados nos jogos que ficaram fora do ajuste."),
                ("fig", ("img/exp/futebol-pouso.webp", "Erro horizontal de pouso por método, em jogos fora do ajuste", "Erro horizontal de pouso, por método, nos jogos que ficaram fora do ajuste. A caixa é a mediana e os quartis, o bigode vai até o extremo. O polinomial erra três vezes mais que o modelo aprendido.")),
                ("fig", ("img/exp/futebol-voo.webp", "Três voos reais com o ajuste de gravidade livre", "Três voos reais e o ajuste com gravidade livre: 5,2, 1,6 e 0,1 m/s². A dispersão é do dado, e é por isso que o resultado é reportado como mediana e não como um valor único.")),
                ("h2", "O passe: o campo de controle contra o modelo só de dados"),
                ("p", "O controle de campo calcula, para cada ponto do gramado, se um jogador chega antes da bola. O modelo de passe que usa esse campo, com o tempo de reação do jogador, teve log-loss de <b>0,150</b> no jogo de teste; a regressão logística só com features de evento ficou em 0,174 e o gradient boosting, em 0,231. Um jogo para ajustar, o outro para testar."),
                ("fig", ("img/exp/futebol-controle.webp", "Confiabilidade do modelo de passe que usa controle de campo", "Confiabilidade do modelo de passe: quando ele diz 0,3, a frequência observada fica perto de 0,3. Um modelo que acerta a probabilidade serve para decidir em campo; um que só ordena bem, não.")),
                ("h2", "O xG: aqui a física não pagou"),
                ("p", "Em finalizações da Euro 2024, o modelo com as features físicas deu log-loss de <b>0,2429</b> contra <b>0,2413</b> do mesmo modelo sem elas. Pior, e dentro do ruído. O xG publicado do StatsBomb, na mesma base de teste, fica em 0,2267. A conclusão ficou registrada como negativa: para finalização, o que decide é o contexto do chute, não a trajetória da bola."),
                ("h2", "O que sobra"),
                ("p", "Três de quatro. Onde a física é o fenômeno, como a bola no ar e o tempo de chegada de um jogador, ela ganha por larga margem. Onde ela entra como mais uma coluna numa tabela de features, não ganha nada. Saber a diferença antes de vender a solução é metade do trabalho."),
            ],
            "en": [
                ("p", "Tracking and event data is cheap and abundant, and the temptation is to throw all of it into a model. The question in this experiment is narrower and more useful: when physics comes in, does it <b>pay</b>? Across four fronts, the answer was not the same."),
                ("h2", "The ball: drag, Magnus and a gravity that is not 9.81"),
                ("p", "On high flights in public tracking data, the fit that leaves gravity free returns <b>6.09 m/s²</b> as a median. The ball did not get lighter: the broadcast data carries a bias, and the fit exposes it instead of hiding it. On simulated kicks with 0.2 m of noise, the same fit recovers the drag coefficient to within 0.024."),
                ("p", "In practice, predicting where the ball lands from the first half of the flight alone: the polynomial fit errs 7.51 m; drag plus Magnus errs 3.37 m; the hybrid model 2.55 m; the learned model <b>2.44 m</b>. All of them scored on the matches left out of the fit."),
                ("fig", ("img/exp/futebol-pouso.webp", "Horizontal landing error per method, on held-out matches", "Horizontal landing error per method, on the matches held out of the fit. The box is the median and the quartiles, the whisker reaches the extreme. The polynomial errs three times more than the learned model.")),
                ("fig", ("img/exp/futebol-voo.webp", "Three real flights with the free-gravity fit", "Three real flights and the free-gravity fit: 5.2, 1.6 and 0.1 m/s². The spread belongs to the data, which is why the result is reported as a median and not as a single value.")),
                ("h2", "The pass: pitch control against the data-only model"),
                ("p", "Pitch control computes, for every point of the pitch, whether a player gets there before the ball. The pass model that uses that field, with the player's reaction time, scored a log-loss of <b>0.150</b> on the test match; logistic regression on event features alone scored 0.174 and gradient boosting 0.231. One match to fit, the other to test."),
                ("fig", ("img/exp/futebol-controle.webp", "Reliability of the pass model that uses pitch control", "Reliability of the pass model: when it says 0.3, the observed frequency lands near 0.3. A model that gets the probability right can be used to decide on the pitch; one that only ranks well cannot.")),
                ("h2", "Expected goals: here physics did not pay"),
                ("p", "On Euro 2024 shots, the model with the physics features scored a log-loss of <b>0.2429</b> against <b>0.2413</b> for the same model without them. Worse, and inside the noise. The published StatsBomb xG on the same test set sits at 0.2267. The conclusion was recorded as negative: for a shot, what decides is the context, not the ball's trajectory."),
                ("h2", "What is left"),
                ("p", "Three out of four. Where physics is the phenomenon, as with a ball in the air or a player's time to reach a point, it wins by a wide margin. Where it enters as one more column in a feature table, it wins nothing. Knowing the difference before selling the solution is half the work."),
            ],
        },
    ),
    dict(
        slug="co2-supercritico",
        iso="2026-11-11",
        mins=7,
        thumb="img/exp/co2-identidades.webp",
        chart=True,
        tag={"pt": "Termodinâmica", "en": "Thermodynamics"},
        date={"pt": "11 de novembro de 2026", "en": "11 November 2026"},
        title={
            "pt": "O substituto mais preciso era o que quebrava a termodinâmica",
            "en": "The more accurate surrogate was the one breaking thermodynamics",
        },
        lead={
            "pt": "Duas famílias de substituto para CO₂ perto do ponto crítico, com os mesmos dados e o mesmo orçamento de treino. A rede direta acerta mais e viola a identidade de c_v em 1.100%. A de potencial erra mais e, com convexidade na entrada, mantém as seis identidades abaixo de 0,002%.",
            "en": "Two families of surrogate for CO₂ near the critical point, on the same data and the same training budget. The direct network is more accurate and violates the c_v identity by 1,100%. The potential one errs more and, with input convexity, keeps all six identities below 0.002%.",
        },
        metric={
            "pt": ("1.100%", "de violação da identidade de c_v no substituto direto, contra 0,0021% no potencial com convexidade"),
            "en": ("1,100%", "violation of the c_v identity in the direct surrogate, against 0.0021% in the convex potential one"),
        },
        limits={
            "pt": "O alvo é uma equação de estado (Span & Wagner, 1996), não um ensaio: o que está medido é a fidelidade ao modelo de referência, não ao CO₂ real. O domínio é o CO₂ supercrítico perto do ponto crítico, com 5 sementes e intervalos de 95%. Na extrapolação mais quente, a rede de potencial (MLP) ficou estável em 33% dos pontos, contra 100% da rede direta, e com 9.000 passos de treino a diferença de erro na região de treino deixa de ser significativa. O potencial custa de 4 a 10 vezes mais tempo de treino.",
            "en": "The target is an equation of state (Span & Wagner, 1996), not a test: what is measured is fidelity to the reference model, not to real CO₂. The domain is supercritical CO₂ near the critical point, with 5 seeds and 95% intervals. In the hotter extrapolation the potential network (MLP) was stable on 33% of the points, against 100% for the direct one, and at 9,000 training steps the error gap in the training region stops being significant. The potential costs four to ten times more training time.",
        },
        body={
            "pt": [
                ("p", "Uma rede neural que devolve pressão, entropia, calor específico e velocidade do som, cada uma pela sua própria saída, pode ser muito precisa e ainda assim inútil: nada no treino obriga as derivadas que ligam essas grandezas a continuarem valendo. Perto do ponto crítico, onde as propriedades variam rápido, essa diferença decide se o resultado pode entrar num solver."),
                ("h2", "O experimento"),
                ("p", "Mesmos dados (CoolProp sobre a equação de Span & Wagner), mesmos passos de treino, mesmas sementes. Três modelos: rede direta, com uma saída por propriedade; rede de potencial, que aprende a energia de Helmholtz e tira cada propriedade por derivada; e a versão com convexidade na entrada (ICNN, Amos e outros, 2017). A avaliação cobre a região de treino, duas extrapolações (mais quente e mais denso) e seis identidades termodinâmicas."),
                ("h2", "O número que separa os dois"),
                ("p", "Erro RMS normalizado pelo desvio da propriedade, na região de treino: <b>0,0995</b> para a rede direta, <b>1,61</b> para a de potencial e <b>1,24</b> para a versão com convexidade. A direta é cerca de <b>16 vezes mais precisa</b>, com um sexto do tempo de treino (21 s por semente, contra 85 s e 213 s)."),
                ("p", "Nas identidades, o resultado se inverte. Violação relativa no percentil 95: a rede direta viola a relação de Maxwell em <b>41%</b>, a dependência de c_v com a densidade em <b>1.100%</b> e a relação de Mayer em 240%. A de potencial fica em 0,0028% na Maxwell e 0,0003% na de c_v. A exceção é a velocidade do som, onde o potencial sem convexidade é pior que a rede direta, 540% contra 88%, e é justamente o que a versão com convexidade corrige: 0,001%."),
                ("fig", ("img/exp/co2-identidades.webp", "Violação relativa das identidades termodinâmicas, por modelo", "Violação relativa das seis identidades termodinâmicas, percentil 95, em escala logarítmica de 10⁻⁷ a 10. Vermelho, rede direta; azul, potencial; verde, potencial com convexidade. A barra azul de velocidade do som é a exceção que o texto discute, e a verde mostra o que a convexidade resolve.")),
                ("fig", ("img/exp/co2-erros.webp", "Erro de propriedade nas três regiões de avaliação", "O outro lado da moeda: o erro de propriedade nas três regiões. Onde a rede direta é mais precisa, e é por uma ordem de grandeza.")),
                ("h2", "Por que o erro não é o critério"),
                ("p", "Um solver que recebe calor específico e velocidade do som de fontes que não conversam entre si não converge, ou converge para o que não devia. A rede direta otimiza cada propriedade contra o dado, e nada no treino impede as derivadas de se contradizerem: por isso ela acerta cada número e erra a relação entre eles. Na rede de potencial toda propriedade sai da mesma função, então as identidades valem por construção, e o que sobra é o resíduo do ajuste."),
                ("p", "O preço está do outro lado, e é honesto dizer qual é. O potencial treina de quatro a dez vezes mais devagar, e fora do domínio ele desestabiliza: na extrapolação mais quente, só 33% dos pontos ficaram estáveis, contra 100% da rede direta. Com o triplo de passos, e mais sementes, a diferença de erro na região de treino deixa de ser significativa, o que sugere que a vantagem da rede direta é de orçamento, não de arquitetura."),
                ("fig", ("img/exp/co2-isotermas.webp", "Isotermas perto do ponto crítico para os três modelos", "Isotermas perto do ponto crítico, que é onde um erro de 1% em densidade vira um erro grande em pressão. É também a região em que os dois tipos de substituto mais se afastam.")),
                ("h2", "O que isso decide"),
                ("p", "Para interpolar propriedades num pós-processamento, onde ninguém vai derivar nada, a rede direta é a escolha. Para alimentar um solver de CFD, a de potencial, com o erro declarado ao lado. O experimento não elege um vencedor: ele põe preço em cada um, que é o que faltava para escolher."),
            ],
            "en": [
                ("p", "A neural network that returns pressure, entropy, heat capacity and speed of sound, each from its own output, can be very accurate and still useless: nothing in the training forces the derivatives that link those quantities to keep holding. Near the critical point, where properties vary fast, that difference decides whether the result can go into a solver."),
                ("h2", "The experiment"),
                ("p", "Same data (CoolProp over the Span & Wagner equation), same training steps, same seeds. Three models: a direct network, one output per property; a potential network, which learns the Helmholtz energy and takes every property as a derivative; and the input-convex version (ICNN, Amos and others, 2017). Evaluation covers the training region, two extrapolations (hotter and denser) and six thermodynamic identities."),
                ("h2", "The number that separates them"),
                ("p", "RMS error normalised by the property's standard deviation, in the training region: <b>0.0995</b> for the direct network, <b>1.61</b> for the potential one and <b>1.24</b> for the convex version. The direct one is about <b>16 times more accurate</b>, on a sixth of the training time (21 s per seed, against 85 s and 213 s)."),
                ("p", "On the identities, the result inverts. Relative violation at the 95th percentile: the direct network violates the Maxwell relation by <b>41%</b>, the density dependence of c_v by <b>1,100%</b> and the Mayer relation by 240%. The potential one sits at 0.0028% on Maxwell and 0.0003% on the c_v one. The exception is the speed of sound, where the potential network without convexity is worse than the direct one, 540% against 88%, and that is exactly what the convex version fixes: 0.001%."),
                ("fig", ("img/exp/co2-identidades.webp", "Relative violation of the thermodynamic identities, per model", "Relative violation of the six thermodynamic identities, 95th percentile, on a log scale from 10⁻⁷ to 10. Red, direct network; blue, potential; green, potential with convexity. The blue speed-of-sound bar is the exception the text discusses, and the green one shows what convexity fixes.")),
                ("fig", ("img/exp/co2-erros.webp", "Property error across the three evaluation regions", "The other side of the coin: property error across the three regions. Where the direct network is more accurate, and it is by an order of magnitude.")),
                ("h2", "Why error is not the criterion"),
                ("p", "A solver handed heat capacity and speed of sound from sources that do not agree with each other either fails to converge or converges to something it should not. The direct network optimises each property against the data, and nothing in the training stops the derivatives from contradicting one another: that is why it gets every number right and the relation between them wrong. In the potential network every property comes from the same function, so the identities hold by construction, and what is left is the fit residual."),
                ("p", "The price is on the other side, and it is fair to state it. The potential trains four to ten times slower, and outside the domain it destabilises: in the hotter extrapolation only 33% of the points stayed stable, against 100% for the direct network. With triple the steps, and more seeds, the error gap in the training region stops being significant, which suggests the direct network's advantage is one of budget, not of architecture."),
                ("fig", ("img/exp/co2-isotermas.webp", "Isotherms near the critical point for the three models", "Isotherms near the critical point, which is where a 1% error in density becomes a large error in pressure. It is also the region where the two kinds of surrogate drift furthest apart.")),
                ("h2", "What this decides"),
                ("p", "To interpolate properties in post-processing, where nobody will differentiate anything, the direct network is the choice. To feed a CFD solver, the potential one, with the error stated beside it. The experiment crowns no winner: it puts a price on each, which is what was missing in order to choose."),
            ],
        },
    ),
    dict(
        slug="guardrail-veriphysics",
        iso="2026-10-02",
        mins=6,
        thumb="img/verificacao.jpg",
        tag={"pt": "Verificação", "en": "Verification"},
        date={"pt": "2 de outubro de 2026", "en": "2 October 2026"},
        title={
            "pt": "O que a perda de treino escondeu",
            "en": "What the training loss was hiding",
        },
        lead={
            "pt": "Um modelo já treinado, com loss saudável no relatório, e o resíduo da física mais de cem vezes acima do limite. Foi assim que o guardrail entrou no produto.",
            "en": "An already-trained model, with a healthy loss in the report, and a physics residual more than a hundred times over the limit. That is how the guardrail became part of the product.",
        },
        metric={
            "pt": ("resíduo >100×", "acima do limiar, com a loss de treino saudável"),
            "en": (">100× residual", "over the threshold, with a healthy training loss"),
        },
        limits={
            "pt": "O guardrail diz que o resultado não pode ser usado sem explicação; ele não diz qual é o erro, e não substitui um ensaio. O modelo do cliente é confidencial: o que está publicado é o comportamento da checagem, não o modelo.",
            "en": "The guardrail says the result cannot be used without an explanation; it does not say what the error is, and it does not replace a test. The client's model is confidential: what is published is how the check behaves, not the model.",
        },
        body={
            "pt": [
                ("p", "Um cliente chegou com um modelo de PINN já treinado. O relatório mostrava o que todo relatório mostra: loss caindo, erro pequeno nos pontos de teste, gráfico bonito. A pergunta era simples e é a mesma que a engenharia faz sempre: dá para usar isso numa decisão de projeto?"),
                ("h2", "O que o guardrail olha"),
                ("p", "O VeriPhysics não olha a loss. Ele pega o modelo treinado e mede o que a loss não mede: o resíduo da equação que o modelo deveria satisfazer, a consistência das condições de contorno e a convergência numérica no conjunto de pontos onde ele foi avaliado."),
                ("fig", ("img/verificacao.jpg", "Run do VeriPhysics com nota por checagem", "Um run do VeriPhysics: nota 100/100 nas duas checagens que rodaram, cobertura 0,50. As duas que não rodaram aparecem como “not run”, e derrubam a cobertura, que é o que a nota esconde.")),
                ("h2", "O número"),
                ("p", "O resíduo ficou <b>mais de 100 vezes acima do limiar</b> aceito, com a loss de treino aparentemente saudável. O modelo acertava os pontos que estavam no histórico e violava a física entre eles, que é exatamente onde ninguém olha."),
                ("p", "No mesmo período apareceu outro caso, esse de análise estrutural: uma viga sem apoios que terminou com a mensagem “Job finished” e deslocamento de 1,8×10¹¹ mm. O cálculo terminou; o resultado não existia. O preflight marca FAIL antes da execução, apontando o arquivo e a linha."),
                ("video", ("videos/app8.mp4", "videos/app8.jpg", "O app de preflight apontando o que vai falhar, antes de rodar")),
                ("h2", "Por que isso virou produto"),
                ("p", "Uma ferramenta que só mostra o resultado bonito empurra a decisão para a confiança. Uma ferramenta que mostra a checagem que não rodou devolve a decisão para a engenharia. A regra que ficou: <b>uma checagem que não rodou nunca conta como aprovada</b>, e a nota final é só o que rodou de fato."),
            ],
            "en": [
                ("p", "A client arrived with an already-trained PINN model. The report showed what every report shows: a falling loss, a small error on the test points, a nice plot. The question was simple, and it is the one engineering always asks: can this be used in a design decision?"),
                ("h2", "What the guardrail looks at"),
                ("p", "VeriPhysics does not look at the loss. It takes the trained model and measures what the loss does not: the residual of the equation the model is supposed to satisfy, the consistency of the boundary conditions, and the numerical convergence over the set of points where it was evaluated."),
                ("fig", ("img/verificacao.jpg", "A VeriPhysics run with a score per check", "A VeriPhysics run: 100/100 on the two checks that ran, coverage 0.50. The two that did not run show as “not run”, and they pull the coverage down, which is what the score alone hides.")),
                ("h2", "The number"),
                ("p", "The residual came out <b>more than 100 times over</b> the accepted threshold, with a training loss that looked healthy. The model matched the points in the history and violated the physics between them, which is exactly where nobody looks."),
                ("p", "Around the same time, another case came up on the structural side: an unsupported beam that finished with the message “Job finished” and a displacement of 1.8×10¹¹ mm. The run finished; the result did not exist. Preflight flags FAIL before execution, naming the file and the line."),
                ("video", ("videos/app8.mp4", "videos/app8.jpg", "The preflight app pointing at what will fail, before the run")),
                ("h2", "Why it became a product"),
                ("p", "A tool that only shows the good result pushes the decision onto trust. A tool that shows the check that did not run hands the decision back to engineering. The rule that stayed: <b>a check that did not run never counts as passed</b>, and the final score covers only what actually ran."),
            ],
        },
    ),
    dict(
        slug="asa-1920-projetos",
        iso="2026-09-20",
        mins=7,
        thumb="img/portfolio/13-aircraft-render-pressure.jpg",
        tag={"pt": "Otimização", "en": "Optimization"},
        date={"pt": "20 de setembro de 2026", "en": "20 September 2026"},
        title={
            "pt": "1.920 asas, três objetivos e 13% menos CO₂",
            "en": "1,920 wings, three objectives and 13% less CO₂",
        },
        lead={
            "pt": "Otimização multiobjetivo em CFD 3D: cada asa foi voada no OpenFOAM, e o resultado não é “a melhor asa”, é o mapa de trocas entre três objetivos que brigam entre si.",
            "en": "Multi-objective optimization in 3D CFD: every wing was flown in OpenFOAM, and the result is not “the best wing”, it is the map of trade-offs between three objectives that fight each other.",
        },
        metric={
            "pt": ("−13% CO₂/pax-km", "com a sustentação-alvo mantida em 0,04%"),
            "en": ("−13% CO₂/pax-km", "with target lift held to 0.04%"),
        },
        limits={
            "pt": "Otimização não prova que a asa é fabricável, estruturalmente viável ou boa fora das condições simuladas. O que está medido é arrasto, sustentação e CO₂ nas condições do estudo, conferidos no solver 3D.",
            "en": "Optimization does not prove the wing is manufacturable, structurally sound, or good outside the simulated conditions. What is measured is drag, lift and CO₂ under the study's conditions, checked in the 3D solver.",
        },
        body={
            "pt": [
                ("p", "Aumentar a eficiência de uma aeronave não é minimizar um número. Menos CO₂ por passageiro costuma vir com cruzeiro mais lento ou aproximação mais rápida; baixar a velocidade de aproximação costuma custar arrasto. O projeto é uma negociação, e negociação precisa de mapa, não de resposta única."),
                ("h2", "O que foi feito"),
                ("p", "1.920 geometrias de asa geradas e avaliadas com três objetivos ao mesmo tempo: CO₂ por passageiro-quilômetro, velocidade de cruzeiro e velocidade de aproximação. O algoritmo evolutivo (NSGA-II) escolhe a próxima leva; um substituto treinado nas rodadas anteriores guia a busca; os candidatos que sobram são reverificados no OpenFOAM 3D antes de entrar no resultado."),
                ("fig", ("img/portfolio/13-aircraft-render-pressure.jpg", "Pressão na pele de uma das asas otimizadas", "Pressão na pele (Cp) em OpenFOAM 3D, um dos 1.920 projetos avaliados.")),
                ("h2", "O número"),
                ("p", "<b>−13% de CO₂ por passageiro-quilômetro</b> no conjunto de soluções, com −18,2% de arrasto de perfil e a sustentação-alvo mantida dentro de 0,04%."),
                ("fig", ("img/portfolio/aero_pareto.jpg", "Frente de Pareto com três objetivos", "A frente de Pareto: nenhum ponto domina outro nos três objetivos. Cada ponto é uma troca, não uma vitória.")),
                ("h2", "Como ler o resultado"),
                ("p", "A saída é um conjunto de asas, não uma. Quem quer menos CO₂ aceita um cruzeiro diferente; quem precisa de aproximação lenta escolhe outro ponto da frente. A otimização mostra o preço de cada escolha; quem escolhe é a engenharia."),
                ("video", ("videos/hero-aero.mp4", "videos/hero-aero.jpg", "O campo de pressão girando, do projeto ao resultado")),
            ],
            "en": [
                ("p", "Making an aircraft more efficient is not about minimising one number. Less CO₂ per passenger usually comes with a slower cruise or a faster approach; slowing the approach usually costs drag. The design is a negotiation, and a negotiation needs a map, not a single answer."),
                ("h2", "What was done"),
                ("p", "1,920 wing geometries generated and evaluated against three objectives at once: CO₂ per passenger-kilometre, cruise speed and approach speed. The evolutionary algorithm (NSGA-II) picks the next batch; a surrogate trained on the previous rounds guides the search; the candidates that survive are re-checked in 3D OpenFOAM before they enter the result."),
                ("fig", ("img/portfolio/13-aircraft-render-pressure.jpg", "Skin pressure on one of the optimized wings", "Skin pressure (Cp) in 3D OpenFOAM, one of the 1,920 designs evaluated.")),
                ("h2", "The number"),
                ("p", "<b>−13% CO₂ per passenger-kilometre</b> across the solution set, with −18.2% profile drag and target lift held to within 0.04%."),
                ("fig", ("img/portfolio/aero_pareto.jpg", "Pareto front with three objectives", "The Pareto front: no point dominates another across the three objectives. Every point is a trade, not a win.")),
                ("h2", "How to read the result"),
                ("p", "The output is a set of wings, not one. Whoever wants less CO₂ accepts a different cruise; whoever needs a slow approach picks another point on the front. Optimization shows the price of each choice; engineering makes it."),
                ("video", ("videos/hero-aero.mp4", "videos/hero-aero.jpg", "The pressure field turning, from design to result")),
            ],
        },
    ),
    dict(
        slug="gemeo-hx201",
        iso="2026-09-05",
        mins=6,
        thumb="img/twin.jpg",
        tag={"pt": "Gêmeo digital", "en": "Digital twin"},
        date={"pt": "5 de setembro de 2026", "en": "5 September 2026"},
        title={
            "pt": "O gêmeo que avisou 2,6 horas antes",
            "en": "The twin that warned 2.6 hours ahead",
        },
        lead={
            "pt": "Um permutador em operação, uma incrustação que cresce sem aviso e um modelo que precisa merecer confiança antes de entrar em planta. O erro medido foi 0,216 °C.",
            "en": "An exchanger in operation, fouling that grows without warning, and a model that has to earn trust before it goes on the plant floor. The measured error was 0.216 °C.",
        },
        metric={
            "pt": ("0,216 °C", "de erro contra sonda redundante; alarme 2,6 h antes"),
            "en": ("0.216 °C", "of error against a redundant probe; alarm 2.6 h ahead"),
        },
        limits={
            "pt": "A banda é de estado e foi calibrada numa janela separada; a antecedência de 2,6 h vem de uma extrapolação linear, com o erro da previsão reportado. Fora do regime observado, o modelo não vale.",
            "en": "The band is a state band, calibrated on a separate window; the 2.6 h lead comes from a linear extrapolation, with the forecast error reported. Outside the observed regime, the model does not hold.",
        },
        body={
            "pt": [
                ("p", "Incrustação não quebra o equipamento de uma vez: ela rouba eficiência até o processo sair da faixa. O que a operação quer é antecedência, e a pergunta difícil nunca é a previsão, é se o modelo merece ser ouvido."),
                ("h2", "Como o gêmeo foi validado"),
                ("p", "O modelo (HX-201, um permutador com incrustação) foi ajustado <b>apenas com o histórico anterior à janela de validação</b>. Uma sonda redundante ficou fora do ajuste e serviu de juiz. A banda de incerteza também foi calibrada numa janela separada, então a cobertura relatada não é a do próprio treino."),
                ("fig", ("img/twin.jpg", "Ativo industrial em 3D com painel de leitura ao vivo", "O ativo em 3D com a leitura viva ao lado: rotação, potência, empuxo e vento no instante consultado.")),
                ("h2", "Os números"),
                ("p", "<b>0,216 °C</b> de erro contra a sonda; <b>95,5%</b> de cobertura da banda na janela de validação; incrustação estimada em 0,001651 m²K/W contra 0,001637 verdadeiro; e o alarme disparando <b>2,6 horas antes</b> do cruzamento medido."),
                ("h2", "O que a operação faz com isso"),
                ("p", "Antecedência é tempo para planejar limpeza, negociar uma janela de parada ou ajustar carga. O gêmeo não decide nada: ele avisa, e diz com que erro está avisando."),
            ],
            "en": [
                ("p", "Fouling does not break equipment all at once: it drains efficiency until the process drifts out of band. What operations wants is lead time, and the hard question is never the forecast, it is whether the model deserves to be heard."),
                ("h2", "How the twin was validated"),
                ("p", "The model (HX-201, a fouled exchanger) was fitted <b>only on the history before the validation window</b>. A redundant probe was kept out of the fit and served as judge. The uncertainty band was calibrated on a separate window too, so the reported coverage is not the model's own training score."),
                ("fig", ("img/twin.jpg", "Industrial asset in 3D with a live reading panel", "The asset in 3D beside the live reading: rotation, power, thrust and wind at the moment queried.")),
                ("h2", "The numbers"),
                ("p", "<b>0.216 °C</b> of error against the probe; <b>95.5%</b> band coverage on the validation window; fouling estimated at 0.001651 m²K/W against a true 0.001637; and the alarm firing <b>2.6 hours before</b> the measured crossing."),
                ("h2", "What operations does with it"),
                ("p", "Lead time is time to plan a cleaning, negotiate a shutdown window or shift load. The twin decides nothing: it warns, and states the error it is warning with."),
            ],
        },
    ),
    dict(
        slug="erosao-curva-90",
        iso="2026-08-28",
        mins=5,
        thumb="img/erosao.jpg",
        tag={"pt": "CFD", "en": "CFD"},
        date={"pt": "28 de agosto de 2026", "en": "28 August 2026"},
        title={
            "pt": "Erosão numa curva de 90°: a conta bateu com o ensaio",
            "en": "Erosion in a 90° bend: the numbers met the experiment",
        },
        lead={
            "pt": "Ar com areia a 15 m/s, uma curva de 90° e um ensaio publicado para comparar. O resultado ficou entre 1,05 e 1,49 vez o medido, dentro do fator 2 que a indústria aceita.",
            "en": "Sand-laden air at 15 m/s, a 90° bend and a published experiment to compare against. The result landed between 1.05 and 1.49 times the measured value, inside the factor-2 band industry accepts.",
        },
        metric={
            "pt": ("1,05–1,49×", "do ensaio aberto de Vieira et al. 2016"),
            "en": ("1.05–1.49×", "of the open experiment by Vieira et al. 2016"),
        },
        limits={
            "pt": "O critério é o fator 2, não precisão de 1%. E resíduo estável não prova que o arrasto estabilizou, por isso a comparação é com o ensaio, não com o próprio solver.",
            "en": "The criterion is the factor-2 band, not 1% precision. And flat residuals do not prove drag has settled, which is why the comparison is against the experiment, not against the solver itself.",
        },
        body={
            "pt": [
                ("p", "Erosão não é um fenômeno para precisão de 1%: depende da distribuição de partículas, do material e do histórico de operação. A prática aceita um fator 2. O compromisso do projeto era ficar dentro dele, e dizer isso em voz alta, em vez de prometer uma precisão que o fenômeno não tem."),
                ("h2", "O que foi feito"),
                ("p", "O pipeline CFD completo: geometria da tubulação, malha, OpenFOAM resolvendo o escoamento com partículas, modelo de erosão na parede e um substituto treinado para responder rápido em novas condições de operação."),
                ("fig", ("img/erosao.jpg", "Mapa de erosão na parede de uma curva de 90°", "Mapa de erosão na parede (ensaio T3): tubulação inteira e o zoom na curva, com o pico na parede externa. Escala em mm/ano.")),
                ("h2", "Os números"),
                ("p", "<b>1,05 a 1,49 vez</b> a taxa medida no ensaio de Vieira et al. (2016). O substituto ficou em <b>1,0% de erro</b> na perda de carga, em pontos que não viu no treino. As 32 simulações do estudo, da geometria ao modelo treinado, levaram 23 minutos."),
                ("h2", "O que isso muda"),
                ("p", "Com o substituto, variar diâmetro, raio de curva e vazão deixa de custar um dia por ponto. O CFD continua sendo a referência; o que muda é quantas perguntas dá para fazer antes de pagar o caso caro."),
            ],
            "en": [
                ("p", "Erosion is not a phenomenon for 1% precision: it depends on the particle distribution, the material and the operating history. Practice accepts a factor of 2. The commitment on this project was to land inside that band, and to say so out loud, instead of promising precision the phenomenon does not have."),
                ("h2", "What was done"),
                ("p", "The full CFD pipeline: pipe geometry, mesh, OpenFOAM solving the particle-laden flow, a wall-erosion model, and a surrogate trained to answer quickly under new operating conditions."),
                ("fig", ("img/erosao.jpg", "Wall erosion map on a 90° bend", "Wall erosion map (case T3): the whole pipe and the zoom into the bend, with the peak on the outer wall. Scale in mm/year.")),
                ("h2", "The numbers"),
                ("p", "<b>1.05 to 1.49 times</b> the rate measured in the Vieira et al. (2016) experiment. The surrogate came in at <b>1.0% error</b> on pressure drop, at points it never saw in training. The study's 32 simulations, from geometry to trained model, took 23 minutes."),
                ("h2", "What it changes"),
                ("p", "With the surrogate, varying diameter, bend radius and flow rate no longer costs a day per point. CFD stays the reference; what changes is how many questions you can ask before paying for the expensive case."),
            ],
        },
    ),
    dict(
        slug="substituto-termico",
        iso="2026-07-30",
        mins=6,
        thumb="img/surrogate_speed_rerun.jpg",
        tag={"pt": "Modelo substituto", "en": "Surrogate model"},
        date={"pt": "30 de julho de 2026", "en": "30 July 2026"},
        title={
            "pt": "Um dissipador que responde 200 mil vezes mais rápido",
            "en": "A heat sink that answers 200,000 times faster",
        },
        lead={
            "pt": "Sete geometrias de dissipador, um solver 3D e um modelo que devolve a temperatura de junção em milissegundos. Erro médio de 4,46%; pior caso, 7,35%.",
            "en": "Seven heat-sink geometries, a 3D solver and a model that returns junction temperature in milliseconds. 4.46% mean error; 7.35% worst case.",
        },
        metric={
            "pt": ("~200.000×", "mais rápido, com 4,46% de erro médio"),
            "en": ("~200,000×", "faster, at 4.46% mean error"),
        },
        limits={
            "pt": "4,46% é a média dentro da faixa de geometria treinada; fora dela o erro não está medido. Determinismo não é acerto: os mesmos números em toda rodada não dizem nada sobre regiões onde não há dado.",
            "en": "4.46% is the mean inside the trained geometry range; outside it, the error is unmeasured. Determinism is not accuracy: the same numbers on every run say nothing about regions where there is no data.",
        },
        body={
            "pt": [
                ("p", "Quem projeta dissipador conhece a rotina: cada mudança de aleta é uma nova simulação 3D. Sete variantes viram uma semana; setenta viram o projeto inteiro."),
                ("h2", "O que foi feito"),
                ("p", "Sete geometrias de dissipador resolvidas em FEniCS/dolfinx 3D, com malha gerada em gmsh. Depois, um substituto treinado nessas simulações e comparado contra o solver <b>em pontos que não estavam no treino</b>, a referência é sempre externa ao modelo."),
                ("fig", ("img/surrogate_speed_rerun.jpg", "Substituto contra FEA 3D: erro e ganho de tempo", "À esquerda, temperatura de junção: substituto contra FEA 3D, erro médio de 4,46% e máximo de 7,35%. À direita, o ganho de tempo por geometria, média de 227.059×.")),
                ("h2", "Os números"),
                ("p", "Cerca de <b>200 mil vezes mais rápido</b> (a média medida nas sete geometrias foi 227.059×, com o pior caso em 57.222×). Erro médio de <b>4,46%</b>, pior caso de <b>7,35%</b>. E a previsão é determinística: três rodadas, em dias diferentes, devolveram os mesmos números."),
                ("video", ("videos/app1.mp4", "videos/app1.jpg", "O app de dimensionamento térmico rodando: a resposta sai enquanto você digita")),
                ("h2", "O que isso muda"),
                ("p", "Explorar o espaço de projeto passa a caber numa reunião. O solver continua sendo chamado, para validar a escolha, não para descobrir o ótimo."),
                ("fig", ("img/results/bench_true_vs_pred.png", "Verdadeiro contra previsto", "Verdadeiro contra previsto: três modelos, a mesma condição de contorno.")),
            ],
            "en": [
                ("p", "Anyone who designs heat sinks knows the routine: every change of fin is a new 3D simulation. Seven variants become a week; seventy become the whole project."),
                ("h2", "What was done"),
                ("p", "Seven heat-sink geometries solved in 3D FEniCS/dolfinx, with meshes built in gmsh. Then a surrogate trained on those simulations and compared against the solver <b>at points that were not in the training set</b>, the reference is always external to the model."),
                ("fig", ("img/surrogate_speed_rerun.jpg", "Surrogate against 3D FEA: error and speed-up", "Left: junction temperature, surrogate against 3D FEA, mean error 4.46% and worst case 7.35%. Right: the time gained per geometry, a mean of 227,059×.")),
                ("h2", "The numbers"),
                ("p", "Around <b>200,000 times faster</b> (the measured mean across the seven geometries was 227,059×, with the worst case at 57,222×). Mean error of <b>4.46%</b>, worst case <b>7.35%</b>. And the prediction is deterministic: three runs, on different days, returned the same numbers."),
                ("video", ("videos/app1.mp4", "videos/app1.jpg", "The thermal sizing app running: the answer appears as you type")),
                ("h2", "What it changes"),
                ("p", "Exploring the design space now fits inside one meeting. The solver is still called, to validate the choice, not to discover the optimum."),
                ("fig", ("img/results/bench_true_vs_pred.png", "True against predicted", "True against predicted: three models, the same boundary condition.")),
            ],
        },
    ),
    dict(
        slug="malha-e-preflight",
        iso="2026-06-18",
        mins=5,
        thumb="img/eng/studio-report.webp",
        tag={"pt": "Verificação", "en": "Verification"},
        date={"pt": "18 de junho de 2026", "en": "18 June 2026"},
        title={
            "pt": "A falha que aparece antes de rodar",
            "en": "The failure that shows up before the run",
        },
        lead={
            "pt": "Boa parte do tempo perdido em simulação não é cálculo: é descobrir, depois de horas de fila, que a malha era ruim ou que o caso não tinha apoio. Duas checagens resolvem isso antes do play.",
            "en": "Most of the time lost in simulation is not compute: it is finding out, hours into the queue, that the mesh was poor or the case had no support. Two checks settle that before you press play.",
        },
        metric={
            "pt": ("idêntico ao checkMesh", "métricas de malha conferidas contra o OpenFOAM"),
            "en": ("identical to checkMesh", "mesh metrics checked against OpenFOAM"),
        },
        limits={
            "pt": "Malha boa não garante resultado bom, e preflight não substitui verificação de física. São o primeiro filtro, não o último.",
            "en": "A good mesh does not guarantee a good result, and preflight does not replace physics verification. These are the first filter, not the last.",
        },
        body={
            "pt": [
                ("p", "Um caso pode terminar com “finished” e estar errado. Sem apoio, a viga se desloca 1,8×10¹¹ mm e o solver não reclama. Com malha ruim, o campo sai colorido e sem significado. Nos dois casos, o erro só aparece quando alguém olha com cuidado, normalmente depois da fila."),
                ("h2", "O que foi feito"),
                ("p", "Duas checagens antes da execução. A de <b>malha</b> lê OpenFOAM, Gmsh, VTK, Abaqus e STL e devolve as métricas de qualidade, um heatmap e os piores elementos, com os mesmos números do checkMesh. O <b>preflight</b> lê o caso e devolve PASS, WARNING ou FAIL, com o arquivo e a linha do problema."),
                ("fig", ("img/eng/studio-report.webp", "Relatório de um job com as verificações e o status da evidência", "O relatório de uma execução: o gráfico, as verificações com valor e limite, e o status da evidência, aqui, “inconclusiva”, porque uma checagem não rodou.")),
                ("h2", "Os números"),
                ("p", "As métricas de malha batem com o checkMesh do OpenFOAM. O caso da viga sem apoios é pego <b>antes da execução</b>, como FAIL, em vez de virar um resultado com cara de resultado."),
                ("h2", "O que isso muda"),
                ("p", "A fila deixa de ser o lugar onde o erro é descoberto. E o relatório mostra o que não foi checado: independência de malha, por exemplo, só existe se alguém fez o estudo de refinamento, então ela aparece como “não rodou”, não como aprovada."),
            ],
            "en": [
                ("p", "A case can finish with “finished” and still be wrong. Unsupported, the beam moves 1.8×10¹¹ mm and the solver does not complain. With a poor mesh, the field comes out colourful and meaningless. In both cases the mistake only surfaces when someone looks closely, usually after the queue."),
                ("h2", "What was done"),
                ("p", "Two checks before execution. The <b>mesh</b> check reads OpenFOAM, Gmsh, VTK, Abaqus and STL and returns quality metrics, a heatmap and the worst elements, with the same numbers as checkMesh. <b>Preflight</b> reads the case and returns PASS, WARNING or FAIL, naming the file and the line."),
                ("fig", ("img/eng/studio-report.webp", "A job report with its verifications and evidence status", "A run's report: the chart, the checks with value and limit, and the evidence status, here “inconclusive”, because one check did not run.")),
                ("h2", "The numbers"),
                ("p", "The mesh metrics match OpenFOAM's checkMesh. The unsupported-beam case is caught <b>before execution</b>, as FAIL, instead of turning into a result that looks like a result."),
                ("h2", "What it changes"),
                ("p", "The queue stops being the place where mistakes are found. And the report shows what was not checked: mesh independence, for instance, only exists if someone ran the refinement study, so it appears as “did not run”, not as passed."),
            ],
        },
    ),
]

POST_BY_SLUG = {p["slug"]: p for p in POSTS}

# ---------------------------------------------------------------------------
# Pages and URLs
# ---------------------------------------------------------------------------

PAGES = {
    "home": "",
    "studio": "studio",
    "erosao": "erosao-em-tubulacao",
    "trocadores": "trocadores-e-termico",
    "valvulas": "valvulas-e-maquinas",
    "relatorios": "relatorios",
    "artigos": "artigos",
    "sucessos": "casos-de-sucesso",
    "lib": "lib",
}
for _post in POSTS:
    PAGES[f"post:{_post['slug']}"] = f"artigos/{_post['slug']}"
for _case in CS.CASES:
    PAGES[f"caso:{_case['slug']}"] = f"casos-de-sucesso/{_case['slug']}"


def url(lang: str, page: str) -> str:
    d = LANGUAGES[lang]["dir"]
    slug = PAGES[page]
    parts = [p for p in (d, slug) if p]
    return "/".join(parts) + ("/" if parts else "")


def up(lang: str, page: str) -> str:
    """Relative prefix to reach the site root from a page.

    The slug may itself hold more than one segment (``artigos/<slug>``), so the
    depth is counted per path segment, not per PAGES entry.
    """
    parts = [p for p in (LANGUAGES[lang]["dir"], PAGES[page]) if p]
    depth = sum(len(p.strip("/").split("/")) for p in parts)
    return "../" * depth


# ---------------------------------------------------------------------------
# Shared shell
# ---------------------------------------------------------------------------

NAV = {
    "pt": [("home", "Início"), ("studio", "Studio"), ("relatorios", "Relatórios"),
           ("artigos", "Artigos"), ("lib", "A lib")],
    "en": [("home", "Home"), ("studio", "Studio"), ("relatorios", "Reports"),
           ("artigos", "Articles"), ("lib", "The library")],
}

# Short labels for the footer and the cross-links between segment pages.
SEGLABELS = {
    "pt": {
        "erosao": "Erosão em tubulação",
        "trocadores": "Trocadores e térmico",
        "valvulas": "Válvulas e máquinas",
    },
    "en": {
        "erosao": "Erosion in piping",
        "trocadores": "Exchangers and thermal",
        "valvulas": "Valves and machinery",
    },
}

STRINGS = {
    "pt": {
        "skip": "Pular para o conteúdo",
        "wa": "Falar com um engenheiro",
        "wa_msg": "Olá! Vim pelo site e queria um orçamento: tenho um caso de simulação para discutir.",
        "cta_title": "Tem uma simulação lenta, cara ou difícil de verificar?",
        "cta_lead": "Mande o caso. Respondemos com um escopo fechado e uma métrica de sucesso mensurável, ou dizemos que o método clássico resolve melhor.",
        "cta_primary": "Pedir orçamento",
        "docs_nav": "Docs",
        "cta_short": "Falar com um engenheiro",
        "cta_secondary": "Começar pelo código",
        "foot_tag": "Physics AI de código aberto, com verificação como parte do produto. Modelos que mostram a conta.",
        "foot_platform": "Plataforma",
        "foot_code": "Código",
        "foot_contact": "Contato",
        "foot_law": "LAIS &amp; YAN LTDA · CNPJ 62.766.371/0001-36 · Entrega industrial com a Domus.",
        "foot_rights": "Apache-2.0 no código, verificação por padrão.",
        "lbl_products": "Início",
        "lbl_product": "PINNeAPPle Studio",
        "lbl_articles": "Artigos",
        "lbl_reports": "Relatórios de exemplo",
        "lbl_success": "Casos de sucesso",
        "lbl_lib": "A lib",
        "read_more": "Ler o artigo",
        "min_read": "min de leitura",
        "soon": "Em breve · 2027",
        "all_articles": "Ver todos os artigos",
        "pre_nav": "Pré-acesso",
        "pre_eyebrow": "Pré-acesso",
        "pre_title": "Entre na lista do PINNeAPPle Studio",
        "pre_lead": "O Studio abre em 2027, em prévia fechada. Quem entra na lista recebe o convite antes, na ordem de inscrição, e ajuda a decidir o que entra primeiro.",
        "pre_btn": "Quero pré-acesso",
        "pre_note": "O e-mail serve só para o convite do pré-acesso. Sem spam, e dá para sair em um clique.",
        "hero_note": "O primeiro botão abre o WhatsApp com o texto pronto. O segundo mostra o que sai no fim de um estudo.",
        "prod_note": "O primeiro botão abre o formulário de pré-acesso: três perguntas, e o convite sai em 2027. O segundo abre o WhatsApp com o texto pronto.",
    },
    "en": {
        "skip": "Skip to content",
        "wa": "Talk to an engineer",
        "wa_msg": "Hello! I found the PINNeAPPle Labs site and would like a quote: I have a simulation case to discuss.",
        "cta_title": "Got a simulation that is slow, expensive or hard to verify?",
        "cta_lead": "Send it over. We come back with a closed scope and a measurable success criterion, or we tell you the classical method does it better.",
        "cta_primary": "Request a quote",
        "docs_nav": "Docs",
        "cta_short": "Talk to an engineer",
        "cta_secondary": "Start from the code",
        "foot_tag": "Open-source Physics AI, with verification as part of the product. Models that show their work.",
        "foot_platform": "Platform",
        "foot_code": "Code",
        "foot_contact": "Contact",
        "foot_law": "LAIS &amp; YAN LTDA · CNPJ 62.766.371/0001-36 · Industrial delivery with Domus.",
        "foot_rights": "Apache-2.0 in the code, verification by default.",
        "lbl_products": "Home",
        "lbl_product": "PINNeAPPle Studio",
        "lbl_articles": "Articles",
        "lbl_reports": "Example reports",
        "lbl_success": "Success stories",
        "lbl_lib": "The library",
        "read_more": "Read the article",
        "min_read": "min read",
        "soon": "Coming soon · 2027",
        "all_articles": "See all articles",
        "pre_nav": "Early access",
        "pre_eyebrow": "Early access",
        "pre_title": "Get on the PINNeAPPle Studio list",
        "pre_lead": "The Studio opens in 2027, in a closed preview. Whoever joins the list gets the invite first, in sign-up order, and helps decide what ships first.",
        "pre_btn": "Get early access",
        "pre_note": "The e-mail is used for the early-access invite only. No spam, and one click to leave.",
        "hero_note": "The first button opens WhatsApp with the message ready. The second shows what comes out of a study.",
        "prod_note": "The first button opens the early-access form: three questions, and the invite goes out in 2027. The second opens WhatsApp with the message ready.",
    },
}

META = {
    "home": {
        "pt": dict(
            title="Estudo de CFD com escopo, prazo e erro declarados · PINNeAPPle Labs",
            desc="Estudo de simulação para indústria: você manda a geometria e a pergunta, recebe o escopo com prazo de 4 a 10 semanas e o preço definido a partir dele, e um relatório com o número verificado contra ensaio e o erro declarado.",
            og="img/portfolio/13-aircraft-render-pressure.jpg",
            type="website",
        ),
        "en": dict(
            title="CFD studies with scope, deadline and error stated · PINNeAPPle Labs",
            desc="Simulation studies for industry: you send the geometry and the question, you get the scope with a 4 to 10 week deadline and the price set from it, and a report with the number checked against an experiment and the error stated.",
            og="img/portfolio/13-aircraft-render-pressure.jpg",
            type="website",
        ),
    },
    "produto": {
        "pt": dict(
            title="PINNeAPPle Studio · lançamento em 2027",
            desc="Você escreve o problema de engenharia em português. A plataforma diz se cobre, confere o que já foi provado, roda e devolve o resultado com relatório e evidência. Lançamento em 2027.",
            og="img/eng/studio-home.jpg",
            type="website",
        ),
        "en": dict(
            title="PINNeAPPle Studio · launching in 2027",
            desc="You write the engineering problem in plain language. The platform says whether it covers it, checks what has been proven, runs it and returns the result with a report and evidence. Launching in 2027.",
            og="img/eng/studio-home.jpg",
            type="website",
        ),
    },
    "sucessos": {
        "pt": dict(
            title="Casos de sucesso · PINNeAPPle Labs",
            desc="Seis casos de engenharia, cada número conferido contra uma referência independente — e o que cada um ainda não prova.",
            og="img/casos/cfd04_mapa_erosao.png",
            type="website",
        ),
        "en": dict(
            title="Success stories · PINNeAPPle Labs",
            desc="Six engineering cases, every number checked against an independent reference — and what each one still does not prove.",
            og="img/casos/cfd04_mapa_erosao.png",
            type="website",
        ),
    },
    "artigos": {
        "pt": dict(
            title="Artigos · PINNeAPPle Labs",
            desc="Cada artigo é um experimento contado por inteiro: o que foi medido, contra o que foi comparado e onde ainda não chegamos.",
            og="img/surrogate_speed_rerun.jpg",
            type="website",
        ),
        "en": dict(
            title="Articles · PINNeAPPle Labs",
            desc="Every article is one experiment told in full: what was measured, what it was compared against, and where we are not there yet.",
            og="img/surrogate_speed_rerun.jpg",
            type="website",
        ),
    },
    "lib": {
        "pt": dict(
            title="A biblioteca PINNeAPPle · PINNeAPPle Labs",
            desc="Arquitetura, quickstart e o split honesto do código aberto da plataforma PINNeAPPle: 31 módulos, 248 exemplos, Apache-2.0.",
            og="img/portfolio/13-aircraft-render-pressure.jpg",
            type="website",
        ),
        "en": dict(
            title="The PINNeAPPle library · PINNeAPPle Labs",
            desc="Architecture, quickstart and the honest open-source split of the PINNeAPPle platform: 31 modules, 248 examples, Apache-2.0.",
            og="img/portfolio/13-aircraft-render-pressure.jpg",
            type="website",
        ),
    },
}



def meta(lang: str, page: str) -> dict:
    if page.startswith("caso:"):
        slug = page[5:]
        case = next(c for c in CS.CASES if c["slug"] == slug)
        C = case[lang]
        return dict(title=f'{C["h1"]} · PINNeAPPle Labs', desc=C["deck"][:180],
                    og="img/casos/" + C.get("og", "cfd04_mapa_erosao.png"), type="article")
    if page.startswith("post:"):
        p = POST_BY_SLUG[page[5:]]
        return dict(
            title=f"{p['title'][lang]} · PINNeAPPle Labs",
            desc=p["lead"][lang].replace("<b>", "").replace("</b>", ""),
            og=p["thumb"],
            type="article",
        )
    return META[page][lang]


def head(lang: str, page: str, root: str) -> str:
    L = LANGUAGES[lang]
    M = meta(lang, page)
    alt_pt = f"{SITE}/{url('pt', page)}"
    alt_en = f"{SITE}/{url('en', page)}"
    return f"""<!doctype html>
<html lang="{L['code']}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{M['title']}</title>
<meta name="description" content="{M['desc']}" />
<meta name="theme-color" content="#070a10" />
<link rel="canonical" href="{SITE}/{url(lang, page)}" />
<link rel="alternate" hreflang="pt-BR" href="{alt_pt}" />
<link rel="alternate" hreflang="en" href="{alt_en}" />
<link rel="alternate" hreflang="x-default" href="{alt_pt}" />
<meta property="og:type" content="{M['type']}" />
<meta property="og:title" content="{M['title']}" />
<meta property="og:description" content="{M['desc']}" />
<meta property="og:image" content="{SITE}/{M['og']}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml" />
<link rel="stylesheet" href="{root}fonts.css" />
<link rel="stylesheet" href="{root}styles.css" />
</head>
<body>
<a class="skip-link" href="#main">{STRINGS[lang]['skip']}</a>
"""


LOGO = """<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <path d="M16 2.6c1.35 2.1 1.95 4.4 1.8 6.7" stroke="#3dd6c4" stroke-width="1.9" stroke-linecap="round"/>
        <path d="M15.3 3.4c-2.6 1-4.4 2.9-5.4 5.3" stroke="#3dd6c4" stroke-width="1.9" stroke-linecap="round"/>
        <path d="M16.7 3.4c2.6 1 4.4 2.9 5.4 5.3" stroke="#3dd6c4" stroke-width="1.9" stroke-linecap="round"/>
        <ellipse cx="16" cy="20.1" rx="7.7" ry="9.2" fill="#f0b32e" fill-opacity=".18" stroke="#f0b32e" stroke-width="1.9"/>
        <path d="M12.4 12.6 19.6 27.6M19.6 12.6 12.4 27.6M8.9 17.6h14.2M10.6 22.6h10.8" stroke="#f0b32e" stroke-width="1.15" stroke-opacity=".7"/>
      </svg>"""

WA_ICON = """<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm5.8 14.06c-.24.68-1.4 1.3-1.93 1.35-.53.05-1.02.24-3.44-.72-2.9-1.15-4.72-4.15-4.86-4.34-.14-.19-1.15-1.53-1.15-2.92s.73-2.07 1-2.35c.26-.29.58-.36.77-.36l.55.01c.18 0 .42-.07.65.5.24.58.81 2 .88 2.14.07.14.12.31.02.5-.1.19-.15.31-.29.48l-.44.51c-.15.15-.3.31-.13.6.17.29.75 1.24 1.62 2.01 1.11.99 2.05 1.3 2.34 1.44.29.15.46.12.63-.07.17-.19.72-.84.91-1.13.19-.29.38-.24.64-.15.26.1 1.66.78 1.95.93.29.14.48.22.55.34.07.13.07.75-.17 1.43Z"/></svg>"""


def _other(lang: str) -> str:
    return "en" if lang == "pt" else "pt"


def header(lang: str, page: str, root: str) -> str:
    L = LANGUAGES[lang]
    nav_page = page
    if page.startswith("post:"):
        nav_page = "artigos"
    marks = []
    for key, label in NAV[lang]:
        cur = ' aria-current="page"' if key == nav_page else ""
        marks.append(f'      <a href="{root}{url(lang, key) or ""}"{cur}>{label}</a>')
    links = "\n".join(marks)
    # The documentation lives outside this repo, on the platform's own site.
    links += (f'\n      <a href="{DOCS}" target="_blank" rel="noopener">'
              f'{STRINGS[lang]["docs_nav"]} ↗</a>')
    form = PREACCESS_FORM.get(lang, "")
    if form:
        links += (f'\n      <a class="pre" href="{root}{url(lang, "studio") or ""}#pre-acesso">'
                  f'{STRINGS[lang]["pre_nav"]} ↗</a>')
    other_page = nav_page if not page.startswith("post:") else page
    return f"""<header class="site">
  <div class="bar">
    <a class="brand" href="{root}{url(lang, 'home') or ''}">
      {LOGO}
      <span>PINNeAPPle<span class="labs"> Labs</span></span>
    </a>

    <nav class="main" id="primary-nav" aria-label="{STRINGS[lang]['foot_platform']}">
{links}
    </nav>

    <div class="bar-cta">
      <a class="chip" href="{root}{url(_other(lang), other_page)}" hreflang="{LANGUAGES[_other(lang)]['code']}">{L['other_label']}</a>
      <a class="btn btn-primary btn-sm" href="https://wa.me/{WHATSAPP}?text={_q(STRINGS[lang]['wa_msg'])}" target="_blank" rel="noopener">{STRINGS[lang]['cta_primary']}</a>
    </div>

    <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 5h14M2 9h14M2 13h14"/></svg>
    </button>
  </div>
</header>
"""


def footer(lang: str, page: str, root: str) -> str:
    S = STRINGS[lang]
    o = _other(lang)
    return f"""
<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="{root}{url(lang, 'home') or ''}">
          {LOGO}
          <span>PINNeAPPle<span class="labs"> Labs</span></span>
        </a>
        <p>{S['foot_tag']}</p>
      </div>
      <div>
        <h4>{S['foot_platform']}</h4>
        <ul>
          <li><a href="{root}{url(lang, 'studio')}">{S['lbl_product']}</a></li>
          <li><a href="{root}{url(lang, 'erosao')}">{SEGLABELS[lang]['erosao']}</a></li>
          <li><a href="{root}{url(lang, 'trocadores')}">{SEGLABELS[lang]['trocadores']}</a></li>
          <li><a href="{root}{url(lang, 'valvulas')}">{SEGLABELS[lang]['valvulas']}</a></li>
          <li><a href="#consultoria">{S['lbl_success']}</a></li>
          <li><a href="{root}{url(lang, 'relatorios')}">{S['lbl_reports']}</a></li>
          <li><a href="{root}{url(lang, 'sucessos')}">{S['lbl_articles']}</a></li>
          <li><a href="{root}{url(lang, 'lib')}">{S['lbl_lib']}</a></li>
        </ul>
      </div>
      <div>
        <h4>{S['foot_code']}</h4>
        <ul>
          <li><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></li>
          <li><a href="{PYPI}" target="_blank" rel="noopener">PyPI</a></li>
          <li><a href="{DOCS}" target="_blank" rel="noopener">Docs</a></li>
          <li><a href="{CHANGELOG}" target="_blank" rel="noopener">Changelog</a></li>
        </ul>
      </div>
      <div>
        <h4>{S['foot_contact']}</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{S['wa']}</a></li>
          <li><a href="{root}{url(o, page)}" hreflang="{LANGUAGES[o]['code']}">{LANGUAGES[o]['label']}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base">
      <span>© <span id="yr">2026</span> PINNeAPPle Labs · {S['foot_rights']}</span>
      <span>{S['foot_law']}</span>
    </div>
  </div>
</footer>

<a class="fab" href="https://wa.me/{WHATSAPP}?text={_q(S['wa_msg'])}" target="_blank" rel="noopener" aria-label="{S['wa']}">
  {WA_ICON}<span>{S['wa']}</span>
</a>

<script src="{root}app.js" defer></script>
<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def _q(text: str) -> str:
    return urllib.parse.quote(text)


def wa_button(lang: str, cls: str = "btn btn-primary", label: str | None = None) -> str:
    """The primary call to action, in one place so the wording cannot drift."""
    S = STRINGS[lang]
    text = label or S["cta_primary"]
    return (f'<a class="{cls}" href="https://wa.me/{WHATSAPP}?text={_q(S["wa_msg"])}" '
            f'target="_blank" rel="noopener">{text}</a>')


def pre_band(lang: str, root: str) -> str:
    """The early-access call to action. Empty until that language has a form."""
    form = PREACCESS_FORM.get(lang, "")
    if not form:
        return ""
    S = STRINGS[lang]
    return f"""  <section class="pre-band" id="pre-acesso">
    <div class="wrap pre-inner">
      <div>
        <p class="eyebrow">{S['pre_eyebrow']}</p>
        <h2>{S['pre_title']}</h2>
        <p class="lead" style="max-width:52ch">{S['pre_lead']}</p>
      </div>
      <div class="pre-actions">
        <a class="btn btn-primary" href="{form}" target="_blank" rel="noopener">
          {S['pre_btn']} <span aria-hidden="true">↗</span>
        </a>
        <p class="pre-note">{S['pre_note']}</p>
      </div>
    </div>
  </section>
"""

def cta_band(lang: str, root: str) -> str:
    S = STRINGS[lang]
    return f"""  <section class="cta-band">
    <div class="wrap cta-inner">
      <div>
        <p class="eyebrow">{'Traga o seu caso' if lang == 'pt' else 'Bring your case'}</p>
        <h2>{S['cta_title']}</h2>
        <p class="lead" style="max-width:52ch">{S['cta_lead']}</p>
      </div>
      <div class="cta-actions">
        {wa_button(lang)}
        <a class="btn btn-ghost" href="{GITHUB}" target="_blank" rel="noopener">{S['cta_secondary']}</a>
      </div>
    </div>
  </section>
"""


def _anchor(name: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")


def fig(src: str, alt: str, cap: str, root: str, cls: str = "") -> str:
    return (f'<figure class="fig{cls}"><img src="{root}{src}" alt="{alt}" loading="lazy" decoding="async" />'
            f'<figcaption>{cap}</figcaption></figure>')


# ---------------------------------------------------------------------------
# The reel: clips the base generated, for the product page
# ---------------------------------------------------------------------------

REEL = {
    "pt": [
        ("videos/reel-carro.mp4", "videos/reel-carro.jpg",
         "CFD 3-D de um carro a 70 m/s, rodada a rodada", "aerodinamica-autonoma"),
        ("videos/reel-rover.mp4", "videos/reel-rover.jpg",
         "Rover lunar aprendendo o solo pelas próprias rodas", "rover-aprende-solo"),
        ("videos/reel-unity.mp4", "videos/reel-unity.jpg",
         "O mesmo campo girando dentro do Unity", "gemeo-no-unity"),
        ("videos/reel-blocos.mp4", "videos/reel-blocos.jpg",
         "Busca evolutiva de construções de bloco", "construcoes-de-bloco"),
        ("videos/reel-enso.mp4", "videos/reel-enso.jpg",
         "El Niño de 1997 simulado por ondas de Kelvin", "el-nino-28-modelos"),
    ],
    "en": [
        ("videos/reel-carro.mp4", "videos/reel-carro.jpg",
         "3D CFD of a car at 70 m/s, round by round", "aerodinamica-autonoma"),
        ("videos/reel-rover.mp4", "videos/reel-rover.jpg",
         "Lunar rover learning the soil from its own wheels", "rover-aprende-solo"),
        ("videos/reel-unity.mp4", "videos/reel-unity.jpg",
         "The same field turning inside Unity", "gemeo-no-unity"),
        ("videos/reel-blocos.mp4", "videos/reel-blocos.jpg",
         "Evolutionary search over brick builds", "construcoes-de-bloco"),
        ("videos/reel-enso.mp4", "videos/reel-enso.jpg",
         "The 1997 El Niño simulated with Kelvin waves", "el-nino-28-modelos"),
    ],
}


def reel(lang: str, root: str) -> str:
    """A strip of clips the examples produced, each linking to its article.

    They are small (70 KB to 430 KB), muted and only play while on screen, so the
    section costs less than a single screenshot and shows the product working.
    """
    cards = "".join(
        f'<figure class="reel-card"><video src="{root}{mp4}" poster="{root}{poster}" muted loop '
        f'playsinline preload="none" data-autoplay aria-label="{label}"></video>'
        f'<figcaption><a href="{root}{url(lang, "post:" + slug)}">{label}</a></figcaption></figure>\n'
        for mp4, poster, label, slug in REEL[lang]
    )
    return f'<div class="reel reveal">\n{cards}</div>'


def vfig(src: str, poster: str, cap: str, root: str) -> str:
    return (f'<figure class="fig vfig"><video src="{root}{src}" poster="{root}{poster}" muted loop playsinline '
            f'preload="none" data-autoplay aria-label="{cap}"></video>'
            f'<figcaption>{cap}</figcaption></figure>')


# ---------------------------------------------------------------------------
# Content shared by the home page and the product page
# ---------------------------------------------------------------------------

CAPS = {
    "pt": [
        ("Modelo substituto",
         "Responder em segundos, não em dias",
         "A simulação que você já rodou vira um modelo que responde na hora. Serve para responder “e se?” sem pagar o preço de uma simulação por pergunta.",
         "no dissipador: ~200 mil vezes mais rápido, com 4,46% de erro médio"),
        ("Gêmeo digital",
         "Acompanhar um equipamento de verdade",
         "O modelo passa a andar ao lado do dado real, com o erro declarado, e avisa antes de um limite ser cruzado.",
         "no HX-201: erro de 0,216 °C e alarme 2,6 h antes"),
        ("Otimização de projeto",
         "Testar milhares de versões antes de escolher uma",
         "Milhares de geometrias avaliadas contra objetivos que brigam entre si, com o mapa de trocas no lugar de uma resposta única.",
         "em 1.920 asas: −13% de CO₂ por passageiro-quilômetro"),
        ("Verificação",
         "Conferir um resultado antes de decidir",
         "O resultado é medido contra a física, o ensaio ou a norma, e não contra ele mesmo. O que não foi checado aparece como não checado.",
         "pegou resíduo 100× acima do limite num modelo já treinado"),
        ("CFD",
         "Rodar o caso completo, sem montar o caso",
         "Geometria, malha, solver, pós-processamento e a comparação com a referência, na mesma sessão.",
         "erosão em curva de 90°: 1,05–1,49× do ensaio publicado"),
        ("Dimensionamento rápido",
         "Ter o número agora, no meio da reunião",
         "Cálculo fechado para o caso do dia: dissipador, placa, elemento. Segundos em vez de horas, contra correlação publicada.",
         "dissipador: 0–5% contra a literatura"),
    ],
    "en": [
        ("Surrogate model",
         "Answer in seconds, not days",
         "A simulation you already ran becomes a model that answers on the spot. It exists to answer “what if?” without paying for one simulation per question.",
         "on the heat sink: ~200,000× faster, at 4.46% mean error"),
        ("Digital twin",
         "Follow real equipment as it runs",
         "The model walks beside live data, with the error stated, and warns before a limit is crossed.",
         "on HX-201: 0.216 °C error and an alarm 2.6 h ahead"),
        ("Design optimization",
         "Try thousands of versions before picking one",
         "Thousands of geometries evaluated against objectives that fight each other, with the trade-off map instead of a single answer.",
         "across 1,920 wings: −13% CO₂ per passenger-kilometre"),
        ("Verification",
         "Check a result before you decide",
         "The result is measured against the physics, the experiment or the standard, never against itself. What was not checked shows as not checked.",
         "caught a residual 100× over the limit on an already-trained model"),
        ("CFD",
         "Run the whole case, without building the case",
         "Geometry, mesh, solver, post-processing and the comparison against the reference, in one session.",
         "erosion in a 90° bend: 1.05–1.49× the published experiment"),
        ("Fast sizing",
         "Get the number now, mid-meeting",
         "A closed-form calculation for the case at hand: heat sink, board, part. Seconds instead of hours, against a published correlation.",
         "heat sink: 0–5% against the literature"),
    ],
}

HOME = {
    "pt": dict(
        eyebrow="Physics AI · Open Source · Engenharia e Ciência",
        h1="A próxima geração da engenharia será construída com Physics AI.",
        lead="Unimos física, simulação numérica e inteligência artificial para desenvolver tecnologias abertas, acelerar a pesquisa científica e criar soluções de engenharia para desafios reais da indústria.",
        cta_primary="Explorar a plataforma",
        cta_secondary="Discutir um projeto",
        chips=["Plataforma aberta", "Consultoria de engenharia", "Pesquisa aplicada"],
        hero_img="img/portfolio/13-aircraft-render-pressure.jpg",
        hero_alt="Visualização de pressão em uma asa: exemplo de otimização e modelagem física",
        hero_fig_b="Physics AI em ação",
        hero_fig_s="Modelagem, otimização e validação",
        problem_eyebrow="O problema",
        problem_h="A física explica o mundo. A inteligência artificial amplia o que podemos fazer com ela.",
        problem_p="Simulações permitem compreender fenômenos complexos, mas podem exigir muito tempo, computação e conhecimento especializado. Physics AI amplia essas capacidades, desde que seus resultados sejam verificáveis.",
        problems=[
            ("Custo computacional", "Surrogate models e operadores neurais podem acelerar análises, quando apropriados e validados."),
            ("Complexidade de desenvolvimento", "Pipelines integrados conectam dados, simulação, treinamento e implantação."),
            ("Confiabilidade física", "Verificação, validação, rastreabilidade e limites de aplicação explícitos."),
        ],
        entrega_eyebrow="Consultoria",
        entrega_h="Consultoria e projetos personalizados",
        entrega_p="Além da plataforma aberta, desenvolvemos soluções de Physics AI sob medida. Começamos pelo problema físico, definimos escopo e critérios de sucesso, e avaliamos a abordagem mais adequada.",
        entrega=[
            ("Diagnóstico e escopo", "Entendemos o desafio, os dados disponíveis, as restrições e as métricas de sucesso."),
            ("Desenvolvimento e integração", "Combinamos simulação, IA e ferramentas de engenharia em um pipeline reproduzível."),
            ("Validação e entrega", "Documentamos evidências, incertezas, limites de uso e resultados do projeto."),
        ],
        entrega_note_b="Escopo personalizado:",
        entrega_note="O escopo, o prazo e o investimento são definidos conforme cada projeto. Serviços de ensaio, laudos legais ou projeto mecânico completo não estão incluídos automaticamente.",
        seg_eyebrow="O que a gente resolve",
        seg_h="Três problemas que chegam aqui com nome e sobrenome",
        seg_p="Cada um já teve um estudo publicado, com o número medido contra uma referência externa. Se o seu caso é parecido, o caminho existe.",
        segs=[
            ("Erosão e desgaste em tubulação", "Onde a parede vai furar, a que taxa em mm/ano e em quanto tempo — na sua geometria, no seu material e no seu ponto de operação.", "erosao", "erosao-curva-90"),
            ("Trocadores de calor e térmico", "Se o trocador dá conta com a incrustação, quanto tempo até sair da faixa e onde o calor não dissipa, com a incerteza declarada.", "trocadores", "gemeo-hx201"),
            ("Válvulas e máquinas de fluxo", "A válvula, o bocal ou o orifício no seu ponto de operação: vazão, perda de carga e o regime que o catálogo do fornecedor não cobre.", "valvulas", "motor-prius-dois-solvers"),
        ],
        seg_link="Ver o estudo",
        seg_more="Ver o segmento",
        product_eyebrow="O produto",
        product_h="PINNeAPPle Studio",
        product_lead="A engenharia em texto: você escreve o que precisa, e a plataforma encontra uma ferramenta que já existe, confere se o seu caso está dentro do que aquela ferramenta já provou, roda e devolve o resultado com relatório e evidência.",
        product_points=[
            "<b>Entende o pedido escrito</b>, sem nome de método e sem montar o caso.",
            "<b>Diz na cara se cobre</b>: “dá”, “falta este dado”, “só em parte” ou “não cobre”.",
            "<b>Só roda o que tem prova</b>: cada ferramenta é descoberta, testada ou verificada.",
            "<b>Devolve o relatório junto</b>: o que rodou, o que não rodou e a origem de cada número.",
        ],
        product_cap="O relatório de uma execução: gráfico, verificações com valor e limite, e o status da evidência, aqui “inconclusiva”, porque uma checagem não rodou.",
        product_cta="Ver o produto completo",
        product_soon="Chega em 2027. Quem entrar na lista testa antes.",
        caps_eyebrow="O que dá para fazer",
        caps_h="Seis coisas que a plataforma vai fazer, e que a base já faz hoje.",
        caps_p="Cada cartão traz um caso que já rodou, com o número medido. Os exemplos vêm da biblioteca aberta, não de uma promessa de roadmap.",
        how_eyebrow="Como funciona",
        how_h="Três passos, nenhum deles técnico",
        how_p="O que hoje exige alguém que saiba montar o caso vira uma frase escrita, uma conferência automática e um relatório que se pode mostrar.",
        how=[
            ("Você escreve o problema", "Em português comum: o que precisa, de que material, com que tamanho e qual limite. Sem nome de método e sem arquivo de configuração."),
            ("A plataforma diz se cobre", "Procura a ferramenta que resolve, compara os seus números com a faixa em que ela foi validada e aponta o que falta antes de rodar."),
            ("Você recebe resultado e relatório", "Com o valor, as verificações que rodaram, as que não rodaram, a versão do código e o que continua não provado."),
        ],
        stats=[
            ("~200.000×", "mais rápido que a simulação 3D real, num substituto térmico", "4,46% de erro vs. FEniCS"),
            ("1,05–1,49×", "erosão simulada vs. ensaio aberto, dentro do fator 2", "Vieira et al. 2016"),
            ("0,216 °C", "de erro no gêmeo de um permutador em operação", "95,5% de cobertura"),
            ("2,6 h", "de antecedência no alarme, com o erro declarado", "HX-201, incrustação"),
        ],
        proofs_eyebrow="Do que já rodou",
        proofs_h="O que já rodou, com o número na frente",
        proofs_p="Seis experimentos abertos, cada um com artigo inteiro: o que foi medido, contra o que foi comparado e o que ainda não está provado.",
        proofs=[
            ("img/portfolio/13-aircraft-render-pressure.jpg", "Pressão na pele de uma asa otimizada",
             "Otimização", "1.920 asas, três objetivos", "asa-1920-projetos"),
            ("img/erosao-card.webp", "Mapa de erosão na parede de uma curva de 90°, com a taxa em mm/ano",
             "CFD", "A erosão que bateu com o ensaio", "erosao-curva-90"),
            ("img/twin.jpg", "Gêmeo digital de um ativo em 3D, com a leitura viva ao lado",
             "Gêmeo digital", "Um ativo em 3D, com leitura viva", "gemeo-hx201"),
            ("img/exp/unity-thumb.webp", "Carretel com o campo de temperatura, vindo do solver para o Unity",
             "Gêmeo digital", "Do solver ao motor de jogo, em 23 ms", "gemeo-no-unity"),
            ("img/exp/motor-campo.webp", "Campo magnético no quarto de máquina do motor do Prius",
             "Eletromagnetismo", "Dois solvers concordam em 0,19%", "motor-prius-dois-solvers"),
            ("img/verificacao.jpg", "Run do VeriPhysics com a nota por checagem",
             "Verificação", "A checagem que não rodou não conta", "guardrail-veriphysics"),
        ],
        news_eyebrow="Artigos",
        news_h="O que a gente mediu, contado por inteiro",
        news_p="Um experimento por artigo, com imagens, vídeo e os números que saíram da execução. Inclusive os que limitam o resultado.",
        show_eyebrow="A apresentação",
        show_h="A plataforma inteira em uma gravação",
        show_p="A apresentação que fizemos no evento da SIMR: o pedido escrito, a busca, a execução e o relatório, sem corte no meio. É o jeito mais rápido de ver o que o PINNeAPPle Studio faz.",
        show_cap="A apresentação do PINNeAPPle Studio no evento da SIMR",
        show_play="Assistir à apresentação",
        story_eyebrow="Quem faz",
        story_h="Uma regra só: se não tem número medido, não vai para a tela.",
        story_p=[
            "A PINNeAPPle começou como uma biblioteca pessoal para não ter de confiar: cada resultado carrega a referência contra a qual foi conferido. Virou produto quando ficou claro que o problema não é o modelo, é a falta de prova.",
            "Dizer “não” faz parte. Num caso de mobilidade de rover, o método numérico clássico era mais rápido e mais exato que a rede; a recomendação foi o método clássico.",
        ],
        person_name="Yan Barros",
        person_role="criador do PINNeAPPle",
        person_bio="Físico de formação, une física, IA e engenharia para levar modelos científicos a aplicações reais. Criou o PINNeAPPle e atua com IA aplicada a problemas de engenharia e indústria no Brasil.",
        story_cta="Conhecer a base aberta",
    ),
    "en": dict(
        eyebrow="Physics AI · Open Source · Engineering and Science",
        h1="The next generation of engineering will be built with Physics AI.",
        lead="We combine physics, numerical simulation, and artificial intelligence to build open technologies, accelerate scientific research, and deliver engineering solutions for real industrial challenges.",
        cta_primary="Explore the platform",
        cta_secondary="Discuss a project",
        chips=["Open platform", "Engineering consulting", "Applied research"],
        hero_img="img/portfolio/13-aircraft-render-pressure.jpg",
        hero_alt="Pressure visualization on an aircraft wing: an example of physics-based optimization",
        hero_fig_b="Physics AI in action",
        hero_fig_s="Modeling, optimization and validation",
        problem_eyebrow="The problem",
        problem_h="Physics explains the world. Artificial intelligence expands what we can do with it.",
        problem_p="Simulation helps us understand complex phenomena, but can demand significant time, computing resources, and specialist expertise. Physics AI extends those capabilities when its results can be verified.",
        problems=[
            ("Computational cost", "Surrogate models and neural operators can accelerate analysis when appropriate and validated."),
            ("Development complexity", "Integrated pipelines connect data, simulation, training, and deployment."),
            ("Physics reliability", "Verification, validation, traceability, and explicit validity limits."),
        ],
        entrega_eyebrow="Consulting",
        entrega_h="Consulting and custom engineering projects",
        entrega_p="Beyond the open platform, we develop tailored Physics AI solutions. We start with the physical problem, define scope and success criteria, and evaluate the most suitable approach.",
        entrega=[
            ("Discovery and scope", "We clarify the challenge, available data, constraints, and success metrics."),
            ("Development and integration", "We combine simulation, AI, and engineering tools in a reproducible pipeline."),
            ("Validation and delivery", "We document evidence, uncertainty, limits of use, and project results."),
        ],
        entrega_note_b="Custom scope:",
        entrega_note="Scope, timeline, and budget are defined for each project. Experimental testing, legal certification, and full mechanical design are not automatically included.",
        seg_eyebrow="What we solve",
        seg_h="Three problems that arrive here with a name and a surname",
        seg_p="Each one already has a published study, with the number measured against an external reference. If your case looks like one of them, the path exists.",
        segs=[
            ("Erosion and wear in piping", "Where the wall will fail, at what rate in mm/year and in how long — on your geometry, your material and your operating point.", "erosao", "erosao-curva-90"),
            ("Heat exchangers and thermal", "Whether the exchanger still copes with the fouling, how long until it leaves the band and where the heat does not dissipate, with the uncertainty stated.", "trocadores", "gemeo-hx201"),
            ("Valves and flow machinery", "The valve, nozzle or orifice at your operating point: flow rate, pressure drop and the regime the vendor catalogue does not cover.", "valvulas", "motor-prius-dois-solvers"),
        ],
        seg_link="Read the study",
        seg_more="See the segment",
        product_eyebrow="The product",
        product_h="PINNeAPPle Studio",
        product_lead="Studio in plain text: you write what you need, and the platform finds a tool that already exists, checks whether your case sits inside what that tool has already proven, runs it, and returns the result with a report and evidence.",
        product_points=[
            "<b>It understands the written request</b>, no method name, no case to build.",
            "<b>It says plainly whether it covers you</b>: “yes”, “this value is missing”, “partly” or “no”.",
            "<b>It only runs what has proof</b>: every tool is discovered, tested or verified.",
            "<b>It hands back the report</b>: what ran, what did not, and where each number came from.",
        ],
        product_cap="A run's report: the chart, the checks with value and limit, and the evidence status, here “inconclusive”, because one check did not run.",
        product_cta="See the full product",
        product_soon="Arrives in 2027. Those on the list test it first.",
        caps_eyebrow="What you can do",
        caps_h="Six things the platform will do, and the base already does today.",
        caps_p="Every card carries a case that has already run, with its measured number. The examples come from the open library, not from a roadmap promise.",
        how_eyebrow="How it works",
        how_h="Three steps, none of them technical",
        how_p="What today needs someone who knows how to build the case becomes a written sentence, an automatic check and a report you can show.",
        how=[
            ("You write the problem", "In plain words: what you need, from which material, at what size, under which limit. No method name and no configuration file."),
            ("It says whether it covers you", "It looks for the tool that solves it, compares your numbers with the range that tool was validated in, and names what is missing before the run."),
            ("You get the result and the report", "With the value, the checks that ran, the ones that did not, the code version and what is still unproven."),
        ],
        stats=[
            ("~200,000×", "faster than the real 3D simulation, on a thermal surrogate", "4.46% error vs. FEniCS"),
            ("1.05–1.49×", "simulated erosion vs. an open experiment, inside factor 2", "Vieira et al. 2016"),
            ("0.216 °C", "of error on the twin of an exchanger in operation", "95.5% coverage"),
            ("2.6 h", "of alarm lead, with the error stated", "HX-201, fouling"),
        ],
        proofs_eyebrow="From what already ran",
        proofs_h="What already ran, with the number up front",
        proofs_p="Six open experiments, each with a full article: what was measured, what it was compared against, and what is not proven yet.",
        proofs=[
            ("img/portfolio/13-aircraft-render-pressure.jpg", "Skin pressure on an optimized wing",
             "Optimization", "1,920 wings, three objectives", "asa-1920-projetos"),
            ("img/erosao-card.webp", "Wall erosion map on a 90° bend, rate in mm/year",
             "CFD", "Erosion that met the published experiment", "erosao-curva-90"),
            ("img/twin.jpg", "Digital twin of an asset in 3D, with the live reading beside it",
             "Digital twin", "An asset in 3D, with a live reading", "gemeo-hx201"),
            ("img/exp/unity-thumb.webp", "Spool with the temperature field, from the solver to Unity",
             "Digital twin", "From the solver to the game engine, in 23 ms", "gemeo-no-unity"),
            ("img/exp/motor-campo.webp", "Magnetic field in the quarter machine of the Prius motor",
             "Electromagnetics", "Two solvers agree to 0.19%", "motor-prius-dois-solvers"),
            ("img/verificacao.jpg", "A VeriPhysics run with the score per check",
             "Verification", "A check that did not run does not count", "guardrail-veriphysics"),
        ],
        news_eyebrow="Articles",
        news_h="What we measured, told in full",
        news_p="One experiment per article, with images, video and the numbers that came out of the run. Including the ones that limit the result.",
        show_eyebrow="The talk",
        show_h="The whole platform in one recording",
        show_p="The talk we gave at the SIMR event: the written request, the search, the run and the report, without cuts in between. It is the fastest way to see what PINNeAPPle Studio does.",
        show_cap="The PINNeAPPle Studio talk at the SIMR event",
        show_play="Watch the talk",
        story_eyebrow="Who makes it",
        story_h="One rule: if it has no measured number, it does not go on screen.",
        story_p=[
            "PINNeAPPle started as a personal library so its author would not have to take anything on trust: every result carries the reference it was checked against. It became a product when it was clear the problem is not the model, it is the lack of proof.",
            "Saying “no” is part of it. In one rover-mobility case the classical numerical method was faster and more accurate than the network; the recommendation was the classical method.",
        ],
        person_name="Yan Barros",
        person_role="creator of PINNeAPPle",
        person_bio="A physicist by training, he combines physics, AI and engineering to take scientific models into real applications. He created PINNeAPPle and works on AI applied to real engineering and industrial problems in Brazil.",
        story_cta="Meet the open base",
    ),
}

PRODUCT = {
    "pt": dict(
        eyebrow="O produto · lançamento em 2027",
        h1="PINNeAPPle Studio",
        lead="Do problema de engenharia ao relatório que você pode defender numa reunião. Você escreve o que precisa; a plataforma diz se cobre, roda o que já tem prova e devolve o resultado com a conta aberta.",
        chips=["Studio no navegador", "Lançamento em 2027", "Roda sobre a base aberta"],
        cta_primary="Quero testar quando abrir",
        cta_secondary="Ver os artigos",
        hero_cap="A tela inicial do Studio: uma caixa de busca, o catálogo do que já existe e quantas dessas ferramentas foram verificadas.",
        what_eyebrow="O que é",
        what_h="Uma plataforma que responde engenharia, não que desenha gráfico",
        what_p=[
            "A maioria das ferramentas de simulação entrega um campo colorido e deixa a interpretação com você. O Studio faz o caminho contrário: começa no pedido, escrito em português comum, e termina num relatório que diz o que foi feito, o que foi conferido e o que ainda não foi provado.",
            "Por baixo está a biblioteca aberta da PINNeAPPle: cada ferramenta é uma função real, com assinatura, unidade, faixa de validade e o histórico de testes. A plataforma não inventa capacidade: ela encontra o que existe, confere se o seu caso cabe ali e executa em ambiente isolado.",
        ],
        counts=[
            ("10.055", "ferramentas catalogadas pelo próprio Studio"),
            ("4.987", "executáveis de ponta a ponta"),
            ("1.693", "verificadas contra uma referência"),
            ("71 de 97", "exemplos e reproduções que rodam no Studio"),
        ],
        counts_note="Contagens lidas do Studio na versão atual, as mesmas que a tela de cobertura mostra, a partir do código e das execuções gravadas.",
        flow_eyebrow="Do pedido ao relatório",
        flow_h="O caminho que o pedido percorre",
        flow_p="Quatro etapas entre a frase escrita e o relatório assinado. Nenhuma delas exige que você monte um caso de simulação.",
        flow=[
            ("01", "Você descreve o problema", "Uma frase basta: “dissipador de calor com aletas para 60 W”. A plataforma estrutura o pedido e mostra o que já existe para aquilo."),
            ("02", "Ela diz se cobre", "Quatro respostas possíveis: cobre e roda; falta um dado (e ela pergunta só esse); cobre em parte (e diz o que teria de mudar); ou não cobre (e diz por quê)."),
            ("03", "Confere antes de rodar", "Os seus números são comparados com a faixa em que aquela ferramenta já foi validada. Fora da faixa, o resultado não é apresentado como se valesse."),
            ("04", "Entrega resultado, evidência e relatório", "Com as verificações que rodaram, as que não rodaram, a versão do código, o tempo e a memória gastos e o hash de cada arquivo."),
        ],
        flow_reel_note="Cinco pipelines que a base já gerou, cada um com o artigo inteiro: o carro em CFD 3-D, o rover que aprende o solo, o gêmeo dentro do Unity, a busca evolutiva de construções de bloco e o El Niño de 1997.",
        caps_eyebrow="O que você vai poder fazer",
        caps_h="Seis trabalhos que hoje custam uma semana",
        caps_p="Cada um com um exemplo que já rodou na base aberta. É o que o produto vai colocar na frente de quem não é especialista em método numérico.",
        trust_eyebrow="Por que dá para confiar",
        trust_h="O que a plataforma faz para não te enganar",
        trust=[
            "<b>Ela confere a validade antes de rodar</b>: se o seu caso está fora da faixa em que a ferramenta foi validada, o resultado não sai como se valesse.",
            "<b>Ela não inventa capacidade</b>, porque o catálogo é gerado por introspecção do código real, com o estado de cada ferramenta: descoberta, testada ou verificada.",
            "<b>O que não rodou aparece como não rodou</b>: uma checagem que não executou nunca conta como aprovada e derruba a cobertura do resultado.",
            "<b>A evidência fica arquivada</b>: versão, hardware, tempo, memória, logs e hash de cada arquivo, para reproduzir a execução.",
            "<b>Existe um portão humano</b>: formulação e aprovação de modelo são decisões de engenharia, não da plataforma.",
        ],
        io_eyebrow="Entra e sai",
        io_h="O que você entrega e o que você recebe",
        io_p="A mesma lista serve para os dois lados: se o que você tem não cobre o que entra, a plataforma diz isso antes de rodar.",
        inputs=[
            "O problema escrito, em português comum",
            "Geometria em STL, STEP ou CAD, quando o caso pede",
            "Dados de ensaio, série de sensores ou histórico de operação",
            "Condições de contorno, material e limites de operação",
            "Um arquivo de simulação existente (OpenFOAM, CalculiX, Abaqus)",
        ],
        outputs=[
            "O número que responde à pergunta, com unidade",
            "O campo, o gráfico ou a série, prontos para levar adiante",
            "As verificações, uma por uma, com valor e limite",
            "O relatório em Markdown, com a origem de cada parâmetro",
            "A evidência arquivada: versão, hardware, tempo e hash dos arquivos",
            "O que não foi checado e o que ainda não está provado",
        ],
        shots_eyebrow="O produto por dentro",
        shots_h="Telas reais do Studio, hoje",
        shots_p="Nada de mockup: são capturas da aplicação em desenvolvimento, com os dados de uma execução real.",
        shots=[
            ("img/eng/studio-report.webp", "Uma execução do Studio com o resultado e as verificações", "A execução: o job concluído, a evidência declarada, o valor que sai e as verificações com valor e limite, uma por uma."),
            ("img/eng/studio-coverage.webp", "Tela de cobertura do Studio", "A tela de cobertura: o que roda pelo Studio, contado a partir do código e das execuções gravadas, nunca estimado."),
        ],
        film_eyebrow="Veja rodando",
        film_h="Do pedido ao relatório, em 28 segundos",
        film_p="Este vídeo é uma gravação da aplicação, com legenda: a busca em português, a escolha da ferramenta, a execução e a volta com as verificações. Nada foi encenado. A espera do solver foi cortada. O corte preto no meio do vídeo marca onde.",
        film=("videos/studio-pt.mp4", "videos/studio-pt.jpg", "Busca, ferramenta, execução, verificações e relatório: a aplicação respondendo um job de verdade. A espera do solver foi cortada."),
        videos_eyebrow="Mais dois apps da base",
        videos_h="O que já existe para além do Studio",
        videos_p="O Studio executa as ferramentas da biblioteca. Estes dois vídeos são apps da base rodando: dimensionamento térmico e preflight de simulação.",
        videos=[
            ("videos/app1.mp4", "videos/app1.jpg", "Dimensionamento térmico: a resposta sai enquanto você digita"),
            ("videos/app8.mp4", "videos/app8.jpg", "Preflight de simulação: PASS, WARNING ou FAIL antes de rodar"),
        ],
        state_eyebrow="Estado atual, sem marketing",
        state_h="O que já roda e o que chega no lançamento",
        state_p="A plataforma é construída em módulos. É mais honesto dizer o que está pronto do que fingir que tudo chegou junto.",
        state_rows=[
            ("Studio e catálogo", "Busca, filtros, execução de ferramentas da base, relatório e evidência", "roda hoje"),
            ("Engenheiro (intake)", "Pedido em texto, perguntas de esclarecimento e plano aprovável", "roda hoje"),
            ("CFD / Solvers", "Caso completo com solver externo e comparação com referência", "em 2027"),
            ("VeriPhysics", "Checagens de física, convergência e cobertura sobre modelos e resultados", "em 2027"),
            ("Surrogate Factory", "Treino de substituto com domínio de validade declarado", "em 2027"),
            ("PINNeAPPle Twin", "Replay de ativo com alarme e erro declarado, depois telemetria ao vivo", "em 2027"),
        ],
        limits_note="O que o produto não faz: não substitui ensaio, não garante resultado fora da faixa validada e não decide por você. Quando o método clássico resolve melhor, a recomendação é o método clássico.",
        soon_note="Lançamento previsto para 2027, sem data fechada. Quem entra na lista testa antes e ajuda a decidir o que entra primeiro.",
    ),
    "en": dict(
        eyebrow="The product · launching in 2027",
        h1="PINNeAPPle Studio",
        lead="From the engineering problem to a report you can defend in a meeting. You write what you need; the platform says whether it covers it, runs what already has proof, and returns the result with the working shown.",
        chips=["Studio in the browser", "Launching in 2027", "Runs on the open base"],
        cta_primary="I want to test it when it opens",
        cta_secondary="Read the articles",
        hero_cap="The Studio home: a search box, the catalogue of what already exists, and how many of those tools are verified.",
        what_eyebrow="What it is",
        what_h="A platform that answers engineering, not one that draws plots",
        what_p=[
            "Most simulation tools hand back a colourful field and leave the interpretation to you. Studio goes the other way: it starts from the request, written in plain language, and ends in a report that says what was done, what was checked, and what has not been proven yet.",
            "Underneath sits PINNeAPPle's open library: every tool is a real function, with a signature, units, a validity range and a test history. The platform does not invent capability: it finds what exists, checks whether your case fits, and runs it in an isolated environment.",
        ],
        counts=[
            ("10,055", "tools catalogued by the Studio itself"),
            ("4,987", "runnable end to end"),
            ("1,693", "verified against a reference"),
            ("71 of 97", "examples and reproductions that run in the Studio"),
        ],
        counts_note="Counts read from the Studio in its current version, the same ones the coverage screen shows, taken from the code and the recorded runs.",
        flow_eyebrow="From request to report",
        flow_h="The path a request takes",
        flow_p="Four stages between the written sentence and the signed report. None of them asks you to build a simulation case.",
        flow=[
            ("01", "You describe the problem", "One sentence is enough: “finned heat sink for 60 W”. The platform structures the request and shows what already exists for it."),
            ("02", "It says whether it covers you", "Four possible answers: it covers and runs; a value is missing (and it asks only for that); it covers in part (and says what would have to change); or it does not cover (and says why)."),
            ("03", "It checks before running", "Your numbers are compared with the range in which that tool was validated. Outside the range, the result is not presented as if it held."),
            ("04", "It returns result, evidence and report", "With the checks that ran, the ones that did not, the code version, the time and memory spent, and the hash of every file."),
        ],
        flow_reel_note="Five pipelines the base has already produced, each with a full article: the car in 3D CFD, the rover learning the soil, the twin inside Unity, the evolutionary search over brick builds and the 1997 El Niño.",
        caps_eyebrow="What you will be able to do",
        caps_h="Six jobs that today cost a week",
        caps_p="Each with an example that has already run on the open base. This is what the product puts in front of someone who is not a numerical-method specialist.",
        trust_eyebrow="Why it can be trusted",
        trust_h="What the platform does so it does not fool you",
        trust=[
            "<b>It checks validity before running</b>: if your case falls outside the range the tool was validated in, the result does not come out as if it held.",
            "<b>It does not invent capability</b>, because the catalogue is generated by introspecting the real code, with each tool's state: discovered, tested or verified.",
            "<b>What did not run shows as did not run</b>: a check that never executed never counts as passed, and it pulls the result's coverage down.",
            "<b>The evidence is filed</b>: version, hardware, time, memory, logs and the hash of every file, so the run can be reproduced.",
            "<b>There is a human gate</b>: formulation and model approval are engineering decisions, not the platform's.",
        ],
        io_eyebrow="In and out",
        io_h="What you hand over and what you get back",
        io_p="The same list serves both sides: if what you have does not cover what goes in, the platform says so before running.",
        inputs=[
            "The problem, written in plain language",
            "Geometry in STL, STEP or CAD when the case calls for it",
            "Test data, a sensor series or an operating history",
            "Boundary conditions, material and operating limits",
            "An existing simulation file (OpenFOAM, CalculiX, Abaqus)",
        ],
        outputs=[
            "The number that answers the question, with units",
            "The field, chart or series, ready to take forward",
            "The checks, one by one, with value and limit",
            "The report in Markdown, with the origin of every parameter",
            "The filed evidence: version, hardware, time and file hashes",
            "What was not checked and what is not proven yet",
        ],
        shots_eyebrow="The product inside",
        shots_h="Real screens from the Studio, today",
        shots_p="No mockups: these are captures of the application under development, with data from a real run.",
        shots=[
            ("img/eng/studio-report.webp", "A Studio run with its result and checks", "The run: job finished, evidence stated, the value that comes out and the checks with value and limit, one by one."),
            ("img/eng/studio-coverage.webp", "The Studio coverage screen", "The coverage screen: what runs through the Studio, counted from the code and the recorded runs, never estimated."),
        ],
        film_eyebrow="See it running",
        film_h="From request to report, in 27 seconds",
        film_p="This is a recording of the application, with captions: the search, the choice of tool, the run, and the answer coming back with the checks. Nothing staged. The solver wait was cut out. The black cut in the middle marks where.",
        film=("videos/studio-en.mp4", "videos/studio-en.jpg", "Search, tool, run, checks and report: the application answering a real job. The solver wait has been cut out."),
        videos_eyebrow="Two more apps from the base",
        videos_h="What already exists beyond the Studio",
        videos_p="The Studio executes the library's tools. These two clips are base apps running: thermal sizing and simulation preflight.",
        videos=[
            ("videos/app1.mp4", "videos/app1.jpg", "Thermal sizing: the answer appears as you type"),
            ("videos/app8.mp4", "videos/app8.jpg", "Simulation preflight: PASS, WARNING or FAIL before the run"),
        ],
        state_eyebrow="Current state, no marketing",
        state_h="What runs today and what lands at launch",
        state_p="The platform is built in modules. Saying what is ready is more honest than pretending it all arrived together.",
        state_rows=[
            ("Studio and catalogue", "Search, filters, execution of base tools, report and evidence", "runs today"),
            ("Engineer (intake)", "Request in text, clarifying questions and an approvable plan", "runs today"),
            ("CFD / Solvers", "Full case with an external solver and comparison against a reference", "in 2027"),
            ("VeriPhysics", "Physics, convergence and coverage checks over models and results", "in 2027"),
            ("Surrogate Factory", "Surrogate training with a stated validity domain", "in 2027"),
            ("PINNeAPPle Twin", "Asset replay with alarms and stated error, then live telemetry", "in 2027"),
        ],
        limits_note="What the product does not do: it does not replace a test, it does not guarantee a result outside the validated range, and it does not decide for you. When the classical method does better, the recommendation is the classical method.",
        soon_note="Launching in 2027, no fixed date yet. People on the list test it first and help decide what ships first.",
    ),
}

ARTICLES = {
    "pt": dict(
        eyebrow="Artigos",
        h1="Os casos, contados por inteiro.",
        lead="Cada artigo é um experimento: o que foi medido, contra o que foi comparado e onde ainda não chegamos. É a mesma regra da casa, aplicada ao texto.",
    ),
    "en": dict(
        eyebrow="Articles",
        h1="The cases, told in full.",
        lead="Every article is one experiment: what was measured, what it was compared against, and where we are not there yet. The same house rule, applied to writing.",
    ),
}

# ---------------------------------------------------------------------------
# Segment pages: one per problem the studio solves, not one per industry.
#
# A buyer searches by object and phenomenon — "erosão em tubulação", "simulador
# de trocador de calor", "vazão em válvula" — never by industry. Every claim on
# these pages points at a study that is already public on this site.
# ---------------------------------------------------------------------------

SEGUI = {
    "pt": {
        "pain_eyebrow": "Onde dói",
        "pain_h": "O problema como ele chega aqui",
        "io_eyebrow": "Entra e sai",
        "io_h": "O que a gente precisa e o que você recebe",
        "io_in": "Entra",
        "io_out": "Sai",
        "proof_eyebrow": "A prova",
        "proof_h": "O número, com a referência na frente",
        "more": "Outras provas",
        "study": "Ler o estudo completo",
        "others_eyebrow": "Outros segmentos",
        "others_h": "O mesmo rigor, outro fenômeno",
        "io_note": "Sem estes dados o estudo não começa; com eles, o número sai com a faixa de validade declarada.",
        "pdf": REPORT_LABEL["pt"],
    },
    "en": {
        "pain_eyebrow": "Where it hurts",
        "pain_h": "The problem as it arrives here",
        "io_eyebrow": "In and out",
        "io_h": "What we need and what you get",
        "io_in": "In",
        "io_out": "Out",
        "proof_eyebrow": "The proof",
        "proof_h": "The number, with the reference up front",
        "more": "More proof",
        "study": "Read the full study",
        "others_eyebrow": "Other segments",
        "others_h": "The same rigour, another phenomenon",
        "io_note": "Without these the study does not start; with them, the number comes with its validity range stated.",
        "pdf": REPORT_LABEL["en"],
    },
}

SEGMENTS = {
    "erosao": {
        "slug": "erosao-em-tubulacao",
        "pt": dict(
            meta_title="Erosão em tubulação: onde vai furar e em quanto tempo · PINNeAPPle Labs",
            meta_desc=("Estudo de erosão em tubos e curvas, verificado contra ensaio publicado: taxa em mm/ano, "
                       "posição do pico e vida útil. Prazo de 4 a 10 semanas, orçamento a partir do escopo."),
            eyebrow="Erosão e desgaste · tubulação",
            h1="Onde a sua tubulação vai furar — e em quanto tempo.",
            lead=("Estudo de erosão em tubos, curvas, reduções e manifolds: taxa na parede em mm/ano, posição do pico "
                  "e vida útil até a espessura mínima, conferidos contra ensaio publicado."),
            chips=["Curva, redução, T e manifold", "Verificado contra ensaio", "Entrega em 4 a 10 semanas"],
            pains=[
                ("A parada não programada", "Erosão não aparece na inspeção de rotina até furar. Quando aparece, a linha já está fora e a parada não é mais planejada."),
                ("O material comprado “por segurança”", "Aumentar espessura ou trocar por liga resolve — e custa. Sem a taxa, o dimensionamento vira uma aposta para o lado caro."),
                ("A fórmula de bolso que erra por 100×", "A fórmula fechada da norma, sem CFD, ficou 97 a 100 vezes abaixo do ensaio em dois dos três casos que verificamos."),
            ],
            pains_p="Três dores que trazem um estudo de erosão até aqui — e que o número resolve ou delimita.",
            hero_fig="img/erosao-card.webp",
            inputs=[
                "Geometria: CAD, STEP ou desenho com diâmetro, raio de curva e trechos",
                "Fluido: vazão, pressão e temperatura de operação",
                "Partículas: tamanho, densidade, forma e concentração (ou taxa de areia medida)",
                "Material e dureza da parede; espessura inicial e mínima admissível",
                "Histórico: horas de operação por ano e paradas",
            ],
            outputs=[
                "Mapa de erosão na parede, em mm/ano, na sua geometria",
                "Posição e valor do pico — onde medir espessura primeiro",
                "Vida útil até a espessura mínima, com a faixa de incerteza",
                "Sensibilidade a vazão, raio de curva e material",
                "Relatório com a verificação contra ensaio e a seção de limites",
            ],
            stats=[
                ("1,05–1,49×", "do ensaio de Vieira et al. (2016)", "dentro do fator 2 nos três pontos"),
                ("50,6°", "de pico calculado, contra 45° medido", "posição do ponto crítico"),
                ("~100×", "é o erro da fórmula fechada sem CFD", "em 2 dos 3 ensaios"),
                ("22,6 min", "para 32 casos, do CAD ao modelo treinado", "1,94 h de CPU"),
            ],
            fig="img/erosao.jpg",
            fig_alt="Mapa de erosão na parede de uma curva de 90°, com a taxa em mm por ano",
            fig_b="Estudo aberto, curva de 90°",
            fig_s="pico na parede externa",
            fig_cap=("Mapa de erosão do estudo aberto: tubulação inteira e zoom na curva, com o pico na parede externa "
                     "logo após a entrada da curva. Escala em mm/ano."),
            post="erosao-curva-90",
            report="estudo-erosao-curva-90",
            extras=[
                ("Estudo de malha: onde o número converge", "Três níveis e três pontos: o ΔP converge com GCI de 6,8–12,6% na malha fina; a erosão só converge no ponto de referência (2,9%). Onde não converge, está declarado.", "post", "erosao-curva-90"),
                ("A checagem que não rodou não conta", "No mapa de provas do mesmo estudo: 11 verificações a favor, 0 contra e 6 que não rodaram — 65% de cobertura, declarada no relatório.", "post", "guardrail-veriphysics"),
            ],
        ),
        "en": dict(
            meta_title="Erosion in piping: where it will fail and how soon · PINNeAPPle Labs",
            meta_desc=("Erosion study for pipes and bends, checked against a published experiment: rate in mm/year, "
                       "peak position and service life. 4 to 10 weeks, quoted from the scope."),
            eyebrow="Erosion and wear · piping",
            h1="Where your piping will fail — and how soon.",
            lead=("An erosion study for pipes, bends, reducers and manifolds: wall rate in mm/year, peak position and "
                  "service life down to the minimum thickness, checked against a published experiment."),
            chips=["Bend, reducer, tee and manifold", "Checked against an experiment", "Delivered in 4 to 10 weeks"],
            pains=[
                ("The unplanned shutdown", "Erosion does not show up in routine inspection until it breaks through. By then the line is out and the shutdown is no longer planned."),
                ("The material bought “to be safe”", "A thicker wall or a different alloy works — and costs. Without the rate, sizing becomes a bet on the expensive side."),
                ("The rule of thumb that is off by 100×", "The standard's closed-form formula, without CFD, came out 97 to 100 times below the experiment in two of the three cases we checked."),
            ],
            pains_p="Three pains that bring an erosion study here — and that the number either settles or bounds.",
            hero_fig="img/erosao-card.webp",
            inputs=[
                "Geometry: CAD, STEP or a drawing with diameter, bend radius and runs",
                "Fluid: flow rate, pressure and operating temperature",
                "Particles: size, density, shape and concentration (or measured sand rate)",
                "Wall material and hardness; initial and minimum allowable thickness",
                "History: operating hours per year and shutdowns",
            ],
            outputs=[
                "Wall erosion map, in mm/year, on your geometry",
                "Peak position and value — where to measure thickness first",
                "Service life down to the minimum thickness, with its uncertainty band",
                "Sensitivity to flow rate, bend radius and material",
                "Report with the experiment check and the limits section",
            ],
            stats=[
                ("1.05–1.49×", "of the Vieira et al. (2016) experiment", "inside the factor-2 band at all three points"),
                ("50.6°", "computed peak, against 45° measured", "position of the critical point"),
                ("~100×", "is the error of the closed form without CFD", "in 2 of the 3 experiments"),
                ("22.6 min", "for 32 cases, from CAD to trained model", "1.94 CPU-hours"),
            ],
            fig="img/erosao.jpg",
            fig_alt="Wall erosion map on a 90° bend, rate in mm/year",
            fig_b="Open study, 90° bend",
            fig_s="peak on the outer wall",
            fig_cap=("Erosion map from the open study: the whole pipe and the zoom into the bend, with the peak on the "
                     "outer wall just after the bend entry. Scale in mm/year."),
            post="erosao-curva-90",
            report="estudo-erosao-curva-90",
            extras=[
                ("Mesh study: where the number converges", "Three levels, three points: ΔP converges at 6.8–12.6% GCI on the fine mesh; erosion converges only at the reference point (2.9%). Where it does not, the report says so.", "post", "erosao-curva-90"),
                ("A check that did not run does not count", "In the same study's proof map: 11 checks for, 0 against and 6 that did not run — 65% coverage, stated in the report.", "post", "guardrail-veriphysics"),
            ],
        ),
    },
    "trocadores": {
        "slug": "trocadores-e-termico",
        "pt": dict(
            meta_title="Trocadores de calor e simulação térmica · PINNeAPPle Labs",
            meta_desc=("Estudo térmico de trocadores, dissipadores e painéis: temperatura no ponto crítico, margem até "
                       "o limite e tempo até a incrustação tirar o processo da faixa. Prazo de 4 a 10 semanas."),
            eyebrow="Trocadores de calor e térmico",
            h1="O trocador sujo antes de virar parada de planta.",
            lead=("Estudo térmico de trocadores, dissipadores e painéis: temperatura no ponto crítico, margem até o "
                  "limite e quanto tempo a incrustação leva para tirar o processo da faixa — com a incerteza declarada."),
            chips=["Trocadores, dissipadores e painéis", "Erro medido e declarado", "Entrega em 4 a 10 semanas"],
            pains=[
                ("A margem que ninguém sabe quanto sobrou", "O projeto foi feito com folga. Ninguém sabe quanto dela já foi consumida pela incrustação."),
                ("A temperatura que só aparece na parada", "Quando a leitura sai da faixa, a janela de limpeza já passou e a decisão vira emergência."),
                ("A bancada que custa mais que a decisão", "Montar ensaio térmico para cada geometria custa caro e chega tarde, quando o projeto já foi fechado."),
            ],
            pains_p="Três dores que trazem um estudo térmico até aqui — e o que o número muda na decisão.",
            inputs=[
                "Geometria do trocador, dissipador ou painel (CAD, STEP ou desenho cotado)",
                "Fluidos, vazões e temperaturas de entrada dos dois lados",
                "Propriedades do material e condutividade das interfaces",
                "Para o gêmeo: histórico de operação (temperaturas, vazões, limpezas)",
                "Limite de operação: temperatura máxima e margem que a planta exige",
            ],
            outputs=[
                "Campo de temperatura e a temperatura no ponto crítico",
                "Margem até o limite de operação, com a banda de incerteza",
                "Coeficiente global e incrustação estimada (no gêmeo)",
                "Tempo estimado até sair da faixa, com a antecedência do alarme",
                "Relatório com a verificação e a seção de limites",
            ],
            stats=[
                ("0,216 °C", "de erro contra sonda redundante", "gêmeo em operação, janela separada"),
                ("95,5%", "de cobertura da banda de incerteza", "calibrada fora do treino"),
                ("2,6 h", "de antecedência no alarme", "com o erro da previsão declarado"),
                ("4,46%", "de erro médio do substituto térmico", "pior caso 7,35%, na faixa treinada"),
            ],
            fig="img/twin.jpg",
            fig_alt="Gêmeo digital de um ativo em 3D com painel de leitura ao vivo",
            fig_b="Gêmeo em operação",
            fig_s="0,216 °C de erro · alarme 2,6 h antes",
            fig_cap=("O ativo em 3D com a leitura viva ao lado — o formato do gêmeo que acompanha o trocador em operação."),
            post="gemeo-hx201",
            report="gemeo-hx201",
            extras=[
                ("Um dissipador que responde 200 mil vezes mais rápido", "Sete geometrias, um solver 3D e um substituto com 4,46% de erro médio (7,35% no pior caso), dentro da faixa treinada.", "post", "substituto-termico"),
                ("O campo certo, a física reprovada", "Um FNO com 1,7% de erro contra volumes finitos e resíduo de PDE de 0,164 contra o limite de 0,1: o cartão de confiança disse não, e o artigo mostra por quê.", "post", "fno-placa-fria"),
            ],
        ),
        "en": dict(
            meta_title="Heat exchangers and thermal simulation · PINNeAPPle Labs",
            meta_desc=("Thermal study for exchangers, heat sinks and panels: temperature at the critical point, margin "
                       "to the limit and time until fouling takes the process out of band. 4 to 10 weeks."),
            eyebrow="Heat exchangers and thermal",
            h1="The fouled exchanger before it becomes a plant shutdown.",
            lead=("A thermal study for exchangers, heat sinks and panels: temperature at the critical point, margin to "
                  "the limit and how long fouling takes to push the process out of band — with the uncertainty stated."),
            chips=["Exchangers, heat sinks and panels", "Measured and stated error", "Delivered in 4 to 10 weeks"],
            pains=[
                ("The margin nobody can size", "The design was built with slack. Nobody knows how much of it the fouling has already eaten."),
                ("The temperature that only shows up at shutdown", "By the time the reading leaves the band, the cleaning window has passed and the decision is an emergency."),
                ("The bench that costs more than the decision", "Building a thermal test for every geometry is expensive and late, arriving after the design is closed."),
            ],
            pains_p="Three pains that bring a thermal study here — and what the number changes in the decision.",
            inputs=[
                "Exchanger, heat sink or panel geometry (CAD, STEP or a dimensioned drawing)",
                "Fluids, flow rates and inlet temperatures on both sides",
                "Material properties and interface conductivity",
                "For the twin: operating history (temperatures, flow rates, cleanings)",
                "Operating limit: maximum temperature and the margin the plant requires",
            ],
            outputs=[
                "Temperature field and the temperature at the critical point",
                "Margin to the operating limit, with its uncertainty band",
                "Overall coefficient and estimated fouling (in the twin)",
                "Estimated time to leave the band, with the alarm lead time",
                "Report with the verification and the limits section",
            ],
            stats=[
                ("0.216 °C", "of error against a redundant probe", "twin in operation, separate window"),
                ("95.5%", "band coverage", "calibrated outside training"),
                ("2.6 h", "of alarm lead time", "with the forecast error stated"),
                ("4.46%", "mean error of the thermal surrogate", "7.35% worst case, inside the trained range"),
            ],
            fig="img/twin.jpg",
            fig_alt="Digital twin of an asset in 3D with a live reading panel",
            fig_b="Twin in operation",
            fig_s="0.216 °C of error · alarm 2.6 h ahead",
            fig_cap=("The asset in 3D with the live reading beside it — the shape of the twin that follows the exchanger in operation."),
            post="gemeo-hx201",
            report="gemeo-hx201",
            extras=[
                ("A heat sink that answers 200,000 times faster", "Seven geometries, one 3D solver and a surrogate at 4.46% mean error (7.35% worst case), inside the trained range.", "post", "substituto-termico"),
                ("The right field, the physics rejected", "An FNO at 1.7% error against finite volumes and a PDE residual of 0.164 against the 0.1 limit: the trust card said no, and the article shows why.", "post", "fno-placa-fria"),
            ],
        ),
    },
    "valvulas": {
        "slug": "valvulas-e-maquinas",
        "pt": dict(
            meta_title="Válvulas, bocais e máquinas de fluxo · PINNeAPPle Labs",
            meta_desc=("Estudo de escoamento compressível em válvulas, bocais e orifícios: vazão, perda de carga, "
                       "campos de pressão e a checagem que recusa o caso quando o regime não é o do projeto."),
            eyebrow="Válvulas e máquinas de fluxo",
            h1="A sua válvula opera na faixa que o catálogo promete?",
            lead=("Escoamento compressível em válvulas, bocais e orifícios: vazão, perda de carga, campos de pressão e "
                  "temperatura — e a checagem que recusa o caso quando o regime não é o que o projeto supõe."),
            chips=["Válvula, bocal, orifício", "Gás em alta queda de pressão", "Entrega em 4 a 10 semanas"],
            pains=[
                ("O catálogo dá a faixa, não o seu ponto", "A curva do fornecedor vale para água ou ar padrão. No seu gás, na sua pressão, o regime é outro."),
                ("O regime sônico que ninguém confere", "Com gás em alta queda de pressão, metade dos casos trava no gargalo. Sem essa conta, o resultado do solver sai bonito e errado."),
                ("A otimização que começa na bancada", "Testar cinco geometrias em ensaio custa meses. A ordem certa é filtrar no computador e ensaiar só a vencedora."),
            ],
            pains_p="Três dores que trazem um estudo de escoamento até aqui — e o que o número decide.",
            inputs=[
                "Geometria da válvula, bocal, orifício ou passagem (CAD/STEP), com curso e abertura",
                "Fluido e equação de estado (gás real, quando é o caso)",
                "Pressão e temperatura de entrada e de saída; vazão esperada",
                "Material e rugosidade das paredes",
                "O que a decisão precisa: vazão, perda de carga, força, ruído ou forma",
            ],
            outputs=[
                "Vazão mássica e coeficiente de descarga na abertura avaliada",
                "Perda de carga e campos de pressão, temperatura e Mach",
                "Checagem de travessia acústica: aviso quando o caso não é representável",
                "Malha com qualidade medida (não-ortogonalidade e checkMesh) registrada",
                "Relatório com a verificação e a seção de limites",
            ],
            stats=[
                ("0,19%", "de diferença entre dois solvers independentes", "benchmark público do motor Prius"),
                ("90 mil", "de células na malha hexa-dominante", "não-ortogonalidade média 10,7°"),
                ("671 s", "para o caso completo, com verificação", "válvula globo, gás em 80 → 60 bar"),
                ("3", "geometrias cobertas pelo mesmo pipeline", "válvula, orifício e bocal"),
            ],
            fig="img/exp/motor-campo.webp",
            fig_alt="Campo magnético no quarto de máquina do motor do Prius",
            fig_b="Motor Prius, dois solvers",
            fig_s="0,19% de diferença",
            fig_cap=("Do benchmark aberto do motor Prius: o mesmo caso resolvido por dois solvers independentes, com 0,19% de diferença."),
            post="motor-prius-dois-solvers",
            report="valvula-globo",
            extras=[
                ("Válvula globo, 80 → 60 bar em metano", "Caso completo em tempo físico: 2,042 kg/s, Mach 0,525 e ΔT de −7,15 K, com 5 checagens aprovadas e as 3 abertas declaradas no relatório.", "pdf", "valvula-globo"),
                ("Dois solvers, 0,19% de diferença", "O mesmo caso do motor Prius resolvido por dois solvers independentes — a checagem cruzada que sustenta o resto do pipeline.", "post", "motor-prius-dois-solvers"),
            ],
        ),
        "en": dict(
            meta_title="Valves, nozzles and flow machinery · PINNeAPPle Labs",
            meta_desc=("Compressible flow study for valves, nozzles and orifices: flow rate, pressure drop, pressure "
                       "fields and the check that refuses the case when the regime is not the design one."),
            eyebrow="Valves and flow machinery",
            h1="Does your valve operate in the range the catalogue promises?",
            lead=("Compressible flow in valves, nozzles and orifices: flow rate, pressure drop, pressure and temperature "
                  "fields — and the check that refuses the case when the regime is not what the design assumes."),
            chips=["Valve, nozzle, orifice", "Gas at high pressure drop", "Delivered in 4 to 10 weeks"],
            pains=[
                ("The catalogue gives the range, not your point", "The vendor curve holds for water or standard air. In your gas, at your pressure, the regime is another one."),
                ("The sonic regime nobody checks", "With gas at a high pressure drop, half the cases choke. Without that check, the solver result comes out pretty and wrong."),
                ("Optimization that starts on the bench", "Testing five geometries experimentally costs months. The right order is to filter on the computer and test only the winner."),
            ],
            pains_p="Three pains that bring a flow study here — and what the number decides.",
            inputs=[
                "Valve, nozzle, orifice or passage geometry (CAD/STEP), with stroke and opening",
                "Fluid and equation of state (real gas, where that is the case)",
                "Inlet and outlet pressure and temperature; expected flow rate",
                "Wall material and roughness",
                "What the decision needs: flow rate, pressure drop, force, noise or shape",
            ],
            outputs=[
                "Mass flow and discharge coefficient at the evaluated opening",
                "Pressure drop and pressure, temperature and Mach fields",
                "Acoustic crossing check: a warning when the case is not representable",
                "Mesh quality measured and recorded (non-orthogonality and checkMesh)",
                "Report with the verification and the limits section",
            ],
            stats=[
                ("0.19%", "between two independent solvers", "public Prius motor benchmark"),
                ("90k", "cells in the hex-dominant mesh", "10.7° mean non-orthogonality"),
                ("671 s", "for the full case, verification included", "globe valve, gas at 80 → 60 bar"),
                ("3", "geometries covered by the same pipeline", "valve, orifice and nozzle"),
            ],
            fig="img/exp/motor-campo.webp",
            fig_alt="Magnetic field in the quarter machine of the Prius motor",
            fig_b="Prius motor, two solvers",
            fig_s="0.19% apart",
            fig_cap=("From the open Prius motor benchmark: the same case solved by two independent solvers, 0.19% apart."),
            post="motor-prius-dois-solvers",
            report="valvula-globo",
            extras=[
                ("Globe valve, 80 → 60 bar in methane", "Full case in physical time: 2.042 kg/s, Mach 0.525 and −7.15 K, with 5 checks passed and the 3 open ones stated in the report.", "pdf", "valvula-globo"),
                ("Two solvers, 0.19% apart", "The same Prius motor case solved by two independent solvers — the cross-check the rest of the pipeline stands on.", "post", "motor-prius-dois-solvers"),
            ],
        ),
    },
}


# One META entry per segment page, built from the SEGMENTS table so the two cannot drift.
for _key, _seg in SEGMENTS.items():
    META[_key] = {
        lang: dict(
            title=_seg[lang]["meta_title"],
            desc=_seg[lang]["meta_desc"],
            og=_seg[lang]["fig"],
            type="website",
        )
        for lang in LANGUAGES
    }

# The Studio is its own page now; it keeps the product metadata.
META["studio"] = META["produto"]

META["relatorios"] = {
    "pt": dict(
        title="Relatórios de exemplo por área · PINNeAPPle Labs",
        desc=("Sete relatórios de estudo, um por área: erosão em tubulação, válvula em gás, trocador de calor, "
              "aerodinâmica do corpo de Ahmed, otimização topológica, máquina síncrona de ímãs e previsão de El Niño — "
              "cada um com a sua verificação e a sua página de limites."),
        og="img/portfolio/13-aircraft-render-pressure.jpg",
        type="website",
    ),
    "en": dict(
        title="Example reports by area · PINNeAPPle Labs",
        desc=("Seven study reports, one per area: erosion in piping, gas valve, heat exchanger, Ahmed-body "
              "aerodynamics, topology optimization, surface-PM machine and El Niño forecasting — each with its "
              "own verification and its own limits page."),
        og="img/portfolio/13-aircraft-render-pressure.jpg",
        type="website",
    ),
}


# ---------------------------------------------------------------------------
# Page: home
# ---------------------------------------------------------------------------


def page_home(lang: str) -> str:
    root = up(lang, "home")
    S = STRINGS[lang]
    C = HOME[lang]
    SH = SUCCESS_HOME[lang]
    parts = [head(lang, "home", root), header(lang, "home", root), '<main id="main">']

    chips = "".join(f'<span class="chip">{c}</span>' for c in C["chips"])
    parts.append(f"""
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">{C['eyebrow']}</p>
        <h1>{C['h1']}</h1>
        <p class="lead">{C['lead']}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{GITHUB}" target="_blank" rel="noopener">{C['cta_primary']}</a>
          <a class="btn btn-ghost" href="{root}{url(lang, 'artigos')}">{C['cta_secondary']} →</a>
        </div>
        <p class="hero-note">{ "Da pesquisa à aplicação industrial: explore a tecnologia aberta ou converse conosco sobre um projeto personalizado." if lang == "pt" else "From research to industrial applications: explore the open technology or discuss a custom project with us." }</p>
        <div class="hero-meta">{chips}</div>
      </div>
      <div>
        <figure class="hero-media">
          <img src="{root}{C['hero_img']}" alt="{C['hero_alt']}" fetchpriority="high" decoding="async" />
          <figcaption><b>{C['hero_fig_b']}</b><span>{C['hero_fig_s']}</span></figcaption>
        </figure>
      </div>
    </div>
  </section>
""")

    problems = "".join(
        f'<article class="problem-card reveal"><h3>{t}</h3><p>{b}</p></article>'
        for t, b in C["problems"]
    )
    pillar_cards = "".join(f'<article class="problem-card"><h3>{h}</h3><p>{p}</p></article>' for h,p in ([
        ("Plataforma aberta", "Ferramentas, modelos e pipelines para simulação, treinamento, inferência e verificação física."),
        ("Consultoria e projetos", "Soluções personalizadas para problemas industriais, da modelagem física à implantação."),
        ("Pesquisa e desenvolvimento", "Novos métodos, benchmarks, modelos físicos e colaboração científica."),
        ("Aplicações reais", "CFD, estruturas, energia, otimização, modelos substitutos e gêmeos digitais."),
    ] if lang == "pt" else [
        ("Open platform", "Tools, models, and pipelines for simulation, training, inference, and physics verification."),
        ("Consulting and projects", "Custom industrial solutions, from physical modeling to deployment."),
        ("Research and development", "New methods, benchmarks, physics models, and scientific collaboration."),
        ("Real-world applications", "CFD, structures, energy, optimization, surrogates, and digital twins."),
    ]))
    parts.append(f"""\n  <section id="o-que-fazemos" class="tight"><div class="wrap"><div class="section-head split"><div><p class="eyebrow">{'O que fazemos' if lang == 'pt' else 'What we do'}</p><h2>{'Da pesquisa científica à engenharia aplicada.' if lang == 'pt' else 'From scientific research to applied engineering.'}</h2></div><p>{'O PINNeAPPle Labs conecta desenvolvimento tecnológico, pesquisa e consultoria para tornar Physics AI acessível e aplicável em diferentes áreas da ciência e engenharia.' if lang == 'pt' else 'PINNeAPPle Labs brings together technology development, research, and consulting to make Physics AI accessible and useful across science and engineering.'}</p></div><div class="problem-grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">{pillar_cards}</div></div></section>\n""")
    parts.append(f"""
  <section id="problema" class="alt tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['problem_eyebrow']}</p><h2>{C['problem_h']}</h2></div>
        <p>{C['problem_p']}</p>
      </div>
      <div class="problem-grid reveal">{problems}</div>
    </div>
  </section>
""")

    entrega = "".join(
        f'<article class="problem-card reveal"><h3>{t}</h3><p>{b}</p></article>'
        for t, b in C["entrega"]
    )
    parts.append(f"""
  <section id="consultoria" class="tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['entrega_eyebrow']}</p><h2>{C['entrega_h']}</h2></div>
        <p>{C['entrega_p']}</p>
      </div>
      <div class="problem-grid reveal">{entrega}</div>
      <div class="note reveal"><span><b>{C['entrega_note_b']}</b> {C['entrega_note']}</span></div>
      <p class="section-cta reveal">{wa_button(lang, label="Discutir um projeto" if lang == "pt" else "Discuss a project")} {report_button(lang, root)}</p>
    </div>
  </section>
""")

    stats = "".join(
        f'    <div class="stat-cell" role="listitem"><div class="n{" cyan" if i % 2 else ""}">{n}</div>'
        f'<div class="l">{l}</div><div class="s">{s}</div></div>\n'
        for i, (n, l, s) in enumerate(C["stats"])
    )
    parts.append(f'  <div class="stats" role="list">\n{stats}  </div>\n')

    proofs = "".join(
        f'<figure class="result"><img src="{root}{src}" alt="{alt}" loading="lazy" decoding="async" />'
        f'<figcaption><span class="kind">{tag}</span><b>{title}</b></figcaption>'
        f'<a class="stretch" href="{root}{url(lang, "post:" + slug)}" aria-label="{title}"></a></figure>\n'
        for src, alt, tag, title, slug in C["proofs"]
    )
    parts.append(f"""
  <section id="resultados">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['proofs_eyebrow']}</p><h2>{C['proofs_h']}</h2></div>
        <p>{C['proofs_p']}</p>
      </div>
      <div class="result-grid reveal">
{proofs}      </div>
      <div class="reveal" style="margin-top:3.4rem">
        <p class="eyebrow">{SH['eyebrow']}</p>
        <div class="grid-4">{success_highlights(lang, root)}</div>
      </div>
      <p class="section-cta reveal">
        <a class="btn btn-primary" href="{root}{url(lang, 'sucessos')}">{SH['btn']} →</a>
        <a class="btn btn-ghost" href="{root}{url(lang, 'relatorios')}">{S['lbl_reports']} →</a>
      </p>
    </div>
  </section>
""")

    segs = "".join(
        f'<article class="problem-card reveal"><h3><a href="{root}{url(lang, key)}">{t}</a></h3><p>{b}</p>'
        f'<p class="src-note"><a href="{root}{url(lang, key)}">{C["seg_more"]} →</a> · '
        f'<a href="{root}{url(lang, "post:" + post)}">{C["seg_link"]}</a></p></article>'
        for t, b, key, post in C["segs"]
    )
    parts.append(f"""
  <section id="segmentos" class="alt tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['seg_eyebrow']}</p><h2>{C['seg_h']}</h2></div>
        <p>{C['seg_p']}</p>
      </div>
      <div class="problem-grid reveal">{segs}</div>
      <p class="section-cta reveal"><a class="btn btn-ghost" href="{root}{url(lang, 'artigos')}">{S['all_articles']} →</a></p>
    </div>
  </section>
""")

    parts.append(f"""
  <section id="produto" class="tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['product_eyebrow']} · 2027</p><h2>{C['product_h']}</h2></div>
        <p>{C['product_lead']}</p>
      </div>
      <p class="section-cta reveal" style="border:0;padding-top:0">
        <a class="btn btn-ghost" href="{root}{url(lang, 'studio')}">{C['product_cta']} →</a>
        <a class="btn btn-quiet" href="{root}{url(lang, 'studio')}#pre-acesso">{S['pre_btn']} ↗</a>
      </p>
    </div>
  </section>
""")

    cards = "".join(post_card(lang, p, root) for p in POSTS[:3])
    parts.append(f"""
  <section id="artigos" class="alt">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['news_eyebrow']}</p><h2>{C['news_h']}</h2></div>
        <p>{C['news_p']}</p>
      </div>
      <div class="post-grid reveal">{cards}</div>
      <p class="section-cta reveal"><a class="btn btn-ghost" href="{root}{url(lang, 'artigos')}">{S['all_articles']} →</a></p>
    </div>
  </section>
""")

    story_p = "".join(f"<p>{p}</p>" for p in C["story_p"])
    parts.append(f"""
  <section id="historia">
    <div class="wrap split-block reveal">
      <div>
        <p class="eyebrow">{C['story_eyebrow']}</p>
        <h2 style="font-size:clamp(1.5rem,2.8vw,2rem);margin-bottom:1rem">{C['story_h']}</h2>
        <div class="prose" style="max-width:56ch">{story_p}</div>
        <div class="card person-card">
          <div class="person">
            <img src="{root}img/team/yan-barros.jpg" alt="{C['person_name']}" loading="lazy" decoding="async" />
            <div>
              <strong>{C['person_name']}</strong>
              <span class="role">{C['person_role']}</span>
              <p>{C['person_bio']}</p>
            </div>
          </div>
        </div>
        <p class="section-cta" style="border:0;padding:0;margin-top:1.4rem">
          <a class="btn btn-ghost" href="{root}{url(lang, 'lib')}">{C['story_cta']} →</a>
          <a class="btn btn-quiet" href="https://www.linkedin.com/in/yan-barros-yan" target="_blank" rel="noopener">LinkedIn →</a>
        </p>
      </div>
      <figure class="media">
        <img src="{root}img/erosao.jpg" alt="Mapa de erosão na parede de uma curva de 90 graus" loading="lazy" decoding="async" />
        <figcaption>Erosão numa curva de 90°, comparada com ensaio publicado: 1,05–1,49×.</figcaption>
      </figure>
    </div>
  </section>
""")

    parts.append(cta_band(lang, root))
    parts.append("</main>")
    parts.append(footer(lang, "home", root))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Page: product
# ---------------------------------------------------------------------------


def produto_sections(lang: str, root: str) -> str:
    """The product deep dive, rendered inside the home page."""
    S = STRINGS[lang]
    C = PRODUCT[lang]

    chips = "".join(f'<span class="chip">{c}</span>' for c in C["chips"])
    counts = "".join(
        f'<div class="exist-cell"><b>{n}</b><span>{l}</span></div>' for n, l in C["counts"]
    )
    flow = "".join(
        f'<div class="step reveal"><span class="sn">{n}</span><h3>{t}</h3><p>{b}</p></div>'
        for n, t, b in C["flow"]
    )
    flow_shots = reel(lang, root)
    caps = "".join(
        f'<article class="cap reveal"><p class="kind">{kind}</p><h3>{title}</h3><p>{body}</p>'
        f'<p class="ex"><b>{example}</b></p></article>'
        for kind, title, body, example in CAPS[lang]
    )
    trust = "".join(f"<li>{t}</li>" for t in C["trust"])
    inputs = "".join(f"<li>{t}</li>" for t in C["inputs"])
    outputs = "".join(f"<li>{t}</li>" for t in C["outputs"])
    shots = "".join(
        f'<figure class="shot"><img src="{root}{src}" alt="{alt}" loading="lazy" decoding="async" />'
        f'<figcaption>{cap}</figcaption></figure>'
        for src, alt, cap in C["shots"]
    )
    videos = "".join(
        f'<figure class="fig vfig"><video src="{root}{src}" poster="{root}{poster}" muted loop playsinline '
        f'preload="none" data-autoplay aria-label="{cap}"></video><figcaption>{cap}</figcaption></figure>'
        for src, poster, cap in C["videos"]
    )
    rows = "".join(
        f'      <tr><td class="name">{name}</td><td>{what}</td>'
        f'<td><span class="badge {"ok" if when in ("roda hoje", "runs today") else "warn"}">{when}</span></td></tr>\n'
        for name, what, when in C["state_rows"]
    )

    return f"""  <section id="produto" class="alt tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['what_eyebrow']}</p><h2>{C['what_h']}</h2></div>
        <div><p>{C['what_p'][0]}</p><p style="margin-top:1rem">{C['what_p'][1]}</p></div>
      </div>
      <div class="exist-grid reveal">{counts}</div>
      <p class="src-note reveal">{C['counts_note']}</p>
    </div>
  </section>

  <section id="fluxo">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['flow_eyebrow']}</p><h2>{C['flow_h']}</h2></div>
        <p>{C['flow_p']}</p>
      </div>
      <div class="steps reveal">{flow}</div>
      <div class="single-shot reveal">{flow_shots}</div>
      <p class="reel-note">{C["flow_reel_note"]}</p>
    </div>
  </section>

  <section id="capacidades" class="alt">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['caps_eyebrow']}</p><h2>{C['caps_h']}</h2></div>
        <p>{C['caps_p']}</p>
      </div>
      <div class="grid-3 reveal">{caps}</div>
    </div>
  </section>

  <section id="confianca">
    <div class="wrap split-block reveal">
      <div>
        <p class="eyebrow">{C['trust_eyebrow']}</p>
        <h2 style="font-size:clamp(1.5rem,2.8vw,2rem);margin-bottom:1rem">{C['trust_h']}</h2>
        <ul class="checks">{trust}</ul>
      </div>
      <figure class="frame">
        <div class="frame-bar" aria-hidden="true"><i></i><i></i><i></i><span>VeriPhysics · {'verificação' if lang == 'pt' else 'verification'}</span></div>
        <img src="{root}img/verificacao.jpg" alt="Relatório de checagens com nota por item" loading="lazy" decoding="async" />
        <figcaption>Nota por checagem, com cobertura declarada. O que não rodou não conta como aprovado.</figcaption>
      </figure>
    </div>
  </section>

  <section id="entra-sai" class="alt">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['io_eyebrow']}</p><h2>{C['io_h']}</h2></div>
        <p>{C['io_p']}</p>
      </div>
      <div class="io-grid reveal">
        <div class="io-col"><h3>{'Entra' if lang == 'pt' else 'In'}</h3><ul class="ticks">{inputs}</ul></div>
        <div class="io-col"><h3>{'Sai' if lang == 'pt' else 'Out'}</h3><ul class="ticks">{outputs}</ul></div>
      </div>
    </div>
  </section>

  <section id="telas">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['shots_eyebrow']}</p><h2>{C['shots_h']}</h2></div>
        <p>{C['shots_p']}</p>
      </div>
      <div class="shot-grid reveal">{shots}</div>
      <div class="section-head reveal" style="margin-top:3.5rem">
        <p class="eyebrow">{C['film_eyebrow']}</p><h2 style="font-size:clamp(1.4rem,2.6vw,1.9rem)">{C['film_h']}</h2>
        <p>{C['film_p']}</p>
      </div>
      <figure class="fig film reveal">
        <video src="{root}{C['film'][0]}" poster="{root}{C['film'][1]}" muted playsinline
               preload="none" data-autoplay controls aria-label="{C['film'][2]}"></video>
        <figcaption>{C['film'][2]}</figcaption>
      </figure>
      <div class="section-head reveal" style="margin-top:3.5rem">
        <p class="eyebrow">{C['videos_eyebrow']}</p><h2 style="font-size:clamp(1.4rem,2.6vw,1.9rem)">{C['videos_h']}</h2>
        <p>{C['videos_p']}</p>
      </div>
      <div class="video-grid reveal">{videos}</div>
    </div>
  </section>

  <section id="estado" class="alt">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['state_eyebrow']}</p><h2>{C['state_h']}</h2></div>
        <p>{C['state_p']}</p>
      </div>
      <div class="table-wrap reveal">
        <table class="data">
          <thead><tr><th scope="col">{'Módulo' if lang == 'pt' else 'Module'}</th><th scope="col">{'O que faz' if lang == 'pt' else 'What it does'}</th><th scope="col">{'Quando' if lang == 'pt' else 'When'}</th></tr></thead>
          <tbody>
{rows}          </tbody>
        </table>
      </div>
      <div class="note reveal"><span><b>{'Limite declarado' if lang == 'pt' else 'Stated limit'}:</b> {C['limits_note']}</span></div>
      <div class="note reveal"><span><b>{S['soon']}:</b> {C['soon_note']}</span></div>
      <p class="section-cta reveal">
        <a class="btn btn-primary" href="https://wa.me/{WHATSAPP}?text={_q(C['cta_primary'])}" target="_blank" rel="noopener">{C['cta_primary']}</a>
        <a class="btn btn-ghost" href="{root}{url(lang, 'lib')}">{S['lbl_lib']} →</a>
      </p>
    </div>
  </section>
"""


# ---------------------------------------------------------------------------
# Pages: segment and product
# ---------------------------------------------------------------------------


def oferta_section(lang: str, root: str, extra: str = "") -> str:
    """Scope, deadline and price — the same block on the home and on every segment page."""
    C = HOME[lang]
    O = OFERTA[lang]
    cards = "".join(
        f'<article class="problem-card reveal"><h3>{t}</h3><p>{b}</p></article>'
        for t, b in C["entrega"]
    )
    return f"""  <section id="oferta" class="tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{O['eyebrow']}</p><h2>{O['h']}</h2></div>
        <p>{O['linha']}</p>
      </div>
      <div class="problem-grid reveal">{cards}</div>
      <div class="note reveal"><span><b>{C['entrega_note_b']}</b> {C['entrega_note']}</span></div>
      <p class="section-cta reveal">{wa_button(lang, label=C['cta_primary'])} {extra}</p>
    </div>
  </section>
"""


def report_button(lang: str, root: str, slug: str = "estudo-erosao-curva-90",
                  cls: str = "btn btn-ghost") -> str:
    """The public example report, the closest thing to seeing the deliverable."""
    return (f'<a class="{cls}" href="{root}{REPORT_FILES[slug][lang]}" target="_blank" rel="noopener">'
            f'{REPORT_LABEL[lang]} ↗</a>')


def page_segment(lang: str, key: str) -> str:
    """One problem, one page: the object the buyer searches for, its proof, its offer."""
    root = up(lang, key)
    S = STRINGS[lang]
    U = SEGUI[lang]
    O = OFERTA[lang]
    C = SEGMENTS[key][lang]

    parts = [head(lang, key, root), header(lang, key, root), '<main id="main">']

    chips = "".join(f'<span class="chip">{c}</span>' for c in C["chips"])
    if C.get("report"):
        second = report_button(lang, root, C["report"])
    else:
        second = (f'<a class="btn btn-ghost" href="{root}{url(lang, "post:" + C["post"])}">'
                  f'{U["study"]} →</a>')
    parts.append(f"""
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">{C['eyebrow']}</p>
        <h1>{C['h1']}</h1>
        <p class="lead">{C['lead']}</p>
        <div class="hero-actions">
          {wa_button(lang, label=HOME[lang]['cta_primary'])}
          {second}
        </div>
        <p class="hero-note">{O['linha']}</p>
        <div class="hero-meta">{chips}</div>
      </div>
      <div>
        <figure class="hero-media">
          <img src="{root}{C.get('hero_fig', C['fig'])}" alt="{C['fig_alt']}" />
          <figcaption><b>{C['fig_b']}</b><span>{C['fig_s']}</span></figcaption>
        </figure>
      </div>
    </div>
  </section>
""")

    pains = "".join(
        f'<article class="problem-card reveal"><h3>{t}</h3><p>{b}</p></article>'
        for t, b in C["pains"]
    )
    parts.append(f"""
  <section id="dor" class="alt tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{U['pain_eyebrow']}</p><h2>{U['pain_h']}</h2></div>
        <p>{C['pains_p']}</p>
      </div>
      <div class="problem-grid reveal">{pains}</div>
    </div>
  </section>
""")

    ins = "".join(f"<li>{t}</li>" for t in C["inputs"])
    outs = "".join(f"<li>{t}</li>" for t in C["outputs"])
    parts.append(f"""
  <section id="entra-sai" class="tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{U['io_eyebrow']}</p><h2>{U['io_h']}</h2></div>
        <p>{U['io_note']}</p>
      </div>
      <div class="io-grid reveal">
        <div class="io-col"><h3>{U['io_in']}</h3><ul class="ticks">{ins}</ul></div>
        <div class="io-col"><h3>{U['io_out']}</h3><ul class="ticks">{outs}</ul></div>
      </div>
    </div>
  </section>
""")

    stats = "".join(
        f'<div class="exist-cell"><b>{n}</b><span>{l} · {s}</span></div>'
        for n, l, s in C["stats"]
    )
    extra_cards = []
    for title, body, kind, ref in C.get("extras", []):
        if kind == "pdf":
            href = root + REPORT_FILES[ref][lang]
            label = REPORT_LABEL[lang]
        else:
            href = root + url(lang, "post:" + ref)
            label = SEGUI[lang]["study"]
        extra_cards.append(
            f'<article class="problem-card reveal"><h3>{title}</h3><p>{body}</p>'
            f'<p class="src-note"><a href="{href}">{label} →</a></p></article>'
        )
    extras = (f'<h3 class="reveal" style="margin-top:2.6rem">{SEGUI[lang]["more"]}</h3>'
              f'<div class="problem-grid reveal">{"".join(extra_cards)}</div>') if extra_cards else ""
    parts.append(f"""
  <section id="prova" class="alt tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{U['proof_eyebrow']}</p><h2>{U['proof_h']}</h2></div>
        <p>{C['fig_cap']}</p>
      </div>
      <div class="exist-grid reveal">{stats}</div>
      <figure class="fig reveal">
        <img src="{root}{C['fig']}" alt="{C['fig_alt']}" loading="lazy" decoding="async" />
        <figcaption>{C['fig_cap']}</figcaption>
      </figure>
      {extras}
      <p class="section-cta reveal">
        <a class="btn btn-ghost" href="{root}{url(lang, "post:" + C["post"])}">{U['study']} →</a>
        {report_button(lang, root, C.get("report", "estudo-erosao-curva-90"), "btn btn-quiet")}
        <a class="btn btn-quiet" href="{root}{url(lang, 'relatorios')}">{S['lbl_reports']} →</a>
      </p>
    </div>
  </section>
""")

    parts.append(oferta_section(lang, root, report_button(lang, root, C.get("report", "estudo-erosao-curva-90"))))

    others = "".join(
        f'<a class="btn btn-ghost" href="{root}{url(lang, k)}">{SEGLABELS[lang][k]} →</a>'
        for k in SEGMENTS
        if k != key
    )
    parts.append(f"""
  <section id="outros" class="tight">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">{U['others_eyebrow']}</p>
        <h2 style="font-size:clamp(1.4rem,2.6vw,1.9rem)">{U['others_h']}</h2>
      </div>
      <p class="section-cta reveal" style="border:0;padding-top:0">{others}</p>
    </div>
  </section>
""")

    parts.append(cta_band(lang, root))
    parts.append("</main>")
    parts.append(footer(lang, key, root))
    return "".join(parts)


def apresentacao_section(lang: str, root: str) -> str:
    """The SIMR talk: the whole product in one recording, proof rather than a promise."""
    C = HOME[lang]
    return f"""  <section id="apresentacao" class="tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['show_eyebrow']}</p><h2>{C['show_h']}</h2></div>
        <p>{C['show_p']}</p>
      </div>
      <button class="yt reveal" data-id="bTRafLSKADk" aria-label="{C['show_play']}">
        <img src="{root}img/simr.jpg" alt="{C['show_cap']}" loading="lazy" decoding="async" />
        <span class="yt-play" aria-hidden="true"></span>
        <span class="yt-cap">{C['show_cap']}</span>
      </button>
    </div>
  </section>
"""


def page_studio(lang: str) -> str:
    """The product, on its own address, with the early-access list as its conversion."""
    root = up(lang, "studio")
    S = STRINGS[lang]
    C = PRODUCT[lang]
    M = META["studio"][lang]
    form = PREACCESS_FORM.get(lang, "")
    chips = "".join(f'<span class="chip">{c}</span>' for c in C["chips"])
    primary = (f'<a class="btn btn-primary" href="{form}" target="_blank" rel="noopener">'
               f'{S["pre_btn"]} <span aria-hidden="true">↗</span></a>') if form else wa_button(lang)

    parts = [head(lang, "studio", root), header(lang, "studio", root), '<main id="main">']
    parts.append(f"""
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">{C['eyebrow']}</p>
        <h1>PINNeAPPle Studio</h1>
        <p class="lead">{M['desc']}</p>
        <div class="hero-actions">
          {primary}
          <a class="btn btn-ghost" href="#fluxo">{'Como funciona' if lang == 'pt' else 'How it works'} →</a>
        </div>
        <p class="hero-note">{S['prod_note']}</p>
        <div class="hero-meta">{chips}</div>
      </div>
      <div>
        <figure class="frame">
          <div class="frame-bar" aria-hidden="true"><i></i><i></i><i></i><span>PINNeAPPle Studio</span></div>
          <img src="{root}img/eng/studio-home.webp" alt="{C['hero_cap']}" fetchpriority="high" decoding="async" />
          <figcaption>{C['hero_cap']}</figcaption>
        </figure>
      </div>
    </div>
  </section>
""")
    parts.append(produto_sections(lang, root))
    parts.append(apresentacao_section(lang, root))
    parts.append(pre_band(lang, root))
    parts.append("</main>")
    parts.append(footer(lang, "studio", root))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Pages: articles
# ---------------------------------------------------------------------------


def post_card(lang: str, p: dict, root: str) -> str:
    S = STRINGS[lang]
    # A chart is not a photograph: cropping it to fill the card would cut the axes
    # off, so chart cards get the picture whole, on a plate. See `.thumb.chart`.
    thumb = "thumb chart" if p.get("chart") else "thumb"
    return f"""<a class="post-card" href="{root}{url(lang, 'post:' + p['slug'])}">
  <span class="{thumb}"><img src="{root}{p['thumb']}" alt="{p['title'][lang]}" loading="lazy" decoding="async" /></span>
  <span class="pb">
    <span class="meta">{p['tag'][lang]} · {p['mins']} {S['min_read']}</span>
    <h3>{p['title'][lang]}</h3>
    <p>{p['lead'][lang]}</p>
    <span class="foot">{p['date'][lang]}</span>
  </span>
</a>"""


def page_artigos(lang: str) -> str:
    root = up(lang, "artigos")
    C = ARTICLES[lang]
    cards = "".join(post_card(lang, p, root) for p in POSTS)
    return "".join([
        head(lang, "artigos", root), header(lang, "artigos", root),
        f"""<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow">{C['eyebrow']}</p>
      <h1>{C['h1']}</h1>
      <p class="lead" style="max-width:66ch">{C['lead']}</p>
    </div>
  </section>

  <section class="tight">
    <div class="wrap">
      <div class="post-grid reveal">{cards}</div>
    </div>
  </section>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, "artigos", root),
    ])


def render_block(lang: str, block: tuple, root: str) -> str:
    kind = block[0]
    if kind == "h2":
        return f"<h2>{block[1]}</h2>"
    if kind == "p":
        return f"<p>{block[1]}</p>"
    if kind == "fig":
        src, alt, cap = block[1]
        return fig(src, alt, cap, root)
    if kind == "video":
        src, poster, cap = block[1]
        return vfig(src, poster, cap, root)
    raise ValueError(f"unknown block {kind}")


def page_post(lang: str, slug: str) -> str:
    page = f"post:{slug}"
    root = up(lang, page)
    S = STRINGS[lang]
    p = POST_BY_SLUG[slug]
    body = "".join(render_block(lang, b, root) for b in p["body"][lang])
    value, label = p["metric"][lang]

    idx = [x["slug"] for x in POSTS].index(slug)
    newer = POSTS[idx - 1] if idx > 0 else None
    older = POSTS[idx + 1] if idx + 1 < len(POSTS) else None
    nav = ""
    if newer or older:
        left = (f'<a class="post-prev" href="{root}{url(lang, "post:" + newer["slug"])}">'
                f'← {newer["title"][lang]}</a>') if newer else "<span></span>"
        right = (f'<a class="post-next" href="{root}{url(lang, "post:" + older["slug"])}">'
                 f'{older["title"][lang]} →</a>') if older else "<span></span>"
        nav = f'<nav class="post-nav" aria-label="{"Mais artigos" if lang == "pt" else "More articles"}">{left}{right}</nav>'

    return "".join([
        head(lang, page, root), header(lang, page, root),
        f"""<main id="main">
  <article>
    <header class="post-head">
      <div class="wrap">
        <p class="post-tagline"><a href="{root}{url(lang, 'artigos')}">← {'Artigos' if lang == 'pt' else 'Articles'}</a></p>
        <p class="eyebrow">{p['tag'][lang]}</p>
        <h1>{p['title'][lang]}</h1>
        <p class="lead" style="max-width:62ch">{p['lead'][lang]}</p>
        <p class="post-meta">
          <span class="chip">{p['date'][lang]}</span>
          <span class="chip">{p['mins']} {S['min_read']}</span>
        </p>
      </div>
    </header>

    <div class="wrap post-body">
      <div class="prose">
{body}
        <div class="measure"><b>{value}</b><span>{label}</span></div>
        <div class="note limits-up"><span><b>{'O que não foi provado' if lang == 'pt' else 'What was not proven'}:</b> {p['limits'][lang]}</span></div>
        {nav}
      </div>
    </div>
  </article>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, page, root),
    ])


# ---------------------------------------------------------------------------
# Page: library
# ---------------------------------------------------------------------------

LAYERS = [
    ("Aplicação", "APPS &amp; SERVING", ["pinneapple_app", "pinneapple_studio", "pinneapple_lab", "pinneapple_hub", "pinneapple_arena", "pinneapple_autolab", "pinneapple_orchestration", "REST / FastAPI"]),
    ("Agentes", "AGENTS", ["pinneapple_llm", "pinneapple_reason", "pinneapple_query", "pinneapple_condense", "pinneapple_flow", "pinneapple_mcp"]),
    ("Modelos", "NEURAL", ["pinneapple_neural", "pinneapple_models", "pinneapple_train", "pinneapple_worldmodel", "PINN", "FNO", "DeepONet", "GNN"]),
    ("Física &amp; solvers", "PHYSICS", ["pinneapple_physics", "pinneapple_solvers", "pinneapple_simulation", "pinneapple_problemdesign", "OpenFOAM", "FEniCS/dolfinx", "CalculiX"]),
    ("Análise &amp; verificação", "ANALYSIS &amp; UQ", ["pinneapple_analysis", "pinneapple_veriphysics", "pinneapple_check", "pinneapple_decision", "pinneapple_adaptation", "pinneapple_stability", "UQ", "EnKF"]),
    ("Dados &amp; geometria", "DATA", ["pinneapple_data", "pinneapple_design", "pinneapple_catalog", "pinneapple_pdb", "pinneapple_twin3d", "pinneapple_blender", "pinneapple_unity", "pinneapple_perception"]),
    ("Núcleo", "CORE", ["pinneapple_core", "pinneapple_registry", "pinneapple_tools", "pinneapple_security", "pinneapple_systems", "pinneapple_science", "pinneapple_presets", "pinneapple_quantum", "pinneapple_futures"]),
]

LAYERS_EN = [
    ("Application", "APPS &amp; SERVING", LAYERS[0][2]),
    ("Agents", "AGENTS", LAYERS[1][2]),
    ("Models", "NEURAL", LAYERS[2][2]),
    ("Physics &amp; solvers", "PHYSICS", LAYERS[3][2]),
    ("Analysis &amp; verification", "ANALYSIS &amp; UQ", LAYERS[4][2]),
    ("Data &amp; geometry", "DATA", LAYERS[5][2]),
    ("Core", "CORE", LAYERS[6][2]),
]

LIB = {
    "pt": dict(
        eyebrow="A biblioteca",
        h1="Um pipeline, do PDE escrito à predição servida.",
        lead="44 pacotes Python num só install: você importa só a camada que precisa. Nenhuma camada esconde a de baixo, então você vê a malha, o resíduo, a arquitetura e o erro.",
        stack_h="Arquitetura em camadas",
        why_bold="Por que isso importa",
        why="a mesma biblioteca que treina a rede é a que roda o solver de referência. Comparar o modelo com ele mesmo é o erro mais comum em Physics AI. Aqui a referência é sempre externa ao treino.",
        start_h="A equação entra como texto",
        start_p="Instalação com um comando, sem build. O PyPI está na 0.7.0 e o repositório já está na 0.8.0. O mesmo pacote roda o problema, o treino, a comparação com o solver e o relatório.",
        gains_h="O que você ganha no primeiro dia",
        gains=[
            "<b>Um ambiente reproduzível</b>: 105 projetos de exemplo, 173 execuções com saída versionada e 642 arquivos de teste, para comparar com o seu resultado.",
            "<b>Benchmarks públicos</b>: SSQN Helmholtz, LBM vortex shedding, espaço de projeto LPM, latência e I/O.",
            "<b>Interoperabilidade real</b>: OpenFOAM, CalculiX, FEniCS/dolfinx, Gmsh, VTK, STL, USD e glTF na mesma sessão.",
            "<b>Padrões da indústria</b>: AAS, DTDL, NGSI-LD, Eclipse Ditto e OPC UA para o que a planta já consome.",
        ],
        oss_h="A base é pública. A verificação também.",
        oss_p="Apache-2.0, no PyPI, com releases versionadas. O que é aberto está aberto de verdade, e o que é produto está dito como produto.",
        honest_bold="A separação honesta",
        honest="Os quatro repositórios acima são genuinamente abertos. Os produtos são entregues como engenharia, não como release de código aberto.",
        repos=[
            ("PINNeAPPle-Labs/PINNeAPPle", "O núcleo: PINN, FNO, DeepONet, GNN, solvers, geometria, UQ, gêmeos digitais e serving REST.", "★ 118 · forks 34 · Apache-2.0 · PyPI 0.7.0 · repositório 0.8.0"),
            ("PINNeAPPle-Labs/pinnfactory", "Framework leve e independente para PINNs a partir de PDEs em SymPy, com autodiferenciação em PyTorch.", "★ 72 · Apache-2.0 · standalone"),
            ("PINNeAPPle-Labs/PINNeAPPle-Benchmark", "Benchmarks públicos e reprodutíveis: SSQN Helmholtz, LBM vortex shedding, LPM, latência, shard balance.", "reprodutível · gráficos versionados"),
            ("PINNeAPPle-Labs/pinnaitor", "Framework agêntico de uso geral (ELM AI Agentic Framework), em estágio anterior, dito com clareza.", "★ 22 · MIT · estágio inicial"),
        ],
        install="pip install pinneapple",
        docs_btn="Abrir a documentação",
    ),
    "en": dict(
        eyebrow="The library",
        h1="One pipeline, from the written PDE to the served prediction.",
        lead="44 Python packages in one install: you import only the layer you need. No layer hides the one below it, so you see the mesh, the residual, the architecture and the error.",
        stack_h="Layered architecture",
        why_bold="Why this matters",
        why="the same library that trains the network also runs the reference solver. Comparing a model against itself is the most common mistake in Physics AI. Here the reference is always external to training.",
        start_h="The equation goes in as text",
        start_p="One-command install, no build. PyPI is on 0.7.0 and the repository is already on 0.8.0. The same package runs the problem, the training, the comparison against the solver and the report.",
        gains_h="What you get on day one",
        gains=[
            "<b>A reproducible environment</b>: 105 example projects, 173 runs with versioned output and 642 test files, to compare against your own result.",
            "<b>Public benchmarks</b>: SSQN Helmholtz, LBM vortex shedding, LPM design space, latency and I/O.",
            "<b>Real interoperability</b>: OpenFOAM, CalculiX, FEniCS/dolfinx, Gmsh, VTK, STL, USD and glTF in one session.",
            "<b>Industry standards</b>: AAS, DTDL, NGSI-LD, Eclipse Ditto and OPC UA for what the plant already consumes.",
        ],
        oss_h="The base is public. So is verification.",
        oss_p="Apache-2.0, on PyPI, with versioned releases. What is open is genuinely open, and what is a product is called a product.",
        honest_bold="The honest split",
        honest="The four repositories above are genuinely open source. The products are delivered as engineering, not as an open-source release.",
        repos=[
            ("PINNeAPPle-Labs/PINNeAPPle", "The core: PINN, FNO, DeepONet, GNN, solvers, geometry, UQ, digital twins and REST serving.", "★ 118 · 34 forks · Apache-2.0 · PyPI 0.7.0 · repository 0.8.0"),
            ("PINNeAPPle-Labs/pinnfactory", "A lightweight, standalone framework for PINNs from PDEs in SymPy, with PyTorch autodiff.", "★ 72 · Apache-2.0 · standalone"),
            ("PINNeAPPle-Labs/PINNeAPPle-Benchmark", "Public, reproducible benchmarks: SSQN Helmholtz, LBM vortex shedding, LPM, latency, shard balance.", "reproducible · versioned plots"),
            ("PINNeAPPle-Labs/pinnaitor", "A general-purpose agentic framework (ELM AI Agentic Framework), at an earlier stage, said plainly.", "★ 22 · MIT · early stage"),
        ],
        install="pip install pinneapple",
        docs_btn="Open the documentation",
    ),
}

CODE = """<pre class="code"><span class="c"># o coeficiente h que ninguém mede, a partir de alguns termopares</span>
<span class="k">from</span> pinneapple_physics <span class="k">import</span> HeatConduction1D
<span class="k">from</span> pinneapple_neural <span class="k">import</span> PINNTrainer

problem = HeatConduction1D(conductivity=<span class="n">50.0</span>, length=<span class="n">0.30</span>, learn_h=<span class="k">True</span>)
model = PINNTrainer(problem, layers=[<span class="n">3</span>, <span class="n">64</span>, <span class="n">64</span>, <span class="n">1</span>])
report = model.fit(thermocouples=medicoes, epochs=<span class="n">5000</span>)

<span class="f">print</span>(report.h, report.h_std)         <span class="c"># 14.8 0.3  (verdadeiro: 15)</span>
report.verify_against(<span class="s">"finite-volume"</span>)  <span class="c"># erro por campo, mapa de erro</span></pre>"""

CODE_EN = CODE.replace("o coeficiente h que ninguém mede, a partir de alguns termopares",
                       "the h nobody measures, from a handful of thermocouples") \
               .replace("verdadeiro: 15", "true value: 15") \
               .replace("erro por campo, mapa de erro", "per-field error, error map") \
               .replace("medicoes", "readings")


def page_relatorios(lang: str) -> str:
    """The report library: every example report, grouped by the area of engineering."""
    root = up(lang, "relatorios")
    C = REPORTS_INDEX[lang]
    label = REPORT_LABEL[lang]
    parts = [head(lang, "relatorios", root), header(lang, "relatorios", root), '<main id="main">']

    parts.append(f"""
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">{C['eyebrow']}</p>
      <h1>{C['h1']}</h1>
      <p class="lead" style="max-width:64ch">{C['lead']}</p>
      <p class="hero-note" style="max-width:64ch">{C['note']}</p>
    </div>
  </section>
""")

    sections = []
    for i, (area, blurb, items) in enumerate(C["areas"]):
        cards = "".join(
            f'<article class="problem-card reveal"><h3>{title}</h3><p>{body}</p>'
            f'<p class="src-note"><a href="{root}{REPORT_FILES[slug][lang]}" target="_blank" '
            f'rel="noopener">{label} ↗</a></p></article>'
            for slug, title, body in items
        )
        sections.append(f"""
  <section class="{'alt ' if i % 2 else ''}tight" id="area-{i + 1}">
    <div class="wrap area-row">
      <div class="reveal">
        <p class="eyebrow">{C['area_lbl']} {i + 1:02d}</p>
        <h2>{area}</h2>
        <p class="area-blurb">{blurb}</p>
      </div>
      <div class="problem-grid reveal">{cards}</div>
    </div>
  </section>
""")

    how = "".join(f"<li>{h}</li>" for h in C["how"])
    parts.append("".join(sections))
    parts.append(f"""
  <section class="tight">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['how_eyebrow']}</p><h2>{C['how_h']}</h2></div>
      </div>
      <ul class="ticks reveal">{how}</ul>
    </div>
  </section>
""")
    parts.append(cta_band(lang, root))
    parts.append("</main>")
    parts.append(footer(lang, "relatorios", root))
    return "".join(parts)


def page_lib(lang: str) -> str:
    root = up(lang, "lib")
    C = LIB[lang]
    layers = LAYERS if lang == "pt" else LAYERS_EN
    stack = "".join(
        f'<div class="layer"><div class="lname">{name}<small>{sub}</small></div>'
        f'<div class="lmods">{"".join(f"<span>{m}</span>" for m in mods)}</div></div>\n'
        for name, sub, mods in layers
    )
    gains = "".join(f"<li>{g}</li>" for g in C["gains"])
    repos = "".join(
        f'''<article class="repo">
          <div><h3><svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8a8 8 0 0 0 5.47 7.59c.4.07.55-.17.55-.38v-1.34c-2.23.48-2.7-1.07-2.7-1.07-.36-.93-.89-1.18-.89-1.18-.73-.5.05-.49.05-.49.81.06 1.23.83 1.23.83.72 1.23 1.88.87 2.34.67.07-.52.28-.88.51-1.08-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.6 7.6 0 0 1 4 0c1.53-1.03 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.28.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48v2.19c0 .21.15.46.55.38A8 8 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>{name}</h3>
            <p>{desc}</p><div class="rmeta"><span>{meta}</span></div></div>
          <div class="rlinks"><a class="btn btn-ghost btn-sm" href="https://github.com/{name}" target="_blank" rel="noopener">GitHub</a></div>
        </article>'''
        for name, desc, meta in C["repos"]
    )

    return "".join([
        head(lang, "lib", root), header(lang, "lib", root),
        f"""<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow">{C['eyebrow']}</p>
      <h1>{C['h1']}</h1>
      <p class="lead" style="max-width:68ch">{C['lead']}</p>
      <p style="margin-top:1.6rem">
        <button class="install" data-copy="{C['install']}" aria-label="{C['install']}">
          <span class="prompt" aria-hidden="true">$</span>
          <span class="cmd">{C['install']}</span>
          <span class="copy-ico" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 3.5v-1a1 1 0 0 0-1-1h-7a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h1"/></svg></span>
        </button>
      </p>
      <div class="hero-meta">
        <span class="chip"><span class="dot"></span>PyPI 0.7.0</span>
        <span class="chip">Python ≥ 3.10</span>
        <span class="chip">31 módulos</span>
        <span class="chip">248 exemplos</span>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{'Arquitetura' if lang == 'pt' else 'Architecture'}</p><h2>{C['stack_h']}</h2></div>
      <div class="stack reveal">
{stack}      </div>
      <div class="note reveal"><span><b>{C['why_bold']}:</b> {C['why']}</span></div>
    </div>
  </section>

  <section class="alt">
    <div class="wrap split-block reveal">
      <div class="code-card">
        <div class="code-head"><span class="fname">inverse_heat.py</span></div>
        {CODE if lang == 'pt' else CODE_EN}
      </div>
      <div>
        <p class="eyebrow">{'Começar' if lang == 'pt' else 'Get started'}</p>
        <h2 style="font-size:clamp(1.5rem,2.8vw,2rem);margin-bottom:1rem">{C['start_h']}</h2>
        <p style="color:var(--text-dim)">{C['start_p']}</p>
        <h3 style="margin:1.8rem 0 .8rem">{C['gains_h']}</h3>
        <ul class="checks">{gains}</ul>
        <p class="section-cta" style="margin-top:1.6rem">{wa_button(lang)}<a class="btn btn-ghost" href="{DOCS}" target="_blank" rel="noopener">{C['docs_btn']} ↗</a></p>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{'Código aberto' if lang == 'pt' else 'Open source'}</p><h2>{C['oss_h']}</h2></div>
        <p>{C['oss_p']}</p>
      </div>
      <div class="grid-2 reveal">{repos}</div>
      <div class="note reveal"><span><b>{C['honest_bold']}:</b> {C['honest']}</span></div>
    </div>
  </section>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, "lib", root),
    ])


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Page: success stories — customer-story format
# ---------------------------------------------------------------------------

SUCCESS = {
    "pt": dict(
        objective="Objetivo",
        results="Principais resultados",
        notproven="O que este caso ainda não prova",
        others="Outros casos",
        back="Casos de sucesso",
        hub_cta="Ver todos os casos de sucesso",
        hub_cta2="Ver os relatórios",
    ),
    "en": dict(
        objective="Objective",
        results="Key results",
        notproven="What this case does not prove yet",
        others="Other cases",
        back="Success stories",
        hub_cta="See every success story",
        hub_cta2="See the reports",
    ),
}

SUCCESS_HOME = {
    "pt": dict(
        eyebrow="Casos de sucesso",
        h="Seis casos, cada número conferido contra uma referência independente.",
        btn="Ver os casos de sucesso",
    ),
    "en": dict(
        eyebrow="Success stories",
        h="Six cases, every number checked against an independent reference.",
        btn="See the success stories",
    ),
}


def _plain(markup: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", markup)


def success_highlights(lang: str, root: str) -> str:
    """The four single-metric cards, shared by the hub and the home page."""
    return "".join(
        f'<a class="cs-hi" href="{root}{url(lang, "caso:" + slug)}">'
        f'<b>{value if lang == "pt" else value_en}</b>'
        f'<span>{desc if lang == "pt" else desc_en}</span>'
        f'<em>{who if lang == "pt" else who_en}</em></a>'
        for slug, value, value_en, _i, desc, desc_en, who, who_en in CS.HIGHLIGHTS
    )


def page_sucessos(lang: str) -> str:
    root = up(lang, "sucessos")
    H = CS.HUB[lang]
    S = SUCCESS[lang]

    cards = ""
    for case in CS.CASES:
        C = case[lang]
        cards += (
            f'<a class="cs-card" href="{root}{url(lang, "caso:" + case["slug"])}">'
            f'<span class="k">{C["eyebrow"]} · {C["evidence"][1]}</span>'
            f'<h3>{C["h1"]}</h3>'
            f'<p>{C["short"]}</p>'
            f'<span class="n">{C["key"]}</span></a>'
        )

    more = "".join(
        f'<div class="cs-row"><span>{t}</span><b>{v}</b></div>'
        for t, v in CS.MORE[lang]
    )

    return "".join([
        head(lang, "sucessos", root), header(lang, "sucessos", root),
        f"""<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow">{H['eyebrow']}</p>
      <h1>{H['h1']}</h1>
      <p class="lead" style="max-width:66ch">{H['lead']}</p>
    </div>
  </section>

  <section class="tight">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{H['hi_k']}</p><h2>{H['highlights_h']}</h2></div>
      <div class="grid-4 reveal">{success_highlights(lang, root)}</div>
    </div>
  </section>

  <section class="alt tight">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{H['cases_k']}</p><h2>{H['cases_h']}</h2></div>
      <div class="grid-3 reveal">{cards}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{H['more_k']}</p><h2>{H['more_h']}</h2></div>
        <p>{H['more_p']}</p>
      </div>
      <div class="cs-rows reveal">{more}</div>

      <h3 style="margin-top:3.6rem">{H['legend_h']}</h3>
      <div class="cs-legend reveal">
        <div><span class="badge ok">{H['legend_val'][0]}</span><p>{H['legend_val'][1]}</p></div>
        <div><span class="badge warn">{H['legend_poc'][0]}</span><p>{H['legend_poc'][1]}</p></div>
      </div>

      <p class="section-cta reveal">
        {wa_button(lang)}
        <a class="btn btn-ghost" href="{root}{url(lang, 'relatorios')}">{H['table_link']} →</a>
      </p>
      <div class="note reveal"><span>{H['cta']}</span></div>
    </div>
  </section>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, "sucessos", root),
    ])


def page_sucesso(lang: str, slug: str) -> str:
    case = next(c for c in CS.CASES if c["slug"] == slug)
    C = case[lang]
    S = SUCCESS[lang]
    page = "caso:" + slug
    root = up(lang, page)

    meta_rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in C["meta"])
    stats = "".join(
        f'<div class="cs-stat"><b>{v}</b><span>{l}</span></div>' for v, l in C["stats"]
    )
    takeaways = "".join(f"<li>{t}</li>" for t in C["takeaways"])

    body = ""
    for sec in C["sections"]:
        paras = "".join(f"<p>{p}</p>" for p in sec["body"])
        figs = "".join(
            f'<figure class="cs-fig"><img src="{root}img/casos/{src}" alt="{_plain(cap)[:110]}" '
            f'loading="lazy" decoding="async" /><figcaption>{cap}</figcaption></figure>'
            for src, cap in sec.get("figs", [])
        )
        body += f'<div class="cs-sec"><h2>{sec["h"]}</h2>{paras}{figs}</div>'

    limits = "".join(f"<p>{p}</p>" for p in C["limits"])
    others = [c for c in CS.CASES if c["slug"] != slug][:2]
    related = "".join(
        f'<a class="cs-card" href="{root}{url(lang, "caso:" + o["slug"])}">'
        f'<span class="k">{o[lang]["eyebrow"]}</span>'
        f'<h3>{o[lang]["h1"]}</h3>'
        f'<span class="n">{o[lang]["key"]}</span></a>'
        for o in others
    )

    return "".join([
        head(lang, page, root), header(lang, page, root),
        f"""<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow"><a href="{root}{url(lang, 'sucessos')}">{S['back']}</a> · {C['crumb']}</p>
      <h1>{C['h1']}</h1>
      <p class="lead" style="max-width:60ch">{C['deck']}</p>
      <p style="margin-top:1.4rem"><span class="badge {C['evidence'][0]}">{C['evidence'][1]}</span></p>
    </div>
  </section>

  <section class="tight">
    <div class="wrap cs">
      <dl class="cs-meta">{meta_rows}</dl>
      <div class="cs-stats">{stats}</div>
      <div class="cs-sec"><h2>{S['objective']}</h2><p>{C['objective']}</p></div>
      <div class="cs-sec"><h2>{S['results']}</h2><ol class="cs-list">{takeaways}</ol></div>
      {body}
      <blockquote class="cs-quote"><p>“{C['quote'][0]}”</p><footer>{C['quote'][1]}</footer></blockquote>
      <aside class="cs-limits"><h2>{S['notproven']}</h2>{limits}</aside>
    </div>
  </section>

  <section class="alt tight">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{S['others']}</p></div>
      <div class="grid-3 reveal">{related}</div>
      <p class="section-cta reveal">
        <a class="btn btn-primary" href="{root}{url(lang, 'sucessos')}">{S['hub_cta']} →</a>
        <a class="btn btn-ghost" href="{root}{url(lang, 'relatorios')}">{S['hub_cta2']} →</a>
      </p>
    </div>
  </section>
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, page, root),
    ])


BUILDERS = {
    "home": page_home,
    "studio": page_studio,
    "erosao": lambda lang: page_segment(lang, "erosao"),
    "trocadores": lambda lang: page_segment(lang, "trocadores"),
    "valvulas": lambda lang: page_segment(lang, "valvulas"),
    "relatorios": page_relatorios,
    "artigos": page_artigos,
    "sucessos": page_sucessos,
    "lib": page_lib,
}

# Old addresses that must keep working: the URL stays, the destination changes.
REDIRECTS = {
    "engineering": {
        "pt": ("/studio/", "Ver o produto"),
        "en": ("/en/studio/", "See the product"),
    },
    "casos-de-uso": {
        "pt": ("/artigos/", "Ver os artigos"),
        "en": ("/en/artigos/", "See the articles"),
    },
    "historia": {
        "pt": ("/#historia", "Ir para o início"),
        "en": ("/en/#historia", "Go to the home page"),
    },
}


def redirect_page(target: str, label: str) -> str:
    """A small page that sends the old URL to its new home, without indexing it twice."""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex" />
<meta http-equiv="refresh" content="0; url={target}" />
<link rel="canonical" href="{target}" />
<title>PINNeAPPle Labs</title>
<style>body{{background:#070a10;color:#eef2f7;font:400 16px/1.6 system-ui,sans-serif;display:grid;place-items:center;height:100vh;margin:0}}a{{color:#f0b32e}}</style>
</head>
<body>
<p>Esta página mudou de lugar. <a href="{target}">{label} →</a></p>
</body>
</html>
"""


def build() -> list[str]:
    written = []
    for page, builder in BUILDERS.items():
        for lang in LANGUAGES:
            rel = url(lang, page)
            out = ROOT / rel / "index.html" if rel else ROOT / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(builder(lang), encoding="utf-8")
            written.append(str(out.relative_to(ROOT)))

    for post in POSTS:
        for lang in LANGUAGES:
            rel = url(lang, f"post:{post['slug']}")
            out = ROOT / rel / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page_post(lang, post["slug"]), encoding="utf-8")
            written.append(str(out.relative_to(ROOT)))

    for case in CS.CASES:
        for lang in LANGUAGES:
            rel = url(lang, "caso:" + case["slug"])
            out = ROOT / rel / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page_sucesso(lang, case["slug"]), encoding="utf-8")
            written.append(str(out.relative_to(ROOT)))

    # The old addresses keep working: same URL, new destination.
    for old, targets in REDIRECTS.items():
        for lang in LANGUAGES:
            target, label = targets[lang]
            rel = "/".join(p for p in (LANGUAGES[lang]["dir"], old) if p)
            out = ROOT / rel / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(redirect_page(target, label), encoding="utf-8")
            written.append(str(out.relative_to(ROOT)))

    return written


def write_sitemap() -> str:
    """Every page in every language, with the hreflang alternates search engines use."""
    entries = []
    for page in PAGES:
        for lang in LANGUAGES:
            alternates = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{LANGUAGES[o]["code"]}" href="{SITE}/{url(o, page)}"/>'
                for o in LANGUAGES
            )
            priority = "1.0" if page == "home" else ("0.7" if page.startswith("post:") else "0.8")
            entries.append(
                f"  <url>\n    <loc>{SITE}/{url(lang, page)}</loc>\n{alternates}\n"
                f"    <priority>{priority}</priority>\n  </url>"
            )
    body = "\n".join(entries)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{body}\n</urlset>\n"
    )
    out = ROOT / "sitemap.xml"
    out.write_text(xml, encoding="utf-8")
    return str(out.relative_to(ROOT))


def main() -> int:
    for path in build():
        print("wrote", path)
    print("wrote", write_sitemap())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
