"""Tests for pb-de-redirect-link's redirect-following logic.

No real network calls: the HTTP fetch step is always injected or, for
`fetch_headers` itself, monkeypatched at the urllib opener level.
"""

from __future__ import annotations

from email.message import Message
from typing import TYPE_CHECKING, NoReturn

import pytest
from conftest import load_script

if TYPE_CHECKING:
    from urllib.request import Request

from urllib.error import HTTPError, URLError

mod = load_script("pb-de-redirect-link")


def http_error(url: str, code: int, reason: str) -> HTTPError:
    """Build an HTTPError with no headers, as a 4xx/5xx from our fakes has."""
    return HTTPError(url, code, reason, Message(), None)


@pytest.fixture
def messages(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Capture what the script would have notified, instead of notifying."""
    captured: list[str] = []

    def fake_notify(message: str, **_kwargs: object) -> None:
        captured.append(message)

    monkeypatch.setattr(mod, "notify", fake_notify)
    return captured


class FakeResponse:
    """Stand-in for the object `_opener.open(...)` returns."""

    def __init__(self, status: int, location: str | None = None) -> None:
        self.status = status
        self.headers = {"Location": location} if location else {}

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *exc_info: object) -> bool:
        return False


class FakeOpener:
    """Stand-in for `mod._opener`: pops canned outcomes off a queue."""

    def __init__(self, outcomes: list[FakeResponse | HTTPError]) -> None:
        self._outcomes = list(outcomes)
        self.calls: list[tuple[str, str]] = []
        self.timeouts: list[float | None] = []

    def open(self, request: Request, timeout: float | None = None) -> FakeResponse:
        self.calls.append((request.get_method(), request.full_url))
        self.timeouts.append(timeout)
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class TestIsUrl:
    def test_https(self) -> None:
        assert mod.is_url("https://example.com")

    def test_http(self) -> None:
        assert mod.is_url("http://example.com")

    def test_strips_surrounding_whitespace(self) -> None:
        assert mod.is_url("  http://example.com\n")

    def test_plain_text_is_not_a_url(self) -> None:
        assert not mod.is_url("just some text")

    def test_non_http_scheme_is_not_a_url(self) -> None:
        assert not mod.is_url("ftp://example.com")

    def test_empty_string(self) -> None:
        assert not mod.is_url("")


class TestFetchHeaders:
    """Exercise fetch_headers by faking the urllib opener it calls."""

    def test_head_success_returns_status_and_location(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        opener = FakeOpener([FakeResponse(200)])
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (200, None)
        assert opener.calls == [("HEAD", "http://example.com")]

    def test_head_redirect_returns_location(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        opener = FakeOpener([FakeResponse(302, "http://example.com/dest")])
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (302, "http://example.com/dest")

    def test_head_405_falls_back_to_get(self, monkeypatch: pytest.MonkeyPatch) -> None:
        opener = FakeOpener(
            [
                http_error("http://example.com", 405, "Not Allowed"),
                FakeResponse(200),
            ]
        )
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (200, None)
        assert [method for method, _ in opener.calls] == ["HEAD", "GET"]

    def test_head_non_405_error_does_not_fall_back(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        opener = FakeOpener([http_error("http://example.com", 403, "Forbidden")])
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (403, None)
        assert [method for method, _ in opener.calls] == ["HEAD"]

    def test_uses_the_urls_own_scheme(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # The old Ruby always spoke plain HTTP on port 80, even for https://
        # URLs. Confirm the request we build carries the real URL through.
        opener = FakeOpener([FakeResponse(200)])
        monkeypatch.setattr(mod, "_opener", opener)

        mod.fetch_headers("https://example.com:8443/secure")

        assert opener.calls == [("HEAD", "https://example.com:8443/secure")]


class TestFollowRedirects:
    def test_no_redirect_returns_original_url(self) -> None:
        def fetch(_url: str) -> tuple[int, str | None]:
            return (200, None)

        assert mod.follow_redirects("http://a", fetch=fetch) == "http://a"

    def test_follows_a_single_redirect(self) -> None:
        def fetch(url: str) -> tuple[int, str | None]:
            return (302, "http://b") if url == "http://a" else (200, None)

        assert mod.follow_redirects("http://a", fetch=fetch) == "http://b"

    def test_follows_a_chain_of_redirects(self) -> None:
        chain: dict[str, tuple[int, str | None]] = {
            "http://a": (301, "http://b"),
            "http://b": (302, "http://c"),
            "http://c": (200, None),
        }

        def fetch(url: str) -> tuple[int, str | None]:
            return chain[url]

        assert mod.follow_redirects("http://a", fetch=fetch) == "http://c"

    def test_resolves_relative_location_header(self) -> None:
        def fetch(url: str) -> tuple[int, str | None]:
            if url == "http://example.com/a":
                return (302, "/b")
            return (200, None)

        result = mod.follow_redirects("http://example.com/a", fetch=fetch)
        assert result == "http://example.com/b"

    def test_redirect_status_without_location_is_treated_as_final(self) -> None:
        def fetch(_url: str) -> tuple[int, str | None]:
            return (302, None)

        assert mod.follow_redirects("http://a", fetch=fetch) == "http://a"

    def test_loop_detection_notifies_and_returns_current(
        self, messages: list[str]
    ) -> None:
        # http://a always redirects back to itself.
        def fetch(_url: str) -> tuple[int, str | None]:
            return (302, "http://a")

        result = mod.follow_redirects("http://a", fetch=fetch)

        assert result == "http://a"
        assert any("looping" in message for message in messages)

    def test_non_web_redirect_target_is_refused(self, messages: list[str]) -> None:
        # A redirect to file:// must not reach the clipboard, even though we
        # never open it: the last reachable http(s) URL is the useful answer.
        def fetch(_url: str) -> tuple[int, str | None]:
            return (302, "file:///etc/passwd")

        result = mod.follow_redirects("http://a", fetch=fetch)

        assert result == "http://a"
        assert any("isn't a web link" in message for message in messages)

    def test_relative_redirect_keeps_the_scheme_it_started_with(self) -> None:
        def fetch(url: str) -> tuple[int, str | None]:
            return (302, "/b") if url == "https://example.com/a" else (200, None)

        assert (
            mod.follow_redirects("https://example.com/a", fetch=fetch)
            == "https://example.com/b"
        )

    def test_hop_limit_notifies_and_returns_last_url(self, messages: list[str]) -> None:
        def fetch(url: str) -> tuple[int, str | None]:
            n = int(url.rsplit("/", 1)[-1])
            return (302, f"http://example.com/{n + 1}")

        result = mod.follow_redirects("http://example.com/0", fetch=fetch, max_hops=3)

        assert result == "http://example.com/3"
        assert any("Gave up" in message for message in messages)

    def test_network_error_notifies_and_returns_current(
        self, messages: list[str]
    ) -> None:
        def fetch(_url: str) -> NoReturn:
            raise URLError("boom")

        result = mod.follow_redirects("http://a", fetch=fetch)

        assert result == "http://a"
        assert any("Couldn't reach" in message for message in messages)


class TestDeRedirectLink:
    def test_strips_whitespace_and_follows_through_fetch_headers(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        opener = FakeOpener(
            [FakeResponse(301, "https://final.example/page"), FakeResponse(200)]
        )
        monkeypatch.setattr(mod, "_opener", opener)

        result = mod.de_redirect_link("  http://short.example/abc\n")

        assert result == "https://final.example/page"
        assert opener.calls[0] == ("HEAD", "http://short.example/abc")
