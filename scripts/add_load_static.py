#!/usr/bin/env python3
"""Add `{% load static %}` to templates that are missing it.

Usage:
  . .venv/bin/activate && python scripts/add_load_static.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

LOAD_TAG = "{% load static %}"


def needs_load(text: str) -> bool:
    """Return True when template text appears to need `{% load static %}`.

    Detects `{% static %}` or `static(` usage and returns True if the
    `{% load static %}` tag is missing.
    """
    if re.search(r"\{%\s*load\s+static\s*%\}", text):
        return False
    # If the template contains any 'static(' or '{% static' usages, we should add the tag
    if re.search(r"\{%\s*static\s+['\"]", text) or "static(" in text:
        return True
    return False


def process_file(path: Path) -> bool:
    """Return True if `path` was updated to include `{% load static %}`."""
    text = path.read_text(encoding="utf-8")
    if needs_load(text):
        # Insert after possible template encoding comment or right at top
        lines = text.splitlines()
        insert_at = 0
        # skip leading empty lines or {% extends %} should stay at top — put load after extends
        if lines and re.match(r"\s*\{%\s*extends", lines[0]):
            # place load after extends line
            insert_at = 1
        lines.insert(insert_at, LOAD_TAG)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    return False


def main():
    """Walk templates and add `{% load static %}` where necessary."""
    changed = []
    for p in TEMPLATES_DIR.rglob("*.html"):
        try:
            if process_file(p):
                changed.append(p.relative_to(ROOT))
        except (OSError, UnicodeDecodeError) as e:
            # File I/O or decoding error — report and continue processing other templates
            print(f"Failed {p}: {e}")
    if changed:
        print("Updated templates:")
        for c in changed:
            print(" -", c)
    else:
        print("No templates needed `{% load static %}`.")


if __name__ == "__main__":
    main()
