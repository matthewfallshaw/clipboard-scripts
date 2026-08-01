# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of scripts that transform the macOS pasteboard, triggered from launchers such as Quicksilver or Alfred. See `README.md` for install and usage.

## Architecture

- **Scripts**: root-level `pb-*` files — 42 Python, 9 bash. Extensionless and executable.
- **`lib/pbclip.py`**: the shared toolkit — `paste`, `copy`, `notify`, `transform`, `osascript`, `find_binary`, `require_binary`, `die`.
- **`lib/notify`**: the single notification implementation. Every script goes through it, so swapping the backend is a one-file change.
- **`lib/inflect.py`**, **`lib/textstats.py`**: word/case transforms and word counting, shared between related scripts.
- **`install`**: symlinks `pb-*` into `bin/`, rebuilding it from scratch.
- **`tests/`**: pytest. `tests/conftest.py` provides `load_script("pb-foo")` to import an extensionless script as a module.

## Commands

```bash
./install               # symlink scripts into bin/
./install --dry-run     # report what would change
uv run pytest           # all tests except live ones
uv run pytest -m live   # tests that hit the network or the Claude API
```

## Constraints

**Standard library only at runtime.** No pip dependencies in the scripts. `uv` is for tests.

**Python 3.9 syntax.** Launchers run scripts with a bare `PATH`, so `#!/usr/bin/env python3` resolves to macOS's system Python (3.9), not to `uv`'s or nix's. Start every script with `from __future__ import annotations`; no `match`, no runtime `X | Y` unions. `tests/test_shebang_compat.py` enforces this and the executable bit.

**Resolve `__file__` before finding `lib/`.** `bin/pb-foo` is a symlink to the repo root, so scripts use `Path(__file__).resolve().parent / "lib"` (Python) or `dirname "$(readlink -f "$0")"` (bash). Anything else breaks when run through `bin/`.

**Notify through `lib/notify`.** Never `growlnotify` (gone), never a raw `osascript` notification.

**Put the logic in a pure function.** `transform(fn)` handles the clipboard I/O; tests exercise `fn`.

## Project Refactoring Goals

The Ruby-to-Python migration is complete — no Ruby remains. Remaining direction: keep dependencies minimal and setup simple.

### Sticky notifications want replacing

`lib/notify --sticky` uses `display alert` — persistent, but a modal that steals focus. Matt hates it. Used by `pb-rot13`, `pb-peek-at-clipboard` (over 100 chars), `pb-peek-at-clipboard-sticky`, `pb-pwgen-sticky`.

The replacement is specced in `~/code/hammerspoon-config/TODO.md` and not yet built. Nothing in this repo changes when it is, beyond `lib/notify` — keep it that way.

### Open question for Matt

`pb-strip`'s default regex swallows the newline after each trimmed line, so two adjacent padded lines get glued together. Left as-is pending a decision: trim each line but keep the line breaks?
