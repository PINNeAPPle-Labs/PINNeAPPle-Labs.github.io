"""Generate the 100 bilingual Digital Twin detail pages from the published catalogs.

The catalogs are the source of truth for title, domain, status, issue and slug.
Templates preserve the approved public detail-page layout.
"""
from __future__ import annotations

from html import escape, unescape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
CARD = re.compile(r'<article\s+class="twin"(?=[^>]*data-domain=")([\s\S]*?)</article>')
ATTR = re.compile(r'data-(domain|status|name)="([^"]*)"')


def catalog_items(lang: str) -> list[dict[str, str]]:
    path = ROOT / ("en/digital-twins/index.html" if lang == "en" else "digital-twins/index.html")
    source = path.read_text(encoding="utf-8")
    items = []
    for match in CARD.finditer(source):
        card = match.group(0)
        attrs = {key: unescape(value) for key, value in ATTR.findall(card)}
        title = re.search(r"<h2>(.*?)</h2>", card, re.S)
        issue = re.search(r"github\.com/PINNeAPPle-Labs/PINNeAPPle/issues/(\d+)", card)
        detail = re.search(r'href="\./([a-z0-9-]+)/"', card)
        if not (title and issue and detail and attrs.get("domain") and attrs.get("status")):
            raise ValueError(f"Incomplete twin catalog entry: {card[:160]}")
        visual = re.search(r'<div class="scene">([\s\S]*?)</div>', card)
        if not visual:
            raise ValueError(f"Missing catalog illustration: {card[:160]}")
        items.append({
            "title": unescape(title.group(1)),
            "domain": attrs["domain"],
            "status": attrs["status"],
            "issue": issue.group(1),
            "slug": detail.group(1),
            "visual": visual.group(1),
        })
    if len(items) != 50 or len({item["slug"] for item in items}) != 50:
        raise ValueError(f"Expected exactly 50 distinct {lang} twins, found {len(items)}")
    return items


def image_for_twin(lang: str, item: dict[str, str]) -> str | None:
    manifest_path = ROOT / "assets/twin-visuals/manifest.json"
    if not manifest_path.is_file():
        return None
    record = json.loads(manifest_path.read_text(encoding="utf-8")).get("images", {}).get(item["slug"])
    if not record:
        return None
    asset = ROOT / record["file"]
    if not asset.is_file():
        return None  # Do not publish broken image links before the binary is deployed.
    alt = escape(record["alt_en" if lang == "en" else "alt_pt"], quote=True)
    root_prefix = "../../../" if lang == "en" else "../../"
    return f'<img src="{root_prefix}{record["file"]}" alt="{alt}" loading="lazy" decoding="async" style="max-width:100%;height:auto;display:block">'


def detail_page(lang: str, item: dict[str, str]) -> str:
    template = (ROOT / f"templates/twin-detail-{lang}.html").read_text(encoding="utf-8")
    status = (
        ("MVP inicial, não verificado" if lang == "pt" else "Initial MVP, not independently verified")
        if item["status"] == "MVP"
        else ("Conceito, implementação pendente" if lang == "pt" else "Concept, implementation pending")
    )
    for key, value in {
        "TITLE": escape(item["title"], quote=True),
        "DOMAIN": escape(item["domain"], quote=True),
        "SLUG": item["slug"],
        "STATUS": status,
        "ISSUE": item["issue"],
        "VISUAL": image_for_twin(lang, item) or item["visual"],
    }.items():
        template = template.replace("{{" + key + "}}", value)
    if "{{" in template:
        raise ValueError(f"Unresolved placeholder in {lang}/{item['slug']}")
    return template


def update_catalog_images() -> list[str]:
    """Upgrade catalog cards to local WebP assets, preserving SVG fallbacks."""
    changed = []
    for lang in ("pt", "en"):
        rel = "en/digital-twins/index.html" if lang == "en" else "digital-twins/index.html"
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        import json
        manifest = json.loads((ROOT / "assets/twin-visuals/manifest.json").read_text(encoding="utf-8"))["images"]
        prefix = "../../" if lang == "en" else "../"
        def transform(match):
            card = match.group(0)
            slug_match = re.search(r'href="\./([a-z0-9-]+)/"', card)
            if not slug_match:
                return card
            slug = slug_match.group(1)
            entry = manifest.get(slug)
            if not entry or not (ROOT / entry["file"]).is_file():
                return card
            alt = escape(entry["alt_en" if lang == "en" else "alt_pt"], quote=True)
            visual = f'<div class="scene"><img src="{prefix}{entry["file"]}" alt="{alt}" loading="lazy" decoding="async" style="width:100%;height:100%;object-fit:cover;display:block"></div>'
            return re.sub(r'<div class="scene">[\s\S]*?</div>', lambda _: visual, card, count=1)
        output = CARD.sub(transform, source)
        if output != source:
            path.write_text(output, encoding="utf-8")
            changed.append(rel)
    return changed


def build_twin_pages() -> list[str]:
    written = []
    for lang in ("pt", "en"):
        prefix = "en/" if lang == "en" else ""
        for item in catalog_items(lang):
            rel = f"{prefix}digital-twins/{item['slug']}/index.html"
            output = ROOT / rel
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(detail_page(lang, item), encoding="utf-8")
            written.append(rel)
    if len(written) != 100:
        raise ValueError("Expected exactly 100 bilingual detail pages")
    return written
