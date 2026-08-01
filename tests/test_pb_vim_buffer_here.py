"""Tests for pb-vim-buffer-here's target-file-selection logic."""

from pathlib import Path

from conftest import load_script

mod = load_script("pb-vim-buffer-here")
choose_target = mod.choose_target
NEW_FILE_PROMPT = mod.NEW_FILE_PROMPT
OPEN_FILE_PROMPT = mod.OPEN_FILE_PROMPT


def always_text(_path: str) -> bool:
    return True


def never_text(_path: str) -> bool:
    return False


class TestNothingSelected:
    def test_missing_path_falls_back_to_tempfile(self) -> None:
        path, dialog_text = choose_target("", always_text)
        assert path == "/tmp/tempfile.txt"
        assert dialog_text == NEW_FILE_PROMPT

    def test_vanished_path_falls_back_to_tempfile(self, tmp_path: Path) -> None:
        missing = tmp_path / "gone.txt"
        path, dialog_text = choose_target(str(missing), always_text)
        assert path == "/tmp/tempfile.txt"
        assert dialog_text == NEW_FILE_PROMPT


class TestDirectorySelected:
    def test_directory_gets_readme_inside_it(self, tmp_path: Path) -> None:
        path, dialog_text = choose_target(str(tmp_path), always_text)
        assert path == str(tmp_path / "readme.txt")
        assert dialog_text == NEW_FILE_PROMPT


class TestFileSelected:
    def test_text_file_is_opened_directly(self, tmp_path: Path) -> None:
        file_path = tmp_path / "notes.txt"
        file_path.write_text("hello")
        path, dialog_text = choose_target(str(file_path), always_text)
        assert path == str(file_path)
        assert dialog_text == OPEN_FILE_PROMPT

    def test_non_text_file_gets_readme_alongside_it(self, tmp_path: Path) -> None:
        file_path = tmp_path / "image.png"
        file_path.write_bytes(b"\x89PNG\r\n")
        path, dialog_text = choose_target(str(file_path), never_text)
        assert path == str(tmp_path / "readme.txt")
        assert dialog_text == NEW_FILE_PROMPT


class TestIsTextFile:
    def test_uses_file_command_output(self, tmp_path: Path) -> None:
        text_file = tmp_path / "notes.txt"
        text_file.write_text("hello world\n")
        assert mod.is_text_file(str(text_file)) is True

        binary_file = tmp_path / "data.bin"
        binary_file.write_bytes(bytes(range(256)))
        assert mod.is_text_file(str(binary_file)) is False
