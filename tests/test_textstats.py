"""Tests for lib/textstats.py — shared word/char counting for pb-wc and pb-wcc."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))

from textstats import count_chars, count_words


class TestCountWords:
    def test_simple_sentence(self) -> None:
        assert count_words("hello world") == 2

    def test_empty_string(self) -> None:
        assert count_words("") == 0

    def test_whitespace_only(self) -> None:
        assert count_words("   \n\t  ") == 0

    def test_single_word(self) -> None:
        assert count_words("hello") == 1

    def test_hyphenated_word_counts_as_one(self) -> None:
        assert count_words("well-known fact") == 2

    def test_multiple_hyphens(self) -> None:
        assert count_words("state-of-the-art design") == 2

    def test_leading_hyphen_not_a_word(self) -> None:
        assert count_words("-hello") == 1

    def test_standalone_hyphen(self) -> None:
        assert count_words("a - b") == 3

    def test_underscores_are_word_chars(self) -> None:
        assert count_words("hello_world foo") == 2

    def test_punctuation_splits_words(self) -> None:
        assert count_words("hello, world!") == 2

    def test_numbers_are_word_chars(self) -> None:
        assert count_words("test123 456") == 2

    def test_mixed_content(self) -> None:
        assert count_words("Hello, world! This is a well-known test.") == 7

    def test_newlines_split_words(self) -> None:
        assert count_words("hello\nworld\nfoo") == 3

    def test_tabs_split_words(self) -> None:
        assert count_words("hello\tworld") == 2

    def test_unicode_word_chars(self) -> None:
        # Deliberately Unicode-aware (unlike the ASCII-only Ruby original) —
        # see the module docstring.
        assert count_words("café résumé") == 2


class TestCountChars:
    def test_empty(self) -> None:
        assert count_chars("") == 0

    def test_simple(self) -> None:
        assert count_chars("hello") == 5

    def test_includes_spaces_and_newlines(self) -> None:
        assert count_chars("a b\nc") == 5

    def test_unicode(self) -> None:
        assert count_chars("café") == 4
