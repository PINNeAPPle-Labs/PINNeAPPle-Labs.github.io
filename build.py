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
    "produto": "studio",
    "artigos": "artigos",
    "lib": "lib",
}
for _post in POSTS:
    PAGES[f"post:{_post['slug']}"] = f"artigos/{_post['slug']}"


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
    "pt": [("home", "Início"), ("produto", "O produto"), ("artigos", "Artigos"), ("lib", "A lib")],
    "en": [("home", "Home"), ("produto", "The product"), ("artigos", "Articles"), ("lib", "The library")],
}

STRINGS = {
    "pt": {
        "skip": "Pular para o conteúdo",
        "wa": "Falar com um engenheiro",
        "wa_msg": "Olá! Vim pelo site da PINNeAPPle Labs e tenho um problema de engenharia para discutir.",
        "cta_title": "Tem uma simulação lenta, cara ou difícil de verificar?",
        "cta_lead": "Mande o caso. Respondemos com um escopo fechado e uma métrica de sucesso mensurável, ou dizemos que o método clássico resolve melhor.",
        "cta_primary": "Falar com um engenheiro",
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
        "lbl_lib": "A lib",
        "read_more": "Ler o artigo",
        "min_read": "min de leitura",
        "soon": "Em breve · 2027",
        "all_articles": "Ver todos os artigos",
    },
    "en": {
        "skip": "Skip to content",
        "wa": "Talk to an engineer",
        "wa_msg": "Hello! I found PINNeAPPle Labs through the site and have an engineering problem to discuss.",
        "cta_title": "Got a simulation that is slow, expensive or hard to verify?",
        "cta_lead": "Send it over. We come back with a closed scope and a measurable success criterion, or we tell you the classical method does it better.",
        "cta_primary": "Talk to an engineer",
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
        "lbl_lib": "The library",
        "read_more": "Read the article",
        "min_read": "min read",
        "soon": "Coming soon · 2027",
        "all_articles": "See all articles",
    },
}

META = {
    "home": {
        "pt": dict(
            title="PINNeAPPle Labs · engenharia com a conta aberta",
            desc="Resposta de engenharia em horas, não em semanas. O PINNeAPPle Studio chega em 2027; hoje os casos já rodam com o time. Números medidos, erro declarado, relatório verificável.",
            og="img/portfolio/13-aircraft-render-pressure.jpg",
            type="website",
        ),
        "en": dict(
            title="PINNeAPPle Labs · engineering with the working shown",
            desc="Engineering answers in hours, not weeks. PINNeAPPle Studio arrives in 2027; today the cases run with our team. Measured numbers, stated error, verifiable report.",
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
      <a class="btn btn-primary btn-sm" href="https://wa.me/{WHATSAPP}?text={_q(STRINGS[lang]['wa_msg'])}" target="_blank" rel="noopener">{STRINGS[lang]['wa']}</a>
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
          <li><a href="{root}{url(lang, 'home') or ''}">{S['lbl_products']}</a></li>
          <li><a href="{root}{url(lang, 'produto')}">{S['lbl_product']}</a></li>
          <li><a href="{root}{url(lang, 'artigos')}">{S['lbl_articles']}</a></li>
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


def vfig(src: str, poster: str, cap: str, root: str) -> str:
    return (f'<figure class="fig vfig"><video src="{root}{src}" poster="{root}{poster}" muted loop playsinline '
            f'preload="none" data-autoplay aria-label="{cap}"></video>'
            f'<figcaption>{cap}</figcaption></figure>')


def shot(src: str, alt: str, cap: str, root: str) -> str:
    """An app screenshot inside a browser frame: it reads as a product, not as a render."""
    return f"""<figure class="frame">
  <div class="frame-bar" aria-hidden="true"><i></i><i></i><i></i><span>PINNeAPPle Studio</span></div>
  <img src="{root}{src}" alt="{alt}" loading="lazy" decoding="async" />
  <figcaption>{cap}</figcaption>
</figure>"""


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
        eyebrow="PINNeAPPle Labs · engenharia assistida por física",
        h1="Resposta de engenharia em horas, não em semanas.",
        lead="Você descreve o problema. A gente diz se dá para resolver, qual método usar e quanto custa, e entrega o resultado com a conta aberta. O produto que faz isso sozinho, o <b>PINNeAPPle Studio</b>, chega em 2027. Hoje, os casos rodam com o nosso time.",
        cta_secondary="Conhecer o PINNeAPPle Studio",
        chips=["Em breve: PINNeAPPle Studio", "Números medidos, nunca estimados", "Base de código aberto"],
        hero_cap="O PINNeAPPle Studio: você escreve o que precisa e ele mostra o que já existe pronto para rodar.",
        problem_eyebrow="O problema",
        problem_h="Por que a simulação trava o projeto",
        problem_p="Não é falta de software. É tempo, custo e, principalmente, confiança no número que sai.",
        problems=[
            ("O prazo", "Uma semana para montar o caso, outra para rodar, mais uma para conferir. Quando o resultado chega, a decisão já foi tomada no chute."),
            ("O custo", "Licença, máquina parada e especialista. Às vezes a simulação custa mais caro que a decisão que ela deveria sustentar."),
            ("A confiança", "O resultado sai colorido e bonito, e ninguém sabe se está certo. Sem uma referência externa, o número vira opinião."),
        ],
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
        proofs_p="Três experimentos abertos, cada um com artigo inteiro: o que foi medido, contra o que foi comparado e o que ainda não está provado.",
        proofs=[
            ("img/portfolio/13-aircraft-render-pressure.jpg", "Pressão na pele de uma asa otimizada",
             "Otimização", "1.920 asas, três objetivos", "asa-1920-projetos"),
            ("img/erosao-card.webp", "Mapa de erosão na parede de uma curva de 90°, com a taxa em mm/ano",
             "CFD", "A erosão que bateu com o ensaio", "erosao-curva-90"),
            ("img/twin.jpg", "Gêmeo digital de um ativo em 3D, com a leitura viva ao lado",
             "Gêmeo digital", "Um ativo em 3D, com leitura viva", "gemeo-hx201"),
        ],
        news_eyebrow="Artigos",
        news_h="O que a gente mediu, contado por inteiro",
        news_p="Um experimento por artigo, com imagens, vídeo e os números que saíram da execução. Inclusive os que limitam o resultado.",
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
        eyebrow="PINNeAPPle Labs · physics-assisted engineering",
        h1="Engineering answers in hours, not weeks.",
        lead="You describe the problem. We say whether it can be solved, with which method, and at what cost, and deliver the result with the working shown. The product that does this on its own, <b>PINNeAPPle Studio</b>, arrives in 2027. Today, the cases run with our team.",
        cta_secondary="Meet PINNeAPPle Studio",
        chips=["Arriving in 2027: PINNeAPPle Studio", "Measured numbers, never estimates", "Open-source base"],
        hero_cap="The PINNeAPPle Studio: you write what you need and it shows what is already ready to run.",
        problem_eyebrow="The problem",
        problem_h="Why simulation holds the project up",
        problem_p="It is not a lack of software. It is time, cost and, mostly, trust in the number that comes out.",
        problems=[
            ("The deadline", "A week to build the case, another to run it, another to check it. By the time the result lands, the decision was already made on a guess."),
            ("The cost", "Licence, idle machine and a specialist. Sometimes the simulation costs more than the decision it was meant to support."),
            ("The trust", "The result comes out colourful and pretty, and nobody knows whether it is right. Without an external reference, the number is just an opinion."),
        ],
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
        proofs_p="Three open experiments, each with a full article: what was measured, what it was compared against, and what is not proven yet.",
        proofs=[
            ("img/portfolio/13-aircraft-render-pressure.jpg", "Skin pressure on an optimized wing",
             "Optimization", "1,920 wings, three objectives", "asa-1920-projetos"),
            ("img/erosao-card.webp", "Wall erosion map on a 90° bend, rate in mm/year",
             "CFD", "Erosion that met the published experiment", "erosao-curva-90"),
            ("img/twin.jpg", "Digital twin of an asset in 3D, with the live reading beside it",
             "Digital twin", "An asset in 3D, with a live reading", "gemeo-hx201"),
        ],
        news_eyebrow="Articles",
        news_h="What we measured, told in full",
        news_p="One experiment per article, with images, video and the numbers that came out of the run. Including the ones that limit the result.",
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
        flow_shots=[
            ("img/eng/studio-explore.webp", "Busca por dissipador de calor com aletas no Studio", "A busca por “dissipador de calor com aletas”: 167 resultados, e cada um diz se é executável, testada ou verificada."),
        ],
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
        flow_shots=[
            ("img/eng/studio-explore.webp", "Search for a finned heat sink in the Studio", "The search for “finned heat sink”: 167 results, and each one says whether it is runnable, tested or verified."),
        ],
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
# Page: home
# ---------------------------------------------------------------------------


def page_home(lang: str) -> str:
    root = up(lang, "home")
    S = STRINGS[lang]
    C = HOME[lang]
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
          {wa_button(lang)}
          <a class="btn btn-ghost" href="{root}{url(lang, 'produto')}">{C['cta_secondary']} →</a>
        </div>
        <div class="hero-meta">{chips}</div>
      </div>
      <div>
        {shot('img/eng/studio-home.webp', C['hero_cap'], C['hero_cap'], root)}
      </div>
    </div>
  </section>
""")

    problems = "".join(
        f'<article class="problem-card reveal"><h3>{t}</h3><p>{b}</p></article>'
        for t, b in C["problems"]
    )
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

    points = "".join(f"<li>{p}</li>" for p in C["product_points"])
    parts.append(f"""
  <section id="produto">
    <div class="wrap">
      <div class="split-block reveal">
        <div>
          <p class="badge-soon">{S['soon']}</p>
          <h2 style="margin-top:1.1rem">{C['product_h']}</h2>
          <p style="color:var(--text-dim);margin-top:1rem">{C['product_lead']}</p>
          <ul class="checks">{points}</ul>
          <p class="product-actions">
            <a class="btn btn-primary" href="{root}{url(lang, 'produto')}">{C['product_cta']} →</a>
            <a class="btn btn-ghost" href="https://wa.me/{WHATSAPP}?text={_q(C['product_soon'])}" target="_blank" rel="noopener">{'Entrar na lista' if lang == 'pt' else 'Join the list'}</a>
          </p>
          <p class="src-note">{C['product_soon']}</p>
        </div>
        <div>
          {shot('img/eng/studio-report.webp', C['product_cap'], C['product_cap'], root)}
        </div>
      </div>
    </div>
  </section>
""")

    caps = "".join(
        f'<article class="cap reveal"><p class="kind">{kind}</p><h3>{title}</h3><p>{body}</p>'
        f'<p class="ex"><b>{example}</b></p></article>'
        for kind, title, body, example in CAPS[lang]
    )
    parts.append(f"""
  <section id="capacidades" class="alt">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['caps_eyebrow']}</p><h2>{C['caps_h']}</h2></div>
        <p>{C['caps_p']}</p>
      </div>
      <div class="grid-3 reveal">{caps}</div>
    </div>
  </section>
""")

    steps = "".join(
        f'<div class="step reveal"><span class="sn">0{i + 1}</span><h3>{t}</h3><p>{b}</p></div>'
        for i, (t, b) in enumerate(C["how"])
    )
    parts.append(f"""
  <section id="como">
    <div class="wrap">
      <div class="section-head split reveal">
        <div><p class="eyebrow">{C['how_eyebrow']}</p><h2>{C['how_h']}</h2></div>
        <p>{C['how_p']}</p>
      </div>
      <div class="steps cols3 reveal">{steps}</div>
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


def page_produto(lang: str) -> str:
    root = up(lang, "produto")
    S = STRINGS[lang]
    C = PRODUCT[lang]
    page = "produto"

    chips = "".join(f'<span class="chip">{c}</span>' for c in C["chips"])
    counts = "".join(
        f'<div class="exist-cell"><b>{n}</b><span>{l}</span></div>' for n, l in C["counts"]
    )
    flow = "".join(
        f'<div class="step reveal"><span class="sn">{n}</span><h3>{t}</h3><p>{b}</p></div>'
        for n, t, b in C["flow"]
    )
    flow_shots = "".join(shot(src, alt, cap, root) for src, alt, cap in C["flow_shots"])
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

    return "".join([
        head(lang, page, root), header(lang, page, root),
        f"""<main id="main">
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="badge-soon">{S['soon']}</p>
        <h1 style="margin-top:1.1rem">{C['h1']}</h1>
        <p class="lead">{C['lead']}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="https://wa.me/{WHATSAPP}?text={_q(C['cta_primary'])}" target="_blank" rel="noopener">{C['cta_primary']}</a>
          <a class="btn btn-ghost" href="{root}{url(lang, 'artigos')}">{C['cta_secondary']} →</a>
        </div>
        <div class="hero-meta">{chips}</div>
      </div>
      <div>{shot('img/eng/studio-home.webp', C['hero_cap'], C['hero_cap'], root)}</div>
    </div>
  </section>

  <section id="oque" class="alt tight">
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
""",
        cta_band(lang, root),
        "</main>",
        footer(lang, page, root),
    ])


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

BUILDERS = {
    "home": page_home,
    "produto": page_produto,
    "artigos": page_artigos,
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
