"""Every script must run under the Python a launcher will actually give it.

Quicksilver and Alfred invoke scripts with a bare PATH, so `#!/usr/bin/env python3`
resolves to the macOS system Python (3.9), not to whatever `uv` or a nix profile
provides. A script using newer syntax fails silently at launch time — which is
exactly the class of breakage this suite exists to catch.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_DIR = Path(__file__).resolve().parent.parent
SYSTEM_PYTHON = Path("/usr/bin/python3")


def python_scripts() -> "list[Path]":
    """Repo-root pb-* scripts plus lib modules with a python3 shebang."""
    found = [p for p in sorted(REPO_DIR.glob("pb-*")) if is_python(p)]
    found.extend(sorted(REPO_DIR.glob("lib/*.py")))
    found.append(REPO_DIR / "install")
    return [p for p in found if p.is_file()]


def is_python(path: Path) -> bool:
    if not path.is_file():
        return False
    with path.open("rb") as handle:
        return b"python" in handle.readline()


@pytest.mark.parametrize("script", python_scripts(), ids=lambda p: p.name)
def test_compiles_under_system_python(script: Path) -> None:
    if not SYSTEM_PYTHON.exists():
        pytest.skip("no /usr/bin/python3 on this machine")
    result = subprocess.run(
        [str(SYSTEM_PYTHON), "-m", "py_compile", str(script)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_found_some_scripts() -> None:
    """Guard against the glob silently matching nothing."""
    assert len(python_scripts()) > 5


@pytest.mark.parametrize(
    "script", [p for p in sorted(REPO_DIR.glob("pb-*")) if p.is_file()],
    ids=lambda p: p.name,
)
def test_is_executable(script: Path) -> None:
    assert script.stat().st_mode & 0o100, "%s is not executable" % script.name
