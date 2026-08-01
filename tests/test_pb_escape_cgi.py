"""Tests for pb-escape-cgi."""

from conftest import load_script

mod = load_script("pb-escape-cgi")
escape_cgi = mod.escape_cgi


class TestEscapeCgi:
    def test_space_becomes_plus(self) -> None:
        assert escape_cgi("a b") == "a+b"

    def test_alphanumerics_unescaped(self) -> None:
        assert escape_cgi("abcXYZ012") == "abcXYZ012"

    def test_reserved_char_is_escaped(self) -> None:
        assert escape_cgi("a&b=c") == "a%26b%3Dc"

    def test_empty_string(self) -> None:
        assert escape_cgi("") == ""

    def test_unicode(self) -> None:
        assert escape_cgi("café") == "caf%C3%A9"

    def test_multiline(self) -> None:
        assert escape_cgi("a\nb") == "a%0Ab"


class TestRoundTrip:
    def test_round_trip(self) -> None:
        unescape_cgi = load_script("pb-unescape-cgi").unescape_cgi
        original = "héllo wörld & friends = 100%"
        assert unescape_cgi(escape_cgi(original)) == original
