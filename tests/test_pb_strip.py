"""Tests for pb-strip: default whitespace-padded-line stripping, and the
optional regex-argument mode."""

from conftest import load_script

mod = load_script("pb-strip")
strip_text = mod.strip_text


class TestDefaultBehaviour:
    """No pattern argument: trim every line, drop the empty ones."""

    def test_trims_leading_and_trailing_whitespace_on_a_line(self) -> None:
        assert strip_text("  hello  \n") == "hello"

    def test_keeps_internal_whitespace(self) -> None:
        assert strip_text("  hello  world  \n") == "hello  world"

    def test_unpadded_line_keeps_its_text(self) -> None:
        assert strip_text("no leading or trailing\n") == "no leading or trailing"

    def test_blank_lines_are_dropped(self) -> None:
        assert strip_text("line1\n\n\nline2\n") == "line1\nline2"

    def test_whitespace_only_line_becomes_empty(self) -> None:
        assert strip_text("   \n") == ""

    def test_adjacent_padded_lines_stay_separate(self) -> None:
        """The bug this replaced glued these two into one line."""
        assert strip_text("  a  \n  b  \n") == "a\nb"

    def test_line_with_only_leading_whitespace_is_trimmed(self) -> None:
        assert strip_text("  a\nb  \n") == "a\nb"

    def test_indented_block_is_dedented(self) -> None:
        assert strip_text("    one\n    two\n    three\n") == "one\ntwo\nthree"

    def test_tabs_count_as_whitespace(self) -> None:
        assert strip_text("\ta\t\n") == "a"

    def test_single_line_without_newline(self) -> None:
        assert strip_text("  hello  ") == "hello"

    def test_empty_string(self) -> None:
        assert strip_text("") == ""


class TestPatternArgument:
    """A pattern argument deletes every match instead."""

    def test_deletes_all_matches(self) -> None:
        assert strip_text("foo123bar456", r"\d+") == "foobar"

    def test_no_matches_is_a_no_op(self) -> None:
        assert strip_text("hello world", r"\d+") == "hello world"

    def test_literal_pattern(self) -> None:
        assert strip_text("a-b-c", "-") == "abc"
