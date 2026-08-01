"""Tests for pb-pwgen-sticky: alternates and dictionary-word passphrase."""

import random
from pathlib import Path

from conftest import load_script

mod = load_script("pb-pwgen-sticky")
generate_password = mod.generate_password
clean_word = mod.clean_word
random_words = mod.random_words
find_wordlist = mod.find_wordlist
build_message = mod.build_message
PWGEN_LENGTH = mod.PWGEN_LENGTH
WORD_COUNT = mod.WORD_COUNT


class TestGeneratePassword:
    def test_default_length(self) -> None:
        assert len(generate_password()) == PWGEN_LENGTH

    def test_all_character_classes_present(self) -> None:
        pw = generate_password()
        assert any(c in mod.LOWER for c in pw)
        assert any(c in mod.UPPER for c in pw)
        assert any(c in mod.DIGITS for c in pw)
        assert any(c in mod.PUNCTUATION for c in pw)


class TestCleanWord:
    def test_downcases(self) -> None:
        assert clean_word("Hello") == "hello"

    def test_strips_apostrophe_bang_ampersand_dot_slash_digits(self) -> None:
        assert clean_word("it's!&./0great1") == "itsgreat"

    def test_replaces_whitespace_with_dash(self) -> None:
        assert clean_word("two words") == "two-words"

    def test_replaces_non_word_chars_with_dash(self) -> None:
        assert clean_word("foo+bar") == "foo-bar"

    def test_replaces_multiple_non_word_runs(self) -> None:
        assert clean_word("a@#b") == "a--b"

    def test_plain_word_unchanged(self) -> None:
        assert clean_word("apple") == "apple"


class TestRandomWords:
    def test_returns_requested_count(self, tmp_path: Path) -> None:
        wordlist = tmp_path / "words.txt"
        wordlist.write_text("\n".join(f"word{i}" for i in range(100)) + "\n")
        words = random_words(wordlist, count=10, rng=random.Random(1))
        assert len(words) == 10

    def test_caps_count_at_available_lines(self, tmp_path: Path) -> None:
        wordlist = tmp_path / "words.txt"
        wordlist.write_text("only\nfour\nlines\nhere\n")
        words = random_words(wordlist, count=WORD_COUNT, rng=random.Random(1))
        assert len(words) == 4

    def test_words_are_cleaned(self, tmp_path: Path) -> None:
        wordlist = tmp_path / "words.txt"
        wordlist.write_text("HELLO!\n")
        words = random_words(wordlist, count=1, rng=random.Random(1))
        assert words == ["hello"]

    def test_deterministic_with_seeded_rng(self, tmp_path: Path) -> None:
        wordlist = tmp_path / "words.txt"
        wordlist.write_text("\n".join(f"word{i}" for i in range(50)) + "\n")
        words1 = random_words(wordlist, count=5, rng=random.Random(99))
        words2 = random_words(wordlist, count=5, rng=random.Random(99))
        assert words1 == words2


class TestFindWordlist:
    def test_finds_crossword_file_case_insensitively(self, tmp_path: Path, monkeypatch) -> None:
        documents = tmp_path / "Documents"
        wordlist_dir = documents / "wordlists"
        wordlist_dir.mkdir(parents=True)
        target = wordlist_dir / "moby-CROSSWORD-117969"
        target.write_text("a\nb\n")
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        assert find_wordlist() == target

    def test_missing_documents_dir_returns_none(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        assert find_wordlist() is None

    def test_no_matching_wordlist_returns_none(self, tmp_path: Path, monkeypatch) -> None:
        documents = tmp_path / "Documents"
        (documents / "wordlists").mkdir(parents=True)
        (documents / "wordlists" / "moby-names-21986").write_text("a\n")
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        assert find_wordlist() is None

    def test_survives_renamed_wordlist_directory(self, tmp_path: Path, monkeypatch) -> None:
        documents = tmp_path / "Documents"
        wordlist_dir = documents / "wordlist-archive-2026"
        wordlist_dir.mkdir(parents=True)
        target = wordlist_dir / "some-crossword-list"
        target.write_text("a\n")
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        assert find_wordlist() == target


class TestBuildMessage:
    def test_includes_header_and_alternates(self) -> None:
        message = build_message(["passwordA", "passwordB"], [])
        assert message.startswith("New password in clipboard.\n\nOther options:\n")
        assert "    passwordA" in message
        assert "    passwordB" in message

    def test_includes_words_when_present(self) -> None:
        message = build_message(["pw1"], ["cat", "dog"])
        assert message.endswith("cat dog")

    def test_omits_word_section_when_no_wordlist(self) -> None:
        message = build_message(["pw1", "pw2"], [])
        assert "cat" not in message
        assert message.count("\n\n") == 1  # only the header/options separator
