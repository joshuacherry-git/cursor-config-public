#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CURSOR_DIR="$HOME/.cursor"

backed_up=()
linked=()
skipped=()

link() {
  local src="$1" dest="$2"

  if [ -L "$dest" ]; then
    local current
    current="$(readlink "$dest")"
    if [ "$current" = "$src" ]; then
      skipped+=("$dest (already linked)")
      return
    fi
    rm "$dest"
  elif [ -e "$dest" ]; then
    local bak="$dest.bak"
    local n=1
    while [ -e "$bak" ]; do
      bak="$dest.bak.$n"
      n=$((n + 1))
    done
    mv "$dest" "$bak"
    backed_up+=("$dest -> $bak")
  fi

  mkdir -p "$(dirname "$dest")"
  ln -s "$src" "$dest"
  linked+=("$dest -> $src")
}

echo "=== Cursor Config Install (Public) ==="
echo "Repo: $REPO_DIR"
echo

link "$REPO_DIR/skills" "$CURSOR_DIR/skills"
link "$REPO_DIR/agents" "$CURSOR_DIR/agents"
link "$REPO_DIR/rules"  "$CURSOR_DIR/rules"

echo "--- Symlinks ---"
if [ ${#linked[@]} -gt 0 ]; then
  for item in "${linked[@]}"; do echo "  LINKED: $item"; done
fi
if [ ${#skipped[@]} -gt 0 ]; then
  for item in "${skipped[@]}"; do echo "  SKIPPED: $item"; done
fi
if [ ${#backed_up[@]} -gt 0 ]; then
  echo
  echo "--- Backups ---"
  for item in "${backed_up[@]}"; do echo "  BACKUP: $item"; done
fi

echo
echo "--- Next Steps ---"
echo "  - Copy mcp-template.json to ~/.cursor/mcp.json and fill in your server URLs."
echo "  - Set up a thoughts journal at ~/code/thoughts/ (see README.md)."
echo
echo "Done."
