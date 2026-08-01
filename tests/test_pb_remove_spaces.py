"""Tests for pb-remove-spaces."""

from conftest import load_script

mod = load_script("pb-remove-spaces")
remove_spaces = mod.remove_spaces


class TestRemoveSpaces:
    def test_removes_all_spaces(self) -> None:
        assert remove_spaces("a b c") == "abc"

    def test_leaves_other_whitespace_alone(self) -> None:
        assert remove_spaces("a\tb\nc") == "a\tb\nc"

    def test_no_spaces_is_a_no_op(self) -> None:
        assert remove_spaces("abc") == "abc"

    def test_empty_string(self) -> None:
        assert remove_spaces("") == ""
