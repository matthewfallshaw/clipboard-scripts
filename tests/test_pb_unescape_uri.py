"""Tests for pb-unescape-uri."""

from conftest import load_script

mod = load_script("pb-unescape-uri")
unescape_uri = mod.unescape_uri


class TestUnescapeUri:
    def test_space(self) -> None:
        assert unescape_uri("a%20b") == "a b"

    def test_percent_decode(self) -> None:
        assert unescape_uri("100%25") == "100%"

    def test_unicode(self) -> None:
        assert unescape_uri("caf%C3%A9") == "café"

    def test_empty_string(self) -> None:
        assert unescape_uri("") == ""

    def test_no_escapes_is_noop(self) -> None:
        assert unescape_uri("plain text") == "plain text"

    def test_multiline(self) -> None:
        assert unescape_uri("a%0Ab") == "a\nb"

    def test_plus_is_not_space(self) -> None:
        # Unlike CGI/form decoding, URI unescape does not treat "+" as space.
        assert unescape_uri("a+b") == "a+b"


class TestRoundTrip:
    def test_round_trip(self) -> None:
        escape_uri = load_script("pb-escape-uri").escape_uri
        original = "héllo wörld/path?q=a b&x=100%"
        assert unescape_uri(escape_uri(original)) == original
