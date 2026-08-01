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

### To be confirmed by Matt

- **Sticky notifications are now a modal alert.** `lib/notify --sticky` shows a `display alert` dialog, detached into the background so it doesn't block the caller. It stays until dismissed, but unlike Growl's sticky it steals focus. Used by `pb-rot13`, `pb-peek-at-clipboard` (over 100 chars), `pb-peek-at-clipboard-sticky`, `pb-pwgen-sticky`. If it's too intrusive, `lib/notify` is the only file to change.
  FIXME: Urghh, I hate it. Did we have a stub attempt to implement something better via Hammerspoon? Search (via subagent) ~/.hammerspoon/ to see if anything exists in there (if it does, do not attempt to complete the work from here — look for a doc like TODO.md or CLAUDE.md that might already contain a spec for what we want, including invocation arguments, and create/append/improve a spec if not existing/good).
- **Behaviour deliberately preserved despite looking wrong**: `pb-underscore` does not collapse internal separator runs ("Hello There,  World" gives `Hello_There__World`), matching the Ruby. `pb-strip`'s default regex merges adjacent padded lines. Both were verified against real Ruby before porting.
  FIXME: Well spotted. Collapsing adjacent items seems better. Please fix.
- **Bugs fixed in passing**: … `pb-finder-path`/`-xdropbox` looked for `lib/` outside the repo; …
  FIXME: Excellent work. Please make the -xdropbox variant also convert

  | current | desired |
  | --- | ------- |
  | `~/Library/CloudStorage/GoogleDrive-matt@intelligence.org/My Drive/~templates/Style templates.gdoc` | `GoogleDrive:/My Drive/~templates/Style templates.gdoc` |
  | `~/Library/CloudStorage/GoogleDrive-matt@bellroy.com/Shared drives/Advertising/Amazon/API/OpenAPI_SponsoredProducts.json` | `GoogleDrive:/Shared drives/Advertising/Amazon/API/OpenAPI_SponsoredProducts.json` |

  (or suggest a better output form; rationale - comms about GDrive docs are usually within org, so including the account identifiers is not useful)
