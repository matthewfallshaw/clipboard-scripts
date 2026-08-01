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
    """Google Drive lives under ~/Library/CloudStorage/GoogleDrive-<account>/."""

    def test_my_drive(self) -> None:
        assert rewrite_finder_path(
            "/Users/matt/Library/CloudStorage/GoogleDrive-matt@intelligence.org"
            "/My Drive/~templates/Style templates.gdoc"
        ) == "GoogleDrive:/My Drive/~templates/Style templates.gdoc"

    def test_shared_drives(self) -> None:
        assert rewrite_finder_path(
            "/Users/matt/Library/CloudStorage/GoogleDrive-matt@bellroy.com"
            "/Shared drives/Advertising/Amazon/API/OpenAPI_SponsoredProducts.json"
        ) == (
            "GoogleDrive:/Shared drives/Advertising/Amazon/API"
            "/OpenAPI_SponsoredProducts.json"
        )

    def test_account_is_dropped_whichever_it_is(self) -> None:
        for account in (
            "matt@bellroy.com",
            "matt@intelligence.org",
            "matthew.fallshaw@gmail.com",
        ):
            assert rewrite_finder_path(
                "/Users/matt/Library/CloudStorage/GoogleDrive-%s/My Drive/f" % account
            ) == "GoogleDrive:/My Drive/f"

    def test_drive_root_itself(self) -> None:
        assert rewrite_finder_path(
            "/Users/matt/Library/CloudStorage/GoogleDrive-matt@bellroy.com/My Drive/"
        ) == "GoogleDrive:/My Drive/"

    def test_other_cloudstorage_providers_left_alone(self) -> None:
        assert rewrite_finder_path(
            "/Users/matt/Library/CloudStorage/OneDrive-Personal/file"
        ) == "~/Library/CloudStorage/OneDrive-Personal/file"


class TestUnaffectedPaths:
    def test_root_level_path(self) -> None:
        assert rewrite_finder_path("/etc/hosts") == "/etc/hosts"

    def test_empty_string(self) -> None:
        assert rewrite_finder_path("") == ""
