#!/bin/bash
# Onboarding helper to enable local git hooks for this repository.
# Run this once per developer machine to enable the provided .githooks scripts.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_DIR="$REPO_ROOT/.githooks"

echo "Enabling repository hooks from: $HOOK_DIR"
if [ ! -d "$HOOK_DIR" ]; then
  echo "Hook directory not found: $HOOK_DIR" >&2
  exit 1
fi

git config core.hooksPath "$HOOK_DIR"
chmod +x "$HOOK_DIR"/* || true

echo "Hooks enabled. You can now commit and post-commit hook will update changelogs automatically."

echo "If you want to revert to default hooks path run: git config --unset core.hooksPath"
