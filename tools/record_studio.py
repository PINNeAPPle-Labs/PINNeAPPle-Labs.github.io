#!/usr/bin/env python3
"""Records the two Studio tours the product page plays, straight from the running app.

    python3 tools/record_studio.py pt
    python3 tools/record_studio.py en

The videos in `videos/studio-*.mp4` are produced by this script, nothing is mocked
or re-enacted, so a screen the site shows is a screen the application renders.

It needs the app running and an API key:

    cd ../pinneapple-engineering-api
    JOB_BACKEND=inline ./.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010
    ./.venv/bin/python -m app.cli key create --name site-demo   # prints the key

Put that key in a file and pass `--key-file` (default `/tmp/pea_key.txt`). The tool
runs the tour, records it, then cuts the clip: the solver takes around 20 s per run
and nobody watches a progress bar, so the wait is removed and the junction dipped to
black for a tenth of a second, which reads as an edit rather than a glitch.

Output, per language: `videos/studio-<lang>.mp4` and `videos/studio-<lang>.jpg`
(the poster, taken from the poster time below).

Note on the app's CSP: it answers with `style-src 'self'`, so <style> elements and
`style="…"` attributes are refused. The caption and the fake cursor are therefore
styled through `document.adoptedStyleSheets` (CSSOM, which the policy does not
govern) and every class change goes through `classList`.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "videos"
W, H = 1280, 800
DIP = 0.16  # seconds of black at the junction
POSTER_AT = 2.4

T = {
    "pt": dict(
        query="dissipador de calor com aletas",
        run_button="Rodar",
        s1=("Studio", "Você descreve o problema em português comum."),
        s2=("Busca", "A plataforma mostra o que já existe pronto para rodar."),
        s3=("Catálogo", "Cada ferramenta diz se é executável, testada ou verificada."),
        s4=("Execução", "Você roda com os seus números, no seu caso."),
        s5=("Verificações", "A resposta vem com as verificações, uma por uma."),
        s6=("Relatório", "E com o relatório: o que rodou, o que não rodou, a versão do código."),
        s7=("Cobertura", "O que roda hoje é contado do código e das execuções, nunca estimado."),
        waiting=("Rodando", "Rodando no solver, com os parâmetros declarados."),
        end=("Em breve", "PINNeAPPle Engineering", "Lançamento em 2027 · pinneapple-labs.github.io"),
        marker="Verificações",
    ),
    "en": dict(
        query="plate fin heatsink forced",
        run_button="Run",
        s1=("Studio", "You describe the problem in plain language."),
        s2=("Search", "The platform shows what already exists and is ready to run."),
        s3=("Catalogue", "Every tool says whether it is runnable, tested or verified."),
        s4=("Run", "You run it with your own numbers, on your own case."),
        s5=("Checks", "The answer comes back with the checks, one by one."),
        s6=("Report", "And with the report: what ran, what did not, the code version."),
        s7=("Coverage", "What runs today is counted from the code and the runs, never estimated."),
        waiting=("Running", "Running in the solver, with the stated parameters."),
        end=("Coming soon", "PINNeAPPle Engineering", "Launching in 2027 · pinneapple-labs.github.io"),
        marker="Verifications",
    ),
}

CSS = """
#demo-cursor{position:fixed;width:18px;height:18px;border-radius:50%;
  background:#f0b32e;box-shadow:0 0 0 6px rgba(240,179,46,.18),0 6px 18px rgba(0,0,0,.5);
  transform:translate(-50%,-50%);opacity:1;
  transition:left .42s cubic-bezier(.4,0,.2,1),top .42s cubic-bezier(.4,0,.2,1),opacity .3s ease;
  pointer-events:none;z-index:2147483646}
#demo-cursor.hidden{opacity:0}
#demo-cursor::after{content:"";position:absolute;inset:-14px;border-radius:50%;
  border:2px solid rgba(240,179,46,.85);opacity:0;transform:scale(.4)}
#demo-cursor.tap::after{animation:demoTap .5s ease-out}
@keyframes demoTap{0%{opacity:.9;transform:scale(.4)}100%{opacity:0;transform:scale(1.5)}}
#demo-caption{position:fixed;left:30px;bottom:30px;max-width:660px;z-index:2147483645;
  background:rgba(7,10,16,.94);border:1px solid #1e2836;border-left:2px solid #f0b32e;
  border-radius:0 10px 10px 0;padding:15px 22px 16px;
  font:400 20px/1.45 -apple-system,"Segoe UI",Roboto,sans-serif;color:#eef2f7;
  box-shadow:0 18px 40px -18px rgba(0,0,0,.9);opacity:0;transform:translateY(10px);
  transition:opacity .35s ease,transform .35s ease;pointer-events:none}
#demo-caption.on{opacity:1;transform:none}
#demo-caption b{display:block;margin-bottom:6px;
  font:600 11px/1 "IBM Plex Mono",ui-monospace,monospace;
  letter-spacing:.16em;text-transform:uppercase;color:#f0b32e}
#demo-end{position:fixed;inset:0;z-index:2147483647;display:grid;place-items:center;
  background:radial-gradient(60% 60% at 50% 40%,rgba(240,179,46,.12),transparent 70%),rgba(7,10,16,.965);
  opacity:0;transition:opacity .6s ease;pointer-events:none;text-align:center;
  font-family:-apple-system,"Segoe UI",Roboto,sans-serif}
#demo-end.on{opacity:1}
#demo-end .k{font:600 12px/1 "IBM Plex Mono",ui-monospace,monospace;
  letter-spacing:.2em;text-transform:uppercase;color:#f0b32e}
#demo-end h2{margin:18px 0 12px;font-size:54px;line-height:1.05;font-weight:800;
  color:#eef2f7;letter-spacing:-.02em}
#demo-end p{font:400 18px/1.5 "IBM Plex Mono",ui-monospace,monospace;color:#93a1b4;margin:0}
"""


def ensure_ui(page) -> None:
    page.evaluate(
        """(css) => {
            if (!window.__demoSheet) {
                const s = new CSSStyleSheet();
                s.replaceSync(css);
                document.adoptedStyleSheets = [...document.adoptedStyleSheets, s];
                window.__demoSheet = s;
                const p = new CSSStyleSheet();
                p.replaceSync('#demo-cursor{left:680px;top:430px}');
                document.adoptedStyleSheets = [...document.adoptedStyleSheets, p];
                window.__posSheet = p;
            }
            if (!document.getElementById('demo-cursor')) {
                const c = document.createElement('div');
                c.id = 'demo-cursor';
                document.body.appendChild(c);
            }
            if (!document.getElementById('demo-caption')) {
                const d = document.createElement('div');
                d.id = 'demo-caption';
                document.body.appendChild(d);
            }
        }""",
        CSS,
    )


def caption(page, kicker: str, text: str) -> None:
    ensure_ui(page)
    page.evaluate(
        """([k, t]) => {
            const c = document.getElementById('demo-caption');
            c.innerHTML = '<b>' + k + '</b>' + t;
            c.classList.add('on');
        }""",
        [kicker, text],
    )


def hide_caption(page) -> None:
    page.evaluate("document.getElementById('demo-caption')?.classList.remove('on')")


def move_to(page, selector: str) -> None:
    box = page.locator(selector).first.bounding_box()
    if not box:
        return
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    ensure_ui(page)
    page.evaluate(
        "([x, y]) => window.__posSheet.replaceSync('#demo-cursor{left:' + x + 'px;top:' + y + 'px}')",
        [round(x), round(y)],
    )
    page.wait_for_timeout(470)


def cursor_visible(page, visible: bool) -> None:
    page.evaluate(
        "(v) => document.getElementById('demo-cursor')?.classList.toggle('hidden', !v)",
        visible,
    )


def tap(page) -> None:
    page.evaluate(
        """() => { const c = document.getElementById('demo-cursor');
                   c.classList.remove('tap'); void c.offsetWidth; c.classList.add('tap'); }"""
    )


def smooth_scroll(page, total: int, steps: int = 10, pause: int = 45) -> None:
    for _ in range(steps):
        page.mouse.wheel(0, total // steps)
        page.wait_for_timeout(pause)


def record(lang: str, key: str, url: str) -> tuple[Path, dict[str, float]]:
    T_ = T[lang]
    stamps: dict[str, float] = {}
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        ctx = browser.new_context(
            viewport={"width": 1360, "height": 850},
            record_video_dir=str(OUT / ".raw"),
            record_video_size={"width": 1360, "height": 850},
            device_scale_factor=1,
        )
        page = ctx.new_page()
        t0 = time.time()

        page.goto(url, wait_until="networkidle")
        page.select_option("#theme", "dark")
        if lang != "pt":
            page.select_option("#lang", lang)
        page.wait_for_timeout(900)
        if page.locator("#keybtn").is_visible():
            page.click("#keybtn")
            page.fill("#keyin", key)
            page.click("#keysave")
            page.wait_for_timeout(400)

        ensure_ui(page)
        caption(page, *T_["s1"])
        page.wait_for_timeout(600)
        move_to(page, "#hq")
        tap(page)
        page.click("#hq")
        page.type("#hq", T_["query"], delay=55)
        page.wait_for_timeout(500)

        page.keyboard.press("Enter")
        page.wait_for_timeout(1400)
        caption(page, *T_["s2"])
        page.wait_for_timeout(600)
        smooth_scroll(page, 200)
        page.wait_for_timeout(400)

        caption(page, *T_["s3"])
        move_to(page, 'a[href*="#/tool/preset%3Aplate_fin_heatsink_forced"]')
        tap(page)
        page.wait_for_timeout(300)
        page.click('a[href*="#/tool/preset%3Aplate_fin_heatsink_forced"]')
        page.wait_for_timeout(1800)
        smooth_scroll(page, 240)
        page.wait_for_timeout(500)

        caption(page, *T_["s4"])
        page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        page.wait_for_timeout(600)
        move_to(page, "button:has-text('" + T_["run_button"] + "')")
        tap(page)
        stamps["click"] = time.time() - t0
        page.click("button:has-text('" + T_["run_button"] + "')")
        page.wait_for_timeout(1800)

        caption(page, *T_["waiting"])
        for _ in range(90):
            page.wait_for_timeout(500)
            if T_["marker"] in page.evaluate("document.body.innerText"):
                break
        stamps["results"] = time.time() - t0

        caption(page, *T_["s5"])
        cursor_visible(page, False)
        page.wait_for_timeout(600)
        smooth_scroll(page, 620, steps=14, pause=55)
        page.wait_for_timeout(700)

        caption(page, *T_["s6"])
        smooth_scroll(page, 700, steps=14, pause=55)
        page.wait_for_timeout(800)

        caption(page, *T_["s7"])
        cursor_visible(page, True)
        move_to(page, 'a[href="#/cobertura"]')
        tap(page)
        page.click('a[href="#/cobertura"]')
        page.wait_for_timeout(1800)
        smooth_scroll(page, 300)
        page.wait_for_timeout(900)

        hide_caption(page)
        cursor_visible(page, False)
        page.evaluate(
            """([k, h, t]) => {
                const d = document.createElement('div');
                d.id = 'demo-end';
                d.innerHTML = '<div><div class="k">' + k + '</div><h2>' + h + '</h2><p>' + t + '</p></div>';
                document.body.appendChild(d);
                requestAnimationFrame(() => d.classList.add('on'));
            }""",
            list(T_["end"]),
        )
        page.wait_for_timeout(4000)
        stamps["end"] = time.time() - t0

        video = page.video.path()
        ctx.close()
        browser.close()

    raw = OUT / f".raw-{lang}.webm"
    Path(video).replace(raw)
    (OUT / f".raw-{lang}.json").write_text(json.dumps(stamps, indent=2))
    return raw, stamps


def run(*args: str) -> str:
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode:
        sys.exit(out.stderr[-2000:])
    return out.stdout


def duration(path: Path) -> float:
    return float(
        run("ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(path)).strip()
    )


def encode(lang: str, raw: Path, stamps: dict[str, float]) -> None:
    """Cuts the solver wait out and encodes the clip the site serves."""
    total = duration(raw)
    # A: to a second into the progress bar, so the click is seen and the
    #    "running" caption has time to arrive.
    a_end = min(stamps["click"] + 2.9, stamps["results"] - 1.0)
    # B: from just after the results rendered, by then the caption has already
    #    changed to the checks, to the end card.
    b_start = stamps["results"] + 0.35

    mp4 = OUT / f"studio-{lang}.mp4"
    run(
        "ffmpeg", "-v", "error", "-y",
        "-ss", "0", "-to", f"{a_end:.3f}", "-i", str(raw),
        "-ss", f"{b_start:.3f}", "-to", f"{total:.3f}", "-i", str(raw),
        "-filter_complex",
        f"[0:v]scale={W}:{H},setsar=1,fps=25,"
        f"fade=t=out:st={a_end - DIP:.3f}:d={DIP},setpts=PTS-STARTPTS[a];"
        f"[1:v]scale={W}:{H},setsar=1,fps=25,"
        f"fade=t=in:st=0:d={DIP},setpts=PTS-STARTPTS[b];"
        f"[a][b]concat=n=2:v=1:a=0,format=yuv420p[v]",
        "-map", "[v]",
        "-c:v", "libx264", "-crf", "24", "-preset", "slow",
        "-profile:v", "high", "-movflags", "+faststart", "-an",
        str(mp4),
    )
    run("ffmpeg", "-v", "error", "-y", "-ss", str(POSTER_AT), "-i", str(mp4),
        "-frames:v", "1", "-q:v", "4", str(OUT / f"studio-{lang}.jpg"))
    print(f"{mp4.name}: {duration(mp4):.2f} s, {mp4.stat().st_size // 1024} KB"
          f" (cut {a_end:.2f} | {b_start:.2f})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", choices=["pt", "en", "both"], nargs="?", default="both")
    ap.add_argument("--url", default="http://127.0.0.1:8010/")
    ap.add_argument("--key-file", type=Path, default=Path("/tmp/pea_key.txt"))
    ap.add_argument("--reuse", action="store_true",
                    help="re-encode the raw recording already in videos/ instead of recording again")
    args = ap.parse_args()

    for lang in (["pt", "en"] if args.lang == "both" else [args.lang]):
        raw = OUT / f".raw-{lang}.webm"
        stampsf = OUT / f".raw-{lang}.json"
        if args.reuse:
            stamps = json.loads(stampsf.read_text())
        else:
            key = re.search(r"pea_[A-Za-z0-9]+", args.key_file.read_text()).group(0)
            print(f"recording {lang}…")
            raw, stamps = record(lang, key, args.url)
        encode(lang, raw, stamps)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
