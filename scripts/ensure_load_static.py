#!/usr/bin/env python3
"""Ensure `{% load static %}` is present in templates that use `{% static` but don't load the tag.

This script edits files in-place. It will:
 - walk `templates/` directory
 - for each `.html` file, if it contains `{% static` but not `{% load static %}`, it will insert
   `{% load static %}` after an `{% extends %}` line if present, otherwise at the top.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"


def process_file(p: Path):
    text = p.read_text(encoding="utf-8")
    if "{% static" not in text:
        return False
    if "{% load static %}" in text:
        return False
    lines = text.splitlines()
    # find first extends line
    for i, line in enumerate(lines[:5]):
        if line.strip().startswith("{% extends"):
            insert_at = i + 1
            break
    else:
        insert_at = 0
    lines.insert(insert_at, "{% load static %}")
    p.write_text("\n".join(lines), encoding="utf-8")
    return True


def main():
    changed = []
    for p in TEMPLATES_DIR.rglob("*.html"):
        try:
            if process_file(p):
                changed.append(str(p.relative_to(ROOT)))
        except Exception as e:  # noqa: E722
            print("ERROR", p, e)
    print("Updated", len(changed), "templates")
    for c in changed[:200]:
        print(" -", c)


if __name__ == "__main__":
    main()
