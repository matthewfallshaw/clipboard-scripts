"""Tests for pb-unescape-html."""

from conftest import load_script

mod = load_script("pb-unescape-html")
unescape_html = mod.unescape_html


class TestUnescapeHtml:
    def test_ampersand(self) -> None:
        assert unescape_html("a &amp; b") == "a & b"

    def test_angle_brackets(self) -> None:
        assert unescape_html("&lt;div&gt;") == "<div>"

    def test_quotes(self) -> None:
        assert unescape_html("say &quot;hi&quot;") == 'say "hi"'

    def test_apostrophe_hex_entity(self) -> None:
        assert unescape_html("it&#x27;s") == "it's"

    def test_numeric_entity(self) -> None:
        assert unescape_html("&#65;&#66;&#67;") == "ABC"

    def test_empty_string(self) -> None:
        assert unescape_html("") == ""

    def test_plain_text_unchanged(self) -> None:
        assert unescape_html("hello world") == "hello world"

    def test_multiline(self) -> None:
        assert (
            unescape_html("&lt;b&gt;x&lt;/b&gt;\n&lt;i&gt;y&lt;/i&gt;")
            == "<b>x</b>\n<i>y</i>"
        )

    def test_no_entities_is_noop(self) -> None:
        assert unescape_html("not & escaped < at all") == "not & escaped < at all"


class TestRoundTrip:
    def test_round_trip(self) -> None:
        escape_html = load_script("pb-escape-html").escape_html
        original = '<div class="a & b">it\'s <b>bold</b></div> café'
        assert unescape_html(escape_html(original)) == original
