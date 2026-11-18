#!/usr/bin/env python3
"""Writes ``data/api.json``: the public operations of the Engineering API, read from its OpenAPI schema.

    ../pinneapple-engineering-api/.venv/bin/python tools/api_docs.py [--api ../pinneapple-engineering-api]

Runs from the site repo but imports the app from the API checkout, so the reference cannot drift from the code:
the description, the parameters, the request body and the responses all come from ``app.openapi()``. Only the
documented surface is kept (``meta``, ``capabilities``, ``jobs``, ``agent``, ``products``, ``solvers``, ``lpm``);
the Studio, platform and administration routers are internal and are not published.

The interpreter has to be one that can import the API (``fastapi``, ``pydantic``, the app's own modules): the
checkout's ``.venv/bin/python`` is the usual one.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess  # noqa: S404 - re-running this same script under the checkout's interpreter
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "api.json"

#: Tags that make up the public surface. Anything outside this list is an internal router.
PUBLIC_TAGS = ["meta", "capabilities", "jobs", "agent", "products", "solvers", "lpm"]


def _shape(schema: dict, root: dict, depth: int = 0) -> list[dict]:
    """Flatten one level of a request body into fields, keeping the type and the description."""
    if depth > 2:
        return []
    ref = schema.get("$ref")
    if ref:
        schema = _resolve(root, ref)
    fields = []
    for name, spec in (schema.get("properties") or {}).items():
        if "$ref" in spec:
            spec = _resolve(root, spec["$ref"])
        if spec.get("type") == "array" and isinstance(spec.get("items"), dict):
            item = spec["items"]
            if "$ref" in item:
                item = _resolve(root, item["$ref"])
            fields.append({"name": name, "type": f"array<{item.get('type', 'object')}>",
                           "required": name in (schema.get("required") or []),
                           "description": item.get("description", "")})
            continue
        fields.append({"name": name, "type": spec.get("type", "object"),
                       "required": name in (schema.get("required") or []),
                       "description": spec.get("description", "")})
    return fields


def _resolve(root: dict, ref: str) -> dict:
    node: dict = root
    for part in ref.lstrip("#/").split("/"):
        node = node.get(part, {})
    return node


def build(api: Path) -> dict:
    cwd = os.getcwd()
    os.chdir(api)                       # the app resolves its static files relative to its own package
    sys.path.insert(0, str(api))
    try:
        from app.main import app  # noqa: PLC0415 - after the path is set
    finally:
        os.chdir(cwd)
    schema = app.openapi()
    ops = []
    for path, item in schema["paths"].items():
        if path == "/":
            continue
        for method, op in item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            tags = op.get("tags") or []
            if not any(t in PUBLIC_TAGS for t in tags):
                continue
            params = [{"name": p["name"], "in": p["in"], "required": bool(p.get("required")),
                       "type": (p.get("schema") or {}).get("type", ""),
                       "description": p.get("description", "")}
                      for p in op.get("parameters") or []]
            body = []
            payload = (op.get("requestBody") or {}).get("content", {}).get("application/json", {}).get("schema")
            if payload:
                body = _shape(payload, schema, depth=0)
            ops.append({
                "method": method.upper(),
                "path": path,
                "tags": tags,
                "summary": op.get("summary") or op.get("operationId", ""),
                "description": (op.get("description") or "").strip(),
                "auth": "api_key" if op.get("security") else "none",
                "params": params,
                "body": body,
                "samples": (op.get("x-codeSamples") or []),
                "responses": sorted(str(code) for code in (op.get("responses") or {})),
            })
    ops.sort(key=lambda o: (PUBLIC_TAGS.index(next((t for t in o["tags"] if t in PUBLIC_TAGS), "meta")),
                            o["path"], o["method"]))
    return {
        "info": {"title": schema["info"].get("title", ""), "version": schema["info"].get("version", ""),
                 "description": (schema["info"].get("description") or "").strip()},
        "generated_from": "app.openapi()",
        "tags": PUBLIC_TAGS,
        "operations": ops,
        "counts": {"operations": len(ops),
                   "paths": len({o["path"] for o in ops}),
                   "internal_paths_omitted": len(schema["paths"]) - len({o["path"] for o in ops})},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools/api_docs.py")
    ap.add_argument("--api", default=os.environ.get("ENGINEERING_API_SRC", "../pinneapple-engineering-api"),
                    help="checkout of the API to read the schema from")
    ap.add_argument("--python", help="interpreter that can import the API; runs this script again with it")
    args = ap.parse_args(argv)

    api = Path(args.api).resolve() if not Path(args.api).is_absolute() else Path(args.api)
    if args.python:
        r = subprocess.run([args.python, __file__, "--api", str(api)], check=False)
        return r.returncode

    payload = build(api)
    if not payload["operations"]:
        raise SystemExit("no public operation found: did the tags change?")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    c = payload["counts"]
    print(f"wrote {OUT.relative_to(ROOT)}: {c['operations']} operations over {c['paths']} paths "
          f"({c['internal_paths_omitted']} internal paths omitted)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
