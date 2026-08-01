"""Tests for pb-escape-uri."""

from conftest import load_script

mod = load_script("pb-escape-uri")
escape_uri = mod.escape_uri


class TestEscapeUri:
    def test_space_is_encoded(self) -> None:
        assert escape_uri("a b") == "a%20b"

    def test_alphanumerics_unescaped(self) -> None:
        assert escape_uri("abcXYZ012") == "abcXYZ012"

    def test_unreserved_marks_unescaped(self) -> None:
        assert escape_uri("-_.!~*'()") == "-_.!~*'()"

    def test_reserved_chars_unescaped(self) -> None:
        assert escape_uri(";/?:@&=+$,[]#") == ";/?:@&=+$,[]#"

    def test_percent_is_escaped(self) -> None:
        assert escape_uri("100%") == "100%25"

    def test_quote_char_is_escaped(self) -> None:
        assert escape_uri('"') == "%22"

    def test_empty_string(self) -> None:
        assert escape_uri("") == ""

    def test_unicode(self) -> None:
        assert escape_uri("café") == "caf%C3%A9"

    def test_multiline(self) -> None:
        assert escape_uri("a\nb") == "a%0Ab"

    def test_full_url_left_mostly_intact(self) -> None:
        url = "http://example.com/path?q=a b&x=1"
        assert escape_uri(url) == "http://example.com/path?q=a%20b&x=1"


class TestRoundTrip:
    def test_round_trip(self) -> None:
        unescape_uri = load_script("pb-unescape-uri").unescape_uri
        original = "héllo wörld/path?q=a b&x=100%"
        assert unescape_uri(escape_uri(original)) == original

    def test_already_escaped_input_gets_percent_re_escaped(self) -> None:
        # Escaping is not idempotent: a literal "%" in already-escaped text
        # gets re-escaped to %25, just like the old Ruby URI.escape.
        assert escape_uri("%20") == "%2520"
