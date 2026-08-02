# Clipboard Scripts

Scripts that transform the macOS pasteboard. Trigger them from Quicksilver, Alfred, or any launcher that can run a shell script.

Copy some text, invoke `pb-unformat`, and the clipboard now holds the same text with all formatting stripped. There are fifty-odd of these — sorting, case conversion, hashing, URL escaping, password generation, rich-text-to-markdown, Finder paths.

## Install

```bash
git clone https://github.com/matthewfallshaw/clipboard-scripts.git
cd clipboard-scripts
./install
```

`./install` symlinks every `pb-*` script into `bin/`, rebuilding that directory from scratch. Point your launcher at `bin/`, or add it to your `PATH`.

Nothing else to install: the scripts use only the Python standard library and macOS built-ins. `./install --dry-run` reports what it would change.

### Quicksilver

1. `⌘,` for preferences, then Catalog.
2. Click `+` at bottom left, add a File & Folder Scanner, and select this repo's `bin` directory.
3. Click the `i` at bottom right and set "Include Contents:" to Folder Contents, Depth 2.
4. `⌘R` to rescan.

Now invoke Quicksilver, type enough of a script's name to find it, and hit return.

## Writing a script

`pb-dasherize` is the canonical shape:

```python
#!/usr/bin/env python3
"""Dasherize the clipboard on macOS."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from pbclip import transform


def dasherize(text: str) -> str:
    """Collapse runs of non-word characters into single dashes, and trim them."""
    dashed = re.sub(r"[\W_]", "-", text, flags=re.ASCII)
    return re.sub(r"^-+|-+$", "", re.sub(r"-+", "-", dashed))


if __name__ == "__main__":
    transform(dasherize)
```

The logic lives in a pure function so tests can reach it; `transform` does the clipboard I/O and notification. See `lib/pbclip.py` for the rest of the toolkit, and `lib/notify` for the one place notification is implemented.

Two constraints worth knowing before you write one:

- **Standard library only.** No pip dependencies at runtime.
- **Python 3.9 syntax.** Launchers run scripts with a bare `PATH`, so `#!/usr/bin/env python3` finds macOS's system Python, not your nix or `uv` one. `tests/test_shebang_compat.py` enforces this.

Genuine one-liners can stay in bash — see `pb-downcase`.

## Tests and linting

```bash
uv run pytest           # everything except the live tests
uv run pytest -m live   # tests that hit the network or the Claude API
./lint                  # ruff + ruff format + pyright (strict) over every Python file
./lint --fix            # apply ruff's safe fixes and the formatter first
```

`./lint` exists because ruff and pyright both find files by extension, and the `pb-*` scripts have none. It finds them by shebang and hands both tools the list; the rules themselves live in `pyproject.toml`, so an editor's ruff and pyright report the same thing.

## License

[Creative Commons Attribution-Share Alike 3.0 Australia](http://creativecommons.org/licenses/by-sa/3.0/au/).
