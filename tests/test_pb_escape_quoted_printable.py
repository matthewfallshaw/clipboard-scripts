"""Tests for pb-escape-quoted-printable."""

from conftest import load_script

mod = load_script("pb-escape-quoted-printable")
escape_quoted_printable = mod.escape_quoted_printable


class TestEscapeQuotedPrintable:
    def test_plain_ascii_unchanged(self) -> None:
        assert escape_quoted_printable("hello") == "hello"

    def test_existing_newline_becomes_crlf(self) -> None:
        assert escape_quoted_printable("hello\n") == "hello\r\n"

    def test_unicode_is_percent_style_escaped(self) -> None:
        assert escape_quoted_printable("café") == "caf=C3=A9"

    def test_empty_string(self) -> None:
        assert escape_quoted_printable("") == ""

    def test_multiline(self) -> None:
        assert escape_quoted_printable("line1\nline2\n") == "line1\r\nline2\r\n"

    def test_long_line_soft_wrapped_with_crlf(self) -> None:
        result = escape_quoted_printable("a" * 100)
        assert "\r\n" in result
        for line in result.split("\r\n"):
            assert len(line) <= 76
        # Soft-break markers and content should reconstitute the original run.
        assert result.replace("=\r\n", "").replace("\r\n", "") == "a" * 100

    def test_no_bare_lf_in_output(self) -> None:
        result = escape_quoted_printable("a" * 200 + "\n" + "b" * 50)
        assert "\n" not in result.replace("\r\n", "")


class TestRoundTrip:
    def test_round_trip_plain(self) -> None:
        unescape_quoted_printable = load_script(
            "pb-unescape-quoted-printable"
        ).unescape_quoted_printable
        original = "hello world"
        assert (
            unescape_quoted_printable(escape_quoted_printable(original)) == original
        )

    def test_round_trip_unicode_multiline(self) -> None:
        unescape_quoted_printable = load_script(
            "pb-unescape-quoted-printable"
        ).unescape_quoted_printable
        original = "café\nwörld\n" + ("x" * 100)
        assert (
            unescape_quoted_printable(escape_quoted_printable(original)) == original
        )
