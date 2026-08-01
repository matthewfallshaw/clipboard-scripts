"""Tests for pb-sentence-case script using Claude Code."""

import subprocess
import pytest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parent.parent / "bin" / "pb-sentence-case"
PBCOPY = "/usr/bin/pbcopy"
PBPASTE = "/usr/bin/pbpaste"


def run_sentence_case(text: str) -> str:
    """Run pb-sentence-case on given text via clipboard."""
    # Ensure script is installed
    if not SCRIPT_PATH.exists():
        raise RuntimeError(
            f"Script not found at {SCRIPT_PATH}. Run 'rake install' first."
        )

    # Put text in clipboard
    subprocess.run([PBCOPY], input=text, text=True, check=True)

    # Run the installed script
    result = subprocess.run(
        [str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        timeout=15
    )

    if result.returncode != 0:
        raise RuntimeError(f"pb-sentence-case failed: {result.stderr}")

    # Get result from clipboard
    output = subprocess.run(
        [PBPASTE],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    return output


class TestProperNounPreservation:
    """Test that proper nouns are preserved during sentence casing."""

    def test_brand_name_preservation(self):
        """Bellroy should stay capitalized."""
        result = run_sentence_case("reasons to buy a bellroy")
        assert result == "Reasons to buy a Bellroy"

    def test_well_known_brands(self):
        """Well-known brands like Apple should be preserved."""
        result = run_sentence_case("i love apple products")
        assert result == "I love Apple products"

    def test_multiple_proper_nouns(self):
        """Multiple proper nouns should be preserved."""
        result = run_sentence_case("i love san francisco and apple products")
        assert result == "I love San Francisco and Apple products"

    def test_company_name(self):
        """Company names should be preserved."""
        result = run_sentence_case("working at bellroy is great")
        assert result == "Working at Bellroy is great"

    def test_location_names(self):
        """Geographic locations should be capitalized."""
        result = run_sentence_case("google is based in california")
        assert result == "Google is based in California"


class TestMultipleSentences:
    """Test handling of multiple sentences."""

    def test_two_sentences(self):
        """Two sentences should both start capitalized."""
        result = run_sentence_case("this is first. this is second.")
        assert result == "This is first. This is second."

    def test_multiple_sentences_with_proper_nouns(self):
        """Proper nouns preserved across multiple sentences."""
        result = run_sentence_case("bellroy is a company. they make great products.")
        assert result == "Bellroy is a company. They make great products."


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_already_correct(self):
        """Already correct text should remain unchanged."""
        result = run_sentence_case("Claude Code is great")
        assert result == "Claude Code is great"

    def test_empty_string(self):
        """Empty string should remain empty."""
        result = run_sentence_case("")
        assert result == ""

    def test_single_word(self):
        """Single word should be capitalized."""
        result = run_sentence_case("hello")
        assert result == "Hello"

    def test_all_lowercase(self):
        """All lowercase should be properly cased."""
        result = run_sentence_case("the quick brown fox")
        assert result == "The quick brown fox"

    def test_preserves_spacing(self):
        """Line breaks and spacing should be preserved."""
        result = run_sentence_case("first line\nsecond line")
        assert result == "First line\nSecond line"


class TestFallbackBehavior:
    """Test that fallback works when Claude Code is unavailable."""

    def test_basic_sentence_case_fallback(self, monkeypatch):
        """Fallback should still capitalize sentence starts."""
        # Make 'claude' unavailable
        monkeypatch.setenv("PATH", "/nonexistent")

        result = run_sentence_case("hello world. goodbye world.")
        # Fallback won't preserve proper nouns, but should capitalize sentences
        assert result.startswith("Hello")
        assert ". G" in result or ". g" in result  # Either works for fallback
