#!/usr/bin/env python3
"""List static files that map to the same destination path and their sources.

Run from project root with the virtualenv activated:
  . .venv/bin/activate && python scripts/list_static_conflicts.py
"""
# flake8: noqa: E402
import os

# Ensure Django settings module is set before importing Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import logging
from collections import defaultdict

import django

django.setup()

from django.contrib.staticfiles import finders


def storage_repr(storage):
    # Try to display useful info about the storage/source
    cls = storage.__class__.__module__ + "." + storage.__class__.__name__
    loc = getattr(storage, "location", None) or getattr(storage, "prefix", None)
    return f"{cls} (location={loc})"


def main():
    mapping = defaultdict(list)
    for finder in finders.get_finders():
        try:
            for path, storage in finder.list([]):
                mapping[path].append(storage_repr(storage))
        except Exception as e:  # noqa: E722 - external finders may raise various errors
            # some finders may not support list without globs depending on Django version
            logging.warning("finder.list([]) failed: %s", e)
            try:
                for path, storage in finder.list(["*"]):
                    mapping[path].append(storage_repr(storage))
            except Exception as e2:  # noqa: E722
                logging.warning("finder.list([*]) also failed: %s", e2)

    conflicts = {p: s for p, s in mapping.items() if len({*s}) > 1}

    if not conflicts:
        print("No duplicate static destination paths found.")
        return

    print("Duplicate static destination paths and their sources:\n")
    for path, sources in sorted(conflicts.items()):
        print(path)
        for src in sorted(set(sources)):
            print("  -", src)
        print()


if __name__ == "__main__":
    main()
