"""Tests for pb-gravatar-url transformation logic."""

import hashlib
import pytest

# Import the functions directly by loading the script as a module
from pathlib import Path
import importlib.machinery
import importlib.util

_script_path = Path(__file__).parent.parent / "pb-gravatar-url"
_loader = importlib.machinery.SourceFileLoader("pb_gravatar_url", str(_script_path))
_spec = importlib.util.spec_from_loader("pb_gravatar_url", _loader)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

gravatar_url = _mod.gravatar_url
is_email = _mod.is_email


class TestIsEmail:
    def test_simple_email(self) -> None:
        assert is_email("user@example.com")

    def test_plus_addressing(self) -> None:
        assert is_email("user+tag@example.com")

    def test_subdomain(self) -> None:
        assert is_email("user@mail.example.co.uk")

    def test_long_tld(self) -> None:
        assert is_email("user@example.museum")

    def test_not_an_email(self) -> None:
        assert not is_email("not an email")

    def test_missing_at(self) -> None:
        assert not is_email("user.example.com")

    def test_empty(self) -> None:
        assert not is_email("")

    def test_url(self) -> None:
        assert not is_email("http://example.com")


class TestGravatarUrl:
    def test_known_hash(self) -> None:
        """Verify against a known MD5 hash."""
        email = "test@example.com"
        expected_hash = hashlib.md5(b"test@example.com").hexdigest()
        assert gravatar_url(email) == f"http://gravatar.com/avatar/{expected_hash}"

    def test_strips_whitespace(self) -> None:
        assert gravatar_url("  test@example.com  ") == gravatar_url("test@example.com")

    def test_lowercases(self) -> None:
        assert gravatar_url("TEST@EXAMPLE.COM") == gravatar_url("test@example.com")
