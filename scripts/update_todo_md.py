#!/usr/bin/env python3
"""
Lightweight script to render TODO.md from `scripts/todo_state.json` and to toggle statuses.

Usage:
  python scripts/update_todo_md.py
      Regenerates `TODO.md` from `scripts/todo_state.json`.

  python scripts/update_todo_md.py set <id> <completed|in-progress|not-started>
      Update a task status and regenerate `TODO.md`.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "scripts" / "todo_state.json"
TODO_MD = ROOT / "TODO.md"


def load_state():
    with STATE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def render_md(state):
    lines = [
        "# TODO (Canlı Liste)",
        "",
        "Bu dosya otomatik olarak `scripts/todo_state.json` dosyasından üretilir.",
        "",
    ]

    completed = [t for t in state["todos"] if t["status"] == "completed"]
    inprog = [t for t in state["todos"] if t["status"] == "in-progress"]
    notstart = [t for t in state["todos"] if t["status"] == "not-started"]

    if completed:
        lines.append("## Tamamlanan (✔)")
        lines.append("")
        for t in completed:
            lines.append(f"- ✔ {t['title']} — {t.get('description', '')}")
        lines.append("")

    if inprog:
        lines.append("## Devam Eden / Yapılmakta")
        lines.append("")
        for t in inprog:
            lines.append(f"- ⏳ {t['title']} — {t.get('description', '')}")
        lines.append("")

    if notstart:
        lines.append("## Beklemede / Başlanmamış")
        lines.append("")
        for t in notstart:
            lines.append(f"- ☐ {t['title']} — {t.get('description', '')}")
        lines.append("")

    lines.append("---")
    lines.append(
        "Bu dosya otomatik olarak güncellenebilir: "
        "`python scripts/update_todo_md.py set <id> <completed|in-progress|not-started>`"
    )
    lines.append("")
    return "\n".join(lines)


def cmd_set(state, tid, newstatus):
    found = False
    for t in state["todos"]:
        if int(t["id"]) == int(tid):
            t["status"] = newstatus
            found = True
            break
    if not found:
        print(f"Task id {tid} not found")
        sys.exit(2)
    save_state(state)
    md = render_md(state)
    TODO_MD.write_text(md, encoding="utf-8")
    print("Updated TODO.md and state file")


def main(argv):
    if len(argv) < 2:
        state = load_state()
        md = render_md(state)
        TODO_MD.write_text(md, encoding="utf-8")
        print("TODO.md regenerated from state")
        return

    cmd = argv[1]
    if cmd == "set" and len(argv) == 4:
        _, _, tid, newstatus = argv
        if newstatus not in ("completed", "in-progress", "not-started"):
            print("Status must be one of completed|in-progress|not-started")
            sys.exit(2)
        state = load_state()
        cmd_set(state, tid, newstatus)
        return

    print("Usage:")
    print("  python scripts/update_todo_md.py")
    print(
        "  python scripts/update_todo_md.py set <id> <completed|in-progress|not-started>"
    )


if __name__ == "__main__":
    main(sys.argv)
