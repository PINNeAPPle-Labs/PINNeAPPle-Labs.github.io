#!/usr/bin/env python3
"""Writes ``data/modelos.json``: the published model family, read from the library.

    python3 tools/modelos.py [--pinneapple ../PINNeAPPle] [--python /path/to/python]

The page ``modelos/`` is rendered by ``build.py`` from this file, so the site never restates a metric: every
number comes from ``pp.zoo.anchors.public()``, which reads the zoo manifest and the model cards. Run this once
when an anchor changes and ``build.py`` whenever the shell changes.

The interpreter has to be one that can import the library (``torch`` included); ``--python`` runs this same
script under another one, which is how a checkout with its own virtualenv is used.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "modelos.json"


def build(library: Path) -> dict:
    sys.path.insert(0, str(library))
    from pinneapple_hub.zoo import anchors  # noqa: PLC0415 - after the path is set

    payload = anchors.public()
    if payload["problems"]:
        raise SystemExit("refusing to publish a family with problems:\n  " + "\n  ".join(payload["problems"]))
    return payload


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools/modelos.py")
    ap.add_argument("--pinneapple", default=os.environ.get("PINNEAPPLE_SRC", "../PINNeAPPle"),
                    help="PINNeAPPle checkout to read the family from")
    ap.add_argument("--python", help="interpreter that can import the library; runs this script again with it")
    args = ap.parse_args(argv)

    library = (ROOT / args.pinneapple).resolve() if not Path(args.pinneapple).is_absolute() \
        else Path(args.pinneapple)
    if args.python:
        r = subprocess.run([args.python, __file__, "--pinneapple", str(library)], check=False)
        return r.returncode

    payload = build(library)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(payload['anchors'])} anchors "
          f"({payload['family']['name']} {payload['family']['version']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
