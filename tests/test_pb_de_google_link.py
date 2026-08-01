"""Tests for pb-de-google-link's Google redirect-link extraction."""

from conftest import load_script

mod = load_script("pb-de-google-link")
is_google_link = mod.is_google_link
de_google_link = mod.de_google_link

# The three worked examples from the original Ruby script's comments.
LESSWRONG_LINK = (
    "https://www.google.com/url?q=http://lesswrong.com/lw/jg/planning_fallacy/"
    "&sa=U&ei=G6ulUf-LComYqAHbuIDQCQ&ved=0CAcQFjAA&client=internal-uds-cse"
    "&usg=AFQjCNFnb1OtVL1uuIiuvTnjaqOaqsraxQ"
)
WIKIPEDIA_LINK = (
    "https://www.google.com.au/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja"
    "&ved=0CDAQFjAA&url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FPlanning_fallacy"
    "&ei=_qulUbTqOMmCiQfbx4CYCw&usg=AFQjCNGFtR1K-hSLR-8aeW0EowOGhDcuSQ"
    "&sig2=NXIWMQfEp9nMCDLgSwLuTw&bvm=bv.47008514,d.aGc"
)
GIVEDIRECTLY_LINK = (
    "https://www.google.com.au/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja"
    "&uact=8&ved=0ahUKEwiZsbLPsdzJAhWDIqYKHZhLBqgQFgglMAA"
    "&url=https%3A%2F%2Fwww.givedirectly.org%2F"
    "&usg=AFQjCNFSnkTpUyRj51TbStjpwPw_dRa3aQ&sig2=ReCY5wIG7CbCuYM_ajaJtA"
)


class TestIsGoogleLink:
    def test_lesswrong_example(self) -> None:
        assert is_google_link(LESSWRONG_LINK)

    def test_wikipedia_example(self) -> None:
        assert is_google_link(WIKIPEDIA_LINK)

    def test_givedirectly_example(self) -> None:
        assert is_google_link(GIVEDIRECTLY_LINK)

    def test_plain_url_is_not_a_google_link(self) -> None:
        assert not is_google_link("https://example.com/path")

    def test_google_homepage_is_not_a_google_link(self) -> None:
        assert not is_google_link("https://www.google.com/")

    def test_empty_string(self) -> None:
        assert not is_google_link("")


class TestDeGoogleLink:
    def test_q_param_destination(self) -> None:
        assert (
            de_google_link(LESSWRONG_LINK)
            == "http://lesswrong.com/lw/jg/planning_fallacy/"
        )

    def test_url_param_destination_wikipedia(self) -> None:
        assert (
            de_google_link(WIKIPEDIA_LINK)
            == "http://en.wikipedia.org/wiki/Planning_fallacy"
        )

    def test_url_param_destination_givedirectly(self) -> None:
        assert de_google_link(GIVEDIRECTLY_LINK) == "https://www.givedirectly.org/"

    def test_strips_surrounding_whitespace(self) -> None:
        assert (
            de_google_link(f"  {GIVEDIRECTLY_LINK}  \n")
            == "https://www.givedirectly.org/"
        )

    def test_url_param_preferred_over_q_when_both_present(self) -> None:
        link = (
            "https://www.google.com/url?q=http://example.com/search-terms"
            "&url=http://example.com/destination&sig=xyz"
        )
        assert de_google_link(link) == "http://example.com/destination"

    def test_falls_back_to_regex_when_query_parse_finds_nothing(self) -> None:
        # "url=" only appears as a substring of another param's value here,
        # so parse_qs won't find a "url" or "q" key with an http(s) value -
        # the regex fallback still finds the embedded destination.
        link = (
            "https://www.google.com/url?blah=1"
            "&nested=xurl=http://example.com/path&more=2"
        )
        assert de_google_link(link) == "http://example.com/path"
