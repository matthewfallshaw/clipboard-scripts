"""Tests for pb-json-dumps."""

import json

from conftest import load_script

mod = load_script("pb-json-dumps")
json_dumps = mod.json_dumps


class TestJsonDumps:
    def test_simple_string(self) -> None:
        assert json_dumps("hello") == '"hello"'

    def test_string_with_quotes(self) -> None:
        assert json_dumps('say "hi"') == json.dumps('say "hi"')

    def test_multiline_string(self) -> None:
        assert json_dumps("line1\nline2") == json.dumps("line1\nline2")

    def test_no_trailing_newline_added(self) -> None:
        # Clipboard content with no trailing newline must not gain one.
        assert json_dumps("no newline here") == '"no newline here"'

    def test_preserves_existing_trailing_newline(self) -> None:
        # Clipboard content that does have a trailing newline must keep
        # exactly what was there - not a synthetic extra one.
        assert json_dumps("has newline\n") == json.dumps("has newline\n")

    def test_empty_string(self) -> None:
        assert json_dumps("") == '""'
