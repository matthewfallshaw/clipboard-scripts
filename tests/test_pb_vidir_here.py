"""Tests for pb-vidir-here's directory-selection logic."""

from pathlib import Path

from conftest import load_script

mod = load_script("pb-vidir-here")
target_directory = mod.target_directory


class TestTargetDirectory:
    def test_directory_selection_used_as_is(self, tmp_path: Path) -> None:
        assert target_directory(str(tmp_path)) == str(tmp_path)

    def test_file_selection_uses_parent_directory(self, tmp_path: Path) -> None:
        file_path = tmp_path / "notes.txt"
        file_path.write_text("hello")
        assert target_directory(str(file_path)) == str(tmp_path)

    def test_nonexistent_path_returns_none(self, tmp_path: Path) -> None:
        missing = tmp_path / "does-not-exist"
        assert target_directory(str(missing)) is None

    def test_empty_string_returns_none(self) -> None:
        assert target_directory("") is None
