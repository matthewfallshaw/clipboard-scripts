"""Tests for pb-strip: default whitespace-padded-line stripping, and the
optional regex-argument mode."""

from conftest import load_script

mod = load_script("pb-strip")
strip_text = mod.strip_text


class TestDefaultBehaviour:
    """No pattern argument: trim whitespace-padded lines."""

    def test_trims_leading_and_trailing_whitespace_on_a_line(self) -> None:
        assert strip_text("  hello  \n") == "hello"

    def test_keeps_internal_whitespace(self) -> None:
        assert strip_text("  hello  world  \n") == "hello  world"

    def test_line_without_leading_whitespace_is_untouched(self) -> None:
        assert strip_text("no leading or trailing\n") == "no leading or trailing\n"

    def test_blank_lines_collapse_away(self) -> None:
        assert strip_text("line1\n\n\nline2\n") == "line1\nline2"

    def test_whitespace_only_line_becomes_empty(self) -> None:
        assert strip_text("   \n") == ""

    def test_line_with_only_leading_whitespace_is_untouched(self) -> None:
        # Needs *both* leading and trailing whitespace to match.
        assert strip_text("  a\nb  \n") == "  a\nb  \n"

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
