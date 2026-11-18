#!/usr/bin/env python3
"""Builds the public example reports: one A4 document per case, in pt-BR and English.

    python3 tools/build_relatorios.py            # every report, both languages
    python3 tools/build_relatorios.py erosao     # just one

Each report is a HTML file printed to PDF by the local Chrome, so the type and the
colours are the same ones the site uses. Every number here comes from a case that
already exists in the repository — `PINNeAPPle-CFD/casos/cfd04-curva-areia`,
`casos/cfd08-valvula-globo` and `PINNeAPPle/apps/twin_ops` — with the reference it was
checked against. Nothing is rounded up, and each report carries its own limits page.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "relatorios"
SRC = OUT / "src"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LANGS = ("pt", "en")

CSS = """
  @font-face { font-family: 'Archivo'; font-weight: 400 800; src: url(../../fonts/k3kPo8UDI-1M0wlSV9XAw6lQkqWY8Q82sLydOxKsv4Rn.woff2) format('woff2'); }
  @font-face { font-family: 'JetBrains Mono'; font-weight: 400 500; src: url(../../fonts/tDbv2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8yKwBNntkaToggR7BYRbKPxDcwgknk-4.woff2) format('woff2'); }
  :root {
    --ink: #262626; --dim: #4a4a4a; --mute: #767676; --line: #e0e0e0;
    --gold: #a23a00; --gold-bg: #f7e7df; --cyan: #0081be; --cyan-bg: #e3f0f8;
    --ok: #1f7a4d; --fail: #b03a3a;
  }
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body { font-family: 'Archivo', system-ui, sans-serif; color: var(--ink); font-size: 10.2pt; line-height: 1.55; -webkit-font-smoothing: antialiased; }
  .page { width: 210mm; min-height: 297mm; padding: 20mm 18mm 16mm; position: relative; break-after: page; page-break-after: always; }
  .page:last-child { break-after: auto; page-break-after: auto; }
  .runhead { display: flex; justify-content: space-between; align-items: baseline; font-family: 'JetBrains Mono', monospace; font-size: 7pt; letter-spacing: .06em; text-transform: uppercase; color: var(--mute); border-bottom: 1px solid var(--line); padding-bottom: 3mm; margin-bottom: 8mm; }
  .runfoot { position: absolute; left: 18mm; right: 18mm; bottom: 8mm; display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 7pt; color: var(--mute); border-top: 1px solid var(--line); padding-top: 2.5mm; }
  h1 { font-size: 12pt; margin: 0 0 5mm; letter-spacing: -0.01em; }
  h2 { font-size: 15pt; margin: 0 0 4mm; letter-spacing: -0.015em; }
  h3 { font-size: 10.5pt; margin: 7mm 0 2mm; }
  p { margin: 0 0 3.2mm; }
  .lead { font-size: 11.5pt; color: var(--dim); line-height: 1.5; }
  .eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--gold); margin: 0 0 3mm; }
  small { font-size: 8pt; color: var(--mute); }
  code, .mono { font-family: 'JetBrains Mono', monospace; }
  .cover { display: flex; flex-direction: column; justify-content: space-between; height: 297mm; }
  .cover .top { border-bottom: 3px solid var(--gold); padding-bottom: 6mm; }
  .brand { display: flex; align-items: center; gap: 3mm; font-weight: 700; font-size: 12pt; letter-spacing: -0.02em; }
  .brand span.labs { font-weight: 400; color: var(--dim); }
  .cover h1 { font-size: 28pt; line-height: 1.1; margin: 10mm 0 3mm; letter-spacing: -0.03em; }
  .cover .sub { font-size: 12pt; color: var(--dim); max-width: 130mm; }
  .cover .numbers { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; margin-top: 8mm; }
  .num { border-top: 2px solid var(--ink); padding-top: 3mm; }
  .num b { display: block; font-size: 21pt; letter-spacing: -0.03em; }
  .num span { font-size: 8.5pt; color: var(--dim); }
  .cover img { width: 100%; max-height: 86mm; object-fit: contain; background: #fff; border: 1px solid var(--line); border-radius: 2mm; margin-top: 8mm; }
  .cover .meta { font-family: 'JetBrains Mono', monospace; font-size: 7.5pt; color: var(--mute); line-height: 1.9; }
  table { width: 100%; border-collapse: collapse; margin: 0 0 4mm; font-size: 9pt; }
  th, td { text-align: left; padding: 2mm 2.5mm; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { font-family: 'JetBrains Mono', monospace; font-size: 7pt; letter-spacing: .06em; text-transform: uppercase; color: var(--mute); border-bottom: 1px solid var(--ink); }
  td.n { font-family: 'JetBrains Mono', monospace; white-space: nowrap; }
  .callout { border-left: 3px solid var(--gold); background: var(--gold-bg); padding: 4mm 5mm; margin: 0 0 5mm; font-size: 9.5pt; }
  .callout.cyan { border-color: var(--cyan); background: var(--cyan-bg); }
  .verdict { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 7.5pt; padding: .6mm 2mm; border-radius: 1.5mm; letter-spacing: .04em; }
  .v-ok { background: #e3f4ea; color: var(--ok); }
  .v-fail { background: #f8e6e6; color: var(--fail); }
  .v-mid { background: #f7e7df; color: var(--gold); }
  ul { margin: 0 0 3.5mm; padding-left: 4.5mm; }
  li { margin-bottom: 1.2mm; }
  figure { margin: 0 0 4mm; }
  figure img { width: 100%; border: 1px solid var(--line); border-radius: 2mm; }
  figcaption { font-family: 'JetBrains Mono', monospace; font-size: 7pt; color: var(--mute); margin-top: 2mm; line-height: 1.6; }
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin: 0 0 5mm; }
  .kpi { border: 1px solid var(--line); border-radius: 2mm; padding: 3.5mm; }
  .kpi b { display: block; font-size: 15pt; letter-spacing: -0.02em; }
  .kpi span { font-size: 8pt; color: var(--dim); }
"""

LOGO = ('<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true">'
        '<circle cx="16" cy="16" r="15" fill="#a23a00"/>'
        '<path d="M16 6c4 3 6 6.5 6 10s-2.5 6.5-6 10c-3.5-3.5-6-6.5-6-10s2-7 6-10z" fill="#262626"/>'
        '<path d="M16 8.5v15" stroke="#262626" stroke-width="1.2"/></svg>')


def render_block(b: tuple) -> str:
    kind = b[0]
    if kind == "p":
        return f"<p>{b[1]}</p>"
    if kind == "small":
        return f"<p><small>{b[1]}</small></p>"
    if kind == "lead":
        return f'<p class="lead">{b[1]}</p>'
    if kind == "h3":
        return f"<h3>{b[1]}</h3>"
    if kind == "table":
        headers, rows = b[1], b[2]
        widths = b[3] if len(b) > 3 else None
        head = ""
        for i, h in enumerate(headers):
            w = f' style="width:{widths[i]}"' if widths and widths[i] else ""
            head += f"<th{w}>{h}</th>"
        body = "".join(
            "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows
        )
        return f"<table><tr>{head}</tr>{body}</table>"
    if kind == "callout":
        tone, label, text = b[1], b[2], b[3]
        cls = "callout cyan" if tone == "cyan" else "callout"
        return f'<div class="{cls}"><b>{label}</b> {text}</div>' if label else f'<div class="{cls}">{text}</div>'
    if kind == "figure":
        return f'<figure><img src="../../{b[1]}" alt="{b[2]}" /><figcaption>{b[2]}</figcaption></figure>'
    if kind == "bullets":
        return "<ul>" + "".join(f"<li>{i}</li>" for i in b[1]) + "</ul>"
    if kind == "kpi":
        cells = "".join(f'<div class="kpi"><b>{n}</b><span>{l}</span></div>' for n, l in b[1])
        return f'<div class="kpi-row">{cells}</div>'
    raise ValueError(kind)


def render(report: dict, lang: str) -> str:
    R = report[lang]
    nums = "".join(f'<div class="num"><b>{n}</b><span>{s}</span></div>' for n, s in R["numbers"])
    meta = "<br />".join(R["meta"])
    cover_img = (f'<img src="../../{R["cover_img"]}" alt="{R["cover_alt"]}" />'
                 if R.get("cover_img") else "")
    cover = f"""
<section class="page cover">
  <div class="top">
    <div class="brand">{LOGO}<span>PINNeAPPle</span></div>
    <p class="eyebrow" style="margin-top:6mm">{R['eyebrow']}</p>
    <h1>{R['title']}</h1>
    <p class="sub">{R['sub']}</p>
    <div class="numbers">{nums}</div>
  </div>
  <div>
    {cover_img}
    <div class="meta" style="margin-top:6mm">{meta}</div>
  </div>
</section>
"""
    pages = []
    for i, (title, blocks) in enumerate(R["pages"], start=1):
        body = "\n  ".join(render_block(b) for b in blocks)
        pages.append(f"""
<section class="page">
  <div class="runhead"><span>{R['short']}</span><span>{title}</span></div>
  {body}
  <div class="runfoot"><span>PINNeAPPle · {R['foot']}</span><span>{i}</span></div>
</section>
""")
    return (f'<!doctype html>\n<html lang="{R["html_lang"]}">\n<head>\n<meta charset="utf-8" />\n'
            f"<title>{R['doc_title']}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
            + cover + "".join(pages) + "\n</body>\n</html>\n")


# ---------------------------------------------------------------------------
# The reports
# ---------------------------------------------------------------------------

REPORTS = {}

# --- CFD-04: erosion in a 90° bend ----------------------------------------
REPORTS["estudo-erosao-curva-90"] = {
    "pt": dict(
        html_lang="pt-BR",
        doc_title="Estudo de erosão em curva de 90° — PINNeAPPle",
        eyebrow="Relatório de estudo · exemplo público",
        title="Erosão em curva de 90°<br />ar com areia a 15 m/s",
        sub="Onde a parede erode, a que taxa, em quanto tempo — e por que este número pode ser usado numa decisão.",
        numbers=[("1,05–1,49×", "do ensaio publicado, dentro do fator 2 que a prática aceita"),
                 ("50,6°", "de pico calculado, contra 45° medido"),
                 ("32 casos", "do CAD ao modelo treinado, em 22,6 min")],
        cover_img="img/erosao-card.webp",
        cover_alt="Mapa de erosão na parede de uma curva de 90°, com a taxa em mm por ano",
        meta=["Documento ERC-04 · versão 1.0 · 2026",
              "Caso de demonstração (geometria e condições públicas, sem dado de cliente)",
              "Ensaio de referência: Vieira et al. (2016), dados abertos",
              "PINNeAPPle · LAIS &amp; YAN LTDA · pinneapple-labs.github.io"],
        short="ERC-04 · erosão em curva de 90°",
        foot="relatório de exemplo",
        pages=[
            ("1 · o pedido", [
                ("lead", "Uma curva de 90° de 50 mm transporta ar com areia. A pergunta não era “quanto erode”: era <b>quando a parede chega na espessura mínima</b> e <b>se trocar o raio da curva muda a resposta o suficiente para justificar a obra</b>."),
                ("h3", "Escopo contratado"),
                ("table", ["Entregável", "O que contém"], [
                    ["Mapa de erosão", "Taxa na parede (mm/ano) em toda a geometria, com a posição do pico"],
                    ["Vida útil", "Anos até a espessura mínima, para o ponto crítico"],
                    ["Verificação", "Comparação com ensaio publicado e escolha do modelo de erosão justificada"],
                    ["Modelo substituto", "Resposta em segundos para novas vazões e raios de curva"],
                    ["Limites", "O que não está provado e o que precisa de ensaio"],
                ], ["38%", None]),
                ("h3", "Fora do escopo"),
                ("p", "Projeto mecânico do tubo, seleção de material, inspeção em campo, ensaio experimental. O estudo entrega o número e a prova; a decisão de engenharia e a compra continuam do lado de quem contrata."),
                ("callout", "gold", "Como ler este documento.", "Cada número aparece com a referência contra a qual foi conferido — ensaio publicado, solver independente ou estudo de malha. Números sem referência não entram no relatório: ficam na seção de limites, como pergunta aberta."),
                ("h3", "Premissas que mudam a resposta"),
                ("bullets", [
                    "A taxa de areia é a do cenário informado; um pico de partículas muda o resultado mais que a malha.",
                    "A parede é aço-carbono; outro material muda o coeficiente de erosão, não a distribuição de impactos.",
                    "O escoamento é permanente no ponto de operação avaliado; regime transitório (partidas, golpe) não está coberto.",
                ]),
            ]),
            ("2 · dados de entrada", [
                ("p", "Este é o formulário do caso de demonstração — no estudo de um cliente, estes campos vêm do CAD, da ficha de processo e do histórico de operação."),
                ("table", ["Item", "Valor", "Origem"], [
                    ["Geometria", '<span class="mono">curva 90°, D = 50 mm</span>', "10·D a montante e 20·D a jusante"],
                    ["Fluido", '<span class="mono">ar a 20 °C · ρ = 1,204 kg/m³ · µ = 1,825·10⁻⁵ Pa·s</span>', "catálogo de fluidos"],
                    ["Partículas", '<span class="mono">quartzo · ρp = 2.650 kg/m³ · dp = 150 µm</span>', "Fs = 0,53 · ṁp = 10⁻⁴ kg/s"],
                    ["Parede", '<span class="mono">aço-carbono · 7.800 kg/m³ · HB 150</span>', "espessura 5 → 2 mm · 8.760 h/ano"],
                    ["Ponto de referência", '<span class="mono">U = 20 m/s · R/D = 1,5</span>', "caso base do mapa e do estudo de malha"],
                    ["Campanha", '<span class="mono">32 pontos · Sobol</span>', "U de 10 a 30 m/s · R/D de 1,5 a 5"],
                ], ["16%", "46%", None]),
                ("callout", "cyan", "Regra do estudo:", "a faixa de validade é declarada antes de rodar. Fora de U = 10–30 m/s ou de R/D = 1,5–5, o modelo substituto avisa que está extrapolando — e o número perde a garantia."),
                ("h3", "Como o método foi montado"),
                ("table", ["Etapa", "Escolha"], [
                    ["Malha", 'Hexaédrica gerada por script (<span class="mono">classy_blocks</span>), 10.400 células, y⁺ alvo 50, <span class="mono">checkMesh</span> aprovado'],
                    ["Escoamento", '<span class="mono">simpleFoam</span>, k-ω SST, 109 iterações até convergir, balanço de massa 3,5·10⁻⁶'],
                    ["Partículas", '<span class="mono">icoUncoupledKinematicParcelFoam</span>, 2.000 parcelas (4.000 no teste estatístico)'],
                    ["Erosão", "Modelo de impacto DNV-RP-O501 aplicado aos impactos na parede; E/CRC e Finnie como checagem"],
                    ["Convergência do caso", "26 s de parede em 4 núcleos · 14 a 17 mil impactos na parede"],
                ], ["30%", None]),
            ]),
            ("3 · verificação", [
                ("lead", "Antes de reportar uma taxa de erosão, o modelo foi obrigado a reproduzir um ensaio que ele nunca viu: a curva de Vieira et al. (2016), D = 76,2 mm, R/D = 1,5, areia de 150 µm, em três velocidades."),
                ("table", ["Ensaio", "U (m/s)", "Medido (mm/ano)", "Calculado (mm/ano)", "Razão", "Fator 2"], [
                    ["T1", "11", "6,5", "6,8", "1,05×", '<span class="verdict v-ok">aprovado</span>'],
                    ["T3", "15", "13,2", "16,9", "1,28×", '<span class="verdict v-ok">aprovado</span>'],
                    ["T5", "23", "36,2", "53,8", "1,49×", '<span class="verdict v-ok">aprovado</span>'],
                    ["posição do pico", "—", "45°", "50,6°", "+5,6°", '<span class="verdict v-ok">aprovado</span>'],
                ]),
                ("small", "Areia de 150 µm nos três ensaios. Razões e posições calculadas com o modelo de impacto da DNV-RP-O501, na malha do estudo. Medidos: Khan et al. (2023); posição do pico: Khan et al. (2022)."),
                ("callout", "gold", "Por que isto importa.", "Erosão não é fenômeno para precisão de 1%: depende da distribuição de partículas, do material e do histórico. A prática de projeto aceita um fator 2. O compromisso é ficar dentro da faixa <b>e dizer em que ponto dela</b>."),
                ("h3", "Os outros modelos foram testados e reprovados"),
                ("table", ["Modelo de erosão", "Contra os três ensaios", "Leitura"], [
                    ["DNV-RP-O501 (impacto)", "1,05–1,49×", '<span class="verdict v-ok">adotado</span> dentro do fator 2 nos três'],
                    ["E/CRC", "1,98–2,5× acima", '<span class="verdict v-fail">reprovado</span> sai da faixa nos três'],
                    ["Finnie", "~28× acima", '<span class="verdict v-fail">reprovado</span> ordem de grandeza errada'],
                    ["Fórmula fechada DNV §8.4 (sem CFD)", "97–100× abaixo em 2 de 3", '<span class="verdict v-fail">reprovado</span> depende do fator G, que varia de 0,02 a 1'],
                ], ["34%", "26%", None]),
                ("callout", "cyan", "O que ainda não está provado.", "As constantes de erosão dos três modelos vêm de fonte secundária (o ensaio original é pago). A verificação acima é a melhor evidência disponível hoje, declarada como tal — não como validação definitiva."),
            ]),
            ("4 · resultado", [
                ("h3", "Primeiro o ensaio, resolvido: T3, 15 m/s"),
                ("figure", "img/erosao.jpg", "Mapa de erosão na parede no ensaio T3: tubulação inteira e zoom na curva, com o pico na parede externa logo após a entrada da curva. Escala em mm/ano."),
                ("p", "O máximo não está no meio da curva: está na parede externa, 50,6° depois da entrada (o ensaio mede 45°). É esse ponto que a inspeção precisa medir primeiro — e é ele que define a vida útil do resto da linha."),
                ("h3", "Depois o caso de projeto: U = 20 m/s, R/D = 1,5"),
                ("table", ["Modelo de erosão", "Taxa máxima (mm/ano)", "Vida útil 5 → 2 mm"], [
                    ["DNV-RP-O501 (adotado)", "1,47", "2,0 anos"],
                    ["E/CRC", "2,83", "1,1 anos"],
                    ["Finnie (checagem cruzada)", "23,8", "0,13 ano"],
                    ["Fórmula fechada DNV §8.4 (sem CFD)", "0,037", "81 anos"],
                ], ["40%", None, None]),
                ("callout", "gold", "O que a decisão precisa saber:", "com o modelo verificado, a vida útil projetada é de <b>2 anos</b> no ponto crítico. A fórmula fechada sem CFD diria 81 anos para a mesma geometria. A diferença não é precisão: é a decisão entre “troca programada” e “nenhuma ação”."),
            ]),
            ("5 · modelo substituto", [
                ("lead", "Trinta e dois casos cobrindo U de 10 a 30 m/s e R/D de 1,5 a 5 foram resolvidos em CFD e usados para treinar um modelo que responde em segundos. Os 32 terminaram sem rejeição, em 22,6 min de parede (1,94 h de CPU)."),
                ("table", ["Indicador", "Referência sem IA", "Validação", "Teste", "Fora da faixa"], [
                    ["Perda de carga (ΔP)", "Darcy + Colebrook", "0,7%", "1,0%", "0,4%"],
                    ["Taxa máxima de erosão", "DNV §8.4", "15,7%", "10,6%", "19,7%"],
                ], ["32%", None, None, None, None]),
                ("small", "Erro relativo médio. O intervalo de confiança por bootstrap não foi calculado: há 9 pontos de teste e fora da faixa, e o critério exige no mínimo 10."),
                ("h3", "Para que serve, na prática"),
                ("bullets", [
                    "Variar diâmetro, raio de curva e vazão deixa de custar um dia por ponto.",
                    "A vida útil deixa de ser um número único e passa a ser uma curva contra a vazão.",
                    "Fora da faixa de treino, o modelo avisa que está extrapolando, com o erro medido de 19,7%.",
                ]),
                ("callout", "cyan", "O que o substituto não faz:", "substituir o ensaio. Ele reproduz o CFD dentro da faixa treinada — se o CFD estiver errado para o seu caso, o substituto erra junto, mais rápido."),
            ]),
            ("6 · limites", [
                ("lead", "Esta seção existe porque um número sem os seus limites é uma opinião com casas decimais. Tudo o que não passou por referência externa está aqui."),
                ("table", ["Item", "Estado", "Consequência prática"], [
                    ["Malha da campanha", '<span class="verdict v-fail">grossa</span>', "10.400 células: ~30% acima no ΔP e ~40% abaixo na erosão, contra o valor extrapolado da malha fina"],
                    ["Convergência de malha (GCI)", '<span class="verdict v-fail">fora da meta</span>', "ΔP com GCI de 6,8–12,6% na malha fina (meta 5%); a erosão só converge no ponto de referência (2,9%)"],
                    ["Constantes de erosão", '<span class="verdict v-fail">fonte secundária</span>', "DNV, E/CRC e Finnie vêm de literatura secundária; o ensaio original é pago"],
                    ["Campos enviados à verificação", '<span class="verdict v-fail">6 provas não rodaram</span>', "11 a favor, 0 contra, 65% de cobertura"],
                    ["Interpolação do substituto", '<span class="verdict v-ok">medida</span>', "1,0% no ΔP e 10,6% na erosão, em pontos fora do treino"],
                    ["Extrapolação do substituto", '<span class="verdict v-fail">avisada, não garantida</span>', "fora de U 10–30 m/s ou R/D 1,5–5, o erro sobe (19,7%)"],
                ], ["30%", "22%", None]),
                ("callout", "gold", "Regra da casa.", "Resultado com malha grossa vale como demonstração do pipeline, não como número de cliente. Este documento é público justamente por isso."),
                ("h3", "O que faria este número subir de patamar"),
                ("bullets", ["Campanha na malha fina, com GCI dentro de 5% também para a erosão.",
                             "Ensaio próprio, ou a compra do ensaio original, para trocar as constantes secundárias.",
                             "Envio dos campos completos para a verificação, fechando as seis provas que não rodaram."]),
            ]),
            ("7 · conclusão", [
                ("kpi", [("1,47", "mm/ano no ponto crítico"), ("2,0", "anos até 5 → 2 mm"),
                         ("50,6°", "posição do pico na curva"), ("1,0%", "erro do substituto no ΔP")]),
                ("h3", "Recomendação"),
                ("p", "Inspecionar a parede externa logo após a entrada da curva, não o meio dela. Com a taxa verificada e a espessura mínima adotada, a janela de troca programada é de dois anos — e o substituto permite testar, em segundos, se aumentar o raio compra mais tempo que trocar o material."),
                ("h3", "O que este estudo não decide"),
                ("p", "Qual material comprar, qual fornecedor escolher, quando parar a planta. Ele entrega a taxa, a posição e o erro; a decisão econômica usa esses números junto com custo de parada e preço do tubo."),
                ("h3", "Proveniência"),
                ("table", ["O que", "Onde"], [
                    ["Ensaio de referência", "Vieira et al. (2016), E/CRC Tulsa · tabela aberta em Khan et al. (2023), <i>Eng. Proc.</i> 45:28"],
                    ["Posição do pico medida", "Khan et al. (2022), <i>Materials</i> 15:3721"],
                    ["Artigo público do estudo", '<span class="mono">pinneapple-labs.github.io/artigos/erosao-curva-90/</span>'],
                    ["Código e caso", '<span class="mono">github.com/PINNeAPPle-Labs/PINNeAPPle-CFD · casos/cfd04-curva-areia</span>'],
                ], ["30%", None]),
                ("callout", "cyan", "Este é um relatório de exemplo,", "montado sobre um caso de demonstração com geometria e condições públicas. Um estudo para a sua planta segue a mesma estrutura, com a mesma seção de limites."),
            ]),
        ],
    ),
    "en": dict(
        html_lang="en",
        doc_title="Erosion study in a 90° bend — PINNeAPPle",
        eyebrow="Study report · public example",
        title="Erosion in a 90° bend<br />sand-laden air at 15 m/s",
        sub="Where the wall erodes, at what rate, in how long — and why this number can carry a decision.",
        numbers=[("1.05–1.49×", "of the published experiment, inside the factor-2 band practice accepts"),
                 ("50.6°", "computed peak, against 45° measured"),
                 ("32 cases", "from CAD to trained model, in 22.6 min")],
        cover_img="img/erosao-card.webp",
        cover_alt="Wall erosion map on a 90° bend, rate in mm/year",
        meta=["Document ERC-04 · version 1.0 · 2026",
              "Demonstration case (public geometry and conditions, no client data)",
              "Reference experiment: Vieira et al. (2016), open data",
              "PINNeAPPle · LAIS &amp; YAN LTDA · pinneapple-labs.github.io"],
        short="ERC-04 · erosion in a 90° bend",
        foot="example report",
        pages=[
            ("1 · the request", [
                ("lead", "A 50 mm 90° bend carries sand-laden air. The question was not “how much erodes”: it was <b>when the wall reaches the minimum thickness</b> and <b>whether changing the bend radius moves the answer enough to justify the work</b>."),
                ("h3", "Contracted scope"),
                ("table", ["Deliverable", "What it contains"], [
                    ["Erosion map", "Wall rate (mm/year) across the geometry, with the peak position"],
                    ["Service life", "Years to the minimum thickness, at the critical point"],
                    ["Verification", "Comparison with a published experiment, and the choice of erosion model justified"],
                    ["Surrogate model", "Answers in seconds for new flow rates and bend radii"],
                    ["Limits", "What is not proven and what needs a test"],
                ], ["38%", None]),
                ("h3", "Out of scope"),
                ("p", "Mechanical design of the pipe, material selection, field inspection, experimental testing. The study delivers the number and the proof; the engineering decision and the purchase stay with whoever hires us."),
                ("callout", "gold", "How to read this document.", "Every number appears with the reference it was checked against — a published experiment, an independent solver or a mesh study. Numbers without a reference do not enter the report: they stay on the limits page, as an open question."),
                ("h3", "Assumptions that move the answer"),
                ("bullets", [
                    "The sand rate is the one in the scenario; a particle surge moves the result more than the mesh.",
                    "The wall is carbon steel; another material changes the erosion coefficient, not the impact distribution.",
                    "The flow is steady at the evaluated operating point; transients (starts, water hammer) are not covered.",
                ]),
            ]),
            ("2 · input data", [
                ("p", "This is the demonstration case form — in a client study these fields come from the CAD, the process sheet and the operating history."),
                ("table", ["Item", "Value", "Source"], [
                    ["Geometry", '<span class="mono">90° bend, D = 50 mm</span>', "10·D upstream and 20·D downstream"],
                    ["Fluid", '<span class="mono">air at 20 °C · ρ = 1.204 kg/m³ · µ = 1.825·10⁻⁵ Pa·s</span>', "fluid catalogue"],
                    ["Particles", '<span class="mono">quartz · ρp = 2,650 kg/m³ · dp = 150 µm</span>', "Fs = 0.53 · ṁp = 10⁻⁴ kg/s"],
                    ["Wall", '<span class="mono">carbon steel · 7,800 kg/m³ · HB 150</span>', "5 → 2 mm · 8,760 h/year"],
                    ["Reference point", '<span class="mono">U = 20 m/s · R/D = 1.5</span>', "base case for the map and the mesh study"],
                    ["Campaign", '<span class="mono">32 points · Sobol</span>', "U from 10 to 30 m/s · R/D from 1.5 to 5"],
                ], ["16%", "46%", None]),
                ("callout", "cyan", "Study rule:", "the validity range is declared before the run. Outside U = 10–30 m/s or R/D = 1.5–5 the surrogate says it is extrapolating — and the number loses its guarantee."),
                ("h3", "How the method was built"),
                ("table", ["Step", "Choice"], [
                    ["Mesh", 'Hexahedral, script-generated (<span class="mono">classy_blocks</span>), 10,400 cells, y⁺ target 50, <span class="mono">checkMesh</span> passed'],
                    ["Flow", '<span class="mono">simpleFoam</span>, k-ω SST, 109 iterations to converge, mass balance 3.5·10⁻⁶'],
                    ["Particles", '<span class="mono">icoUncoupledKinematicParcelFoam</span>, 2,000 parcels (4,000 in the statistical test)'],
                    ["Erosion", "DNV-RP-O501 impact model applied to the wall impacts; E/CRC and Finnie as cross-checks"],
                    ["Case convergence", "26 s wall-clock on 4 cores · 14 to 17 thousand wall impacts"],
                ], ["30%", None]),
            ]),
            ("3 · verification", [
                ("lead", "Before reporting an erosion rate, the model had to reproduce an experiment it had never seen: the Vieira et al. (2016) bend, D = 76.2 mm, R/D = 1.5, 150 µm sand, at three velocities."),
                ("table", ["Test", "U (m/s)", "Measured (mm/year)", "Computed (mm/year)", "Ratio", "Factor 2"], [
                    ["T1", "11", "6.5", "6.8", "1.05×", '<span class="verdict v-ok">passed</span>'],
                    ["T3", "15", "13.2", "16.9", "1.28×", '<span class="verdict v-ok">passed</span>'],
                    ["T5", "23", "36.2", "53.8", "1.49×", '<span class="verdict v-ok">passed</span>'],
                    ["peak position", "—", "45°", "50.6°", "+5.6°", '<span class="verdict v-ok">passed</span>'],
                ]),
                ("small", "150 µm sand in all three tests. Ratios and positions computed with the DNV-RP-O501 impact model, on the study mesh. Measured: Khan et al. (2023); peak position: Khan et al. (2022)."),
                ("callout", "gold", "Why this matters.", "Erosion is not a 1%-precision phenomenon: it depends on the particle distribution, the material and the operating history. Design practice accepts a factor of 2. The commitment is to land inside the band <b>and say where in the band</b>."),
                ("h3", "The other models were tested and rejected"),
                ("table", ["Erosion model", "Against the three tests", "Reading"], [
                    ["DNV-RP-O501 (impact)", "1.05–1.49×", '<span class="verdict v-ok">adopted</span> inside factor 2 at all three'],
                    ["E/CRC", "1.98–2.5× above", '<span class="verdict v-fail">rejected</span> leaves the band at all three'],
                    ["Finnie", "~28× above", '<span class="verdict v-fail">rejected</span> wrong order of magnitude'],
                    ["DNV §8.4 closed form (no CFD)", "97–100× below in 2 of 3", '<span class="verdict v-fail">rejected</span> depends on factor G, which ranges 0.02 to 1'],
                ], ["34%", "26%", None]),
                ("callout", "cyan", "What is not proven yet.", "The erosion constants of all three models come from secondary sources (the original experiment is paywalled). The verification above is the best evidence available today, declared as such — not as definitive validation."),
            ]),
            ("4 · result", [
                ("h3", "First the experiment, solved: T3, 15 m/s"),
                ("figure", "img/erosao.jpg", "Wall erosion map for test T3: the whole pipe and the zoom into the bend, with the peak on the outer wall just after the bend entry. Scale in mm/year."),
                ("p", "The maximum is not in the middle of the bend: it is on the outer wall, 50.6° after the entry (the experiment measures 45°). That is the point inspection must measure first — and the one that sets the life of the rest of the line."),
                ("h3", "Then the design case: U = 20 m/s, R/D = 1.5"),
                ("table", ["Erosion model", "Peak rate (mm/year)", "Life 5 → 2 mm"], [
                    ["DNV-RP-O501 (adopted)", "1.47", "2.0 years"],
                    ["E/CRC", "2.83", "1.1 years"],
                    ["Finnie (cross-check)", "23.8", "0.13 year"],
                    ["DNV §8.4 closed form (no CFD)", "0.037", "81 years"],
                ], ["40%", None, None]),
                ("callout", "gold", "What the decision needs to know:", "with the verified model, projected life is <b>2 years</b> at the critical point. The closed form without CFD would say 81 years for the same geometry. The difference is not precision: it is the choice between “planned replacement” and “no action”."),
            ]),
            ("5 · surrogate model", [
                ("lead", "Thirty-two cases covering U from 10 to 30 m/s and R/D from 1.5 to 5 were solved in CFD and used to train a model that answers in seconds. All 32 finished without rejection, in 22.6 min wall-clock (1.94 CPU-hours)."),
                ("table", ["Indicator", "Reference without AI", "Validation", "Test", "Out of range"], [
                    ["Pressure drop (ΔP)", "Darcy + Colebrook", "0.7%", "1.0%", "0.4%"],
                    ["Peak erosion rate", "DNV §8.4", "15.7%", "10.6%", "19.7%"],
                ], ["32%", None, None, None, None]),
                ("small", "Mean relative error. The bootstrap confidence interval was not computed: there are 9 test and out-of-range points, and the criterion requires at least 10."),
                ("h3", "What it is for"),
                ("bullets", [
                    "Varying diameter, bend radius and flow rate no longer costs a day per point.",
                    "Service life stops being a single number and becomes a curve against flow rate.",
                    "Outside the training range the model says it is extrapolating, with the measured 19.7% error.",
                ]),
                ("callout", "cyan", "What the surrogate does not do:", "replace the experiment. It reproduces the CFD inside the trained range — if the CFD is wrong for your case, the surrogate is wrong with it, faster."),
            ]),
            ("6 · limits", [
                ("lead", "This page exists because a number without its limits is an opinion with decimal places. Everything that did not pass an external reference is here."),
                ("table", ["Item", "State", "Practical consequence"], [
                    ["Campaign mesh", '<span class="verdict v-fail">coarse</span>', "10,400 cells: ~30% high on ΔP and ~40% low on erosion, against the extrapolated fine-mesh value"],
                    ["Mesh convergence (GCI)", '<span class="verdict v-fail">off target</span>', "ΔP at 6.8–12.6% GCI on the fine mesh (target 5%); erosion converges only at the reference point (2.9%)"],
                    ["Erosion constants", '<span class="verdict v-fail">secondary source</span>', "DNV, E/CRC and Finnie come from secondary literature; the original experiment is paywalled"],
                    ["Fields sent to verification", '<span class="verdict v-fail">6 checks did not run</span>', "11 for, 0 against, 65% coverage"],
                    ["Surrogate interpolation", '<span class="verdict v-ok">measured</span>', "1.0% on ΔP and 10.6% on erosion, at points held out of training"],
                    ["Surrogate extrapolation", '<span class="verdict v-fail">warned, not guaranteed</span>', "outside U 10–30 m/s or R/D 1.5–5 the error rises (19.7%)"],
                ], ["30%", "22%", None]),
                ("callout", "gold", "House rule.", "A coarse-mesh result counts as a demonstration of the pipeline, not as a client number. This document is public for exactly that reason."),
                ("h3", "What would take this number up a level"),
                ("bullets", ["Campaign on the fine mesh, with GCI inside 5% for erosion as well.",
                             "Our own test, or buying the original experiment, to replace the secondary constants.",
                             "Sending the full fields to verification, closing the six checks that did not run."]),
            ]),
            ("7 · conclusion", [
                ("kpi", [("1.47", "mm/year at the critical point"), ("2.0", "years to 5 → 2 mm"),
                         ("50.6°", "peak position in the bend"), ("1.0%", "surrogate error on ΔP")]),
                ("h3", "Recommendation"),
                ("p", "Inspect the outer wall just after the bend entry, not the middle of the bend. With the verified rate and the adopted minimum thickness, the planned-replacement window is two years — and the surrogate lets you test, in seconds, whether a larger radius buys more time than a material change."),
                ("h3", "What this study does not decide"),
                ("p", "Which material to buy, which supplier to pick, when to stop the plant. It delivers the rate, the position and the error; the economic decision uses those numbers together with downtime cost and pipe price."),
                ("h3", "Provenance"),
                ("table", ["What", "Where"], [
                    ["Reference experiment", "Vieira et al. (2016), E/CRC Tulsa · open table in Khan et al. (2023), <i>Eng. Proc.</i> 45:28"],
                    ["Measured peak position", "Khan et al. (2022), <i>Materials</i> 15:3721"],
                    ["Public article of the study", '<span class="mono">pinneapple-labs.github.io/artigos/erosao-curva-90/</span>'],
                    ["Code and case", '<span class="mono">github.com/PINNeAPPle-Labs/PINNeAPPle-CFD · casos/cfd04-curva-areia</span>'],
                ], ["30%", None]),
                ("callout", "cyan", "This is an example report,", "built on a demonstration case with public geometry and conditions. A study for your plant follows the same structure, with the same limits page."),
            ]),
        ],
    ),
}

# --- HX-201: digital twin of a fouled exchanger ---------------------------
REPORTS["gemeo-hx201"] = {
    "pt": dict(
        html_lang="pt-BR",
        doc_title="Gêmeo digital HX-201 — PINNeAPPle",
        eyebrow="Relatório de estudo · exemplo público",
        title="Gêmeo digital HX-201<br />permutador com incrustação",
        sub="Um contrato de acurácia assinado antes da operação — e o que aconteceu quando a incrustação apareceu.",
        numbers=[("0,216 °C", "de RMSE contra a sonda reservada"),
                 ("95,5%", "de cobertura da banda, calibrada fora do treino"),
                 ("2,6 h", "de antecedência no alarme, com o erro da previsão")],
        cover_img="img/twin.jpg",
        cover_alt="Gêmeo digital de um ativo em 3D com painel de leitura ao vivo",
        meta=["Documento TW-201 · versão 1.0 · 2026",
              "Histórico sintético de demonstração: não é registro de comissionamento de planta",
              "Referência: sonda TT-105, reservada e fora do filtro",
              "PINNeAPPle · LAIS &amp; YAN LTDA · pinneapple-labs.github.io"],
        short="TW-201 · gêmeo do permutador HX-201",
        foot="relatório de exemplo",
        pages=[
            ("1 · o pedido", [
                ("lead", "Um permutador casco-e-tubo perde eficiência com incrustação. A operação não quer previsão: quer saber <b>quanto tempo tem</b> até a carga a jusante não fechar."),
                ("p", "O risco de um gêmeo não é errar a previsão — é ser ouvido sem merecer. Por isso o estudo começa por um contrato escrito antes de qualquer dado: as métricas, as faixas e os limites que o modelo precisa cumprir para existir."),
                ("h3", "O que foi contratado"),
                ("bullets", [
                    "Modelo <span class=\"mono\">exchanger-ntu 1.0</span>, com piso de acurácia declarado de 1 °C.",
                    "Gates de aceitação: RMSE ≤ 2,5% do span, viés ≤ 1%, cobertura ≥ 90%, antecedência de alarme ≥ 1 h.",
                    "Uma sonda redundante (TT-105) que nunca entra no filtro: ela é o juiz.",
                    "Faixa de validade declarada em contrato: T de 80 a 110 °C e ṁ de 0,5 a 2,0 kg/s.",
                ]),
                ("callout", "gold", "A ordem importa.", "O contrato é assinado antes do primeiro passo do filtro. Métrica escolhida depois de ver o resultado não é métrica: é desculpa."),
            ]),
            ("2 · o contrato", [
                ("h3", "Grandezas previstas e limites de processo"),
                ("table", ["Grandeza", "Faixa", "Limite de processo"], [
                    ["T_ho (saída quente)", "35–75 °C", "alarme acima de 60,0 °C"],
                    ["T_co (saída fria)", "45–75 °C", "alarme abaixo de 57,8 °C"],
                    ["R_f (incrustação)", "0–0,0025 m²K/W", "sem limite de engenharia declarado"],
                ], ["34%", None, None]),
                ("h3", "Sensores"),
                ("table", ["Papel", "Sensores", "Uso"], [
                    ["Entradas (ponto de operação)", "TT-101, TT-102, FT-101, FT-102", "movem o modelo"],
                    ["Assimilados", "TT-103, TT-104", "entram no filtro, ruído 0,15 °C"],
                    ["Reservado", "TT-105", "só compara; nunca entra no filtro"],
                ], ["34%", None, None]),
                ("h3", "Gates de aceitação"),
                ("table", ["Gate", "Critério", "Por quê"], [
                    ["RMSE", "≤ 2,5% do span de 40 °C", "≈ 1 °C, o mesmo piso de acurácia do modelo"],
                    ["Viés", "≤ 1%", "erro sistemático não pode se esconder na média"],
                    ["Cobertura da banda", "≥ 90%", "a banda tem de conter o que acontece"],
                    ["Antecedência do alarme", "≥ 3.600 s", "aviso inútil não é aviso"],
                ], ["30%", "28%", None]),
                ("callout", "cyan", "Faixa de validade:", "T de 80 a 110 °C e ṁ de 0,5 a 2,0 kg/s. Fora dela o gêmeo não promete nada — e o relatório diz isso em vez de extrapolar em silêncio."),
            ]),
            ("3 · o resultado", [
                ("lead", "852 passos, 255.300 s (70,9 h) na janela de validação. As métricas são calculadas só na parte que não foi usada para calibrar a banda."),
                ("kpi", [("0,216 °C", "RMSE contra a sonda reservada"), ("0,168 °C", "erro absoluto médio"),
                         ("0,432 °C", "p95 do erro absoluto"), ("−0,010 °C", "viés")]),
                ("table", ["Gate", "Critério", "Obtido", "Situação"], [
                    ["RMSE", "≤ 2,5% do span", "0,54% do span", '<span class="verdict v-ok">passa</span>'],
                    ["Viés", "≤ 1%", "−0,026% do span", '<span class="verdict v-ok">passa</span>'],
                    ["Cobertura", "≥ 90%", "95,5%", '<span class="verdict v-ok">passa</span>'],
                    ["Antecedência do alarme", "≥ 3.600 s", "9.300 s", '<span class="verdict v-ok">passa</span>'],
                ], ["30%", None, None, None]),
                ("p", "A incrustação estimada ao fim da janela foi de <b>0,001652 m²K/W</b>, contra 0,001637 do valor verdadeiro do cenário — 0,9% de diferença. É a variável que a operação não mede e que o gêmeo passa a estimar."),
                ("callout", "gold", "O juiz é externo.", "A sonda TT-105 ficou fora do filtro durante todo o comissionamento. A métrica que aparece aqui é a distância entre o modelo e uma medição que ele nunca viu."),
            ]),
            ("4 · a banda, o alarme e o que não está provado", [
                ("p", "A banda de incerteza não é um intervalo de previsão: é uma banda de estado, e foi calibrada uma única vez numa janela separada (os primeiros 127.500 s), depois avaliada no resto. A escala aplicada foi ×1,336; sem ela, a banda bruta do ensemble cobriria 86,4% — abaixo do gate de 90%."),
                ("p", "Isso está declarado no relatório, não escondido: uma banda que só funciona depois de ajustada é uma banda ajustada, e quem lê precisa saber disso para decidir o que fazer com ela."),
                ("h3", "O alarme"),
                ("table", ["Indicador", "Valor", "Leitura"], [
                    ["Antecedência do alarme", "9.300 s (2,6 h)", "tempo entre o aviso e o cruzamento do limite"],
                    ["Erro da previsão do cruzamento", "3.900 s (1,1 h)", "distância entre o instante previsto e o medido"],
                    ["Origem da antecedência", "extrapolação linear do estado latente", "cresce com qualquer mudança de regime"],
                ], ["36%", "28%", None]),
                ("callout", "cyan", "Regra da casa.", "Antecedência sem erro declarado é chute com relógio. O número que a operação usa é o par: 2,6 h de aviso, com 1,1 h de erro na hora do cruzamento."),
                ("h3", "O que não está provado"),
                ("table", ["Item", "O que o relatório diz"], [
                    ["A banda é de estado", "não é intervalo de previsão para mudança de regime"],
                    ["Comissionado só na faixa declarada", "fora de T 80–110 °C ou ṁ 0,5–2,0 kg/s, nenhuma promessa"],
                    ["Primeiros 12 quadros", "assimilados, mas excluídos das métricas"],
                    ["Sem antecedência para R_f", "nenhum limite de engenharia foi declarado para a incrustação"],
                    ["Histórico sintético", "demonstração; não é registro de comissionamento de planta"],
                    ["Sem reajuste", "é o gêmeo como foi entregue, não um modelo retreinado depois"],
                ], ["30%", None]),
                ("callout", "gold", "Por que publicar os limites de um gêmeo.", "Porque o valor dele é justamente ser auditable: um modelo que declara onde não vale pode ser usado; um que não declara não pode."),
            ]),
            ("5 · conclusão", [
                ("kpi", [("95,5%", "cobertura da banda"), ("0,216 °C", "RMSE contra a sonda"),
                         ("2,6 h", "de antecedência no alarme"), ("0,001652", "m²K/W de incrustação estimada")]),
                ("h3", "O que a operação faz com isso"),
                ("p", "Antecedência é tempo para planejar limpeza, negociar uma janela de parada ou ajustar carga. O gêmeo não decide nada: ele avisa, e diz com que erro está avisando."),
                ("h3", "O que este estudo não decide"),
                ("p", "O momento econômico da parada, o fornecedor da limpeza e o custo da perda de carga. Ele entrega a estimativa de incrustação e a janela de aviso; o resto é decisão de operação."),
                ("h3", "Proveniência"),
                ("table", ["O que", "Onde"], [
                    ["Contrato de acurácia", '<span class="mono">PINNeAPPle/apps/twin_ops/spec_hx201.yaml</span>'],
                    ["Evidência do comissionamento", '<span class="mono">twin_evidence_hx201.json</span> · spec 6b86712f52ed2644'],
                    ["Pré-condições", "11 verificações de preflight, 11 aprovadas"],
                    ["Artigo público", '<span class="mono">pinneapple-labs.github.io/artigos/gemeo-hx201/</span>'],
                ], ["30%", None]),
                ("callout", "cyan", "Este é um relatório de exemplo,", "com histórico sintético de demonstração. Um gêmeo para a sua planta segue a mesma estrutura: contrato antes, sonda reservada como juiz e a mesma página de limites."),
            ]),
        ],
    ),
    "en": dict(
        html_lang="en",
        doc_title="HX-201 digital twin — PINNeAPPle",
        eyebrow="Study report · public example",
        title="HX-201 digital twin<br />a fouled heat exchanger",
        sub="An accuracy contract signed before operation — and what happened when the fouling showed up.",
        numbers=[("0.216 °C", "of RMSE against the held-out probe"),
                 ("95.5%", "band coverage, calibrated outside training"),
                 ("2.6 h", "of alarm lead time, with the forecast error")],
        cover_img="img/twin.jpg",
        cover_alt="Digital twin of an asset in 3D with a live reading panel",
        meta=["Document TW-201 · version 1.0 · 2026",
              "Synthetic demonstration history: not a plant commissioning record",
              "Reference: probe TT-105, held out of the filter",
              "PINNeAPPle · LAIS &amp; YAN LTDA · pinneapple-labs.github.io"],
        short="TW-201 · HX-201 exchanger twin",
        foot="example report",
        pages=[
            ("1 · the request", [
                ("lead", "A shell-and-tube exchanger loses efficiency to fouling. Operations does not want a forecast: it wants to know <b>how much time it has</b> before the downstream load stops closing."),
                ("p", "The risk of a twin is not getting the forecast wrong — it is being heard without deserving it. So the study starts with a contract written before any data: the metrics, the ranges and the limits the model must meet in order to exist."),
                ("h3", "What was contracted"),
                ("bullets", [
                    'Model <span class="mono">exchanger-ntu 1.0</span>, with a declared accuracy floor of 1 °C.',
                    "Acceptance gates: RMSE ≤ 2.5% of span, bias ≤ 1%, coverage ≥ 90%, alarm lead ≥ 1 h.",
                    "A redundant probe (TT-105) that never enters the filter: it is the judge.",
                    "Validity range declared in the contract: T from 80 to 110 °C and ṁ from 0.5 to 2.0 kg/s.",
                ]),
                ("callout", "gold", "Order matters.", "The contract is signed before the first filter step. A metric chosen after seeing the result is not a metric: it is an excuse."),
            ]),
            ("2 · the contract", [
                ("h3", "Predicted fields and process limits"),
                ("table", ["Field", "Range", "Process limit"], [
                    ["T_ho (hot outlet)", "35–75 °C", "alarm above 60.0 °C"],
                    ["T_co (cold outlet)", "45–75 °C", "alarm below 57.8 °C"],
                    ["R_f (fouling)", "0–0.0025 m²K/W", "no engineering limit declared"],
                ], ["34%", None, None]),
                ("h3", "Sensors"),
                ("table", ["Role", "Sensors", "Use"], [
                    ["Inputs (operating point)", "TT-101, TT-102, FT-101, FT-102", "drive the model"],
                    ["Assimilated", "TT-103, TT-104", "enter the filter, noise 0.15 °C"],
                    ["Held out", "TT-105", "only compares; never enters the filter"],
                ], ["34%", None, None]),
                ("h3", "Acceptance gates"),
                ("table", ["Gate", "Criterion", "Why"], [
                    ["RMSE", "≤ 2.5% of the 40 °C span", "≈ 1 °C, the model's own accuracy floor"],
                    ["Bias", "≤ 1%", "systematic error cannot hide in the mean"],
                    ["Band coverage", "≥ 90%", "the band has to contain what happens"],
                    ["Alarm lead", "≥ 3,600 s", "a warning that arrives late is not a warning"],
                ], ["30%", "28%", None]),
                ("callout", "cyan", "Validity range:", "T from 80 to 110 °C and ṁ from 0.5 to 2.0 kg/s. Outside it the twin promises nothing — and the report says so instead of extrapolating quietly."),
            ]),
            ("3 · the result", [
                ("lead", "852 steps, 255,300 s (70.9 h) in the validation window. Metrics are computed only on the part that was not used to calibrate the band."),
                ("kpi", [("0.216 °C", "RMSE against the held-out probe"), ("0.168 °C", "mean absolute error"),
                         ("0.432 °C", "p95 of absolute error"), ("−0.010 °C", "bias")]),
                ("table", ["Gate", "Criterion", "Achieved", "Status"], [
                    ["RMSE", "≤ 2.5% of span", "0.54% of span", '<span class="verdict v-ok">passes</span>'],
                    ["Bias", "≤ 1%", "−0.026% of span", '<span class="verdict v-ok">passes</span>'],
                    ["Coverage", "≥ 90%", "95.5%", '<span class="verdict v-ok">passes</span>'],
                    ["Alarm lead", "≥ 3,600 s", "9,300 s", '<span class="verdict v-ok">passes</span>'],
                ], ["30%", None, None, None]),
                ("p", "Fouling estimated at the end of the window was <b>0.001652 m²K/W</b>, against 0.001637 in the scenario's true value — 0.9% apart. It is the variable operations cannot measure and that the twin starts estimating."),
                ("callout", "gold", "The judge is external.", "Probe TT-105 stayed out of the filter for the whole commissioning. The metric shown here is the distance between the model and a measurement it never saw."),
            ]),
            ("4 · the band, the alarm and what is not proven", [
                ("p", "The uncertainty band is not a prediction interval: it is a state band, calibrated once on a separate window (the first 127,500 s) and then scored on the rest. The scale applied was ×1.336; without it, the raw ensemble band would cover 86.4% — below the 90% gate."),
                ("p", "That is stated in the report, not hidden: a band that only works after being scaled is a scaled band, and the reader needs to know that to decide what to do with it."),
                ("h3", "The alarm"),
                ("table", ["Indicator", "Value", "Reading"], [
                    ["Alarm lead", "9,300 s (2.6 h)", "time between the warning and the limit crossing"],
                    ["Crossing forecast error", "3,900 s (1.1 h)", "distance between the predicted and the measured instant"],
                    ["Where the lead comes from", "linear extrapolation of the latent state", "it grows with any change of regime"],
                ], ["36%", "28%", None]),
                ("callout", "cyan", "House rule.", "Lead time without a stated error is a guess with a clock. The number operations uses is the pair: 2.6 h of warning, with 1.1 h of error on the crossing."),
                ("h3", "What is not proven"),
                ("table", ["Item", "What the report says"], [
                    ["The band is a state band", "not a prediction interval for a change of regime"],
                    ["Commissioned inside the declared range only", "outside T 80–110 °C or ṁ 0.5–2.0 kg/s, no claim"],
                    ["First 12 frames", "assimilated, but excluded from the metrics"],
                    ["No lead time for R_f", "no engineering limit was declared for fouling"],
                    ["Synthetic history", "a demonstration; not a plant commissioning record"],
                    ["No re-fit", "this is the twin as shipped, not a model retrained later"],
                ], ["30%", None]),
                ("callout", "gold", "Why publish a twin's limits.", "Because its value is being auditable: a model that declares where it does not hold can be used; one that does not, cannot."),
            ]),
            ("5 · conclusion", [
                ("kpi", [("95.5%", "band coverage"), ("0.216 °C", "RMSE against the probe"),
                         ("2.6 h", "of alarm lead"), ("0.001652", "m²K/W estimated fouling")]),
                ("h3", "What operations does with it"),
                ("p", "Lead time is time to plan a cleaning, negotiate a shutdown window or shift load. The twin decides nothing: it warns, and states the error it is warning with."),
                ("h3", "What this study does not decide"),
                ("p", "The economic moment of the shutdown, the cleaning vendor and the cost of lost head. It delivers the fouling estimate and the warning window; the rest is an operations decision."),
                ("h3", "Provenance"),
                ("table", ["What", "Where"], [
                    ["Accuracy contract", '<span class="mono">PINNeAPPle/apps/twin_ops/spec_hx201.yaml</span>'],
                    ["Commissioning evidence", '<span class="mono">twin_evidence_hx201.json</span> · spec 6b86712f52ed2644'],
                    ["Preconditions", "11 preflight checks, 11 passed"],
                    ["Public article", '<span class="mono">pinneapple-labs.github.io/artigos/gemeo-hx201/</span>'],
                ], ["30%", None]),
                ("callout", "cyan", "This is an example report,", "on a synthetic demonstration history. A twin for your plant follows the same structure: contract first, held-out probe as judge, and the same limits page."),
            ]),
        ],
    ),
}

# --- CFD-08: globe valve, methane 80 → 60 bar ----------------------------
REPORTS["valvula-globo"] = {
    "pt": dict(
        html_lang="pt-BR",
        doc_title="Válvula globo, metano 80 → 60 bar — PINNeAPPle",
        eyebrow="Relatório de estudo · exemplo público",
        title="Válvula globo<br />metano 80 → 60 bar",
        sub="O que o documento do cliente dizia, o que o CFD diz — e o que ainda não fecha.",
        numbers=[("2,042 kg/s", "de vazão mássica no ponto de operação"),
                 ("Mach 0,525", "contra 0,904 do caso original, acima do teto isentrópico"),
                 ("15,28 bar", "de queda de pressão estática, com 5 checagens aprovadas")],
        cover_img=None,
        cover_alt="",
        meta=["Documento VR-08 · versão 1.0 · 2026",
              "Caso de cliente anonimizado: geometria e condições de processo preservadas, identidade não",
              "OpenFOAM v2606 · Peng-Robinson · rhoPimpleFoam em tempo físico",
              "PINNeAPPle · LAIS &amp; YAN LTDA · pinneapple-labs.github.io"],
        short="VR-08 · válvula globo, 80 → 60 bar",
        foot="relatório de exemplo",
        pages=[
            ("1 · o que chegou", [
                ("lead", "Chegou um documento com a simulação de uma válvula globo em Ansys Fluent, cujos resultados, nas palavras de quem enviou, “não apresentam um resultado físico coerente”, junto com o CAD da peça."),
                ("p", "Antes de rodar qualquer coisa, o caso original foi diagnosticado. Quatro números dele se negam entre si:"),
                ("table", ["#", "Achado", "O número", "Por que não fecha"], [
                    ["1", "o tempo físico", '<span class="mono">300 × 1e-7 s = 30 µs</span>', "a travessia acústica do corpo é ≈ 0,83 ms: a simulação parou em 3,6% de uma travessia"],
                    ["2", "o regime", '<span class="mono">Mach 0,904</span>', "com 80 → 60 bar o teto isentrópico é 0,674; Mach 0,904 exigiria a saída em 48,3 bar"],
                    ["3", "a temperatura", '<span class="mono">209 a 367 K</span>', "a laminação isentálpica dá −8,12 K; 209 K exigiriam Mach 1,4"],
                    ["4", "a geometria", "obturador a 4 mm da sede", "o CAD mostra a folga, e o campo não é o de uma abertura de 4 mm"],
                ], ["5%", "22%", "26%", None]),
                ("callout", "gold", "Veredito em uma linha.", "O diagnóstico do caso original é conclusivo e não precisou de CFD: ele parou antes de o campo existir. O que veio depois é o campo resolvido em tempo físico, com números na faixa física certa."),
            ]),
            ("2 · o que foi medido", [
                ("p", "Pipeline genérico de passagem compressível da plataforma, sem código escrito para este caso."),
                ("table", ["Item", "Valor"], [
                    ["Domínio", "3-D, construído do CAD: dois bocais Ø20, corpo esférico R29, pescoço, haste, anel da sede e obturador"],
                    ["Malha", '<span class="mono">snappyHexMesh</span>, 16.010 células hexa-dominantes, não-ortogonalidade 41°/10,4°, <span class="mono">checkMesh</span> aprovado, 137,3 cm³'],
                    ["Solver", '<span class="mono">rhoPimpleFoam</span> (OpenFOAM v2606) em tempo físico, 3.191 passos até t = 27,5 ms (≈ 33 travessias acústicas)'],
                    ["Entrada / saída", 'estagnação 80 bar (<span class="mono">totalPressure</span>) · 60 bar estáticos na saída'],
                    ["Média", '<span class="mono">fieldAverage</span> no último quarto da janela'],
                ], ["26%", None]),
                ("table", ["Grandeza", "Valor"], [
                    ["Vazão mássica", '<span class="mono">2,042 kg/s</span> (7.351 kg/h) · 131,1 m³/h'],
                    ["Pressão estática na entrada", '<span class="mono">75,28 bar</span> (a estagnação imposta é 80 bar; a diferença é a carga dinâmica)'],
                    ["Kv (IEC 60534-2-1)", '<span class="mono">7,95</span> contra 8,84 da correlação (desvio 10%; Cd no gargalo 0,497)'],
                    ["Temperatura na saída · ΔT", '<span class="mono">292,85 K</span> · −7,15 K (isentálpico: −7,45 K)'],
                    ["Mach máximo · u máxima", '<span class="mono">0,525</span> · 232,0 m/s'],
                    ["Densidade na entrada", '<span class="mono">56,12 kg/m³</span>, igual ao Peng-Robinson a 0,10% (gás ideal daria 48,42)'],
                ], ["26%", None]),
                ("h3", "Por que a pressão sobe em rampa"),
                ("p", "Um passo único de 80 bar sobre um domínio parado não fecha: a primeira correção de pressão sobre-acelera, o gás expande localmente abaixo da pressão de saída e a inversão T(h) do Peng-Robinson estoura. O caso sobe a estagnação em estágios — 62 → 66 → 70 → 74 → 77 → 80 bar —, cada um aquecido pelo campo do anterior, com esquema progressivamente menos difusivo."),
            ]),
            ("3 · as checagens, e o que ainda não fecha", [
                ("table", ["Checagem", "Resultado", "Situação"], [
                    ["Malha (<span class=\"mono\">checkMesh</span>)", "aprovado", '<span class="verdict v-ok">passa</span>'],
                    ["Solver chegou ao fim do tempo físico", "sim", '<span class="verdict v-ok">passa</span>'],
                    ["Regime não afogado (p₂/p₁ = 0,803 > 0,545)", "sim", '<span class="verdict v-ok">passa</span>'],
                    ["Densidade contra Peng-Robinson", "0,01%", '<span class="verdict v-ok">passa</span>'],
                    ["Kv contra IEC 60534-2-1", "9,62 contra 10,67 (Cd 0,601)", '<span class="verdict v-ok">passa</span>'],
                    ["Conservação de massa", "0,22% (critério 0,1%)", '<span class="verdict v-fail">sem referência</span>'],
                    ["Joule-Thomson contra isentálpico", "−7,15 K contra −7,45 K (tolerância 1 K)", '<span class="verdict v-mid">sem referência</span>'],
                    ["Entalpia de estagnação", "+1,20% (critério 1%)", '<span class="verdict v-fail">sem referência</span>'],
                    ["Resultado do documento original", "ver seção 1", '<span class="verdict v-fail">falha</span>'],
                ], ["42%", "36%", None]),
                ("callout", "gold", "O que interessa aqui.", "Cinco checagens aprovadas não escondem três que não fecham. As duas falhas de física têm a mesma origem provável — a cortina da sede com ~2 células na radial — e vêm com o próximo passo nomeado."),
                ("h3", "O que ainda não fecha"),
                ("table", ["Item", "Estado", "Consequência"], [
                    ["Cortina da sede", "~2 células na radial (célula de 2 mm numa abertura de 4 mm)", "explica o Kv 10% abaixo da correlação e o resíduo de 1,2% na entalpia"],
                    ["Janela de média", "27,5 ms, 33 travessias acústicas", "o critério de 0,1% na massa pede janela maior (~25 min por dobra)"],
                    ["Oscilação do campo", "não medida", "16 instantâneos guardados entre 27,7 e 31,5 ms esperam a série temporal"],
                    ["Varrido de abertura", "não feito", "só depois de a malha da sede estabilizar"],
                ], ["24%", "30%", None]),
                ("callout", "cyan", "Regra da casa.", "Um número com três checagens abertas continua sendo útil — desde que as três apareçam. Este relatório é a diferença entre “o CFD disse” e “o CFD disse, e aqui está o que ele não disse”."),
            ]),
            ("4 · conclusão", [
                ("kpi", [("2,042", "kg/s de vazão mássica"), ("0,525", "Mach máximo"),
                         ("−7,15", "K de queda de temperatura"), ("5/9", "checagens aprovadas")]),
                ("h3", "O que já dá para decidir"),
                ("p", "A vazão, a queda de pressão e o coeficiente de descarga na abertura avaliada estão na faixa física: Mach 0,525, densidade dentro de 0,10% do gás real e ΔT a 0,3 K da referência isentálpica. Para operação e para comparação de alternativas, esse número serve — com as ressalvas ao lado."),
                ("h3", "O que ainda não dá"),
                ("p", "A curva característica em função da abertura, e qualquer decisão de compra que dependa de Kv com precisão melhor que 10%. Para isso, a cortina da sede precisa de pelo menos 6 células na radial."),
                ("h3", "Proveniência"),
                ("table", ["O que", "Onde"], [
                    ["Registro técnico do caso", '<span class="mono">PINNeAPPle-CFD/casos/cfd08-valvula-globo/RELATORIO.md</span>'],
                    ["Pipeline usado", '<span class="mono">pinneapple_simulation.pipelines.compressible_internal</span>'],
                    ["Referência de Kv", "IEC 60534-2-1 · equação de estado Peng-Robinson"],
                    ["Identidade do cliente", "preservada fora deste documento; geometria e condições, mantidas"],
                ], ["30%", None]),
                ("callout", "cyan", "Este é um relatório de exemplo,", "de um caso de cliente anonimizado. Um estudo para a sua válvula segue a mesma estrutura: diagnóstico do que existe, campo em tempo físico, checagens com resultado e a página do que ainda não fecha."),
            ]),
        ],
    ),
    "en": dict(
        html_lang="en",
        doc_title="Globe valve, methane 80 → 60 bar — PINNeAPPle",
        eyebrow="Study report · public example",
        title="Globe valve<br />methane 80 → 60 bar",
        sub="What the client's document said, what the CFD says — and what still does not close.",
        numbers=[("2.042 kg/s", "of mass flow at the operating point"),
                 ("Mach 0.525", "against 0.904 in the original, above the isentropic ceiling"),
                 ("15.28 bar", "of static pressure drop, with 5 checks passed")],
        cover_img=None,
        cover_alt="",
        meta=["Document VR-08 · version 1.0 · 2026",
              "Anonymised client case: geometry and process conditions kept, identity not",
              "OpenFOAM v2606 · Peng-Robinson · rhoPimpleFoam in physical time",
              "PINNeAPPle · LAIS &amp; YAN LTDA · pinneapple-labs.github.io"],
        short="VR-08 · globe valve, 80 → 60 bar",
        foot="example report",
        pages=[
            ("1 · what arrived", [
                ("lead", "A document arrived with a globe valve simulated in Ansys Fluent whose results, in the sender's words, “do not present a coherent physical result”, together with the CAD of the part."),
                ("p", "Before running anything, the original case was diagnosed. Four of its numbers contradict each other:"),
                ("table", ["#", "Finding", "The number", "Why it does not hold"], [
                    ["1", "physical time", '<span class="mono">300 × 1e-7 s = 30 µs</span>', "the body's acoustic crossing is ≈ 0.83 ms: the run stopped at 3.6% of one crossing"],
                    ["2", "regime", '<span class="mono">Mach 0.904</span>', "with 80 → 60 bar the isentropic ceiling is 0.674; Mach 0.904 would need 48.3 bar at the outlet"],
                    ["3", "temperature", '<span class="mono">209 to 367 K</span>', "isenthalpic throttling gives −8.12 K; 209 K would need Mach 1.4"],
                    ["4", "geometry", "plug 4 mm from the seat", "the CAD shows the gap, and the field is not that of a 4 mm opening"],
                ], ["5%", "22%", "26%", None]),
                ("callout", "gold", "Verdict in one line.", "The diagnosis of the original case is conclusive and needed no CFD: it stopped before the field existed. What came next is the field solved in physical time, with numbers in the right physical range."),
            ]),
            ("2 · what was measured", [
                ("p", "The platform's generic compressible-passage pipeline, with no code written for this case."),
                ("table", ["Item", "Value"], [
                    ["Domain", "3-D, built from the CAD: two Ø20 nozzles, R29 spherical body, neck, stem, seat ring and plug"],
                    ["Mesh", '<span class="mono">snappyHexMesh</span>, 16,010 hex-dominant cells, non-orthogonality 41°/10.4°, <span class="mono">checkMesh</span> passed, 137.3 cm³'],
                    ["Solver", '<span class="mono">rhoPimpleFoam</span> (OpenFOAM v2606) in physical time, 3,191 steps to t = 27.5 ms (≈ 33 acoustic crossings)'],
                    ["Inlet / outlet", '80 bar stagnation (<span class="mono">totalPressure</span>) · 60 bar static at the outlet'],
                    ["Averaging", '<span class="mono">fieldAverage</span> over the last quarter of the window'],
                ], ["26%", None]),
                ("table", ["Quantity", "Value"], [
                    ["Mass flow", '<span class="mono">2.042 kg/s</span> (7,351 kg/h) · 131.1 m³/h'],
                    ["Static inlet pressure", '<span class="mono">75.28 bar</span> (imposed stagnation is 80 bar; the difference is dynamic head)'],
                    ["Kv (IEC 60534-2-1)", '<span class="mono">7.95</span> against 8.84 from the correlation (10% off; throat Cd 0.497)'],
                    ["Outlet temperature · ΔT", '<span class="mono">292.85 K</span> · −7.15 K (isenthalpic: −7.45 K)'],
                    ["Peak Mach · peak u", '<span class="mono">0.525</span> · 232.0 m/s'],
                    ["Inlet density", '<span class="mono">56.12 kg/m³</span>, within 0.10% of Peng-Robinson (ideal gas would give 48.42)'],
                ], ["26%", None]),
                ("h3", "Why the pressure ramps up"),
                ("p", "A single 80 bar step over a still domain does not close: the first pressure correction over-accelerates, the gas expands locally below the outlet pressure and the Peng-Robinson T(h) inversion blows up. The case raises stagnation in stages — 62 → 66 → 70 → 74 → 77 → 80 bar —, each warmed by the previous field, with a progressively less diffusive scheme."),
            ]),
            ("3 · the checks, and what still does not close", [
                ("table", ["Check", "Result", "Status"], [
                    ["Mesh (<span class=\"mono\">checkMesh</span>)", "passed", '<span class="verdict v-ok">passes</span>'],
                    ["Solver reached the end of physical time", "yes", '<span class="verdict v-ok">passes</span>'],
                    ["Regime not choked (p₂/p₁ = 0.803 > 0.545)", "yes", '<span class="verdict v-ok">passes</span>'],
                    ["Density against Peng-Robinson", "0.01%", '<span class="verdict v-ok">passes</span>'],
                    ["Kv against IEC 60534-2-1", "9.62 against 10.67 (Cd 0.601)", '<span class="verdict v-ok">passes</span>'],
                    ["Mass conservation", "0.22% (criterion 0.1%)", '<span class="verdict v-fail">no reference</span>'],
                    ["Joule-Thomson against isenthalpic", "−7.15 K against −7.45 K (tolerance 1 K)", '<span class="verdict v-mid">no reference</span>'],
                    ["Stagnation enthalpy", "+1.20% (criterion 1%)", '<span class="verdict v-fail">no reference</span>'],
                    ["Result of the original document", "see section 1", '<span class="verdict v-fail">fails</span>'],
                ], ["42%", "36%", None]),
                ("callout", "gold", "What matters here.", "Five passing checks do not hide three that do not close. The two physics failures share a likely cause — the seat curtain with ~2 cells radially — and come with the next step named."),
                ("h3", "What still does not close"),
                ("table", ["Item", "State", "Consequence"], [
                    ["Seat curtain", "~2 cells radially (2 mm cell in a 4 mm opening)", "explains the Kv 10% below the correlation and the 1.2% enthalpy residual"],
                    ["Averaging window", "27.5 ms, 33 acoustic crossings", "the 0.1% mass criterion needs a longer window (~25 min per doubling)"],
                    ["Field oscillation", "not measured", "16 snapshots between 27.7 and 31.5 ms wait for the time series"],
                    ["Opening sweep", "not done", "only after the seat mesh settles"],
                ], ["24%", "30%", None]),
                ("callout", "cyan", "House rule.", "A number with three open checks is still useful — as long as all three appear. This report is the difference between “the CFD said” and “the CFD said, and here is what it did not say”."),
            ]),
            ("4 · conclusion", [
                ("kpi", [("2.042", "kg/s of mass flow"), ("0.525", "peak Mach"),
                         ("−7.15", "K of temperature drop"), ("5/9", "checks passed")]),
                ("h3", "What can already be decided"),
                ("p", "Flow, pressure drop and discharge coefficient at the evaluated opening are in the physical range: Mach 0.525, density within 0.10% of real gas and ΔT 0.3 K from the isenthalpic reference. For operation and for comparing alternatives, that number works — with the caveats beside it."),
                ("h3", "What cannot, yet"),
                ("p", "The characteristic curve against opening, and any purchase decision that depends on Kv better than 10%. For that, the seat curtain needs at least 6 cells radially."),
                ("h3", "Provenance"),
                ("table", ["What", "Where"], [
                    ["Technical record of the case", '<span class="mono">PINNeAPPle-CFD/casos/cfd08-valvula-globo/RELATORIO.md</span>'],
                    ["Pipeline used", '<span class="mono">pinneapple_simulation.pipelines.compressible_internal</span>'],
                    ["Kv reference", "IEC 60534-2-1 · Peng-Robinson equation of state"],
                    ["Client identity", "kept out of this document; geometry and conditions kept"],
                ], ["30%", None]),
                ("callout", "cyan", "This is an example report,", "from an anonymised client case. A study for your valve follows the same structure: a diagnosis of what exists, the field in physical time, checks with results, and the page of what does not close yet."),
            ]),
        ],
    ),
}


# The other areas with a measured case — aerodynamics, electromagnetics, structural
# mechanics and climate — live in their own module, so this file stays readable.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from relatorios_areas import REPORTS as AREA_REPORTS  # noqa: E402

REPORTS.update(AREA_REPORTS)


def build(slug: str | None = None) -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    for name, report in REPORTS.items():
        if slug and name != slug:
            continue
        for lang in LANGS:
            html = render(report, lang)
            src = SRC / f"{name}-{lang}.html"
            src.write_text(html, encoding="utf-8")
            pdf = OUT / f"{name}-{lang}.pdf"
            subprocess.run(
                [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                 f"--print-to-pdf={pdf}", f"file://{src}"],
                check=True, capture_output=True,
            )
            print("wrote", pdf.relative_to(ROOT), f"({pdf.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
