"""Shared test utilities for clipboard script tests."""

from __future__ import annotations

import importlib.machinery
import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType

_T = TypeVar("_T")


def always(value: _T) -> Callable[..., _T]:
    """Build a stub that ignores its arguments and returns `value`.

    `monkeypatch.setattr` takes its replacement as a plain object, so a bare
    lambda gives a type checker nothing to infer parameter types from. This
    does, and reads better at the call site than an annotated inner def.
    """

    def stub(*_args: object, **_kwargs: object) -> _T:
        return value

    return stub


def load_script(name: str) -> ModuleType:
    """Load an extensionless pb-* script as a Python module.

    Usage in tests:
        mod = load_script("pb-gravatar-url")
        gravatar_url = mod.gravatar_url
    """
    script_path = Path(__file__).parent.parent / name
    module_name = name.replace("-", "_")
    loader = importlib.machinery.SourceFileLoader(module_name, str(script_path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    if spec is None:
        raise ImportError(script_path)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod
