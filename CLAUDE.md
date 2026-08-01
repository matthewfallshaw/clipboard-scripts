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

## Notifications

```
lib/notify [--sticky] [--from NAME] [--title TEXT] [--id NAME] [--duration SECONDS] [--persist] [--] MESSAGE...
```

Routes to hammerspoon-config's `bin/notify` (non-modal, persistent-until-dismissed, stacked) when `~/code/hammerspoon-config/bin/notify` is executable; otherwise falls back to `osascript`, which understands only `--sticky` and the message.

`--from` names the notification after the calling script and is the default for both `--title` and `--id`. `pbclip.notify()` passes it automatically, from `sys.argv[0]`; bash scripts that call `lib/notify` directly pass `--from "$(basename "$0")"`. `--id` is a replace-in-place key: a second call with the same id updates that card instead of stacking a new one — so a script whose successive results should coexist, not replace each other, must pass its own unique `--id`.

**Nothing reaches disk by default.** That default lives in the backend, so `--persist` is passed straight through and its absence sends nothing. `--persist` is for an alert worth surviving a Hammerspoon restart because nothing else records it; no script needs it today.

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

## Direction

Keep dependencies minimal and setup simple. The codebase is all Python and bash; don't reintroduce Ruby.
