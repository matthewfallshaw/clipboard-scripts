"""Tests for pb-unescape-quoted-printable."""

from conftest import load_script

mod = load_script("pb-unescape-quoted-printable")
unescape_quoted_printable = mod.unescape_quoted_printable


class TestUnescapeQuotedPrintable:
    def test_plain_ascii_unchanged(self) -> None:
        assert unescape_quoted_printable("hello") == "hello"

    def test_crlf_becomes_lf(self) -> None:
        assert unescape_quoted_printable("hello\r\n") == "hello\n"

    def test_percent_style_escape_decoded(self) -> None:
        assert unescape_quoted_printable("caf=C3=A9") == "café"

    def test_soft_line_break_removed(self) -> None:
        assert unescape_quoted_printable("abc=\r\ndef") == "abcdef"

    def test_empty_string(self) -> None:
        assert unescape_quoted_printable("") == ""

    def test_multiline(self) -> None:
        assert unescape_quoted_printable("line1\r\nline2\r\n") == "line1\nline2\n"


class TestRoundTrip:
    def test_round_trip(self) -> None:
        escape_quoted_printable = load_script(
            "pb-escape-quoted-printable"
        ).escape_quoted_printable
        original = "héllo\nwörld\n" + ("y" * 120)
        assert escape_quoted_printable(
            unescape_quoted_printable(escape_quoted_printable(original))
        ) == escape_quoted_printable(original)

    def test_round_trip_simple(self) -> None:
        escape_quoted_printable = load_script(
            "pb-escape-quoted-printable"
        ).escape_quoted_printable
        original = "plain text, no surprises"
        assert unescape_quoted_printable(escape_quoted_printable(original)) == original
