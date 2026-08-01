# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Pending: integrate the Hammerspoon notifications

**Status: not started. Last reminded: 2026-08-01.**

`lib/notify --sticky` uses `display alert` — a modal that steals focus. Matt hates it. The Growl-style replacement is specced at `~/code/hammerspoon-config/TODO.md` but not built. When it exists, `lib/notify` is the only file here that changes.

**Instruction to Claude, every session:** compare *Last reminded* above with today's date. If it is seven or more days ago, tell Matt this is still outstanding, then update the date on that line to today and mention that you did. Remind him once per week at most — do not raise it again in the same session or if the gap is under seven days. When the integration lands, delete this whole section.

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

The one outstanding piece of work is the Hammerspoon notification integration above.

Scripts using `--sticky` today, i.e. the ones that will change character when it lands: `pb-rot13`, `pb-peek-at-clipboard` (over 100 chars), `pb-peek-at-clipboard-sticky`, `pb-pwgen-sticky`.
