"""Tests for pb-unescape-cgi."""

from conftest import load_script

mod = load_script("pb-unescape-cgi")
unescape_cgi = mod.unescape_cgi


class TestUnescapeCgi:
    def test_plus_becomes_space(self) -> None:
        assert unescape_cgi("a+b") == "a b"

    def test_percent_decode(self) -> None:
        assert unescape_cgi("a%26b%3Dc") == "a&b=c"

    def test_empty_string(self) -> None:
        assert unescape_cgi("") == ""

    def test_unicode(self) -> None:
        assert unescape_cgi("caf%C3%A9") == "café"

    def test_multiline(self) -> None:
        assert unescape_cgi("a%0Ab") == "a\nb"

    def test_no_escapes_is_noop_except_plus(self) -> None:
        assert unescape_cgi("plain-text") == "plain-text"


class TestRoundTrip:
    def test_round_trip(self) -> None:
        escape_cgi = load_script("pb-escape-cgi").escape_cgi
        original = "héllo wörld & friends = 100%"
        assert escape_cgi(unescape_cgi(escape_cgi(original))) == escape_cgi(original)
