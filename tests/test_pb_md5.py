"""Tests for pb-md5."""

from __future__ import annotations

from conftest import load_script

md5_hex = load_script("pb-md5").md5_hex


def test_known_digest() -> None:
    assert md5_hex("hello") == "5d41402abc4b2a76b9719d911017c592"


def test_empty_string() -> None:
    assert md5_hex("") == "d41d8cd98f00b204e9800998ecf8427e"


def test_digest_is_32_hex_chars() -> None:
    digest = md5_hex("anything at all")
    assert len(digest) == 32
    assert all(c in "0123456789abcdef" for c in digest)


def test_unicode_hashes_as_utf8() -> None:
    assert md5_hex("café") == "07117fe4a1ebd544965dc19573183da2"


def test_whitespace_is_significant() -> None:
    assert md5_hex("hello") != md5_hex("hello\n")
