"""Tests for pb-gravatar-url transformation logic."""

from __future__ import annotations

import hashlib

from conftest import load_script

script = load_script("pb-gravatar-url")
gravatar_url = script.gravatar_url
is_email = script.is_email


class TestIsEmail:
    def test_simple_email(self) -> None:
        assert is_email("user@example.com")

    def test_plus_addressing(self) -> None:
        assert is_email("user+tag@example.com")

    def test_subdomain(self) -> None:
        assert is_email("user@mail.example.co.uk")

    def test_long_tld(self) -> None:
        assert is_email("user@example.museum")

    def test_surrounding_whitespace(self) -> None:
        """A copied address usually brings a trailing newline with it."""
        assert is_email("  user@example.com\n")

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
        expected = hashlib.md5(b"test@example.com", usedforsecurity=False).hexdigest()
        assert gravatar_url("test@example.com") == (
            f"https://gravatar.com/avatar/{expected}"
        )

    def test_strips_whitespace(self) -> None:
        assert gravatar_url("  test@example.com  ") == gravatar_url("test@example.com")

    def test_lowercases(self) -> None:
        assert gravatar_url("TEST@EXAMPLE.COM") == gravatar_url("test@example.com")

    def test_is_https(self) -> None:
        assert gravatar_url("test@example.com").startswith("https://")
