"""Tests for pb-define's URL-building logic."""

from conftest import load_script

mod = load_script("pb-define")
dict_url = mod.dict_url


class TestDictUrl:
    def test_simple_word(self) -> None:
        assert dict_url("hello") == "dict:///hello"

    def test_strips_surrounding_whitespace(self) -> None:
        assert dict_url("  hello  \n") == "dict:///hello"

    def test_phrase_with_spaces_is_percent_encoded(self) -> None:
        assert dict_url("hello world") == "dict:///hello%20world"

    def test_special_characters_are_percent_encoded(self) -> None:
        # Characters that would otherwise break the URL or a shell command
        # (quotes, slashes, ampersands, backticks) must be escaped.
        result = dict_url('a/b "c" & `d`')
        assert " " not in result
        assert '"' not in result
        assert "`" not in result
        assert "/" not in result.removeprefix("dict:///")
