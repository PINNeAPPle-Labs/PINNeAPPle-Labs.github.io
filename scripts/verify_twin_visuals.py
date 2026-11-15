#!/usr/bin/env python3
"""Fail unless all 50 WebP files and 100 rendered image references are present."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "assets/twin-visuals/manifest.json").read_text(encoding="utf-8"))
images = manifest["images"]
assert len(images) == 50, f"Expected 50 twins, got {len(images)}"
for slug, entry in images.items():
    path = ROOT / entry["file"]
    assert path.is_file(), f"Missing image: {path}"
    data = path.read_bytes()
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP", f"Invalid WebP: {path}"
    for lang in ("pt", "en"):
        prefix = "en/" if lang == "en" else ""
        detail = ROOT / f"{prefix}digital-twins/{slug}/index.html"
        assert detail.is_file(), f"Missing detail page: {detail}"
        html = detail.read_text(encoding="utf-8")
        assert entry["file"] in html, f"Image not used on detail: {detail}"
        assert "bring-your-problem" in html, f"CTA missing: {detail}"
for lang in ("pt", "en"):
    prefix = "en/" if lang == "en" else ""
    catalog = (ROOT / f"{prefix}digital-twins/index.html").read_text(encoding="utf-8")
    assert catalog.count('class="twin"') == 50, f"Expected 50 cards in {lang}"
    for entry in images.values():
        assert entry["file"] in catalog, f"Catalog missing image: {entry['file']}"
print("Verified 50 WebP assets, 100 illustrated detail pages and bilingual catalogs.")
