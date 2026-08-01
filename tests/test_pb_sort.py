"""Tests for pb-sort, ported from spec/pb-sort_spec.rb."""

from conftest import load_script

mod = load_script("pb-sort")
sort_list = mod.sort_list


class TestSortList:
    def test_sorts_multi_line_lists(self) -> None:
        assert sort_list("b\na\nd\nc") == "a\nb\nc\nd\n"

    def test_sorts_single_line_comma_separated_lists(self) -> None:
        assert sort_list("b,a,d,c") == "a,b,c,d\n"

    def test_sorts_single_line_comma_and_space_separated_lists(self) -> None:
        assert sort_list("b, a, d, c") == "a,b,c,d\n"

    def test_case_insensitive(self) -> None:
        assert sort_list("banana\nApple\ncherry") == "Apple\nbanana\ncherry\n"

    def test_ignores_leading_blank_in_comma_list(self) -> None:
        # Only a single leading space is stripped per item (matching `sed
        # 's/^ //'`), but the sort key ignores any remaining leading blanks.
        assert sort_list("b,  a") == " a,b\n"

    def test_empty_clipboard_is_a_no_op(self) -> None:
        assert sort_list("") == ""

    def test_preserves_trailing_newline_on_multi_line_input(self) -> None:
        assert sort_list("b\na\nd\nc\n") == "a\nb\nc\nd\n"
