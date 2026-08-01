"""Tests for pb-finder-path-xdropbox's path-rewriting logic."""

from conftest import load_script

mod = load_script("pb-finder-path-xdropbox")
rewrite_finder_path = mod.rewrite_finder_path


class TestHomeDir:
    def test_rewrites_users_prefix_to_tilde(self) -> None:
        assert (
            rewrite_finder_path("/Users/matt/code/project/file.txt")
            == "~/code/project/file.txt"
        )

    def test_leaves_non_users_paths_alone(self) -> None:
        assert rewrite_finder_path("/tmp/foo/bar") == "/tmp/foo/bar"


class TestDropbox:
    def test_plain_dropbox(self) -> None:
        assert (
            rewrite_finder_path("/Users/matt/Dropbox/notes.txt")
            == "Dropbox:notes.txt"
        )

    def test_dropbox_with_parenthetical_suffix(self) -> None:
        assert (
            rewrite_finder_path("/Users/matt/Dropbox (Personal)/notes.txt")
            == "Dropbox:notes.txt"
        )


class TestGoogleDrive:
    def test_plain_google_drive_under_home(self) -> None:
        assert (
            rewrite_finder_path("/Users/matt/Google Drive/file")
            == "Google Drive:file"
        )

    def test_google_drive_with_parenthetical_suffix(self) -> None:
        assert (
            rewrite_finder_path(
                "/Users/matt/Google Drive (matthew.fallshaw@gmail.com)/file"
            )
            == "Google Drive:file"
        )

    def test_volumes_googledrive(self) -> None:
        assert (
            rewrite_finder_path("/Volumes/GoogleDrive/My Drive/file")
            == "Google Drive:My Drive/file"
        )

    def test_volumes_googledrive_numbered(self) -> None:
        assert (
            rewrite_finder_path("/Volumes/GoogleDrive-1/My Drive/file")
            == "Google Drive:My Drive/file"
        )


class TestUnaffectedPaths:
    def test_root_level_path(self) -> None:
        assert rewrite_finder_path("/etc/hosts") == "/etc/hosts"

    def test_empty_string(self) -> None:
        assert rewrite_finder_path("") == ""
