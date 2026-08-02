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
            rewrite_finder_path("/Users/matt/Dropbox/notes.txt") == "Dropbox:notes.txt"
        )

    def test_dropbox_with_parenthetical_suffix(self) -> None:
        assert (
            rewrite_finder_path("/Users/matt/Dropbox (Personal)/notes.txt")
            == "Dropbox:notes.txt"
        )


class TestGoogleDrive:
    """Google Drive lives under ~/Library/CloudStorage/GoogleDrive-<account>/."""

    def test_my_drive_keeps_the_account(self) -> None:
        """Three accounts are mounted, so "My Drive" alone would be ambiguous."""
        assert rewrite_finder_path(
            "/Users/matt/Library/CloudStorage/GoogleDrive-matt@intelligence.org"
            "/My Drive/~templates/Style templates.gdoc"
        ) == (
            "GoogleDrive-matt@intelligence.org:/My Drive"
            "/~templates/Style templates.gdoc"
        )

    def test_shared_drives_drops_the_account(self) -> None:
        """A shared drive is org-owned; which account reached it is noise."""
        assert rewrite_finder_path(
            "/Users/matt/Library/CloudStorage/GoogleDrive-matt@bellroy.com"
            "/Shared drives/Advertising/Amazon/API/OpenAPI_SponsoredProducts.json"
        ) == (
            "GoogleDrive:/Shared drives/Advertising/Amazon/API"
            "/OpenAPI_SponsoredProducts.json"
        )

    def test_shared_drives_drops_any_account(self) -> None:
        for account in (
            "matt@bellroy.com",
            "matt@intelligence.org",
            "matthew.fallshaw@gmail.com",
        ):
            root = f"/Users/matt/Library/CloudStorage/GoogleDrive-{account}"
            assert (
                rewrite_finder_path(f"{root}/Shared drives/f")
                == "GoogleDrive:/Shared drives/f"
            )

    def test_my_drive_keeps_any_account(self) -> None:
        for account in (
            "matt@bellroy.com",
            "matt@intelligence.org",
            "matthew.fallshaw@gmail.com",
        ):
            assert (
                rewrite_finder_path(
                    f"/Users/matt/Library/CloudStorage/GoogleDrive-{account}/My Drive/f"
                )
                == f"GoogleDrive-{account}:/My Drive/f"
            )

    def test_my_drive_root_itself(self) -> None:
        root = "/Users/matt/Library/CloudStorage/GoogleDrive-matt@bellroy.com"
        assert (
            rewrite_finder_path(f"{root}/My Drive/")
            == "GoogleDrive-matt@bellroy.com:/My Drive/"
        )

    def test_shared_drives_root_itself(self) -> None:
        assert (
            rewrite_finder_path(
                "/Users/matt/Library/CloudStorage/GoogleDrive-matt@bellroy.com"
                "/Shared drives/"
            )
            == "GoogleDrive:/Shared drives/"
        )

    def test_unexpected_root_keeps_the_account(self) -> None:
        """Anything that isn't "Shared drives" is treated as needing the account."""
        assert (
            rewrite_finder_path(
                "/Users/matt/Library/CloudStorage/GoogleDrive-matt@bellroy.com/Other/f"
            )
            == "GoogleDrive-matt@bellroy.com:/Other/f"
        )

    def test_other_cloudstorage_providers_left_alone(self) -> None:
        assert (
            rewrite_finder_path(
                "/Users/matt/Library/CloudStorage/OneDrive-Personal/file"
            )
            == "~/Library/CloudStorage/OneDrive-Personal/file"
        )


class TestUnaffectedPaths:
    def test_root_level_path(self) -> None:
        assert rewrite_finder_path("/etc/hosts") == "/etc/hosts"

    def test_empty_string(self) -> None:
        assert rewrite_finder_path("") == ""
