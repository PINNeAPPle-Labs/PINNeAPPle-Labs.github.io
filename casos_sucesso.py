#!/usr/bin/env python3
"""Content for the success-stories pages (customer-story format).

Pure data: no imports, no HTML. `build.py` renders it with the site shell so the
pages inherit the nav, the footer and the WhatsApp button, and so the two
languages cannot drift apart.

Every number here comes from `PINNeAPPle-casos-de-sucesso/casos-de-sucesso.html`
(November 2026) and from the experiment READMEs. Nothing is rounded up, and each
case carries the paragraph saying what it still does not prove.
"""

HUB = {
    "pt": dict(
        eyebrow="Casos de sucesso",
        h1="Física + IA que prova o que entrega",
        lead=(
            "Seis casos de engenharia, cada número conferido contra uma referência independente: "
            "ensaio publicado, solução exata ou simulação de alta fidelidade. Onde a prova ainda não "
            "existe, a página diz qual é o buraco."
        ),
        hi_k="Destaques",
        highlights_h="Resultados em uma linha",
        cases_k="Casos",
        more_k="Mais",
        cases_h="Os seis casos",
        more_h="Mais resultados já publicados",
        more_p="Casos menores, com a mesma regra: cada um traz a referência usada e o que ele não prova.",
        legend_h="Como ler o nível de evidência",
        legend_val=("Validado", "Comparado com experimento, ensaio publicado ou solução exata independente."),
        legend_poc=("Prova de conceito", "Funciona ponta a ponta, mas ainda sem dado real de cliente ou sem referência externa para todos os campos."),
        table_link="Ver as validações técnicas completas",
        cta=(
            "Todo caso começa pela mesma pergunta: contra o que este resultado vai ser conferido? "
            "Se a resposta não existe, o primeiro entregável é a referência."
        ),
    ),
    "en": dict(
        eyebrow="Success stories",
        h1="Physics + AI that proves what it delivers",
        lead=(
            "Six engineering cases, every number checked against an independent reference: a published "
            "experiment, an exact solution or a high-fidelity simulation. Where the proof does not exist "
            "yet, the page names the gap."
        ),
        hi_k="Highlights",
        highlights_h="Results in one line",
        cases_k="Cases",
        more_k="More",
        cases_h="The six cases",
        more_h="More published results",
        more_p="Smaller cases, same rule: each one carries the reference it used and what it does not prove.",
        legend_h="How to read the evidence level",
        legend_val=("Validated", "Compared with an experiment, a published test or an independent exact solution."),
        legend_poc=("Proof of concept", "Works end to end, but still without client data or without an external reference for every field."),
        table_link="See the full technical validations",
        cta=(
            "Every case starts with the same question: what will this result be checked against? "
            "If there is no answer, the first deliverable is the reference."
        ),
    ),
}

# The four single-metric cards on the hub, and the small rows under them.
HIGHLIGHTS = [
    ("dissipador-227-mil", "227.059×", "227,059×", 0,
     "mais rápido que uma simulação 3D real, com 4,46% de erro médio de temperatura.",
     "faster than a real 3D simulation, with 4.46% mean temperature error.",
     "Eletrônica de potência", "Power electronics"),
    ("erosao-tubulacao", "1,05–1,49×", "1.05–1.49×", 1,
     "da erosão medida em ensaio publicado, dentro do critério de fator 2.",
     "of the erosion measured in a published test, inside the factor-2 criterion.",
     "Óleo e gás", "Oil and gas"),
    ("oceano-sete-dias", "0,93 °C", "0.93 °C", 2,
     "de erro em 7 dias, contra 1,06 °C da persistência, em 43 anos de satélite.",
     "error at 7 days, against 1.06 °C for persistence, over 43 years of satellite data.",
     "Clima e offshore", "Climate and offshore"),
    ("camera-compacta", "768×", "768×", 3,
     "é o custo estimado do solve direto contra a física óptica; 98% do ótimo com 12 solves caros.",
     "is the estimated cost of the direct solve against physical optics; 98% of the optimum with 12 expensive solves.",
     "Antenas e RF", "Antennas and RF"),
]

MORE = {
    "pt": [
        ("Conversor de malha remove todos os defeitos de uma exportação legada", "15→0 · 10→0 · 20→0"),
        ("PIV por software recupera a estrutura de um vórtice", "3,94% de erro"),
        ("Modelo roda–solo com restrições físicas", "45× menos erro na tração"),
        ("Biblioteca de PINNs conferida contra solução exata", "4,5·10⁻³ de erro L2"),
    ],
    "en": [
        ("Mesh converter removes every defect from a legacy export", "15→0 · 10→0 · 20→0"),
        ("Software PIV recovers the structure of a vortex", "3.94% error"),
        ("Wheel–soil model with physical constraints", "45× less traction error"),
        ("PINN library checked against exact solutions", "4.5·10⁻³ L2 error"),
    ],
}

CASES = [
    # ---------------------------------------------------------------- erosão
    dict(
        slug="erosao-tubulacao",
        pt=dict(
            crumb="Caso · óleo e gás",
            eyebrow="Óleo, gás, mineração e transporte pneumático",
            h1="Onde e quando a tubulação vai furar",
            deck="Erosão por areia em curva de 90°: CFD de verdade, validado contra ensaio publicado, e um modelo de IA que responde em milissegundos.",
            evidence=("ok", "Validado"),
            short="Erosão por areia em curva de 90°, com campanha de CFD e substituto de IA",
            key="1,05–1,49×",
            meta=[
                ("Aplicação", "Curva de 90° em linha de transporte de sólidos — plataforma PINNeAPPle-CFD"),
                ("Setor", "Óleo e gás, mineração, transporte pneumático"),
                ("Tema", "CFD, substituto de IA, verificação independente"),
                ("Pilha", "OpenFOAM (escoamento + partículas), modelo de erosão DNV RP-O501, PINNeAPPle"),
                ("Referência", "Ensaio publicado de Vieira et al. (2016): ar com areia de 150 µm"),
            ],
            stats=[
                ("1,05–1,49×", "erosão simulada ÷ medida nos três ensaios (critério de aceitação: fator 2)"),
                ("1,0%", "erro da IA na perda de carga, em casos fora do treino"),
                ("10,6%", "erro da IA na taxa de erosão (19,7% fora da faixa de treino)"),
                ("US$ 0,06", "custo de CPU de uma campanha: 32 simulações em 23 minutos"),
            ],
            objective=(
                "Partículas sólidas desgastam curvas e conexões até a parede furar. As fórmulas de mão usadas na "
                "indústria para estimar quanto e onde a tubulação vai desgastar podem errar por ordens de grandeza, "
                "e um estudo de CFD tradicional leva semanas e exige um especialista dedicado. O objetivo do caso "
                "foi responder a duas perguntas com o mesmo artefato: onde a parede vai furar primeiro, e com que "
                "frequência se pode refazer essa conta quando a vazão muda."
            ),
            takeaways=[
                "<b>A simulação ficou entre 1,05× e 1,49× da erosão medida em laboratório</b>, dentro do critério de aceitação de fator 2. A fórmula de mão, aplicada ao mesmo caso, ficou cerca de 100× abaixo do medido.",
                "<b>A IA treinada sobre a campanha reproduz a perda de carga com 1,0% de erro</b> em configurações que nunca viu, e a taxa de erosão com 10,6% dentro da faixa de treino — 19,7% fora dela.",
                "<b>Uma campanha completa custa 1,9 CPU-hora</b>: 32 simulações em 23 minutos, cerca de US$ 0,06. É o que torna viável refazer o mapa a cada mudança de vazão.",
            ],
            sections=[
                dict(h="O problema: a fórmula de mão não é conservadora, é imprevisível", body=[
                    "O desgaste por erosão é dominado pelo ângulo de impacto e pela velocidade local das partículas. Numa curva de 90°, o pico fica na parede externa, logo depois da entrada — uma região de poucos centímetros que concentra a maior parte do dano. Estimativas de mão tratam a curva como um todo e perdem justamente essa concentração.",
                    "O padrão da indústria para esse tipo de cálculo é a DNV RP-O501, que exige um campo de escoamento resolvido. Ou seja: para saber onde a parede vai furar, é preciso resolver o escoamento, não estimá-lo.",
                ], figs=[
                    ("cfd04_validacao_vieira.png", "Taxa máxima de erosão: medida em laboratório × simulada (modelos DNV e E/CRC) × fórmula de mão. Escala logarítmica — é a distância de três ordens de grandeza que a fórmula de mão perde."),
                    ("cfd04_mapa_erosao.png", "Mapa de erosão na parede calculado pela simulação. O pico fica na parede externa, logo após a entrada da curva — a região que a estimativa de mão não resolve."),
                ]),
                dict(h="Um fluxo guiado, do problema ao mapa de erosão", body=[
                    "A plataforma descreve o problema em passos — geometria (peça padrão ou CAD do cliente em STL, STEP ou IGES), nível de malha, fluido e partículas —, gera a malha, roda o OpenFOAM com transporte de partículas e modelo de erosão, executa a campanha e treina um modelo de IA sobre os resultados.",
                    "Cada número entregue sai acompanhado de um mapa de provas: o que foi simulado, o que foi aprendido, contra o que foi conferido e o que ainda está pendente.",
                ]),
                dict(h="O substituto, conferido contra a simulação e não contra si mesmo", body=[
                    "O modelo de IA é treinado sobre a campanha e depois testado em configurações que não estavam nela. O painel abaixo mostra os casos de teste com intervalo de confiança de 95%; em laranja, os que caem fora da faixa de treino, onde o erro sobe de 10,6% para 19,7%.",
                ], figs=[
                    ("cfd04_paridade_ia_cfd.png", "Modelo de IA × simulação completa, em casos que a IA nunca viu, com intervalo de confiança de 95%. Em laranja, os casos fora da faixa de treino."),
                ]),
            ],
            quote=(
                "As constantes dos modelos de erosão vêm de fonte secundária, por isso a plataforma marca a erosão como PRELIMINAR. O que está provado é a comparação: a simulação fica dentro do fator 2 do ensaio; a fórmula de mão, não.",
                "Registro do experimento · PINNeAPPle-CFD",
            ),
            limits=[
                "As constantes dos modelos de erosão vêm de fonte secundária. Por isso a plataforma marca o resultado de erosão como <b>PRELIMINAR</b>, e não como valor de projeto.",
                "A campanha usou malha grossa: a perda de carga converge, mas a incerteza de malha na malha fina ficou em <b>GCI de 6,8–12,6%</b> contra a meta de 5%, e a erosão só convergiu em um dos três pontos estudados. A campanha em malha fina está em execução.",
                "A validação cobre <b>ar com areia de 150 µm em uma curva de 90°</b>. Outros fluidos, granulometrias e geometrias pedem validação própria — o mapa de provas marca cada uma como pendente até que ela exista.",
            ],
        ),
        en=dict(
            crumb="Case · oil and gas",
            eyebrow="Oil, gas, mining and pneumatic conveying",
            h1="Where the pipeline will fail, and when",
            deck="Sand erosion in a 90° bend: real CFD, validated against a published experiment, plus an AI model that answers in milliseconds.",
            evidence=("ok", "Validated"),
            short="Sand erosion in a 90° bend, with a CFD campaign and a surrogate model",
            key="1.05–1.49×",
            meta=[
                ("Application", "90° bend in a solids conveying line — PINNeAPPle-CFD platform"),
                ("Sector", "Oil and gas, mining, pneumatic conveying"),
                ("Topic", "CFD, surrogate model, independent verification"),
                ("Stack", "OpenFOAM (flow + particles), DNV RP-O501 erosion model, PINNeAPPle"),
                ("Reference", "Published experiment, Vieira et al. (2016): air with 150 µm sand"),
            ],
            stats=[
                ("1.05–1.49×", "simulated ÷ measured erosion across the three tests (acceptance criterion: factor 2)"),
                ("1.0%", "AI error on pressure drop, on cases outside training"),
                ("10.6%", "AI error on erosion rate (19.7% outside the training range)"),
                ("US$0.06", "CPU cost of one campaign: 32 simulations in 23 minutes"),
            ],
            objective=(
                "Solid particles wear bends and fittings until the wall fails. The hand formulas the industry uses to "
                "estimate how much and where a pipeline will wear can be off by orders of magnitude, and a traditional "
                "CFD study takes weeks and needs a dedicated specialist. This case set out to answer two questions with "
                "the same artefact: where the wall fails first, and how often that answer can be recomputed when the "
                "flow rate changes."
            ),
            takeaways=[
                "<b>The simulation landed between 1.05× and 1.49× the erosion measured in the lab</b>, inside the factor-2 acceptance criterion. The hand formula, applied to the same case, came out about 100× below the measurement.",
                "<b>The AI trained on the campaign reproduces pressure drop to 1.0% error</b> on configurations it never saw, and erosion rate to 10.6% inside the training range — 19.7% outside it.",
                "<b>A full campaign costs 1.9 CPU-hours</b>: 32 simulations in 23 minutes, about US$0.06. That is what makes it viable to redo the map every time the flow rate changes.",
            ],
            sections=[
                dict(h="The problem: the hand formula is not conservative, it is unpredictable", body=[
                    "Erosion damage is governed by impact angle and by the local particle velocity. In a 90° bend the peak sits on the outer wall, just past the inlet — a region a few centimetres wide that carries most of the damage. Hand estimates treat the bend as a whole and lose exactly that concentration.",
                    "The industry standard for this kind of calculation is DNV RP-O501, which requires a resolved flow field. In other words: to know where the wall will fail, you have to solve the flow, not estimate it.",
                ], figs=[
                    ("cfd04_validacao_vieira.png", "Peak erosion rate: measured in the lab × simulated (DNV and E/CRC models) × hand formula. Log scale — this is the three orders of magnitude the hand formula loses."),
                    ("cfd04_mapa_erosao.png", "Wall erosion map computed by the simulation. The peak sits on the outer wall just past the bend inlet — the region a hand estimate cannot resolve."),
                ]),
                dict(h="A guided flow, from the problem to the erosion map", body=[
                    "The platform takes the problem in steps — geometry (a standard part or the client's CAD in STL, STEP or IGES), mesh level, fluid and particles — builds the mesh, runs OpenFOAM with particle tracking and an erosion model, runs the campaign and trains a model on the results.",
                    "Every number ships with an evidence map: what was simulated, what was learned, what it was checked against, and what is still pending.",
                ]),
                dict(h="The surrogate, checked against the simulation and not against itself", body=[
                    "The AI model is trained on the campaign and then tested on configurations that were not in it. The panel below shows the test cases with a 95% confidence interval; in orange, the ones outside the training range, where the error rises from 10.6% to 19.7%.",
                ], figs=[
                    ("cfd04_paridade_ia_cfd.png", "AI model × full simulation, on cases the AI never saw, with a 95% confidence interval. In orange, cases outside the training range."),
                ]),
            ],
            quote=(
                "The erosion model constants come from a secondary source, so the platform flags erosion as PRELIMINARY. What is proven is the comparison: the simulation lands inside the experiment's factor 2; the hand formula does not.",
                "Experiment record · PINNeAPPle-CFD",
            ),
            limits=[
                "The erosion model constants come from a secondary source. That is why the platform flags the erosion result as <b>PRELIMINARY</b> rather than a design value.",
                "The campaign used a coarse mesh: pressure drop converges, but mesh uncertainty on the fine mesh came out at <b>GCI 6.8–12.6%</b> against a 5% target, and erosion only converged at one of the three points studied. The fine-mesh campaign is running.",
                "Validation covers <b>air with 150 µm sand in one 90° bend</b>. Other fluids, particle sizes and geometries need their own validation — the evidence map marks each one pending until it exists.",
            ],
        ),
    ),
    # ------------------------------------------------------------ dissipador
    dict(
        slug="dissipador-227-mil",
        pt=dict(
            crumb="Caso · eletrônica de potência",
            eyebrow="Eletrônica de potência e otimização térmica",
            h1="Substituto treinado responde 227 mil vezes mais rápido que a simulação 3D",
            deck="Sete dissipadores reais, cada previsão conferida contra uma simulação de elementos finitos de verdade — nunca contra outro modelo de IA.",
            evidence=("ok", "Validado"),
            short="Substituto térmico conferido contra FEA 3D real, design por design",
            key="227.059×",
            meta=[
                ("Aplicação", "Previsão de temperatura de junção em geometrias de dissipador"),
                ("Setor", "Eletrônica de potência, data centers, automotivo"),
                ("Tema", "Substituto neural, verificação contra simulação de alta fidelidade"),
                ("Pilha", "PINNeAPPle, FEniCS/dolfinx, gmsh"),
                ("Referência", "Solução de elementos finitos 3D, mesma malha usada em produção"),
            ],
            stats=[
                ("227.059×", "mais rápido que a simulação 3D real, em média (57 mil× a 399 mil× por design)"),
                ("4,46%", "erro médio de temperatura contra a FEA 3D real"),
                ("7,35%", "pior caso entre os sete designs, dentro do limite de 10%"),
                ("3×", "rodadas reais em dias diferentes, com o mesmo erro de temperatura"),
            ],
            objective=(
                "Otimizar a geometria de um dissipador exige rodar dezenas de simulações térmicas 3D, cada uma levando "
                "segundos. Isso inviabiliza uma varredura de design interativa ou um otimizador que precise avaliar "
                "centenas de candidatos. Um substituto que responda em microssegundos resolve o custo — desde que cada "
                "previsão dele seja conferida contra uma simulação de verdade, e não contra o próprio modelo que o treinou."
            ),
            takeaways=[
                "<b>Em sete geometrias significativamente diferentes</b> — aletas densas, esparsas, altas, curtas, com potência alta e baixa — o substituto respondeu em microssegundos onde a simulação real levou de 0,6 a 5,9 segundos.",
                "<b>O erro de temperatura ficou dentro de 10% em todos os casos</b>: média de 4,46%, pior caso de 7,35%.",
                "<b>O erro é reprodutível.</b> Três rodadas em dias diferentes deram exatamente o mesmo erro de temperatura; só o fator de aceleração muda, porque ele depende da carga da máquina no momento do teste.",
            ],
            sections=[
                dict(h="Sete geometrias, sete simulações 3D de verdade", body=[
                    "O conjunto de teste foi desenhado para conter mudanças que quebram substitutos treinados em variações pequenas: densidade de aletas, altura, espessura de base e nível de potência mudam ao mesmo tempo entre os sete designs.",
                    "Cada ponto da figura abaixo é uma previsão do substituto medida contra uma solução de elementos finitos resolvida na hora — não contra um resultado guardado de treino.",
                ], figs=[
                    ("surrogate_speed_rerun.jpg", "Concordância de temperatura (esquerda) e fator de aceleração por design (direita), rodada real de 2026-10-02, com FEniCS e gmsh."),
                ]),
                dict(h="Por que a referência é a FEA, não o próprio modelo", body=[
                    "Um substituto validado contra o conjunto de validação do seu próprio treino mede apenas o quanto ele é consistente consigo mesmo. É por isso que os erros de 0,01% que aparecem em muitos relatórios de surrogate não sobrevivem à primeira geometria nova.",
                    "Aqui a referência é externa e independente: um solver de elementos finitos, com malha gerada por gmsh, resolvido para cada um dos sete designs no momento do teste.",
                ]),
                dict(h="O que o fator de aceleração mede — e o que ele não mede", body=[
                    "Aceleração é uma razão entre dois tempos de relógio, e o tempo da simulação de referência depende da máquina. Por isso o fator varia entre 57 mil× e 399 mil× entre designs e entre execuções, enquanto o erro de temperatura é idêntico nas três rodadas.",
                    "A leitura correta é: a previsão é determinística, o custo de referência não é.",
                ]),
            ],
            quote=(
                "A previsão de temperatura é determinística — o mesmo erro nas três rodadas. Só o fator de aceleração muda com a carga da máquina no momento do teste.",
                "Registro do experimento · substituto térmico",
            ),
            limits=[
                "É uma <b>demonstração curada de capacidade</b>, não o produto interno completo (<code>heatsink_design_ai</code>) exposto como ferramenta genérica.",
                "Sete designs cobrem a família de dissipadores aletados estudada. Geometrias fora dessa família — aletas em pino, microcanais, convecção forçada em regime turbulento — não foram testadas.",
                "O erro de 7,35% é o pior caso medido, não um limite garantido para qualquer geometria.",
            ],
        ),
        en=dict(
            crumb="Case · power electronics",
            eyebrow="Power electronics and thermal optimization",
            h1="A trained surrogate answers 227,000 times faster than the 3D simulation",
            deck="Seven real heat sinks, every prediction checked against a real finite-element simulation — never against another AI model.",
            evidence=("ok", "Validated"),
            short="A thermal surrogate checked against real 3D FEA, design by design",
            key="227,059×",
            meta=[
                ("Application", "Junction temperature prediction across heat-sink geometries"),
                ("Sector", "Power electronics, data centers, automotive"),
                ("Topic", "Neural surrogate, verification against high-fidelity simulation"),
                ("Stack", "PINNeAPPle, FEniCS/dolfinx, gmsh"),
                ("Reference", "3D finite-element solution, same mesh used in production"),
            ],
            stats=[
                ("227,059×", "faster than the real 3D simulation, on average (57,000× to 399,000× per design)"),
                ("4.46%", "mean temperature error against the real 3D FEA"),
                ("7.35%", "worst case across the seven designs, inside the 10% limit"),
                ("3×", "real runs on different days, with the same temperature error"),
            ],
            objective=(
                "Optimising a heat-sink geometry means running dozens of 3D thermal simulations, each taking seconds. "
                "That rules out an interactive design sweep or an optimiser that has to evaluate hundreds of candidates. "
                "A surrogate that answers in microseconds solves the cost — provided every prediction it makes is checked "
                "against a real simulation, and not against the model that trained it."
            ),
            takeaways=[
                "<b>Across seven significantly different geometries</b> — dense, sparse, tall and short fins, at high and low power — the surrogate answered in microseconds where the real simulation took 0.6 to 5.9 seconds.",
                "<b>Temperature error stayed inside 10% in every case</b>: 4.46% mean, 7.35% worst case.",
                "<b>The error is reproducible.</b> Three runs on different days gave exactly the same temperature error; only the speed-up factor moves, because it depends on machine load at test time.",
            ],
            sections=[
                dict(h="Seven geometries, seven real 3D simulations", body=[
                    "The test set was built to contain the changes that break surrogates trained on small variations: fin density, height, base thickness and power level all move together across the seven designs.",
                    "Every point in the figure below is a surrogate prediction measured against a finite-element solution solved on the spot — not against a stored training result.",
                ], figs=[
                    ("surrogate_speed_rerun.jpg", "Temperature agreement (left) and speed-up per design (right), real run of 2026-10-02, with FEniCS and gmsh."),
                ]),
                dict(h="Why the reference is FEA, not the model itself", body=[
                    "A surrogate validated against its own training validation set only measures how consistent it is with itself. That is why the 0.01% errors in many surrogate reports do not survive the first new geometry.",
                    "Here the reference is external and independent: a finite-element solver, with a mesh built by gmsh, solved for each of the seven designs at test time.",
                ]),
                dict(h="What the speed-up factor measures — and what it does not", body=[
                    "Speed-up is a ratio between two wall-clock times, and the reference simulation time depends on the machine. That is why the factor ranges from 57,000× to 399,000× across designs and runs, while the temperature error is identical across all three.",
                    "The correct reading is: the prediction is deterministic, the reference cost is not.",
                ]),
            ],
            quote=(
                "The temperature prediction is deterministic — the same error across three runs. Only the speed-up factor moves with machine load at test time.",
                "Experiment record · thermal surrogate",
            ),
            limits=[
                "This is a <b>curated capability demonstration</b>, not the full internal product (<code>heatsink_design_ai</code>) exposed as a general tool.",
                "Seven designs cover the finned heat-sink family studied. Geometries outside it — pin fins, microchannels, turbulent forced convection — were not tested.",
                "The 7.35% error is the worst case measured, not a guaranteed bound for any geometry.",
            ],
        ),
    ),
    # ---------------------------------------------------------------- oceano
    dict(
        slug="oceano-sete-dias",
        pt=dict(
            crumb="Caso · clima e offshore",
            eyebrow="Pesca, clima, energia offshore e seguros",
            h1="Sete dias de antecedência para a temperatura do mar",
            deck="Quarenta e três anos de satélite NOAA na Confluência Brasil–Malvinas, com incerteza calibrada e comparação contra as referências que a operação já usa.",
            evidence=("ok", "Validado"),
            short="Previsão de temperatura da superfície do mar em 1 a 7 dias, contra persistência",
            key="0,93 °C",
            meta=[
                ("Aplicação", "Previsão de temperatura da superfície do mar em horizontes de 1 a 7 dias"),
                ("Setor", "Pesca, meteorologia, energia offshore, seguros"),
                ("Tema", "Aprendizado profundo, operador neural, incerteza conformal"),
                ("Dados", "NOAA OISST 1982–2024, recorte da Confluência Brasil–Malvinas"),
                ("Teste", "2018–2024, período nunca usado no treino"),
            ],
            stats=[
                ("0,93 °C", "erro em 7 dias, contra 1,06 °C da persistência (−12%)"),
                ("0,74", "correlação de anomalia em 7 dias (persistência: 0,69)"),
                ("4/4", "estações do ano em que o modelo vence a persistência"),
                ("92–95%", "cobertura real dos intervalos de confiança nominais de 90–95%"),
            ],
            objective=(
                "A temperatura da superfície do mar move a pesca, a previsão de tempo e as operações offshore. Na "
                "Confluência Brasil–Malvinas, uma das regiões mais turbulentas do Atlântico Sul, bater a persistência — "
                "a previsão ingênua de que amanhã será igual a hoje — já é difícil. O caso mede se um modelo aprendido "
                "consegue essa vantagem de forma estável, e se a incerteza que ele declara é honesta."
            ),
            takeaways=[
                "<b>O modelo vence todas as referências em todos os horizontes de 1 a 7 dias</b> e em todas as estações do ano: 0,93 °C de erro em 7 dias contra 1,06 °C da persistência.",
                "<b>O ganho não vem de acertar a média</b>: a correlação de anomalia em 7 dias sobe de 0,69 para 0,74, o que indica que o modelo captura estrutura, não só o nível.",
                "<b>A incerteza declarada é verificada.</b> Intervalos nominais de 90% e 95% cobrem 92–95% dos casos reais no período de teste.",
            ],
            sections=[
                dict(h="A referência mais difícil de bater não é a climatologia", body=[
                    "Em previsão oceânica de curto prazo, persistência e persistência amortecida são baselines fortes: a inércia térmica da superfície do mar é alta, e um modelo que apenas repete o último campo acerta muito. Climatologia, por outro lado, é fácil de bater e por isso engana.",
                    "O caso compara os quatro: persistência, persistência amortecida, climatologia e o modelo aprendido — nos mesmos horizontes, no mesmo recorte e no mesmo período de teste.",
                ]),
                dict(h="Quarenta e três anos de satélite como único dado de treino", body=[
                    "Não há dado sintético nem reanálise no treino: são observações de satélite NOAA OISST de 1982 a 2024. O período de 2018 a 2024 foi separado antes do treino e nunca participou dele.",
                    "Ensembles de redes convolucionais e de operador neural (FNO) foram treinados em paralelo, para que a comparação não dependesse de uma única arquitetura ter dado sorte.",
                ]),
                dict(h="Incerteza que se pode checar", body=[
                    "Intervalos de confiança conformais foram calculados sobre as previsões e depois medidos no período de teste: um intervalo nominal de 90% deve conter o valor observado em 90% dos casos. A cobertura real ficou entre 92% e 95% para os dois níveis, o que significa que o modelo não está subdeclarando a própria incerteza.",
                ]),
            ],
            quote=(
                "O ganho é real, mas moderado: cerca de 12% em 7 dias. É a diferença entre uma previsão que a operação pode usar como segunda opinião e uma que ela pode usar como única.",
                "Registro do experimento · previsão oceânica",
            ),
            limits=[
                "A previsão em 7 dias <b>suaviza estruturas finas</b> — vórtices pequenos desaparecem antes do que na observação.",
                "A região estudada é uma só. Outras áreas pedem novo treino e novo teste; a transferência entre bacias não foi medida.",
                "É temperatura de superfície. O caso não diz nada sobre estrutura vertical da coluna d'água.",
            ],
        ),
        en=dict(
            crumb="Case · climate and offshore",
            eyebrow="Fisheries, climate, offshore energy and insurance",
            h1="Seven days of lead time for sea surface temperature",
            deck="Forty-three years of NOAA satellite data over the Brazil–Malvinas Confluence, with calibrated uncertainty and a comparison against the baselines operations already use.",
            evidence=("ok", "Validated"),
            short="Sea surface temperature forecast at 1 to 7 days, against persistence",
            key="0.93 °C",
            meta=[
                ("Application", "Sea surface temperature forecast at 1 to 7 day horizons"),
                ("Sector", "Fisheries, weather, offshore energy, insurance"),
                ("Topic", "Deep learning, neural operator, conformal uncertainty"),
                ("Data", "NOAA OISST 1982–2024, Brazil–Malvinas Confluence region"),
                ("Test", "2018–2024, a period never used in training"),
            ],
            stats=[
                ("0.93 °C", "error at 7 days, against 1.06 °C for persistence (−12%)"),
                ("0.74", "anomaly correlation at 7 days (persistence: 0.69)"),
                ("4/4", "seasons in which the model beats persistence"),
                ("92–95%", "actual coverage of the nominal 90–95% confidence intervals"),
            ],
            objective=(
                "Sea surface temperature drives fisheries, weather forecasting and offshore operations. In the "
                "Brazil–Malvinas Confluence, one of the most turbulent regions of the South Atlantic, beating persistence — "
                "the naive forecast that tomorrow equals today — is already hard. This case measures whether a learned "
                "model holds that advantage consistently, and whether the uncertainty it declares is honest."
            ),
            takeaways=[
                "<b>The model beats every baseline at every horizon from 1 to 7 days</b> and in every season: 0.93 °C error at 7 days against 1.06 °C for persistence.",
                "<b>The gain is not in getting the mean right</b>: 7-day anomaly correlation rises from 0.69 to 0.74, which means the model captures structure, not just the level.",
                "<b>The declared uncertainty is verified.</b> Nominal 90% and 95% intervals cover 92–95% of real cases over the test period.",
            ],
            sections=[
                dict(h="The hardest baseline to beat is not climatology", body=[
                    "In short-range ocean forecasting, persistence and damped persistence are strong baselines: sea surface thermal inertia is high, and a model that just repeats the last field scores well. Climatology, on the other hand, is easy to beat and therefore misleading.",
                    "The case compares all four: persistence, damped persistence, climatology and the learned model — same horizons, same region, same test period.",
                ]),
                dict(h="Forty-three years of satellite data as the only training input", body=[
                    "There is no synthetic data and no reanalysis in training: these are NOAA OISST satellite observations from 1982 to 2024. The 2018–2024 period was set aside before training and never took part in it.",
                    "Convolutional and neural-operator (FNO) ensembles were trained in parallel, so the comparison did not depend on one architecture getting lucky.",
                ]),
                dict(h="Uncertainty you can check", body=[
                    "Conformal confidence intervals were computed on the forecasts and then measured on the test period: a nominal 90% interval should contain the observed value in 90% of cases. Actual coverage came out between 92% and 95% for both levels, which means the model is not understating its own uncertainty.",
                ]),
            ],
            quote=(
                "The gain is real but moderate: about 12% at 7 days. That is the difference between a forecast operations can use as a second opinion and one they can use as the only one.",
                "Experiment record · ocean forecasting",
            ),
            limits=[
                "The 7-day forecast <b>smooths fine structure</b> — small vortices disappear earlier than in the observation.",
                "The region studied is a single one. Other areas need new training and new testing; transfer between basins was not measured.",
                "This is surface temperature. The case says nothing about the vertical structure of the water column.",
            ],
        ),
    ),
    # ---------------------------------------------------------------- gêmeo
    dict(
        slug="gemeo-canal-termico",
        pt=dict(
            crumb="Caso · processos térmicos",
            eyebrow="Processos térmicos e resfriamento industrial",
            h1="Um gêmeo digital que se corrige com seis sensores esparsos",
            deck="Quatro famílias de IA aprendem a dinâmica de um canal com aquecedor e vazão variáveis; um filtro de Kalman por ensemble mantém a previsão na curva quando a planta muda.",
            evidence=("poc", "Prova de conceito"),
            short="Gêmeo de um canal térmico com assimilação de sensores em tempo real",
            key="+23%",
            meta=[
                ("Aplicação", "Gêmeo digital de processo térmico com correção por sensores"),
                ("Setor", "Resfriamento industrial, processos térmicos, energia"),
                ("Tema", "Operador neural, autoencoder, assimilação de dados (EnKF)"),
                ("Pilha", "PINNeAPPle, solver Navier–Stokes + energia, FNO, DeepONet, POD"),
                ("Referência", "Solução numérica do canal 2D laminar com aquecedor"),
            ],
            stats=[
                ("12%", "erro relativo na temperatura em trajetórias de controle inéditas (FNO)"),
                ("22–32×", "mais rápido que a simulação de referência"),
                ("+23%", "de precisão ao assimilar 6 sensores esparsos com EnKF"),
                ("5,3%", "erro relativo na velocidade longitudinal em trajetórias inéditas"),
            ],
            objective=(
                "Um gêmeo digital de processo precisa responder mais rápido do que a planta e continuar certo quando o "
                "operador muda vazão e potência de formas que o modelo nunca viu. Simulação completa é lenta demais para "
                "acompanhar a operação, e um modelo puramente aprendido erra justamente quando a entrada sai do padrão. "
                "O caso mede as duas metades do problema: a velocidade do substituto e a capacidade de corrigi-lo com "
                "poucos sensores."
            ),
            takeaways=[
                "<b>A IA acompanha a temperatura máxima quase sobre a curva da simulação</b> em sinais de controle que não estavam no treino, e roda dezenas de vezes mais rápido.",
                "<b>Seis sensores esparsos corrigem a deriva.</b> O EnKF melhora a precisão em 23% em relação à previsão pura — é o que separa um vídeo do processo de um gêmeo.",
                "<b>A arquitetura é o resultado</b>, não o número: quatro famílias de modelo foram comparadas nas mesmas trajetórias, para que a escolha não dependesse de uma só ter funcionado.",
            ],
            sections=[
                dict(h="Entradas que o modelo nunca viu", body=[
                    "Treinar em degraus e testar em degraus é o erro que produz gêmeos digitais que funcionam na demonstração e falham na planta. As trajetórias de teste aqui são chirp, dente de serra e passeio aleatório em vazão e potência — nenhuma delas aparece no treino.",
                    "O FNO foi o melhor dos quatro nas trajetórias inéditas, com 12% de erro relativo na temperatura e 5,3% na velocidade longitudinal.",
                ]),
                dict(h="Corrigir com poucos sensores, não medir tudo", body=[
                    "Medir o campo inteiro é o que a simulação já faz. O valor do gêmeo está em manter a estimativa certa com instrumentação esparsa — seis sensores no caso. O filtro de Kalman por ensemble assimila essas leituras e corrige a previsão latente.",
                ], figs=[
                    ("canal_enkf.png", "Assimilação de sensores: previsão pura (tracejado), com correção latente (amarelo) e com EnKF (verde) contra a simulação de referência (branco)."),
                ]),
            ],
            quote=(
                "É um canal 2D laminar sintético, não uma planta. Serve como demonstração da arquitetura de gêmeo digital, não como número de projeto.",
                "Registro do experimento · gêmeo térmico",
            ),
            limits=[
                "O objeto é um <b>canal 2D laminar sintético</b> com aquecedor e vazão variáveis. Não é uma planta industrial, nem geometria de cliente.",
                "A pressão é o campo mais difícil: erro de 27%. Temperatura e velocidade convergem; pressão ainda não.",
                "O estudo de malha da simulação de referência tem incerteza alta, com <b>GCI ≈ 50%</b>. O erro do substituto é medido contra uma referência que carrega essa incerteza.",
            ],
        ),
        en=dict(
            crumb="Case · thermal processes",
            eyebrow="Thermal processes and industrial cooling",
            h1="A digital twin that corrects itself with six sparse sensors",
            deck="Four AI families learn the dynamics of a channel with a heater and varying flow; an ensemble Kalman filter keeps the prediction on the curve when the plant changes.",
            evidence=("poc", "Proof of concept"),
            short="A thermal channel twin with real-time sensor assimilation",
            key="+23%",
            meta=[
                ("Application", "Digital twin of a thermal process, corrected by sensors"),
                ("Sector", "Industrial cooling, thermal processes, energy"),
                ("Topic", "Neural operator, autoencoder, data assimilation (EnKF)"),
                ("Stack", "PINNeAPPle, Navier–Stokes + energy solver, FNO, DeepONet, POD"),
                ("Reference", "Numerical solution of the 2D laminar channel with a heater"),
            ],
            stats=[
                ("12%", "relative temperature error on unseen control trajectories (FNO)"),
                ("22–32×", "faster than the reference simulation"),
                ("+23%", "accuracy from assimilating 6 sparse sensors with EnKF"),
                ("5.3%", "relative error on streamwise velocity on unseen trajectories"),
            ],
            objective=(
                "A process digital twin has to answer faster than the plant and stay right when the operator changes "
                "flow rate and power in ways the model has never seen. A full simulation is too slow to follow the "
                "operation, and a purely learned model fails exactly when the input leaves the pattern. This case "
                "measures both halves of the problem: the surrogate's speed and the ability to correct it with a few sensors."
            ),
            takeaways=[
                "<b>The AI tracks peak temperature almost on top of the simulation curve</b> for control signals that were not in training, and runs tens of times faster.",
                "<b>Six sparse sensors correct the drift.</b> EnKF improves accuracy by 23% over the raw prediction — that is what separates a video of the process from a twin.",
                "<b>The architecture is the result</b>, not the number: four model families were compared on the same trajectories, so the choice did not depend on one of them working.",
            ],
            sections=[
                dict(h="Inputs the model has never seen", body=[
                    "Training on steps and testing on steps is the mistake that produces digital twins which work in the demo and fail on the plant. The test trajectories here are chirp, sawtooth and random walk in flow rate and power — none of them appears in training.",
                    "FNO was the best of the four on unseen trajectories, with 12% relative error on temperature and 5.3% on streamwise velocity.",
                ]),
                dict(h="Correct with a few sensors, not by measuring everything", body=[
                    "Measuring the whole field is what the simulation already does. The twin's value is keeping the estimate right with sparse instrumentation — six sensors in this case. The ensemble Kalman filter assimilates those readings and corrects the latent prediction.",
                ], figs=[
                    ("canal_enkf.png", "Sensor assimilation: raw prediction (dashed), latent correction (yellow) and EnKF (green) against the reference simulation (white)."),
                ]),
            ],
            quote=(
                "This is a synthetic 2D laminar channel, not a plant. It stands as a demonstration of the digital-twin architecture, not as a design number.",
                "Experiment record · thermal twin",
            ),
            limits=[
                "The object is a <b>synthetic 2D laminar channel</b> with a heater and varying flow. It is not an industrial plant, nor a client geometry.",
                "Pressure is the hardest field: 27% error. Temperature and velocity converge; pressure does not yet.",
                "The reference simulation's mesh study carries high uncertainty, at <b>GCI ≈ 50%</b>. The surrogate error is measured against a reference that carries that uncertainty.",
            ],
        ),
    ),
    # -------------------------------------------------------------- câmara
    dict(
        slug="camera-compacta",
        pt=dict(
            crumb="Caso · antenas e RF",
            eyebrow="Antenas, RF e câmaras de medição",
            h1="Antes de propor um substituto, medimos o solver",
            deck="Seiscentas e trinta configurações de um refletor de câmara compacta resolvidas duas vezes, nas mesmas condições e métricas — para saber o que cada fidelidade custa e onde ela erra.",
            evidence=("ok", "Validado"),
            short="Física óptica contra solve exato em 630 configurações de refletor",
            key="768×",
            meta=[
                ("Aplicação", "Refletor de câmara compacta para medição de antenas (zona quieta)"),
                ("Setor", "Antenas, RF, instrumentação de medição"),
                ("Tema", "Duas fidelidades, correção aprendida, orçamento de solves"),
                ("Pilha", "Modelo 2-D do refletor, física óptica (PO), solve de equação integral"),
                ("Referência", "Série analítica de cilindro condutor, reproduzida com 0,6–0,9% de erro"),
            ],
            stats=[
                ("768×", "custo estimado do solve direto em 3-D contra a física óptica: 4,3 h contra 20 s por projeto"),
                ("98%", "do melhor projeto alcançado com 12 solves caros, contra 81% gastando os mesmos 12 às cegas"),
                ("0,6–0,9%", "erro do solve direto contra a série exata (a física óptica erra 500–780% no mesmo teste)"),
                ("630", "configurações resolvidas duas vezes, nas mesmas condições e métricas"),
            ],
            objective=(
                "Otimizar o refletor de uma câmara compacta — a peça que define o tamanho da zona quieta onde a antena é "
                "medida — pede centenas de configurações. A física óptica é barata e aproximada; o solve exato é caro. Sem "
                "medir os dois lado a lado, qualquer proposta de substituto ou de multi-fidelidade é suposição: não se "
                "sabe quanto custa cada lado nem onde o barato erra."
            ),
            takeaways=[
                "<b>Em 3-D o solve direto custa cerca de 768× a física óptica</b> — 20 segundos contra aproximadamente 4,3 horas por projeto. O substituto não é preferência, é necessidade.",
                "<b>Ordenar pelo modelo barato já leva a 94% do melhor projeto</b> com 12 solves caros; combinar as duas fidelidades chega a 97–98% com o mesmo orçamento, contra 81% de uma busca cega.",
                "<b>A física óptica só é útil onde se sabe quanto ela erra.</b> Contra a série exata do cilindro, ela erra 500–780%; o solve direto erra 0,6–0,9%.",
            ],
            sections=[
                dict(h="Duas fidelidades, as mesmas métricas", body=[
                    "As 630 configurações — tamanho do refletor, iluminação e 18 perfis de borda — foram resolvidas pelos dois métodos, com as mesmas métricas de saída. A diferença entre eles virou um modelo aprendido, e não um fator de correção escolhido a dedo.",
                    "O passo anterior é a verificação de cada solver: o solve direto reproduz a série analítica de um cilindro condutor com 0,6–0,9% de erro. Sem essa âncora, não haveria como saber qual dos dois está certo.",
                ]),
                dict(h="O que a correção aprendida remove — e o que ela não transfere", body=[
                    "A correção reduz o erro da física óptica por indicador dentro da família de bordas ensaiada. Com um perfil de borda inteiro mantido fora do treino, sobram 17–20% nas grandezas de amplitude e nada em ripple, fase e largura útil: a transferência tem limite, e o limite é medível.",
                ], figs=[
                    ("compact_range_validacao.jpg", "Esquerda: quanto do erro da física óptica a correção aprendida remove, por indicador — e o que sobra quando um perfil de borda inteiro fica fora do treino. Direita: fração do melhor projeto alcançada pelas quatro estratégias com o mesmo orçamento de solves caros."),
                ]),
                dict(h="Quanto custa cada lado", body=[
                    "O custo do solve direto em 3-D não foi medido diretamente: vem do custo medido de uma única aplicação do operador integral denso, 391 segundos na malha de produção, repetida 40 vezes por solve. A regra que fecha a conta com o solve do cliente é direta: para um solve direto de T segundos, divida T por 391 para saber quantas aplicações do operador cabem no mesmo tempo.",
                ]),
            ],
            quote=(
                "Nenhuma proposta de substituto deveria existir antes de medir os dois lados na mesma bancada. O valor não estava em prever melhor, estava em saber quanto cada método erra e quanto custa.",
                "Registro do experimento · refletor de câmara compacta",
            ),
            limits=[
                "O modelo é <b>2-D</b>: as métricas são relativas (taper, ripple, largura útil), não o diâmetro de zona quieta 3-D.",
                "O solve direto em 3-D <b>não foi implementado</b> para este estudo. O fator de 768× é uma estimativa a partir do custo medido de uma aplicação do operador, não um tempo de relógio de um solve completo.",
                "A correção aprendida transfere dentro da família de bordas ensaiada. Com um perfil fora dela, sobra erro em amplitude e o ganho em ripple, fase e largura útil desaparece.",
                "No mapa de tamanho × iluminação, a física óptica erra a escolha vencedora em 162 mm na largura útil.",
            ],
        ),
        en=dict(
            crumb="Case · antennas and RF",
            eyebrow="Antennas, RF and measurement chambers",
            h1="Before proposing a surrogate, we measured the solver",
            deck="Six hundred and thirty configurations of a compact-range reflector solved twice, under the same conditions and metrics — to find out what each fidelity costs and where it errs.",
            evidence=("ok", "Validated"),
            short="Physical optics against a direct solve across 630 reflector configurations",
            key="768×",
            meta=[
                ("Application", "Compact-range reflector for antenna measurement (quiet zone)"),
                ("Sector", "Antennas, RF, measurement instrumentation"),
                ("Topic", "Two fidelities, learned correction, solve budget"),
                ("Stack", "2-D reflector model, physical optics (PO), integral-equation solve"),
                ("Reference", "Analytic conducting-cylinder series, reproduced to 0.6–0.9% error"),
            ],
            stats=[
                ("768×", "estimated cost of the 3-D direct solve against physical optics: 4.3 h against 20 s per design"),
                ("98%", "of the best design reached with 12 expensive solves, against 81% spending the same 12 blindly"),
                ("0.6–0.9%", "direct-solve error against the exact series (physical optics is off by 500–780% on the same test)"),
                ("630", "configurations solved twice, under the same conditions and metrics"),
            ],
            objective=(
                "Optimising a compact-range reflector — the part that sets the size of the quiet zone where the antenna "
                "is measured — takes hundreds of configurations. Physical optics is cheap and approximate; the exact "
                "solve is expensive. Without measuring both side by side, any surrogate or multi-fidelity proposal is a "
                "guess: you do not know what each side costs or where the cheap one errs."
            ),
            takeaways=[
                "<b>In 3-D the direct solve costs about 768× physical optics</b> — 20 seconds against roughly 4.3 hours per design. The surrogate is not a preference, it is a necessity.",
                "<b>Ranking by the cheap model already reaches 94% of the best design</b> with 12 expensive solves; combining both fidelities reaches 97–98% on the same budget, against 81% for a blind search.",
                "<b>Physical optics is only useful where you know how much it errs.</b> Against the exact cylinder series it is off by 500–780%; the direct solve is off by 0.6–0.9%.",
            ],
            sections=[
                dict(h="Two fidelities, the same metrics", body=[
                    "All 630 configurations — reflector size, illumination and 18 edge profiles — were solved by both methods, with identical output metrics. The difference between them became a learned model, not a correction factor picked by hand.",
                    "The step before that is verifying each solver: the direct solve reproduces the analytic series of a conducting cylinder to 0.6–0.9% error. Without that anchor there would be no way to tell which of the two is right.",
                ]),
                dict(h="What the learned correction removes — and what it does not transfer", body=[
                    "The correction reduces the physical-optics error per indicator inside the edge family tested. With a whole edge profile held out of training, 17–20% remains on the amplitude quantities and nothing remains on ripple, phase and useful width: the transfer has a limit, and the limit is measurable.",
                ], figs=[
                    ("compact_range_validacao.jpg", "Left: how much of the physical-optics error the learned correction removes, per indicator — and what remains when an entire edge profile is held out of training. Right: fraction of the best design reached by the four strategies on the same budget of expensive solves."),
                ]),
                dict(h="What each side costs", body=[
                    "The 3-D direct-solve cost was not measured directly: it comes from the measured cost of a single application of the dense integral operator, 391 seconds on the production mesh, repeated 40 times per solve. The rule that closes the account with the client's own solver is simple: for a direct solve of T seconds, divide T by 391 to get how many operator applications fit in the same time.",
                ]),
            ],
            quote=(
                "No surrogate proposal should exist before measuring both sides on the same bench. The value was not in predicting better; it was in knowing how much each method errs and what it costs.",
                "Experiment record · compact-range reflector",
            ),
            limits=[
                "The model is <b>2-D</b>: the metrics are relative (taper, ripple, useful width), not the 3-D quiet-zone diameter.",
                "The 3-D direct solve <b>was not implemented</b> for this study. The 768× factor is an estimate from the measured cost of one operator application, not a wall-clock time for a complete solve.",
                "The learned correction transfers inside the edge family tested. With a profile outside it, amplitude error remains and the gain on ripple, phase and useful width disappears.",
                "On the size × illumination map, physical optics picks the wrong winner by 162 mm in useful width.",
            ],
        ),
    ),
    # ------------------------------------------------------------ text2part
    dict(
        slug="text2part",
        pt=dict(
            crumb="Caso · CAD a partir de texto",
            eyebrow="CAD e geração de geometria",
            h1="Peça CAD a partir de uma descrição em texto, e onde ela ainda falha",
            deck="Um LLM local escolhe entre construtores geométricos determinísticos. A malha final nunca vem do texto — e cada falha fica visível e mensurável.",
            evidence=("ok", "Validado"),
            short="Do texto ao STL por builders determinísticos, com o erro medido por peça",
            key="≤0,6%",
            meta=[
                ("Aplicação", "Geometria CAD a partir de descrição em linguagem natural"),
                ("Setor", "Design de produto, prototipagem, engenharia mecânica"),
                ("Tema", "LLM com saída restrita, geometria determinística, medição de erro"),
                ("Pilha", "LLM local via Ollama, builders paramétricos, STL"),
                ("Referência", "Dimensões pedidas na descrição, conferidas na malha gerada"),
            ],
            stats=[
                ("≤0,6%", "erro dimensional em cilindro, caixa e placa com furo"),
                ("526%", "erro máximo na peça composta (arruela) — o LLM escolheu o builder errado"),
                ("100%", "das peças aceitas vieram de um builder determinístico, nunca de malha gerada livre"),
                ("1–2", "tentativas do LLM até aceitar um plano de construção"),
            ],
            objective=(
                "Descrever uma peça em texto — “uma placa retangular com um furo central” — e chegar a um STL válido hoje "
                "exige um engenheiro de CAD. Um LLM que desenhasse a malha diretamente poderia alucinar geometria "
                "fisicamente inválida, e o erro seria invisível até a impressão. A pergunta do caso é se dá para obter a "
                "conveniência do texto sem abrir mão da garantia geométrica."
            ),
            takeaways=[
                "<b>Para geometria de builder único, o erro dimensional fica dentro de 0,6%</b> — cilindro, caixa e placa com furo.",
                "<b>Para uma peça composta, o erro passou de 500%.</b> O LLM escolheu o builder errado para uma arruela e justificou a escolha com uma descrição geometricamente incorreta.",
                "<b>O produto nunca alucina triângulos soltos:</b> toda falha é uma escolha errada de builder ou de parâmetro, visível e mensurável contra a descrição pedida.",
            ],
            sections=[
                dict(h="O LLM escolhe, o builder constrói", body=[
                    "O LLM local só tem permissão para escolher entre builders geométricos determinísticos já existentes — cilindro, caixa, placa com furo, booleana — e os parâmetros deles. A malha final sempre vem do builder, nunca do texto do modelo.",
                    "Isso converte o problema de “gerar geometria” em “escolher a construção certa”, que é um problema verificável: dá para comparar as dimensões da malha resultante com as dimensões pedidas na descrição.",
                ]),
                dict(h="A falha que interessa: builder errado", body=[
                    "Para a arruela, o LLM escolheu o builder de caixa com furo e justificou: “a washer is a box with a cylindrical hole cut from its center”. A descrição está errada — uma arruela é um cilindro com um furo passante, não uma caixa — e a malha saiu distorcida.",
                    "O modo de falha é o que importa: não foi uma geometria aleatória e inválida, foi uma escolha errada entre opções válidas. Isso é diagnosticável e, em princípio, corrigível com verificação automática da construção.",
                ], figs=[
                    ("text2part_case.png", "Geometria de builder único sai correta (verde); a arruela composta sai distorcida (vermelho), com a justificativa do LLM registrada ao lado."),
                ]),
            ],
            quote=(
                "O produto nunca alucina triângulos soltos: toda falha é uma escolha errada de builder ou de parâmetro, visível e mensurável contra a descrição pedida.",
                "Registro do experimento · Text2Part",
            ),
            limits=[
                "Peças compostas com <b>múltiplas operações booleanas não são confiáveis</b> sem revisão humana.",
                "O repertório é o dos builders existentes. Uma peça que exija uma operação que não está na biblioteca não é gerada — e o erro de 526% mostra o que acontece quando o LLM força a peça no builder mais próximo.",
                "A medição de erro é dimensional, contra as dimensões pedidas. Erro de forma em peças compostas corretamente escolhidas não foi caracterizado.",
            ],
        ),
        en=dict(
            crumb="Case · CAD from text",
            eyebrow="CAD and geometry generation",
            h1="A CAD part from a text description, and where it still fails",
            deck="A local LLM chooses between deterministic geometric builders. The final mesh never comes from the text — and every failure stays visible and measurable.",
            evidence=("ok", "Validated"),
            short="From text to STL through deterministic builders, with per-part error measured",
            key="≤0.6%",
            meta=[
                ("Application", "CAD geometry from a natural-language description"),
                ("Sector", "Product design, prototyping, mechanical engineering"),
                ("Topic", "Constrained LLM output, deterministic geometry, error measurement"),
                ("Stack", "Local LLM via Ollama, parametric builders, STL"),
                ("Reference", "Dimensions requested in the description, checked on the generated mesh"),
            ],
            stats=[
                ("≤0.6%", "dimensional error on cylinder, box and plate with a hole"),
                ("526%", "worst error on the composite part (washer) — the LLM picked the wrong builder"),
                ("100%", "of accepted parts came from a deterministic builder, never from free-generated mesh"),
                ("1–2", "LLM attempts before accepting a construction plan"),
            ],
            objective=(
                "Describing a part in text — “a rectangular plate with a central hole” — and getting a valid STL today "
                "takes a CAD engineer. An LLM that drew the mesh directly could hallucinate physically invalid geometry, "
                "and the error would stay invisible until printing. This case asks whether the convenience of text can be "
                "had without giving up the geometric guarantee."
            ),
            takeaways=[
                "<b>For single-builder geometry, dimensional error stays inside 0.6%</b> — cylinder, box and plate with a hole.",
                "<b>For a composite part, the error went past 500%.</b> The LLM picked the wrong builder for a washer and justified it with a geometrically wrong description.",
                "<b>The product never hallucinates loose triangles:</b> every failure is a wrong choice of builder or parameter, visible and measurable against the requested description.",
            ],
            sections=[
                dict(h="The LLM chooses, the builder builds", body=[
                    "The local LLM may only choose among existing deterministic geometric builders — cylinder, box, plate with a hole, boolean — and their parameters. The final mesh always comes from the builder, never from the model's text.",
                    "That turns “generate geometry” into “choose the right construction”, which is a verifiable problem: the resulting mesh dimensions can be compared against the dimensions asked for in the description.",
                ]),
                dict(h="The failure that matters: wrong builder", body=[
                    "For the washer, the LLM picked the box-with-a-hole builder and justified it: “a washer is a box with a cylindrical hole cut from its center”. The description is wrong — a washer is a cylinder with a through hole, not a box — and the mesh came out distorted.",
                    "The failure mode is the point: not a random invalid geometry, but a wrong choice among valid options. That is diagnosable and, in principle, fixable with automatic verification of the construction.",
                ], figs=[
                    ("text2part_case.png", "Single-builder geometry comes out correct (green); the composite washer comes out distorted (red), with the LLM's own justification recorded beside it."),
                ]),
            ],
            quote=(
                "The product never hallucinates loose triangles: every failure is a wrong choice of builder or parameter, visible and measurable against the requested description.",
                "Experiment record · Text2Part",
            ),
            limits=[
                "Composite parts with <b>multiple boolean operations are not reliable</b> without human review.",
                "The repertoire is the existing builders. A part that needs an operation outside the library is not generated — and the 526% error shows what happens when the LLM forces the part into the nearest builder.",
                "Error is measured dimensionally, against the requested dimensions. Shape error on correctly chosen composite parts was not characterised.",
            ],
        ),
    ),
]
