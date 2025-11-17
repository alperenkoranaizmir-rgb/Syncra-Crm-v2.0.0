#!/usr/bin/env python3
"""
Append a timestamped entry to CHANGELOG.md and insert a short 'Son Değişiklikler' note
into a set of project markdown files so they stay in sync.

Usage:
  python3 scripts/update_changelogs.py "Short description of change"

If no message is provided, the script will use the last git commit message (if available).
"""
import subprocess  # nosec B404 - calling git is a controlled local operation
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
FILES_TO_UPDATE = [
    ROOT / "PROGRAM_ASAMASI.md",
    ROOT / "README.md",
    ROOT / "HATALAR.md",
    ROOT / "TEMPLATES.md",
    ROOT / "TODO.md",
    ROOT / "YAPILAN_ISLER.md",
    ROOT / "YAPILMASI_GEREKENLER.md",
    ROOT / "ONERILER.md",
]


def get_message():
    """Return a user-provided message or fall back to the last git commit message.

    Priority: command-line arguments > last git commit message > manual marker.
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    # try to get last git commit message
    try:
        out = (
            subprocess.check_output(["git", "log", "-1", "--pretty=%B"])  # nosec B603 B607
            .decode()
            .strip()
        )
        return out or "(no commit message)"
    except (subprocess.CalledProcessError, OSError):
        return "(manual update)"


def append_changelog(msg: str):
    """Append a timestamped entry to the repository `CHANGELOG.md`.

    The entry is prepended to the file (keeps existing content).
    """
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"## {ts} — {msg}\n\n"
    # Prepend to CHANGELOG (keep existing content)
    if not CHANGELOG.exists():
        CHANGELOG.write_text("# CHANGELOG\n\n")
    content = CHANGELOG.read_text(encoding="utf-8")
    new_content = content + "\n" + entry
    CHANGELOG.write_text(new_content, encoding="utf-8")
    print(f"Appended to {CHANGELOG}")


def update_md_files(msg: str):
    """Insert a short 'Son Değişiklikler' note into each file in `FILES_TO_UPDATE`.

    If a target file does not exist it will be created with a header and the note.
    """
    note = f"\n### Son Değişiklikler ({datetime.now(timezone.utc).date()}):\n- {msg}\n"
    for f in FILES_TO_UPDATE:
        if not f.exists():
            f.write_text(f"# {f.name}\n\n{note}\n", encoding="utf-8")
            print(f"Created {f}")
        else:
            txt = f.read_text(encoding="utf-8")
            if "Son Değişiklikler" in txt:
                # append to existing section at end
                txt = txt.rstrip() + "\n" + note
            else:
                txt = txt + "\n" + note
            f.write_text(txt, encoding="utf-8")
            print(f"Updated {f}")


def main():
    """Script entrypoint: determine message and update changelog and markdown files."""
    msg = get_message()
    append_changelog(msg)
    update_md_files(msg)


if __name__ == "__main__":
    main()
