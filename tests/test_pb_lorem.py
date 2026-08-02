"""Tests for pb-lorem."""

import pytest
from conftest import load_script

mod = load_script("pb-lorem")
lorem_ipsum = mod.lorem_ipsum
LOREM_PARAGRAPHS = mod.LOREM_PARAGRAPHS


class TestLoremIpsum:
    def test_default_is_one_paragraph(self) -> None:
        assert lorem_ipsum() == LOREM_PARAGRAPHS[0]

    def test_starts_with_classic_opening(self) -> None:
        assert lorem_ipsum().startswith("Lorem ipsum dolor sit amet")

    def test_multiple_paragraphs_separated_by_blank_line(self) -> None:
        result = lorem_ipsum(2)
        assert result == LOREM_PARAGRAPHS[0] + "\n\n" + LOREM_PARAGRAPHS[1]

    def test_paragraph_count_matches_requested(self) -> None:
        for n in (1, 2, 3):
            result = lorem_ipsum(n)
            assert len(result.split("\n\n")) == n

    def test_cycles_when_more_paragraphs_than_defined(self) -> None:
        n = len(LOREM_PARAGRAPHS) + 2
        result = lorem_ipsum(n)
        paragraphs = result.split("\n\n")
        assert len(paragraphs) == n
        assert paragraphs[len(LOREM_PARAGRAPHS)] == LOREM_PARAGRAPHS[0]

    def test_zero_paragraphs_raises(self) -> None:
        with pytest.raises(ValueError, match="must be at least 1"):
            lorem_ipsum(0)

    def test_negative_paragraphs_raises(self) -> None:
        with pytest.raises(ValueError, match="must be at least 1"):
            lorem_ipsum(-1)
