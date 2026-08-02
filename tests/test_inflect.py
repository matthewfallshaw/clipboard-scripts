"""Tests for lib/inflect.py -- word/case transforms.

`TestHumanize` ports the cases from the old `spec/pb-humanize_spec.rb`
(Ruby's `HumanizingString#humanize`), which pins the required behaviour.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from inflect import humanize, titlecase, undasherize, underscorize


class TestHumanize:
    """Cases ported from spec/pb-humanize_spec.rb."""

    def test_all_caps_sentence(self) -> None:
        assert humanize("LOREM IPSUM DOLOR SIT AMET.") == "Lorem Ipsum Dolor Sit Amet."

    def test_all_caps_lowercases_small_words(self) -> None:
        assert (
            humanize("JAKE AND THE NEVER LAND PIRATES")
            == "Jake and the Never Land Pirates"
        )

    def test_dotted_string_removes_stops(self) -> None:
        assert (
            humanize("Jake.and.the.Never.Land.Pirates")
            == "Jake and the Never Land Pirates"
        )

    def test_normalizes_episode_label(self) -> None:
        assert humanize("Pirates.S01E05") == "Pirates S01E05"


class TestHumanizeAdditional:
    """Cases not in the Ruby spec, covering behaviour visible in the source."""

    def test_underscore_becomes_space(self) -> None:
        assert humanize("some_variable_name") == "Some variable name"

    def test_at_and_dash_become_spaces(self) -> None:
        assert humanize("foo@bar-baz") == "Foo bar baz"

    def test_plain_sentence_gets_first_letter_capitalised(self) -> None:
        assert humanize("hello world") == "Hello world"

    def test_small_words_lowercased_even_outside_all_caps_branch(self) -> None:
        assert humanize("a story of the sea") == "A story of the sea"

    def test_empty_string(self) -> None:
        assert humanize("") == ""

    def test_all_caps_with_no_letters_at_all(self) -> None:
        # No lowercase letters present at all -> the all-caps branch runs
        # even though there's nothing alphabetic to capitalise.
        assert humanize("123-456") == "123 456"


class TestTitlecase:
    def test_capitalises_ordinary_words(self) -> None:
        assert titlecase("the quick brown fox") == "The Quick Brown Fox"

    def test_small_words_lowercased_in_the_middle(self) -> None:
        assert titlecase("a tale of two cities") == "A Tale of Two Cities"

    def test_small_word_capitalised_when_first(self) -> None:
        assert titlecase("the hobbit") == "The Hobbit"

    def test_small_word_capitalised_when_last(self) -> None:
        assert titlecase("something to look at") == "Something to Look At"

    def test_already_uppercase_acronym_left_alone(self) -> None:
        assert titlecase("NASA launches rocket") == "NASA Launches Rocket"

    def test_camel_case_word_left_alone(self) -> None:
        assert titlecase("get the new iPhone today") == "Get the New iPhone Today"

    def test_preserves_whitespace_structure(self) -> None:
        assert titlecase("hello   world") == "Hello   World"

    def test_hyphenated_word(self) -> None:
        assert titlecase("a well-known fact") == "A Well-Known Fact"

    def test_empty_string(self) -> None:
        assert titlecase("") == ""

    def test_single_small_word_is_capitalised(self) -> None:
        # It's the only word, so it's both first and last.
        assert titlecase("the") == "The"


class TestUnderscorize:
    """Shared by pb-underscore and pb-underscorize."""

    def test_spaces_become_underscores(self) -> None:
        assert underscorize("foo bar") == "foo_bar"

    def test_runs_are_collapsed(self) -> None:
        assert underscorize("foo  bar") == "foo_bar"
        assert underscorize("foo---bar") == "foo_bar"

    def test_mixed_separator_run_collapses(self) -> None:
        assert underscorize("Hello There,  World!") == "Hello_There_World"

    def test_leading_and_trailing_underscores_trimmed(self) -> None:
        assert underscorize("  foo bar  ") == "foo_bar"

    def test_existing_underscore_runs_collapse(self) -> None:
        assert underscorize("a__b") == "a_b"


class TestUndasherize:
    """Shared by pb-undasherize, pb-ununderscore, and pb-ununderscorize."""

    def test_dashes_and_underscores_become_spaces(self) -> None:
        assert undasherize("foo-bar_baz") == "foo bar baz"

    def test_runs_are_collapsed(self) -> None:
        assert undasherize("foo--bar") == "foo bar"
        assert undasherize("foo___bar") == "foo bar"

    def test_mixed_separator_run_collapses(self) -> None:
        assert undasherize("foo-_-bar") == "foo bar"

    def test_leading_and_trailing_spaces_trimmed(self) -> None:
        assert undasherize("--foo--") == "foo"
