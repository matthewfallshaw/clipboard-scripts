"""Shared test utilities for clipboard script tests."""

import importlib.machinery
import importlib.util
from pathlib import Path
from types import ModuleType


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
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
