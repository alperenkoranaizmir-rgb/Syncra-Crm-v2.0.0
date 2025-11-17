#!/usr/bin/env python3
"""Audit templates for common AdminLTE issues to start pixel-perfect pass.

Checks performed:
 - presence of `{% load static %}`
 - presence of `{% block content %}`
 - uses of CDN URLs (http:// or https://) in templates
 - occurrences of `bootstrap-icons` (to consider replacing with FontAwesome)
 - occurrences of `static/vendor` (legacy vendor folder)

This script prints a report; it does not change files.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"


def audit_file(p: Path):
    """Return a list of detected issues for template file `p`.

    Checks for missing `{% load static %}`, missing content block, CDN links
    and legacy vendor/bootstrap-icons usage.
    """
    txt = p.read_text(encoding="utf-8")
    issues = []
    if "{% static" in txt and "{% load static %}" not in txt:
        issues.append("missing {% load static %}")
    if "{% block content %}" not in txt:
        issues.append("missing {% block content %}")
    # find CDN links
    cdns = re.findall(r"https?://[\w./-]+", txt)
    if cdns:
        issues.append(f"cdn links: {len(cdns)}")
    if "bootstrap-icons" in txt:
        issues.append("uses bootstrap-icons")
    if "static/vendor" in txt:
        issues.append("uses static/vendor (legacy)")
    return issues


def main():
    """Run an audit over templates and print a summary report to stdout."""
    report = {}
    files = list(TEMPLATES.rglob("*.html"))
    for p in files:
        issues = audit_file(p)
        if issues:
            report[str(p.relative_to(ROOT))] = issues
    print("\nTemplate audit report: {} files with issues".format(len(report)))
    for f, issues in sorted(report.items()):
        print(f)
        for i in issues:
            print("  -", i)


if __name__ == "__main__":
    main()
