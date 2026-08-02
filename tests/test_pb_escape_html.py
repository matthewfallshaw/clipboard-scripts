"""Tests for pb-escape-html."""

from conftest import load_script

mod = load_script("pb-escape-html")
escape_html = mod.escape_html


class TestEscapeHtml:
    def test_ampersand(self) -> None:
        assert escape_html("a & b") == "a &amp; b"

    def test_angle_brackets(self) -> None:
        assert escape_html("<div>") == "&lt;div&gt;"

    def test_quotes(self) -> None:
        assert escape_html('say "hi"') == "say &quot;hi&quot;"

    def test_apostrophe(self) -> None:
        assert escape_html("it's") == "it&#x27;s"

    def test_empty_string(self) -> None:
        assert escape_html("") == ""

    def test_plain_text_unchanged(self) -> None:
        assert escape_html("hello world") == "hello world"

    def test_unicode_passthrough(self) -> None:
        # html.escape only touches &, <, >, and quotes; unicode is left as-is.
        assert escape_html("café") == "café"

    def test_multiline(self) -> None:
        assert (
            escape_html("<b>x</b>\n<i>y</i>")
            == "&lt;b&gt;x&lt;/b&gt;\n&lt;i&gt;y&lt;/i&gt;"
        )

    def test_already_escaped_input_is_double_escaped(self) -> None:
        # Escaping is not idempotent: an existing entity's `&` gets re-escaped.
        # This matches the Ruby HTMLEntities behaviour, and is expected for an
        # "escape" operation (round trip is escape -> unescape, not escape -> escape).
        assert escape_html("&amp;") == "&amp;amp;"


class TestRoundTrip:
    def test_round_trip(self) -> None:
        unescape_html = mod.__dict__.get("unescape_html")
        if unescape_html is None:
            from conftest import load_script as _load

            unescape_html = _load("pb-unescape-html").unescape_html
        original = '<div class="a & b">it\'s <b>bold</b></div>'
        assert unescape_html(escape_html(original)) == original
