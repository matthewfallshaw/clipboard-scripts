"""Tests for pb-pwgen password generation."""

import pytest
from conftest import load_script

mod = load_script("pb-pwgen")
generate_password = mod.generate_password
PWGEN_LENGTH = mod.PWGEN_LENGTH
LOWER = mod.LOWER
UPPER = mod.UPPER
DIGITS = mod.DIGITS
PUNCTUATION = mod.PUNCTUATION
ALL_CHARS = mod.ALL_CHARS


class TestGeneratePassword:
    def test_default_length(self) -> None:
        assert len(generate_password()) == PWGEN_LENGTH

    def test_custom_length(self) -> None:
        assert len(generate_password(30)) == 30

    def test_minimum_length(self) -> None:
        assert len(generate_password(4)) == 4

    def test_too_short_raises(self) -> None:
        with pytest.raises(ValueError, match="length must be at least"):
            generate_password(3)

    def test_contains_lowercase(self) -> None:
        pw = generate_password()
        assert any(c in LOWER for c in pw)

    def test_contains_uppercase(self) -> None:
        pw = generate_password()
        assert any(c in UPPER for c in pw)

    def test_contains_digit(self) -> None:
        pw = generate_password()
        assert any(c in DIGITS for c in pw)

    def test_contains_punctuation(self) -> None:
        pw = generate_password()
        assert any(c in PUNCTUATION for c in pw)

    def test_all_chars_from_allowed_set(self) -> None:
        pw = generate_password()
        assert all(c in ALL_CHARS for c in pw)

    def test_no_whitespace_or_quotes(self) -> None:
        # Must be safe to paste anywhere: no whitespace, quotes, or shell
        # metacharacters that would break naive pasting into a shell/URL/CSV.
        pw = generate_password(200)
        forbidden = set(" \t\n'\"`\\;:,<>&|/?[]{}()~")
        assert not (set(pw) & forbidden)

    def test_generates_different_passwords(self) -> None:
        passwords = {generate_password() for _ in range(20)}
        assert len(passwords) == 20

    def test_all_character_classes_present_across_many_runs(self) -> None:
        # At minimum length, every class must appear every time (not just on average).
        for _ in range(50):
            pw = generate_password(4)
            assert any(c in LOWER for c in pw)
            assert any(c in UPPER for c in pw)
            assert any(c in DIGITS for c in pw)
            assert any(c in PUNCTUATION for c in pw)
