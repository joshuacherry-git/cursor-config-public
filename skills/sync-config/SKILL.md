---
name: sync-config
description: >-
  Commit and push changes to the cursor-config repo (skills, agents, rules,
  MCP config, editor settings, thoughts, specs) and sync the public repo. Use when
  the user says "sync config", "push config", "save config", "commit skills",
  "commit agents", or asks to push Cursor configuration changes to GitHub.
---

# Sync Cursor Config

Stage, commit, and push all pending changes in `~/code/cursor-config/`, then sync the public repo.

## Phase 1: Push Private Repo

1. Run `git -C ~/code/cursor-config status --short` to see what changed.
2. If there are no changes, tell the user everything is already up to date and skip to Phase 2 (the public repo may still need syncing).
3. Run `git -C ~/code/cursor-config diff` to review the actual changes.
4. Group changes by category for the commit message:
   - `skills/` — skill additions or edits
   - `agents/` — agent additions or edits
   - `rules/` — rule additions or edits
   - `mcp.json` — MCP server config changes
   - `editor/` — settings or keybinding changes
   - `thoughts/` — journal entries (daily, decisions, ideas, TILs, etc.)
   - `specs/` — spec packages (`spec.md`, `_refinement/`, etc.)
   - `extensions.txt` — extension list changes
   - `public/` — public repo overlay files
   - Root files — install.sh, README.md, .gitignore, sync-public.sh
5. Stage all changes: `git -C ~/code/cursor-config add -A`
6. Commit with a message summarizing what changed, using this format:

   ```
   config: <brief summary>

   <category>: <what changed>
   <category>: <what changed>
   ```

   Example:

   ```
   config: add web-scraping rule, update mcp servers

   rules: add web-scraping.mdc
   mcp: add sourcegraph server
   ```

7. Push to origin: `git -C ~/code/cursor-config push`
8. Confirm to the user what was committed and pushed.

## Phase 2: Sync Public Repo

9. Run `~/code/cursor-config/sync-public.sh` to rsync skills, agents, and rules into `~/code/cursor-config-public/`.
10. Run `git -C ~/code/cursor-config-public status --short` to check if the sync produced any changes.
11. If there are no changes in the public repo, tell the user the public repo is already up to date and stop.
12. Stage all changes: `git -C ~/code/cursor-config-public add -A`
13. Commit with a message mirroring the private commit summary, prefixed with `sync:`:

    ```
    sync: <same brief summary as the private commit>
    ```

14. Push to origin: `git -C ~/code/cursor-config-public push`
15. Confirm to the user what was synced and pushed to the public repo.
