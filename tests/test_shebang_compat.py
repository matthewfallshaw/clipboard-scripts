"""Every script must run under the Python a launcher will actually give it.

Quicksilver and Alfred invoke scripts with a bare PATH, so `#!/usr/bin/env python3`
resolves to the macOS system Python (3.9), not to whatever `uv` or a nix profile
provides. A script using newer syntax fails silently at launch time — which is
exactly the class of breakage this suite exists to catch.

Which files count as Python here is `./lint`'s answer, so a file can't be linted
without also being held to 3.9, or vice versa. Only `tests/` is exempt: pytest
runs it under the dev interpreter, never under a launcher.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from conftest import load_script

REPO_DIR = Path(__file__).resolve().parent.parent
SYSTEM_PYTHON = Path("/usr/bin/python3")
TESTS_DIR = Path(__file__).resolve().parent


def python_scripts() -> list[Path]:
    """Every Python file a launcher (or the dev running `./install`) executes."""
    lint = load_script("lint")
    return [p for p in lint.python_files() if p.parent != TESTS_DIR]


@pytest.mark.parametrize("script", python_scripts(), ids=lambda p: p.name)
def test_compiles_under_system_python(script: Path) -> None:
    if not SYSTEM_PYTHON.exists():
        pytest.skip("no /usr/bin/python3 on this machine")
    result = subprocess.run(
        [str(SYSTEM_PYTHON), "-m", "py_compile", str(script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_found_some_scripts() -> None:
    """Guard against the glob silently matching nothing."""
    assert len(python_scripts()) > 5


def test_covers_the_extensionless_scripts() -> None:
    """The whole point: discovery must not stop at `*.py`."""
    names = {p.name for p in python_scripts()}
    assert {"pb-dasherize", "install", "lint"} <= names


@pytest.mark.parametrize(
    "script",
    [p for p in sorted(REPO_DIR.glob("pb-*")) if p.is_file()],
    ids=lambda p: p.name,
)
def test_is_executable(script: Path) -> None:
    assert script.stat().st_mode & 0o100, f"{script.name} is not executable"
