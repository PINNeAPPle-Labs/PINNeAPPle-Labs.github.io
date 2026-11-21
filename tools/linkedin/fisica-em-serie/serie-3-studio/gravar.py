#!/usr/bin/env python3
"""Gravador dos episódios da Série 3: dirige a app real do Studio e captura quadro a quadro.

Cada episódio abre uma app do `PINNeAPPle/apps/`, executa a interação de verdade (rodar o
analisador, arrastar o slider que refaz a malha, orbitar o campo em 3-D) e codifica em `midia/`.

    python gravar.py brakecool | soundshape | heatsink | pcb | afpm

As apps precisam estar de pé; as portas estão em `PORTAS`.
"""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
MIDIA = AQUI / "midia"
FPS = 30
LARGURA = 1200
VIS = {"width": 1500, "height": 950}

PORTAS = {"ahmed": 8451, "afpm": 8191, "pcb": 8401, "aero": 8092, "heatsink": 8402,
          "soundshape": 8403, "brakecool": 8404, "ridetune": 8405, "observatory": 8406, "optics": 8166}


def _codificar(pasta: Path, destino: Path) -> None:
    n = len(list(pasta.glob("f*.png")))
    if n == 0:
        raise SystemExit("nenhum quadro capturado")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS),
                    "-i", str(pasta / "f%04d.png"), "-vf", f"scale={LARGURA}:-2",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-movflags", "+faststart", str(destino)], check=True)
    seg = n / FPS
    print(f"  {destino.name}: {n} quadros ({seg:.1f} s), {destino.stat().st_size/1e6:.1f} MB")


class Gravador:
    """Conta quadros e recorta a região de interesse a cada captura."""

    def __init__(self, pg, pasta: Path, clip: dict):
        self.pg, self.pasta, self.clip, self.i = pg, pasta, clip, 0

    def quadro(self) -> None:
        self.pg.screenshot(path=str(self.pasta / f"f{self.i:04d}.png"), clip=self.clip)
        self.i += 1

    def parado(self, n: int, espera: float = 0.0) -> None:
        # as paradas são o momento de ler o número: duram o dobro do pedido
        for _ in range(int(round(n * 1.8))):
            if espera:
                self.pg.wait_for_timeout(int(espera * 1000))
            self.quadro()

    def rolar(self, n: int, delta: float = 90, x: int = 1000, y: int = 500) -> None:
        """Rolagem suave, um quadro por passo — é assim que a página desce no vídeo."""
        self.pg.mouse.move(x, y)
        for _ in range(n):
            self.pg.mouse.wheel(0, delta)
            self.pg.wait_for_timeout(90)
            self.quadro()

    def orbita(self, caixa, n, amplitude=190, altura=55, passo=0.0) -> None:
        """Arrasta sobre o canvas em arco; `passo` é a pausa entre quadros."""
        cx, cy = caixa["x"] + caixa["width"] / 2, caixa["y"] + caixa["height"] / 2
        self.pg.mouse.move(cx, cy)
        self.pg.mouse.down()
        for k in range(n):
            f = k / max(n - 1, 1)
            # arco de ida e volta, para o vídeo não terminar de costas
            x = cx + amplitude * math.sin(f * 2 * math.pi)
            y = cy - altura * math.sin(f * math.pi)
            self.pg.mouse.move(x, y)
            if passo:
                self.pg.wait_for_timeout(int(passo * 1000))
            self.quadro()
        self.pg.mouse.up()


def _esperar_texto(pg, seletor, proibido="—", limite=240.0, passo=1.5):
    """Espera o painel de resultado parar de mostrar o marcador de vazio."""
    import time
    t0 = time.time()
    while time.time() - t0 < limite:
        try:
            if proibido not in pg.inner_text(seletor):
                return True
        except Exception:
            pass
        pg.wait_for_timeout(int(passo * 1000))
    return False


def _maior_canvas(pg):
    """O maior canvas visível da página — nas apps com abas, os outros estão escondidos."""
    melhor, area = None, 0.0
    for c in pg.locator("canvas").all():
        try:
            if not c.is_visible():
                continue
            b = c.bounding_box()
        except Exception:
            continue
        if b and b["width"] * b["height"] > area:
            melhor, area = c, b["width"] * b["height"]
    return melhor


def _arrastar_slider(pg, seletor, valor):
    pg.eval_on_selector(seletor, """(e, v) => {
        e.value = String(v);
        e.dispatchEvent(new Event('input', {bubbles: true}));
        e.dispatchEvent(new Event('change', {bubbles: true}));
    }""", valor)


# ------------------------------------------------------------------ episódios

def brakecool(pg, g: Gravador):
    """Freio ventilado: rotor em 3-D, temperatura nos dutos entre as aletas."""
    pg.goto(f"http://127.0.0.1:{PORTAS['brakecool']}/", wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(3000)
    caixa = pg.locator("#viewer canvas").first.bounding_box()
    g.clip = {"x": 170, "y": 130, "width": 1150, "height": 690}   # painel + campo
    g.parado(6)
    g.orbita(caixa, 55, amplitude=200, altura=60)
    pg.click("#btn-optimize")
    pg.wait_for_timeout(6000)
    _esperar_texto(pg, "#result", limite=90)
    pg.wait_for_timeout(800)
    caixa = pg.locator("#viewer canvas").first.bounding_box()
    g.orbita(caixa, 55, amplitude=200, altura=60)
    # condição mais severa: o campo esquenta e a legenda acompanha
    _arrastar_slider(pg, "#power", "1600")
    pg.wait_for_timeout(1600)
    caixa = pg.locator("#viewer canvas").first.bounding_box()
    g.orbita(caixa, 60, amplitude=140, altura=90)
    # Monte Carlo de tolerância de fabricação, o objetivo da app
    pg.click("#btn-uncertainty")
    pg.wait_for_timeout(5000)
    _esperar_texto(pg, "#uncertainty-result", limite=120)
    pg.wait_for_timeout(1200)
    g.rolar(18, delta=95)
    pg.locator("#uncertainty-result").evaluate("e => e.scrollIntoView({block: 'center'})")
    pg.wait_for_timeout(900)
    g.clip = {"x": 170, "y": 150, "width": 1150, "height": 700}
    g.parado(40, espera=0.12)


def soundshape(pg, g: Gravador):
    """Duto bass-reflex: malha em 3-D, frequência de Helmholtz ao vivo."""
    pg.goto(f"http://127.0.0.1:{PORTAS['soundshape']}/", wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(3000)
    g.clip = {"x": 170, "y": 130, "width": 1150, "height": 640}
    caixa = pg.locator("#viewer canvas").first.bounding_box()
    cx, cy = caixa["x"] + caixa["width"] / 2, caixa["y"] + caixa["height"] / 2
    # o duto é um cilindro: girar em torno do eixo não mostra nada — inclina para revelar o 3-D
    pg.mouse.move(cx, cy)
    pg.mouse.down()
    for k in range(28):
        f = k / 27
        pg.mouse.move(cx + 70 * f, cy - 95 * f)
        g.quadro()
    pg.mouse.up()
    # afina o duto ao alvo de 40 Hz arrastando o raio e o comprimento
    for v in (28, 30, 32, 34, 36, 38, 40):
        _arrastar_slider(pg, "#s-radius", v)
        pg.wait_for_timeout(450)
        g.quadro()
    for v in (95, 88, 82, 76):
        _arrastar_slider(pg, "#s-length", v)
        pg.wait_for_timeout(450)
        g.quadro()
    pg.mouse.move(cx, cy)
    pg.mouse.down()
    for k in range(24):
        f = k / 23
        pg.mouse.move(cx - 120 * f, cy + 30 * f)
        g.quadro()
    pg.mouse.up()
    # o otimizador devolve o projeto, não o palpite manual
    pg.click("#btn-optimize")
    pg.wait_for_timeout(5000)
    _esperar_texto(pg, "#result", limite=90)
    pg.mouse.move(cx, cy)
    for k in range(10):                       # roda o mouse para o tooltip aparecer
        pg.mouse.wheel(0, -120)
        pg.wait_for_timeout(120)
        g.quadro()
    # a fronteira de compromisso: a curva que escolhe tamanho contra sintonia
    pg.click("#btn-frontier")
    pg.wait_for_timeout(6000)
    for _ in range(24):                       # rolagem suave até o gráfico
        pg.mouse.wheel(0, 90)
        pg.wait_for_timeout(90)
        g.quadro()
    g.clip = {"x": 170, "y": 130, "width": 1150, "height": 690}
    g.parado(30, espera=0.12)


def heatsink(pg, g: Gravador):
    """Dissipador aletado: 38 mil candidatos triados, 24 verificados, campo em 3-D."""
    pg.goto(f"http://127.0.0.1:{PORTAS['heatsink']}/", wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(2500)
    g.clip = {"x": 90, "y": 130, "width": 1320, "height": 760}
    g.parado(10, espera=0.12)
    pg.get_by_role("button", name="Find designs").click()
    pg.wait_for_timeout(7000)
    g.parado(20, espera=0.15)
    pg.get_by_role("button", name="Details").first.click()
    pg.wait_for_timeout(6000)
    canvas = pg.locator("canvas").nth(0)
    canvas.scroll_into_view_if_needed()
    pg.wait_for_timeout(1500)
    caixa = canvas.bounding_box()
    g.clip = {"x": 90, "y": max(0, caixa["y"] - 210), "width": 1320, "height": 900}
    g.orbita(caixa, 70, amplitude=200, altura=40)
    # as vistas ortográficas mostram o gradiente base → topo das aletas
    for nome in ("Top", "Side", "Iso"):
        pg.get_by_role("button", name=nome, exact=True).click()
        pg.wait_for_timeout(900)
        g.parado(6, espera=0.1)
    g.orbita(caixa, 30, amplitude=110, altura=40)


def pcb(pg, g: Gravador):
    """Placa com FPGA/DDR: 13,8 W em 6 partes, junção e margem por componente, campo em 3-D."""
    pg.goto(f"http://127.0.0.1:{PORTAS['pcb']}/", wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(2500)
    g.clip = {"x": 90, "y": 95, "width": 1320, "height": 830}
    g.parado(8, espera=0.15)
    pg.click("#run-full")
    pg.wait_for_timeout(11000)
    canvas = _maior_canvas(pg)
    canvas.evaluate("e => e.scrollIntoView({block: 'center'})")
    pg.wait_for_timeout(1500)
    caixa = canvas.bounding_box()
    g.clip = {"x": 90, "y": max(0, caixa["y"] - 120), "width": 1320, "height": 900}
    g.orbita(caixa, 60, amplitude=210, altura=50)
    for nome in ("Top", "Front", "Iso"):
        try:
            pg.get_by_role("button", name=nome, exact=True).click()
            pg.wait_for_timeout(900)
        except Exception:
            pass
        g.parado(8, espera=0.12)
    g.orbita(caixa, 35, amplitude=120, altura=50)


def afpm(pg, g: Gravador):
    """Motor de fluxo axial: o estimate quasi-3-D e o campo |B| em 3-D, com a verificação."""
    pg.goto(f"http://127.0.0.1:{PORTAS['afpm']}/", wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(2500)
    g.clip = {"x": 0, "y": 0, "width": 1500, "height": 950}
    g.parado(10, espera=0.15)
    pg.get_by_role("button", name="Estimate (quasi-3D)").click()
    # o job leva minutos: guarda o painel de progresso sem repetir o mesmo quadro
    g.parado(10, espera=2.0)
    _esperar_texto(pg, "#results", limite=360)
    pg.wait_for_timeout(1000)
    canvas = _maior_canvas(pg)
    canvas.evaluate("e => e.scrollIntoView({block: 'center'})")
    pg.wait_for_timeout(1500)
    caixa = canvas.bounding_box()
    g.clip = {"x": 0, "y": max(0, caixa["y"] - 200), "width": 1500, "height": 950}
    g.parado(8, espera=0.2)
    g.orbita(caixa, 80, amplitude=200, altura=45, passo=0.02)
    for nome in ("iso", "Top", "Front"):
        try:
            pg.get_by_role("button", name=nome, exact=False).first.click()
            pg.wait_for_timeout(800)
        except Exception:
            continue
        g.parado(8, espera=0.12)


def ridetune(pg, g: Gravador):
    """Braço de suspensão: viga em 3-D com a tensão de flexão viva, e a sensibilidade que decide."""
    pg.goto(f"http://127.0.0.1:{PORTAS['ridetune']}/", wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(3000)
    g.clip = {"x": 170, "y": 130, "width": 1150, "height": 640}
    caixa = pg.locator("#viewer canvas").first.bounding_box()
    g.orbita(caixa, 45, amplitude=180, altura=70)
    # afina a seção: a cor da viga acompanha a tensão na hora
    for v in (44, 40, 36, 32):
        _arrastar_slider(pg, "#s-width", v)
        pg.wait_for_timeout(500)
        g.quadro()
    for v in (20, 18, 16, 14):
        _arrastar_slider(pg, "#s-thickness", v)
        pg.wait_for_timeout(500)
        g.quadro()
    caixa = pg.locator("#viewer canvas").first.bounding_box()
    g.orbita(caixa, 30, amplitude=110, altura=60)
    # o otimizador devolve o projeto e a verificação contra a fórmula fechada
    pg.click("#btn-optimize")
    pg.wait_for_timeout(6000)
    _esperar_texto(pg, "#result", limite=120)
    pg.wait_for_timeout(1200)
    g.parado(26, espera=0.12)
    # a análise que decide qual variável importa: espessura pesa o dobro da largura
    pg.click("#btn-sensitivity")
    pg.wait_for_timeout(5000)
    _esperar_texto(pg, "#sensitivity-result", limite=120)
    pg.locator("#sensitivity-result").evaluate("e => e.scrollIntoView({block: 'center'})")
    pg.wait_for_timeout(900)
    g.clip = {"x": 170, "y": 150, "width": 1150, "height": 700}
    g.parado(34, espera=0.12)


def observatory(pg, g: Gravador):
    """O céu de agora em 3-D: catálogo de estrelas, Lua com fase e distância, e o sistema solar."""
    pg.goto(f"http://127.0.0.1:{PORTAS['observatory']}/", wait_until="load", timeout=90000)
    pg.wait_for_timeout(8000)
    try:                                     # fecha o cartão de curiosidade que cobre o céu
        pg.click("text=×", timeout=2500)
    except Exception:
        pass
    g.clip = {"x": 0, "y": 0, "width": 1074, "height": 950}
    # anoitece: o céu de São Paulo às 21h30 de hoje
    pg.eval_on_selector("#tDate", """e => {
        e.value = '2026-11-21T21:30';
        e.dispatchEvent(new Event('change', {bubbles: true}));
    }""")
    pg.wait_for_timeout(4000)
    caixa = pg.locator("#gl").bounding_box()
    g.orbita(caixa, 70, amplitude=260, altura=90)
    # a grade equatorial e a eclíptica mostram o plano em que os planetas andam
    try:
        pg.check("text=Equatorial grid")
        pg.wait_for_timeout(1500)
    except Exception:
        pass
    g.orbita(caixa, 30, amplitude=180, altura=60)
    # sai do céu para o sistema solar: o mesmo instante, visto de fora
    pg.click("#vSys")
    pg.wait_for_timeout(5000)
    g.clip = {"x": 0, "y": 0, "width": 1500, "height": 950}
    caixa = pg.locator("#gl").bounding_box()
    g.orbita(caixa, 45, amplitude=240, altura=70)
    # roda o tempo: os planetas andam nas órbitas
    for _ in range(14):
        pg.click("#tFwd")
        pg.wait_for_timeout(320)
        g.quadro()


def optics(pg, g: Gravador):
    """Óptica: imagem aérea de um clipe litográfico em 3-D, com as checagens ao lado de cada número."""
    pg.goto(f"http://127.0.0.1:{PORTAS['optics']}/", wait_until="load", timeout=90000)
    pg.wait_for_timeout(9000)
    g.clip = {"x": 170, "y": 120, "width": 1160, "height": 760}
    def iso():
        """Espera o campo novo e devolve a caixa do canvas (o campo novo não herda a câmera do anterior)."""
        pg.wait_for_timeout(1800)
        return pg.locator("#viewer canvas").first.bounding_box()

    caixa = iso()
    g.orbita(caixa, 45, amplitude=110, altura=200)
    # outro sistema óptico: EUV, onde o mesmo clipe imprime com viés quase nulo
    pg.get_by_role("button", name="EUV").click()
    pg.wait_for_timeout(9000)
    caixa = iso()
    g.orbita(caixa, 40, amplitude=120, altura=180)
    # e de volta ao ArF imersão, que é o caso apertado (viés de 20 nm, NILS 2,2)
    pg.get_by_role("button", name="ArF imersão").click()
    pg.wait_for_timeout(9000)
    caixa = iso()
    g.orbita(caixa, 35, amplitude=100, altura=150)


EPISODIOS = {"brakecool": brakecool, "soundshape": soundshape, "heatsink": heatsink,
             "pcb": pcb, "afpm": afpm, "ridetune": ridetune, "observatory": observatory, "optics": optics}


def main() -> None:
    chave = sys.argv[1] if len(sys.argv) > 1 else "brakecool"
    if chave not in EPISODIOS:
        raise SystemExit(f"episódio desconhecido: {chave} (opções: {', '.join(EPISODIOS)})")
    pasta = Path(f"/tmp/grav_{chave}")
    pasta.mkdir(parents=True, exist_ok=True)
    for velho in pasta.glob("f*.png"):
        velho.unlink()
    MIDIA.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport=VIS)
        g = Gravador(pg, pasta, {"x": 0, "y": 0, "width": 1500, "height": 950})
        EPISODIOS[chave](pg, g)
        b.close()
    _codificar(pasta, MIDIA / f"{chave}.mp4")


if __name__ == "__main__":
    main()
