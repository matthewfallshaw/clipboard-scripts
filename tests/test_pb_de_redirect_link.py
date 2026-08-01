"""Tests for pb-de-redirect-link's redirect-following logic.

No real network calls: the HTTP fetch step is always injected or, for
`fetch_headers` itself, monkeypatched at the urllib opener level.
"""

from urllib.error import HTTPError, URLError

from conftest import load_script

mod = load_script("pb-de-redirect-link")


class FakeResponse:
    """Stand-in for the object `_opener.open(...)` returns."""

    def __init__(self, status: int, location: str = None) -> None:
        self.status = status
        self.headers = {"Location": location} if location else {}

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *exc_info: object) -> bool:
        return False


class FakeOpener:
    """Stand-in for `mod._opener`: pops canned outcomes off a queue."""

    def __init__(self, outcomes: list) -> None:
        self._outcomes = list(outcomes)
        self.calls: list = []

    def open(self, request: object, timeout: float = None) -> FakeResponse:
        self.calls.append((request.get_method(), request.full_url))
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

    def test_head_success_returns_status_and_location(self, monkeypatch) -> None:
        opener = FakeOpener([FakeResponse(200)])
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (200, None)
        assert opener.calls == [("HEAD", "http://example.com")]

    def test_head_redirect_returns_location(self, monkeypatch) -> None:
        opener = FakeOpener([FakeResponse(302, "http://example.com/dest")])
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (302, "http://example.com/dest")

    def test_head_405_falls_back_to_get(self, monkeypatch) -> None:
        opener = FakeOpener(
            [HTTPError("http://example.com", 405, "Not Allowed", {}, None), FakeResponse(200)]
        )
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (200, None)
        assert [method for method, _ in opener.calls] == ["HEAD", "GET"]

    def test_head_non_405_error_does_not_fall_back(self, monkeypatch) -> None:
        opener = FakeOpener([HTTPError("http://example.com", 403, "Forbidden", {}, None)])
        monkeypatch.setattr(mod, "_opener", opener)

        status, location = mod.fetch_headers("http://example.com")

        assert (status, location) == (403, None)
        assert [method for method, _ in opener.calls] == ["HEAD"]

    def test_uses_the_urls_own_scheme(self, monkeypatch) -> None:
        # The old Ruby always spoke plain HTTP on port 80, even for https://
        # URLs. Confirm the request we build carries the real URL through.
        opener = FakeOpener([FakeResponse(200)])
        monkeypatch.setattr(mod, "_opener", opener)

        mod.fetch_headers("https://example.com:8443/secure")

        assert opener.calls == [("HEAD", "https://example.com:8443/secure")]


class TestFollowRedirects:
    def test_no_redirect_returns_original_url(self) -> None:
        result = mod.follow_redirects("http://a", fetch=lambda url: (200, None))
        assert result == "http://a"

    def test_follows_a_single_redirect(self) -> None:
        def fetch(url: str):
            return (302, "http://b") if url == "http://a" else (200, None)

        assert mod.follow_redirects("http://a", fetch=fetch) == "http://b"

    def test_follows_a_chain_of_redirects(self) -> None:
        chain = {
            "http://a": (301, "http://b"),
            "http://b": (302, "http://c"),
            "http://c": (200, None),
        }
        assert mod.follow_redirects("http://a", fetch=lambda url: chain[url]) == "http://c"

    def test_resolves_relative_location_header(self) -> None:
        def fetch(url: str):
            if url == "http://example.com/a":
                return (302, "/b")
            return (200, None)

        result = mod.follow_redirects("http://example.com/a", fetch=fetch)
        assert result == "http://example.com/b"

    def test_redirect_status_without_location_is_treated_as_final(self) -> None:
        result = mod.follow_redirects("http://a", fetch=lambda url: (302, None))
        assert result == "http://a"

    def test_loop_detection_notifies_and_returns_current(self, monkeypatch) -> None:
        messages = []
        monkeypatch.setattr(
            mod, "notify", lambda message, sticky=False: messages.append(message)
        )

        # http://a always redirects back to itself.
        result = mod.follow_redirects("http://a", fetch=lambda url: (302, "http://a"))

        assert result == "http://a"
        assert any("looping" in message for message in messages)

    def test_hop_limit_notifies_and_returns_last_url(self, monkeypatch) -> None:
        messages = []
        monkeypatch.setattr(
            mod, "notify", lambda message, sticky=False: messages.append(message)
        )

        def fetch(url: str):
            n = int(url.rsplit("/", 1)[-1])
            return (302, f"http://example.com/{n + 1}")

        result = mod.follow_redirects(
            "http://example.com/0", fetch=fetch, max_hops=3
        )

        assert result == "http://example.com/3"
        assert any("Gave up" in message for message in messages)

    def test_network_error_notifies_and_returns_current(self, monkeypatch) -> None:
        messages = []
        monkeypatch.setattr(
            mod, "notify", lambda message, sticky=False: messages.append(message)
        )

        def fetch(url: str):
            raise URLError("boom")

        result = mod.follow_redirects("http://a", fetch=fetch)

        assert result == "http://a"
        assert any("Couldn't reach" in message for message in messages)


class TestDeRedirectLink:
    def test_strips_whitespace_and_follows_through_fetch_headers(self, monkeypatch) -> None:
        opener = FakeOpener(
            [FakeResponse(301, "https://final.example/page"), FakeResponse(200)]
        )
        monkeypatch.setattr(mod, "_opener", opener)

        result = mod.de_redirect_link("  http://short.example/abc\n")

        assert result == "https://final.example/page"
        assert opener.calls[0] == ("HEAD", "http://short.example/abc")
