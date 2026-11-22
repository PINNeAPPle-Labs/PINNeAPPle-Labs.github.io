#!/usr/bin/env python3
"""Manifesto de proveniência de cada episódio: de onde o vídeo veio e o que ele não afirma.

Um vídeo sem rastro é alegação. O manifesto amarra cada arquivo de mídia ao app que o produziu, ao
commit do app na biblioteca, ao driver de captura e ao número que a ficha publica — com hash e
duração medidos do próprio arquivo, não digitados.

    python manifesto.py           # todos os episódios
    python manifesto.py 05        # só um

Saída: ``midia/<episódio>.manifest.json``, schema ``pinneapple.cinema.media/1``. A ficha em
``episodios/`` é a fonte do título, da área e do app; o resto é medido.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[3]                      # a raiz do checkout do site
BIBLIOTECA = Path("/Users/yanbarros/Documents/GitHub/pinneapple-labs/PINNeAPPle")
MIDIA, VERTICAL, FICHAS = AQUI / "midia", AQUI / "midia-vertical", AQUI / "episodios"
TECNICA = AQUI / "midia-tecnica"
SCHEMA = "pinneapple.cinema.media/1"

CABECALHO = re.compile(
    r"\*\*Área\*\*\s*(?P<area>.+?)\s*·\s*\*\*App\*\*\s*`(?P<app>[a-z0-9_]+)`\s*\((?P<app_nome>[^)]+)\)"
    r".*?\*\*Duração\*\*\s*(?P<duracao>[\d,]+)\s*s\s*·\s*\*\*Mídia\*\*\s*`(?P<midia>[^`]+)`")


def _run(*cmd: str) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip()


def _sha(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _sonda(caminho: Path) -> dict:
    """Largura, altura, quadros e duração lidos do arquivo — nada de confiar na ficha."""
    saida = _run("ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height,nb_frames,r_frame_rate",
                 "-show_entries", "format=duration", "-of", "json", str(caminho))
    d = json.loads(saida)
    s = d["streams"][0]
    num, den = (s.get("r_frame_rate") or "0/1").split("/")
    return {"width": s["width"], "height": s["height"],
            "frames": int(s.get("nb_frames") or 0),
            "fps": round(int(num) / max(int(den), 1), 3),
            "duration_s": round(float(d["format"]["duration"]), 2),
            "sha256": _sha(caminho),
            "bytes": caminho.stat().st_size}


def _commit_app(app: str) -> str:
    """Commit que por último tocou a app na biblioteca — o rastro do código que aparece no vídeo."""
    try:
        return _run("git", "-C", str(BIBLIOTECA), "log", "-1", "--format=%h %ad",
                    "--date=short", "--", f"apps/{app}")
    except subprocess.CalledProcessError:
        return "desconhecido"


def _commit_driver() -> str:
    return _run("git", "-C", str(REPO), "log", "-1", "--format=%h %ad", "--date=short", "--",
                "tools/linkedin/fisica-em-serie/serie-3-studio/gravar.py")


def _ficha(ep: str) -> dict:
    texto = (FICHAS / f"{ep}.md").read_text(encoding="utf-8")
    m = CABECALHO.search(texto.replace("\n", " "))
    if not m:
        raise SystemExit(f"{ep}: cabeçalho da ficha fora do formato esperado")
    return m.groupdict()


def _afirmacao(ep: str) -> dict:
    """O número e a ressalva vêm da cartela, que é o que aparece no vídeo vertical."""
    from vertical import TEXTOS
    c = TEXTOS[ep]
    return {"number": c.numero, "source": c.detalhe, "not_affirmed": c.ressalva}


def manif(ep: str) -> Path | None:
    fonte = MIDIA / f"{ep}.mp4"
    if not fonte.is_file():
        return None
    ficha = _ficha(ep)
    produtos = [{"id": "screen-16x9", "file": f"midia/{ep}.mp4", **_sonda(fonte)}]
    for pasta, ident in ((VERTICAL, "short-9x16"), (TECNICA, "technical-16x9")):
        alt = pasta / f"{ep}.mp4"
        if alt.is_file():
            produtos.append({"id": ident, "file": f"{pasta.name}/{ep}.mp4", **_sonda(alt)})
    capturado = datetime.fromtimestamp(fonte.stat().st_mtime, tz=timezone.utc)
    titulo = (FICHAS / f"{ep}.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
    doc = {
        "schema": SCHEMA,
        "episode": {"id": ep, "title": titulo, "area": ficha["area"]},
        "experiment": {"app": ficha["app"], "app_name": ficha["app_nome"],
                       "app_path": f"apps/{ficha['app']}", "library_commit": _commit_app(ficha["app"])},
        "capture": {"driver": "tools/linkedin/fisica-em-serie/serie-3-studio/gravar.py",
                    "driver_commit": _commit_driver(),
                    "driver_sha256": _sha(AQUI / "gravar.py"),
                    "fps": 30, "viewport": "1500x950",
                    "captured_at": capturado.strftime("%Y-%m-%dT%H:%M:%SZ")},
        "claim": _afirmacao(ep),
        "products": produtos,
        "note": "quadros capturados de uma execução real da app; nenhuma etapa generativa",
    }
    destino = MIDIA / f"{ep}.manifest.json"
    destino.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {destino.name}: {len(produtos)} produto(s), app {ficha['app']}")
    if BIBLIOTECA_PEDIDA:
        _na_biblioteca(doc)
    return destino


RAIZ_SITE = "PINNeAPPle-Labs.github.io"
BIBLIOTECA_PEDIDA = False


def _na_biblioteca(doc: dict) -> None:
    """Escreve ``apps/<app>/cinema.json`` na biblioteca: a galeria do Studio passa a saber que existe vídeo.

    A biblioteca não guarda os mp4 — ela guarda o ponteiro com o hash, e o portão confere o hash quando o checkout
    do site está acessível. Assim o vídeo não vira arquivo solto num diretório de marketing."""
    app = doc["experiment"]["app"]
    pasta = BIBLIOTECA / "apps" / app
    if not pasta.is_dir():
        print(f"  (sem apps/{app} na biblioteca, cinema.json não escrito)")
        return
    produtos = [{"id": p["id"], "repo": RAIZ_SITE, "path": f"tools/linkedin/fisica-em-serie/serie-3-studio/{p['file']}",
                 **{k: p[k] for k in ("sha256", "duration_s", "width", "height", "frames", "fps")}}
                for p in doc["products"]]
    alvo = {"schema": SCHEMA, "episode": doc["episode"]["area"],
            "episode_id": doc["episode"]["id"], "claim": doc["claim"],
            "capture": {k: doc["capture"][k] for k in ("driver", "driver_commit", "fps", "viewport", "captured_at")},
            "products": produtos,
            "note": doc["note"]}
    caminho = pasta / "cinema.json"
    caminho.write_text(json.dumps(alvo, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  apps/{app}/cinema.json")


def main() -> None:
    global BIBLIOTECA_PEDIDA
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    BIBLIOTECA_PEDIDA = "--biblioteca" in sys.argv
    alvo = args[0] if args else ""
    feitos = sum(1 for f in sorted(MIDIA.glob("*.mp4"))
                 if (not alvo or f.stem.startswith(alvo)) and manif(f.stem))
    print(f"{feitos} manifestos em {MIDIA}")


if __name__ == "__main__":
    main()
