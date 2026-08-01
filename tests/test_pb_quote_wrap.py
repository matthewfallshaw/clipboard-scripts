"""Tests for pb-quote-wrap.

Cases carried over from the unittest suite that used to live inside the script.
"""

from __future__ import annotations

from conftest import load_script

fix_nested_quotes = load_script("pb-quote-wrap").fix_nested_quotes


def test_unquoted_string() -> None:
    assert fix_nested_quotes('An "unquoted" string') == "\"An 'unquoted' string\""


def test_already_fixed_string() -> None:
    assert fix_nested_quotes("\"An 'unquoted' string\"") == "\"An 'unquoted' string\""


def test_nested_quotes() -> None:
    assert fix_nested_quotes('"An "unquoted" string"') == "\"An 'unquoted' string\""


def test_multiple_nested_quotes() -> None:
    assert fix_nested_quotes('James said "hello", then he said "goodbye".') == (
        "\"James said 'hello', then he said 'goodbye'.\""
    )


def test_deep_nesting() -> None:
    given = (
        "James said \"Dave said 'Deep nesting is awesome!', with an annoyingly "
        'wry grin on his face", with his own annoyingly wry grin.'
    )
    expected = (
        "\"James said 'Dave said 'Deep nesting is awesome!', with an annoyingly "
        "wry grin on his face', with his own annoyingly wry grin.\""
    )
    assert fix_nested_quotes(given) == expected


def test_plain_text_just_gets_wrapped() -> None:
    assert fix_nested_quotes("plain") == '"plain"'


def test_empty_string() -> None:
    assert fix_nested_quotes("") == '""'
