"""Tests for pb-sentence-case.

The Claude-backed path is exercised by tests marked `live`, which are deselected
by default (they cost money and take ~8s each). Run them with `uv run pytest -m live`.
"""

from __future__ import annotations

import pytest

from conftest import load_script

script = load_script("pb-sentence-case")


class TestStripCodeFence:
    def test_leaves_plain_text_alone(self) -> None:
        assert script.strip_code_fence("Hello world") == "Hello world"

    def test_unwraps_bare_fence(self) -> None:
        assert script.strip_code_fence("```\nHello world\n```") == "Hello world"

    def test_unwraps_tagged_fence(self) -> None:
        assert script.strip_code_fence("```json\n{}\n```") == "{}"

    def test_keeps_internal_newlines(self) -> None:
        assert script.strip_code_fence("```\nline one\nline two\n```") == (
            "line one\nline two"
        )

    def test_leaves_unterminated_fence_alone(self) -> None:
        assert script.strip_code_fence("```\nHello") == "```\nHello"


class TestSimpleSentenceCase:
    def test_capitalises_first_letter(self) -> None:
        assert script.simple_sentence_case("hello world") == "Hello world"

    def test_capitalises_each_sentence(self) -> None:
        assert script.simple_sentence_case("this is first. this is second.") == (
            "This is first. This is second."
        )

    def test_downcases_shouting(self) -> None:
        assert script.simple_sentence_case("THE QUICK BROWN FOX") == (
            "The quick brown fox"
        )

    def test_loses_proper_nouns(self) -> None:
        """The documented limitation of the fallback — Claude is what fixes this."""
        assert script.simple_sentence_case("i love Apple products") == (
            "I love apple products"
        )

    def test_empty_string(self) -> None:
        assert script.simple_sentence_case("") == ""

    def test_preserves_line_breaks(self) -> None:
        assert script.simple_sentence_case("first line\nsecond line") == (
            "First line\nsecond line"
        )


class TestSentenceCaseFallback:
    def test_falls_back_when_claude_is_missing(self, monkeypatch) -> None:
        monkeypatch.setattr(script, "find_binary", lambda name: None)
        assert script.sentence_case("hello world. goodbye world.") == (
            "Hello world. Goodbye world."
        )

    def test_falls_back_when_claude_fails(self, monkeypatch) -> None:
        monkeypatch.setattr(script, "find_binary", lambda name: "/bin/claude")
        monkeypatch.setattr(script, "claude_sentence_case", lambda text, claude: None)
        assert script.sentence_case("hello world") == "Hello world"

    def test_uses_claude_when_it_answers(self, monkeypatch) -> None:
        monkeypatch.setattr(script, "find_binary", lambda name: "/bin/claude")
        monkeypatch.setattr(
            script, "claude_sentence_case", lambda text, claude: "I love Apple products"
        )
        assert script.sentence_case("i love apple products") == "I love Apple products"


@pytest.mark.live
class TestClaudeSentenceCase:
    """Real calls to the Claude CLI. Deselected unless `-m live`."""

    @pytest.fixture(scope="class")
    def claude(self) -> str:
        found = script.find_binary("claude")
        if not found:
            pytest.skip("claude CLI not installed")
        return found

    @pytest.mark.parametrize(
        "given,expected",
        [
            ("i love apple products", "I love Apple products"),
            ("working at bellroy is great", "Working at Bellroy is great"),
            ("google is based in california", "Google is based in California"),
            (
                "bellroy is a company. they make great products.",
                "Bellroy is a company. They make great products.",
            ),
        ],
    )
    def test_preserves_proper_nouns(
        self, claude: str, given: str, expected: str
    ) -> None:
        assert script.claude_sentence_case(given, claude) == expected

    def test_preserves_line_breaks(self, claude: str) -> None:
        """Line structure is the contract; per-line casing is the model's call."""
        result = script.claude_sentence_case("first line\nsecond line", claude)
        assert result is not None
        assert result.splitlines() == ["First line", "Second line"] or (
            result.splitlines() == ["First line", "second line"]
        )
