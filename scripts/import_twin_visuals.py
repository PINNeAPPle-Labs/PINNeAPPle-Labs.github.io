#!/usr/bin/env python3
"""Import the prepared 50-image ZIP into this repository, then rebuild and verify.

Usage: python3 scripts/import_twin_visuals.py /path/to/pinneapple-50-realistic-visuals.zip
"""
from pathlib import Path
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/twin-visuals"

def main(zip_path: Path) -> None:
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    expected = {entry["file"] for entry in manifest["images"].values()}
    if len(expected) != 50:
        raise ValueError(f"Expected 50 unique images, got {len(expected)}")
    with zipfile.ZipFile(zip_path) as archive:
        available = set(archive.namelist())
        missing = expected - available
        if missing:
            raise ValueError(f"ZIP is missing {len(missing)} required assets: {sorted(missing)}")
        for name in sorted(expected):
            output = ROOT / name
            if not output.resolve().is_relative_to(ASSETS.resolve()):
                raise ValueError(f"Unsafe image path: {name}")
            data = archive.read(name)
            if len(data) < 100 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
                raise ValueError(f"Invalid WebP: {name}")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
    subprocess.run([sys.executable, "build.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT, check=True)
    print("Imported 50 WebP images and rebuilt the bilingual site successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 scripts/import_twin_visuals.py ZIP_PATH")
    main(Path(sys.argv[1]))
