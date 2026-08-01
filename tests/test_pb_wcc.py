"""Tests for pb-wcc message formatting (character count, then word count)."""

from __future__ import annotations

from conftest import load_script

mod = load_script("pb-wcc")
char_count_message = mod.char_count_message


class TestCharCountMessage:
    def test_simple_sentence(self) -> None:
        assert char_count_message("hello world") == "11 characters\n(2 words)"

    def test_empty_string(self) -> None:
        assert char_count_message("") == "0 characters\n(0 words)"

    def test_hyphenated_word_counts_as_one(self) -> None:
        assert char_count_message("well-known fact") == "15 characters\n(2 words)"

    def test_unicode(self) -> None:
        assert char_count_message("café") == "4 characters\n(1 words)"
