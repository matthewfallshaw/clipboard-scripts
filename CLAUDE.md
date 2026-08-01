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
- **`bin/` is wiped and rebuilt** by `./install`, which removed 64 stale entries (old script copies plus leftover Bundler binstubs). It's still gitignored.
- **`pb-sentence-case` timeout is 60s** (`CLAUDE_TIMEOUT_SECONDS`), up from a buried 10s that was below the ~8s typical round trip — some invocations were silently falling back to the regex. Debug output now needs `PB_DEBUG=1`.
- **`pb-pwgen` no longer shells out to `pwgen`**; it uses Python's `secrets` with the symbol set `!@#$%^*-_=+` (quotes, backslash, `&`, `/`, `<>`, brackets, `|`, `;:,~` excluded as paste-hostile). The old `pwgen` default used no symbols at all.
- **Word counting is Unicode-aware**, so "café résumé" counts as 2 words. Ruby's `\w` was ASCII-only and counted 4.
- **`pb-tomarkdown` no longer needs `clipdown`.** It reads the pasteboard's `public.html` flavour and converts with a stdlib `html.parser` converter, which beat `clipdown` on multi-paragraph blockquotes and nested-list indentation.
- **Deleted**: `pb-qrencode` (as asked), plus `pb-bit-ly`, `pb-pivotal-lookup`, `pb-passwd-composer`, `pb-markdown-to-html`, `pb-html-to-textile`, `pb-textile-to-html` (already staged for deletion before this work).
- **`~/.dotfiles_secrets` is gone**, along with the Rakefile machinery that substituted secrets at install time. The only scripts that used it were the deleted ones. Nothing currently needs a secret; if something does, use `security find-generic-password`.
- **Behaviour deliberately preserved despite looking wrong**: `pb-underscore` does not collapse internal separator runs ("Hello There,  World" gives `Hello_There__World`), matching the Ruby. `pb-strip`'s default regex merges adjacent padded lines. Both were verified against real Ruby before porting.
- **Bugs fixed in passing**: `pb-vidir-here` ignored the selected directory and hardcoded this repo's `bin/`; `pb-de-redirect-link` spoke plain HTTP on port 80 even for `https://` URLs, and crashed on relative `Location` headers; `pb-finder-path`/`-xdropbox` looked for `lib/` outside the repo; `pb-json-dumps` added a spurious trailing newline; `pb-define` interpolated the clipboard into a URL unescaped; `pb-escape-html` never worked because `htmlentities` was never in the Gemfile.
- **`pb-lorem` and `pb-pwgen-pin` were silently broken** (missing `lorem` binary, missing `growlnotify`) and now work.
