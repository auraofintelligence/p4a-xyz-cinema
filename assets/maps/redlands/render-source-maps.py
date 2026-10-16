"""Render reviewed, downloaded map originals. No network acquisition or invented geometry.

Requires Poppler pdftoppm. Source editions, rights and update dates are in
content/councils/redland.json. Keep full pages, legends and attribution intact.
Run from the repository root: python assets/maps/redlands/render-source-maps.py
"""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
for source in root.glob("*.pdf"):
    if source.name == "queensland-local-election-report-2024.pdf":
        continue
    subprocess.run(["pdftoppm", "-f", "1", "-singlefile", "-scale-to", "2200", "-png",
                    str(source), str(source.with_suffix(""))], check=True)
    print(source.with_suffix(".png").name)
